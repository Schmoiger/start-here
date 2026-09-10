# Tasks: Align start-here Context with Bollinger

**Branch**: `refactor/commit-framework`
**Status**: Planning
**Scope**: Port improvements from `/Users/avi/Repos/bollinger/context` into `start-here/context` — agent frontmatter standardisation, rule renames/additions, template additions, workflow additions, README rewrites, script generator replacement.
**Design**: N/A
**Created**: 2026-04-12
**Note**: Some items from the CF-1–CF-15 refactor (bash-environment.mdc, prepare-commit-msg.py, continuous-improvement.yaml, build/bugfix/design.yaml, metrics-logging removal) are already done in this branch. Tasks below cover the remaining gaps.

---

## Task Index (required)

Update status immediately when work begins and when it completes. Every task in the index must have a matching specification section below.

Tasks grouped by disjoint file scope. Groups A–E can run in parallel. Group F is blocked by A (rule rename).

### Group A — Rules

Sequential within group (shared rule files).

| ID | Pri | Status | Blocked By | Task |
|----|-----|--------|------------|------|
| AL-1 | critical | pending | - | Rename conventional-commits.mdc → git-commits.mdc and sync content with bollinger |
| AL-2 | high | pending | - | Add supabase.mdc from bollinger |
| AL-3 | high | pending | - | Add handoff-hygiene.mdc (referenced in bollinger orchestrator.md) |
| AL-4 | medium | pending | - | Retire file-operations.mdc (superseded by bash-environment.mdc) |
| AL-5 | low | pending | - | Retire orchestrator-delegation.mdc (content merged into orchestrator.md) |

### Group B — Agents

Sequential within group (shared agent files; frontmatter updates touch every file).

| ID | Pri | Status | Blocked By | Task |
|----|-----|--------|------------|------|
| AL-6 | high | pending | AL-1 | Update orchestrator.md: model → opus, simplify body, update rules refs |
| AL-7 | high | pending | AL-1 | Update all agent frontmatter: remove allowed_tools, rename rule refs, add MCP tools |
| AL-8 | medium | pending | AL-1 | Remove gcp-devops.md agent (replaced by deploy.yaml workflow) |

### Group C — Templates

Parallel within group (no shared files).

| ID | Pri | Status | Blocked By | Task |
|----|-----|--------|------------|------|
| AL-9 | high | pending | - | Add architecture-template.md from bollinger |
| AL-10 | high | pending | - | Add design-template.md from bollinger |
| AL-11 | medium | pending | - | Lowercase template filenames (HANDOFF-TEMPLATE.md → handoff-template.md, TASK-PROMPT-TEMPLATE.md → task-prompt-template.md) |
| AL-12 | medium | pending | - | Remove handoff-schema.json and review-schema.json (schemas now in markdown) |
| AL-13 | medium | pending | - | Sync templates/README.md with bollinger version |

### Group D — Workflows

Parallel within group (no shared files).

| ID | Pri | Status | Blocked By | Task |
|----|-----|--------|------------|------|
| AL-14 | high | pending | - | Add deploy.yaml from bollinger |
| AL-15 | medium | pending | - | Add content.yaml from bollinger |
| AL-16 | medium | pending | - | Add full-test.yaml from bollinger |
| AL-17 | medium | pending | - | Rename default.yaml → build.yaml (or remove if build.yaml already created) |

### Group E — Scripts and Generator

Sequential within group (shared scripts dir).

| ID | Pri | Status | Blocked By | Task |
|----|-----|--------|------------|------|
| AL-18 | high | pending | - | Replace generate_claude_md.py with generate_agents_md.py from bollinger |
| AL-19 | medium | pending | - | Add supabase_boundary.py validator from bollinger |

### Group F — READMEs and AGENTS.md

Sequential (AGENTS.md regenerated from generator).

| ID | Pri | Status | Blocked By | Task |
|----|-----|--------|------------|------|
| AL-20 | high | pending | AL-18 | Regenerate AGENTS.md using new generator script |
| AL-21 | medium | pending | - | Sync context/README.md with bollinger version |
| AL-22 | medium | pending | - | Rewrite context/agents/README.md to match bollinger (minimal index only) |

---

## AL-1: Rename conventional-commits.mdc → git-commits.mdc and sync content

**Rationale**: Bollinger calls this file `git-commits.mdc`. It is the more authoritative name and all bollinger agent frontmatter references `git-commits.mdc`. Our CF-15/CF-8/CF-13 refactor added significant new content to `conventional-commits.mdc` (Orchestrator Commit Procedure, Who Commits, Pre-Commit formatting, interaction tracking fields, Pull Requests section). The rename preserves this work while aligning the filename.

