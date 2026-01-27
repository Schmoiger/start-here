# Multi-Agent Orchestration Guide

This document is your agent knowledge base. Reference it when coordinating workflows.

## Core Principles

**Context Isolation**: Each agent has its own focus and tools. Don't ask an agent to do work outside its domain.

**Filesystem as Shared Memory**: All agents read/write to `./artifacts/`. This is the single source of truth for context.

**Sequential Dependency**: Agents run in phases, with gates between them.

**No Nested Spawning**: Agents cannot spawn other agents. The main Claude Code session is the orchestrator.

---

## Complete Workflow

```
Phase 0: Discovery
    @product-owner → requirements.md, user-stories.md, open-questions.md
        ↓
Phase 1: Design (can run in parallel)
    @solution-architect → architecture.md, api-contract.json, data-model.md
    @database-designer → schema.sql, migrations/, er-diagram.md
    @api-designer → openapi.yaml, api-design-guide.md
    @ui-designer → design-tokens.json, components.md, wireframes.md
        ↓
Phase 1b: Visual Assets (after ui-designer)
    @visual-designer → visuals/ (SVGs, mockups, infographics)
        ↓
Phase 2: Development (sequential)
    @python-coder → ./artifacts/python/
        ↓
    @typescript-coder → ./artifacts/typescript/
        ↓
Phase 3: Review (sequential gate)
    @tech-lead → tech-review.md [GATE: must approve first]
        ↓ [APPROVED?]
        ├─ NO → Back to Phase 2
        └─ YES ↓
    @code-reviewer → code-review.md [deep bug hunting]
        ↓
        ↓
Phase 4: Testing (parallel)
    @functional-tester → test-results/
    @ui-tester → ui-test-results/
    @security-tester → security-audit/
        ↓
Phase 5: Deploy
    @gcp-devops → gcp/terraform/
        ↓
Phase 6: Documentation
    @documentation → docs/
```

---

## Agent Roles

### Phase 0: Discovery

#### product-owner
**When to use**: Starting a new project, clarifying vague requirements, defining scope.

**Tools**: Read, Write, Glob, Grep

**Context**: Any existing materials in `./artifacts/`

**Constraints**:
- Be specific and testable—no vague language
- Prioritise ruthlessly: P0 (MVP), P1 (soon after), P2 (future)
- Describe problems, not solutions
- Flag ambiguities in open-questions.md

**Output**: `requirements.md`, `user-stories.md`, `open-questions.md`

---

### Phase 1: Design

#### solution-architect
**When to use**: Designing system structure, component boundaries, technology choices.

**Tools**: Read, Write, Glob, Grep

**Context**: Reads `./artifacts/requirements.md`, `./artifacts/user-stories.md`

**Constraints**:
- Design for requirements, not hypothetical futures
- Prefer simplicity—avoid over-engineering
- Make technology choices explicit with trade-off analysis
- Define clear interfaces between components

**Output**: `architecture.md`, `api-contract.json` (logical), `data-model.md` (conceptual)

**Ownership**: Creates the logical API contract and conceptual data model. `@api-designer` expands into detailed OpenAPI; `@database-designer` implements as physical schema.

---

#### database-designer
**When to use**: Project needs persistent data storage, schema design, migrations.

**Tools**: Read, Write, Glob, Grep

**Context**: Reads `./artifacts/requirements.md`, `./artifacts/architecture.md`

**Constraints**:
- Default to PostgreSQL syntax
- Prefer normalisation unless performance requires otherwise
- Use UUIDs for primary keys
- Include indexes for foreign keys and common queries
- Design reversible migrations

**Output**: `./artifacts/database/schema.sql`, `./artifacts/database/migrations/`, `er-diagram.md`

**Ownership**: Implements the physical schema based on `@solution-architect`'s conceptual `data-model.md`. Does NOT modify `data-model.md`.

---

#### api-designer
**When to use**: Defining REST or GraphQL APIs, creating OpenAPI specifications.

**Tools**: Read, Write, Glob, Grep

