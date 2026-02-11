#!/usr/bin/env python3
"""Generate AGENTS.md orchestration guide from context directory.

Creates two files:
- AGENTS.md: Full agent orchestration guide
- CLAUDE.md: Simple file that references @AGENTS.md

Usage:
    uv run python context/scripts/generators/generate_claude_md.py [--workflow default|prototype]
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


def generate_state_recovery(workflow: dict) -> str:
    """Generate state recovery section."""
    state_recovery = workflow.get('state_recovery', {})

    if not state_recovery:
        return ""

    sections = ["## State Recovery After Context Compaction\n"]
    sections.append("**CRITICAL**: After context compaction or at session start, the orchestrating agent SHALL:\n")

    after_compaction = state_recovery.get('after_compaction', [])
    if after_compaction:
        sections.append("\n### Recovery Checklist\n")
        for step in after_compaction:
            sections.append(f"- [ ] {step}")

    critical_files = state_recovery.get('critical_files', [])
    if critical_files:
        sections.append("\n### Critical State Files\n")
        sections.append("\nThese files maintain project state across sessions:\n")
        for file in critical_files:
            sections.append(f"- `{file}`")

        sections.append("\n**Read these files immediately after compaction to understand current state.**")

    return '\n'.join(sections)


def generate_estimation_guidance(workflow: dict) -> str:
    """Generate effort estimation guidance section."""
    estimation = workflow.get('estimation_guidance', [])

    if not estimation:
        return ""

    sections = ["## Effort Estimation Guidance\n"]
    sections.append("**IMPORTANT**: Estimate effort in tokens, NOT time. Time estimates are unreliable.\n")

    for guideline in estimation:
        sections.append(f"- {guideline}")

    return '\n'.join(sections)


def generate_parallel_planning(workflow: dict) -> str:
    """Generate parallel planning guidance section."""
    parallel = workflow.get('parallel_planning', [])

    if not parallel:
        return ""

    sections = ["## Parallel Execution Planning\n"]
    sections.append("**When spawning multiple agents**, the orchestrator SHALL present parallel execution options:\n")

    for guideline in parallel:
        sections.append(f"- {guideline}")

    sections.append("\nSee workflow-standards.md §11 for complete parallel execution template.")

    return '\n'.join(sections)


def generate_agents_md(workflow_name: str) -> str:
    """Generate complete AGENTS.md content."""
    workflow = load_workflow(workflow_name)
    agents = load_agent_definitions()

    workflow_desc = workflow.get('description', '')

    template = f"""# Multi-Agent Orchestration Guide

**Generated from**: `context/` directory
**Workflow**: `{workflow_name}` - {workflow_desc}
**Auto-generated**: Do not edit manually. Run `uv run python context/scripts/generators/generate_claude_md.py` to regenerate.

---

## Overview

This guide describes the orchestration of specialised agents for software development tasks. Each agent has specific capabilities, follows defined standards, and produces specific outputs.

**Context Directory**: All standards, rules, and agent definitions are in `context/`. See [context/README.md](context/README.md) for complete index.

