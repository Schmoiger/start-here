from __future__ import annotations

import textwrap
from pathlib import Path

from context.scripts.validators.verify_typst_formatting import (
    check_and_fix_file,
    check_prose_process_models,
)


def _write(tmp_path: Path, name: str, content: str) -> Path:
    p = tmp_path / name
    p.write_text(textwrap.dedent(content).lstrip("\n"), encoding="utf-8")
    return p


def test_clean_doc_has_no_process_model_errors(tmp_path: Path) -> None:
    p = _write(
        tmp_path,
        "doc.md",
        """
        # Title

        ---

        ## Section

        Ordinary prose that mentions a single step.

        ---

        ## Process Model

        ```mermaid
        flowchart TD
            A --> B
        ```
        """,
    )
    assert check_prose_process_models(p) == []
    assert check_and_fix_file(p) == []


def test_flags_inline_prose_process_model(tmp_path: Path) -> None:
    p = _write(
        tmp_path,
        "doc.md",
        """
        # Title

        ## Process Model

        1. Read the agent definition. 2. Resolve applicable rules. 3. Assign disjoint scopes.
        """,
    )
    errs = check_prose_process_models(p)
    assert len(errs) == 1
    assert "Mermaid" in errs[0]
    assert "1" in errs[0] and "2" in errs[0] and "3" in errs[0]
    # Message must point the fixing agent at the authoring skill.
    assert "mermaid-authoring" in errs[0]
    assert "context/skills/mermaid-authoring.md" in errs[0]


def test_mermaid_and_code_fences_are_excluded(tmp_path: Path) -> None:
    p = _write(
        tmp_path,
        "doc.md",
        """
        # Title

        ```mermaid
        flowchart TD
            A --> B
        ```

        ```text
        1. not a model 2. still not 3. a model
        ```
        """,
    )
    assert check_prose_process_models(p) == []


def test_typst_skip_region_is_excluded(tmp_path: Path) -> None:
    p = _write(
        tmp_path,
        "doc.md",
        """
        # Title

        <!-- typst-skip-start -->
        1. skipped 2. skipped 3. skipped
        <!-- typst-skip-end -->
        """,
    )
    assert check_prose_process_models(p) == []


def test_fewer_than_three_steps_allowed_in_process_section(tmp_path: Path) -> None:
    p = _write(
        tmp_path,
        "doc.md",
        """
        # Title

        ## Process Model

        1. First step. 2. Second step.
        """,
    )
    assert check_prose_process_models(p) == []


def test_prose_outside_process_section_not_flagged(tmp_path: Path) -> None:
    # Three inline markers on one line, but not inside a process-marked section
    # (open-questions MC options) — must not be flagged.
    p = _write(
        tmp_path,
        "doc.md",
        """
        # Title

        ## Open Questions

        1. Keep unified. 2. Split per runtime. 3. Add onboarding flow.
        """,
    )
    assert check_prose_process_models(p) == []


def test_table_rows_in_flow_section_not_flagged(tmp_path: Path) -> None:
    # Tabular flow representation (a "Steps (call chain)" column) is not prose.
    p = _write(
        tmp_path,
        "doc.md",
        """
        # Title

        ## User Flows

        | Flow | Steps (call chain) |
        |------|--------------------|
        | Derive Spec | 1. Intake -> 2. Scan -> 3. Profile -> 4. Draft |
        """,
    )
    assert check_prose_process_models(p) == []
