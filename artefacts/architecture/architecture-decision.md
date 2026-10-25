# Architecture Decisions

Running log of significant technical decisions (the *why* behind choices). Format: numbered ADR with Date,
Status, Context, Decision, and Consequences (see `context/standards/doc-standards.md` §4.2).

---

## ADR-001: Canonical OpenAPI specification lives under `artefacts/architecture/`

- **Date**: 25 Oct 2026
- **Status**: Accepted
- **Context**: TASK-015 retires the separate API designer agent and absorbs its role into
  `@solution-architect`. Ownership of the API contract was
  contradicted in three places: `solution-architect.md` §Deliverables and `architecture-fidelity.md` named
  `artefacts/architecture/openapi.yaml`, while `artefacts/README.md`, `context/standards/doc-standards.md`
  §4.3 and `context/standards/context-framework.md` named `artefacts/api/openapi.yaml`. An empty scaffold
  existed at `artefacts/api/openapi.yaml`. Two owners and two paths is the same defect as two specs: the
  contract drifts from whichever copy the implementer happens to read.
- **Decision**: `{project-root}/artefacts/architecture/openapi.yaml` is the single canonical OpenAPI
  specification, owned and maintained by `@solution-architect`. `artefacts/api/` keeps ancillary artefacts
  (`api-contract.json`, `api-design-guide.md`) but never holds a second specification. Chosen over the
  `artefacts/api/` location because the architect already produces the contract in the
  `design-architecture` phase and the majority of executable references (agent definition, skill, workflow,
  tester) already resolve there; the empty scaffold at `artefacts/api/openapi.yaml` carries no content to
  migrate.
- **Consequences**: `artefacts/README.md`, `context/standards/doc-standards.md` §4.2–4.3 and
  `context/standards/context-framework.md` now agree with the architect definition, `design.yaml`, the
  `openapi-authoring` skill, and `architecture-fidelity.md`. The category taxonomy decision (whether API
  contracts deserve a top-level `artefacts/` lane at all) remains for TASK-008; this ADR fixes the path and
  ownership only.
