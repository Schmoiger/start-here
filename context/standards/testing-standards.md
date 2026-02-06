# Testing Standards

**TDD-First Development**: Write tests before implementation. No code without passing tests.

**Quality Gate**: All tests must pass before commits, reviews, or deployments.

**Testing Pyramid**:

- **Unit Tests (70%)**: Isolated functions/methods with mocked dependencies
- **Integration Tests (20%)**: Component interactions with real services
- **E2E Tests (10%)**: Complete user workflows with real browsers

## TDD Cycle

**Red**: Write failing test first for each requirement/behaviour.

**Green**: Implement minimal code to pass test.

**Refactor**: Clean up code while maintaining passing tests.

## Test Types

**Unit Tests (pytest/Vitest)**: Isolated functions/methods, mock all dependencies.
- Agent: @functional-tester writes these
- Run via: pytest, vitest
- Mock all external services

**Integration Tests**: Component interactions, use real services where safe.
- Agent: @functional-tester writes these
- Test API endpoints with real backend
- May use TestClient (FastAPI) or supertest (Express)

**E2E Tests (Browser)**: Complete user workflows with real browsers.
- Agent: @ui-tester performs these
- **MUST use actual browser** (Chrome DevTools)
- **MUST capture screenshots** as evidence
- Tests user-facing behaviour, not APIs
- Verify visual elements render correctly

**Distinction:**
- @functional-tester: Writes automated test code (pytest/vitest files)
- @ui-tester: Executes manual browser testing with Chrome DevTools

## Phase Workflow

**Requirements**: Write failing acceptance tests first. Get approval. Commit.

**Implementation**: TDD cycle (Red-Green-Refactor) for each unit. Test after each phase.

**Integration**: Test component interactions. Address issues. Get approval.

**End-to-End**: Deploy to staging. Manual testing. Visual testing for UI. Final approval.

**Commit Discipline**: Never commit broken code. Include test coverage in commit messages.

```bash
feat: implement user authentication
- 15 unit tests (100% passing)
- Integration tests: DB persistence
- E2E: Login/logout flow
```

## Test Organisation

```
tests/
├── unit/test_{service}.py      # Unit tests, mock all dependencies
├── integration/test_{flow}.py  # Component integration
└── e2e/test_{journey}.py       # User journey tests
```

## Data & Mocking

- Use factories for consistent test data
- Mock external services in unit tests
- Real services for integration tests
- Independent test isolation

## Visual Testing

### When to Use Visual Testing

- **UI Components**: Components with visual appearance requirements
- **Marketing Pages**: Landing pages, dashboards, forms
- **Responsive Design**: Breakpoint testing across devices
- **Brand Consistency**: Ensuring UI matches design system

### Implementation

```typescript
// Example visual test with Playwright
test('dashboard layout matches design', async ({ page }) => {
  await page.goto('/dashboard');

  // Take screenshot and compare
  await expect(page).toHaveScreenshot('dashboard-layout.png', {
    fullPage: true,
    threshold: 0.1  // Allow 10% difference for anti-aliasing
  });
});
```

### Visual Testing Workflow

1. **Baseline**: Initial approved screenshots become "golden" images
2. **Regression Detection**: CI catches visual changes from baseline
3. **Manual Review**: Team reviews and approves or rejects changes
4. **Update Baselines**: Approved changes become new baseline

## Testing Tools & Frameworks

### Backend (Python)

- **pytest**: Core testing framework
- **pytest-asyncio**: Async test support
- **pytest-mock**: Mocking utilities
- **pytest-cov**: Code coverage reporting
- **hypothesis**: Property-based testing

### Frontend (TypeScript/React)

- **Vitest**: Fast unit testing for Vite/React projects
- **Testing Library**: Component testing utilities
- **Playwright**: E2E and visual testing
- **MSW**: Mock Service Worker for API mocking

### CI/CD Integration

- **GitHub Actions**: Automated test execution on PRs
- **Quality Gates**: 100% of tests must pass before merge
- **Warnings**: Bugs to be raised for all warnings

## Coverage Requirements

Coverage requirements increase as code progresses toward deployment. Thresholds are enforced **per service** (not aggregate across all services).

### Phase-Based Thresholds

| Phase          | Coverage | Pass Rate | Concessioned | Fail Rate | Enforcement                  |
| -------------- | -------- | --------- | ------------ | --------- | ---------------------------- |
| Prototype      | ≥90%     | ≥90%      | ≤10%         | 0%        | Warning (advisory)           |
| Development    | ≥94%     | ≥94%      | ≤6%          | 0%        | Build fails below threshold  |
| Pre-deployment | ≥97%     | ≥97%      | ≤3%          | 0%        | Merge blocked below threshold |

**Definitions:**
- **Coverage**: Percentage of code lines executed by tests
- **Pass Rate**: Percentage of tests that pass (non-concessioned tests must have 100% pass rate)
- **Concessioned**: Tests marked as `@pytest.mark.skip` or `@pytest.mark.xfail` with documented reason and ticket
- **Fail Rate**: Percentage of tests that fail (always 0% - no failing tests allowed)
- **Module**: Service level (e.g., `services/data-service/`, `frontend/`)

### Concessioned Tests

Tests may be concessioned (skipped or expected to fail) only for:

1. **External dependencies unavailable locally**: Integration tests requiring live APIs, databases, or third-party services
2. **Known bugs with tracking ticket**: `@pytest.mark.xfail(reason="Issue #123")`
3. **TDD RED phase**: Tests written before implementation (temporary, must pass in GREEN phase)
4. **Platform-specific tests**: Tests that only run in certain environments

