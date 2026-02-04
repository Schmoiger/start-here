# Meta-Orchestrator

```yaml
id: meta-orchestrator
type: orchestrator
scope: repository
context: domains.yaml
```

## Purpose

Route tasks to domain orchestrators. Decompose cross-cutting tasks. Handle escalations.

## Routing

**Inbound**:
1. Parse for domain signals
2. If single match → route to domain
3. If multiple matches → decompose into subtasks
4. If no match → route to most likely or escalate to human

**Escalation from Domain**:
1. Match `relates_to` against domain capabilities
2. Route to matched domain or escalate to human

**Cross-Cutting**: Decompose into sequenced subtasks with dependencies

## Handoff Format

Use `handoff-template.md` or JSON format (see `handoff-schema.json`).

## Anti-Patterns

❌ Load full domain context → Use domains.yaml only
❌ Route directly to agents → Always route to domain orchestrator
❌ Make implementation decisions → Delegate to domains
