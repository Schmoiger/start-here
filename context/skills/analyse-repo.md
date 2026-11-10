---
name: analyse-repo
description: Procedural guidance for analysing a repository with the deterministic spec-indexer tools (scan/verify) before agent synthesis — index schema, backend degradation, evidence citation, confidence bands, and the repo-profile deliverable.
globs: ["**/repo-index.json", "**/spec-scan.md", "**/repo-profile.md", "**/*.py", "**/*.ts"]
---

# Analyse-Repo Skill

**Applies to**: derive-spec phases 1/3 (indexing) and 6/8 (verification) — any task that must ground a specification in an existing codebase.

---

## Overview

`context/scripts/code-specs/spec_indexer.py` is a deterministic, zero-LLM
indexer. It turns a repository into `repo-index.json` (structured index) and
`spec-scan.md` (compact evidence map) — plus the agent-authored `repo-profile.md`
(Phase 1 deliverable). Agents then synthesise specifications from the index;
they do not re-read the repository from scratch.

**Agents must invoke the tools rather than reading the repository directly.**
Run every command below through the indexer; do not duplicate its extraction by
hand-reading source files. Read the index and the cited line ranges only
(§9 token rationale).

---

## 1. Scan — Build the Index (Phases 1 & 3)

### 1.1 Invocation

```bash
uv run context/scripts/code-specs/spec_indexer.py scan \
  --repo <repo-root> \
  --mode product|technical|both \
  [--out <repo-index.json path>] \
  [--max-files N] \
  [--extractors auto|stdlib|ctags|tree-sitter|ast-grep|ts-morph]
```

| Flag | Meaning |
|------|---------|
| `--repo` | Repo root to index (default: cwd). Scope a monorepo/service by passing `<service-root>` — one scan per repo. |
| `--mode` | derive-spec mode hint recorded in the index: `product`, `technical`, or `both` (default). Shared phases read it from `meta.mode`. |
| `--out` | Output path for `repo-index.json` (default `<repo>/artefacts/build/derived-spec-working/repo-index.json` when `artefacts/build/derived-spec-working` exists, else repo root). `spec-scan.md` is written beside it. |
| `--max-files` | Scan-size bound (default 2000); `meta.scan_too_large` is set when the bound is hit. |
| `--history` | Bounded git-history evidence into `meta.history` (T-017): last N commit subjects + rename/refactor clues from `git log --name-status` (default 200; `0` disables the pull; key absent with no git metadata, §3.5). |
| `--extractors` | Extraction backend (§6). Default `auto` probes the toolchain and prefers the richest backend per language; `stdlib` is the zero-dependency fallback tier. |

### 1.2 Phase 1 — full-repo discovery scan

```bash
uv run context/scripts/code-specs/spec_indexer.py scan --repo . --mode both
# → artefacts/build/derived-spec-working/repo-index.json   (structured index)
# → artefacts/build/derived-spec-working/spec-scan.md      (human/agent-readable evidence map)
# → artefacts/build/derived-spec-working/repo-profile.md   (agent synthesis: app type, entry points, module boundaries)
```

Phase 1 also discovers existing spec documents (`docs` key) via the document
globs — requirements / architecture / API / design docs — and collects the test
inventory, the capped git-history evidence (`meta.history`, §3.5): last N
commit subjects + rename/refactor clues as cheap feature descriptions,
especially for unorganised repos, and the comment/docstring evidence
(`comments`, §3.6): author-intent "why" notes, doc-comments, and
magic-number explanations.

### 1.3 Phase 3 — evidence pass

Rerun the scan for dense evidence (symbols · routes · UI · schema · tests)
after the Phase 1 profile exists:

```bash
uv run context/scripts/code-specs/spec_indexer.py scan --repo . --mode both
```

To force the richest TS/TSX backend, include it in the run (§6.3):

```bash
uv run --with tree-sitter --with tree-sitter-language-pack python context/scripts/code-specs/spec_indexer.py scan --repo . --mode both --extractors tree-sitter
```

Respect scope limits to bound token burn: target `--max-files`, read the index
first, and plan only the few targeted line-range reads Phase 3 needs.

### 1.4 Outputs

- `repo-index.json` — deterministic JSON index (§3).
- `spec-scan.md` — rendered summary of docs, symbols, API, schema, UI, tests (§4).
- `repo-profile.md` — the agent-authored Phase 1 deliverable (§5); the indexer does not write it.

---

## 2. Verify — Citation Resolution & Coverage Gate (Phases 6 & 8)

`verify` checks that every cited `file:line` still resolves in the working tree.

