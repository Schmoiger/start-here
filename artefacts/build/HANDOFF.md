# Handoff: T-020 — `verify --require-coverage` (deterministic Phase 6 gate)

**From**: @orchestrator (default agent, small-task workflow)
**To**: @human-operator
**Date**: 2026-09-11
**Workflow**: small-task
**Phase**: complete
**Status**: completed — human APPROVED; committed `0ccd87c` (feat), pushed to `feat/spec-agent`

---

## Summary

`spec_indexer.py verify` gains a deterministic Phase 6 coverage gate,
implemented, tested, and validated against the acceptance criteria:

- **`verify --doc --require-coverage`** parses the derived-spec confidence
  schema and exits non-zero listing every content subsection missing tier /
  banded % / `file:line`. Content subsections are `##`-`####` headings minus
  structural sections (Confidence Schema, Subsection Format,
  Open-Questions Appendix, Drift, Verification and Review Record) and
  `{placeholder}` headings. Field errors are reported per subsection and
  band/% consistency is enforced against fixed bands (Verified 85–100 ·
  Needs Confirmation 50–85 · Assumed <50; 85 valid for the two high tiers).
- **Deterministic, not agent-discretion**: parsing keys off the template
  schema (tier + `NN%` + `path.ext:NN`), so Phase 6 question coverage is
  machine-checked; `derive-spec.yaml` Phase 6 validation now runs
  `verify --doc --require-coverage` on the staged drafts.
- **Docs**: analyse-repo §2.1 documents the gate; workflows README command
  list updated. `_CITATION_RE` now matches `.md` citations too (surfaced and
  fixed a wrong `requirements.md:133` citation in product-spec).
- **Run against pilot A draft outputs**: all 4 derived docs + 4 working
  drafts were repaired to cite real index rows
  (`derived-spec-working/repo-index.json:452/7466/7467`); all 8 now pass
  `verify --doc --require-coverage`.

## Changes

| File | Change |
|------|--------|
| `context/scripts/code-specs/spec_indexer.py` | `check_doc_coverage()`, `--require-coverage` flag + `--doc` guard, coverage reporting in `run_verify`, `.md` added to `_CITATION_RE` |
| `context/scripts/tests/test_spec_indexer.py` | **`TestDocCoverage`** — 12 new tests |
| `context/skills/analyse-repo.md` | §2.1 gate documentation (no task tags) |
| `context/workflows/README.md` | command list gains `verify --doc --require-coverage` |
| `context/workflows/derive-spec.yaml` | Phase 6 validation wired to the deterministic gate |
| `artefacts/build/derived/*.md` (4) + `derived-spec-working/*-draft.md` (4) | evidence repaired to real index file:line citations so coverage+verify pass |
| `artefacts/build/tasks-spec-agent.md` | T-020 → completed + amendment log |

## Validation

- `uv run pytest context/scripts/tests/test_spec_indexer.py -q` → **34 passed**
- Full scripts suite → **268 passed, 2 skipped, 0 failed**
- `verify --doc --require-coverage` on all 4 derived + 4 draft docs → exit 0,
  coverage OK, citations resolve
- `--require-coverage` without `--doc` → exit 2 with a clear error
- `uv run --with ruff ruff check` → clean (spec_indexer.py, test file)
- Adapter projections regenerated (gitignored) after the source edits so the
  drift tests stay green.

## Next Tasks

| ID | Task | Priority | Depends On | Status |
|----|------|----------|------------|--------|
| T-019 | Pilot B: derive-spec on foreign/unorganised repo | critical | T-008 ✅ | pending |
| T-021 | Indexer `comments` extraction | high | T-015 ✅ | pending |

## Key Decisions

- Coverage treats any `##`-`####` heading as a content subsection unless it is
  a structural section or a `{placeholder}`; structural names are the template
  set (Confidence Schema, Subsection Format, Open-Questions Appendix, Drift,
  Verification and Review Record).
- A section that HAS a confidence line is "covered" for counting but its line
  is still field-validated, so malformed lines both count and fail the gate.
- `.md` added to citation matching: derived specs cite markdown docs (e.g.
  `orchestrator.md:115-140`); this also made `verify --doc` catch silently
  skipped dangling citations (fixed two `requirements.md` paths).
- Scope: indexer + tests + 2 skill/README docs + workflow yaml + pilot A doc
  repairs — H1 AMBER, one logical unit, small task, python-scripting skill.

<!-- state: ready for commit -->
