# Tasks — Agent Context Drift

**Workflow**: `continuous-improvement` (mode: incident) · **Branch**: `ci/agent-context-drift` · **Phase**: `diagnose` · **Status**: in progress
**Amended**: 25 Oct 2026 — task index lifted above task detail; prose compressed for agents.
**Reading guide**: §Task Index → §Dispatch → your task's detail. Completed-task detail is a verification record — read it only when your task builds on that merge.

---

## Task Index

| ID | Pri | Status | Phase | Assignee | Blocked By | Description |
|----|-----|--------|-------|----------|------------|-------------|
| TASK-001 | critical | completed | diagnose | - | - | Record phantom-reference inventory for all 18 agents (§Findings) |
| TASK-002 | critical | completed | fix | @harness-analyst | TASK-013 | Fix `context/templates/agent-template.md` — replace dead rule names (`british-english.md`, `handoff-hygiene.md`, `escalation.md`); add `Source` column to rules table |
| TASK-003 | high | completed | fix | @functional-tester | - | RED: failing test in `context/scripts/tests/test_agent_validator.py` — body-table `Source` that does not resolve MUST error |
| TASK-004 | high | completed | fix | @python-coder | TASK-003 | GREEN: extend `context/scripts/validators/agent_definitions.py` to parse body rule tables and assert each `Source` resolves under `context/rules/` or `context/skills/` (mirror L71–90) |
| TASK-005 | high | completed | fix | @harness-analyst | TASK-002, TASK-013 | Rewrite `context/agents/python-coder.md` rule table to match frontmatter; remove duplicate type-hint constraint (L51 vs L72) |
| TASK-006 | high | completed | fix | @harness-analyst | TASK-002, TASK-013 | Rewrite remaining 17 agent rule tables — drop pointer-only rows, keep short imperatives, add `Source` attribution. 14 of 15 definitions done; `orchestrator` §Rule Resolution is TASK-007's scope |
| TASK-007 | normal | pending | fix | @harness-analyst | TASK-013 | Reconcile `context/agents/orchestrator.md` Rule Resolution always-apply list (L80–85, L105–106) with files that exist; decide whether `SKIPPED_FILES` (L30) keeps it |
| TASK-008 | normal | pending | discuss | @solution-architect | TASK-012 | Decide compliance mechanism and layer taxonomy (frontmatter vs body vs injection); record in `artefacts/architecture/architecture-decision.md`; include whether a framework-maintainer agent is needed |
| TASK-009 | normal | pending | fix | @devops | TASK-004, TASK-005, TASK-006, TASK-007 | Regenerate runtime projections, clear adapter drift, add the validator to `.github/workflows/pr-subrepo-checks.yml` |
| TASK-010 | normal | pending | fix | @tech-lead | TASK-008, TASK-009 | Gate: run `agent_definitions.py`, `pytest`, `adapter_drift.py`; verify acceptance; verdict to `artefacts/build/tech-review.md` |
| TASK-011 | low | pending | record | @orchestrator | TASK-010 | Record outcome — close `artefacts/build/todo.md` DRY items; log root cause, fix, commit hash in `artefacts/build/agent-incidents.md` |
| TASK-012 | high | pending | diagnose | @solution-architect | TASK-017 | Add artefact-type lanes (code / harness / docs) with owner and validation to `continuous-improvement.yaml` §fix, so non-code fixes do not route to `@python-coder` (§Fix lanes) |
| TASK-013 | high | completed | fix | @orchestrator | TASK-012, TASK-018 | Create `context/agents/harness-analyst.md` — harness owner; register in `context/agents/README.md`; regenerate adapters (§Harness-analyst spec) |
| TASK-014 | high | completed | fix | @harness-analyst | TASK-013 | Product merge — `product-expert` absorbed into `product-owner` (elicit + structure modes) |
| TASK-015 | high | completed | fix | @harness-analyst | TASK-013 | API merge — `api-designer` absorbed into `solution-architect`; OpenAPI conventions → skill |
| TASK-016 | high | completed | fix | @harness-analyst | TASK-013 | Analyst merge — one `harness-analyst` + `workflow-analysis.md` and `tokenomics-audit.md` lens skills |
| TASK-017 | high | pending | diagnose | @orchestrator | - | Fix TASK-012 lanes inconsistency — harness implementer is `@harness-analyst`, not `@orchestrator` |
| TASK-018 | normal | completed | diagnose | @orchestrator | - | Extend `harness-analyst` spec — add `python-scripting`, `git-subrepo-operations`, `agent-sandbox` skills and `workflow-standards` standard |
| TASK-019 | high | completed | fix | @harness-analyst | TASK-013, TASK-015 | Single `devops` — absorb `database-designer`, extract technology playbooks to skills, `small` → `medium` |

Detail map: TASK-001–TASK-013 → §Findings · TASK-014–TASK-019 → §Task detail.

---

## Dispatch

**Execution order**: TASK-018 → TASK-017 → TASK-013 → TASK-014 · TASK-015 · TASK-016 → TASK-019.
TASK-015 precedes TASK-019 (both rewrite `context/workflows/design.yaml`).

