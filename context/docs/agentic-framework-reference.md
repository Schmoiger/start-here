# Agentic Framework Reference

**Status**: Second pass
**Date**: 2026-04-13
**Audience**: New contributors who need a deeper map after reading `context/docs/agentic-framework.md`

---

## How To Use This Reference

Read `context/docs/agentic-framework.md` first for the system view. Use this document when you need to answer a narrower question such as:

- "What is this directory for?"
- "Why does this asset exist?"
- "Which file should I change?"
- "How do the framework parts relate to each other?"

This is a reference map, not a replacement for the source files.

---

## Framework Topology

| Area | Purpose | Main Consumer |
|------|---------|---------------|
| `context/standards/` | Explanatory guidance and engineering rationale | Humans and agents needing reference context |
| `context/rules/` | Short non-negotiable operational rules | Agents and validators |
| `context/agents/` | Specialised worker definitions | Orchestrator and agent runtimes |
| `context/workflows/` | Phase sequencing, outputs, validation, recovery | Orchestrator |
| `context/docs/` | Operator guides for using and adapting the framework | Humans |
| `context/templates/` | Standard artefact shapes | Orchestrator and producing agents |
| `context/persona/` | Voice guidance for human-facing content | Documentation and content agents |
| `context/scripts/` | Automation, generation, and validation | Repo tooling |

The top-level design pattern is consistent throughout the framework:

- **define** the role or rule
- **explain** how to use it
- **standardise** the output
- **validate** the result

---

## Root-Level Framework Files

### `AGENTS.md`

Auto-generated registry of workflows and agents. It acts as the root-level quick-start for agent runtimes and humans. Design rationale: derived documentation lowers onboarding cost, but generation avoids hand-maintained drift.

### `CLAUDE.md`

Root agent guidance surfaced to the runtime. In this repo it points to `AGENTS.md`, making the generated registry the durable entry point instead of duplicating framework detail in multiple places.

### `README.md`

Repository-level onboarding and setup document. It complements `context/README.md`: the root README explains the repo; `context/README.md` explains the framework.

Design note: this split keeps newcomer setup instructions close to the repository root whilst leaving framework theory in the portable context package.

---

## Authoritative And Derived Files

The framework intentionally mixes source files, generated projections, and operator guides. New contributors should treat them differently.

| Type | Examples | Role |
|------|----------|------|
| **Authoritative source** | `context/agents/*.md`, `context/workflows/*.yaml`, `context/rules/*.mdc`, `context/standards/*.md`, `context/templates/*.md`, `context/persona/*.md` | These define how the framework behaves |
| **Derived projection** | `AGENTS.md`, `CLAUDE.md` | These surface framework information in runtime-friendly form |
| **Human operator guidance** | `context/docs/*.md`, `README.md`, these design docs | These explain how to use, extend, or evaluate the framework |
| **Automation and enforcement** | `context/scripts/**` | These keep the repository aligned with the design |

Design rationale:

- contributors need quick entry points, but generated entry points should not become the hidden source of truth
- changes should happen in one place and propagate outward
- review is easier when source-of-truth files are obvious

---

## `context/README.md`

This file is the canonical orientation page for the framework. It defines directory purposes, gives quick references for agents and humans, and explains the DRY split between rules and standards.

Design rationale:

- one obvious entry point lowers navigation friction
- both humans and agents can use it
- it teaches the storage model before contributors start creating artefacts in the wrong place

---

## `context/standards/`

Standards are detailed reference material. They are intentionally longer and more explanatory than rules.

### `README.md`

Index for the standards set. Exists so contributors can discover the right document without opening everything.

### `12-factor-principles.md`

Maps framework or service work onto twelve-factor application principles. Exists to anchor deployment-facing design in well-known operational guidance.

### `LESS-Engineering-Principles.md`

Captures the LESS principles used by review agents and design discussions. Exists so abstraction and architecture decisions have a shared reference point.

### `agent-standards.md`

