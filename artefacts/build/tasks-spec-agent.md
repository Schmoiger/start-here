# Tasks: Derive Product and Technical Specifications from Repo

**Branch**: feat/spec-agent
**Status**: In Progress
**Scope**: New harness capability: derive product and/or technical specifications from an existing codebase (organised or not) via a single mode-switched workflow, backed by a deterministic zero-LLM indexer (`spec_indexer.py`) and agent synthesis with confidence tiers.
**Design**: `context/workflows/README.md` § derive-spec (overview, mode branch, runtime/tool wiring, token ledger); `context/scripts/code-specs/spec_indexer.py` (schema documented in README Commands / Repository Index)
**Created**: 2026-10-29
**Amended**: 2026-10-30 — Q0 answered (Q1–Q10 recommended decisions below); task index expanded T-003…T-015; T-011 (workflows README) and T-012 (indexer) completed; T-SETUP (dependencies) and T-014 (analyse-repo skill) added; T-015 (tool-backed extraction backends) added
**Amended**: 2026-01-11 (follow-up) — detail headings aligned to the task index; duplicate short T-015 section removed; T-021 (comment/docstring extraction) added after the AST-discard gap was identified
**Amended**: 2026-01-11 (T-SETUP done) — T-SETUP marked completed (ctags 6.2.1, ast-grep 0.51.0, tree-sitter via uv, ts-morph skipped); T-015 ast-grep backend reworded to the `ast-grep` binary (`sg` deprecated as of 0.51)
**Amended**: 2026-01-11 (T-015 done) — T-015 completed: `--extractors` backends (auto/stdlib/ctags/tree-sitter/ast-grep/ts-morph), `meta.extractors` + `meta.confidence` + per-file `extractor`, `ts_extract.mjs` helper, parity + fixture tests (15/15 with tree-sitter); README Commands notes the flag

## Task Index

| ID | Priority | Status | Blocked By | Task |
|----|----------|--------|------------|------|
| Q0 | critical | completed | - | Answer clarifying questions (recommended decisions below) |
| T-SETUP | critical | completed | - | Install / verify toolchain dependencies (human-run) before implementation starts — verified 2026-01-11: ctags 6.2.1, ast-grep 0.51.0, tree-sitter OK via `uv run --with`, ts-morph skipped (absent) |
| T-012 | high | completed | - | Write `context/scripts/code-specs/spec_indexer.py` (`scan` / `verify` subcommands) |
| T-011 | high | completed | - | Author `context/workflows/README.md` (diagrams + runtime narrative + token ledger); note in `context/README.md` |
| T-015 | high | completed | T-SETUP | Tool-backed extraction backends with graceful fallback (`--extractors`: ctags, tree-sitter, ast-grep, ts-morph) |
| T-014 | high | pending | T-SETUP,T-015 | Wrap indexer tool usage in skill `context/skills/analyse-repo.md` (documents the actual backends) |
| T-001 | critical | pending | Q0,T-014 | Create skill `context/skills/derive-spec.md` (modes: product, technical, both) |
| T-002 | high | pending | Q0 | Create workflow `context/workflows/derive-spec.yaml` (modes, phases, gates, state recovery) |
| T-003 | high | pending | T-001 | Extend `context/agents/product-owner.md` — Mode 3 derive (loads derive-spec skill) |
| T-004 | high | pending | T-001 | Extend `context/agents/solution-architect.md` — derive mode (drafts only) |
| T-005 | high | pending | T-001 | Add confirmation mode to `context/skills/requirements-elicitation.md` |
| T-006 | medium | pending | T-001 | Add `context/templates/derived-spec-template.md` (confidence schema + open-question appendix) |
| T-007 | high | pending | T-001,T-002,T-006 | Regenerate adapters; run validators green |
| T-010 | high | pending | T-007 | Unit tests: skill/workflow schema, indexer extraction + verify |
| T-008 | critical | pending | T-010 | Pilot A: run derive-spec (`mode=both`) on this repo; measure token ledger before/after; outputs land in `derived/` |
| T-009 | low | pending | T-008 | Optional: register derive-spec as a `build.yaml` precursor phase |
| T-013 | high | pending | T-002,T-012 | Wire indexer into `derive-spec.yaml` Phases 1 & 3 (agent `tool_scope` = index + cited ranges) |
| T-016 | high | pending | T-015 | Indexer: env/config/feature-flag extraction into `config` key — user-facing constraints for product spec + TSD constraints |
| T-017 | medium | pending | T-015 | Indexer: capped git-history evidence into `meta.history` (commit subjects + renames; zero LLM) |
| T-018 | high | pending | T-006 | Confidence bands + promotion DoD in `derived-spec-template.md` (Verified 85–100 · Needs Confirmation 50–85 · Assumed <50; unanswered stays Assumed) |
| T-019 | critical | pending | T-008 | Pilot B: derive-spec on the human-chosen foreign/unorganised repo; validate Phases 1–2 + `derived/` landing |
| T-020 | low | pending | T-010 | Extend `verify` with `--require-coverage` (deterministic Phase 6 gate: tier + % + citation per subsection) |
| T-021 | high | pending | T-015 | Indexer: comment/docstring extraction into `comments` key (stdlib `tokenize`, docstrings, TS JSDoc, SQL `--`); intent evidence attached to symbols; consumed via analyse-repo skill |