**Validation gate — every task**: `uv run python context/scripts/validators/agent_definitions.py` →
`uv run python context/scripts/generators/generate_adapters.py` →
`uv run python context/scripts/validators/adapter_drift.py` → `uv run pytest context/scripts/tests/ -v`.
A merge is complete only when all four pass and no reference to a deleted agent remains outside
`artefacts/build/archive/`.

**Target roster** (19 → 15; harness owner and retrospective analyst are one role):
`orchestrator`, `harness-analyst`, `product-owner`, `solution-architect`, `ui-designer`, `python-coder`,
`typescript-coder`, `functional-tester`, `ui-tester`, `security-tester`, `tech-lead`, `code-reviewer`,
`principles-reviewer`, `devops`, `documentation`.

### Assignment rationale

Assignee is chosen by **artefact type**, not implementation language. The first draft routed 7 of 10 tasks
to `@python-coder` because the repo is Python — not a role boundary.

| Agent | Tasks | Why |
|-------|-------|-----|
| `@python-coder` | TASK-004 | The only Python source deliverable: validator logic |
| `@functional-tester` | TASK-003 | RED test first — no implementation without a failing test (`tdd-workflow.md`) |
| `@harness-analyst` | TASK-002, 005, 006, 007 | Specialist owner of the agent-facing harness (TASK-013) — the gate must not implement |
| `@orchestrator` | TASK-011, 013 | Bootstraps the harness role (completed), then records the incident |
| `@solution-architect` | TASK-008, 012 | Owns design decisions and ADRs — lane taxonomy and layer authority |
| `@devops` | TASK-009 | Owns `build-standards.md` and CI/CD; adapters and workflow wiring are pipeline concerns |
| `@tech-lead` | TASK-010 | Gate only — `tech-lead.md` L77: "Don't rewrite code — describe what needs to change" |
| `@documentation` | none | Remit is user-facing documentation (`documentation.md` L20), not internal framework config |

**Orchestrator `< 50 lines per file` limit**: definitions run 80–140 lines; the planned edits are ~11-line
table blocks, so surgical edits stay within the limit. Wholesale rewrites exceed it and must be raised in
TASK-008.

---

## Task detail

File-level specs for TASK-014–TASK-019. Detail for TASK-001–TASK-013 lives in §Findings.

### TASK-014 — Product merge (`product-expert` → `product-owner`)

**Completed 25 Oct 2026** by Cline (role not yet created; `@harness-analyst` holds the record). Gate green:
validator valid for `product-owner.md`, adapters 1 created / 4 updated + two orphaned `product-expert`
projections removed by hand, drift in sync, 186 tests, acceptance grep empty. Repo-wide validator stays red on
10 legacy agents (baseline 12/18 in TASK-016).

**Decision**: one product agent, name `product-owner` (least reference churn), `model: large`.
Mode 1 elicitation (interview → `discovery-notes.md`); Mode 2 structuring (EARS requirements, user stories,
open questions). Rationale: one pipeline — `product-expert.md` L94 already hands off "ready for
@product-owner" — identical rules/standards, sequential dispatch in `design.yaml`.

**Files**

- `context/agents/product-owner.md` — rewrite to `agent-template.md` shape (legacy `Required Standards` /
  `Required Rules` sections are validator-rejected); `model: large`; `mcp_tools`: `exa_web_search`,
  `context7`, `tavily_search`; `skills`: `bootstrap-workflow.md`, `intent-fidelity.md`,
  `technical-authoring.md`; body gains Mode 1 / Mode 2; deliverables `discovery-notes.md`,
  `requirements.md`, `user-stories.md`, `open-questions.md` under `{project-root}/artefacts/product/`.
- Create `context/skills/requirements-elicitation.md` from `product-expert.md` L50–88
  (problem / users / scope / constraints / success criteria; one or two questions at a time; reflect back;
  challenge "fast"/"easy"/"user-friendly"). `globs: ["artefacts/product/**", "**/discovery-notes.md"]`.
- Delete `context/agents/product-expert.md`.
- `context/workflows/design.yaml` L11–12 — discovery phase `agents:` becomes a single `product-owner` entry.
- `context/workflows/content.yaml` L8 — `product-expert` → `product-owner` (research phase).
  `context/workflows/prototype.yaml` L14 already names `product-owner`; no change.
- `context/agents/README.md` L7–8 — delete the product-expert row; `product-owner` → large, purpose widened
  to "Elicits and structures requirements and user stories".
- `context/models.yaml` L59 — user-stories/requirements structuring `medium` → `large`;
  L85 — `@product-expert` → `@product-owner`.
- `context/scripts/generators/adapters/core/agents_md.py` L34 — remove `'product-expert'` from `category_order`.
- `artefacts/README.md` L11 — primary agents → `@product-owner`.
- `context/docs/agentic-framework.md` (L15 "nineteen") and `agentic-framework-reference.md` — counts and references.

**Acceptance**: `grep -rn product-expert context/ artefacts/` empty outside `artefacts/build/archive/`;
design, content and prototype workflows dispatch only existing agents; `product-owner` is `large` in both
the definition and `context/agents/README.md`; `requirements-template.md` and `user-stories-template.md`
still referenced.

