# Handoff: T-018 — Confidence bands + promotion DoD in `derived-spec-template.md`

**From**: @orchestrator (default agent, small-task workflow)
**To**: @human-operator
**Date**: 2026-09-11
**Workflow**: small-task
**Phase**: complete
**Status**: completed — human APPROVED; committed `3c583dc` (docs), pushed to `feat/spec-agent`

---

## Summary

T-018 hardens the confidence schema and promotion definition of done that
T-006 drafted (the template previously said "drafted here, hardened with
T-018"). The template is now the **single source of truth** consumed by the
T-005 confirmation-mode exit criteria and the derive-spec Phase 8 promotion
decision, per the acceptance criteria:

- **Band table, fixed ranges, evidence per band**: Verified 85–100 (resolving
  `path:line` citations; usage counts / call chains where material),
  Needs Confirmation 50–85 (plausible from indexed evidence, requires a human
  answer — Phase 7 / T-005), Assumed <50 (inference only).
- **Per-doc Promotion DoD** (itemised): every subsection at Needs Confirmation
  or above, no blocking still-open question, `verify --doc` pass, review
  record + drift confirmed, APPROVED gate; recorded-human-override path; each
  doc promotes independently.
- **Update rule baked into the subsection template**: confirmed → raise
  band/% and cite; unanswered → stays Assumed + still-open appendix row;
  never promote silently.
- **Consumed by T-005 and Phase 8**: `requirements-elicitation.md` §3.3/§3.4
  (confirmation-mode exit criteria) and `derive-spec.md` (Confidence Model,
  Phase 8) now point at the template as the definition; `derive-spec.yaml`
  already referenced the T-018 DoD.

## Changes

| File | Change |
|------|--------|
| `context/templates/derived-spec-template.md` | hardened Confidence Schema (band evidence table, itemised Promotion DoD, update rule, consumer references); update rule baked into subsection comment; Promotion DoD row in review record |
| `context/skills/requirements-elicitation.md` | §3.3 DoD definition pointer + §3.4 exit-criteria bullet (T-018) |
| `context/skills/derive-spec.md` | Confidence Model Promotion DoD points at the template |
| `context/README.md` | Template Index description (+ promotion DoD) |
| `artefacts/build/tasks-spec-agent.md` | T-018 → completed + amendment log |

## Validation

- `uv run pytest context/scripts/tests/test_spec_indexer.py -q` → 22 passed
  (schema tests still green after derive-spec/requirements-elicitation edits)
- Full scripts suite → **256 passed, 2 skipped, 0 failed** — the two
  pre-existing adapter-drift failures (`test_adapter_drift_clean_repo`,
  `test_drift_validator_callable`) are now GREEN: regenerating the (gitignored)
  adapter projections `.cline/` / `.agents/` / AGENTS.md synced them to the
  current context sources (no tracked diff; the files are not versioned).

## Next Tasks

| ID | Task | Priority | Depends On | Status |
|----|------|----------|------------|--------|
| T-019 | Pilot B: derive-spec on foreign/unorganised repo | critical | T-008 ✅ | pending |
| T-020 | `verify --require-coverage` | low | T-010 ✅ | pending |
| T-021 | Indexer `comments` extraction | high | T-015 ✅ | pending |

## Key Decisions

- Template is the single definition; derive-spec skill and T-005 records keep
  one-line summaries and point at it (DRY), rather than duplicating the DoD.
- DoD is itemised and per-doc: one category may promote while another stays in
  draft; overrides must be recorded (ID + reason) in the review record.
- **Human review (CHANGES REQUIRED)**: durable docs must survive without the
  tasks doc, so task-ID provenance was stripped from every doc except
  `tasks-spec-agent.md` (and this HANDOFF): template, derive-spec /
  requirements-elicitation skills, product-owner / solution-architect agents,
  `derive-spec.yaml`, and `drift-candidates.md` now say "Confirmation
  mode" / "Promotion DoD" without task tags. The generated projections were
  regenerated via `generate_adapters.py --all` so no stale T-018 text remains in
  the (gitignored) `.cline/` / `.agents/` copies either.
- Scope: template + consumer skills/agents + workflow yaml + README + trackers
  — H1 AMBER, one logical unit, small task, technical-authoring skill applied.

<!-- state: ready for commit -->
