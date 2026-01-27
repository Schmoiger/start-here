# Model Recommendations by Agent

This guide recommends which Claude model to use for each agent based on task complexity, reasoning requirements, and cost optimization.

## Model Tiers

| Model | Best For | Cost | Speed |
|-------|----------|------|-------|
| **Opus** | Complex reasoning, architecture decisions, nuanced judgment | $$$ | Slower |
| **Sonnet** | Most coding tasks, reviews, structured outputs | $$ | Medium |
| **Haiku** | Simple transformations, templated outputs, fast iteration | $ | Fast |

---

## Recommendations by Agent

### Phase 0: Discovery

| Agent | Model | Rationale |
|-------|-------|-----------|
| **product-owner** | **Sonnet** | Requires understanding nuance, prioritization judgment, translating vague ideas into structured requirements. Not Opus because output format is well-defined. |

### Phase 1: Design

| Agent | Model | Rationale |
|-------|-------|-----------|
| **solution-architect** | **Opus** | Critical decisions with long-term impact. Needs to weigh trade-offs, consider edge cases, make technology choices. Worth the cost. |
| **database-designer** | **Sonnet** | Schema design follows patterns. Complex enough to need good reasoning but well-constrained domain. |
| **api-designer** | **Sonnet** | OpenAPI generation is structured. Needs consistency and good examples but not deep reasoning. |
| **ui-designer** | **Sonnet** | Design systems require creativity within constraints. Component specs are detailed but templated. |
| **visual-designer** | **Haiku** | Mostly prompt crafting and tool operation. Translates existing specs into prompts for other tools. |

### Phase 2: Development

| Agent | Model | Rationale |
|-------|-------|-----------|
| **python-coder** | **Sonnet** | Core coding task. Needs good code quality but working within defined architecture. |
| **typescript-coder** | **Sonnet** | Same as Python. Sonnet handles TypeScript well. |

### Phase 3: Review

| Agent | Model | Rationale |
|-------|-------|-----------|
| **tech-lead** | **Opus** | Judgment calls on architecture compliance. Needs to catch subtle issues and make approval decisions. High-stakes gate. |
| **code-reviewer** | **Sonnet** | Bug finding is pattern-based. Sonnet catches most issues. Could upgrade to Opus for security-critical code. |

### Phase 4: Testing

| Agent | Model | Rationale |
|-------|-------|-----------|
| **functional-tester** | **Sonnet** | Test writing requires understanding code intent. Good coverage needs reasoning about edge cases. |
| **ui-tester** | **Haiku** | Mostly following test scripts and reporting results. Straightforward execution. |
| **security-tester** | **Opus** | Security requires adversarial thinking, understanding attack vectors, subtle vulnerability detection. Critical domain. |

### Phase 5: Deploy

| Agent | Model | Rationale |
|-------|-------|-----------|
| **gcp-devops** | **Sonnet** | Terraform is structured. Needs to understand requirements but follows IaC patterns. |

### Phase 6: Documentation

| Agent | Model | Rationale |
|-------|-------|-----------|
| **documentation** | **Haiku** | Mostly extracting and reformatting existing content. Templates are well-defined. Fast iteration helpful. |

---

## Summary Table

| Model | Agents | Count |
|-------|--------|-------|
| **Opus** | solution-architect, tech-lead, security-tester | 3 |
| **Sonnet** | product-owner, database-designer, api-designer, ui-designer, python-coder, typescript-coder, code-reviewer, functional-tester, gcp-devops | 9 |
| **Haiku** | visual-designer, ui-tester, documentation | 3 |

---

## Cost Optimization Tips

1. **Start with Haiku, upgrade if needed**: For iteration-heavy tasks, start with Haiku and upgrade if quality is insufficient.

2. **Use Opus for gates**: The review phase is a gate—investing in Opus here catches issues before expensive testing.

3. **Haiku for high-volume**: Documentation and visual asset generation involve many small tasks. Haiku's speed helps.

4. **Sonnet is the workhorse**: Most coding and design tasks are well-served by Sonnet's balance of capability and cost.

5. **Context matters**: If your project is security-critical, consider upgrading code-reviewer and functional-tester to Opus.

---

## Configuring Models in Agent Files

Add a `model` field to the frontmatter:

```yaml
---
name: solution-architect
description: ...
model: opus
allowed_tools:
  - Read
  - Write
  ...
---
```

Valid values: `opus`, `sonnet`, `haiku`

If not specified, defaults to `sonnet`.
