# Tasks: Derive Product and Technical Specifications from Repo

**Branch**: feat/spec-agent
**Status**: Planning
**Scope**: Create a new harness capability to derive product and/or technical specifications from an existing codebase using a single workflow with mode switches.
**Created**: 2026-10-29
**Amended**: 2026-10-29

## Task Index

| ID | Priority | Status | Blocked By | Task |
|----|----------|--------|------------|-------|
| Q0 | critical | pending | - | Answer the clarifying questions in §Questions below |
| T-001 | critical | pending | Q0 | Create skill `context/skills/derive-spec.md` with modes: product, technical, both |
| T-002 | high | pending | Q0 | Create workflow `context/workflows/derive-spec.yaml` with modes, shared phases, and mode-specific phases |

## File Scope

- `artefacts/build/tasks-spec-agent.md` — task definition and workflow specification
- `context/skills/derive-spec.md` — new skill with mode switches: product, technical, both
- `context/workflows/derive-spec.yaml` — new workflow YAML supporting all three modes
- `context/workflows/build.yaml` — optional phase dependency
- `context/agents/product-owner.md` — extends agent for product-spec synthesis modes
- `context/agents/solution-architect.md` — extends agent for technical-spec synthesis modes
- `artefacts/product/product-spec.md` — generated product specification output
- `artefacts/architecture/architecture.md` — generated architecture documentation output
- `artefacts/architecture/data-model.md` — generated data model documentation output
- `artefacts/architecture/api-catalogue.md` — generated API catalogue output

## Task

### Q0: Answer the clarifying questions in §Questions below
- **Priority**: critical
- **Status**: pending
- **Blocked By**: none
- **Description**: Answer Q1 through Q10. These questions block all implementation work for both product and technical spec derivation modes.

### T-001: Create new skill `context/skills/derive-spec.md`
- **Priority**: critical
- **Status**: pending
- **Blocked By**: Q0
- **Description**: Create a new skill with mode switches. Product mode phases: repo-analysis, spec-discovery, feature-inventory, ux-flow-analysis, spec-draft, confirmation-questions, elicit-answers, spec-finalise. Technical mode phases: repo-analysis, architecture-analysis, api-analysis, data-model-analysis, spec-draft, confirmation-questions, elicit-answers, spec-finalise. Both mode runs product then technical sequentially.

### T-002: Create new workflow `context/workflows/derive-spec.yaml`
- **Priority**: high
- **Status**: pending
- **Blocked By**: Q0
- **Description**: Define phases with agent assignments, validation criteria, quality gates, state recovery, and mode selection. Shared phases run across all modes; mode-specific phases run only when relevant mode is selected. Quality gate requires human review before commit.

## §Questions — Clarifying Decisions Required Before Implementation

These questions block progress on Q0, T-001 and T-002.

### Q1 — Output Location for the Generated Specification
Options:
A. `artefacts/product/product-spec.md` (single canonical product spec)
B. `artefacts/product/[service-name]-product-spec.md` (per-service, matches `PRD-[service-name].md` convention in reverse-spec.md)
C. Let the human choose per-run via a `--spec-name` flag

### Q2 — Question Format for Confirmation Step
Options:
A. Multiple-choice with 2–3 options plus "Other" (matches reverse-spec.md Step 3)
B. Yes/No confirmation only
C. Open-ended text answers

### Q3 — Repo Organization Scope
Options:
A. Repos "organised like mine" (build/product folder, artefacts/product/) only
B. Any repo with generic heuristics (discover spec docs anywhere)
C. Configurable via a `spec-docs-glob` setting in workflow YAML

### Q4 — Confidence Model
Options:
A. Confidence % per subsection only (your original idea)
B. Tiered confidence labels + % (Verified / Needs Confirmation / Assumed from reverse-spec.md, displayed as %)
C. Tiered labels only, no %

### Q5 — Agent for Technical Spec Synthesis
Options:
A. Reuse `@solution-architect` agent (recommended)
B. Create a new `@tech-spec-architect` agent
C. Have `@solution-architect` plus `@ui-designer` co-derive

### Q6 — Elicitation Skill for Technical Spec
Options:
A. Reuse `requirements-elicitation` skill (for problem discovery, not architectural clarification)
B. Add a **code-confirmation** mode to `requirements-elicitation.md`
C. Create a new separate skill (e.g. `code-confirmation.md`) distinct from requirements-elicitation
D. Create a new `architecture-elicitation.md` skill for technical clarification

### Q7 — Integration with Build Workflow
Options:
A. Standalone workflow only (`derive-spec.yaml`)
B. Standalone + added as an optional precursor phase to `build.yaml` task-planning
C. Auto-trigger whenever `artefacts/product/product-spec.md` or `artefacts/architecture/architecture.md` is missing

### Q8 — Maximum Repo Size / Scan Limit
Options:
A. No limit (scan everything)
B. Max lines-of-code threshold (flag large repos for manual scoping)
C. Max file count for UI scanning; human must scope large repos first

### Q9 — Mode Selection Mechanism
Options:
A. CLI arg / workflow input (`--mode product | technical | both`)
B. Environment variable / config flag
C. Human prompt at workflow entry

### Q10 — Combined Output Format
Options:
A. Single spec doc with Product and Technical sections
B. Two separate docs (product-spec.md and architecture.md/data-model.md/api-catalogue.md)
C. Single doc with mode-appropriate sections depending on mode selected
