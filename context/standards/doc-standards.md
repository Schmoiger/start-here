# Documentation Standards

## 1. Introduction

This document outlines the standards for documentation across the software projects in this monorepo. Its purpose is to ensure consistent, discoverable, and useful documentation for all developers and AI agents.

## 2. Project Context

### 2.1. Directory Structure

This repository is a monorepo, containing multiple projects (services and packages).

*   **Monorepo Root:** The top-level directory of the repository.
*   **Project Root:** A directory within the monorepo that contains a specific project (e.g., `/services/data-service/`, `/packages/shared-types/python/`).

The documentation shall be structured as follows:

*   **`/context/`**: Input files at monorepo root containing standards and rules for all projects
    *   `/context/standards/`: Development standards (coding, testing, documentation, workflow)
    *   `/context/rules/`: Development guidelines (EARS notation, TDD practices)
*   **`/artifacts/`**: Output files representing work completed
    *   Monorepo root `/artifacts/`: System-wide artifacts (architecture, requirements, API contracts, design)
    *   Project-level `{service}/artifacts/`: Service-specific artifacts (bugs, tasks, todo, test results)

For example:

```
/ (monorepo root)
├── context/                         # INPUT: Standards & rules
│   ├── standards/
│   │   ├── coding-standards.md
│   │   ├── doc-standards.md
│   │   └── testing-standards.md
│   └── rules/
│       └── EARS-notation-requirements.mdc
│
├── artifacts/                       # OUTPUT: System-wide
│   ├── architecture.md
│   ├── requirements.md
│   ├── user-stories.md
│   ├── data-model.md
│   ├── api/
│   │   ├── openapi.yaml
│   │   └── api-design-guide.md
│   ├── design/
│   │   ├── design-tokens.json
│   │   └── wireframes.md
│   └── shared/
│       ├── handoffs/
│       ├── fixtures/
│       └── mocks/
│
├── services/data-service/           # Service example
│   ├── artifacts/                   # OUTPUT: Service-specific
│   │   ├── bugs.md
│   │   ├── tasks.md
│   │   ├── todo.md
│   │   ├── test-results/
│   │   └── fixtures/
│   ├── HANDOFF.md                   # Intra-service coordination
│   ├── src/
│   ├── tests/
│   └── README.md
│
└── packages/shared-types/python/    # Package example
    ├── artifacts/
    │   ├── bugs.md
    │   ├── tasks.md
    │   ├── todo.md
    │   └── test-results/
    ├── bollinger_types/
    ├── tests/
    └── README.md
```

### 2.2. Artifact Organization Principle

**Rule**: Context is organized by domain boundary.

*   **Service-specific artifacts** → `{service}/artifacts/`
    *   Example: Bugs only affecting data-service go in `services/data-service/artifacts/bugs.md`
*   **System-wide artifacts** → `/artifacts/` (monorepo root)
    *   Example: System architecture affecting all services goes in `/artifacts/architecture.md`
*   **Cross-service coordination** → `/artifacts/shared/`
    *   Example: Integration handoffs go in `/artifacts/shared/handoffs/`

### 2.3. Service/Package Artifact Files

Each service or package shall maintain the following files in its `artifacts/` directory:

*   **`bugs.md`**: Current and past bugs (per bug-standards.md format)
    *   Format: One line per bug with status, description, file path, and link
    *   Example: `[TODO] | Cache isolation bug INSTEAD shared cache | src/routers/cache.py:83 | #BUG-001`
*   **`tasks.md`**: Current, past, and future tasks
    *   The project root shall be defined and all file paths shall be relative to the project root
    *   For each task assigned to an agent, `tasks.md` shall specify whether the agent shall commit its changes automatically upon completion or shall wait for user approval before committing
    *   Each task description shall provide the necessary and sufficient context for an agent to execute the task, assuming it operates in a standalone context
*   **`todo.md`**: Technical debt and future improvements
    *   Smaller items not urgent enough for tasks.md
    *   Deferred low-priority bugs
    *   Future enhancements and optimizations
*   **`test-results/`**: Test investigation reports and outputs
*   **`fixtures/`**: Service-specific test data (optional)
*   **`code-review.md`**: Code review findings (created by @code-reviewer)
*   **`tech-review.md`**: Tech lead review (created by @tech-lead)

### 2.4. Agent Handoff Files

The system shall maintain handoff documentation for agent coordination:

#### Service-Level Handoffs (`HANDOFF.md`)

Each service directory shall contain a `HANDOFF.md` file at its root for intra-domain coordination:

*   **Location**: `{service-directory}/HANDOFF.md`
*   **Purpose**: Track handoffs between agents working on the same context domain
*   **Format**: Use template from `/artifacts/shared/HANDOFF-TEMPLATE.md`

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
- Expected cache behavior documented in DS-005

**Artifacts**:
- Tests: `tests/`
- Fixtures: `tests/fixtures/`
- Tasks: `artifacts/tasks.md`

