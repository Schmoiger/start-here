# Context Directory

Portable standards, rules, and agent definitions for multi-agent development workflows.

---

## Quick Reference

| What | Where | When |
|------|-------|------|
| **Non-negotiable rules** | `rules/*.mdc` | Agent frontmatter lists applicable rules |
| **Reference docs** | `standards/*.md` | Read when agent needs guidance |
| **Agent definitions** | `agents/*.md` | Orchestrator spawns with Task tool |
| **Workflows** | `workflows/*.yaml` | Defines phase dependencies |
| **Workflow usage guides** | `docs/workflow-*.md` | How to use each workflow (with diagrams) |
| **Orchestration patterns** | `docs/orchestration-patterns.md` | Multi-agent coordination patterns |
| **Output templates** | `templates/` | Handoff, review, artefact formats |
| **Writing personas** | `persona/*.md` | Voice/style for human-facing content (blogs, papers) |
| **Validators** | `scripts/validators/` | Pre-commit hooks, CI/CD |
| **Generators** | `scripts/generators/` | CLAUDE.md/AGENTS.md generators |

---

## For Agents

**Quick scan** - Read these when spawned:

**Rules** (non-negotiable): [python-env](rules/python-environment.mdc) · [ts-env](rules/typescript-environment.mdc) · [secrets](rules/secrets-management.mdc) · [tdd](rules/tdd-workflow.mdc) · [types](rules/type-safety.mdc) · [outputs](rules/output-locations.mdc) · [commits](rules/conventional-commits.mdc) · [spelling](rules/british-english.mdc) · [EARS](rules/EARS-notation-requirements.mdc) · [metrics](rules/metrics-logging.mdc) · [file-ops](rules/file-operations.mdc) · [handoff](rules/handoff-hygiene.mdc) · [escalation](rules/escalation.mdc) · [arch-fidelity](rules/architecture-fidelity.mdc) · [ui-reuse](rules/ui-component-reuse.mdc) · [visual](rules/visual-fidelity.mdc) · [quality-gates](rules/quality-gates.mdc)

**Standards** (reference): [coding](standards/coding-standards.md) · [testing](standards/testing-standards.md) · [tech](standards/tech-standards.md) · [doc](standards/doc-standards.md) · [workflow](standards/workflow-standards.md) · [security](standards/security-standards.md) · [context](standards/context-framework.md) · [12-factor](standards/12-factor-principles.md) · [LESS](standards/LESS-Engineering-Principles.md) · [visual](standards/visual-standards.md)

**Workflows**: [default](workflows/default.yaml) · [prototype](workflows/prototype.yaml) · [agent-effectiveness](workflows/agent-effectiveness.yaml) · [documentation-for-humans](workflows/documentation-for-humans.yaml)

**Usage guides**: [default](docs/workflow-default.md) · [prototype](docs/workflow-prototype.md) · [effectiveness](docs/workflow-agent-effectiveness.md) · [documentation-for-humans](docs/workflow-documentation-for-humans.md) · [patterns](docs/orchestration-patterns.md) · [writing-personas](docs/writing-personas.md)

**Templates**: [handoffs](templates/handoffs/) · [reviews](templates/reviews/) · [artefacts](templates/artefacts/)

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
- Frontmatter lists applicable rules + standards
- Orchestrator spawns with Task tool
- See AGENTS.md for complete reference (auto-generated from workflows)

**Workflows** (`workflows/*.yaml`):
- Phase definitions, dependencies, quality gates
- Each phase lists agents, outputs, validation
- Source of truth for phase ordering

**Workflow Usage Guides** (`docs/workflow-*.md`):
- How to use each workflow (when, how to invoke agents, phase-by-phase)
- Each includes mermaid diagram showing phase flow
- Best practices, common issues, tips

**Orchestration Patterns** (`docs/orchestration-patterns.md`):
- Multi-agent coordination patterns (single, chain, swarm, hive, loop)
- Decision tree for choosing patterns
- Token optimization strategies

**Templates** (`templates/`):
- Output formats for handoffs, reviews, artefacts
- Agents use these for consistent outputs

**Personas** (`persona/*.md`):
- Writing voice/style for human-facing content (blogs, papers, marketing)
- NOT for technical handoffs (README, API docs, architecture)
- See `docs/writing-personas.md` for complete guide

**Scripts** (`scripts/`):
- Validators: Pre-commit hooks for rule enforcement
- Generators: Auto-generate CLAUDE.md/AGENTS.md from workflows
- Tests: Validator test suite

### DRY Between Rules & Standards

Some duplication is **intentional**:
- Rules tell agents **what to do** (concise, actionable)
- Standards explain **why and how** (detailed, contextual)

An agent following a rule should succeed without reading standards. Standards exist for when someone asks "why?" or hits an edge case.

---

## Orchestrator Responsibilities

The orchestrator (main Claude session or coordinating agent) coordinates work but delegates implementation.

### Delegation Principle

**Rule**: For implementation work, delegate to specialised agents.

