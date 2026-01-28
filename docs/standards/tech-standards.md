# withineve Technical Context

## System Overview

**withineve** is a monorepo containing multiple applications and services for health and wellness data connectivity. The system integrates with various health/fitness APIs (Vital API, etc.) to provide a unified data platform.

### Architecture
- **Monorepo Structure**: Single repository with multiple packages using workspaces
- **Workspace Management**: Root `package.json` workspaces array must be explicitly maintained
  - **Compliance**: All Node.js workspaces listed explicitly (no wildcards: `backend/*`)
  - **When to Update**: Add/remove projects when creating new Node.js packages or deprecating existing ones
  - **Why Explicit**: Prevents accidental inclusion of incomplete/broken projects and Python projects
- **Deployment Strategy**:
  - Backend: Cloud Run Functions Gen 2 direct source deployment
  - Frontend: Firebase Hosting
  - Mobile: Native iOS (Swift), Android (Kotlin - future)
- **Networking**: Frontend accepts public traffic; Backend is internal-only (Google Cloud VPC)
- **Data Flow**: APIs → Backend → Frontend/Mobile → Users

## Technology Stack

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
# Clone repository
git clone https://github.com/within-eve/withineve-prototype-2.git
cd withineve-prototype-2

# Install dependencies
yarn install
cd backend/data-api && uv sync
# iOS dependencies: pod install (from mobile/withineve-ios/)

# Environment variables (see .env.example files)
# Google Cloud service account key file required for local development
```

### Secret Management
- **Local Development**: `.env` files with development secrets
- **Production**: Environment variables injected by Cloud Run/Firebase

## Repository Structure

```
withineve-prototype-2/
├── backend/                    # Backend services
│   ├── chat-api/               # Chat API (Python, FastAPI)
│   ├── data-api/               # Data Accessor API (Python, FastAPI)
│   ├── llm-orchestrator/       # LLM orchestration service (TypeScript)
│   ├── medgemma-llm/           # MedGemma LLM service (Python)
│   ├── pii-scrubber/           # PII detection and redaction (Python, FastAPI)
│   ├── prompts-api/            # Prompts management API (Python, FastAPI)
│   └── secrets-manager/        # SDK to access GCP secrets (Python/TypeScript)
├── docs/                       # Documentation
│   ├── common/                 # Shared standards, blueprints, and schemas
│   ├── llm-pipeline/           # LLM pipeline documentation
│   ├── monorepo-migration/     # Documents related to the monorepo setup
│   └── Vital API Reference/    # Documentation for the Vital API
├── frontend/                   # Web applications
│   ├── admin-frontend/         # Admin dashboard (Next.js)
│   ├── chat-prototype/         # Chat prototype (Vite + React)
│   └── user-frontend/          # User interface (Next.js)
├── mobile/                     # Mobile applications
│   ├── withineve_connect_flutter/ # Flutter application DEPRECATED
│   ├── withineve-connect/      # React Native application DEPRECATED
│   ├── withineve-connect-expo/ # React Native (Expo) application DEPRECATED
│   └── withineve-connect-swift/ # iOS Swift application
├── packages/                   # Shared packages
│   ├── auth/                   # Authentication package
│   ├── design-system/          # Design system components
│   ├── prompt-library/         # Prompt management library
│   ├── shared-types/           # Shared TypeScript types
│   └── ui/                     # UI component library
└── workflows/                  # CI/CD and other workflows
    ├── data-pipeline/          # Data processing (BigQuery)
    ├── gcp-build/              # GCP build workflows (GitHub Actions)
    └── github-build/           # GitHub build workflows DEPRECATED
```


## Development Workflows

See `docs/standards/workflow-standards.md` for complete development processes, quality gates, and deployment pipelines.

## Coding Standards

See `docs/standards/coding-standards.md` for complete coding patterns, naming conventions, and implementation standards.

## Testing Standards

See `docs/standards/testing-standards.md` for comprehensive testing guidelines, TDD practices, and testing tools/frameworks.

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
- `docs/standards/` - All development standards (coding, testing, workflows)
- `docs/` - Project documentation and guides
- Service-specific READMEs for setup instructions

### Development Support
- **Cloud SDK**: `gcloud --version`
- **Node**: `node --version; yarn --version`
- **Xcode**: `xcodebuild -version`

## Deployment & Build Pipeline

See [Build & Deployment Standards](../../standards/build-standards.md) for complete build configuration, templates, and deployment patterns.

This context should enable autonomous development across the entire withineve platform. Reference this document when making architectural decisions or introducing new patterns.
