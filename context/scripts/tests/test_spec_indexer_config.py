"""T-016 tests: config extraction (env templates, settings/config modules, config data files).

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
sys.modules[_spec.name] = si
_spec.loader.exec_module(si)

ENV_TEMPLATE = """# demo template
LOG_LEVEL=info
DATABASE_URL=postgres://user:pass@localhost/db
ENABLE_RETRY=true
QUOTED_VALUE="hello world"
EMPTY_VALUE=
"""

SETTINGS_PY = '''"""settings module"""
import os

DEBUG = True
FEATURE_BETA = "on"
API_KEY = "sk-live-1234"
RETRY_COUNT = os.getenv("RETRY_COUNT", "3")
TOKEN = os.environ.get("TOKEN")
'''


def _write_tree(repo: Path, files: dict[str, str]) -> Path:
    for rel, text in files.items():
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return repo


def _scan(repo: Path, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "repo-index.json"
    code = si.run_scan(repo, "both", out, 2000, False, "auto")
    assert code == 0, f"run_scan returned {code}"
    return json.loads(out.read_text(encoding="utf-8"))


def _config_map(index: dict) -> dict[str, dict]:
    return {e["key"]: e for e in index["config"]}


class TestConfigSources:
    def test_env_template_extraction(self, tmp_path):
        repo = _write_tree(tmp_path, {".env.example": ENV_TEMPLATE})
        index = _scan(repo, tmp_path / "out")
        cfg = _config_map(index)
        assert cfg["LOG_LEVEL"]["value_hint"] == "info"
        assert cfg["LOG_LEVEL"]["source"] == ".env.example"
        assert cfg["LOG_LEVEL"]["line"] == 2
        # feature flag by key naming
        assert cfg["ENABLE_RETRY"]["feature"] is True
        # quotes stripped; secrets redacted
        assert cfg["QUOTED_VALUE"]["value_hint"] == "hello world"
        assert cfg["DATABASE_URL"]["value_hint"] == "<redacted>"
        # empty values still produce a key, with an empty hint
        assert cfg["EMPTY_VALUE"]["value_hint"] == ""

    def test_python_settings_module(self, tmp_path):
        repo = _write_tree(tmp_path, {"settings.py": SETTINGS_PY})
        index = _scan(repo, tmp_path / "out")
        cfg = _config_map(index)
        assert cfg["DEBUG"]["value_hint"] == "True"
        assert cfg["DEBUG"]["feature"] is True  # boolean value
        assert cfg["FEATURE_BETA"]["feature"] is True
        assert cfg["API_KEY"]["value_hint"] == "<redacted>"
        # os.getenv with default: the default becomes the value-hint
        assert cfg["RETRY_COUNT"]["value_hint"] == "3"
        assert cfg["RETRY_COUNT"]["source"] == "settings.py"
        assert cfg["RETRY_COUNT"]["line"] > 0
        # env read without a default still records the key (redacted hint for TOKEN)
        assert cfg["TOKEN"]["value_hint"] == "<redacted>"

    def test_yaml_config_file(self, tmp_path):
        repo = _write_tree(
            tmp_path,
            {
                "config.yaml": (
                    "app_name: demo\n"
                    "ENABLE_CACHE: true\n"
                    "max_connections: 10\n"
                    "nested:\n"
                    "  ignored: true\n"
                )
            },
        )
        index = _scan(repo, tmp_path / "out")
        cfg = _config_map(index)
        assert cfg["app_name"]["value_hint"] == "demo"
        assert cfg["app_name"]["line"] == 1
        assert cfg["ENABLE_CACHE"]["feature"] is True
        assert cfg["max_connections"]["value_hint"] == "10"
        assert "ignored" not in cfg  # nested structures are not value-hints

    def test_json_config_file(self, tmp_path):
        repo = _write_tree(
            tmp_path,
            {"appsettings.json": '{"Name": "demo", "FeatureB": true, "Nested": {"x": 1}}'},
        )
        index = _scan(repo, tmp_path / "out")
        cfg = _config_map(index)
        assert cfg["Name"]["value_hint"] == "demo"
        assert cfg["Name"]["line"] == 1
        assert cfg["FeatureB"]["feature"] is True  # boolean value
        assert "Nested" not in cfg

    def test_non_config_files_ignored(self, tmp_path):
        repo = _write_tree(
            tmp_path,
            {
                # non-config python module: UPPER_CASE constant + env read must not leak
                "main.py": "X = 1\nimport os\ny = os.getenv('IGNORED_KEY')\n",
                "package.json": '{"name": "x"}\n',
                "openapi.yaml": "openapi: 3.0.0\n",
                "models.yaml": "user:\n  name: a\n",
            },
        )
        index = _scan(repo, tmp_path / "out")
        for key in ("X", "IGNORED_KEY", "name", "openapi", "user"):
            assert key not in _config_map(index)

    def test_precedence_first_source_wins(self, tmp_path):
        # same key in settings.py (highest precedence) and .env.example
        repo = _write_tree(
            tmp_path,
            {"settings.py": "RETRY_COUNT = 5\n", ".env.example": "RETRY_COUNT=3\n"},
        )
        index = _scan(repo, tmp_path / "out")
        assert len(index["config"]) == 1
        entry = _config_map(index)["RETRY_COUNT"]
        assert entry["value_hint"] == "5"
        assert entry["source"] == "settings.py"

    def test_determinism(self, tmp_path):
        repo = _write_tree(
            tmp_path,
            {
                "settings.py": SETTINGS_PY,
                ".env.example": ENV_TEMPLATE,
                "config.yaml": "app_name: demo\n",
            },
        )
        keys_1 = [e["key"] for e in _scan(repo, tmp_path / "out1")["config"]]
        keys_2 = [e["key"] for e in _scan(repo, tmp_path / "out2")["config"]]
        assert keys_1 == keys_2


class TestConfigVerify:
    def test_verify_index_covers_config_citations(self, tmp_path):
        repo = _write_tree(tmp_path, {".env.example": ENV_TEMPLATE, "settings.py": SETTINGS_PY})
        index_path = tmp_path / "out" / "repo-index.json"
        _scan(repo, tmp_path / "out")
        assert si.run_verify(index_path, repo, None, False) == 0
        # break the config citations: settings.py disappears → verify must fail
        (repo / "settings.py").unlink()
        assert si.run_verify(index_path, repo, None, False) == 1


class TestRealRepo:
    def test_start_here_env_template_keys_redacted(self):
        cfg = {e.key: e for e in si.collect_config(REPO_ROOT)}
        assert "UPSTREAM_PUSH_TOKEN" in cfg
        assert cfg["SUPABASE_URL"].value_hint == "<redacted>"
        assert cfg["UPSTREAM_PUSH_TOKEN"].value_hint == "<redacted>"
        assert cfg["SUPABASE_URL"].source == ".env.template"