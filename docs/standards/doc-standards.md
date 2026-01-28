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

*   The system shall store all documentation that applies to all projects at the monorepo root, in the `/docs/` directory (e.g., `/docs/standards/`, `/docs/rules/`).
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
    *   The system shall write all requirements using the EARS notation, as specified in `docs/rules/EARS-notation-requirements.mdc`.
*   `design.md`: The system shall use this file to describe the architectural and design decisions for the project.

### 2.2.1. Agent Handoff Files

The system shall maintain handoff documentation for agent coordination:

#### Service-Level Handoffs (`HANDOFF.md`)

Each service directory shall contain a `HANDOFF.md` file for intra-domain coordination:

*   **Location**: `{service-directory}/HANDOFF.md`
*   **Purpose**: Track handoffs between agents working on the same context domain
*   **Format**: Use template from `artifacts/shared/HANDOFF-TEMPLATE.md`

Required elements:
*   **Timestamp**: ISO 8601 with timezone (e.g., `2026-01-27T18:45:32Z`)
*   **From/To Agents**: Source and destination agent names with @ prefix
*   **Task IDs**: Range of tasks covered (e.g., `DS-001 through DS-008`)
*   **Status**: ✅ Complete | 🚧 In Progress | ⚠️ Blocked | 🔴 Failed
*   **Summary**: Brief description of work completed (2-3 sentences)
*   **Notes for Next Agent**: Critical information, gotchas, files to review
*   **Artifacts**: Paths to code, tests, fixtures, documentation
*   **Blockers**: Any issues preventing progress
*   **Commit Hash**: Git commit linking handoff to code changes

Example:
```markdown
### From: @functional-tester
**To**: @python-coder
**Timestamp**: 2026-01-27T18:45:32Z
**Tasks**: DS-001 through DS-008
**Status**: ✅ Complete

**Summary**: All data-service tests written and failing. Test coverage
includes yfinance integration, Bronze/Silver stores, cache management,
and API endpoints.

**Notes for Next Agent**:
- Test fixtures in tests/fixtures/
- Mock yfinance responses in tests/mocks/
- Expected cache behaviour documented in DS-005

**Artifacts**:
- Tests: `services/data-service/tests/`
- Fixtures: `services/data-service/tests/fixtures/`

**Commit**: abc1234 - test(data-service): DS-001-008 add failing tests
```

#### Cross-Domain Handoffs

For coordination between services, use `artifacts/shared/handoffs/`:

*   **Integration Status**: `artifacts/shared/handoffs/integration-status.md`
  - Master coordination file showing readiness of all domains
  - Updated when services reach integration-ready state

*   **Service API Status**: `artifacts/shared/handoffs/{service}-api.md`
  - Documents API endpoint stability for consumers
  - Created when endpoints are stable and ready for integration
  - Template: `artifacts/shared/handoffs/TEMPLATE-service-api.md`

Required elements for API handoffs:
*   **Endpoint Status**: ✅ Stable | 🚧 In Development | ⚠️ Breaking Change | 🔴 Blocked
*   **Since Timestamp**: When endpoint became stable
*   **OpenAPI Reference**: Lines in openapi.yaml
*   **Example Response**: Path to fixture file
*   **Mock Client**: Path to mock implementation
*   **Consumers**: Which services depend on this endpoint
*   **Dependencies**: Which services this endpoint depends on
*   **Known Issues**: Any bugs or limitations
*   **Breaking Changes**: Upcoming changes with ETAs

### 2.3. Project `README.md`

The system shall maintain a `README.md` file in the root of each project. The `README.md` file shall describe:

-   The project's purpose.
-   Instructions for setting up the development environment and running common commands.
-   A summary of important architectural or technical decisions.
-   A list of other projects or services that this project depends on.

## 3. Common Documentation Resources

The system maintains shared documentation resources in `/docs/` for use across all projects. 

```
/ (monorepo root)
├── docs/
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

All project context files shall be reviewed from the perspective of an expert context engineer to ensure they are:

*   **Necessary**: Each piece of information serves a clear purpose in understanding or developing the project.
*   **Sufficient**: Contains all essential information needed for autonomous agent understanding and execution.
*   **Human-Friendly**: Easily understandable by humans without requiring specialized knowledge, avoiding unnecessary technical jargon.
*   **Non-Verbose**: Concise and focused, avoiding redundancy while not consuming unnecessary tokens in AI context windows.
*   **Actionable**: Provides clear, specific guidance that enables effective decision-making and implementation.
