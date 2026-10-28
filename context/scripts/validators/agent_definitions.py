#!/usr/bin/env python3
# /// script
# dependencies = [
#   "pyyaml",
# ]
# ///
from __future__ import annotations

"""Validate agent definition structural integrity (context/agents/*.md).

Checks:
1. Valid YAML frontmatter with required 'name' and 'model' fields.
2. Referenced standards, rules, and skills exist on disk.
3. No hardcoded absolute paths or ./artefacts/ paths.
4. Presence of the canonical 'Context Acquisition' body section
   (see context/templates/agent-template.md). Legacy 'Required Standards' /
   'Required Rules' body sections are rejected — the frontmatter is the single
   source of truth and the template defines the body shape.
5. Critical reminders include source attribution.
6. Body attributions resolve — every 'Source' cell in a body rule table and
   every inline `file.md §section` citation names a file that exists under
   `context/`, and, when a section is given, a heading that file carries.
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
CONTEXT_DIR = REPO_ROOT / "context"
AGENTS_DIR = CONTEXT_DIR / "agents"

SKIPPED_FILES = {"TEMPLATE.md", "MODEL-RECOMMENDATIONS.md"}

# Canonical body section defined by context/templates/agent-template.md.
CONTEXT_ACQUISITION_HEADING = "## Context Acquisition"

# Interruption logs are one rolling file per task (context/templates/logging-template.md
# § Interruption Log). Legacy per-agent or per-timestamp names are drift.
INTERRUPTIONS_PATH_PATTERN = re.compile(r"artefacts/build/interruptions/([^\s`)\]|]+)")
INTERRUPTION_LOG_NAME_PATTERN = re.compile(r"^\{task-id\}\.jsonl$")

# Body attributions. A body rule table may attribute a constraint to its source
# through a 'Source' column, and constraint bullets carry `file.md §section`
# citations. Both are references to a rule, skill or standard: one that does not
# resolve is the same defect class as a phantom frontmatter entry — the agent is
# told to read something that is not there, then paraphrases from memory.
SOURCE_COLUMN_NAME = "source"
# `file.md` is the placeholder agent-template.md uses to illustrate the
# citation shape; it is not a reference to a file on disk.
PLACEHOLDER_CITATIONS = {"file.md"}
CITATION_PATTERN = re.compile(
    r"`?(?P<file>[A-Za-z0-9_][A-Za-z0-9_./-]*\.md)`?(?:\s*§\s*(?P<section>[^§`|;\n]*))?"
)
CITATION_SEARCH_DIRS = (
    "rules",
    "skills",
    "standards",
    "agents",
    "templates",
    "workflows",
    "docs",
)
HEADING_PATTERN = re.compile(r"^#{1,6}\s+(?P<title>.+?)\s*$")
TABLE_SEPARATOR_PATTERN = re.compile(r"^:?-{2,}:?$")


def _normalise_title(text: str) -> str:
    """Fold a heading or citation section into comparable words."""
    folded = re.sub(r"[^a-z0-9]+", " ", text.strip().lower())
    return re.sub(r"\s+", " ", folded).strip()


def _without_number(title: str) -> str:
    """Drop the leading '1.' / '2.6.' style numbering from a normalised heading."""
    return re.sub(r"^\d+(?:\s+\d+)*\s*", "", title)


def _headings(path: Path) -> list[str]:
    """Return the file's headings, normalised for comparison with a citation."""
    try:
        content = path.read_text()
    except (OSError, UnicodeDecodeError):
        return []
    return [
        _normalise_title(match.group("title"))
        for line in content.splitlines()
        if (match := HEADING_PATTERN.match(line))
    ]


def _is_prefix(short: str, long: str) -> bool:
    """True when `short` is `long` or a whole-word prefix of it."""
    return bool(short) and (long == short or long.startswith(f"{short} "))


