# Commit Message Template

## Format

```
<type>(<scope>): <subject>

<body>

Tasks: <task-ids>
Agent-Session: tool=<tool> model=<model> agents=<agent-ids> tokens=<in>K/<out>K duration=<time>

Co-Authored-By: <tool-or-identifier> <<email>>
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

Single-line metrics block, machine-parseable. **Record the triplet accurately: tool, model, and agent(s).**

```
Agent-Session: tool=<tool> model=<model> agents=<agent-ids> tokens=<in>K/<out>K duration=<time>
```

| Field | Format | Example |
|-------|--------|---------|
| tool | The IDE/platform that ran the model | tool=cursor, tool=claude-ide, tool=copilot, tool=windsurf |
| model | The model/backend used | model=sonnet, model=opus, model=gpt-4, model=claude-3-5-sonnet |
| agents | Agent role(s) from context/agents | agents=python-coder, agents=functional-tester,code-reviewer |
| tokens | in/out with K suffix | tokens=12.4K/8.2K |
| duration | minutes or hours | duration=45m |

**Triplet**: Always list the actual (tool, model, agent) for this commit. Agent names are from `context/agents/*.md` (e.g. python-coder, typescript-coder, functional-tester, code-reviewer, tech-lead). Do not substitute a default; use what was actually used.

### Co-Authored-By (required for agent commits)

GitHub-recognised trailer format. Use a line that identifies the tool (or tool + model) so the commit is attributed correctly. The **authoritative triplet** is in the Agent-Session line; Co-Authored-By is for GitHub display.

```
Co-Authored-By: Cursor <cursor@cursor.com>
Co-Authored-By: Claude Sonnet <sonnet@anthropic.com>
Co-Authored-By: GitHub Copilot <copilot@github.com>
```

Match the tool (and optionally model) to what is in Agent-Session. Do not use a fixed co-author; use the actual tool/model that was used.

## Examples

### Simple Feature

```
feat(auth): add token refresh endpoint

Tasks: AUTH-001
Agent-Session: tool=cursor model=sonnet agents=python-coder tokens=8.2K/5.1K duration=32m

Co-Authored-By: Cursor <cursor@cursor.com>
```
(Triplet: cursor + sonnet + python-coder; list what was actually used.)

### Multi-Task with Review

```
feat(data): implement retry logic for webhooks

Exponential backoff with max 5 attempts.
Addresses reliability issues from incident INC-042.

Tasks: DATA-003, DATA-004
Agent-Session: tool=cursor model=sonnet agents=python-coder,code-reviewer tokens=15.6K/9.8K duration=58m

Co-Authored-By: Cursor <cursor@cursor.com>
```
(Triplet: tool, model, agents from context/agents.)

### Bug Fix with Blocker Resolution

```
fix(payments): correct decimal precision on refunds

Tasks: PAY-012
Agent-Session: tool=claude-ide model=opus agents=python-coder tokens=6.1K/3.2K duration=18m
Blocker-Resolved: PAY-042 (see domain-rules.yaml#PAY-042)

Co-Authored-By: Claude Opus <opus@anthropic.com>
```
(Triplet reflects actual tool, model, and agent.)

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
# Parse metrics line (triplet: tool, model, agents)
import re
pattern = r'tool=([a-z0-9-]+) model=([a-z0-9.-]+) agents=([\w,-]+) tokens=([\d.]+K)/([\d.]+K) duration=(\d+[mh])'
match = re.search(pattern, line)
# match.group(1)=tool, (2)=model, (3)=agents, (4)=tokens_in, (5)=tokens_out, (6)=duration
```

## Link to Detailed Metrics

For per-task breakdown, see:
- `tasks.md` - task status and summary
- `metrics/session-log.jsonl` - full token log per agent turn
