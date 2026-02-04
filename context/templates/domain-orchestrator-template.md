# {Domain} Orchestrator

```yaml
id: {domain}-orchestrator
type: orchestrator
scope: {domain}
escalate_to: meta-orchestrator
context: services/{domain}/context/domain-rules.yaml
```

## Purpose

Route tasks within domain. Manage agent lifecycle. Escalate out-of-scope requests.

## Capabilities

```yaml
capabilities: [{capability-1}, {capability-2}]
paths: [src/{domain}/**, tests/{domain}/**]
```

## Agents

| Agent | Spawns | Handles |
|-------|--------|---------|
| {domain}-coder | on-demand | implementation, bugs, refactoring |
| {domain}-reviewer | on-demand | code review, architecture review |

## Routing

**Inbound**:
1. Check capabilities match
2. If match → spawn agent, route via handoff
3. If no match → escalate to meta-orchestrator

**Agent Selection**:
- Implementation/bugs → coder
- Review → reviewer
- Other domain → escalate

**Completion**:
- Complete → log metrics, report to meta
- Needs review → route to reviewer
- Blocked outside domain → escalate

## Escalation

**When**:
- Other domain's paths → escalate
- Missing capabilities → escalate
- Agent blocked externally → escalate

**Format**: See `handoff-schema.json`

## Handoff Format

Use `handoff-template.md` or JSON format (see `handoff-schema.json`).

## Lifecycle

**Spawn**: Load agent definition → inject context → send handoff
**Monitor**: Track active agents, timeout, single agent per type
**Complete**: Log metrics, verify invariants, release agent

## Blocker Resolution

1. Human adds to `domain-rules.yaml` (resolved_blockers)
2. Reference in handoff: `resolution_ref: "domain-rules.yaml#X"`
3. Resume with context