Defines expectations for how agents should behave, recover state, use tools, and coordinate. This is one of the framework's core documents because it describes the behavioural contract around the agents, not just their roles.

### `build-standards.md`

Explains how build-phase work should be structured and assessed. Exists to support the main development loop with more detail than workflow YAML alone can carry.

### `coding-standards.md`

Language and implementation guidance for code quality. Exists so coding agents and reviewers have a stable quality reference that does not need to be repeated in each task.

### `context-framework.md`

Defines the framework's theory of context: reference vs actionable context, priority, handoff format, terse formats, and context quality. This is a foundational design text because it expresses the repo's core belief that context is itself a deliverable.

### `doc-standards.md`

Documentation structure, quality, archival, diagram, and maintenance guidance. Exists so docs are treated as part of the system, not as ad hoc prose.

### `security-standards.md`

Security guidance for design, implementation, and review. Exists so security is not only represented by a single review phase but also by shared design expectations.

### `tech-mobile-standards.md`

Mobile-specific technical guidance. Exists to keep mobile guidance separate from general stack guidance rather than bloating the main technology standard.

### `tech-standards.md`

Primary technology stack reference. This is the broad operational handbook for the stack and tooling choices expected across the repo.

### `testing-standards.md`

Testing philosophy and practice, including TDD expectations. Exists because testing is central to the framework and needs a richer explanation than terse workflow rules can provide.

### `visual-standards.md`

Guidance for design consistency, UI quality, and visual review concerns. Exists so visual work has a defined quality bar rather than being treated as subjective taste.

### `workflow-standards.md`

Shared workflow conventions, invocation practices, and orchestration rules. Exists to describe the operating model that spans multiple concrete workflow YAML files.

Design rationale for the standards directory:

- keep long-form rationale out of hot execution paths
- preserve nuanced thinking without inflating every task prompt
- give humans a place to understand "why" and not only "what"

---

## `context/rules/`

Rules are short, enforceable constraints. They are designed for injection into agent prompts and for validator-backed enforcement.

### Environment And Tooling

| File | Purpose |
|------|---------|
| `bash-environment.mdc` | Prevents unsafe or inconsistent bash usage and pushes work toward the approved tool model |
| `mermaid-environment.mdc` | Constrains Mermaid diagram syntax, layout direction, and node label conventions |
| `python-environment.mdc` | Enforces Python environment and command conventions such as `uv` usage |
| `typescript-environment.mdc` | Enforces TypeScript environment and package manager conventions |
| `supabase.mdc` | Defines constraints around Supabase-related usage where relevant |

### Quality And Process

| File | Purpose |
|------|---------|
| `tdd-workflow.mdc` | Enforces RED -> GREEN -> BLUE discipline |
| `quality-gates.mdc` | Encodes non-negotiable review and release criteria |
| `output-locations.mdc` | Keeps artefacts in the correct directories |
| `handoff-hygiene.mdc` | Enforces durable, useful handoffs |
| `escalation.mdc` | Defines when agents may assume, flag, or escalate |
| `git-commits.mdc` | Standardises commit structure and agent session metadata |
| `metrics-logging.mdc` | Constrains how workflow and performance signals are recorded |
| `no-ai-slop.mdc` | Eliminates AI-generated writing tics from persona-driven documentation |

### Architecture, Design, And Safety

| File | Purpose |
|------|---------|
| `architecture-fidelity.mdc` | Prevents implementation drift from approved architecture |
| `visual-fidelity.mdc` | Prevents drift from approved UI and visual design |
| `ui-component-reuse.mdc` | Encourages reuse and discourages needless UI duplication |
| `type-safety.mdc` | Protects typed contracts and discourages unsafe shortcuts |
| `browser-automation.mdc` | Constrains browser-based test and automation behaviour |
| `secrets-management.mdc` | Prevents unsafe handling of secrets and credentials |

### Language And Requirements Hygiene

