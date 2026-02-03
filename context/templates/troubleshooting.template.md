# Troubleshooting: {Service}

Context for complex bugs. Simple bugs don't need entries here.

---

## DATA-003

**Issue**: Retry fires immediately INSTEAD exponential backoff
**Location**: `clients/yfinance_client.py:78`
**Status**: RESOLVED (2026-01-28)

### Attempts

1. **Add sleep in retry loop**: FAILED
   - Missing `continue` after sleep; exception re-raised before reaching it
   - Learnt: Trace actual execution path; don't assume code reaches a line

2. **Fix control flow**: FAILED
   - Implementation was correct; test assertions were wrong (checking wall-clock not delays)
   - Learnt: Verify test expectations before assuming impl is broken

3. **Fix test expectations**: SUCCESS
   - Mock `time.sleep` and verify call arguments
   - Commit: `a1b2c3d`

### Root Cause

Two compounding issues: code bug (missing continue) AND test bug (wrong assertion). Attempt 1 fixed the code but we didn't notice because test was also broken.

### Prevention

- [x] Test: `test_retry_delays_are_exponential`
- [x] Docs: Retry behaviour in README

---

## DATA-007

**Issue**: Cache refresh races with concurrent requests
**Location**: `storage/cache.py:201`
**Status**: ACTIVE

### Attempts

1. **Add lock around refresh**: FAILED
   - Deadlock when refresh calls fetch which checks cache
   - Learnt: Don't hold locks across async boundaries

2. **Use asyncio.Event for coordination**: IN PROGRESS
   - Hypothesis: Let first request trigger refresh, others await the event

---

## VIS-012

**Issue**: Band calculation wrong for first N points
**Location**: `calculators/bollinger.py:45`
**Status**: RESOLVED (2026-01-27)

### Attempts

1. **Check for None**: FAILED
   - pandas returns NaN not None; `if value is None` doesn't catch it
   - Learnt: NaN != None in pandas; use `pd.isna()`

2. **Use pd.isna()**: SUCCESS
   - Commit: `b2c3d4e`

### Root Cause

pandas represents missing values as NaN (float), not None. Python `is None` check passes, comparison then fails.

---

## Template

Copy this for new entries:

```markdown
## {ID}

**Issue**: {actual} INSTEAD {expected}
**Location**: `{file}:{line}`
**Status**: ACTIVE

### Attempts

1. **{approach}**: FAILED
   - {what happened}
   - Learnt: {insight}

### Root Cause

{explanation when resolved}
```
