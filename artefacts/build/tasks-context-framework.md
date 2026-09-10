# Tasks: Context Framework Hardening

**Branch**: `{branch-name}`
**Status**: Planning
**Scope**: Port agent framework improvements to a new repo — centralised commits, two-tier escalation, compaction recovery, context budget delegation, continuous improvement workflow, interaction tracking, PR metrics
**Design**: N/A
**Created**: 2026-04-12
**Amended**: 2026-04-12 — added CF-13/14/15, regrouped by topic

---

## Task Index

Tasks grouped by disjoint file scope. Groups A–D can run in parallel. E and F are blocked by cross-group dependencies.

### Group A — agent-standards.md, orchestrator.md, AGENTS.md, escalation.mdc, coding-standards.md, task-prompt-template.md, bash-environment.mdc

Sequential within group (shared files: agent-standards.md, orchestrator.md).

| ID | Pri | Status | Blocked By | Task |
|----|-----|--------|------------|------|
| CF-1 | critical | pending | - | Centralise commits to orchestrator |
| CF-2 | critical | pending | CF-1 | Fix Rule Resolution to guarantee always-apply rules |
| CF-3 | high | pending | CF-2 | Add two-tier escalation with impact classification |
| CF-4 | high | pending | CF-2 | Add context budget test to orchestrator delegation |
| CF-9 | high | pending | CF-3 | Add continuous improvement workflow and incident log |

### Group B — git-commits.mdc, commit-message-template.md, conventional_commits.py, prepare-commit-msg.py/.sh, .pre-commit-config.yaml, workflow-analyst.md, tech-lead.md

Sequential within group (shared files: git-commits.mdc, commit-message-template.md, conventional_commits.py, .pre-commit-config.yaml).

| ID | Pri | Status | Blocked By | Task |
|----|-----|--------|------------|------|
| CF-15 | critical | pending | - | Add orchestrator commit procedure to git-commits rule |
| CF-8 | medium | pending | CF-15 | Add lint-before-stage to git-commits rule |
| CF-10 | medium | pending | CF-8 | Add prepare-commit-msg hook for token metrics |
| CF-13 | high | pending | CF-10 | Add interaction tracking fields to Agent-Session |
| CF-11 | low | pending | CF-10 | Remove agent self-reporting metrics infrastructure |

### Group C — build.yaml, bugfix.yaml, prototype.yaml, design.yaml

Sequential within group (shared file: build.yaml).

| ID | Pri | Status | Blocked By | Task |
|----|-----|--------|------------|------|
| CF-5 | high | pending | - | Add compaction recovery to all workflows |
| CF-6 | medium | pending | CF-5 | Add scope-collision checks for parallel dispatch |

### Group D — tasks-template.md

| ID | Pri | Status | Blocked By | Task |
|----|-----|--------|------------|------|
| CF-7 | medium | pending | - | Strengthen tasks template |

### Group E — workflow-standards.md (blocked by A + B)

| ID | Pri | Status | Blocked By | Task |
|----|-----|--------|------------|------|
| CF-12 | medium | pending | CF-3, CF-13 | Update workflow-standards for current model |

### Group F — pr-description-template.md (blocked by B)

| ID | Pri | Status | Blocked By | Task |
|----|-----|--------|------------|------|
| CF-14 | medium | pending | CF-13 | Add efficiency and autonomy metrics to PR template |

---

### CF-1: Centralise commits to orchestrator

**Rationale**: Parallel agents committing independently cause git ref-lock collisions (`O_CREAT | O_EXCL` on `.git/index.lock` does not retry). Centralising commits to the orchestrator eliminates this and ensures sequential, conflict-free staging.

