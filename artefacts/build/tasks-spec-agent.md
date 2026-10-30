# Tasks: Derive Product and Technical Specifications from Repo

**Branch**: feat/spec-agent
**Status**: In Progress
**Scope**: New harness capability: derive product and/or technical specifications from an existing codebase (organised or not) via a single mode-switched workflow, backed by a deterministic zero-LLM indexer (`spec_indexer.py`) and agent synthesis with confidence tiers.
**Design**: `context/workflows/README.md` § derive-spec (overview, mode branch, runtime/tool wiring, token ledger); `context/scripts/spec_indexer.py` (schema documented in README § 4.2)
**Created**: 2026-10-29
**Amended**: 2026-10-30 — Q0 answered (Q1–Q10 recommended decisions below); task index expanded T-003…T-013; T-011 (workflows README) and T-012 (indexer) completed

## Task Index

| ID | Priority | Status | Blocked By | Task |
|----|----------|--------|------------|------|
| Q0 | critical | completed | - | Answer clarifying questions (recommended decisions below) |
| T-012 | high | completed | - | Write `context/scripts/spec_indexer.py` (`scan` / `verify` subcommands) |
| T-011 | high | completed | - | Author `context/workflows/README.md` (diagrams + runtime narrative + token ledger); note in `context/README.md` |
| T-001 | critical | pending | Q0 | Create skill `context/skills/derive-spec.md` (modes: product, technical, both) |
| T-002 | high | pending | Q0 | Create workflow `context/workflows/derive-spec.yaml` (modes, phases, gates, state recovery) |
| T-003 | high | pending | T-001 | Extend `context/agents/product-owner.md` — Mode 3 derive (loads derive-spec skill) |
| T-004 | high | pending | T-001 | Extend `context/agents/solution-architect.md` — derive mode (drafts only) |
| T-005 | high | pending | T-001 | Add confirmation mode to `context/skills/requirements-elicitation.md` |
| T-006 | medium | pending | T-001 | Add `context/templates/derived-spec-template.md` (confidence schema + open-question appendix) |
| T-007 | high | pending | T-001,T-002,T-006 | Regenerate adapters; run validators green |
| T-010 | high | pending | T-007 | Unit tests: skill/workflow schema, indexer extraction + verify |
| T-008 | critical | pending | T-010 | Pilot: run derive-spec (`mode=both`) on this repo; measure token ledger before/after |
| T-009 | low | pending | T-008 | Optional: register derive-spec as a `build.yaml` precursor phase |
| T-013 | high | pending | T-002,T-012 | Wire indexer into `derive-spec.yaml` Phases 1 & 3 (agent `tool_scope` = index + cited ranges) |

## File Scope

- `artefacts/build/tasks-spec-agent.md` — task definition and workflow specification
- `context/skills/derive-spec.md` — new skill with mode switches: product, technical, both
- `context/workflows/derive-spec.yaml` — new workflow YAML supporting all three modes
- `context/workflows/README.md` — workflow index, derive-spec diagrams, runtime/tool wiring, token ledger *(completed)*
- `context/README.md` — brief pointer to the workflows index *(completed)*
- `context/scripts/spec_indexer.py` — deterministic indexer (`scan` / `verify`) *(completed)*
- `context/agents/product-owner.md` — adds derive mode for product-spec synthesis
- `context/agents/solution-architect.md` — adds derive mode for technical-spec synthesis
- `context/skills/requirements-elicitation.md` — adds confirmation mode
- `context/templates/derived-spec-template.md` — derived spec output format
- `context/workflows/build.yaml` — optional precursor-phase dependency
- Derived outputs (drafts, then promoted on approval): `artefacts/product/`, `artefacts/architecture/`

## Recommended Decisions (Q0)

Q0 recorded on 2026-10-30 during planning; chosen options bind T-001 and T-002.

