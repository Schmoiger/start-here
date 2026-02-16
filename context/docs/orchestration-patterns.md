# Orchestration Patterns

This guide shows **how to coordinate agents** using different orchestration patterns. Choose the pattern that matches your task complexity.

---

## Pattern 1: Single Agent (Simple Tasks)

**Use when**: Task is straightforward, requires one specialist, no dependencies.

**Example**: Fix a specific bug, add a simple feature, write documentation.

```
User: @python-coder Fix the login validation bug in auth_service.py

Agent reads:
- context/agents/python-coder.md (agent definition)
- context/standards/tech-standards.md (Python patterns)
- context/rules/python-environment.mdc (uv usage)

Agent writes:
- Fixed code
- Updated tests
- HANDOFF.md entry
```

**When to use**:
- Single-file changes
- Clear requirements
- No design decisions needed
- No cross-agent dependencies

**Avoid when**:
- Task touches multiple languages/domains
- Requires design review
- Needs sequential approval gates

---

## Pattern 2: Sequential Chain (Dependent Tasks)

**Use when**: Tasks must complete in order, each depends on previous output.

**Example**: Design → Implement → Review

```
# Phase 1: Design
User: @solution-architect Design user authentication system

[Wait for architecture.md]

# Phase 2: Implement
User: @python-coder Implement auth based on architecture.md

[Wait for implementation]

# Phase 3: Review
User: @tech-lead Review the authentication implementation

[Wait for approval]
```

**When to use**:
- Clear dependencies (A → B → C)
- Quality gates required
- Each phase needs human verification

**Workflow mapping**: Matches TDD workflow (RED → GREEN → BLUE)

---

## Pattern 3: Parallel Swarm (Independent Tasks)

**Use when**: Multiple agents work simultaneously on independent tasks.

**Example**: Design phase with parallel specialists

```
User: Spawn these agents in parallel:

@solution-architect Design system architecture
@database-designer Design PostgreSQL schema
@api-designer Create OpenAPI specification
@ui-designer Design component structure

[All agents run simultaneously, no dependencies]
```

**When to use**:
- Tasks are independent (no shared state)
- Can merge outputs later
- Want maximum speed

**Token cost**: Higher (context duplicated across agents)
**Time savings**: ~40-50% faster than sequential

**Workflow mapping**: Matches `design` phase in default.yaml (parallel: true)

---

## Pattern 4: Hive (Coordinated Parallel)

**Use when**: Multiple agents work in parallel but need coordination points.

**Example**: TDD GREEN phase (parallel coders, shared test suite)

```
# Coordination point 1: Tests defined
User: @functional-tester Write tests for auth endpoints
[Wait for tests to exist]

# Parallel execution
User: Spawn in parallel:

@python-coder Implement backend to pass tests
@typescript-coder Implement frontend to pass tests

[Both agents share same test suite, work independently]

# Coordination point 2: Merge and verify
User: @tech-lead Review combined implementation
```

**When to use**:
- Parallel work with shared contracts (tests, API specs, schemas)
- Clear integration points
- Want speed but need coordination

**Coordination mechanisms**:
- Shared artefacts (tests, schemas, API specs)
- Sequential gates before/after parallel work
- Clear boundaries (backend vs frontend)

**Workflow mapping**: Matches `tdd-green` phase (parallel coders, shared tests)

---

## Pattern 5: Iterative Loop (Refinement)

**Use when**: Agent output needs review and revision until approved.

**Example**: Design review with revisions

```
# Iteration 1
User: @solution-architect Design authentication system
User: @tech-lead Review architecture

[Result: CHANGES REQUIRED - missing rate limiting]

# Iteration 2
User: @solution-architect Add rate limiting to architecture
User: @tech-lead Review updated architecture

[Result: APPROVED]
```

**When to use**:
- Quality gates with potential rejections
- Iterative refinement needed
- Uncertain requirements

**Workflow mapping**: Matches quality gate phases (design-review, quality-review)

---

## Pattern Comparison

| Pattern | Speed | Token Cost | Coordination | Use Case |
|---------|-------|------------|--------------|----------|
| **Single** | Fast | Low | None | Simple, isolated tasks |
| **Sequential** | Slow | Low | Linear | Dependencies, quality gates |
| **Parallel Swarm** | Fastest | High | None | Independent tasks |
| **Hive** | Fast | High | Shared artefacts | Coordinated parallel work |
| **Iterative** | Varies | Medium | Approval loops | Refinement, quality gates |

---

## Choosing a Pattern

**Decision tree**:

