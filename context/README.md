# Context Directory

Portable standards, rules, and agent definitions for multi-agent development workflows.

**Purpose**: This directory contains reusable context that can be pre-loaded into any project. All paths use `{project-root}` placeholders for portability.

---

## Quick Links

**Standards**: [coding](standards/coding-standards.md) | [testing](standards/testing-standards.md) | [tech](standards/tech-standards.md) | [doc](standards/doc-standards.md) | [workflow](standards/workflow-standards.md) | [visual](standards/visual-standards.md)

**Rules** (Enforceable): [commits](rules/conventional-commits.mdc) | [EARS](rules/EARS-notation-requirements.mdc) | [English](rules/british-english.mdc) | [metrics](rules/metrics-logging.mdc)

**Agents**: [all agents](agents/) | [template](agents/TEMPLATE.md)

**Workflows**: [default (TDD)](workflows/default.yaml) | [prototype (fast)](workflows/prototype.yaml)

**Templates**: [handoffs](templates/HANDOFF-TEMPLATE.md) | [reviews](templates/REVIEW-FORMAT.md) | [artefacts](templates/)

**Scripts**: [validators](scripts/validators/) | [generators](scripts/generators/)

---

## Four-Part Context System

**Separation of Concerns**: Content is organized by type and purpose to prevent redundancy.

| Directory | Purpose | Type | Example |
|-----------|---------|------|---------|
| **standards/** | HOW to do work | Guidance (human judgment) | "Use TDD cycle: RED → GREEN → REFACTOR" |
| **rules/** | WHAT constraints apply | Enforceable (binary pass/fail) | "Commits SHALL use conventional format" |
| **agents/** | WHO does work & WHEN | Role definitions | "@python-coder implements after tests written" |
| **workflows/** | Orchestration patterns | YAML definitions | "discovery → design → tdd-red → tdd-green → review" |

**Key Principle**: Agents inherit standards and rules automatically. They don't need to repeat them.

---

## Architecture

```
context/                           # Portable, pre-loadable directory
├── README.md                      # This file (index)
├── standards/                     # HOW: Guidance (coding, testing, doc, tech, workflow, visual)
├── rules/                        # WHAT: Enforceable constraints (validated by scripts)
├── agents/                       # WHO: 16 specialized agents (discovery → deploy)
├── workflows/                    # Orchestration patterns
│   ├── default.yaml             # Full TDD: 8 phases, quality gates (90% coverage, 0 critical issues)
│   └── prototype.yaml           # Fast iteration: minimal gates for POCs
├── templates/                    # Output templates (handoffs, reviews, artefacts)
│   ├── handoff-*.json           # Token-optimized: 45-81% reduction vs prose
│   └── *.template.md            # Standardized artefact formats
├── mcp/                          # MCP server config template (copy to .mcp.json on setup)
└── scripts/                     # Portable tools
    ├── validators/              # Enforce rules (british_english, conventional_commits, EARS, metrics)
    └── generators/              # Auto-generate CLAUDE.md from workflows
```

---

## Workflows

**default.yaml** (Full TDD):
- **Phases**: discovery → design → visual-design → tdd-red → tdd-green → review-gate → verification → deployment → documentation
- **Quality Gates**: 90% test coverage, 0 critical security issues, architecture compliance
- **Use When**: Production code, quality-critical projects
- **Duration**: 2-3 days for typical feature

**prototype.yaml** (Fast Iteration):
- **Phases**: Streamlined discovery → design → implement → review
- **Quality Gates**: Minimal (no coverage requirement, optional reviews)
- **Use When**: POCs, throwaway code, experiments
- **Duration**: Hours to 1 day

---

## Templates

**Purpose**: Reduce decision fatigue, ensure consistency, optimize tokens.

**Handoff Formats**:
- **Prose** (~9,526 bytes): Human-readable, external communication
- **JSON comprehensive** (~5,266 bytes): Full audit trail, 45% token reduction
- **JSON minimal** (~1,771 bytes): High-frequency coordination, 81% token reduction

**Artefact Templates**: bugs, requirements, user-stories, tasks, commit messages, PR descriptions

**Schema Validation**: JSON schemas enforce structure for handoffs and reviews.

---

## Validation

**4 Automated Validators** in `scripts/validators/`:

| Validator | Enforces | Integration |
|-----------|----------|-------------|
| `british_english.py` | British spelling (colour, artefacts) | Pre-commit hooks |
| `conventional_commits.py` | Commit format: `type(scope): description` | Pre-commit hooks |
| `ears_notation.py` | Requirements: "When/If [condition], system SHALL [action]" | CI validation |
| `metrics_logging.py` | Agent session metadata (model, tokens, duration) | Post-execution |

**Run validators**:
```bash
uv run python context/scripts/validators/british_english.py context/
uv run pytest context/scripts/tests/
```

---

## Setup for New Repository

When instantiating a new repository with this context:

1. **Copy context**: `cp -r context/ /new-repo/context/`
2. **Copy MCP config**: `cp context/mcp/mcp.json .mcp.json`
3. **Generate CLAUDE.md**: `uv run python context/scripts/generators/generate_claude_md.py`
4. **Update API keys**: Edit `.mcp.json` with your project's keys
5. **Run validators**: Integrate into pre-commit hooks (see `scripts/validators/README.md`)

**Template remains**: `context/mcp/mcp.json` stays as template; `.mcp.json` is active config.

---

## Agent Invocation

Agents are specialized roles that inherit all standards and rules automatically.

**Discovery Phase**:
- `@product-expert` - Clarify vague requirements
- `@product-owner` - Formalize requirements

**Design Phase** (parallel):
- `@solution-architect` - System architecture
- `@database-designer` - Schema design
- `@api-designer` - OpenAPI specs
- `@ui-designer` - UI/UX design
- `@visual-designer` - Visual assets

**Development Phase** (TDD):
- `@functional-tester` - Write failing tests (RED)
- `@python-coder` / `@typescript-coder` - Implement (GREEN)

**Review Phase** (quality gates):
- `@tech-lead` - Architecture compliance (GATE)
- `@code-reviewer` - Code quality

**Testing Phase**:
- `@ui-tester` - Browser testing
- `@security-tester` - OWASP, prompt injection

**Deploy & Docs**:
- `@gcp-devops` - Infrastructure-as-code
- `@documentation` - API references

**See**: `/CLAUDE.md` (auto-generated) for complete workflow and agent coordination.

---

## File Count

- **Standards**: 9 files (coding, testing, tech, doc, workflow, visual, agent, bug, build)
- **Rules**: 6 files (3 core + 3 new; 68% reduction from 19 files)
- **Agents**: 20 files (16 agents + 4 supporting docs)
- **Templates**: 23 files (handoffs, reviews, artefacts, processes)
- **Workflows**: 2 files (default TDD, prototype fast)
- **Scripts**: 15+ files (4 validators + generator + tests)

**Total**: ~75 files, fully portable, self-contained context system.
