---
purpose: Code patterns, naming conventions, and implementation standards
audience: All developers and coding agents
read-when: Writing code, reviewing PRs, understanding patterns
not-for: Tool choices (see tech-standards.md), testing methodology (see testing-standards.md)
related: [tech-standards, testing-standards, security-standards]
---

# Coding Standards

**Languages**: Python (backend), TypeScript (frontend)

## File Organisation

```
services/{service-name}/
├── main.py              # FastAPI app entry point
├── config.py            # Configuration classes
├── models.py            # Pydantic/SQLAlchemy models
├── routes/              # API route handlers
├── services/            # Business logic
├── schemas/             # Pydantic schemas
└── tests/               # Test directory

frontend/
├── app/                 # Application routes
├── components/          # Reusable components
├── hooks/              # Custom React hooks
├── lib/                # Utilities, API clients
├── types/              # TypeScript definitions
└── tests/              # Test directory
```

## Naming Conventions

```typescript
// Files: kebab-case (login-form.tsx)
// Components: PascalCase (LoginForm)
// Hooks: camelCase with 'use' (useAuth)
// Event handlers: handleXxx (handleSubmit)
```

## Virtual Environment

A virtual environment shall be initialised at the project root.

## Component Structure

```typescript
export const ComponentName: FunctionalComponent<Props> = ({ prop }) => {
  // Hooks first (useEffect, useState before conditionals)
  const [state, setState] = useState(initialState);

  // Event handlers as separate functions
  const handleAction = async (event: Event) => {
    try {
      await asyncOperation(prop);
    } catch (error) {
      console.error('Failed:', error);
    }
  };

  // JSX with early returns for conditionals
  if (loading) return <div>Loading...</div>;

  return (
    <form onSubmit={handleAction}>
      {/* Element */}
    </form>
  );
};
```

## Import Organisation

```typescript
// 1. React imports
import { useState } from 'react';

// 2. Third-party libraries
import { useQuery } from '@tanstack/react-query';

// 3. Internal imports (absolute paths)
import { apiClient } from '@/lib/api-client';

// 4. Type imports
import type { User } from '@/types/user';
```

## Python/FastAPI Patterns

```python
# Service classes with dependency injection
class HealthDataService:
    def __init__(self, vital_client):
        self.vital_client = vital_client

    async def get_data(self, user_id: str) -> Optional[Dict]:
        try:
            response = await self.vital_client.get(f"/users/{user_id}/data")
            return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch data: {e}")
            raise HTTPException(500, "DATA_RETRIEVAL_FAILED")

# FastAPI routes with service injection
@router.get("/{user_id}")
async def get_user_data(
    user_id: str,
    service: HealthService = Depends()
) -> ResponseModel:
    data = await service.get_data(user_id)
    if not data:
        raise HTTPException(404, "Data not found")
    return ResponseModel(**data)
```

## Error Handling & Safe Failure

**Principle**: Errors must fail closed, loudly, and recoverably — without leaking secrets, stack traces, or internal structure.

| Principle | What This Means |
|-----------|----------------|
| **Log richly, return boring** | Log full context for developers (stack trace, user ID, request ID), but return vague user-facing messages |
| **Catch at boundaries** | One error translator at API edge, not scattered try/catch everywhere |
| **Fail closed** | If auth fails, validation fails, or anything unexpected happens — deny access, don't fall through |
| **Make failure observable** | Every error gets logged with correlation ID for diagnosis |

**Error responses should include**: error code (machine-readable), user message (sanitised), correlation ID, timestamp.

**Never return**: Stack traces, database errors, internal paths, schema details.

