# Context Scripts Test Suite

Comprehensive tests for validation and generation scripts in `context/scripts/`.

## Test Coverage

### Validators (38 tests)

**conventional_commits.py** (11 tests)
- Valid commit format
- Invalid formats: no scope, too long, past tense
- Agent session metadata validation
- Co-Authored-By format
- Merge commit handling

**ears_notation.py** (10 tests)
- All EARS patterns: ubiquitous, event, state, optional, forbidden, complex
- Valid/invalid requirements files
- Code block exclusion
- Pattern recognition

**british_english.py** (7 tests)
- Valid British English
- American spelling detection: color, behavior, organize, center, license
- Code block and inline code exclusion

**metrics_logging.py** (10 tests)
- Valid JSONL format
- Required fields validation
- Timestamp, event, token source validation
- Handoff/escalate event requirements
- Empty files and invalid JSON handling

### Agent Validator (12 tests)

**validate_agent_definitions.py**
- YAML frontmatter validation
- Required fields: name, model, allowed_tools
- Hardcoded path detection
- Relative path flagging
- Critical reminders attribution
- {project-root} placeholder support
- Referenced standards/rules existence checks

### Generator & Adapter Projections (27 tests)

**generate_adapters.py & test_cli_dispatcher.py** (5 tests)
- Target normalization and aliases (all, gemini, claude, github, copilot, codex, openai)
- CLI parser flags and shortcuts (`-g`, `-c`, `-p`, `-o`, `-d`, `-a`, `-n`)
- Dry-run mode (`-d`) filesystem isolation
- Smart change detection (`--new` default) preserving mtimes on unchanged files
- Benchmark assertion: projection compilation in < 2.0s

**test_adapters_core.py** (5 tests)
- CanonicalAgent and WorkflowDAG dataclasses
- Loader validation and error handling for missing definitions
- Capability registry extensibility
- Token estimator budgeting

**test_gemini_adapter.py** (2 tests)
- Antigravity SKILL.md generation with standards and rules
- GEMINI.md generation with system instructions and model tier mappings

**test_claude_adapter.py** (2 tests)
- CLAUDE.md generation with system instructions and subagent spawning
- Subagent prompt generation in `.claude/prompts/`

**test_github_adapter.py** (3 tests)
- `.github/copilot-instructions.md` generation
- Custom prompts in `.github/prompts/*.prompt.md`
- Scoped instructions in `.github/instructions/*.instructions.md` via `applyTo` parsing

**test_openai_adapter.py** (3 tests)
- System prompts in `.openai/prompts/*.txt`
- Function calling schemas in `.openai/tools.json`
- Lightweight execution runner harness `.openai/runner.py`

**test_adapter_drift.py** (4 tests)
- Clean repository zero-drift verification
- Drift detection on modified projections
- Drift detection on missing projections
- Drift detection on orphaned files

**test_e2e_compilation.py** (3 tests)
- End-to-end multi-target compilation in an isolated directory (86+ files)
- Deterministic byte-for-byte reproducibility across repeated forced compilations
- Minimal synthetic context compilation verifying end-to-end pipeline

## Running Tests

```bash
# All tests
uv run pytest context/scripts/tests/ -v

# Specific test file
uv run pytest context/scripts/tests/test_cli_dispatcher.py -v
uv run pytest context/scripts/tests/test_adapter_drift.py -v
uv run pytest context/scripts/tests/test_e2e_compilation.py -v

# With coverage
uv run pytest context/scripts/tests/ --cov=context/scripts --cov-report=html
```

## Test Fixtures

Located in `fixtures/`:
- Commit messages (valid/invalid variants)
- Requirements files (valid/invalid EARS notation)
- British English samples
- Metrics JSONL files
- Workflow YAML
- Agent definitions (valid/invalid variants)

## Dependencies

- pytest >= 7.4.0
- pyyaml >= 6.0

Installed via root `pyproject.toml` dev dependencies or managed via `uv run`.

## Test Organisation

```
tests/
├── README.md                 # This file
├── conftest.py               # Pytest configuration and fixtures
├── test_validators.py        # Rule validator tests (conventional commits, EARS, British English, metrics)
├── test_agent_validator.py   # Agent definition validator tests
├── test_adapters_core.py     # Canonical IR loader and registry tests
├── test_gemini_adapter.py    # Antigravity/Gemini adapter tests
├── test_claude_adapter.py    # Claude Code adapter tests
├── test_github_adapter.py    # GitHub Copilot adapter tests
├── test_openai_adapter.py    # OpenAI/Codex adapter tests
├── test_cli_dispatcher.py    # generate_adapters.py CLI tests
├── test_adapter_drift.py     # adapter_drift.py validator tests
├── test_e2e_compilation.py   # End-to-end multi-target compilation tests
└── fixtures/                 # Test data files
```
