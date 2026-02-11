# Workflow Analyst Usage Guide

## Overview

The `@workflow-analyst` agent measures and improves your agentic development workflow by analyzing completed work cycles for efficiency, bottlenecks, and improvement opportunities.

## When to Use

### 1. Post-Deployment Analysis (Recommended)
After successful deployment to production:
```
@workflow-analyst Analyze the workflow for [feature-name] deployment

Cycle period: [start-date] to [end-date]
Focus areas: Overall efficiency, standards adherence, token usage
```

### 2. Mid-Cycle Health Check
During development to catch issues early:
```
@workflow-analyst Run mid-cycle efficiency check

Cycle period: [start-date] to today
Focus: Bottlenecks in current phase, repeated violations
```

### 3. Quarterly Trend Analysis
Every 3 months to track improvement:
```
@workflow-analyst Analyze trends across last 3 months

Compare cycles: [cycle1, cycle2, cycle3]
Focus: Long-term improvements, persistent issues
```

### 4. Troubleshooting
When workflow feels inefficient:
```
@workflow-analyst Investigate current workflow inefficiency

Symptoms: [slow reviews, repeated rework, high token usage]
Focus: Root cause analysis
```

## What It Analyzes

### Data Sources

1. **Task Files**
   - `artefacts/build/tasks.md` - System-wide tasks
   - `{service}/artefacts/tasks.md` - Service-specific tasks
   - Metrics: Task count, completion time, blocked tasks, rework tasks

2. **Handoff Files**
   - `{service}/HANDOFF.md` - Intra-domain handoffs
   - `artefacts/shared/handoffs/*.md` - Inter-domain handoffs
   - Metrics: Handoff completeness, blocked handoffs, handoff timing

3. **Git History**
   - Commit log analysis
   - Metrics: Commit count, commits per agent, rework commits, branch churn

4. **Conversation History**
   - Agent invocations
   - Repeated prompts
   - Standards violations

5. **Token Usage**
   - Estimated vs actual tokens
   - Token distribution by phase
   - Token waste sources

## Key Metrics Produced

### Efficiency Metrics
- **Cycle Duration**: Total time from discovery to deployment
- **Task Velocity**: Tasks completed per day
- **First-time Pass Rate**: % tasks passing review first time
- **Token Efficiency**: Actual/estimated ratio

### Quality Metrics
- **Rework Rate**: % tasks requiring rework
- **Standards Adherence Rate**: % prompts following protocols
- **Test Coverage**: Actual vs target coverage

### Waste Metrics
- **Rework Cycles**: Times returned from review-gate
- **Repeated Prompts**: Same correction given multiple times
- **Tool Violations**: Standards violations count

### Health Score
- Overall score: 0-100
- Component scores: Efficiency, Quality, Standards, Resources
- Trend: Improving/Stable/Declining

## Output

**Primary Report**: `artefacts/build/efficiency-report.md`

Contains:
- Executive Summary (key metrics, overall assessment)
- Detailed Metrics (cycle, phase, agent, standards)
- Bottleneck Analysis (top 5 issues with fixes)
- Repeated Issues (patterns requiring attention)
- Token Analysis (usage breakdown, waste sources)
- Recommendations (prioritized action items)
- Workflow Health Score (0-100 with trend)
- Next Steps (actionable checklist)

**Supporting Data**: `artefacts/build/efficiency-data/`
- Git logs
- Extracted metrics
- Raw analysis data

## Example Invocation

```
@workflow-analyst Analyze workflow efficiency for authentication feature

BEFORE starting, read these standards:
1. context/standards/workflow-standards.md
2. context/standards/agent-standards.md
3. context/standards/doc-standards.md

Cycle details:
- Feature: User authentication with Google Sign-In
- Period: 2026-01-15 to 2026-01-22 (7 days)
- Deployment: Completed successfully to production

Data sources to analyze:
- artefacts/build/tasks.md
- services/auth-service/HANDOFF.md
- Git history since 2026-01-15
- Conversation history (this session)

Focus areas:
1. Standards adherence (tool usage, TDD workflow)
2. Token efficiency (actual vs estimated)
3. Bottlenecks in review phase (multiple rework cycles observed)
4. Repeated prompt patterns

Output: artefacts/build/efficiency-report.md
```

