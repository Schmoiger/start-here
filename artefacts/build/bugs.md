# Bugs: derive-spec harness work — process & compliance defects

**Branch**: feat/spec-agent
**Status**: In Progress
**Scope**: Process and compliance defects found by auditing the shipped spec-agent work (T-014 → T-016) against the harness's own rules/standards/skills — tdd-workflow.md, testing.md, python-environment.md, python-scripting.md, secrets.md, tech-writing.md, doc-standards.md, workspace-conventions.md.
**Audited**: 2026-02-11 — post-hoc context-acquisition sweep (triggered by the failure chain recorded in B-001)
**Related**: `artefacts/build/tasks-spec-agent.md` (feature tasks). Bugs here are process defects; feature backlog lives there.

---

## Bug Index

| ID | Priority | Status | Component | Bug |
|----|----------|--------|-----------|-----|
| B-001 | critical | mitigated | TDD discipline | RED-first ordering reversed in T-015/T-016 — tests written after implementation |
| B-002 | high | fixed | Workspace conventions | Session metrics never appended to `artefacts/build/metrics/session-log.jsonl` for T-014→T-016 and T-015 |
| B-003 | medium | open | Context acquisition | Matching skill/rule not loaded before code tasks — root cause of B-001 |
| B-004 | low | partial | Code hygiene | ruff not run/enforced on `context/scripts/` — 228 findings in indexer code/tests |
| B-005 | low | open | Coverage evidence | pytest-cov absent — Coverage % per testing.md §1.1 cannot be reported |

---

## B-001: TDD RED-first ordering reversed (T-015/T-016) — tests written after implementation

#### Symptom

- T-015 (`feat(spec): implement T-015 extraction backends`, e2e243c) shipped implementation and tests in one commit, with no observed-failing "RED" evidence.
- T-016 (698bb5d) repeated the pattern: `collect_config` was implemented end-to-end and smoke-validated **before** `test_spec_indexer_config.py` existed. The tests then caught real bugs (env-call RHS hoisting, JSON key line detection, test-file config pollution) — but that is regression testing, not TDD.
- Test names did not follow `test_<subject>_should_<behaviour>_when_<condition>`; some expected values were confirmed against the implementation's own output instead of being pre-computed from the task spec.

#### Failure Chain (root cause)

1. **Context acquisition skipped.** `tdd-workflow` (globs `**/tests/**`, `**/*.test.py`) and `testing.md` both match the test files being written, yet neither was loaded before the first code edit. The rule was in the very first context packet (AGENTS.md skills table) — it was simply never invoked.
2. **Precedent anchoring.** The existing `test_spec_indexer_extractors.py` (T-015) was treated as the authoritative pattern — same shape, same implementation-first commit style. The instruction "adhere to existing conventions" was resolved against the stricter process rule silently, in favour of the observed pattern.
3. **Task-file rationalisation.** T-010 ("Unit tests: skill/workflow schema, indexer extraction + verify") reads like a separate later deliverable and was used as permission to defer per-task testing discipline. It organises work; it does not waive `testing.md`/`tdd-workflow.md`.
4. **Gate substitute.** Every verification run (pytest green, drift clean, typst pass) checked *outcome*, never *order* (test-fails-first is unenforceable mechanically). Validated results stood in for disciplined process — exactly the shape of a test-after workflow.

#### Fix

- **Applied** (2026-02-11): T-016 tests renamed to the `should` convention — `test(spec): rename config tests to should convention`, f6a49fb.
- **Agreed with human** (2026-02-11): RED-GREEN with a single commit per task for remaining code tasks — failing `should` tests written first, RED observed before any implementation edit, minimal implementation, one commit, report `Pass rate: X% | Coverage: …` per testing.md §1.1.

#### Acceptance Criteria

- [x] T-016 tests use `should` naming and the suite is green (9/9)
- [ ] T-017 starts with failing tests (RED observed) before implementation edits
- [ ] T-021 starts with failing tests (RED observed) before implementation edits
- [ ] Task reports include Pass-rate / coverage evidence in the testing.md §1.1 format

---

## B-002: Session metrics never appended to `session-log.jsonl`

#### Symptom

`artefacts/build/metrics/session-log.jsonl` has no entries after 2026-10-30; commits `db09c5b` (T-014) → `f6a49fb` (rename) carry no metric records. T-015 (e2e243c, 2026-11-01) is missing too. `orchestrator.md` §2 Reporting mandates appending session metrics per task completion.

#### Fix

