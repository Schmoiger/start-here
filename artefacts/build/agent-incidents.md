# Agent Incidents

Framework failure log. Records cases where agents operated incorrectly due to missing, ambiguous, or conflicting standards.

**Distinct from**:
- `agent-interruptions.md` — blocking moments during a task ("I'm blocked right now")
- Git log Agent-Session lines — system telemetry (tokens, duration)

**Managed by**: Orchestrator via `context/workflows/continuous-improvement.yaml`

---

## Format

```
## INC-NNN — Short title
**Date**: YYYY-MM-DD
**Severity**: critical | high | medium | low
**Observed by**: @agent-name | human
**Symptom**: What was observed (behaviour, output, or failure mode)
**Root cause**: The specific rule, standard, or workflow gap that caused it
**Fix**: File paths changed + commit hash (added after fix is applied)
**Tasks**: Reference to tasks file entry (if applicable)
```

**Severity guide**:
- `critical` — caused data loss, security breach, or production incident
- `high` — caused incorrect output accepted by a quality gate
- `medium` — caused rework or a blocked task
- `low` — caused minor deviation corrected before handoff

---

## Incidents

_No incidents recorded yet._