## Interpreting Results

### Health Score Ranges

| Score | Assessment | Action |
|-------|------------|--------|
| 90-100 | Excellent | Maintain current practices |
| 75-89 | Good | Minor optimizations needed |
| 60-74 | Fair | Address top 3 bottlenecks |
| 0-59 | Poor | Major process improvements required |

### Common Bottlenecks and Fixes

**Bottleneck**: High rework rate (>30%)
**Fix**: Strengthen pre-spawn checklist enforcement, add more examples to agent prompts

**Bottleneck**: Tool violations (bash instead of Write/Edit)
**Fix**: Add TOOL REQUIREMENTS block to every agent spawn (Protocol 1)

**Bottleneck**: TDD phases combined
**Fix**: Use TDD Workflow Enforcement protocol with separate phase prompts (Protocol 2)

**Bottleneck**: Long review cycles
**Fix**: Improve agent prompts with standards context upfront, reduce rework

**Bottleneck**: Token overruns (>120% of estimate)
**Fix**: Use parallel execution less, reduce context duplication, fix repeated prompts

## Integration with Workflow

### Option A: Add to Default Workflow (Automatic)

Edit `context/workflows/default.yaml`:
```yaml
  - id: deployment-review
    name: Deployment Review
    ... existing phase ...

  - id: retrospective  # NEW
    name: Workflow Efficiency Analysis
    depends_on: [deployment-review]
    optional: true
    agents:
      - workflow-analyst
    outputs:
      - artefacts/build/efficiency-report.md
    validation:
      - All data sources analyzed
      - Metrics calculated
      - Recommendations provided
```

Then regenerate AGENTS.md:
```bash
uv run --with pyyaml python context/scripts/generators/generate_claude_md.py --workflow default
```

### Option B: Run On-Demand (Manual)

Keep it as a standalone agent, invoke when needed:
```
@workflow-analyst [analysis request]
```

## Continuous Improvement Loop

1. **Deploy feature** → Run @workflow-analyst
2. **Review efficiency report** → Identify top 3 issues
3. **Update prompts/protocols** → Address repeated violations
4. **Next cycle** → Compare metrics, track improvement
5. **Quarterly review** → Long-term trend analysis

## Tips for Better Analysis

1. **Provide complete cycle dates** - Include exact start/end timestamps
2. **Specify focus areas** - Guide analysis to specific concerns
3. **Include context** - Mention known issues or unusual circumstances
4. **Compare to baselines** - Reference previous cycle metrics if available
5. **Act on recommendations** - Don't just collect data, implement fixes

## Metrics to Track Over Time

Create a tracking file: `artefacts/build/workflow-metrics-history.csv`

```csv
Cycle,Date,Duration_Days,Tasks,Token_Efficiency,Rework_Rate,Health_Score
auth-v1,2026-01-22,7,12,95%,15%,82
payments-v1,2026-02-05,5,8,88%,25%,78
...
```

Use this to track improvement trends across cycles.

## Advanced Usage

### Custom Focus Analysis

Request specific deep-dive:
```
@workflow-analyst Deep-dive analysis on TDD workflow adherence

Focus ONLY on:
- TDD phase separation (RED/GREEN/BLUE)
- Test modifications during GREEN phase
- Refactoring discipline in BLUE phase

Provide detailed breakdown per agent and recommendations for TDD enforcement.
```

### Comparative Analysis

Compare multiple cycles:
```
@workflow-analyst Compare efficiency across last 3 deployments

Cycles: auth-v1, payments-v1, dashboard-v1
Identify: Improvements, degradations, persistent issues
```

### Real-time Monitoring

Mid-cycle health check:
```
@workflow-analyst Quick health check (we're in tdd-green phase)

Current concerns:
- Lots of rework from review-gate
- Token usage seems high
- Repeated prompts about tool usage

Quick assessment and immediate recommendations only.
```

## Questions?

See:
- Agent definition: `context/agents/workflow-analyst.md`
- Workflow integration: `context/workflows/retrospective-addon.yaml`
- Standards context: `context/standards/workflow-standards.md`
