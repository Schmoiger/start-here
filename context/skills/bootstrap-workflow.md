---
name: bootstrap-workflow
description: Procedural workflow for bootstrapping a new project or feature context.
globs: []
---

# Bootstrap Workflow Skill

---

## Overview

This skill provides the procedural steps for an agent to set up the necessary context documents, placeholders, and scripts when assigned to work on a new product or feature.

---

## 1. Product Description Verification

- If no product description is provided in the initial context, the agent shall request one from the user.
- The product description shall include sufficient detail about the purpose, target users, and key functionality to enable proper requirements analysis.

---

## 2. Common Subrepositories

If the project requires standardised context rules or PDF generation/typesetting, the agent shall clone the standard subrepositories using `git subrepo` if they are not already present:

- **Context Subrepo**:
  ```bash
  PATH="/opt/homebrew/bin:/usr/local/bin:$PATH" git subrepo clone https://github.com/Schmoiger/agents-framework.git context -b main
  ```
- **Typst Subrepo**:
  ```bash
  PATH="/opt/homebrew/bin:/usr/local/bin:$PATH" git subrepo clone https://github.com/Schmoiger/typst-engine.git typst -b main
  ```

*For more information on operating subrepositories, refer to `context/skills/git-subrepo-operations.md`.*

---

## 3. Documentation Creation Sequence

After obtaining the product description, the agent shall create or amend the following documents in strict order:

1. **`/artefacts/requirements.md`**: Functional and non-functional requirements using EARS notation as specified in `/context/rules/EARS-notation-requirements.md`.

2. **`/artefacts/architecture.md`**: Architectural and design decisions that describe how the product will be implemented.

3. **`{service}/artefacts/tasks.md`**: Comprehensive task breakdown for implementation, verified against standards in `/context/standards/`.

**For each document created or amended, the agent shall pause and wait for explicit human review and approval before proceeding to the next document.**

---

## 4. Placeholder Document Creation

Following the core specification documents, the agent shall create blank placeholder documents:

- **`{service}/artefacts/todo.md`**: For listing smaller items, technical debt, or future improvements.
- **`{service}/artefacts/bugs.md`**: For listing current and past bugs.

---

## 5. Documentation Standards Compliance

All documentation created during this workflow shall conform to the standards outlined in `/context/standards/doc-standards.md`, including:

- Proper file location within the project structure (system-wide in `/artefacts/`, service-specific in `{service}/artefacts/`)
- Content formatting and structure requirements
- Required elements for requirements (EARS notation), design decisions, and task specifications

---

## 6. Start Scripts

The agent shall create `(project)/scripts/start.sh` for local development startup and a root-level start script for the monorepo. The root-level script orchestrates starting all the needed local services.

---

## 7. Build Script

The agent shall create `scripts/build.yaml` following the standards in `/context/standards/build-standards.md`.

---

## 8. Workflow Completion

- Upon completion of all build work, the agent shall review common documents as outlined in `/context/standards/doc-standards.md` and make very concise changes as required, in particular:
  - `README.md` (service root)
  - Project-specific artefacts in `{service}/artefacts/`

- Upon completion of all documents, the agent shall summarise what was created and confirm with the user before beginning any implementation work.
- The agent shall not commence task execution until all context documents have been reviewed and approved by humans.