## File Scope

- `artefacts/build/tasks-spec-agent.md` — task definition and workflow specification
- `context/skills/analyse-repo.md` — analysis-tool skill wrapping `spec_indexer.py` usage (T-014)
- `context/scripts/code-specs/spec_indexer.py` — indexer with multi-backend extraction (T-015)
- `context/scripts/code-specs/ts_extract.mjs` — optional ts-morph Node helper (T-015)
- `context/skills/derive-spec.md` — new skill with mode switches: product, technical, both
- `context/workflows/derive-spec.yaml` — new workflow YAML supporting all three modes
- `context/workflows/README.md` — workflow index, derive-spec diagrams, runtime/tool wiring, token ledger *(completed)*
- `context/README.md` — brief pointer to the workflows index *(completed)*
- `context/scripts/code-specs/spec_indexer.py` — deterministic indexer (`scan` / `verify`) *(completed)*
- `context/agents/product-owner.md` — adds derive mode for product-spec synthesis
- `context/agents/solution-architect.md` — adds derive mode for technical-spec synthesis
- `context/skills/requirements-elicitation.md` — adds confirmation mode
- `context/templates/derived-spec-template.md` — derived spec output format
- `context/workflows/build.yaml` — optional precursor-phase dependency
- Derived outputs (staged drafts, then promoted on approval): `artefacts/build/spec-drafts/` → `artefacts/{product,architecture}/derived/`; plus `artefacts/build/repo-profile.md`

## Recommended Decisions (Q0)

Q0 recorded on 2026-10-30 during planning (Q1–Q10). A1–A4 recorded 2026-01-11 — Q1 (A1: land in `derived/`), Q4 (A2: fixed confidence bands), Q11 (A3: monorepo per-repo), and T-019 (A4: pilot B repo, human-chosen). Chosen options bind T-001 and T-002.

| Q | Question | Decision | Rationale |
|---|----------|----------|-----------|
| Q1 | Output location for generated specs | **C** — per-run choice via workflow input; drafts staged in `artefacts/build/spec-drafts/`, approval promotes to `artefacts/{category}/derived/` (e.g. `artefacts/product/derived/product-spec.md`) | Decision **A1**: land in `derived/`; derive-spec never rewrites canonical docs |
| Q2 | Question format for confirmation | **A** — numbered multiple-choice with “Other”, each citing files (reverse-spec Step 3) | One batched round; highest completion rate |
| Q3 | Repo organisation scope | **C** — configurable `spec-docs-glob` (defaults: `artefacts/product/**`, `artefacts/architecture/**`, `docs/**`, `**/README.md`, `PRD*`, `*spec*.md`, `openapi*.yaml`) | Structured + unstructured repos; candidates confirmed by human, never silent |
| Q4 | Confidence model | **B** — tier (Verified / Needs Confirmation / Assumed) + banded % per subsection + `file:line` evidence: **Verified 85–100 · Needs Confirmation 50–85 · Assumed <50** | Decision **A2**: fixed bands; confirmed answers raise band/%; unanswered questions stay Assumed (still-open appendix) |
| Q5 | Agent for technical synthesis | **A** — reuse `@solution-architect` via a derive mode | Modes are the harness pattern; no roster bloat |
| Q6 | Elicitation skill for technical confirmation | **B** — add a confirmation mode to `requirements-elicitation.md` | One elicitation skill; product-owner already loads it; discipline identical |
| Q7 | Integration with build workflow | **B** — standalone first; optional precursor phase in `build.yaml` later (T-009) | Bootstrap capability, then wire in |
| Q8 | Maximum repo size / scan limit | **B** — line/file-count threshold; large repos flagged for human scoping (`scan_too_large` meta flag) | A size-bound agent reads an index, so bounds are cheap |
| Q9 | Mode selection mechanism | **A** — workflow input (`--mode product \| technical \| both`); recorded in `index.meta.mode` | Deterministic, reproducible, testable |
| Q10 | Combined output format | **B** — separate docs per artefacts category (product-spec, architecture, data model, api catalogue) | Matches the canonical artefacts layout 1:1 |
| Q11 | Monorepo / multi-repo handling | **A** — run once per repo or service; `--repo <service-root>` scopes the scan; one HANDOFF per run | Decision **A3**: products spanning multiple repos get one derived spec set per repo; cross-repo questions go to the elicitation round |

