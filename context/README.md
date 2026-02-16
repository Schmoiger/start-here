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
| **Workflow usage guides** | `docs/workflow-*.md` | How to use each workflow |
| **Orchestration patterns** | `docs/orchestration-patterns.md` | Multi-agent coordination patterns |
| **Validators** | `scripts/validators/` | Pre-commit hooks, CI/CD |

---

## For Agents

**Rules**: [python-env](rules/python-environment.mdc) · [ts-env](rules/typescript-environment.mdc) · [secrets](rules/secrets-management.mdc) · [tdd](rules/tdd-workflow.mdc) · [types](rules/type-safety.mdc) · [outputs](rules/output-locations.mdc) · [commits](rules/conventional-commits.mdc) · [spelling](rules/british-english.mdc) · [EARS](rules/EARS-notation-requirements.mdc) · [metrics](rules/metrics-logging.mdc) · [file-ops](rules/file-operations.mdc) · [handoff](rules/handoff-hygiene.mdc) · [escalation](rules/escalation.mdc) · [arch-fidelity](rules/architecture-fidelity.mdc) · [ui-reuse](rules/ui-component-reuse.mdc) · [visual](rules/visual-fidelity.mdc)

**Standards**: [coding](standards/coding-standards.md) · [testing](standards/testing-standards.md) · [tech](standards/tech-standards.md) · [doc](standards/doc-standards.md) · [workflow](standards/workflow-standards.md) · [security](standards/security-standards.md) · [context](standards/context-framework.md) · [12-factor](standards/12-factor-principles.md) · [LESS](standards/LESS-Engineering-Principles.md) · [visual](standards/visual-standards.md)

**Delegation**: Python → `@python-coder` · TypeScript → `@typescript-coder` · Tests → `@functional-tester` · Architecture → `@solution-architect` · Reviews → `@tech-lead` / `@code-reviewer`

---

## For Humans

### Rules vs Standards

**Key insight**: Rules and standards serve different purposes.

#### Rules (Non-Negotiables)

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

#### Standards (Reference Documentation)

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

#### DRY Consideration

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

## Directory Structure

```
context/                           # Portable, pre-loadable directory
├── README.md                      # This file (index + key concepts)
├── standards/                     # Reference documentation
│   ├── README.md                 # Standards index
│   ├── coding-standards.md       # Code patterns, style
│   ├── testing-standards.md      # TDD, coverage, anti-patterns
│   ├── tech-standards.md         # Architecture, tools
│   ├── doc-standards.md          # Documentation structure
│   ├── workflow-standards.md     # Processes, retrospectives
│   ├── security-standards.md     # Security principles
│   ├── context-framework.md      # Sharing formats, terse formats
│   ├── 12-factor-principles.md   # SaaS application patterns
│   ├── LESS-Engineering-Principles.md # Design philosophy
│   ├── visual-standards.md       # Visual design standards
│   └── tech-mobile-standards.md  # Mobile standards (deferred)
├── rules/                         # Non-negotiables (break if ignored)
│   ├── python-environment.mdc    # uv run, uv add
│   ├── typescript-environment.mdc # yarn, not npm
│   ├── secrets-management.mdc    # /secrets only
│   ├── tdd-workflow.mdc          # RED fails, GREEN no test mods
│   ├── type-safety.mdc           # Type hints, strict mode
│   ├── output-locations.mdc      # artefacts/ structure
│   ├── conventional-commits.mdc  # Commit format
│   ├── british-english.mdc       # Spelling
│   ├── EARS-notation-requirements.mdc # Requirements format
│   ├── metrics-logging.mdc       # Agent metrics
│   ├── file-operations.mdc       # Write/Edit not bash
│   ├── handoff-hygiene.mdc       # Handoff completeness
│   ├── escalation.mdc            # Issue escalation
│   ├── architecture-fidelity.mdc # Architecture consistency
│   ├── ui-component-reuse.mdc    # UI component reusability
│   ├── visual-fidelity.mdc       # Visual design consistency
│   └── quality-gates.mdc         # Quality gate enforcement
├── agents/                        # Agent definitions
│   ├── TEMPLATE.md               # Template for new agents
│   ├── product-expert.md         # Requirements clarification
│   ├── product-owner.md          # Requirements formalisation
│   ├── solution-architect.md     # Architecture design
│   ├── database-designer.md      # Database schema
│   ├── api-designer.md           # API design
│   ├── ui-designer.md            # UI design
│   ├── visual-designer.md        # Visual design
│   ├── python-coder.md           # Python implementation
│   ├── typescript-coder.md       # TypeScript implementation
│   ├── functional-tester.md      # Test writing
│   ├── ui-tester.md              # E2E testing
│   ├── tech-lead.md              # Architecture review
│   ├── code-reviewer.md          # Code quality review
│   ├── principles-reviewer.md    # LESS principles review
│   ├── security-tester.md        # Security testing
│   ├── gcp-devops.md             # GCP deployment
│   ├── documentation.md          # Documentation
│   └── workflow-analyst.md       # Workflow efficiency analysis
├── workflows/                     # Workflow patterns
│   ├── default.yaml              # Full TDD with quality gates
│   ├── prototype.yaml            # Fast iteration, skip gates
│   └── agent-effectiveness.yaml  # Retrospective addon
├── docs/                          # Usage guides
│   ├── orchestration-patterns.md # Multi-agent coordination patterns
│   ├── workflow-default.md       # Default workflow usage guide
│   ├── workflow-prototype.md     # Prototype workflow usage guide
│   ├── agent-effectiveness.md    # Effectiveness analysis guide
│   ├── workflow-analyst-usage.md # Detailed analyst examples
│   └── framework-adapters.md     # Cross-framework compatibility
├── templates/                     # Output templates
│   ├── handoffs/                 # Handoff formats
│   ├── reviews/                  # Review formats
│   └── artefacts/                # Artefact templates
├── mcp/                          # MCP server configuration
│   └── mcp.json                  # Template config
└── scripts/                      # Portable tools
    ├── validators/               # Rule validators
    ├── generators/               # CLAUDE.md generator
    └── tests/                    # Validator tests
```

