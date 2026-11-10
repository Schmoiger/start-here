"""T-010 tests: skill frontmatter schema, workflow YAML phase schema, indexer
extraction (Python / TS/TSX / SQL), and ``verify`` pass/fail on synthetic repos.

The indexer module lives under ``context/scripts/code-specs/`` (hyphenated dir,
not importable as a package), so it is loaded via ``importlib``. Schema tests
load the real ``context/skills/*.md`` and ``context/workflows/*.yaml`` files and
validate them against the expected schema, plus exercise the validator against
synthetic broken inputs.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest
import yaml

INDEXER_PATH = Path(__file__).resolve().parents[1] / "code-specs" / "spec_indexer.py"
REPO_ROOT = Path(__file__).resolve().parents[3]
CONTEXT_DIR = REPO_ROOT / "context"
SKILLS_DIR = CONTEXT_DIR / "skills"
AGENTS_DIR = CONTEXT_DIR / "agents"
WORKFLOWS_DIR = CONTEXT_DIR / "workflows"

_spec = importlib.util.spec_from_file_location("spec_indexer", INDEXER_PATH)
si = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
# dataclasses introspect sys.modules for the defining module — register it first.
sys.modules[_spec.name] = si
_spec.loader.exec_module(si)

KNOWN_AGENTS = {p.stem for p in AGENTS_DIR.glob("*.md")}

# The two derive-spec-relevant skills carry name/description/globs frontmatter.
SKILL_FILES = ["derive-spec.md", "analyse-repo.md"]

TSX_FIXTURE = """export interface CardProps {
  items: string[];
}

export function Header({ title, onSave, isActive = false }: HeaderProps): JSX.Element {
  return <div><Button label={title} /></div>;
}

export const Card = ({ items, onOpen }: CardProps) => {
  return <Button label="x" />;
};

