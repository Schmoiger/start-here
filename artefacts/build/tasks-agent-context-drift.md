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

## Rationalisation Tasks (adopted 25 Oct 2026)

Roster review adopted six changes. Executing them takes the roster from 19 to 16 agents:

`orchestrator`, `agent-harness`, `product-owner`, `solution-architect`, `ui-designer`,
`python-coder`, `typescript-coder`, `functional-tester`, `ui-tester`, `security-tester`,
`tech-lead`, `code-reviewer`, `principles-reviewer`, `devops`, `documentation`, `harness-analyst`.

Execution order: TASK-018 and TASK-017 amend the specs first; TASK-013 then creates the role;
TASK-014, TASK-015, TASK-016 and TASK-019 implement the merges. TASK-015 must precede TASK-019 —
both rewrite `context/workflows/design.yaml`.

| ID | Pri | Status | Phase | Assignee | Blocked By | Description |
|----|-----|--------|-------|----------|------------|-------------|
| TASK-014 | high | pending | fix | @agent-harness | TASK-013 | Adopt product merge — `product-expert` absorbed into `product-owner` (large; elicit + structure modes) |
| TASK-015 | high | pending | fix | @agent-harness | TASK-013 | Adopt API merge — `api-designer` absorbed into `solution-architect`; OpenAPI conventions → skill |
| TASK-016 | high | completed | fix | @agent-harness | TASK-013 | Adopt analyst merge — one `harness-analyst` + `workflow-analysis.md` and `tokenomics-audit.md` lens skills |
| TASK-017 | high | pending | diagnose | @orchestrator | - | Fix TASK-012 lanes inconsistency — harness lane implementer is `@agent-harness`, not `@orchestrator` |
| TASK-018 | normal | pending | diagnose | @orchestrator | - | Extend `agent-harness` spec — add `python-scripting`, `git-subrepo-operations`, `agent-sandbox` skills and `workflow-standards` standard |
| TASK-019 | high | pending | fix | @agent-harness | TASK-013, TASK-015 | Adopt single `devops` — absorb `database-designer`, extract technology playbooks to skills, model `small` → `medium` |

Every task below ends with the same validation gate: `uv run python context/scripts/validators/agent_definitions.py`,
then `uv run python context/scripts/generators/generate_adapters.py`, then
`uv run python context/scripts/validators/adapter_drift.py`, then `uv run pytest context/scripts/tests/ -v`.
A merge is not complete until all four pass and no reference to a deleted agent remains outside
`artefacts/build/archive/`.

### TASK-014 — Product merge (`product-expert` → `product-owner`)

**Decision**: one product agent, name `product-owner` (least reference churn), `model: large`.
Mode 1 Elicitation (interview → `discovery-notes.md`); Mode 2 Structuring (EARS requirements,
user stories, open questions). Rationale: the pair is one pipeline — `product-expert.md` L94
already says the output is "ready for @product-owner" — with identical rules/standards and
sequential dispatch in `design.yaml`.

**Files**:

- `context/agents/product-owner.md` — rewrite to `context/templates/agent-template.md` shape (it
  still has legacy `Required Standards` / `Required Rules` sections the validator rejects);
  `model: large`; `mcp_tools`: `exa_web_search`, `context7`, `tavily_search`; `skills`:
  `bootstrap-workflow.md`, `intent-fidelity.md`, `technical-authoring.md`; body gains Mode 1 /
  Mode 2; deliverables: `discovery-notes.md`, `requirements.md`, `user-stories.md`,
  `open-questions.md` — all in `{project-root}/artefacts/product/`.
- Create `context/skills/requirements-elicitation.md` — the questioning framework and interview
  constraints moved from `context/agents/product-expert.md` L50–88 (problem / users / scope /
  constraints / success criteria; one or two questions at a time; reflect back; challenge
  "fast"/"easy"/"user-friendly"). `globs: ["artefacts/product/**", "**/discovery-notes.md"]`.
- Delete `context/agents/product-expert.md`.
- `context/workflows/design.yaml` L11–12 — discovery phase `agents:` becomes a single
  `product-owner` entry.
