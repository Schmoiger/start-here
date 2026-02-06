# Technology Standards

## Overview

This document describes preferred technology patterns and architectural decisions. Projects should follow these patterns unless there is a compelling reason to deviate.

## Architecture Preferences

### Monorepo Structure

**Preference**: Monorepo with multiple packages using workspaces.

- **Workspace Management**: Root `package.json` workspaces array must be explicitly maintained
  - **Compliance**: All Node.js workspaces listed explicitly (no wildcards: `backend/*`)
  - **When to Update**: Add/remove projects when creating new Node.js packages or deprecating existing ones
  - **Why Explicit**: Prevents accidental inclusion of incomplete/broken projects and Python projects

### Deployment Strategy

- **Backend**: Cloud Run Functions Gen 2 direct source deployment (preferred)
- **Frontend**: Firebase Hosting (preferred)
- **Mobile**: Native iOS (Swift), Android (Kotlin - future)

### Networking

- **Frontend**: Accepts public traffic
- **Backend**: Internal-only (Google Cloud VPC or equivalent)
- **Data Flow**: APIs → Backend → Frontend/Mobile → Users

## Preferred Technology Stack

### Backend Services

- **Python**: Always run Python in a virtual environment. Use `uv` and a `.python-version` file per project.

```yaml
platform: Cloud Run Functions Gen 2 (Google Cloud)
languages: Python
frameworks: FastAPI
databases: Cloud SQL (PostgreSQL 18) with pgvector (future), BigQuery
secrets: Google Cloud Secret Manager (env vars only)
```

### Frontend Applications

```yaml
platforms: Firebase Hosting
languages: TypeScript / React (Next.js/Vite)
frameworks: Next.js, Vite, React, TailwindCSS
state: Redux Toolkit, React Query
ui: DaisyUI + custom components, TailwindCSS
deployment: Firebase hosting with rewrite rules
```

### Authentication Architecture

**Stack Decision**: Firebase Authentication with Google Sign-In (managed auth provider).

```yaml
provider: Firebase Authentication (upgrade to Identity Platform if needed)
sign_in_methods: Google Sign-In (primary)
frontend_sdk: Firebase Auth SDK
backend_verification: Firebase Admin SDK (ID token verification)
upgrade_trigger: Multi-tenancy, SAML/OIDC federation, or blocking functions
```

#### User Authentication

**Flow**: User signs in via frontend (Firebase Auth SDK + Google Sign-In) → Frontend receives ID token → Frontend attaches token to API requests → Backend verifies token (Firebase Admin SDK) → Backend extracts user claims and checks authorisation.

**Token handling**: ID tokens are short-lived (1 hour default), frontend SDK auto-refreshes, backend verifies signature and expiry on every request.

#### Service-to-Service Authentication

**Pattern**: Use Workload Identity (OIDC tokens from GCP metadata server). Service A requests token with Service B's URL as audience → Attaches token to request → Service B verifies using GCP's public keys.

**Principles**: Platform identity over shared secrets, short-lived tokens, no credentials in code or environment.