| Q | Question | Decision | Rationale |
|---|----------|----------|-----------|
| Q1 | Output location for generated specs | **C** — per-run choice via workflow input; default drafts `artefacts/product/product-spec.derived.md`, `artefacts/architecture/*.derived.md`; promoted only on approval | Never clobbers canonical docs; matches artefacts layout |
| Q2 | Question format for confirmation | **A** — numbered multiple-choice with “Other”, each citing files (reverse-spec Step 3) | One batched round; highest completion rate |
| Q3 | Repo organisation scope | **C** — configurable `spec-docs-glob` (defaults: `artefacts/product/**`, `artefacts/architecture/**`, `docs/**`, `**/README.md`, `PRD*`, `*spec*.md`, `openapi*.yaml`) | Structured + unstructured repos; candidates confirmed by human, never silent |
| Q4 | Confidence model | **B** — tier (Verified / Needs Confirmation / Assumed) + % per subsection + `file:line` evidence | Auditable; citations originate from the indexer |
| Q5 | Agent for technical synthesis | **A** — reuse `@solution-architect` via a derive mode | Modes are the harness pattern; no roster bloat |
| Q6 | Elicitation skill for technical confirmation | **B** — add a confirmation mode to `requirements-elicitation.md` | One elicitation skill; product-owner already loads it; discipline identical |
| Q7 | Integration with build workflow | **B** — standalone first; optional precursor phase in `build.yaml` later (T-009) | Bootstrap capability, then wire in |
| Q8 | Maximum repo size / scan limit | **B** — line/file-count threshold; large repos flagged for human scoping (`scan_too_large` meta flag) | A size-bound agent reads an index, so bounds are cheap |
| Q9 | Mode selection mechanism | **A** — workflow input (`--mode product \| technical \| both`); recorded in `index.meta.mode` | Deterministic, reproducible, testable |
| Q10 | Combined output format | **B** — separate docs per artefacts category (product-spec, architecture, data model, api catalogue) | Matches the canonical artefacts layout 1:1 |

---

## Task

### T-001: Create skill `context/skills/derive-spec.md`

#### Acceptance Criteria

- Frontmatter matches skill schema: `name`, `description`, `globs` (target: `**/*.py`, `**/*.ts`, `**/*.tsx`, `**/*.sql`, `**/openapi*.yaml`, `repo-index.json`)
- Covers procedural steps for both modes: discovery (glob candidates + human confirmation), evidence consumption from `repo-index.json`, product derivation (UI inventory → candidate features → UX flows), technical derivation (architecture / API draft / data-model draft), confidence model (tier + % + citation), open-question batching, verification via `spec_indexer.py verify`
- States output lifecycle: derived drafts only, promotion behind approval; drift section vs canonical docs
- References the workflows README § 4 (runtime/tools) without duplicating the schema table

#### Primary Output Path

`context/skills/derive-spec.md`

### T-002: Create workflow `context/workflows/derive-spec.yaml`

#### Acceptance Criteria

- Phases 0–8 per workflows README; mode conditional on 4a/4b; shared phases single-run
- Each phase declares `agents`, `outputs`, `validation:`; gate phases (`verification` pass, `final review`) marked `gate: true` with APPROVED semantics
- `state_recovery:` reads `artefacts/build/spec-scan.md` and `repo-index.json`; critical files listed
- Phase 6 invokes `spec_indexer.py verify --index`; Phase 8 invokes `verify --doc` on drafts

#### Primary Output Path

`context/workflows/derive-spec.yaml`

### T-003: Extend `context/agents/product-owner.md` with derive mode

#### Acceptance Criteria

- New Mode (derive) declared alongside existing modes: loads `derive-spec.md`, runs product derivation, writes drafts, bats MC questions (Q2 format), updates per answers
- Intake, escalation, reporting, state-recovery protocols unchanged; derives never promote

#### Primary Output Path

`context/agents/product-owner.md`

### T-004: Extend `context/agents/solution-architect.md` with derive mode

