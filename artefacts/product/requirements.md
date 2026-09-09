# Example Requirements: Agentic Orchestration Harness

THIS SECTION IS POPULATED AS AN EXAMPLE. THESE ARE THE PRODUCT REQUIREMENS FOR THE AGENTIC HARNESS AND SHOULD BE REPLACED BY THE PRODUCT REQUIREMENTS FOR YOUR PROJECT.

## Overview

The Agentic Orchestration Harness is a vendor-neutral, portable framework designed to coordinate teams of specialised AI agents across heterogeneous development runtimes (Claude Code, GitHub Copilot, Codex/OpenAI, and Gemini/Antigravity). The system enforces a strict architectural separation between a portable, authoritative **Core Harness** (canonical agents, rules, standards, workflows, and templates) and **Runtime Adapters** (compilation targets projecting canonical assets into platform-specific instructions, skills, hooks, and tool schemas).

## Legend

| Symbol | Meaning |
| -------- | --------- |
| **M** | MVP (P0) - Must have for baseline cross-platform release |
| **P** | Post-MVP (P1) - Next iteration (enhanced automation and broad ecosystem) |
| **F** | Future (P2) - Backlog (autonomous adapter synthesis) |
| ✓ | Complete |
| ○ | In progress |
| · | Pending |

## Functional Requirements

### 1. Canonical Core Harness (`context/`)

The Core Harness serves as the single source of truth (SSOT) for all agent specifications, operating rules, reference standards, workflow topologies, and artefact templates.

| ID | Pri | Requirement (EARS) | Acceptance Criteria |
| ---- | ----- | ------------------- | --------------------- |
| REQ-COR-001 | M | THE core-harness SHALL maintain all authoritative agent definitions, rules, standards, and workflow topologies in a versioned `context/` directory. | Core definitions exist in git, formatted as Markdown with YAML frontmatter (`agents/`), MDC (`rules/`), Markdown (`standards/`), and YAML (`workflows/`). |
| REQ-COR-002 | M | THE core-harness SHALL isolate concise, binary rules (`context/rules/*.mdc`) from detailed reference standards (`context/standards/*.md`). | Rules are independently injectable (<200 tokens each) with binary compliance criteria; standards contain rationale and in-depth guidance. |
| REQ-COR-003 | M | WHEN an agent is spawned, THE core-harness SHALL dynamically resolve and inject only applicable rules by glob-matching the task file scope against rule headers. | Unrelated rules are excluded from agent context, keeping framework injection overhead under 2,500 tokens per spawn. |
| REQ-COR-004 | M | THE core-harness SHALL define multi-phase execution DAGs with strict dependencies and quality gates in declarative YAML files (`context/workflows/*.yaml`). | Workflows support phase chaining, dependencies, agent assignments, outputs, and review gate validation criteria. |
| REQ-COR-005 | M | THE core-harness SHALL enforce orchestrator governance where only the orchestrator commits to version control. | Specialised child agents produce code and artefacts within assigned file scopes but SHALL NOT execute git commits directly. |
| REQ-COR-006 | M | WHILE executing a workflow, THE core-harness SHALL persist all execution state, task lists, and handoffs directly to disk in `artefacts/`. | Session state is fully recoverable from disk artefacts after context compaction without relying on conversational history. |
| REQ-COR-007 | M | THE core-harness SHALL provide standardised artefact templates (`context/templates/`) for all system deliverables. | Handoffs, requirements, architectures, task lists, and reviews conform to uniform templates across all runtimes. |
| REQ-COR-008 | P | WHEN workflow definitions are modified, THE core-harness SHALL validate the dependency graph for circular dependencies and unmapped agents. | Static validation script halts execution if an invalid agent or phase dependency is referenced. |

### 2. Runtime Adapters Architecture

Runtime Adapters compile or project the canonical core harness into target platforms, preserving vendor neutrality without sacrificing platform-specific capabilities.

| ID | Pri | Requirement (EARS) | Acceptance Criteria |
| ---- | ----- | ------------------- | --------------------- |
| REQ-ADP-001 | M | THE adapter-system SHALL generate derived runtime configuration files from canonical assets without requiring manual edits in target files. | Derived files (`AGENTS.md`, `CLAUDE.md`, Copilot instructions) include auto-generation headers and warning notices against direct edits. |
| REQ-ADP-002 | M | WHEN canonical assets in `context/` are updated, THE adapter-system SHALL regenerate all target runtime configuration files deterministically. | Running generator scripts updates all target configs to reflect current rules, agents, and workflows. |
| REQ-ADP-003 | M | IF a generated runtime configuration drifts from the canonical source, THE adapter-system SHALL fail verification during pre-commit and CI validation. | Drift detector reports desynchronised files and halts commit until regenerated. |
| REQ-ADP-004 | M | THE adapter-system SHALL map abstract canonical tool capabilities to runtime-specific tool implementations. | Canonical requests for file operations map to `Write`/`Edit` in Claude, `replace_file_content`/`write_to_file` in Gemini, and JSON function calling in Codex. |

### 3. Runtime Adapter Implementations

