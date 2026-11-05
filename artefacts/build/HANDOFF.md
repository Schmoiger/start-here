# Handoff: Derive-Spec Harness (spec-agent)

**From**: @orchestrator
**To**: @human-operator
**Date**: 2026-05-11
**Workflow**: small-task
**Phase**: promote
**Status**: promoted

---

## Summary

T-010 (unit tests for spec-indexer) is **completed and committed** (8fa3ada + d9e98cd). 
All 22 tests pass; full scripts suite 243/245 green (2 skipped, tree-sitter backend).

**T-008: Pilot A — run derive-spec (`mode=both`) on this repo** is **complete**. 
Drafts staged in `artefacts/build/spec-drafts/` and promoted to 
`artefacts/build/derived/` (per human Q-001/Q-010 decision to use `build/derived/` 
instead of `artefacts/{category}/derived/`). All 4 drafts pass `verify --doc`.
Token ledger measurement: pending (not yet instrumented in repo).

---

## Tasks Completed

| ID | Task | Status | Notes |
|----|------|--------|-------|
| T-010 | Unit tests: skill/workflow schema, indexer extraction + verify | completed | committed 8fa3ada + d9e98cd; 22/22 pass |
| T-008 | Pilot A: run derive-spec (`mode=both`) on this repo | completed | Phase 1-6 complete; Phase 7 human Qs answered; Phase 8 promoted |

---

## Next Tasks

| ID | Task | Priority | Depends On |
|----|------|----------|------------|
| T-020 | Extend `verify` with `--require-coverage` | low | T-010 ✅ |

---

## Derive-Spec Intake (Phase 0) — Completed

| Field | Value |
|-------|-------|
| Mode | both (product + technical) |
| Target | . (repo root) |
| Max files | 2000 (default) |
| Extractors | stdlib.ast + ast-grep (tree-sitter unavailable in env) |
| Output drafts | `artefacts/build/spec-drafts/` |
| Promotion target | `artefacts/build/derived/` (human Q-001/Q-010 override) |

---

## Phase Status

| Phase | Name | Status |
|-------|------|--------|
| 0 | Intake & Scope | ✅ complete |
| 1 | Repo & Doc Discovery | ✅ complete (61 files, 731 symbols, 245 tests, 25 docs, 8 config keys) |
| 2 | Baseline & Drift | ✅ complete (D-001…D-004) |
| 3 | Evidence Gathering | ✅ complete |
| 4a | Product Draft | ✅ complete |
| 4b | Technical Drafts | ✅ complete |
| 5 | Draft stage | ✅ complete |
| 6 | Verification | ✅ complete (`verify --index` OK; `verify --doc` OK on all 4 drafts) |
| 7 | Human confirmation | ✅ complete (Q-001, Q-002, Q-003, Q-010, Q-011, Q-020, Q-022 APPROVED; Q-021, Q-023 remain still-open) |
| 8 | Promotion | ✅ complete (4 drafts → `artefacts/build/derived/`) |

---

## Open Questions (Confirmed / Still-Open)

| ID | Decision |
|----|----------|
| Q-001 | Product spec → `build/derived/` (**APPROVED**) |
| Q-002 | UX flows complete as listed (**APPROVED**) |
| Q-003 | Runtime Projection kept unified (**APPROVED**) |
| Q-010 | Architecture → `build/derived/` (**APPROVED**) |
| Q-011 | 6 components (not 7) (**APPROVED**) |
| Q-020 | CLI/library-only (no HTTP routes; index api=0) (**APPROVED**) |
| Q-021 | Remove empty "Request and Response Shapes" subsection? (**still-open**) |
| Q-023 | Remove empty "Columns and Constraints" subsection? (**still-open**) |

---

## Artefacts Created / Modified

### New (T-008)
- `artefacts/build/spec-drafts/product-spec.md`
- `artefacts/build/spec-drafts/architecture.md`
- `artefacts/build/spec-drafts/api-catalogue.md`
- `artefacts/build/spec-drafts/data-model.md`
- `artefacts/build/derived/product-spec.md` (promoted)
- `artefacts/build/derived/architecture.md` (promoted)
- `artefacts/build/derived/api-catalogue.md` (promoted)
- `artefacts/build/derived/data-model.md` (promoted)

### Modified (T-008)
- `artefacts/build/HANDOFF.md`

### Existing (unchanged)
- `context/scripts/code-specs/spec_indexer.py`
- `context/scripts/tests/test_spec_indexer.py`
- `artefacts/product/requirements.md` (example placeholder — D-001)
- `artefacts/architecture/architecture.md` (example placeholder — D-002)
- `artefacts/architecture/data-model.md`, `artefacts/architecture/api-catalogue.md`

---

## Statistics

- **Tests**: 22/22 (test_spec_indexer.py); full scripts suite 243/245 (2 skipped, tree-sitter backend)
- **Index**: 731 symbols, 61 Python files, 8 config keys, 245 tests, 25 docs
- **Verify**: 739 citations resolve; 4 drafts verified OK

---

## Key Decisions

- The `quality_gates` schema is intentionally heterogeneous across workflows
  (bugfix uses `{phase, type, required, criteria}`; derive-spec/small-task use
  `{phase, gate, ...}`). The phase-schema contract therefore asserts reference
  integrity (every `quality_gates[].phase` resolves; every phase `gate` is boolean)
  rather than a uniform shape.
- T-015 backend-parity tests already live in `test_spec_indexer_extractors.py`;
  this file adds T-010's core extraction + schema + verify coverage plus an
  invalid-extractor/provenance smoke test, avoiding duplication.
- Promotion target overridden to `artefacts/build/derived/` per human Q-001/Q-010
  (workflow template default is `artefacts/{category}/derived/`).
- Component count corrected to 6 per human Q-011.

<!-- state: ready for commit -->