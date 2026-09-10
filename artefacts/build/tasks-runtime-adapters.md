# Tasks: Build Runtime Adapters

**Branch**: `env/runtime-adapters`  
**Status**: Completed  
**Scope**: Build the multi-platform runtime adapter system to compile canonical `context/` assets into native configurations, prompts, and tool mappings for Google Gemini / Antigravity, GitHub Copilot, Claude Code, and OpenAI Codex.  
**Design**: `artefacts/architecture/architecture.md`  
**Created**: 2026-09-09  
**Amended**: 2026-09-09  

---

## Orchestrator Notes

### Parallelism Strategy

Tasks are grouped into eight sequential sprints, prioritising the adapters in order: Gemini / Antigravity, GitHub Copilot, Claude Code, and OpenAI / Codex. Within each sprint, tasks with disjoint file scopes can be executed in parallel.

- **Sprint 1 (Foundation)**: AD-1 → AD-2 + AD-3 (parallel)  
  *file_scope*: `context/scripts/generators/adapters/core/`, `context/standards/`
- **Sprint 2 (Gemini / Antigravity)**: AD-4 → AD-5 → AD-6  
  *file_scope*: `context/scripts/generators/adapters/gemini/`, `context/scripts/tests/test_gemini_adapter.py`, `.agents/skills/`, `GEMINI.md`
- **Sprint 3 (GitHub Copilot)**: AD-7 → AD-8 → AD-9  
  *file_scope*: `context/scripts/generators/adapters/github/`, `context/scripts/tests/test_github_adapter.py`, `.github/`
- **Sprint 4 (Claude Code)**: AD-10 → AD-11 → AD-12  
  *file_scope*: `context/scripts/generators/adapters/claude/`, `context/scripts/tests/test_claude_adapter.py`, `CLAUDE.md`, `AGENTS.md`
- **Sprint 5 (OpenAI / Codex)**: AD-13 → AD-14 → AD-15  
  *file_scope*: `context/scripts/generators/adapters/codex/`, `context/scripts/runners/`, `context/scripts/tests/test_codex_adapter.py`
- **Sprint 6 (CLI & Drift Enforcement)**: AD-16 → AD-17 → AD-18  
  *file_scope*: `context/scripts/generators/generate_adapters.py`, `context/scripts/validators/`, `.pre-commit-config.yaml`
- **Sprint 7 (Docs & E2E Verification)**: AD-19 + AD-20 (parallel) → AD-21  
  *file_scope*: `context/docs/`, `context/scripts/tests/`, `README.md`
- **Sprint 8 (Packaging & Distribution)**: AD-22 + AD-23 (parallel)  
  *file_scope*: `context/scripts/dist/`, `context/docs/`, `pyproject.toml`, `context/scripts/generators/`

### Commit Strategy

One commit per task on branch `env/runtime-adapters`. Conventional commit format:

| Task | Commit message |
|------|---------------|
| AD-1 | `feat(adapters): define intermediate canonical representation and schema` |
| AD-2 | `feat(adapters): implement abstract tool capability mapping registry` |
| AD-3 | `feat(adapters): implement context budgeting and ingestion strategies` |
| AD-4 | `feat(adapters): implement gemini and antigravity adapter generator` |
| AD-5 | `test(adapters): add test suite for gemini adapter generator` |
| AD-6 | `feat(adapters): generate and verify initial gemini projections` |
| AD-7 | `feat(adapters): implement github copilot adapter generator` |
| AD-8 | `test(adapters): add test suite for github copilot adapter generator` |
| AD-9 | `feat(adapters): generate and verify initial github projections` |
| AD-10 | `feat(adapters): implement claude code adapter generator` |
| AD-11 | `test(adapters): add test suite for claude code adapter generator` |
| AD-12 | `feat(adapters): generate and verify initial claude projections` |
| AD-13 | `feat(adapters): implement codex and openai adapter generator` |
| AD-14 | `test(adapters): add test suite for codex and openai adapter generator` |
| AD-15 | `feat(adapters): generate and verify initial codex and openai projections` |
| AD-16 | `feat(adapters): create unified generate_adapters.py cli dispatcher` |
| AD-17 | `feat(validators): implement adapter_drift.py pre-commit validator` |
| AD-18 | `ci(hooks): wire adapter drift verification into git pre-commit hooks` |
| AD-19 | `docs(adapters): update framework reference and architecture documentation` |
| AD-20 | `test(adapters): add end-to-end multi-target compilation tests` |
| AD-21 | `chore(build): final quality review and tasks sign-off` |
| AD-22 | `feat(subrepo): configure git-subrepo distribution and bi-directional sync for standards` |
| AD-23 | `build(packaging): configure pyproject.toml and publish generator engine to GCP Artifact Registry` |

