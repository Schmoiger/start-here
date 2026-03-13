# Task Prompt Template

Used by orchestrator when spawning agents. Agents must read their definition from `context/agents/{agent-name}.md`.

---

## Structure

```markdown
You are @{agent-name} running {task-id} for the {project-name} project.

BEFORE starting, read:
1. context/agents/{agent-name}.md
2. context/standards/agent-standards.md
3. context/standards/tech-standards.md
4. context/standards/coding-standards.md
[add relevant standards for the task]

TOOL REQUIREMENTS (MANDATORY):
- File operations: Write/Edit tools ONLY — NEVER bash echo/cat/sed/awk/heredoc
- Python packages: `uv add` ONLY — NEVER pip
- Python one-off tools: `uvx <tool>` ONLY — NEVER pipx/bare tool name (e.g. `uvx ruff check .`)
- TypeScript packages: `yarn add` ONLY — NEVER npm
- TypeScript one-off tools: `yarn dlx <tool>` ONLY — NEVER npx
- Run Python: `uv run pytest`
- Run TypeScript tests: `yarn test --run` from `frontend/`
- Lint TypeScript: `./node_modules/.bin/biome check .` (NOT `yarn biome check`)
- Find files: Glob tool (NOT bash find/ls)
- Search content: Grep tool (NOT bash grep)

ESCALATION (MANDATORY):
Log to `artefacts/build/agent-interruptions.md` under the current sprint section
whenever the user's or orchestrator's attention was required:

1. QUESTION — you cannot proceed without an external answer:
   **Type**: Question | **Question**: ... | **Answered by**: _(blank)_ | **Resolution**: _(blank)_

2. TOOL APPROVAL — user was prompted to approve a tool use:
   **Type**: Tool approval | **Tool**: ... | **Approved by**: User | **Resolution**: Approved/Denied

Do NOT log autonomous decisions or self-resolved issues.

---

## IMMEDIATE CONTEXT

Branch: `{branch}`
Working directory: `/path/to/project`
Current state: {1–3 sentences describing what exists and what has just completed}

Key files for this task:
- `{file}` — {what it contains / why it matters}
- `{file}` — {what it contains / why it matters}

---

## TASK: {task-id}

{task-description}

---

## IMPLEMENTATION

{numbered-implementation-steps}

---

## ACCEPTANCE

{bulleted-acceptance-criteria}

---

## COMMIT

{conventional-commit-format}

---

## REPORT BACK

{what the orchestrator needs to know when the agent finishes}
```

---

## Orchestrator Usage

1. Read `artefacts/build/tasks.md` for the current task
2. Fill ALL placeholders — never leave `{...}` in the prompt
3. Always include IMMEDIATE CONTEXT — agents have no inherited context
4. Always include TOOL REQUIREMENTS — agents do not know project conventions otherwise
5. Always include ESCALATION block — agents must know where to log blockers
6. Spawn agent

**Placeholders**:
- `{agent-name}`: Without @ (e.g., `python-coder`)
- `{task-id}`: From tasks.md (e.g., `RESEARCH-17-RED`)
- `{branch}`: Current git branch
- `{task-description}`: Brief context — what this agent is building and why
- `{numbered-implementation-steps}`: Numbered list with specific file paths
- `{acceptance-criteria}`: Bulleted list — what DONE looks like
- `{commit-format}`: Conventional commit with task ID
- `{report-back}`: What the orchestrator needs from the agent's summary

---

## TDD Phase Variants

**RED Phase** — add `MODE: TDD RED` in TASK section:
- Implementation: write tests only, no production code
- Acceptance: ALL tests FAIL on first run; confirm failure count
- Commit: `test({scope}): {task-id} {feature} failing tests`

**GREEN Phase** — add `MODE: TDD GREEN` in TASK section:
- Acceptance: ALL tests pass; no test file modifications
- Commit: `feat({scope}): {task-id} implement {feature}`

**BLUE Phase** — add `MODE: TDD BLUE` in TASK section:
- Acceptance: ALL tests still pass; no new functionality
- Commit: `refactor({scope}): {task-id} {description}`

---

## Anti-Patterns

❌ Override agent definition inline — agents read it from `context/agents/`
❌ Omit IMMEDIATE CONTEXT — agents have zero inherited state
❌ Omit TOOL REQUIREMENTS — agents will use wrong tools (pip, npx, bash echo)
❌ Omit ESCALATION block — agents won't know where to log blockers
❌ Use `yarn biome check` — use `./node_modules/.bin/biome check .` instead
✅ Reference agent definition: `Read: context/agents/{agent-name}.md`
✅ Provide specific file paths in implementation steps
✅ Tell the agent exactly what to report back
