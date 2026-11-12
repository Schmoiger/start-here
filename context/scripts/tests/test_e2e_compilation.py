import shutil
from pathlib import Path

import pytest

from context.scripts.generators.adapters.core.loader import load_canonical_context
from context.scripts.generators.generate_adapters import (
    run_generation,
)
from context.scripts.validators.adapter_drift import check_adapter_drift


def test_e2e_full_compilation_all_targets(tmp_path: Path):
    """Validate end-to-end compilation of all 4 runtime adapters in an isolated environment."""
    repo_root = Path(__file__).resolve().parent.parent.parent.parent
    context_dir = repo_root / "context"

    # Copy context/ into sandbox tmp_path
    shutil.copytree(context_dir, tmp_path / "context", symlinks=True, ignore_dangling_symlinks=True)

    # Run full compilation across all targets
    result = run_generation(
        repo_root=tmp_path,
        context_dir=tmp_path / "context",
        targets={"all"},
        force=True,
    )

    created_files = result["created"] + result["updated"]
    assert len(created_files) >= 80

    # Expected projection count is derived from canonical definitions, not pinned
    # to the roster size — merges and retirements must not break this gate.
    expected_agents = len(
        [p for p in (context_dir / "agents").glob("*.md") if p.name != "README.md"]
    )

    # 1. Core verification
    assert (tmp_path / "AGENTS.md").is_file()
    agents_content = (tmp_path / "AGENTS.md").read_text()
    assert "# AGENTS.md" in agents_content
    # AGENTS.md is prose-only by design: the workflow/agent registry was dropped in
    # favour of the sections declared in context/workflows/agents-md.yaml, plus the
    # generator-owned Runtime Context section.
    assert "## Runtime Context" in agents_content
    assert "## Harness Context" in agents_content
    assert "## Project Context" in agents_content
    assert "## Workflows" not in agents_content
    assert "## Agents" not in agents_content

    # 2. Gemini / Antigravity verification
    assert (tmp_path / "GEMINI.md").is_file()
    gemini_content = (tmp_path / "GEMINI.md").read_text()
    assert "@AGENTS.md" in gemini_content
    skills_dir = tmp_path / ".agents" / "skills"
    assert skills_dir.is_dir()
    skill_files = list(skills_dir.glob("*/SKILL.md"))
    assert len(skill_files) >= 18

    # 3. Claude Code verification
    assert (tmp_path / "CLAUDE.md").is_file()
    claude_content = (tmp_path / "CLAUDE.md").read_text()
    assert "@AGENTS.md" in claude_content
    claude_prompts_dir = tmp_path / ".claude" / "prompts"
    assert claude_prompts_dir.is_dir()
    claude_prompts = list(claude_prompts_dir.glob("*.md"))
    assert len(claude_prompts) >= expected_agents

    # 4. GitHub Copilot verification
    assert (tmp_path / ".github" / "copilot-instructions.md").is_file()
    gh_prompts_dir = tmp_path / ".github" / "prompts"
    assert gh_prompts_dir.is_dir()
    gh_prompts = list(gh_prompts_dir.glob("*.prompt.md"))
    assert len(gh_prompts) >= expected_agents
    gh_instructions_dir = tmp_path / ".github" / "instructions"
    assert gh_instructions_dir.is_dir()
    assert len(list(gh_instructions_dir.glob("*.instructions.md"))) >= 3

    # 5. OpenAI / Codex verification
    openai_prompts_dir = tmp_path / ".openai" / "prompts"
    assert openai_prompts_dir.is_dir()
    openai_prompts = list(openai_prompts_dir.glob("*.txt"))
    assert len(openai_prompts) >= expected_agents
    assert (tmp_path / ".openai" / "tools.json").is_file()
    assert (tmp_path / ".openai" / "runner.py").is_file()

    # 6. Cline verification
    assert (tmp_path / "CLINE.md").is_file()
    cline_content = (tmp_path / "CLINE.md").read_text()
    assert "@AGENTS.md" in cline_content
    assert "execute_command" in cline_content
    assert (tmp_path / ".clinerules" / "00-core.md").is_file()
    cline_skills_dir = tmp_path / ".cline" / "skills"
    assert cline_skills_dir.is_dir()
    cline_skill_files = list(cline_skills_dir.glob("*/SKILL.md"))
    canonical_skill_count = len(load_canonical_context(str(context_dir))["skills"])
    assert len(cline_skill_files) >= canonical_skill_count

    # 7. Verify zero drift against validator
    is_synced, drift_issues = check_adapter_drift(
        repo_root=tmp_path,
        context_dir=tmp_path / "context",
        targets={"all"},
    )
    assert is_synced, f"Generated projections drifted: {drift_issues}"


