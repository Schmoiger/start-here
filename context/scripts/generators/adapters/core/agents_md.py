from pathlib import Path
from typing import Any

import yaml


def generate_agents_md(
    context: dict[str, Any],
    output_dir: Path,
    dry_run: bool = False,
    source_file: Path | None = None,
    runtime_context_bullets: list[str] | None = None,
) -> dict[Path, str]:
    """Generates AGENTS.md from a YAML source file.

    Args:
        context: Canonical context dictionary (retained for signature compatibility,
          but not used when source_file is provided).
        output_dir: Directory to write AGENTS.md into.
        dry_run: Preview only, do not write.
        source_file: Required path to YAML file defining AGENTS.md sections.
        runtime_context_bullets: Optional list of bullet lines injected into the
          "Runtime Context" section.

    Raises:
        ValueError: If source_file is None.
        FileNotFoundError: If source_file does not exist.
    """
    if source_file is None:
        raise ValueError("source_file is required for AGENTS.md generation")

    if not source_file.is_file():
        raise FileNotFoundError(f"AGENTS.md source file not found: {source_file}")

    with source_file.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}

    sections = data.get("sections", [])
    if not sections:
        raise ValueError(f"No sections found in source file: {source_file}")

    # Build Runtime Context section dynamically if bullets are provided.
    runtime_context_section = ""
    if runtime_context_bullets:
        bullets = "\n".join(f"{b}" for b in runtime_context_bullets)
        runtime_context_section = f"---\n\n## Runtime Context\n\n{bullets}\n\n"

    # Render remaining sections (skip Runtime Context if already generated above
    # to avoid duplication — the source file should not define Runtime Context
    # when runtime_context_bullets is supplied).
    body_parts: list[str] = []
    for section in sections:
        name = section.get("name", "Untitled")
        if name == "Runtime Context" and runtime_context_section:
            # Source-defined Runtime Context is superseded by dynamic bullets.
            continue
        content = section.get("content", "")
        body_parts.append(f"---\n\n## {name}\n\n{content}\n\n")

    # Insert Runtime Context section at the top if we have dynamic bullets.
    if runtime_context_section:
        body_parts.insert(0, runtime_context_section)

    agents_path = output_dir / "AGENTS.md"
    content = "# AGENTS.md\n\n" + "".join(body_parts)

    if not dry_run:
        agents_path.write_text(content)
    return {agents_path: content}