- `context/workflows/content.yaml` L8 — `product-expert` → `product-owner` (research phase).
- `context/workflows/prototype.yaml` L14 — already `product-owner`; no change.
- `context/agents/README.md` L7–8 — delete the product-expert row; `product-owner` → large,
  purpose widened to "Elicits and structures requirements and user stories".
- `context/models.yaml` L59 — move "User stories and requirements structuring (@product-owner)"
  from `medium` to `large`; L85 — replace `@product-expert` with `@product-owner`.
- `context/scripts/generators/adapters/core/agents_md.py` L34 — remove `'product-expert'` from
  `category_order`.
- `artefacts/README.md` L11 — primary agents `@product-expert`, `@product-owner` → `@product-owner`.
- `context/docs/agentic-framework.md` (L15 "nineteen") and `agentic-framework-reference.md` —
  update counts and references.

**Acceptance**: `grep -rn product-expert context/ artefacts/` returns nothing outside
`artefacts/build/archive/`; design, content and prototype workflows dispatch only existing agents;
`product-owner` is `large` in both the definition and `context/agents/README.md`; both output
templates (`requirements-template.md`, `user-stories-template.md`) are still referenced.

**Write scope**: `context/agents/`, `context/skills/`, `context/workflows/`, `context/models.yaml`,
`context/scripts/generators/`, `context/docs/`, `artefacts/README.md` (agent tables only).

---

### TASK-015 — API merge (`api-designer` → `solution-architect`)

**Decision**: `solution-architect` owns the whole API artefact chain — logical contracts
(`architecture.md`, `api-catalogue.md`) and the canonical OpenAPI spec. `model: large` (unchanged).
OpenAPI authoring conventions become a skill. Rationale: `solution-architect.md` §Deliverables
already claims `openapi.yaml`, ownership is contradicted three ways today (see below), and
`api-designer` is dispatched once per design cycle and never during build.

**Files**:

- `context/agents/solution-architect.md` — absorb `api-designer.md` §Task Constraints (L56–62:
  OpenAPI 3.0+, camelCase JSON / kebab-case URLs, every response documented, realistic examples,
  backwards compatibility, standard HTTP semantics); `standards:` += `security-standards.md`,
  `doc-standards.md`; `skills:` += `openapi-authoring.md`; rewrite §Deliverables and
  §Boundary Clarifications — remove "@api-designer maintains and extends it", state single
  ownership; align body to the template.
- Create `context/skills/openapi-authoring.md` from the same constraints.
  `globs: ["**/openapi*.yaml", "**/openapi*.yml", "**/openapi*.json", "artefacts/api/**"]`.
  Include the YAML validation command
  (`uv run python -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" {file}`).
- Delete `context/agents/api-designer.md`.
- `context/workflows/design.yaml` — `design-architecture` output list gains `openapi.yaml`;
  `design-contracts` (L30–34) removes `api-designer` (the phase is schema-only for `devops` after
  TASK-019); update L118 notes and the L136 dependency comment.
- `context/agents/README.md` L12 — delete the api-designer row; solution-architect purpose widened.
- `context/models.yaml` L58 — remove `@api-designer`; leave the schema half for TASK-019 to
  finalise (sequence TASK-015 first).
- `context/scripts/generators/adapters/core/agents_md.py` L35 — remove `'api-designer'`.
- `context/templates/architecture-template.md` L3 — remove `api-designer` from the consumers list.
- `artefacts/README.md` L13 — API row primary agent → `@solution-architect`.
- `context/docs/*` — counts and references.

**Open decision (record it, do not guess silently)**: canonical OpenAPI path. `design.yaml` L118,
`api-designer.md` L62 and `solution-architect.md` §Deliverables say
`artefacts/architecture/openapi.yaml`; `artefacts/README.md` L13 says `artefacts/api/openapi.yaml`.
Choose one, record the rationale in `artefacts/architecture/architecture-decision.md` (feeds
TASK-008), and make every reference agree. Default if no human input:
`artefacts/architecture/openapi.yaml` (current behaviour, no migration).