---

## Task

### T-001: Create skill `context/skills/derive-spec.md` (modes: product, technical, both)

#### Acceptance Criteria

- Frontmatter matches skill schema: `name`, `description`, `globs` (target: `**/*.py`, `**/*.ts`, `**/*.tsx`, `**/*.sql`, `**/openapi*.yaml`, `repo-index.json`)
- Covers procedural steps for both modes: discovery (glob candidates + human confirmation), evidence consumption from `repo-index.json` + `repo-profile.md`, product derivation (UI inventory → candidate features → roles/actors → UX flows), technical derivation (architecture / API draft / data-model draft), confidence model (tier + banded % + citation), open-question batching, verification via `spec_indexer.py verify`
- Includes repo-profiling guidance (Phase 1: app type, entry points, module boundaries from the index) for unorganised repositories
- Question ordering: drift candidates (existing-doc vs code deltas) before pure code facts; product derivation names the actor/role per UX flow
- States output lifecycle: drafts staged in `artefacts/build/spec-drafts/`, promotion to `artefacts/{category}/derived/` behind approval (T-018 DoD); canonical docs never rewritten; drift section vs canonical docs
- References the workflows README § 4 (runtime/tools) without duplicating the schema table

#### Primary Output Path

`context/skills/derive-spec.md`

### T-002: Create workflow `context/workflows/derive-spec.yaml` (modes, phases, gates, state recovery)

#### Acceptance Criteria

- Phases 0–8 per workflows README (diagram + Commands, phase-aligned): intake (0) · discovery + repo profile (1) · baseline + drift (2) · evidence (3) · derivation 4a/4b (mode conditional) · draft (5) · verification (6) · confirmation (7) · finalise + gate (8); shared phases single-run
- Intake inputs: `mode`, `target` (service root passed to the indexer via `--repo <service-root>`), limits, output location
- Each phase declares `agents`, `outputs`, `validation:`; gate phases (Phase 6 verification pass, Phase 8 final review) marked `gate: true` with APPROVED semantics
- `state_recovery:` reads `artefacts/build/spec-scan.md`, `repo-profile.md` and `repo-index.json`; critical files listed
- Promotion path wired: drafts in `artefacts/build/spec-drafts/`; APPROVED copies to `artefacts/{category}/derived/`
- Phase 6 invokes `spec_indexer.py verify --index`; Phase 8 invokes `verify --doc` on drafts

#### Primary Output Path

`context/workflows/derive-spec.yaml`

### T-003: Extend `context/agents/product-owner.md` — Mode 3 derive (loads derive-spec skill)

#### Acceptance Criteria

- New Mode (derive) declared alongside existing modes: loads `derive-spec.md`, runs product derivation, writes drafts, bats MC questions (Q2 format), updates per answers
- Product derivation includes actor/role discovery from auth/permission evidence (`reverse-spec.md` §1.1); each UX flow names its actor, cited to the auth evidence
- Intake, escalation, reporting, state-recovery protocols unchanged; derives never promote

#### Primary Output Path

