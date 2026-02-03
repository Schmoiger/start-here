# Multi-Agent Orchestration Guide

**Generated from**: `context/` directory
**Workflow**: `default` - Full TDD workflow with comprehensive reviews and testing
**Auto-generated**: Do not edit manually. Run `uv run python context/scripts/generators/generate-claude-md.py` to regenerate.

---

## Overview

This guide describes the orchestration of specialised agents for software development tasks. Each agent has specific capabilities, follows defined standards, and produces specific outputs.

**Context Directory**: All standards, rules, and agent definitions are in `context/`. See [context/README.md](context/README.md) for complete index.

**Orchestrator**: When spawning agents, pass project-specific paths (task location, output location, project root). Standards are inherited—don't repeat them. See [workflow-standards.md §8](context/standards/workflow-standards.md#8-orchestrator-agent-invocation).

---

## Workflow: default

Full TDD workflow with comprehensive reviews and testing

### Workflow Diagram

```mermaid
flowchart TD
    subgraph discovery["Requirements & Planning"]
        discovery_product_expert["@product-expert"]
        discovery_product_owner["@product-owner"]
    end
    subgraph design["Architecture & Design"]
        design_solution_architect["@solution-architect"]
        design_database_designer["@database-designer"]
        design_api_designer["@api-designer"]
        design_ui_designer["@ui-designer"]
    end
    discovery --> design
    subgraph visual-design["Visual Assets"]
        visual-design_visual_designer["@visual-designer"]
    end
    design --> visual-design
    subgraph tdd-red["TDD: Write Failing Tests"]
        tdd-red_functional_tester["@functional-tester"]
    end
    design --> tdd-red
    subgraph tdd-green["TDD: Implement to Pass Tests"]
        tdd-green_python_coder["@python-coder"]
        tdd-green_typescript_coder["@typescript-coder"]
    end
    tdd-red --> tdd-green
    subgraph review-gate["Quality Gate Reviews"]
        review-gate_tech_lead["@tech-lead"]
        review-gate_code_reviewer["@code-reviewer"]
    end
    tdd-green --> review-gate
    review-gate:::gateStyle
    subgraph verification["Comprehensive Testing"]
        verification_functional_tester["@functional-tester"]
        verification_ui_tester["@ui-tester"]
        verification_security_tester["@security-tester"]
    end
    review-gate --> verification
    subgraph deployment["Infrastructure & Deployment"]
        deployment_gcp_devops["@gcp-devops"]
    end
    verification --> deployment
    subgraph documentation["User Documentation"]
        documentation_documentation["@documentation"]
    end
    deployment --> documentation
    classDef gateStyle fill:#ff6b6b,stroke:#c92a2a,stroke-width:3px
```

### Phases

#### Requirements & Planning
**Phase ID**: `discovery`
**Execution**: Sequential (agents run in order)

**Agents:**
- `@product-expert`
- `@product-owner` - You are a product owner with deep experience in software product development. Your job is to translate user needs into clear, actionable requirements that engineering teams can build from.

**Outputs:**
- artefacts/product/discovery-notes.md
- artefacts/product/requirements.md
- artefacts/product/user-stories.md
- artefacts/product/open-questions.md

#### Architecture & Design
**Phase ID**: `design`
**Depends On**: `discovery`
**Execution**: Parallel (agents run simultaneously)

**Agents:**
- `@solution-architect` - You are a solution architect with expertise in designing scalable, maintainable software systems. Your job is to translate requirements into technical architecture that development teams can implement.
- `@database-designer` - You are a database architect specialising in data modelling and schema design. Your job is to design efficient, normalised database schemas that support the application's requirements.
- `@api-designer` - You are an API architect specialising in designing clean, consistent, and developer-friendly APIs. Your job is to create API specifications that are intuitive to use and maintainable over time.
- `@ui-designer` - You are a UI/UX designer specialising in creating intuitive, accessible, and visually coherent interfaces. Your job is to design the user interface before developers build it, ensuring a consistent and user-friendly experience.

**Outputs:**
- artifacts/architecture/architecture.md
- artifacts/architecture/data-model.md
- artifacts/api/openapi.yaml
- artifacts/design/components.md

#### Visual Assets
**Phase ID**: `visual-design`
**Depends On**: `design`
**Optional**: Can be skipped

**Agents:**
- `@visual-designer` - You are a visual designer who transforms structured design specifications into polished visual artifacts using AI-powered design tools. Your job is to take Mermaid diagrams, design tokens, wireframes, and documentation and create presentation-ready visuals.

