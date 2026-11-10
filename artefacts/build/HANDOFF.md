# Handoff: T-021 — indexer `comments` key (comment/docstring extraction)

**From**: @orchestrator (default agent, small-task workflow)
**To**: @human-operator
**Date**: 2026-10-11
**Workflow**: small-task
**Phase**: hitl (complete — awaiting human APPROVED)
**Status**: implemented + validated; not yet committed (human gate)

---

## Summary

`spec_indexer.py` now extracts comment/docstring **intent evidence** into a
top-level `comments` key, attached to symbols (`symbols[].docstring` +
`symbols[].comments`), consumed via the analyse-repo skill:

- **Python**: `#` comments via stdlib `tokenize` (COMMENT tokens are exact —
  `#` inside a string literal is a string, never a comment; trailing comments
  never join doc-blocks) + docstrings via `ast.get_docstring` on
  module/class/function/method nodes.
- **TS/JS**: JSDoc `/** */` + `//` on string-masked source (regex v1).
- **SQL**: `--` and `/* */`; attached to the nearest table/column from the
  `CREATE TABLE` parser (`ColumnDef` now records `line`).
- **Attachment**: doc-comment blocks ≤3 lines above a definition (`leading`,
  fills `symbol.docstring`), line-range overlap / trailing (`inline`); orphan
  comments (TODOs, licence headers, magic-number notes, module docstrings)
  stay in the stream with `attached: null`.
- **Schema**: `{file, line, kind: docstring│leading│inline│block, text,
  attached: {kind, name, line}|null}`; deterministic (sorted, soft-capped at
  2000 with a scan warning); `verify --index` covers the new citations;
  `spec-scan.md` shows a `## Comments & Docstrings (intent evidence)` map.
- `Symbol` gains `end_line` (populated by Python ast, tree-sitter, ast-grep)
  so inline span attachment is exact.

## Changes

| File | Change |
|------|--------|
| `context/scripts/code-specs/spec_indexer.py` | `CommentEntry` dataclass; `Symbol.end_line/docstring/comments`; `ColumnDef.line`; `collect_comments()` + per-language extractors (`_python_comments` via tokenize, `_ts_comments`, `_sql_comments`, masked-string helper); leading/inline/SQL attachment; `comments` key in the index; spec-scan section; `verify` comment citations; module docstring bullet |
| `context/scripts/tests/test_spec_indexer_comments.py` | **22 new tests** (tokenize string-safety, leading/inline/orphan attachment, docstrings, JSDoc, SQL table/column attach, determinism, render, verify, CLI, real-repo) |
| `context/skills/analyse-repo.md` | §1.2 (comments collected), §3.1 (`comments` schema row), §3.4 (planned keys → none), new §3.6 consumption guidance |
| `context/workflows/README.md` | Phase 3 tools row + schema list mention `comments` |
| `artefacts/build/derived-spec-working/repo-index.json` + `spec-scan.md` | regenerated (history=200; **comments=866**; `verify --index` green on **1709 citations**) |
| `artefacts/build/derived-spec-working/product-spec-draft.md` + `artefacts/build/derived/product-spec.md` | stale `spec_indexer.py` citations re-pointed to real lines (`:7` module docstring, `:495` analyze_python, `:2840` main CLI); pre-existing blank-line `derive-spec.yaml:187` citation → `:188` (was already broken before this task) |
| `artefacts/build/tasks-spec-agent.md` | T-021 → completed + amendment log entry |

## Validation

- `uv run pytest context/scripts/tests/test_spec_indexer_comments.py -q` →
  **22 passed**
- Full scripts suite → **287 passed, 2 skipped, 3 failed** — all 3 failures
  are pre-existing and unrelated to this change (verified via `git stash`):
  2 e2e compilation tests drift from the recent `agents-md.yaml` harness
  commit `a5f927d`, 1 workflow-schema glob that treats `agents-md.yaml` as a
  workflow.
- `verify --index` on the regenerated index → exit 0 (1709 citations, incl. 866
  comment rows).
- All 4 drafts + 4 promoted derived docs → `verify --doc --require-coverage`
  green (repo-profile/spec-scan are Phase-1/generated artefacts, not
  coverage-gated).
- `uv run --with ruff ruff check` → clean; `tech_writing` spelling + EARS →
  clean; `adapter_drift.py` → projections in sync (regenerated after the skill
  edit).

## Next Tasks

| ID | Task | Priority | Depends On | Status |
|----|------|----------|------------|--------|
| T-019 | Pilot B: derive-spec on foreign/unorganised repo | critical | T-008 ✅ | pending |

## Key Decisions

- Kind vocabulary extends the acceptance enum with `docstring` (Python
  `ast.get_docstring` entries + TS JSDoc), so docstrings are searchable in the
  same stream; `leading`/`inline` are position-based; `block` is multi-line
  `/* */`.
- Trailing comments never join a doc-block, so `x = 3  # note` can't drag a
  standalone doc comment above into a merged block.
- Inline attachment needs symbol end lines — `Symbol.end_line` is additive
  (0 = backend unknown) so nothing breaks on `stdlib.regex`/ctags backends.
- The top-level stream is soft-capped at 2000 deterministic entries with a
  scan warning; symbol-level attachments are unaffected by the cap.

<!-- state: awaiting human APPROVED before commit -->