**Deviations** (deliberate): (1) `requirements-elicitation.md` is listed in the agent's `skills:` frontmatter,
not only the body — the original list would have left the new skill unloaded; (2) `test_e2e_compilation.py`
roster assertions now derive from `context/agents/*.md` instead of pinned `>= 18`, so TASK-015/019 do not
break an unrelated gate.

**Write scope**: `context/agents/`, `context/skills/`, `context/workflows/`, `context/models.yaml`,
`context/scripts/generators/`, `context/docs/`, `artefacts/README.md` (agent tables only).

---

### TASK-015 — API merge (`api-designer` → `solution-architect`)

**Completed 25 Oct 2026** by Cline (`@harness-analyst` role). Gate green: `solution-architect.md` passes
`agent_definitions.py`; adapters 1 created / 3 updated, orphaned `.agents/skills/api-designer` removed by
hand; drift in sync; 186 tests; acceptance grep empty outside this task file. Repo-wide validator remains red
on 9 legacy agents (down from 10 — the architect body was rewritten to the template shape).

**Open decision resolved by human**: canonical OpenAPI path is `artefacts/architecture/openapi.yaml`.
Recorded as ADR-001 in `artefacts/architecture/architecture-decision.md` (file did not exist; created as the
ADR log). The empty, tracked `artefacts/api/openapi.yaml` scaffold was deleted so `artefacts/api/` holds only
companion artefacts; standards references (`doc-standards.md` §4.2–4.3, `context-framework.md`) were updated
to match, extending the TASK-014 write scope by `context/standards/` and the two scaffold files.

**Decision**: `solution-architect` owns the whole API artefact chain — logical contracts (`architecture.md`,
`api-catalogue.md`) and the canonical OpenAPI spec; `model: large` unchanged. OpenAPI authoring conventions
become a skill. Rationale: `solution-architect.md` §Deliverables already claims `openapi.yaml`, ownership is
contradicted three ways today, and `api-designer` is dispatched once per design cycle and never during build.

**Files**

- `context/agents/solution-architect.md` — absorb `api-designer.md` §Task Constraints (L56–62: OpenAPI 3.0+,
  camelCase JSON / kebab-case URLs, every response documented, realistic examples, backwards compatibility,
  standard HTTP semantics); `standards:` += `security-standards.md`, `doc-standards.md`;
  `skills:` += `openapi-authoring.md`; rewrite §Deliverables and §Boundary Clarifications (remove
  "@api-designer maintains and extends it", state single ownership); align body to the template.
- Create `context/skills/openapi-authoring.md` from the same constraints.
  `globs: ["**/openapi*.yaml", "**/openapi*.yml", "**/openapi*.json", "artefacts/api/**"]`. Include the YAML
  validation command (`uv run python -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" {file}`).
- Delete `context/agents/api-designer.md`.
- `context/workflows/design.yaml` — `design-architecture` output list gains `openapi.yaml`; `design-contracts`
  (L30–34) removes `api-designer` (the phase is schema-only for `devops` after TASK-019); update L118 notes
  and the L136 dependency comment.
- `context/agents/README.md` L12 — delete the api-designer row; widen solution-architect purpose.
- `context/models.yaml` L58 — remove `@api-designer`; leave the schema half for TASK-019 to finalise
  (sequence TASK-015 first).
- `context/scripts/generators/adapters/core/agents_md.py` L35 — remove `'api-designer'`.
- `context/templates/architecture-template.md` L3 — remove `api-designer` from the consumers list.
- `artefacts/README.md` L13 — API row primary agent → `@solution-architect`.
- `context/docs/*` — counts and references.

**Open decision** (record it, do not guess silently): canonical OpenAPI path. `design.yaml` L118,
`api-designer.md` L62 and `solution-architect.md` §Deliverables say `artefacts/architecture/openapi.yaml`;
`artefacts/README.md` L13 says `artefacts/api/openapi.yaml`. Choose one, record the rationale in
`artefacts/architecture/architecture-decision.md` (feeds TASK-008), and make every reference agree. Default if
no human input: `artefacts/architecture/openapi.yaml` (current behaviour, no migration).

**Acceptance**: `grep -rn api-designer context/ artefacts/` empty outside archive; the canonical path is
identical in the architect definition, `design.yaml`, `artefacts/README.md` and the ADR; the OpenAPI skill is
listed in the architect's frontmatter.

**Write scope**: as TASK-014, plus `artefacts/architecture/architecture-decision.md` (append only).

---

### TASK-016 — Analyst merge → `harness-analyst`

**Completed 25 Oct 2026** before TASK-013, on direct user request, by Cline. Gate green: validator for
`harness-analyst.md`, adapters 4 created / 1 updated, drift in sync, 186 tests, acceptance grep empty; output
paths unchanged. Repo-wide validator stays red on 12 legacy agents (baseline 14/18) — owned by
TASK-014/015/019. Deviation: the composite "Workflow Health Score X/100" was dropped (per-metric rubric kept)
because `retrospective.yaml` §workflow_rules prohibits health scores — rule wins over agent.

**Decision**: one retrospective measurement agent, `model: medium`, lens selected by the task prompt.
Rationale: identical frontmatter pools, identical data sources (interruptions JSONL, session-log JSONL,
incidents, git `Agent-Session:` trailers), identical trigger. Only the analysis lens differs — "how", not "who".

**Files**

