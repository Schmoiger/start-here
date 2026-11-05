# Handoff: Derive-Spec Harness (spec-agent)

**From**: @orchestrator
**To**: @human-operator
**Date**: 2026-05-11
**Workflow**: small-task
**Phase**: hitl
**Status**: needs_review

---

## Summary

Implemented T-010: a new unit-test suite at `context/scripts/tests/test_spec_indexer.py`
covering skill frontmatter schema, workflow YAML phase-schema, indexer extraction
(Python / TS/TSX / SQL), and `verify` pass/fail on synthetic repos. All 22 tests
pass; the full scripts suite (243 passed, 2 skipped) remains green and ruff is clean.
Awaiting human APPROVED on the diff before commit.

---

## Tasks Completed

| ID | Task | Status | Notes |
|----|------|--------|-------|
| T-010 | Unit tests: skill/workflow schema, indexer extraction + verify | partial | tests written + green; awaiting human APPROVED to commit |

---

## Next Tasks

| ID | Task | Priority | Depends On |
|----|------|----------|------------|
| T-008 | Pilot A: run derive-spec (`mode=both`) on this repo | critical | T-010 |
| T-020 | Extend `verify` with `--require-coverage` | low | T-010 |

---

## Artefacts

- **Tests**: `context/scripts/tests/test_spec_indexer.py`
- **Source under test**: `context/scripts/code-specs/spec_indexer.py`

---

## Statistics

- **Tests**: 22/22 (new file); full scripts suite 243/245 (2 skipped, tree-sitter backend)
- **Files Created**: 2 (`test_spec_indexer.py`, this `HANDOFF.md`)
- **Files Modified**: 0

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

<!-- state: awaiting human APPROVED on the T-010 diff before commit -->