**Orchestrator**: When spawning agents, use the task prompt template at `context/templates/TASK-PROMPT-TEMPLATE.md`. The template ensures agents read their definition file and receive consistent task structure. Never inline agent definitions—agents will read them from `context/agents/{{agent-name}}.md`. See [workflow-standards.md §8](context/standards/workflow-standards.md#8-orchestrator-agent-invocation).

---

## Session Initialisation Checklist

**Use this checklist after context compaction or at session start:**

**For the orchestrator (you), before beginning work:**

1. **Core Standards** (Read if compacted or unfamiliar):
   - `context/standards/agent-standards.md` - Agent behaviour, tool usage, handoffs
   - `context/standards/workflow-standards.md` - Development workflow, TDD process
   - `context/standards/doc-standards.md` - Documentation structure, artefact organisation

2. **Technical Standards** (Read when working on implementation):
   - `context/standards/tech-standards.md` - Tech stack (uv, yarn, FastAPI, React)
   - `context/standards/coding-standards.md` - Code quality, patterns, error handling
   - `context/standards/testing-standards.md` - TDD cycle, coverage requirements

3. **Project Context** (Read when unfamiliar with current work):
   - `artefacts/product/requirements.md` - System requirements
   - `artefacts/architecture/architecture.md` - System architecture
   - `artefacts/build/tasks.md` - Current task list

4. **Verification**:
   - ✅ I know which workflow phase we're in (discovery/design/tdd-red/tdd-green/review/etc.)
   - ✅ I understand the TDD workflow (RED then GREEN then BLUE - three separate phases, never combined)
   - ✅ I will include TOOL REQUIREMENTS in every agent prompt (Write/Edit not bash, uv not pip, yarn dlx not npx)
   - ✅ I will present parallel options before spawning 2+ agents
   - ✅ I know agents read their definitions from `context/agents/{{agent-name}}.md`

**After compaction:** The conversation summary provides what happened, but standards may have changed. Re-read core standards to ensure compliance.

**When spawning agents:** Spawned agents do NOT inherit your context. You MUST explicitly tell them to read relevant standards. See "Agent Spawning Protocol" below.

---

{generate_state_recovery(workflow)}

---

{generate_estimation_guidance(workflow)}

---

{generate_parallel_planning(workflow)}

---

## Workflow: {workflow.get('name', workflow_name)}

{workflow_desc}

### Understanding Parallelism

This workflow uses two types of parallelism:

**1. Phase-Level Parallelism (Inter-Phase)**
- Multiple **phases** run simultaneously when they don't depend on each other
- Example: If phase A and B both depend on phase C, then A and B can run in parallel after C completes
- Determined by: `depends_on` field (implicit - no dependency = can be parallel)
- Current workflow: **Linear chain** - no phase-level parallelism

**2. Agent-Level Parallelism (Intra-Phase)**
- Multiple **agents** within a single phase run simultaneously
- Example: `@python-coder` and `@typescript-coder` in tdd-green phase
- Determined by: `parallel: true` flag (explicit)
- If `sequential: true`, agents run one after another in order

**Phase Dependencies in This Workflow:**
```
discovery → design → design-review → tdd-red → tdd-green → tdd-blue →
unit-test → integration-test → e2e-test → quality-review →
docs-cleanup → deployment → deployment-review → retrospective (optional)
```
Each phase waits for the previous phase to complete (strict sequence).

**Quality Gates:** design-review, quality-review, deployment-review
**Optional:** retrospective (workflow efficiency analysis)

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

### Pre-Spawn Checklist

**BEFORE spawning any agent, verify ALL of these:**

- [ ] Agent prompt includes "Read context/standards/tech-standards.md first"
- [ ] Agent prompt includes TOOL REQUIREMENTS block (Write/Edit not bash, uv not pip, yarn dlx not npx)
- [ ] If TDD phase: Specified which phase (RED/GREEN/BLUE) and requirements
- [ ] If spawning 2+ agents: Presented parallel vs sequential options to user
- [ ] Task is clear and unambiguous

**If any checkbox is unchecked, do NOT spawn the agent yet.**

### Agent Spawning Protocol

**CRITICAL**: When spawning agents, the orchestrator MUST explicitly provide standards context. Spawned agents start with fresh context and do NOT automatically inherit standards.

**Template for spawning agents:**

```
@agent-name [task description]

BEFORE starting, read these standards:
1. context/standards/tech-standards.md - Tech stack (uv, yarn, Puppeteer)
2. context/standards/agent-standards.md - Tool usage (Write/Edit not bash)
3. context/standards/[relevant-standard].md

Key reminders:
- Python: use `uv add`, `uv run` (NOT pip)
- TypeScript: use `yarn add`, `yarn dlx` (NOT npm, npx)
- Files: use Write/Edit tools (NOT bash echo/cat/sed)

Then: [specific task instructions]
```

**Why this is required:**
- Spawned agents don't have access to CLAUDE.md/AGENTS.md
- Standards are NOT inherited automatically
- Explicit reading prevents common violations (npx vs yarn dlx, pip vs uv, bash vs Write/Edit)

### Invocation Examples

**Correct (with standards context):**
```
@python-coder Implement authentication service

Read context/standards/tech-standards.md first.
Use `uv add` for packages (NOT pip).
Use Write/Edit tools for files (NOT bash).

Implement: [task details]
```

**Incorrect (missing standards):**
```
@python-coder Implement authentication service
```
❌ Agent will likely use pip, bash for files, default behaviors

### Critical Adherence Protocols

**These protocols are MANDATORY. Violations indicate orchestrator failure.**

#### Protocol 1: Tool Usage Enforcement

**BEFORE spawning any agent, verify agent prompt includes:**

```
TOOL REQUIREMENTS (MANDATORY):
- File operations: Use Write/Edit tools ONLY (NEVER bash echo/cat/sed/awk)
- Python packages: Use `uv add` ONLY (NEVER pip)
- TypeScript packages: Use `yarn add` ONLY (NEVER npm)
- One-off TypeScript tools: Use `yarn dlx` ONLY (NEVER npx)
- Find files: Use Glob tool (NEVER bash find/ls)
- Search files: Use Grep tool (NEVER bash grep/rg)

If you use bash for file operations, the task will be rejected.
```

**Validation**: After agent completes, check tool usage in transcript. Reject if violations found.

#### Protocol 2: TDD Workflow Enforcement

**TDD phases are SEPARATE. They CANNOT be combined.**

**When starting TDD work:**

```
Phase 1: TDD RED (write failing tests)
@functional-tester Write tests for [feature]

Requirements:
- Tests MUST fail when first run
- Do NOT write implementation code
- Report: "All tests failing as expected"

Phase 2: TDD GREEN (implement to pass)
@python-coder / @typescript-coder Implement [feature]

Requirements:
- Tests MUST pass when done
- Do NOT modify tests
- Do NOT refactor yet
- Report: "All tests passing"

Phase 3: TDD BLUE (refactor)
@python-coder / @typescript-coder Refactor [feature]

Requirements:
- Tests MUST still pass
- Improve code quality only
- No new functionality
- Report: "Refactored, all tests still passing"
```

**Validation**: Each phase must complete before next begins. No combining phases.

#### Protocol 3: Parallel Execution Planning

**BEFORE spawning 2+ agents, ALWAYS present parallel options to user.**

**Mandatory template:**

```
I'm about to spawn [N] agents: [@agent1, @agent2, ...]

EXECUTION OPTIONS:

Option A: Sequential
- Agents run one after another: @agent1 → @agent2 → @agent3
- Time: ~X minutes total
- Tokens: Y tokens (baseline)
- Risk: Low (easier to debug, clear order)

Option B: Parallel
- Agents run simultaneously: @agent1 + @agent2 + @agent3
- Time: ~Z minutes (~40-50% faster)
- Tokens: Y + N tokens (~10-20% more due to context duplication)
- Risk: Medium (merge conflicts possible, coordination overhead)

Which option do you prefer?
```

**Validation**: If spawning 2+ agents without presenting options, this is a protocol violation.

### Tool Usage Reminders

**CRITICAL**: Agents must use the correct tools for each operation:

| Operation | ✅ Use | ❌ Don't Use |
|-----------|--------|--------------|
| Create/modify files | Write, Edit tools | bash with echo, cat, sed, awk, heredoc |
| Run tests | bash with `uv run pytest` or `yarn test` | N/A |
| Python package management | `uv add`, `uv remove`, `uv run` | pip, manual edits |
| TypeScript package management | `yarn add`, `yarn remove` | npm, pnpm |
| One-off TypeScript tools | `yarn dlx <tool>` | npx, global installs |
| Find files | Glob tool | bash find, ls |
| Search file contents | Grep tool | bash grep, rg |
| Git operations | bash | N/A |

**Why this matters:**
- Write/Edit tools don't require user permission (faster execution)
- Bash file operations require permission prompts (slower, interrupts flow)
- Using correct package managers ensures consistent environments

See agent-standards.md §3.3 for complete tool usage guidelines.

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

Regenerate AGENTS.md after changes to:
- `context/workflows/*.yaml`
- `context/agents/*.md`
- `context/README.md`

```bash
uv run python context/scripts/generators/generate_claude_md.py --workflow default
```

### Adding New Agents

1. Copy `context/agents/TEMPLATE.md`
2. Fill in standards/rules in frontmatter
3. Add to appropriate workflow phase
4. Regenerate AGENTS.md

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
        description='Generate AGENTS.md and CLAUDE.md from context directory'
    )
    parser.add_argument(
        '--workflow',
        choices=['default', 'prototype'],
        default='default',
        help='Workflow to use (default: default)'
    )

    args = parser.parse_args()

    print(f"🔧 Generating AGENTS.md from {args.workflow} workflow...")

    try:
        # Generate AGENTS.md with full content
        agents_content = generate_agents_md(args.workflow)
        agents_path = Path('AGENTS.md')
        agents_path.write_text(agents_content)

        print(f"✅ Generated AGENTS.md ({len(agents_content)} bytes)")
        print(f"   Workflow: {args.workflow}")
        print(f"   Location: {agents_path.absolute()}")

        # Generate simple CLAUDE.md that references AGENTS.md
        claude_content = "@AGENTS.md\n"
        claude_path = Path('CLAUDE.md')
        claude_path.write_text(claude_content)

        print(f"✅ Generated CLAUDE.md (references @AGENTS.md)")
        print(f"   Location: {claude_path.absolute()}")

    except Exception as e:
        print(f"❌ Error generating files: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