**Acceptance**: `grep -rn api-designer context/ artefacts/` empty outside archive; the canonical
path is identical in the architect definition, `design.yaml`, `artefacts/README.md` and the ADR;
the OpenAPI skill is listed in the architect's frontmatter.

**Write scope**: as TASK-014, plus `artefacts/architecture/architecture-decision.md` (append only).

---

### TASK-016 — Analyst merge → `harness-analyst`

**Status: completed (25 Oct 2026)** — executed out of dependency order (before TASK-013) on direct user request, by
Cline rather than `@agent-harness`. All files below landed; both lens skills exist and are in the agent frontmatter;
output paths unchanged. Gate: `agent_definitions.py` valid for `harness-analyst.md`, `generate_adapters.py`
(4 created / 1 updated), `adapter_drift.py` in sync, `pytest context/scripts/tests/` 186 passed, acceptance grep
(`workflow-analyst|tokenomics-analyst` in `context/`) empty. Caveat: repo-wide `agent_definitions.py` stays red on
12 legacy agents outside this task's scope (baseline 14/18 failing at HEAD before this change) — owned by
TASK-014/015/019 and pending template-alignment work. One deliberate deviation: the composite "Workflow Health
Score X/100" from `workflow-analyst.md` was dropped (kept the per-metric scoring rubric) because
`retrospective.yaml` §workflow_rules prohibits health scores — rule wins over agent.

**Decision**: one retrospective measurement agent, `model: medium`, with lens selection by task
prompt. Rationale: identical frontmatter pools, identical data sources (interruptions JSONL,
session-log JSONL, incidents, git `Agent-Session:` trailers), identical trigger. Only the analysis
lens differs — "how", not "who".

**Files**:

- Create `context/agents/harness-analyst.md` — template shape; `standards`: `workflow-standards.md`,
  `agent-standards.md`, `doc-standards.md`, `coding-standards.md`, `testing-standards.md`,
  `tech-standards.md`; `rules`: `bash-environment.md`, `multi-agent-collaboration.md`,
  `tech-writing.md`, `workspace-conventions.md`; `skills`: `multi-agent-workflows.md`,
  `workflow-analysis.md`, `tokenomics-audit.md`; body keeps the shared data-source inventory;
  outputs: `artefacts/build/efficiency-report.md`, `artefacts/build/efficiency-data/`,
  `artefacts/build/tokenomics-report.md`.
- Create `context/skills/workflow-analysis.md` — the macro lens moved from `workflow-analyst.md`
  (task/handoff/cycle-time/bottleneck metrics, scoring rubric, report format; roughly L48–216 and
  L340–420).
- Create `context/skills/tokenomics-audit.md` — the micro lens moved from `tokenomics-analyst.md`
  (six audit lenses, model-tier conformance vs `context/models.yaml`, autonomy rate, context bloat,
  token economics).
- Delete `context/agents/workflow-analyst.md` and `context/agents/tokenomics-analyst.md`.
- `context/workflows/continuous-improvement.yaml` L38–44 — review phase `agents: [harness-analyst]`;
  notes name the lens in the task prompt and keep the two specialisation descriptions as lens
  descriptions; if parallelism matters, spawn twice with disjoint outputs (`efficiency-report.md`
  vs `tokenomics-report.md`).
- `context/workflows/retrospective.yaml` L8 — `workflow-analyst` → `harness-analyst`; note the
  default lens (workflow-analysis).
- `context/agents/README.md` L28–29 — replace both rows with `harness-analyst` (medium).
- `context/models.yaml` L61 — `@workflow-analyst, @tokenomics-analyst` → `@harness-analyst`.
- `context/scripts/generators/adapters/core/agents_md.py` L41–42 — replace both entries with
  `'harness-analyst'`.
- `context/docs/*` — counts and references.

**Acceptance**: `grep -rn 'workflow-analyst\|tokenomics-analyst' context/` empty outside archive;
both workflows dispatch `harness-analyst`; both lens skills exist and appear in the agent
frontmatter; output paths unchanged so existing retrospective consumers still resolve.

