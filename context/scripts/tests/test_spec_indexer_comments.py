"""T-021 tests: comment/docstring extraction into the top-level ``comments`` key.

Covers Python ``#`` collection via stdlib ``tokenize`` (string contents never
leak), Python ``ast.get_docstring`` attachment (module/function/class/method),
TS/JS JSDoc ``/** */`` + ``//``, SQL ``--`` / ``/* */`` with nearest
table/column attachment, symbol-level ``docstring``/``comments`` fields, orphan
handling, determinism, ``verify --index`` coverage, spec-scan rendering, and
CLI wiring.

The indexer module lives under ``context/scripts/code-specs/`` (hyphenated dir,
not importable as a package), so it is loaded via ``importlib``.
"""

import importlib.util
import json
import sys
from pathlib import Path

INDEXER_PATH = Path(__file__).resolve().parents[1] / "code-specs" / "spec_indexer.py"
REPO_ROOT = Path(__file__).resolve().parents[3]

_spec = importlib.util.spec_from_file_location("spec_indexer", INDEXER_PATH)
si = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
# dataclasses introspect sys.modules for the defining module — register it first.
sys.modules[_spec.name] = si
_spec.loader.exec_module(si)


def _write(repo: Path, files: dict[str, str]) -> Path:
    for rel, text in files.items():
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return repo


