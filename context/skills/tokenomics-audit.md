---
name: tokenomics-audit
description: Micro analysis lens for @harness-analyst — agent effectiveness, token economics, context efficiency, model-tier conformance vs context/models.yaml, autonomy rate, and tokenomics report format.
globs: ["context/models.yaml", "artefacts/build/**"]
---

# Tokenomics Audit Skill

---

## Overview

The micro lens of `@harness-analyst` (`context/agents/harness-analyst.md`). It audits how efficiently agents consume tokens, adhere to model tiering, manage context windows, and deliver value across development cycles. The macro lens (workflow flow, handoffs, cycle times) lives in `workflow-analysis.md`. Telemetry inputs are listed in the agent's Shared Data-Source Inventory; this skill defines what to extract from them.

---

## Model Intent & Telemetry Lookup Table (LUT)

Consult **{project-root}/context/models.yaml** for:
- Abstract intent tiers (`small`, `medium`, `large`) and their provider model mappings (Anthropic Claude, Google Gemini, OpenAI Codex)
- Guidelines for token budgets and typical tasks per tier
- Runtime-specific telemetry sources (Git trailers, Claude JSONL & Managed Agents Dreams, Antigravity transcripts)

---

## Audit Lenses

Evaluate agent executions through six core lenses:

### 1. Context & Ingestion Efficiency
- **Over-ingestion**: Were entire files loaded when targeted slices (`StartLine`/`EndLine`) or search patterns (`grep_search`) were sufficient?
- **Redundant reads**: Did an agent re-read the same unchanged standards, rules, or source files repeatedly within a session?
- **Rule resolution compliance**: Did the orchestrator inject unnecessary rules, bloating the agent's prompt context?
- **Budget violation**: Did the orchestrator exceed its context budget (>2 files read or >50 lines written) instead of delegating to a specialised subagent?

### 2. Generation & Output Density
- **Prose-to-code ratio**: Did the agent generate bloated conversational filler, verbose apologies, or redundant recaps?
- **Lean code adherence**: Is the code lean and dense (per `coding-standards.md`), avoiding premature abstractions, speculative features, or dead code?
- **Surgical edits vs full rewrites**: Did the agent use precise chunk replacements (`replace_file_content`) or expensively rewrite entire files?

### 3. Rework & Failure Churn
- **Banned tool attempts**: Did the agent waste tokens trying bash for file operations (`cat`, `echo`, `sed`) or prohibited package managers (`pip`, `npm`, `npx`) before being corrected?
- **Rule amnesia**: Did the agent fail basic repository invariants (e.g. British English spelling, conventional commits, EARS notation), causing avoidable review rejection cycles?
- **Gate bounces**: Did deliverables fail tech-lead or test gates, requiring multi-turn corrective loops?

### 4. Model Tiering & Sizing Economics
- **Intent vs capability**: Using `context/models.yaml`, check whether tasks assigned to `large` (e.g. Opus / Gemini Ultra) could have been executed equally well on `medium` (Sonnet / Gemini Pro) or `small` (Haiku / Gemini Flash).
- **Over-provisioning**: Were simple smoke checks, UI tests, or command runners dispatched with expensive reasoning models?
- **Under-provisioning**: Were delicate architectural decompositions dispatched to models without sufficient reasoning depth, triggering rework?

### 5. Autonomy & Human Cost
- **Autonomy rate**: What percentage of commits achieved full autonomy (`dispatch=orchestrator interactions=0 approvals=0`)?
- **Unnecessary interruptions**: Did the agent prompt the user with trivial questions or ask permission for read-only / sandboxed operations?

### 6. Token Yield / ROI
- **Functional yield**: How many net clean lines of code, test cases, or specification artefacts were delivered per 1,000 tokens consumed?
- **Waste percentage**: What proportion of total tokens was consumed by failed attempts, retries, and corrections?

---

## Audit Workflow

1. Read the agent definition `context/agents/harness-analyst.md` and all required standards.
2. Read `context/models.yaml` to load model intent mappings and runtime telemetry paths.
3. Parse git log for `Agent-Session:` trailers over the target commit range or sprint.
4. If available, inspect platform-specific session traces (Claude JSONL, Dreams, Antigravity transcripts).
5. Cross-reference actual token consumption against task estimates in `tasks*.md`.
6. Calculate core metrics:
   - Total token spend (Input vs Output).
   - Cost distribution by agent role and workflow phase.
   - Autonomy rate (% zero-interaction commits).
   - Rework and churn token overhead.
   - Model tiering alignment (violations of `small`/`medium`/`large` guidance).
7. Synthesise concrete, actionable interventions:
   - Specific prompt templates to trim.
   - Rules to clarify or promote to pre-commit checks.
   - Model tier adjustments for subagent dispatch.
   - File reading patterns to replace with targeted slices or grep.
8. Produce `{project-root}/artefacts/build/tokenomics-report.md`.
9. Report findings back to the orchestrator.

---

## Report Format

Write the report to: `{project-root}/artefacts/build/tokenomics-report.md`

```markdown
# Agent Effectiveness & Tokenomics Report

**Cycle/Scope**: [Sprint ID, Feature Name, or Commit Range]
**Period**: [Start date] to [End date]
**Audited by**: @harness-analyst
**Date**: [Report date]

---

## 1. Executive Summary

- **Total Token Spend**: X.X M tokens (Input: X.X M | Output: X.X K)
- **Token Efficiency vs Estimate**: X% of budget
- **Autonomy Rate**: X% (commits with 0 human interactions)
- **Rework & Churn Waste**: Estimated X K tokens (X% of total spend)
- **Model Tiering Alignment**: X% compliance with `context/models.yaml`

---

## 2. Agent Effectiveness Scorecard

| Agent | Invocations | Tier (Declared / Actual) | Avg In / Out Tokens | Autonomy Rate | Churn Rate | Cost Rating |
|-------|-------------|-------------------------|---------------------|---------------|------------|-------------|
| @python-coder | N | medium / Sonnet | 45K / 2.1K | 85% | 10% | Optimal |
| @ui-tester | N | small / Haiku | 18K / 0.8K | 95% | 5% | Optimal |
| @tech-lead | N | medium / Sonnet | 62K / 1.5K | 100% | 0% | Optimal |

---

## 3. Token Waste Audit

### A. Context & Ingestion Waste
- [Observation with file:line and token impact]

### B. Output & Generation Bloat
- [Observation with file:line and token impact]

### C. Tool & Rule Violations
- [Observation with file:line and token impact]

### D. Model Misallocations
- [Instances where high-cost tiers were used for low-complexity tasks]

---

## 4. Actionable Interventions

### Immediate (High Impact)
1. **[Intervention Title]**:
   - **Root Cause**: [Why tokens were wasted]
   - **Remedy**: [Exact change to rule, prompt template, or agent definition]
   - **Expected Token Saving**: [Estimated reduction]

### Systemic (Medium Impact)
1. **[Intervention Title]**:
   - **Remedy**: [...]

---

## 5. Next Steps

1. [ ] Discuss findings with team / human during continuous improvement review gate
2. [ ] Apply prompt and rule refinements
3. [ ] Track token delta in subsequent sprint
```

---

## Constraints

- Only report actionable interventions tied to concrete evidence — no vanity metrics or abstract scores without fixable gaps
- Ground all findings in specific file:line references, git commit SHAs, or session trace markers
- Adhere strictly to British English spelling (`tech-writing.md` §1)
- Consult `context/models.yaml` as the canonical reference for abstract model intent tiers (small, medium, large)
- Do not modify source code or tests directly; recommendations must be presented for human review or delegated to appropriate agents
