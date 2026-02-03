# Meta-Orchestrator Template

```yaml
---
id: meta-orchestrator
type: orchestrator
scope: repository
version: 1.0
---
```

## Purpose

Route tasks to appropriate domain orchestrators. Decompose cross-cutting tasks. Handle escalations from domain orchestrators.

## Context

```yaml
domains: !include domains.yaml
```

## Routing Rules

### Inbound Task

```
1. Parse task for domain signals (keywords, file paths, service names)
2. Match against domain capabilities
3. IF single domain match:
     Route to domain orchestrator
   ELIF multiple domain match:
     Decompose into subtasks (see Cross-Cutting Tasks)
   ELIF no match:
     Route to most likely domain with { confidence: low }
     OR escalate to human if ambiguous
```

### Escalation from Domain

```
1. Receive: { type: escalate, from: <domain>, relates_to: <hint> }
2. Match relates_to against domain capabilities
3. IF match found:
     Route to matched domain orchestrator
   ELIF relates_to: "unknown":
     Analyse task content, attempt routing
     OR escalate to human
```

### Cross-Cutting Tasks

When task spans multiple domains:

```json
{
  "type": "cross-cutting",
  "task": "Original task description",
  "decomposition": [
    {
      "sequence": 1,
      "domain": "auth-service",
      "subtask": "Domain-specific portion",
      "outputs": ["token-validator.ts"]
    },
    {
      "sequence": 2,
      "domain": "data-service",
      "subtask": "Domain-specific portion",
      "depends_on": [1],
      "inputs": ["token-validator.ts"]
    }
  ],
  "integration": {
    "owner": "data-service",
    "task": "Verify integration works end-to-end"
  }
}
```

## Handoff Format

### To Domain Orchestrator

```json
{
  "type": "task | query | subtask",
  "id": "TASK-001",
  "from": "meta-orchestrator",
  "to": "<domain>-orchestrator",
  "payload": {
    "description": "Task description",
    "context": "Relevant cross-domain context (minimal)",
    "constraints": [],
    "deadline": null
  },
  "routing": {
    "confidence": "high | medium | low",
    "signals": ["Keywords or paths that triggered routing"]
  }
}
```

### From Domain Orchestrator (Escalation)

```json
{
  "type": "escalate",
  "from": "<domain>-orchestrator",
  "original_task": "TASK-001",
  "reason": "out-of-scope | needs-decomposition | blocked",
  "relates_to": "Capability hint for re-routing",
  "context": "What was attempted, why it failed"
}
```

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Load full domain context | Use only domains.yaml registry |
| Make implementation decisions | Delegate to domain orchestrators |
| Route directly to agents | Always route to domain orchestrator |
| Hold cross-domain state | Pass state via handoff artifacts |

## Metrics Logging

On every routing decision:

```json
{
  "ts": "<ISO8601>",
  "task": "<task-id>",
  "agent": "meta-orchestrator",
  "event": "route",
  "tokens": { "in": 0, "out": 0, "source": "api_response | estimated" },
  "routing": {
    "to": "<domain>",
    "confidence": "high | medium | low",
    "cross_cutting": false
  }
}
```
