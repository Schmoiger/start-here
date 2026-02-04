# Task Prompt Template

Used by orchestrator when spawning agents. Agents must read their definition from `context/agents/{agent-name}.md`.

---

## Structure

```markdown
AGENT CONTEXT:
Read: context/agents/{agent-name}.md

---

TASK: {task-id}

{task-description}

---

IMPLEMENTATION:

{implementation-steps}

---

ACCEPTANCE:

{acceptance-criteria}

---

COMMIT:

{commit-format}
```

---

## Orchestrator Usage

1. Extract task from `artefacts/build/tasks.md`
2. Fill placeholders
3. Spawn agent with filled template

**Placeholders**:
- `{agent-name}`: Without @ (e.g., `python-coder`)
- `{task-id}`: From tasks.md (e.g., `V2-001-GREEN`)
- `{task-description}`: Brief context
- `{implementation-steps}`: Numbered list
- `{acceptance-criteria}`: Bulleted list
- `{commit-format}`: Conventional commit with task ID

---

## TDD Variants

**RED Phase** (add `MODE: TDD RED` after AGENT CONTEXT):
- Acceptance: All tests FAIL (no implementation)
- Commit: `test({scope}): add failing tests for {feature}`

**GREEN Phase** (add `MODE: TDD GREEN` after AGENT CONTEXT):
- Acceptance: All tests pass, no test modifications
- Commit: `feat({scope}): implement {feature}`

---

## Anti-Patterns

❌ Override agent definition
❌ Repeat agent definition in prompt
✅ Reference agent definition: `Read: context/agents/{agent-name}.md`