**Write scope**: as TASK-014.

---

### TASK-017 — Fix the TASK-012 lanes inconsistency

**Decision**: the harness lane is implemented by `@agent-harness` (matching the TASK-013 boundary
table: "Harness implements, tech-lead gates"). `@functional-tester` writes the RED validator tests.
`@orchestrator` keeps only the bootstrap exception (creating the role that does not yet exist) and
ownership of `HANDOFF.md` / `tasks.md` / `bugs.md`.

**Files**:

- `artefacts/build/tasks-agent-context-drift.md` § "Workflow gap — the `fix` phase assumes a code
  fix" → "Proposed lanes" table — harness lane
  Implementer becomes `` `@agent-harness`; `@functional-tester` for validator behaviour (RED first) ``;
  the artefacts list gains `context/models.yaml` and `context/scripts/generators/` (TASK-013 write
  scope); add the note: orchestrator writes task files/HANDOFF and bootstraps the role only.
- The TASK-012 row in this file — description references the corrected table; `Blocked By` gains
  TASK-017.
- Re-read TASK-006, TASK-007 and TASK-009 assignments; confirm they read correctly once the harness
  owner exists (they already name `@agent-harness` / `@devops`).

**Acceptance**: lanes table, TASK-012 description, TASK-013 boundary table and write scope all
agree; no task in this file implies a gate agent (`@tech-lead`, `@code-reviewer`,
`@principles-reviewer`, `@security-tester`) implements harness changes.

---

### TASK-018 — Extend the `agent-harness` skill/standards pools

**Decision** (roster review §1): the harness role needs the machinery skills in its durable
frontmatter, not only glob-resolved ones.

**Files**:

- `artefacts/build/tasks-agent-context-drift.md` § "New agent spec — agent-harness":
  - `skills` += `python-scripting.md` — validators and generators are PEP 723 scripts under
    `context/scripts/**/*`;
  - `skills` += `git-subrepo-operations.md` — `context/` is a git-subrepo; pushing harness changes
    upstream is this role's job;
  - `skills` += `agent-sandbox.md` — sandbox-safe command execution for generator/validator runs;
  - `standards` += `workflow-standards.md` — `context/workflows/` is in the harness write scope.
- The TASK-013 row — `Blocked By` gains TASK-018; acceptance criteria mention the full pool
  (4 standards, 6 skills).