| File | Purpose |
|------|---------|
| `british-english.mdc` | Enforces consistent spelling in framework outputs |
| `EARS-notation-requirements.mdc` | Enforces the chosen requirements notation |

Design rationale for the rules directory:

- rules must be brief enough to inject repeatedly
- each rule should correspond to a real failure mode
- binary rules are easier to automate and review than vague preferences

---

## `context/agents/`

Agent definitions are markdown files with frontmatter and an instruction body. They are the role catalogue of the framework.

### Core Coordinator

| File | Purpose |
|------|---------|
| `orchestrator.md` | Coordinates the system, resolves rules, assigns file scope, validates phase outputs, and manages quality gates |

### Product And Discovery

| File | Purpose |
|------|---------|
| `product-expert.md` | Elicits problem understanding and discovery insight from the user |
| `product-owner.md` | Turns clarified needs into structured requirements and stories |

### Design

| File | Purpose |
|------|---------|
| `solution-architect.md` | Designs architecture, boundaries, and data flow |
| `database-designer.md` | Designs schemas, relationships, and migrations |
| `api-designer.md` | Designs APIs and contract artefacts |
| `ui-designer.md` | Designs UI structure, component behaviour, and user flow |
| `visual-designer.md` | Produces visuals, mockups, and visual review input |

### Implementation And Test

| File | Purpose |
|------|---------|
| `python-coder.md` | Implements Python production work |
| `typescript-coder.md` | Implements TypeScript and frontend work |
| `functional-tester.md` | Writes and runs tests in the TDD flow |
| `ui-tester.md` | Executes browser-based UI verification |

### Review And Governance

| File | Purpose |
|------|---------|
| `tech-lead.md` | Acts as the principal architecture and quality gate reviewer |
| `code-reviewer.md` | Performs implementation-focused review for bugs, risks, and maintainability |
| `principles-reviewer.md` | Reviews designs and code against higher-level engineering principles |
| `security-tester.md` | Reviews for vulnerabilities and security risks |

### Operations And Maintenance

| File | Purpose |
|------|---------|
| `devops.md` | Handles deployment and infrastructure-related work |
| `documentation.md` | Cleans up, archives, and maintains human-facing documentation |
| `workflow-analyst.md` | Reviews process effectiveness and supports retrospectives |

### Supporting Files

| File | Purpose |
|------|---------|
| `README.md` | Human-readable inventory of the agent catalogue |
| `cursor-workflow-helper.mdc` | Cursor-specific helper guidance colocated with agent definitions |

Design rationale for the agents directory:

- keep prompts role-scoped instead of building one massive general prompt
- attach model choice, rules, and standards directly to each role
- make role boundaries visible so the workflow can express handoffs clearly

---

## `context/workflows/`

Workflow YAML files are operational blueprints. They define phases, dependencies, skills, outputs, validation, quality gates, state recovery, and workflow rules.

### `build.yaml`

Primary implementation workflow. It covers planning, TDD execution, review, regression, documentation cleanup, and final holistic review. Design rationale: make the main delivery path explicit and strongly gated.

### `design.yaml`

Discovery and design workflow that runs before implementation. Design rationale: treat design as a formal phase with review rather than informal pre-work.

### `prototype.yaml`

Fast path for proof-of-concept work. Design rationale: allow speed when appropriate, but keep the distinction from production-quality work explicit.

### `deploy.yaml`

Deployment-focused workflow. Design rationale: deployment is operationally distinct enough to deserve its own sequence and checks.

### `bugfix.yaml`

Workflow for reproducing, diagnosing, fixing, and verifying defects. Design rationale: bug work has a different evidence pattern from feature work and benefits from its own discipline.

### `full-test.yaml`

Full regression and verification workflow. Design rationale: separate targeted changed-scope testing from broader release-confidence testing.

### `content.yaml`

Workflow for human-facing written content. Design rationale: content work has different outputs and style requirements from code work.

### `continuous-improvement.yaml`

Workflow for retrospective framework improvement and incident response. Design rationale: the framework itself should evolve through a repeatable process, not occasional intuition.

