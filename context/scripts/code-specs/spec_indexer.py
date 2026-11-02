# /// script
# dependencies = [
#     "pyyaml>=6.0",
# ]
# ///
#!/usr/bin/env python3
"""Deterministic codebase indexer for the derive-spec workflow.

Zero-LLM extraction of a structural map of a repository so that agents spawned
by the derive-spec workflow spend their token budget on synthesis and judgement
instead of file reads.

Subcommands
-----------
scan   Build <repo>/artefacts/build/repo-index.json and spec-scan.md.
verify Validate that every cited file:line in an index (or in a markdown spec
       document) resolves to an existing line in the repository.

Extraction backends (all deterministic, ~0 LLM tokens) selected via ``--extractors``:
  * auto (default) - probe the toolchain and prefer the richest backend per
              language; provenance is recorded in ``meta.extractors``.
  * Python  - stdlib ``ast``: imports, classes, functions, decorators, route
              registrations (FastAPI/Flask style), constants.
  * TS/JS   - tree-sitter (tsx/typescript/javascript) when available; ast-grep
              rules; the optional ts-morph Node helper; conservative line
              regexes (v1) as the permanent stdlib fallback.
  * Foreign - universal-ctags JSON (Go, Rust, Java, C, C++, Ruby, PHP, Swift).
  * SQL     - CREATE TABLE parsing from migrations.
  * OpenAPI - PyYAML parse of openapi*.yaml/json.
  * Tests   - pytest --collect-only / yarn test --listTests when available:
              test node-ids are candidate feature names.

The index schema is documented in context/skills/analyse-repo.md (§ Consuming repo-index.json).
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - declared in PEP 723 metadata
    yaml = None

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

LANG_BY_SUFFIX: dict[str, str] = {
    ".py": "python",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".js": "javascript",
    ".jsx": "javascript",
    ".mjs": "javascript",
    ".sql": "sql",
}

# Foreign languages handled by the universal-ctags backend (T-015) when available.
FOREIGN_LANG_SUFFIXES: dict[str, str] = {
    ".go": "go",
    ".rs": "rust",
    ".java": "java",
    ".kt": "kotlin",
    ".cs": "csharp",
    ".c": "c",
    ".h": "c",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".hpp": "cpp",
    ".rb": "ruby",
    ".php": "php",
    ".swift": "swift",
}
FOREIGN_LANGS: frozenset[str] = frozenset(FOREIGN_LANG_SUFFIXES.values())
TS_LANGS: tuple[str, ...] = ("typescript", "javascript")

# (relative glob, kind) pairs for the Phase-1 existing-document discovery.
DOC_GLOBS: list[tuple[str, str]] = [
    ("artefacts/product/*.md", "requirements"),
    ("artefacts/product/**/*.md", "requirements"),
    ("artefacts/architecture/*.md", "architecture"),
    ("artefacts/architecture/**/*.md", "architecture"),
    ("artefacts/api/*.md", "api"),
    ("artefacts/design/*.md", "design"),
    ("artefacts/design/**/*.md", "design"),
    ("docs/**/*.md", "docs"),
    ("**/discovery-notes.md", "discovery"),
]

DOC_BASENAME_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"^PRD[-_].*\.md$", re.IGNORECASE), "prd"),
    (re.compile(r"^.*[-_]prd\.md$", re.IGNORECASE), "prd"),
    (re.compile(r"^TSD[-_].*\.md$", re.IGNORECASE), "tsd"),
    (re.compile(r"^.*[-_]tsd\.md$", re.IGNORECASE), "tsd"),
    (re.compile(r"^.*(?:spec).*\.md$", re.IGNORECASE), "spec"),
    (re.compile(r"^README.*\.(?:md|rst|txt)$", re.IGNORECASE), "readme"),
    (re.compile(r"^requirements.*\.(?:md|txt)$", re.IGNORECASE), "requirements"),
    (re.compile(r"^openapi.*\.(?:ya?ml|json)$", re.IGNORECASE), "openapi"),
]

EXCLUDED_DIRS: set[str] = {
    ".git",
    ".hg",
    ".venv",
    "venv",
    ".env",
    "node_modules",
    "dist",
    "out",
    "target",
    "build",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    ".nox",
    "coverage",
    ".idea",
    ".vscode",
    ".DS_Store",
}

ROUTE_METHOD_ATTRS: frozenset[str] = frozenset(
    {"get", "post", "put", "patch", "delete", "options", "head"}
)

_JSX_TAG_RE: re.Pattern[str] = re.compile(r"<([A-Z][A-Za-z0-9_]*)(?=[\s/>])")

# --- TS/JS heuristics --------------------------------------------------------
_TS_IMPORT_NAMED: re.Pattern[str] = re.compile(
    r"^\s*import\s+(?:type\s+)?\{[^}]*\}\s+from\s+['\"]([^'\"]+)['\"]"
)
_TS_IMPORT_DEFAULT: re.Pattern[str] = re.compile(
    r"^\s*import\s+(?:type\s+)?(\w+)\s+from\s+['\"]([^'\"]+)['\"]"
)
_TS_FUNC: re.Pattern[str] = re.compile(
    r"^\s*(?:export\s+|default\s+)*(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)"
)
_TS_ARROW: re.Pattern[str] = re.compile(
    r"^\s*(?:export\s+|default\s+)*const\s+(\w+)\s*(?::[^=]+)?=\s*(?:async\s*)?"
    r"((?:\([^)]*\)|[A-Za-z_$][\w$]*))\s*=>"
)
_TS_CLASS: re.Pattern[str] = re.compile(r"^\s*(?:export\s+|default\s+)*class\s+(\w+)")
_TS_IFACE: re.Pattern[str] = re.compile(r"^\s*(?:export\s+)*interface\s+(\w+)")
_TS_TYPE: re.Pattern[str] = re.compile(r"^\s*(?:export\s+)*type\s+(\w+)\s*=")
_TS_REQUIRE: re.Pattern[str] = re.compile(
    r"^\s*const\s+[\w$]+\s*=\s*require\s*\(\s*['\"]([^'\"]+)['\"]\s*\)"
)

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class Symbol:
    kind: str  # class | function | method | component | interface | type | const
    name: str
    signature: str = ""
    line: int = 0
    decorators: list[str] = field(default_factory=list)
    props: list[str] = field(default_factory=list)

    def to_jsonb(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "name": self.name,
            "signature": self.signature,
            "line": self.line,
            "decorators": self.decorators,
            "props": self.props,
        }


@dataclass
class FileRecord:
    path: str
    language: str
    line_count: int = 0
    symbols: list[Symbol] = field(default_factory=list)
    imports: list[str] = field(default_factory=list)
    extractor: str = ""  # T-015: backend that produced this record (e.g. "tree-sitter")

    def to_jsonb(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "language": self.language,
            "line_count": self.line_count,
            "symbols": [s.to_jsonb() for s in self.symbols],
            "imports": self.imports,
            "extractor": self.extractor,
        }


@dataclass
class ApiEntry:
    method: str
    path: str
    handler: str
    file: str
    line: int = 0

    def to_jsonb(self) -> dict[str, Any]:
        return {
            "method": self.method,
            "path": self.path,
            "handler": self.handler,
            "file": self.file,
            "line": self.line,
        }


@dataclass
class ColumnDef:
    name: str
    type: str = ""

    def to_jsonb(self) -> dict[str, Any]:
        return {"name": self.name, "type": self.type}


@dataclass
class TableDef:
    table: str
    columns: list[ColumnDef] = field(default_factory=list)
    file: str = ""
    line: int = 0

    def to_jsonb(self) -> dict[str, Any]:
        return {
            "table": self.table,
            "columns": [c.to_jsonb() for c in self.columns],
            "file": self.file,
            "line": self.line,
        }


@dataclass
class UiComponent:
    component: str
    file: str
    line: int = 0
    props: list[str] = field(default_factory=list)
    usages: int = 0
    kind: str = "component"

    def to_jsonb(self) -> dict[str, Any]:
        return {
            "component": self.component,
            "file": self.file,
            "line": self.line,
            "props": self.props,
            "usages": self.usages,
            "kind": self.kind,
        }


@dataclass
class TestNode:
    node_id: str
    file: str = ""

    def to_jsonb(self) -> dict[str, Any]:
        return {"node_id": self.node_id, "file": self.file}


@dataclass
class DocRecord:
    path: str
    kind: str = "unknown"

    def to_jsonb(self) -> dict[str, Any]:
        return {"path": self.path, "kind": self.kind}


# ---------------------------------------------------------------------------
# Repository walking
# ---------------------------------------------------------------------------


def rel(repo: Path, path: Path) -> str:
    """Return path relative to the repo root, using forward slashes."""
    return str(path.relative_to(repo)).replace(os.sep, "/")


def language_of(name: str) -> str | None:
    suffix = Path(name).suffix.lower()
    if suffix in LANG_BY_SUFFIX:
        return LANG_BY_SUFFIX[suffix]
    return FOREIGN_LANG_SUFFIXES.get(suffix)


def find_target_files(repo: Path, max_files: int) -> tuple[list[str], list[str], bool]:
    """Return (relative paths, warnings, too_large) for files to index.

    Prefers git-tracked files (respects .gitignore, skips untracked junk).
    Falls back to a bounded os.walk when the repo has no git metadata.
    """
    warnings: list[str] = []
    too_large = False

    try:
        proc = subprocess.run(
            [
                "git",
                "-C",
                str(repo),
                "ls-files",
                "-z",
                "--cached",
                "--others",
                "--exclude-standard",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired):
        proc = None

    if proc is not None and proc.returncode == 0 and proc.stdout:
        raw = proc.stdout.replace("\x00", "\n").split("\n")
        paths = [p for p in raw if p and not Path(p).name.startswith(".")]
    else:
        paths = []
        for root, dirs, files in os.walk(repo):
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
            for fname in files:
                if fname.startswith("."):
                    continue
                p = Path(root) / fname
                rp = rel(repo, p)
                if any(part in EXCLUDED_DIRS for part in p.parts):
                    continue
                paths.append(rp)

    if len(paths) > max_files:
        too_large = True
        warnings.append(
            f"repo scan exceeds max_files={max_files} ({len(paths)} tracked files); "
            "consider scoping with --repo to a subpath"
        )
    return sorted(paths), warnings, too_large


# ---------------------------------------------------------------------------
# Python extraction (stdlib ast)
# ---------------------------------------------------------------------------


def _unparse(node: ast.AST | None) -> str:
    try:
        return ast.unparse(node) if node is not None else ""
    except Exception:  # pragma: no cover - defensive against odd nodes
        return ""


def _decorator_names(decorators: list[ast.expr]) -> list[str]:
    out: list[str] = []
    for dec in decorators:
        text = _unparse(dec).replace("\n", " ").strip()
        out.append(text[:120])
    return out


def _route_from_decorator(dec: ast.expr) -> tuple[str, str] | None:
    """Extract (METHOD, path) from FastAPI/Flask route decorators."""
    if not isinstance(dec, ast.Call):
        return None
    func = dec.func
    if not isinstance(func, ast.Attribute):
        return None
    attr = func.attr
    first = dec.args[0] if dec.args else None
    path = _unparse(first) if isinstance(first, ast.Constant) or first is not None else ""
    path = path.strip().strip("'\"") if path else ""
    if attr in ROUTE_METHOD_ATTRS and path:
        return attr.upper(), path
    if attr == "route" and path:
        methods: list[str] = []
        for kw in dec.keywords:
            if kw.arg == "methods" and isinstance(kw.value, (ast.List, ast.Tuple)):
                for elt in kw.value.elts:
                    if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                        methods.append(elt.value.upper())
        method = methods[0] if methods else "GET"
        return method, path
    return None


def _method_body(owner: str, node: ast.FunctionDef | ast.AsyncFunctionDef) -> Symbol:
    args_text = _unparse(node.args)
    return Symbol(
        kind="method",
        name=f"{owner}.{node.name}",
        signature=f"({args_text})",
        line=node.lineno,
        decorators=_decorator_names(node.decorator_list),
    )


def analyze_python(abs_path: Path, rel_path: str) -> tuple[FileRecord, list[ApiEntry]]:
    """Parse a Python module with stdlib ast; return record plus API routes."""
    record = FileRecord(path=rel_path, language="python", extractor="stdlib.ast")
    api: list[ApiEntry] = []
    try:
        source = abs_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return record, api
    record.line_count = source.count("\n") + 1
    try:
        tree = ast.parse(source, filename=str(abs_path))
    except SyntaxError:
        return record, api

    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                record.imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            record.imports.append(node.module)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            record.symbols.append(
                Symbol(
                    kind="function",
                    name=node.name,
                    signature=f"({_unparse(node.args)})",
                    line=node.lineno,
                    decorators=_decorator_names(node.decorator_list),
                )
            )
            for dec in node.decorator_list:
                route = _route_from_decorator(dec)
                if route:
                    api.append(ApiEntry(route[0], route[1], node.name, rel_path, node.lineno))
        elif isinstance(node, ast.ClassDef):
            record.symbols.append(
                Symbol(kind="class", name=node.name, signature="", line=node.lineno)
            )
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    record.symbols.append(_method_body(node.name, item))
                    for dec in item.decorator_list:
                        route = _route_from_decorator(dec)
                        if route:
                            api.append(
                                ApiEntry(
                                    route[0],
                                    route[1],
                                    f"{node.name}.{item.name}",
                                    rel_path,
                                    item.lineno,
                                )
                            )
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id.isupper():
                    record.symbols.append(
                        Symbol(kind="const", name=target.id, signature="", line=node.lineno)
                    )
        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and node.target.id.isupper():
                record.symbols.append(
                    Symbol(kind="const", name=node.target.id, signature="", line=node.lineno)
                )
    return record, api


# ---------------------------------------------------------------------------
# TypeScript / JavaScript extraction (v1 line heuristics; tree-sitter later)
# ---------------------------------------------------------------------------


def _destructured_props(signature: str) -> list[str]:
    """Extract prop names from a destructured parameter list, e.g. `({a, b}: Props)`."""
    m = re.match(r"^\s*\(\s*\{(.*?)\}", signature, re.DOTALL)
    if not m:
        return []
    names: list[str] = []
    for part in m.group(1).split(","):
        name = re.split(r"[:=]", part.strip(), maxsplit=1)[0].strip().strip("?")
        if re.fullmatch(r"[A-Za-z_$][A-Za-z0-9_$]*", name or ""):
            names.append(name)
    return names


def _is_component(name: str, kind: str) -> bool:
    return bool(re.match(r"^[A-Z]", name)) and kind in ("function", "const_arrow", "class")


def analyze_tsjs(abs_path: Path, rel_path: str, language: str) -> tuple[FileRecord, list[str]]:
    """Return record plus jsx-tag usage list for UI aggregation."""
    record = FileRecord(path=rel_path, language=language, extractor="stdlib.regex")
    usages: list[str] = []
    try:
        lines = abs_path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return record, usages
    record.line_count = len(lines)

    for lineno, raw in enumerate(lines, start=1):
        stripped = raw.strip()
        if not stripped or stripped.startswith(("//", "/*", "*")):
            continue

        m = _TS_IMPORT_NAMED.match(raw)
        if m:
            record.imports.append(m.group(1))
            continue
        m = _TS_IMPORT_DEFAULT.match(raw)
        if m:
            record.imports.append(m.group(2))
            continue
        if stripped.startswith("import "):
            m = re.match(r"^\s*import\s+['\"]([^'\"]+)['\"]", raw)
            if m:
                record.imports.append(m.group(1))
            continue
        m = _TS_REQUIRE.match(raw)
        if m:
            record.imports.append(m.group(1))
            continue

        m = _TS_FUNC.match(raw)
        if m:
            record.symbols.append(
                Symbol(
                    kind="function",
                    name=m.group(1),
                    signature=f"({m.group(2).strip()})",
                    line=lineno,
                )
            )
            continue
        m = _TS_ARROW.match(raw)
        if m:
            params = m.group(2).strip()
            sig = params if params.startswith("(") else f"({params})"
            record.symbols.append(
                Symbol(
                    kind="const_arrow",
                    name=m.group(1),
                    signature=sig,
                    line=lineno,
                    props=_destructured_props(sig),
                )
            )
            continue
        m = _TS_CLASS.match(raw)
        if m:
            record.symbols.append(Symbol(kind="class", name=m.group(1), line=lineno))
            continue
        m = _TS_IFACE.match(raw)
        if m:
            record.symbols.append(Symbol(kind="interface", name=m.group(1), line=lineno))
            continue
        m = _TS_TYPE.match(raw)
        if m:
            record.symbols.append(Symbol(kind="type", name=m.group(1), line=lineno))
            continue

    for lineno, raw in enumerate(lines, start=1):
        for tag in _JSX_TAG_RE.findall(raw):
            usages.append(tag)

    # props for component consts/functions (from earlier pass)
    for sym in record.symbols:
        if _is_component(sym.name, sym.kind) and sym.kind in ("function", "const_arrow"):
            if not sym.props:
                sym.props = _destructured_props(sym.signature)
    return record, usages


# ---------------------------------------------------------------------------
# Backend selection (T-015): --extractors flag, probing, provenance
# ---------------------------------------------------------------------------


EXTRACTOR_CHOICES: tuple[str, ...] = (
    "auto",
    "stdlib",
    "ctags",
    "tree-sitter",
    "ast-grep",
    "ts-morph",
)

# Which backends can cover which languages.
BACKEND_LANG_COVERAGE: dict[str, tuple[str, ...]] = {
    "ctags": ("python", *TS_LANGS, *FOREIGN_LANGS),
    "tree-sitter": TS_LANGS,
    "ast-grep": TS_LANGS,
    "ts-morph": TS_LANGS,
    "stdlib": ("python", *TS_LANGS, "sql"),
}

_EXTRACTOR_LABEL: dict[str, str] = {
    "stdlib.ast": "stdlib ast (Python)",
    "stdlib.regex": "regex heuristics (TS/JS)",
    "stdlib.sql": "SQL CREATE TABLE parser",
    "ctags": "universal-ctags JSON",
    "tree-sitter": "tree-sitter (language pack)",
    "ast-grep": "ast-grep rules",
    "ts-morph": "ts-morph (Node)",
    "none": "no backend for language",
}


def _cmd_ok(cmd: list[str], cwd: Path, timeout: int = 20) -> bool:
    try:
        proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout)
        return proc.returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def probe_backends(repo: Path) -> dict[str, bool]:
    """Report which external extractors are available. Every probe is wrapped; never raises.

    tree-sitter is provided on demand via
    ``uv run --with tree-sitter --with tree-sitter-language-pack``.
    """
    out: dict[str, bool] = {}
    out["ctags"] = _cmd_ok(["ctags", "--version"], repo)
    out["ast-grep"] = _cmd_ok(["ast-grep", "--version"], repo) or _cmd_ok(
        ["sg", "--version"], repo
    )
    out["ts-morph"] = _cmd_ok(["node", "-e", "require.resolve('ts-morph')"], repo)
    try:
        import tree_sitter_language_pack  # type: ignore  # noqa: F401

        out["tree-sitter"] = True
    except ImportError:
        out["tree-sitter"] = False
    return out


def _likely_backend(lang: str, avail: dict[str, bool]) -> tuple[str, str]:
    """Auto-mode per-language choice: (backend, reason)."""
    if lang == "python":
        return "stdlib.ast", "stdlib ast handles routes/decorators/API — richest for Python"
    if lang in TS_LANGS:
        if avail["tree-sitter"]:
            return "tree-sitter", "tree-sitter AST is the richest TS/TSX backend"
        if avail["ast-grep"]:
            return "ast-grep", "ast-grep rules (tree-sitter unavailable)"
        if avail["ts-morph"]:
            return "ts-morph", "ts-morph helper (tree-sitter/ast-grep unavailable)"
        return "stdlib.regex", "no AST backend available; regex heuristics"
    if lang in FOREIGN_LANGS:
        if avail["ctags"]:
            return "ctags", "universal-ctags JSON (no dedicated parser)"
        return "none", f"ctags unavailable — {lang} symbols not extracted"
    if lang == "sql":
        return "stdlib.sql", "SQL CREATE TABLE parser"
    return "none", f"no extractor for {lang}"


def _stdlib_for(lang: str, reason_note: str) -> str:
    if lang == "python":
        return "stdlib.ast"
    if lang in TS_LANGS:
        return "stdlib.regex"
    if lang == "sql":
        return "stdlib.sql"
    return "none"


def resolve_plan(
    choice: str, avail: dict[str, bool], languages: set[str]
) -> tuple[dict[str, str], dict[str, str], list[str], list[str]]:
    """Map each present language to an extractor.

    Returns (plan, reasons, errors, warnings). A non-auto selection of an
    unavailable backend is an error (the CLI exits non-zero), except ts-morph
    which degrades quietly by design.
    """
    plan: dict[str, str] = {}
    reasons: dict[str, str] = {}
    errors: list[str] = []
    warnings: list[str] = []

    if choice == "auto":
        for lang in sorted(languages):
            plan[lang], reasons[lang] = _likely_backend(lang, avail)
        return plan, reasons, errors, warnings

    if choice == "stdlib":
        for lang in sorted(languages):
            plan[lang] = _stdlib_for(lang, "")
            reasons[lang] = "explicit --extractors stdlib"
        return plan, reasons, errors, warnings

    if choice not in BACKEND_LANG_COVERAGE:
        errors.append(f"unknown extractor: {choice}")
        return plan, reasons, errors, warnings

    if not avail[choice]:
        if choice == "ts-morph":
            warnings.append("ts-morph requested but unavailable; using stdlib fallback")
            for lang in sorted(languages):
                plan[lang] = _stdlib_for(lang, "")
                reasons[lang] = "ts-morph unavailable; stdlib fallback"
            return plan, reasons, errors, warnings
        errors.append(f"selected extractor '{choice}' is not available on this machine")
        return plan, reasons, errors, warnings

    for lang in sorted(languages):
        if lang in BACKEND_LANG_COVERAGE[choice]:
            plan[lang] = choice
            reasons[lang] = f"explicit --extractors {choice}"
        else:
            plan[lang] = _stdlib_for(lang, "")
            reasons[lang] = f"{choice} does not cover {lang}; stdlib fallback"
    return plan, reasons, errors, warnings


def _extractor_meta(
    avail: dict[str, bool], plan: dict[str, str], reasons: dict[str, str]
) -> dict[str, dict[str, Any]]:
    tools = ("ctags", "tree-sitter", "ast-grep", "ts-morph")
    meta: dict[str, dict[str, Any]] = {}
    for tool in tools:
        used_langs = [lang for lang, backend in plan.items() if backend == tool]
        meta[tool] = {
            "available": avail[tool],
            "used": bool(used_langs),
            "reason": "; ".join(reasons.get(lang, "") for lang in sorted(used_langs))
            if used_langs
            else "not selected",
        }
    meta["stdlib"] = {
        "available": True,
        "used": any(b.startswith("stdlib") for b in plan.values()),
        "reason": "zero-dependency fallback tier (stdlib ast + regex + PyYAML + SQL heuristics)",
    }
    return meta


def _ctags_kind(kind: str) -> str:
    k = (kind or "").lower()
    mapping = {
        "function": "function",
        "func": "function",
        "class": "class",
        "struct": "class",
        "trait": "class",
        "enum": "class",
        "interface": "interface",
        "method": "method",
        "alias": "type",
        "typedef": "type",
        "type": "type",
        "constant": "const",
    }
    return mapping.get(k, "const" if k in ("variable", "field", "member", "property") else k)


def analyze_ctags(abs_path: Path, rel_path: str, language: str) -> FileRecord:
    """universal-ctags JSON backend (primary for languages without a dedicated parser)."""
    record = FileRecord(path=rel_path, language=language, extractor="ctags")
    try:
        source = abs_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return record
    record.line_count = source.count("\n") + 1
    proc = subprocess.run(
        ["ctags", "--output-format=json", "--fields=+nKS", str(abs_path)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if proc.returncode != 0 or not proc.stdout:
        return record
    seen: set[tuple[str, int, str]] = set()
    for raw in proc.stdout.splitlines():
        raw = raw.strip()
        if not raw.startswith("{"):
            continue
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if not isinstance(data, dict) or data.get("_type") != "tag":
            continue
        raw_kind = str(data.get("kind", ""))
        if raw_kind in ("property",):  # interface-member noise; skip
            continue
        name = data.get("name")
        line = data.get("line")
        if not name or not isinstance(line, int) or line <= 0:
            continue
        kind = _ctags_kind(raw_kind)
        if kind == "method" and data.get("scope"):
            name = f"{data['scope']}.{name}"
        key = (name, line, kind)
        if key in seen:
            continue
        seen.add(key)
        sig = ""
        pattern = data.get("pattern") or ""
        if kind in ("function", "method", "const") and pattern:
            m = re.search(r"\(([^)]*)\)", pattern)
            if m:
                sig = f"({m.group(1)})"
        record.symbols.append(Symbol(kind=kind, name=str(name), signature=sig, line=line))
    return record


_TS_PACK_LANG: dict[str, str] = {
    ".ts": "typescript",
    ".tsx": "tsx",
    ".js": "javascript",
    ".jsx": "jsx",
    ".mjs": "javascript",
}


def analyze_tsjs_treesitter(
    abs_path: Path, rel_path: str, language: str
) -> tuple[FileRecord, list[str]]:
    """Real-AST pass for TS/TSX via tree-sitter. Richer than the regex backend:
    multiline destructured props, JSX usage counts, decorators, named imports.

    Requires tree-sitter, provided on demand via
    ``uv run --with tree-sitter --with tree-sitter-language-pack``.
    """
    from tree_sitter_language_pack import get_parser  # type: ignore

    record = FileRecord(path=rel_path, language=language, extractor="tree-sitter")
    usages: list[str] = []
    try:
        source = abs_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return record, usages
    record.line_count = source.count("\n") + 1
    pack_key = _TS_PACK_LANG.get(
        abs_path.suffix.lower(), "typescript" if language == "typescript" else "javascript"
    )
    parser = get_parser(pack_key)
    tree = parser.parse(bytes(source, "utf-8"))

    def node_line(node: Any) -> int:
        return node.start_point[0] + 1

    def field_text(node: Any, field: str) -> str:
        child = node.child_by_field_name(field)
        return child.text.decode("utf-8", errors="replace") if child is not None else ""

    def decorators_before(node: Any) -> list[str]:
        parent = node.parent
        if parent is None:
            return []
        out: list[str] = []
        for child in parent.named_children:
            if child == node:
                break
            if child.type == "decorator":
                out.append(child.text.decode("utf-8", errors="replace")[:120])
        return out

    def prop_names_from_object(obj: Any) -> list[str]:
        names: list[str] = []
        for child in obj.named_children:
            if child.type == "shorthand_property_identifier_pattern":
                names.append(child.text.decode("utf-8", errors="replace"))
            elif child.type == "object_assignment_pattern":
                first = child.named_children[0] if child.named_children else None
                if first is not None:
                    names.append(first.text.decode("utf-8", errors="replace"))
            elif child.type == "pair_pattern":
                key = child.child_by_field_name("key")
                if key is not None:
                    names.append(key.text.decode("utf-8", errors="replace"))
        return names

    def params_from(fn_params: Any) -> tuple[str, list[str]]:
        """Return (signature, destructured props) from a formal_parameters node."""
        if fn_params is None:
            return "", []
        sig = fn_params.text.decode("utf-8", errors="replace").replace("\n", " ")
        props: list[str] = []
        for child in fn_params.named_children:
            for sub in child.named_children:
                if sub.type == "object_pattern":
                    props.extend(prop_names_from_object(sub))
        return sig, props

    def walk(node: Any, class_owner: str | None = None) -> None:
        ntype = node.type
        if ntype == "import_statement":
            module = ""
            for child in node.named_children:
                if child.type == "string":
                    frag = child.child_by_field_name("text")
                    if frag is None and child.named_children:
                        frag = child.named_children[0]
                    if frag is not None:
                        module = frag.text.decode("utf-8", errors="replace")
            if module and module not in record.imports:
                record.imports.append(module)
            for child in node.named_children:
                if child.type == "named_imports":
                    for spec in child.named_children:
                        if spec.type == "import_specifier":
                            name = spec.child_by_field_name("name")
                            if name is not None:
                                record.imports.append(
                                    name.text.decode("utf-8", errors="replace")
                                )
            return
        if ntype in ("program", "export_statement"):
            for child in node.named_children:
                walk(child, class_owner)
            return
        if ntype == "function_declaration":
            name = field_text(node, "name")
            params = node.child_by_field_name("parameters")
            sig, props = params_from(params)
            record.symbols.append(
                Symbol(
                    kind="function",
                    name=name,
                    signature=sig,
                    line=node_line(node),
                    decorators=decorators_before(node),
                    props=props,
                )
            )
            # fall through: walk the body so JSX inside functions is captured
        if ntype == "class_declaration":
            name = field_text(node, "name")
            record.symbols.append(
                Symbol(
                    kind="class",
                    name=name,
                    line=node_line(node),
                    decorators=decorators_before(node),
                )
            )
            for child in node.named_children:
                walk(child, name)
            return
        if ntype == "method_definition":
            mname = field_text(node, "name")
            mparams = node.child_by_field_name("parameters")
            msig, _ = params_from(mparams)
            display = f"{class_owner}.{mname}" if class_owner else mname
            record.symbols.append(
                Symbol(
                    kind="method",
                    name=display,
                    signature=msig,
                    line=node_line(node),
                    decorators=decorators_before(node),
                )
            )
            # fall through to walk the method body (JSX)
        if ntype == "interface_declaration":
            record.symbols.append(
                Symbol(kind="interface", name=field_text(node, "name"), line=node_line(node))
            )
            return
        if ntype == "type_alias_declaration":
            record.symbols.append(
                Symbol(kind="type", name=field_text(node, "name"), line=node_line(node))
            )
            return
        if ntype == "lexical_declaration":
            for decl in node.named_children:
                if decl.type != "variable_declarator":
                    continue
                dname = decl.child_by_field_name("name")
                value = decl.child_by_field_name("value")
                name = (
                    dname.text.decode("utf-8", errors="replace") if dname is not None else ""
                )
                if value is not None and value.type in ("arrow_function", "function_expression"):
                    params = value.child_by_field_name("parameters")
                    sig, props = params_from(params)
                    record.symbols.append(
                        Symbol(
                            kind="const_arrow",
                            name=name,
                            signature=sig,
                            line=node_line(decl),
                            props=props,
                            decorators=decorators_before(decl),
                        )
                    )
                else:
                    record.symbols.append(Symbol(kind="const", name=name, line=node_line(decl)))
            # fall through to walk the initializers (arrow bodies contain JSX)
        if ntype in ("jsx_opening_element", "jsx_self_closing_element"):
            first = node.named_children[0] if node.named_children else None
            if first is not None:
                tag = first.text.decode("utf-8", errors="replace")
                if first.type == "member_expression":
                    tag = tag.split(".")[-1]
                usages.append(tag)
            # keep walking: opening elements can nest further JSX
        for child in node.named_children:
            walk(child, class_owner)
    walk(tree.root_node)
    return record, usages


# ast-grep rule patterns for TS/JS (degraded-mode backend; tree-sitter preferred).
_ASTGREP_PATTERNS: list[tuple[str, str]] = [
    ("function", "function $F($$$PARAMS) { $$$BODY }"),
    ("class", "class $C"),
    ("interface", "interface $I { $$$ }"),
    ("type", "type $T = $V"),
    ("const_arrow", "const $N = ($ARGS) => $$$"),
    ("const_arrow", "const $N = $ARGS => $$$"),
]
_ASTGREP_KIND_RE: dict[str, re.Pattern[str]] = {
    "function": re.compile(r"function\s+(\w+)"),
    "class": re.compile(r"class\s+(\w+)"),
    "interface": re.compile(r"interface\s+(\w+)"),
    "type": re.compile(r"type\s+(\w+)"),
    "const_arrow": re.compile(
        r"const\s+(\w+)\s*=\s*(?:async\s*)?(?:\(([^)]*)\)|([A-Za-z_$][\w$]*))\s*=>"
    ),
}
_ASTGREP_LANG_FLAG: dict[str, str] = {
    ".ts": "ts",
    ".tsx": "tsx",
    ".js": "javascript",
    ".jsx": "jsx",
    ".mjs": "javascript",
}


def analyze_tsjs_astgrep(
    abs_path: Path, rel_path: str, language: str
) -> tuple[FileRecord, list[str]]:
    """Rule-driven TS/JS pass via ast-grep, used when tree-sitter is unavailable."""
    record = FileRecord(path=rel_path, language=language, extractor="ast-grep")
    usages: list[str] = []
    try:
        source = abs_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return record, usages
    record.line_count = source.count("\n") + 1
    lang_flag = _ASTGREP_LANG_FLAG.get(
        abs_path.suffix.lower(), "ts" if language == "typescript" else "javascript"
    )
    seen: set[tuple[str, str]] = set()
    for kind, pattern in _ASTGREP_PATTERNS:
        proc = subprocess.run(
            ["ast-grep", "run", "--lang", lang_flag, "-p", pattern, str(abs_path), "--json"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if proc.returncode != 0 or not proc.stdout:
            continue
        try:
            matches = json.loads(proc.stdout)
        except json.JSONDecodeError:
            continue
        if not isinstance(matches, list):
            continue
        for match in matches:
            text = match.get("text") or "" if isinstance(match, dict) else ""
            if not text:
                continue
            first_line = text.splitlines()[0]
            rm = _ASTGREP_KIND_RE[kind].search(first_line)
            if not rm:
                continue
            line = 0
            rng = match.get("range") or {}
            start = (rng.get("start") or {}) if isinstance(rng, dict) else {}
            if isinstance(start, dict) and isinstance(start.get("line"), int):
                line = start["line"] + 1
            key = (kind, rm.group(1))
            if key in seen:
                continue
            seen.add(key)
            sig = ""
            props: list[str] = []
            if kind == "function":
                m = re.search(r"\(([^)]*)\)", first_line)
                if m:
                    sig = f"({m.group(1).strip()})"
                props = _destructured_props(sig)
            elif kind == "const_arrow":
                sig = f"({rm.group(2) or rm.group(3) or ''})"
                props = _destructured_props(sig)
            record.symbols.append(
                Symbol(kind=kind, name=rm.group(1), signature=sig, line=line, props=props)
            )

    # JSX usage via the cheap line scan (ast-grep has no reliable JSX pattern set).
    for raw in source.splitlines():
        for tag in _JSX_TAG_RE.findall(raw):
            usages.append(tag)
    return record, usages


def analyze_tsjs_tsmorph(
    abs_path: Path, rel_path: str, language: str, helper: Path
) -> tuple[FileRecord, list[str]]:
    """Optional Node/ts-morph backend; skipped quietly when node or ts-morph is absent."""
    record = FileRecord(path=rel_path, language=language, extractor="ts-morph")
    usages: list[str] = []
    try:
        source = abs_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return record, usages
    record.line_count = source.count("\n") + 1
    proc = subprocess.run(
        ["node", str(helper), str(abs_path)],
        capture_output=True,
        text=True,
        timeout=60,
    )
    if proc.returncode != 0 or not proc.stdout:
        return record, usages
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return record, usages
    record.imports.extend(data.get("imports", []))
    for sym in data.get("symbols", []):
        if not isinstance(sym, dict):
            continue
        record.symbols.append(
            Symbol(
                kind=str(sym.get("kind", "const")),
                name=str(sym.get("name", "")),
                signature=str(sym.get("signature", "")),
                line=int(sym.get("line", 0) or 0),
                decorators=list(sym.get("decorators", [])),
                props=list(sym.get("props", [])),
            )
        )
    usages.extend(str(tag) for tag in data.get("usages", []))
    return record, usages


# ---------------------------------------------------------------------------
# SQL extraction (migrations)
# ---------------------------------------------------------------------------

_SQL_CREATE: re.Pattern[str] = re.compile(
    r"^\s*CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([`\"\w.]+)\s*\(",
    re.IGNORECASE,
)
_SQL_SKIP_COLUMN = re.compile(
    r"^\s*(?:PRIMARY\s+KEY|FOREIGN\s+KEY|UNIQUE|CONSTRAINT|CHECK\s*\(|REFERENCES|"
    r"INDEX|COMMENT|ON\s+DELETE|ON\s+UPDATE|NOT\s+DEFERRABLE|EXCLUDE)",
    re.IGNORECASE,
)


def analyze_sql(abs_path: Path, rel_path: str) -> list[TableDef]:
    tables: list[TableDef] = []
    try:
        lines = abs_path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return tables

    current: TableDef | None = None
    depth = 0
    for lineno, raw in enumerate(lines, start=1):
        m = _SQL_CREATE.match(raw)
        if m:
            current = TableDef(table=m.group(1).strip('`"'), file=rel_path, line=lineno)
            depth = raw.count("(") - raw.count(")")
            tables.append(current)
            continue
        if current is None:
            continue
        if ";" in raw or depth <= 0:
            depth = 0
            current = None
            continue
        stripped = raw.strip().rstrip(",")
        if not stripped or _SQL_SKIP_COLUMN.match(raw):
            continue
        cm = re.match(r"^([`\"\w]+)\s+([^\s,]+.*?)\s*$", stripped)
        if cm:
            current.columns.append(
                ColumnDef(name=cm.group(1).strip('`"'), type=cm.group(2).strip())
            )
    return tables


# ---------------------------------------------------------------------------
# Test inventory (candidate features at ~0 tokens)
# ---------------------------------------------------------------------------


def _run(cmd: list[str], cwd: Path, timeout: int = 60) -> str:
    try:
        proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout)
        return proc.stdout
    except (OSError, subprocess.TimeoutExpired):
        return ""


def collect_tests(repo: Path) -> tuple[list[str], list[str]]:
    """Return (test node-ids, warnings). Best effort; never fails the scan."""
    node_ids: list[str] = []
    warnings: list[str] = []

    pytest_markers = [(repo / "pytest.ini").exists(), (repo / "pyproject.toml").exists()]
    if any(pytest_markers):
        out = _run(["python3", "-m", "pytest", "--collect-only", "-q"], repo)
        if out:
            for line in out.splitlines():
                line = line.strip()
                if (
                    "::" in line
                    and not line.startswith("=")
                    and not line.lower().startswith(("no tests", "warning"))
                ):
                    node_ids.append(line)
        if node_ids:
            warnings.append(f"pytest: {len(node_ids)} collected (py3)")
        else:
            out_uv = _run(
                ["uv", "run", "--no-sync", "python", "-m", "pytest", "--collect-only", "-q"], repo
            )
            for line in out_uv.splitlines():
                line = line.strip()
                if (
                    "::" in line
                    and not line.startswith("=")
                    and not line.lower().startswith(("no tests", "warning"))
                ):
                    node_ids.append(line)
            if node_ids:
                warnings.append(f"pytest: {len(node_ids)} collected (uv)")

    pkg_json = repo / "package.json"
    if pkg_json.exists():
        try:
            pkg = json.loads(pkg_json.read_text(encoding="utf-8"))
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            if "jest" in deps:
                out = _run(["yarn", "--silent", "test", "--listTests"], repo, timeout=90)
                for line in out.splitlines():
                    line = line.strip()
                    if line:
                        node_ids.append(line)
                if out:
                    warnings.append(f"jest: {len(out.splitlines())} test files listed")
        except (OSError, json.JSONDecodeError):
            pass

    return node_ids, warnings


# ---------------------------------------------------------------------------
# Existing document discovery (Phase 1 input)
# ---------------------------------------------------------------------------


def discover_docs(repo: Path) -> list[DocRecord]:
    docs: dict[str, DocRecord] = {}

    def add(path: Path, kind: str) -> None:
        name = rel(repo, path)
        if name not in docs:
            docs[name] = DocRecord(path=name, kind=kind)

    for pattern, kind in DOC_GLOBS:
        try:
            for p in repo.glob(pattern):
                if p.is_file():
                    add(p, kind)
        except OSError:
            continue

    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for fname in files:
            p = Path(root) / fname
            for pattern, kind in DOC_BASENAME_PATTERNS:
                if pattern.match(fname):
                    add(p, kind)
                    break
    return sorted(docs.values(), key=lambda d: d.path)


# ---------------------------------------------------------------------------
# OpenAPI extraction
# ---------------------------------------------------------------------------


def analyze_openapi(docs: list[DocRecord], repo: Path) -> tuple[list[ApiEntry], list[str]]:
    """Parse openapi*.yaml/json documents into API entries + schema names."""
    api: list[ApiEntry] = []
    schemas: list[str] = []
    if yaml is None and any(d.kind == "openapi" for d in docs):
        return api, schemas
    for doc in docs:
        if doc.kind != "openapi":
            continue
        abs_path = repo / doc.path
        try:
            if abs_path.suffix.lower() == ".json":
                data = json.loads(abs_path.read_text(encoding="utf-8"))
            else:
                data = yaml.safe_load(abs_path.read_text(encoding="utf-8"))
        except Exception:  # io / yaml / json errors — skip non-conforming docs
            continue
        if not isinstance(data, dict):
            continue
        for path, methods in (data.get("paths") or {}).items():
            if not isinstance(methods, dict):
                continue
            for method, op in methods.items():
                if method.lower() not in ROUTE_METHOD_ATTRS:
                    continue
                op_id = op.get("operationId", "") if isinstance(op, dict) else ""
                api.append(ApiEntry(method.upper(), path, str(op_id), doc.path, 0))
        components = data.get("components") or {}
        schemas_node = components.get("schemas") if isinstance(components, dict) else None
        if isinstance(schemas_node, dict):
            schemas.extend(str(k) for k in schemas_node.keys())
    return api, schemas


# ---------------------------------------------------------------------------
# scan: orchestrate extraction + write index artefacts
# ---------------------------------------------------------------------------

MAX_MAP_ROWS = 300
MAX_API_ROWS = 200
MAX_UI_ROWS = 200
MAX_TEST_ROWS = 200
MAX_SCHEMA_ROWS = 200


def _default_out_dir(repo: Path) -> Path:
    build_dir = repo / "artefacts" / "build"
    return build_dir if build_dir.is_dir() else repo


def render_spec_scan(index: dict[str, Any]) -> str:
    meta = index["meta"]
    out: list[str] = [f"# Spec Scan: {meta['repo']}"]
    out.append(
        f"Generated: {meta['generated_at']} · mode: {meta['mode']} · "
        f"{meta['scanned_files']} files · languages: {', '.join(sorted(meta['languages'])) or 'n/a'}"
    )
    if index["warnings"]:
        out.append("\n## Scan Warnings")
        out.extend(f"- {w}" for w in index["warnings"])

    out.append("\n## Existing Spec Documents")
    if index["docs"]:
        out.append("| Path | Kind |")
        out.append("|---|---|")
        for doc in index["docs"]:
            out.append(f"| `{doc['path']}` | {doc['kind']} |")
    else:
        out.append("None found — baseline will be code-derived only.")

    out.append("\n## Repository Map (symbols)")
    rows = 0
    for file_rec in index["files"]:
        sig = file_rec["symbols"]
        if not sig:
            continue
        labels = ", ".join(
            f"{s['kind']} {s['name']}" + (f"({s['line']})" if s["line"] else "") for s in sig
        )
        rows += 1
        if rows > MAX_MAP_ROWS:
            out.append(f"… {len(index['files']) - rows + 1} further files omitted")
            break
        line_info = f" ({file_rec['line_count']} lines)" if file_rec["line_count"] else ""
        out.append(f"- `{file_rec['path']}`{line_info}: {labels}")

    out.append("\n## API Surface")
    if index["api"]:
        for entry in index["api"][:MAX_API_ROWS]:
            loc = (
                f" @{entry['file']}:{entry['line']}" if entry.get("line") else f" ({entry['file']})"
            )
            handler = f" → {entry['handler']}" if entry["handler"] else ""
            out.append(f"- {entry['method']} `{entry['path']}`{handler}{loc}")
        if len(index["api"]) > MAX_API_ROWS:
            out.append(f"… {len(index['api']) - MAX_API_ROWS} more endpoints")
    else:
        out.append("None detected (no route decorators / OpenAPI docs found).")

    out.append("\n## Data Model")
    if index["schema"]:
        for table in index["schema"][:MAX_SCHEMA_ROWS]:
            loc = (
                f" ({table['file']}:{table['line']})"
                if table.get("line")
                else f" ({table['file']})"
            )
            out.append(
                f"- `{table['table']}`{loc}"
                + (f" — {len(table['columns'])} cols" if table["columns"] else " (openapi schema)")
            )
    else:
        out.append("None detected (no SQL migrations / OpenAPI schemas found).")

    out.append("\n## UI Components")
    if index["ui"]:
        for comp in index["ui"][:MAX_UI_ROWS]:
            props = ", ".join(comp["props"][:12]) if comp["props"] else "-"
            out.append(
                f"- {comp['component']} @`{comp['file']}:{comp['line']}` "
                f"usages={comp['usages']} props=[{props}]"
            )
        if len(index["ui"]) > MAX_UI_ROWS:
            out.append(f"… {len(index['ui']) - MAX_UI_ROWS} more components")
    else:
        out.append("None detected (no TS/JSX component definitions found).")

    out.append("\n## Test Inventory (candidate features)")
    if index["tests"]:
        for node in index["tests"][:MAX_TEST_ROWS]:
            out.append(f"- {node['node_id']}")
        if len(index["tests"]) > MAX_TEST_ROWS:
            out.append(f"… {len(index['tests']) - MAX_TEST_ROWS} more test node-ids")
    else:
        out.append("None collected (no pytest/jest marker detected).")

    out.append(
        "\n---\nGenerated deterministically by `context/scripts/code-specs/spec_indexer.py scan` "
        "(zero LLM tokens). Consume via `repo-index.json`."
    )
    return "\n".join(out) + "\n"


def run_scan(
    repo: Path, mode: str, out_json: Path, max_files: int, verbose: bool, extractors: str = "auto"
) -> int:
    repo = repo.resolve()
    paths, warnings, too_large = find_target_files(repo, max_files)

    languages_present: set[str] = {lang for p in paths if (lang := language_of(p)) is not None}
    avail = probe_backends(repo)
    plan, reasons, errors, plan_warnings = resolve_plan(extractors, avail, languages_present)
    warnings.extend(plan_warnings)
    if errors:
        for error in errors:
            print(f"error: {error}")
        return 2

    records: list[FileRecord] = []
    api: list[ApiEntry] = []
    tables: list[TableDef] = []
    jsx_usage: dict[str, int] = {}
    ui_components: dict[str, UiComponent] = {}
    language_counts: dict[str, int] = {}

    for rel_path in paths:
        abs_path = repo / rel_path
        if not abs_path.is_file():
            continue
        lang = language_of(rel_path)
        if lang is None:
            continue
        language_counts[lang] = language_counts.get(lang, 0) + 1

        backend = plan.get(lang, "stdlib.ast")
        if lang == "python":
            if backend == "ctags":
                records.append(analyze_ctags(abs_path, rel_path, lang))
            else:
                record, api_hits = analyze_python(abs_path, rel_path)
                records.append(record)
                api.extend(api_hits)
        elif lang in TS_LANGS:
            if backend == "tree-sitter":
                record, usages = analyze_tsjs_treesitter(abs_path, rel_path, lang)
            elif backend == "ast-grep":
                record, usages = analyze_tsjs_astgrep(abs_path, rel_path, lang)
            elif backend == "ts-morph":
                helper = Path(__file__).with_name("ts_extract.mjs")
                record, usages = analyze_tsjs_tsmorph(abs_path, rel_path, lang, helper)
            else:  # stdlib.regex (permanent fallback)
                record, usages = analyze_tsjs(abs_path, rel_path, lang)
            records.append(record)
            for tag in usages:
                jsx_usage[tag] = jsx_usage.get(tag, 0) + 1
            for sym in record.symbols:
                if _is_component(sym.name, sym.kind):
                    key = sym.name
                    if key not in ui_components:
                        ui_components[key] = UiComponent(
                            component=key,
                            file=record.path,
                            line=sym.line,
                            props=sym.props,
                            kind=sym.kind,
                        )
        elif lang in FOREIGN_LANGS:
            if backend == "ctags":
                records.append(analyze_ctags(abs_path, rel_path, lang))
            # else: stdlib has no foreign-language parser — skip symbols, keep count
        elif lang == "sql":
            table_hits = analyze_sql(abs_path, rel_path)
            tables.extend(table_hits)

    for comp in ui_components.values():
        comp.usages = jsx_usage.get(comp.component, 0)
    ui = sorted(ui_components.values(), key=lambda c: c.usages, reverse=True)

    docs = discover_docs(repo)
    api_openapi, openapi_schemas = analyze_openapi(docs, repo)
    api.extend(api_openapi)

    test_nodes, test_warnings = collect_tests(repo)
    warnings.extend(test_warnings)

    for schema_name in openapi_schemas:
        tables.append(TableDef(table=schema_name, columns=[], file="", line=0))

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    confidence = (
        "degraded"
        if "none" in plan.values()
        else "regex"
        if any(b == "stdlib.regex" for b in plan.values())
        else "full"
    )
    index: dict[str, Any] = {
        "meta": {
            "repo": repo.name,
            "repo_abs": str(repo),
            "generated_at": generated_at,
            "mode": mode,
            "scanned_files": len(records),
            "languages": language_counts,
            "loc": sum(r.line_count for r in records),
            "scan_too_large": too_large,
            "extractors": _extractor_meta(avail, plan, reasons),
            "confidence": confidence,
        },
        "warnings": warnings,
        "docs": [d.to_jsonb() for d in docs],
        "files": [r.to_jsonb() for r in records],
        "api": [e.to_jsonb() for e in sorted(api, key=lambda e: (e.path, e.method))],
        "schema": [t.to_jsonb() for t in tables],
        "ui": [u.to_jsonb() for u in ui],
        "tests": [TestNode(node_id=n, file=n.split("::")[0]).to_jsonb() for n in test_nodes],
    }

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    out_md = out_json.parent / "spec-scan.md"
    out_md.write_text(render_spec_scan(index), encoding="utf-8")

    print(f"repo-index.json  -> {out_json}")
    print(f"spec-scan.md     -> {out_md}")
    print(
        f"files={len(records)} symbols={sum(len(r.symbols) for r in records)} "
        f"api={len(api)} tables={len(tables)} ui={len(ui)} tests={len(test_nodes)}"
    )
    if verbose:  # pragma: no cover - informational
        for w in warnings:
            print(f"warning: {w}")
    return 0


# ---------------------------------------------------------------------------
# verify: check every cited file:line resolves
# ---------------------------------------------------------------------------

_CITATION_RE: re.Pattern[str] = re.compile(
    r"([\w./\\-]+\.(?:py|ts|tsx|js|jsx|mjs|sql|ya?ml|json)):(\d+)"
)


def _line_text(abs_file: Path, line: int) -> str:
    """Return the text of a specific 1-based line, or '' if out of range."""
    try:
        with open(abs_file, encoding="utf-8", errors="replace") as fh:
            for i, ln in enumerate(fh, 1):
                if i == line:
                    return ln.rstrip("\n")
                if i > line:
                    break
    except OSError:
        return ""
    return ""


def run_verify(
    index_path: Path | None, repo_path: Path, doc_path: Path | None, verbose: bool
) -> int:
    index: dict[str, Any] = {}
    if index_path is not None:
        try:
            index = json.loads(index_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"error: cannot read index {index_path}: {exc}")
            return 2

    repo = repo_path.resolve()
    checked = 0
    failures: list[str] = []

    def check(relative: str, line: int) -> None:
        nonlocal checked
        if not relative:
            return
        abs_file = repo / relative
        if line <= 0:  # e.g. OpenAPI entries without line info — unverifiable, not a failure
            return
        checked += 1
        if not abs_file.is_file():
            failures.append(f"missing file: {relative} (cited at line {line})")
            return
        if not _line_text(abs_file, line):
            failures.append(f"line out of range: {relative}:{line}")

    if doc_path is not None:
        try:
            text = doc_path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"error: cannot read doc {doc_path}: {exc}")
            return 2
        for m in _CITATION_RE.finditer(text):
            check(m.group(1), int(m.group(2)))
    else:
        for file_rec in index.get("files", []):
            for sym in file_rec.get("symbols", []):
                check(file_rec["path"], sym.get("line", 0))
        for entry in index.get("api", []):
            check(entry.get("file", ""), entry.get("line", 0))
        for table in index.get("schema", []):
            check(table.get("file", ""), table.get("line", 0))
        for comp in index.get("ui", []):
            check(comp.get("file", ""), comp.get("line", 0))

    print(
        f"checked {checked} citations "
        f"""({"from " + str(doc_path) if doc_path else "in index"})"""
    )
    if failures:
        for f in sorted(set(failures))[:40]:
            print(f"FAIL  {f}")
        extra = len(set(failures)) - 40
        if extra > 0:
            print(f"… {extra} more failures")
        return 1
    print("OK — all citations resolve")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="spec-indexer",
        description=__doc__.split("\n\n")[0],
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_scan = sub.add_parser("scan", help="build repo-index.json and spec-scan.md")
    p_scan.add_argument("--repo", default=".", help="repo root to index (default: cwd)")
    p_scan.add_argument(
        "--mode",
        choices=["product", "technical", "both"],
        default="both",
        help="derive-spec mode hint recorded in the index (default: both)",
    )
    p_scan.add_argument(
        "--out",
        default=None,
        help="output path for repo-index.json (default: <repo>/artefacts/build/repo-index.json "
        "when artefacts/build exists, else repo root)",
    )
    p_scan.add_argument(
        "--max-files", type=int, default=2000, help="scan size flag (default: 2000)"
    )
    p_scan.add_argument("--verbose", action="store_true", help="print warnings")
    p_scan.add_argument(
        "--extractors",
        choices=list(EXTRACTOR_CHOICES),
        default="auto",
        help="extraction backend: auto probes and prefers the richest per language "
        "(default: auto); stdlib is the zero-dependency fallback tier",
    )

    p_verify = sub.add_parser("verify", help="validate file:line citations")
    p_verify.add_argument(
        "--index",
        default=None,
        help="path to repo-index.json (mutually exclusive intent with --doc)",
    )
    p_verify.add_argument(
        "--doc", default=None, help="markdown spec to citation-check instead of the index"
    )
    p_verify.add_argument(
        "--repo", default=None, help="repo root (default: index meta.repo_abs, else cwd)"
    )
    p_verify.add_argument("--verbose", action="store_true")

    args = parser.parse_args(argv)

    if args.command == "scan":
        out = (
            Path(args.out) if args.out else (_default_out_dir(Path(args.repo)) / "repo-index.json")
        )
        return run_scan(
            Path(args.repo), args.mode, out, args.max_files, args.verbose, args.extractors
        )

    if not args.index and not args.doc:
        parser.error("verify requires --index or --doc")

    index_path = Path(args.index).resolve() if args.index else None
    doc_path = Path(args.doc).resolve() if args.doc else None
    repo_path = Path(args.repo).resolve() if args.repo else None

    if repo_path is None and index_path is not None:
        try:
            meta = json.loads(index_path.read_text(encoding="utf-8")).get("meta", {})
            abs_repo = meta.get("repo_abs")
            if abs_repo:
                repo_path = Path(abs_repo)
        except (OSError, json.JSONDecodeError):
            pass
    if repo_path is None:
        repo_path = Path.cwd()
    return run_verify(index_path, repo_path, doc_path, args.verbose)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130)
