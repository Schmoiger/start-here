# Tasks — Agent Context Drift

Workflow: `continuous-improvement` (mode: incident)
Branch: `ci/agent-context-drift`
Phase: `diagnose`

**Root cause (already diagnosed, see Findings)**: agent definitions carry three hand-maintained copies of the
same obligations — YAML frontmatter, a "Required Rules (Must Follow!)" body table, and the orchestrator's
always-apply list. Only the frontmatter is machine-validated, so the body tables drifted to reference eight
rule files that do not exist. CI reports `✅ All 18 agent definitions valid` while every subagent is
instructed to read phantom paths and silently falls back to an 8-word paraphrase.

---

## Tasks

| ID | Pri | Status | Phase | Assignee | Blocked By | Description |
|----|-----|--------|-------|----------|------------|-------------|
| TASK-001 | critical | completed | diagnose | - | - | Record phantom-reference inventory for all 18 agents (see Findings) |
| TASK-012 | high | pending | diagnose | @solution-architect | - | Extend `context/workflows/continuous-improvement.yaml` fix phase with artefact-type lanes (code / harness / docs), each with an owning agent and validation, so non-code fixes are not routed to `@python-coder` |
| TASK-013 | high | pending | fix | @orchestrator | TASK-012 | Create `context/agents/agent-harness.md` — specialist owner for the agent-facing harness (definitions, rules, skills, templates, workflows, validators); register in `context/agents/README.md`; regenerate adapters. Spec in Findings |
| TASK-002 | critical | pending | fix | @agent-harness | TASK-013 | Fix `context/templates/agent-template.md` — replace dead rule names (`british-english.md`, `handoff-hygiene.md`, `escalation.md`); add `Source` column to the rules table |
| TASK-003 | high | pending | fix | @functional-tester | - | RED: add failing test in `context/scripts/tests/test_agent_validator.py` — a body-table `Source` that does not resolve MUST produce an error |
| TASK-004 | high | pending | fix | @python-coder | TASK-003 | GREEN: extend `context/scripts/validators/agent_definitions.py` to parse body rule tables and assert each `Source` resolves under `context/rules/` or `context/skills/` (mirror frontmatter checks at L71–90) |
| TASK-005 | high | pending | fix | @agent-harness | TASK-002, TASK-013 | Rewrite `context/agents/python-coder.md` rule table to match its frontmatter; remove duplicate type-hint constraint (L51 vs L72) |
| TASK-006 | high | pending | fix | @agent-harness | TASK-002, TASK-013 | Rewrite remaining 17 agent rule tables — delete pointer-only rows, keep short imperatives, add `Source` attribution |
| TASK-007 | normal | pending | fix | @agent-harness | TASK-013 | Reconcile `context/agents/orchestrator.md` Rule Resolution always-apply list (L80–85, L105–106) with files that exist; decide whether `orchestrator.md` stays in `SKIPPED_FILES` (L30) |
| TASK-008 | normal | pending | discuss | @solution-architect | TASK-012 | Decide the compliance mechanism and layer taxonomy (frontmatter vs body vs injection); record in `artefacts/architecture/architecture-decision.md`; include whether a framework-maintainer agent is needed |
| TASK-009 | normal | pending | fix | @devops | TASK-004, TASK-005, TASK-006, TASK-007 | Regenerate runtime projections (`generate_adapters.py`), clear adapter drift, and add the validator to `.github/workflows/pr-subrepo-checks.yml` |
| TASK-010 | normal | pending | fix | @tech-lead | TASK-008, TASK-009 | Gate: run `agent_definitions.py`, `pytest`, `adapter_drift.py`; verify acceptance criteria; issue APPROVED / CHANGES REQUIRED to `artefacts/build/tech-review.md` |
| TASK-011 | low | pending | record | @orchestrator | TASK-010 | Record outcome — close `artefacts/build/todo.md` items on agent/standards DRY; update `artefacts/build/agent-incidents.md` with root cause, fix, commit hash |

---

## Assignment rationale

Assignee is chosen by **artefact type**, not by implementation language. Corrected after review — the first draft
defaulted to `@python-coder` for 7 of 10 tasks because the repo is Python, which is not a role boundary.