| ID | Pri | Requirement (EARS) | Acceptance Criteria |
| ---- | ----- | ------------------- | --------------------- |
| REQ-PLT-001 | M | THE claude-adapter SHALL project canonical workflows and agent registries into `CLAUDE.md` and `AGENTS.md` optimised for Claude Code CLI and subagent Task tool invocations. | Generates valid `CLAUDE.md`/`AGENTS.md` with phase transitions, agent spawn templates, and token telemetry hook bindings. |
| REQ-PLT-002 | M | THE gemini-adapter SHALL project canonical agents, rules, and workflows into Google Antigravity-compatible skills (`.agents/skills/`), `GEMINI.md`, and MCP configurations. | Generates structured Antigravity skill folders with `SKILL.md` frontmatter and maps large-context standard ingestion. |
| REQ-PLT-003 | P | THE github-adapter SHALL project canonical instructions into `.github/copilot-instructions.md`, custom prompts (`.github/prompts/`), and workspace rule configurations. | Produces valid GitHub Copilot workspace instructions and prompt files aligned with canonical rules and EARS notation. |
| REQ-PLT-004 | P | THE codex-adapter SHALL project canonical agent definitions and workflows into OpenAI-compatible system prompts and JSON schema tool definitions. | Generates structured prompt bundles and tool declarations compatible with OpenAI Assistants API and execution harnesses. |
| REQ-PLT-005 | M | THE claude-adapter SHALL inject session token telemetry into git commit trailers via a prepare-commit-msg hook. | Every commit created by the orchestrator records Agent-Session, model, and token metrics. |
| REQ-PLT-006 | P | THE adapter-system SHALL adapt context delivery depth based on runtime context window capacities. | Runtimes with >1M context (Gemini) receive preloaded reference standards; runtimes with compact budgets (Claude/Codex) receive on-demand reference links. |

### 4. Workflow Orchestration & Coordination Patterns

| ID | Pri | Requirement (EARS) | Acceptance Criteria |
| ---- | ----- | ------------------- | --------------------- |
| REQ-WF-001 | M | THE orchestration-engine SHALL enforce Test-Driven Development (TDD) as three non-combinable, sequential phases: RED, GREEN, and BLUE. | The orchestrator prohibits combining RED test authoring with GREEN implementation or BLUE refactoring within the same agent spawn. |
| REQ-WF-002 | M | WHEN spawning multiple agents in a parallel hive phase, THE orchestrator SHALL assign disjoint file scopes to each agent. | No two concurrent agents are permitted write access to overlapping file paths, preventing merge collisions. |
| REQ-WF-003 | M | WHEN proposing parallel agent execution, THE orchestrator SHALL present token cost, time, and coordination risk trade-offs to the human operator. | User is presented with explicit Sequential vs Parallel execution options prior to dispatching multi-agent tasks. |
| REQ-WF-004 | M | WHILE a quality gate is unapproved, THE orchestration-engine SHALL prevent progression to downstream workflow phases. | Quality reviewers (tech-lead, code-reviewer, security-tester) must record formal approval in `artefacts/build/` before subsequent phases unlock. |
| REQ-WF-005 | P | IF an agent encounters unresolvable ambiguity or rule conflict, THE agent SHALL halt and record an escalation issue in `artefacts/product/open-questions.md`. | Agents avoid ungrounded assumptions by formally pausing execution and raising blocking questions to the human operator. |

### 5. Verification, Quality Gates & Continuous Improvement

| ID | Pri | Requirement (EARS) | Acceptance Criteria |
| ---- | ----- | ------------------- | --------------------- |
| REQ-VER-001 | M | THE verification-system SHALL validate all requirements files (`**/requirements.md`) for strict EARS syntax adherence via pre-commit hooks. | `ears_notation.py` executes on staged requirements and blocks non-compliant commits. |
| REQ-VER-002 | M | THE verification-system SHALL validate documentation and commit messages for British English spelling and formatting conventions. | `british_spelling.py` verifies standard spelling (`colour`, `behaviour`, `artefacts`, `licence`) across markdown and code. |
| REQ-VER-003 | M | THE continuous-improvement-engine SHALL support reactive incident diagnosis and proactive retrospective analysis of framework performance. | Causal incident logs (`artefacts/build/agent-incidents.md`) trace failures to specific missing rules, ambiguous standards, or template defects. |
| REQ-VER-004 | P | THE verification-system SHALL require visual regression and screenshot evidence in `artefacts/test-results/` for all UI modifications. | UI testing workflows fail quality review if automated browser screenshots are missing from test results. |

## Non-Functional Requirements

| ID | Category | Requirement | Target |
| ---- | ---------- | ------------- | -------- |
| NFR-001 | Token Efficiency | Overhead of framework rules and agent frontmatter injected into a single agent spawn prompt | < 2,500 tokens |
| NFR-002 | Portability | Canonical core files (`context/agents/`, `rules/`, `standards/`, `workflows/`) containing zero vendor-specific tool names or proprietary prompt syntax | 100% vendor-agnostic |
| NFR-003 | Generation Speed | Execution time to regenerate all runtime adapter projections from canonical sources | < 2.0 seconds |
| NFR-004 | Determinism | Repeated runs of adapter generators on unchanged canonical files produce identical byte-for-byte outputs | 100% reproducible |
| NFR-005 | Recoverability | Time required for an orchestrator to resume workflow execution from disk artefacts following a context compaction event | < 1 turn / 10 seconds |
| NFR-006 | Security & Safety | Prevention of credentials or API secrets committing to git or leaking into agent prompt payloads | Zero committed secrets; strict rule enforcement |

## Out of Scope

- Implementing end-user domain application features (the harness is strictly an agent coordination and governance engine).
- Autonomous unconstrained swarm exploration without orchestrator oversight (the framework implements centralised Hive and Chain patterns).
- Graphical drag-and-drop workflow visualizer editor (workflows are authored and reviewed directly as YAML code).
- Hosting proprietary model endpoints or custom LLM weights (the harness coordinates external runtimes via their native interfaces).

## Revision History

| Date | Author | Changes |
|------|--------|---------|
| 09/09/2026 | Product Owner (@product-owner) | Initial product requirements specification for Core Harness and Framework Adapters |
