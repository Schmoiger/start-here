# Drift Candidates: Existing Docs vs Derived Behaviour

**Generated**: 2026-11-05T13:30:00Z (Phase 2)  
**Index**: `repo-index.json` (mode: both, 61 files, 731 symbols)  
**Scan Backend**: stdlib.ast + ast-grep rules  

---

## Drift: Requirements — Example vs Reality

| ID | Doc Path | Kind | Drift Description | Question Raised |
|----|----------|------|-------------------|-----------------|
| D-001 | `artefacts/product/requirements.md` | requirements | Document is explicitly marked as an **example** to be replaced: *"THIS SECTION IS POPULATED AS AN EXAMPLE. THESE ARE THE PRODUCT REQUIREMENTS FOR THE AGENTIC HARNESS AND SHOULD BE REPLACED BY THE PRODUCT REQUIREMENTS FOR YOUR PROJECT."* — code (spec_indexer.py) documents the actual framework requirements extracted from code, but the existing doc is a template placeholder, not derived from the harness's own code-enforced REQ-*. | Should the derived product spec replace this with code-extracted requirements, or keep it as a user-overridable template? |
| D-002 | `artefacts/architecture/architecture.md` | architecture | Document is explicitly marked as an **example** to be replaced: *"THIS SECTION IS POPULATED AS AN EXAMPLE. THIS IS THE ARCHITECTURE FOR THE AGENTIC HARNESS AND SHOULD BE REPLACED BY THE ARCHITECTURE DEFINITION FOR YOUR PROJECT."* — code describes the actual architecture but the existing doc is a placeholder. | Same question: replace with code-extracted architecture, or keep template? |

---

## Drift: Architecture — Example vs Reality

| ID | Doc Path | Kind | Drift Description | Question Raised |
|----|----------|------|-------------------|-----------------|
| D-003 | `artefacts/architecture/architecture.md` | architecture | Document header states it *"should be replaced by the architecture definition for your project."* — The code index shows 34 agents, 11 workflow YAMLs, 5 test suites, and a structured context/ rules/ standards/ workflows/ templates/ persona/ hierarchy — but the existing doc is a meta-description, not a self-description of this specific repo's architecture. | Does the derive-spec process auto-generate an architecture.md from the index, or does it remain a human-maintained document? |
| D-004 | `artefacts/architecture/data-model.md` | data-model | No explicit example marker, but contains framework-level data-model descriptions. Index extraction shows no SQL tables (api=0, sql not in language coverage for this repo), so data-model claims would be Assumed (<50%). | Are there zero data tables in this repo? If so, the data-model subsection should be Assumed with an open question. |

---

## Drift: Design Assets

| ID | Doc Path | Kind | Drift Description | Question Raised |
|----|----------|------|-------------------|-----------------|
| D-005 | `artefacts/design/design-tokens.json` | design | Design tokens file exists. Index found no JSX/TSX extraction (tree-sitter unavailable), so UI component claims would be Assumed. | Can we confidently claim UI component inventory from Python-only extraction? |
| D-006 | `artefacts/design/user-flows.md` | design | User-flows doc exists. Index found 245 pytest-collected tests but no UI route extraction (api=0). | Are user-flows documented solely from test node‑ids, or is there actual UI mapping? |

---

## Drift: API Contract

| ID | Doc Path | Kind | Drift Description | Question Raised |
|----|----------|------|-------------------|-----------------|
| D-007 | `artefacts/architecture/api-catalogue.md` | api-catalogue | No HTTP routes extracted (api=0 in index — Python harness repo, no FastAPI/Flask routes). Claims about API routes would be Assumed (<50%). | Should this subsection be marked Assumed with an open question, or removed entirely? |
| D-008 | `artefacts/api/api-design-guide.md` | api-design-guide | Exists but not populated with code-extracted routes. | Same question as D-007. |

---

## Drift: Open Questions Appendix (Phase 7 format)

Pending confirmation round — each of the above items (D-001 through D-008) will become a numbered multiple-choice question in Phase 7 (batched human confirmation). Format follows `context/skills/derive-spec.md §Confidence Model` and `context/templates/derived-spec-template.md §Open-Questions Appendix`.

---

## Confidence Band Pre-population

Each drift subsection above will carry a confidence band at promotion:
- **Assumed** (<50%) — current state for most claims (no code evidence beyond doc existence)
- **Needs Confirmation** (50–85%) — once human confirms whether examples should be replaced or preserved
- **Verified** (85–100%) — only if code citation directly supports the claim (currently none)

**Promotion DoD (per doc)**: no subsection below Needs Confirmation and no blocking still-open questions — or a recorded human override.