### `retrospective.yaml`

Workflow for retrospective analysis. Design rationale: process review is important enough to be modelled directly rather than folded into an informal meeting.

Design rationale for workflow YAML in general:

- phase logic becomes inspectable and versioned
- validation criteria become durable
- recovery after interruption is possible because workflow state is externalised

---

## `context/docs/`

These documents explain how to operate, adapt, and evaluate the framework.

| File | Purpose |
|------|---------|
| `framework-adapters.md` | Explains how the markdown agent format maps to other orchestration systems such as LangGraph, CrewAI, AutoGen, Cursor, Aider, Continue, and Windsurf |
| `how-to-measure-agent-effectiveness.md` | Explains how to assess agent performance and workflow outcomes |
| `orchestration-patterns.md` | Defines coordination patterns such as single agent, chain, swarm, hive, and iterative loop |
| `workflow-agent-effectiveness.md` | Guide focused on evaluating workflow quality and agent contribution |
| `workflow-default.md` | Usage guide for the default or primary workflow |
| `workflow-documentation-for-humans.md` | Guide for documentation or content-oriented workflow usage |
| `workflow-prototype.md` | Usage guide for the prototype workflow |
| `writing-personas.md` | Explains when and how writing personas should be used |

Design rationale:

- keep framework operation guidance outside the workflow YAML
- separate "what the workflow is" from "how a human should run it"
- make portability and evaluation explicit parts of the framework

---

## `context/templates/`

Templates define standard output shapes so artefacts are predictable.

| File | Purpose |
|------|---------|
| `README.md` | Index of available templates |
| `agent-template.md` | Starting point for creating a new specialised agent |
| `architecture-template.md` | Standard structure for system architecture documents |
| `bugs-template.md` | Standard bug tracker format |
| `commit-message-template.md` | Standard commit message structure |
| `design-template.md` | Standard design document for complex features or screens |
| `domain-rules-template.yaml` | Template for domain-specific constraints |
| `handoff-template.md` | Standard agent handoff format |
| `pr-description-template.md` | Standard pull request description format |
| `requirements-template.md` | Standard requirements structure |
| `review-template.md` | Standard review finding format |
| `task-prompt-template.md` | Orchestrator prompt scaffold for spawning agents correctly |
| `tasks-template.md` | Standard task tracking format |
| `test-dashboard-template.md` | Standard structure for test dashboards |
| `user-stories-template.md` | Standard user story format |

Design rationale:

- standard shapes reduce ambiguity for both writers and readers
- predictable outputs make automation and follow-on agent work easier
- the task prompt template is especially important because it carries rule resolution and file-scope discipline into subagent execution

---

## `context/persona/`

Personas are for human-facing writing only.

| File | Purpose |
|------|---------|
| `editor.md` | Editorial voice and polish guidance |
| `expert-reviewer.md` | Review-oriented writing persona |
| `technical-writer.md` | Practitioner cookbook voice for guides and reference prose |
| `opinionated-blogger.md` | Conversational voice for blog posts and opinion pieces |

Design rationale:

- content tone is a separate concern from technical correctness
- personas are isolated so implementation agents do not inherit unnecessary style baggage
- colocation under `context/` keeps all framework assets in one portable directory

---

## `context/scripts/`

Scripts are the automation layer of the framework.

### Generators And Validators (Top-Level)

| File | Purpose |
|------|---------|
| `generators/generate_agents_md.py` | Generates the derived `AGENTS.md` registry from framework assets |
| `validate_agent_definitions.py` | Validates agent definition integrity: frontmatter, required sections, path conventions |

Design rationale: generation is used where duplication would otherwise drift. Top-level validation scripts complement the per-rule validators below.

### Validators

