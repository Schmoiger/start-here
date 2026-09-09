# Tasks: Build Runtime Adapters

**Branch**: `env/runtime-adapters`  
**Status**: Planning  
**Scope**: Build the multi-platform runtime adapter system to compile canonical `context/` assets into native configurations, prompts, and tool mappings for Claude Code, Google Gemini / Antigravity, GitHub Copilot, and OpenAI Codex.  
**Design**: `artefacts/architecture/architecture.md`  
**Created**: 2026-09-09  
**Amended**: N/A  

---

## Orchestrator Notes

### Parallelism Strategy

Tasks are grouped into six sequential sprints. Within each sprint, tasks with disjoint file scopes can be executed in parallel.

- **Sprint 1 (Foundation)**: AD-1 → AD-2 + AD-3 (parallel)  
  *file_scope*: `context/scripts/generators/adapters/core/`, `context/standards/`
- **Sprint 2 (Claude & Gemini)**: AD-4 + AD-5 (parallel) → AD-6 + AD-7 (parallel)  
  *file_scope*: `context/scripts/generators/adapters/claude/`, `context/scripts/generators/adapters/gemini/`, `.agents/`
- **Sprint 3 (GitHub & Codex)**: AD-8 + AD-9 (parallel) → AD-10 + AD-11 (parallel)  
  *file_scope*: `context/scripts/generators/adapters/github/`, `context/scripts/generators/adapters/codex/`, `.github/`
- **Sprint 4 (CLI & Drift Enforcement)**: AD-12 → AD-13 + AD-14 (parallel)  
  *file_scope*: `context/scripts/generators/generate_adapters.py`, `context/scripts/validators/`
- **Sprint 5 (Docs & E2E Verification)**: AD-15 + AD-16 (parallel) → AD-17  
  *file_scope*: `context/docs/`, `context/scripts/tests/`, `README.md`
- **Sprint 6 (Packaging & Distribution)**: AD-18 + AD-19 (parallel)  
  *file_scope*: `pyproject.toml`, `cookiecutter.json`, `{{cookiecutter.project_name}}/`

### Commit Strategy

One commit per task on branch `env/runtime-adapters`. Conventional commit format:

| Task | Commit message |
|------|---------------|
| AD-1 | `feat(adapters): define intermediate canonical representation and schema` |
| AD-2 | `feat(adapters): implement abstract tool capability mapping registry` |
| AD-3 | `feat(adapters): implement context budgeting and ingestion strategies` |
| AD-4 | `feat(adapters): implement claude code adapter generator` |
| AD-5 | `feat(adapters): implement gemini and antigravity adapter generator` |
| AD-6 | `test(adapters): add test suite for claude and gemini adapters` |
| AD-7 | `feat(adapters): generate initial claude and gemini projections` |
| AD-8 | `feat(adapters): implement github copilot adapter generator` |
| AD-9 | `feat(adapters): implement codex and openai adapter generator` |
| AD-10 | `test(adapters): add test suite for github and codex adapters` |
| AD-11 | `feat(adapters): generate initial github and codex projections` |
| AD-12 | `feat(adapters): create unified generate_adapters.py cli dispatcher` |
| AD-13 | `feat(validators): implement adapter_drift.py pre-commit validator` |
| AD-14 | `ci(hooks): wire adapter drift verification into git pre-commit hooks` |
| AD-15 | `docs(adapters): update framework reference and architecture documentation` |
| AD-16 | `test(adapters): add end-to-end multi-target compilation tests` |
| AD-17 | `chore(build): final quality review and tasks sign-off` |
| AD-18 | `feat(packaging): scaffold cruft and cookiecutter template for framework distribution` |
| AD-19 | `build(packaging): configure pyproject.toml to publish generator engine as CLI library` |

Push cadence: Push after each completed sprint.

### Effort Estimates