- Create `context/agents/harness-analyst.md` — template shape; `standards`: `workflow-standards.md`,
  `agent-standards.md`, `doc-standards.md`, `coding-standards.md`, `testing-standards.md`,
  `tech-standards.md`; `rules`: `bash-environment.md`, `multi-agent-collaboration.md`, `tech-writing.md`,
  `workspace-conventions.md`; `skills`: `multi-agent-workflows.md`, `workflow-analysis.md`,
  `tokenomics-audit.md`; body keeps the shared data-source inventory; outputs
  `artefacts/build/efficiency-report.md`, `artefacts/build/efficiency-data/`,
  `artefacts/build/tokenomics-report.md`.
- Create `context/skills/workflow-analysis.md` — the macro lens moved from `workflow-analyst.md`
  (task/handoff/cycle-time/bottleneck metrics, scoring rubric, report format; roughly L48–216 and L340–420).
- Create `context/skills/tokenomics-audit.md` — the micro lens moved from `tokenomics-analyst.md` (six audit
  lenses, model-tier conformance vs `context/models.yaml`, autonomy rate, context bloat, token economics).
- Delete `context/agents/workflow-analyst.md` and `context/agents/tokenomics-analyst.md`.
- `context/workflows/continuous-improvement.yaml` L38–44 — review phase `agents: [harness-analyst]`; notes name
  the lens in the task prompt and keep the two specialisation descriptions as lens descriptions; if
  parallelism matters, spawn twice with disjoint outputs (`efficiency-report.md` vs `tokenomics-report.md`).
- `context/workflows/retrospective.yaml` L8 — `workflow-analyst` → `harness-analyst`; note the default lens
  (workflow-analysis).
- `context/agents/README.md` L28–29 — replace both rows with `harness-analyst` (medium).
- `context/models.yaml` L61 — `@workflow-analyst, @tokenomics-analyst` → `@harness-analyst`.
- `context/scripts/generators/adapters/core/agents_md.py` L41–42 — replace both entries with `'harness-analyst'`.
- `context/docs/*` — counts and references.

**Acceptance**: `grep -rn 'workflow-analyst\|tokenomics-analyst' context/` empty outside archive; both
workflows dispatch `harness-analyst`; both lens skills exist and appear in the agent frontmatter; output paths
unchanged so existing retrospective consumers still resolve.

**Write scope**: as TASK-014.

---

### TASK-017 — Fix the TASK-012 lanes inconsistency

**Decision**: the harness lane is implemented by `@harness-analyst` (matching the TASK-013 boundary table:
"Harness implements, tech-lead gates"). `@functional-tester` writes the RED validator tests. `@orchestrator`
keeps only the bootstrap exception (creating the role that does not yet exist) and ownership of `HANDOFF.md` /
`tasks.md` / `bugs.md`.

**Files**

- `artefacts/build/tasks-agent-context-drift.md` §Fix lanes — harness lane Implementer becomes
  `@harness-analyst`; `@functional-tester` for validator behaviour (RED first); the artefacts list gains
  `context/models.yaml` and `context/scripts/generators/` (TASK-013 write scope); add the note: orchestrator
  writes task files/HANDOFF and bootstraps the role only.
- The TASK-012 row in §Task Index — description references the corrected table; `Blocked By` gains TASK-017.
- Re-read TASK-006, TASK-007 and TASK-009 assignments; confirm they read correctly once the harness owner
  exists (they already name `@harness-analyst` / `@devops`).

**Acceptance**: lanes table, TASK-012 description, TASK-013 boundary table and write scope all agree; no task
in this file implies a gate agent (`@tech-lead`, `@code-reviewer`, `@principles-reviewer`, `@security-tester`)
implements harness changes.

---

### TASK-018 — Extend the `harness-analyst` skill/standards pools

**Completed 25 Oct 2026** — the four standards and six machinery skills landed in the frontmatter with the two
lens skills (eight total); every entry resolves under `context/standards/` or `context/skills/` — no phantom
paths.

**Decision** (roster review §1): the harness role needs the machinery skills in its durable frontmatter, not
only glob-resolved ones.

**Files** — §Harness-analyst spec:

- `skills` += `python-scripting.md` — validators and generators are PEP 723 scripts under `context/scripts/**/*`.
- `skills` += `git-subrepo-operations.md` — `context/` is a git-subrepo; pushing harness changes upstream is
  this role's job.
- `skills` += `agent-sandbox.md` — sandbox-safe command execution for generator/validator runs.
- `standards` += `workflow-standards.md` — `context/workflows/` is in the harness write scope.
- The TASK-013 row — `Blocked By` gains TASK-018; acceptance criteria mention the full pool (4 standards,
  6 skills).