1. **Is this a single, isolated task?**
   - Yes → Single Agent
   - No → Continue

2. **Can tasks run independently?**
   - Yes → Parallel Swarm
   - No → Continue

3. **Do tasks share artefacts (tests, schemas)?**
   - Yes → Hive (parallel with coordination)
   - No → Continue

4. **Are there sequential dependencies?**
   - Yes → Sequential Chain
   - No → Continue

5. **Does output need iterative refinement?**
   - Yes → Iterative Loop
   - No → Reconsider requirements

---

## Workflow Integration

The **default workflow** combines these patterns:

- **discovery**: Sequential Chain (product-expert → product-owner)
- **design**: Parallel Swarm (5 designers, independent)
- **design-review**: Sequential Chain (5 reviewers, approval gate)
- **tdd-red**: Single Agent (functional-tester)
- **tdd-green**: Hive (parallel coders, shared tests)
- **tdd-blue**: Hive (parallel coders, shared tests)
- **testing**: Sequential Chain (unit → integration → e2e)
- **quality-review**: Iterative Loop (review → fix → re-review)
- **deployment**: Sequential Chain (deploy → review)

**Pattern mixing**: Real workflows combine multiple patterns across phases.

---

## Best Practices

### Single Agent
- ✅ Keep task scope narrow
- ✅ Provide clear context files to read
- ❌ Don't use for multi-domain tasks

### Sequential Chain
- ✅ Define clear handoff points
- ✅ Update HANDOFF.md between phases
- ❌ Don't parallelize dependencies

### Parallel Swarm
- ✅ Ensure true independence (no shared state)
- ✅ Define merge strategy upfront
- ❌ Don't use when agents need each other's output

### Hive
- ✅ Define shared artefacts before parallel work
- ✅ Use coordination points (before/after parallel)
- ❌ Don't skip integration verification

### Iterative Loop
- ✅ Set max iterations (avoid infinite loops)
- ✅ Track rejection reasons
- ❌ Don't auto-retry without addressing feedback

---

## Token Optimization

**Parallel work increases token usage** because context is duplicated:

**Example**: 3 agents in parallel
- Sequential: 100K tokens (reuse context)
- Parallel: 120K tokens (context × 3, ~20% overhead)

**When to parallelize**:
- Time is critical (speed > cost)
- Tasks are large (parallelism overhead is small % of total)
- Agents have different contexts (minimal duplication)

**When to stay sequential**:
- Token budget is tight
- Tasks are small (overhead dominates)
- Context is large and identical across agents

---

## Error Handling

**Pattern-specific strategies**:

| Pattern | Error Handling |
|---------|----------------|
| **Single** | Agent reports error → user fixes → retry |
| **Sequential** | Current phase fails → fix → restart from failure point |
| **Parallel** | One agent fails → others continue → fix failed agent → merge |
| **Hive** | Coordination failure → rollback to coordination point → retry |
| **Iterative** | Rejection → fix → re-submit → max N iterations |

**General principle**: Always report errors to orchestrator, never auto-retry without fixing root cause.

---

## Examples

### Example 1: New Feature (Hive Pattern)

```
Task: Add user profile feature

# Step 1: Design (Parallel Swarm)
@solution-architect Design profile architecture
@database-designer Design profile schema
@api-designer Create profile API spec
@ui-designer Design profile UI

# Step 2: Review (Sequential)
@tech-lead Review architecture
@code-reviewer Review API spec

# Step 3: Tests (Single)
@functional-tester Write failing tests for profile

# Step 4: Implement (Hive - shared tests)
@python-coder Implement backend (make tests pass)
@typescript-coder Implement frontend (make tests pass)

# Step 5: Verify (Sequential)
@tech-lead Review implementation
@security-tester Audit security
```

### Example 2: Bug Fix (Single Agent)

```
Task: Fix validation bug

# Single agent, single phase
@python-coder Fix email validation in auth_service.py
```

### Example 3: Architecture Refactor (Iterative Loop)

```
Task: Refactor to microservices

# Iteration 1
@solution-architect Design microservices architecture
@tech-lead Review architecture
→ CHANGES REQUIRED: missing service boundaries

# Iteration 2
@solution-architect Define service boundaries
@tech-lead Review updated architecture
→ APPROVED
```

---

## See Also

- `context/workflows/default.yaml` - Full TDD workflow combining patterns
- `context/workflows/prototype.yaml` - Fast workflow with minimal gates
- `context/docs/workflow-default.md` - How to use default workflow
- `AGENTS.md` - Auto-generated agent reference
