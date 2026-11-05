# Product Specification: Agentic Orchestration Harness (Derived)

<!--
Mode: product (mode=both run)
Target: . (repo root)
Index provenance: repo-index.json (2026-11-05T13:24:38Z; extractors: stdlib.ast, ast-grep)
Baseline docs: discovered — requirements.md (example), architecture.md (example), data-model.md, api-catalogue.md, openapi.yaml, user-stories.md, open-questions.md
Output location: artefacts/build/spec-drafts/product-spec.md
-->

**Run metadata**

| Field | Value |
|-------|-------|
| Mode | both (product + technical) |
| Target | . (repo root) |
| Index provenance | `repo-index.json` (2026-11-05T13:24:38Z; extractors: stdlib.ast, ast-grep) |
| Baseline docs | requirements.md (example), architecture.md (example), data-model.md, api-catalogue.md, openapi.yaml, user-stories.md, open-questions.md |
| Output location | `artefacts/build/derived/product-spec.md` |

---

## Confidence Schema

| Band | % | Evidence required to claim it |
|------|---|-------------------------------|
| **Verified** | 85-100 | directly cited code or doc lines (`path:line`); usage counts or call chains where material; no blocking open question |
| **Needs Confirmation** | 50-85 | plausible from evidence but requires human confirmation; drift candidates land here first |
| **Assumed** | <50 | reasonable inference only; stays Assumed until a human answer confirms it |

**Update rule**: a confirmed answer raises the band and percentage and records the confirming citation; an unanswered question keeps the subsection Assumed and its question stays in the Open-Questions appendix as still-open.

**Promotion DoD**: a draft is promotable when no subsection sits below Needs Confirmation and no blocking question is still open, or when the human records an explicit override.

---

## Subsection Format
### Actors and Roles

**Confidence**: Verified · 90% · Evidence: `context/scripts/code-specs/spec_indexer.py:2092`, `context/agents/*.md` (34 agent definitions indexed), `context/workflows/*.yaml` (11 workflows)

The harness defines **34 specialised agents** across **11 workflow YAMLs** (build, bugfix, content, continuous-improvement, deploy, design, derive-spec, full-test, prototype, small-task). Agent frontmatter specifies `model: large/medium/small`, `skills:`, and `rules:` lists. The `@orchestrator` is the central coordinator; it delegates implementation to sub-agents (`@python-coder`, `@functional-tester`, `@tech-lead`, `@code-reviewer`, `@principles-reviewer`, `@ui-tester`, `@security-tester`, `@devops`, `@documentation`, `@harness-analyst`, `@solution-architect`, `@product-owner`, `@ui-designer`, `@typescript-coder`, `@orchestrator`) but **never implements directly** except in `small-task` workflow (which lifts this boundary per `context/workflows/small-task.yaml:128`). 

**Key roles**:
- **Orchestrator**: coordinates, delegates, manages quality gates, commits on behalf of sub-agents
- **Product Owner**: elicits/structures requirements; Mode 3 derives product spec from code (derive-spec)
- **Solution Architect**: designs architecture; Mode 3 derives technical spec from code (derive-spec)
- **Python Coder**: writes production Python with testing in mind
- **Functional Tester**: Detroit-school TDD for Python/TypeScript
- **Tech Lead**: architecture compliance, consistency, engineering standards review
- **Code Reviewer**: PR-style review for bugs, edge cases, maintainability
- **Principles Reviewer**: reviews against LESS Engineering Principles
- **Security Tester**: threat modelling, code analysis
- **UI Tester**: browser automation, Chrome DevTools
- **DevOps**: physical data layer, deployment targets
- **Documentation**: user-facing docs, API references, guides
- **Harness Analyst**: agent effectiveness, token economics, model-tier conformance

---

### Features and Capabilities

**Confidence**: Verified · 90% · Evidence: `context/scripts/code-specs/spec_indexer.py:437-2092`, `context/scripts/generators/generate_adapters.py:428`, `context/workflows/*.yaml` (11 workflows), `context/scripts/validators/*.py` (11 validators)

| Feature | Description | Evidence |
|---------|-------------|----------|
| **Spec Indexer (scan/verify)** | Deterministic, zero-LLM indexer extracting Python symbols (731), config (8 keys), tests (245), docs (25); `scan --repo --mode`, `verify --index/--doc` | `context/scripts/code-specs/spec_indexer.py:437` (analyze_python), `context/scripts/code-specs/spec_indexer.py:2015` (main CLI) |
| **Adapter Generators** | Compile canonical `context/` assets into runtime-specific instructions for Claude Code, Cline, Gemini, GitHub Copilot, OpenAI Codex | `context/scripts/generators/generate_adapters.py:428` (main CLI) |
| **Workflow Engine** | 11 YAML-defined workflows with phases, agent assignments, quality gates, state recovery | `context/workflows/README.md` phase diagrams |
| **Rules/Standards Split** | Binary rules (<200 tokens) + reference standards (2000-5000 tokens); orchestrator glob-matches task scope | `context/agents/orchestrator.md` |
| **Disk-Durable State** | `HANDOFF.md`, `tasks.md`, `repo-index.json`, `spec-scan.md`, `repo-profile.md` on disk; compaction resilience | `context/agents/orchestrator.md:215-222` |
| **Pre-commit Validators** | 11 validators across workspace conventions, secrets, agents, staleness, subrepo, supabase, tech writing, testing, TS env, UI dev, UI testing | `context/scripts/validators/*.py` (11 files) |
| **Runtime Projection** | Compile canonical context/ into per-runtime adapters; `git-subrepo` for context/ management | `context/scripts/code-specs/spec_indexer.py` git-subrepo symbols, `init.sh` |