**Files**:
- `context/standards/agent-standards.md` §4.4 — rewrite: agents do not commit, orchestrator commits on their behalf (format → stage → commit, one at a time). Push cadence: commit per task (orchestrator), push per sprint (orchestrator).
- `context/standards/agent-standards.md` §6.2 — change "agents shall only `git add`" to "agents shall only write or edit files within their scope"
- `context/standards/agent-standards.md` §6.3 — agents *request* commits by writing message to `/tmp/{task-id}_commit_msg.txt` and reporting file list. Remove all `git add`/`git commit` instructions.
- `context/standards/agent-standards.md` §6.4 — add "Commit sequentially" rule. Update mermaid diagram to show `files + msg` flow and `format + commit` step.
- `context/standards/coding-standards.md` workflow section — steps become: complete task → run tests → lint → write commit message → report back
- `context/standards/doc-standards.md` tasks.md guidance — change to "Agents do not commit — the orchestrator commits on their behalf"
- `context/agents/orchestrator.md` "May Do Directly" — add "Committing on behalf of subagents (format → stage → commit, one at a time)"
- `context/agents/orchestrator.md` file scope — change "paths it may `git add`" to "paths it may write or edit"
- `context/templates/task-prompt-template.md` FILE SCOPE — change to "You may only write or edit files within this scope". Add "Do NOT run `git add` or `git commit`"
- `context/templates/task-prompt-template.md` COMMIT section — add lint-before-reporting instructions with absolute-path commands. Write commit message to `/tmp/{task-id}_commit_msg.txt`
- `context/templates/task-prompt-template.md` REPORT BACK — add required fields: files changed, commit message path
- `context/rules/bash-environment.mdc` — change "Batch Edit then commit" to "Batch Edit then report"

**Acceptance**: grep for "git add" and "git commit" across context/ — only orchestrator-scoped references remain. No agent instruction says to commit directly.

---

### CF-2: Fix Rule Resolution to guarantee always-apply rules

**Rationale**: Rules with `alwaysApply: true` in `.mdc` frontmatter were silently dropped because Rule Resolution step 1 said "rules not in agent's frontmatter are never considered" — but `alwaysApply` rules weren't in agent frontmatter pools. The fix hardcodes always-apply rules in the orchestrator definition.

**Files**:
- `context/agents/orchestrator.md` frontmatter — add `standards:` and `rules:` fields listing the orchestrator's own dependencies
- `context/agents/orchestrator.md` Rule Resolution §1 — hardcode always-apply rules as an explicit list:
  - `bash-environment.mdc` — tool substitution, banned bash patterns
  - `git-commits.mdc` — commit message format, agents don't commit
  - `escalation.mdc` — escalate uncertainty to orchestrator
  - `output-locations.mdc` — output directory conventions
  - `british-english.mdc` — spelling conventions
- `context/agents/orchestrator.md` Rule Resolution §2 — agent-specific rules come from the agent's `rules:` frontmatter, filtered by glob match. Remove `alwaysApply` from the signal table (it's now handled by step 1).
- `context/standards/agent-standards.md` §1.1 — add "Rule Injection" subsection documenting that `alwaysApply: true` alone is NOT sufficient; must also be in the orchestrator's hardcoded list
- `AGENTS.md` On Start — add: "Read `context/agents/orchestrator.md`. Read each file in its `rules:` and `standards:` frontmatter."

**Acceptance**: The orchestrator's Rule Resolution procedure has two clearly separated steps — always-apply (hardcoded list) and agent-specific (glob-filtered pool). No rule relies solely on `alwaysApply: true` frontmatter to be injected.

---

### CF-3: Add two-tier escalation with impact classification

**Rationale**: Agents were confidently miscategorising high-impact deferrals (e.g. unbounded table growth) as low-impact scope decisions. The escalation rule only addressed uncertainty, not confident-but-wrong impact assessment. Additionally, the single escalation path (subagent → orchestrator → human) gave no guidance on when the orchestrator should resolve vs forward.

