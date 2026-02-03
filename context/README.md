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
└── scripts/                     # Portable tools
    ├── validators/              # Rule validators
    └── generators/              # Code generators
```

For complete documentation, see full content above.
