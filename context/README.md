# Context Directory

Portable standards, rules, and agent definitions for multi-agent development workflows.

---

## Quick Reference

| What                       | Where                            | When                                                 |
| -------------------------- | -------------------------------- | ---------------------------------------------------- |
| **Non-negotiable rules**   | `rules/*.mdc`                    | Agent frontmatter lists applicable rules             |
| **Reference docs**         | `standards/*.md`                 | Read when agent needs guidance                       |
| **Agent definitions**      | `agents/*.md`                    | Orchestrator spawns with Task tool                   |
| **Workflows**              | `workflows/*.yaml`               | Defines phase dependencies                           |
| **Model profiles (LUT)**   | `models.yaml`                    | Maps abstract intent tiers to provider families and telemetry |
| **Downstream integration** | `#downstream-integration--standards-synchronisation-git-subrepo` | Bi-directional standards synchronisation via `git-subrepo` |
| **Output templates**       | `templates/`                     | Handoff, review, artefact formats                    |
| **Writing personas**       | `persona/*.md`                   | Voice/style for human-facing content (blogs, papers) |
| **Validators**             | `scripts/validators/`            | Pre-commit hooks, CI/CD, adapter drift               |
| **Generators**             | `scripts/generators/`            | Unified runtime adapter CLI (Gemini, Claude, Copilot, Codex) |

---

## For Agents

**Quick scan** - Read these when spawned:

**Rules** (non-negotiable): [python-env](rules/python-environment.mdc) · [ts-env](rules/typescript-environment.mdc) · [secrets](rules/secrets-management.mdc) · [tdd](rules/tdd-workflow.mdc) · [types](rules/type-safety.mdc) · [outputs](rules/output-locations.mdc) · [commits](rules/git-commits.mdc) · [spelling](rules/british-english.mdc) · [EARS](rules/EARS-notation-requirements.mdc) · [bash](rules/bash-environment.mdc) · [handoff](rules/handoff-hygiene.mdc) · [escalation](rules/escalation.mdc) · [arch-fidelity](rules/architecture-fidelity.mdc) · [ui-reuse](rules/ui-component-reuse.mdc) · [visual](rules/visual-fidelity.mdc) · [quality-gates](rules/quality-gates.mdc) · [browser](rules/browser-automation.mdc)

**Standards** (reference): [coding](standards/coding-standards.md) · [testing](standards/testing-standards.md) · [tech](standards/tech-standards.md) · [doc](standards/doc-standards.md) · [workflow](standards/workflow-standards.md) · [security](standards/security-standards.md) · [context](standards/context-framework.md) · [12-factor](standards/12-factor-principles.md) · [LESS](standards/LESS-Engineering-Principles.md) · [visual](standards/visual-standards.md)

**Model Profiles (LUT)**: [models](models.yaml) — Abstract model intent tiers (`small`, `medium`, `large`), provider mapping, and telemetry locations.

**Workflows**: [build](workflows/build.yaml) · [design](workflows/design.yaml) · [prototype](workflows/prototype.yaml) · [deploy](workflows/deploy.yaml) · [bugfix](workflows/bugfix.yaml) · [full-test](workflows/full-test.yaml) · [content](workflows/content.yaml) · [continuous-improvement](workflows/continuous-improvement.yaml)

