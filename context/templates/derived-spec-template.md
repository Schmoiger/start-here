# {Product Spec | Architecture | Data Model | API Catalogue}: {Subject} (Derived)

<!--
derive-spec draft template. The deriving agent copies this template once per artefacts category and fills the matching skeleton:

  mode=product    -> product-spec.md      (@product-owner, Phase 4a)
  mode=technical  -> architecture.md, api-catalogue.md, data-model.md
                                              (@solution-architect, Phase 4b)
  mode=both       -> all four

Layout rule (B-008): the shipped doc opens with the content subsections —
never with boilerplate. Fill the matching skeleton below in place, strip the
`## Skeleton:` wrapper and the `{placeholder}` rows, then close with the
`## Drift` section (only when baseline docs exist) and finally the
`## Appendices` container (run metadata · confidence schema · subsection
format · open questions · verification and review record). Delete this
comment block from the shipped doc.

Drafts stage in `artefacts/build/derived-spec-working/`. Promotion to
`artefacts/{category}/derived/` happens only behind a human APPROVED verdict. Canonical docs are never rewritten by derive-spec.
-->

## Skeleton: product-spec.md (mode product | both)

<!-- Derived per Phase 4a: features from the UI inventory, roles from
     auth/permission evidence, flows from call chains, constraints from the
     `config` index key. Actor/role is named per UX flow; never anonymous. -->

### Actors and Roles
<!-- Each role cites its auth/permission evidence: guards, decorators, RBAC, role-scoped API paths. -->

### Features and Capabilities
<!-- Candidate features from `ui` components, `api` routes the UI consumes, and test node-ids. Cite the inventory rows. -->

### UX Flows
<!-- One subsection per flow; each names its actor and cites the call chain (`path:line` per hop). -->

### User-Facing Constraints
<!-- From `config`: env toggles, rate/limit hints, feature availability per key. Keys are redacted in the index; cite the key, never a secret value. -->

---

## Skeleton: architecture.md (mode technical | both)

<!-- Derived per Phase 4b. Module boundaries cite `files`/`imports`; entry points cite the index. Drafts only: canonical architecture ownership is untouched. -->

### System Purpose (Derived)
<!-- 2-4 sentences from entry points and module shape, not from marketing prose. -->

### Module Boundaries
<!-- One entry per module: responsibility, entry points, key dependencies. Cite `files`/`imports` evidence. -->

### Service and Process Shape
<!-- Visible processes, jobs, queues as evidenced by entry points and background-worker symbols. -->

### Deployment-Relevant Seams
<!-- From `config`: runtime toggles, timeouts, bounded resources, feature flags. Cite the config key and its source file. -->

---

## Skeleton: data-model.md (mode technical | both)

<!-- Derived from `schema` plus constraint hints in code. Note every constraint's origin as a citation. -->

### Tables and Collections
| Table / Collection | Purpose (observed) | Confidence | Evidence |
|--------------------|--------------------|------------|----------|
| {name} | {what it stores, from schema + usage} | {Band} · {NN}% | `{path:line}` |

### Columns and Constraints
<!-- Per table: columns, types, keys, unique/not-null/check constraints. Each constraint cites its origin: migration, model, or index row. -->

### Relationships
<!-- Foreign keys and join paths observed in `schema` and code; cite both sides. -->

---

## Skeleton: api-catalogue.md (mode technical | both)

<!-- Derived from `api` routes, `schema`, and UI consumption. This is a catalogue, not a contract: the canonical `openapi.yaml` is never rewritten. -->

### Routes
| Method | Path | Handler (`path:line`) | Auth / Guard | Consumed By | Confidence |
|--------|------|----------------------|--------------|-------------|------------|
| {GET} | {/path} | `{path:line}` | {guard or none} | {UI component(s)} | {Band} · {NN}% |

### Request and Response Shapes
<!-- Only where `schema` or handler code evidences the shape; cite the source. Unknown shapes go to the appendix, not to guesswork. -->

---

## Drift: Canonical Docs vs Derived Behaviour (required when baseline docs exist)

<!-- One row per delta where an existing doc says X and the code does Y. Omit
     this section only when the repo had no discoverable spec docs; then the
     Run metadata appendix records "none: code-derived only". Drift rows are
     asked first in the Phase 7 confirmation round. -->

