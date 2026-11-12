"""T-017 tests: capped git-history evidence in ``meta.history``.

Covers commit-subject capture (newest first), rename/refactor clues from
``git log --name-status``, the ``--history N`` cap (including ``0`` disabling
the pull), key absence when the repo has no git metadata / no commits,
determinism, CLI wiring, and the spec-scan rendering.

The indexer module lives under ``context/scripts/code-specs/`` (hyphenated dir,
not importable as a package), so it is loaded via ``importlib``.
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

INDEXER_PATH = Path(__file__).resolve().parents[1] / "code-specs" / "spec_indexer.py"
REPO_ROOT = Path(__file__).resolve().parents[3]

_spec = importlib.util.spec_from_file_location("spec_indexer", INDEXER_PATH)
si = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
sys.modules[_spec.name] = si
_spec.loader.exec_module(si)


def _git(repo: Path, *args: str, env: dict | None = None) -> None:
    subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        env=env,
        check=True,
    )


def _init_repo(repo: Path) -> None:
    repo.mkdir(parents=True, exist_ok=True)
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t017@example.com")
    _git(repo, "config", "user.name", "T-017 Test")


def _commit(repo: Path, message: str, files: dict[str, str], when: str) -> None:
    for rel, text in files.items():
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        _git(repo, "add", "--", rel)
    env = {**os.environ, "GIT_AUTHOR_DATE": when, "GIT_COMMITTER_DATE": when}
    _git(repo, "commit", "-q", "-m", message, env=env)


def _scan(repo: Path, out_dir: Path, history_cap: int = 200) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "repo-index.json"
    code = si.run_scan(repo, "both", out, 2000, False, "auto", history_cap=history_cap)
    assert code == 0, f"run_scan returned {code}"
    return json.loads(out.read_text(encoding="utf-8"))


class TestHistoryPresence:
    def test_history_should_list_commit_subjects_newest_first(self, tmp_path):
        repo = tmp_path / "repo"
        _init_repo(repo)
        _commit(repo, "feat: add billing", {"app.py": "x = 1\n"}, "2026-01-01T10:00:00Z")
        _commit(repo, "fix: retry on 429", {"app.py": "x = 2\n"}, "2026-01-02T10:00:00Z")
        _commit(repo, "test: cover billing", {"check.py": "y = 1\n"}, "2026-01-03T10:00:00Z")
        index = _scan(repo, tmp_path / "out")
        history = index["meta"]["history"]
        assert history["count"] == 3
        assert history["commit_subjects"] == [
            "test: cover billing",
            "fix: retry on 429",
            "feat: add billing",
        ]
        assert history["capped"] is False
        assert history["renames"] == []

    def test_history_should_record_rename_clues_when_files_moved(self, tmp_path):
        repo = tmp_path / "repo"
        _init_repo(repo)
        _commit(
            repo,
            "feat: initial layout",
            {"src/main.py": "def run():\n    return 'hello'\n"},
            "2026-02-01T10:00:00Z",
        )
        src = repo / "src" / "main.py"
        dst = repo / "lib" / "runner.py"
        dst.parent.mkdir(parents=True, exist_ok=True)
        src.rename(dst)
        env = {
            **os.environ,
            "GIT_AUTHOR_DATE": "2026-02-02T10:00:00Z",
            "GIT_COMMITTER_DATE": "2026-02-02T10:00:00Z",
        }
        _git(repo, "add", "-A", env=env)
        _git(repo, "commit", "-q", "-m", "refactor: move runner to lib", env=env)
        index = _scan(repo, tmp_path / "out")
        renames = index["meta"]["history"]["renames"]
        assert renames, "expected rename clues in meta.history"
        assert any(
            r["old"] == "src/main.py"
            and r["new"] == "lib/runner.py"
            and r["subject"] == "refactor: move runner to lib"
            and len(r["commit"]) == 40
            for r in renames
        )

    def test_history_should_respect_history_cap_with_capped_flag(self, tmp_path):
        repo = tmp_path / "repo"
        _init_repo(repo)
        for i in range(5):
            _commit(
                repo,
                f"feat: change {i}",
                {"a.txt": f"content {i}\n"},
                f"2026-03-0{i + 1}T10:00:00Z",
            )
        index = _scan(repo, tmp_path / "out", history_cap=2)
        history = index["meta"]["history"]
        assert history["count"] == 2
        assert history["commit_subjects"] == ["feat: change 4", "feat: change 3"]
        assert history["capped"] is True

    def test_history_should_be_deterministic_across_scans(self, tmp_path):
        repo = tmp_path / "repo"
        _init_repo(repo)
        _commit(repo, "feat: one", {"a.txt": "a\n"}, "2026-05-01T10:00:00Z")
        _commit(repo, "refactor: b", {"b.txt": "b\n"}, "2026-05-02T10:00:00Z")
        first = _scan(repo, tmp_path / "out1")["meta"]["history"]
        second = _scan(repo, tmp_path / "out2")["meta"]["history"]
        assert first == second


class TestHistoryAbsent:
    def test_history_should_be_absent_when_repo_has_no_git_metadata(self, tmp_path):
        repo = tmp_path / "plain"
        repo.mkdir(parents=True, exist_ok=True)
        (repo / "app.py").write_text("x = 1\n", encoding="utf-8")
        index = _scan(repo, tmp_path / "out")
        assert "history" not in index["meta"]

    def test_history_should_be_absent_when_git_repo_has_no_commits(self, tmp_path):
        repo = tmp_path / "empty"
        _init_repo(repo)
        (repo / "app.py").write_text("x = 1\n", encoding="utf-8")
        index = _scan(repo, tmp_path / "out")
        assert "history" not in index["meta"]

    def test_history_cap_zero_should_disable_the_git_pull(self, tmp_path):
        repo = tmp_path / "repo"
        _init_repo(repo)
        _commit(repo, "feat: first", {"a.txt": "a\n"}, "2026-04-01T10:00:00Z")
        index = _scan(repo, tmp_path / "out", history_cap=0)
        assert "history" not in index["meta"]


class TestHistoryCli:
    def test_cli_history_flag_should_wire_into_run_scan(self, tmp_path):
        repo = tmp_path / "repo"
        _init_repo(repo)
        for i in range(3):
            _commit(repo, f"feat: c{i}", {"a.txt": f"{i}\n"}, f"2026-06-0{i + 1}T10:00:00Z")
        out = tmp_path / "cli" / "repo-index.json"
        code = si.main(["scan", "--repo", str(repo), "--out", str(out), "--history", "1"])
        assert code == 0
        index = json.loads(out.read_text(encoding="utf-8"))
        history = index["meta"]["history"]
        assert history["commit_subjects"] == ["feat: c2"]
        assert history["capped"] is True

    def test_cli_default_history_cap_should_be_200(self, tmp_path):
        repo = tmp_path / "repo"
        _init_repo(repo)
        _commit(repo, "feat: only", {"a.txt": "a\n"}, "2026-07-01T10:00:00Z")
        out = tmp_path / "default.json"
        code = si.main(["scan", "--repo", str(repo), "--out", str(out)])
        assert code == 0
        index = json.loads(out.read_text(encoding="utf-8"))
        assert index["meta"]["history"]["count"] == 1


class TestRenderHistory:
    def test_render_spec_scan_should_list_subjects_and_renames(self):
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
                "history": {
                    "count": 2,
                    "capped": True,
                    "commit_subjects": ["feat: b", "feat: a"],
                    "renames": [
                        {
                            "commit": "abc123",
                            "subject": "feat: b",
                            "old": "old.py",
                            "new": "new.py",
                        }
                    ],
                },
            },
        }
        md = si.render_spec_scan(index)
        assert "## Recent Git History (evidence)" in md
        assert "feat: b" in md
        assert "capped" in md
        assert "`old.py` → `new.py`" in md

    def test_render_spec_scan_should_say_absent_when_no_history(self):
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
        md = si.render_spec_scan(index)
        assert "No git metadata" in md


class TestRealRepo:
    def test_history_for_real_repo_should_match_latest_commit_subject(self):
        proc = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "log", "-1", "--format=%s"],
            capture_output=True,
            text=True,
            check=True,
        )
        history = si.collect_history(REPO_ROOT, 5)
        assert history is not None
        assert history["commit_subjects"][0] == proc.stdout.strip()

    def test_history_for_real_repo_should_include_rename_clues(self):
        history = si.collect_history(REPO_ROOT, 50)
        assert history is not None
        assert any(r["old"] != r["new"] for r in history["renames"]), (
            "real repo history contains renames (derived-spec-working move)"
        )