See [security-standards.md §Authentication & Authorisation](security-standards.md#authentication--authorisation) for security principles (least privilege, phase-appropriate auth, library-first approach).

### Mobile Applications

```yaml
platforms: iOS (Swift), Android (Kotlin - future)
languages: Swift (current), Kotlin (planned)
deployment: App Store (iOS), Play Store (Android - future)
testing_targets:
  primary_device: iPhone 16
  primary_os: iOS 18.1
  supported_os_range: iOS 17.0+
```

### Monorepo Tools

```yaml
package_manager: Yarn workspaces
build_tools:
  - TypeScript: tsx, tsc
  - Python: uv
  - Swift: Xcode, Swift Package Manager
documentation: Mermaid
linting: Biome (TypeScript), SwiftLint
testing:
  unit: Vitest (frontend), Pytest (backend), XCTest (iOS)
  integration_api: FastAPI TestClient (backend), Vitest + fetch (frontend)
  integration_component: Testing Library (React/DOM interactions)
  ui_e2e: Puppeteer (browser automation)
```

### Testing Tools

**Unit Testing:**
- **Vitest** (Frontend TypeScript): Fast, Vite-native, TypeScript-first
- **Pytest** (Backend Python): Industry standard, fixture-based, plugin ecosystem
- **XCTest** (iOS Swift): Native Apple framework, integrated with Xcode

**API Integration Testing:**
- **FastAPI TestClient** (Backend): Tests Python API endpoints with real backend logic, mocked database
- **Vitest + fetch/axios** (Frontend): Tests API client code, mocked HTTP responses

**Component Integration Testing:**
- **Testing Library** (@testing-library/react, @testing-library/user-event): Tests React components with user interactions in simulated browser (jsdom). Extends testing beyond API surface to include UI behaviour without full browser overhead. Renders components, simulates clicks/typing, verifies DOM updates.

**Rationale**: Lighter than full browser automation for component-level testing. Focuses on user-facing behaviour (what user sees/does) not implementation details (component state/props).

**UI E2E Testing:**
- **Puppeteer** (puppeteer-core): Automates Chrome via DevTools Protocol for full user workflow testing. Real browser, real rendering, captures screenshots as evidence. Chrome-only (matches current Chrome DevTools approach).

**Rationale**: Lightweight (2MB with puppeteer-core using installed Chrome), matches existing Chrome DevTools workflow, sufficient for Chrome-focused web testing. Avoids Playwright's multi-browser overhead (~530MB).

**Installation:**
```bash
# Frontend
yarn add -D vitest @testing-library/react @testing-library/user-event puppeteer-core

# Backend
cd backend/{service-name}
uv add --dev pytest pytest-cov
```

## Static Analysis & Code Quality

### Pre-commit Hooks

- **Configuration Approach**: Project-specific `.pre-commit-config.yaml` files for Python backend services only (not used for frontend TypeScript projects)
- **Scope**: Include code formatting, linting, type checking, and general file validation for Python codebases
- **Enforcement**: `pre-commit run --all-files` before commits and in CI/CD for backend Python services

### Language-Specific Tools

- **TypeScript/JavaScript**: Biome (linting + formatting), Vitest for testing
- **Python**: Black (formatting) + isort (import sorting) + mypy (type checking) or Ruff + pyright
- **Swift**: SwiftLint (linting), SwiftFormat (formatting)

### Quality Gates

- **Type Checking**: Strict mode enabled (TypeScript `strict: true`, Python `--strict`)
- **Test Coverage**: Minimum 90% code coverage (backend Python, frontend TypeScript)
- **Linting**: Zero tolerance - all auto-fixable issues resolved automatically

## Development Environment Setup

### Prerequisites

- Node.js
- Python
- Xcode (for iOS/Swift development)
- Google Cloud SDK
- Firebase CLI (for frontend deployment)

### Local Development

```bash
# Install dependencies
yarn install
cd backend/{service-name} && uv sync
# iOS dependencies: pod install (from mobile/{app-name}/)

# Environment variables (see .env.example files)
# Google Cloud service account key file required for local development

# Run tests
uv run pytest                    # Python tests
yarn test                        # TypeScript tests
```

**Test Commands:**
- **Python**: `uv run pytest` (not `pytest` alone, not `pip` or `poetry`)
- **TypeScript**: `yarn test` (not `npm test`)
- **Coverage**: `uv run pytest --cov` or `yarn test --coverage`

### Secret Management

- **Local Development**: `.env` files with development secrets
- **Production**: Environment variables injected by Cloud Run/Firebase

## Preferred Repository Structure

```
{monorepo-root}/
├── backend/                    # Backend services
│   ├── {service-name}/         # Example: API service (Python, FastAPI)
│   └── {service-name}/         # Example: Background worker (TypeScript)
├── context/                    # Shared context (standards, rules, agents, MCP)
│   ├── agents/                 # Agent definitions
│   ├── mcp/                    # Model Context Protocol configs
│   ├── rules/                  # Development rules
│   └── standards/              # Development standards
├── frontend/                   # Web applications
│   ├── {app-name}/            # Example: Admin dashboard (Next.js)
│   └── {app-name}/             # Example: User interface (Vite + React)
├── mobile/                     # Mobile applications
│   └── {app-name}/             # Example: iOS Swift application
├── packages/                   # Shared packages
│   ├── {package-name}/        # Example: Authentication package
│   ├── {package-name}/        # Example: Design system components
│   └── {package-name}/        # Example: Shared TypeScript types
└── workflows/                  # CI/CD and other workflows
    ├── {workflow-name}/        # Example: Build workflows
    └── {workflow-name}/        # Example: Data processing pipelines
```

## Development Workflows

See [workflow-standards.md](workflow-standards.md) for complete development processes, quality gates, and deployment pipelines.

## Coding Standards

See [coding-standards.md](coding-standards.md) for complete coding patterns, naming conventions, and implementation standards.

## Testing Standards

See [testing-standards.md](testing-standards.md) for comprehensive testing guidelines, TDD practices, and testing tools/frameworks.

## Performance Considerations

### Frontend Optimisation

- **Static generation** where possible (`output: 'export'`)
- **Lazy loading** for route components
- **Image optimisation** via Next.js Image component
- **Bundle analysis** with `@next/bundle-analyzer`

### Backend Optimisation

- **Async/await** for I/O operations
- **Connection pooling** for databases
- **Caching layers** (Redis/Memory) for expensive operations
- **Background tasks** for heavy processing

### Mobile Optimisation

- **Platform-specific builds** (single architecture)
- **Asset optimisation** (compressed images, WebP)
- **Offline-first** design where applicable

## Monitoring & Observability

**Stack**: GCP Cloud Logging and Cloud Monitoring for backend, Firebase Analytics for mobile, Google Analytics 4 for frontend.

**Logging format**: Structured JSON logs with correlation IDs. See [coding-standards.md §Logging Standards](coding-standards.md#logging-standards) for format and [security-standards.md §Logging & Monitoring as Security](security-standards.md#logging--monitoring-as-security) for what to log from security perspective.

### Metrics Collection

- **Frontend**: Google Analytics 4, custom events
- **Backend**: Cloud Logging (structured JSON), Cloud Monitoring (custom metrics)
- **Mobile**: Firebase Analytics, crash reporting
- **Infrastructure**: Cloud Monitoring dashboards

## Key Decision Records

### Tech Stack Choices

- **Firebase**: Managed authentication, hosting, and real-time features
- **Google Cloud**: Unified ecosystem with Firebase, strong Python support
- **Swift**: Native iOS development with excellent performance and ecosystem
- **Environment Variables**: Consistent secret management across platforms

### Architecture Principles

Guided by **LESS Engineering Principles** (see [LESS-Engineering-Principles.md](LESS-Engineering-Principles.md) for full framework):

- **Lean**: MVP first, defer commitment until feedback
- **Ethical**: Trustworthy, inclusive, beneficial
- **Scalable**: Loose coupling, modularity, statelessness
- **Sustainable**: Minimise data transfer and resource usage

Applied as:

- **Serverless-first**: Prefer managed services over self-hosted
- **Library-first**: Prefer established, well-maintained packages over custom implementations
- **Lean and token-efficient**: Eliminate waste in code, documentation, and architecture (see [coding-standards.md](coding-standards.md))
- **Mobile-first**: Desktop/web features are progressive enhancements
- **Offline-capable**: Core functionality works without network
- **Privacy-by-design**: Minimise data collection and retention

## Getting Help

### Documentation Sources

- `context/standards/` - All development standards (coding, testing, workflows)
- `context/` - Shared context (agents, rules, standards, MCP)
- `artefacts/` - Project-specific work output (specs, tasks, bugs, guides)
- Service-specific READMEs for setup instructions

### Development Support

- **Cloud SDK**: `gcloud --version`
- **Node**: `node --version; yarn --version`
- **Xcode**: `xcodebuild -version`

## Deployment & Build Pipeline

See [build-standards.md](build-standards.md) for complete build configuration, templates, and deployment patterns.

Reference this document when making architectural decisions or introducing new patterns. These are preferred patterns; document deviations and rationale when choosing alternatives.
## 12-Factor App Principles

For building software-as-a-service applications with portability and resilience:

1. **Codebase**: Exactly one codebase for a deployed service, used for many deployments
2. **Dependencies**: All dependencies declared, no implicit reliance on system tools
3. **Config**: Configuration that varies between deployments stored in environment
4. **Backing services**: All backing services treated as attached resources
5. **Build, release, run**: Strict delivery pipeline of build → release → run
6. **Processes**: Deploy as stateless processes, persist data in backing services
7. **Port binding**: Self-contained services available via specified ports
8. **Concurrency**: Scale by individual processes
9. **Disposability**: Fast startup and shutdown for robust systems
10. **Dev/Prod parity**: All environments as similar as possible
11. **Logs**: Produce logs as event streams, let execution environment aggregate
12. **Admin Processes**: Admin tasks in source control, packaged with application

## Context7 Integration

Always use Context7 when needing:
- Code generation
- Setup or configuration steps
- Library/API documentation

Automatically use Context7 MCP tools to resolve library ID and get library docs without explicit request.

## Package Installation

Install packages at the project root folder, not at the monorepo root. This ensures proper dependency isolation and allows each project to manage its own dependencies independently.

**Python projects:**
```bash
cd {project-root}
uv add package-name
```

**Node.js projects:**
```bash
cd {project-root}
yarn add package-name
```