**Acceptance**: the spec table lists all four standards and all six machinery skills (eight skills in total
once the two measurement lenses are included); TASK-013 acceptance references them; every listed path exists
under `context/skills/` or `context/standards/` (no phantom entries — see this incident's own root cause).

---

### TASK-019 — Single `devops` (absorb `database-designer`, extract skills, `small` → `medium`)

**Completed 25 Oct 2026** by Cline (`@harness-analyst` role). Gate: `devops.md` passes
`agent_definitions.py`; adapters 2 created / 4 updated, orphaned `.agents/skills/database-designer` and
`.github/prompts/database-designer.prompt.md` removed by hand; drift in sync; 186 tests; Typst formatting
clean on all changed markdown. Repo-wide validator red on 8 legacy agents (down from 9 — `devops` is the
agent fixed and `database-designer` the one retired). Acceptance grep for `database-designer` / `gcp-devops`
is empty outside this task file; `supabase db push` appears only in the "Wrong" mapping row of
`supabase-operations.md`; all workflows dispatch existing agents (15 role files on disk).

**Deviations** (deliberate): (1) `context/workflows/deploy.yaml` was updated as well — its three devops
notes pointed at `context/agents/devops.md` "Mode 2", which no longer exists; they now point at
`gcp-deployment.md`. (2) `context/README.md` skills inventory and the skills catalogue in
`agentic-framework-reference.md` gained `database-design` and `gcp-deployment`. (3) `architecture-fidelity.md`
was **not** added to the skills list — the absorbed boundary is written into the body instead, because the
skill's globs cover `openapi.yaml` rather than `data-model.md`. (4) The `database-design.md` ER-diagram
example gained a blank line to satisfy `verify_typst_formatting.py`. (5) `context/agents/cursor-workflow-helper.mdc`
still named `database-designer.md` and the non-existent `gcp-devops.md`; it is not globbed by the validator
(`*.md` only), so it was edited by hand to keep the acceptance grep honest — the rest of that file's drift
(`./artefacts/`, `context/agents/CLAUDE.md`) is out of this task's scope.

**Follow-on (same day, human direction)**: `context/rules/supabase.md` deleted. A rule file that asserts
*how to use a tool* duplicates the skill that owns the same domain, globs, and workflows — the skill is the
right home. Its full intent moved into `supabase-operations.md` §1 (MCP-only tooling, forbidden
`db push`/`db query`/`db reset`/`psql`, the single `supabase functions deploy` whitelist, never assume Docker,
the `schema_migrations` audit insert, and timestamp-bloat prevention); later sections renumbered, §5 → §6.
Four agents dropped `supabase.md` from `rules:`; `functional-tester` and `tech-lead` gained
`supabase-operations.md` in `skills:` so the guidance still reaches them, and `python-coder`'s stale
"supabase CLI" tool entry became "supabase MCP". `supabase.py` is unchanged in behaviour and now cites the
skill; pre-commit hook names, `context/README.md`, both framework docs and `validators/README.md` retargeted.
Gate: `agent_definitions.py` 8/14 legacy (unchanged), adapters 10 updated, drift in sync, 186 tests,
`supabase.py` ✅.

**Decision**: one data and infrastructure owner spanning design-time schema, build-time migrations, Supabase
local/staging deployment and GCP deployment. Technology playbooks move to skills; the agent body keeps mode
dispatch plus the generic deploy procedure. `model: medium` — physical schema design is judgement work, and
every other design agent is medium or large. Rationale: `build.yaml`'s `schema-migration` phase (L53–64)
already assigns migrations to devops; the split with `database-designer` is by lifecycle phase, not domain.

**Files**

- `context/agents/devops.md` — `model: small` → `medium`; absorb from `context/agents/database-designer.md`
  §Constraints (L55–63: PostgreSQL default, normalisation, UUID PKs, `created_at`/`updated_at`, snake_case,
  FK and common-query indexes) and §Boundary Clarifications (L76–85: conceptual `data-model.md` from
  @solution-architect → physical schema; never modify `data-model.md`); deliverables gain
  `artefacts/database/` (`schema.sql`, `migrations/`, `er-diagram.md`, `design-decisions.md`);
  `standards:` += `doc-standards.md`; `skills:` += `database-design.md`, `mermaid-authoring.md`,
  `supabase-operations.md` (keep `agent-sandbox.md`, `agent-workflows.md`, `git-subrepo-operations.md`,
  `python-scripting.md`); fix `tools:` frontmatter to Supabase **MCP** (not CLI); replace the Mode 1 / Mode 2
  playbooks with mode dispatch + skill references + generic procedure (intake → plan → staging → validate →
  approval gate → rollback → log).
- Create `context/skills/database-design.md` from the absorbed conventions.
  `globs: ["**/migrations/*.sql", "**/supabase/**", "**/database_service/**", "**/stores/**", "artefacts/database/**"]`.
- Create `context/skills/gcp-deployment.md` from `devops.md` Mode 2 (L80–100): `terraform validate` and `plan`
  before apply, staging before production, explicit production approval, Cloud Run Functions Gen 2, Firebase
  Hosting, Workload Identity, region `europe-west2`, least privilege, encryption at rest and in transit,
  rollback plan mandatory. `globs: ["**/*.tf", "**/terraform/**", "artefacts/gcp/**"]`.
- Extend `context/skills/supabase-operations.md` with the Mode 1 deploy procedure (from `devops.md` L59–78):
  pending-migration check, edge-function deploy, RLS validation against `pg_policies`, smoke test,
  deployment-log format, rollback steps.
- `context/rules/supabase.md` §1 — resolve the live contradiction: `devops.md` L70 says "via Supabase MCP or
  `supabase db push`" and L113 validates with `supabase db push --dry-run`, while the rule says "Never use the
  Supabase CLI" and the skill marks `supabase db push` as wrong. Keep MCP for queries and migrations; whitelist
  only CLI operations MCP cannot perform — verify against `context/mcp/mcp.json` (the skill's mapping table has
  no edge-function-deploy tool, so `supabase functions deploy` is the expected whitelist). Replace the dry-run
  validation with a schema assertion via `execute_sql`.
- Delete `context/agents/database-designer.md`.
- `context/workflows/design.yaml` L30–34 — `design-contracts` agents: `database-designer` → `devops`; rename the
  phase "Physical Schema Design"; update L118 notes and the L136 dependency comment.
- `context/workflows/build.yaml` L63 — verify the "devops operates in local mode" note still matches the
  rewritten definition.
- `context/agents/README.md` L11 and L25 — delete the database-designer row; devops purpose widened,
  model `medium`.
- `context/models.yaml` — L29 remove "Infrastructure deployment commands (@devops)" from `small`; add devops to
  `medium` typical tasks; L58 "Schema and API design (@database-designer, @api-designer)" → "Schema design
  (@devops)" (coordinate with TASK-015, which removes the API half).
- `context/scripts/generators/adapters/core/agents_md.py` — L35 remove `'database-designer'`; L39 remove stale
  `'gcp-devops'` (no such agent exists).
- `context/templates/architecture-template.md` L3 — remove `database-designer` from the consumers list.
- `artefacts/README.md` L12 — architecture row primary agents → `@solution-architect`, `@devops`.
- `context/docs/*` — counts and references.

**Acceptance**: `devops` is `medium` in the definition and inventory;
`grep -rn 'supabase db push' context/agents/ context/skills/` returns only the §1 forbiddance and the "Wrong"
mapping row in `supabase-operations.md` (amended by the follow-on note above, which deleted the rule file);
no reference to `database-designer` or `gcp-devops` remains outside archive; the
design workflow dispatches only existing agents; the four validation commands pass.

**Write scope**: as TASK-014, plus `context/rules/supabase.md`.

---

## Findings

**Root cause**: agent definitions carry three hand-maintained copies of the same obligations — YAML
frontmatter, a "Required Rules (Must Follow!)" body table, and the orchestrator's always-apply list. Only the
frontmatter is machine-validated (`agent_definitions.py` L71–90), so the body tables drifted to reference eight
rule files that do not exist. CI reports `✅ All 18 agent definitions valid` while every subagent is instructed
to read phantom paths and silently falls back to an 8-word paraphrase.

### Phantom references

Zero matches anywhere in the repo (verified with `find`, excluding `.git` and `node_modules`):

| Referenced name | Reality | Agents |
|-----------------|---------|--------|
| `handoff-hygiene.md` | does not exist | 18 |
| `escalation.md` | does not exist | 18 |
| `british-english.md` | does not exist | 17 |
| `git-commits.md` | folded into `workspace-conventions.md` §2 | 8 |
| `quality-gates.md` | folded into `testing.md` §1 | 3 |
| `output-locations.md` | folded into `workspace-conventions.md` §1 | 3 |
| `type-safety.md` | does not exist | 2 |
| `secrets-management.md` | file is `secrets.md` | 2 |

### Secondary defects

- `context/agents/python-coder.md` rules table lists `tdd-workflow.md` and `architecture-fidelity.md` — both
  live in `context/skills/`, not `context/rules/`.
- `python-coder.md` frontmatter declares `testing.md`; its table cites `quality-gates.md` instead.
- `functional-tester.md` L39 says "Read all 3 standards files" while frontmatter declares 4
  (`context-framework.md` orphaned).
- CI blind spot: `agent_definitions.py` L71–90 validates frontmatter only; `orchestrator.md` is in
  `SKIPPED_FILES` (L30).

### Resolution — TASK-002, 005, 006 (25 Oct 2026)

Body rule tables are gone from 14 definitions; the frontmatter is the single source of truth and every
surviving constraint carries a `file.md §section` attribution. `orchestrator` deferred by human direction
(TASK-007). Gate green after every commit: `agent_definitions.py` 14/14, adapters regenerated, drift in
sync, 186 tests.

| Agent | Commit | Notes |
|-------|--------|-------|
| `tech-lead` | `3944b00` | gate procedure and boundary table kept; wiring check now cites the architect's tracing method |
| `functional-tester` | `0161ca2` | context-framework.md restored to the standards list (was "read all 3"); RED/GREEN and gap protocol kept |
| `ui-designer` | `3bc917f` | design constraints re-attributed to `ui-dev.md`, `visual-standards.md`, `mermaid-authoring.md` |
| `ui-tester` | `93d38d1` | validity bar attributed to `workflow-standards.md` §9 |
| `security-tester` | `f6ba141` | review scope attributed to `security-standards.md` §Boundaries and §LLM/AI APIs |
| `principles-reviewer` | `d2e224d` | design and implementation review become explicit modes |
| `documentation` | `8cd2f0c` | archive procedure repointed from `doc-standards.md` §2.5 to §2.6 |
| `typescript-coder` | `d57b842` | seven phantom rule names replaced by `typescript-environment.md`, `secrets.md`, `ui-dev.md` |
| `code-reviewer` | `27fb423` | frontmatter advertised the forbidden Supabase CLI |
| `agent-template.md` | `3ee0fab` | TASK-002: attribution rule and frontmatter supremacy stated; no body table permitted |
| `bash-environment.md`, `agent-sandbox.md` | `9d936de` | the last two `escalation.md` phantom references repointed to `multi-agent-collaboration.md` §1 |

`python-coder`, `harness-analyst`, `product-owner`, `solution-architect` and `devops` were already in template
shape; `code-reviewer` passed the validator but carried the CLI drift above.

### Resolution — TASK-006 audit pass (25 Oct 2026)

Structural conformance was already green, so this pass audited content: every `file.md §section`
citation in the 14 non-orchestrator definitions was resolved against the real file and the real
heading, and every constraint bullet that paraphrased a rule was given its source. 81 citations
checked; only `orchestrator.md` §Rule Resolution remains, and that list is TASK-007's scope by
definition.

| Agent | Commit | Notes |
|-------|--------|-------|
| `ui-tester` | `5ef7962`, `e4aac57` | two files named `ui-testing.md` (rules and skills) were cited interchangeably; evidence bullets attributed to `workflow-standards.md` §9 |
| `documentation` | `8a340b9` | §2.6 citation did not resolve as written (stray colon) |
| `harness-analyst` | `4810273` | lens rule stated twice; projection ban stated twice; three YAML "§" pseudo-sections corrected to keys and phases; `L77` line citation replaced |
| `devops` | `453da10`, `42d7c24` | `mcp_tools:` → `tools:`; trigger added to description; procedure restatements dropped; platform enumeration replaced by `gcp-deployment.md` §Platform Shape; schema bullets attributed to `database-design.md` §Physical Design Rules |
| `product-owner` | `9e98090` | `mcp_tools:` → `tools:`; `exa_web_search`/`tavily_search` were MCP method names, not server names |
| `solution-architect` | `e42b6f0`, `3797da5` | `mcp_tools:` → `tools:`; Lean and technology constraints attributed |
| `functional-tester` | `94dbf8c` | five unattributed bullets attributed |
| `python-coder` | `7cc7307` | eight bullets became five, each attributed |
| `typescript-coder` | `dea984c` | module constraint attributed |

**Residual findings for later tasks** (not TASK-006 defects, recorded so they are not lost):

1. Tool declarations use the roster convention `{server} MCP` (`supabase MCP`), while `context/mcp/mcp.json`
   registers `supabase`. Nothing validates the name, so a definition can declare a capability that no
   runtime exposes — the same failure class as a phantom rule file. Candidate check for TASK-004.
2. No validator resolves `file.md §section` citations today. The audit script used here
   (resolve file, then match heading) found six defects across five definitions in one pass — worth
   promoting into `context/scripts/validators/` with a RED test first (TASK-003, TASK-004).
3. `context/agents/cursor-workflow-helper.mdc` cites `context/agents/CLAUDE.md` and uses `./artefacts/`
   paths. Not a definition and not globbed by the validator; same drift class, unowned.

### Resolution — TASK-003, TASK-004 (25 Oct 2026)

The body-blind spot is closed. `agent_definitions.py` now resolves two body shapes: a `Source` cell in a
body rule table, and an inline `file.md §section` citation (residual finding 2 promoted into the validator,
which is why the check is not table-only). Both name a file under `context/` — searched in `rules/`,
`skills/`, `standards/`, `agents/`, `templates/`, `workflows/`, `docs/` — and, when a section is named, a
heading that file carries. Section matching is deliberately generous (case/punctuation folded, abbreviations,
bare section numbers, citations trailing into prose) so it catches deleted headings, not shorthand. Errors
carry the offending line number.

| Item | Detail |
|------|--------|
| RED | `d7c7271` — eight tests, four failing: phantom `Source` file, unresolved `Source` section, phantom inline citation file, unresolved inline citation section. The four positives (resolvable table, resolvable inline citation, `Source`-less table ignored, existing suite) pinned the false-positive boundary first. |
| GREEN | `agent_definitions.py` — `_source_cells`, `_validate_body_citations`, `_resolve_context_file`, `_section_resolves`; `file.md` is the template placeholder and is skipped, not resolved. |
| Gate | `agent_definitions.py` 14/14 valid, adapters 61 unchanged, drift in sync, 193 tests, ruff clean. Repo-wide run is now fully green — the 8 legacy failures recorded in TASK-019 are gone. |
| Scope note | No agent definition carries a body rule table today (TASK-005/006 removed them), so the `Source` branch is forward-looking; the inline-citation branch is what protects the current definitions. |
| Deviation | `context/scripts/validators/README.md`, `context/scripts/tests/README.md`, and both framework docs were updated with the new check — a validator nobody can find in the docs is the same discoverability gap that produced this incident. |

---

## Fix lanes (TASK-012, TASK-017)

`continuous-improvement.yaml` §fix declares `agents: [python-coder, typescript-coder]` and the note "Delegate
implementation changes to appropriate agents" — two coders plus an undefined word, so *appropriate* resolves to
*coder*. The unstated assumption is that a framework fix is a code fix; this incident disproves it. Of the 13
original tasks, one is application code (TASK-004), seven edit the agent-facing harness (TASK-002, 003, 005,
006, 007, 012, 013) and five are process — diagnosis, design, CI wiring, gate, record (TASK-001, 008, 009, 010,
011).

Proposed lanes, for TASK-012 to ratify:

| Lane | Artefacts | Implementer | Gate |
|------|-----------|-------------|------|
| code | `services/**/src/`, `tests/` | `@python-coder` / `@typescript-coder`, after RED | `@tech-lead` |
| harness | `context/agents/`, `context/rules/`, `context/skills/`, `context/templates/`, `context/workflows/`, `context/scripts/validators/`, `context/scripts/generators/`, `context/models.yaml` | `@harness-analyst`; `@functional-tester` for validator behaviour (RED first) | `@tech-lead` |
| docs | `artefacts/`, service `README.md`, user guides | `@documentation` | `@tech-lead` (informal) |

- **Edge case** TASK-012 must resolve: `agent_definitions.py` is harness intent implemented in Python. The
  resolving rule — **lane by intent, implementer by artefact, gate by risk** — needs writing down, because
  nothing today distinguishes a validator from a product module.
- TASK-012 must also set a real ceiling for the orchestrator `< 50 lines per file` exception, or state why
  agent definitions are exempt: they run 80–140 lines, so the limit is already bent by TASK-005/006.

### Roster gap — closed by TASK-013

No agent owned the context framework, which is why harness work defaulted to `@orchestrator` as an exception
and then to `@python-coder` by language. `@tech-lead` cannot absorb it: it is the gate, and `tech-lead.md` L77
("Don't rewrite code — describe what needs to change") is only meaningful if the reviewer is not the author.

| Activity | Owner |
|----------|-------|
| Decide the taxonomy and lane boundaries | `@solution-architect` (TASK-012, TASK-008) |
| Apply it to definitions, rules, templates, workflows | `@harness-analyst` (TASK-002, 005, 006, 007) |
| Approve or reject the result | `@tech-lead` (TASK-010) |

`@orchestrator` retains TASK-013 because the role does not exist yet to create itself, and keeps its ownership
of spawn prompts, `HANDOFF.md`, `tasks.md`, `bugs.md`.

---

## Harness-analyst spec (TASK-013)

**Completed 25 Oct 2026** — `harness-analyst.md` carries the combined contract, is registered at `large` in
`context/agents/README.md` and `context/models.yaml`, and every former harness-owner reference names it. Gate
green: validator, adapters regenerated, drift, 186 tests. TASK-018 landed within this work; TASK-012 (fix-phase
lane wiring) is outstanding. The definition keeps both measurement lenses beside the six machinery skills
(eight total) so TASK-016's retrospective function survives.

| Field | Value |
|-------|-------|
| `name` | `harness-analyst` |
| `model` | `large` — must hold the full harness contract (frontmatter ↔ rules ↔ skills ↔ injected prompts) at once; a wrong edit propagates to every spawn |
| `standards` | `agent-standards.md`, `context-framework.md`, `doc-standards.md`, `workflow-standards.md` |
| `rules` | `bash-environment.md`, `multi-agent-collaboration.md`, `tech-writing.md`, `workspace-conventions.md` |
| `skills` | `agent-sandbox.md`, `agent-workflows.md`, `architecture-fidelity.md`, `git-subrepo-operations.md`, `multi-agent-workflows.md`, `python-scripting.md`, `tokenomics-audit.md`, `workflow-analysis.md` |

First six skills = TASK-018 machinery pool; the last two = TASK-016 measurement lenses.

**Write scope**: `context/agents/`, `context/rules/`, `context/skills/`, `context/templates/`,
`context/workflows/`, `context/scripts/validators/`, `context/scripts/generators/`, `context/models.yaml`.
**Non-goals**: application code (`services/**`), any quality gate, human-facing documentation in `artefacts/`.

**Boundaries** — the reason the role exists:

| Agent | Division of labour |
|-------|--------------------|
| `@tech-lead` | Harness implements, tech-lead gates. `tech-lead.md` L77 forbids rewriting what it reviews |
| `@solution-architect` | Architect decides the taxonomy (TASK-012, TASK-008); harness applies it mechanically |
| `@orchestrator` | Orchestrator owns spawn prompts, `HANDOFF.md`, `tasks.md`; harness owns the definitions those spawns read |
| `@functional-tester` | Tester writes validator tests (RED); harness implements behaviour (GREEN) |
| `@python-coder` | Harness owns validators and generators as harness intent; coders own product modules |

**Non-negotiables** (in the agent body): a definition that references a file not on disk is a defect, not a
warning · change the agent to match the rule, never the rule to match the agent · every rule citation carries
`file.md §section`; a paraphrase without a source is a fork.

**Registration**: add to the `context/agents/README.md` inventory; `generate_adapters.py` propagates to
`AGENTS.md` and the runtime projections; `agent_definitions.py` and `adapter_drift.py` must pass.

---

## Design decision

Keep the two-layer pattern; eliminate the duplication. Frontmatter is the single source of truth and the body
table must be derived from it, verified by the validator, and attributed by file (`Source` column) so no
paraphrase survives without a pointer.

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
7. `@harness-analyst` exists, is registered in `context/agents/README.md`, passes `agent_definitions.py`, and owns every harness task — no gate agent implements.