Push cadence: Push after each completed sprint.

### Effort Estimates

| Task | Agent(s) | Effort |
|------|----------|--------|
| AD-1 | solution-architect | Medium (30–50k tokens) |
| AD-2 | python-coder | Medium (30–50k tokens) |
| AD-3 | python-coder | Small (20–30k tokens) |
| AD-4 | python-coder | Medium (40–60k tokens) |
| AD-5 | functional-tester | Small (20–30k tokens) |
| AD-6 | python-coder | Small (15–25k tokens) |
| AD-7 | python-coder | Medium (40–60k tokens) |
| AD-8 | functional-tester | Small (20–30k tokens) |
| AD-9 | python-coder | Small (15–25k tokens) |
| AD-10 | python-coder | Medium (40–60k tokens) |
| AD-11 | functional-tester | Small (20–30k tokens) |
| AD-12 | python-coder | Small (15–25k tokens) |
| AD-13 | python-coder | Medium (40–60k tokens) |
| AD-14 | functional-tester | Small (20–30k tokens) |
| AD-15 | python-coder | Small (15–25k tokens) |
| AD-16 | python-coder | Medium (30–50k tokens) |
| AD-17 | python-coder | Small (20–30k tokens) |
| AD-18 | devops | Small (15–25k tokens) |
| AD-19 | documentation | Medium (30–50k tokens) |
| AD-20 | functional-tester | Medium (35–55k tokens) |
| AD-21 | tech-lead | Small (15–25k tokens) |
| AD-22 | devops | Medium (30–50k tokens) |
| AD-23 | devops | Small (20–30k tokens) |
| **Total** | | **~520–800k tokens** |

---

## Task Index (required)

Update status immediately when work begins and when it completes. Every task in the index has a matching specification section below.

### Sprint 1: Adapter Foundation & Tool Mapping Schema

| ID | Pri | Status | Blocked By | Task |
|----|-----|--------|------------|------|
| AD-1 | critical | completed | - | Define intermediate canonical representation model and loader |
| AD-2 | high | completed | AD-1 | Implement abstract tool capability mapping registry |
| AD-3 | high | completed | AD-1 | Implement context budgeting and token delivery strategies |

### Sprint 2: Gemini / Antigravity Adapter Layer

| ID | Pri | Status | Blocked By | Task |
|----|-----|--------|------------|------|
| AD-4 | critical | completed | AD-2, AD-3 | Implement Gemini / Antigravity adapter (skills, `GEMINI.md`, MCP bindings) |
| AD-5 | high | completed | AD-4 | Add unit test suite for Gemini adapter generator |
| AD-6 | medium | completed | AD-5 | Generate and verify initial Gemini projections in repository |

### Sprint 3: GitHub Copilot Adapter Layer

| ID | Pri | Status | Blocked By | Task |
|----|-----|--------|------------|------|
| AD-7 | high | completed | AD-2, AD-3 | Implement GitHub Copilot adapter (`.github/copilot-instructions.md`, prompt files) |
| AD-8 | high | completed | AD-7 | Add unit test suite for GitHub adapter generator |
| AD-9 | medium | completed | AD-8 | Generate and verify initial GitHub projections in repository |

### Sprint 4: Claude Code Adapter Layer

| ID | Pri | Status | Blocked By | Task |
|----|-----|--------|------------|------|
| AD-10 | critical | completed | AD-2, AD-3 | Implement Claude Code adapter (`CLAUDE.md`, `AGENTS.md`, subagent prompts, native orchestration reconciliation) |
| AD-11 | high | completed | AD-10 | Add unit test suite for Claude adapter generator |
| AD-12 | medium | completed | AD-11 | Generate and verify initial Claude projections in repository |