| Task | Agent(s) | Effort |
|------|----------|--------|
| AD-1 | solution-architect | Medium (30–50k tokens) |
| AD-2 | python-coder | Medium (30–50k tokens) |
| AD-3 | python-coder | Small (20–30k tokens) |
| AD-4 | python-coder | Medium (40–60k tokens) |
| AD-5 | python-coder | Medium (40–60k tokens) |
| AD-6 | functional-tester | Medium (30–50k tokens) |
| AD-7 | python-coder | Small (15–25k tokens) |
| AD-8 | python-coder | Medium (40–60k tokens) |
| AD-9 | python-coder | Medium (40–60k tokens) |
| AD-10 | functional-tester | Medium (30–50k tokens) |
| AD-11 | python-coder | Small (15–25k tokens) |
| AD-12 | python-coder | Medium (30–50k tokens) |
| AD-13 | python-coder | Small (20–30k tokens) |
| AD-14 | devops | Small (15–25k tokens) |
| AD-15 | documentation | Medium (30–50k tokens) |
| AD-16 | functional-tester | Medium (35–55k tokens) |
| AD-17 | tech-lead | Small (15–25k tokens) |
| AD-18 | devops | Medium (30–50k tokens) |
| AD-19 | devops | Small (20–30k tokens) |
| **Total** | | **~520–800k tokens** |

---

## Task Index (required)

Update status immediately when work begins and when it completes. Every task in the index has a matching specification section below.

### Sprint 1: Adapter Foundation & Tool Mapping Schema

| ID | Pri | Status | Blocked By | Task |
|----|-----|--------|------------|------|
| AD-1 | critical | pending | - | Define intermediate canonical representation model and loader |
| AD-2 | high | pending | AD-1 | Implement abstract tool capability mapping registry |
| AD-3 | high | pending | AD-1 | Implement context budgeting and token delivery strategies |

### Sprint 2: Claude Code & Gemini / Antigravity Adapters

| ID | Pri | Status | Blocked By | Task |
|----|-----|--------|------------|------|
| AD-4 | critical | pending | AD-2, AD-3 | Implement Claude Code adapter (`CLAUDE.md`, `AGENTS.md`, subagent prompts) |
| AD-5 | critical | pending | AD-2, AD-3 | Implement Gemini / Antigravity adapter (skills, `GEMINI.md`, MCP bindings) |
| AD-6 | high | pending | AD-4, AD-5 | Add unit test suite for Claude and Gemini adapter generators |
| AD-7 | medium | pending | AD-6 | Generate and verify initial Claude and Gemini projections in repository |

### Sprint 3: GitHub Copilot & Codex / OpenAI Adapters

| ID | Pri | Status | Blocked By | Task |
|----|-----|--------|------------|------|
| AD-8 | high | pending | AD-2, AD-3 | Implement GitHub Copilot adapter (`.github/copilot-instructions.md`, prompt files) |
| AD-9 | high | pending | AD-2, AD-3 | Implement Codex / OpenAI adapter (system prompts, tool JSON schemas, runner harness) |
| AD-10 | high | pending | AD-8, AD-9 | Add unit test suite for GitHub and Codex adapter generators |
| AD-11 | medium | pending | AD-10 | Generate and verify initial GitHub and Codex projections in repository |

### Sprint 4: Unified Adapter CLI & Drift Enforcement

| ID | Pri | Status | Blocked By | Task |
|----|-----|--------|------------|------|
| AD-12 | high | pending | AD-7, AD-11 | Create unified `generate_adapters.py` CLI dispatcher |
| AD-13 | high | pending | AD-12 | Implement `adapter_drift.py` pre-commit validator |
| AD-14 | medium | pending | AD-13 | Wire adapter drift check into `.pre-commit-config.yaml` |

### Sprint 5: Documentation & End-to-End Verification

| ID | Pri | Status | Blocked By | Task |
|----|-----|--------|------------|------|
| AD-15 | medium | pending | AD-12 | Update framework reference and portability adapter documentation |
| AD-16 | high | pending | AD-12, AD-13 | Add end-to-end multi-target compilation test suite |
| AD-17 | critical | pending | AD-15, AD-16 | Quality gate review: verify all 4 adapters compile without errors |

