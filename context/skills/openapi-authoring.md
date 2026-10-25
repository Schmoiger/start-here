---
name: openapi-authoring
description: Procedural guidance for authoring and maintaining the canonical OpenAPI specification — consistent naming, complete responses, realistic examples, backwards compatibility, and standard HTTP semantics.
globs: ["**/openapi*.yaml", "**/openapi*.yml", "**/openapi*.json", "artefacts/api/**"]
---

# OpenAPI Authoring Skill

**Applies to**: every change to the canonical API specification and its companion conventions.

---

## Single Canonical Spec

Maintain `{project-root}/artefacts/architecture/openapi.yaml` as the single canonical API specification — paths, request/response schemas, error format, and conventions. Do not create a second spec in `artefacts/api/` or a service directory.

- Conventions and port assignments live in `{project-root}/artefacts/architecture/api-catalogue.md`.
- `artefacts/api/` holds ancillary machine-readable contracts (`api-contract.json`) and the human-facing `api-design-guide.md`; the authoritative specification is the architecture copy.
- When the implementation disagrees with the spec, record the inconsistency as a finding for the architect to resolve. Do not silently diverge from the contract.

---

## Authoring Rules

1. **OpenAPI 3.0+** — use a supported OpenAPI version; never invent dialect extensions.
2. **Consistent naming** — camelCase for JSON fields, kebab-case for URL paths.
3. **Document every response** — each endpoint lists all possible responses, including error responses.
4. **Realistic examples** — every schema carries an example that a consumer could use as-is.
5. **Backwards compatibility** — additive changes by default; a breaking change requires an explicit decision record.
6. **Standard HTTP semantics** — use established methods and status codes before inventing custom conventions.
7. **One format for errors** — a single error envelope shared by all endpoints, documented once and referenced.

---

## Validation

Validate the specification before reporting completion:

```bash
uv run python -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" {file}
```

Validate companion markdown with:

```bash
uv run python context/scripts/validators/verify_typst_formatting.py {files}
```

---

## Why

Two sources of truth produce two implementations. A single owned specification, validated on every change, keeps the contract, the service layer, and the consumers aligned; an unvalidated or duplicated spec is a fork that will drift silently.