def test_e2e_deterministic_reproducibility(tmp_path: Path):
    """Verify that repeated compilation produces byte-for-byte identical output."""
    repo_root = Path(__file__).resolve().parent.parent.parent.parent
    context_dir = repo_root / "context"
    shutil.copytree(context_dir, tmp_path / "context", symlinks=True, ignore_dangling_symlinks=True)

    # Run 1
    run_generation(
        repo_root=tmp_path,
        context_dir=tmp_path / "context",
        targets={"all"},
        force=True,
    )

    first_run_hashes: dict[str, str] = {}
    for f in tmp_path.rglob("*"):
        if f.is_file() and not str(f).startswith(str(tmp_path / "context")):
            first_run_hashes[str(f.relative_to(tmp_path))] = f.read_text()

    # Run 2 (forced full regeneration)
    run_generation(
        repo_root=tmp_path,
        context_dir=tmp_path / "context",
        targets={"all"},
        force=True,
    )

    second_run_hashes: dict[str, str] = {}
    for f in tmp_path.rglob("*"):
        if f.is_file() and not str(f).startswith(str(tmp_path / "context")):
            second_run_hashes[str(f.relative_to(tmp_path))] = f.read_text()

    assert first_run_hashes.keys() == second_run_hashes.keys()
    for rel_path, content1 in first_run_hashes.items():
        content2 = second_run_hashes[rel_path]
        assert content1 == content2, f"File {rel_path} differed between compilation runs"


def test_e2e_synthetic_context_compilation(tmp_path: Path):
    """Verify compilation with a minimal synthetic context directory."""
    synth_context = tmp_path / "context"
    agents_dir = synth_context / "agents"
    workflows_dir = synth_context / "workflows"
    rules_dir = synth_context / "rules"
    standards_dir = synth_context / "standards"

    agents_dir.mkdir(parents=True)
    workflows_dir.mkdir(parents=True)
    rules_dir.mkdir(parents=True)
    standards_dir.mkdir(parents=True)

    # 1 synthetic agent
    (agents_dir / "custom-bot.md").write_text(
        "---\n"
        "name: custom-bot\n"
        "description: Performs automated custom tasks.\n"
        "standards:\n"
        "  - custom-standards.md\n"
        "rules:\n"
        "  - custom-rule.md\n"
        "---\n\n"
        "# Custom Bot\n\nCustom bot body.\n"
    )

    # 1 synthetic workflow
    (workflows_dir / "sample-flow.yaml").write_text(
        "name: sample-flow\n"
        "description: Sample automated workflow.\n"
        "steps:\n"
        "  - name: step-1\n"
        "    agent: custom-bot\n"
    )

    # AGENTS.md content source — mandatory input for the generator since
    # context/workflows/agents-md.yaml became the single source of AGENTS.md prose.
    (workflows_dir / "agents-md.yaml").write_text(
        "title: AGENTS.md\n"
        "description: Synthetic AGENTS.md source.\n"
        "sections:\n"
        "  - name: Harness Context\n"
        "    content: |\n"
        "      - Synthetic harness bullet.\n"
        "  - name: Project Context\n"
        "    content: |\n"
        "      - Synthetic project bullet.\n"
    )

    # 1 synthetic standard with applyTo
    (standards_dir / "custom-standards.md").write_text(
        "# Custom Standards\n\n"
        "## Deployment Safety\n"
        '<!-- applyTo: "custom/**/*.py" -->\n\n'
        "Safety instructions.\n"
    )

    # 1 synthetic rule
    (rules_dir / "custom-rule.md").write_text("# Custom Rule\n\nRule details.\n")

    # Run compilation on synthetic context
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    result = run_generation(
        repo_root=output_dir,
        context_dir=synth_context,
        targets={"all"},
        force=True,
    )

    assert len(result["created"]) > 0
    assert (output_dir / "AGENTS.md").is_file()
    synthetic_agents_content = (output_dir / "AGENTS.md").read_text()
    assert "## Harness Context" in synthetic_agents_content
    assert "Synthetic harness bullet." in synthetic_agents_content
    assert (output_dir / "GEMINI.md").is_file()
    assert (output_dir / "CLAUDE.md").is_file()
    assert (output_dir / "CLINE.md").is_file()
    assert (output_dir / ".clinerules" / "00-core.md").is_file()
    assert (output_dir / ".agents" / "skills" / "custom-bot" / "SKILL.md").is_file()
    assert (output_dir / ".claude" / "prompts" / "custom-bot.md").is_file()
    assert (output_dir / ".github" / "prompts" / "custom-bot.prompt.md").is_file()
    assert (output_dir / ".openai" / "prompts" / "custom-bot.txt").is_file()


def test_e2e_synthetic_context_without_agents_md_source_fails_loudly(tmp_path: Path):
    """AGENTS.md generation must fail loudly when the declared source file is absent.

    ``context/workflows/agents-md.yaml`` is a mandatory input, not a fallback: a
    missing source would otherwise silently emit an AGENTS.md with no sections.
    """
    synth_context = tmp_path / "context"
    for subdir in ("agents", "workflows", "rules", "standards"):
        (synth_context / subdir).mkdir(parents=True)

    (synth_context / "agents" / "custom-bot.md").write_text(
        "---\n"
        "name: custom-bot\n"
        "description: Performs automated custom tasks.\n"
        "---\n\n"
        "# Custom Bot\n\nCustom bot body.\n"
    )

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    with pytest.raises(FileNotFoundError, match="agents-md.yaml"):
        run_generation(
            repo_root=output_dir,
            context_dir=synth_context,
            targets={"all"},
            force=True,
        )
