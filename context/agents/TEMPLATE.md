---
name: agent-name
description: Brief description of agent's purpose. Use when [trigger condition]. Outputs [deliverables] to {project-root}/artefacts/[location].
model: sonnet
allowed_tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
standards:
  - tech-standards.md
  - coding-standards.md
rules:
  - conventional-commits.mdc
  - british-english.mdc
---

You are [role description]. Your job is to [primary responsibility].

## Required Standards (Read First!)

1. **{project-root}/context/standards/tech-standards.md** - Technology and tooling patterns
2. **{project-root}/context/standards/coding-standards.md** - Code quality and style guidelines

Read the standards files listed above before starting work. They contain detailed guidance on:
- Tool usage (uv, pytest, Node.js)
- Architecture patterns (12-factor, microservices)
- Code organisation and structure
- Language-specific conventions

## Required Rules (Must Follow!)

1. **{project-root}/context/rules/conventional-commits.mdc** - Commit message format (type(scope): subject)
2. **{project-root}/context/rules/british-english.mdc** - Use British English spelling (colour, optimise, etc.)

These are enforceable constraints that MUST be followed in all output.

## Critical Reminders (from standards above)

- ALWAYS use `uv run` for Python commands (tech-standards.md:34)
- Type hints on all functions (coding-standards.md:15)
- Each module should have single responsibility (coding-standards.md:42)

Format: `- [Reminder] ([source-file.md]:[line-number])`

## Context Paths

- Read requirements from `{project-root}/artefacts/product/requirements.md`
- Integrate with existing code in `{project-root}/artefacts/[language]/`
- Check API contracts in `{project-root}/artefacts/api/api-contract.json`

## Workflow

1. Read standards and rules listed in "Required Standards/Rules" sections above
2. Read context from paths listed in "Context Paths" section
3. Execute task following constraints below
4. Validate output against acceptance criteria
5. Update deliverables as specified below

## Constraints

- [Agent-specific constraint 1]
- [Agent-specific constraint 2]
- [Agent-specific constraint 3]

## Deliverables

- Output to `{project-root}/artefacts/[location]/`
- Update `{project-root}/artefacts/[location]/README.md` with [what to document]
- [Additional deliverable requirements]

## Task

{$ARGUMENTS}
