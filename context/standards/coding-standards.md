# Coding Standards

**Languages**: Python (backend), TypeScript (frontend)

## File Organization

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

## Import Organization

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

## Security Patterns

```typescript
// Input validation with Zod
const Schema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100)
});

export async function POST(request: Request) {
  const body = await request.json();
  const validated = Schema.parse(body);
  return NextResponse.json({ success: true });
}
```

## Performance Patterns

```typescript
// Lazy loading
const Component = lazy(() => import('./Component'));

// Memoization for expensive operations
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

Co-Authored-By: Claude {MODEL_NAME} ({MODEL_ID}) <noreply@anthropic.com>
```

**Note**: Agents must use their actual model name and ID (e.g., "Sonnet 4.5 (claude-sonnet-4-5-20250929)").

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

Co-Authored-By: Claude Sonnet 4.5 (claude-sonnet-4-5-20250929) <noreply@anthropic.com>

# TDD GREEN - implementation
feat(data-service): DS-101 create project structure and dependencies

Co-Authored-By: Claude Sonnet 4.5 (claude-sonnet-4-5-20250929) <noreply@anthropic.com>

# Review approval
docs(data-service): DS-301 add tech lead review - APPROVED

Co-Authored-By: Claude Opus 4.5 (claude-opus-4-5-20251101) <noreply@anthropic.com>

# General commits (non-task)
feat: add user authentication
fix: resolve token refresh bug
docs: update API documentation
refactor: simplify data service logic
```

