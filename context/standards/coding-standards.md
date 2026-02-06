# Coding Standards

**Languages**: Python (backend), TypeScript (frontend)

## File Organisation

```
backend/{service-name}/
├── main.py              # FastAPI app entry point
├── config.py            # Configuration classes
├── models.py            # Pydantic/SQLAlchemy models
├── routes/              # API route handlers
├── services/            # Business logic
├── schemas/             # Pydantic schemas
└── tests/               # Test directory

frontend/
├── app/                 # Next.js app router
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

## Error Handling

```typescript
// Frontend: Custom error types
class ServiceError extends Error {
  constructor(public code: string, message: string) {
    super(message);
    this.name = 'ServiceError';
  }
}

// Backend: Structured error responses
class APIError(HTTPException):
    def __init__(self, status_code: int, error_code: str, message: str):
        super().__init__(status_code, {
            "error": error_code,
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        })
```

## Security

See [security-standards.md](security-standards.md) for input validation, authentication, API security, data protection, and safe failure patterns.

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

**Prefer established packages** (see Library-first in tech-standards.md):
- Use well-maintained libraries over custom implementations
- Fewer lines to maintain, test, and read

**Minimise indirection:**
- Reduce layers between intent and execution
- Avoid patterns that exist only to satisfy a pattern (factories for one type, interfaces for one implementation)
- Inline short functions used once

**Apply to documentation too** (see Token-Efficient in doc-standards.md):
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

```python
# Structured logging
logger = logging.getLogger(__name__)

def log_api_call(method: str, endpoint: str, user_id: str, duration_ms: int):
    logger.info(json.dumps({
        "event": "api_call",
        "method": method,
        "endpoint": endpoint,
        "user_id": user_id,
        "duration_ms": duration_ms,
        "timestamp": datetime.utcnow().isoformat()
    }))
```

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

**Linting**: Biome (TS), black + isort (Python) - auto-fix all issues before commits

## Commit Protocol

**Every task completion requires a commit.** This ensures fine-grained history, easy reverts, and clear audit trails.

### Commit Message Format

```
{type}({scope}): {TASK-ID} {description}

{optional body}

Tasks: {task-ids}
Agent-Session: model={model} agents={list} tokens={in}K/{out}K duration={time}

Co-Authored-By: Claude {MODEL_NAME} ({MODEL_ID}) <noreply@anthropic.com>
```

**Note**:
- Agents must use their actual model name and ID (e.g., "Sonnet 4.5 (claude-sonnet-4-5-20250929)")
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

Use the service/package name as scope:

- `shared-types` - Shared type definitions
- `data-service` - Data fetching service
- `vis-service` - Visualisation service
- `llm-service` - LLM service
- `frontend` - React frontend

### Workflow

1. Complete task
2. Run tests (verify expected state: failing for RED, passing for GREEN)
3. Stage relevant files
4. Commit with task ID in message
5. Mark task as complete `[x]`

### Examples

```bash
# TDD RED - failing tests
test(data-service): DS-001 add failing tests for yfinance data fetching

Tasks: DS-001
Agent-Session: model=sonnet agents=functional-tester tokens=8.2K/5.1K duration=32m

Co-Authored-By: Claude Sonnet 4.5 (claude-sonnet-4-5-20250929) <noreply@anthropic.com>

# TDD GREEN - implementation
feat(data-service): DS-101 create project structure and dependencies

Tasks: DS-101
Agent-Session: model=sonnet agents=python-coder tokens=12.4K/8.2K duration=45m

Co-Authored-By: Claude Sonnet 4.5 (claude-sonnet-4-5-20250929) <noreply@anthropic.com>

# Review approval
docs(data-service): DS-301 add tech lead review - APPROVED

Tasks: DS-301
Agent-Session: model=opus agents=tech-lead tokens=15.6K/6.3K duration=28m

Co-Authored-By: Claude Opus 4.5 (claude-opus-4-5-20251101) <noreply@anthropic.com>

# Human commits (no Agent-Session or Co-Authored-By)
feat: add user authentication
fix: resolve token refresh bug
docs: update API documentation
refactor: simplify data service logic
```


## Framework-Specific Best Practices

### React/Next.js/TypeScript

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

**Next.js:**
- App Router, Server Components by default
- 'use client' only for: events, browser APIs, state, client libs
- Image/Link/Script components for optimisation

**State Management:**

| Scope | Use |
|-------|-----|
| Local | useState, useReducer |
| Shared | useContext |
| Global | Redux Toolkit (createSlice) |

**Styling:** Tailwind CSS, Mobile-first, Dark mode via CSS vars, WCAG contrast

**Quality:**
- Zod for validation
- Jest + React Testing Library
- Error boundaries with Sentry
- Semantic HTML, ARIA, keyboard nav

### SwiftUI/iOS

**Architecture:** MVVM with SwiftUI, Prefer structs over classes

**Structure:** Features/, Core/, UI/, Resources/

**Naming:** camelCase vars/funcs, PascalCase types, Boolean: is/has/should prefix

**Patterns:**

| Area | Use |
|------|-----|
| Concurrency | async/await |
| State | @Published, @StateObject |
| Errors | Result type |
| UI | SwiftUI first, UIKit when needed |
| Icons | SF Symbols |

**Quality:**
- Profile with Instruments
- XCTest + XCUITest
- Support dark mode, dynamic type
- Keychain for secrets, certificate pinning

### React Native for Web

**Goal:** Write Once, Run on Multiple Platforms

**Principles:**

1. **Organise Repository for Shared Code**
   - Shared components in `packages/shared-ui/`
   - Platform-specific overrides in `mobile/` and `web/`

2. **Reuse Components Across Platforms**
   - Use React Native primitives (View, Text, etc.)
   - Platform-specific files: `.ios.tsx`, `.android.tsx`, `.web.tsx`

3. **Consolidate State Management**
   - Shared Redux store
   - Platform-agnostic business logic

4. **Optimize Build and Deployment**
   - Separate build pipelines
   - Shared TypeScript config base

5. **Focus on Developer Experience**
   - Fast refresh for all platforms
   - Shared dev tools and debugging