**Context**: Reads `./artifacts/requirements.md`, `./artifacts/architecture.md`, `./artifacts/database/`

**Constraints**:
- Follow OpenAPI 3.0+ specification
- Use consistent naming: camelCase for JSON, kebab-case for URLs
- Document all possible responses
- Include realistic examples

**Output**: `./artifacts/api/openapi.yaml`, `api-design-guide.md`

**Ownership**: Creates detailed OpenAPI spec based on `@solution-architect`'s `api-contract.json`. Does NOT modify `api-contract.json`.

---

#### ui-designer
**When to use**: Before frontend development—designing layouts, components, and design systems.

**Tools**: Read, Write, Glob, Grep

**Context**: Reads `./artifacts/requirements.md`, `./artifacts/user-stories.md`

**Constraints**:
- Use Mermaid diagrams for flows and layouts
- Define design tokens with exact values
- Design for accessibility (WCAG 2.1 AA)
- Cover all states (default, hover, focus, error, loading)
- Consider responsive breakpoints

**Output**: `./artifacts/design/design-tokens.json`, `components.md`, `wireframes.md`, `user-flows.md`, `accessibility.md`

---

#### visual-designer
**When to use**: After ui-designer—generating polished visual assets from Mermaid diagrams and design specs.

**Tools**: Read, Write, Glob, Grep, Bash, Chrome browser tools

**Context**: Reads `./artifacts/design/` (wireframes, user-flows, design-tokens)

**Constraints**:
- Use Napkin AI for infographics and flow visualizations
- Use Mermaid Live for diagram exports
- Use Excalidraw for sketch-style wireframes
- Export as SVG when possible
- Maintain brand colors from design-tokens.json

**Output**: `./artifacts/design/visuals/`, `visuals-manifest.md`

---

### Phase 2: Development

#### python-coder
**When to use**: Building or modifying Python modules, functions, classes.

**Tools**: Read, Write, Edit, Bash, Glob, Grep

**Context**: Reads `./artifacts/requirements.md`, `./artifacts/api-contract.json`, `./artifacts/python/`

**Constraints**:
- Type hints on all functions (Python 3.10+)
- Assume pytest for testing
- Keep modules under 300 lines
- Document public APIs with docstrings

**Output**: Code to `./artifacts/python/`, updated `README.md`

---

#### typescript-coder
**When to use**: Building frontend or backend TypeScript, integrating with Python APIs.

**Tools**: Read, Write, Edit, Bash, Glob, Grep

**Context**: Reads Python APIs from `./artifacts/python/README.md` and `./artifacts/api-contract.json`

**Constraints**:
- Strict mode tsconfig, no `any` types
- Keep modules under 250 lines
- Import from Python only via documented contracts
- Document public exports with JSDoc

**Output**: Code to `./artifacts/typescript/`, updated `README.md`

---

### Phase 3: Review

#### tech-lead
**When to use**: After development, before testing. Validates architecture compliance and standards.

**Tools**: Read, Write, Glob, Grep

**Context**: Reads `./artifacts/architecture.md`, `./artifacts/api-contract.json`, all code

**Review Areas**:
- Architecture compliance
- Code quality and module size limits
- Standards compliance (type hints, strict mode)
- Testability

**Output**: `tech-review.md` with APPROVED or CHANGES REQUIRED status

**Gate**: This is THE gate. If CHANGES REQUIRED, code goes back to developers. Only after APPROVED does code proceed to `@code-reviewer`.

---

#### code-reviewer
**When to use**: After tech-lead approves. Deep code inspection for bugs, edge cases.

**Tools**: Read, Write, Glob, Grep

**Context**: Reads all code in `./artifacts/python/` and `./artifacts/typescript/`

