# Documentation Standards

## 1. Introduction

This document outlines the standards for documentation across the software projects in this monorepo. Its purpose is to ensure consistent, discoverable, and useful documentation for all developers and AI agents.

## 2. Project Context

### 2.1. Documentation Location

This repository is a monorepo, containing multiple projects.

*   **Monorepo Root:** The top-level directory of the repository.
*   **Project Root:** A directory within the monorepo that contains a specific project. Each project directory shall be at the second folder level:

(monorepo root)/(major system)/(project root)

The documentation shall be structured with a clear separation of concerns:

*   **`/context/`** (Monorepo Root): Shared input knowledge that applies to all projects—agent definitions, standards, rules, and MCP configurations. This is **input** that guides how work is done.
*   **`/artifacts/`** (Project Root): Project-specific work output—specifications, tasks, bugs, design documents, and guides. This is **output** produced during development.

For example:

```
/ (monorepo root)
├── context/                      # Shared input (applies to all projects)
│   ├── agents/                   # Agent role definitions
│   ├── mcp/                      # Model Context Protocol configs
│   ├── rules/                    # Development rules and conventions
│   └── standards/                # Development standards
├── project-a/ (project root)
│   ├── artifacts/                # Project work output
│   │   ├── api/                  # API specifications
│   │   ├── architecture/         # Architecture decisions
│   │   ├── bugs/                 # Bug tracking
│   │   ├── design/               # UI/UX design
│   │   ├── product/              # Product specs
│   │   ├── shared/               # Shared fixtures, handoffs, mocks
│   │   └── tasks/                # Task breakdowns
│   ├── scripts/
│   ├── src/
│   ├── tests/
│   └── README.md
├── project-b/ (project root)
│   ├── artifacts/                # Project work output
│   ├── scripts/
│   ├── src/
│   ├── tests/
│   └── README.md
```

### 2.1.1. Separation of Concerns: Context vs Artifacts

**`/context/` = Input (Shared Knowledge)**
- Contains reusable knowledge that guides how work is done across all projects
- Includes: agent definitions, coding standards, workflow rules, MCP tool configs
- **Purpose**: Provides the "how" and "who" for development work
- **Lifecycle**: Persistent, version-controlled, shared across projects
- **Location**: Monorepo root only

**`/artifacts/` = Output (Project Work)**
- Contains project-specific deliverables produced during development
- Includes: specifications, requirements, design docs, tasks, bugs, guides, handoffs
- **Purpose**: Documents "what" is being built and tracks progress
- **Lifecycle**: Project-specific, may be ephemeral during development, promoted to final docs after approval
- **Location**: Each project root has its own `artifacts/` folder

This separation ensures that:
- Shared knowledge (context) remains clean and reusable
- Project work (artifacts) is clearly scoped to specific deliverables
- Agents can distinguish between "how to work" (context) and "what to build" (artifacts)

### 2.2. Recommended Project Artifacts Structure

Projects should organize their work output in the `artifacts/` folder. The following structure is recommended:

**`artifacts/product/`** - Product specifications:
*   `product.md` (or `user-stories.md`): Product vision, goals, user stories, and success criteria
*   `requirements.md`: Functional and non-functional requirements using EARS notation (see `context/rules/EARS-notation-requirements.mdc`)
*   `open-questions.md`: Unresolved product questions and decisions

**`artifacts/architecture/`** - Technical architecture:
*   `architecture.md`: System architecture and technical design decisions
*   `data-model.md`: Data models and schemas

**`artifacts/design/`** - UI/UX design:
*   `design.md` (or `components.md`, `wireframes.md`): UI component specifications and wireframes
*   `design-tokens.json`: Design system tokens
*   `user-flows.md`: User interaction flows
*   `visuals/`: Design assets (SVGs, images, themes)

**`artifacts/api/`** - API specifications:
*   `openapi.yaml`: OpenAPI specification
*   `api-contract.json`: API contract definitions
*   `api-design-guide.md`: API design guidelines