**Files**:
- `context/rules/escalation.mdc` description — update to "escalate uncertainty and high-impact deferrals"
- `context/rules/escalation.mdc` — add Orchestrator Triage table: resolve (single obvious remediation) vs forward to human (trade-offs, scope/architecture decisions). Default: forward if in doubt.
- `context/rules/escalation.mdc` — add Impact Classification table: scope deferrals (low) vs operational deferrals (high — unbounded growth, retention, resource limits)
- `context/rules/escalation.mdc` Escalate When — add: deferring work with operational/data-growth consequences; maintenance omission accumulating production infrastructure debt
- `context/rules/escalation.mdc` How to Escalate — add logging requirement: orchestrator logs every escalation to `artefacts/build/agent-interruptions.md`
- `context/standards/agent-standards.md` §4.6 — add Escalation as third interruption type with format template (Impact, Escalated to, Options considered, Resolution)

**Acceptance**: Escalation rule has three sections — Decision Matrix, Orchestrator Triage, Impact Classification. Interruptions log format includes Escalation type.

---

### CF-4: Add context budget test to orchestrator delegation

**Rationale**: The orchestrator's "May Do Directly" list was permissive enough (e.g. "Reading and summarising files", "Non-code config edits") that it could rationalise doing substantive work itself, consuming context that accelerates compaction.

**Files**:
- `context/agents/orchestrator.md` Delegation — add Context Budget Test: "Will this require reading more than ~2 files or producing more than ~50 lines of output? No → do it directly. Yes → delegate."
- `context/agents/orchestrator.md` Delegation — add: "Reading source code is investigation. Writing or editing beyond task management files is implementation. Both should be delegated."
- `context/agents/orchestrator.md` May Do Directly — remove "Reading and summarising files" and "Non-code config edits (YAML, JSON)". Keep: git ops, task management, coordinating outputs, committing on behalf of subagents, file ops when no content judgement needed.
- `context/agents/orchestrator.md` Why — update to reference context degradation, not context window survival

**Acceptance**: Orchestrator definition contains a Context Budget Test with a concrete threshold. "May Do Directly" list contains no items that imply reading or producing substantive content.

---

### CF-5: Add compaction recovery to all workflows

**Rationale**: After context compaction, the orchestrator loses in-memory dispatch context. Without recovery procedures, it cannot verify pending subagent reports against the correct criteria.

**Files**:
- `context/workflows/build.yaml` state_recovery — add 6-step recovery: re-read orchestrator rules, glob artefacts READMEs, git log, read HANDOFF.md phase, read validation block, read dispatch.md. Add critical_files list. Add compaction safety rules (incremental writes, commit after subtask, update HANDOFF before spawn, write dispatch.md).
- `context/workflows/bugfix.yaml` state_recovery — add orchestrator rule re-read as first step
- `context/workflows/prototype.yaml` — add state_recovery section and compaction safety rules (HANDOFF update before spawn, log agent scope, commit at milestones)
- `context/workflows/design.yaml` — add state_recovery section and compaction safety rules (incremental writes, HANDOFF update, scope logging for parallel design-contracts phase). Add critical_files list.

**Acceptance**: Every workflow YAML has a `state_recovery.after_compaction` section whose first step is re-reading orchestrator rules. Build and design workflows list critical_files.

---

### CF-6: Add scope-collision checks for parallel dispatch

**Rationale**: Parallel agents with overlapping file scopes cause commit collisions, stale-index failures, and file-content overwrites. The orchestrator needs an explicit pre-dispatch check.

**Files**:
- `context/workflows/build.yaml` parallel_planning — add 4-step scope-collision check: list scopes, reject overlaps, sequence shared paths, log verified matrix in HANDOFF
- `context/workflows/build.yaml` subtask schema — add `file_scope` field per subtask
- `context/workflows/build.yaml` phase notes — add "Every subtask declares file_scope; parallel subtasks have disjoint scopes"

**Acceptance**: build.yaml parallel_planning includes scope-collision check steps. Subtask schema includes `file_scope` field.

---

### CF-7: Strengthen tasks template

**Rationale**: Observed weaknesses in orchestrator-generated task files: missing status tracking, mixed terminology (wave/sprint/track), incomplete TypeScript dispatch chains, no file_scope per parallel group, checkboxes not updated, no push cadence.