const plain = 42;
"""


# ---------------------------------------------------------------------------
# Schema helpers (skills + workflows)
# ---------------------------------------------------------------------------


def _parse_frontmatter(path: Path) -> dict:
    text = Path(path).read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"{path} has no YAML frontmatter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"{path} malformed YAML frontmatter")
    fm = yaml.safe_load(parts[1])
    if not isinstance(fm, dict):
        raise ValueError(f"{path} frontmatter is not a mapping")
    return fm


def _validate_skill(fm: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(fm.get("name"), str) or not fm["name"]:
        errors.append("skill missing non-empty 'name' string")
    if not isinstance(fm.get("description"), str) or not fm["description"]:
        errors.append("skill missing non-empty 'description' string")
    globs = fm.get("globs")
    if globs is not None and (
        not isinstance(globs, list) or not all(isinstance(g, str) and g for g in globs)
    ):
        errors.append("skill 'globs' must be a list of non-empty strings")
    return errors


def _validate_workflow(data: dict, known_agents: set[str]) -> list[str]:
    """Return a list of schema violations for a workflow document."""
    errors: list[str] = []
    phases = data.get("phases")
    if not isinstance(phases, list):
        return ["workflow has no 'phases' list"]

    ids: list[str] = []
    for ph in phases:
        if not isinstance(ph, dict):
            errors.append("phase is not a mapping")
            continue
        pid = ph.get("id")
        if not isinstance(pid, str) or not pid:
            errors.append("phase missing non-empty 'id' string")
        else:
            if pid in ids:
                errors.append(f"duplicate phase id: {pid}")
            ids.append(pid)

    for ph in phases:
        if not isinstance(ph, dict):
            continue
        pid = ph.get("id")
        if not isinstance(ph.get("name"), str) or not ph["name"]:
            errors.append(f"phase {pid!r} missing non-empty 'name' string")
        if "gate" in ph and not isinstance(ph["gate"], bool):
            errors.append(f"phase {pid!r} 'gate' must be a boolean")
        agents = ph.get("agents")
        if not isinstance(agents, list):
            errors.append(f"phase {pid!r} missing 'agents' list")
        else:
            for agent in agents:
                a = str(agent).split("#", 1)[0].strip().lstrip("@")
                if a and a not in known_agents:
                    errors.append(f"phase {pid!r} references unknown agent {a!r}")
        for dep in ph.get("depends_on") or []:
            if dep not in ids:
                errors.append(f"phase {pid!r} depends_on unknown phase {dep!r}")

    qgates = data.get("quality_gates") or []
    if not isinstance(qgates, list):
        errors.append("'quality_gates' must be a list")
        qgates = []
    listed: set[str] = set()
    for g in qgates:
        if not isinstance(g, dict):
            errors.append("quality_gate entry is not a mapping")
            continue
        pid = g.get("phase")
        if pid not in ids:
            errors.append(f"quality_gate references unknown phase {pid!r}")
        listed.add(pid)
    return errors


def _valid_workflow() -> dict:
    return {
        "name": "w",
        "phases": [
            {"id": "a", "name": "A", "agents": ["orchestrator"]},
            {
                "id": "b",
                "name": "B",
                "depends_on": ["a"],
                "agents": ["product-owner"],
                "gate": True,
            },
        ],
        "quality_gates": [{"phase": "b", "gate": True}],
    }


def _scan(repo: Path, out_dir: Path, extractors: str = "auto") -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "repo-index.json"
    code = si.run_scan(repo, "both", out, 2000, False, extractors)
    assert code == 0, f"run_scan returned {code}"
    return json.loads(out.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Skill frontmatter schema
# ---------------------------------------------------------------------------


class TestSkillFrontmatterSchema:
    def test_derive_skills_have_valid_frontmatter(self):
        for name in SKILL_FILES:
            fm = _parse_frontmatter(SKILLS_DIR / name)
            assert _validate_skill(fm) == [], f"{name} failed: {_validate_skill(fm)}"

    def test_skill_name_matches_filename_stem(self):
        for name in SKILL_FILES:
            fm = _parse_frontmatter(SKILLS_DIR / name)
            assert fm["name"] == Path(name).stem

    def test_skill_globs_is_list_of_glob_strings(self):
        for name in SKILL_FILES:
            fm = _parse_frontmatter(SKILLS_DIR / name)
            assert isinstance(fm.get("globs"), list)
            assert all(isinstance(g, str) and g for g in fm["globs"])


# ---------------------------------------------------------------------------
# Workflow YAML phase schema
# ---------------------------------------------------------------------------


class TestWorkflowPhaseSchema:
    def test_all_real_workflows_pass_schema(self):
        for path in sorted(WORKFLOWS_DIR.glob("*.yaml")):
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            errors = _validate_workflow(data, KNOWN_AGENTS)
            assert errors == [], f"{path.name} failed: {errors}"

    def test_rejects_duplicate_phase_ids(self):
        wf = _valid_workflow()
        wf["phases"][1] = {"id": "a", "name": "dup", "agents": ["orchestrator"]}
        errors = _validate_workflow(wf, KNOWN_AGENTS)
        assert any("duplicate phase id" in e for e in errors)

    def test_rejects_unresolvable_depends_on(self):
        wf = _valid_workflow()
        wf["phases"][1]["depends_on"] = ["ghost"]
        errors = _validate_workflow(wf, KNOWN_AGENTS)
        assert any(e == "phase 'b' depends_on unknown phase 'ghost'" for e in errors)

    def test_rejects_unknown_agent(self):
        wf = _valid_workflow()
        wf["phases"][0]["agents"] = ["ghost"]
        errors = _validate_workflow(wf, KNOWN_AGENTS)
        assert any("unknown agent" in e for e in errors)

    def test_accepts_at_prefix_and_inline_comment_agents(self):
        wf = _valid_workflow()
        wf["phases"][1]["agents"] = ["@product-owner  # modes product | both"]
        assert _validate_workflow(wf, KNOWN_AGENTS) == []

    def test_rejects_non_boolean_phase_gate(self):
        wf = _valid_workflow()
        wf["phases"][1]["gate"] = "yes"
        errors = _validate_workflow(wf, KNOWN_AGENTS)
        assert any(e == "phase 'b' 'gate' must be a boolean" for e in errors)

    def test_gate_phase_without_quality_gates_entry_is_allowed(self):
        # build.yaml phases with gate:true need not each have a quality_gates entry.
        wf = _valid_workflow()
        wf.pop("quality_gates")
        assert _validate_workflow(wf, KNOWN_AGENTS) == []

    def test_rejects_quality_gate_unknown_phase(self):
        wf = _valid_workflow()
        wf["quality_gates"] = [{"phase": "ghost", "gate": True}]
        errors = _validate_workflow(wf, KNOWN_AGENTS)
        assert any(e == "quality_gate references unknown phase 'ghost'" for e in errors)

    def test_accepts_evidence_style_quality_gate_without_gate_key(self):
        # bugfix.yaml gates use {phase, type, required, criteria} — no 'gate' key.
        wf = _valid_workflow()
        wf["quality_gates"] = [{"phase": "b", "type": "evidence", "required": True}]
        assert _validate_workflow(wf, KNOWN_AGENTS) == []


# ---------------------------------------------------------------------------
# Python extraction (symbols, routes, constants)
# ---------------------------------------------------------------------------


class TestPythonExtraction:
    PY_SOURCE = """\
