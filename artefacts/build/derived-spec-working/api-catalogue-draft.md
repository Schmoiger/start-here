# API Catalogue: Agentic Orchestration Harness (Derived)

Mode: technical (mode=both run)
Target: . (repo root)
Index provenance: repo-index.json (2026-11-05T13:24:38Z; extractors: stdlib.ast, ast-grep)
Baseline docs: artefacts/architecture/api-catalogue.md, artefacts/api/api-design-guide.md
Output location: artefacts/build/derived/api-catalogue.md

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

## Routes

**Confidence**: Assumed · 20% · Evidence: artefacts/build/repo-index.json:api (0 routes extracted)

This is a catalogue, not a contract: the canonical openapi.yaml is never rewritten.

No HTTP routes were extracted from the repository (index api=0). The harness is a Python CLI / library framework; it exposes no HTTP surface. Any API catalogue content would be Assumed (<50%) and must not be presented as Verified.

| Method | Path | Handler (path:line) | Auth / Guard | Consumed By | Confidence |
|--------|------|---------------------|--------------|-------------|------------|
| — | — | — | — | — | — |

---

## Request and Response Shapes

**Confidence**: Assumed · 20% · Evidence: artefacts/build/repo-index.json:api (0 routes extracted)

Only where schema or handler code evidences the shape; cite the source. Unknown shapes go to the appendix, not to guesswork.

No request/response shapes are evidenced. The harness is a CLI/library with no HTTP surface.

---

## Open-Questions Appendix

| ID | Subsection | Priority | Question | Options | Status |
|----|------------|----------|----------|---------|--------|
| Q-020 | Routes | blocking | Does the harness expose any HTTP routes, or is it CLI/library-only? | 1. CLI/library-only · 2. Has HTTP routes (not yet indexed) · Other | **APPROVED** |
| Q-021 | Request and Response Shapes | high | If no HTTP surface, should this subsection be removed entirely? | 1. Remove · 2. Keep as Assumed with open question · Other | still-open |

---

## Verification and Review Record

| Check | Result | Date |
|-------|--------|------|
| verify --index (citations resolve) | pending | 2026-11-05 |
| verify --doc (final drafts) | pending | 2026-11-05 |
| Human review gate | pending | 2026-11-05 |