**`artifacts/tasks/`** - Task management:
*   `tasks.md` (or per-service files like `tasks-data-service.md`): Task breakdowns with task IDs
    *   The project root shall be defined and all file paths shall be relative to the project root.
    *   For each task assigned to an agent, tasks shall specify whether the agent shall commit its changes automatically upon completion or shall wait for user approval before committing.
    *   Each task description shall provide the necessary and sufficient context for an agent to execute the task, assuming it operates in a standalone context. This includes references to relevant requirements, design documents, and source files.
*   `todo.md`: Smaller items, technical debt, or future improvements

**`artifacts/bugs/`** - Bug tracking:
*   `bugs.md` (or per-service files like `*-bugs.md`): Bug tracking following `context/standards/bug-standards.md`
*   `code-review-*.md`: Detailed code review documentation

**`artifacts/shared/`** - Cross-cutting artifacts:
*   `handoffs/`: Agent-to-agent handoff documentation (see section 2.2.1)
*   `HANDOFF-TEMPLATE.md`: Template for intra-domain agent handoffs
*   `TEMPLATE-handoff-to-human.md`: Template for handoffs to humans (format and behaviour in `context/standards/agent-standards.md` section 3.4.5)
*   `fixtures/`: Test fixtures and sample data
*   `mocks/`: Mock implementations for testing

Handoffs from agents to humans use a single file `artifacts/HANDOFF-TO-HUMAN.md` (overwritten each time). Format and behaviour are in agent-standards section 3.4.5.

### 2.2.1. Agent Handoff Files (Locations Only)

Handoff *format*, *required elements*, *workflow*, and *handoffs to humans* are defined in `context/standards/agent-standards.md` (section 3.4). This section defines *where* handoff files live.

**Intra-domain** (same service/package):
*   `{service-directory}/HANDOFF.md`
*   Template: `artifacts/shared/HANDOFF-TEMPLATE.md`

**Inter-domain** (between services), under `artifacts/shared/handoffs/`:
*   `integration-status.md` — master coordination file for readiness of all domains
*   `{service}-api.md` — API endpoint stability for consumers; template: `TEMPLATE-service-api.md`

### 2.3. Project `README.md`

The system shall maintain a `README.md` file in the root of each project. The `README.md` file shall describe:

-   The project's purpose.
-   Instructions for setting up the development environment and running common commands.
-   A summary of important architectural or technical decisions.
-   A list of other projects or services that this project depends on.

## 3. Common Documentation Resources

The system maintains shared documentation resources in `/context/` for use across all projects. 

```
/ (monorepo root)
├── context/
│   ├── agents/
│   ├── mcp/
│   ├── rules/
│   └── standards/
└── project-a/ (project root)
```

### 3.1. Common Documentation Resources

*   **`agents/`**: AI agent definitions and configurations for different roles and responsibilities.
*   **`mcp/`**: Model Context Protocol configuration and tool definitions for AI agent integration.
*   **`rules/`**: Development guidelines and coding conventions including EARS requirements notation and TDD practices.
*   **`standards/`**: Development standards covering coding, testing, building, documentation, and workflow processes.

### 3.2. Context File Quality Standards

All files in `/context/` (shared input knowledge) shall be reviewed from the perspective of an expert context engineer to ensure they are:

*   **Necessary**: Each piece of information serves a clear purpose in understanding or developing the project.
*   **Sufficient**: Contains all essential information needed for autonomous agent understanding and execution.
*   **Human-Friendly**: Easily understandable by humans without requiring specialized knowledge, avoiding unnecessary technical jargon.
*   **Non-Verbose**: Concise and focused, avoiding redundancy while not consuming unnecessary tokens in AI context windows.
*   **Actionable**: Provides clear, specific guidance that enables effective decision-making and implementation.

**Note**: Files in `artifacts/` (project work output) have different quality standards—they are project-specific deliverables that evolve during development. They should be clear and well-structured, but they don't need to meet the same "reusable across all projects" standard as `/context/` files.
