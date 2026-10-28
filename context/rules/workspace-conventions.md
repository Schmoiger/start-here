---
description: Universal workspace conventions covering output locations, git commits, metrics logging, interruption logging, and effort estimation
globs: []
alwaysApply: true
---

# Workspace Conventions

**Applies to**: All agent operations, file generation, and version control.

---

## 1. Output Locations

### Directory Structure
```
{project-root}/
├── artefacts/                    # All build outputs
│   ├── architecture/             # Architecture docs, diagrams
│   ├── build/                    # Tasks, reviews, implementation docs
│   ├── product/                  # Requirements, user stories
│   ├── test-results/             # Test output files
│   └── design/                   # UI designs, wireframes
├── secrets/                      # Credentials (gitignored)
└── services/{name}/              # Service implementation
    └── tests/                    # Service tests
```

### File Naming
| Type | Convention | Example |
|------|------------|---------|
| Test results | `v2-{task-id}-results.txt` | `v2-004-red-results.txt` |
| Reviews | `{phase}-review.md` | `phase-2-3-tech-review.md` |
| Implementation docs | `{TASK-ID}-IMPLEMENTATION.md` | `BUG-UI-030-IMPLEMENTATION.md` |

---

## 2. Git Commits

1. **Who Commits**: If invoked directly by a human, **commit directly**. If spawned as a subagent by an Orchestrator, **DO NOT commit** — write your message to `/tmp/{task-id}_commit_msg.txt` and return the file paths.
2. **Pre-Commit**: Always format before staging (e.g. `uv run ruff format {files}` or `yarn biome check --write {files}`). If a hook reverts your changes, read the formatted file and commit it.
3. **Message Format**: Commits MUST follow `{type}({scope}): {description}`.
4. **Agent Trailers**: Commits MUST include the `Agent-Session` trailer and `Co-Authored-By` for AI-authored work.
5. **Hook-Owned Trailer Fields**: `tool=`, `model=`, and `tokens=` in the `Agent-Session` trailer are populated by the `prepare-commit-msg` hook from runtime session telemetry (Claude Code, Antigravity, Copilot, Codex, Cline). Do not hand-write them: the `commit-msg` validator rejects values that runtime telemetry contradicts or cannot corroborate.

---

## 3. Metrics Logging

1. **Session Log**: Append events (start, handoff, escalate, complete, blocked) to `artefacts/build/metrics/session-log.jsonl`.
2. **Schema**: Fields, token-source rules, and examples are defined in `context/templates/logging-template.md` § Session Metrics Log.
3. **Format**: One JSON object per line. Never overwrite.
4. **Location**: Metrics are build records, so they live under `artefacts/build/` alongside tasks, reviews, and interruption logs. A repository-root `metrics/` directory is not permitted.

---

## 4. Interruption Logging

1. **Task Log**: Append each blocking interruption to `artefacts/build/interruptions/{task-id}.jsonl` — one rolling log per task.
2. **Schema**: The record fields are defined in `context/templates/logging-template.md` § Interruption Log; the log's filename stem MUST equal the `task_id` of every record it contains.
3. **Format**: One JSON object per line, appended and never rewritten. Record the interruption when it is resolved; if logged at the point of blocking, leave outcome fields `null` and append a `resolution` record referencing the original `id`.

---

## 5. Effort Estimation

1. Estimate effort in tokens, not time — models consume tokens, not minutes; token estimates are stable across machines and interruptions.