**Files**:
- Rename `context/rules/conventional-commits.mdc` → `context/rules/git-commits.mdc`
- Check bollinger's `context/rules/git-commits.mdc` for any content our version is missing; merge in any gaps
- Update `context/README.md` quick-reference link
- Update `.pre-commit-config.yaml` (or its template) if the hook references the filename
- Update `context/scripts/generators/generate_agents_md.py` (or `generate_claude_md.py`) if it references the rule filename
- Update `AGENTS.md` Rules section

**Acceptance**: `conventional-commits.mdc` does not exist. All references to it are updated. `git-commits.mdc` contains all content from both the CF refactor and bollinger.

---

## AL-2: Add supabase.mdc

**Rationale**: Bollinger has a `rules/supabase.mdc` covering Supabase MCP operations, migration workflow with `schema_migrations` tracking, autovacuum tuning, and replication slot management. Several agents (database-designer, python-coder, functional-tester, tech-lead) reference it in bollinger.

**Files**:
- Copy/create `context/rules/supabase.mdc` — content: Supabase-specific operations via MCP tools, migration workflow, autovacuum tuning, replication slot management. Read the bollinger version at `/Users/avi/Repos/bollinger/context/rules/supabase.mdc` for exact content.

**Acceptance**: `context/rules/supabase.mdc` exists with Supabase operation rules and MCP tool guidance.

---

## AL-3: Add handoff-hygiene.mdc

**Rationale**: Bollinger's `orchestrator.md` frontmatter references `handoff-hygiene.mdc` as a required rule, but the file is not yet present in start-here.

**Files**:
- Check if `context/rules/handoff-hygiene.mdc` exists in bollinger at `/Users/avi/Repos/bollinger/context/rules/handoff-hygiene.mdc`
- If it exists: copy it to `context/rules/handoff-hygiene.mdc`
- If it doesn't exist: create a stub with the handoff update requirements already documented in agent-standards.md §3.4 (update HANDOFF.md before spawning, write dispatch.md, commit per subtask)

**Acceptance**: `context/rules/handoff-hygiene.mdc` exists.

---

## AL-4: Retire file-operations.mdc

**Rationale**: Bollinger does not have `file-operations.mdc`. Its content (tool substitution guidance) was superseded by `bash-environment.mdc` created in CF-1.

**Files**:
- Archive `context/rules/file-operations.mdc` to `context/rules/archive/` (do not delete)
- Remove any remaining references to it in agent frontmatter (handled in AL-7)
- Update `context/README.md` rules table

**Acceptance**: `file-operations.mdc` not referenced by any active agent. Archived copy retained.

---

## AL-5: Retire orchestrator-delegation.mdc

**Rationale**: Bollinger does not have this file. Its content has been absorbed into `orchestrator.md` (Context Budget Test, Delegation table, May Do Directly list added in CF-4).

**Files**:
- Archive `context/rules/orchestrator-delegation.mdc` to `context/rules/archive/` if it exists
- Remove any references from agent frontmatter

**Acceptance**: `orchestrator-delegation.mdc` not referenced by any active agent.

---

## AL-6: Update orchestrator.md to match bollinger model

**Rationale**: Bollinger's orchestrator uses `opus` (more capable for coordination), has simplified body text (concise delegation principle vs verbose step-by-step tables), updated rule references (`git-commits.mdc` not `conventional-commits.mdc`, added `handoff-hygiene.mdc`), and refined spawning guidance (task-prompt-template usage, model parameter passing, artefact template selection).

