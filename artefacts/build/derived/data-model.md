# Data Model: Agentic Orchestration Harness (Derived)

Mode: technical (mode=both run)
Target: . (repo root)
Index provenance: repo-index.json (2026-11-05T13:24:38Z; extractors: stdlib.ast, ast-grep)
Baseline docs: artefacts/architecture/data-model.md
Output location: artefacts/build/derived/data-model.md

---

## Confidence Schema

| Band | % | Evidence required to claim it |
|------|---|-------------------------------|
| Verified | 85-100 | directly cited code or doc lines (path:line); usage counts or call chains where material; no blocking open question |
| Needs Confirmation | 50-85 | plausible from evidence but requires human confirmation; drift candidates land here first |
| Assumed | <50 | reasonable inference only; stays Assumed until a human answer confirms it |

Update rule: a confirmed answer raises the band and percentage and records the confirming citation; an unanswered question keeps the subsection Assumed and its question stays in the Open-Questions appendix as still-open.

Promotion DoD: a draft is promotable when no subsection sits below Needs Confirmation and no blocking question is still open, or when the human records an explicit override.

---

## Subsection Format

### {Subsection title}

Confidence: {Band} · {NN}% · Evidence: path:line, path:line

{Content.}

---

## Tables and Collections

**Confidence**: Assumed · 20% · Evidence: artefacts/build/derived-spec-working/repo-index.json:7467 (0 tables extracted)

No SQL tables or collections were extracted from this repository (index schema=0). The harness is a Python CLI/library repo; there is no database layer.

| Table / Collection | Purpose (observed) | Confidence | Evidence |
|--------------------|--------------------|------------|----------|
| — | — | — | — |

---

## Columns and Constraints

**Confidence**: Assumed · 20% · Evidence: artefacts/build/derived-spec-working/repo-index.json:7467 (0 tables extracted)

Per table: columns, types, keys, unique/not-null/check constraints. Each constraint cites its origin: migration, model, or index row.

No tables exist, so no columns or constraints.

---

## Relationships

**Confidence**: Assumed · 20% · Evidence: artefacts/build/derived-spec-working/repo-index.json:7467 (0 tables extracted)

Foreign keys and join paths observed in schema and code; cite both sides.

No tables exist, so no relationships.

---

## Open-Questions Appendix

| ID | Subsection | Priority | Question | Options | Status |
|----|------------|----------|----------|---------|--------|
| Q-022 | Tables and Collections | blocking | Does this repo have any data tables or collections? | 1. No tables/collections (CLI/library only) · 2. Has data tables (not indexed) · Other | **APPROVED** |
| Q-023 | Columns and Constraints | high | If no tables, should this subsection be removed? | 1. Remove · 2. Keep as Assumed with open question · Other | still-open |

---

## Verification and Review Record

| Check | Result | Date |
|-------|--------|------|
| verify --index (citations resolve) | pending | 2026-11-05 |
| verify --doc (final drafts) | pending | 2026-11-05 |
| Human review gate | pending | 2026-11-05 |