#!/usr/bin/env python3
"""
Verify and enforce Typst-friendly Markdown formatting rules.

Rules enforced:
1. Double line spacing (at least 2 blank lines) following mermaid diagrams / diagram blocks.
2. Horizontal rule ('---') preceding major section headings (level 2 headings '## '),
   ensuring consistent section separation for Typst document generation.
3. Process-model hygiene: a non-table prose line inside a Process/Flow/Workflow/
   Sequence section carrying three or more inline numbered steps ("1. … 2. … 3. …")
   is a prose process model and must be rendered as a Mermaid diagram instead
   (doc-standards.md §6.1; hint at the `mermaid-authoring` skill,
   `context/skills/mermaid-authoring.md`, in the violation message).

Usage:
    uv run python context/scripts/validators/verify_typst_formatting.py [files...]
    uv run python context/scripts/validators/verify_typst_formatting.py --fix [files...]
    uv run python context/scripts/validators/verify_typst_formatting.py --staged
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

# Matches an inline numbered step marker (placed at line start or after
# whitespace) where the step begins with a capital letter, e.g. "1. Read",
# "2. Resolve". Only the step number is captured.
PROCESS_STEP_MARKER_RE = re.compile(r"(?:^|\s)(\d{1,2})\.\s+[A-Z]")

# A single line needs this many inline step markers to be treated as a prose
# process model rather than ordinary prose that happens to mention "1. x 2. y".
# A single line needs this many inline step markers to be treated as a prose
# process model rather than ordinary prose that happens to mention "1. x 2. y".
PROCESS_MODEL_STEP_THRESHOLD = 3

# Section headings (##/###) whose title contains one of these mark a
# process-model context; only prose there is checked, so MC-option lists
# (appendix) and task-file enumerations are not flagged.
PROCESS_HEADING_KEYWORDS = ("process", "flow", "workflow", "sequence")
PROCESS_MODEL_STEP_THRESHOLD = 3


def get_repo_root() -> Path:
    """Return git repository root or fallback to script grandparent."""
    try:
        res = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
        return Path(res.stdout.strip()).resolve()
    except (subprocess.SubprocessError, FileNotFoundError):
        return Path(__file__).resolve().parent.parent.parent


TYPST_DIRS = ("typst", "docs/drafts")


def is_typst_doc(rel_path: str) -> bool:
    """Return True if rel_path is inside a designated Typst document directory."""
    return any(rel_path == d or rel_path.startswith(f"{d}/") for d in TYPST_DIRS)


def get_staged_markdown_files(repo_root: Path) -> list[Path]:
    """Return list of staged markdown files in Typst document directories."""
    cmd = ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"]
    res = subprocess.run(cmd, cwd=repo_root, capture_output=True, text=True, check=False)
    files: list[Path] = []
    for line in res.stdout.splitlines():
        rel = line.strip()
        if not rel or not rel.endswith(".md") or not is_typst_doc(rel):
            continue
        p = (repo_root / rel).resolve()
        if p.exists() and p.is_file():
            files.append(p)
    return files


def get_tracked_markdown_files(repo_root: Path) -> list[Path]:
    """Return list of tracked markdown files in Typst document directories."""
    files: list[Path] = []
    for d in TYPST_DIRS:
        dir_path = repo_root / d
        if dir_path.is_dir():
            files.extend(sorted(dir_path.rglob("*.md")))
    return files


def check_prose_process_models(path: Path) -> list[str]:
    """Flag prose lines that read as process models inside process sections.

    A non-table prose line inside a Process/Flow/Workflow/Sequence section
    that carries three or more inline numbered steps ("1. do X 2. do Y 3. do Z",
    as in the B-009 architecture Process Model) is a prose process model and
    should be rendered as a Mermaid diagram (doc-standards.md §6.1;
    mermaid-authoring skill). Table rows, Mermaid / other code fences,
    `<!-- typst-skip -->` regions, and prose outside a process-marked section
    are excluded to avoid flagging MC-option lists and task-file enumerations.
    """
    errors: list[str] = []
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return errors

    in_mermaid = False
    in_code_block = False
    in_typst_skip = False
    in_process_section = False

    for lineno, line in enumerate(content.splitlines(), start=1):
        stripped = line.strip()
        if stripped == "<!-- typst-skip-start -->":
            in_typst_skip = True
            continue
        if stripped == "<!-- typst-skip-end -->":
            in_typst_skip = False
            continue
        if stripped == "```mermaid":
            in_mermaid = True
            in_code_block = True
            continue
        if stripped.startswith("```"):
            if in_mermaid:
                in_mermaid = False
                in_code_block = False
            else:
                in_code_block = not in_code_block
            continue

        # Track process-model section context from ATX headings.
        if stripped.startswith("#") and not in_code_block and not in_typst_skip:
            heading_title = re.sub(r"^#{1,6}\s*", "", stripped).lower()
            in_process_section = any(
                kw in heading_title for kw in PROCESS_HEADING_KEYWORDS
            )
            continue

        if in_typst_skip or in_mermaid or in_code_block:
            continue
        # Tabular flow representation (Markdown table rows) is not prose.
        if stripped.startswith("|"):
            continue
        if not in_process_section:
            continue

        markers = PROCESS_STEP_MARKER_RE.findall(line)
        if len(markers) >= PROCESS_MODEL_STEP_THRESHOLD:
            errors.append(
                f"{path}:{lineno} Prose process model (inline numbered steps "
                f"{', '.join(markers)}) should be rendered as a Mermaid diagram "
                "(doc-standards.md §6.1). See the **mermaid-authoring** skill at "
                "`context/skills/mermaid-authoring.md` for syntax and layout"
            )
    return errors


def check_and_fix_file(path: Path, fix: bool = False) -> list[str]:
    """
    Check a markdown file for Typst formatting requirements.

    Returns a list of error descriptions (if any).
    If fix is True, writes updated content when violations can be auto-remediated.
    """
    errors: list[str] = []
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        # Skip broken symlinks or files with restricted access
        return errors
    lines = content.splitlines()

    new_lines: list[str] = []
    modified = False

    in_mermaid = False
    in_code_block = False
    i = 0
    total_lines = len(lines)

    # Track if we are inside typst-skip blocks
    in_typst_skip = False

    while i < total_lines:
        line = lines[i]
        stripped = line.strip()

        if stripped == "<!-- typst-skip-start -->":
            in_typst_skip = True
        elif stripped == "<!-- typst-skip-end -->":
            in_typst_skip = False

        # Detect mermaid fence start/end
        if stripped == "```mermaid":
            in_mermaid = True
            in_code_block = True
            new_lines.append(line)
            i += 1
            continue

        if in_mermaid and stripped == "```":
            in_mermaid = False
            in_code_block = False
            new_lines.append(line)

            # Count following blank lines
            blank_count = 0
            peek = i + 1
            while peek < total_lines and not lines[peek].strip():
                blank_count += 1
                peek += 1

            if peek < total_lines and blank_count < 2:
                errors.append(
                    f"{path}:{i + 1} Mermaid diagram fence must be followed by at least 2 blank lines (found {blank_count})"
                )
                if fix:
                    new_lines.extend(["", ""])
                    modified = True
                    i = peek  # skip original blanks and resume at next content
                    continue
            i += 1
            continue

        if stripped.startswith("```"):
            in_code_block = not in_code_block
            new_lines.append(line)
            i += 1
            continue

        # Check section separation for level 2 headings '## '
        # (Exclude '# Title', '## Table of Contents', and headings inside typst-skip or code blocks)
        if (
            stripped.startswith("## ")
            and not in_typst_skip
            and not in_mermaid
            and not in_code_block
        ):
            heading_title = stripped[3:].strip()
            if heading_title.lower() != "table of contents":
                # Check previous non-blank line in new_lines
                prev_idx = len(new_lines) - 1
                while prev_idx >= 0 and not new_lines[prev_idx].strip():
                    prev_idx -= 1

                prev_content = new_lines[prev_idx].strip() if prev_idx >= 0 else ""
                if prev_content != "---":
                    errors.append(
                        f"{path}:{i + 1} Section heading '## {heading_title}' must be preceded by '---' horizontal rule"
                    )
                    if fix:
                        # Ensure there is a blank line before '---' unless at start
                        if prev_idx >= 0 and new_lines and new_lines[-1].strip():
                            new_lines.append("")
                        new_lines.append("---")
                        new_lines.append("")
                        modified = True

        new_lines.append(line)
        i += 1

    if fix and modified:
        # Preserve trailing newline
        new_content = "\n".join(new_lines)
        if content.endswith("\n") and not new_content.endswith("\n"):
            new_content += "\n"
        path.write_text(new_content, encoding="utf-8")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Typst-specific Markdown formatting rules.")
    parser.add_argument("files", nargs="*", type=Path, help="Markdown files to check")
    parser.add_argument("--fix", action="store_true", help="Auto-fix violations where possible")
    parser.add_argument("--staged", action="store_true", help="Check git staged markdown files")

    args = parser.parse_args()
    repo_root = get_repo_root()

    target_files: list[Path] = []
    if args.staged:
        target_files = get_staged_markdown_files(repo_root)
        if not target_files:
            return 0
    elif args.files:
        for f in args.files:
            p = f.resolve()
            if p.is_dir():
                target_files.extend(sorted(p.rglob("*.md")))
            elif p.is_file() and p.suffix == ".md":
                target_files.append(p)
            elif not p.exists():
                continue
    else:
        target_files = get_tracked_markdown_files(repo_root)

    all_errors: list[str] = []
    process_errors: list[str] = []
    for file_path in target_files:
        if not file_path.exists() or file_path.suffix != ".md":
            continue
        all_errors.extend(check_and_fix_file(file_path, fix=args.fix))
        process_errors.extend(check_prose_process_models(file_path))

    # Process-model violations are not auto-fixable, so they always fail.
    if process_errors:
        print("Process-model check failed:", file=sys.stderr)
        for err in process_errors:
            print(f"  - {err}", file=sys.stderr)
        print("\nRender the flagged process model as a Mermaid diagram.", file=sys.stderr)
        return 1

    if all_errors and not args.fix:
        print("Typst formatting check failed:", file=sys.stderr)
        for err in all_errors:
            print(f"  - {err}", file=sys.stderr)
        print("\nRun with '--fix' to automatically remediate formatting issues.", file=sys.stderr)
        return 1

    if args.fix and all_errors:
        print(f"Fixed {len(all_errors)} Typst formatting violation(s).")
    else:
        print(f"Typst formatting check passed ({len(target_files)} file(s) checked).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
