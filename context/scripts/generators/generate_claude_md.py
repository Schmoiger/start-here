#!/usr/bin/env python3
"""Generate CLAUDE.md orchestration guide from context directory.

Usage:
    uv run python context/scripts/generators/generate-claude-md.py [--workflow default|prototype]
"""

import argparse
import sys
from pathlib import Path
from typing import Any
import yaml
import re


def load_workflow(workflow_name: str) -> dict[str, Any]:
    """Load workflow YAML file."""
    workflow_path = Path('context/workflows') / f'{workflow_name}.yaml'

    if not workflow_path.exists():
        print(f"❌ Workflow not found: {workflow_path}")
        sys.exit(1)

    with workflow_path.open() as f:
        return yaml.safe_load(f)


def load_agent_definitions() -> dict[str, dict]:
    """Load all agent definitions."""
    agents = {}
    agents_dir = Path('context/agents')

    for agent_file in agents_dir.glob('*.md'):
        if agent_file.name in ['TEMPLATE.md', 'README.md', 'MODEL-RECOMMENDATIONS.md']:
            continue

        content = agent_file.read_text()

        # Extract frontmatter
        if not content.startswith('---'):
            continue

        parts = content.split('---', 2)
        if len(parts) < 3:
            continue

        try:
            frontmatter = yaml.safe_load(parts[1])
            agents[frontmatter['name']] = {
                'frontmatter': frontmatter,
                'content': parts[2].strip()
            }
        except (yaml.YAMLError, KeyError):
            continue

    return agents


def extract_description(agent_content: str) -> str:
    """Extract role description from agent content."""
    # Look for first paragraph after frontmatter
    lines = agent_content.split('\n')
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('#'):
            return stripped

    return "Agent description not found"


def generate_workflow_diagram(workflow: dict) -> str:
    """Generate Mermaid diagram from workflow phases."""
    lines = ["```mermaid", "flowchart TD"]

    phases = workflow.get('phases', [])

    for i, phase in enumerate(phases):
        phase_id = phase['id']
        phase_name = phase.get('name', phase_id)
        agents = phase.get('agents', [])

        # Create phase subgraph
        lines.append(f'    subgraph {phase_id}["{phase_name}"]')

        # List agents in phase
        for agent in agents:
            agent_id = f"{phase_id}_{agent.replace('-', '_')}"
            lines.append(f'        {agent_id}["@{agent}"]')

        lines.append('    end')

        # Add dependencies
        if 'depends_on' in phase:
            for dep in phase['depends_on']:
                lines.append(f'    {dep} --> {phase_id}')
        elif i == 0:
            # First phase, no dependencies
            pass
        else:
            # Connect to previous phase if no explicit dependencies
            prev_phase_id = phases[i-1]['id']
            if 'depends_on' not in phase:
                lines.append(f'    {prev_phase_id} --> {phase_id}')

        # Mark gates
        if phase.get('gate'):
            lines.append(f'    {phase_id}:::gateStyle')

    # Add styling
    lines.append('    classDef gateStyle fill:#ff6b6b,stroke:#c92a2a,stroke-width:3px')
    lines.append("```")

    return '\n'.join(lines)


def generate_phase_details(workflow: dict, agents: dict) -> str:
    """Generate detailed phase descriptions."""
    sections = []

    for phase in workflow.get('phases', []):
        phase_id = phase['id']
        phase_name = phase.get('name', phase_id)
        phase_agents = phase.get('agents', [])

        section = [f"#### {phase_name}"]
        section.append(f"**Phase ID**: `{phase_id}`")

        if 'depends_on' in phase:
            deps = ', '.join(f"`{d}`" for d in phase['depends_on'])
            section.append(f"**Depends On**: {deps}")

        if phase.get('parallel'):
            section.append("**Execution**: Parallel (agents run simultaneously)")

        if phase.get('sequential'):
            section.append("**Execution**: Sequential (agents run in order)")

        if phase.get('optional'):
            section.append("**Optional**: Can be skipped")

        if phase.get('gate'):
            section.append("**Quality Gate**: ⚠️ Approval required before proceeding")

        section.append("\n**Agents:**")
        for agent_name in phase_agents:
            if agent_name in agents:
                section.append(f"- `@{agent_name}` - See `context/agents/{agent_name}.md`")
            else:
                section.append(f"- `@{agent_name}`")

        if 'outputs' in phase:
            section.append("\n**Outputs:**")
            for output in phase['outputs']:
                section.append(f"- {output}")

        if 'validation' in phase:
            section.append("\n**Validation:**")
            for validation in phase['validation']:
                section.append(f"- {validation}")

        if 'notes' in phase:
            section.append("\n**Notes:**")
            for note in phase['notes']:
                section.append(f"- {note}")

        sections.append('\n'.join(section))

    return '\n\n'.join(sections)


