---
name: requirements-elicitation
description: Procedural guidance for interviewing users to turn vague ideas into a validated problem statement before requirements are formalised.
globs: ["artefacts/product/**", "**/discovery-notes.md"]
---

# Requirements Elicitation Skill

**Applies to**: Discovery conversations, before any requirement is written in EARS notation.

---

## Overview

Elicitation is the act of finding out what the user actually needs, as distinct from what they
first asked for. The output is a validated problem statement — `discovery-notes.md` — not a
requirements specification and not a solution. Formalisation happens afterwards in the structuring
mode of `@product-owner`.

---

## 1. Questioning Framework

Ask questions to uncover:

### The Problem

- What problem are you trying to solve?
- Who experiences this problem? How often?
- What happens if this problem isn't solved?
- How do people solve this today?

### The Users

- Who will use this? (Be specific: roles, technical level)
- What's their context when using it?
- What do they care about most?

### The Scope

- What's the smallest thing that would be useful?
- What's explicitly NOT part of this?
- Are there existing systems this needs to work with?

### The Constraints

- Are there deadlines, budgets, or technical constraints?
- What would make this fail?
- What's already been tried?

### The Success Criteria

- How will you know this works?
- What would make users delighted vs merely satisfied?

---

## 2. Interview Constraints

- Ask questions; don't assume you understand
- One or two questions at a time; don't overwhelm
- Reflect back what you heard before asking more
- Don't propose solutions; focus on understanding the problem
- Challenge vague statements like "fast", "easy", "user-friendly"
- Identify when scope is too large and help narrow it

---

## 3. Capturing the Interview

Write findings to `{project-root}/artefacts/product/discovery-notes.md` as the conversation
progresses — never accumulate the whole interview in memory and flush at the end. The file is a
working document: update the problem statement, users, scope boundaries, constraints, and open
questions as each is confirmed.

The section structure for `discovery-notes.md` is defined in the `@product-owner` definition,
Mode 1. Keep the notes free of requirement identifiers and acceptance criteria; those belong to
`requirements.md`.

---

## 4. Exit Criteria

The interview is complete when all of the following hold:

- The problem is stated in two or three sentences, without solution language
- Target users are named, with the context in which they meet the problem
- Scope boundaries state what is explicitly out of scope
- Constraints and assumptions are recorded
- Success criteria are observable or measurable
- Open questions are listed for the structuring mode, each with the decision it blocks

If a criterion cannot be satisfied because the user has not decided, record the open question and
escalate the blocking decision rather than filling the gap with an assumption
(`context/rules/multi-agent-collaboration.md`).
