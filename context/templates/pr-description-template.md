# PR Description Template

## Format

```markdown
## Summary

<1-3 sentence description of what this PR accomplishes>

## Changes

| Task | Description | Status |
|------|-------------|--------|
| #ID | Brief description | Done/Partial |

## Agent Metrics

| Metric | Value |
|--------|-------|
| Model | <primary-model> |
| Agents | <list> |
| Total Tokens | <in>/<out> |
| Duration | <time> |
| Commits | <count> |

<details>
<summary>Per-task breakdown</summary>

| Task | Agents | Tokens | Duration |
|------|--------|--------|----------|
| #ID | agents | in/out | time |

</details>

## Test Plan

- [ ] <verification step>

## Links

- [Task details](tasks.md)
- [Session metrics](metrics/session-log.jsonl)

---
Generated with [Claude Code](https://claude.ai/code)
```

## Section Details

### Summary (required)

One to three sentences. What does this PR do and why?

```markdown
## Summary

Implements webhook retry logic with exponential backoff. Addresses reliability
issues where failed endpoints were overwhelmed by immediate retries.
```

### Changes (required)

Table linking to task IDs with brief descriptions:

```markdown
## Changes

| Task | Description | Status |
|------|-------------|--------|
| DATA-003 | Add retry queue for failed webhooks | Done |
| DATA-004 | Implement exponential backoff logic | Done |
| DATA-005 | Add circuit breaker for repeated failures | Partial |
```

### Agent Metrics (required for agent PRs)

Aggregated metrics across all commits in the PR:

```markdown
## Agent Metrics

| Metric | Value |
|--------|-------|
| Model | claude-sonnet-4 |
| Agents | data-orchestrator, data-coder, data-reviewer |
| Total Tokens | 45.2K / 28.1K |
| Duration | 2h 15m |
| Commits | 4 |
```

### Per-Task Breakdown (optional, in collapsible)

For larger PRs, include per-task metrics in a collapsed section:

```markdown
<details>
<summary>Per-task breakdown</summary>

| Task | Agents | Tokens (in/out) | Duration |
|------|--------|-----------------|----------|
| DATA-003 | data-coder | 12.4K / 8.2K | 32m |
| DATA-004 | data-coder, data-reviewer | 18.6K / 11.4K | 58m |
| DATA-005 | data-coder | 14.2K / 8.5K | 45m |

</details>
```

### Test Plan (required)

Checklist of verification steps:

```markdown
## Test Plan

- [ ] Unit tests pass (`npm test`)
- [ ] Integration tests pass (`npm run test:integration`)
- [ ] Manual verification of retry behaviour
- [ ] Load test with simulated failures
```

### Links (required)

Always link to task details and metrics:

```markdown
## Links

- [Task details](tasks.md)
- [Session metrics](metrics/session-log.jsonl)
- [Relevant ADR](docs/adr/003-webhook-retry-strategy.md)
```

### Footer (required for agent PRs)

```markdown
---
Generated with [Claude Code](https://claude.ai/code)
```

## Complete Example

```markdown
## Summary

Implements webhook retry logic with exponential backoff to improve reliability
when downstream services are temporarily unavailable.

## Changes

| Task | Description | Status |
|------|-------------|--------|
| DATA-003 | Add retry queue for failed webhooks | Done |
| DATA-004 | Implement exponential backoff (base 2, max 5 attempts) | Done |
| DATA-005 | Add circuit breaker for repeated failures | Done |

## Agent Metrics

| Metric | Value |
|--------|-------|
| Model | claude-sonnet-4 |
| Agents | data-orchestrator, data-coder, data-reviewer |
| Total Tokens | 45.2K / 28.1K |
| Duration | 2h 15m |
| Commits | 4 |

<details>
<summary>Per-task breakdown</summary>

| Task | Agents | Tokens (in/out) | Duration |
|------|--------|-----------------|----------|
| DATA-003 | data-coder | 12.4K / 8.2K | 32m |
| DATA-004 | data-coder, data-reviewer | 18.6K / 11.4K | 58m |
| DATA-005 | data-coder | 14.2K / 8.5K | 45m |

</details>

## Test Plan

- [x] Unit tests pass
- [x] Integration tests with mock failing endpoint
- [ ] Manual verification in staging
- [ ] Load test with 10% simulated failures

## Assumptions Made

| Decision | Confidence | Impact |
|----------|------------|--------|
| Max 5 retry attempts sufficient | High | Low |
| 1 hour max delay acceptable | Medium | Medium |

## Links

- [Task details](tasks.md#data-003)
- [Session metrics](metrics/session-log.jsonl)
- [Blocker resolution](services/data-service/context/domain-rules.yaml#DATA-042)

---
Generated with [Claude Code](https://claude.ai/code)
```

## Human-Only PRs

Omit Agent Metrics section and footer:

```markdown
## Summary

Updates API documentation for new webhook endpoints.

## Changes

| Task | Description | Status |
|------|-------------|--------|
| DOC-001 | Document retry behaviour | Done |

## Test Plan

- [x] Documentation renders correctly
- [x] Code examples verified

## Links

- [Task details](tasks.md)
```
