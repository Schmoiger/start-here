#!/usr/bin/env python3
"""Generic import boundary enforcer.

Reads boundaries from context/scripts/validators/import-boundaries.yaml and
enforces that specified import patterns only appear in allowed directories.

Usage (invoked by pre-commit):
    uv run python context/scripts/validators/import_boundaries.py <file> [<file> ...]

Config format (import-boundaries.yaml):
    boundaries:
      - name: "supabase isolation"
        import_pattern: "^\\s*(import supabase|from supabase\\b)"
        allowed_in:
          - "services/database-service/"
        message: "supabase must only be imported in database-service"
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: uv add --dev pyyaml", file=sys.stderr)
    sys.exit(2)

CONFIG_PATH = Path(__file__).resolve().parent / "import-boundaries.yaml"
REPO_ROOT = Path(__file__).resolve().parents[3]


def load_boundaries() -> list[dict]:
    if not CONFIG_PATH.exists():
        return []
    with CONFIG_PATH.open() as f:
        data = yaml.safe_load(f)
    return data.get("boundaries", []) if data else []


def is_allowed(file_path: Path, allowed_in: list[str]) -> bool:
    try:
        rel = str(file_path.relative_to(REPO_ROOT))
    except ValueError:
        rel = str(file_path)
    return any(rel.startswith(allowed) for allowed in allowed_in)


def main() -> int:
    boundaries = load_boundaries()
    if not boundaries:
        return 0

    violations: list[str] = []

    for path_str in sys.argv[1:]:
        path = Path(path_str).resolve()
        try:
            text = path.read_text()
        except Exception:
            continue
        for boundary in boundaries:
            pattern = re.compile(boundary["import_pattern"], re.MULTILINE)
            allowed_in = boundary.get("allowed_in", [])
            if pattern.search(text) and not is_allowed(path, allowed_in):
                msg = boundary.get(
                    "message",
                    f"Import boundary violation: {boundary.get('name', boundary['import_pattern'])}",
                )
                violations.append(f"  {path_str}: {msg}")

    if violations:
        print("Import boundary violations:", file=sys.stderr)
        for v in violations:
            print(v, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