### Sprint 6: Packaging & Distribution

| ID | Pri | Status | Blocked By | Task |
|----|-----|--------|------------|------|
| AD-18 | high | pending | AD-17 | Scaffold Cruft / Cookiecutter template structure |
| AD-19 | high | pending | AD-17 | Package the Generator Engine as a Python CLI library (`pyproject.toml`) |

---

## Detailed Task Specifications

### AD-1: Define intermediate canonical representation model and loader

**Rationale**: The canonical layer contains YAML workflows, markdown agents with frontmatter, MDC rules, and markdown standards. Before generating platform-specific files, a parsed, type-safe intermediate representation (IR) is needed so adapters do not duplicate file parsing and validation logic.

**Files**:
- Create `context/scripts/generators/adapters/__init__.py`
- Create `context/scripts/generators/adapters/core/models.py`
- Create `context/scripts/generators/adapters/core/loader.py`

**Acceptance**:
- Python dataclasses or Pydantic models define `CanonicalAgent`, `CanonicalRule`, `CanonicalStandard`, `WorkflowDAG`, and `Phase`.
- `load_canonical_context()` parses all files in `context/` into strongly typed IR objects.
- Raises structured errors if an agent references a non-existent rule or a workflow references an unmapped agent.

---

### AD-2: Implement abstract tool capability mapping registry

**Rationale**: Runtimes expose different tool names for the same core operations (e.g. Claude uses `Write`/`Edit`; Gemini uses `write_to_file`/`replace_file_content`; Codex uses JSON function schemas; GitHub uses IDE operations). A capability registry translates abstract capabilities into runtime-specific tool manifests.

**Files**:
- Create `context/scripts/generators/adapters/core/tools.py`

**Acceptance**:
- Defines abstract capabilities: `FILE_WRITE`, `FILE_EDIT`, `FILE_READ`, `DIRECTORY_LIST`, `CONTENT_SEARCH`, `SHELL_EXEC`.
- Maps each capability to platform-specific tool identifiers and parameter schemas for Claude, Gemini, GitHub, and Codex.
- Provides helper to inject formatted tool requirement blocks into prompt templates per target runtime.

---

### AD-3: Implement context budgeting and token delivery strategies

**Rationale**: Different runtimes have wildly divergent context windows (Gemini: 1M–2M tokens; Claude: 200k tokens; Codex: 128k tokens; Copilot: prompt-budgeted RAG). The adapter framework must support differentiated context delivery: inlining standards for large-window models vs reference linking on demand for compact models.

**Files**:
- Create `context/scripts/generators/adapters/core/budget.py`

**Acceptance**:
- Defines delivery strategies: `INLINE_COMPREHENSIVE` (Gemini), `ON_DEMAND_LINK` (Claude, Codex), `INDEXED_CHUNKS` (GitHub Copilot).
- Computes estimated token overhead per agent prompt to ensure budget compliance (<2,500 tokens for rules/frontmatter).

---

### AD-4: Implement Claude Code adapter generator

**Rationale**: Claude Code relies on `CLAUDE.md`, `AGENTS.md`, and subagent prompts dispatched via the Task tool. The adapter must generate `AGENTS.md` and `CLAUDE.md` with phase transitions, agent spawn templates, and token telemetry hook configurations.

**Files**:
- Create `context/scripts/generators/adapters/claude/__init__.py`
- Create `context/scripts/generators/adapters/claude/generator.py`

**Acceptance**:
- Generates `AGENTS.md` and `CLAUDE.md` reflecting all workflows and agent frontmatter.
- Formats spawn prompts with mandatory tool requirement blocks (`Write`/`Edit`, `uv run`, `yarn dlx`).
- Includes session telemetry git hook configuration guidance.

---

### AD-5: Implement Gemini / Antigravity adapter generator

**Rationale**: Gemini and the Google Antigravity IDE use `.agents/skills/*/SKILL.md` structures, `GEMINI.md`, and MCP server configurations. Large context windows allow direct ingestion of reference standards.

