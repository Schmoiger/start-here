# Rule Validators

Automated validators for enforceable rules in the Bollinger project.

## Overview

These validators enforce consistency across the codebase by checking:

1. **conventional_commits.py** - Commit message format compliance
2. **ears_notation.py** - Requirements using EARS notation syntax
3. **british_english.py** - British English spelling conventions
4. **metrics_logging.py** - Agent metrics logging format

## Installation

Install pre-commit hooks:

```bash
uv add --dev pre-commit
uv run pre-commit install
uv run pre-commit install --hook-type commit-msg
```

## Usage

### Manual Validation

Run individual validators:

```bash
# Validate commit message
uv run python scripts/validators/conventional_commits.py .git/COMMIT_EDITMSG

# Validate requirements file
uv run python scripts/validators/ears_notation.py artifacts/product/requirements.md

# Validate British English in file
uv run python scripts/validators/british_english.py README.md

# Validate metrics log
uv run python scripts/validators/metrics_logging.py metrics/session-log.jsonl
```

### Pre-Commit Hooks

Hooks run automatically on commit:

```bash
git commit -m "feat(validation): add validators"
```

Run manually on all files:

```bash
uv run pre-commit run --all-files
```

Run specific hook:

```bash
uv run pre-commit run conventional-commits
uv run pre-commit run ears-notation
uv run pre-commit run british-english
uv run pre-commit run metrics-logging
```

## Validator Details

### Conventional Commits (`conventional_commits.py`)

Validates commit messages against the format specified in `context/rules/conventional-commits.mdc`.

**Format:**
```
{type}({scope}): {description}

{optional body}

Tasks: {task-ids}
Agent-Session: model={model} agents={list} tokens={in}K/{out}K duration={time}

Co-Authored-By: Claude {Model} <{model}@anthropic.com>
```

**Valid types:** feat, fix, test, refactor, docs, chore, perf

**Constraints:**
- Max 72 characters for subject line
- Scope: lowercase, alphanumeric with hyphens
- Description: imperative mood (e.g., "add" not "added")
- Agent commits require Agent-Session and Co-Authored-By

**Examples:**

Valid:
```
feat(validation): add rule validators
fix(data-service): correct bollinger band calculation
test(llm-service): improve coverage for prompt templates
```

Invalid:
```
added validation          # Missing type and scope
feat: add validation      # Missing scope
feat(validation) add      # Missing colon
feat(Validation): add     # Scope not lowercase
```

### EARS Notation (`ears_notation.py`)

Validates requirements files use EARS (Easy Approach to Requirements Syntax) notation as specified in `context/rules/EARS-notation-requirements.mdc`.

**Patterns:**

| Type | Syntax | Example |
|------|--------|---------|
| Ubiquitous | THE {system} SHALL {action} | THE system SHALL encrypt all user data |
| Event | WHEN {trigger}, THE {system} SHALL {action} | WHEN user clicks Save, THE system SHALL persist changes |
| State | WHILE {state}, THE {system} SHALL {action} | WHILE in maintenance mode, THE system SHALL show notice |
| Optional | IF {condition}, THE {system} SHALL {action} | IF user is admin, THE system SHALL show admin menu |
| Forbidden | THE {system} SHALL NOT {action} | THE system SHALL NOT log passwords |
| Complex | WHEN {trigger}, IF {condition}, THE {system} SHALL {action} | WHEN user clicks Print, IF printer offline, THE system SHALL show error |

**Target files:**
- `artifacts/product/requirements.md`
- `artifacts/product/user-stories.md`

**Examples:**

Valid:
```
THE system SHALL validate all user inputs before processing
WHEN user submits form, THE system SHALL display confirmation message
IF user is authenticated, THE system SHALL show dashboard
```

Invalid:
```
System must validate inputs              # No "shall"
The system should validate               # "should" not "shall"
System shall be validated                # Wrong structure (missing "THE")
```

### British English (`british_english.py`)

Validates British English spelling as specified in `context/rules/british-english.mdc`.