### Sprint 5: OpenAI / Codex Adapter Layer

| ID | Pri | Status | Blocked By | Task |
|----|-----|--------|------------|------|
| AD-13 | high | completed | AD-2, AD-3 | Implement Codex / OpenAI adapter (system prompts, tool JSON schemas, runner harness) |
| AD-14 | high | completed | AD-13 | Add unit test suite for Codex and OpenAI adapter generator |
| AD-15 | medium | completed | AD-14 | Generate and verify initial Codex and OpenAI projections in repository |

### Sprint 6: Unified Adapter CLI & Drift Enforcement

| ID | Pri | Status | Blocked By | Task |
|----|-----|--------|------------|------|
| AD-16 | high | completed | AD-6, AD-9, AD-12, AD-15 | Create unified `generate_adapters.py` CLI dispatcher |
| AD-17 | high | completed | AD-16 | Implement `adapter_drift.py` pre-commit validator |
| AD-18 | medium | completed | AD-17 | Wire adapter drift check into `.pre-commit-config.yaml` |

### Sprint 7: Documentation & End-to-End Verification

| ID | Pri | Status | Blocked By | Task |
|----|-----|--------|------------|------|
| AD-19 | medium | completed | AD-16 | Update framework reference and portability adapter documentation |
| AD-20 | high | completed | AD-16, AD-17 | Add end-to-end multi-target compilation test suite |
| AD-21 | critical | completed | AD-19, AD-20 | Quality gate review: verify all 4 adapters compile without errors |

### Sprint 8: Packaging & Distribution

| ID | Pri | Status | Blocked By | Task |
|----|-----|--------|------------|------|
| AD-22 | high | completed | AD-21 | Configure git-subrepo distribution and bi-directional sync for context/ |
| AD-23 | high | completed | AD-21 | Package and publish Generator Engine to GCP Artifact Registry |

---

## Detailed Task Specifications

### AD-1: Define intermediate canonical representation model and loader

**Rationale**: The canonical layer contains YAML workflows, markdown agents with frontmatter, MDC rules, markdown standards, and writing personas. Before generating platform-specific files, a parsed, type-safe intermediate representation (IR) is needed so adapters do not duplicate file parsing and validation logic.

**Files**:
- Create `context/scripts/generators/adapters/__init__.py`
- Create `context/scripts/generators/adapters/core/models.py`
- Create `context/scripts/generators/adapters/core/loader.py`

**Acceptance**:
- Python dataclasses or Pydantic models define `CanonicalAgent`, `CanonicalRule`, `CanonicalStandard`, `WorkflowDAG`, `Phase`, and `CanonicalPersona`.
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

### AD-4: Implement Gemini / Antigravity adapter generator

**Rationale**: Gemini and the Google Antigravity IDE use `.agents/skills/*/SKILL.md` structures, `GEMINI.md`, and MCP server configurations. Large context windows allow direct ingestion of reference standards.

**Files**:
- Create `context/scripts/generators/adapters/gemini/__init__.py`
- Create `context/scripts/generators/adapters/gemini/generator.py`

**Acceptance**:
- Generates `.agents/skills/` skill packages containing `SKILL.md` with YAML frontmatter for specialised workflows.
- Generates `GEMINI.md` system instructions mapped to Antigravity tool calling primitives (`replace_file_content`, `run_command`, `call_mcp_tool`).
- Generates MCP tool definitions matching the template in `context/mcp/mcp.json`.

---

### AD-5: Add unit test suite for Gemini adapter generator

**Rationale**: Test-Driven Development requires verified tests for generators before deploying them to production pipelines.

**Files**:
- Create `context/scripts/tests/test_gemini_adapter.py`

**Acceptance**:
- Tests verify output structure, markdown syntax, frontmatter parsing, and tool mappings for Gemini.
- All tests pass via `python3 -m unittest` or `pytest`.

---

### AD-6: Generate and verify initial Gemini projections in repository

**Rationale**: Apply the new Gemini generator to produce repository-level projections and verify that no manual drift exists.

**Files**:
- Output `GEMINI.md`
- Output `.agents/skills/` (if enabled in repo configuration)

