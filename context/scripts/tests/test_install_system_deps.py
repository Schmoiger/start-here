"""Tests for the system-dependency bootstrap declared in the project manifest.

The script under test reads ``[tool.agent-harness.system-dependencies]`` from
``pyproject.toml``, probes each declared binary, and installs only the missing
ones. Probes and installs are injected so no real package manager runs in tests.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from context.scripts.setup import install_system_deps as deps

REPO_ROOT = Path(__file__).resolve().parents[3]

FAKE_MANIFEST = """
[tool.agent-harness.system-dependencies.fake-tool]
probe = ["fake-tool", "--version"]
install = { linux = "apt-get install -y fake", darwin = "brew install fake" }
"""


def _write_manifest(tmp_path: Path, body: str) -> Path:
    manifest = tmp_path / "pyproject.toml"
    manifest.write_text(body, encoding="utf-8")
    return manifest


def _never_available(_command: tuple[str, ...]) -> bool:
    return False


def _always_available(_command: tuple[str, ...]) -> bool:
    return True


class TestLoadSystemDependencies:
    def test_manifest_should_parse_probe_and_platform_install_commands(self, tmp_path: Path):
        loaded = deps.load_system_dependencies(_write_manifest(tmp_path, FAKE_MANIFEST))

        assert set(loaded) == {"fake-tool"}
        dep = loaded["fake-tool"]
        assert dep.name == "fake-tool"
        assert dep.probe == ("fake-tool", "--version")
        assert dep.install_command("linux") == "apt-get install -y fake"
        assert dep.install_command("darwin") == "brew install fake"
        assert dep.install_command("win32") is None

    def test_manifest_should_fall_back_to_default_install_command(self, tmp_path: Path):
        manifest = _write_manifest(
            tmp_path,
            """
[tool.agent-harness.system-dependencies.fake-tool]
probe = ["fake-tool"]
install = { default = "install-fake" }
""",
        )
        loaded = deps.load_system_dependencies(manifest)

        assert loaded["fake-tool"].install_command("linux") == "install-fake"

    def test_manifest_should_return_empty_when_section_is_absent(self, tmp_path: Path):
        manifest = _write_manifest(tmp_path, '[project]\nname = "x"\n')

        assert deps.load_system_dependencies(manifest) == {}

    def test_manifest_should_return_empty_when_parent_table_is_absent(self, tmp_path: Path):
        manifest = _write_manifest(tmp_path, "")

        assert deps.load_system_dependencies(manifest) == {}

    def test_manifest_should_reject_entry_without_probe(self, tmp_path: Path):
        manifest = _write_manifest(
            tmp_path,
            """
[tool.agent-harness.system-dependencies.broken]
install = { linux = "true" }
""",
        )

        with pytest.raises(ValueError, match="probe"):
            deps.load_system_dependencies(manifest)

    def test_manifest_should_reject_empty_probe_list(self, tmp_path: Path):
        manifest = _write_manifest(
            tmp_path,
            """
[tool.agent-harness.system-dependencies.broken]
probe = []
install = { linux = "true" }
""",
        )

        with pytest.raises(ValueError, match="probe"):
            deps.load_system_dependencies(manifest)

    def test_manifest_should_reject_entry_without_install_table(self, tmp_path: Path):
        manifest = _write_manifest(
            tmp_path,
            """