def _section_resolves(section: str, headings: list[str]) -> bool:
    """True when the cited section names a heading the file actually carries.

    Citations are written for humans, so they abbreviate (`§1 British English`
    for `1. British English Spelling & Invariants`), cite a number alone
    (`§6`), or trail into prose. Each of those still resolves; a name that
    matches no heading does not.
    """
    target = _normalise_title(section)
    if not target:
        return True
    if any(
        _is_prefix(target, heading)
        or _is_prefix(heading, target)
        or _is_prefix(_without_number(heading), target)
        for heading in headings
    ):
        return True
    number = re.match(r"^\d+(?:\s+\d+)*", target)
    return bool(number) and any(
        _is_prefix(number.group(0), heading) for heading in headings
    )


def _resolve_context_file(name: str, ctx: Path) -> Path | None:
    """Resolve a citation to a file under `context/`, or a repo-relative path."""
    if name.startswith(("context/", "artefacts/")):
        candidate = REPO_ROOT / name
        return candidate if candidate.exists() else None
    if (candidate := ctx / name).exists():
        return candidate
    for directory in CITATION_SEARCH_DIRS:
        if (candidate := ctx / directory / name).exists():
            return candidate
    return None


def _source_cells(body: str) -> list[tuple[int, str]]:
    """Return (line number, cell) for every 'Source' cell in the body tables."""
    cells: list[tuple[int, str]] = []
    source_index: int | None = None
    for number, line in enumerate(body.splitlines(), 1):
        stripped = line.strip()
        if not stripped.startswith("|"):
            source_index = None
            continue
        row = [cell.strip() for cell in stripped.strip("|").split("|")]
        if source_index is None:
            # First row after prose is the header for this table.
            names = [_normalise_title(cell) for cell in row]
            source_index = names.index(SOURCE_COLUMN_NAME) if SOURCE_COLUMN_NAME in names else -1
            continue
        if source_index < 0 or source_index >= len(row):
            continue
        if all(TABLE_SEPARATOR_PATTERN.match(cell or "") for cell in row):
            continue
        cells.append((number, row[source_index]))
    return cells


def _validate_body_citations(body: str, ctx: Path, line_offset: int = 0) -> list[str]:
    """Resolve every body attribution: Source cells and inline citations.

    `line_offset` is the number of file lines before the body, so diagnostics
    quote the line number an editor would show.
    """
    errors: list[str] = []
    seen: set[str] = set()

    def check(name: str, section: str | None, location: str) -> None:
        if name in PLACEHOLDER_CITATIONS:
            return
        path = _resolve_context_file(name, ctx)
        cited = (section or "").strip().rstrip(".,;:)`")
        if path is None:
            message = f"Body source doesn't exist: {name} ({location})"
        elif cited and not _section_resolves(cited, _headings(path)):
            message = f"Body source section doesn't exist: {name} §{cited} ({location})"
        else:
            return
        if message not in seen:
            seen.add(message)
            errors.append(message)

    for number, cell in _source_cells(body):
        for match in CITATION_PATTERN.finditer(cell):
            check(match.group("file"), match.group("section"), f"line {number + line_offset}")

    for number, line in enumerate(body.splitlines(), 1):
        for match in CITATION_PATTERN.finditer(line):
            if match.group("section") is not None:
                check(
                    match.group("file"),
                    match.group("section"),
                    f"line {number + line_offset}",
                )

    return errors


