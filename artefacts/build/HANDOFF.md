# Handoff: T-017 — Indexer `meta.history` (capped git-history evidence)

**From**: @orchestrator (default agent, small-task workflow)
**To**: @human-operator
**Date**: 2026-09-11
**Workflow**: small-task
**Phase**: hitl
**Status**: awaiting human APPROVED for commit

---

## Summary

T-017 (Indexer: capped git-history evidence into `meta.history`) is
**implemented, tested, and validated** against its acceptance criteria:

- `scan` records `meta.history`: `{count, capped, commit_subjects, renames}` —
  last N commit subjects (newest first) + rename/refactor clues from
  `git log --name-status` — zero LLM, deterministic.
- `--history N` bounds the pull (default 200); `--history 0` disables it. The
  key is **absent** (never empty) when the repo has no git metadata or no
  commits; a scan warning notes the absence.
- `spec-scan.md` gains a `## Recent Git History (evidence)` section.
- Documented in the `analyse-repo` skill (§1.1 flag row, §3.1 schema row, §3.4
  planned-keys cleanup, new §3.5 consumption guidance, §5 repo-profile bullet)
  and the workflows README `Commands & Repository Index` list.
- Reference outputs regenerated (`derived-spec-working/repo-index.json` +
  `spec-scan.md` — history=200, renames=16) and `verify --index` green.

## Changes

| File | Change |
|------|--------|
| `context/scripts/code-specs/spec_indexer.py` | `collect_history()`, `--history` CLI flag, `meta.history` emission, spec-scan history section, module docstring |
| `context/scripts/tests/test_spec_indexer_history.py` | **new** — 13 tests (synthetic git repos) |
| `context/skills/analyse-repo.md` | schema row, flag doc, §3.4 planned keys, new §3.5, §5 bullet |
| `context/workflows/README.md` | `--history` in the command list |
| `artefacts/build/derived-spec-working/repo-index.json`, `spec-scan.md` | regenerated reference output |
| `artefacts/build/tasks-spec-agent.md` | T-017 → completed + amendment log |

## Validation

- `uv run pytest context/scripts/tests/test_spec_indexer_history.py -v` → **13 passed**
- Full scripts suite → **254 passed, 2 skipped**. The 2 failures
  (`test_adapter_drift_clean_repo`, `test_packaging.py::test_drift_validator_callable`)
  were reproduced on the clean committed tree via `git stash` — **pre-existing**
  (known backlog gap T-007 "Regenerate adapters / validators green", status:
  won't do), not caused by T-017.
- `uv run --with ruff ruff check` on changed Python → clean
- `verify --index artefacts/build/derived-spec-working/repo-index.json` →
  `OK — all citations resolve` (769 citations)

## Next Tasks

| ID | Task | Priority | Depends On | Status |
|----|------|----------|------------|--------|
| T-018 | Confidence bands + promotion DoD in derived-spec-template | high | T-006 ✅ | pending |
| T-019 | Pilot B: derive-spec on foreign/unorganised repo | critical | T-008 ✅ | pending |
| T-020 | `verify --require-coverage` | low | T-010 ✅ | pending |
| T-021 | Indexer `comments` extraction | high | T-015 ✅ | pending |

## Key Decisions

- **Schema shape**: `meta.history = {count, capped, commit_subjects, renames}`;
  renames capped at 500; `git rev-list --count HEAD` determines `capped`.
- **Absent-not-empty contract**: no git metadata / no commits / `--history 0` →
  key omitted from `meta` plus a scan warning; agents treat it as absent
  evidence, never empty.
- **Fitness (small-task)**: H1 AMBER (6 files) — human chose small-task for this
  single unit at intake; one coherent logical unit (H8 clear); R1/R5/R6/R7 lean
  small-task; python-scripting skill loaded.

<!-- state: ready for commit -->