---

## Workflows & Orchestration

### Available Workflows

**Default** (`workflows/default.yaml` + `docs/workflow-default.md`):
- Full TDD with comprehensive reviews and testing
- 14 phases, 3 quality gates, 18 agents
- Use for: Production code, critical features
- Duration: 2-3 days typical feature
- Coverage: 95% development, 97% pre-deployment

**Prototype** (`workflows/prototype.yaml` + `docs/workflow-prototype.md`):
- Fast iteration without quality gates
- 4 phases, 0 quality gates, 5 agents
- Use for: POCs, experiments, throwaway code
- Duration: Hours to 1 day
- Coverage: Optional (smoke tests only)

**Agent Effectiveness** (`workflows/agent-effectiveness.yaml` + `docs/agent-effectiveness.md`):
- Workflow addon for retrospective analysis
- Analyzes agent/workflow efficiency, identifies bottlenecks
- Can be added to any workflow or run standalone
- Duration: ~30min

### Orchestration Patterns

See `docs/orchestration-patterns.md` for detailed guide on:

1. **Single Agent** - Simple tasks, one agent handles everything
2. **Sequential Chain** - Dependent tasks, agents run in order
3. **Parallel Swarm** - Independent tasks, agents run simultaneously
4. **Hive** - Coordinated parallel work with shared artifacts
5. **Iterative Loop** - Refinement cycle with approval gates

Each workflow combines these patterns. For example, default workflow uses:
- Sequential Chain: discovery, testing phases, review gates
- Parallel Swarm: design phase (5 independent designers)
- Hive: tdd-green, tdd-blue (parallel coders, shared tests)
- Iterative Loop: quality gates (may require fixes)

### Framework Compatibility

See `docs/framework-adapters.md` for using these workflows with:
- Claude Code (native)
- LangGraph, CrewAI, AutoGen (with adapter code)
- Cursor, Aider, Continue, Windsurf (with manual orchestration)

---

## Syncing Context Across Projects

**Note**: `start-here` is the golden source. This context folder should be copied into new projects, but can be kept in sync if actively developing across multiple repos.

### Same Machine: Use Symlinks (Recommended)

If all your repos are on the same machine, use symbolic links for automatic synchronisation.

**Setup** (one-time):

```bash
# Keep context in start-here (git tracks changes here)
# Create symlinks FROM other repos TO start-here

cd /Users/your-username/repos/project-a
rm -rf context  # Remove copied context folder
ln -s /Users/your-username/Repos/start-here/context context

cd /Users/your-username/repos/project-b
rm -rf context
ln -s /Users/your-username/Repos/start-here/context context
```

**Benefits**:
- ✅ All edits instantly reflected across all repos
- ✅ No manual sync required
- ✅ Works transparently with IDEs (Cursor, VS Code) and AI agents
- ✅ Git tracking intact (start-here tracks files, other repos track symlink)

**Workflow**:
- Edit context files in any project (bollinger, new-devx, etc.)
- Changes immediately available in all linked projects
- Run `git status` in start-here to see changes
- Commit changes in start-here repo:
  ```bash
  cd /Users/your-username/Repos/start-here
  git add context/
  git commit -m "feat(context): update agent definitions"
  ```

**Git Behavior**:
- **start-here**: Tracks actual context files (commit here)
- **Other repos**: Track the symlink `context -> /path/to/start-here/context`

### Different Machines: Manual Sync

If working across different machines or prefer not to use symlinks, copy the context folder into each project and manually sync changes as needed.

Consider creating a sync script or using `rsync` to push/pull changes between repos when context evolves.

---

## Adding New Rules

When something keeps failing because agents don't follow it:

1. **Is it binary?** Can you definitively say "followed" or "not followed"?
2. **Does it break things?** Not just style—actual failures?
3. **Is it actionable?** Can you give clear DO/DON'T commands?

If yes to all three, create a rule:

```markdown
# Rule Name

**Applies to**: [scope]

## Commands

| Action | Correct | Wrong |
|--------|---------|-------|
| ... | ... | ... |

## Why

[Brief explanation of what breaks]
```

Keep rules under 200 tokens. If you need more explanation, put it in standards.

---

## Adding New Agents

When a task domain needs repeated specialised work:

1. Copy `agents/TEMPLATE.md`
2. Set `name`, `description`, `model` in frontmatter
3. List applicable `rules` and `standards` in frontmatter
4. Write concise body with rules summary and workflow
5. Add to workflow YAML if part of standard process

See existing agents for examples.