| ID | Canonical source (`path:line`) | Says | Code does (`path:line`) | Question raised |
|----|-------------------------------|------|-------------------------|-----------------|
| D-001 | `{path:line}` | {documented claim} | {observed behaviour} | Q-001 |

---

## Appendices

### Appendix A · Run Metadata

| Field | Value |
|-------|-------|
| Mode | {product \| technical \| both} |
| Target | {repo or service root, `--repo` value} |
| Index provenance | `repo-index.json` ({scan date}; extractors: {meta.extractors}) |
| Baseline docs | {discovered spec docs, or "none: code-derived only"} |
| Output location | `artefacts/build/derived-spec-working/{category}.md` |

---

### Appendix B · Confidence Schema

<!-- Fixed bands (Q4 · A2). Keep this table in every
     promoted draft so readers can interpret the tiers without opening the
     skill, workflow, or template. The Promotion DoD below is the single
     source of truth consumed by the confirmation-mode records
     (requirements-elicitation skill §3.3-3.4) and the derive-spec Phase 8
     promotion gate (derive-spec skill; derive-spec.yaml). -->

| Band | % | Evidence required to claim it |
|------|---|-------------------------------|
| **Verified** | 85–100 | directly cited code or doc lines (`path:line`) that resolve; usage counts or call chains where material (`ui` / `api` / `tests` index rows); no blocking open question |
| **Needs Confirmation** | 50–85 | plausible from indexed evidence but requires a human answer (Phase 7, confirmation mode); drift candidates land here first |
| **Assumed** | <50 | reasonable inference only; stays Assumed until a human answer or a confirmed citation raises it |

**Update rule** (baked into every subsection below): a confirmed answer raises
the band and percentage and records the confirming citation; an unanswered
question keeps the subsection Assumed and its question stays in the
Open-Questions appendix as still-open. Never promote a still-open question
silently.

**Promotion DoD** (per doc): a draft is promotable at Phase 8 when all
of the following hold:

1. Every subsection sits at **Needs Confirmation or above**, or the human
   recorded an explicit override for it (override recorded in the Verification
   and Review record).
2. No **blocking** open question is still-open in the appendix; non-blocking
   still-open questions are listed with priority.
3. `verify --doc` passes on the final draft (all `path:line` citations resolve).
4. The Verification and Review record shows confirmed answers with their
   citations, and the drift section reflects confirmed deltas.
5. Human review gate verdict is **APPROVED** (derive-spec Phase 8);
   CHANGES REQUIRED returns the doc to the specified phase.

Each doc is promoted independently: one category may meet the DoD and promote
while another stays in draft.

---

### Appendix C · Subsection Format

### {Subsection title}

**Confidence**: {Band} · {NN}% · Evidence: `{path:line}`, `{path:line}`

<!-- 2-4 sentences or a table: what the code does, present tense. Every claim
     carries a citation. No citation, no claim.
     Update rule: a confirmed answer raises the band/% here and cites
     the confirming evidence; an unanswered question keeps Assumed and adds a
     still-open row to the Open-Questions appendix. Never promote silently. -->

{Content.}

---

### Appendix D · Open Questions

<!-- One row per question raised during derivation or drift analysis. Options
     are numbered multiple-choice with "Other" (Q2 · reverse-spec.md Step 3),
     each option citing the files involved. Drift questions are listed first:
     they are asked first in Phase 7. Confirmed rows move to Status "resolved"
     with the answer and citation; unanswered rows stay "still-open" and their
     subsections stay Assumed. -->

| ID | Subsection | Priority | Question | Options | Status |
|----|------------|----------|----------|---------|--------|
| Q-001 | {§Subsection title} | {blocking \| high \| low} | {question}? | 1. {option} (`{path}`) · 2. {option} (`{path}`) · Other | still-open |

---

### Appendix E · Verification and Review Record

| Check | Result | Date |
|-------|--------|------|
| `verify --index` (citations resolve) | {pass \| fail} | {DD/MM/YYYY} |
| `verify --doc` (final drafts) | {pass \| fail} | {DD/MM/YYYY} |
| Promotion DoD | {met \| override \| not met} | {DD/MM/YYYY} |
| Human review gate | {APPROVED \| CHANGES REQUIRED} | {DD/MM/YYYY} |

<!-- Promotion copies this draft to artefacts/{category}/derived/ only after
     APPROVED and only when the Promotion DoD holds. Canonical docs are never
     rewritten; the drift section above carries the deltas instead. -->