**Acceptance**: the spec table lists all four standards and all six skills; TASK-013 acceptance
criteria reference them; every listed path exists under `context/skills/` or `context/standards/`
(no phantom entries — see this incident's own root cause).

---

### TASK-019 — Single `devops` (absorb `database-designer`, extract skills, model `small` → `medium`)

**Decision**: one data and infrastructure owner spanning design-time schema, build-time migrations,
Supabase local/staging deployment and GCP deployment. Technology playbooks move to skills; the agent
body keeps mode dispatch plus the generic deploy procedure. `model: medium` — physical schema design
is judgement work, and every other design agent is medium or large. Rationale: `build.yaml`'s
`schema-migration` phase (L53–64) already assigns migrations to devops; the split with
`database-designer` is by lifecycle phase, not by domain.

**Files**:

- `context/agents/devops.md` — `model: small` → `medium`; absorb from `context/agents/database-designer.md`
  §Constraints (L55–63: PostgreSQL default, normalisation, UUID PKs, `created_at`/`updated_at`,
  snake_case, FK and common-query indexes) and §Boundary Clarifications (L76–85: conceptual
  `data-model.md` from @solution-architect → physical schema; never modify `data-model.md`);
  deliverables gain `artefacts/database/` (`schema.sql`, `migrations/`, `er-diagram.md`,
  `design-decisions.md`); `standards:` += `doc-standards.md`; `skills:` += `database-design.md`,
  `mermaid-authoring.md`, `supabase-operations.md` (keep `agent-sandbox.md`, `agent-workflows.md`,
  `git-subrepo-operations.md`, `python-scripting.md`); fix `tools:` frontmatter to Supabase **MCP**
  (not CLI); replace the Mode 1 / Mode 2 playbooks with mode dispatch + skill references + generic
  procedure (intake → plan → staging → validate → approval gate → rollback → log).
- Create `context/skills/database-design.md` from the absorbed conventions.
  `globs: ["**/migrations/*.sql", "**/supabase/**", "**/database_service/**", "**/stores/**", "artefacts/database/**"]`.
- Create `context/skills/gcp-deployment.md` from `devops.md` Mode 2 (L80–100): `terraform validate`
  and `plan` before apply, staging before production, explicit production approval, Cloud Run
  Functions Gen 2, Firebase Hosting, Workload Identity, region `europe-west2`, least privilege and
  encryption at rest and in transit, rollback plan mandatory.
  `globs: ["**/*.tf", "**/terraform/**", "artefacts/gcp/**"]`.
- Extend `context/skills/supabase-operations.md` with the Mode 1 deploy procedure (from
  `devops.md` L59–78): pending-migration check, edge-function deploy, RLS validation against
  `pg_policies`, smoke test, deployment-log format, rollback steps.
- `context/rules/supabase.md` §1 — resolve the live contradiction: `devops.md` L70 says "via
  Supabase MCP or `supabase db push`" and L113 validates with `supabase db push --dry-run`, while
  the rule says "Never use the Supabase CLI" and the skill marks `supabase db push` as wrong. Keep
  MCP for queries and migrations; whitelist only CLI operations MCP cannot perform — verify against
  `context/mcp/mcp.json` (the skill's mapping table has no edge-function-deploy tool, so
  `supabase functions deploy` is the expected whitelist). Replace the dry-run validation with a
  schema assertion via `execute_sql`.
- Delete `context/agents/database-designer.md`.
- `context/workflows/design.yaml` L30–34 — `design-contracts` agents: `database-designer` → `devops`;
  rename the phase "Physical Schema Design"; update L118 notes and the L136 dependency comment.
- `context/workflows/build.yaml` L63 — verify the "devops operates in local mode" note still matches
  the rewritten definition.
- `context/agents/README.md` L11 and L25 — delete the database-designer row; devops purpose widened,
  model `medium`.
- `context/models.yaml` — L29 remove "Infrastructure deployment commands (@devops)" from `small`;
  add devops to `medium` typical tasks; L58 "Schema and API design (@database-designer, @api-designer)"
  → "Schema design (@devops)" (coordinate with TASK-015, which removes the API half).
- `context/scripts/generators/adapters/core/agents_md.py` — L35 remove `'database-designer'`; L39
  remove stale `'gcp-devops'` (no such agent exists).
- `context/templates/architecture-template.md` L3 — remove `database-designer` from the consumers list.
- `artefacts/README.md` L12 — architecture row primary agents → `@solution-architect`, `@devops`.
- `context/docs/*` — counts and references.

**Acceptance**: `devops` is `medium` in the definition and inventory;
`grep -rn 'supabase db push' context/agents/ context/skills/` returns only the "Wrong" mapping row in
`supabase-operations.md`; no reference to `database-designer` or `gcp-devops` remains outside
archive; the design workflow dispatches only existing agents; the four validation commands pass.

**Write scope**: as TASK-014, plus `context/rules/supabase.md`.

---

## Tasks

| ID | Pri | Status | Phase | Assignee | Blocked By | Description |
|----|-----|--------|-------|----------|------------|-------------|
| TASK-001 | critical | completed | diagnose | - | - | Record phantom-reference inventory for all 18 agents (see Findings) |
| TASK-012 | high | pending | diagnose | @solution-architect | TASK-017 | Extend `context/workflows/continuous-improvement.yaml` fix phase with artefact-type lanes (code / harness / docs), each with an owning agent and validation, so non-code fixes are not routed to `@python-coder` |
| TASK-013 | high | pending | fix | @orchestrator | TASK-012, TASK-018 | Create `context/agents/agent-harness.md` — specialist owner for the agent-facing harness (definitions, rules, skills, templates, workflows, validators); register in `context/agents/README.md`; regenerate adapters. Spec in Findings |
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