def _scan(repo: Path, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "repo-index.json"
    code = si.run_scan(repo, "both", out, 2000, False, "stdlib")
    assert code == 0, f"run_scan returned {code}"
    return json.loads(out.read_text(encoding="utf-8"))


def _entries(index: dict, path: str) -> list[dict]:
    return [c for c in index["comments"] if c["file"] == path]


def _symbol(index: dict, path: str, name: str) -> dict:
    rec = next(f for f in index["files"] if f["path"] == path)
    return next(s for s in rec["symbols"] if s["name"] == name)


PY_FIXTURE = '''"""Demo module."""

# retry budget for the connect path
MAX_RETRIES = 3  # keep under the provider limit

# standalone orphan near nothing



def run():
    """Run the pipeline."""
    # retry loop body note
    url = "https://x.example/#fragment"  # trailing not a comment
    return MAX_RETRIES  # trailing inside body
'''


class TestPythonCommentsTokenize:
    def test_comment_markers_inside_strings_are_never_captured(self, tmp_path):
        repo = _write(tmp_path, {"app.py": PY_FIXTURE})
        index = _scan(repo, tmp_path / "out")
        texts = [c["text"] for c in index["comments"]]
        # the '#fragment' inside the URL string is a STRING token, never a comment
        assert not any("fragment" in t for t in texts)
        # the real trailing comment on the same line IS captured
        assert any(t == "trailing not a comment" for t in texts)

    def test_doc_block_above_definition_attaches_leading_and_fills_docstring(self, tmp_path):
        repo = _write(tmp_path, {"app.py": PY_FIXTURE})
        index = _scan(repo, tmp_path / "out")
        sym = _symbol(index, "app.py", "MAX_RETRIES")
        assert sym["docstring"] == "retry budget for the connect path"
        kinds = {c["kind"] for c in sym["comments"]}
        assert "leading" in kinds and "inline" in kinds

    def test_trailing_comment_does_not_join_the_doc_block(self, tmp_path):
        repo = _write(tmp_path, {"app.py": PY_FIXTURE})
        index = _scan(repo, tmp_path / "out")
        # the doc block above MAX_RETRIES must be exactly the standalone line
        lead = next(
            c for c in _entries(index, "app.py") if c["kind"] == "leading" and c.get("attached")
        )
        assert lead["text"] == "retry budget for the connect path"
        assert lead["line"] == 3
        assert lead["attached"] == {"kind": "const", "name": "MAX_RETRIES", "line": 4}

    def test_body_comments_attach_inline_within_symbol_span(self, tmp_path):
        repo = _write(tmp_path, {"app.py": PY_FIXTURE})
        index = _scan(repo, tmp_path / "out")
        sym = _symbol(index, "app.py", "run")
        texts = [c["text"] for c in sym["comments"]]
        assert "retry loop body note" in texts
        assert "trailing inside body" in texts

    def test_orphan_comments_stay_in_the_stream_unattached(self, tmp_path):
        repo = _write(tmp_path, {"app.py": PY_FIXTURE})
        index = _scan(repo, tmp_path / "out")
        orphans = [
            c for c in _entries(index, "app.py") if c["text"] == "standalone orphan near nothing"
        ]
        assert len(orphans) == 1
        assert orphans[0]["attached"] is None


class TestPythonDocstrings:
    def test_module_docstring_is_an_orphan_docstring_entry(self, tmp_path):
        repo = _write(tmp_path, {"app.py": PY_FIXTURE})
        index = _scan(repo, tmp_path / "out")
        entry = next(c for c in _entries(index, "app.py") if c["kind"] == "docstring")
        assert entry["text"] == "Demo module."
        assert entry["line"] == 1
        assert entry["attached"] is None

    def test_function_docstring_attaches_to_symbol(self, tmp_path):
        repo = _write(tmp_path, {"app.py": PY_FIXTURE})
        index = _scan(repo, tmp_path / "out")
        sym = _symbol(index, "app.py", "run")
        assert sym["docstring"] == "Run the pipeline."
        doc = next(c for c in sym["comments"] if c["kind"] == "docstring")
        assert doc["text"] == "Run the pipeline."
        stream = next(
            c for c in _entries(index, "app.py") if c["kind"] == "docstring" and c.get("attached")
        )
        assert stream["attached"] == {"kind": "function", "name": "run", "line": 10}

    def test_class_and_method_docstrings_attach(self, tmp_path):
        src = (
            'class Service:\n    """Service doc."""\n\n'
            '    def run(self):\n        """Run it."""\n        return 1\n'
        )
        repo = _write(tmp_path, {"svc.py": src})
        index = _scan(repo, tmp_path / "out")
        assert _symbol(index, "svc.py", "Service")["docstring"] == "Service doc."
        assert _symbol(index, "svc.py", "Service.run")["docstring"] == "Run it."


TS_FIXTURE = """/**
 * Card component.
 * Renders an item card.
 */
export const Card = (props) => {
  // inline note
  return <div title="// not a comment">{props.items}</div>;
};

// doc above helper
export function helper(a: number): number {
  return a * 2;
}
/* legacy header block */
const x = 1;
"""


class TestTsJsComments:
    def test_jsdoc_attaches_as_docstring_and_sets_symbol_docstring(self, tmp_path):
        repo = _write(tmp_path, {"App.tsx": TS_FIXTURE})
        index = _scan(repo, tmp_path / "out")
        sym = _symbol(index, "App.tsx", "Card")
        assert sym["docstring"] == "Card component. | Renders an item card."
        assert any(c["kind"] == "docstring" for c in sym["comments"])

    def test_line_comment_inside_string_is_masked(self, tmp_path):
        repo = _write(tmp_path, {"App.tsx": TS_FIXTURE})
        index = _scan(repo, tmp_path / "out")
        texts = [c["text"] for c in index["comments"]]
        assert not any("not a comment" in t for t in texts)

    def test_line_doc_block_above_function_attaches_leading(self, tmp_path):
        repo = _write(tmp_path, {"App.tsx": TS_FIXTURE})
        index = _scan(repo, tmp_path / "out")
        sym = _symbol(index, "App.tsx", "helper")
        assert sym["docstring"] == "doc above helper"
        assert any(c["kind"] == "leading" for c in sym["comments"])

    def test_block_comment_is_orphan_until_attached(self, tmp_path):
        repo = _write(tmp_path, {"App.tsx": TS_FIXTURE})
        index = _scan(repo, tmp_path / "out")
        block = next(c for c in _entries(index, "App.tsx") if c["kind"] == "block")
        assert block["text"] == "legacy header block"
        assert block["attached"] is None


SQL_FIXTURE = """-- users table
CREATE TABLE users (
  -- unique id
  id SERIAL PRIMARY KEY
);

/* legacy schema note */
CREATE TABLE posts (
  id INT PRIMARY KEY
);
"""


class TestSqlComments:
    def test_double_dash_comment_attaches_to_nearest_table(self, tmp_path):
        repo = _write(tmp_path, {"schema.sql": SQL_FIXTURE})
        index = _scan(repo, tmp_path / "out")
        entry = next(c for c in _entries(index, "schema.sql") if c["text"] == "users table")
        assert entry["kind"] == "leading"
        assert entry["attached"] == {"kind": "table", "name": "users", "line": 2}

    def test_column_comment_attaches_to_nearest_column(self, tmp_path):
        repo = _write(tmp_path, {"schema.sql": SQL_FIXTURE})
        index = _scan(repo, tmp_path / "out")
        entry = next(c for c in _entries(index, "schema.sql") if c["text"] == "unique id")
        assert entry["attached"] == {"kind": "column", "name": "users.id", "line": 4}

    def test_block_comment_attaches_to_nearest_table(self, tmp_path):
        repo = _write(tmp_path, {"schema.sql": SQL_FIXTURE})
        index = _scan(repo, tmp_path / "out")
        block = next(c for c in _entries(index, "schema.sql") if c["kind"] == "block")
        assert block["text"] == "legacy schema note"
        assert block["attached"] == {"kind": "table", "name": "posts", "line": 8}
        users = next(t for t in index["schema"] if t["table"] == "users")
        id_col = next(c for c in users["columns"] if c["name"] == "id")
        assert id_col["line"] == 4


class TestIndexIntegration:
    def test_comments_key_sorted_and_deterministic(self, tmp_path):
        repo = _write(
            tmp_path,
            {"app.py": PY_FIXTURE, "App.tsx": TS_FIXTURE, "schema.sql": SQL_FIXTURE},
        )
        index = _scan(repo, tmp_path / "out1")
        keys = [(c["file"], c["line"]) for c in index["comments"]]
        assert keys == sorted(keys)
        index2 = _scan(repo, tmp_path / "out2")
        assert index2["comments"] == index["comments"]

    def test_verify_index_checks_comment_citations(self, tmp_path):
        repo = _write(tmp_path, {"app.py": PY_FIXTURE, "schema.sql": SQL_FIXTURE})
        out = tmp_path / "out" / "repo-index.json"
        si.run_scan(repo, "both", out, 2000, False, "stdlib")
        assert si.run_verify(out, repo, None, False) == 0
        (repo / "app.py").unlink()
        assert si.run_verify(out, repo, None, False) == 1

    def test_render_spec_scan_shows_comment_map(self):
        index = {
            "warnings": [],
            "docs": [],
            "files": [],
            "api": [],
            "schema": [],
            "ui": [],
            "tests": [],
            "config": [],
            "comments": [
                {
                    "file": "a.py",
                    "line": 3,
                    "kind": "leading",
                    "text": "retry note",
                    "attached": {"kind": "function", "name": "run", "line": 4},
                },
                {
                    "file": "b.sql",
                    "line": 1,
                    "kind": "block",
                    "text": "licence",
                    "attached": None,
                },
            ],
            "meta": {
                "repo": "demo",
                "generated_at": "2026-01-01T00:00:00Z",
                "mode": "both",
                "scanned_files": 0,
                "languages": {},
            },
        }
        md = si.render_spec_scan(index)
        assert "## Comments & Docstrings (intent evidence)" in md
        assert "2 comment blocks across 2 files" in md
        assert "a.py:3" in md and "retry note" in md and "`run`" in md
        assert "b.sql:1" in md

    def test_render_spec_scan_says_none_when_no_comments(self):
        index = {
            "warnings": [],
            "docs": [],
            "files": [],
            "api": [],
            "schema": [],
            "ui": [],
            "tests": [],
            "config": [],
            "meta": {
                "repo": "demo",
                "generated_at": "2026-01-01T00:00:00Z",
                "mode": "both",
                "scanned_files": 0,
                "languages": {},
            },
        }
        assert "None detected in indexed sources" in si.render_spec_scan(index)

    def test_cli_scan_emits_comments_key(self, tmp_path):
        repo = _write(tmp_path, {"app.py": PY_FIXTURE})
        out = tmp_path / "cli" / "repo-index.json"
        code = si.main(["scan", "--repo", str(repo), "--out", str(out), "--extractors", "stdlib"])
        assert code == 0
        index = json.loads(out.read_text(encoding="utf-8"))
        assert index["comments"]
        assert all(c["line"] > 0 for c in index["comments"])


class TestRealRepo:
    def test_real_repo_module_docstring_is_indexed(self):
        entries, _warnings = si.collect_comments(
            REPO_ROOT, [], [], ["context/scripts/code-specs/spec_indexer.py"]
        )
        docs = [e for e in entries if e.kind == "docstring"]
        assert any(e.text.startswith("Deterministic codebase indexer") for e in docs), (
            "spec_indexer.py module docstring must be indexed"
        )

    def test_real_repo_comment_stream_uses_exact_file_lines(self):
        entries, _warnings = si.collect_comments(
            REPO_ROOT, [], [], ["context/scripts/code-specs/spec_indexer.py"]
        )
        assert len(entries) > 10
        for e in entries:
            assert e.line >= 1
        # the module docstring is the first docstring entry
        assert entries[0].kind == "docstring"