**Review Areas**:
- Correctness and logic errors
- Edge cases (empty inputs, boundaries, unicode)
- Maintainability and performance
- Code-level bugs (NOT systematic security—that's `@security-tester`)

**Output**: `code-review.md` with prioritised issues (Critical > High > Medium > Low)

**Sequencing**: Runs AFTER tech-lead approves. Focuses on bugs, not architecture.

---

### Phase 4: Testing

#### functional-tester
**When to use**: Writing pytest tests, vitest/jest tests, generating test reports.

**Tools**: Read, Write, Edit, Bash, Glob, Grep

**Context**: Reads `./artifacts/python/` and `./artifacts/typescript/` READMEs

**Constraints**:
- Never modify production code
- Aim for 80%+ coverage
- Include happy path + edge cases
- Run tests and capture output

**Output**: Tests to `./artifacts/*/tests/`, results to `./artifacts/test-results/`

---

#### ui-tester
**When to use**: Testing user workflows, end-to-end testing, accessibility checks.

**Tools**: Chrome DevTools MCP only (Read, Write, Bash for logging)

**Context**: Reads `./artifacts/ui-test-scenarios.md` and component docs

**Constraints**:
- Use Chrome DevTools ONLY, no external frameworks
- Test user workflows, not implementation details
- Capture screenshots on failure

**Output**: Results to `./artifacts/ui-test-results/`

---

#### security-tester
**When to use**: Security audit, threat modelling, dependency scanning, prompt injection testing.

**Tools**: Read, Write, Glob, Grep (prompt-based reasoning)

**Context**: Reads all code in `./artifacts/python/` and `./artifacts/typescript/`

**Framework**:
- OWASP Top 10 assessment
- Input validation & sanitisation
- Auth/authz patterns
- Secrets & credentials handling
- Dependency vulnerabilities (requirements.txt, package.json)
- Data exposure & error handling
- **Prompt injection attacks** (for LLM integrations)

**Output**: Findings to `./artifacts/security-audit/`, including `prompt-injection-assessment.md` if LLM integrations exist

**Scope**: Systematic security analysis. `@code-reviewer` catches code-level bugs; you do threat modeling and attack surface analysis.

---

### Phase 5: Deploy

#### gcp-devops
**When to use**: Infrastructure-as-code, deployment config, GCP resource setup.

**Tools**: Read, Write, Edit, Bash, Glob, Grep

**Context**: Reads `./artifacts/requirements.md` and Python/TypeScript READMEs

**Constraints**:
- Use Terraform for IaC
- GCP resources only (Cloud Run, Cloud Build, Firestore, etc.)
- Follow least privilege + encryption best practices
- Include monitoring & logging

**Output**: Terraform configs to `./artifacts/gcp/terraform/`, guides and checklists

---

### Phase 6: Documentation

#### documentation
**When to use**: After code is stable, generate user-facing docs and API references.

**Tools**: Read, Write, Glob, Grep

**Context**: All code, architecture, and API specs in `./artifacts/`

**Documentation Types**:
- API Reference
- Getting Started Guide
- Developer Guide

**Constraints**:
- Write for the audience
- Use concrete examples
- Don't duplicate information—link between docs

**Output**: `./artifacts/docs/api-reference.md`, `getting-started.md`, `developer-guide.md`

---

## Artifacts Directory Structure

```
./artifacts/
├── requirements.md              # Product owner output
├── user-stories.md              # Product owner output
├── open-questions.md            # Product owner output
├── architecture.md              # Solution architect output
├── api-contract.json            # Solution architect output
├── data-model.md                # Solution architect output
├── database/
│   ├── schema.sql               # Database designer output
│   ├── migrations/              # Database designer output
│   ├── er-diagram.md            # Database designer output
│   └── design-decisions.md      # Database designer output
├── api/
│   ├── openapi.yaml             # API designer output
│   └── api-design-guide.md      # API designer output
├── design/
│   ├── design-tokens.json       # UI designer output
│   ├── components.md            # UI designer output
│   ├── wireframes.md            # UI designer output
│   ├── user-flows.md            # UI designer output
│   ├── accessibility.md         # UI designer output
│   ├── visuals/                 # Visual designer output
│   │   ├── *.svg                # Exported diagrams and mockups
│   │   └── *.png                # Raster images when needed
│   └── visuals-manifest.md      # Visual designer output
├── python/
│   ├── *.py                     # Python coder output
│   ├── requirements.txt         # Python coder output
│   ├── README.md                # Python coder output
│   └── tests/                   # Functional tester output
├── typescript/
│   ├── *.ts                     # TypeScript coder output
│   ├── package.json             # TypeScript coder output
│   ├── README.md                # TypeScript coder output
│   └── tests/                   # Functional tester output
├── test-results/
│   └── functional-tests.json    # Functional tester output
├── ui-test-results/
│   ├── screenshots/             # UI tester output
│   ├── ui-tests.json            # UI tester output
│   └── test-log.md              # UI tester output
├── security-audit/
│   ├── findings.json            # Security tester output
│   ├── remediation-guide.md     # Security tester output
│   ├── threat-model.md          # Security tester output
│   └── prompt-injection-assessment.md  # Security tester output (if LLM integrations)
├── gcp/
│   └── terraform/               # GCP DevOps output
├── tech-review.md               # Tech lead output
├── code-review.md               # Code reviewer output
└── docs/
    ├── README.md                # Documentation output
    ├── api-reference.md         # Documentation output
    ├── getting-started.md       # Documentation output
    └── developer-guide.md       # Documentation output
```

---

## Agent Boundaries & Ownership

These rules prevent overlap and clarify who owns what.

### Design Phase Ownership

| Artifact | Owner | Consumers | Rule |
|----------|-------|-----------|------|
| `api-contract.json` | solution-architect | api-designer, coders | **Logical** contract. api-designer expands, doesn't modify. |
| `openapi.yaml` | api-designer | coders, documentation | **Detailed** HTTP spec. Based on api-contract.json. |
| `data-model.md` | solution-architect | database-designer | **Conceptual** model. database-designer implements, doesn't modify. |
| `schema.sql` | database-designer | coders, gcp-devops | **Physical** schema. May differ from conceptual model. |

### Review Phase Sequencing

```
Development complete
        ↓
@tech-lead reviews (architecture, standards)
        ↓
    [APPROVED?]
        │
        ├─ NO → Back to coders (fix blockers)
        │
        └─ YES ↓
              @code-reviewer reviews (bugs, edge cases)
                    ↓
              [Issues found?]
                    │
                    ├─ YES → Back to coders (fix issues)
                    │
                    └─ NO → Proceed to testing
```

### Security Review Split

| Agent | Scope | Examples |
|-------|-------|----------|
| **code-reviewer** | Code-level bugs that are security-related | Null pointer crash, obvious SQL injection in reviewed code |
| **security-tester** | Systematic security analysis | OWASP Top 10, threat modeling, dependency CVEs, prompt injection, auth patterns |

### Visual Designer Trigger

`@visual-designer` runs **on demand**, not automatically. Invoke when you need:
- Presentation-ready mockups for stakeholders
- Exported diagrams for documentation
- Marketing assets

For development, Mermaid diagrams in `wireframes.md` are sufficient.

---

## Workflow Patterns

### Pattern 1: Full Project (All Phases)
```
@product-owner define requirements for [project idea]
    ↓
@solution-architect design the system
@database-designer design the data model
@api-designer create the API specification
@ui-designer design the UI and components
@visual-designer generate visual assets from designs
    ↓
@python-coder implement the backend
    ↓
@typescript-coder implement the frontend
    ↓
@tech-lead review the implementation
    ↓ [if approved]
@functional-tester write and run tests
@security-tester audit for vulnerabilities
    ↓
@gcp-devops create infrastructure
    ↓
@documentation generate user docs
```

### Pattern 2: Quick Feature (Skip Planning)
```
@python-coder add [feature] to existing code
    ↓
@typescript-coder update frontend for new feature
    ↓
@code-reviewer review the changes
    ↓
@functional-tester add tests for new feature
```

### Pattern 3: Design Only
```
@product-owner clarify requirements for [idea]
    ↓
@solution-architect propose architecture options
@api-designer draft API specification
@ui-designer create wireframes and design system
@visual-designer generate polished visuals for presentation
```

### Pattern 4: Parallel Testing
```
@functional-tester run all tests
    ↑          ↑
    │          └─ @ui-tester test user workflows
    │
@security-tester audit for vulnerabilities
```

---

## Communication Between Agents

**Agent → Artifact Updates**:
- Product owner writes `requirements.md` → Solution architect reads it
- Solution architect writes `api-contract.json` → Coders read it
- UI designer writes `design/` → Visual designer reads for asset generation
- Visual designer writes `design/visuals/` → Documentation includes in docs
- UI designer writes `design/` → TypeScript coder reads components and tokens
- Python coder writes `README.md` → TypeScript coder reads it
- Tech lead writes `tech-review.md` → Coders read blockers

**Review Loop**:
- Tech lead reviews → CHANGES REQUIRED → Coders fix → Tech lead re-reviews
- Code reviewer finds issues → Developers address them

**Test Results as Feedback**:
- Tests write to `./artifacts/test-results/` with pass/fail summary
- If failures, tester notes them but doesn't fix (coders handle fixes)
- Rerun agent to iterate

---

## Common Commands in Claude Code

```bash
# Initialize agent environment
./coordinate.sh init

# List available agents
./coordinate.sh list

# Show workflow diagram
./coordinate.sh workflow
```

## Invoking Agents

In Claude Code terminal, use `@agent-name` syntax:

```
# Phase 0: Discovery
@product-owner define requirements for a task management API

# Phase 1: Design
@solution-architect design the system architecture
@database-designer design the database schema
@api-designer create OpenAPI specification
@ui-designer design the user interface and components

# Phase 1b: Visual Assets
@visual-designer generate mockups and diagrams from design specs

# Phase 2: Development
@python-coder implement the task service
@typescript-coder create the frontend client

# Phase 3: Review (sequential - tech-lead first!)
@tech-lead review the implementation
# Wait for APPROVED, then:
@code-reviewer perform detailed code review

# Phase 4: Testing
@functional-tester write and run tests
@ui-tester test the user workflows
@security-tester audit for OWASP vulnerabilities and prompt injection

# Phase 5: Deploy
@gcp-devops create Cloud Run deployment

# Phase 6: Documentation
@documentation generate API reference and guides
```

---

## Best Practices

**1. Start with product-owner**
Don't jump into coding. Let `@product-owner` create `requirements.md` first.

**2. Design before code**
Run `@solution-architect`, `@database-designer`, and `@api-designer` before coding.

**3. Respect the review gate**
Don't skip `@tech-lead` review. It catches issues before expensive testing.

**4. Let agents fail gracefully**
If tests fail, tester reports it. Don't auto-fix; let the coder iterate.

**5. Use filesystem as validation**
If an agent didn't produce expected files in `./artifacts/`, the work wasn't done.

**6. Iterate in loops**
```
code → review → fix → review → approved → test
```

---

## Troubleshooting

**Agent says it can't find files**:
→ Ensure `./artifacts/` directory structure exists. Run `./coordinate.sh init`.

**TypeScript coder says "no Python README"**:
→ `@python-coder` needs to run first and write `./artifacts/python/README.md`.

**Tech lead says CHANGES REQUIRED**:
→ Read `tech-review.md` for blockers. Fix them with the relevant coder agent.

**Tests fail but agent doesn't fix code**:
→ That's correct! `@functional-tester` reports failures; coders fix them.

**Security audit finds issues**:
→ Read `./artifacts/security-audit/remediation-guide.md`. Share findings with relevant coder.

**GCP DevOps can't validate Terraform**:
→ Ensure you have a valid GCP project and credentials. Run `gcloud auth login`.

---

## Further Reading

- [Claude Code Documentation](https://code.claude.com/docs)
- [Claude Code Subagents Guide](https://code.claude.com/docs/en/sub-agents)
- [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk)