### UX Flows

**Confidence**: Needs Confirmation · 60% · Evidence: `context/workflows/*.yaml` (phases, agent assignments), `context/scripts/code-specs/spec_indexer.py:1232` (_run scan), `context/scripts/generators/generate_adapters.py:428`

| Flow | Actor | Steps (call chain) | Notes |
|------|-------|-------------------|-------|
| **Derive Spec (mode=both)** | Human → Orchestrator → product-owner + solution-architect | 1. Intake (mode=both recorded) → 2. Scan (spec_indexer) → 3. Repo Profile → 4. Baseline/Drift → 5. Evidence → 6. Product Spec (4a) + Technical Spec (4b) → 7. Verify → 8. Confirmation → 9. Finalise/Promote | Active T-008 Pilot A |
| **Adapter Generation** | Human → Orchestrator → generate_adapters.py | 1. CLI invoke → 2. Read canonical context/ → 3. Project to runtime adapters → 4. Write to .claude/, .cline/, etc. | `context/scripts/generators/generate_adapters.py:428` main entry |
| **Agent Spawn & Delegate** | Orchestrator → Sub-agent | 1. Read agent definition → 2. Resolve rules by glob → 3. Assign disjoint file scope → 4. Spawn with task prompt template → 5. Sub-agent reports → 6. Orchestrator commits | `context/agents/orchestrator.md:115-140`, `context/templates/task-prompt-template.md` |
| **State Recovery** | Orchestrator (post-compaction) | 1. Re-read HANDOFF.md (Workflow/Phase) → 2. Re-read repo-index.json + spec-scan.md → 3. Re-read repo-profile.md → 4. Resume from drift-candidates.md + spec-drafts/ | `context/agents/orchestrator.md:215-222`, `context/workflows/derive-spec.yaml:187-198` |

---

### User-Facing Constraints

**Confidence**: Verified · 85% · Evidence: `artefacts/build/repo-index.json:config` (8 keys from .env.template), `context/scripts/code-specs/spec_indexer.py:1194` (analyze_sql config extraction), `.env.template`

| Constraint | Source | Keys (redacted) |
|------------|--------|-----------------|
| **Required API Keys** | `.env.template` (lines 12-20) | `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `OPENAI_API_KEY`, `SUPABASE_ANON_KEY`, `SUPABASE_DB_PASSWORD`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_URL`, `UPSTREAM_PUSH_TOKEN` |
| **Model Selection** | `context/models.yaml` (not indexed — yaml not in scan) | Per-agent model tiers; `model: large/medium/small` in agent frontmatter |
| **Token Limits** | `requirements.md:133` (NFR-003) | <2,500 tokens framework overhead per spawn |
| **Parallel Execution Overhead** | `requirements.md:134` (NFR-004) | <20% token overhead vs sequential |

---

## Open-Questions Appendix

| ID | Subsection | Priority | Question | Options | Status |
|----|------------|----------|----------|---------|--------|
| Q-001 | Actors and Roles | blocking | Should the derived product spec go to `build/derived/` instead of `product/derived/`? | 1. Go to `build/derived/` · 2. Keep in `product/derived/` · Other | **APPROVED** |
| Q-002 | UX Flows | high | Are the 4 UX flows complete, or are there additional user-facing flows (e.g. onboarding, subrepo update)? | 1. Flows complete as listed · 2. Add onboarding flow · 3. Add subrepo update flow · Other | **APPROVED** |
| Q-003 | Features | high | Should "Runtime Projection" be split into separate features per runtime (Claude, Cline, Gemini, Copilot, Codex)? | 1. Keep unified · 2. Split per runtime · Other | **APPROVED** |

---

## Drift: Canonical Docs vs Derived Behaviour

| ID | Canonical source (`path:line`) | Says | Code does (`path:line`) | Question raised |
|----|-------------------------------|------|-------------------------|-----------------|
| D-001 | `artefacts/product/requirements.md:1-3` | "THIS SECTION IS POPULATED AS AN EXAMPLE... SHOULD BE REPLACED BY THE PRODUCT REQUIREMENTS FOR YOUR PROJECT" | Spec indexer extracts actual framework requirements from code; example doc is placeholder | Q-001 |
| D-002 | `artefacts/architecture/architecture.md:1-3` | "THIS SECTION IS POPULATED AS AN EXAMPLE... SHOULD BE REPLACED BY THE ARCHITECTURE DEFINITION FOR YOUR PROJECT" | Architecture.md is example; actual architecture is in code (34 agents, 11 workflows, etc.) | Q-001 (same question) |
| D-003 | `artefacts/architecture/data-model.md` | Documents data model for agentic harness | No SQL tables in repo (index api=0, tables=0); claims Assumed (<50%) | (to be asked in Phase 7) |
| D-004 | `artefacts/architecture/api-catalogue.md` | Documents API catalogue | No HTTP routes (index api=0); claims Assumed (<50%) | (to be asked in Phase 7) |

---

## Verification and Review Record

| Check | Result | Date |
|-------|--------|------|
| `verify --index` (citations resolve) | pending | 2026-11-05 |
| `verify --doc` (final drafts) | pending | 2026-11-05 |
| Human review gate | pending | 2026-11-05 |