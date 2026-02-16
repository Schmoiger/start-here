---
purpose: Tool and platform choices for all projects
audience: All agents and developers
read-when: Making tech choices, setting up projects, installing tools
not-for: Testing methodology (see testing-standards.md), code patterns (see coding-standards.md), security principles (see security-standards.md)
related: [testing-standards, coding-standards, security-standards, build-standards, 12-factor-principles, tech-mobile-standards]
---

# Technology Standards

## Overview

This document describes preferred technology patterns and architectural decisions. Projects should follow these patterns unless there is a compelling reason to deviate.

For testing methodology and TDD process, see [testing-standards.md](testing-standards.md). For code patterns and naming, see [coding-standards.md](coding-standards.md). For SaaS design principles, see [12-factor-principles.md](12-factor-principles.md).

## Version Policy

Use the latest stable version of chosen tools. Do not pin to specific versions in standards.

Each project maintains a compatibility matrix in its README documenting known version clashes (e.g. gcloud CLI requiring a specific Python version). Resolve clashes per-project, not in standards.

## Architecture Preferences

### Monorepo Structure

**Preference**: Monorepo with multiple packages using workspaces.

- **Workspace Management**: Root `package.json` workspaces array must be explicitly maintained
  - **Compliance**: All Node.js workspaces listed explicitly (no wildcards: `services/*`)
  - **When to Update**: Add/remove projects when creating new Node.js packages or deprecating existing ones
  - **Why Explicit**: Prevents accidental inclusion of incomplete/broken projects and Python projects

### Deployment Strategy

- **Backend**: Cloud Run Functions Gen 2 direct source deployment (preferred)
- **Frontend**: Firebase Hosting (preferred)
- **Mobile**: See [tech-mobile-standards.md](tech-mobile-standards.md)

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
databases: Cloud SQL (PostgreSQL) with pgvector, BigQuery
secrets: Google Cloud Secret Manager (delivered as env vars)
migrations: Alembic (pre-deployment)
```

### Database & Time-Series Strategy

We use **native Postgres** features to remain portable between Supabase and GCP Cloud SQL.

**Time-Series (Native Partitioning)**

- **Standard:** Do not use TimescaleDB (removed from Supabase PG17).
- **Implementation:** Use native PostgreSQL declarative partitioning (`PARTITION BY RANGE`). Target `pg_partman` for automated maintenance once available on Supabase (promised Oct 2025, still pending as of Feb 2026).
- **Maintenance:** Use `pg_cron` to automate partition creation and data retention (when available). Manual maintenance until then.
- **Supabase default**: PG17. Note: `pg_partman` and `pg_cron` are not yet installable on Supabase PG17.

**Vector Search**

- **Standard:** Use `pgvector` for all embeddings.
- **Index:** Standardise on **HNSW** for production vector search.
- **Constraint:** All embeddings must be generated server-side (FastAPI) to prevent data drift.

### Database Lifecycle

| Tier | Storage | Purpose |
|------|---------|---------|
| Development | Supabase (local/hosted) | Local dev, prototyping, free tier |
| Deployed — Hot | Cloud SQL PostgreSQL | Active queries, API serving, dashboards |
| Deployed — ML | BigQuery | ML training, analytics, large-scale queries |
| Deployed — Archive | Cloud Storage (Parquet/CSV) | Compliance, long-term retention, lowest cost |

**Data ageing**: Hot (0–90 days, partitioned Postgres) → warm (3–12 months, detached partitions) → cold (>1 year, BigQuery or Cloud Storage).

### Database Migrations

**Phase-based approach:**

| Phase | Strategy | Tool |
|-------|----------|------|
| Prototype | Manual SQL or rebuild schema | None (iterate quickly) |
| Development | Start tracking migrations | Alembic setup |
| Pre-deployment | Production-ready migrations | Alembic (required) |

**Tool: Alembic** (SQLAlchemy-based migrations for Python + PostgreSQL)

**Setup:**
```bash
cd services/{service-name}
uv add alembic
alembic init alembic
```

**Naming convention:**
```
YYYYMMDD_HHMM_description.py
Example: 20260206_1430_add_portfolio_table.py
```

**Migration workflow:**
1. **Generate**: `alembic revision --autogenerate -m "add portfolio table"`
2. **Review**: Check generated SQL for safety (destructive operations, data loss)
3. **Test locally**: Run `alembic upgrade head` then `alembic downgrade -1`
4. **Deploy**: Apply in staging before production
5. **Rollback plan**: Always test downgrade path before deploying

**Critical rules:**
- Never edit applied migrations (create new migration instead)
- Always test rollback (`downgrade`) before deploying forward (`upgrade`)
- Use transactions where possible (PostgreSQL supports DDL transactions)
- Avoid data migrations in schema migrations (separate data scripts)
- **Partitioned tables:** When using native partitioning or pg_partman, ensure Alembic ignores child partitions in `autogenerate` (e.g. via `include_object` or env.py filters) so autogenerate does not emit redundant table-creation DDL for partition children.

### Frontend Applications

```yaml
platforms: Firebase Hosting
languages: TypeScript / React (Vite)
frameworks: Vite, React, TailwindCSS
state: TanStack Query (server state), Zustand (client/UI state), React built-in hooks (component state)
ui: DaisyUI + custom components, TailwindCSS
icons: Heroicons (preferred; matches Tailwind ecosystem)
deployment: Firebase hosting with rewrite rules
```

**Styling principle:** Prefer DaisyUI semantic classes and Tailwind utility classes; avoid custom CSS. Use DaisyUI theming and CSS custom properties for colours and spacing. Custom CSS is only acceptable when no DaisyUI or Tailwind pattern exists (e.g. one-off layout or animation). Do not maintain large custom stylesheets or component-specific CSS files.

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

### Monorepo Tools

```yaml
package_manager: Yarn Berry 4.x (workspaces)
build_tools:
  - TypeScript: tsx, tsc
  - Python: uv