| Agent | Tasks | Why |
|-------|-------|-----|
| `@python-coder` | TASK-004 | The only Python source deliverable: validator logic |
| `@functional-tester` | TASK-003 | RED test first — no implementation without a failing test (`skills/tdd-workflow.md`) |
| `@agent-harness` | TASK-002, 005, 006, 007 | Specialist owner of the agent-facing harness (TASK-013) — the gate must not implement |
| `@orchestrator` | TASK-011, 013 | Bootstraps the harness role, then records the incident |
| `@solution-architect` | TASK-008, 012 | Owns design decisions and ADRs — lane taxonomy and layer authority |
| `@devops` | TASK-009 | Owns `build-standards.md` and CI/CD; adapters and workflow wiring are pipeline concerns |
| `@tech-lead` | TASK-010 | THE GATE only — `tech-lead.md` L77: "Don't rewrite code — describe what needs to change" |
| `@documentation` | none | Remit is user-facing documentation (`documentation.md` L20), not internal framework config |

**Note on the orchestrator's `< 50 lines per file` limit**: agent definitions run 80–140 lines. The edits planned
here are ~11-line table blocks, so surgical edits stay within the limit; if a file is rewritten wholesale the limit
is exceeded and must be raised in TASK-008.

### Roster gap — closed by TASK-013