**Why**: Specialised agents have rules loaded in their context. If the orchestrator writes code directly, it may not follow rules like `python-environment.mdc`.

### When No Agent Exists

1. **Simple non-code tasks**: Orchestrator handles directly
   - File moves, git operations, task management
   - Reading/summarising files
   - Coordinating between agents

2. **Code-adjacent tasks**: Follow relevant rules directly
   - Read applicable rules before starting
   - State which rules you're following
   - Example: "Following `python-environment.mdc`, using `uv run python`..."

3. **New domain requiring repeated work**: Create new agent
   - Copy `agents/TEMPLATE.md`
   - Define rules and standards in frontmatter
   - Add to workflow if ongoing

---

## Workflows

See `docs/workflow-*.md` for complete usage guides with diagrams.

**Default** (`workflows/default.yaml`):
- Full TDD: 14 phases, 3 quality gates, 18 agents
- Production code, critical features
- 95% coverage (development), 97% (pre-deployment)
- Duration: 2-3 days

**Prototype** (`workflows/prototype.yaml`):
- Fast iteration: 4 phases, 0 quality gates, 5 agents
- POCs, experiments, throwaway code
- Optional coverage (smoke tests only)
- Duration: Hours to 1 day
- ⚠️ Must rewrite with default workflow before production

**Agent Effectiveness** (`workflows/agent-effectiveness.yaml`):
- Workflow addon: 1 phase, ~30min
- Analyzes efficiency, identifies bottlenecks
- Post-deployment retrospective or mid-cycle health check

**Documentation for Humans** (`workflows/documentation-for-humans.yaml`):
- Human-facing content: 5 phases, 1 agent (multiple personas)
- Blogs, papers, user guides (NOT API docs/handoffs)
- Uses writing personas (conversational, British English)
- Duration: 2-4 hours

**Orchestration patterns**: Single Agent, Sequential Chain, Parallel Swarm, Hive, Iterative Loop (see `docs/orchestration-patterns.md`)

**Framework compatibility**: Claude Code (native), LangGraph, CrewAI, AutoGen, Cursor, Aider, Continue, Windsurf (see `docs/framework-adapters.md`)

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
│   └── *.md                      # 18 specialised agents (see AGENTS.md for complete list)
├── workflows/                     # Workflow patterns (phase dependencies)
│   ├── default.yaml              # Full TDD with quality gates
│   ├── prototype.yaml            # Fast iteration
│   ├── agent-effectiveness.yaml  # Retrospective addon
│   └── documentation-for-humans.yaml # Human-facing content with personas
├── docs/                          # Usage guides
│   ├── orchestration-patterns.md       # Multi-agent coordination
│   ├── workflow-default.md             # Default workflow guide (with diagram)
│   ├── workflow-prototype.md           # Prototype workflow guide (with diagram)
│   ├── workflow-agent-effectiveness.md # Effectiveness guide (with diagram)
│   ├── workflow-documentation-for-humans.md # Human-facing content guide (with diagram)
│   ├── how-to-measure-agent-effectiveness.md # Detailed measurement examples
│   ├── writing-personas.md             # When/how to use writing personas
│   └── framework-adapters.md           # Cross-framework compatibility
├── templates/                     # Output templates
│   ├── handoffs/                 # Handoff formats
│   ├── reviews/                  # Review formats
│   └── artefacts/                # Artefact templates
├── persona/                       # Writing voice for human-facing content
│   ├── technical-writer.md       # Dr. Sarah Chen persona (blogs, papers)
│   ├── editor.md                 # Editorial voice
│   └── expert-reviewer.md        # Review voice
├── mcp/                          # MCP server configuration
│   └── mcp.json                  # Template config
└── scripts/                      # Portable tools
    ├── validators/               # Rule validators (pre-commit hooks)
    ├── generators/               # CLAUDE.md/AGENTS.md generators
    └── tests/                    # Validator tests
```

---

## Syncing Context Across Projects

**Golden source**: `start-here` repo

### Same Machine: Symlinks (Recommended)

```bash
# Keep context in start-here (git tracks changes here)
# Create symlinks FROM other repos TO start-here

cd /Users/your-username/repos/project-a
rm -rf context
ln -s /Users/your-username/Repos/start-here/context context

cd /Users/your-username/repos/project-b
rm -rf context
ln -s /Users/your-username/Repos/start-here/context context
```

**Benefits**: Instant sync, no manual copying, git tracking intact

**Git behaviour**:
- **start-here**: Tracks actual context files (commit here)
- **Other repos**: Track the symlink `context -> /path/to/start-here/context`

### Different Machines: Manual Sync

Copy context folder into each project. Use `rsync` or custom sync script for updates.

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
6. Regenerate AGENTS.md: `uv run python context/scripts/generators/generate_claude_md.py`

---

## See Also

- **Auto-generated references**: `AGENTS.md` (comprehensive agent reference from workflows)
- **Root README**: `../README.md` (deployment instructions for context system)
- **Standards index**: `standards/README.md` (detailed standards catalogue)
