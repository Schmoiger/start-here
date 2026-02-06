# Technology Development Workflow

## Overview

The developer workflow follows a structured approach to ensure quality and consistency across all projects.

## 1. Create Git Branch

Create and switch to a new feature branch following the branch naming conventions. Add gitignore that inherits monorepo gitignore (see `README.md`)

**Branch Naming:**

- `feature/feature-name` for new features
- `bugfix/bugref-name` for bug fixes

**Commands:**

```bash
git checkout -b feature/feature-name
git push -u origin feature/feature-name
```

## 2. Project Setup

Set up project folder with blank files according to documentation standards.

**Files to create:**

- `/artefacts/requirements.md` - Requirements specification (system-wide)
- `/artefacts/architecture.md` - Architecture and design specification (system-wide)
- `{service}/artefacts/tasks.md` - Task breakdown (service-specific)
- README.md and other project files as per standards

## 3. Write Specifications

Write the specs documents in this order:

1. **Requirements** (`/artefacts/requirements.md`)
  - Detail functional and non-functional requirements using EARS notation
  - Specify acceptance criteria and constraints
2. **User Stories** (`/artefacts/user-stories.md`)
  - Define end-to-end user stories spanning multiple services
  - Identify key stakeholders and success criteria
3. **Architecture** (`/artefacts/architecture.md`)
  - Outline technical architecture and design decisions
  - Define data models, APIs, and service interactions

## 4. Check Specs Against Standards

Validate all specifications against the following standards:

- **Documentation Standards** (`/context/standards/`)
  - Ensure consistency with existing patterns
  - Verify adherence to formatting and structure guidelines
- **Technical Standards** (`/context/standards/tech-standards.md`)
  - Confirm technical decisions align with approved patterns
  - Validate architectural choices

## 5. Write Tasks

Break down the specifications into actionable development tasks in `{service}/artefacts/tasks.md` (service-specific).

**Task Structure:**

- Clear, measurable objectives
- Estimated effort and dependencies
- Acceptance criteria
- References to relevant specification sections

## 6. Check Tasks Against Rules

Validate tasks against the established rules and guidelines:

- **Development Rules** (`/context/rules/`)
  - Ensure tasks comply with coding standards
  - Verify testing requirements are included
  - Confirm security considerations are addressed
- **Quality Gates**
  - Unit testing plans
  - Integration testing requirements
  - Code review criteria
  - Deployment readiness checklists

## 7. Update Documentation

Update both project and monorepo-level documentation to reflect completed work.

**Project Documentation:**

- `README.md` - Update with implementation details, usage guides, and deployment instructions
- `{service}/artefacts/` - Update bugs, tasks, todo, test results, and fixtures
- Configuration files documentation

**Monorepo Documentation:**

- `README.md` - Update workspace description
- `/artefacts/` - Update system-wide artefacts (architecture, API contracts, requirements)


## Assumption Handling Protocol

### Escalation Thresholds

Domain sensitivity shifts the decision matrix. Set in `domain-rules.yaml`.

| Threshold | Domains | Effect |
|-----------|---------|--------|
| low | Payments, security, auth | Escalate earlier |
| medium | Default | Standard matrix |
| high | UI, docs, tooling | More autonomy |

### Decision Matrix (threshold: medium)

| Impact if Wrong | Confidence | Action |
|-----------------|------------|--------|
| Low | Any | Assume, document, proceed |
| Medium | High | Assume, document, proceed |
| Medium | Low | Assume, document, flag for review |
| High | Any | Escalate as blocker |

### Document in Handoff

```json
{
  "assumptions": [
    {
      "decision": "What was assumed",
      "confidence": "low|medium|high",
      "rationale": "Why this assumption",
      "impact_if_wrong": "low|medium|high"
    }
  ],
  "blockers": [
    {
      "id": "DOMAIN-001",
      "question": "What needs answering",
      "impact": "high|medium|low",
      "status": "open|resolved",
      "resolution_ref": "domain-rules.yaml#DOMAIN-001"
    }
  ]
}
```

### Resolution Flow

1. Agent hits blocker → logs in handoff (question, status: open)
2. Human resolves → adds to domain-rules.yaml#resolved_blockers
3. Orchestrator updates handoff → status: resolved, resolution_ref
4. Knowledge persists for future tasks

**Single source of truth**: `domain-rules.yaml`. Handoff contains reference only.

### Impact Assessment

| Impact | Characteristics |
|--------|-----------------|
| Low | Easily reversible, localised, no external dependencies |
| Medium | Requires rework but contained, single domain |
| High | Cascading, external APIs, security, data migration |

### Escalation Path

```
Agent → Domain Orchestrator → Meta-Orchestrator → Human
```

### Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Silently assume | Document every assumption |
| Block on low-impact unknowns | Proceed with documented assumption |
| Guess on high-impact decisions | Escalate as blocker |
| Ask humans for every question | Reserve for blockers |
| Duplicate resolution in handoff | Reference domain-rules.yaml |
| Escalate without checking resolved_blockers | Check first |

## Retrospective Guidelines

### Structure

Check-in → What Went Well → What Didn't → Action Items → Check-out

### Prime Directive

"Everyone did the best they could given what they knew at the time."

### Rules

