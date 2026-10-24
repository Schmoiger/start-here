# Logging Template

Canonical schema for the two append-only logs agents write. Rules and agent definitions reference this file rather than restating the fields, so the schema has exactly one home.

- Rules: `context/rules/workspace-conventions.md` §3 (metrics) and §4 (interruptions)
- Validator: `context/scripts/validators/workspace_conventions.py` (`metrics`, `interruptions` subcommands)

Both logs share one discipline: **one JSON object per line, appended, never rewritten**. A line already written is immutable — corrections are new records, not edits.

---

## 1. Session Metrics Log

**Path**: `artefacts/build/metrics/session-log.jsonl`

One log for the workspace. Append one record at each lifecycle event: session `start`, agent `handoff`, `escalate`, `complete`, or `blocked`.

| Field | Required | Value |
| :--- | :--- | :--- |
| `ts` | yes | ISO-8601 UTC timestamp, e.g. `2026-10-23T14:05:11Z` |
| `task` | yes | Task identifier, e.g. `TASK-004` |
| `agent` | yes | Agent name without the `@`, e.g. `python-coder` |
| `event` | yes | `start` \| `handoff` \| `escalate` \| `complete` \| `blocked` |
| `tokens` | yes | Object: `in` (int), `out` (int), `source` (`api_response` \| `estimated` \| `unavailable`) |
| `to` | for `handoff` and `escalate` | Target agent, e.g. `tech-lead` |
| `notes` | no | Free-text context |

### Token Estimation

| Source | When | Accuracy |
| :--- | :--- | :--- |
| `api_response` | Platform provides usage metadata | Exact |
| `estimated` | Calculate as characters / 4 | Roughly 80% |
| `unavailable` | Platform exposes nothing and nothing can be estimated | Log anyway — accuracy beats silence |

Never backfill a `source` you did not observe. A fabricated `api_response` count is worse than an honest `unavailable`.

```jsonl
{"ts":"2026-10-23T14:00:02Z","task":"TASK-004","agent":"python-coder","event":"start","tokens":{"in":0,"out":0,"source":"unavailable"}}
{"ts":"2026-10-23T15:12:40Z","task":"TASK-004","agent":"python-coder","event":"handoff","tokens":{"in":18400,"out":2100,"source":"api_response"},"to":"tech-lead"}
{"ts":"2026-10-23T15:41:09Z","task":"TASK-004","agent":"tech-lead","event":"complete","tokens":{"in":5200,"out":600,"source":"estimated"},"notes":"review passed, no rework"}
```

---

## 2. Interruption Log

**Path**: `artefacts/build/interruptions/{task-id}.jsonl`

One rolling log per task. The filename stem MUST equal the `task_id` of every record it contains, so a task's interruptions stay in one place for retrospective analysis.

Base fields, carried by every record:

| Field | Value |
| :--- | :--- |
| `id` | Unique short identifier within the log, e.g. `a1f3` |
| `ts` | ISO-8601 UTC timestamp, e.g. `2026-10-23T14:05:11Z` |
| `agent` | Your agent name, without the `@`, e.g. `python-coder` |
| `task_id` | The task identifier, e.g. `TASK-004` |
| `type` | `question` \| `tool_approval` \| `escalation` \| `resolution` |

Fields by `type`:

| `type` | Additional fields |
| :--- | :--- |
| `question` | `question`, `blocker`, `answered_by`, `resolution` |
| `tool_approval` | `tool`, `action`, `decision` (`approved` \| `denied`), `decision_by` |
| `escalation` | `impact` (`high` \| `medium` \| `low`), `escalated_to`, `options` (array), `resolution`, `decided_by` |
| `resolution` | `ref` (the `id` of the record it resolves), `resolution`, `decided_by` |

```jsonl
{"id":"a1f3","ts":"2026-10-23T14:05:11Z","agent":"python-coder","task_id":"TASK-004","type":"question","question":"Which schema applies to the audit fields?","blocker":"AC-2 cannot be met without it","answered_by":"orchestrator","resolution":"Use the schema in artefacts/architecture/data-model.md"}
{"id":"b7c2","ts":"2026-10-23T14:05:19Z","agent":"python-coder","task_id":"TASK-004","type":"tool_approval","tool":"supabase","action":"db push --linked","decision":"approved","decision_by":"user"}
{"id":"c9d4","ts":"2026-10-23T15:01:02Z","agent":"solution-architect","task_id":"TASK-008","type":"escalation","impact":"high","escalated_to":"human","options":["frontmatter-only","body-table"],"resolution":"frontmatter-only","decided_by":"human"}
```

Write the record when the interruption is resolved, so the ask and its outcome share a line. If you must log at the moment of blocking — you are halting and cannot continue — leave the outcome fields `null` and append a `resolution` record with `ref` set to that record's `id`.

---

## 3. Validation

```bash
uv run python context/scripts/validators/workspace_conventions.py metrics artefacts/build/metrics/session-log.jsonl
uv run python context/scripts/validators/workspace_conventions.py interruptions artefacts/build/interruptions/TASK-004.jsonl
```

The pre-commit hooks `workspace-conventions-metrics` and `workspace-conventions-interruptions` run the same checks on staged logs. A bare path argument auto-detects the log type from the path.
