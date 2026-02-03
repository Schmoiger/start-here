# Start Here

**Portable multi-agent development context** for AI-assisted software engineering.

This repository provides a complete, reusable context system that can be copied into any new project to enable structured, high-quality multi-agent workflows.

---

## What's Included

- **`context/`** - Portable standards, rules, agents, workflows, templates, and validation scripts
- **`artefacts/`** - Example output structure (requirements, architecture, design, tests)
- **`CLAUDE.md`** - Auto-generated orchestration guide (16 agents, TDD workflow)

**Total**: ~75 context files covering coding standards, TDD workflow, 16 specialized agents, 23 templates, and automated validators.

---

## Quick Start: New Repository Setup

### 1. Copy Context to Your Project

```bash
# Clone or copy this repository
git clone https://github.com/Schmoiger/start-here.git
cd start-here

# Copy to your new project
cp -r context/ /path/to/your-project/context/
cp CLAUDE.md /path/to/your-project/CLAUDE.md
```

### 2. Configure MCP Servers (Claude Code)

For **Claude Code** (CLI):

```bash
# Copy MCP configuration to .claude directory
mkdir -p ~/.claude
cp context/mcp/mcp.json ~/.claude/mcp.json

# Edit with your API keys
vim ~/.claude/mcp.json
```

For **Claude Desktop** (GUI):

```bash
# Copy MCP configuration to Claude config directory
# macOS:
cp context/mcp/mcp.json ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Windows:
# %APPDATA%\Claude\claude_desktop_config.json

# Linux:
# ~/.config/Claude/claude_desktop_config.json
```

For **Cursor IDE**:

```bash
# Copy to project root as .mcp.json
cp context/mcp/mcp.json /path/to/your-project/.mcp.json
```

For **Other Tools** (Aider, Continue, etc.):

```bash
# Copy to project root
cp context/mcp/mcp.json /path/to/your-project/.mcp.json

# Or follow tool-specific MCP configuration instructions
```

### 3. Generate CLAUDE.md

```bash
cd /path/to/your-project

# Generate orchestration guide from workflow
uv run python context/scripts/generators/generate_claude_md.py

# Output: /CLAUDE.md (16 agents, TDD workflow, quality gates)
```

### 4. Set Up Validation (Optional)

```bash
# Install dependencies
cd context/scripts
uv sync

# Run validators
uv run python validators/british_english.py ../
uv run python validators/conventional_commits.py

# Run tests
uv run pytest tests/

# Add to pre-commit hooks (see context/scripts/validators/README.md)
```

### 5. Create Artefacts Structure

```bash
# Create output directories for your project
mkdir -p artefacts/{product,architecture,api,design,build,test-results,shared}
mkdir -p artefacts/shared/{handoffs,fixtures,mocks}

# Or copy example structure
cp -r artefacts/ /path/to/your-project/artefacts/
```

---

## What You Get

### Context System (Portable)

**Standards** (9 files) - HOW to do work:
- `coding-standards.md` - Code quality, style, patterns
- `testing-standards.md` - TDD cycle, 90% coverage minimum
- `tech-standards.md` - Technology stack, 12-factor app
- `doc-standards.md` - Documentation structure
- `workflow-standards.md` - Development processes
- `visual-standards.md` - Design, WCAG 2.1 AA accessibility
- `agent-standards.md` - Agent interaction patterns
- `bug-standards.md` - Bug tracking format
- `build-standards.md` - Build and deployment

**Rules** (6 files) - WHAT constraints (enforceable):
- `british-english.mdc` - Spell checking (colour, artefacts)
- `conventional-commits.mdc` - Commit format validation
- `EARS-notation-requirements.mdc` - Requirements syntax
- `metrics-logging.mdc` - Agent session metadata

**Agents** (16 specialized roles):
- **Discovery**: product-expert, product-owner
- **Design**: solution-architect, database-designer, api-designer, ui-designer, visual-designer
- **Development**: functional-tester, python-coder, typescript-coder
- **Review**: tech-lead, code-reviewer
- **Testing**: ui-tester, security-tester
- **Deploy**: gcp-devops, documentation

**Workflows** (2 YAML definitions):
- `default.yaml` - Full TDD (8 phases, 90% coverage, 0 critical issues)
- `prototype.yaml` - Fast iteration (minimal gates)

**Templates** (23 files):
- Handoff formats (prose, JSON: 45-81% token reduction)
- Review formats
- Artefact templates (bugs, requirements, user-stories, tasks)
- Process templates (commit messages, PR descriptions)

**Validators** (4 automated):
- British English spell checker
- Conventional commit format
- EARS requirements notation
- Agent metrics structure

---

## Workflows

### Default TDD Workflow (Production Code)

**8 Phases**:
1. **Discovery** - @product-expert + @product-owner define requirements
2. **Design** - @solution-architect, @database-designer, @api-designer, @ui-designer (parallel)
3. **Visual Design** - @visual-designer creates polished assets
4. **TDD RED** - @functional-tester writes failing tests
5. **TDD GREEN** - @python-coder/@typescript-coder implement
6. **Review Gate** - @tech-lead (architecture) → @code-reviewer (quality)
7. **Verification** - @ui-tester, @security-tester validate
8. **Deploy & Docs** - @gcp-devops, @documentation