**Files**:
- `context/agents/orchestrator.md` frontmatter: change model from `sonnet` → `opus`
- `context/agents/orchestrator.md` frontmatter `rules:`: replace `conventional-commits.mdc` with `git-commits.mdc`; add `handoff-hygiene.mdc`; remove `doc-standards.md` and `coding-standards.md` if present (bollinger removed them — orchestrator doesn't apply these directly)
- `context/agents/orchestrator.md` body: read bollinger version at `/Users/avi/Repos/bollinger/context/agents/orchestrator.md` and compare. Adopt the concise delegation principle. Keep CF-4's Context Budget Test and May Do Directly list (these are not in bollinger yet). Keep CF-1's Commit Procedure. Merge the spawning guidance (task-prompt-template, model parameter, artefact template selection).

**Acceptance**: orchestrator.md uses opus, references git-commits.mdc and handoff-hygiene.mdc, has concise delegation section, retains Commit Procedure and Context Budget Test from CF refactor.

---

## AL-7: Update all agent frontmatter

**Rationale**: Bollinger agents have standardised frontmatter: no `allowed_tools` list (tools are unrestricted for most agents), `rules:` references `git-commits.mdc` not `conventional-commits.mdc`, no `file-operations.mdc`, added `bash-environment.mdc`, added `supabase.mdc` where relevant, added `chrome-devtools` MCP tool for UI/testing agents.

**Agents to update** (read each one, apply changes):
- `agents/code-reviewer.md` — remove `allowed_tools`, add `chrome-devtools` and `supabase` to mcp_tools, rename rule refs
- `agents/tech-lead.md` — change model if different, remove `allowed_tools`, add `supabase` to mcp_tools, rename rule refs
- `agents/python-coder.md` — remove `allowed_tools`, add `supabase` to mcp_tools, rename rule refs
- `agents/typescript-coder.md` — remove `allowed_tools`, add `chrome-devtools` to mcp_tools, rename rule refs
- `agents/ui-designer.md` — remove `allowed_tools`, add `chrome-devtools` to mcp_tools, rename rule refs
- `agents/database-designer.md` — remove `allowed_tools`, add `supabase.mdc` to rules and `supabase` to mcp_tools, rename rule refs
- `agents/functional-tester.md` — update description to reference "Detroit-school TDD (intent-first, tests before implementation)", remove `allowed_tools`, add `supabase` to mcp_tools and `supabase.mdc` to rules, rename rule refs
- `agents/solution-architect.md` — remove `allowed_tools`, add `supabase` to mcp_tools, rename rule refs
- `agents/ui-tester.md`, `agents/visual-designer.md`, `agents/documentation.md`, `agents/product-owner.md`, `agents/product-expert.md`, `agents/api-designer.md`, `agents/workflow-analyst.md` — rename rule refs (conventional-commits → git-commits), remove file-operations.mdc if present

**Acceptance**: No agent frontmatter references `conventional-commits.mdc`, `file-operations.mdc`, or `orchestrator-delegation.mdc`. `allowed_tools` removed from all. MCP tools added where applicable.

---

## AL-8: Remove gcp-devops.md agent

**Rationale**: Bollinger does not have `agents/gcp-devops.md`. GCP deployment is handled by `workflows/deploy.yaml` instead.

**Files**:
- Archive `context/agents/gcp-devops.md` to `context/agents/archive/`
- Remove from any workflow YAML that references it
- Remove from AGENTS.md agent reference section

**Acceptance**: `gcp-devops.md` not referenced by any active workflow or AGENTS.md section.

---

## AL-9: Add architecture-template.md

**Rationale**: Bollinger has this template (required by solution-architect). Start-here does not.

**Files**:
- Read `/Users/avi/Repos/bollinger/context/templates/architecture-template.md`
- Copy to `context/templates/architecture-template.md`

**Acceptance**: File exists at `context/templates/architecture-template.md`.

---

## AL-10: Add design-template.md

**Rationale**: Bollinger has this template (required by ui-designer). Start-here does not.

**Files**:
- Read `/Users/avi/Repos/bollinger/context/templates/design-template.md`
- Copy to `context/templates/design-template.md`

**Acceptance**: File exists at `context/templates/design-template.md`.

---

## AL-11: Lowercase template filenames

**Rationale**: Bollinger standardises template filenames to lowercase. Start-here has `HANDOFF-TEMPLATE.md` and `TASK-PROMPT-TEMPLATE.md` (uppercase).

**Files**:
- Rename `context/templates/HANDOFF-TEMPLATE.md` → `context/templates/handoff-template.md` (use Bash: `mv`)
- Rename `context/templates/TASK-PROMPT-TEMPLATE.md` → `context/templates/task-prompt-template.md` (use Bash: `mv`)
- Update any references in agent definitions, AGENTS.md, standards, or READMEs

**Acceptance**: No uppercase template filenames. All references updated.

---

## AL-12: Remove JSON schema files

**Rationale**: Bollinger removed `handoff-schema.json` and `review-schema.json`. Schemas are now expressed in the markdown templates themselves.

**Files**:
- Archive `context/templates/handoff-schema.json` to `context/templates/archive/` (if it exists)
- Archive `context/templates/review-schema.json` to `context/templates/archive/` (if it exists)

**Acceptance**: No JSON schema files in active templates directory.

---

## AL-13: Sync templates/README.md

**Rationale**: Bollinger's templates/README.md has a clearer structure: renamed "Template Index", added "How template selection works" explanation (orchestrator selects, agents don't), and a unified table of all templates with output types.

**Files**:
- Read `/Users/avi/Repos/bollinger/context/templates/README.md`
- Read `context/templates/README.md`
- Update start-here version to adopt the heading rename, "How template selection works" section, and unified table format

**Acceptance**: templates/README.md has "Template Index" heading and "How template selection works" section.

---

## AL-14: Add deploy.yaml

**Rationale**: Bollinger has a dedicated GCP cloud deployment workflow. Start-here has no equivalent.

