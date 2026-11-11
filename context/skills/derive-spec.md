---
name: derive-spec
description: "Procedural guidance for deriving product and/or technical specifications from an existing codebase (organised or not) via deterministic indexing and agent synthesis — modes: product, technical, both; discovery, evidence consumption, confidence model, batched confirmation, verification, and promotion to derived/."
globs: ["**/*.py", "**/*.ts", "**/*.tsx", "**/*.sql", "**/openapi*.yaml", "repo-index.json"]
---

# Derive-Spec Skill

**Applies to**: deriving product and/or technical specifications from a codebase — `context/workflows/derive-spec.yaml` (Phases 0–8). Loaded by `@product-owner` (modes `product` | `both`) and `@solution-architect` (modes `technical` | `both`).

---

## Overview

derive-spec turns any existing codebase — organised or not — into new product
and/or technical specifications. Extraction is deterministic and zero-LLM
(`spec_indexer.py`, driven through the **analyse-repo** skill); synthesis adds
confidence tiers, batched human confirmation, and a review gate before
promotion. The workflow never rewrites canonical docs.

The authoritative phase map is the workflows README `## derive-spec.yaml`
(Overview diagram, Runtime Sequence, action/tool table, notes for agents).
This skill is the agent-facing how-to; tool invocations and the
`repo-index.json` schema are documented in the **analyse-repo** skill (§1, §2,
§3) — do not duplicate either here.

---

## Modes

- `product` | `technical` | `both`, set at intake (workflow input) and recorded
  in `index.meta.mode` by `scan --mode`.
- Shared phases (0–3, 5–8) run **once**; derivation branches after evidence
  gathering: Phase 4a (product) and/or Phase 4b (technical). `both` runs 4a then
  4b, then shares draft → verify → confirm → finalise.
- Mode determines outputs (Q10 — separate docs per artefacts category):
  - `product` → `product-spec.md`
  - `technical` → `architecture.md` · `api-catalogue.md` · `data-model.md`
  - `both` → all four

---

## Phase 0 · Intake & Scope

Record at intake:

- **Mode** — `product` | `technical` | `both`.
- **Target** — repo root for the scan; for monorepos pass the service root:
  `--repo <service-root>` (Q11 · A3 — one run per repo/service, one HANDOFF per
  run; cross-repo questions go to the elicitation round).
- **Limits** — `--max-files` bound; large repos flagged by
  `meta.scan_too_large` → consult the human on scoping before spending tokens.
- **Output location** — per-run choice; drafts stage in
  `artefacts/build/derived-spec-working/`, approval promotes to `artefacts/derived/{category}/`.

---

## Phase 1 · Discovery & Repo Profile

1. **Run the scan** (analyse-repo §1) with the mode and scope:
   `scan --repo <target> --mode <mode>` → `repo-index.json` + `spec-scan.md`.
2. **Discover existing spec documents** by glob — candidates are confirmed by
   the human, never silent:
   `artefacts/product/**` · `artefacts/architecture/**` · `docs/**` ·
   `**/README.md` · `PRD*` · `*spec*.md` · `openapi*.yaml`
3. **Write `repo-profile.md`** (Phase 1 deliverable; analyse-repo §5) at
   `artefacts/build/derived-spec-working/repo-profile.md`: app type, entry points, and module
   boundaries ground-truth from the index. This is the orientation for
   **unorganised repositories** — when the repo has no docs or an unfamiliar
   layout, the profile replaces guesswork; every claim carries `file:line`.

---

## Phase 2 · Baseline & Drift

- Read the existing specs discovered in Phase 1 (small, targeted prose reads).
- Build the **drift candidate list**: existing-doc vs code deltas (doc says X,
  code does Y) — this list feeds Phase 7 questions, ordered first.
- No existing docs → run the empty-extraction path and annotate the output as
  "code-derived only" (no baseline to drift from).

---

## Phase 3 · Evidence Gathering

- Rerun the scan for dense evidence — symbols · routes · UI · schema · tests
  (analyse-repo §1.3).
- **Cross-index reasoning** over `repo-index.json`: consume `api`, `schema`,
  `ui`, `tests`, and per-file `symbols` without re-reading the repo.
- `tool_scope` is the index **plus the cited line ranges only** — targeted
  reads for the lines the synthesis actually needs (analyse-repo §9 token
  rationale). Never bulk-read the repository.

---

## Phase 4 · Derivation

### 4a · Product (modes `product` | `both`) — @product-owner

- **UI inventory → candidate features**: from `ui` (components, props, usage
  counts), `api` (routes a UI consumes), and `tests` (test node-ids are
  candidate feature names).
