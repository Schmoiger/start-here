# Rules Reference Card

Quick reference for all project rules. Source: `context/rules/*.mdc`

## Always Apply

| Rule | File | Summary |
|------|------|---------|
| British English | british-english.mdc | colour, organise, behaviour; DD/MM/YYYY |
| No AI slop | detecting-ai-slop.mdc | No em dashes, triads, hedging, empty preambles |
| DRY | dry.mdc | Single source of truth |
| TDD | test-driven-development.mdc | London School: Red → Green → Refactor |
| Teaching persona | teching-engineer-rule.mdc | Suggest improvements, explain clearly |

## On Demand

| Rule | File | Trigger |
|------|------|---------|
| EARS notation | EARS-notation-requirements.mdc | Requirements docs |
| Mermaid | prefer-mermaid.mdc | Diagrams |
| Conventional commits | conventional-commits.mdc | Git commits |
| 12-Factor | twelve-factors-app-rule.mdc | SaaS apps |
| Doc maintenance | documentation-maintenance.mdc | CI pipeline |
| Retrospectives | retrospective-rules.mdc | Sprint reviews |
| Project root | project-root.mdc | Package installs |
| Context7 | use-context7.mdc | Code generation |

## Platform-Specific

| Rule | File | Platform |
|------|------|----------|
| SwiftUI | swift-ui.mdc | iOS |
| React/Next.js | react-native-ui.mdc | Web |
| React Native | react-native-web.mdc | Mobile + Web |
| UI/UX | ux-ui-best-practices.mdc | All interfaces |

## Quick Reference

### EARS Patterns

| Type | Syntax |
|------|--------|
| Ubiquitous | THE {system} SHALL {action} |
| Event | WHEN {trigger}, THE {system} SHALL {action} |
| State | WHILE {state}, THE {system} SHALL {action} |
| Optional | IF {condition}, THE {system} SHALL {action} |

### TDD Cycle

| Phase | Do | Constraint |
|-------|-----|------------|
| Red | Write failing test | Compilation error |
| Green | Minimum to pass | No logic |
| Refactor | Improve design | DRY, SOLID |

### Commit Format

`{type}({scope}): {ID} {description}`

Types: feat, fix, test, refactor, docs, chore

### AI Slop Checklist

- [ ] No em dashes
- [ ] No triads
- [ ] No empty preambles
- [ ] No excessive transitions
- [ ] Specific examples
