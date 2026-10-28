---
name: workflow-analysis
description: Macro analysis lens for @harness-analyst — task, handoff, cycle-time, and bottleneck metrics, target-based scoring rubric, and efficiency report format.
globs: ["artefacts/build/**"]
---

# Workflow Analysis Skill

---

## Overview

The macro lens of `@harness-analyst` (`context/agents/harness-analyst.md`). It measures workflow efficiency across completed work cycles — task flow, handoffs, cycle times, standards adherence, and bottlenecks — and produces the efficiency report. The micro lens (token economics, model tiering) lives in `tokenomics-audit.md`. Telemetry inputs are listed in the agent's Shared Data-Source Inventory; this skill defines what to extract from them.

---

## Analysis Scope

Analyze these data sources to measure workflow efficiency:

### 1. Task Tracking

**Files**: `{project-root}/artefacts/build/tasks.md`, `{service}/artefacts/tasks.md`

**Metrics to extract**:

- Total tasks in cycle
- Tasks per phase (discovery/design/tdd-red/tdd-green/tdd-blue/review/test)
- Task completion time (from git log timestamps)
- Blocked tasks (dependencies not met)
- Rework tasks (returned from review-gate)

### 2. Handoff Analysis

**Files**: `{service}/HANDOFF.md`, `{project-root}/artefacts/shared/handoffs/*.md`

**Metrics to extract**:

- Number of handoffs per phase
- Handoff completeness (all required fields present?)
- Blocked handoffs (⚠️ Blocked status)
- Failed handoffs (🔴 Failed status)
- Handoff-to-handoff time (time between entries)

### 3. Git History Analysis

**Command**: `git log --all --oneline --since="<start-date>"`

**Metrics to extract**:

- Total commits in cycle
- Commits per agent (from Co-Authored-By tags)
- Commit frequency (commits per hour/day)
- Rework commits (fixes, reverts, amendments)
- Branch churn (branches created, deleted, merged)

### 4. Standards Adherence

**Analysis**: Review git log and conversation history

**Violations to count**:

- Bash used for file operations (should use Write/Edit)
- pip used instead of uv
- npm/npx used instead of yarn/yarn dlx
- Tests modified during tdd-green phase
- TDD phases combined (RED+GREEN together)
- Missing parallel execution options presentation

### 5. Token Usage Analysis

**Files**: Conversation history, estimation guidance from AGENTS.md

**Metrics to extract**:

- Estimated tokens (from planning phase)
- Actual tokens used (from conversation)
- Token efficiency ratio (actual/estimated)
- Token distribution by phase (discovery, design, implementation, review)
- Token waste (repeated prompts, rework, violations)

### 6. Repeated Patterns

**Analysis**: Review conversation history for repeated prompts

**Patterns to identify**:

- Same correction given multiple times
- Same standard referenced multiple times
- Same agent spawned multiple times for rework
- Repeated tool usage violations
- Repeated TDD phase violations

---

## Analysis Process

### Step 1: Data Collection

```bash
# Gather git statistics
git log --all --oneline --since="<cycle-start-date>" > analysis/git-log.txt
git log --all --numstat --since="<cycle-start-date>" > analysis/git-stats.txt

# Count commits by agent (Co-Authored-By analysis)
git log --all --since="<cycle-start-date>" | grep "Co-Authored-By" | sort | uniq -c

# Analyze commit frequency
git log --all --since="<cycle-start-date>" --format="%ai" | cut -d' ' -f1 | uniq -c
```

Read all relevant handoff and task files using Read tool.

### Step 2: Metric Calculation

Calculate these key metrics:

**Cycle Metrics**:

- Cycle duration (start to deployment)
- Phase durations (time in each workflow phase)
- Cycle velocity (tasks completed per day)

**Quality Metrics**:

- First-time pass rate (% tasks passing review first time)
- Rework rate (% tasks requiring rework)
- Standards adherence rate (% prompts following protocols)