**Acceptance**:
- Files contain auto-generated warning headers (`Auto-generated: Do not edit manually`).
- Successfully passes `validate_agent_definitions.py` and `ears_notation.py`.

---

### AD-7: Implement GitHub Copilot adapter generator

**Rationale**: GitHub Copilot uses `.github/copilot-instructions.md`, custom reusable prompts (`.github/prompts/*.prompt.md`), and workspace indexing settings.

**Files**:
- Create `context/scripts/generators/adapters/github/__init__.py`
- Create `context/scripts/generators/adapters/github/generator.py`

**Acceptance**:
- Generates `.github/copilot-instructions.md` containing global rules, British English constraints, and EARS notation requirements.
- Generates `.github/prompts/` reusable prompt templates for specific agent roles (e.g. `@python-coder`, `@tech-lead`).

---

### AD-8: Add unit test suite for GitHub adapter generator

**Rationale**: Ensure GitHub adapter outputs conform to target platform specifications.

**Files**:
- Create `context/scripts/tests/test_github_adapter.py`

**Acceptance**:
- Tests verify `.github/copilot-instructions.md` generation, prompt file formatting, and markdown syntax.
- All tests pass with zero errors.

---

### AD-9: Generate and verify initial GitHub projections in repository

**Rationale**: Produce actual GitHub Copilot instructions to validate real-world file layout.

**Files**:
- Output `.github/copilot-instructions.md`
- Output `.github/prompts/`

**Acceptance**:
- Generated files adhere to GitHub Copilot conventions.
- Auto-generation notices are clearly displayed.

---

### AD-10: Implement Claude Code adapter generator

**Rationale**: Claude Code relies on `CLAUDE.md`, `AGENTS.md`, and subagent prompts dispatched via the Task tool. The adapter must generate `AGENTS.md` and `CLAUDE.md` with phase transitions, agent spawn templates, and token telemetry hook configurations. To satisfy REQ-ADP-006 (Claude Native Orchestration Reconciliation), this adapter must balance the framework's governance (rule injection, file scopes, quality gates, handoffs) with Claude's native multi-agent primitives (subagent spawning, Task tool).

**Files**:
- Create `context/scripts/generators/adapters/claude/__init__.py`
- Create `context/scripts/generators/adapters/claude/generator.py`
- Create `context/scripts/generators/adapters/claude/reconciler.py` (to handle native orchestration mapping)

**Acceptance**:
- Generates `AGENTS.md` and `CLAUDE.md` reflecting all workflows and agent frontmatter.
- Formats spawn prompts with mandatory tool requirement blocks (`Write`/`Edit`, `uv run`, `yarn dlx`).
- Includes session telemetry git hook configuration guidance.
- Reconciles Claude's native orchestration primitives (Task tool, subagents) with framework governance (quality gates, phase execution, handoffs).

---

### AD-11: Add unit test suite for Claude adapter generator

**Rationale**: Ensure Claude Code adapter outputs conform to target platform specifications and subagent dispatch schemas.

**Files**:
- Create `context/scripts/tests/test_claude_adapter.py`

**Acceptance**:
- Tests verify output structure, markdown syntax, frontmatter parsing, and tool mappings for Claude.
- All tests pass via `python3 -m unittest` or `pytest`.

---

### AD-12: Generate and verify initial Claude projections in repository

**Rationale**: Apply the new Claude generator to produce repository-level projections and verify that no manual drift exists.

**Files**:
- Output `AGENTS.md`
- Output `CLAUDE.md`

**Acceptance**:
- Files contain auto-generated warning headers (`Auto-generated: Do not edit manually`).
- Successfully passes `validate_agent_definitions.py` and `ears_notation.py`.

---

### AD-13: Implement Codex / OpenAI adapter generator

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

### AD-14: Add unit test suite for Codex and OpenAI adapter generator

**Rationale**: Ensure Codex and OpenAI adapter outputs conform to JSON schemas and system prompt structures.

**Files**:
- Create `context/scripts/tests/test_codex_adapter.py`

**Acceptance**:
- Tests verify prompt formatting and Codex JSON Schema validity.
- All tests pass with zero errors.

---

### AD-15: Generate and verify initial Codex and OpenAI projections in repository

**Rationale**: Produce actual Codex configuration bundles to validate real-world file layout.