No agent owned the context framework, which is why harness work defaulted to `@orchestrator` as an exception and then
to `@python-coder` by language. `@tech-lead` cannot absorb it: it is the gate, and `tech-lead.md` L77 ("Don't rewrite
code — describe what needs to change") is only meaningful if the reviewer is not the author. The same logic applies
to harness artefacts as to product code.

TASK-013 creates the missing role, giving a three-way separation:

| Activity | Owner |
|----------|-------|
| Decide the taxonomy and lane boundaries | `@solution-architect` (TASK-012, TASK-008) |
| Apply it to definitions, rules, templates, workflows | `@agent-harness` (TASK-002, 005, 006, 007) |
| Approve or reject the result | `@tech-lead` (TASK-010) |

`@orchestrator` retains TASK-013 because the role does not exist yet to create itself, and keeps its existing
ownership of spawn prompts, `HANDOFF.md`, `tasks.md`, and `bugs.md`.

---

## Findings

Phantom files — **zero** matches anywhere in the repo (verified with `find`, excluding `.git` and `node_modules`):

| Referenced name | Reality | Occurrences |
|-----------------|---------|-------------|
| `handoff-hygiene.md` | Does not exist | 18 agents |
| `escalation.md` | Does not exist | 18 agents |
| `british-english.md` | Does not exist | 17 agents |
| `git-commits.md` | Folded into `workspace-conventions.md` §2 | 8 agents |
| `quality-gates.md` | Folded into `testing.md` §1 | 3 agents |
| `output-locations.md` | Folded into `workspace-conventions.md` §1 | 3 agents |
| `type-safety.md` | Does not exist | 2 agents |
| `secrets-management.md` | File is `secrets.md` | 2 agents |

Secondary defects in `context/agents/python-coder.md`:

- Rules table lists `tdd-workflow.md` and `architecture-fidelity.md` — both live in `context/skills/`, not `context/rules/`
- Frontmatter declares `testing.md`; table cites `quality-gates.md` instead
- `functional-tester.md` L39 says "Read all 3 standards files" while frontmatter declares 4 (`context-framework.md` orphaned)
- CI blind spot: `agent_definitions.py` L71–90 validates frontmatter only; `orchestrator.md` is in `SKIPPED_FILES` (L30)

### Workflow gap — the `fix` phase assumes a code fix (TASK-012)

`continuous-improvement.yaml` `fix` declares `agents: [python-coder, typescript-coder]` and the note
"Delegate implementation changes to appropriate agents". Two coder agents and an undefined word — so *appropriate*
resolves to *coder* by default. The unstated assumption is that a framework fix is a code fix.

This incident disproves it. Of the 13 tasks here, one is application code (TASK-004), seven edit the agent-facing
harness (TASK-002, 003, 005, 006, 007, 012, 013), and five are process — diagnosis, design, CI wiring, gate, record
(TASK-001, 008, 009, 010, 011). Routing all of them to `@python-coder` was not an arbitrary mistake; the workflow
invited it.

Proposed lanes, for TASK-012 to ratify:

| Lane | Artefacts | Implementer | Gate |
|------|-----------|-------------|------|
| code | `services/**/src/`, `tests/` | `@python-coder` / `@typescript-coder`, after RED | `@tech-lead` |
| harness | `context/agents/`, `context/rules/`, `context/skills/`, `context/templates/`, `context/workflows/`, `context/scripts/validators/` | `@orchestrator`; `@functional-tester` for validator behaviour | `@tech-lead` |
| docs | `artefacts/`, service `README.md`, user guides | `@documentation` | `@tech-lead` (informal) |

Edge case TASK-012 must resolve: `agent_definitions.py` is harness intent implemented in Python. The rule that
resolves it — **lane by intent, implementer by artefact, gate by risk** — needs to be written down, because today
nothing distinguishes a validator from a product module.

TASK-012 must also set a real ceiling for the orchestrator exception ("`< 50 lines per file`") or state why agent
definitions are exempt: they run 80–140 lines, so the limit is already being bent by the edits in TASK-005/006.

---

### New agent spec — `agent-harness` (TASK-013)

| Field | Value |
|-------|-------|
| `name` | `agent-harness` |
| `model` | `large` — must hold the full harness contract (frontmatter ↔ rules ↔ skills ↔ injected prompts) at once; a wrong edit propagates to every spawn |
| `standards` | `agent-standards.md`, `context-framework.md`, `doc-standards.md` |
| `rules` | `bash-environment.md`, `multi-agent-collaboration.md`, `tech-writing.md`, `workspace-conventions.md` |
| `skills` | `agent-workflows.md`, `architecture-fidelity.md`, `multi-agent-workflows.md` |

**Write scope**: `context/agents/`, `context/rules/`, `context/skills/`, `context/templates/`, `context/workflows/`,
`context/scripts/validators/`, `context/scripts/generators/`, `context/models.yaml`.

**Non-goals**: application code (`services/**`), any quality gate, human-facing documentation in `artefacts/`.

**Boundaries** — the reason the role exists is these separations:

| Agent | Division of labour |
|-------|--------------------|
| `@tech-lead` | Harness implements, tech-lead gates. `tech-lead.md` L77 forbids rewriting what it reviews |
| `@solution-architect` | Architect decides the taxonomy (TASK-012, TASK-008); harness applies it mechanically |
| `@orchestrator` | Orchestrator owns spawn prompts, `HANDOFF.md`, `tasks.md`; harness owns the definitions those spawns read |
| `@functional-tester` | Tester writes validator tests (RED); harness implements behaviour (GREEN) |
| `@python-coder` | Harness owns validators and generators as harness intent; coders own product modules |

**Non-negotiables** (to appear in the agent body):

- A definition that references a file not on disk is a defect, not a warning
- Change the agent to match the rule, never the rule to match the agent
- Every rule citation carries `file.md §section`; a paraphrase without a source is a fork

**Registration and validation**: add to the `context/agents/README.md` inventory; `generate_adapters.py` propagates
to `AGENTS.md` and the runtime projections; `agent_definitions.py` and `adapter_drift.py` must pass.

---

## Design decision

Keep the two-layer pattern; eliminate the duplication. Frontmatter is the single source of truth and the
body table must be derived from it, verified by the validator, and attributed by file (`Source` column) so
no paraphrase survives without a pointer.

- **Inline** short, absolute, high-blast-radius imperatives (`uv run`, never bare `python`; never modify test files)
- **Pointer only** for long procedural rules (escalation, handoff format, commit trailers)
- **Never paraphrase** a rule without `file.md §section` attribution

---

## Reference context

- `context/scripts/validators/agent_definitions.py` — validator to extend (frontmatter checks L71–90)
- `context/templates/agent-template.md` — source of the recurring drift
- `context/standards/agent-standards.md` §1.1 — inherited-compliance statement
- `context/agents/orchestrator.md` §Rule Resolution — injection mechanism
- `context/standards/context-framework.md` — terse format rules (one line per task)
- `.github/workflows/pr-subrepo-checks.yml` — CI job that runs the validator

---

## Acceptance criteria

1. No agent definition references a file that does not exist in `context/rules/` or `context/skills/`.
2. `agent_definitions.py` fails when a body-table `Source` does not resolve.
3. Body rule tables agree with frontmatter for all 18 agents.
4. Adapter drift check passes after regeneration.
5. One of the two competing compliance mechanisms is documented as authoritative.
6. The `fix` phase declares an explicit lane for non-code artefacts, so every task in this file routes to an owner without human judgement.
7. `@agent-harness` exists, is registered in `context/agents/README.md`, passes `agent_definitions.py`, and owns every harness task — no gate agent implements.