```bash
# Phase 6 — every citation in the index resolves
uv run context/scripts/code-specs/spec_indexer.py verify --index artefacts/build/derived-spec-working/repo-index.json

# Phase 8 — every file:line cited by a final draft resolves
uv run context/scripts/code-specs/spec_indexer.py verify --doc artefacts/product/derived/product-spec.md

# Phase 6 — deterministic coverage gate: every content subsection carries tier · NN% · file:line
uv run context/scripts/code-specs/spec_indexer.py verify --doc artefacts/build/derived-spec-working/product-spec-draft.md --require-coverage
```

`--doc` accepts any markdown file whose `path.ext:line` citations should be
validated (`.md` citations included). `--repo` overrides the root (default:
`meta.repo_abs` from the index, else cwd). Exit 0 = all citations resolve
(`OK — all citations resolve`); non-zero lists failures. Lines ≤ 0 (e.g.
OpenAPI entries without line info) are skipped, not failed.

### 2.1 `--require-coverage` — Phase 6 coverage gate

`verify --doc --require-coverage` parses the derived-spec confidence schema
(`context/templates/derived-spec-template.md` § Confidence Schema) so the
Phase 6 "question coverage" check is deterministic rather than
agent-discretionary:

- Content subsections are `##`/`###`/`####` headings that are neither
  structural sections (Confidence Schema, Subsection Format,
  Open-Questions Appendix, Drift, Verification and Review Record) nor
  `{placeholder}` headings.
- Every content subsection must contain a `**Confidence**:` line carrying:
  tier (`Verified` · `Needs Confirmation` · `Assumed`), a banded percentage
  (`NN%`, consistent with the band), and at least one `file:line` citation
  (`path.ext:NN`, `.md` included). Band/% consistency uses the fixed bands
  (Verified 85–100 · Needs Confirmation 50–85 · Assumed <50), with 85 accepted
  for both Verified and Needs Confirmation.
- Missing tier / percentage / citation, or a band mismatch, is listed per
  subsection and exits non-zero (`COVERAGE FAIL`). Structural headings and
  template placeholders are skipped. Running plain `verify --doc` leaves the
  gate off.

---

## 3. Consuming `repo-index.json`

### 3.1 Schema

| Key | Contents |
|-----|----------|
| `meta` | repo, absolute root (`repo_abs`), UTC `generated_at`, mode, file/language counts, LOC, `scan_too_large` flag, `confidence` tier, `extractors` provenance |
| `warnings` | scan-level warnings (size threshold, collection method, backend fallbacks) |
| `docs` | existing spec documents: `[ {path, kind} ]` — `requirements │ architecture │ api │ design │ docs │ discovery │ prd │ tsd │ spec │ readme │ openapi` |
| `files` | per file: path, language, line count, `symbols` (kind, name, signature, line, decorators, props), imports, and the per-file `extractor` backend |
| `api` | `[ {method, path, handler, file, line} ]` from route decorators (FastAPI/Flask) and OpenAPI documents |
| `schema` | `[ {table, columns, file, line} ]` from SQL migrations plus OpenAPI schema names |
| `ui` | `[ {component, file, line, props, usages, kind} ]` from TS/JSX component definitions, aggregated with JSX-tag usage counts |
| `tests` | `[ {node_id, file} ]` from pytest collection / jest listTests — each test name is a candidate feature name |
| `config` | user-facing constraints (T-016): `[ {key, source, line, value_hint, feature} ]` from `.env.example`/`.env.template` env files, `settings.py`/`config.*` modules, and config YAML/JSON — secret-looking keys redacted to `<redacted>`; `feature` marks flags/toggles (ENABLE_*/FEATURE_* or boolean); test/fixture paths excluded; feeds product-spec + TSD constraints |
| `meta.history` | capped git evidence (T-017): `{count, capped, commit_subjects, renames}` from `git log --name-status` — newest-first commit subjects + rename/refactor clues (`{commit, subject, old, new}`); **absent** (never empty) when the repo has no git metadata / no commits, or with `--history 0` (§3.5) |
| `comments` | author-intent evidence (T-021): `[ {file, line, kind, text, attached} ]` — Python `#` via stdlib `tokenize` (comments inside strings never leak) + docstrings via `ast.get_docstring`; TS/JS JSDoc `/** */` + `//`; SQL `--` / `/* */` (strings masked). `kind` ∈ `docstring │ leading │ inline │ block`; `attached` points at an owning symbol/table `{kind, name, line}` or is absent for orphans (TODOs, licence headers, magic-number notes). Symbols carry `docstring` + `comments` too — read them before any source read (§3.6) |