import os
from flask import Flask

app = Flask(__name__)

MAX_RETRIES = 3
DEFAULT_SCHEME = "https"

def helper(x):
    return x + 1

@app.route("/health", methods=["GET"])
def health():
    return "ok"

class UserService:
    def get_user(self, uid: int):
        return uid

    @app.post("/users")
    async def create_user(self, name: str):
        return name
"""

    def test_symbols_and_constants(self, tmp_path):
        py = tmp_path / "service.py"
        py.write_text(self.PY_SOURCE, encoding="utf-8")
        record, _api = si.analyze_python(py, "service.py")
        kinds = {(s.kind, s.name, s.line) for s in record.symbols}
        assert ("const", "MAX_RETRIES", 6) in kinds
        assert ("const", "DEFAULT_SCHEME", 7) in kinds
        assert ("function", "helper", 9) in kinds
        assert ("function", "health", 13) in kinds
        assert ("class", "UserService", 16) in kinds
        assert ("method", "UserService.get_user", 17) in kinds
        assert ("method", "UserService.create_user", 21) in kinds
        assert record.extractor == "stdlib.ast"

    def test_imports_recorded(self, tmp_path):
        py = tmp_path / "service.py"
        py.write_text(self.PY_SOURCE, encoding="utf-8")
        record, _api = si.analyze_python(py, "service.py")
        assert "os" in record.imports
        assert "flask" in record.imports

    def test_route_decorators_produce_api_entries(self, tmp_path):
        py = tmp_path / "service.py"
        py.write_text(self.PY_SOURCE, encoding="utf-8")
        record, api = si.analyze_python(py, "service.py")
        routes = {(e.method, e.path, e.handler) for e in api}
        assert ("GET", "/health", "health") in routes
        assert ("POST", "/users", "UserService.create_user") in routes
        # every ApiEntry points back at the file being scanned
        assert all(e.file == "service.py" for e in api)
        assert record.line_count > 0


# ---------------------------------------------------------------------------
# TypeScript / TSX extraction (components, props, usage counts)
# ---------------------------------------------------------------------------


class TestTsJsExtraction:
    def test_components_props_and_usage(self, tmp_path):
        fixture = tmp_path / "App.tsx"
        fixture.write_text(TSX_FIXTURE, encoding="utf-8")
        record, usages = si.analyze_tsjs(fixture, "App.tsx", "typescript")
        kinds = {(s.kind, s.name) for s in record.symbols}
        assert ("interface", "CardProps") in kinds
        assert ("function", "Header") in kinds
        assert ("const_arrow", "Card") in kinds
        header = next(s for s in record.symbols if s.name == "Header")
        card = next(s for s in record.symbols if s.name == "Card")
        assert sorted(header.props) == ["isActive", "onSave", "title"]
        assert sorted(card.props) == ["items", "onOpen"]
        assert usages.count("Button") == 2
        assert record.extractor == "stdlib.regex"

    def test_scan_aggregates_ui_components(self, tmp_path):
        (tmp_path / "App.tsx").write_text(TSX_FIXTURE, encoding="utf-8")
        index = _scan(tmp_path, tmp_path / "out", extractors="stdlib")
        ui = {u["component"]: u for u in index["ui"]}
        assert {"Header", "Card"} <= set(ui)
        assert sorted(ui["Header"]["props"]) == ["isActive", "onSave", "title"]
        assert sorted(ui["Card"]["props"]) == ["items", "onOpen"]
        # Button is used but never defined in this repo → not a local ui entry
        assert "Button" not in ui
        # per-file extractor provenance is populated
        app_rec = next(f for f in index["files"] if f["path"] == "App.tsx")
        assert app_rec["extractor"] == "stdlib.regex"


# ---------------------------------------------------------------------------
# SQL table parsing
# ---------------------------------------------------------------------------


class TestSqlParsing:
    SQL_SOURCE = """\
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE posts (
  id INT PRIMARY KEY,
  user_id INT REFERENCES users(id)
);
"""

    def test_create_table_columns(self, tmp_path):
        sql = tmp_path / "schema.sql"
        sql.write_text(self.SQL_SOURCE, encoding="utf-8")
        tables = si.analyze_sql(sql, "schema.sql")
        names = {t.table for t in tables}
        assert {"users", "posts"} <= names
        users = next(t for t in tables if t.table == "users")
        posts = next(t for t in tables if t.table == "posts")
        assert sorted(c.name for c in users.columns) == ["created_at", "email", "id"]
        assert {c.name for c in posts.columns} == {"id", "user_id"}
        assert all(t.file == "schema.sql" and t.line > 0 for t in tables)
        # PK / FK constraint lines are not themselves columns
        assert not any(c.type.startswith("PRIMARY KEY") for t in tables for c in t.columns)


# ---------------------------------------------------------------------------
# verify pass/fail on synthetic repos
# ---------------------------------------------------------------------------


class TestVerifyOnSyntheticRepo:
    def test_verify_passes_index_then_fails_when_source_removed(self, tmp_path):
        (tmp_path / "app.py").write_text(
            "import os\n\nMAX_RETRIES = 3\n\ndef run():\n    return MAX_RETRIES\n",
            encoding="utf-8",
        )
        out = tmp_path / "out" / "repo-index.json"
        assert si.run_scan(tmp_path, "both", out, 2000, False, "auto") == 0
        assert si.run_verify(out, tmp_path, None, False) == 0
        (tmp_path / "app.py").unlink()
        assert si.run_verify(out, tmp_path, None, False) == 1

    def test_verify_doc_checks_cited_file_lines(self, tmp_path):
        (tmp_path / "a.py").write_text("x = 1\ny = 2\nz = 3\n", encoding="utf-8")
        doc = tmp_path / "draft.md"
        doc.write_text("See a.py:2 for y.\n", encoding="utf-8")
        assert si.run_verify(None, tmp_path, doc, False) == 0
        # valid file, out-of-range line → failure
        doc.write_text("See a.py:99 nonexistent.\n", encoding="utf-8")
        assert si.run_verify(None, tmp_path, doc, False) == 1
        # missing file → failure
        doc.write_text("See missing.py:1 gone.\n", encoding="utf-8")
        assert si.run_verify(None, tmp_path, doc, False) == 1


# ---------------------------------------------------------------------------
# T-015 backend smoke: invalid extractor + provenance
# ---------------------------------------------------------------------------


class TestExtractorSmoke:
    def test_invalid_extractor_exits_nonzero(self, tmp_path):
        (tmp_path / "a.py").write_text("x = 1\n", encoding="utf-8")
        out = tmp_path / "out" / "repo-index.json"
        assert si.run_scan(tmp_path, "both", out, 2000, False, "bogus") == 2

    def test_meta_extractors_provenance_populated(self, tmp_path):
        (tmp_path / "a.py").write_text("X = 1\n", encoding="utf-8")
        out = tmp_path / "out" / "repo-index.json"
        assert si.run_scan(tmp_path, "both", out, 2000, False, "stdlib") == 0
        index = json.loads(out.read_text(encoding="utf-8"))
        meta = index["meta"]["extractors"]
        assert meta["stdlib"]["available"] is True
        assert meta["stdlib"]["used"] is True
        assert set(meta) == {"ctags", "tree-sitter", "ast-grep", "ts-morph", "stdlib"}
        rec = next(f for f in index["files"] if f["path"] == "a.py")
        assert rec["extractor"] == "stdlib.ast"


# ---------------------------------------------------------------------------
# T-020: verify --doc --require-coverage (deterministic Phase 6 coverage gate)
# ---------------------------------------------------------------------------


def _write_source(tmp_path: Path) -> Path:
    """Create a repo with app.py long enough to satisfy file:line citations."""
    lines = "\n".join(f"# line {i}" for i in range(1, 60)) + "\ndef handler():\n    pass\n"
    (tmp_path / "app.py").write_text(lines, encoding="utf-8")
    return tmp_path


GOOD_DOC = """# Product Spec: Demo (Derived)

