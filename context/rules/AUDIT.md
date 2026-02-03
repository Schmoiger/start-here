# Rules Audit - Phase 1

## Classification

### ✅ Enforceable Rules (Keep in rules/)

| File | Validator Type | Reason |
|------|---------------|---------|
| conventional-commits.mdc | Regex pattern | Can validate commit message format |
| EARS-notation-requirements.mdc | Syntax parser | Can parse WHEN/IF/THE/SHALL patterns |
| metrics-logging.mdc | Format validator | Can validate agent metrics structure |
| british-english.mdc | Spell checker | Can validate spelling (colour vs color) |

### ❌ Non-Enforceable (Move to Standards)

| File | Move To | Type | Reason |
|------|---------|------|--------|
| prefer-mermaid.mdc | doc-standards.md | Preference | Subjective tool choice |
| detecting-ai-slop.mdc | doc-standards.md | Guideline | Subjective quality assessment |
| dry.mdc | coding-standards.md | Principle | Design principle, already there |
| test-driven-development.mdc | testing-standards.md | Methodology | Development workflow |
| twelve-factors-app-rule.mdc | tech-standards.md | Architecture | Architecture principles |
| react-native-ui.mdc | coding-standards.md | Best Practices | Framework patterns |
| react-native-web.mdc | coding-standards.md | Best Practices | Framework patterns |
| swift-ui.mdc | coding-standards.md | Best Practices | Framework patterns |
| assumption-handling.mdc | workflow-standards.md | Process | Workflow protocol |
| documentation-maintenance.mdc | doc-standards.md | Process | Maintenance process |
| retrospective-rules.mdc | workflow-standards.md | Process | Sprint process |
| teching-engineer-rule.mdc | workflow-standards.md | Persona | Communication style |
| project-root.mdc | tech-standards.md | Guidance | Setup guidance |
| use-context7.mdc | tech-standards.md | Workflow | Tool usage guidance |
| ux-ui-best-practices.mdc | doc-standards.md | Patterns | Design patterns |

## Summary

**Keep**: 4 rules (enforceable)
**Move**: 15 rules → standards (not enforceable)