**Files**:
- Create `context/scripts/generators/adapters/gemini/__init__.py`
- Create `context/scripts/generators/adapters/gemini/generator.py`

**Acceptance**:
- Generates `.agents/skills/` skill packages containing `SKILL.md` with YAML frontmatter for specialised workflows.
- Generates `GEMINI.md` system instructions mapped to Antigravity tool calling primitives (`replace_file_content`, `run_command`, `call_mcp_tool`).
- Generates MCP tool definitions matching the template in `context/mcp/mcp.json`.

---

### AD-6: Add unit test suite for Claude and Gemini adapter generators

**Rationale**: Test-Driven Development requires verified tests for generators before deploying them to production pipelines.

**Files**:
- Create `context/scripts/tests/test_claude_adapter.py`
- Create `context/scripts/tests/test_gemini_adapter.py`

**Acceptance**:
- Tests verify output structure, markdown syntax, frontmatter parsing, and tool mappings for both Claude and Gemini.
- All tests pass via `python3 -m unittest` or `pytest`.

---

### AD-7: Generate and verify initial Claude and Gemini projections in repository

**Rationale**: Apply the new generators to produce repository-level projections and verify that no manual drift exists.

**Files**:
- Output `AGENTS.md`
- Output `CLAUDE.md`
- Output `.agents/skills/` (if enabled in repo configuration)

**Acceptance**:
- Files contain auto-generated warning headers (`Auto-generated: Do not edit manually`).
- Successfully passes `validate_agent_definitions.py` and `ears_notation.py`.

---

### AD-8: Implement GitHub Copilot adapter generator

**Rationale**: GitHub Copilot uses `.github/copilot-instructions.md`, custom reusable prompts (`.github/prompts/*.prompt.md`), and workspace indexing settings.

**Files**:
- Create `context/scripts/generators/adapters/github/__init__.py`
- Create `context/scripts/generators/adapters/github/generator.py`

**Acceptance**:
- Generates `.github/copilot-instructions.md` containing global rules, British English constraints, and EARS notation requirements.
- Generates `.github/prompts/` reusable prompt templates for specific agent roles (e.g. `@python-coder`, `@tech-lead`).

---

### AD-9: Implement Codex / OpenAI adapter generator

**Rationale**: Codex and OpenAI developer tools rely on structured system prompts, JSON Schema function declarations, and API-based workflow execution harnesses.

**Files**:
- Create `context/scripts/generators/adapters/codex/__init__.py`
- Create `context/scripts/generators/adapters/codex/generator.py`
- Create `context/scripts/runners/openai_runner.py` (lightweight harness to execute workflow YAML via OpenAI API / Swarm)

**Acceptance**:
- Generates JSON Schema definitions for file and bash tools.
- Generates system message strings formatted for OpenAI model families.
- Runner script is capable of parsing `workflows/build.yaml` and invoking sequential phase steps.

---

### AD-10: Add unit test suite for GitHub and Codex adapter generators

**Rationale**: Ensure GitHub and Codex adapter outputs conform to target platform specifications and JSON schemas.

**Files**:
- Create `context/scripts/tests/test_github_adapter.py`
- Create `context/scripts/tests/test_codex_adapter.py`

**Acceptance**:
- Tests verify `.github/copilot-instructions.md` generation, prompt file formatting, and Codex JSON Schema validity.
- All tests pass with zero errors.

---

### AD-11: Generate and verify initial GitHub and Codex projections in repository

**Rationale**: Produce actual GitHub Copilot instructions and Codex configuration bundles to validate real-world file layout.

**Files**:
- Output `.github/copilot-instructions.md`
- Output `.github/prompts/`

**Acceptance**:
- Generated files adhere to GitHub Copilot conventions.
- Auto-generation notices are clearly displayed.

---

### AD-12: Create unified `generate_adapters.py` CLI dispatcher

**Rationale**: Developers need a single CLI entry point to regenerate all or individual adapter projections from canonical `context/` files.