**Files**:
- `context/templates/tasks-template.md` header — add `**Status**: Planning | In Progress | Complete`
- `context/templates/tasks-template.md` table format — rename to "Task Index (required)". Add "update status immediately" instruction. Add "Every task in the index must have a matching specification section". Remove Tokens/Duration columns.
- `context/templates/tasks-template.md` Parallelism Strategy — add terminology guidance (use "sprint", not "wave"/"track"/"phase"/"batch"). Add TypeScript dispatch chain requirement. Add `file_scope` per parallel group. Update examples to Sprint 1/Sprint 2 with file_scope and full RED/GREEN dispatch chains.
- `context/templates/tasks-template.md` Commit Strategy — add "Agents do not commit" note and push cadence (orchestrator pushes after each completed sprint)

**Acceptance**: Template uses "sprint" terminology consistently. Parallelism example includes file_scope and TypeScript dispatch. Commit Strategy references centralised commit model.

---

### CF-8: Add lint-before-stage to git-commits rule

**Rationale**: Pre-commit hooks with auto-fix (`ruff --fix`, `biome --write`) rewrite files after staging, causing working tree divergence from the git index. Agents then see "linter reverted my edit" and enter a revert loop. Formatting before staging means hooks find nothing to change.

**Files**:
- `context/rules/git-commits.mdc` — update "Applies to" to reference orchestrator. Add "Who Commits" section. Relabel "Commit Commands" as orchestrator-only.
- `context/rules/git-commits.mdc` — add "Pre-Commit: Format Before Staging" section with absolute-path commands for ruff and biome. Include: "Do NOT re-apply edits after a hook 'reverts' your changes."

**Acceptance**: git-commits rule has a "Who Commits" section and a "Pre-Commit: Format Before Staging" section with absolute-path format commands.

---

### CF-9: Add continuous improvement workflow and incident log

**Rationale**: The original retrospective workflow was metrics-driven and output-shaped (health scores, efficiency reports). In practice, framework improvements come from two sources: reactive (human reports a specific failure) and proactive (reviewing accumulated data for patterns). These share the same fix → record tail and belong in a single workflow with two modes. An incident log captures framework failure modes distinctly from interruptions (blocking moments) and metrics (telemetry).

**Files**:
- `context/workflows/continuous-improvement.yaml` — **new**. Two modes: `incident` (report → diagnose → fix → record) and `retrospective` (review → discuss → fix → record). Shared fix and record phases. Quality gate on `discuss` phase in retrospective mode only. Workflow rules: no vanity metrics, every finding must lead to a fixable gap, human decides in retro mode.
- `context/workflows/retrospective.yaml` — **delete** (replaced by continuous-improvement)
- `artefacts/build/agent-incidents.md` — **new**. Format: INC-NNN with date, severity, observed by, symptom, root cause, fix (file paths + commit hash), tasks file reference. Distinct from interruptions (which block agents mid-task) and metrics (system telemetry).
- `context/standards/agent-standards.md` §4.6 — update to reference agent-incidents.md and explain the distinction: interruptions = "I'm blocked right now", incidents = "something went wrong in how agents operate"
- `AGENTS.md` workflow table — replace `retrospective` and add `continuous-improvement`

**Acceptance**: Single `continuous-improvement.yaml` exists with both modes. `retrospective.yaml` deleted. `agent-incidents.md` exists with format template. AGENTS.md lists `continuous-improvement` workflow.

---

### CF-10: Add prepare-commit-msg hook for token metrics

**Rationale**: Agents cannot reliably self-report token usage — Claude Code does not expose token counts programmatically. However, session JSONL files in `~/.claude/projects/` contain exact `input_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`, and `output_tokens` per API call. A `prepare-commit-msg` hook can read these at commit time and inject accurate metrics into the commit message with zero agent effort.