Backfill schema-conformant `complete` entries for every shipped task (T-014, T-001, T-002, T-013, T-016, plus rename/audit work), citing commit hashes; validate with `uv run python context/scripts/validators/workspace_conventions.py metrics <file>`. Log on completion going forward.

#### Acceptance Criteria

- [x] Entries exist for all spec-agent tasks shipped by this audit date
- [x] `workspace_conventions.py metrics` validates clean
- [ ] Future task completions append entries as part of the same commit

---

## B-003: Context-acquisition screen skipped before code tasks

#### Symptom

The task-intake step consumed acceptance criteria and code context only; the agent's own pool (standards/rules/skills in `context/`) was never acquired for the work class before the first edit. This is the root cause of B-001 and the mechanism behind every other gap in this document.

#### Fix

Load-first self-check before any task touching code/tests: read the matching skill and rule for the work class (`tdd-workflow.md`, `testing.md`, `python-scripting.md`, `python-environment.md`, `secrets.md`, `tech-writing.md`, …) and invoke the skill if one matches. When an observed convention conflicts with a governing rule, surface the conflict to the human instead of resolving it silently.

#### Acceptance Criteria

- [x] Post-hoc sweep executed for T-014→T-016 (findings in this document)
- [ ] T-017/T-021 sweep (acquisition screen) happens *before* implementation begins
- [ ] Any future code task loads its matching skill/rule before the first edit, noting it in the handoff/tasks file

---

## B-004: ruff not run/enforced on `context/scripts/`

#### Symptom

`ruff check` on the four indexer code/test files reports 228 findings (dominated by pre-existing line-length / import-order issues in the T-015-era `spec_indexer.py`; one fixable — a missing trailing newline in `test_spec_indexer_config.py`). The repo's pre-commit hook config only lints `^services/.*\.py$`; `context/scripts/**` sits outside the ruff gate entirely, so the `python-scripting` skill's lint-verification step can neither detect nor be enforced.

#### Fix

Apply `ruff --fix` for the single fixable item (W292) in the newly-added test file. Do **not** mass-reformat the pre-existing indexer in this bug. Propose extending the ruff scope (or a dedicated `context/scripts` rule set) as a harness improvement at T-010 / continuous-improvement.

#### Acceptance Criteria

- [x] `ruff --fix` applied to the T-016 test file (W292 only); suite still green
- [ ] (proposal) ruff scope extends to `context/scripts/` — tracked at T-010 / continuous-improvement
- [ ] (proposal) consider ruff for the indexer as part of the T-019 pilot cleanup, not mid-flight

---

## B-005: pytest-cov absent — Coverage % cannot be reported

#### Symptom

`testing.md` §1.1 mandates reporting `Coverage: X% | Pass rate: X%` on every test run; `pytest --cov` is unsupported because `pytest-cov` is not in the root `[dependency-groups] dev` group. Sessions have been reporting pass counts only.

#### Fix

Add `pytest-cov` to `[dependency-groups] dev` (root `pyproject.toml`) at T-010 together with the schema/extraction tests; thereafter report module coverage for changed files. Do not add the dependency mid-task without a human-approved dev-deps change.

#### Acceptance Criteria

- [ ] dev deps include `pytest-cov`
- [ ] A task report (T-017 or later) includes a real Coverage % per tested module

---

## Sweep Verdict (2026-02-11)

All deterministic validators are green against shipped artefacts: `tech_writing.py` (British English + dates), `testing.py` (outcomes not interactions), `secrets.py` (incl. `ts_extract.mjs`), `workspace_conventions.py` paths + commit-msg, `agent_definitions.py` (15 agents), `adapter_drift.py`. Python environment baseline is sound (root `pyproject.toml`, `uv.lock`, `.python-version`, dev deps incl. pytest); indexer runs used `uv run` throughout and the PEP 723 metadata, `from __future__ import annotations`, type hints, and `argparse` exit-code conventions in `python-scripting.md` are followed. Secrets handling is correct: the indexer reads only committed template files, never the live `.env`, and redacts secret-looking value-hints.

Observations (not bugs): `doc-standards.md` §7.1 "no em dashes" targets documentation artefacts; `context/skills/` prose uses em-dashes ecosystem-wide (analyse-repo.md 32, derive-spec.md 30), so harmonisation, if wanted, is a separate docs task. `python-environment.md` §2's `--project` flag reads as applying when a pyproject is absent at cwd; at the repo root a pyproject resolves so the repo's own canonical commands (`uv run pytest context/scripts/tests/`) are consistent. HANDOFF.md was not written this session because no subagents were spawned (orchestrator-as-implementer, task file as record).