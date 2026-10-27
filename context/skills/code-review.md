---
name: code-review
description: Procedural guidance for performing detailed PR-style code review focused on bugs, edge cases, and maintainability — with an explicit boundary against the security-tester's systematic analysis.
globs: ["**/*.py", "**/*.ts", "**/*.tsx"]
---

# Code Review Skill

**Applies to**: line-by-line review of changed code, performed by a reviewer agent after the `@tech-lead` gate APPROVED the change.

---

## Review Scope

- Catch bugs, edge cases, and maintainability problems — the deep-bug-hunting pass.
- Review the diff **and its context**: read the callers and callees of every changed function; a change cannot be judged in isolation.
- Review only after the `@tech-lead` gate APPROVED — you are the second reviewer, after the gate (`tech-lead.md` §You Are the Gate). Verify approval in `{project-root}/artefacts/build/tech-review.md` before starting.

---

## Technique

1. **Trace every code path** — happy path, error path, and edge cases (empty collections, null/undefined, boundary values, concurrency, ordering).
2. **Cite `file:line` for every finding** — a review claim without a location is unverifiable.
3. **Explain why, not just what** — state the failure mode and the input that triggers it.
4. **Prioritise** — Critical > High > Medium > Low.
5. **Show the fix** — include a code snippet when a concrete fix exists.
6. **Acknowledge good patterns** — a manufactured finding is a defect in the review.
7. **Focus on substance, not style** — ignore what the linters already enforce (`tech-lead.md` §Task Constraints); do not nitpick formatting.

---

## What to Catch

- Logic bugs and off-by-one / boundary errors
- Missing or silently swallowed error handling
- Race conditions and ordering assumptions
- Resource leaks (connections, cursors, subscriptions)
- Incidental security issues in the changed code (e.g. an obvious SQL injection in a query) — these are bugs caught in passing

---

## Boundaries

- **Do not duplicate `@security-tester`** — threat modelling, OWASP Top 10 assessment, dependency vulnerability scanning, prompt injection testing, and auth pattern review belong to the security tester (`security-tester.md` §Review Scope). You catch security *bugs in the changed code*; you do not run a systematic security audit.
- **Do not rewrite code** — describe what needs to change; the authoring agent fixes it (`tech-lead.md` §Task Constraints).

---

## Output

Write the review to `{project-root}/artefacts/build/code-review.md` with prioritised findings. A reviewer is a gate agent: writable only to its review artefact, never to the code under review (`multi-agent-workflows.md` §Read-Only Agents).

---

## Why

The only check that catches an author's blind spots is a review by a different agent than the author. Keeping the technique in one skill keeps it DRY across reviewer roles, and the explicit security boundary stops two roles from duplicating each other's analysis.