- Focus on improvement, not blame
- Be honest; listen to others
- Create SMART action items (Specific, Measurable, Achievable, Relevant, Time-bound)

## Communication Style

### Teaching Engineer Persona

When working with users, adopt an expert engineer teaching a novice:
- Suggest improvements, simplifications, and optimisations
- Explain clearly and simply
- Provide rationale for decisions
- Offer learning opportunities

## 8. Orchestrator Agent Invocation

When spawning subagents, pass project-specific paths only. Standards are inherited (agent-standards.md §1.1).

**Required context:**
- Project root: `{absolute-path}`
- Task reference: `Read {TASK-ID} from {path}/tasks.md`
- Output location: `Create at {path}/{file}` (reference doc-standards.md section)

**Example:**
```
@python-coder execute LOG-003

Project: /Users/avi/Repos/bollinger
Task: Read LOG-003 from artefacts/build/tasks.md
Output: packages/shared-types/python/bollinger_types/
```

**Anti-pattern:** Don't repeat standards (coding, testing, doc) - agents inherit these.

---

## 9. UI Testing Quality Gate

When @ui-tester completes, orchestrator SHALL verify deliverables before accepting results:

**Required Evidence (ALL must be present):**
- [ ] Screenshots in `artefacts/test-results/e2e/screenshots/` (minimum 1)
- [ ] Test log documents browser interactions (not just API calls)
- [ ] At least one complete user workflow tested

**Rejection Criteria:**
- ❌ No screenshots → Not valid UI test
- ❌ Only API testing → Use @functional-tester instead
- ❌ No browser interactions documented → Insufficient evidence

**Example Valid Test Log:**
```
1. Opened browser to http://localhost:3000
2. Clicked search input
3. Typed "AAPL"
4. Screenshot: search-results.png showing dropdown
5. Clicked first result
6. Screenshot: chart-loaded.png showing Bollinger Bands
```

**Example Invalid Test Log:**
```
1. curl http://localhost:8001/data/search?q=AAPL → 200 OK
2. All APIs responding correctly
```

---

## 10. Parallel Execution Analysis

### When to Suggest Parallelisation

The orchestrator should proactively analyse parallelisation opportunities when:
- Spawning multiple agents (>1 agent)
- Tasks expected to exceed 5 minutes
- Multiple independent modules/services being worked on
- Code reviews, testing, or builds across separate domains
- Any situation where independent work streams exist

### Presenting Options

Use this template when suggesting parallel execution to users:

**Current Approach: [Sequential/Single]**
- Timeline: [Agent A → Agent B → Agent C]
- Estimated time: X minutes
- Estimated tokens: Y tokens (baseline)

**Option A: [Partial Parallel]**
- Execution: [Track 1: A+B parallel, Track 2: C]
- Time saved: Z% faster (X min → W min)
- Token increase: +N% (context duplication, coordination overhead)
- Trade-offs: [Merge complexity, potential conflicts]

**Option B: [Full Parallel]**
- Execution: [A, B, C all parallel]
- Time saved: Z% faster (X min → W min)
- Token increase: +N% (context duplication, coordination overhead)
- Trade-offs: [Higher coordination, merge conflicts, more complex error handling]

### Decision Criteria

Present options and let user choose based on priorities:
- **Speed priority**: Full parallel execution
- **Cost priority**: Sequential execution (minimal token usage)
- **Quality priority**: Sequential with careful human review between stages
- **Balanced**: Partial parallel (2-3 independent tracks)

### Estimation Guidelines

**Time Savings**:
- 2 independent agents: ~40-50% faster (not 50% due to coordination)
- 3+ independent agents: ~60-70% faster (diminishing returns)

**Token Increase**:
- 2 agents: +10-15% (shared context, some duplication)
- 3 agents: +20-30% (more context duplication)
- 4+ agents: +30-40% (significant overhead)

### Examples

**Example 1: Code Review**
```
Current: Single reviewer, 30 min, 150k tokens

Option A (2 tracks):
- Backend + Frontend parallel
- 20 min (33% faster)
- 165k tokens (+10%)
- Trade-off: Need to merge findings

Option B (3 tracks):
- Backend, Frontend, Integration all parallel
- 12 min (60% faster)
- 180k tokens (+20%)
- Trade-off: Higher coordination, merge conflicts
```

**Example 2: TDD Implementation**
```
Current: Frontend then Backend, 40 min, 200k tokens

Option A (parallel):
- Frontend + Backend simultaneously
- 22 min (45% faster)
- 220k tokens (+10%)
- Trade-off: API contract must be agreed first
```

### When NOT to Parallelise

- Tasks with sequential dependencies (B needs A's output)
- Single-file modifications (conflicts guaranteed)
- High coordination overhead (>30% of work is merging)
- User explicitly requests sequential approach
- Quality gate reviews (must run sequentially by design)

### Best Practices

1. **Identify dependencies first** - Map out what depends on what
2. **Define clear boundaries** - Separate work by file, module, or service
3. **Agree contracts upfront** - API contracts, interfaces, schemas
4. **Plan merge strategy** - Who merges what, conflict resolution
5. **Monitor progress** - Check agents aren't duplicating work
6. **Learn and adapt** - Track actual vs estimated time/tokens
