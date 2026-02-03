# Bug Reporting Standards

## 1. Introduction

This document defines the standard for reporting bugs in a way that enables an AI agent to address them autonomously. The goal is to create a centralised, concise, and machine-readable list of bugs.

All bugs shall be listed in a `bugs.md` file located in the project's artefacts directory (e.g., `/services/data-service/artefacts/bugs.md`).

## 2. Format

Each bug shall be recorded on a single line in the `bugs.md` file. This allows each bug to be referenced by its line number, which serves as its unique ID.

The format for each bug entry shall be as follows:

```
[Status] | [Short Description] | [File Path or Entry Point] | [Link to Task/Issue]
```

### 2.1. Field Descriptions

*   **Status:** The current state of the bug. The system shall use one of the following statuses:
    *   **[TODO]:** The bug has been reported and is ready for an agent to begin work.
    *   **[WIP]:** An agent is currently working on the bug (Work in Progress).
    *   **[DONE]:** The agent has implemented a fix and committed the changes.
    *   **[BLOCKED]:** The agent cannot proceed and requires human intervention.
    *   **[WONTFIX]:** The bug will not be fixed. This may be because it is obsolete, is working as intended, or requires a new feature that is not yet prioritized.
*   **Short Description:** A brief, clear summary of the bug. The system shall use the format: `[Observed Incorrect Behavior] INSTEAD [Expected Correct Behavior]` (e.g., "User is redirected to /home on logout INSTEAD user should be redirected to /login").
*   **File Path or Entry Point:** The most relevant file, function, or component to begin the investigation (e.g., `src/auth/logout.js`).
*   **Link to Task/Issue:** A hyperlink to a full bug report. This report must provide the necessary and sufficient context for an agent to execute the task, as defined in `agent-standards.md`. The link may point to:
    *   A specific line in the project's `tasks.md` file.
    *   A GitHub Issue.
    *   An entry in another issue tracking system.

## 3. Example

Here is an example of a `bugs.md` file for `project-a`:

```markdown
# project-a Bugs

[TODO] | User is sent to /home after logout INSTEAD user is sent to /login | src/auth/logout.js | [tasks.md#L25](./artefacts/tasks.md#L25)
[WIP] | Product page API call fails with 500 error INSTEAD API call returns product data | src/products/api.js | #123
[WONTFIX] | User cannot export data to CSV INSTEAD user can export data | src/reports/component.js | #125
```
