# Context Directory

Portable standards, rules, and agent definitions for multi-agent development workflows.

**Purpose**: This directory contains reusable context that can be pre-loaded into any project. All paths use `{project-root}` placeholders for portability.

---

## Quick Links

**Standards**: [coding](standards/coding-standards.md) | [testing](standards/testing-standards.md) | [tech](standards/tech-standards.md) | [doc](standards/doc-standards.md) | [workflow](standards/workflow-standards.md)

**Rules** (Enforceable): [commits](rules/conventional-commits.mdc) | [EARS](rules/EARS-notation-requirements.mdc) | [English](rules/british-english.mdc) | [metrics](rules/metrics-logging.mdc)

**Agents**: [all agents](agents/) | [template](agents/TEMPLATE.md)

**Workflows**: [default (TDD)](workflows/default.yaml) | [prototype (fast)](workflows/prototype.yaml)

**Scripts**: [validators](scripts/validators/) | [generators](scripts/generators/)

---

## Architecture

```
context/                           # Portable, pre-loadable directory
├── README.md                      # This file (index)
├── standards/                     # Guidance (how to do things)
├── rules/                        # Enforceable (binary pass/fail)
├── agents/                       # Agent definitions
├── workflows/                    # Workflow patterns
│   ├── default.yaml             # Full TDD with all gates
│   └── prototype.yaml           # Fast iteration
├── templates/                    # Output templates
├── mcp/                          # MCP server configuration (copy to root on instantiation)
└── scripts/                     # Portable tools
    ├── validators/              # Rule validators
    └── generators/              # Code generators
```

## Setup for New Repository

When instantiating a new repository with this context:

1. Copy entire `context/` directory to new repo
2. **Copy MCP config to root**: `cp context/mcp/mcp.json .mcp.json`
3. Generate CLAUDE.md: `uv run python context/scripts/generators/generate_claude_md.py`
4. Update API keys in `.mcp.json` for your project

The `context/mcp/mcp.json` file remains as a template; the root `.mcp.json` is the active configuration.