See [security-standards.md §Safe Failure](security-standards.md#safe-failure) for security-specific concerns.

## Security

See standards for security implementation:
- [tech-standards.md §Authentication Architecture](tech-standards.md#authentication-architecture) - Firebase Auth, workload identity, token flows
- [security-standards.md](security-standards.md) - Input validation, API security, data protection, safe failure principles

## Lean Code (Token-Efficient by Design)

Lean code and token-efficient code are the same thing: eliminate waste so both humans and LLMs can read, understand, and modify code with minimum effort.

**Every line must earn its place:**
- No dead code, commented-out blocks, or unused imports
- No speculative features (YAGNI); build for current requirements only
- No premature abstraction; three similar lines beat a premature helper
- No wrapper functions that just forward arguments

**Keep modules small and focused:**
- One responsibility per module; if you can't name it clearly, split it
- Prefer flat structure over deep nesting
- Small files are cheaper to read (for humans and LLMs)

**Prefer established packages** (see Library-first in [tech-standards.md](tech-standards.md)):
- Use well-maintained libraries over custom implementations
- Fewer lines to maintain, test, and read

**Minimise indirection:**
- Reduce layers between intent and execution
- Avoid patterns that exist only to satisfy a pattern (factories for one type, interfaces for one implementation)
- Inline short functions used once

**Apply to documentation too** (see Token-Efficient in [doc-standards.md](doc-standards.md)):
- Comments explain *why*, never *what*
- Self-documenting code over verbose comments
- Docstrings on public APIs only; skip obvious ones

## Performance Patterns

```typescript
// Lazy loading
const Component = lazy(() => import('./Component'));

// Memoisation for expensive operations
const processedData = useMemo(() => heavyComputation(data), [data]);

// Concurrent backend operations
user_data, health_data = await asyncio.gather(
    db.get_user(user_id),
    db.get_health_data(user_id)
)
```

## Logging Standards

**Format**: Use structured logging (JSON) with consistent fields: event type, timestamp, correlation ID, context (user_id, request_id, etc.).

**What to log**: See [security-standards.md §Logging & Monitoring as Security](security-standards.md#logging--monitoring-as-security) for security events (auth attempts, permission denials, validation failures) and what never to log (passwords, tokens, PII).

**Tools**: See [tech-standards.md §Monitoring & Observability](tech-standards.md#monitoring--observability) for platform choices.

## Code Quality Requirements

```json
// tsconfig.json (TypeScript strict mode)
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true
  }
}

// Python mandatory type hints
def process_data(user_id: str, data: Dict[str, Any]) -> Optional[Result]:
    # Full type annotations required
    pass
```

**Linting and formatting**: Python uses **Ruff** (format + lint) and **Pyright** (type checking); see [tech-standards.md §Static Analysis](tech-standards.md#static-analysis--code-quality). Auto-fix all issues before commits.

## Commit Protocol

**Every task completion requires a commit.** This ensures fine-grained history, easy reverts, and clear audit trails.

### Commit Message Format

```
{type}({scope}): {TASK-ID} {description}

{optional body}

Tasks: {task-ids}
Agent-Session: tool={tool} model={model} agents={agent-ids} tokens={in}K/{out}K duration={time}

Co-Authored-By: {tool-or-model} <email>
```

**Note**:
- **Triplet**: Record the actual tool (e.g. cursor, claude-ide), model (e.g. sonnet, gpt-4), and agent(s) from context/agents (e.g. python-coder, functional-tester). Do not substitute a default.
- Agent-Session line tracks metrics for session analysis
- Tasks line references task IDs from tasks.md or artefacts/build/tasks.md

### Commit Types by TDD Phase

| Phase            | Type       | Example                                                                   |
| ---------------- | ---------- | ------------------------------------------------------------------------- |
| TDD RED (tests)  | `test`     | `test(data-service): DS-001 add failing tests for yfinance data fetching` |
| TDD GREEN (impl) | `feat`     | `feat(vis-service): VS-102 implement Bollinger Band calculator`           |
| Review           | `docs`     | `docs(frontend): FE-301 add tech lead review - APPROVED`                  |
| Bug fix          | `fix`      | `fix(llm-service): LLM-105 handle OpenRouter timeout`                     |
| Refactor         | `refactor` | `refactor(shared-types): ST-107 simplify model exports`                   |

### Scopes

Use the service/package name as scope (e.g. `shared-types`, `data-service`, `vis-service`, `llm-service`, `frontend`).

For commit types, workflow, and full examples, see [conventional-commits.mdc](../rules/conventional-commits.mdc).


## Framework-Specific Best Practices

### React/TypeScript

**Philosophy:** Functional/declarative, SOLID, Type safety, Component-driven

**Naming Conventions:**

| Case | Use For |
|------|---------|
| PascalCase | Components, Types, Interfaces |
| kebab-case | Directories, files |
| camelCase | Variables, functions, hooks, props |
| UPPERCASE | Env vars, constants |

**Prefixes:** handle* (events), is/has/can (booleans), use* (hooks)

**React Patterns:**
- Functional components with TypeScript interfaces
- useCallback for memoised callbacks
- useMemo for expensive computations
- React.memo() strategically
- Proper cleanup in useEffect

**State Management:**

| Scope | Use |
|-------|-----|
| Component | useState, useReducer |
| Shared (local) | useContext |
| Global (client) | Zustand |
| Server | TanStack Query |

**Styling:** Tailwind CSS, Mobile-first, Dark mode via CSS vars, WCAG contrast

**UI Components (DaisyUI):**

**Styling priority:** (1) DaisyUI semantic classes first, (2) Tailwind utilities second, (3) custom CSS only as a last resort when neither provides what's needed. Do not create component-specific `.css` files without exhausting DaisyUI and Tailwind options first.
Enforced by [ui-component-reuse.mdc](../rules/ui-component-reuse.mdc).

| Do | Don't |
|----|-------|
| Use semantic classes (`btn`, `card`, `modal`) | Build custom components that duplicate DaisyUI functionality |
| Customise via DaisyUI theming and CSS custom properties | Override with `!important` or specificity hacks |
| Use semantic classes for components, utilities for layout | Mix semantic and utility classes inconsistently on the same element |
| Extend through DaisyUI configuration and variants | Create wrapper components that break theme consistency |
| Document which components nest inside which | Use ad-hoc nesting without established patterns |
| Follow DaisyUI breakpoint conventions consistently | Create ad-hoc responsive workarounds per component |

**Quality:**
- Zod for validation (see [security-standards.md §Input Validation](security-standards.md#input-validation) for principles)
- Vitest + React Testing Library
- Error boundaries with Sentry
- Semantic HTML, ARIA, keyboard nav

For mobile coding patterns (SwiftUI/iOS, React Native for Web), see [tech-mobile-standards.md](tech-mobile-standards.md).

## API Design Standards

### RESTful Principles

**Resource-based URLs:**
- ✅ `/portfolios/{id}` - Resource noun, ID in path
- ❌ `/getPortfolio` - Action verb in URL

**HTTP verbs:**
- `GET` - Read resource (idempotent, cacheable)
- `POST` - Create resource (not idempotent)
- `PUT` - Replace entire resource (idempotent)
- `PATCH` - Update partial resource (not idempotent)
- `DELETE` - Remove resource (idempotent)

**Status codes:**
- `200 OK` - Successful GET/PATCH/PUT
- `201 Created` - Successful POST with new resource
- `204 No Content` - Successful DELETE or PUT with no body
- `400 Bad Request` - Client error (invalid input)
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Authenticated but not authorized
- `404 Not Found` - Resource doesn't exist
- `409 Conflict` - Resource conflict (duplicate, version mismatch)
- `422 Unprocessable Entity` - Validation failed
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - Temporary unavailability

### Pagination

**Query parameters:**
```
GET /portfolios?page=2&limit=20          # Offset-based
GET /portfolios?cursor=xyz123&limit=20   # Cursor-based (preferred for large datasets)
```

**Response envelope:**
```json
{
  "data": [...],
  "pagination": {
    "page": 2,
    "limit": 20,
    "total": 150,
    "hasNext": true,
    "nextCursor": "xyz123"
  }
}
```

### Versioning

**URL versioning (preferred):**
```
GET /v1/portfolios/{id}
```

**Header versioning (alternative):**
```
Accept: application/vnd.api+json; version=1
```

**Deprecation:** Maintain previous version for 6 months after new version release.

### Request/Response Format

**Request bodies (POST/PUT/PATCH):**
```json
{
  "name": "Tech Portfolio",
  "description": "Technology stocks",
  "holdings": [...]
}
```

**Success responses:**
```json
{
  "data": { "id": "123", "name": "Tech Portfolio", ... },
  "meta": { "timestamp": "2026-02-06T14:00:00Z" }
}
```

**Error responses (see [coding-standards.md §Error Handling](coding-standards.md#error-handling--safe-failure)):**
```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Invalid portfolio name",
    "correlationId": "abc-123",
    "timestamp": "2026-02-06T14:00:00Z"
  }
}
```
