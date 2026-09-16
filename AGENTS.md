# AGENTS.md

---

## System Instructions
Always follow the specific instructions in the `context/` directory.

---

## Standards
INLINE_COMPREHENSIVE

---

## Tool Mappings
- Use `replace_file_content` for editing contiguous blocks of code.
- Use `run_command` for executing terminal commands.
- Use `call_mcp_tool` for MCP interactions.

---

## On Start
Glob `**/artefacts/README.md` and read all matches. Run `git log --oneline -5`.
Read `@context/agents/orchestrator.md`.
Read `artefacts/build/HANDOFF.md` if it exists — the `Workflow:` field identifies the active workflow.
Load `@context/workflows/<workflow>.yaml`. If no HANDOFF.md exists, ask the user which workflow to start.

---

## Workflows

| Workflow | Purpose |
|----------|---------|
| `bugfix` | Empirical bug reproduction, fix, and verification — with a commit as the record |
| `build` | Subtask planning through local deployment — primary development loop |
| `content` | Human-facing content creation with writing personas |
| `continuous-improvement` | Framework improvement — reactive or proactive |
| `deploy` | GCP cloud deployment and deployment review — run after build workflow local-deployment |
| `design` | Discovery through design review — run before build workflow |
| `full-test` | Full-suite testing across all modules — run before merge to master or on demand |
| `prototype` | Fast iteration workflow for prototyping and experimentation |
| `retrospective` | Proactive framework review — analyse accumulated data, suggest improvements, fix and record |

---

## Agents

| Agent | Purpose |
|-------|---------|
| `@product-owner` | Transforms vague user requests into structured requirements and user stories |
| `@product-expert` | Helps elucidate vague ideas into clearer requirements through conversation |
| `@solution-architect` | Designs system architecture, component boundaries, and data flow |
| `@database-designer` | Designs database schemas, relationships, and migrations |
| `@api-designer` | Designs RESTful and GraphQL APIs with OpenAPI specifications |
| `@ui-designer` | Designs user interfaces, component layouts, design systems, and visual assets |
| `@functional-tester` | Writes and runs tests for Python and TypeScript code using Detroit-school TDD |
| `@python-coder` | Writes production Python code with testing in mind |
| `@typescript-coder` | Builds frontend or backend TypeScript, integrating with Python APIs |
| `@tech-lead` | Reviews code for architecture compliance, consistency, and engineering standards |
| `@code-reviewer` | Performs detailed PR-style code review focusing on bugs, edge cases, and maintainability |
| `@principles-reviewer` | Reviews designs and implementations against LESS Engineering Principles |
| `@ui-tester` | Tests UI behaviour using Chrome DevTools and browser automation |
| `@security-tester` | Identifies security vulnerabilities using threat modelling and code analysis |
| `@devops` | Deploys and validates infrastructure |
| `@documentation` | Generates user-facing documentation, API references, and guides |
| `@workflow-analyst` | Analyzes workflow efficiency by examining handoffs, tasks, git history, token usage, and standards adherence |
| `@tokenomics-analyst` | Audits agent effectiveness, token economics, context efficiency, and model tiering across workflows and runtimes |
| `@orchestrator` | Coordinates workflow execution, delegates implementation to specialised agents, and manages quality gates |

---

## Skills

| Skill | Purpose | Globs / Triggers |
|-------|---------|------------------|
| `agent-sandbox` | Procedural guidance and rationale for executing terminal commands within agent sandboxes, avoiding common heuristics that trigger security blocks | _None_ |
| `agent-workflows` | Procedural guidance for agent git commits, pull requests, and metrics logging | _None_ |
| `architecture-fidelity` | Procedural guidance for adhering to architecture docs and API contracts during implementation | `**/*.py`, `**/*.ts`, `**/*.tsx` |
| `bootstrap-workflow` | Procedural workflow for bootstrapping a new project or feature context | _None_ |
| `git-subrepo-operations` | Procedural guidance and constraints for managing canonical context using git-subrepo | `**/.gitrepo`, `context/**`, `typst/**` |
| `intent-fidelity` | Procedural guidance for ensuring business and functional intent is clearly captured in requirements, tasks, and reflected faithfully in TDD and testing | `**/requirements.md`, `**/tasks.md`, `**/user-stories.md` |
| `mermaid-authoring` | Mermaid diagram syntax, layout constraints, and semantic guidance | `**/*.md` |
| `multi-agent-workflows` | Procedural guidance for orchestrator triage and handoff archival | `**/*` |
| `python-scripting` | Procedural guidance and craft for authoring, running, and testing Python scripts with uv, PEP 723 inline metadata, and the --with pattern | `**/*.py`, `**/pyproject.toml`, `context/scripts/**/*`, `scripts/**/*` |
| `supabase-operations` | Procedural guidance for Supabase migrations, queries, and maintenance via MCP | `**/migrations/*.sql`, `**/supabase/**`, `**/database_service/**`, `**/stores/**` |
| `tdd-workflow` | Strict Detroit-School Test-Driven Development procedural guide | `**/tests/**`, `**/*.test.py`, `**/*.test.ts` |
| `technical-authoring` | Procedural guidance and craft for authoring and editing technical whitepapers, architecture roadmaps, and book chapters using the Amara Osei persona | `docs/drafts/**/*.md`, `docs/books/**/*.md`, `artefacts/content/**/*.md` |
| `typescript-development` | Procedural guidance for setting up and working with TypeScript/JavaScript projects using Yarn Berry workspaces | `**/*.ts`, `**/*.tsx`, `**/*.js`, `**/*.jsx`, `**/package.json` |
| `typst-pipeline` | Procedural guidance for authoring, building, and publishing PDFs using the project's Typst/Pandoc typesetting engine | `docs/drafts/**/*.md`, `build.yaml`, `typst/**` |
| `ui-development` | Procedural guidance for authoring UI components and layouts | `**/*.tsx`, `**/*.jsx` |
| `ui-testing` | Procedural guidance for UI testing and browser automation | `**/*.test.ts`, `**/*.spec.ts` |

**Spawn**: `"Read @context/agents/{name}.md before starting. [task]"`

_Auto-generated by context/scripts/generators/generate_adapters.py — do not edit manually_
