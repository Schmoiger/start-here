# Task Prompt Template

This template is used by the orchestrator when invoking agents via the Task tool.

---

## Template Structure

```markdown
AGENT CONTEXT:
Read your agent definition: context/agents/{agent-name}.md

This file contains:
- Your role and responsibilities
- Required standards and rules to follow
- Workflow steps
- Tool usage constraints
- Deliverables expected

---

TASK: {task-id}

{task-description}

---

IMPLEMENTATION:

{implementation-steps}

---

ACCEPTANCE CRITERIA:

{acceptance-criteria}

---

COMMIT FORMAT:

{commit-format}

---

IMPORTANT REMINDERS:
- Use Write/Edit tools for file operations (not bash)
- Follow TDD workflow (tests written by @functional-tester in RED phase)
- Use package managers specified in tech-standards.md (uv for Python, yarn for TypeScript)
```

---

## Usage Instructions for Orchestrator

### 1. Identify Agent and Task

From `artefacts/build/tasks.md`, extract:
- Task ID (e.g., V2-001-GREEN)
- Agent name (e.g., @python-coder)
- Task description
- Implementation steps
- Acceptance criteria

### 2. Fill Template Variables

Replace placeholders:
- `{agent-name}`: Agent identifier without @ (e.g., `python-coder`)
- `{task-id}`: Task identifier from tasks.md (e.g., `V2-001-GREEN`)
- `{task-description}`: Brief context from tasks.md "Context" section
- `{implementation-steps}`: Numbered list from tasks.md "Implementation" section
- `{acceptance-criteria}`: Bulleted list from tasks.md "Acceptance Criteria" section
- `{commit-format}`: Conventional commit format with task ID

### 3. Example: V2-001-GREEN

**From tasks.md:**
```markdown
#### V2-001-GREEN: Implement Python Shared Types (TDD GREEN)
**Agent:** @python-coder
**Context:** Implement Pydantic models to pass tests written in V2-001-RED
```

**Generated prompt:**
```markdown
AGENT CONTEXT:
Read your agent definition: context/agents/python-coder.md

---

TASK: V2-001-GREEN

Implement Pydantic models for v2 features to pass tests written in V2-001-RED.

---

IMPLEMENTATION:

1. Read tests from V2-001-RED (in tests/ directory)
2. Implement minimal code in packages/shared-types/python/bollinger_types/ to pass tests
3. Run: uv run pytest
4. All tests SHOULD pass

---

ACCEPTANCE CRITERIA:

- All tests from V2-001-RED pass
- No test files modified
- Code follows coding-standards.md
- Type hints on all functions

---

COMMIT FORMAT:

feat(shared-types): implement v2 Pydantic models

Tasks: V2-001-GREEN

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>

---

IMPORTANT REMINDERS:
- Use Write/Edit tools for file operations (not bash)
- Follow TDD workflow (tests written by @functional-tester in RED phase)
- Use package managers specified in tech-standards.md (uv for Python, yarn for TypeScript)
```

---

## Template Variants

### TDD RED Phase (Functional Tester)

```markdown
AGENT CONTEXT:
Read your agent definition: context/agents/functional-tester.md

MODE: TDD RED (Tests First)

---

TASK: {task-id}

Write failing tests for {feature}. Tests should fail because implementation doesn't exist yet.

---

IMPLEMENTATION:

{implementation-steps}

---

ACCEPTANCE CRITERIA:

- All tests written
- All tests FAIL (no implementation exists)
- Coverage targets defined
- Tests committed

---

COMMIT FORMAT:

test({scope}): add failing tests for {feature}

Tasks: {task-id}

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### TDD GREEN Phase (Coder)

```markdown
AGENT CONTEXT:
Read your agent definition: context/agents/{agent-name}.md

MODE: TDD GREEN (Implement to Pass Tests)

---

TASK: {task-id}

Implement minimal code to pass tests written in {red-task-id}.

---

IMPLEMENTATION:

1. Read tests from {red-task-id}
2. Implement minimal code to pass tests
3. Run tests (should pass)
4. Do NOT modify tests

---

ACCEPTANCE CRITERIA:

- All tests pass
- No test modifications
- Minimal implementation (no over-engineering)
- Standards compliant

---

COMMIT FORMAT:

feat({scope}): implement {feature}

Tasks: {task-id}

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

---

## Anti-Patterns to Avoid

### ❌ Bad: Override Agent Definition

```markdown
Your job: Write tests AND implementation.
```

**Problem:** Contradicts agent definition (coders don't write tests)

### ❌ Bad: Missing Agent Context

```markdown
TASK: V2-001
Implement shared types.
```

**Problem:** Agent doesn't know to read definition file

### ❌ Bad: Repeat Agent Definition

```markdown
You are an expert Python engineer. Use uv for package management.
Use type hints on all functions. Don't write tests...
[entire agent definition copied]
```

**Problem:** Not DRY, bloats prompt, creates sync issues

### ✅ Good: Reference Agent Definition

```markdown
AGENT CONTEXT:
Read your agent definition: context/agents/python-coder.md

TASK: V2-001-GREEN
[task-specific instructions only]
```

**Benefit:** DRY, single source of truth, minimal prompt

---

## Maintenance

When updating this template:
1. Test with at least 2 agent types (python-coder, typescript-coder)
2. Verify agents read their definition file
3. Confirm standards compliance
4. Update CLAUDE.md if template structure changes significantly
