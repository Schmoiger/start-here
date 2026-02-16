# Workflow Diagrams

Visual comparison of all available workflows.

---

## Default Workflow (Full TDD)

**14 phases | 3 quality gates | 18 agents | 2-3 days**

```mermaid
flowchart TD
    start([Start]) --> discovery

    subgraph discovery["🔍 Discovery (30min)"]
        pe["@product-expert<br/>Clarify requirements"]
        po["@product-owner<br/>Write formal requirements"]
        pe --> po
    end

    discovery --> design

    subgraph design["🎨 Design (1-2h)"]
        sa["@solution-architect<br/>Architecture"]
        dd["@database-designer<br/>Schema"]
        ad["@api-designer<br/>API spec"]
        ud["@ui-designer<br/>Components"]
        vd["@visual-designer<br/>Visuals"]
    end

    design --> design_review

    subgraph design_review["🚦 Design Review Gate (1h)"]
        dr1["@tech-lead<br/>APPROVE"]
        dr2["@code-reviewer<br/>Feasibility"]
        dr3["@principles-reviewer<br/>LESS principles"]
        dr4["@visual-designer<br/>Design consistency"]
        dr5["@security-tester<br/>Security"]
        dr1 --> dr2 --> dr3 --> dr4 --> dr5
    end

    design_review --> tdd_red

    subgraph tdd_red["🔴 TDD RED (1h)"]
        ft1["@functional-tester<br/>Write failing tests"]
    end

    tdd_red --> tdd_green

    subgraph tdd_green["🟢 TDD GREEN (2-4h)"]
        pc1["@python-coder<br/>Backend implementation"]
        tc1["@typescript-coder<br/>Frontend implementation"]
    end

    tdd_green --> tdd_blue

    subgraph tdd_blue["🔵 TDD BLUE (1h)"]
        pc2["@python-coder<br/>Backend refactor"]
        tc2["@typescript-coder<br/>Frontend refactor"]
    end

    tdd_blue --> testing

    subgraph testing["🧪 Testing (1h)"]
        ft2["@functional-tester<br/>Unit tests"]
        ft3["@functional-tester<br/>Integration tests"]
        ut["@ui-tester<br/>E2E tests + screenshots"]
        ft2 --> ft3 --> ut
    end

    testing --> quality_review

    subgraph quality_review["🚦 Quality Review Gate (1h+)"]
        qr1["@tech-lead<br/>APPROVE"]
        qr2["@code-reviewer<br/>Code quality"]
        qr3["@principles-reviewer<br/>LESS principles"]
        qr4["@visual-designer<br/>UI standards"]
        qr5["@security-tester<br/>Security"]
        qr1 --> qr2 --> qr3 --> qr4 --> qr5
    end

    quality_review --> docs

    subgraph docs["📝 Docs (30min)"]
        doc["@documentation<br/>Update docs, archive artefacts"]
    end

    docs --> deployment

    subgraph deployment["🚀 Deployment (1h)"]
        gcp["@gcp-devops<br/>Deploy to staging"]
    end

    deployment --> deployment_review

    subgraph deployment_review["🚦 Deployment Review Gate"]
        tl["@tech-lead<br/>Review deployment"]
    end

    deployment_review --> retro

    subgraph retro["📊 Retrospective (30min, optional)"]
        wa["@workflow-analyst<br/>Efficiency analysis"]
    end

    retro --> finish([Complete])

    classDef gateStyle fill:#ff6b6b,stroke:#c92a2a,stroke-width:3px
    classDef optionalStyle fill:#e9ecef,stroke:#868e96,stroke-dasharray: 5 5

    class design_review,quality_review,deployment_review gateStyle
    class retro optionalStyle
```

**Coverage thresholds**:
- Development (quality-review): 95%
- Pre-deployment (deployment-review): 97%

**Quality gates block progress** until criteria met.

---

## Prototype Workflow (Fast Iteration)

**4 phases | 0 quality gates | 5 agents | Hours to 1 day**

