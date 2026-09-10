# Start Here

Portable multi-agent development context for AI-assisted software engineering.

---

## Quick Deployment

### 1. Copy to Your Project

```bash
# Copy context directory and orchestration guide
cp -r context/ /path/to/your-project/context/
cp CLAUDE.md /path/to/your-project/CLAUDE.md
cp AGENTS.md /path/to/your-project/AGENTS.md
```

### 2. Configure MCP (Optional)

```bash
# Claude Code CLI
cp context/mcp/mcp.json ~/.claude/mcp.json

# Claude Desktop
# macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
# Windows: %APPDATA%\Claude\claude_desktop_config.json
# Linux: ~/.config/Claude/claude_desktop_config.json

# Cursor IDE
cp context/mcp/mcp.json /path/to/your-project/.mcp.json
```

### 3. Generate Runtime Adapters

```bash
cd /path/to/your-project
# Smart update all projections (Gemini, Claude Code, Copilot, Codex)
uv run python context/scripts/generators/generate_adapters.py

# Or generate for a specific runtime
uv run python context/scripts/generators/generate_adapters.py -t claude
uv run python context/scripts/generators/generate_adapters.py -g          # Gemini / Antigravity
uv run python context/scripts/generators/generate_adapters.py -p          # GitHub Copilot
uv run python context/scripts/generators/generate_adapters.py -o          # OpenAI / Codex
```

### 4. Create Artefacts Structure

```bash
mkdir -p artefacts/{product,architecture,design,build,test-results,shared}
mkdir -p artefacts/shared/{handoffs,fixtures,mocks}
```

---

## Runtime Adapters & Architecture

This framework employs a **Hexagonal (Ports and Adapters)** architecture to ensure cross-platform portability across AI coding runtimes.

```
                  ┌─────────────────────────────────────┐
                  │    Canonical Context (Source of Truth) │
                  │  • context/agents/*.md               │
                  │  • context/workflows/*.yaml          │
                  │  • context/rules/*.mdc               │
                  │  • context/standards/*.md            │
                  │  • context/models.yaml               │
                  └──────────────────┬──────────────────┘
                                     │
                        generate_adapters.py (CLI)
                                     │
      ┌───────────────┬──────────────┴──────────────┬───────────────┐
      ▼               ▼                             ▼               ▼
┌───────────┐   ┌───────────┐                 ┌───────────┐   ┌───────────┐
│ Antigravity│  │Claude Code│                 │  GitHub   │   │  OpenAI   │
│  / Gemini │   │           │                 │  Copilot  │   │  / Codex  │
├───────────┤   ├───────────┤                 ├───────────┤   ├───────────┤
│.agents/   │   │CLAUDE.md  │                 │.github/   │   │.openai/   │
│skills/    │   │.claude/   │                 │prompts/   │   │prompts/   │
│GEMINI.md  │   │prompts/   │                 │instructs/ │   │tools.json │
└───────────┘   └───────────┘                 └───────────┘   └───────────┘
```

### Core Non-Functional Requirements (NFRs)

1. **Autonomy**: Each projection provides self-contained context and tool contracts tailored to the target platform, enabling autonomous agent loops and subagent spawning without human intervention.
2. **Token Efficiency**: Scoped projection instructions and selective includes ensure agent context windows are never polluted with irrelevant guidelines. Model tiers (`small`, `medium`, `large`) route tasks to cost-effective models via `models.yaml`. Smart generation (`--new`) only writes modified files, preventing file-watcher and cache churn.
3. **Intent Preservation**: The canonical definition in `context/` acts as the single source of truth. Projections are deterministic transformations ensuring consistent engineering standards across all AI tools.

### CLI Usage (`generate_adapters.py`)

```bash
# Smart update: write only changed or new files (default)
uv run python context/scripts/generators/generate_adapters.py

# Force full regeneration of all files
uv run python context/scripts/generators/generate_adapters.py -a

# Dry-run: preview files that would be modified without writing to disk
uv run python context/scripts/generators/generate_adapters.py -d

# Target filtering with convenience shortcuts
uv run python context/scripts/generators/generate_adapters.py -g          # Gemini / Antigravity
uv run python context/scripts/generators/generate_adapters.py -c          # Claude Code
uv run python context/scripts/generators/generate_adapters.py -p          # GitHub Copilot
uv run python context/scripts/generators/generate_adapters.py -o          # OpenAI / Codex
```

### Automated Drift Enforcement (`adapter_drift.py`)

To prevent divergence between canonical context files and generated adapter projections, an automated drift validator runs during pre-commit checks:

```bash
uv run python context/scripts/validators/adapter_drift.py
```

If any generated projection is missing, manually edited, or out of date, the validator fails with exit code `1` and actionable remediation instructions.

---

## Documentation

- **Getting started**: See `context/README.md` - Complete guide for agents and humans
- **Workflow guide**: See `AGENTS.md` / `CLAUDE.md` - Auto-generated orchestration guides
- **Agent reference**: See `context/agents/` - Individual agent definitions
- **Standards**: See `context/standards/` - Coding, testing, tech stack guidance
- **Workflows**: See `context/workflows/` - Structured delivery pipelines (TDD, design, prototype, content, deploy, bugfix)
- **Validators**: See `context/scripts/validators/README.md` - Pre-commit consistency validators

---

## What's Included

- **19 specialised agents** - Discovery, architecture, coding, review, testing, deployment, workflow analysis, tokenomics
- **14 standards** - Coding, testing, architecture, tech stack, documentation, security
- **18 rules** - Enforceable constraints with automated validators
- **9 workflows** - Including build (Detroit TDD), design, prototype, content, deploy, bugfix, full-test, continuous-improvement, retrospective
- **4 runtime adapters** - Antigravity/Gemini, Claude Code, GitHub Copilot, OpenAI/Codex
- **1 unified generator CLI** - Deterministic compilation with smart change detection and drift prevention