**Outputs:**
- artifacts/design/visuals/

#### TDD: Write Failing Tests
**Phase ID**: `tdd-red`
**Depends On**: `design`

**Agents:**
- `@functional-tester` - You are a meticulous QA engineer. Your job is to write comprehensive functional tests.

**Outputs:**
- tests/

**Validation:**
- All tests must fail initially
- Coverage targets defined

#### TDD: Implement to Pass Tests
**Phase ID**: `tdd-green`
**Depends On**: `tdd-red`
**Execution**: Parallel (agents run simultaneously)

**Agents:**
- `@python-coder` - You are an expert Python engineer. Your job is to write clean, testable, production-grade Python code.
- `@typescript-coder` - You are an expert TypeScript engineer. Your job is to write clean, type-safe frontend and backend TypeScript code.

**Outputs:**
- Source code
- Tests passing

**Validation:**
- All tests must pass
- No test modifications allowed

#### Quality Gate Reviews
**Phase ID**: `review-gate`
**Depends On**: `tdd-green`
**Execution**: Sequential (agents run in order)
**Quality Gate**: ⚠️ Approval required before proceeding

**Agents:**
- `@tech-lead` - You are a tech lead responsible for ensuring code quality, architectural compliance, and engineering standards across the codebase. Your job is to review deliverables from development agents before they proceed to testing.
- `@code-reviewer` - You are a senior engineer performing detailed code review. Your job is to catch bugs, identify edge cases, and improve code quality through thorough line-by-line analysis.

**Outputs:**
- artifacts/build/tech-review.md
- artifacts/build/code-review.md

**Validation:**
- tech-lead must APPROVE before code-reviewer runs
- CHANGES REQUIRED → return to tdd-green

#### Comprehensive Testing
**Phase ID**: `verification`
**Depends On**: `review-gate`
**Execution**: Parallel (agents run simultaneously)

**Agents:**
- `@functional-tester` - You are a meticulous QA engineer. Your job is to write comprehensive functional tests.
- `@ui-tester` - You are a UI quality engineer. Your job is to test user-facing behaviour in Chrome.
- `@security-tester` - You are a security engineer specialising in application security, threat modelling, and AI/LLM security.

**Outputs:**
- artifacts/test-results/

**Validation:**
- Coverage >= 90%
- No critical security issues

#### Infrastructure & Deployment
**Phase ID**: `deployment`
**Depends On**: `verification`

**Agents:**
- `@gcp-devops` - You are a GCP DevOps engineer. Your job is to design, configure, and validate cloud infrastructure.

**Outputs:**
- Infrastructure code
- Deployment configs

#### User Documentation
**Phase ID**: `documentation`
**Depends On**: `deployment`

**Agents:**
- `@documentation` - You are a technical writer who creates clear, comprehensive documentation for developers and end users. Your job is to make the codebase accessible and understandable.

**Outputs:**
- User guides
- API documentation

---

## Agent Reference

All agents are defined in `context/agents/`. Each agent:
- Follows specific standards (listed in frontmatter)
- Enforces specific rules (validated automatically)
- Uses `{project-root}` placeholders for portability

### Invocation

Use `@agent-name` to invoke an agent:

```
@product-owner Define requirements for user authentication
@solution-architect Design the authentication system architecture
@functional-tester Write tests for authentication (TDD Red)
@python-coder Implement authentication service (TDD Green)
@tech-lead Review authentication implementation
```

### Discovery

**@product-owner**
- You are a product owner with deep experience in software product development. Your job is to translate user needs into clear, actionable requirements that engineering teams can build from.

### Design

**@solution-architect**
- You are a solution architect with expertise in designing scalable, maintainable software systems. Your job is to translate requirements into technical architecture that development teams can implement.

**@database-designer**
- You are a database architect specialising in data modelling and schema design. Your job is to design efficient, normalised database schemas that support the application's requirements.

**@api-designer**
- You are an API architect specialising in designing clean, consistent, and developer-friendly APIs. Your job is to create API specifications that are intuitive to use and maintainable over time.

**@ui-designer**
- You are a UI/UX designer specialising in creating intuitive, accessible, and visually coherent interfaces. Your job is to design the user interface before developers build it, ensuring a consistent and user-friendly experience.

**@visual-designer**
- You are a visual designer who transforms structured design specifications into polished visual artifacts using AI-powered design tools. Your job is to take Mermaid diagrams, design tokens, wireframes, and documentation and create presentation-ready visuals.

### Development

