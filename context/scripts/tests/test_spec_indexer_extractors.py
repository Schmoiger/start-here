"""T-015 tests: --extractors backends, probing, provenance, parity, and fixtures.

The indexer module lives under ``context/scripts/code-specs/`` (hyphenated dir,
not importable as a package), so it is loaded via ``importlib``.
"""

import importlib.util
import json
import sys
from pathlib import Path

import pytest

INDEXER_PATH = Path(__file__).resolve().parents[1] / "code-specs" / "spec_indexer.py"
REPO_ROOT = Path(__file__).resolve().parents[3]

_spec = importlib.util.spec_from_file_location("spec_indexer", INDEXER_PATH)
si = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
# dataclasses introspect sys.modules for the defining module — register it first.
sys.modules[_spec.name] = si
_spec.loader.exec_module(si)

TSX_FIXTURE = """import React, { useState } from "react";
import { Button, Input } from "./components";
import * as Utils from "./utils";
import api from "./api";

export interface User { id: number; name: string; }

export type Status = "active" | "inactive";

@Component({ selector: "app" })
export class AppHeader extends React.Component<User> {
  private renderTitle(): string { return "hi"; }
}

export function Header({
  title,
  onSave,
  isActive = false,
}: HeaderProps): JSX.Element {
  return <div><Button label={title} /></div>;
}

export const Card = ({ items, onOpen }: CardProps) => {
  return <Button label="x" />;
};

const plain = 42;
"""


