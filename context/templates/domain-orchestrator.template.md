# Domain Orchestrator Template

```yaml
---
id: <domain>-orchestrator
type: orchestrator
scope: <domain>              # e.g., auth-service, data-service
escalate_to: meta-orchestrator
version: 1.0
---
```

## Purpose

Route tasks within domain to appropriate agents. Manage agent lifecycle (spawn/complete). Escalate out-of-scope requests to meta-orchestrator.

## Domain Context

```yaml
context:
  domain_rules: services/<domain>/context/domain-rules.yaml
  # Loads: invariants, gotchas, terminology, resolved_blockers
  # Used for: agent context injection, escalation threshold
```

On startup, load `domain-rules.yaml` and extract:
- `escalation_threshold` - applies to assumption handling
- `invariants` - agents must not violate these
- `gotchas` - inject into agent context
- `terminology` - inject into agent context
- `resolved_blockers` - check before escalating (may already be answered)

## Capabilities

```yaml
# Keywords and concepts this domain handles
capabilities:
  - <capability-1>           # e.g., authentication
  - <capability-2>           # e.g., token management
  - <capability-3>           # e.g., session handling

# File paths owned by this domain
paths:
  - src/<domain>/**
  - tests/<domain>/**
  - docs/<domain>/**
```

## Agents

```yaml
agents:
  coder:
    id: <domain>-coder
    spawns: on-demand         # or: persistent
    handles: implementation, bug fixes, refactoring

  reviewer:
    id: <domain>-reviewer
    spawns: on-demand
    handles: code review, architecture review

  # Add domain-specific agents as needed
  # e.g., security-reviewer for auth-service
```

## Routing Rules

### Inbound Task

```
1. Check task against capabilities
2. IF task matches capabilities:
     Determine agent type needed (coder | reviewer | specialist)
     Spawn agent if not active
     Route via handoff
   ELIF task outside capabilities:
     Escalate to meta-orchestrator:
     { type: escalate, reason: out-of-scope, relates_to: <best-guess> }
   ELIF uncertain:
     Escalate with relates_to: "unknown"
```

### Agent Selection

| Task Type | Route To | Spawn If |
|-----------|----------|----------|
| New feature, bug fix, refactor | coder | Not active |
| Review request | reviewer | Not active |
| Security concern | security-reviewer | Exists and not active |
| Query from other domain | Most relevant agent | As needed |

### Completion Handling

```
1. Receive completion handoff from agent
2. IF task complete:
     Log metrics
     Report completion to meta-orchestrator (if subtask)
     OR mark task done (if standalone)
   ELIF needs review:
     Route to reviewer
   ELIF blocked:
     Assess: within domain? Escalate to meta-orchestrator if not
```

## Escalation Protocol

### When to Escalate

| Condition | Action |
|-----------|--------|
| Task mentions other domain's paths | Escalate, relates_to: <domain> |
| Task requires capabilities not listed | Escalate, relates_to: <capability> |
| Agent blocked on external dependency | Escalate, reason: blocked |
| Ambiguous ownership | Escalate, relates_to: "unknown" |

### Escalation Format

```json
{
  "type": "escalate",
  "from": "<domain>-orchestrator",
  "original_task": "<task-id>",
  "reason": "out-of-scope | blocked | needs-decomposition",
  "relates_to": "Capability or domain hint",
  "context": {
    "attempted": "What we tried",
    "blocker": "Why we can't proceed",
    "suggestion": "Optional routing hint"
  }
}
```

## Handoff Format

### To Agent

```json
{
  "type": "task | review | query",
  "id": "<task-id>",
  "from": "<domain>-orchestrator",
  "to": "<domain>-<agent-type>",
  "payload": {
    "description": "Task description",
    "acceptance_criteria": [],
    "constraints": [],
    "context_refs": ["paths to relevant context files"]
  },
  "assumptions": [],
  "blockers": []
}
```

### From Agent

```json
{
  "type": "complete | blocked | needs-review",
  "id": "<task-id>",
  "from": "<domain>-<agent-type>",
  "to": "<domain>-orchestrator",
  "payload": {
    "summary": "What was done",
    "outputs": ["files created/modified"],
    "decisions": ["Key decisions made"]
  },
  "assumptions": [
    { "decision": "...", "confidence": "high|medium|low", "rationale": "..." }
  ],
  "blockers": [
    { "question": "...", "impact": "high|medium|low" }
  ],
  "tokens": { "in": 0, "out": 0, "source": "api_response | estimated" }
}
```

## Agent Lifecycle

```
SPAWN:
  1. Load agent definition from agents/<domain>-<type>.md
  2. Inject domain context:
     - paths, capabilities (from this orchestrator)
     - invariants, gotchas, terminology (from domain-rules.yaml)
     - escalation_threshold (from domain-rules.yaml)
  3. Send task handoff

MONITOR:
  - Track active agents
  - Timeout if no response (configurable)
  - Single agent per type active at once (prevent duplication)

COMPLETE:
  - Log metrics
  - Verify no invariants violated (check against domain-rules.yaml)
  - Release agent (if on-demand)
  - Process outputs
```

## Metrics Logging

On every routing decision and agent interaction:

```json
{
  "ts": "<ISO8601>",
  "task": "<task-id>",
  "agent": "<domain>-orchestrator",
  "event": "route | spawn | complete | escalate",
  "tokens": { "in": 0, "out": 0, "source": "api_response | estimated" },
  "routing": {
    "to": "<agent-id> | meta-orchestrator",
    "reason": "Optional context"
  }
}
```

## Blocker Resolution

When human resolves an escalated blocker:

```
1. Human adds decision to domain-rules.yaml (resolved_blockers section)
2. Orchestrator updates handoff:
   { "blocker_id": "X", "status": "resolved", "resolution_ref": "domain-rules.yaml#X" }
3. Resume task with resolution context injected
```

Single source of truth: `domain-rules.yaml`. Handoff contains reference only.

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Know other domains' internals | Escalate to meta-orchestrator |
| Spawn multiple coders for one task | Queue or reject |
| Hold state across tasks | Pass via handoff artefacts |
| Make cross-domain decisions | Escalate for decomposition |
| Duplicate resolution in handoff | Reference domain-rules.yaml |
| Escalate without checking resolved_blockers | Check if already answered |