`context/agents/product-owner.md`

### T-004: Extend `context/agents/solution-architect.md` — derive mode (drafts only)

#### Acceptance Criteria

- Derive mode: architecture / API / data-model drafting from index evidence, drafts only (`*.derived.md`), canonical ownership boundary preserved (`openapi.yaml` untouched)
- Runs Review Mode trace checks against index call chains

#### Primary Output Path

`context/agents/solution-architect.md`

### T-005: Add confirmation mode to `context/skills/requirements-elicitation.md`

#### Acceptance Criteria

- Confirmation mode documented distinctly from problem-discovery: batched MC + Other, evidence-cited, one/two questions at a time, stop-and-wait
- Exit criteria: every Assumed / Needs-Confirmation claim has a question; confirmed answers update drafts **and** the banded confidence (Assumed → Needs Confirmation → Verified); questions the human cannot answer stay Assumed and remain in the open-questions appendix as still-open

#### Primary Output Path

`context/skills/requirements-elicitation.md`

### T-006: Add `context/templates/derived-spec-template.md` (confidence schema + open-question appendix)

#### Acceptance Criteria

- Subsection skeletons for product-spec / architecture / data model / api catalogue with confidence fields (tier + banded % + evidence `path:line`)
- Open-question appendix format (per subsection, priority, MC options), drift section header
- Confidence band rubric + promotion DoD drafted here, hardened with T-018

#### Primary Output Path

`context/templates/derived-spec-template.md`

---

### T-018: Confidence bands + promotion DoD in `derived-spec-template.md` (Verified 85–100 · Needs Confirmation 50–85 · Assumed <50; unanswered stays Assumed)

#### Acceptance Criteria

- Band table with fixed ranges (Verified 85–100 · Needs Confirmation 50–85 · Assumed <50) stating what evidence each band requires (citations + usage counts, call chains, human-confirmed)
- Per-doc promotion definition of done (e.g. no subsection below Needs Confirmation and no blocking still-open questions, or recorded human override)
- Update rule baked into the subsection template: confirmed answer → raise band/%; unanswered question → stays Assumed and remains in the open-questions appendix as still-open
- Consumed by T-005 exit criteria and the Phase 8 promotion decision

#### Primary Output Path

`context/templates/derived-spec-template.md` (amended with T-006)

---

### T-007: Regenerate adapters; run validators green

#### Acceptance Criteria

- `uv run python context/scripts/generators/generate_adapters.py` reflects the new skill/workflow in AGENTS.md/CLINE.md/GEMINI.md registries (if projection applies)
- `uv run pytest context/scripts/tests/` green; `adapter_drift.py` and `tech_writing.py` green on changed files

#### Primary Output Path

Generated registry files; commit message in `/tmp/T-007_commit_msg.txt`

### T-010: Unit tests: skill/workflow schema, indexer extraction + verify

#### Acceptance Criteria

- Skill frontmatter schema test; workflow YAML phase-schema test (unique ids, resolvable `depends_on`, known agents, gates defined)
- Indexer tests: Python extraction (symbols, routes, constants), TS/TSX extraction (components, props, usage counts — fixture per smoke test), SQL table parsing, `verify` pass/fail on synthetic repo
- **T-015 backend parity tests**:
  - `--extractors stdlib` on this repo reproduces the `auto` symbol/api/schema counts exactly (determinism contract)
  - TS/JSX fixture scan with `--extractors tree-sitter` yields strictly richer output than `--extractors stdlib` (captures multiline destructured props, accurate JSX usage counts, decorator annotations) — asserted as a diff delta
  - `--extractors ctags` available when `ctags` on PATH; `ast-grep` when `sg` on PATH; `ts-morph` when `node` + `ts-morph` resolvable — all degraded cleanly when absent
  - `meta.extractors` provenance populated; per-file `extractor` field populated; `meta.confidence` tier set correctly
  - invalid `--extractors bad` exits non-zero with a clear message
- `uv run pytest context/scripts/tests/test_spec_indexer.py` green

#### Primary Output Path

`context/scripts/tests/test_spec_indexer.py`

---

### T-020: Extend `verify` with `--require-coverage` (deterministic Phase 6 gate: tier + % + citation per subsection)

#### Acceptance Criteria

