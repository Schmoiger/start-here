# Repository Profile: start-here

**Generated**: 2026-11-05T13:24:38Z  
**Index**: `repo-index.json`  
**Scan Mode**: both (product + technical)  
**Toolchain**: stdlib.ast + ast-grep (tree-sitter unavailable)  

---

## App Type

**Python harness framework** — deterministic spec-indexer pipeline (`spec_indexer.py`) with
34 agents defined across 11 workflow YAMLs, 5 test suites, and cross-service coordination
infrastructure. Serves as the reference repo for `derive-spec` skill pilot.

---

## Entry Points

- `context/scripts/code-specs/spec_indexer.py` — main CLI entry (`spec-indexer scan` /
  `spec-indexer verify`); `__main__` at line 2092
- `context/scripts/generators/generate_adapters.py` — adapter generator CLI
- `context/scripts/tests/test_spec_indexer.py` — unit-test suite (22 T-010 tests)
- `context/scripts/tests/` — general test fixtures

---

## Key Module Boundaries

| Module | Purpose | Key Lines |
|--------|---------|-----------|
| `context/scripts/code-specs/spec_indexer.py` | Indexer core (731 symbols extracted) | Lines 1–2092 |
| `context/scripts/code-specs/` | Indexer submodules: parsers, extractors, validators | Lines ~200–640 |
| `context/scripts/generators/` | Adapter generators (Claude, Cline, Gemini, OpenAI) | Lines ~200–600 |
| `context/scripts/validators/` | Pre-commit/CLI validators (workspace conventions, secrets, etc.) | Lines ~100–750 |
| `context/agents/` | Agent definition files (product-owner, solution-architect, etc.) | Lines ~50–150 each |
| `context/workflows/` | 11 workflow YAMLs defining phases, gates, quality criteria | Full files |
| `context/scripts/tests/` | Test suites (test_spec_indexer.py: 22 tests; others) | Full dir |

---

## Language Distribution

| Language | File Count | Symbols Extracted |
|----------|-----------|------------------|
| Python | 60 | 731 |
| JavaScript | 1 | minimal |

---

## Symbol Counts (per-file top classes/functions)

Key indexed symbols from `spec_indexer.py`:
- `LANG_BY_SUFFIX` (62 entries), `FOREIGN_LANG_SUFFIXES` (73), `TS_LANGS` (89)
- `DOC_GLOBS` (92), `DOC_BASENAME_PATTERNS` (104), `EXCLUDED_DIRS` (115)
- `ROUTE_METHOD_ATTRS` (138), `_JSX_TAG_RE` (142), `_TS_IMPORT_NAMED` (145)
- `Symbol` class (171), `FileRecord` class (191), `ApiEntry` class (211)
- `ColumnDef` class (229), `TableDef` class (238), `UiComponent` class (254)
- `TestNode` class (274), `DocRecord` class (283), `ConfigEntry` class (292)
- `rel()` (316), `language_of()` (321), `find_target_files()` (328)
- `_unparse()` (386), `_decorator_names()` (393), `_route_from_decorator()` (401)
- `_method_body()` (426), `analyze_python()` (437), `_destructured_props()` (509)
- `_is_component()` (522), `analyze_tsjs()` (526)
- `EXTRACTOR_CHOICES` (614), `BACKEND_LANG_COVERAGE` (624)
- `_ASTGREP_PATTERNS` (1044), `_ASTGREP_KIND_RE` (1052), `_ASTGREP_LANG_FLAG` (1061)

---

## Index Coverage Highlights

- **config keys extracted**: 8 (ANTHROPIC_API_KEY, GEMINI_API_KEY, OPENAI_API_KEY,
  SUPABASE_ANON_KEY, SUPABASE_DB_PASSWORD, SUPABASE_SERVICE_ROLE_KEY, SUPABASE_URL,
  UPSTREAM_PUSH_TOKEN) — all from `.env.template`
- **245 pytest-collected tests** identified
- **25 existing spec/documents** discovered (readmes, requirements, architecture,
  design, api-catalogue, api-design-guide)
- **731 total symbols** extracted from 61 Python files
- **Extractor**: stdlib.ast (zero-dependency fallback) with ast-grep rules applied
  as secondary pass (tree-sitter unavailable on this machine)

---

## Module Dependencies (inferred)

1. **spec_indexer.py** → `context/scripts/code-specs/` parsers (ctags/ast-grep/stdlib)
2. **generators/** adapters → `context/scripts/code-specs/spec_indexer.py` index for symbol references
3. **validators/** → `context/scripts/tests/test_spec_indexer.py` schema
4. **workflows/** YAMLs → `context/agents/*.md` agent definitions (quality gates, phase schemas)
5. **agents/** MD → `context/README.md` agent index; `context/skills/*.md` procedural guides

---

## Scan Limitations

- `tree-sitter` not available → JSX/TSX not extracted; counts stay 0
- `ts-morph` not available → ruled out quietly
- `ast-grep` used as secondary backend → pattern-based symbol discovery
- Result: pure Python/stdlib extraction; no TypeScript/JSX structural evidence
- Prompt: re-run with `--extractors tree-sitter` if tree-sitter is installed

---

## Confidence Bands (pre-populated from index)

TBD — will be populated in Phases 4a/4b derived spec drafts per confidence model
(Q4 A2: bands Verified 85-100%, Needs Confirmation 50-85%, Assumed <50%).