### 3.2 `meta.extractors` provenance

`meta.extractors` records, per backend tool (`ctags`, `tree-sitter`, `ast-grep`,
`ts-morph`, `stdlib`): `available` (probed on this machine), `used` (whether the
plan selected it for any language), and `reason`. `meta.confidence` is a
machine-level tier: `full` (no backend degraded), `regex` (TS/JS fell back to
stdlib regex), `degraded` (some languages have no extractor at all — e.g. a
foreign language without ctags). Probe failures are never fatal in auto mode: an
unavailable candidate is simply skipped and the reason is recorded.

### 3.3 Per-file `extractor`

Each `files[]` record carries an `extractor` field naming the backend that
parsed that file (`stdlib.ast`, `stdlib.regex`, `stdlib.sql`, `ctags`,
`tree-sitter`, `ast-grep`, `ts-morph`). When a symbol record looks thin, check
the file's `extractor` before concluding the code lacks structure — it may
indicate a degraded backend rather than absence of the construct.

### 3.4 Planned keys

None — `config` (§3.1), `meta.history` (§3.5), and `comments` (§3.6) are all
implemented. Treat an absent key as absent evidence, never as an empty list.

### 3.5 `meta.history` — capped git-history evidence (T-017)

`meta.history` carries zero-LLM git evidence captured by `scan`:

- `commit_subjects` — the last N commit subjects, newest first (N = `--history`,
  default 200). These are cheap **feature descriptions**: a commit subject often
  states the feature intent that code alone hides — precisely the signal
  sparse/unorganised repos lack.
- `renames` — `{commit, subject, old, new}` rename/refactor clues from
  `git log --name-status` (capped at 500). Batch moves such as
  `refactor: move X to Y` reveal module boundaries the tree alone does not
  expose.
- `count` / `capped` — how many subjects were captured and whether the repo has
  more commits than the bound (`capped: true`).

The key is **absent**, not empty, when the repo has no git metadata, when `git
log` has no commits to emit, or when `--history 0` disables the pull (a scan
warning notes the absence). `verify --index` does not cite history entries —
commits are evidence of intent, not `file:line` citations.

### 3.6 `comments` & docstrings — consumption

`scan` extracts author-intent evidence into the top-level `comments` stream
**and** onto symbols themselves (all zero-LLM, exact `file:line`):

- `symbols[].docstring` — the doc-comment / `ast.get_docstring` text for that
  definition: a Python docstring, TS JSDoc `/** */`, or a contiguous `#` / `//`
  block immediately above it.