```mermaid
flowchart TD
    start([Start]) --> plan

    subgraph plan["📝 Quick Plan (15min)"]
        po["@product-owner<br/>Minimal requirements<br/>(hypothesis to test)"]
    end

    plan --> sketch

    subgraph sketch["✏️ Minimal Design (30min)"]
        sa["@solution-architect<br/>High-level architecture<br/>(skip detailed specs)"]
    end

    sketch --> build

    subgraph build["⚡ Build Prototype (2-4h)"]
        pc["@python-coder<br/>Backend prototype"]
        tc["@typescript-coder<br/>Frontend prototype"]
    end

    build --> validate

    subgraph validate["✅ Smoke Test (30min, optional)"]
        ft["@functional-tester<br/>Happy path only<br/>(manual OK)"]
    end

    validate --> finish([Complete<br/>⚠️ Not production-ready])

    classDef optionalStyle fill:#e9ecef,stroke:#868e96,stroke-dasharray: 5 5
    classDef warningStyle fill:#fff9db,stroke:#f59f00,stroke-width:2px

    class validate optionalStyle
    class finish warningStyle
```

**⚠️ Warning**: Prototype code should NOT go to production. If successful, rewrite with default workflow.

**Trade-offs**:
- ✅ Fast: Hours vs days
- ✅ Proves concept quickly
- ❌ No tests (optional smoke tests only)
- ❌ No reviews (quality/security gaps)
- ❌ Technical debt acceptable
- ❌ Must rewrite for production

---

## Agent Effectiveness Analysis (Addon)

**1 phase | Can attach to any workflow | 30min**

```mermaid
flowchart TD
    start([Trigger:<br/>After deployment<br/>OR on-demand]) --> collect

    subgraph collect["📊 Data Collection"]
        tasks["Read tasks.md<br/>(phase durations)"]
        handoffs["Read handoffs/<br/>(handoff quality)"]
        git["Read git log<br/>(commit patterns)"]
        conv["Analyze conversation<br/>(tool usage, spawning)"]
    end

    collect --> analyze

    subgraph analyze["🔍 Analysis"]
        metrics["Calculate metrics:<br/>- Phase duration vs targets<br/>- Review rejection rate<br/>- Handoff completeness<br/>- Tool usage efficiency<br/>- Rework rate"]
        bottlenecks["Identify top 3-5<br/>bottlenecks"]
        trends["Compare to previous<br/>cycles (if available)"]
        health["Calculate workflow<br/>health score (0-100)"]

        metrics --> bottlenecks
        bottlenecks --> trends
        trends --> health
    end

    analyze --> output

    subgraph output["📄 Outputs"]
        report["efficiency-report.md<br/>(executive summary,<br/>recommendations)"]
        data["efficiency-data/<br/>(raw JSON for<br/>trend tracking)"]
    end

    output --> finish([Complete])

    classDef dataStyle fill:#d3f9d8,stroke:#37b24d
    classDef analyzeStyle fill:#fff3bf,stroke:#fab005
    classDef outputStyle fill:#d0ebff,stroke:#228be6

    class collect dataStyle
    class analyze analyzeStyle
    class output outputStyle
```

**Use cases**:
1. **Post-deployment retrospective** - After deployment-review gate
2. **Mid-cycle health check** - During any workflow phase (on-demand)
3. **Trend analysis** - Compare efficiency across cycles

**Agent**: `@workflow-analyst`

**Outputs**:
- Health score (90-100: Excellent, 70-89: Good, 50-69: Fair, <50: Poor)
- Top bottlenecks with actionable recommendations
- Phase-by-phase breakdown
- Trend comparison (if previous data exists)

---

## Workflow Comparison Matrix

```mermaid
graph LR
    subgraph comparison[" "]
        default["<b>Default</b><br/><br/>14 phases<br/>3 gates<br/>95-97% coverage<br/>2-3 days<br/><br/>✅ Production<br/>✅ Quality critical<br/>✅ Team collaboration"]

        prototype["<b>Prototype</b><br/><br/>4 phases<br/>0 gates<br/>Optional coverage<br/>Hours-1 day<br/><br/>✅ POCs<br/>✅ Experiments<br/>❌ Production"]

        effectiveness["<b>Effectiveness</b><br/><br/>1 phase<br/>Addon<br/>N/A coverage<br/>30 min<br/><br/>✅ Retrospectives<br/>✅ Health checks<br/>✅ Optimization"]
    end

    classDef defaultStyle fill:#d3f9d8,stroke:#37b24d,stroke-width:3px
    classDef prototypeStyle fill:#fff3bf,stroke:#fab005,stroke-width:3px
    classDef effectivenessStyle fill:#d0ebff,stroke:#228be6,stroke-width:3px

    class default defaultStyle
    class prototype prototypeStyle
    class effectiveness effectivenessStyle
```