def generate_agent_reference(agents: dict) -> str:
    """Generate agent reference section."""
    sections = []

    # Group agents by category
    categories = {
        'Discovery': ['product-owner'],
        'Design': ['solution-architect', 'database-designer', 'api-designer', 'ui-designer', 'visual-designer'],
        'Development': ['functional-tester', 'python-coder', 'typescript-coder'],
        'Review': ['tech-lead', 'code-reviewer'],
        'Testing': ['ui-tester', 'security-tester'],
        'Deployment': ['gcp-devops'],
        'Documentation': ['documentation']
    }

    for category, agent_names in categories.items():
        section = [f"### {category}"]

        for agent_name in agent_names:
            if agent_name in agents:
                section.append(f"\n**@{agent_name}** - See `context/agents/{agent_name}.md`")

        sections.append('\n'.join(section))

    return '\n\n'.join(sections)


def generate_quality_gates(workflow: dict) -> str:
    """Generate quality gates section."""
    gates = workflow.get('quality_gates', [])

    if not gates:
        return "No quality gates defined for this workflow."

    sections = []
    for gate in gates:
        phase = gate.get('phase', 'unknown')
        gate_type = gate.get('type', 'unknown')
        desc = gate.get('description', '')
        required = gate.get('required', False)

        section = [f"#### {phase.replace('-', ' ').title()}"]
        section.append(f"**Type**: {gate_type}")
        section.append(f"**Required**: {'Yes' if required else 'No'}")
        section.append(f"\n{desc}")

        if 'criteria' in gate:
            section.append("\n**Criteria:**")
            for criterion in gate['criteria']:
                metric = criterion.get('metric')
                threshold = criterion.get('threshold')
                operator = criterion.get('operator')
                section.append(f"- {metric} {operator} {threshold}")

        sections.append('\n'.join(section))

    return '\n\n'.join(sections) if sections else "No quality gates defined."


def generate_workflow_rules(workflow: dict) -> str:
    """Generate workflow rules section."""
    rules = workflow.get('workflow_rules', [])
    warnings = workflow.get('warnings', [])

    sections = []

    if rules:
        sections.append("### Workflow Rules\n")
        for rule in rules:
            sections.append(f"- {rule}")

    if warnings:
        sections.append("\n### Warnings\n")
        for warning in warnings:
            sections.append(f"{warning}")

    return '\n'.join(sections) if sections else "No specific workflow rules defined."