**All concessioned tests must**:
- Include reason in marker: `@pytest.mark.skip(reason="External API unavailable")`
- Be documented in `{service}/artefacts/test-gaps.md`
- Have tracking ticket if representing technical debt

**Not permitted as concessions**:
- ❌ Broken tests without ticket
- ❌ Tests skipped for convenience
- ❌ Tests that "sometimes fail"
- ❌ Tests skipped to hit coverage target

### Gap Documentation Format

Document all coverage gaps and concessioned tests in `{service}/artefacts/test-gaps.md`:

```markdown
# Test Coverage Gaps

## Coverage Gaps

### [Module/Component Name]
- **Current Coverage**: 94%
- **Gap Location**: `src/auth/oauth.py:45-60`
- **Reason**: External OAuth provider callback - requires live integration
- **Mitigation**: Manual testing checklist in `{service}/artefacts/guides/oauth-testing.md`
- **Ticket**: #123 (to address later)

## Concessioned Tests

### [Test Name]
- **Location**: `tests/integration/test_external_api.py::test_fetch_user_data`
- **Marker**: `@pytest.mark.skip(reason="External API unavailable locally")`
- **Reason**: Requires live connection to third-party API
- **Mitigation**: Runs in CI with API credentials
- **Ticket**: #456 (mock implementation planned)
```

### Enforcement

**Prototype phase:**
```bash
# Advisory only - build succeeds with warning
pytest --cov=src --cov-report=term-missing --cov-fail-under=90
```

**Development phase:**
```bash
# Build fails below threshold
pytest --cov=src --cov-report=term-missing --cov-fail-under=94
```

**Pre-deployment phase:**
```bash
# Strict enforcement - blocks merge
pytest --cov=src --cov-report=term-missing --cov-fail-under=97 --strict-markers
```

## Anti-Patterns (Forbidden)

These practices undermine test quality and are explicitly prohibited:

### 1. Excessive Fallback Usage

```python
# FORBIDDEN: Catching all exceptions to make tests pass
try:
    result = risky_operation()
except Exception:
    result = default_value  # Hides real failures
```

### 2. Skipping Tests to Pass CI

```python
# FORBIDDEN: Skipping without documented reason
@pytest.mark.skip("flaky")  # Not acceptable
def test_critical_feature():
    ...
```

### 3. Mocking Away Failures

```python
# FORBIDDEN: Mocking to avoid testing real behaviour
@patch('module.database.query', return_value=[])  # Avoids testing DB errors
def test_should_handle_empty_results():
    ...  # Never tests what happens with actual DB failures
```

### 4. Test Pollution

```python
# FORBIDDEN: Tests that depend on execution order or shared state
class TestUser:
    user_id = None  # Shared across tests - creates coupling
```

### 5. Assertion-Free Tests

```python
# FORBIDDEN: Tests that don't actually verify anything
def test_user_creation():
    create_user("test@example.com")
    # No assertions - test always passes
```

### Acceptable Patterns

```python
# ACCEPTABLE: Specific exception handling with test for error case
def test_handles_connection_timeout():
    with pytest.raises(ConnectionTimeout):
        slow_operation(timeout=0.001)

# ACCEPTABLE: Skip with documented reason and ticket
@pytest.mark.skip(reason="Requires GCP credentials - see #456")
def test_cloud_storage_upload():
    ...

# ACCEPTABLE: Targeted mocking for isolation
@patch('module.external_api.fetch')
def test_processes_api_response(mock_fetch):
    mock_fetch.return_value = {"status": "ok"}
    result = process_data()
    assert result.success is True
    mock_fetch.assert_called_once()
```


## Test-Driven Development (TDD)

### London School TDD Cycle

**Red → Green → Refactor**

| Phase | Action | Constraint |
|-------|--------|------------|
| Red | Write one failing test | Must fail for right reason |
| Green | Minimum code to pass | Hardcoded returns, no logic |
| Refactor | Improve design | DRY, SOLID, proper names |

### Core Rules

1. **Start with acceptance test** (consumer perspective)
2. **Isolate units**: interface per collaborator, mock for verification
3. **Tell Don't Ask**: command collaborators, don't query state
4. **One behaviour per test**: single assertion, descriptive name
5. **Recurse to boundaries**: DB, APIs, filesystem, clock

### Invariant Tests

Complementary to TDD with different purpose.

**TDD vs Invariants:**

| Aspect | TDD | Invariants |
|--------|-----|------------|
| Question | "What should happen?" | "What should NEVER happen?" |
| Inputs | Specific scenarios | Property-based (often random) |
| Scope | One behaviour | One domain rule |
| Timing | Before implementation | Before OR when rule discovered |

**Test Pyramid:**
```
┌─────────────────────────┐
│  Invariant tests        │  ← Domain rules (essential complexity)
├─────────────────────────┤
│  Unit tests (TDD)       │  ← Behaviour specs
├─────────────────────────┤
│  Integration tests      │  ← Boundaries
└─────────────────────────┘
```

**Invariant Sources:**
1. `domain-rules.yaml` - invariants section
2. Discovered during development (add to domain-rules.yaml)
3. Post-incident (encode "this must never happen again")

**Invariant Test Pattern:**
```typescript
// tests/{domain}/invariants.test.ts
describe('Domain Invariants', () => {
  // From domain-rules.yaml#INV-001
  it('balance is never negative', () => {
    fc.assert(fc.property(
      fc.array(transactionArb),
      (transactions) => {
        const account = applyTransactions(transactions);
        return account.balance >= 0;
      }
    ));
  });
});
```

**Handoff Criteria:**
- All TDD tests pass (behaviour correct)
- All invariant tests pass (domain rules respected)
- If invariant fails: agent hit essential complexity, must fix or escalate
