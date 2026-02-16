---
purpose: Testing methodology, TDD process, and coverage requirements
audience: All developers and testing agents
read-when: Writing tests, defining coverage, TDD process questions
not-for: Tool installation (see tech-standards.md §Testing Tools)
related: [tech-standards, coding-standards, workflow-standards]
---

# Testing Standards

**TDD-First Development**: Write tests before implementation. No code without passing tests.

**Quality Gate**: All tests must pass before commits, reviews, or deployments.

**Test Dashboard**: Maintain auto-generated `test-results/DASHBOARD.md` for at-a-glance status (coverage, pass rates, trends, concessioned tests). Update after each test run.

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

**Integration Tests (20% of pyramid)**: Component interactions, use real services where safe. Two levels:

*API Integration*:
- Agent: @functional-tester writes these
- Test service-to-service communication (backend ↔ backend)
- Test API contracts (frontend → backend API)
- Real database with isolation (per-test transactions or cleanup)
- Mocked external services
- Focus: Contract compliance, error handling, data flow
- Tools: See [tech-standards.md §Monorepo Tools](tech-standards.md#monorepo-tools)

**Database Isolation Requirements:**
- Real database **per test** (no shared state between tests)
- Use database transactions with rollback, or cleanup fixtures
- Database fixtures/factories for test data (not hardcoded)
- No test pollution - each test starts with clean state

*Component Integration (Browser-based)*:
- Agent: @functional-tester writes these
- Test components with user interactions in simulated browser environment
- Render components, simulate clicks/typing, verify DOM updates
- Extends testing beyond API surface to include UI behaviour
- Real component rendering, mocked backend API responses
- Focus: Component behaviour with user interactions, not isolated unit logic
- Example: "Click 'Add to Portfolio' button → verify modal opens and form renders"
- Tools: See [tech-standards.md §Monorepo Tools](tech-standards.md#monorepo-tools)

**E2E Tests (10% of pyramid)**: Complete user workflows with real browsers.
- Agent: @ui-tester performs these
- **MUST use actual browser** (not simulated DOM)
- **MUST capture screenshots** as evidence
- Tests user-facing behaviour and complete workflows
- Verify visual elements render correctly
- Real browser, real backend, real external services (or staging equivalents)
- Focus: User journeys end-to-end
- Example: "User signs in → views portfolio → adds holding → verifies chart updates"
- Tools: See [tech-standards.md §Monorepo Tools](tech-standards.md#monorepo-tools)

**Test Scope Distinction:**
- **Unit**: Isolated function, all dependencies mocked
- **API Integration**: Multiple components, real database, mocked external APIs
- **Component Integration**: UI component + interactions, mocked backend
- **E2E**: Full user workflow, real browser, real services

**Agent Distinction:**
- @functional-tester: Writes automated test code (unit, API integration, component integration)
- @ui-tester: Executes browser-based E2E scenario testing with evidence capture

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
// Example pattern: navigate, capture screenshot, assert. Use the E2E tool specified in tech-standards.
// Pseudocode: launch browser → goto URL → screenshot → compare to baseline (threshold per context).
```

**Visual Regression Thresholds:**
- **0.1% (0.001)**: Pixel-perfect matching (typography, layout, spacing)
- **1-2% (0.01-0.02)**: Anti-aliasing differences across browsers/devices
- **5% (0.05)**: Dynamic content areas (timestamps, user-specific data)

### Visual Testing Workflow

1. **Baseline**: Initial approved screenshots become "golden" images
2. **Regression Detection**: CI catches visual changes from baseline
3. **Manual Review**: Team reviews and approves or rejects changes
4. **Update Baselines**: Approved changes become new baseline

## Testing Tools & Frameworks

For tool choices and installation commands, see [tech-standards.md §Testing Tools](tech-standards.md#testing-tools).

### CI/CD Integration

- **GitHub Actions**: Automated test execution on PRs
- **Quality Gates**: 100% of tests must pass before merge
- **Warnings**: Bugs to be raised for all warnings

## Coverage Requirements

Coverage requirements increase as code progresses toward deployment. Thresholds are enforced **per service** (not aggregate across all services).

### Phase-Based Thresholds

| Phase          | Coverage | Pass Rate | Concessioned | Fail Rate | Enforcement                  |
| -------------- | -------- | --------- | ------------ | --------- | ---------------------------- |
| Prototype      | No threshold | No threshold | —        | —         | Advisory (just needs to work)|
| Development    | ≥95%     | ≥95%      | ≤5%          | 0%        | Build fails below threshold  |
| Pre-deployment | ≥97%     | ≥97%      | ≤3%          | 0%        | Merge blocked below threshold |

Enforced by [quality-gates.mdc](../rules/quality-gates.mdc).

**TDD RED Phase Exception**: During TDD RED phase only, newly written tests may fail if:
- Marked with `@pytest.mark.wip` or `@pytest.mark.xfail(reason="TDD RED - not implemented")`
- Must pass in TDD GREEN phase before GREEN commit
- Cannot remain in WIP state >24 hours
- RED commit message must use `test:` type (e.g., `test(auth): add failing tests for OAuth flow`)

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

```bash
# Enforcement: adjust threshold per phase
pytest --cov=src --cov-report=term-missing --cov-fail-under={THRESHOLD}
# THRESHOLD: none (prototype), 95 (development), 97 (pre-deployment)
# Enforced by quality-gates.mdc
```

## UI Test Coverage

UI tests use **scenario coverage** rather than code coverage. The same phase-based thresholds apply to the percentage of test scenarios executed with evidence.

### Scenario-Based Coverage

**Coverage metric**: Percentage of defined test scenarios that have been executed with evidence (screenshots + test log entries).

**Module**: Service or application (e.g., `frontend/`, `mobile/ios/`)

| Phase          | Scenario Coverage | Pass Rate | Concessioned | Fail Rate |
| -------------- | ----------------- | --------- | ------------ | --------- |
| Prototype      | ≥90%              | ≥90%      | ≤10%         | 0%        |
| Development    | ≥94%              | ≥94%      | ≤6%          | 0%        |
| Pre-deployment | ≥97%              | ≥97%      | ≤3%          | 0%        |

### Test Scenario Structure

Define test scenarios in `{service}/artefacts/test-results/e2e/test-scenarios.md` with measurable checkpoints:

```markdown
# UI Test Scenarios

## User Authentication Journey

### SC-001: Sign in with Google
- **Priority**: Critical
- **Steps**: Navigate to homepage → Click "Sign in with Google" → Complete OAuth → Verify dashboard redirect → Verify user name in header
- **Evidence Required**: Screenshots of homepage, dashboard, user name
- **Status**: ✅ Passed (2026-02-06)
```

Follow this structure for all scenarios. Full format in `{service}/artefacts/test-results/e2e/test-scenarios.md`.

### Evidence Requirements

Each executed scenario must have:
1. **Screenshots**: Saved to `{service}/artefacts/test-results/e2e/screenshots/{scenario-id}/`
2. **Test log entry**: In `{service}/artefacts/test-results/e2e/test-log.md` with timestamp, actions, and outcome
3. **Status marker**: ✅ Passed | ❌ Failed | ⏸️ Concessioned

### Evidence Storage Management

Screenshots accumulate quickly. Implement retention policy:

**Retention:**
- Keep latest 3 test runs in `e2e/screenshots/`
- Archive older runs to `test-results/archive/{date}-e2e/`
- Compress screenshots: lossless PNG → WebP (80-90% size reduction)
- Max evidence directory size: 500MB per service

**Cleanup:**
```bash
# Archive old screenshots (keep latest 3 runs)
find test-results/e2e/screenshots -type d -mtime +3 | xargs -I{} mv {} test-results/archive/$(date +%Y-%m-%d)-e2e/

# Compress archived screenshots
find test-results/archive -name "*.png" -exec cwebp -lossless {} -o {}.webp \;
```

**Example test log entry:**

```markdown
## SC-001: Sign in with Google
**Date**: 2026-02-06T14:32:00Z | **Tester**: @ui-tester | **Duration**: 45s
**Actions**: Navigated to localhost:5173 → Clicked google-signin → Completed OAuth → Verified /dashboard redirect → Verified user-name element
**Result**: ✅ PASSED
**Evidence**: `e2e/screenshots/SC-001/{01-homepage, 04-dashboard, 05-user-name}.png` | Chrome 131 | 1920×1080
```

### Coverage Calculation

**Reported Coverage**: `(Passed + Concessioned) / Total × 100` — must meet phase threshold
**Effective Coverage**: `Passed / Total × 100` — tracks actual tested scenarios
**Fail Rate**: Must be 0% (no failing tests allowed). Build fails if >0%.

Track effective coverage to prevent concessioned tests from masking untested areas.

### Concessioned Scenarios

UI scenarios may be concessioned only for:

1. **Browser-specific features**: Tests requiring Safari/Firefox when only Chrome available
2. **Platform-specific tests**: Mobile tests requiring physical device
3. **External authentication**: OAuth flows requiring production credentials
4. **Third-party integrations**: Features requiring external service (e.g., payment gateway)

**All concessioned scenarios must**:
- Have status `⏸️ Concessioned` with reason
- Be documented in `{service}/artefacts/test-gaps.md`
- Have tracking ticket
- Include mitigation plan (e.g., "Runs in CI with device farm")

### Gap Documentation

Include concessioned UI scenarios in `{service}/artefacts/test-gaps.md`:

```markdown
## Concessioned UI Scenarios

### SC-003: Mobile responsive layout
- **Location**: `e2e/test-scenarios.md#sc-003`
- **Reason**: Requires physical mobile device for accurate touch target testing
- **Mitigation**: Runs in CI with BrowserStack device farm
- **Ticket**: #234 (BrowserStack integration planned)
- **Estimated Resolution**: Sprint 4
```

### Automation Tools

While markdown scripts are valid for scenario definition and evidence tracking, consider these tools for execution:

**Chrome DevTools Protocol (current approach)**:
- ✅ No external framework dependency
- ✅ Direct browser control
- ❌ Manual test log maintenance
- ❌ Screenshot management overhead

**Lightweight alternatives** (if automation needed):
- Use the browser automation tool specified in [tech-standards.md](tech-standards.md) (§Testing Tools).
- Options: Markdown test reporter (generates logs from test code), or script that reads markdown scenarios and executes (see tech-standards for usage).

**Recommendation**: Continue with markdown scripts in prototype/development phases. Consider automation only in pre-deployment phase if scenario count >100.

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
