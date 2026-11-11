# Handoff: B-008 — content at front of derived docs should be in the appendix

**From**: @orchestrator (default agent, small-task workflow)
**To**: @human-operator
**Date**: 2026-11-11
**Workflow**: small-task
**Phase**: hitl (complete — awaiting human APPROVED)
**Status**: implemented + validated; not yet committed (human gate)

---

## Summary

Derived docs now open with content and carry their boilerplate in a trailing
appendix, per B-008. The layout rule is enforced in the source of truth
(template + skills + workflow validation), so future derive-spec runs produce
content-first docs — not just the current pilot output.

## Changes

| File | Change |
|------|--------|
| `context/templates/derived-spec-template.md` | Content skeletons open the doc; `## Drift` (when baseline docs exist) → `## Appendices` container with A · Run Metadata, B · Confidence Schema, C · Subsection Format, D · Open Questions, E · Verification and Review Record; instruction comment states the content-first rule (B-008) |
| `context/scripts/code-specs/spec_indexer.py` | `_COVERAGE_NON_CONTENT_RE` extended: `Appendices` container + `Appendix …` items are structural (was exact-title anchored — would have failed the coverage gate on the new headings); docstring updated |
| `context/scripts/tests/test_spec_indexer.py` | New `test_coverage_skips_appendices_container_and_items` regression test (13/13 TestDocCoverage pass) |
| `context/skills/analyse-repo.md` | §2.1 structural-section list now includes Appendices container/items + Run Metadata |
| `context/skills/derive-spec.md` | Phase 5: content-first wording, boilerplate → Appendices container |
| `context/workflows/derive-spec.yaml` | Phase 5 validation: content-first layout check |
| `artefacts/build/derived/*.md` + `derived-spec-working/*-draft.md` (8) | Restructured in place — content opens, Drift before Appendices, all five boilerplate sections relocated into the appendices; body lines byte-preserved |

## Validation

- Full scripts suite → **295 passed, 2 skipped, 3 failed** — the same
  pre-existing failure set as before this change (2 e2e compilation drift from
  the `agents-md.yaml` harness commits; 1 workflow-schema glob treating
  `agents-md.yaml` as a workflow). Verified the 3 failures were pre-existing
  via a clean HEAD worktree comparison.
- `verify --doc --require-coverage` on all 8 docs → outcome identical to HEAD
  baseline: api-catalogue + data-model **green** (2/3 content subsections);
  product-spec + architecture carry the same pre-existing stale citations
  (`generate_adapters.py:428` points at a blank line, `derive-spec.yaml:188`)
  that fail identically on the pristine copies — not introduced here.
- `ruff check` + `ruff format --check` clean; `tech_writing.py spelling` clean
  on all 8 docs + template + skills.
- `adapter_drift.py` ✅ in sync (projections regenerated after skill edits).
- `verify_typst_formatting.py` passes (derived docs are not typst-gated).

## Pre-existing findings (unchanged by this task, surfaced by validators)

- `agent_definitions.py`: `tech-lead.md` cites `solution-architect.md §Review
  Mode: End-to-End Data Flow Tracing` which does not exist (unrelated to B-008;
  agent files untouched).
- `secrets.py`: flags the local `.env` file (gitignored, local environment).

## Next Steps

| ID | Task | Priority | Status |
|----|------|----------|--------|
| B-010 | After open questions are answered, update docs with answers + confidence band | high | open |

## Key Decisions

- Coverage gate is the enforcement point: instead of a layout linter, the
  existing `verify --doc --require-coverage` and the updated template/skills
  keep future runs content-first; appendix headings are structural (skipped),
  content subsections carry Confidence lines.
- Drift stays a top-level section before the appendices (it is review-critical
  content, not boilerplate); the bug's "examples" list did not include it.
- Product-spec skips Appendix C (Subsection Format): its placeholder body was
  consumed into real content when the doc was authored, so the item would be
  empty; lettering stays aligned with the template for the other docs.

<!-- state: awaiting human APPROVED before commit -->