**Files**:
- Read `/Users/avi/Repos/bollinger/context/workflows/deploy.yaml`
- Copy to `context/workflows/deploy.yaml`

**Acceptance**: `context/workflows/deploy.yaml` exists.

---

## AL-15: Add content.yaml

**Rationale**: Bollinger has a human-facing content creation workflow using writing personas. Start-here's `documentation-for-humans.yaml` (if it exists) may be superseded by this.

**Files**:
- Read `/Users/avi/Repos/bollinger/context/workflows/content.yaml`
- Copy to `context/workflows/content.yaml`
- If `context/workflows/documentation-for-humans.yaml` exists, archive it

**Acceptance**: `context/workflows/content.yaml` exists.

---

## AL-16: Add full-test.yaml

**Rationale**: Bollinger has a full regression suite workflow. Start-here does not.

**Files**:
- Read `/Users/avi/Repos/bollinger/context/workflows/full-test.yaml`
- Copy to `context/workflows/full-test.yaml`

**Acceptance**: `context/workflows/full-test.yaml` exists.

---

## AL-17: Rename default.yaml → build.yaml (or verify already done)

**Rationale**: Bollinger uses `build.yaml` as the primary workflow name. Start-here has `default.yaml`. Our CF-5 agent may have already created `build.yaml` — if so, archive `default.yaml`.

**Files**:
- Check if `context/workflows/build.yaml` already exists (created in CF-5)
- If yes: archive `context/workflows/default.yaml` (if it still exists)
- If no: rename `default.yaml` → `build.yaml`
- Update `context/README.md` workflows section

**Acceptance**: `build.yaml` is the primary workflow. `default.yaml` does not exist in active workflows directory.

---

## AL-18: Replace generate_claude_md.py with generate_agents_md.py

**Rationale**: Bollinger replaced `generate_claude_md.py` with `generate_agents_md.py` (generates AGENTS.md from agent definitions and workflows, not CLAUDE.md which no longer exists as a separate file).

**Files**:
- Read `/Users/avi/Repos/bollinger/context/scripts/generators/generate_agents_md.py`
- Copy to `context/scripts/generators/generate_agents_md.py`
- Archive `context/scripts/generators/generate_claude_md.py`
- Update any references to the old script in AGENTS.md maintenance section and context/README.md

**Acceptance**: `generate_agents_md.py` exists. `generate_claude_md.py` archived. References updated.

---

## AL-19: Add supabase_boundary.py validator

**Rationale**: Bollinger has a `scripts/validators/supabase_boundary.py` that validates Supabase schema and API boundary constraints.

**Files**:
- Read `/Users/avi/Repos/bollinger/context/scripts/validators/supabase_boundary.py`
- Copy to `context/scripts/validators/supabase_boundary.py`
- Add hook to `.pre-commit-config.yaml` template if bollinger has one

**Acceptance**: `supabase_boundary.py` exists in validators directory.

---

## AL-20: Regenerate AGENTS.md

**Rationale**: After renaming workflows, adding/removing agents, and updating frontmatter, AGENTS.md must be regenerated to reflect current state.

**Files**:
- Run: `uv run python context/scripts/generators/generate_agents_md.py` (or the appropriate generator)
- Review output for accuracy — check that continuous-improvement workflow appears, gcp-devops is absent, git-commits.mdc referenced correctly

**Acceptance**: AGENTS.md reflects current agents, workflows, and rule references.

---

## AL-21: Sync context/README.md

**Rationale**: Bollinger's README has a "For Humans" section explaining the Rules vs Standards distinction, updated orchestrator responsibilities, revised workflow list (build/design/prototype/deploy/bugfix/full-test/content/continuous-improvement), updated directory structure (mcp/mcp.json, prepare-commit-msg.py), and symlinks-first syncing guidance.

**Files**:
- Read `/Users/avi/Repos/bollinger/context/README.md`
- Read `context/README.md`
- Update start-here version to adopt:
  - "For Humans" section
  - Updated orchestrator responsibilities (concise principle)
  - Workflow list update
  - Directory structure update
  - Syncing guidance: symlinks preferred over copies

**Acceptance**: context/README.md has "For Humans" section, symlinks syncing guidance, updated workflow list.

---

## AL-22: Rewrite context/agents/README.md

**Rationale**: Bollinger's agents/README.md is a minimal index pointing to AGENTS.md. Start-here's version is a comprehensive multi-phase workflow guide — content that now lives in AGENTS.md itself.

**Files**:
- Read `/Users/avi/Repos/bollinger/context/agents/README.md`
- Rewrite `context/agents/README.md` to match bollinger's minimal "Agent Inventory" format

**Acceptance**: agents/README.md is a short index pointing to AGENTS.md, not a duplicate workflow guide.
