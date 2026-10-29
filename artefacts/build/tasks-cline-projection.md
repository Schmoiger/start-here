# Tasks: Cline Runtime Projection

**Branch**: `feat/cline-projection`
**Status**: Planning
**Scope**: Add a fifth runtime adapter projecting the canonical harness (`context/`) into Cline-native configuration (`CLINE.md`, `.clinerules/`, `.cline/skills/`), plus canonical guidance rules distilled from observed terminal stall patterns, telemetry metadata, wiring, tests, and documentation.
**Design**: N/A — the adapter mirrors the existing `claude/` and `gemini/` adapters (`context/scripts/generators/adapters/`). Prior evidence `artefacts/build/CLINE-STALL-PATTERNS.md` is archived by the human and must **not** be read by agents; its runtime-agnostic lessons are authored directly into this doc.
**Created**: 2026-10-29
**Amended**: —

---

## Orchestrator Notes

This is a **sequential, single-agent** build. **No parallel agents** are dispatched at any point. Agents **build only** — all QA is performed by the human at the checkpoints in [Human QA Gates](#human-qa-gates). Every task is small enough for a less capable agent: read the listed context, apply the instructions, run the done-signal command, report.

### Pipeline Overview

```
Sprint 1 (canonical context)  T-001 → T-002 → T-003
Sprint 2 (adapter, TDD)       T-004 → T-005 → T-006 → T-007 → T-008 → T-009
Sprint 3 (wiring & docs)      T-010 → T-011 → T-012 → T-013
Sprint 4 (regenerate/verify)  T-014 → T-015
[HUMAN QA — see checklist]
```

Each task is one agent invocation, one task, one commit. Dispatch the next task only after the previous task's done signal is confirmed and the commit is on disk (commit + push immediately after each task).

### Parallelism Strategy

**Explicitly sequential** — no parallel workstreams. file_scope is fully disjoint per task (each task owns specific files listed in its `## File Scope`), so there is no collision risk. Dispatch order is exactly the numeric task order; do not reorder.

Intra-sprint TDD discipline: `T-004` (failing tests) and `T-005` (generator implementation) are **two separate commits** — never squash RED and GREEN.

### Commit Strategy

One commit per task on `feat/cline-projection`. Agents **do not commit** — they write the commit message to `/tmp/{task-id}_commit_msg.txt` and report the changed-file list; the orchestrator commits and pushes (per `agent-standards.md` §4.4). Commit messages are conventional commits. Push immediately after every commit.

| Task | Commit message |
|------|---------------|
| T-001 | `feat(context): add non-interactive terminal execution guidance to agent-sandbox skill` |
| T-002 | `feat(context): add verify-before-retry invariant to bash-environment rule` |
| T-003 | `feat(context): register cline telemetry source in models.yaml` |
| T-004 | `test(generators): add failing cline adapter tests (TDD red)` |
| T-005 | `feat(generators): add cline runtime adapter projections` |
| T-006 | `feat(generators): point AGENTS.md at @CLINE.md runtime entry` |
| T-007 | `feat(generators): register cline target in adapter CLI` |
| T-008 | `feat(validators): track cline projections in adapter drift validator` |
| T-009 | `test(generators): cover cline in dispatcher/e2e/drift suites` |
| T-010 | `docs(context): document cline telemetry source and adapter inventory` |
| T-011 | `docs: update framework docs, requirements, and architecture for cline adapter` |
| T-012 | `docs(scripts): update test inventory for cline adapter` |
| T-013 | `feat(init): support cline runtime target in init.sh` |
| T-014 | `chore(harness): regenerate projections with cline target and verify zero drift` |
| T-015 | `test: confirm full generator/adapter suite green via baseline command in done signal` |

### Effort Estimates

| Task | Agent(s) | Effort |
|------|----------|--------|
| T-001 | python-coder | Small (10–30k tokens) |
| T-002 | python-coder | Small (10–30k tokens) |
| T-003 | python-coder | Small (10–30k tokens) |
| T-004 | functional-tester | Medium (30–80k tokens) |
| T-005 | python-coder | Medium (30–80k tokens) |
| T-006 | python-coder | Small (10–30k tokens) |
| T-007 | python-coder | Small (10–30k tokens) |
| T-008 | python-coder | Small (10–30k tokens) |
| T-009 | functional-tester | Medium (30–80k tokens) |
| T-010 | documentation | Small (10–30k tokens) |
| T-011 | documentation | Medium (30–80k tokens) |
| T-012 | documentation | Small (10–30k tokens) |
| T-013 | devops | Small (10–30k tokens) |
| T-014 | python-coder | Small (10–30k tokens) |
| T-015 | functional-tester | Small (10–30k tokens) |
| **Total** | | **~200–400k tokens** |

### Backlog Cleanup

After all tasks complete, update `artefacts/build/todo.md`:
- **TASK § Extend harness to the Cline runtime** (`todo.md` line 41, already `[x]` for telemetry): annotate that the adapter projection is now complete via this sprint.
- **ITEM "Add projection to OpenRouter runtime"**: remains TODO — out of scope.
- **ITEM "Do we need context/agents/cursor-workflow-helper.mdc?"**: remains TODO — out of scope (canonical documentation, not a generated projection).

### Potential Further Work (non-blocking, do not implement in this sprint)

- Cline Subagents / Agent Teams (`@orchestrator` spawn parity via `.cline/agents/`) — design conversation, not an anti-pattern fix.
- Parameterise the `AGENTS.md` generator's hardcoded Gemini tool-mapping section per runtime (latent issue surfaced by the Cline projection).
- **Conditional** `.clinerules/*.md` entries with `paths:` frontmatter derived from canonical skill `globs` — deferred until a concrete need emerges; Cline Skills are currently the on-demand mechanism.

**Agents used**: python-coder / functional-tester (build), documentation (docs), devops (init.sh). Every agent reads only its task's `### Context` files. Orchestrator inlines `context/rules/bash-environment.md` + `context/rules/workspace-conventions.md` into every prompt; agents do not re-read all standards.

---

## Human QA Gates

These replace the build workflow's agent-based review gates (`tasks-review`, `test-plan-review`, `quality-review`) — **humans QA, agents build**.

- [ ] **Gate 1 — Plan approval**: human approves this tasks doc before dispatch begins.
- [ ] **Gate 2 — Adapter smoke**: after T-009, human runs `uv run pytest context/scripts/tests/test_cline_adapter.py -v` and spot-checks a generated `CLINE.md` / `.clinerules/00-core.md` / one `.cline/skills/*/SKILL.md`.
- [ ] **Gate 3 — Final human QA**: after T-015, human executes the [Final Human QA Checklist](#final-human-qa-checklist) in a real Cline session.

---

## Task Index

- **Priority**: critical, high, medium, low
- **Status**: pending, in_progress, blocked, completed
- **Blocked By**: task IDs or `-` if none

| ID | Priority | Status | Blocked By | Task |
|----|----------|--------|------------|------|
| T-001 | critical | pending | - | Add non-interactive terminal-execution guidance to `agent-sandbox.md` skill |
| T-002 | critical | pending | T-001 | Add verify-before-retry invariant to `bash-environment.md` rule |
| T-003 | high | pending | T-001 | Register `cline` telemetry source in `context/models.yaml` |
| T-004 | critical | pending | T-003 | Write failing `test_cline_adapter.py` (TDD red) |
| T-005 | critical | pending | T-004 | Implement `adapters/cline/generator.py` (CLINE.md, rules, skills) |
| T-006 | high | pending | T-005 | Add `@CLINE.md` runtime-entry pointer to generated `AGENTS.md` |
| T-007 | critical | pending | T-005 | Register `cline` target in `generate_adapters.py` CLI |
| T-008 | high | pending | T-007 | Track cline projections in `adapter_drift.py` |
| T-009 | high | pending | T-006,T-008 | Update dispatcher/e2e/drift tests for cline |
| T-010 | medium | pending | T-003 | Document cline telemetry + adapter inventory in `context/README.md` |
| T-011 | medium | pending | T-010 | Update framework docs, requirements, architecture, root README |
| T-012 | low | pending | T-011 | Update `context/scripts/tests/README.md` + validators README counts |
| T-013 | high | pending | T-008 | Add `cline` runtime option + pruning to `init.sh` |
| T-014 | critical | pending | T-013 | Add cline to `.agent-targets`, regenerate projections, verify zero drift |
| T-015 | critical | pending | T-014 | Full generator/adapter test suite green + benchmark |

---

# Sprint 1 — Canonical Context & Telemetry Metadata

## File Scope

- `context/skills/agent-sandbox.md`

## Task

T-001: Add non-interactive terminal-execution guidance to `context/skills/agent-sandbox.md`.

### Context

- `context/skills/agent-sandbox.md` (edit target)
- `context/rules/bash-environment.md` (read-only — cross-reference style)
- `context/standards/tech-standards.md` lines 235–239 (read-only — confirms `yarn test` is the mandated runner)

### Instructions

Append a new `## Non-Interactive Command Execution` section to `agent-sandbox.md`, after the existing "Piping and Command Substitution" section (and before `### File Modification and Reading`). The section must be **runtime-agnostic** (bash/zsh/macOS syntax only — no PowerShell `$env:`, no `*>` redirects, no `Write-Host`). Content requirements:

1. **Streaming / animated test runners**: test runners with animated progress output (e.g. Vitest spinners emitting `\r`) can hang or garble output capture in agent terminal sessions. Safe form:
   - `CI=1 yarn test > /tmp/test-out.txt 2>&1` — `CI=1` disables the animated reporter and watch mode; output goes to a temp file read back in a separate step. Env-prefix form is mandatory (never `CI=1 && yarn test` — see `bash-environment.md` banned patterns).
   - Use `yarn` as the package manager (`yarn test`, `yarn add`) exactly as mandated by `tech-standards.md` — **never** `npm`.
2. **Interactive CLI tools**: never run commands that may enter interactive mode (prompts, editors, browser confirmation). Prefer the non-interactive form, e.g. `gh pr create --no-browser --body-file /tmp/body.md`, and for GitHub issues use `gh api repos/.../issues --method POST --field title=... --field body=@/tmp/body.md` instead of interactive `gh issue create`.
3. **Multi-line / long values in command arguments**: write multi-line bodies or long values to a temp file first and pass them file-based (`git commit -F /tmp/msg.txt`, `--body-file`, `--field body=@file`). Cross-reference the existing heredoc ban above.
4. **Verify state before retrying**: after an apparently failed command, the command may actually have succeeded with broken result reporting. Before retrying or "correcting": `git -C <repo> log --oneline -3`, `git -C <repo> status`, `git -C <repo> diff --stat`, or read the redirect temp file. Treat "no result signal" as **unknown**, not **failed**. Do not re-run mutating commands from assumption.

Keep the section concise (one short paragraph per bullet), in the document's existing expository style, with a short rationale sentence per bullet.

### Acceptance Criteria

- `grep -c "## Non-Interactive Command Execution" context/skills/agent-sandbox.md` → outputs `1`.
- The section contains the exact strings `CI=1 yarn test`, `--no-browser`, `--field body=@`, `unknown`, and `git -C`.
- The section contains **no** PowerShell syntax (`$env:`, `*>`, `Write-Host`, `Select-Object`).
- `uv run pytest tests/context-unit-tests/ -q` → all pass.

### Primary Output Path

`context/skills/agent-sandbox.md`

---

## File Scope

- `context/rules/bash-environment.md`

## Task

T-002: Add the verify-before-retry invariant (Pattern 8) to `context/rules/bash-environment.md`.

### Context

- `context/rules/bash-environment.md` (edit target — the "Banned Bash Patterns" table)

### Instructions

Add one row to the "Banned Bash Patterns" table in `bash-environment.md`:

| Pattern | Problem | Fix |
|---------|---------|-----|
| Retrying or "correcting" after an apparent command failure without first verifying true state | Duplicate side effects (double commits, double issues) when the first command actually succeeded but result-reporting broke; wasted retries | After any apparent failure: verify true state with `git -C <root> log --oneline -3`, `git -C <root> status`, `git -C <root> diff --stat`, or read the command's redirect/output temp file before retrying. Treat "no result signal" as unknown, not failed |

Keep the table format exactly as-is (pipe-aligned rows). Do not add any other content to the file.

### Acceptance Criteria

- `grep -c "unknown, not failed" context/rules/bash-environment.md` → outputs `1`.
- `grep -c "no result signal" context/rules/bash-environment.md` → outputs `1`.
- The existing table rows are unchanged (no added rows beyond the one new row).
- `uv run pytest tests/context-unit-tests/ -q` → all pass.

### Primary Output Path

`context/rules/bash-environment.md`

---

## File Scope

- `context/models.yaml`

## Task

T-003: Register the `cline` telemetry source in `context/models.yaml`.

### Context

- `context/models.yaml` — the `telemetry_sources:` block (entries for `anthropic_claude`, `google_antigravity`, `github_copilot`, `openai_codex`)
- `context/scripts/prepare-commit-msg.py` lines 528–610 read-only — the `ClineExtractor` class documents the on-disk schema (authoritative for this task)

### Instructions

Add a fifth entry under `telemetry_sources:` (append after `openai_codex`):

```yaml
  cline:
    name: "Cline IDE Telemetry"
    description: "Cline session metadata and per-message usage metrics under the Cline data directory."
    local_session_path: "~/.cline/data/sessions/{session-id}/"
    session_files:
      meta: "{session-id}.json"
      messages: "{session-id}.messages.json"
    storage_type: "json"
    repository_mapping:
      key: "cwd / workspace_root in the session meta JSON"
    token_fields:
      input: "assistant message metrics.inputTokens"
      output: "assistant message metrics.outputTokens"
      cache_read: "assistant message metrics.cacheReadTokens"
      cache_write: "assistant message metrics.cacheWriteTokens"
      model: "meta 'model' or assistant message modelInfo.id"
```

The field names must match what `ClineExtractor` reads (per the Context file) — do not invent fields. Indentation must match the sibling entries (2-space keys under `telemetry_sources`).

### Acceptance Criteria

- `grep -A20 "cline:" context/models.yaml | head -22` → shows the block above with `local_session_path: "~/.cline/data/sessions/{session-id}/"`.
- `grep -c "cacheWriteTokens" context/models.yaml` → outputs `1`.
- File is valid YAML: `uv run python -c "import yaml; yaml.safe_load(open('context/models.yaml'))"` → exits 0 with no error output.

### Primary Output Path

`context/models.yaml`

---

# Sprint 2 — Cline Adapter (TDD)

## File Scope

- `context/scripts/tests/test_cline_adapter.py` (new file)

## Task

T-004: Write failing `test_cline_adapter.py` (TDD red) for the cline adapter generator.

### Context

- `context/scripts/tests/test_gemini_adapter.py` (structural template — mirror its style)
- `context/scripts/generators/adapters/core/models.py` (read-only — `CanonicalSkill` fields: `name`, `description`, `globs`, `body`)
- `context/scripts/generators/adapters/gemini/generator.py` (read-only — how the existing generator writes SKILL.md files)

### Instructions

Create `context/scripts/tests/test_cline_adapter.py` with import lines that reference the **not-yet-written** module `context.scripts.generators.adapters.cline.generator` and this public API:

```python
from context.scripts.generators.adapters.cline.generator import (
    generate_cline_md,
    generate_cline_rules,
    generate_cline_skills,
)
```

The context fixture must include **both** an agent and at least one canonical skill:

```python
from context.scripts.generators.adapters.core.models import CanonicalAgent, CanonicalSkill

self.context = {
    "agents": {"test-agent": CanonicalAgent(name="test-agent", description="A test agent", model="cline-test")},
    "workflows": {},
    "skills": {"demo-skill": CanonicalSkill(
        name="demo-skill",
        description="Run this when executing demo tasks.",
        globs=["**/demo/**"],
        body="# Demo Skill\n\nDemo instructions.",
    )},
}
```

Write three tests (unittest style, mirroring `test_gemini_adapter.py`):

1. `test_generate_cline_md` — calls `generate_cline_md(self.context, self.output_dir)`; asserts `CLINE.md` exists; content contains `Auto-generated`, `@AGENTS.md`, and `execute_command`.
2. `test_generate_cline_rules` — calls `generate_cline_rules(self.context, self.output_dir)`; asserts `.clinerules/00-core.md` exists; content does **not** start with `---\n` (must be an always-on rule, no frontmatter); content contains `yarn` and `unknown`.
3. `test_generate_cline_skills` — calls `generate_cline_skills(self.context, self.output_dir)`; asserts `.cline/skills/demo-skill/SKILL.md` exists; YAML frontmatter `name` equals `demo-skill` and `description` equals the input description (parse with `yaml.safe_load(content.split("---", 2)[1])`); body contains `Auto-generated`.

These tests must **fail** at this point (module does not exist). Run them and record the failure verbatim.

### Acceptance Criteria

- `uv run pytest context/scripts/tests/test_cline_adapter.py -v` → fails with `ModuleNotFoundError` for `context.scripts.generators.adapters.cline` (evidence recorded in the report).
- File is added to the staged set for the next commit.

### Primary Output Path

`context/scripts/tests/test_cline_adapter.py`

---

## File Scope

- `context/scripts/generators/adapters/cline/generator.py` (new file)
- `context/scripts/generators/adapters/cline/__init__.py` (new file, empty)

## Task

T-005: Implement `adapters/cline/generator.py` (CLINE.md, `.clinerules/`, `.cline/skills/`).

### Context

- `context/scripts/generators/adapters/gemini/generator.py` (primary structural template — `generate_skills`, `_extract_model_mappings`, `generate_gemini_md`)
- `context/scripts/generators/adapters/claude/generator.py` (secondary template — `generate_claude_md` header/pointer style)
- `context/scripts/generators/adapters/core/loader.py` (read-only — the `skills:` dict values are `CanonicalSkill` with `.name`, `.description`, `.globs`, `.body`)
- `context/models.yaml` (read-only — provider model aliases for the model-mapping section)
- `context/scripts/generators/adapters/core/agents_md.py` (read-only — the auto-generated header/marker string convention)

### Instructions

Create the package `context/scripts/generators/adapters/cline/` with `generator.py` exposing exactly:

```python
def generate_cline_md(context, output_dir, dry_run=False) -> dict[Path, str]
def generate_cline_rules(context, output_dir, dry_run=False) -> dict[Path, str]
def generate_cline_skills(context, output_dir, dry_run=False) -> dict[Path, str]
```

All three return `{Path: content}` and write to `output_dir` unless `dry_run=True` (mirror the gemini adapter's write discipline; `mkdir(parents=True, exist_ok=True)` for nested dirs).

**1. `generate_cline_md`** → writes `output_dir / "CLINE.md"`:

```markdown
# Cline System Instructions

**Auto-generated by context/scripts/generators/generate_adapters.py — do not edit manually**

Please read and strictly adhere to the instructions, standards, and workflows defined in `@AGENTS.md`.

## Tool Mappings
- Use `write_to_file` / `apply_diff` / `multi_edit` for creating and editing files (the `AGENTS.md` tool names are Gemini-oriented).
- Use `execute_command` / `execute_command_with_output` for executing terminal commands.
- Use `read_file` for reading files.
- Use `search_files` / `list_files` for finding and searching files.
- Use `browser_action` for browser automation.

## Rules & Skills
- Always-on constraints are in `.clinerules/00-core.md` — apply throughout the session.
- Procedural skills are in `.cline/skills/` — they load on demand when a task matches a skill's description; consult the **agent-sandbox** skill before running terminal commands.

## Model Mappings
{model_mappings}
```

`model_mappings` is produced by copying `_extract_model_mappings(repo_root, provider_name)` from the gemini adapter and calling it once per provider key present in `models.yaml` tiers (`anthropic`, `google`, `openai`), emitting a line per tier:
`- \`{tier_name}\` ({provider}) → \`{runtime_alias}\``, prefixed by a note that Cline is provider-agnostic and the operator selects the provider. If `models.yaml` yields nothing for a provider, skip it.

**CAUTION**: verify the exact Cline tool names (`write_to_file`, `apply_diff`, `multi_edit`, `execute_command`, `execute_command_with_output`, `search_files`, `list_files`, `browser_action`) against the installed Cline version's tool list at implementation time. If any differ, use the verified names and note the deviation in the report.

**2. `generate_cline_rules`** → writes `output_dir / ".clinerules" / "00-core.md"`. This is an **always-on** rule: it must **not** start with YAML frontmatter. Content (markdown, no code fence around the file):

```markdown
# Cline Core Rules (always active)

**Auto-generated by context/scripts/generators/generate_adapters.py — do not edit manually**

- Use `yarn` — never `npm` (see `context/standards/tech-standards.md`).
- After an apparently failed command, verify true state before retrying: `git -C <root> log --oneline -3`, `git -C <root> status`, `git -C <root> diff --stat`, or read the command's output temp file. Treat "no result signal" as unknown, not failed.
- Run non-interactive terminal commands that may produce animated output as `CI=1 yarn <command> > /tmp/<name>-out.txt 2>&1`; read the file in a separate step.
- Read `@CLINE.md` for tool mappings and `@AGENTS.md` for workflow and agent dispatch before starting a task.
```

**3. `generate_cline_skills`** → for every entry in `context["skills"]` (canonical skills only — do **not** emit agent-name skill folders), write `output_dir / ".cline" / "skills" / "<name>" / "SKILL.md"`:

```markdown
---
name: {skill.name}
description: {json.dumps(skill.description, ensure_ascii=False) truncated to 1024 characters}
---

{first line of skill.body if it starts with "# ", else "# {Skill Name}"}

**Auto-generated by context/scripts/generators/generate_adapters.py — do not edit manually**

{rest of skill.body}
```

Cline requires `name` to exactly match the directory name and `description` ≤ 1024 chars — truncate long descriptions at 1024 chars with ` …` suffix. Do not include `globs` in the frontmatter (Cline triggers on description only).

### Acceptance Criteria

- `uv run pytest context/scripts/tests/test_cline_adapter.py -v` → **3 passed**.
- `uv run python -m py_compile context/scripts/generators/adapters/cline/generator.py` → exit 0.
- Dry-run safety: `uv run python context/scripts/generators/generate_adapters.py -d` → no cline paths yet (target not registered — expected).

### Primary Output Path

`context/scripts/generators/adapters/cline/generator.py`

---

## File Scope

- `context/scripts/generators/adapters/core/agents_md.py`
- `context/scripts/generators/generate_adapters.py` (only the `get_adapter_projections` function)

## Task

T-006: Add the `@CLINE.md` runtime-entry pointer to the generated `AGENTS.md`.

### Context

- `context/scripts/generators/adapters/core/agents_md.py` — `generate_agents_md(context, output_dir, dry_run=False)` builds AGENTS.md
- `context/scripts/generators/generate_adapters.py` — `get_adapter_projections(context, repo_root, targets)` (lines 153–200)

### Instructions

1. In `agents_md.py`, add an optional parameter `runtime_entry: str | None = None` to `generate_agents_md`. When non-None, render a new section before the final auto-generated marker line:

```markdown
---

## Runtime Entry

- Read `@{runtime_entry}` for {runtime} -specific tool mappings, rules, and model guidance.
```

(The value passed will be `CLINE.md`, so this renders as `Read \`@CLINE.md\``.) Keep the existing default behaviour byte-identical when `runtime_entry` is None.

2. In `generate_adapters.py` `get_adapter_projections`:
   - In the `targets is None or "all" in targets` branch add `"cline"` to `active_targets`.
   - In the non-all branch, after the existing gemini/claude core rule, add: `if "cline" in active_targets: active_targets.add("core")`.
   - The `core` dispatch becomes: `entry = "CLINE.md" if "cline" in active_targets else None; projections.update(generate_agents_md(context, repo_root, dry_run=True, runtime_entry=entry))`. Keep the existing call shape for all other cases.

Do not change AGENTS.md content for non-cline targets (this validates as byte-identical elsewhere).

### Acceptance Criteria

- `uv run python -m py_compile context/scripts/generators/adapters/core/agents_md.py context/scripts/generators/generate_adapters.py` → exit 0.
- `uv run pytest context/scripts/tests/test_e2e_compilation.py -k "not full_compilation" -q` → passes (existing determinism/synthetic tests, which do not target cline, still produce the same files).
- Manual check (dry-run, cline not yet a registered target — interim): the function signatures accept the new parameter without error.

### Primary Output Path

`context/scripts/generators/adapters/core/agents_md.py`

---

## File Scope

- `context/scripts/generators/generate_adapters.py` (full CLI)

## Task

T-007: Register the `cline` target in the `generate_adapters.py` CLI.

### Context

- `context/scripts/generators/generate_adapters.py` — `SUPPORTED_TARGETS`, `TARGET_ALIASES`, `IGNORED_BLOCK`, parsing flags, dispatch in `get_adapter_projections`
- `context/scripts/tests/test_cli_dispatcher.py` (read-only — the parsing conventions to satisfy)

### Instructions

1. Imports: add the three cline generator functions to the import block.
2. `SUPPORTED_TARGETS`: add `"cline"`.
3. `TARGET_ALIASES`: add `"cline": "cline"` and `"l": "cline"` (short alias `-l/--cline`, since `-c/-g/-p/-o` are taken).
4. `IGNORED_BLOCK`: add `CLINE.md`, `.clinerules/`, `.cline/skills/` (keep alphabetical/section ordering consistent).
5. Parser: add a convenience flag group mirroring `-g/-c/-p/-o`:
   `-l, --cline` → `action="store_true", dest="cline"`, help "Convenience flag: project Cline runtime". Update the `-t/--target` help and the CLI `epilog` examples with a cline example (`python generate_adapters.py -l -d`).
6. `main()`: `if args.cline: selected_targets.add("cline")`.
7. Dispatch in `get_adapter_projections`: in the `"cline" in active_targets` branch:
   - `projections.update(generate_cline_md(...))`
   - `projections.update(generate_cline_rules(...))`
   - `projections.update(generate_cline_skills(...))`
   (all called with `dry_run=True` there, matching the other branches).

### Acceptance Criteria

- `uv run pytest context/scripts/tests/test_cli_dispatcher.py -v` → passes **including** new/updated assertions for cline after T-009 lands; at minimum the existing tests still pass after the registration (run before and after T-009).
- `uv run python context/scripts/generators/generate_adapters.py -t cline -d` → exit 0, dry-run reports the cline projections (`CLINE.md`, `.clinerules/00-core.md`, 20+ `.cline/skills/*/SKILL.md`) with no files written to disk.
- `.gitignore` update: running the generator adds the cline entries — confirm `grep -c "clinerules" .gitignore` → outputs `1` after a non-dry-run in T-014 (this check moves to T-014; here just verify `IGNORED_BLOCK` text).

### Primary Output Path

`context/scripts/generators/generate_adapters.py`

---

## File Scope

- `context/scripts/validators/adapter_drift.py`

## Task

T-008: Track cline projections in the adapter drift validator.

### Context

- `context/scripts/validators/adapter_drift.py` — `target_managed_dirs` dict (lines 76–81) and orphan-check loop

### Instructions

Add a `"cline"` entry to `target_managed_dirs`:

```python
"cline": [repo_root / ".clinerules", repo_root / ".cline" / "skills"],
```

No other changes: the expected-set comparison and orphan detection logic are target-agnostic and will pick cline up automatically.

### Acceptance Criteria

- `uv run python -m py_compile context/scripts/validators/adapter_drift.py` → exit 0.
- `uv run pytest context/scripts/tests/test_adapter_drift.py -q` → all existing drift tests pass.
- After T-014 regeneration, `uv run python context/scripts/validators/adapter_drift.py` → "All runtime adapter projections are in sync" (checked in T-014; here the dict exists).

### Primary Output Path

`context/scripts/validators/adapter_drift.py`

---

## File Scope

- `context/scripts/tests/test_cli_dispatcher.py`
- `context/scripts/tests/test_e2e_compilation.py`
- `context/scripts/tests/test_adapter_drift.py`

## Task

T-009: Update dispatcher, e2e, and drift test suites for the cline target.

### Context

- The three test files listed in File Scope (edit targets)
- `context/scripts/generators/generate_adapters.py` (read-only — the cline registration from T-006/T-007)

### Instructions

1. **`test_cli_dispatcher.py`**:
   - In `test_target_normalization` add: `assert normalize_target("cline") == "cline"` and `assert normalize_target("l") == "cline"`.
   - In `test_cli_parser_flags` add: `args_l = parser.parse_args(["-l"]); assert args_l.cline is True`.
   - No other changes.
2. **`test_e2e_compilation.py`**:
   - In `test_e2e_full_compilation_all_targets`, after the OpenAI section add a **6. Cline verification** section:
     - `assert (tmp_path / "CLINE.md").is_file()` and `"@AGENTS.md" in cline_content` and `"execute_command" in cline_content`.
     - `assert (tmp_path / ".clinerules" / "00-core.md").is_file()`.
     - `.cline/skills/` exists and contains at least as many `*/SKILL.md` files as canonical skills in `context/skills` (use `len(list((context_dir / "skills").glob("*.md")))` as the floor, mirroring the gemini skill-count assertion style).
     - The existing `assert len(created_files) >= 80` floor remains valid (count grows with cline).
   - In `test_e2e_synthetic_context_compilation`, add cline assertions: `(output_dir / "CLINE.md").is_file()` and `(output_dir / ".clinerules" / "00-core.md").is_file()` (no `.cline/skills/` assert — synthetic context has no canonical skills).
3. **`test_adapter_drift.py`**: add one test `test_adapter_drift_cline_managed_dirs` reusing the existing claude-target pattern: run generation for `{"cline"}`, then `check_adapter_drift(..., targets={"cline"})` → `(True, [])`; then modify `.clinerules/00-core.md` on disk and assert drift reports a `MODIFIED` issue.

### Acceptance Criteria

- `uv run pytest context/scripts/tests/test_cli_dispatcher.py context/scripts/tests/test_adapter_drift.py context/scripts/tests/test_e2e_compilation.py -q` → all pass.
- `uv run pytest context/scripts/tests/test_cline_adapter.py -q` → still 3 passed.

### Primary Output Path

`context/scripts/tests/test_e2e_compilation.py`

---

# Sprint 3 — Wiring & Documentation

## File Scope

- `context/README.md`

## Task

T-010: Document the cline telemetry source and adapter inventory in `context/README.md`.

### Context

- `context/README.md` — the "Runtime Telemetry & Session Token Tracking" section (Multi-Runtime Comparison Matrix) and the harness inventory ("What's included" / CLI usage)
- `context/models.yaml` (read-only — the T-003 telemetry block is now present)

### Instructions

1. **Multi-Runtime Comparison Matrix**: add a `Cline` row alongside the existing rows (Claude Code, Antigravity, Copilot, Codex). Columns mirror the existing rows; for Cline use: telemetry path `~/.cline/data/sessions/{id}/{id}.json` + `.messages.json`; token fields `metrics.inputTokens` / `metrics.outputTokens` / `metrics.cacheReadTokens` / `metrics.cacheWriteTokens`; model source `meta 'model'` / `modelInfo.id`.
2. **Adapter inventory**: in the adapter count/inventory text, extend "X runtime adapters" (or equivalent list naming Gemini/Antigravity, Claude Code, GitHub Copilot, OpenAI/Codex) to include Cline.
3. **CLI usage**: in the `generate_adapters.py` usage/CLI section, note the `-t cline` / `-l --cline` target.
4. **Skill inventory**: if `context/README.md` lists `.agents/skills/` as a generated skill location, add the cline skill location `.cline/skills/` and rules location `.clinerules/`.

Use `grep -n -i "runtime" context/README.md` and `grep -n -i "adapter" context/README.md` to locate the exact sections; keep the matrix table pipe-aligned with existing rows.

### Acceptance Criteria

- `grep -n -i "cline" context/README.md` → at least 3 distinct lines (matrix row, adapter inventory, CLI usage).
- The matrix row has the same number of columns as sibling rows (spot-check visually).

### Primary Output Path

`context/README.md`

---

## File Scope

- `README.md` (repo root)
- `artefacts/architecture/architecture.md`
- `artefacts/product/requirements.md`
- `context/docs/agentic-framework.md`
- `context/docs/agentic-framework-reference.md`

## Task

T-011: Update framework docs, requirements, architecture, and root README for the cline adapter.

### Context

- The five files in File Scope
- `context/scripts/validators/framework_docs_staleness.py` (read-only — a pre-commit/CI check requires the two framework docs to be updated when `context/` changes)

### Instructions

Update each file for the new Cline runtime, keeping edits minimal and consistent with existing wording:

1. **`README.md` (root)**: "4 runtime adapters" → "5 runtime adapters", and add Cline to any runtime-list paragraph.
2. **`artefacts/architecture/architecture.md`**: add Cline to the system-purpose runtime list and to the "Adapter Compilation Model" section (target formats: `CLINE.md`, `.clinerules/`, `.cline/skills/`). Locate spots with `grep -n -i "runtime" artefacts/architecture/architecture.md | head -40`.
3. **`artefacts/product/requirements.md`**: add Cline to the overview runtime list; add a new requirement after REQ-ADP-011:
   `REQ-ADP-012 | P | THE cline-adapter SHALL project canonical agents, skills, and rules into Cline-native configuration (CLINE.md, .clinerules/, .cline/skills/) and rely on Cline's on-demand skill loading for procedural guidance. | Generates CLINE.md runtime entry, always-on .clinerules/00-core.md, and .cline/skills/<name>/SKILL.md projections; prepare-commit-msg ClineExtractor already covers telemetry.`
4. **Framework docs (`context/docs/agentic-framework.md`, `agentic-framework-reference.md`)**: update derived-projection lists (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.agent/skills/`, `.github/`, `.openai/`) to include `CLINE.md`, `.clinerules/`, `.cline/skills/`; note that Cline skill delivery uses `.cline/skills/` loaded on demand by description (parallel to the Gemini `.agents/skills/` mechanism sentence). Use `grep -n -i "runtime" <file> | head -60` to locate lists.

Complete framework-doc edits in this task so the T-014 commit is not blocked by the staleness validator.

### Acceptance Criteria

- `grep -c "cline" README.md artefacts/architecture/architecture.md artefacts/product/requirements.md` → ≥ 3 combined (at least one per file).
- `grep -c "cline" context/docs/agentic-framework.md context/docs/agentic-framework-reference.md` → ≥ 2 combined.
- `uv run python context/scripts/validators/framework_docs_staleness.py` → exits 0 (synced or bypass path).

### Primary Output Path

`artefacts/product/requirements.md`

---

## File Scope

- `context/scripts/tests/README.md`
- `context/scripts/validators/README.md`

## Task

T-012: Update the scripts test inventory and validators README for the cline adapter.

### Context

- `context/scripts/tests/README.md` — the "Generator & Adapter Projections (27 tests)" section with per-file test lists
- `context/scripts/validators/README.md` — the `adapter_drift.py` description listing managed projection directories

### Instructions

1. **`context/scripts/tests/README.md`**:
   - Re-run the suite to count: after all Sprint 2 tasks, `uv run pytest context/scripts/tests/ -q` and note the new total of adapter/generator projections tests. Update the "(27 tests)" heading to the new count.
   - Add a `test_cline_adapter.py` bullet (mirroring the `test_gemini_adapter.py` bullet) in the per-file test list.
   - Add `test_cline_adapter.py` to the test-file inventory list at the bottom of the file.
2. **`context/scripts/validators/README.md`**: in the `adapter_drift.py` description, extend the parenthesised projection list to include `.clinerules/`, `.cline/skills/`, `CLINE.md`.

### Acceptance Criteria

- `grep -c "cline" context/scripts/tests/README.md context/scripts/validators/README.md` → ≥ 3 combined.
- All test-file names referenced in `context/scripts/tests/README.md` exist on disk.

### Primary Output Path

`context/scripts/tests/README.md`

---

## File Scope

- `init.sh`

## Task

T-013: Add the `cline` runtime option and pruning to `init.sh`.

### Context

- `init.sh` — runtime selection prompt (options 1-5, mapping to `targets_arr`), `ACTIVE_TARGETS` map, and the "Prune unselected runtime files" block

### Instructions

1. **Runtime prompt**: add a `cline` choice to the numbered list and the `case` mapping (e.g. new option `6)` mapped to `targets_arr+=("cline")`; if option numbering is sequential starting at 1, insert cline as `6` and keep `5|all` as-is, or renumber consistently — match the file's existing ordering).
2. **Validation**: update the `-r|--runtime` usage/help text (`Supported: gemini, claude, github, openai, cline, all`).
3. **`ACTIVE_TARGETS`**: add `ACTIVE_TARGETS["cline"]=1` in the all/initialisation block and a `cline|c|l) ACTIVE_TARGETS["cline"]=1 ;;`-style case arm (match the existing `gemini|g)` / `claude|c)` pattern — check there is no `c` collision with claude's `c` alias; if `c` is taken by `claude`, use `cline|l` or just `cline`).
4. **Pruning**: when cline is inactive, `rm -rf .clinerules CLINE.md .cline/skills` (mirror the claude block: `rm -rf .claude CLAUDE.md`).
5. **Usage header** at the top of the file: update the supported-runtime list comment.

### Acceptance Criteria

- `bash -n init.sh` → exits 0 (syntax check).
- `grep -c "cline" init.sh` → ≥ 4 distinct occurrences (prompt, case, ACTIVE_TARGETS init, pruning).
- Dry-run-safe: the new pruning line only executes when cline is not in `ACTIVE_TARGETS`.

### Primary Output Path

`init.sh`

---

# Sprint 4 — Regeneration & Verification

## File Scope

- `.agent-targets`
- Generated projections (`.clinerules/`, `.cline/`, `CLINE.md`, regenerated `AGENTS.md`) — gitignored, verified not committed

## Task

T-014: Add `cline` to `.agent-targets`, regenerate projections, and verify zero drift.

### Context

- `.agent-targets` (current content: `gemini,github`)
- `context/scripts/generators/generate_adapters.py` (the whole pipeline from T-005..T-008)

### Instructions

1. Update `.agent-targets` to `# Target AI coding runtimes configured by init.sh\ngemini,github,cline` (keep existing targets; add cline).
2. Regenerate: `uv run python context/scripts/generators/generate_adapters.py -a` → exit 0.
3. Verify outputs exist:
   - `test -f CLINE.md` and `test -f .clinerules/00-core.md` → true.
   - `ls .cline/skills/ | wc -l` → equals the number of `*.md` files in `context/skills/`.
   - `grep -c "@CLINE.md" AGENTS.md` → outputs `1`.
