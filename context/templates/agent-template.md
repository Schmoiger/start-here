---
id: {domain}-{role}
type: agent
domain: {domain}
orchestrator: {domain}-orchestrator
model: {sonnet|opus|haiku}
tools: [Read, Write, Edit, Bash, Glob, Grep]
reads: [{paths}]
writes: [{paths}]
---

# {Agent Name}

{One-line description}

## Scope

```yaml
capabilities: [{capability-1}, {capability-2}]
paths: [src/{domain}/**, tests/{domain}/**]
```

## Constraints

| Rule | Rationale |
|------|-----------|
| {constraint} | {why} |

## Workflow

1. Receive handoff
2. {step}
3. {step}
4. Write handoff

## Deliverables

- {Primary output}: `{path}`
- Handoff: `artefacts/build/HANDOFF.json`
- Metrics: `metrics/session-log.jsonl`

## Escalation

**When**:
- Outside capabilities → escalate
- Other domain's paths → escalate
- Blocked externally → escalate
- High-impact uncertainty → escalate

**Assumption Handling**:
- Low impact → assume, document
- Medium impact → assume, flag for review
- High impact → escalate

## Handoff Format

Use `handoff.template.md` or JSON (see `handoff-schema.json`).

## Task

{$ARGUMENTS}