**Downstream integration**: [downstream-subrepo](#downstream-integration--standards-synchronisation-git-subrepo)

**Templates**: [index](templates/README.md)

---

## For Humans

### File Type Overview

**Rules** (`rules/*.mdc`):

- Things that **break** if not followed (not style preferences)
- Self-contained, actionable, binary (followed or not)
- Agents load these via frontmatter
- Examples: `uv run pytest` works, bare `pytest` fails; `/secrets/*.json` works, `.env` leaks

**Standards** (`standards/*.md`):

- **How** to do things well (context, rationale, examples)
- Comprehensive reference documentation
- Agents read on-demand (too verbose to preload)
- Examples: Python patterns, TDD philosophy, architecture decisions

**Agents** (`agents/*.md`):

- Specialised agent definitions (who does what)
- Frontmatter lists applicable `rules`, `standards`, and `model`
- `orchestrator.md` defines orchestrator behaviour — read at session start
- Orchestrator spawns with Task tool; see AGENTS.md for the complete registry

**Model Profiles & Runtime Telemetry LUT** (`models.yaml`):

- Decouples agent definitions from vendor-specific model identifiers
- Defines abstract intent tiers (`small`, `medium`, `large`) mapped to model families
- Delegates precise model resolution to runtime adapters / environment configurations
- Catalogues multi-platform telemetry locations (Git trailers, Claude JSONL & Managed Agents Dreams, Antigravity transcripts)

**Workflows** (`workflows/*.yaml`):

- Phase definitions, dependencies, quality gates
- Each phase lists agents, outputs, validation
- Source of truth for phase ordering

**Framework reference** (`docs/agentic-framework-reference.md`):

- Default and prototype workflows (phase-by-phase, diagrams)
- Orchestration patterns (single, chain, hive, loop — see `docs/agentic-framework-reference.md`; swarm is vision-level only)
- Writing personas, portability adapters, effectiveness measurement
- Standards, rules, agents, templates, and scripts at operational depth

**Templates** (`templates/`):

- Output formats for artefacts, handoffs, reviews, git, and agent definitions
- The orchestrator selects the appropriate template when constructing a task prompt; agents use whichever template the task prompt specifies
- See `templates/README.md` for the full index

**Personas** (`persona/*.md`):

- Writing voice/style for human-facing content (blogs, papers, marketing)
- NOT for technical handoffs (README, API docs, architecture)
- See `docs/agentic-framework-reference.md` (Writing Personas) for when and how to use them

**Scripts** (`scripts/`):

- `prepare-commit-msg.py` / `.sh`: Git hook — extracts and injects session token usage across Claude Code, Google Antigravity, GitHub Copilot, and Codex into the Agent-Session commit trailer
- Validators (`validators/`): Pre-commit hooks for rule enforcement (conventional commits, British English, EARS notation, design system, API docs, Supabase boundary, framework docs staleness)
- Generators (`generators/`): Auto-generate CLAUDE.md/AGENTS.md from agent definitions and workflows
- Tests (`tests/`): Test suite for validators, runtime adapters, and telemetry extractors


### DRY Between Rules & Standards

Some duplication is **intentional**:

- Rules tell agents **what to do** (concise, actionable)
- Standards explain **why and how** (detailed, contextual)

An agent following a rule should succeed without reading standards. Standards exist for when someone asks "why?" or hits an edge case.

---

## Orchestrator Responsibilities

The orchestrator (main Claude session) coordinates work but delegates implementation. Full behaviour defined in `context/agents/orchestrator.md` — read at session start.

**Core rule**: Delegate all implementation to specialised agents. The orchestrator writing code directly silently bypasses the environment rules those agents carry.

**When no agent exists for a task**: create one from `agents/TEMPLATE.md`, then delegate. Do not write implementation directly.

---

## Workflows

See `AGENTS.md` for the workflow index. Full phase definitions in `workflows/*.yaml`.

**build** — Primary development loop: task planning → TDD (red/green/blue) → regression → deployment. Quality gates at tasks-review, coverage, quality-review, final-holistic-review.

**design** — Discovery through design review. Run before `build`. Produces requirements, architecture, API specs, UI designs.

**prototype** — Fast iteration for POCs and experiments. No quality gates. Must rewrite with `build` before production.

**deploy** — GCP cloud deployment. Run after `build` local-deployment phase.

**full-test** — Full regression suite across all modules. Run before merge to master or on demand.

**content** — Human-facing content (blogs, papers, guides) using writing personas.

**bugfix** — Empirical bug reproduction, fix, and verification.

**continuous-improvement** — Framework improvement: reactive (human reports incident) or proactive (review interruptions, incidents, and git log metrics).

**Orchestration patterns**: Single Agent, Sequential Chain, Hive, Iterative Loop (see `docs/agentic-framework-reference.md`; exploration “swarm” is out of scope for shipped YAML — `docs/vision.md`)

---

## Directory Structure

```
context/
├── README.md                      # This file
├── standards/                     # Reference docs (how to do things well)
│   └── *.md                      # coding, testing, tech, doc, workflow, security, 12-factor, LESS, visual
├── rules/                         # Non-negotiables (break if ignored)
│   └── *.mdc                     # python-env, ts-env, secrets, tdd, types, outputs, commits, etc.
├── agents/                        # Agent definitions (who does what)
│   ├── TEMPLATE.md               # Template for new agents
│   ├── orchestrator.md           # Orchestrator behaviour (read at session start)
│   └── *.md                      # Specialised agents (see AGENTS.md for registry)
├── workflows/                     # Workflow patterns (phase dependencies)
│   ├── build.yaml                # Primary TDD development loop
│   ├── design.yaml               # Discovery through design review
│   ├── prototype.yaml            # Fast iteration / POC
│   ├── deploy.yaml               # GCP cloud deployment
│   ├── bugfix.yaml               # Bug reproduction, fix, verification
│   ├── full-test.yaml            # Full regression suite
│   ├── content.yaml              # Human-facing content with personas
│   └── continuous-improvement.yaml # Incident response + retrospective
├── templates/                     # Output templates (flat — see templates/README.md for index)
├── persona/                       # Writing voice for human-facing content
│   ├── technical-writer.md       # Amara Osei persona (practitioner guides, technical prose)
│   ├── opinionated-blogger.md   # Dr. Sarah Chen persona (blogs, opinion pieces)
│   ├── editor.md                 # Editorial voice
│   └── expert-reviewer.md        # Review voice
├── mcp/                          # MCP server configuration
│   └── mcp.json                  # Template config
└── scripts/                      # Portable tools
    ├── prepare-commit-msg.py    # Hook: inject token metrics into commits
    ├── prepare-commit-msg.sh    # Shell wrapper (symlinked from .git/hooks/)
    ├── validators/               # Rule validators (pre-commit hooks, incl. adapter_drift.py)
    ├── generators/               # Runtime adapter generators
    │   ├── generate_adapters.py  # Unified CLI dispatcher
    │   └── adapters/             # Platform adapters (core, gemini, claude, github, openai)
    └── tests/                    # Test suites (validators, adapters, E2E compilation)
```

---

## Downstream Integration & Standards Synchronisation (`git-subrepo`)

**Golden source**: `start-here` repository (`main` branch)

The framework distributes canonical context as a self-contained directory (`context/`). Downstream repositories import standards, workflows, and agents without inheriting project-specific tracking state (`artefacts/build/`, `artefacts/product/`, or application code).

Bi-directional synchronisation is managed via `git-subrepo` targeting an upstream `standards` distribution branch:

```mermaid
graph LR
    subgraph Upstream ["start-here (main)"]
        UContext["context/ (Canonical Source)"]
        UBuild["artefacts/build/ (Ignored)"]
        UBranch["standards branch (Split context/)"]
    end

    subgraph Downstream ["New Project"]
        DContext["context/ (Subrepo)"]
        DBuild["artefacts/build/ (Local Only)"]
        DCode["src / services / (Local Only)"]
    end

    UContext -- "git subrepo branch" --> UBranch
    UBranch <== "git subrepo pull / push" ==> DContext
    UBuild -. "Strictly Isolated" .- DBuild
```

### 1. Prerequisites

Downstream workstations and CI runners require:
1. **Git** (version 2.30+)
2. **`git-subrepo`**:
   ```bash
   brew install git-subrepo
   ```
   *Note: Ensure Bash 4+ is available in your PATH (`brew install bash`).*
3. **`uv`**:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

### 2. Initial Project Setup

To adopt the framework in a new or existing repository:

#### Step 1: Import Canonical Context
Run `git subrepo clone` targeting the upstream `standards` branch:

```bash
git subrepo clone git@github.com:Schmoiger/start-here.git context -b standards
```

This creates a local `context/` directory with its own `.gitrepo` tracking file. To developers on your team, `context/` appears as regular files in git—no detached `HEAD` states or recursive submodule commands are needed.

#### Step 2: Configure Pre-Commit Hooks
Add the adapter drift validator to your downstream `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: adapter-drift
        name: Validate Runtime Adapter Drift
        entry: uv run python context/scripts/validators/adapter_drift.py
        language: system
        files: ^(context/|AGENTS\.md|GEMINI\.md|CLAUDE\.md|\.agents/|\.claude/|\.github/|\.openai/)
```

Install the pre-commit hook:
```bash
uv run pre-commit install
```

#### Step 3: Compile Runtime Projections
Run the adapter generator to produce runtime projections (`AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, etc.):

```bash
uv run python context/scripts/generators/generate_adapters.py
```

Commit the generated projections:
```bash
git add .
git commit -m "chore(infra): import standards via git-subrepo and compile projections"
```

### 3. Ongoing Synchronisation Workflows

#### Pulling Upstream Updates
When standards, rules, or agent definitions are updated in `start-here`, pull changes into your downstream repository:

```bash
# 1. Pull upstream changes into context/
git subrepo pull context

# 2. Re-compile runtime adapter projections
uv run python context/scripts/generators/generate_adapters.py

# 3. Verify zero drift
uv run python context/scripts/validators/adapter_drift.py

# 4. Commit updated projections
git add -A
git commit -m "chore(standards): update canonical context and regenerate adapters"
```

#### Pushing Improvements Back Upstream
If your project enhances or fixes a standard, rule, or agent prompt inside `context/`, you can push the improvement back to the upstream `standards` branch:

```bash
# 1. Ensure tests and drift checks pass
uv run python context/scripts/validators/adapter_drift.py
uv run pytest context/scripts/tests -v

# 2. Push context/ changes directly upstream
git subrepo push context
```

Once pushed, open a Pull Request in `start-here` from the `standards` branch to `main` for review.

### 4. Testing Downstream Standards

All validator, adapter, and compilation tests are packaged inside `context/scripts/tests/` and accompany `context/` when cloned via subrepo. Downstream projects can run the test suite at any time:

```bash
uv run pytest context/scripts/tests -v
```

### 5. Upstream Maintenance & Automated Distribution (`start-here`)

The `start-here` repository automatically maintains the upstream `standards` distribution branch using the GitHub Actions workflow in `.github/workflows/sync-standards.yml`:

#### Automated Synchronisation
Whenever pull requests touching `context/**` are merged into `master`, the `sync-standards` workflow:
1. Checks out the repository with complete commit history (`fetch-depth: 0`).
2. Installs `git-subrepo`.
3. Runs `git subrepo branch context -f` to isolate `context/` commits into a clean distribution branch.
4. Pushes the branch directly to `origin/standards` using `GITHUB_TOKEN` with write permissions.

This ensures downstream projects always receive the latest approved standards via `git subrepo pull context` without requiring manual extraction by maintainers.

#### Manual Fallback
Maintainers can also manually extract and push the `standards` distribution branch locally:

```bash
# 1. Extract context/ commits into subrepo branch (requires Bash 4.0+)
PATH="/opt/homebrew/bin:$PATH" git subrepo branch context -f

# 2. Push to remote standards branch
git push origin subrepo/context:standards
```

---

## Runtime Telemetry & Session Token Tracking

The framework tracks cumulative token consumption directly from the underlying AI development runtimes and injects incremental deltas into the `Agent-Session:` git trailer at commit time via `.git/hooks/prepare-commit-msg` (delegating to `context/scripts/prepare-commit-msg.py`).

### Multi-Runtime Comparison Matrix

| Runtime | Local Telemetry Path | Repo Mapping Mechanism | Storage Format | Extracted Token Fields |
|---|---|---|---|---|
| **Anthropic Claude Code** | `~/.claude/projects/{mangled}/` | Path hash: `repo.replace('/', '-')` | JSONL (`{session}.jsonl` & `subagents/*.jsonl`) | `message.usage.input_tokens` (+ cache creation/read) & `output_tokens` |
| **Google Antigravity** | `~/.gemini/antigravity-ide/conversations/*.db` | SQLite `trajectory_metadata_blob` (`file://{repo}`) | SQLite + Protobuf binary in `gen_metadata` | Protobuf Field 1.4: Varint 2 (prompt), Varint 5 (cached), Varint 3 (output), Varint 9/10 (thinking/candidates) |
| **GitHub Copilot Chat** | `Code/User/workspaceStorage/<id>/chatSessions/` | `workspace.json` (`"folder": "file://{repo}"`) | JSONL (`<session-id>.jsonl`) | `metadata.promptTokens`, `metadata.outputTokens` / `completionTokens`, `toolCallRounds[].thinking.tokens` |
| **OpenAI Codex** | `~/.codex/` or API run logs | Project directory or API run trace | JSON / SQLite | `prompt_tokens`, `completion_tokens`, `reasoning_tokens` |

### Architectural Principles

1. **Separation of Runtime Container vs Model**:
   - The `tool=` field in `Agent-Session:` dictates the **execution container** (e.g. `tool=antigravity`, `tool=copilot`, `tool=claude-code`).
   - The `model=` field specifies the LLM (e.g. `model=gemini-flash`, `model=sonnet`, `model=gpt-5-mini`).
   - For example, running Claude Sonnet inside Google Antigravity produces `tool=antigravity model=sonnet`, causing the hook to query Antigravity's local session DB rather than Claude Code CLI storage.
2. **$O(\Delta)$ Incremental Token & Compute Efficiency**:
   - Never re-parse entire conversational histories on each commit.
   - **Antigravity**: Watermark stores `last_idx` and queries SQLite incrementally:
     `SELECT idx, data FROM gen_metadata WHERE idx > ? ORDER BY idx ASC`
   - **Copilot & Claude**: Watermark stores the file byte offset and `seek()`s directly to newly appended lines.
3. **Transparent Error Surfacing over Silent Failure**:
   - If an agent commit trailer (`Agent-Session:`) is present but telemetry extraction fails (e.g., unexpected schema change or missing session), the hook injects:
     ```text
     Agent-Session: tool=antigravity model=gemini-flash ... tokens=error(schema_drift)
     ```
   - Diagnostic warnings are written to `stderr`, and the commit is allowed to succeed with exit code 0.
4. **Brittleness & Maintenance**:
   - Neither Antigravity nor Copilot provides a public, frozen API for local telemetry; extraction relies on internal storage patterns.
   - The test suite in `context/scripts/tests/test_runtime_telemetry.py` includes live runtime sanity checks that run in local development:
     - **Not installed**: Skipped cleanly.
     - **Installed but idle**: Skipped with diagnostic note (`"Runtime installed but no active sessions found for validation"`).
     - **Installed with active sessions**: Fails immediately if vendor schema changes or data formats drift.

---

## Adding New Rules

When something keeps failing because agents don't follow it:

1. **Is it binary?** Can you definitively say "followed" or "not followed"?
2. **Does it break things?** Not just style—actual failures?
3. **Is it actionable?** Can you give clear DO/DON'T commands?

If yes to all three, create a rule in `rules/*.mdc` (keep under 200 tokens).

---

## Adding New Agents

When a task domain needs repeated specialised work:

1. Copy `agents/TEMPLATE.md`
2. Set `name`, `description`, `model` in frontmatter
3. List applicable `rules` and `standards` in frontmatter
4. Write concise body with rules summary and workflow
5. Add to workflow YAML if part of standard process
6. Regenerate adapter projections: `uv run python context/scripts/generators/generate_adapters.py`

---

## See Also

- **AGENTS.md** / **CLAUDE.md** / **GEMINI.md** — auto-generated workflow + agent registries (run `generate_adapters.py` to update)
- **Root README**: `../README.md` — deployment instructions for context system and runtime adapters
- **Standards index**: `standards/README.md` — detailed standards catalogue