#### Acceptance Criteria

- Derive mode: architecture / API / data-model drafting from index evidence, drafts only (`*.derived.md`), canonical ownership boundary preserved (`openapi.yaml` untouched)
- Runs Review Mode trace checks against index call chains

#### Primary Output Path

`context/agents/solution-architect.md`

### T-005: Add confirmation mode to `context/skills/requirements-elicitation.md`

#### Acceptance Criteria

- Confirmation mode documented distinctly from problem-discovery: batched MC + Other, evidence-cited, one/two questions at a time, stop-and-wait
- Exit criteria: every Assumed claim has a question; confirmed answers update drafts

#### Primary Output Path

`context/skills/requirements-elicitation.md`

### T-006: Add `context/templates/derived-spec-template.md`

#### Acceptance Criteria

- Subsection skeletons for product-spec / architecture / data model / api catalogue with confidence fields (tier + % + evidence `path:line`)
- Open-question appendix format (per subsection, priority, MC options), drift section header

#### Primary Output Path

`context/templates/derived-spec-template.md`

### T-007: Regenerate adapters and validators

#### Acceptance Criteria

- `uv run python context/scripts/generators/generate_adapters.py` reflects the new skill/workflow in AGENTS.md/CLINE.md/GEMINI.md registries (if projection applies)
- `uv run pytest context/scripts/tests/` green; `adapter_drift.py` and `tech_writing.py` green on changed files

#### Primary Output Path

Generated registry files; commit message in `/tmp/T-007_commit_msg.txt`

### T-010: Unit tests

#### Acceptance Criteria

- Skill frontmatter schema test; workflow YAML phase-schema test (unique ids, resolvable `depends_on`, known agents, gates defined)
- Indexer tests: Python extraction (symbols, routes, constants), TS/TSX extraction (components, props, usage counts — fixture per smoke test), SQL table parsing, `verify` pass/fail on synthetic repo
- `uv run pytest context/scripts/tests/test_spec_indexer.py` green

#### Primary Output Path

`context/scripts/tests/test_spec_indexer.py`

### T-008: Pilot run (mode=both, this repo)

#### Acceptance Criteria

- `scan` + draft + confirmation + review run end-to-end on start-here
- Every generated subsection carries tier + % + citation; `verify --doc` on all drafts passes
- Drift section present where derived behaviour differs from `requirements.md` / `architecture.md`
- Token ledger filled with measured before/after (README § 5)

#### Primary Output Path

`artefacts/build/spec-pilot-report.md`

### T-009: Optional build.yaml precursor integration

#### Acceptance Criteria

- derive-spec gate completes before build `task-planning` when specs missing; disabled otherwise

#### Primary Output Path

`context/workflows/build.yaml`

### T-013: Wire indexer into derive-spec workflow

#### Acceptance Criteria

- Phases 1/3 consume `repo-index.json` + `spec-scan.md`; agent `tool_scope` restricted to index + cited line ranges
- Re-scan rule documented (index refresh before `verify`)

#### Primary Output Path

`context/workflows/derive-spec.yaml` (with T-002)

---

## Orchestrator Notes

### Parallelism Strategy

**Sprint 1** (critical path after Q0): T-011 → T-012 (both completed) → T-001 → T-002 → T-003 + T-004 + T-005 (parallel, file-scope disjoint) → T-006 → T-007 → T-010 → T-008 → T-009, T-013.
file_scope: `context/skills/` (T-001, T-005), `context/agents/` (T-003, T-004), `context/templates/` (T-006)

### Commit Strategy

One commit per task on `feat/spec-agent`, conventional messages (`feat(spec): …`, `docs(workflows): …`, `test(spec): …`). Push after every commit.

### Backlog Cleanup

- `todo.md`: no overlapping items identified; the workflows README (T-011) reduces the “AGENTS.md distribution” backlog item tension by centralising workflow documentation.