**Commit**: abc1234 - test(data-service): DS-001-008 add failing tests
```

#### Cross-Domain Handoffs

For coordination between services, use `/artifacts/shared/handoffs/`:

*   **Integration Status**: `/artifacts/shared/handoffs/integration-status.md`
  - Master coordination file showing readiness of all domains
  - Updated when services reach integration-ready state

*   **Service API Status**: `/artifacts/shared/handoffs/{service}-api.md`
  - Documents API endpoint stability for consumers
  - Created when endpoints are stable and ready for integration
  - Template: `/artifacts/shared/handoffs/TEMPLATE-service-api.md`

Required elements for API handoffs:
*   **Endpoint Status**: ✅ Stable | 🚧 In Development | ⚠️ Breaking Change | 🔴 Blocked
*   **Since Timestamp**: When endpoint became stable
*   **OpenAPI Reference**: Lines in openapi.yaml
*   **Example Response**: Path to fixture file in `/artifacts/shared/fixtures/`
*   **Mock Client**: Path to mock implementation in `/artifacts/shared/mocks/`
*   **Consumers**: Which services depend on this endpoint
*   **Dependencies**: Which services this endpoint depends on
*   **Known Issues**: Any bugs or limitations
*   **Breaking Changes**: Upcoming changes with ETAs

### 2.5. Project `README.md`

The system shall maintain a `README.md` file in the root of each project. The `README.md` file shall describe:

-   The project's purpose
-   Instructions for setting up the development environment and running common commands
-   A summary of important architectural or technical decisions
-   A list of other projects or services that this project depends on
-   Location of project artifacts (e.g., "See `artifacts/` for bugs, tasks, and test results")

## 3. Common Context Resources

The system maintains shared standards and rules in `/context/` for use across all projects.

```
/ (monorepo root)
├── context/
│   ├── standards/           # Development standards
│   │   ├── agent-standards.md
│   │   ├── bug-standards.md
│   │   ├── coding-standards.md
│   │   ├── doc-standards.md
│   │   ├── testing-standards.md
│   │   └── workflow-standards.md
│   └── rules/              # Development rules
│       └── EARS-notation-requirements.mdc
└── services/               # Projects reference context/
```

### 3.1. Common Context Resources

*   **`context/standards/`**: Development standards covering coding, testing, building, documentation, and workflow processes
*   **`context/rules/`**: Development guidelines including EARS requirements notation and TDD practices

### 3.2. Context File Quality Standards

All project context files shall be reviewed from the perspective of an expert context engineer to ensure they are:

*   **Necessary**: Each piece of information serves a clear purpose in understanding or developing the project
*   **Sufficient**: Contains all essential information needed for autonomous agent understanding and execution
*   **Human-Friendly**: Easily understandable by humans without requiring specialized knowledge, avoiding unnecessary technical jargon
*   **Non-Verbose**: Concise and focused, avoiding redundancy while not consuming unnecessary tokens in AI context windows
*   **Actionable**: Provides clear, specific guidance that enables effective decision-making and implementation

## 4. System-Wide Artifacts

The monorepo root `/artifacts/` directory contains system-wide artifacts that affect multiple services:

### 4.1. Architecture & Design

*   **`architecture.md`**: System architecture describing all services, their interactions, and data flow
*   **`data-model.md`**: Conceptual data model showing entities and relationships across the system
*   **`api/`**: System-wide API contracts
    *   `openapi.yaml`: Complete API specification for all services
    *   `api-design-guide.md`: API design standards and conventions

### 4.2. Requirements & Stories

*   **`requirements.md`**: System-wide functional and non-functional requirements (EARS notation)
*   **`user-stories.md`**: End-to-end user stories spanning multiple services

### 4.3. Design System

*   **`design/`**: System-wide UI design artifacts
    *   `design-tokens.json`: Design system tokens (colours, typography, spacing)
    *   `components.md`: Reusable component specifications
    *   `wireframes.md`: UI wireframes and layouts
    *   `visuals/`: Generated mockups and diagrams

### 4.4. Shared Resources

*   **`shared/handoffs/`**: Cross-service coordination files
*   **`shared/fixtures/`**: Test data used by multiple services (e.g., `AAPL_1y.json`)
*   **`shared/mocks/`**: Mock implementations for cross-service testing

## 5. Decision Criteria

When creating a new artifact, apply these rules:

**Q1**: Is this artifact only relevant to one service/package?
- ✅ YES → Put in `{service}/artifacts/`
- ❌ NO → Continue to Q2

**Q2**: Does this artifact describe system-wide architecture/contracts?
- ✅ YES → Put in root `/artifacts/`
- ❌ NO → Continue to Q3

**Q3**: Is this artifact for coordination between services?
- ✅ YES → Put in `/artifacts/shared/`
- ❌ NO → Re-evaluate Q1-Q3

**Q4**: Is this a standard/rule for developers to follow?
- ✅ YES → Put in `/context/standards/` or `/context/rules/`
- ❌ NO → It's an output, use artifacts per Q1-Q3