- `spec_indexer.py verify --doc --require-coverage` exits non-zero listing subsections missing tier / banded % / `file:line` in a derived-spec doc
- Coverage check parses the template's confidence fields (T-006/T-018 schema) so the Phase 6 "question coverage" check is deterministic, not agent-discretion
- Documented in the analyse-repo skill (T-014) and README Commands; run against pilot A/B drafts (T-008/T-019)

#### Primary Output Path

`context/scripts/code-specs/spec_indexer.py` (extend `verify`) + `context/scripts/tests/test_spec_indexer.py`

---

### T-021: Indexer comment & docstring extraction (`comments` key)

#### Acceptance Criteria

- Python: collect `#` comments via stdlib `tokenize` (AST drops comments by design) and docstrings via `ast.get_docstring()` on module/class/function nodes — zero-LLM, per-file, exact `file:line`
- TS/JS: JSDoc `/** */` + `//` capture on raw source lines (regex v1; tree-sitter backend from T-015 when present); SQL `--` / `/* */` comments attached to the nearest table/column from the CREATE TABLE parser
- Schema (additive): per-symbol `docstring` and `comments` entries (`{text, line, kind: leading|inline|block, attached: {kind, name, line}}`) plus a top-level `comments` stream for orphan comments (magic-number explanations, TODOs, licence headers)
- Comments attach to symbols by line-range overlap (inline) and contiguous leading blocks immediately above a definition (doc-comment style); orphan comments stay in the top-level stream
- Deterministic + idempotent; `verify --index` covers the new comment citations; `spec-scan.md` shows a compact per-file comment map
- analyse-repo skill (T-014) documents consumption: read `symbols[].docstring` / `comments` from the index before any source read; only read the exact cited range when the index text is insufficient (agent-sandbox tool policy)
- Feeds: business intent + domain rules → product spec; magic numbers / limits → TSD constraints; JSDoc semantics → api-catalogue draft; deprecation/TODO comments → drift + open questions; comment-backed claims may reach Needs Confirmation band without a human answer

#### Primary Output Path

`context/scripts/code-specs/spec_indexer.py` (+ `context/workflows/README.md` index table, `context/skills/analyse-repo.md`)

---

### T-008: Pilot A: run derive-spec (`mode=both`) on this repo; measure token ledger before/after; outputs land in `derived/`

#### Acceptance Criteria

- `scan` + draft + confirmation + review run end-to-end on start-here (Pilot A)
- Every generated subsection carries tier + banded % + citation; `verify --doc` on all drafts passes
- Final docs land in `artefacts/{product,architecture}/derived/`; canonical `requirements.md` / `architecture.md` untouched (`git diff --stat` shows zero changes to canonical)
- Drift section present where derived behaviour differs from `requirements.md` / `architecture.md`
- Token ledger filled with measured before/after

##### Token Ledger (derive-spec pilots)

Measured during the T-008 pilot on this repo (`mode=both` skeleton figures;
before/after comparison is the acceptance metric):

| Work | Zero-LLM tools | Agent LLM (rough) |
|------|----------------|-------------------|
| Scan + inventory (198 pytest node-ids in 0.09s, `ast`, route/schema/UI extractors) | ~0 tokens | ~0 |
| Synthesis: features, UX flows, architecture, API, data model | — | ~25–60k |
| Elicitation (batched MC) + finalise | — | ~10–25k |
| **Naive alternative** (agent reads the repository itself) | — | ~200–500k, bounded by repo size |

`@harness-analyst` may audit this with the `tokenomics-audit` lens (glob `artefacts/build/**`).

#### Primary Output Path

`artefacts/build/spec-pilot-report.md`

---

### T-019: Pilot B: derive-spec on the human-chosen foreign/unorganised repo; validate Phases 1–2 + `derived/` landing

#### Acceptance Criteria

- Run derive-spec end-to-end (`mode=both`) on the human-chosen foreign repo (repo + URL recorded in HANDOFF.md at pilot start; not organised like start-here — no harness artefacts layout)
- Phases 1–2 validated: repo profile correctly characterises app type / entry points / module boundaries; doc discovery finds candidates via basename/glob patterns; drift section populated where README/spec docs disagree with code
- Outputs land in `<foreign-repo>/artefacts/{product,architecture}/derived/` (repo-local), canonical docs untouched
- `verify --doc` passes; `--require-coverage` (T-020) passes if implemented; token ledger extended with pilot B measurements
- Unstructured-repo gaps feed back into the T-016/T-017 backlog (config/history evidence)

