# withineve Testing Standards

**TDD-First Development**: Write tests before implementation. No code without passing tests.

**Quality Gate**: All tests must pass before commits, reviews, or deployments.

**Testing Pyramid**:
- **Unit Tests (70%)**: Isolated functions/methods with mocked dependencies
- **Integration Tests (20%)**: Component interactions with real services
- **E2E Tests (10%)**: Complete user workflows with real browsers

## TDD Cycle

**Red**: Write failing test first for each requirement/behavior.

**Green**: Implement minimal code to pass test.

**Refactor**: Clean up code while maintaining passing tests.

## Test Types

**Unit Tests (pytest/Vitest)**: Isolated functions/methods, mock all dependencies.

**Integration Tests**: Component interactions, use real services where safe.

**E2E Tests (Playwright)**: Complete user workflows with real browsers.

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

## Test Organization
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
- **Test Coverage Requirements**: Minimum 90% coverage for new code
- **Quality Gates**: 100% of tests must pass before merge
- **Warnings**: Bugs to be raised for all warnings