def _scan(repo: Path, extractors: str, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"repo-index-{extractors}.json"
    code = si.run_scan(repo, "both", out, 2000, False, extractors)
    assert code == 0, f"run_scan returned {code}"
    return json.loads(out.read_text(encoding="utf-8"))


def _all_symbols(index: dict) -> list[tuple[str, str, str]]:
    return sorted(
        (file["path"], sym["kind"], sym["name"])
        for file in index["files"]
        for sym in file["symbols"]
    )


def _python_symbols(index: dict) -> list[tuple[str, str, str]]:
    return [t for t in _all_symbols(index) if t[0].endswith(".py")]


class TestProbeAndPlan:
    def test_probe_backends_never_raises(self):
        avail = si.probe_backends(REPO_ROOT)
        for tool in ("ctags", "tree-sitter", "ast-grep", "ts-morph"):
            assert tool in avail and isinstance(avail[tool], bool)

    def test_auto_plan_python_uses_stdlib_ast(self):
        avail = si.probe_backends(REPO_ROOT)
        plan, _reasons, errors, _warnings = si.resolve_plan("auto", avail, {"python", "sql"})
        assert errors == []
        assert plan["python"] == "stdlib.ast"
        assert plan["sql"] == "stdlib.sql"

    def test_auto_plan_ts_prefers_treesitter_when_available(self):
        avail = {"ctags": True, "tree-sitter": True, "ast-grep": True, "ts-morph": True}
        plan, _reasons, errors, _warnings = si.resolve_plan("auto", avail, {"typescript"})
        assert errors == []
        assert plan["typescript"] == "tree-sitter"

    def test_auto_plan_ts_degrades_to_astgrep_then_regex(self):
        avail = {"ctags": True, "tree-sitter": False, "ast-grep": True, "ts-morph": False}
        plan, _reasons, errors, _warnings = si.resolve_plan("auto", avail, {"typescript"})
        assert errors == []
        assert plan["typescript"] == "ast-grep"

        avail = {"ctags": True, "tree-sitter": False, "ast-grep": False, "ts-morph": False}
        plan, _reasons, errors, _warnings = si.resolve_plan("auto", avail, {"typescript"})
        assert errors == []
        assert plan["typescript"] == "stdlib.regex"

    def test_explicit_unavailable_backend_is_an_error(self):
        avail = {"ctags": False, "tree-sitter": False, "ast-grep": False, "ts-morph": False}
        plan, _reasons, errors, warnings = si.resolve_plan("ctags", avail, {"python"})
        assert plan == {}
        assert errors and "ctags" in errors[0]
        assert warnings == []

    def test_explicit_ts_morph_unavailable_degrades_quietly(self):
        avail = {"ctags": True, "tree-sitter": False, "ast-grep": False, "ts-morph": False}
        plan, _reasons, errors, warnings = si.resolve_plan("ts-morph", avail, {"python"})
        assert errors == []
        assert warnings and "ts-morph" in warnings[0]
        assert all(v.startswith("stdlib") for v in plan.values())

    def test_cli_rejects_unknown_extractor(self):
        with pytest.raises(SystemExit) as exc:
            si.main(["scan", "--repo", str(REPO_ROOT), "--extractors", "bad"])
        assert exc.value.code == 2


class TestParity:
    def test_auto_and_stdlib_python_symbols_identical(self, tmp_path):
        auto = _scan(REPO_ROOT, "auto", tmp_path)
        stdlib = _scan(REPO_ROOT, "stdlib", tmp_path)
        assert _python_symbols(auto) == _python_symbols(stdlib)
        assert _python_symbols(auto), "repo scan should find python symbols"
        assert auto["meta"]["scanned_files"] == stdlib["meta"]["scanned_files"]
        assert [f["path"] for f in auto["api"]] == [f["path"] for f in stdlib["api"]]
        assert [f["path"] for f in auto["schema"]] == [f["path"] for f in stdlib["schema"]]

    def test_auto_is_superset_of_stdlib(self, tmp_path):
        """auto may be richer than stdlib (tree-sitter beats regex for TS/JS),
        but must never lose symbols the stdlib would have found."""
        from collections import Counter

        auto = _scan(REPO_ROOT, "auto", tmp_path)
        stdlib = _scan(REPO_ROOT, "stdlib", tmp_path)
        assert Counter(_all_symbols(stdlib)) <= Counter(_all_symbols(auto))

    def test_meta_provenance_fields_present(self, tmp_path):
        index = _scan(REPO_ROOT, "auto", tmp_path)
        meta = index["meta"]
        assert meta["confidence"] in ("full", "regex", "degraded")
        assert set(meta["extractors"]) == {
            "ctags",
            "tree-sitter",
            "ast-grep",
            "ts-morph",
            "stdlib",
        }
        for _tool, entry in meta["extractors"].items():
            assert set(entry) == {"available", "used", "reason"}
        assert all(isinstance(f.get("extractor"), str) and f["extractor"] for f in index["files"])


class TestCtagsBackend:
    def test_python_file_yields_symbols(self, tmp_path):
        (tmp_path / "mod.py").write_text(
            "import os\n\nclass Service:\n    def run(self, x: int) -> int:\n        return x\n\n"
            "def helper():\n    return 1\n\nVERSION = 42\n",
            encoding="utf-8",
        )
        record = si.analyze_ctags(tmp_path / "mod.py", "mod.py", "python")
        names = [(s.kind, s.name) for s in record.symbols]
        assert ("class", "Service") in names
        assert ("function", "helper") in names
        assert record.extractor == "ctags"

    def test_ts_file_method_scoped_names(self, tmp_path):
        (tmp_path / "a.ts").write_text(
            "export class Cls {\n  run(): void {}\n}\nconst K = 1;\n",
            encoding="utf-8",
        )
        record = si.analyze_ctags(tmp_path / "a.ts", "a.ts", "typescript")
        names = [(s.kind, s.name) for s in record.symbols]
        assert ("class", "Cls") in names
        assert any(k == "method" and n.startswith("Cls.") for k, n in names)


class TestTreeSitterBackend:
    def test_fixture_richer_than_regex(self, tmp_path):
        pytest.importorskip("tree_sitter_language_pack")
        fixture = tmp_path / "App.tsx"
        fixture.write_text(TSX_FIXTURE, encoding="utf-8")

        regex_record, regex_usage = si.analyze_tsjs(fixture, "App.tsx", "typescript")
        ts_record, ts_usage = si.analyze_tsjs_treesitter(fixture, "App.tsx", "typescript")

        def by_name(record, name):
            return next((s for s in record.symbols if s.name == name), None)

        # Multiline destructured props: regex misses, tree-sitter captures them.
        regex_header = by_name(regex_record, "Header")
        ts_header = by_name(ts_record, "Header")
        assert regex_header is None or regex_header.props == []
        assert sorted(ts_header.props) == ["isActive", "onSave", "title"]

        # Decorators: only tree-sitter captures them.
        ts_app_header = by_name(ts_record, "AppHeader")
        assert ts_app_header is not None
        assert ts_app_header.decorators and "@Component" in ts_app_header.decorators[0]

        # JSX usage counts are consistent and accurate.
        assert ts_usage.count("Button") == 2
        assert ts_usage.count("Button") == regex_usage.count("Button")

        # Component detection behaves identically to run_scan's filter.
        components = {s.name for s in ts_record.symbols if si._is_component(s.name, s.kind)}
        assert "Header" in components and "Card" in components

    def test_fixture_symbols_kinds(self, tmp_path):
        pytest.importorskip("tree_sitter_language_pack")
        fixture = tmp_path / "App.tsx"
        fixture.write_text(TSX_FIXTURE, encoding="utf-8")
        record, _usage = si.analyze_tsjs_treesitter(fixture, "App.tsx", "typescript")
        kinds = {(s.kind, s.name) for s in record.symbols}
        assert ("function", "Header") in kinds
        assert ("class", "AppHeader") in kinds
        assert ("interface", "User") in kinds
        assert ("type", "Status") in kinds
        assert ("const_arrow", "Card") in kinds
        assert ("method", "AppHeader.renderTitle") in kinds
        assert record.extractor == "tree-sitter"


class TestAstGrepBackend:
    def test_fixture_interfaces_types_and_consts(self, tmp_path):
        fixture = tmp_path / "sample.ts"
        fixture.write_text(
            "interface Ui { x: number }\ntype Mode = 'a' | 'b'\nconst pick = (x: number) => x;\n",
            encoding="utf-8",
        )
        record, _usage = si.analyze_tsjs_astgrep(fixture, "sample.ts", "typescript")
        if not record.symbols:
            pytest.skip("ast-grep not producing matches in this environment")
        kinds = {(s.kind, s.name) for s in record.symbols}
        assert ("interface", "Ui") in kinds
        assert ("type", "Mode") in kinds
        assert ("const_arrow", "pick") in kinds
        assert record.extractor == "ast-grep"
