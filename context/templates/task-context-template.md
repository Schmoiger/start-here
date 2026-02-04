# Task Context: {Service}

Implementation decisions and context for complex tasks. Simple tasks don't need entries here.

---

## DS-104

**Task**: Cache with LRU eviction
**Status**: DOING

### Decision: LRU over LFU

**Options considered**:
1. **LRU** (Least Recently Used) - evict oldest access
2. **LFU** (Least Frequently Used) - evict lowest access count
3. **TTL-only** - no eviction, just expiry

**Chose**: LRU

**Rationale**:
- Simpler to implement (OrderedDict in Python)
- Better for bursty access patterns (user checks same ticker repeatedly, then moves on)
- LFU would keep stale "popular" tickers even when user has moved on

**Trade-off accepted**: Recently accessed but rarely needed items may persist. Acceptable given 50MB limit.

### Implementation Notes

- Using `collections.OrderedDict` with `move_to_end()` on access
- Size tracking via `sys.getsizeof()` on serialised JSON
- Eviction triggers when size > limit, removes oldest until under 90% of limit

### Gotchas

- `sys.getsizeof()` doesn't account for nested objects; use `len(json.dumps())` instead
- Must acquire lock before eviction to prevent race with concurrent writes

---

## DS-107

**Task**: /data/ohlcv endpoint
**Status**: BLOCKED (rate limiting decision needed)

### Decision Needed: Rate Limiting Approach

**Options**:
1. **slowapi** (per-endpoint) - simple, FastAPI native
2. **Redis token bucket** - distributed, scales horizontally
3. **nginx rate limiting** - infrastructure level, no code

**Recommendation**: slowapi for P0 (simple), migrate to Redis for P1 if needed

**Waiting on**: @tech-lead approval

### Dependencies

- #DS-104 (cache) - must be complete to avoid hammering yfinance
- #DS-105 (yfinance client) - must handle rate limit responses from upstream

### API Contract

```
GET /data/ohlcv?ticker={ticker}&horizon={horizon}
Response: OHLCVResponse (see openapi.yaml)
Rate limit: 30 req/min (proposed)
```

---

## Template

```markdown
## {ID}

**Task**: {description}
**Status**: {DOING|BLOCKED|DONE}

### Decision: {title}

**Options considered**:
1. **{option}** - {description}

**Chose**: {option}

**Rationale**: {why}

**Trade-off accepted**: {what you gave up}

### Implementation Notes

- {notes}

### Gotchas

- {things to watch out for}
```