- `symbols[].comments` — attached units `{text, line, kind}`: `docstring`,
  `leading` (doc-comment block above a definition), `inline` (comment on a line
  inside the definition's span or trailing), `block` (multi-line `/* */`).
- top-level `comments` — every comment: `{file, line, kind, text, attached}`.
  `attached = {kind, name, line}` for symbol-owned comments (SQL comments attach
  to the nearest table/column); orphans — `attached` absent — are TODOs,
  licence headers, magic-number explanations, and module docstrings.

Consumption rules:

- **Read the index text first**; only read the exact cited range when the index
  text is insufficient (agent-sandbox tool policy).
- Python `#` capture is exact via stdlib `tokenize`: a `#` inside a string
  literal is a string, never a comment. TS/JS and SQL scan string-masked source.
- Feeds: business intent + domain rules → product spec; magic numbers / limits
  (e.g. "retry budget", "provider limit") → TSD constraints; JSDoc semantics →
  api-catalogue draft; deprecation / TODO comments → drift candidates + open
  questions.
- A claim backed by a comment rather than code may reach *Needs Confirmation* —
  comments state intent, not implementation; confirm before Verified.

---

## 4. Consuming `spec-scan.md`

`spec-scan.md` is the human/agent-readable rendering of the same index: scan
warnings, existing spec documents, a repository map of symbols by file, API
surface, data model, UI components, and test inventory. Use it for quick
orientation and as the cross-reference skeleton; cite from `repo-index.json`
(which carries exact `file:line`) in draft specs rather than from the rendered
summary.

---

## 5. Writing `repo-profile.md` (Phase 1 deliverable)

The indexer does not write `repo-profile.md`; the agent authors it in
`artefacts/build/` beside the scan outputs. It must record, from the index:

- **App type** — what the repo is (web app, API service, CLI, library, harness,
  …), grounded in the strongest evidence: entry points, route inventory, UI
  components, doc classification.
- **Entry points** — CLI mains, server/bootstrap modules, route registrations,
  worker scripts, each with `file:line` citations.
- **Module boundaries** — the coarse module/package split and what each side
  owns, again with citations.
- **Feature history** — where `meta.history` (§3.5) exists, mine the newest
  commit subjects and renames for feature intent and refactor clues; cite
  `meta.history` entries as cheap descriptions when the tree offers none.

Every claim carries `file:line` evidence (§7). The profile is the seed the
Phase 2–4 synthesis steps build on; an uncitable claim is an open question, not
an assertion.

---

## 6. Extraction Backends & Degradation (T-015)

### 6.1 `--extractors` choices

| Choice | Coverage | Notes |
|--------|----------|-------|
| `auto` (default) | per-language best available | probes the toolchain; provenance recorded in `meta.extractors` |
| `stdlib` | python, TS/JS, SQL | zero-dependency fallback tier: stdlib `ast` + TS/JS regex heuristics + SQL `CREATE TABLE` parser; parity baseline |
| `ctags` | python, TS/JS, Go, Rust, Java, C, C++, Ruby, PHP, Swift | universal-ctags JSON (primary for languages without a dedicated parser) |
| `tree-sitter` | TS/JS (`tsx`/`typescript`/`javascript`) | richest TS/TSX walker: multiline destructured props, JSX usage counts, decorators, named imports |
| `ast-grep` | TS/JS | rule patterns via the `ast-grep` binary (`sg` is deprecated as of 0.51); JSX usage via line scan |
| `ts-morph` | TS/JS | Node helper `ts_extract.mjs`; skipped quietly when node or ts-morph is absent |

SQL uses `stdlib.sql`; OpenAPI documents are parsed with PyYAML; tests are
collected via `pytest --collect-only` / `yarn test --listTests` — all zero-LLM.

### 6.2 Auto-mode ladder

- Python → `stdlib.ast` (richest — imports, classes, functions, decorators,
  route registrations, constants).
- TS/JS → `tree-sitter` when importable, else `ast-grep`, else `ts-morph`, else
  `stdlib.regex`.
- Foreign languages → `ctags` when available, else `none` (symbols not
  extracted; counts still recorded).
- SQL → `stdlib.sql` (`CREATE TABLE` parsing from migrations).

### 6.3 Degradation semantics

- Auto mode never fails on a missing backend — it falls back and records the
  reason in `meta.extractors` / `meta.confidence` (§3.2).
- Forcing an unavailable backend is an error: the scan exits non-zero
  (`error: selected extractor 'X' is not available on this machine`).
- **Exception**: forcing `ts-morph` when node/ts-morph is absent degrades
  quietly to `stdlib` with a warning.
- Languages outside a forced backend's coverage fall back to `stdlib` (or
  `none` for foreign languages) rather than failing.
- To get the tree-sitter backend under uv, use `uv run --with tree-sitter
  --with tree-sitter-language-pack …` (§1.3).

---

## 7. Evidence Citation Discipline & Confidence Bands

- Every claim in a derived spec cites `file:line` (e.g.
  `context/scripts/code-specs/spec_indexer.py:1697`);
  `verify --doc` (§2) is the gate that every citation resolves after edits.
- Confidence bands per claim:
  - **Verified 85–100** — directly evidenced by the cited code/doc lines.
  - **Needs Confirmation 50–85** — plausible from evidence but requires human
    confirmation (ask drift items first).
  - **Assumed <50** — reasonable inference; unanswered questions stay Assumed
    and remain in the open-questions appendix.
- Confirmed answers raise the band/percentage. Do not present an under-cited
  claim as Verified just because the code "probably" does it.

---

## 8. Re-scan Rule

The index is a snapshot of the tree at scan time. Refresh it before `verify`
after any edit:

1. Re-run `scan` (§1) after changing code or documents.
2. Then run `verify --index` (§2) — if the previous citations no longer
   resolve, the tree changed: re-cite against the refreshed index, then
   re-verify.

The index is deterministic: re-running `scan` on the same tree is idempotent
(modulo `meta.generated_at`), and `verify` fails any citation that no longer
resolves after edits — never hand-edit the index to silence it.

---

## 9. Token Rationale

Extraction is zero-LLM: the indexer does the reading, so synthesis tokens go to
judgement, not scanning. The agent reads only the index, `spec-scan.md`, and a
small set of targeted line ranges cited from the index (§1.4). Scope reads with
`--max-files`; for large repos read the index first and target file reads to
the lines the synthesis actually needs.