---
name: requirements-elicitation
description: "Procedural guidance for requirements discovery across two modes — (1) elicitation: interview users to turn vague ideas into a validated problem statement before requirements are formalised; (2) confirmation: closed, batched multiple-choice validation of claims derived from code, used to raise draft confidence bands (derive-spec Phase 7)."
globs: ["artefacts/product/**", "**/discovery-notes.md"]
---

# Requirements Elicitation Skill

**Applies to**: Discovery conversations, before any requirement is written in EARS notation.

---

## 1. Common to Both Modes

This skill operates an interrogation discipline in two modes — **elicitation** (open discovery:
find out what the user actually needs) and **confirmation** (closed validation: confirm claims
already derived from code). Both seek a human verdict rather than fabricating one, and both share
the same rules:

- **Ask, don't assert.** Interrogate rather than presume — elicitation opens the problem,
  confirmation closes it with a verdict.
- **Never fill a gap with an assumption.** When the human has not decided, record the open
  question or still-open claim rather than inventing an answer:
  - **Elicitation** → record the open question and escalate the blocking decision
    (`context/rules/multi-agent-collaboration.md`).
  - **Confirmation** → record the stated assumption, or keep the claim **Assumed** in the
    open-questions appendix.
- **Ground every claim so it can be verified.** Elicitation reflects back what was heard before
  asking more; confirmation cites the code line(s) that produced each claim.

---

## 2. Elicitation Mode (open discovery)

Finding out what the user actually needs, distinct from what they first asked for. The output is a
validated problem statement — `discovery-notes.md` — not a requirements specification and not a
solution. Formalisation happens afterwards in the structuring mode of `@product-owner`.

### 2.1 Questioning Framework

Ask questions to uncover:

#### The Problem

- What problem are you trying to solve?
- Who experiences this problem? How often?
- What happens if this problem isn't solved?
- How do people solve this today?

#### The Users

- Who will use this? (Be specific: roles, technical level)
- What's their context when using it?
- What do they care about most?

#### The Scope

- What's the smallest thing that would be useful?
- What's explicitly NOT part of this?
- Are there existing systems this needs to work with?

#### The Constraints

- Are there deadlines, budgets, or technical constraints?
- What would make this fail?
- What's already been tried?

#### The Success Criteria

- How will you know this works?
- What would make users delighted vs merely satisfied?

### 2.2 Interview Constraints

- Ask questions; don't assume you understand
- One or two questions at a time; don't overwhelm
- Reflect back what you heard before asking more
- Don't propose solutions; focus on understanding the problem
- Challenge vague statements like "fast", "easy", "user-friendly"
- Identify when scope is too large and help narrow it

### 2.3 Capturing the Interview

Write findings to `{project-root}/artefacts/product/discovery-notes.md` as the conversation
progresses — never accumulate the whole interview in memory and flush at the end. The file is a
working document: update the problem statement, users, scope boundaries, constraints, and open
questions as each is confirmed.

The section structure for `discovery-notes.md` is defined in the `@product-owner` definition,
Mode 1. Keep the notes free of requirement identifiers and acceptance criteria; those belong to
`requirements.md`.

### 2.4 Exit Criteria

The interview is complete when all of the following hold:

- The problem is stated in two or three sentences, without solution language
- Target users are named, with the context in which they meet the problem
- Scope boundaries state what is explicitly out of scope
- Constraints and assumptions are recorded
- Success criteria are observable or measurable
- Open questions are listed for the structuring mode, each with the decision it blocks

---

## 3. Confirmation Mode (closed validation)

Confirming or correcting claims already synthesised from code so a draft's confidence bands can be
raised before promotion. Applied during derive-spec Phase 7 (`batched human confirmation`) and
Mode 3 of `@product-owner` / `@solution-architect`. Presumes a draft exists; do not reopen
discovery.

### 3.1 Applicability

- Derived spec drafts staged in `artefacts/build/derived-spec-working/` ahead of promotion:
  `product-spec-draft.md` · `architecture-draft.md` · `api-catalogue-draft.md` · `data-model-draft.md`.

### 3.2 Questioning Discipline

- **One batched round** per draft — collect all questions up front, then ask once rather than
  drip-feeding.
- **Ask drift candidates first** (existing-doc vs code deltas), then pure code facts — ordering
  from derive-spec Phase 2 / Phase 7.
- **Numbered multiple-choice with an explicit "Other" option**, each option citing the files
  involved (`artefacts/build/reverse-spec.md` Step 3 format).
- Don't re-ask what a confirmed code citation already settles; confirmation targets intent, scope,
  and unclear deltas — not restating facts.

### 3.3 Recording Answers (confidence model — derive-spec § Confidence Model)

- **Confirmed answer** → raise the band/% and record the confirming citation (Verified 85–100 ·
  Needs Confirmation 50–85 · Assumed <50).
- **"Skip questions"** → record the stated assumption in place of the answer.
- **Unanswered question** → claim stays **Assumed** and remains in the open-questions appendix as
  still-open — never silently promoted.
- **Promotion DoD**: no subsection below Needs Confirmation and no blocking still-open question —
  or a recorded human override (derive-spec Phase 8). Definition and per-doc checklist:
  `context/templates/derived-spec-template.md` § Confidence Schema. Each doc is promoted
  independently.

### 3.4 Exit Criteria

Confirmation is complete when all of the following hold:

- Every question answered, skipped-with-assumption, or recorded still-open — none dropped silently.
- Confidence bands updated from the answers and the drift section reflects confirmed deltas.
- Both parties (agent + human) agree on what remains Assumed or still-open before promotion.
- The template's Promotion DoD (`derived-spec-template.md` § Confidence Schema) holds for
  each doc slated for promotion in Phase 8.