**Files**:
- `context/scripts/prepare-commit-msg.py` — **new**. Derives Claude Code project dir from `git rev-parse --show-toplevel` (portable across repos). Finds active session, sums tokens across main + subagent JSONL files. Uses a watermark file (`.tokens-watermark` in session dir) to compute per-commit deltas. Injects `tokens=<in>K/<out>K` into the Agent-Session line. Skips human commits (no Agent-Session line) and merge/squash commits.
- `context/scripts/prepare-commit-msg.sh` — **new**. Shell wrapper that resolves symlinks and calls the Python script. Symlinked from `.git/hooks/prepare-commit-msg`.
- `.pre-commit-config.yaml` — add `token-metrics` hook with `stages: [prepare-commit-msg]`
- `context/templates/commit-message-template.md` — remove `tokens=` and `duration=` from agent-authored format. Add note that `tokens=` is hook-injected. Keep `duration=` as orchestrator-provided. Update examples and parsing regex.
- `context/scripts/validators/conventional_commits.py` — make `tokens=` and `duration=` optional in the Agent-Session regex (tokens are hook-injected, not always present in authored message)

**Acceptance**: Commit with an Agent-Session line gets `tokens=` appended by the hook. Human commits are untouched. `git log --format='%B' | grep Agent-Session` shows token data on agent commits.

---

### CF-11: Remove agent self-reporting metrics infrastructure

