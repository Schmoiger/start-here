# Tasks: {Service}

## Format

See `context/standards/context-framework.md` for prioritisation rules and agent behaviour.

- **Pri**: critical, high, normal, low
- **Status**: pending, in_progress, blocked, completed
- **Blocked By**: task/bug IDs or `-` if none
- **Tokens**: in/out with K suffix (e.g., 8.2K/5.1K) — populated on completion
- **Duration**: minutes or hours (e.g., 32m) — populated on completion

## Tasks

| ID | Pri | Status | Blocked By | Task | Tokens | Duration |
|----|-----|--------|------------|------|--------|----------|
| TASK-001 | critical | completed | - | {description} (REQ-xxx) | 4.1K/2.8K | 18m |
| TASK-002 | high | in_progress | TASK-001 | {description} (REQ-xxx) | - | - |
| TASK-003 | normal | pending | TASK-001 | {description} | - | - |
| TASK-004 | low | pending | - | {description} | - | - |

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