documentation: Mermaid
linting: Biome (TypeScript), Ruff (Python)
testing:
  unit: Vitest (frontend), Pytest (backend)
  integration_api: FastAPI TestClient (backend), Vitest + fetch (frontend)
  integration_component: Testing Library (React/DOM interactions)
  ui_e2e: Puppeteer (browser automation)
```

**Mobile**: See [tech-mobile-standards.md](tech-mobile-standards.md) for mobile build tools and testing.

### Testing Tools

**Unit Testing:**
- **Vitest** (Frontend TypeScript)
- **Pytest** (Backend Python)

**API Integration Testing:**
- **FastAPI TestClient** (Backend)
- **Vitest + fetch/axios** (Frontend)

**Component Integration Testing:**
- **Testing Library** (@testing-library/react, @testing-library/user-event): Tests React components with user interactions in simulated browser (jsdom)

**UI E2E Testing:**
- **Puppeteer** (puppeteer-core): Automates Chrome via DevTools Protocol, captures screenshots as evidence. This is the project’s single E2E tool; testing-standards defers to this section for tool choice and focuses on methodology.

**Installation:**
```bash
# Frontend
yarn add -D vitest @testing-library/react @testing-library/user-event puppeteer-core

# Backend
cd services/{service-name}
uv add --dev pytest pytest-cov
```

**HTTP Response Recording (VCR):**
- **pytest-recording** (wraps vcrpy): Records HTTP exchanges to YAML cassette files on first run, replays from file on subsequent runs
- **When to use**: Integration tests that hit external APIs via services (e.g., LLM service → OpenRouter) and suffer from rate limiting or flakiness
- **When NOT to use**: E2E tests (`@pytest.mark.e2e`), error-condition tests (rate limit, invalid request), or data-only tests that don't call external APIs
- **Configuration**: `vcr_config` fixture in `tests/integration/conftest.py` sets cassette directory, record mode, and header filters
- **Recording cassettes**: Run tests with services running: `uv run pytest tests/integration/ -v --record-mode=once`
- **Refreshing cassettes**: Delete files in `tests/integration/cassettes/` and re-record with services running
- **Cassettes are committed to git** as test fixtures alongside test code

```bash
# Record cassettes (requires services running)
uv run pytest tests/integration/ -v --record-mode=once