**Quality Gates**:
- 90% test coverage minimum
- 0 critical security issues
- Architecture compliance review passed

**Duration**: 2-3 days for typical feature

### Prototype Workflow (POCs)

**4 Phases**:
1. Discovery (quick requirements)
2. Design (architecture sketch)
3. Implement (no test requirement)
4. Review (optional)

**Duration**: Hours to 1 day

---

## File Structure

```
your-project/
├── CLAUDE.md                      # Auto-generated orchestration guide
├── .mcp.json                      # Active MCP config (copy from context/mcp/)
├── context/                       # Portable context (version controlled)
│   ├── standards/                # HOW: Guidance (9 files)
│   ├── rules/                    # WHAT: Enforceable (6 files)
│   ├── agents/                   # WHO: 16 agents + templates
│   ├── workflows/                # Orchestration (default, prototype)
│   ├── templates/                # Output templates (23 files)
│   ├── mcp/                      # MCP config template
│   └── scripts/                  # Validators + generators
├── artefacts/                    # Project outputs (version controlled)
│   ├── product/                  # Requirements, user stories
│   ├── architecture/             # System design, data models
│   ├── api/                      # OpenAPI specs
│   ├── design/                   # UI/UX, design tokens
│   ├── build/                    # Bugs, tasks, reviews
│   ├── test-results/             # Test outputs, coverage
│   └── shared/                   # Handoffs, fixtures, mocks
└── [your code, tests, etc.]
```

---

## Key Features

### Separation of Concerns

| Type | Purpose | Example |
|------|---------|---------|
| **Standards** | Guidance (human judgment) | "Use TDD cycle: RED → GREEN → REFACTOR" |
| **Rules** | Enforceable (binary pass/fail) | "Commits SHALL use conventional format" |
| **Agents** | Specialized roles | "@python-coder implements after tests" |
| **Workflows** | Orchestration patterns | "discovery → design → tdd → review" |

### Token Optimization

- **Handoff formats**: 45-81% token reduction (JSON vs prose)
- **Templates**: Standardized structures reduce LLM decision overhead
- **Compressed formats**: `handoff-example-minimal.json` (1,771 bytes vs 9,526 bytes prose)

### Quality Automation

- **4 validators**: British English, conventional commits, EARS notation, metrics
- **Pre-commit hooks**: Catch issues before CI/CD
- **Test suite**: Validate all validators work correctly

### British English Consistency

- Directory: `/artefacts/` (not `/artifacts/`)
- Spelling: colour, behaviour, optimise, artefacts
- Validator: `british_english.py` enforces throughout

---

## Common Tasks

### Generate CLAUDE.md

```bash
uv run python context/scripts/generators/generate_claude_md.py
```

### Validate British English

```bash
uv run python context/scripts/validators/british_english.py context/
```

### Validate Commit Messages

```bash
uv run python context/scripts/validators/conventional_commits.py "feat(api): add user endpoint"
```

### Validate Requirements (EARS)

```bash
uv run python context/scripts/validators/ears_notation.py artefacts/product/requirements.md
```

### Run All Tests

```bash
cd context/scripts
uv run pytest tests/
```

---

## Customization

### Add Your Own Agent

1. Copy template: `cp context/agents/TEMPLATE.md context/agents/my-agent.md`
2. Edit YAML frontmatter (name, model, tools, standards, rules)
3. Write system prompt defining role and responsibilities
4. Add to workflow: Edit `context/workflows/default.yaml`
5. Regenerate CLAUDE.md: `uv run python context/scripts/generators/generate_claude_md.py`

### Modify Workflow

1. Edit `context/workflows/default.yaml` or create new workflow
2. Regenerate CLAUDE.md
3. Test with agents following new workflow

### Add Validation Rule

1. Create validator in `context/scripts/validators/`
2. Add rule documentation in `context/rules/`
3. Add tests in `context/scripts/tests/`
4. Integrate into pre-commit hooks

---

## Documentation

- **`context/README.md`** - Complete context system documentation
- **`CLAUDE.md`** - Auto-generated orchestration guide (read this first for workflow)
- **`context/agents/`** - Individual agent role definitions
- **`context/standards/`** - Development standards (coding, testing, doc, etc.)
- **`context/workflows/`** - YAML workflow definitions

---

## Framework Compatibility

This context system is **framework-agnostic** and works with:

- **Claude Code** (native) - MCP config in `~/.claude/mcp.json`
- **Claude Desktop** - MCP config in app config directory
- **Cursor IDE** - `.mcp.json` in project root
- **Aider** - Use `.mcp.json` or Aider's context system
- **Continue.dev** - Use `.mcp.json` or Continue's context
- **LangChain/LangGraph** - Adapt agents to LangGraph nodes
- **CrewAI** - Map agents to CrewAI roles
- **AutoGen** - Map agents to AutoGen agents

See `context/README.md` for adaptation guidance.

---

## Support

- **Issues**: https://github.com/Schmoiger/start-here/issues
- **Context docs**: `context/README.md`
- **Workflow guide**: `CLAUDE.md` (auto-generated)
- **Agent definitions**: `context/agents/`

---

## License

This context system is provided as-is for use in your projects. Customize freely.
