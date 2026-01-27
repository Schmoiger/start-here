# Documentation Standards

## 1. Introduction

This document outlines the standards for documentation across the software projects in this monorepo. Its purpose is to ensure consistent, discoverable, and useful documentation for all developers and AI agents.

## 2. Project Context

### 2.1. Documentation Location

This repository is a monorepo, containing multiple projects.

*   **Monorepo Root:** The top-level directory of the repository.
*   **Project Root:** A directory within the monorepo that contains a specific project. Each project directory shall be at the second folder level:

(monorepo root)/(major system)/(project root)

The documentation shall be structured as follows:

*   The system shall store all documentation that applies to all projects at the monorepo root, in the `/docs/` directory (e.g., `/docs/common/`).
*   The system shall store all documentation specific to a single project within that project's own `docs/` folder (e.g., `/project-a/docs/`).

For example:

```
/ (monorepo root)
├── project-a/ (project root)
│   ├── docs/
│   │   ├── build/
│   │   │   ├── bugs.md
│   │   │   ├── tasks.md
│   │   │   └── todo.md
│   │   ├── guides/
│   │   └── specs/
│   │       ├── design.md
│   │       ├── product.md
│   │       └── requirements.md
│   ├── scripts/
│   ├── src/
│   ├── tests/
│   └── README.md
├── project-b/ (project root)
│   ├── docs/
│   ├── scripts/
│   ├── src/
│   ├── tests/
│   └── README.md
```

### 2.2. Recommended Project Context Files

Where a project has a `docs/build` folder, the system shall include the following files:

*   `bugs.md`: The system shall use this file to list current and past bugs.
*   `tasks.md`: The system shall use this file to list current, past, and future tasks.
    *   The project root shall be defined and all file paths shall be relative to the project root.
    *   For each task assigned to an agent, `tasks.md` shall specify whether the agent shall commit its changes automatically upon completion or shall wait for user approval before committing.
    *   Each task description shall provide the necessary and sufficient context for an agent to execute the task, assuming it operates in a standalone context. This includes references to relevant requirements, design documents, and source files.
*   `todo.md`: The system shall use this file for a list of smaller items, technical debt, or future improvements.

Where a project has a `docs/specs` folder, the system shall include the following files:

*   `product.md`: The system shall use this file to detail the user experience of the functionality of the project.
*   `requirements.md`: The system shall use this file to detail the functional and non-functional requirements of the project.
    *   The system shall write all requirements using the EARS notation, as specified in `docs/common/rules/EARS-notation-requirements.mdc`.
*   `design.md`: The system shall use this file to describe the architectural and design decisions for the project.

### 2.3. Project `README.md`

The system shall maintain a `README.md` file in the root of each project. The `README.md` file shall describe:

-   The project's purpose.
-   Instructions for setting up the development environment and running common commands.
-   A summary of important architectural or technical decisions.
-   A list of other projects or services that this project depends on.

## 3. Common Documentation Resources

The system maintains shared documentation resources in `/docs/common/` for use across all projects. 

```
/ (monorepo root)
├── docs/
│   └── common/
│       ├── ai-allow.json
│       ├── infrastructure.md
│       ├── blueprints/
│       ├── mcp/
│       ├── rules/
│       ├── schema/
│       ├── secrets/
│       └── standards/
└── project-a/ (project root)
```

### 3.1. Common Documentation Resources

*   **`ai-allow.json`**: Defines AI agent permissions for allowed, denied, and approval-required CLI commands across the monorepo.
*   **`infrastructure.md`**: Comprehensive inventory of hosted services, databases, cloud infrastructure, and deployment configurations.
*   **`blueprints/`**: Architecture diagrams, flow charts, and design blueprints for prototypes and system components.
*   **`mcp/`**: Model Context Protocol configuration and tool definitions for AI agent integration.
*   **`rules/`**: Development guidelines and coding conventions including EARS requirements notation and TDD practices.
*   **`schema/`**: Data model definitions, API endpoint references, and type specifications used across the monorepo.
*   **`secrets/`**: Configuration templates for API keys, service accounts, and environment secrets management.
*   **`standards/`**: Development standards covering coding, testing, building, documentation, and workflow processes.

### 3.2. Context File Quality Standards

All project context files shall be reviewed from the perspective of an expert context engineer to ensure they are:

*   **Necessary**: Each piece of information serves a clear purpose in understanding or developing the project.
*   **Sufficient**: Contains all essential information needed for autonomous agent understanding and execution.
*   **Human-Friendly**: Easily understandable by humans without requiring specialized knowledge, avoiding unnecessary technical jargon.
*   **Non-Verbose**: Concise and focused, avoiding redundancy while not consuming unnecessary tokens in AI context windows.
*   **Actionable**: Provides clear, specific guidance that enables effective decision-making and implementation.
