# Context Directory

Portable standards, rules, and agent definitions for multi-agent development workflows.

**Purpose**: This directory contains reusable context that can be pre-loaded into any project. All paths use `{project-root}` placeholders for portability.

---

## Quick Links

| Category | Files |
|----------|-------|
| **Rules** | [python-environment](rules/python-environment.mdc) &#124; [typescript-environment](rules/typescript-environment.mdc) &#124; [secrets](rules/secrets-management.mdc) &#124; [tdd](rules/tdd-workflow.mdc) &#124; [types](rules/type-safety.mdc) &#124; [outputs](rules/output-locations.mdc) &#124; [commits](rules/conventional-commits.mdc) &#124; [spelling](rules/british-english.mdc) &#124; [EARS](rules/EARS-notation-requirements.mdc) &#124; [metrics](rules/metrics-logging.mdc) |
| **Standards** | [coding](standards/coding-standards.md) &#124; [testing](standards/testing-standards.md) &#124; [tech](standards/tech-standards.md) &#124; [doc](standards/doc-standards.md) &#124; [workflow](standards/workflow-standards.md) &#124; [security](standards/security-standards.md) &#124; [context](standards/context-framework.md) |
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
├── README.md                      # This file (index + key concepts)
├── rules/                        # Non-negotiables (break if ignored)
│   ├── python-environment.mdc   # uv run, uv add
│   ├── typescript-environment.mdc # yarn, not npm
│   ├── secrets-management.mdc   # /secrets only
│   ├── tdd-workflow.mdc         # RED fails, GREEN no test mods
│   ├── type-safety.mdc          # Type hints, strict mode
│   ├── output-locations.mdc     # artefacts/ structure
│   ├── conventional-commits.mdc # Commit format
│   ├── british-english.mdc      # Spelling
│   ├── EARS-notation-requirements.mdc # Requirements format
│   └── metrics-logging.mdc      # Agent metrics
├── standards/                    # Reference documentation
│   ├── coding-standards.md      # Code patterns, style
│   ├── context-framework.md     # Sharing formats, prioritisation, terse formats
│   ├── security-standards.md    # Security principles, safe failure, data protection
│   ├── testing-standards.md     # TDD, coverage, anti-patterns
│   ├── tech-standards.md        # Architecture, tools
│   ├── doc-standards.md         # Documentation structure
│   └── workflow-standards.md    # Processes, retrospectives
├── agents/                       # Agent definitions
│   ├── TEMPLATE.md              # Template for new agents
│   ├── python-coder.md          # Python implementation
│   ├── typescript-coder.md      # TypeScript implementation
│   ├── functional-tester.md     # Test writing
│   └── ...                      # Other specialists
├── workflows/                    # Workflow patterns
│   ├── default.yaml             # Full TDD with quality gates
│   └── prototype.yaml           # Fast iteration, skip gates
└── scripts/                     # Portable tools
    ├── validators/              # Rule validators
    └── generators/              # CLAUDE.md generator, etc.
```

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
