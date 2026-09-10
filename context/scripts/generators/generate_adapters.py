import os
from pathlib import Path

from context.scripts.generators.adapters.core.loader import load_canonical_context
from context.scripts.generators.adapters.gemini.generator import (
    generate_gemini_md,
    generate_skills,
)
from context.scripts.generators.adapters.github.generator import (
    generate_copilot_instructions,
    generate_prompts,
    generate_scoped_instructions,
)
from context.scripts.generators.adapters.openai.generator import (
    generate_runner_harness,
    generate_system_prompts,
    generate_tool_schemas,
)


def main():
    repo_root = Path(__file__).resolve().parent.parent.parent.parent
    context_dir = repo_root / "context"
    
    # Load Canonical IR
    context = load_canonical_context(str(context_dir))
    
    # Generate Gemini/Antigravity Projections
    generate_skills(context, repo_root)
    generate_gemini_md(context, repo_root)
    print("Successfully generated Gemini projections.")

    # Generate GitHub Projections
    generate_copilot_instructions(context, repo_root)
    generate_prompts(context, repo_root)
    generate_scoped_instructions(repo_root)
    print("Successfully generated GitHub projections.")

    # Generate OpenAI Projections
    generate_system_prompts(context, repo_root)
    generate_tool_schemas(context, repo_root)
    generate_runner_harness(repo_root)
    print("Successfully generated OpenAI projections.")


if __name__ == "__main__":
    main()