#### Primary Output Path

`artefacts/build/spec-pilot-report.md` (extended — records pilots A and B)

---

### T-009: Optional: register derive-spec as a `build.yaml` precursor phase

#### Acceptance Criteria

- derive-spec gate completes before build `task-planning` when specs missing; disabled otherwise

#### Primary Output Path

`context/workflows/build.yaml`

### T-013: Wire indexer into `derive-spec.yaml` Phases 1 & 3 (agent `tool_scope` = index + cited ranges)

#### Acceptance Criteria

- Phases 1/3 consume `repo-index.json` + `spec-scan.md`; agent `tool_scope` restricted to index + cited line ranges
- Phase 1 wires `repo-profile.md` (agent synthesis from the index: app type, entry points, module boundaries) as an input to Phases 2–5
- Promotion path wired: `artefacts/build/spec-drafts/` → `artefacts/{category}/derived/` on APPROVED (per T-018 DoD)
- Re-scan rule documented (index refresh before `verify`)

#### Primary Output Path

`context/workflows/derive-spec.yaml` (with T-002)

### T-015: Tool-backed extraction backends with graceful fallback (`--extractors`: ctags, tree-sitter, ast-grep, ts-morph)

**Status**: completed 2026-01-11 — `--extractors` (auto/stdlib/ctags/tree-sitter/ast-grep/ts-morph) implemented in `spec_indexer.py`; tree-sitter TS/TSX walker (multiline props, JSX usage, decorators); ast-grep rule patterns; ctags JSON for foreign langs; `ts_extract.mjs` ts-morph helper (skipped quietly when absent); `meta.extractors` provenance + `meta.confidence` tier + per-file `extractor` field. Tests: auto/stdlib Python parity + auto⊇stdlib superset + fixtures (13 passed, 2 skipped without tree-sitter; 15/15 with `uv run --with tree-sitter --with tree-sitter-language-pack`).

#### Acceptance Criteria

- `--extractors` flag honoured with choices `auto` (default), `stdlib`, `ctags`, `tree-sitter`, `ast-grep`, `ts-morph`:
  - `auto` probes the toolchain and prefers the richest backend available per language, degrading deterministically with a recorded provenance entry; selecting a backend that is absent errors clearly (non-zero exit with a message naming the missing tool)
  - `stdlib` is the zero-dependency portability mode (stdlib `ast` + regex for TS/JS + PyYAML + SQL heuristics; no external CLI)
- Backends implemented, each wrapped so an absent/broken tool never aborts the scan:
  - **universal-ctags**: `--output-format=json --fields=+n`; primary symbol source for languages without a dedicated parser and cross-check for Python/TS; `path`/`kind`/`line`/`language` mapped to the spec symbol model (`function`/`class`/`module`/`variable`/etc.)
  - **tree-sitter**: via `uv run --with tree-sitter --with tree-sitter-language-pack`; real AST pass for TS/TSX delivering named imports, multiline destructured props, JSX usage counts, and decorator annotations (replaces regex heuristics for those fields)
  - **ast-grep** (`ast-grep run -p PATTERN --json`; legacy `sg` alias deprecated as of 0.51): rule-driven TS/JS pass used when tree-sitter is absent but `ast-grep` is on PATH
  - **ts-morph**: optional Node helper `context/scripts/code-specs/ts_extract.mjs` (guarded by `node` + resolvable `ts-morph`); skipped quietly when absent
  - **Python stdlib `ast`** + regex + PyYAML + SQL heuristics retained as the permanent fallback tier for all languages
- **Provenance & confidence** (additive schema, no consumer changes):
  - `meta.extractors`: per-tool `{available, used, reason}` map + `meta.warnings` entries for any degraded backend
  - per-file `extractor` field on each `FileRecord` (`stdlib.ast`, `tree-sitter`, `ctags`, `ast-grep`, `ts-morph`)
  - `confidence` tier in `meta` (full when a real AST backend was used for a language; lower when regex fallback)
