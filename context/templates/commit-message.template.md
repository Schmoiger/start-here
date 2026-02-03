# Commit Message Template

## Format

```
<type>(<scope>): <subject>

<body>

Tasks: <task-ids>
Agent-Session: <metrics-line>

Co-Authored-By: Claude <model> <<model>@anthropic.com>
```

## Components

### Subject Line (required)

Conventional commits format, max 72 characters:

```
feat(auth): add token refresh endpoint
fix(data): prevent negative balance on refund
refactor(api): extract validation middleware
```

### Body (optional)

Brief context if subject is insufficient. Focus on "why" not "what".

```
Implements exponential backoff for webhook retries.
Previous fixed-interval approach overwhelmed failing endpoints.
```

### Tasks (required)

Reference task IDs from tasks.md:

```
Tasks: AUTH-001, AUTH-002
```

### Agent-Session (required for agent commits)

Single-line metrics block, machine-parseable:

```
Agent-Session: model=sonnet agents=auth-coder,auth-reviewer tokens=12.4K/8.2K duration=45m
```

| Field | Format | Example |
|-------|--------|---------|
| model | sonnet\|opus\|haiku | model=sonnet |
| agents | comma-separated | agents=auth-coder,auth-reviewer |
| tokens | in/out with K suffix | tokens=12.4K/8.2K |
| duration | minutes or hours | duration=45m |

### Co-Authored-By (required for agent commits)

GitHub-recognised trailer format:

```
Co-Authored-By: Claude Sonnet <sonnet@anthropic.com>
Co-Authored-By: Claude Opus <opus@anthropic.com>
Co-Authored-By: Claude Haiku <haiku@anthropic.com>
```

Use the primary model that generated the code.

## Examples

### Simple Feature

```
feat(auth): add token refresh endpoint

Tasks: AUTH-001
Agent-Session: model=sonnet agents=auth-coder tokens=8.2K/5.1K duration=32m

Co-Authored-By: Claude Sonnet <sonnet@anthropic.com>
```

### Multi-Task with Review

```
feat(data): implement retry logic for webhooks

Exponential backoff with max 5 attempts.
Addresses reliability issues from incident INC-042.

Tasks: DATA-003, DATA-004
Agent-Session: model=sonnet agents=data-coder,data-reviewer tokens=15.6K/9.8K duration=58m

Co-Authored-By: Claude Sonnet <sonnet@anthropic.com>
```

### Bug Fix with Blocker Resolution

```
fix(payments): correct decimal precision on refunds

Tasks: PAY-012
Agent-Session: model=opus agents=payments-coder tokens=6.1K/3.2K duration=18m
Blocker-Resolved: PAY-042 (see domain-rules.yaml#PAY-042)

Co-Authored-By: Claude Opus <opus@anthropic.com>
```

### Human-Only Commit

```
docs: update API documentation

Tasks: DOC-001
```

No Agent-Session or Co-Authored-By for human-only commits.

## Parsing

The Agent-Session line is designed for automated extraction:

```bash
# Extract metrics from git log
git log --format='%b' | grep '^Agent-Session:' | \
  sed 's/Agent-Session: //' | \
  awk -F' ' '{print $0}'
```

```python
# Parse metrics line
import re
pattern = r'model=(\w+) agents=([\w,-]+) tokens=([\d.]+K)/([\d.]+K) duration=(\d+[mh])'
match = re.search(pattern, line)
```

## Link to Detailed Metrics

For per-task breakdown, see:
- `tasks.md` - task status and summary
- `metrics/session-log.jsonl` - full token log per agent turn
