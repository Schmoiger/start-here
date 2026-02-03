# Compressed Review Format

**Purpose**: Reduce review verbosity while preserving audit capability and human readability.

---

## Size Comparison (vis-service code-review)

| Format | Bytes | Tokens | Reduction |
|--------|-------|--------|-----------|
| Verbose prose | 18,451 | ~4,600 | Baseline |
| Comprehensive JSON | 6,887 | ~1,700 | 63% |
| Compressed prose | 1,578 | ~395 | **91%** |

**Recommendation**:
- Use **JSON** when agents need to parse and track issue resolution
- Use **compressed prose** for human-focused reviews and audit trails

---

## Why 91% Reduction is Possible

The verbose format wastes tokens on:

| Waste Category | Example | Compressed Alternative |
|----------------|---------|----------------------|
| Full file paths | `/Users/avi/Repos/bollinger/services/vis-service/src/...` | `data_client.py:41` |
| Code blocks (2x) | "Current code" + "Fix" blocks | One-line pattern + one-line fix |
| Impact explanations | 3-4 sentences explaining why it matters | Impact category tag |
| Section dividers | `---` between every issue | None (whitespace sufficient) |
| Verbose headers | `### [CR-001] Resource Leak - HTTPx Client Not Closed` | `**CR-001**` |

---

## Schema Location

```
context/standards/review-schema.json
```

---

## Issue Format (JSON)

```json
{
  "id": "CR-001",
  "severity": "critical",
  "category": "resource_leak",
  "location": "clients/data_client.py:41-43",
  "problem": "HTTPx client not closed on exception; leaks connections under load.",
  "fix": "Use context manager: `with httpx.Client() as client:`",
  "pattern": "client = httpx.Client",
  "impact": "crash"
}
```

**Key constraints**:
- `problem`: max 200 chars, one sentence
- `fix`: max 200 chars, one sentence
- `pattern`: optional grep-able string for finding the issue
- `location`: relative path with line number(s)

---

## Issue Format (Compressed Prose)

```markdown
**CR-001** `data_client.py:41` Resource leak: HTTPx client not closed on exception.
→ Use `with httpx.Client() as client:` context manager.
```

**Pattern**: `**ID** \`location\` Problem description. → Fix instruction.`

---

## Severity Categories

| Severity | Meaning | Action |
|----------|---------|--------|
| critical | Crashes, data corruption, security holes | Fix before deploy |
| high | Significant bugs, poor patterns | Fix this sprint |
| medium | Tech debt, minor issues | Fix next sprint |
| low | Nitpicks, style | Fix when convenient |

---

## Impact Categories

| Impact | Meaning |
|--------|---------|
| crash | Will cause runtime failure |
| data_corruption | Will produce wrong results |
| security_hole | Exploitable vulnerability |
| performance_degradation | Noticeably slower |
| poor_ux | Bad user experience |
| tech_debt | Makes future work harder |

---

## Converting Verbose to Compressed

### Step 1: Extract metadata
```
Verbose: "**Review Date**: 2026-01-28\n**Reviewer**: Claude Sonnet..."
Compressed: {"meta": {"date": "2026-01-28", "reviewer": "@code-reviewer"}}
```

### Step 2: Collapse issue blocks
```
Verbose (45 lines):
### [CR-001] Resource Leak - HTTPx Client Not Closed
- **File**: `/Users/avi/Repos/bollinger/services/...`
- **Severity**: Critical
- **Category**: Resource Management
- **Issue**:
  ```python
  # Current code
  client = httpx.Client(timeout=30.0)
  ...
  ```
- **Problem**: If the `get()` call raises an exception...
- **Fix**:
  ```python
  # Use context manager
  with httpx.Client(timeout=30.0) as client:
  ...
  ```
- **Impact**: Under high load...

Compressed (2 lines):
**CR-001** `data_client.py:41` Resource leak: HTTPx client not closed on exception.
→ Use `with httpx.Client() as client:` context manager.
```

### Step 3: Table for medium issues
```
Verbose: Full writeup for each medium issue (7 × 30 lines = 210 lines)
Compressed: One summary line + "See JSON for details"
```

---

## File Naming

```
services/{service}/artefacts/review/
  code-review.json       # Machine-parseable
  code-review.md         # Human-readable summary
  tech-review.json
  tech-review.md
```

---

## Tracking Issue Resolution

The JSON format supports tracking fixes:

```json
{
  "id": "CR-001",
  "severity": "critical",
  "fixed": true,
  "fixed_in": "abc123"  // commit hash
}
```

Query unfixed issues:
```bash
jq '.issues[] | select(.fixed != true)' code-review.json
```

---

## Agent Instructions

### For @code-reviewer / @tech-lead

1. Use JSON for comprehensive review
2. Keep `problem` and `fix` under 200 chars each
3. Include `pattern` for grep-able issues
4. Set `fixed: false` initially
5. Generate prose summary for humans

### For @python-coder / @react-coder

1. Parse JSON to get issue list
2. Fix in severity order (critical → high → medium)
3. Mark `fixed: true` and add `fixed_in` commit hash
4. Re-run review to verify

---

## Examples

- JSON format: `context/standards/review-example.json`
- Compressed prose: `context/standards/review-example-prose.md`