[tool.agent-harness.system-dependencies.broken]
probe = ["broken", "--version"]
""",
        )

        with pytest.raises(ValueError, match="install"):
            deps.load_system_dependencies(manifest)


class TestProbeDependency:
    def test_probe_should_succeed_for_an_installed_binary(self):
        dep = deps.SystemDependency(name="python", probe=(sys.executable, "--version"), install={})

        assert deps.probe_dependency(dep) is True

    def test_probe_should_fail_without_raising_for_a_missing_binary(self):
        dep = deps.SystemDependency(
            name="ghost", probe=("definitely-not-a-real-binary-9f2c", "--version"), install={}
        )

        assert deps.probe_dependency(dep) is False


class TestEnsureDependencies:
    def test_present_dependency_should_not_run_the_install_command(self, tmp_path: Path):
        manifest = _write_manifest(tmp_path, FAKE_MANIFEST)
        calls: list[str] = []

        def install_runner(command: str) -> bool:
            calls.append(command)
            return True

        outcome = deps.ensure_dependencies(
            manifest,
            platform_key="linux",
            probe_runner=_always_available,
            install_runner=install_runner,
        )

        assert outcome.present == ["fake-tool"]
        assert calls == []
        assert outcome.ok is True

    def test_missing_dependency_should_run_the_platform_install_command(self, tmp_path: Path):
        manifest = _write_manifest(tmp_path, FAKE_MANIFEST)
        calls: list[str] = []
        probed: list[tuple[str, ...]] = []

        def probe_runner(command: tuple[str, ...]) -> bool:
            probed.append(tuple(command))
            return len(probed) > 1  # missing before install, available after

        def install_runner(command: str) -> bool:
            calls.append(command)
            return True

        outcome = deps.ensure_dependencies(
            manifest,
            platform_key="darwin",
            probe_runner=probe_runner,
            install_runner=install_runner,
        )

        assert calls == ["brew install fake"]
        assert outcome.installed == ["fake-tool"]
        assert outcome.commands == {"fake-tool": "brew install fake"}
        assert outcome.ok is True

    def test_failed_install_should_be_reported_as_a_failure(self, tmp_path: Path):
        manifest = _write_manifest(tmp_path, FAKE_MANIFEST)

        outcome = deps.ensure_dependencies(
            manifest,
            platform_key="linux",
            probe_runner=_never_available,
            install_runner=lambda _command: False,
        )

        assert outcome.failed == ["fake-tool"]
        assert outcome.ok is False

    def test_install_that_leaves_the_binary_unavailable_should_fail(self, tmp_path: Path):
        manifest = _write_manifest(tmp_path, FAKE_MANIFEST)

        outcome = deps.ensure_dependencies(
            manifest,
            platform_key="linux",
            probe_runner=_never_available,
            install_runner=lambda _command: True,
        )

        assert outcome.failed == ["fake-tool"]
        assert outcome.installed == []

    def test_unknown_platform_should_be_reported_as_a_failure(self, tmp_path: Path):
        manifest = _write_manifest(tmp_path, FAKE_MANIFEST)

        outcome = deps.ensure_dependencies(
            manifest,
            platform_key="win32",
            probe_runner=_never_available,
            install_runner=lambda _command: True,
        )

        assert outcome.failed == ["fake-tool"]
        assert outcome.commands == {}

    def test_dry_run_should_report_the_command_without_executing_it(self, tmp_path: Path):
        manifest = _write_manifest(tmp_path, FAKE_MANIFEST)
        calls: list[str] = []

        def install_runner(command: str) -> bool:
            calls.append(command)
            return True

        outcome = deps.ensure_dependencies(
            manifest,
            platform_key="linux",
            dry_run=True,
            probe_runner=_never_available,
            install_runner=install_runner,
        )

        assert calls == []
        assert outcome.missing == ["fake-tool"]
        assert outcome.commands == {"fake-tool": "apt-get install -y fake"}

    def test_check_only_should_report_missing_without_executing_installs(self, tmp_path: Path):
        manifest = _write_manifest(tmp_path, FAKE_MANIFEST)
        calls: list[str] = []

        def install_runner(command: str) -> bool:
            calls.append(command)
            return True

        outcome = deps.ensure_dependencies(
            manifest,
            platform_key="linux",
            check_only=True,
            probe_runner=_never_available,
            install_runner=install_runner,
        )

        assert calls == []
        assert outcome.missing == ["fake-tool"]
        assert outcome.ok is False


class TestProjectManifest:
    def test_project_manifest_should_declare_ci_tooling_for_linux_and_darwin(self):
        loaded = deps.load_system_dependencies(REPO_ROOT / "pyproject.toml")

        assert {"ctags", "ast-grep"} <= set(loaded)
        for name in ("ctags", "ast-grep"):
            assert loaded[name].install_command("linux"), f"{name} has no linux install command"
            assert loaded[name].install_command("darwin"), f"{name} has no darwin install command"


class TestCli:
    def test_missing_manifest_should_exit_non_zero(self, tmp_path: Path):
        assert deps.main(["--manifest", str(tmp_path / "absent.toml")]) == 1

    def test_manifest_without_declarations_should_exit_zero(self, tmp_path: Path):
        manifest = _write_manifest(tmp_path, '[project]\nname = "x"\n')

        assert deps.main(["--manifest", str(manifest)]) == 0

    def test_invalid_declaration_should_exit_non_zero(self, tmp_path: Path):
        manifest = _write_manifest(
            tmp_path,
            """
[tool.agent-harness.system-dependencies.broken]
install = { linux = "true" }
""",
        )

        assert deps.main(["--manifest", str(manifest)]) == 1