4. Verify drift: `uv run python context/scripts/validators/adapter_drift.py` → exit 0 and prints "All runtime adapter projections are in sync".
5. Verify `.gitignore`: `grep -c "clinerules" .gitignore` → `1`.
6. Verify generated cline files are NOT tracked by git: `git status --short -- .clinerules .cline CLINE.md AGENTS.md` → empty (all gitignored).
7. Do **not** commit the regenerated files (they are gitignored by design); only `.agent-targets` and any real source diffs from earlier tasks are committed.

### Acceptance Criteria

- Commands 2, 4 run with exit 0 and the stated output.
- The `.cline/skills/` count exactly matches canonical skill count (a mismatch means a skill failed to project — investigate, do not lower the bar).
- `git status --short` shows no generated cline files.

### Primary Output Path

`.agent-targets`

---

## File Scope

- None (verification only)

## Task

T-015: Confirm the full generator/adapter suite is green and the benchmark holds.

### Context

- All Sprint 2 test files plus `context/scripts/tests/` suite

### Instructions

1. Run the full suite: `uv run pytest context/scripts/tests/ -q` → all pass (record the count).
2. Run the unit tests: `uv run pytest tests/ -q` → all pass (canonical context validators, including the T-001/T-002 edited files).
3. Benchmark: `uv run pytest context/scripts/tests/test_cli_dispatcher.py::test_generation_execution_speed_benchmark -v` → passes with duration < 2.0s.
4. Confirm the test inventory matches T-012's updated count.
5. Write a `/tmp/T-015_commit_msg.txt` with message `test: confirm full generator/adapter suite green via baseline command in done signal`, and report the changed-file list (expected: only test/README/doc source diffs from earlier tasks if any remain uncommitted).