**Efficiency Metrics**:

- Token efficiency (actual/estimated ratio)
- Agent efficiency (tasks completed per agent invocation)
- Handoff efficiency (clean handoffs vs blocked handoffs)

**Waste Metrics**:

- Rework cycles (times returned from review-gate)
- Repeated prompts (same correction given multiple times)
- Tool violations (bash used when Write/Edit required)

### Step 3: Bottleneck Identification

Identify the top 3-5 bottlenecks:

- **Phase bottlenecks**: Which phase took longest? Why?
- **Agent bottlenecks**: Which agent required most rework?
- **Standards bottlenecks**: Which standard was most violated?
- **Communication bottlenecks**: Where did handoffs fail?

### Step 4: Pattern Recognition

Identify recurring issues:

- **Repeated violations**: Same tool usage error multiple times
- **Repeated rework**: Same review feedback multiple times
- **Repeated confusion**: Same clarification requested multiple times

### Step 5: Recommendations

Provide actionable recommendations in priority order:

**High Priority** (fix immediately):

- Critical protocol violations causing >20% waste
- Repeated bottlenecks in critical path
- Standards updates needed

**Medium Priority** (fix next cycle):

- Minor inefficiencies causing 10-20% waste
- Process improvements for smoother handoffs
- Agent prompt template improvements

**Low Priority** (nice to have):

- Documentation improvements
- Tool usage optimisations
- Monitoring enhancements

---

## Scoring Rubric

Grade each metric against its target; do not compute a composite score.

- ✅ — within target
- ⚠️ — within 20% of the target threshold
- ❌ — violates target; must appear in Bottleneck Analysis or Repeated Issues with a fix

**Priority mapping** (from Analysis Process Step 5): >20% waste → High; 10-20% → Medium; <10% → Low.

Aggregate health scores and vanity metrics are prohibited (`context/workflows/continuous-improvement.yaml` § workflow_rules). A metric that cannot be attached to a fixable gap is dropped from the report.

---

## Output Format

Write efficiency report to: `{project-root}/artefacts/build/efficiency-report.md`

Supporting data (git logs, extracted metrics) goes to: `{project-root}/artefacts/build/efficiency-data/`

### Report Structure

