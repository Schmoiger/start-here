#!/usr/bin/env python3
"""Frontend design system compliance validator — project template.

This file is a TEMPLATE. Before activating it, fill in the PROJECT_CONFIG
section below with your project's design conventions.

Active checks (always on once hooked):
- CSS architecture: only one CSS file allowed (frontend/src/index.css);
  no component-scoped CSS files elsewhere.

Inactive checks (fill in PROJECT_CONFIG to activate):
- Semantic colour enforcement: disallow concrete colour classes (e.g. text-red-500)
  in favour of semantic tokens defined by your design system.
- Component library import discipline: disallow direct library imports outside
  a barrel file (e.g. enforce all icon imports go through one barrel).
- Spacing scale: restrict className spacing tokens to a declared set.

To activate this validator, add to .pre-commit-config.yaml:
    - id: design-system
      name: Design system compliance
      language: python
      entry: uv run python context/scripts/validators/design_system.py
      types: [file]
      pass_filenames: false

Run from repo root. Exits 0 if compliant, 1 with violations on stderr.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# PROJECT_CONFIG — fill in for your project
# ---------------------------------------------------------------------------

# Path to your frontend source directory (relative to repo root).
FRONTEND_SRC_REL = "frontend/src"

# The single allowed CSS entry-point. All other .css files are violations.
# Set to None to disable the CSS architecture check.
ALLOWED_CSS_FILE_REL: str | None = "frontend/src/index.css"

# --- Colour enforcement (leave empty dict to disable) ---
# Map: human-readable rule name → compiled regex pattern that flags violations.
# The check fires on TSX/JSX files (excluding test/spec files).
# Example: disallow raw Tailwind colour classes, enforce DaisyUI semantic tokens.
DISALLOWED_COLOUR_PATTERNS: dict[str, re.Pattern] = {}
# DISALLOWED_COLOUR_PATTERNS = {
#     "concrete Tailwind colour (use semantic token instead)": re.compile(
#         r"(?:text|bg|border)-(?:green|red|amber|yellow|blue|gray|slate|zinc|neutral|stone)-\d+(?:/\d+)?"
#     ),
# }

# --- Component library barrel enforcement (leave empty list to disable) ---
# List of (import_pattern, barrel_file_substring, error_message) tuples.
# Files whose path contains barrel_file_substring are exempt.
BARREL_IMPORT_RULES: list[tuple[re.Pattern, str, str]] = []
# BARREL_IMPORT_RULES = [
#     (
#         re.compile(r"from\s+['\"]@heroicons/react"),
#         "HeroIcons",  # exempt files whose path contains this string
#         "import from '@heroicons/react' — use barrel from components/icons/HeroIcons.tsx",
#     ),
# ]

# --- Spacing scale enforcement (leave empty set to disable) ---
# Set of allowed spacing className tokens. Any other spacing token is a violation.
ALLOWED_SPACING_TOKENS: set[str] = set()
# ALLOWED_SPACING_TOKENS = {"gap-1", "gap-2", "gap-4", "p-2", "p-4", "px-4"}
# DISALLOWED_SPACING_PATTERN = re.compile(
#     r"\b(?:gap|p|px|py|pt|pb|pl|pr)-[0-9]+(?:\.[0-9]+)?\b"
# )

# ---------------------------------------------------------------------------
# Checks — do not modify unless you are adapting the validator itself
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[3]


def check_css_files() -> list[str]:
    """Enforce single CSS entry-point: only ALLOWED_CSS_FILE_REL is permitted."""
    if ALLOWED_CSS_FILE_REL is None:
        return []
    frontend_src = REPO_ROOT / FRONTEND_SRC_REL
    if not frontend_src.exists():
        return []
    allowed = {(REPO_ROOT / ALLOWED_CSS_FILE_REL).resolve()}
    violations = []
    for f in frontend_src.rglob("*.css"):
        if f.resolve() not in allowed:
            violations.append(
                f"  {f.relative_to(REPO_ROOT)}: component-scoped CSS not allowed"
                f" (only {ALLOWED_CSS_FILE_REL} is permitted)"
            )
    return violations


def check_tsx_files() -> list[str]:
    """Run colour, barrel, and spacing checks on TSX/JSX source files."""
    if not (DISALLOWED_COLOUR_PATTERNS or BARREL_IMPORT_RULES or ALLOWED_SPACING_TOKENS):
        return []
    frontend_src = REPO_ROOT / FRONTEND_SRC_REL
    if not frontend_src.exists():
        return []

    violations: list[str] = []

    for ext in ("*.tsx", "*.jsx"):
        for path in frontend_src.rglob(ext):
            if "__tests__" in path.parts or ".test." in path.name or ".spec." in path.name:
                continue
            try:
                content = path.read_text()
            except Exception as e:
                violations.append(f"  {path.relative_to(REPO_ROOT)}: read error — {e}")
                continue
            rel = path.relative_to(REPO_ROOT)

            for i, line in enumerate(content.splitlines(), 1):
                for rule_name, pattern in DISALLOWED_COLOUR_PATTERNS.items():
                    for m in pattern.finditer(line):
                        violations.append(
                            f"{rel}:{i}: {rule_name} '{m.group(0).strip()}'"
                        )
                for import_pattern, barrel_exempt, message in BARREL_IMPORT_RULES:
                    if barrel_exempt in str(path):
                        continue
                    if import_pattern.search(line):
                        violations.append(f"{rel}:{i}: {message}")

    return violations


def main() -> int:
    if not (REPO_ROOT / FRONTEND_SRC_REL).exists():
        print(f"Frontend src '{FRONTEND_SRC_REL}' not found; skipping.", file=sys.stderr)
        return 0

    all_violations = check_css_files() + check_tsx_files()

    if all_violations:
        print("Design system violations:\n", file=sys.stderr)
        for v in all_violations:
            print(v, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