**Files**:
- Output `.openai/` or runtime prompt configurations
- Output tool schema files

**Acceptance**:
- Generated files adhere to OpenAI tool calling conventions.
- Auto-generation notices are clearly displayed.

---

### AD-16: Create unified `generate_adapters.py` CLI dispatcher

**Rationale**: Developers need a single CLI entry point to regenerate all or individual adapter projections from canonical `context/` files.

**Files**:
- Create `context/scripts/generators/generate_adapters.py`
- Deprecate or wrap `context/scripts/generators/generate_agents_md.py`

**Acceptance**:
- CLI accepts `--target [all|gemini|github|claude|codex]`.
- `--dry-run` flag checks outputs without writing to disk.
- Execution time across all targets is under 2.0 seconds.

---

### AD-17: Implement `adapter_drift.py` pre-commit validator

**Rationale**: If a developer updates `context/` but forgets to run the adapter generator, derived files drift. A pre-commit validator detects desynchronisation and fails the commit.

**Files**:
- Create `context/scripts/validators/adapter_drift.py`
- Create `context/scripts/tests/test_adapter_drift.py`

**Acceptance**:
- Compares on-disk generated files against in-memory generation output.
- Exits with code 0 if identical; exits with code 1 and lists drifted files if out of sync.

---

### AD-18: Wire adapter drift check into `.pre-commit-config.yaml`

**Rationale**: Automated pre-commit hooks ensure drift prevention is strictly enforced before commits enter git history.

**Files**:
- Update `context/scripts/pre-commit-config-template.yaml`
- Update `.pre-commit-config.yaml` (if present at root)

**Acceptance**:
- Pre-commit hook executes `python3 context/scripts/validators/adapter_drift.py`.
- Blocks commit if any generated adapter file has been manually edited or is out of date.

---

### AD-19: Update framework reference and portability adapter documentation

**Rationale**: Operators and contributors need comprehensive documentation explaining how to run, configure, and extend the runtime adapter system, as well as how the adapters ensure the three foundational NFR axes (autonomy, token efficiency, intent preservation).

**Files**:
- Update `context/docs/agentic-framework-reference.md`
- Update `context/README.md`
- Update `README.md`

**Acceptance**:
- Details the Ports and Adapters architecture, CLI commands, and platform configuration guides.
- Explains how the adapters uphold autonomy, token efficiency, and intent preservation requirements.
- British English spelling and documentation standards strictly maintained.

---

### AD-20: Add end-to-end multi-target compilation test suite

**Rationale**: Validate the full pipeline from reading canonical markdown/YAML files through all 4 adapter compilations and drift validation.

**Files**:
- Create `context/scripts/tests/test_e2e_compilation.py`

**Acceptance**:
- Tests end-to-end compilation with synthetic and real `context/` directories.
- Verifies deterministic, byte-for-byte reproducibility on repeated runs.

---

### AD-21: Quality gate review: verify all 4 adapters compile without errors

**Rationale**: Formal quality review gate before concluding the feature build.

**Files**:
- Update `artefacts/build/tasks-runtime-adapters.md` (mark tasks complete)

**Acceptance**:
- @tech-lead approval recorded.
- All validators (`ears_notation.py`, `british_english.py`, `adapter_drift.py`) pass cleanly.

**Quality Gate Review Record (2026-09-10)**:
- **Reviewer**: `@tech-lead`
- **Scope**: Multi-Target Runtime Adapters (Gemini, Claude Code, GitHub Copilot, OpenAI/Codex).
- **Compilation Status**: All 4 runtime projections compile deterministically and cleanly without error.
- **Verification Matrix**:
  - `generate_adapters.py`: All 86 projections generated in < 0.2s with zero byte churn on repeat runs.
  - `adapter_drift.py`: Passes with exit code 0; zero drift detected across all projections.
  - `test_e2e_compilation.py`: Verified multi-target compilation, byte-for-byte reproducibility, and synthetic context loading.
  - Test suite: 77/77 tests passing.
  - Documentation: `README.md`, `context/README.md`, and test READMEs updated and validated against British English standards.
- **Verdict**: APPROVED. Proceed to Sprint 8 (Packaging & Distribution).

---

### AD-22: Configure git-subrepo distribution and bi-directional sync for context/