- **Parity & integrity**:
  - `auto` scan of this repo (Python-only) produces the same symbol set as the current zero-dependency index (no regression in `files`/`symbols`/`api`/`schema`)
  - a synthetic TS/JSX fixture demonstrates richer output vs the regex backend (extra props via multiline destructure, accurate `Header` usage count, decorator capture) — captured as a fixture + assertion in the test suite
  - `--extractors stdlib` reproduces the zero-dependency result exactly (determinism contract)
  - `verify --index` remains green; `--extractors bad` exits non-zero
- Docstring and `context/workflows/README.md` (§ derive-spec Commands) reflect the real backends and the `--extractors` flag

#### Primary Output Path

`context/scripts/code-specs/spec_indexer.py` + `context/scripts/code-specs/ts_extract.mjs` (+ docs: `context/workflows/README.md` § derive-spec Commands, `artefacts/build/tasks-spec-agent.md`)

### T-SETUP: Install / verify toolchain dependencies (human-run) before implementation starts

**Status**: completed 2026-01-11 — ctags 6.2.1 ✓, ast-grep 0.51.0 ✓ (use `ast-grep`; `sg` deprecated), tree-sitter loads via `uv run --with tree-sitter --with tree-sitter-language-pack` (typescript + python parsers) ✓, ts-morph absent → skipped quietly.

#### Acceptance Criteria

- Required runtime present and versioned:
  - `uv --version` (Python package manager)
  - `git --version` · `node --version` · `yarn --version` · `jq --version`
- `pyyaml` importable in the project environment (already declared in `pyproject.toml`):
  - `uv run python -c "import yaml; print(yaml.__version__)"`
- Recommended (optional, enables the T-015 backends at pilot time):
  - `brew install universal-ctags ast-grep`, then `ctags --version` and `sg --version` succeed
  - `uv run --with tree-sitter --with tree-sitter-language-pack python -c "from tree_sitter_language_pack import get_parser; get_parser('typescript')"` succeeds (T-015 tree-sitter backend)
  - `node -e "require.resolve('ts-morph')"` resolves in the project (T-015 ts-morph backend; otherwise skipped quietly)
- Confirmation that the harness is green before implementation work starts:
  - `uv run pytest context/scripts/tests/ -q` → all pass
  - `uv run context/scripts/code-specs/spec_indexer.py scan --repo . --mode both` succeeds
  - `uv run context/scripts/code-specs/spec_indexer.py scan --repo . --mode both --extractors stdlib` matches the `auto` output (T-015 parity)
  - `uv run context/scripts/code-specs/spec_indexer.py verify --index artefacts/build/repo-index.json` → OK

#### Primary Output Path

Environment only — verify via the acceptance criteria; record completion in HANDOFF.md (`Workflow: derive-spec`, note "deps installed").

---

### T-016: Indexer `config` extraction (env / config / feature flags)

#### Acceptance Criteria

- `scan` collects env-style keys and defaults from `.env.example`, `settings.py` / `config.*` modules, and YAML/JSON config files into a new `config` key: `[ {key, source(file:line), value-hint} ]`
- Feature flags / environment toggles (e.g. `ENABLE_*`, boolean config entries) are flagged as such
- Zero-LLM and deterministic; `verify --index` covers the new citations; `--extractors` backends contribute where they add value (e.g. ctags for `config.*`)
- Documented in the analyse-repo skill (T-014) and README `## Repository Index` table
- Feeds phases 4a/4b: user-facing constraints → product spec + TSD constraints subsections (reverse-spec/arch "user-facing technical constraints")

#### Primary Output Path

`context/scripts/code-specs/spec_indexer.py` (+ `context/workflows/README.md` index table, `context/skills/analyse-repo.md`)

---

### T-017: Indexer `meta.history` (capped git-history evidence)

#### Acceptance Criteria

- `scan` records `meta.history`: last N (default 200) commit subjects + rename/refactor clues (`git log --name-status`, capped), zero-LLM
- Optional flag `--history N` bounds the pull; key absent when the repo has no git metadata
- Used by the agent as cheap feature descriptions, esp. for unorganised repos — commit subjects may cite feature intent
- Documented in the analyse-repo skill (T-014) and README `## Repository Index` table

#### Primary Output Path

