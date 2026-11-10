# PR Description Template

---

## Format

```markdown
## Summary

<1-3 sentence description of what this PR accomplishes>

## Changes

| Task | Description | Status |
|------|-------------|--------|
| #ID | Brief description | Done/Partial |

## Agent Metrics

### Efficiency

| Metric | Total | Mean | SD |
|--------|-------|------|----|
| Commits | <count> | — | — |
| Duration | <total> | <mean> | <sd> |
| Tokens (in) | <total> | <mean> | <sd> |
| Tokens (out) | <total> | <mean> | <sd> |

### Autonomy

| Mode | Count | % |
|------|-------|----|
| Fully autonomous | <n> | <pct> |
| With human input | <n> | <pct> |
| Human-directed | <n> | <pct> |

## Test Plan

- [ ] <verification step>

## Links

- [Task details](<path-to-tasks-file>): link to the actual tasks file if it exists (e.g., `artefacts/build/tasks-<branch>.md`, `tasks.md`, or relevant task index)

---
<runtime-footer>: insert the correct runtime here (e.g., `[Claude Code](https://claude.ai/code)`, `[GitHub Copilot](https://github.com/features/copilot)`, `[Google Gemini](https://gemini.google.com)`, `[OpenAI Codex](https://openai.com/codex)`, `[Cline](https://cline.bot)`). Do not hard-code.
```