def validate_agent_definition(
    file_path: Path,
    context_root: Path | None = None,
) -> list[str]:
    """Validate a single agent definition markdown file."""
    ctx = context_root or CONTEXT_DIR
    errors: list[str] = []

    try:
        content = file_path.read_text()
    except (OSError, UnicodeDecodeError) as e:
        return [f"Unable to read file: {e}"]

    # Extract frontmatter
    if not content.startswith("---"):
        errors.append("Missing YAML frontmatter")
        return errors

    parts = content.split("---", 2)
    if len(parts) < 3:
        errors.append("Invalid YAML frontmatter structure")
        return errors

    try:
        frontmatter = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        errors.append(f"Invalid YAML: {e}")
        return errors

    if not isinstance(frontmatter, dict):
        errors.append("YAML frontmatter must be a mapping")
        return errors

    # Check required frontmatter fields
    for field in ["name", "model"]:
        if field not in frontmatter:
            errors.append(f"Missing required field: {field}")

    # Validate standards references
    if "standards" in frontmatter and isinstance(frontmatter["standards"], list):
        for standard in frontmatter["standards"]:
            standard_path = ctx / "standards" / standard
            if not standard_path.exists():
                errors.append(f"Referenced standard doesn't exist: {standard}")

    # Validate rules references
    if "rules" in frontmatter and isinstance(frontmatter["rules"], list):
        for rule in frontmatter["rules"]:
            rule_path = ctx / "rules" / rule
            if not rule_path.exists():
                errors.append(f"Referenced rule doesn't exist: {rule}")

    # Validate skills references
    if "skills" in frontmatter and isinstance(frontmatter["skills"], list):
        for skill in frontmatter["skills"]:
            skill_path = ctx / "skills" / skill
            if not skill_path.exists():
                errors.append(f"Referenced skill doesn't exist: {skill}")

    # Check for hardcoded absolute paths
    body = parts[2]
    if "/Users/" in body or "/home/" in body:
        errors.append("Contains hardcoded absolute paths")

    # Check for {project-root} usage instead of relative paths
    if "./artefacts/" in body:
        errors.append("Contains relative paths - use {project-root}/artefacts/ instead")

    # Check for Critical Reminders section and attribution
    if "Critical Reminders" in body:
        reminder_match = re.search(r"## Critical Reminders.*?(?=##|$)", body, re.DOTALL)
        if reminder_match:
            reminders = reminder_match.group(0)
            for line in reminders.split("\n"):
                stripped = line.strip()
                if stripped.startswith("- ") and "(" not in stripped:
                    errors.append(f"Reminder missing attribution: {stripped}")

    # The frontmatter declares which standards, rules and skills apply; the
    # body's 'Context Acquisition' section instructs the agent to read them.
    # Both are required, and the heading is exact — context/templates/
    # agent-template.md is the only source of definition shape, so a body
    # carrying a legacy heading is drift, not a variant.
    if CONTEXT_ACQUISITION_HEADING not in body:
        errors.append(
            f"Missing '{CONTEXT_ACQUISITION_HEADING}' section "
            "(copy the body structure from context/templates/agent-template.md)"
        )

    # Interruption logs follow the template's one-log-per-task contract. Wildcard
    # references (e.g. reading all logs) are allowed; concrete names must be
    # '{task-id}.jsonl'.
    for match in INTERRUPTIONS_PATH_PATTERN.finditer(body):
        referenced = match.group(1).rstrip(".,;:")
        if referenced.startswith("*") or INTERRUPTION_LOG_NAME_PATTERN.match(referenced):
            continue
        errors.append(
            "Interruption log path must be "
            "'artefacts/build/interruptions/{task-id}.jsonl' "
            f"(found '{referenced}') — one rolling log per task"
        )

    # Body attributions resolve or the definition is lying about what it read.
    # The frontmatter checks above cannot see a body table that cites a file
    # deleted last quarter; this is the same check applied to the body.
    body_line_offset = content[: len(content) - len(body)].count("\n")
    errors.extend(_validate_body_citations(body, ctx, body_line_offset))

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate agent definition structural integrity (context/agents/*.md)"
    )
    parser.add_argument("files", nargs="*", help="Agent definition files to validate")
    args = parser.parse_args()

    if args.files:
        files = [Path(f) for f in args.files if Path(f).is_file()]
    else:
        if not AGENTS_DIR.exists():
            print(f"❌ {AGENTS_DIR} directory not found", file=sys.stderr)
            return 1
        files = [
            f for f in AGENTS_DIR.glob("*.md")
            if f.name not in SKIPPED_FILES
        ]

    all_errors: dict[str, list[str]] = {}
    agent_count = 0

    for agent_file in sorted(files):
        if agent_file.name in SKIPPED_FILES:
            continue

        agent_count += 1
        errors = validate_agent_definition(agent_file)
        if errors:
            all_errors[agent_file.name] = errors

    if all_errors:
        print(f"❌ Validation failed for {len(all_errors)}/{agent_count} agents:\n", file=sys.stderr)
        for fname, errs in all_errors.items():
            print(f"{fname}:", file=sys.stderr)
            for err in errs:
                print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"✅ All {agent_count} agent definitions valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
