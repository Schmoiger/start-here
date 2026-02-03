# Compressed Handoff Format

**Purpose**: Reduce inter-agent coordination overhead while preserving audit capability.

---

## Size Comparison

| Format | Bytes | Tokens | Reduction |
|--------|-------|--------|-----------|
| Prose HANDOFF.md | 9,526 | ~2,380 | Baseline |
| Comprehensive JSON | 5,266 | ~1,316 | 45% |
| Minimal JSON | 1,771 | ~443 | 81% |

**Recommendation**: Use comprehensive JSON for most handoffs. Use minimal JSON for simple phase transitions.

---

## Schema Location

```
context/standards/handoff-schema.json
```

Validate handoffs with:
```bash
npx ajv validate -s context/standards/handoff-schema.json -d path/to/HANDOFF.json
```

Or in Python:
```python
import jsonschema
import json

with open("context/standards/handoff-schema.json") as f:
    schema = json.load(f)
with open("services/vis-service/artefacts/build/HANDOFF.json") as f:
    handoff = json.load(f)

jsonschema.validate(handoff, schema)  # Raises on invalid
```

---

## Required Fields

Every handoff MUST include:

```json
{
  "meta": {
    "service": "string",      // e.g., "visualisation-service"
    "date": "YYYY-MM-DD",
    "phase": "enum",          // DISCOVERY|DESIGN|TDD_RED|TDD_GREEN|REVIEW|INTEGRATION|DEPLOY
    "from_agent": "@agent",   // e.g., "@functional-tester"
    "to_agent": "@agent"      // e.g., "@python-coder"
  },
  "summary": "string",        // Max 500 chars, human-readable
  "tasks_completed": [...],   // Array of task objects
  "next_tasks": [...],        // Array of task objects
  "status": "enum"            // ready|blocked|needs_review|failed
}
```

---

## Optional Fields (Use When Relevant)

| Field | When to Include |
|-------|-----------------|
| `blockers` | When status is not "ready" |
| `artefacts` | When files were created/modified |
| `stats` | For TDD phases (test counts, coverage) |
| `validation_rules` | When passing domain constraints |
| `dependencies` | When environment setup needed |
| `commits` | For audit trail |
| `context.key_decisions` | When non-obvious choices were made |
| `context.warnings` | When gotchas exist for next agent |
| `human_notes` | For human reviewers only |

---

## Task Object Format

```json
{
  "id": "VS-001",           // Required: Pattern [A-Z]{2,4}-\d{3}
  "name": "Brief name",     // Required: Max 100 chars
  "status": "complete",     // Required: complete|partial|blocked|skipped
  "tests": 20,              // Optional: Test count for TDD
  "artefacts": ["path"],    // Optional: Files created
  "notes": "If not complete"// Optional: Explanation
}
```

---

## Context Field: Avoiding Redundancy

The `context` field should reference shared documents, NOT duplicate them:

**Good** (reference):
```json
"context": {
  "architecture_ref": "artefacts/architecture/architecture.md",
  "key_decisions": ["Use JSON not Feather for Bronze layer"]
}
```

**Bad** (duplication):
```json
"context": {
  "architecture": "The system uses a three-service architecture with Data Service handling...[500 words]..."
}
```

---

## File Naming

```
services/{service}/artefacts/build/HANDOFF.json
```

Keep one HANDOFF.json per service, overwritten each phase. For history, use:

```
services/{service}/artefacts/build/handoff-history/
  HANDOFF-2026-01-27-TDD_RED.json
  HANDOFF-2026-01-28-TDD_GREEN.json
```

---

## Agent Instructions

### For Sending Agent

1. Validate JSON against schema before writing
2. Keep `summary` under 500 chars and self-contained
3. Reference shared docs in `context`, don't duplicate
4. Include `warnings` for non-obvious issues
5. Set `status` to "blocked" if next agent cannot proceed

### For Receiving Agent

1. Read `summary` first for overview
2. Check `status` - if not "ready", read `blockers`
3. Use `next_tasks` as work queue
4. Follow `context.architecture_ref` for design questions
5. Heed `context.warnings`

---

## Migration from Prose Format

To convert existing HANDOFF.md to JSON:

1. Extract metadata from header → `meta`
2. Summary paragraph → `summary` (truncate to 500 chars)
3. Task sections → `tasks_completed` array
4. "Next Steps" section → `next_tasks` array
5. Validation rules → `validation_rules` object
6. Dependencies list → `dependencies` object
7. Commit messages → `commits` array
8. Notes/warnings → `context.key_decisions` and `context.warnings`

---

## Examples

- Comprehensive: `context/standards/handoff-example.json`
- Minimal: `context/standards/handoff-example-minimal.json`