def generate_claude_md(workflow_name: str) -> str:
    """Generate complete CLAUDE.md content."""
    workflow = load_workflow(workflow_name)
    agents = load_agent_definitions()

    workflow_desc = workflow.get('description', '')

    template = f"""# Multi-Agent Orchestration Guide

**Generated from**: `context/` directory
**Workflow**: `{workflow_name}` - {workflow_desc}
**Auto-generated**: Do not edit manually. Run `uv run python context/scripts/generators/generate-claude-md.py` to regenerate.

---

## Overview

This guide describes the orchestration of specialised agents for software development tasks. Each agent has specific capabilities, follows defined standards, and produces specific outputs.

**Context Directory**: All standards, rules, and agent definitions are in `context/`. See [context/README.md](context/README.md) for complete index.

**Orchestrator**: When spawning agents, use the task prompt template at `context/templates/TASK-PROMPT-TEMPLATE.md`. The template ensures agents read their definition file and receive consistent task structure. Never inline agent definitions—agents will read them from `context/agents/{{agent-name}}.md`. See [workflow-standards.md §8](context/standards/workflow-standards.md#8-orchestrator-agent-invocation).

---

## Workflow: {workflow.get('name', workflow_name)}

{workflow_desc}

### Workflow Diagram

{generate_workflow_diagram(workflow)}

### Phases

{generate_phase_details(workflow, agents)}

---

## Agent Reference

All agents are defined in `context/agents/`. Each agent:
- Follows specific standards (listed in frontmatter)
- Enforces specific rules (validated automatically)
- Uses `{{project-root}}` placeholders for portability

### Invocation

Use `@agent-name` to invoke an agent:

```
@product-owner Define requirements for user authentication
@solution-architect Design the authentication system architecture
@functional-tester Write tests for authentication (TDD Red)
@python-coder Implement authentication service (TDD Green)
@tech-lead Review authentication implementation
```

{generate_agent_reference(agents)}

---

## Standards & Rules

### Standards (Guidance)

Located in `context/standards/`:
- **coding-standards.md** - Language patterns, frameworks, design principles
- **testing-standards.md** - TDD methodology, coverage requirements
- **tech-standards.md** - Tech stack, tools (uv), deployment
- **doc-standards.md** - Documentation structure, diagrams, writing
- **workflow-standards.md** - Processes, communication, retrospectives

### Rules (Enforced)

Located in `context/rules/` with automated validators:
- **conventional-commits.mdc** - Commit message format
- **EARS-notation-requirements.mdc** - Requirements notation
- **british-english.mdc** - Spelling conventions
- **metrics-logging.mdc** - Agent metrics format

**Pre-commit hooks** validate all rules automatically.

---

## Quality Gates

{generate_quality_gates(workflow)}

---

## Workflow Rules & Warnings

{generate_workflow_rules(workflow)}

---

## Best Practices

### Agent Usage

1. **Start with the workflow** - Follow phase dependencies
2. **One task per agent** - Keep agent prompts focused
3. **Use quality gates** - Don't skip reviews for production code
4. **Let agents fail** - If tests fail, agent reports it (don't auto-fix)
5. **Check outputs** - Verify agent produced expected files

### Workflow Selection

- **Use `default.yaml`** for production code requiring quality and maintainability
- **Use `prototype.yaml`** for experiments, POCs, and throwaway code
- **Don't promote prototype code** to production without rewriting with default workflow

### Troubleshooting

**Agent can't find files:**
→ Check `{{project-root}}` is correctly set for your project structure

**Standards not loaded:**
→ Agent definitions list required standards in frontmatter

**Validation fails:**
→ Run `uv run pre-commit run --all-files` to see specific violations

**Tests fail but agent doesn't fix:**
→ Correct behaviour! `@functional-tester` reports failures; coders fix them

---

## Maintenance

### Updating This File

Regenerate CLAUDE.md after changes to:
- `context/workflows/*.yaml`
- `context/agents/*.md`
- `context/README.md`

```bash
uv run python context/scripts/generators/generate-claude-md.py --workflow default
```

### Adding New Agents

1. Copy `context/agents/TEMPLATE.md`
2. Fill in standards/rules in frontmatter
3. Add to appropriate workflow phase
4. Regenerate CLAUDE.md

### Switching Workflows

```bash
# Generate for prototype workflow
uv run python context/scripts/generators/generate-claude-md.py --workflow prototype
```

---

## Context Directory Structure

```
context/
├── README.md              # Complete index
├── standards/             # How to do things (guidance)
├── rules/                # What must be enforced (validators)
├── agents/               # Who does what (agent definitions)
├── workflows/            # Workflow patterns (this workflow: {workflow_name})
└── scripts/              # Tools (validators, generators)
```

**Full documentation**: [context/README.md](context/README.md)

---

**Generated**: {workflow_name} workflow
**Agents**: {len(agents)} specialised agents
**Standards**: 5 guidance documents
**Rules**: 4 enforceable rules
"""

    return template


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate CLAUDE.md from context directory'
    )
    parser.add_argument(
        '--workflow',
        choices=['default', 'prototype'],
        default='default',
        help='Workflow to use (default: default)'
    )

    args = parser.parse_args()

    print(f"🔧 Generating CLAUDE.md from {args.workflow} workflow...")

    try:
        content = generate_claude_md(args.workflow)

        output_path = Path('CLAUDE.md')
        output_path.write_text(content)

        print(f"✅ Generated CLAUDE.md ({len(content)} bytes)")
        print(f"   Workflow: {args.workflow}")
        print(f"   Location: {output_path.absolute()}")
    except Exception as e:
        print(f"❌ Error generating CLAUDE.md: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