**Files**:
- Create `context/scripts/generators/generate_adapters.py`
- Deprecate or wrap `context/scripts/generators/generate_agents_md.py`

**Acceptance**:
- CLI accepts `--target [all|claude|gemini|github|codex]`.
- `--dry-run` flag checks outputs without writing to disk.
- Execution time across all targets is under 2.0 seconds.

---

### AD-13: Implement `adapter_drift.py` pre-commit validator

**Rationale**: If a developer updates `context/` but forgets to run the adapter generator, derived files drift. A pre-commit validator detects desynchronisation and fails the commit.

**Files**:
- Create `context/scripts/validators/adapter_drift.py`
- Create `context/scripts/tests/test_adapter_drift.py`

**Acceptance**:
- Compares on-disk generated files against in-memory generation output.
- Exits with code 0 if identical; exits with code 1 and lists drifted files if out of sync.

---

### AD-14: Wire adapter drift check into `.pre-commit-config.yaml`

**Rationale**: Automated pre-commit hooks ensure drift prevention is strictly enforced before commits enter git history.

**Files**:
- Update `context/scripts/pre-commit-config-template.yaml`
- Update `.pre-commit-config.yaml` (if present at root)

**Acceptance**:
- Pre-commit hook executes `python3 context/scripts/validators/adapter_drift.py`.
- Blocks commit if any generated adapter file has been manually edited or is out of date.

---

### AD-15: Update framework reference and portability adapter documentation

**Rationale**: Operators and contributors need comprehensive documentation explaining how to run, configure, and extend the runtime adapter system.

**Files**:
- Update `context/docs/agentic-framework-reference.md`
- Update `context/README.md`
- Update `README.md`

**Acceptance**:
- Details the Ports and Adapters architecture, CLI commands, and platform configuration guides.
- British English spelling and documentation standards strictly maintained.

---

### AD-16: Add end-to-end multi-target compilation test suite

**Rationale**: Validate the full pipeline from reading canonical markdown/YAML files through all 4 adapter compilations and drift validation.

**Files**:
- Create `context/scripts/tests/test_e2e_compilation.py`

**Acceptance**:
- Tests end-to-end compilation with synthetic and real `context/` directories.
- Verifies deterministic, byte-for-byte reproducibility on repeated runs.

---

### AD-17: Quality gate review: verify all 4 adapters compile without errors

**Rationale**: Formal quality review gate before concluding the feature build.

**Files**:
- Update `artefacts/build/tasks-runtime-adapters.md` (mark tasks complete)
- Update `artefacts/build/tasks.md`

**Acceptance**:
- @tech-lead approval recorded.
- All validators (`ears_notation.py`, `british_english.py`, `adapter_drift.py`) pass cleanly.

---

### AD-18: Scaffold Cruft / Cookiecutter template structure

**Rationale**: As decided in architecture.md, relying on `rsync` for framework distribution causes merge conflicts and versioning issues. A stateful template manager like `cruft` allows downstream projects to apply upstream updates via 3-way git merges.

**Files**:
- Create `cookiecutter.json`
- Create `{{cookiecutter.project_name}}/context/` (template structure)
- Create `{{cookiecutter.project_name}}/artefacts/`

**Acceptance**:
- Running `cruft create` successfully scaffolds a new repository containing the canonical core.
- Includes pre-commit hook configuration for downstream repositories.

---

### AD-19: Package the Generator Engine as a Python CLI library

**Rationale**: Downstream projects need a reliable way to run the adapter compilation step without copying complex Python logic. Packaging the `context/scripts/generators` folder as a standard Python package enables `uvx agent-harness` or `pip install` usage.

**Files**:
- Update / Create `pyproject.toml`
- Update `context/scripts/generators/generate_adapters.py` (ensure entrypoint compatibility)

**Acceptance**:
- `pyproject.toml` defines a `[project.scripts]` entrypoint (e.g., `agent-harness = "context.scripts.generators.generate_adapters:main"`).
- The package builds successfully (`uv build`).