- **Roles/actors**: from auth/permission evidence (route guards, decorators,
  RBAC, role-scoped API paths), UI inventory (who interacts with what), and doc
  classification.
- **UX flows**: via call chains across backend symbols, named per actor.
- **Name the actor/role per UX flow** — never leave anonymous flows; each flow
  belongs to at least one named actor.
- **User-facing constraints**: from `config` (T-016) — env toggles, rate/limit
  hints, feature availability per config key → product-spec constraints +
  TSD constraints subsections.

### 4b · Technical (modes `technical` | `both`) — @solution-architect (drafts only)

- **Architecture**: module boundaries from `files`/`imports` and entry points,
  visible service/process shape, deployment-relevant seams.
- **API-catalogue draft**: from `api` routes + `schema` + UI consumption of the
  routes.
- **Data-model draft**: from `schema` (tables, columns) plus constraint hints in
  code; note every constraint's origin as a citation.
- **TSD constraints**: from `config` (T-016) — deployment/runtime toggles,
  timeouts, bounded resources, feature flags → TSD constraints subsections.

---

## Phase 5 · Draft with Confidence

- Every subsection carries **tier + banded % + `file:line` citations**
  (confidence model below).
- Render process, workflow, and sequence models as **Mermaid** diagrams:
  `doc-standards.md` §6.1 mandates Mermaid for all diagrams and the
  `mermaid-authoring` skill governs syntax/layout. A subsection that narrates
  steps inline ("1. … 2. … 3. …") instead of a `mermaid` block is a
  process-model defect (B-009) — flag it rather than ship prose.
- Append the **open-questions appendix** (per subsection, priority, MC options)
  and the **drift section** (canonical docs vs derived behaviour).
- Stage drafts in `artefacts/build/derived-spec-working/` — one file per artefacts
  category (`product-spec-draft.md` · `architecture-draft.md` · `api-catalogue-draft.md` ·
  `data-model-draft.md`).

### Confidence Model

| Band | % | Evidence required to claim it |
|------|---|-------------------------------|
| **Verified** | 85–100 | directly cited code/doc lines; usage counts / call chains where material; no blocking open question |
| **Needs Confirmation** | 50–85 | plausible from evidence but requires human confirmation (drift items first) |
| **Assumed** | <50 | reasonable inference only — stays Assumed until a human answer confirms |

- **Update rule**: confirmed answer → raise the band/% and record the
  confirming citation; unanswered question → stays Assumed and remains in the
  open-questions appendix as still-open.
- **Promotion DoD** (per doc; definition and checklist:
  `context/templates/derived-spec-template.md` § Confidence Schema): no
  subsection below Needs Confirmation and no blocking still-open questions —
  or a recorded human override.

---

## Phase 6 · Verification Pass

- Run `verify --index` (analyse-repo §2): every `file:line` citation in the
  index resolves. **Re-scan before verifying after any edit** (re-scan rule,
  analyse-repo §8).
- Check question coverage: every subsection carries tier + banded % +
  citations; unresolved or uncovered claims are fixed (or downgraded) here,
  never left as unannotated assertions.

---

## Phase 7 · Batched Human Confirmation

- **One batched round** of questions; ask **drift candidates first**
  (existing-doc vs code deltas), then pure code facts.
- Format (Q2 · reverse-spec.md Step 3): numbered multiple-choice with "Other",
  each option citing the files involved.
- Use the requirements-elicitation skill (confirmation mode, T-005) for the
  questioning discipline.
- "Skip questions" → record the stated assumption; unanswered → stays Assumed
  and remains in the open-questions appendix (still-open).

---

## Phase 8 · Finalise & Review Gate

1. Update drafts: resolve questions, raise confirmed bands/percentages, report
   the drift section.
2. Run `verify --doc` on the final drafts (analyse-repo §2) — all citations
   resolve.
3. Human review gate: **APPROVED** → promote drafts from
   `artefacts/build/derived-spec-working/` to `artefacts/derived/{category}/` and commit.
   **CHANGES REQUIRED** → return to the specified phase; canonical docs are
   never rewritten.

---

## Output Lifecycle

- Drafts: `artefacts/build/derived-spec-working/` (one file per category).
- Promotion: `artefacts/derived/{category}/` behind human APPROVED
  — e.g. `artefacts/product/derived/product-spec.md`.
- Canonical docs (`requirements.md`, `architecture.md`, …) are **never
  rewritten** by derive-spec; the drift section records deltas vs canonical
  instead.