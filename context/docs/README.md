# Workflow & Reference Guides

Human-readable guides for the context framework. For the machine-readable sources, see `context/workflows/*.yaml`.

---

## Workflow Guides

| Guide | Workflow Covered | Status |
|-------|-----------------|--------|
| `workflow-default.md` | `default.yaml` — full TDD with quality gates | Stale (`default.yaml` superseded by `build.yaml` for most work) |
| `workflow-prototype.md` | `prototype.yaml` — fast iteration for POCs | Current |
| `workflow-agent-effectiveness.md` | `retrospective.yaml` — post-deployment analysis | Stale (references `agent-effectiveness.yaml` which was renamed) |
| `workflow-documentation-for-humans.md` | `content.yaml` — human-facing content with writing personas | Stale (references `documentation-for-humans.yaml` which was renamed to `content.yaml`) |

> **Gap**: There is no `workflow-build.md` for `build.yaml`, which is now the primary development workflow. This should be created.

## Reference Docs

| Doc | Purpose |
|-----|---------|
| `orchestration-patterns.md` | Multi-agent coordination patterns: single agent, chain, swarm, hive, loop — with worked examples |
| `writing-personas.md` | When and how to use writing personas in the documentation workflow |
| `framework-adapters.md` | Cross-framework compatibility guide (Claude Code, Cursor, Cline) |
| `how-to-measure-agent-effectiveness.md` | Detailed measurement examples for the `@workflow-analyst` agent |

---

## Maintenance

- When a workflow YAML is added or renamed, update the table above and create or update the corresponding guide.
- Mark superseded guides as "Stale" — don't delete them, as they may still be referenced or useful for historical context.
- Guides should include Mermaid diagrams showing phase flow where possible.
- The stale guides (`workflow-default.md`, `workflow-agent-effectiveness.md`, `workflow-documentation-for-humans.md`) should be updated to reference the correct YAML filenames when time permits.
