# Tasks: {Service}

## Format

| Status | ID | Task | Deps | Location | Tokens | Duration |
|--------|-----|------|------|----------|--------|----------|

- **Tokens**: in/out with K suffix (e.g., 8.2K/5.1K) - populated on completion
- **Duration**: minutes or hours (e.g., 32m) - populated on completion
- **Location**: file path or `[ctx#id]` link to task-context file

## Tasks

| Status | ID | Task | Deps | Location | Tokens | Duration |
|--------|-----|------|------|----------|--------|----------|
| DONE | #DS-101 | Project structure | - | `src/data_service/` | 4.1K/2.8K | 18m |
| DONE | #DS-102 | Bronze store (raw JSON) | 101 | `storage/bronze.py` | 6.3K/4.2K | 25m |
| DONE | #DS-103 | Silver store (validated) | 102 | `storage/silver.py` | 7.8K/5.1K | 32m |
| DOING | #DS-104 | Cache with LRU eviction | 103 | [ctx#ds-104] | - | - |
| TODO | #DS-105 | yfinance client with retry | 101 | `clients/yfinance.py` | - | - |
| TODO | #DS-106 | Security search | 101 | `clients/search.py` | - | - |
| TODO | #DS-107 | /data/ohlcv endpoint | 104,105 | [ctx#ds-107] | - | - |
| TODO | #DS-108 | /data/search endpoint | 106 | `routers/search.py` | - | - |
| TODO | #DS-109 | /cache/* endpoints | 104 | `routers/cache.py` | - | - |
| TODO | #DS-110 | Health check with deps | 105 | `routers/health.py` | - | - |
| TODO | #DS-111 | Request ID middleware | - | `middleware/tracing.py` | - | - |
| TODO | #DS-112 | Error handling | - | `middleware/errors.py` | - | - |
| | | | | **Total** | **18.2K/12.1K** | **1h15m** |

[ctx#ds-104]: task-context-data-service.md#ds-104
[ctx#ds-107]: task-context-data-service.md#ds-107

## Blocked

| ID | Blocker | Owner |
|----|---------|-------|
| #DS-107 | Rate limiting approach undecided | @tech-lead |

## Metrics Flow

```
session-log.jsonl  →  Per-turn (source of truth)
    ↓ aggregate
tasks.md           →  Per-task (this file)
    ↓ aggregate
git commit         →  Per-commit (Agent-Session line)
    ↓ aggregate
PR description     →  Per-PR rollup
```
