# Code Review: vis-service (2026-01-28)

**Status**: CHANGES REQUIRED | 3 critical, 5 high, 7 medium | 152/160 tests passing (87%)

## Critical (fix before deploy)

**CR-001** `data_client.py:41` Resource leak: HTTPx client not closed on exception.
→ Use `with httpx.Client() as client:` context manager.

**CR-002** `backtest.py:147` Wrong calculation: returns last trade value, not portfolio total.
→ Use `result.metrics.final_capital` instead.

**CR-003** `backtest_engine.py:201` Null crash: `band.lower` can be None for first N-1 points.
→ Add `if band.lower is None: return False` guard.

## High (this sprint)

| ID | Location | Issue | Fix |
|----|----------|-------|-----|
| CR-004 | bollinger.py:75 | Client per-request, no pooling | Use `Depends()` injection |
| CR-005 | main.py:21 | CORS allows all methods | Restrict to GET/POST/OPTIONS |
| CR-006 | bollinger.py:85 | Empty data returns 404 | Should be 400 |
| CR-007 | bollinger.py:78 | Broad `except Exception` | Catch specific errors |
| CR-008 | bollinger.py:65 | No type validation | Use Pydantic or add checks |

## Medium (next sprint)

CR-009 to CR-015: Hardcoded timeout, config path, no pagination, no rate limiting, no logging, duplicate watchlist entries, uncaught file errors. See JSON for details.

## Positives

Good TDD coverage, clean separation of concerns, consistent Pydantic usage, follows OpenAPI spec.

## Action

1. **Now**: Fix CR-001/002/003 (critical) and CR-004-008 (high)
2. **Soon**: Add rate limiting and logging
3. **Later**: Remaining medium issues, increase coverage to 90%