## Confidence Schema

| Band | % | Evidence |
|------|---|----------|
| Verified | 85-100 | path:line |

## Features and Capabilities

**Confidence**: Verified · 90% · Evidence: `app.py:12`

The app has a feature.

## UX Flows

**Confidence**: **Needs Confirmation** · 60% · Evidence: `app.py:5`

Flow text.

## Open-Questions Appendix

| ID | Status |
|----|--------|
| Q-1 | still-open |
"""


class TestDocCoverage:
    def test_coverage_passes_when_every_content_subsection_confident(self, tmp_path):
        repo = _write_source(tmp_path)
        doc = tmp_path / "spec.md"
        doc.write_text(GOOD_DOC, encoding="utf-8")
        assert si.run_verify(None, repo, doc, False, True) == 0

    def test_coverage_can_be_disabled_by_default(self, tmp_path):
        repo = _write_source(tmp_path)
        doc = tmp_path / "spec.md"
        doc.write_text("## Features\n\nNo confidence at all.\n", encoding="utf-8")
        # without require_coverage the plain citation check still succeeds
        assert si.run_verify(None, repo, doc, False, False) == 0

    def test_coverage_fails_on_missing_confidence_line(self):
        covered, total, errors = si.check_doc_coverage("## Features\n\nNo confidence here.\n")
        assert (covered, total) == (0, 1)
        assert any("Features" in e and "Confidence" in e for e in errors)

    def test_coverage_reports_missing_tier(self):
        doc = "## Features\n\n**Confidence**: 90% · Evidence: `app.py:12`\n"
        covered, total, errors = si.check_doc_coverage(doc)
        assert total == 1 and covered == 1
        assert any("tier" in e for e in errors)

    def test_coverage_reports_missing_percentage(self):
        doc = "## Features\n\n**Confidence**: Verified · Evidence: `app.py:12`\n"
        covered, total, errors = si.check_doc_coverage(doc)
        assert total == 1 and covered == 1
        assert any("percentage" in e for e in errors)

    def test_coverage_reports_missing_file_line_citation(self):
        doc = "## Routes\n\n**Confidence**: Assumed · 20% · Evidence: repo-index.json:api (none)\n"
        covered, total, errors = si.check_doc_coverage(doc)
        assert total == 1 and covered == 1
        assert any("file:line" in e for e in errors)

    def test_coverage_reports_band_mismatch(self):
        doc = "## Features\n\n**Confidence**: Verified · 60% · Evidence: `app.py:12`\n"
        covered, total, errors = si.check_doc_coverage(doc)
        assert any("band mismatch" in e for e in errors)

    def test_coverage_accepts_markdown_file_line_citations(self):
        doc = "## F\n\n**Confidence**: Verified · 85% · Evidence: `notes.md:2`\n"
        covered, total, errors = si.check_doc_coverage(doc)
        assert covered == 1 and errors == []

    def test_coverage_boundary_85_allows_verified_or_needs_confirmation(self):
        for tier in ("Verified", "Needs Confirmation"):
            doc = f"## F\n\n**Confidence**: {tier} · 85% · Evidence: `a.md:2`\n"
            covered, _total, errors = si.check_doc_coverage(doc)
            assert covered == 1 and errors == []

    def test_coverage_skips_placeholder_and_structural_headings(self):
        doc = (
            "## Subsection Format\n\n### {Subsection title}\n\n"
            "Confidence: {Band} · {NN}% · Evidence: path:line\n\n"
            "## Drift: Canonical Docs vs Derived Behaviour\n\nSome drift.\n\n"
            "## Open-Questions Appendix\n\nNo confidence needed.\n\n"
        )
        covered, total, errors = si.check_doc_coverage(doc)
        assert covered == 0 and total == 0 and errors == []

    def test_coverage_fails_via_run_verify_and_lists_subsection(self, tmp_path):
        repo = _write_source(tmp_path)
        doc = tmp_path / "bad.md"
        doc.write_text(
            "## Routes\n\n**Confidence**: Assumed · 20% · Evidence: repo-index.json:api\n",
            encoding="utf-8",
        )
        assert si.run_verify(None, repo, doc, False, True) == 1

    def test_cli_require_coverage_requires_doc(self):
        with pytest.raises(SystemExit):
            si.main(["verify", "--index", "/tmp/nonexistent-index.json", "--require-coverage"])
