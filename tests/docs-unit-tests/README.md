# Documentation Unit Tests

Unit tests for validating documentation consistency and format.

## Quick Start

```bash
# Install dependencies
pip install -r tests/docs-unit-tests/requirements.txt

# Run all Python tests
pytest tests/docs-unit-tests/ -v

# Run shell tests (requires bats-core)
bats tests/docs-unit-tests/coordinate.bats
```

## Test Files

| File | Description | LLM Required |
|------|-------------|--------------|
| `test_doc_format.py` | Validates YAML frontmatter, required sections, markdown syntax | No |
| `test_references.py` | Validates cross-references between docs, agent-standards consistency | No |
| `test_llm_consistency.py` | Semantic consistency checks via LLM call | Yes |
| `coordinate.bats` | Shell tests for coordinate.sh worktree management | No |

## Running Tests

### Static Analysis (Fast, No LLM)

Run on every PR - these tests are fast and don't require API keys:

```bash
# Format validation
pytest tests/docs-unit-tests/test_doc_format.py -v

# Cross-reference validation
pytest tests/docs-unit-tests/test_references.py -v

# Shell script tests
bats tests/docs-unit-tests/coordinate.bats
```

### LLM Consistency Check (Slow, Requires API Key)

Run periodically or on significant doc changes:

```bash
export ANTHROPIC_API_KEY=your-key
pytest tests/docs-unit-tests/test_llm_consistency.py -v
```

The LLM test performs a single API call to check for:
- File reference errors
- Agent name mismatches
- Domain inconsistencies between agent-standards.md and coordinate.sh
- Artifact path conflicts
- Standards contradictions
- Missing cross-references

## What Each Test Validates

### test_doc_format.py

**Agent Files:**
- All agent files have YAML frontmatter
- Frontmatter is valid YAML
- Required fields present: `name`, `description`
- Frontmatter `name` matches filename
- `{$ARGUMENTS}` placeholder present
- `## Constraints` section present

**Standards Files:**
- Introduction section present (warning only)

**Rules Files:**
- YAML frontmatter present (warning only)

**All Markdown:**
- No malformed link syntax

### test_references.py

- Context paths in agents reference valid patterns
- File references in standards point to existing files
- Agents listed in agent-standards.md have definition files
- Domains in coordinate.sh match agent-standards.md
- Links in docs/README.md are valid

### coordinate.bats

- coordinate.sh is executable
- All commands work: help, list, workflow, structure, init
- Worktree commands: create, list, switch, sync
- Directory structure created correctly
- Domain configuration matches expectations

## CI Integration

The GitHub Actions workflow (`.github/workflows/docs-test.yml`) runs:

1. **lint** job: Static analysis tests (always runs)
2. **shell** job: Bats tests for coordinate.sh (always runs)
3. **llm-consistency** job: LLM checks (optional, requires secret)

To enable LLM tests in CI:
1. Add `ANTHROPIC_API_KEY` as a repository secret
2. Set repository variable `RUN_LLM_TESTS=true`

## Adding New Tests

When adding new documentation:
1. Agent definitions → Tests in `test_doc_format.py` validate automatically
2. New standards → Add to skip patterns if using example paths
3. New rules → Frontmatter optional but recommended
4. New cross-references → `test_references.py` validates automatically

## Dependencies

```
pytest>=7.0.0
pyyaml>=6.0
anthropic>=0.18.0  # Only for LLM tests
bats-core           # For shell tests (brew install bats-core)
```