**Rationale**: The `metrics-logging.mdc` rule was never injected (not in orchestrator's always-apply list, `alwaysApply: true` alone is insufficient per CF-2). The `agent-metrics.log` file was last written to a month ago. The self-reporting model is replaced by the prepare-commit-msg hook (CF-10). The continuous-improvement workflow now reconstructs metrics from git log Agent-Session lines instead of reading a separate log file.

**Files**:
- `context/rules/metrics-logging.mdc` — **delete**
- `artefacts/build/agent-metrics.log` — **archive** to `artefacts/build/archive/`
- `.pre-commit-config.yaml` — remove `metrics-logging` validator hook
- `context/scripts/pre-commit-config-template.yaml` — remove `metrics-logging` entry
- `context/agents/workflow-analyst.md` — remove `metrics-logging.mdc` from `rules:` frontmatter and rules table
- `context/agents/tech-lead.md` — remove `metrics-logging.mdc` from `rules:` frontmatter and rules table
- `context/workflows/continuous-improvement.yaml` — replace `agent-metrics.log` data source with `git log Agent-Session` lines. Retrospective review phase aggregates tokens per agent, per sprint, per task from git history.

**Acceptance**: `metrics-logging.mdc` does not exist. No agent definition references it. Continuous-improvement workflow uses git log as the metrics source.

---

### CF-12: Update workflow-standards for current model

**Rationale**: `workflow-standards.md` contained stale content: a duplicated escalation/assumption protocol (~80 lines) that was superseded by `escalation.mdc`, a retrospective section referencing the old workflow, an orchestrator invocation section that assumed agents commit directly, a parallel execution section using "Track" terminology with no file scope guidance, and no documentation of the token metrics pipeline.

**Files**:
- `context/standards/workflow-standards.md` Assumption Handling Protocol — collapse duplicated decision matrix, impact assessment, escalation path, and anti-patterns into a reference to `escalation.mdc` (the authoritative source with two-tier triage and impact classification)
- `context/standards/workflow-standards.md` Retrospective Guidelines — replace with Continuous Improvement section referencing `continuous-improvement.yaml` dual-mode workflow (incident + retrospective)
- `context/standards/workflow-standards.md` §8 Orchestrator Invocation — update for centralised commits (agents report, orchestrator commits), reference `task-prompt-template.md`, note that `duration=` is orchestrator-authored and `tokens=` is hook-injected
- `context/standards/workflow-standards.md` §8 Token Metrics — **new subsection**. Document the full pipeline: Claude Code session JSONL data source, `prepare-commit-msg.py` hook (derive project dir, find active session, sum tokens, watermark delta, inject into Agent-Session line), what input/output numbers mean, commit message format showing authored vs injected fields, consumption by continuous-improvement workflow via git log
- `context/standards/workflow-standards.md` §11 Parallel Execution — replace "Track" with "Sprint". Add File Scope and Collision Safety subsection (disjoint scopes, scope-collision check steps, centralised sequential commits). Update best practices for file scopes and git log metrics.

**Acceptance**: workflow-standards.md references `escalation.mdc` instead of duplicating the decision matrix. Token Metrics subsection documents the hook pipeline end-to-end. Parallel execution section includes file scope safety steps. No references to "Track" as a parallel grouping term.

---

### CF-13: Add interaction tracking fields to Agent-Session

**Rationale**: Understanding agent autonomy requires capturing the interaction model per commit — was the task fully autonomous, delegated with human guidance, or human-directed? Raw counts of human messages vs tool approvals separate substantive interventions from permission-gating noise.

**Files**:
- `context/rules/git-commits.mdc` Agent-Session Fields — add three fields: `dispatch` (human|orchestrator), `interactions` (count of human messages during task), `approvals` (count of tool/action approvals). Add "Authored by" column to fields table showing orchestrator as author for all three.
- `context/templates/commit-message-template.md` Agent-Session Fields — add same three fields with "Authored by" column. Update examples to include the fields.
- `context/templates/commit-message-template.md` Parsing — update regex to include optional `dispatch`, `interactions`, `approvals` groups.
- `context/scripts/validators/conventional_commits.py` — update Agent-Session regex to accept optional `dispatch=(human|orchestrator)`, `interactions=\d+`, `approvals=\d+` between `duration` and `tokens`.

**Acceptance**: Agent-Session regex in validator accepts all three new fields. Commit template and rule both document the fields with authorship. Examples show realistic values.

---

### CF-14: Add efficiency and autonomy metrics to PR template

**Rationale**: The PR is the natural place to surface aggregated Agent-Session data. Efficiency metrics (duration, tokens — total/mean/SD) show cost. Autonomy metrics (fully autonomous/human input/human-directed — count/%) show how independent agents were. All derived from `git log --format='%b' | grep Agent-Session` on the branch, no separate data store needed.

**Files**:
- `context/templates/pr-description-template.md` Agent Metrics — replace flat table with two sub-tables: Efficiency (commits, duration, tokens in/out — Total/Mean/SD) and Autonomy (fully autonomous, with human input, human-directed — Count/%). Remove per-task breakdown (redundant with Agent-Session in each commit).
- `context/templates/pr-description-template.md` Section Details — update Agent Metrics guidance with autonomy classification derivation rules and note that pre-change commits default to human-directed.
- `context/templates/pr-description-template.md` Complete Example — update to match new format.
- `context/templates/pr-description-template.md` Links — remove stale `session-log.jsonl` references.
- `context/rules/git-commits.mdc` — add Pull Requests section instructing orchestrator to use `pr-description-template.md` with `git log` extraction command.

**Acceptance**: PR template has Efficiency and Autonomy sub-tables. No per-task breakdown. git-commits rule references the PR template. No stale metrics file links.

---

### CF-15: Add orchestrator commit procedure to git-commits rule

**Rationale**: Newly spawned subagents may not include Agent-Session in their commit message file — they may not have loaded the git-commits rule. The orchestrator, which always has the rule, needs an explicit verification step before committing on behalf of agents.

**Files**:
- `context/rules/git-commits.mdc` Full Format — remove `tokens=` from agent-authored format (hook-injected). Note `duration=` is orchestrator-provided.
- `context/rules/git-commits.mdc` — add "Orchestrator Commit Procedure" section: 6-step checklist (read message → check Agent-Session → append if missing with tool/model/agents/duration/dispatch/interactions/approvals → check Co-Authored-By → format → commit). Include: "The orchestrator owns the commit — if the agent's message is incomplete, fix it rather than rejecting the task."
- `context/rules/git-commits.mdc` Agent-Session Fields — add "Authored by" column distinguishing agent-authored (tool, model, agents), orchestrator-authored (duration, dispatch, interactions, approvals), and hook-injected (tokens) fields.

**Acceptance**: git-commits rule has an "Orchestrator Commit Procedure" section with verification steps. Full Format shows `tokens=` as hook-injected. Fields table has "Authored by" column.