### Acceptance Criteria

- `uv run pytest context/scripts/tests/ -q` → `N passed` (N ≥ previous baseline + new tests) with 0 failures.
- All three commands exit 0.
- Bench duration < 2.0s.

### Primary Output Path

`/tmp/T-015_commit_msg.txt` (no repo files changed)

---

# Final Human QA Checklist

Exit criterion for the sprint. **The human performs these** in a real Cline session in this repo; agents do not.

- [ ] **Card 1 — Projection present**: Cline loads the repo and confirms `AGENTS.md` and the `@CLINE.md` pointer resolve (the runtime-entry section is visible; Cline reads `AGENTS.md` natively).
- [ ] **Card 2 — Rules active**: Cline's Rules panel shows `.clinerules/00-core.md` (workspace rule, always active).
- [ ] **Card 3 — Skills discoverable**: Cline's Skills menu lists the projected skills (e.g. `agent-sandbox`); a task like "run the TypeScript tests" triggers the relevant skill or is at least invocable via `/`.
- [ ] **Card 4 — Tool mapping correct**: Cline uses tools matching `CLINE.md`'s mappings for a sample edit + command.
- [ ] **Card 5 — Terminal safety behaviour**: run `uv run pytest context/scripts/tests/ -q` in Cline; no hang/no spinner stall; on an induced "apparent failure" the agent is observed verifying state (`git status`) before retrying.
- [ ] **Card 6 — Telemetry**: make a commit from Cline; `git log -1 --format=%B` shows `Agent-Session: tool=cline ... tokens=...` (validates the ClineExtractor path end-to-end).
- [ ] **Card 7 — Drift**: after any `context/` edit, `uv run python context/scripts/validators/adapter_drift.py` still reports in sync after regeneration.

---

## Metrics Flow

```
session-log.jsonl  →  artefact/build/metrics/session-log.jsonl    (source of truth)
    ↓ aggregate
tasks.md           →  artefacts/build/tasks-cline-projection.md   (this file)
    ↓ aggregate
git commit         →  Per-commit (Agent-Session line, one per TASK)
    ↓ aggregate
PR description     →  Per-PR rollup (pr-description-template.md)
```

---

_End of `tasks-cline-projection.md`. All tasks sequential; human QA at Gates 1–3 above._








