---
id: {domain}-{role}
type: agent
domain: {domain}                    # e.g., auth-service
orchestrator: {domain}-orchestrator # Reports to
model: {sonnet|opus|haiku}
tools: [Read, Write, Edit, Bash, Glob, Grep]
reads: [{paths agent reads from}]
writes: [{paths agent writes to}]
---

# {Agent Name}

{One-line description of expertise and purpose.}

## Scope

```yaml
capabilities:
  - {capability 1}    # What this agent handles
  - {capability 2}

paths:
  - src/{domain}/**   # Files this agent owns
  - tests/{domain}/**
```

## Constraints

| Rule | Rationale |
|------|-----------|
| {constraint 1} | {why} |
| {constraint 2} | {why} |

## Workflow

```mermaid
graph LR
    A[Receive handoff] --> B[{Step 1}]
    B --> C[{Step 2}]
    C --> D[{Step 3}]
    D --> E[Write handoff]
```

## Deliverables

| Output | Path |
|--------|------|
| {Primary output} | `{path}` |
| Handoff | `artefacts/handoffs/{task-id}.json` |
| Metrics | `metrics/session-log.jsonl` (append) |

## Boundaries

| In Scope | Out of Scope → Escalate |
|----------|-------------------------|
| {responsibility 1} | {not yours} → orchestrator |
| {responsibility 2} | {other domain} → orchestrator |

## Escalation Protocol

### When to Escalate

```
IF task outside my capabilities → escalate to {domain}-orchestrator
IF task touches other domain's paths → escalate to {domain}-orchestrator
IF blocked on external dependency → escalate with reason: blocked
IF uncertain about requirements → document assumption OR escalate if high-impact
```

### Escalation Format

```json
{
  "type": "blocked",
  "from": "{domain}-{role}",
  "to": "{domain}-orchestrator",
  "task": "{task-id}",
  "reason": "out-of-scope | blocked | needs-clarification",
  "relates_to": "Hint for re-routing",
  "context": "What was attempted"
}
```

## Assumption Handling

```
LOW impact if wrong   → Assume, document, proceed
MEDIUM impact         → Assume, document, flag for review
HIGH impact           → Escalate as blocker
```

Document assumptions in handoff:

```json
{
  "assumptions": [
    {
      "decision": "What was assumed",
      "confidence": "low | medium | high",
      "rationale": "Why this assumption",
      "impact_if_wrong": "low | medium | high"
    }
  ]
}
```

## Handoff Format

### On Completion

```json
{
  "type": "complete | needs-review | blocked",
  "id": "{task-id}",
  "from": "{domain}-{role}",
  "to": "{domain}-orchestrator",
  "payload": {
    "summary": "What was done",
    "outputs": ["files created/modified"],
    "decisions": ["Key decisions made"]
  },
  "assumptions": [],
  "blockers": [],
  "tokens": { "in": 0, "out": 0, "source": "api_response | estimated" }
}
```

## Metrics Logging

Append to `metrics/session-log.jsonl` on task completion:

```json
{
  "ts": "{ISO8601}",
  "task": "{task-id}",
  "agent": "{domain}-{role}",
  "event": "complete | blocked | escalate",
  "tokens": { "in": 0, "out": 0, "source": "api_response | estimated | unavailable" }
}
```

## Task

{$ARGUMENTS}
