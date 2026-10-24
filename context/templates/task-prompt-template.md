# Task Prompt Template

Used by orchestrator when spawning agents. Agents must read their definition from `context/agents/{agent-name}.md`.

---

## Structure

```markdown
You are @{agent-name} running {task-id}.

BEFORE starting, read:
1. Your agent definition: context/agents/{agent-name}.md
2. Rules you must follow: {resolved-rules — orchestrator: resolve using Rule Resolution in orchestrator.md. List each rule as a numbered item with its full path.}
3. Relevant skills: {resolved-skills — orchestrator: resolve using Skill Resolution in orchestrator.md. List matching procedural skills as a numbered item with its full path.}
4. Relevant excerpts from standards: {resolved-standards-excerpts — orchestrator: resolve using Standards Resolution in orchestrator.md. List each standard as a numbered item with its full path.}

---

## Task Context

Branch: `{branch}`
Working directory: `{project-root}`
Current state: {1–3 sentences describing what exists and what has just completed}

Key files for this task:
- `{file}` — {what it contains / why it matters}
- `{file}` — {what it contains / why it matters}

---

## File Scope

You may only write or edit files within this scope:
- `{path}` — {what you are writing here}
- `{path}` — {what you are writing here}

Do NOT write to HANDOFF.md, tasks.md, or bugs.md — report changes back to the orchestrator.
Do NOT run `git add` or `git commit` — the orchestrator commits on your behalf (see COMMIT section).

---

## Task

{task-id}: {task-description}

### Acceptance Criteria

{bulleted-acceptance-criteria}

### Primary Output Path 

`{project-root}/{output-path}`

---

## Implementation

{numbered-implementation-steps}

---

## Execution Reminders

- **State Recovery**: If context compaction occurs, execute your standard recovery protocol from your agent definition using the **Primary Output Path** above. Write findings incrementally.
- **Escalation**: If blocked or requiring tool approval, append a record immediately to `artefacts/build/interruptions/{task-id}.jsonl` using the schema in your agent definition's Escalation Protocol.
- **Linting**: Before reporting back, run your designated linter (`ruff` / `biome`) on modified files and fix any errors.
- **Reporting Back**: Include the files changed, commit message, and status summary so that the orchestrator can commit on your behalf.