```markdown
# Workflow Efficiency Report

**Cycle**: [Feature name or sprint ID]
**Period**: [Start date] to [End date]
**Analyzed by**: @harness-analyst
**Date**: [Report date]

---

## Executive Summary

- **Cycle Duration**: X days
- **Total Tasks**: N tasks completed
- **Token Usage**: Y tokens (Z% of estimate)
- **Rework Rate**: W% tasks required rework
- **Standards Adherence**: V% prompts followed protocols

**Overall Assessment**: [Excellent/Good/Fair/Poor]

---

## Detailed Metrics

### Cycle Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Cycle Duration | X days | Y days | ✅/⚠️/❌ |
| Tasks Completed | N tasks | M tasks | ✅/⚠️/❌ |
| First-time Pass Rate | P% | 80% | ✅/⚠️/❌ |
| Rework Rate | Q% | <20% | ✅/⚠️/❌ |

### Phase Breakdown

| Phase | Tasks | Duration | Token Usage | Issues |
|-------|-------|----------|-------------|--------|
| Discovery | N | X hrs | Y tokens | Z issues |
| Design | N | X hrs | Y tokens | Z issues |
| TDD Red | N | X hrs | Y tokens | Z issues |
| TDD Green | N | X hrs | Y tokens | Z issues |
| TDD Blue | N | X hrs | Y tokens | Z issues |
| Review Gate | N | X hrs | Y tokens | Z issues |
| Testing | N | X hrs | Y tokens | Z issues |
| Deployment | N | X hrs | Y tokens | Z issues |

### Agent Performance

| Agent | Invocations | Success Rate | Avg Tokens | Rework Count |
|-------|-------------|--------------|------------|--------------|
| @python-coder | N | X% | Y tokens | Z times |
| @typescript-coder | N | X% | Y tokens | Z times |
| @functional-tester | N | X% | Y tokens | Z times |
| ... | ... | ... | ... | ... |

### Standards Adherence

| Standard | Compliance Rate | Violations | Most Common Violation |
|----------|-----------------|------------|----------------------|
| Tool Usage | X% | N times | bash instead of Write/Edit |
| TDD Workflow | X% | N times | Combined RED+GREEN phases |
| Tech Stack | X% | N times | pip instead of uv |
| Parallel Planning | X% | N times | No options presented |

---

## Bottleneck Analysis

### Top 5 Bottlenecks

1. **[Bottleneck Name]** (Impact: X% time waste)
   - **Where**: [Phase/Agent]
   - **Cause**: [Root cause]
   - **Fix**: [Recommendation]

2. **[Bottleneck Name]** (Impact: Y% time waste)
   ...

---

## Repeated Issues

### Standards Violations (Repeated 3+ times)

1. **Bash used instead of Write/Edit** - 8 occurrences
   - Impact: Permission prompts, slower execution
   - Fix: Strengthen TOOL REQUIREMENTS in agent prompts

2. **npm/npx used instead of yarn/yarn dlx** - 5 occurrences
   - Impact: Inconsistent dependencies
   - Fix: Emphasize tech-standards.md reading in spawning protocol

### Rework Patterns

1. **Type hints missing** - 4 rework cycles
   - Cause: coding-standards.md not read
   - Fix: Add type checking to pre-commit hooks

---

## Token Analysis

### Token Usage Breakdown

| Category | Estimated | Actual | Efficiency |
|----------|-----------|--------|------------|
| Planning | X tokens | Y tokens | Z% |
| Implementation | X tokens | Y tokens | Z% |
| Review | X tokens | Y tokens | Z% |
| Rework | N/A | Y tokens | Waste |
| **Total** | **X tokens** | **Y tokens** | **Z%** |

### Token Waste Sources

1. **Rework cycles**: X tokens (Y% of total)
2. **Repeated prompts**: X tokens (Y% of total)
3. **Standards violations**: X tokens (Y% of total)

---

## Recommendations

### High Priority (Implement Immediately)

1. **[Recommendation]**
   - **Problem**: [Issue description]
   - **Impact**: X% efficiency gain
   - **Action**: [Specific action]
   - **Owner**: [Orchestrator/Agent/User]

### Medium Priority (Next Cycle)

1. **[Recommendation]**
   ...

### Low Priority (Future Improvement)

1. **[Recommendation]**
   ...

---

## Metrics vs Targets

Component targets (grade rows with the Scoring Rubric; no composite score):

- Cycle Efficiency: duration, velocity against plan
- Quality: first-time pass rate ≥80%, rework rate <20%
- Standards Adherence: protocol compliance, violations to zero
- Resource Efficiency: token usage vs estimate, agent efficiency

**Trend**: [Improving/Stable/Declining] compared to last cycle (cite the prior report)

---

## Next Steps

1. [ ] Review high-priority recommendations with team
2. [ ] Update agent prompts to address repeated violations
3. [ ] Schedule retrospective to discuss bottlenecks
4. [ ] Track metrics in next cycle to measure improvement

---

**Generated by**: @harness-analyst
**Report Version**: 1.0
```

---

## When to Run

Run workflow analysis:

- **Post-deployment**: After each successful deployment to production
- **Post-sprint**: After each development sprint/cycle
- **On-demand**: When user requests efficiency review
- **Quarterly**: For trend analysis across multiple cycles

---

## Constraints

- Base findings strictly on verifiable artefacts, git logs, and session records — do not speculate
- Provide actionable recommendations ranked by impact
- Do not modify source code, test files, or workflow definitions directly
- Cite specific commits, agent names, and task IDs when reporting violations