**@functional-tester**
- You are a meticulous QA engineer. Your job is to write comprehensive functional tests.

**@python-coder**
- You are an expert Python engineer. Your job is to write clean, testable, production-grade Python code.

**@typescript-coder**
- You are an expert TypeScript engineer. Your job is to write clean, type-safe frontend and backend TypeScript code.

### Review

**@tech-lead**
- You are a tech lead responsible for ensuring code quality, architectural compliance, and engineering standards across the codebase. Your job is to review deliverables from development agents before they proceed to testing.

**@code-reviewer**
- You are a senior engineer performing detailed code review. Your job is to catch bugs, identify edge cases, and improve code quality through thorough line-by-line analysis.

### Testing

**@ui-tester**
- You are a UI quality engineer. Your job is to test user-facing behaviour in Chrome.

**@security-tester**
- You are a security engineer specialising in application security, threat modelling, and AI/LLM security.

### Deployment

**@gcp-devops**
- You are a GCP DevOps engineer. Your job is to design, configure, and validate cloud infrastructure.

### Documentation

**@documentation**
- You are a technical writer who creates clear, comprehensive documentation for developers and end users. Your job is to make the codebase accessible and understandable.

---

## Standards & Rules

### Standards (Guidance)

Located in `context/standards/`:
- **coding-standards.md** - Language patterns, frameworks, design principles
- **testing-standards.md** - TDD methodology, coverage requirements
- **tech-standards.md** - Tech stack, tools (uv), deployment
- **doc-standards.md** - Documentation structure, diagrams, writing
- **workflow-standards.md** - Processes, communication, retrospectives

### Rules (Enforced)

Located in `context/rules/` with automated validators:
- **conventional-commits.mdc** - Commit message format
- **EARS-notation-requirements.mdc** - Requirements notation
- **british-english.mdc** - Spelling conventions
- **metrics-logging.mdc** - Agent metrics format

**Pre-commit hooks** validate all rules automatically.

---

## Quality Gates

#### Review Gate
**Type**: approval
**Required**: Yes

Tech lead must approve before proceeding

#### Verification
**Type**: metrics
**Required**: Yes



**Criteria:**
- test_coverage >= 90
- critical_security_issues == 0

---

## Workflow Rules & Warnings

### Workflow Rules

- Tests written before implementation (TDD)
- Sequential review (tech-lead → code-reviewer)
- No test modifications during tdd-green phase
- All quality gates must pass

---

## Best Practices

### Agent Usage

1. **Start with the workflow** - Follow phase dependencies
2. **One task per agent** - Keep agent prompts focused
3. **Use quality gates** - Don't skip reviews for production code
4. **Let agents fail** - If tests fail, agent reports it (don't auto-fix)
5. **Check outputs** - Verify agent produced expected files

### Workflow Selection

- **Use `default.yaml`** for production code requiring quality and maintainability
- **Use `prototype.yaml`** for experiments, POCs, and throwaway code
- **Don't promote prototype code** to production without rewriting with default workflow

### Troubleshooting

**Agent can't find files:**
→ Check `{project-root}` is correctly set for your project structure

**Standards not loaded:**
→ Agent definitions list required standards in frontmatter

**Validation fails:**
→ Run `uv run pre-commit run --all-files` to see specific violations

**Tests fail but agent doesn't fix:**
→ Correct behaviour! `@functional-tester` reports failures; coders fix them

---

## Maintenance

### Updating This File

Regenerate CLAUDE.md after changes to:
- `context/workflows/*.yaml`
- `context/agents/*.md`
- `context/README.md`

```bash
uv run python context/scripts/generators/generate-claude-md.py --workflow default
```

### Adding New Agents

1. Copy `context/agents/TEMPLATE.md`
2. Fill in standards/rules in frontmatter
3. Add to appropriate workflow phase
4. Regenerate CLAUDE.md

### Switching Workflows

```bash
# Generate for prototype workflow
uv run python context/scripts/generators/generate-claude-md.py --workflow prototype
```

---

## Context Directory Structure

```
context/
├── README.md              # Complete index
├── standards/             # How to do things (guidance)
├── rules/                # What must be enforced (validators)
├── agents/               # Who does what (agent definitions)
├── workflows/            # Workflow patterns (this workflow: default)
└── scripts/              # Tools (validators, generators)
```

**Full documentation**: [context/README.md](context/README.md)

---

**Generated**: default workflow
**Agents**: 15 specialised agents
**Standards**: 5 guidance documents
**Rules**: 4 enforceable rules
