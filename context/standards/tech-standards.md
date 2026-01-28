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
testing: Vitest (frontend), Pytest (backend), XCTest (iOS)
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
```

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

See `context/standards/workflow-standards.md` for complete development processes, quality gates, and deployment pipelines.

## Coding Standards

See `context/standards/coding-standards.md` for complete coding patterns, naming conventions, and implementation standards.

## Testing Standards

See `context/standards/testing-standards.md` for comprehensive testing guidelines, TDD practices, and testing tools/frameworks.

## Performance Considerations

### Frontend Optimization

- **Static generation** where possible (`output: 'export'`)
- **Lazy loading** for route components
- **Image optimization** via Next.js Image component
- **Bundle analysis** with `@next/bundle-analyzer`

### Backend Optimization

- **Async/await** for I/O operations
- **Connection pooling** for databases
- **Caching layers** (Redis/Memory) for expensive operations
- **Background tasks** for heavy processing

### Mobile Optimization

- **Platform-specific builds** (single architecture)
- **Asset optimization** (compressed images, WebP)
- **Offline-first** design where applicable

## Monitoring & Observability

TODO

### Metrics Collection

- **Frontend**: Google Analytics 4, custom events
- **Backend**: Cloud Logging, custom metrics
- **Mobile**: Firebase Analytics, crash reporting
- **Infrastructure**: Cloud Monitoring dashboards

## Key Decision Records

### Tech Stack Choices

- **Firebase**: Managed authentication, hosting, and real-time features
- **Google Cloud**: Unified ecosystem with Firebase, strong Python support
- **Swift**: Native iOS development with excellent performance and ecosystem
- **Environment Variables**: Consistent secret management across platforms

### Architecture Principles

- **Serverless-first**: Prefer managed services over self-hosted
- **Mobile-first**: Desktop/web features are progressive enhancements
- **Offline-capable**: Core functionality works without network
- **Privacy-by-design**: Minimize data collection and retention

## Getting Help

### Documentation Sources

- `context/standards/` - All development standards (coding, testing, workflows)
- `context/` - Shared context (agents, rules, standards, MCP)
- `artifacts/` - Project-specific work output (specs, tasks, bugs, guides)
- Service-specific READMEs for setup instructions

### Development Support

- **Cloud SDK**: `gcloud --version`
- **Node**: `node --version; yarn --version`
- **Xcode**: `xcodebuild -version`

## Deployment & Build Pipeline

See `context/standards/build-standards.md` for complete build configuration, templates, and deployment patterns.

Reference this document when making architectural decisions or introducing new patterns. These are preferred patterns; document deviations and rationale when choosing alternatives.