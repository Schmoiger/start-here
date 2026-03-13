#!/usr/bin/env python3
"""Validate context/ directory integrity.

Checks that all agent, rule, and standard references resolve correctly.

Usage:
    uv run python context/scripts/validators/validate_context.py
"""

import sys
from pathlib import Path

import yaml


# Directories relative to project root
CONTEXT_DIR = Path("context")
AGENTS_DIR = CONTEXT_DIR / "agents"
RULES_DIR = CONTEXT_DIR / "rules"
STANDARDS_DIR = CONTEXT_DIR / "standards"
WORKFLOWS_DIR = CONTEXT_DIR / "workflows"
TEMPLATES_DIR = CONTEXT_DIR / "templates"

# Agents excluded from orphan detection (utility/meta files)
EXCLUDED_AGENT_FILES = {"TEMPLATE.md", "README.md", "MODEL-RECOMMENDATIONS.md"}

WORKFLOW_FILE = WORKFLOWS_DIR / "build.yaml"
TASK_PROMPT_TEMPLATE = TEMPLATES_DIR / "task-prompt-template.md"


def load_workflow(path: Path) -> dict:
    """Load and parse a workflow YAML file."""
    with path.open() as f:
        return yaml.safe_load(f)


def agents_in_workflow(workflow: dict) -> set[str]:
    """Extract all agent names referenced in workflow phases."""
    names: set[str] = set()
    for phase in workflow.get("phases", []):
        for agent in phase.get("agents", []):
            # Strip inline comments (e.g. "tech-lead  # Decompose sprint...")
            name = agent.split("#")[0].strip() if isinstance(agent, str) else agent
            if name:
                names.add(name)
    return names


def defined_agents() -> set[str]:
    """Return agent names from definition files in context/agents/."""
    names: set[str] = set()
    for path in AGENTS_DIR.glob("*.md"):
        if path.name in EXCLUDED_AGENT_FILES:
            continue
        content = path.read_text()
        if not content.startswith("---"):
            continue
        parts = content.split("---", 2)
        if len(parts) < 3:
            continue
        try:
            fm = yaml.safe_load(parts[1])
            if fm and "name" in fm:
                names.add(fm["name"])
        except yaml.YAMLError:
            continue
    return names


def agent_file_map() -> dict[str, Path]:
    """Return mapping of agent name to definition file path."""
    mapping: dict[str, Path] = {}
    for path in AGENTS_DIR.glob("*.md"):
        if path.name in EXCLUDED_AGENT_FILES:
            continue
        content = path.read_text()
        if not content.startswith("---"):
            continue
        parts = content.split("---", 2)
        if len(parts) < 3:
            continue
        try:
            fm = yaml.safe_load(parts[1])
            if fm and "name" in fm:
                mapping[fm["name"]] = path
        except yaml.YAMLError:
            continue
    return mapping


def agent_references(agent_path: Path) -> tuple[list[str], list[str]]:
    """Extract rules and standards listed in an agent's frontmatter."""
    content = agent_path.read_text()
    if not content.startswith("---"):
        return [], []
    parts = content.split("---", 2)
    if len(parts) < 3:
        return [], []
    try:
        fm = yaml.safe_load(parts[1])
        if not fm:
            return [], []
        rules = fm.get("rules", []) or []
        standards = fm.get("standards", []) or []
        return rules, standards
    except yaml.YAMLError:
        return [], []


def main() -> int:
    """Run all validation checks. Returns 0 on PASS, 1 on FAIL."""
    print("Validating context/...")
    errors: list[str] = []
    warnings: list[str] = []

    # --- Check 1: workflow file exists and parses ---
    if not WORKFLOW_FILE.exists():
        errors.append(f"Workflow file not found: {WORKFLOW_FILE}")
        print(f"  ❌ {errors[-1]}")
        print("FAIL")
        return 1

    try:
        workflow = load_workflow(WORKFLOW_FILE)
    except yaml.YAMLError as exc:
        errors.append(f"build.yaml failed to parse: {exc}")
        print(f"  ❌ {errors[-1]}")
        print("FAIL")
        return 1
    referenced_agents = agents_in_workflow(workflow)
    file_map = agent_file_map()
    all_defined = defined_agents()

    # --- Check 2: every agent in build.yaml has a definition file ---
    missing_agents = []
    for agent in sorted(referenced_agents):
        if agent not in all_defined:
            missing_agents.append(agent)

    if missing_agents:
        for agent in missing_agents:
            msg = f"Agent '{agent}' referenced in build.yaml but not found in context/agents/"
            errors.append(msg)
            print(f"  ❌ {msg}")
    else:
        print(f"  ✅ All {len(referenced_agents)} agents in build.yaml have definition files")

    # --- Check 3: rule references resolve ---
    broken_rules: list[str] = []
    for agent_name in sorted(referenced_agents):
        if agent_name not in file_map:
            continue
        rules, _ = agent_references(file_map[agent_name])
        for rule in rules:
            rule_path = RULES_DIR / rule
            if not rule_path.exists():
                broken_rules.append(
                    f"Agent '{agent_name}' references missing rule: {rule}"
                )

    if broken_rules:
        for msg in broken_rules:
            errors.append(msg)
            print(f"  ❌ {msg}")
    else:
        print("  ✅ All rule references resolve")

    # --- Check 4: standard references resolve ---
    broken_standards: list[str] = []
    for agent_name in sorted(referenced_agents):
        if agent_name not in file_map:
            continue
        _, standards = agent_references(file_map[agent_name])
        for standard in standards:
            std_path = STANDARDS_DIR / standard
            if not std_path.exists():
                broken_standards.append(
                    f"Agent '{agent_name}' references missing standard: {standard}"
                )

    if broken_standards:
        for msg in broken_standards:
            errors.append(msg)
            print(f"  ❌ {msg}")
    else:
        print("  ✅ All standard references resolve")

    # --- Check 5: task-prompt-template.md exists ---
    if not TASK_PROMPT_TEMPLATE.exists():
        msg = f"task-prompt-template.md not found at {TASK_PROMPT_TEMPLATE}"
        errors.append(msg)
        print(f"  ❌ {msg}")
    else:
        print("  ✅ task-prompt-template.md exists")

    # --- Warning: orphan agents (defined but not in build.yaml) ---
    orphan_agents = sorted(all_defined - referenced_agents)
    if orphan_agents:
        warnings.append(f"Orphan agents (not in build.yaml): {', '.join(orphan_agents)}")
        print(f"  ⚠️  {warnings[-1]}")

    # --- Final result ---
    if errors:
        print("FAIL")
        return 1

    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