---

## Decision Tree: Which Workflow?

```mermaid
flowchart TD
    start{What are you building?} -->|Testing hypothesis<br/>POC / Experiment| prototype[Use PROTOTYPE]
    start -->|Production feature<br/>Long-term code| production{Quality critical?}

    production -->|Yes:<br/>Financial, Security,<br/>Healthcare| default[Use DEFAULT]
    production -->|Medium:<br/>Internal tools| consider{Time constraint?}

    consider -->|Tight deadline| risk{Accept risk?}
    risk -->|Yes| prototype
    risk -->|No| default
    consider -->|Normal timeline| default

    start -->|Analyzing workflow<br/>efficiency| effectiveness[Add EFFECTIVENESS<br/>to any workflow]

    prototype --> promote{Promote to<br/>production?}
    promote -->|Yes| rewrite[⚠️ REWRITE<br/>with DEFAULT<br/>workflow]
    promote -->|No| archive[Archive<br/>prototype]

    classDef defaultStyle fill:#d3f9d8,stroke:#37b24d,stroke-width:3px
    classDef prototypeStyle fill:#fff3bf,stroke:#fab005,stroke-width:3px
    classDef effectivenessStyle fill:#d0ebff,stroke:#228be6,stroke-width:3px
    classDef warningStyle fill:#ff8787,stroke:#c92a2a,stroke-width:3px

    class default,rewrite defaultStyle
    class prototype,archive prototypeStyle
    class effectiveness effectivenessStyle
```

---

## Orchestration Patterns (Used Across Workflows)

```mermaid
flowchart TD
    subgraph single["1️⃣ Single Agent"]
        s1["One agent<br/>handles task<br/>end-to-end"]
    end

    subgraph sequential["2️⃣ Sequential Chain"]
        c1["Agent A"] --> c2["Agent B"] --> c3["Agent C"]
        c1b["Output of A<br/>feeds into B"]
    end

    subgraph parallel["3️⃣ Parallel Swarm"]
        p1["Agent A<br/>(independent)"]
        p2["Agent B<br/>(independent)"]
        p3["Agent C<br/>(independent)"]
        p4["All spawn<br/>simultaneously"]
    end

    subgraph hive["4️⃣ Hive"]
        h1["Agent A<br/>(shared context)"]
        h2["Agent B<br/>(shared context)"]
        h3["Shared artifacts:<br/>tests, schema, API"]
    end

    subgraph iterative["5️⃣ Iterative Loop"]
        i1["Agent A<br/>produces work"] --> i2{Reviewer<br/>approves?}
        i2 -->|No| i1
        i2 -->|Yes| i3["Proceed"]
    end

    classDef patternStyle fill:#e9ecef,stroke:#495057,stroke-width:2px

    class single,sequential,parallel,hive,iterative patternStyle
```

**Pattern usage in workflows**:

| Pattern | Default Workflow | Prototype Workflow |
|---------|------------------|-------------------|
| Single Agent | docs-cleanup, retrospective | quick-plan, sketch-design |
| Sequential Chain | discovery, testing phases, review gates | All phases (linear) |
| Parallel Swarm | design (5 designers) | build (2 coders) |
| Hive | tdd-green, tdd-blue (shared tests) | build (shared prototype) |
| Iterative Loop | quality gates (with feedback) | None (no gates) |

See `orchestration-patterns.md` for detailed examples, token optimization strategies, and decision tree.

---

## See Also

- **Workflow definitions**: `context/workflows/*.yaml`
- **Usage guides**: `context/docs/workflow-*.md`
- **Orchestration patterns**: `context/docs/orchestration-patterns.md`
- **Generated reference**: `AGENTS.md` (auto-generated, always up-to-date)
