#!/usr/bin/env python3
"""Bootstrap system (non-Python) dependencies declared in the project manifest.

`pyproject.toml` is the single source of truth for the external binaries the test
suite and the spec indexer rely on. Each dependency is declared under
``[tool.agent-harness.system-dependencies.<name>]`` with:

- ``probe``: the command used to detect the binary (exit code 0 == available).
- ``install``: a table of shell commands keyed by ``platform.system().lower()``,
  with an optional ``default`` fallback.

The script probes every declared dependency and installs only the missing ones, so
a machine that already has the tooling pays one probe per tool and nothing else.
CI runs this before the test suite; a bare runner image therefore bootstraps itself
from the manifest instead of failing a test with ``FileNotFoundError``.

Usage::

    uv run python context/scripts/setup/install_system_deps.py
    uv run python context/scripts/setup/install_system_deps.py --check
    uv run python context/scripts/setup/install_system_deps.py --dry-run
"""

from __future__ import annotations

import argparse
import platform
import subprocess
import sys
import tomllib
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
MANIFEST_PATH = REPO_ROOT / "pyproject.toml"

# Location of the declaration table inside the project manifest.
MANIFEST_SECTION: tuple[str, ...] = ("tool", "agent-harness", "system-dependencies")

PROBE_TIMEOUT_SECONDS = 30
INSTALL_TIMEOUT_SECONDS = 600

ProbeRunner = Callable[[Sequence[str]], bool]
InstallRunner = Callable[[str], bool]


@dataclass(frozen=True)
class SystemDependency:
    """A single external binary declared in the project manifest."""

    name: str
    probe: tuple[str, ...]
    install: Mapping[str, str]

    def install_command(self, platform_key: str) -> str | None:
        """Return the install command for ``platform_key``, falling back to ``default``."""
        return self.install.get(platform_key) or self.install.get("default")


@dataclass
class DependencyOutcome:
    """Result of reconciling declared dependencies against the host environment."""

    present: list[str] = field(default_factory=list)
    installed: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    failed: list[str] = field(default_factory=list)
    commands: dict[str, str] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        """True when nothing failed and nothing is still missing."""
        return not self.failed and not self.missing


def _run_command(command: Sequence[str], timeout: int) -> bool:
    """Run a command, returning True only on exit code 0. Never raises."""
    try:
        proc = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired):
        return False
    return proc.returncode == 0


def _probe_command(command: Sequence[str]) -> bool:
    """Default probe runner: execute the declared probe command."""
    return _run_command(command, PROBE_TIMEOUT_SECONDS)


def _install_command(command: str) -> bool:
    """Default install runner: execute through bash so ``&&`` and ``sudo`` work."""
    return _run_command(["bash", "-lc", command], INSTALL_TIMEOUT_SECONDS)


def load_system_dependencies(manifest_path: Path = MANIFEST_PATH) -> dict[str, SystemDependency]:
    """Parse declared system dependencies from the project manifest.

    Args:
        manifest_path: Path to the ``pyproject.toml`` holding the declarations.

    Returns:
        Mapping of dependency name to its declaration. Empty when the section is absent.

    Raises:
        ValueError: If a declaration is structurally invalid.
    """
    data = tomllib.loads(manifest_path.read_text(encoding="utf-8"))

    section: object = data
    for key in MANIFEST_SECTION:
        if not isinstance(section, dict):
            return {}
        section = section.get(key, {})
    if not isinstance(section, dict):
        raise ValueError(f"'{'.'.join(MANIFEST_SECTION)}' must be a table in {manifest_path}")

    dependencies: dict[str, SystemDependency] = {}
    for name, spec in section.items():
        if not isinstance(spec, dict):
            raise ValueError(f"system dependency '{name}' must be a table in {manifest_path}")

        probe = spec.get("probe")
        if (
            not isinstance(probe, list)
            or not probe
            or not all(isinstance(part, str) for part in probe)
        ):
            raise ValueError(
                f"system dependency '{name}' needs a non-empty 'probe' list of strings"
            )

        install = spec.get("install")
        if not isinstance(install, dict) or not install:
            raise ValueError(f"system dependency '{name}' needs an 'install' table")
        if not all(isinstance(k, str) and isinstance(v, str) for k, v in install.items()):
            raise ValueError(f"system dependency '{name}' install commands must be strings")

        dependencies[name] = SystemDependency(
            name=name,
            probe=tuple(probe),
            install=dict(install),
        )
    return dependencies