| File | Purpose |
|------|---------|
| `validators/README.md` | Explains the validator subsystem |
| `validators/british_english.py` | Enforces spelling conventions |
| `validators/conventional_commits.py` | Enforces commit message shape |
| `validators/design_system.py` | Checks design-system-related conventions |
| `validators/ears_notation.py` | Validates EARS requirements notation |
| `validators/metrics_logging.py` | Validates workflow or session metrics logging |
| `validators/supabase_boundary.py` | Checks Supabase boundary constraints |

Design rationale: validators convert framework expectations into repeatable checks.

### Hook And Coordination Utilities

| File | Purpose |
|------|---------|
| `prepare-commit-msg.py` | Injects or prepares agent-session metadata during commit creation |
| `prepare-commit-msg.sh` | Shell wrapper for the commit hook |
| `coordinate.sh` | Convenience utility for framework coordination tasks |
| `pre-commit-config-template.yaml` | Template for pre-commit integration |

Design rationale: hooks make telemetry and hygiene automatic instead of optional.

### Tests And Fixtures

| File | Purpose |
|------|---------|
| `tests/README.md` | Documents the test suite and how to run it |
| `tests/test_agent_validator.py` | Tests the agent-definition validation behaviour |
| `tests/test_generator.py` | Tests generated output logic |
| `tests/test_validators.py` | Tests the validators |
| `tests/conftest.py` | Shared test setup |
| `tests/fixtures/*` | Positive and negative examples used to prove validators and generators work correctly |

Design rationale: if the framework relies on automation, that automation should itself be tested.

---

## Relationships Between Major Elements

### Agents Read Rules And Standards

Agent files point to the rules and standards they depend on. This keeps prompts small and composable.

### Workflows Sequence Agents

Workflow YAML does not replace agent definitions; it arranges them. The design separates role definition from phase sequencing.

### Templates Shape Outputs

Templates are chosen by the orchestrator and used by producing agents. This makes output conventions an explicit part of orchestration rather than an afterthought.

### Scripts Enforce The Model

Without validators, generators, and hooks, the framework would rely too much on memory and goodwill. The scripts directory is what turns the framework from a collection of ideas into an operating system.

### Adapters Extend Portability

`context/docs/framework-adapters.md` explains how the same framework can travel across runtimes by mapping the markdown agent format to other orchestration systems.

---

## Design Themes That Repeat Across The Framework

### Explicitness Over Convention

Phases, gates, file locations, role boundaries, and recovery steps are written down instead of implied.

### Durability Over Chat Memory

The framework assumes interruptions and context loss will happen, so it records state in artefacts and workflow files.

### Reuse Over Reinvention

Templates, standard agent definitions, and generated registries are all attempts to make the next task cheaper and more predictable than the last.

### Portability Over Tool Lock-In

The framework is designed to survive changes in agent runtime or orchestration platform.

### Verification Over Trust

Reviewers, validators, tests, screenshots, gates, and telemetry all reinforce the same idea: outputs should be evidenced, not merely claimed.

---

## Suggested Reading Paths

### If You Want To Extend The Framework

1. `context/README.md`
2. `context/agents/orchestrator.md`
3. `context/workflows/design.yaml` and `context/workflows/build.yaml`
4. `context/templates/task-prompt-template.md`
5. relevant rules and standards

### If You Want To Add A New Agent

1. `context/agents/README.md`
2. `context/templates/agent-template.md`
3. `context/agents/orchestrator.md`
4. the workflow where the new agent should appear

### If You Want To Port The Framework Elsewhere

1. `README.md`
2. `context/README.md`
3. `context/docs/framework-adapters.md`
4. `AGENTS.md`

### If You Want To Understand Quality Enforcement

1. `context/rules/`
2. `context/workflows/`
3. `context/scripts/validators/`
4. `context/standards/testing-standards.md`
5. `context/standards/doc-standards.md`

---

## Notes

This reference maps the current framework structure and intent based on the existing docs. A later pass could go even deeper by:

- tracing each workflow to the exact standards and rules it relies on
- documenting generator and validator inputs and outputs in more detail
- adding a dependency diagram showing which files are authoritative versus derived
