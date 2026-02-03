# Context Directory

Portable standards, rules, and agent definitions for multi-agent development workflows.

**Purpose**: This directory contains reusable context that can be pre-loaded into any project. All paths use `{project-root}` placeholders for portability.

---

## Quick Links

| Category | Files |
|----------|-------|
| **Rules** | [python-environment](rules/python-environment.mdc) &#124; [typescript-environment](rules/typescript-environment.mdc) &#124; [secrets](rules/secrets-management.mdc) &#124; [tdd](rules/tdd-workflow.mdc) &#124; [types](rules/type-safety.mdc) &#124; [outputs](rules/output-locations.mdc) &#124; [orchestrator](rules/orchestrator-delegation.mdc) &#124; [commits](rules/conventional-commits.mdc) &#124; [spelling](rules/british-english.mdc) &#124; [EARS](rules/EARS-notation-requirements.mdc) &#124; [metrics](rules/metrics-logging.mdc) |
| **Standards** | [coding](standards/coding-standards.md) &#124; [testing](standards/testing-standards.md) &#124; [tech](standards/tech-standards.md) &#124; [doc](standards/doc-standards.md) &#124; [workflow](standards/workflow-standards.md) &#124; [visual](standards/visual-standards.md) |
| **Agents** | [all agents](agents/) &#124; [template](agents/TEMPLATE.md) |
| **Workflows** | [default (TDD)](workflows/default.yaml) &#124; [prototype (fast)](workflows/prototype.yaml) |
| **Scripts** | [validators](scripts/validators/) &#124; [generators](scripts/generators/) |

---

## Rules vs Standards

**Key insight**: Rules and standards serve different purposes and are consumed differently.

### Rules (Non-Negotiables)

**Location**: `context/rules/*.mdc`

**Purpose**: Things that **break** if not followed. Not style preferences—actual failures.

| Characteristic | Description |
|----------------|-------------|
| **Self-contained** | Agent can follow rule without cross-referencing other docs |
| **Actionable** | Clear DO/DON'T commands, not explanations |
| **Binary** | Either followed or not—no grey area |
| **Loaded by agents** | Listed in agent frontmatter, key points in body |

**Examples**:
- `python-environment.mdc`: `uv run pytest` works, bare `pytest` fails
- `secrets-management.mdc`: `/secrets/*.json` works, `.env` with creds leaks
- `tdd-workflow.mdc`: GREEN phase modifying tests breaks TDD discipline

### Standards (Reference Documentation)

**Location**: `context/standards/*.md`

**Purpose**: **How** to do things well. Context, rationale, examples, edge cases.

| Characteristic | Description |
|----------------|-------------|
| **Comprehensive** | Full documentation with examples |
| **Explanatory** | Includes rationale, trade-offs, alternatives |
| **Reference** | Agents look up when they need guidance |
| **Not loaded** | Too verbose for agent context; on-demand only |

**Examples**:
- `coding-standards.md`: Python patterns, React patterns, logging conventions
- `testing-standards.md`: TDD philosophy, coverage strategies, anti-patterns
- `tech-standards.md`: Architecture decisions, deployment strategy

### DRY Consideration

Some duplication between rules and standards is **intentional**:
- Rules tell agents **what to do** (concise, actionable)
- Standards explain **why and how** (detailed, contextual)

An agent following a rule should succeed without reading standards. Standards exist for when someone asks "why?" or hits an edge case.

---

## Orchestrator Responsibilities

The orchestrator (main Claude session or coordinating agent) has specific responsibilities.

### Delegation Principle

**Rule**: For implementation work, delegate to specialised agents when available.

| Task Type | Action |
|-----------|--------|
| Python code | Spawn `@python-coder` |
| TypeScript code | Spawn `@typescript-coder` |
| Tests | Spawn `@functional-tester` |
| Architecture | Spawn `@solution-architect` |
| Code review | Spawn `@tech-lead` or `@code-reviewer` |

**Why**: Specialised agents have rules loaded in their context. If the orchestrator writes Python directly, it may not follow `python-environment.mdc` rules.

### No Agent Available?

If there's no specialised agent for a task:

1. **Simple non-code tasks**: Orchestrator can handle directly
   - File moves, git operations, task management
   - Reading/summarising files
   - Coordinating between agents

2. **Code-adjacent tasks**: Follow relevant rules directly
   - Read the applicable rules before starting
   - State which rules you're following
   - Example: "Following `python-environment.mdc`, using `uv run python`..."

3. **New domain requiring repeated work**: Create a new agent
   - Copy `agents/TEMPLATE.md`
   - Define rules and standards in frontmatter
   - Add to workflow if ongoing

### Orchestrator Anti-Patterns

| Anti-Pattern | Why It's Bad | Do Instead |
|--------------|--------------|------------|
| Writing Python without spawning agent | Rules not loaded, may use bare `python` | Spawn `@python-coder` |
| Writing tests without spawning agent | May not follow TDD discipline | Spawn `@functional-tester` |
| Doing reviews without spawning agent | Missing review checklist context | Spawn `@tech-lead` |
| Waiting for all parallel tasks | Serial execution, not parallel | Let tracks progress independently |

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