def probe_dependency(dep: SystemDependency, probe_runner: ProbeRunner = _probe_command) -> bool:
    """Report whether ``dep`` is already available on this host."""
    return probe_runner(dep.probe)


def ensure_dependencies(
    manifest_path: Path = MANIFEST_PATH,
    *,
    platform_key: str | None = None,
    check_only: bool = False,
    dry_run: bool = False,
    probe_runner: ProbeRunner = _probe_command,
    install_runner: InstallRunner = _install_command,
) -> DependencyOutcome:
    """Probe declared dependencies and install the missing ones.

    Args:
        manifest_path: Path to the project manifest.
        platform_key: Install-command key to select; defaults to ``platform.system().lower()``.
        check_only: Report missing dependencies without installing them.
        dry_run: Report the install command that would run, without running it.
        probe_runner: Injectable probe executor (tests pass a stub).
        install_runner: Injectable install executor (tests pass a stub).

    Returns:
        A :class:`DependencyOutcome` describing what was present, installed, missing or failed.
    """
    resolved_platform = platform_key or platform.system().lower()
    outcome = DependencyOutcome()

    for name, dep in sorted(load_system_dependencies(manifest_path).items()):
        if probe_dependency(dep, probe_runner):
            outcome.present.append(name)
            continue

        command = dep.install_command(resolved_platform)
        if command is None:
            outcome.failed.append(name)
            continue

        outcome.commands[name] = command
        if check_only or dry_run:
            outcome.missing.append(name)
            continue

        if not install_runner(command):
            outcome.failed.append(name)
            continue

        # Re-probe: a "successful" install that leaves the binary off PATH is still a failure.
        if probe_dependency(dep, probe_runner):
            outcome.installed.append(name)
        else:
            outcome.failed.append(name)

    return outcome


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point. Returns the process exit code."""
    parser = argparse.ArgumentParser(
        prog="install-system-deps",
        description=(
            "Install system (non-Python) dependencies declared in the project manifest "
            "([tool.agent-harness.system-dependencies] in pyproject.toml)."
        ),
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=MANIFEST_PATH,
        help="Project manifest to read (default: <repo-root>/pyproject.toml).",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report missing dependencies without installing them.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the install commands without executing them.",
    )
    args = parser.parse_args(argv)

    if not args.manifest.is_file():
        print(f"❌ Project manifest not found: {args.manifest}")
        return 1

    try:
        dependencies = load_system_dependencies(args.manifest)
    except (OSError, ValueError, tomllib.TOMLDecodeError) as exc:
        print(f"❌ Could not read system dependencies: {exc}")
        return 1

    if not dependencies:
        print(f"ℹ️  No system dependencies declared in {args.manifest}.")
        return 0

    print(f"🔧 System dependencies declared in {args.manifest}:")
    outcome = ensure_dependencies(
        args.manifest,
        check_only=args.check,
        dry_run=args.dry_run,
    )

    for name in outcome.present:
        print(f"  ✅ {name} — already available")
    for name in outcome.installed:
        print(f"  ✅ {name} — installed")
    for name in outcome.missing:
        label = "would run" if args.dry_run else "missing"
        print(f"  ⬇️  {name} — {label}: {outcome.commands[name]}")
    for name in outcome.failed:
        detail = outcome.commands.get(name, "no install command for this platform")
        print(f"  ❌ {name} — {detail}")

    if outcome.ok:
        print("✅ All declared system dependencies are available.")
        return 0

    print("❌ System dependency bootstrap incomplete. Fix the entries above and re-run:")
    print("  uv run python context/scripts/setup/install_system_deps.py")
    return 1


if __name__ == "__main__":
    sys.exit(main())
