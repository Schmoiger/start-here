# Tasks: {Service}

## Format

Two formats are used depending on the scope of the task file:

### Table format — service-level task tracking

See `context/standards/context-framework.md` for prioritisation rules and agent behaviour.

- **Pri**: critical, high, medium, low
- **Status**: pending, in_progress, blocked, completed
- **Blocked By**: task/bug IDs or `-` if none
- **Tokens**: in/out with K suffix (e.g., 8.2K/5.1K) — populated on completion
- **Duration**: minutes or hours (e.g., 32m) — populated on completion

| ID | Pri | Status | Blocked By | Task | Tokens | Duration |
|----|-----|--------|------------|------|--------|----------|
| TASK-001 | critical | completed | - | {description} (REQ-xxx) | 4.1K/2.8K | 18m |
| TASK-002 | high | in_progress | TASK-001 | {description} (REQ-xxx) | - | - |
| TASK-003 | medium | pending | TASK-001 | {description} | - | - |
| TASK-004 | low | pending | - | {description} | - | - |

### Checklist format — sprint-based feature task tracking

For multi-sprint feature build docs (e.g., `tasks-v4-*.md`), use `[ ]` / `[x]` checkboxes on
every actionable item so progress is visible at a glance. Rules:

- Every actionable line item begins with `- [ ]` (pending) or `- [x]` (done)
- Phase gates and review approvals also use checkboxes
- Mark `[x]` immediately when the item is confirmed complete — do not batch at end of sprint
- Sprint-level status in the file header (`**Status**: Planning | In Progress | Complete`)
  reflects the overall sprint, not individual items

```markdown
### S1-1. Example task group

- [ ] First action item
- [ ] Second action item
- [x] Already completed item

### S1 Sprint Review

- [ ] @code-reviewer approved
- [ ] @security-tester approved
```

## Metrics Flow

```
session-log.jsonl  →  Per-turn (source of truth)
    ↓ aggregate
tasks.md           →  Per-task (this file)
    ↓ aggregate
git commit         →  Per-commit (Agent-Session line)
    ↓ aggregate
PR description     →  Per-PR rollup
```