`context/scripts/code-specs/spec_indexer.py` (+ `context/workflows/README.md` index table, `context/skills/analyse-repo.md`)

---

#### Orchestrator Notes

**Parallelism Strategy**

- T-015 → T-016 (config) + T-017 (history) + T-021 (comments) run critical path after Q0
- T-014 (analyse-repo skill) depends on T-015/T-016/T-017/T-021 being implemented
- T-001 → T-002 → T-003 + T-004 + T-005 run in parallel (file-scope disjoint)
- T-006 + T-018 → T-007 → T-010 (+ T-020) → T-008 (Pilot A) → T-019 (Pilot B) → T-009, T-013

**Commit Strategy**

One commit per task on `feat/spec-agent`, conventional messages (`feat(spec): …`, `docs(workflows): …`, `test(spec): …`). Push after every commit.

**Backlog Cleanup**

- Verify `uv run pytest context/scripts/tests/ -q` → all pass before implementation
- Confirm ctags/ast-grep/tree-sitter binaries available if targeting those extractors
- Document any degraded-mode warnings encountered during pilot run

---

### T-014: Wrap indexer tool usage in skill `context/skills/analyse-repo.md` (documents the actual backends)

#### Acceptance Criteria

- Frontmatter matches the skill schema: `name: analyse-repo`, `description` (procedural guidance for analysing a repository with the deterministic spec-indexer tools before agent synthesis), `globs` covering `**/repo-index.json`, `**/spec-scan.md`, `**/repo-profile.md`, `**/*.py`, `**/*.ts`
- Documents, with exact commands and flags:
  - `scan` invocation per derive-spec phases 1/3 (`--repo`, `--mode`, `--max-files`, `--out`, `--extractors`), and `verify --index` / `verify --doc` per phases 6/8
  - consuming `repo-index.json` (schema summary incl. `meta.extractors` provenance and per-file `extractor` field), `spec-scan.md`, and `repo-profile.md`; documents the planned `config` (T-016) and `meta.history` (T-017) keys once implemented
  - documents how the agent writes `repo-profile.md` (app type, entry points, module boundaries) as the Phase 1 deliverable
  - documents the actual T-015 backends (tree-sitter / ast-grep / ctags / ts-morph / stdlib fallback) and their `--extractors` choices, with degradation semantics
  - evidence citation discipline (`file:line` per claim) and confidence bands (Verified 85–100 · Needs Confirmation 50–85 · Assumed <50)
  - re-scan rule: refresh the index before `verify` after any edit
  - token rationale: extraction is zero-LLM; the agent reads the index and cited line ranges only
- States that agents must invoke the tools rather than reading the repository directly (README derive-spec note: "invoke tools analyse the repo using the analyse-repo skill")
- `context/workflows/README.md` derive-spec `## Commands` and `## Repository Index` sections reduced to a pointer to the skill (no duplicated procedure)

#### Primary Output Path

`context/skills/analyse-repo.md` (+ pointer edit in `context/workflows/README.md`)

---

## Orchestrator Notes

### Parallelism Strategy

**Sprint 1** (critical path after Q0): **T-SETUP (human installs deps, blocks all implementation)** → T-015 (extraction backends) → T-016 (config extraction) → T-017 (git-history evidence) → T-021 (comment/docstring extraction) → T-014 (analyse-repo skill, documents the backends) → T-001 → T-002 → T-003 + T-004 + T-005 (parallel, file-scope disjoint) → T-006 + T-018 (template + confidence bands) → T-007 → T-010 (+ T-020) → T-008 (Pilot A) → T-019 (Pilot B) → T-009, T-013.
file_scope: `context/skills/` (T-001, T-005, T-014), `context/agents/` (T-003, T-004), `context/templates/` (T-006, T-018), `context/scripts/code-specs/` (T-015, T-016, T-017, T-020, T-021), `artefacts/build/` (T-019 reports)

### Commit Strategy

One commit per task on `feat/spec-agent`, conventional messages (`feat(spec): …`, `docs(workflows): …`, `test(spec): …`). Push after every commit.

### Backlog Cleanup

- `todo.md`: no overlapping items identified; the workflows README (T-011) reduces the “AGENTS.md distribution” backlog item tension by centralising workflow documentation.