**Rationale**: Downstream projects need to import the canonical standards (`context/`) without inheriting project-specific state (`artefacts/build/`, `artefacts/product/`, or application code), and must be able to push standards improvements made in downstream projects back to `start-here`. Using `git-subrepo` against an isolated upstream `standards` distribution branch provides seamless, git-native bi-directional synchronisation with normal commit history and no submodule HEAD detachment issues.

**Files**:
- Native `git-subrepo` command integration (`git subrepo branch context -f`)
- Create `context/docs/downstream-subrepo.md` (downstream guide for cloning, pulling, pushing, and testing standards via git-subrepo)
- Update `README.md` and `context/README.md` (distribution architecture and Mermaid diagrams)
- Update `artefacts/architecture/architecture.md` (ADR and distribution topology)

**Acceptance**:
- Native `git subrepo branch context -f` isolates and produces the clean `subrepo/context` branch without external scripts.
- Downstream workflow is verified:
  1. `git subrepo clone <url> context -b standards` imports only `context/`.
  2. Project-specific directories (`artefacts/build/`, local services) remain strictly outside the subrepo boundary.
  3. Upstream updates can be pulled cleanly via `git subrepo pull context`.
  4. Changes made downstream to standards can be pushed upstream via `git subrepo push context`.
  5. Downstream projects can execute the test suite at any time via `uv run pytest context/scripts/tests`.
- Detailed documentation in `context/docs/downstream-subrepo.md` guides downstream setup and pre-commit enforcement.

---

### AD-23: Package and publish Generator Engine to GCP Artifact Registry

**Rationale**: Downstream projects pulling standards via `git-subrepo` need to compile platform projections (`AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, etc.) and enforce zero drift without managing complex Python logic or dependencies. Packaging the generator engine and drift validator as a standard Python package published to a private GCP Artifact Registry repository enables seamless IAM authentication and instant execution via `uvx` or `pip`.

**Files**:
- Create `pyproject.toml` (standard PEP 517/621 hatchling build configuration)
- Create `context/__init__.py`, `context/scripts/__init__.py`, `context/scripts/generators/__init__.py` (package inits)
- Update `context/scripts/generators/generate_adapters.py` (CLI entrypoint & repo_root detection)
- Update `context/scripts/validators/adapter_drift.py` (CLI entrypoint & repo_root detection)
- Create `context/scripts/tests/test_packaging.py` (entrypoint and metadata test suite)

**Acceptance**:
- `pyproject.toml` defines `[project.scripts]` entrypoints (`agent-harness = "context.scripts.generators.generate_adapters:main"` and `agent-drift = "context.scripts.validators.adapter_drift:main"`).
- The package builds successfully with `uv build` (`dist/*.whl` and `dist/*.tar.gz`).
- The package can be published to a private GCP Artifact Registry repository using modern `uv publish` (via OAuth2 access token or keyring provider) or `twine`.
- Post-sync workflow documented so downstream projects can run `uvx ... agent-harness` to regenerate projections after `git subrepo pull context`.

**Quality Gate Review Record (Sprint 8 - 2026-09-10)**:
- **Reviewer**: `@tech-lead`
- **Scope**: Packaging, Distribution & Bi-directional Standards Synchronisation (Sprint 8).
- **Verification Matrix**:
  - `git-subrepo` native commands verified: `git subrepo branch context -f` cleanly separates the canonical `context/` tree for distribution.
  - `pyproject.toml` validated: Builds cleanly via `uv build` into `dist/agent_harness-0.1.0-py3-none-any.whl` and `dist/agent_harness-0.1.0.tar.gz`.
  - Python CLI entrypoints tested: `agent-harness` and `agent-drift` verified via `test_packaging.py`.
  - Full test suite: 80/80 tests passing via `uv run pytest context/scripts/tests -v`.
  - Documentation: `context/docs/downstream-subrepo.md`, `README.md`, `context/README.md`, and `artefacts/architecture/architecture.md` updated with the bi-directional synchronisation topology diagram.
  - Standards compliance: `british_english.py` and `adapter_drift.py` pass cleanly with exit code 0.
- **Verdict**: APPROVED. All 8 sprints of Runtime Adapters completed.