# Force re-record all cassettes
rm -rf tests/integration/cassettes/*.yaml
uv run pytest tests/integration/ -v --record-mode=once

# Run tests offline using recorded cassettes
uv run pytest tests/integration/ -v
```

For testing methodology, TDD process, and coverage thresholds, see [testing-standards.md](testing-standards.md).

## Static Analysis & Code Quality

### Pre-commit Hooks (Unified)

A **single** root-level `.pre-commit-config.yaml` validates the entire monorepo. Pre-commit (the Python tool) is language-agnostic and runs all hooks from one config.

- **Config**: `.pre-commit-config.yaml` at monorepo root (no per-project configs; no Husky).
- **Hooks**: Python (Ruff on `services/`), TypeScript/JS (Biome on `frontend/`, `packages/`), custom validators (conventional commits, EARS, British English, metrics).
- **Enforcement**: `pre-commit run --all-files` before commits and in CI/CD validates the whole repo in one go.

**Installation** (from monorepo root):

```bash
# Install pre-commit (Python) and the commit-msg hook for conventional commits
uv add --dev pre-commit
uv run pre-commit install
uv run pre-commit install --hook-type commit-msg

# Validate everything
uv run pre-commit run --all-files
```

### Language-Specific Tools

- **TypeScript/JavaScript**: Biome (linting + formatting via pre-commit), Vitest for testing
- **Python**: Ruff (formatting + linting) via pre-commit; Pyright (type checking) run per-service: `cd services/<name> && uv run pyright`

### Quality Gates

- **Type Checking**: Strict mode enabled (TypeScript `strict: true`, Python `--strict`)
- **Test Coverage**: Phase-based thresholds — see [testing-standards.md §Coverage Requirements](testing-standards.md#coverage-requirements)
- **Linting**: Zero tolerance — all auto-fixable issues resolved automatically

## Development Environment Setup

### Prerequisites

- Node.js
- Python
- Google Cloud SDK
- Firebase CLI (for frontend deployment)

### Local Development

```bash
# Install dependencies
yarn install
cd services/{service-name} && uv sync

# Run tests
uv run pytest                    # Python tests
yarn test                        # TypeScript tests
```

**Test Commands:**
- **Python**: `uv run pytest` (not `pytest` alone, not `pip` or `poetry`)
- **TypeScript**: `yarn test` (not `npm test`)
- **Coverage**: `uv run pytest --cov` or `yarn test --coverage`
- **Lint/format (whole repo)**: `uv run pre-commit run --all-files` (single command for Python, Biome, and validators)

### Secret Management & Security

**Rule:** No secrets are stored in plaintext, even in gitignored files.

**Storage vs Delivery:**
- **Storage** (where secrets live at rest): SOPS-encrypted files locally, Google Secret Manager (GSM) in production
- **Delivery** (how apps consume secrets at runtime): Environment variables

These are complementary — secrets are stored encrypted and delivered as env vars at runtime.

**Local Development (SOPS)**

- **Standard:** Encrypt all local secrets using **Mozilla SOPS**.
- **Key:** Use a local `age` key or a shared GCP KMS key.
- **File:** Commit `secrets.enc.json` to Git. This allows safe collaboration (encrypted at rest, decrypt at use).

**Production (GCP)**

- **Rationale:** GSM provides only 6 free secret instances. Consolidating into one JSON blob stays within the free tier.
- **Standard:** Consolidate all keys into a **single JSON blob** stored as one secret in GSM.
- **Access:** Use **Workload Identity Federation** (service-account-less) to fetch secrets at runtime.

See [security-standards.md §Secrets Management](security-standards.md#secrets-management) for security principles and [rules/secrets-management.mdc](../rules/secrets-management.mdc) for loading patterns and rotation.

## Preferred Repository Structure

```
{monorepo-root}/
├── artefacts/                  # System-wide outputs (specs, contracts, shared)
│   ├── product/                # Requirements, user stories
│   ├── architecture/           # System architecture, OpenAPI (openapi.yaml), design decisions
│   ├── design/                 # UI/UX designs, component specs
│   ├── build/                  # Build artefacts, tasks, reviews
│   ├── test-results/           # System-wide test results, dashboard
│   └── shared/                 # Cross-service resources (handoffs, fixtures, mocks)
├── services/                   # Backend services
│   ├── {service-name}/         # Example: API service (Python, FastAPI)
│   │   ├── artefacts/          # Service-specific outputs (tasks, bugs, test-results)
│   │   ├── src/
│   │   └── tests/
│   └── {service-name}/         # Example: Background worker
├── context/                    # Shared context (standards, rules, agents, MCP)
│   ├── agents/                 # Agent definitions
│   ├── mcp/                    # Model Context Protocol configs
│   ├── rules/                  # Development rules
│   ├── standards/              # Development standards
│   └── templates/              # Document templates
├── frontend/                   # Web applications
│   ├── {app-name}/             # Example: Dashboard (Vite + React)
│   │   ├── artefacts/          # App-specific outputs
│   │   └── src/
│   └── {app-name}/             # Example: User interface (Vite + React)
├── packages/                   # Shared packages
│   └── shared-types/           # Cross-language type sharing
│       ├── python/             # Pydantic models (used by services)
│       └── typescript/         # TypeScript types (used by frontend)
└── workflows/                  # CI/CD and other workflows
    ├── {workflow-name}/        # Example: Build workflows
    └── {workflow-name}/        # Example: Data processing pipelines
```

> **Migration note**: The `backend/` directory has been renamed to `services/`. Both paths may appear in older documentation or branches. `services/` is the target state.

## Development Workflows

See [workflow-standards.md](workflow-standards.md) for complete development processes, quality gates, and deployment pipelines.

## Coding Standards

See [coding-standards.md](coding-standards.md) for complete coding patterns, naming conventions, and implementation standards.

## Testing Standards

See [testing-standards.md](testing-standards.md) for comprehensive testing guidelines, TDD practices, and coverage requirements.

## Performance Considerations

### Frontend Optimisation

- **Code splitting** via Vite's automatic chunking and dynamic imports
- **Lazy loading** for route components
- **Image optimisation** via responsive images and lazy loading attributes
- **Bundle analysis** with `rollup-plugin-visualizer` or `vite-bundle-visualizer`

### Backend Optimisation

- **Async/await** for I/O operations
- **Connection pooling** for databases
- **Caching layers** (Redis/Memory) for expensive operations
- **Background tasks** for heavy processing

## Monitoring & Observability

**Stack**: GCP Cloud Logging and Cloud Monitoring for backend, Google Analytics 4 for frontend. For mobile monitoring, see [tech-mobile-standards.md](tech-mobile-standards.md).

**Logging format**: Structured JSON logs with correlation IDs. See [coding-standards.md §Logging Standards](coding-standards.md#logging-standards) for format and [security-standards.md §Logging & Monitoring as Security](security-standards.md#logging--monitoring-as-security) for what to log from security perspective.

### Metrics Collection

- **Frontend**: Google Analytics 4, custom events
- **Backend**: Cloud Logging (structured JSON), Cloud Monitoring (custom metrics)
- **Infrastructure**: Cloud Monitoring dashboards

### Error Tracking

Error tracking groups, deduplicates, and alerts on errors (distinct from raw logging):

- **Frontend**: Sentry (React Error Boundaries + source maps for stack traces)
- **Backend**: GCP Error Reporting (automatic from Cloud Logging structured errors)
- **Alerting**: PagerDuty or Opsgenie for critical errors (configurable thresholds)

**Error vs Logging:**
- **Logging**: Raw event stream (every request, every action)
- **Error Tracking**: Aggregated failures (groups identical errors, tracks frequency, alerts on spikes)

### Feature Flags

**Phase-based approach:**

| Phase | Strategy | Tool |
|-------|----------|------|
| Prototype/Dev | Environment variables | `os.getenv("FEATURE_X")` (Python), `import.meta.env.FEATURE_X` (Vite) |
| Pre-deployment | Remote config with targeting | Firebase Remote Config: `remote_config.get_template()` (server), `getValue(rc, "key")` (client) |

**When to use feature flags:**
- Gradual rollouts (10% → 50% → 100% of users)
- A/B testing, circuit breakers, kill switches, beta features

**Cleanup policy:** Remove flag code after 30 days of 100% rollout. Document flag lifecycle in ticket. Don't let flags rot in codebase.

## Key Decision Records

### Tech Stack Choices

- **Firebase**: Managed authentication, hosting, and real-time features
- **Google Cloud**: Unified ecosystem with Firebase, strong Python support

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
- **Privacy-by-design**: Minimise data collection and retention

## 12-Factor App Principles

See [12-factor-principles.md](12-factor-principles.md).

## Deployment & Build Pipeline

See [build-standards.md](build-standards.md) for complete build configuration, templates, and deployment patterns.

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

Reference this document when making architectural decisions or introducing new patterns. These are preferred patterns; document deviations and rationale when choosing alternatives.