**Common corrections:**

| American | British |
|----------|---------|
| color | colour |
| behavior | behaviour |
| organize | organise |
| realize | realise |
| recognize | recognise |
| center | centre |
| license (noun) | licence |

**Target files:** `.md`, `.py`, `.ts`, `.tsx`, `.js`, `.jsx`

**Exclusions:** Code blocks (```) and inline code (`)

**Examples:**

Valid:
```
The system uses colour schemes for visualisation
Users can organise their data by category
```

Invalid:
```
The system uses color schemes              # American spelling
Users can organize their data              # American spelling
```

### Metrics Logging (`metrics_logging.py`)

Validates agent metrics log entries as specified in `context/rules/metrics-logging.mdc`.

**Schema:**
```json
{
  "ts": "ISO8601 timestamp",
  "task": "task-id",
  "agent": "agent-id",
  "event": "start|handoff|escalate|complete|blocked",
  "tokens": {
    "in": 0,
    "out": 0,
    "source": "api_response|estimated|unavailable"
  },
  "to": "target-agent (for handoff/escalate)",
  "notes": "optional context"
}
```

**Target files:** `metrics/*.jsonl`

**Examples:**

Valid:
```jsonl
{"ts":"2025-01-28T09:00:00Z","task":"AUTH-001","agent":"auth-coder","event":"start","tokens":{"in":0,"out":0,"source":"unavailable"}}
{"ts":"2025-01-28T09:45:00Z","task":"AUTH-001","agent":"auth-coder","event":"complete","tokens":{"in":2340,"out":1890,"source":"api_response"},"to":"auth-orchestrator"}
```

Invalid:
```jsonl
{"ts":"2025-01-28","task":"AUTH-001"}                    # Missing required fields
{"ts":"2025-01-28T09:00:00Z","task":"AUTH-001","event":"invalid"}  # Invalid event type
```

## Exit Codes

All validators follow the same exit code convention:

- `0` - Validation passed
- `1` - Validation failed (with error messages)

## Configuration

Pre-commit configuration is in `.pre-commit-config.yaml` at project root.

To skip pre-commit hooks temporarily:

```bash
git commit --no-verify -m "message"
```

## Development

### Adding New Validators

1. Create validator script in `scripts/validators/`
2. Make executable: `chmod +x scripts/validators/new_validator.py`
3. Add hook to `.pre-commit-config.yaml`
4. Test with `uv run pre-commit run <hook-id> --all-files`

### Testing Validators

```bash
# Test conventional commits
echo "feat(test): add feature" > /tmp/test-commit.txt
uv run python scripts/validators/conventional_commits.py /tmp/test-commit.txt

# Test EARS notation
echo "THE system SHALL validate input" > /tmp/test-req.md
uv run python scripts/validators/ears_notation.py /tmp/test-req.md

# Test British English
echo "This uses colour not color" > /tmp/test-eng.md
uv run python scripts/validators/british_english.py /tmp/test-eng.md

# Test metrics logging
echo '{"ts":"2025-01-28T09:00:00Z","task":"T-001","agent":"coder","event":"start","tokens":{"in":0,"out":0,"source":"unavailable"}}' > /tmp/metrics/test.jsonl
uv run python scripts/validators/metrics_logging.py /tmp/metrics/test.jsonl
```

## Troubleshooting

### Pre-commit hook not running

```bash
# Reinstall hooks
uv run pre-commit uninstall
uv run pre-commit install
uv run pre-commit install --hook-type commit-msg
```

### Validator fails on valid input

Check rule definition in `context/rules/*.mdc` and update validator logic if rules have changed.

### Too many false positives

Consider adjusting validator patterns or adding exclusions to `.pre-commit-config.yaml`.

## References

- Rule definitions: `context/rules/*.mdc`
- Pre-commit documentation: https://pre-commit.com/
- Conventional Commits: https://www.conventionalcommits.org/
- EARS notation: https://www.researchgate.net/publication/224079253_Easy_Approach_to_Requirements_Syntax_EARS
