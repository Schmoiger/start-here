# Compressed Document Formats

**Purpose**: Reduce token overhead while maintaining human readability and agent parseability.

**Principles Applied**:
- DRY: Single source of truth; reference rather than duplicate
- EARS notation: Structured requirements with clear syntax
- British English: All examples use British spelling
- Mermaid: Diagrams where visual > prose

---

## Summary: Compression Potential

| Category | Current | Target | Reduction |
|----------|---------|--------|-----------|
| Context (agents, rules, README) | 32.5 KB | 15 KB | 54% |
| Standards | 44.5 KB | 32 KB | 28% |
| Artifacts (requirements, stories, tasks, bugs) | 65 KB | 38 KB | 42% |
| **Total** | **142 KB** | **85 KB** | **40%** |

---

## 1. Agent Definition Format

### Current (verbose)

```markdown
---
name: python-coder
description: Writes production Python code
model: sonnet
allowed_tools: [Read, Write, Edit, Bash, Glob, Grep]
---

You are an expert Python developer specialising in FastAPI,
async programming, and TDD practices. You write clean,
maintainable code with comprehensive type hints.

## Context Paths

- Read architecture from `./artefacts/architecture/`
- Read requirements from `./artefacts/product/`
- Write code to `./services/{service}/src/`

## Constraints

- Use type hints on all public functions (Python 3.10+ syntax)
- Follow pytest conventions (functional-tester writes tests, you make them pass)
- Single responsibility principle per module
- Document all public APIs with docstrings
- No print statements (use structured logging)
- Handle errors explicitly (no bare except)
- Use dependency injection for testability

## Deliverables

- Production code in `./services/{service}/src/`
- Updated module README if API changes
- Validate syntax with `python -m py_compile`

## Task

{$ARGUMENTS}
```

### Compressed (human-readable, agent-parseable)

```markdown
---
name: python-coder
model: sonnet
tools: [Read, Write, Edit, Bash, Glob, Grep]
reads: [artefacts/architecture/, artefacts/product/, services/*/tests/]
writes: [services/*/src/]
---

# python-coder

Expert Python developer (FastAPI, async, TDD). Makes tests pass.

## Constraints

| Rule | Rationale |
|------|-----------|
| Type hints (3.10+ syntax) | Static analysis, IDE support |
| pytest conventions | functional-tester writes tests |
| Single responsibility/module | Maintainability |
| Docstrings on public APIs | Self-documenting |
| Structured logging (no print) | Production debugging |
| Explicit error handling | No bare except |
| Dependency injection | Testability |

## Deliverables

1. Code → `services/{service}/src/`
2. README update if API changes
3. Validate: `python -m py_compile`

## Task: {$ARGUMENTS}
```

**Reduction**: 1,149 bytes → ~650 bytes (43%)

---

## 2. Rules Format

### Current (verbose .mdc)

```markdown
---
description: Use EARS notation for requirements
globs: ["**/requirements.md", "**/user-stories.md"]
---

## Introduction

EARS (Easy Approach to Requirements Syntax) provides a structured
template for writing requirements that are clear, testable, and
unambiguous. This rule mandates EARS notation for all requirements.

## The EARS Clauses

| Clause | Keyword | Usage |
|--------|---------|-------|
| Ubiquitous | THE | Always-active behaviour |
| Event-driven | WHEN | Triggered by event |
| State-driven | WHILE | Active during state |
| Optional | IF | Feature-dependent |
| Unwanted | SHALL NOT | Prohibited behaviour |

## EARS Requirement Patterns

### Ubiquitous Requirements

**Syntax**: `THE <system> SHALL <action>`

**Example**: THE system SHALL display prices in the user's configured currency.

### Event-Driven Requirements

**Syntax**: `WHEN <trigger>, THE <system> SHALL <action>`

**Example**: WHEN the user clicks "Refresh", THE system SHALL fetch current OHLCV data.

### State-Driven Requirements

**Syntax**: `WHILE <state>, THE <system> SHALL <action>`

**Example**: WHILE the market is closed, THE system SHALL display the last closing price.

[...continues for 50+ more lines...]
```

### Compressed (reference card format)

```markdown
---
name: EARS-notation
applies: [requirements.md, user-stories.md]
---

# EARS Notation

Structured requirements syntax. All requirements MUST use EARS patterns.

## Patterns

| Type | Syntax | Example |
|------|--------|---------|
| Ubiquitous | THE {system} SHALL {action} | THE system SHALL display prices in GBP |
| Event | WHEN {trigger}, THE {system} SHALL {action} | WHEN user clicks Refresh, THE system SHALL fetch OHLCV |
| State | WHILE {state}, THE {system} SHALL {action} | WHILE market closed, THE system SHALL show last close |
| Optional | IF {condition}, THE {system} SHALL {action} | IF premium user, THE system SHALL enable alerts |
| Forbidden | THE {system} SHALL NOT {action} | THE system SHALL NOT store passwords in plaintext |

## Combining

Complex requirements chain clauses:
`WHILE {state}, WHEN {trigger}, IF {condition}, THE {system} SHALL {action}`

Example: WHILE connected, WHEN data stale, IF auto-refresh enabled, THE system SHALL fetch new data.
```

**Reduction**: 3,346 bytes → ~900 bytes (73%)

---

## 3. Requirements Format

### Current (verbose)

```markdown
## Functional Requirements

### P0: MVP Requirements

#### Data Retrieval

- [ ] **REQ-001**: Retrieve Historical Market Data
  - Priority: P0 (MVP)
  - Description: THE system SHALL retrieve historical OHLCV data for
    NYSE and LSE securities using yfinance.
  - Acceptance Criteria:
    - [ ] Fetches Open, High, Low, Close, Volume for valid tickers
    - [ ] Supports NYSE (e.g., AAPL, MSFT) and LSE (e.g., LLOY.L, BP.L)
    - [ ] Returns data within 5 seconds for standard requests
    - [ ] Implements retry logic (3 attempts with exponential backoff)
    - [ ] Gracefully handles invalid tickers with clear error message

- [ ] **REQ-002**: Support Multiple Time Horizons
  [... 20 more lines ...]
```

### Compressed (EARS + table format)

```markdown
# Requirements

## Legend
- **M** = MVP (P0), **P** = Post-MVP (P1), **F** = Future (P2)
- ✓ = complete, ○ = in progress, · = pending

## Functional Requirements

### Data Retrieval

| ID | Pri | Requirement (EARS) | Acceptance |
|----|-----|-------------------|------------|
| R-001 | M | THE system SHALL retrieve OHLCV via yfinance for NYSE/LSE | 5s response, 3 retries, invalid ticker handling |
| R-002 | M | THE system SHALL support horizons: 1w, 1m, 6m, 1y, 2y, 5y | 10s for 5yr, session persistence |
| R-003 | M | THE system SHALL cache data with 24h TTL | LRU eviction at 50MB, staleness indicator |

### Bollinger Bands

| ID | Pri | Requirement (EARS) | Acceptance |
|----|-----|-------------------|------------|
| R-004 | M | THE system SHALL calculate BB (SMA ± k×σ) | Period 5-200, σ 0.5-4.0, validates params |
| R-005 | M | THE system SHALL detect signals (touch, squeeze, expansion) | Configurable thresholds, no duplicate consecutive |

### Visualisation

| ID | Pri | Requirement (EARS) | Acceptance |
|----|-----|-------------------|------------|
| R-006 | M | THE system SHALL render interactive chart (TradingView) | Pan, zoom, crosshair, responsive |
| R-007 | M | WHEN signal detected, THE system SHALL highlight on chart | Colour-coded markers, click for details |
| R-008 | P | THE system SHALL support dark/light themes | System preference detection, manual override |
```

**Reduction**: 10,800 bytes → ~4,500 bytes (58%)

---

## 4. User Stories Format

### Current (verbose)

```markdown
### Epic 1: Security Selection & Retrieval

#### US-001: Search by Ticker Symbol
- **Priority**: P0 (MVP)
- **As a** trader
- **I want to** search for securities by ticker symbol
- **So that** I can quickly find stocks I already know

**Acceptance Criteria**:
- [ ] Search returns results within 2 seconds
- [ ] Results show ticker symbol and company name
- [ ] Supports partial ticker matching
- [ ] Shows exchange (NYSE/LSE) for each result
- [ ] Handles invalid input gracefully
```

### Compressed (structured format)

```markdown
# User Stories

## Legend
- **M** = MVP, **P** = Post-MVP, **F** = Future
- Roles: **T** = Trader, **A** = Analyst, **C** = Casual investor

## Epic 1: Security Selection

| ID | Pri | Role | Story | Acceptance |
|----|-----|------|-------|------------|
| US-001 | M | T | Search by ticker → quick find | 2s response, ticker+name, partial match, shows exchange |
| US-002 | M | C | Search by name → find without ticker | Case-insensitive, partial match, exchange shown |
| US-003 | M | T | View recent searches → quick re-access | Last 10, persisted, one-click select |
| US-004 | P | A | Filter by exchange → focus on market | NYSE/LSE/All toggle, persists preference |

## Epic 2: Bollinger Bands

| ID | Pri | Role | Story | Acceptance |
|----|-----|------|-------|------------|
| US-005 | M | T | See BB overlay → identify opportunities | Upper/middle/lower bands, colour-coded |
| US-006 | M | A | Adjust parameters → test strategies | Period/σ sliders, live update, reset to defaults |
| US-007 | M | T | See current position → know where price is | %B indicator, squeeze/expansion status |
```

**Reduction**: 16,200 bytes → ~6,500 bytes (60%)

---

## 5. Tasks Format

### Current (verbose)

```markdown
## Phase 2: TDD GREEN - Implementation

### FE-101: Project Setup and Configuration
- [ ] Create Vite project with React 18 + TypeScript
- [ ] Configure path aliases (@/ for src/)
- [ ] Set up Vitest with React Testing Library
- [ ] Configure TailwindCSS with DaisyUI
- [ ] Add environment configuration (.env.example)
- [ ] Set up ESLint + Prettier
- [ ] Create base folder structure

**Dependencies**: None
**Estimated Effort**: 2-3 hours
**Commit Protocol**: `feat(frontend): FE-101 project setup and configuration`
```

### Compressed (matrix format)

```markdown
# Tasks: Frontend

## Status: Phase 1 ✓ | Phase 2 ○ (3/20) | Phase 3 ·

## Phase 2: TDD GREEN [3/20]

| ID | Task | Status | Deps | Commit |
|----|------|--------|------|--------|
| FE-101 | Project setup (Vite, TS, Tailwind, Vitest) | ✓ | - | abc123 |
| FE-102 | Data service client | ✓ | 101 | def456 |
| FE-103 | Vis service client | ✓ | 101 | ghi789 |
| FE-104 | LLM service client | ○ | 101 | - |
| FE-105 | App shell + routing | · | 101 | - |
| FE-106 | SecuritySearch component (9 tests) | · | 102 | - |
| FE-107 | Chart component (30 tests) | · | 102,103 | - |
| FE-108 | Watchlist component (15 tests) | · | 102 | - |

## Blocked

| ID | Blocker | Owner | ETA |
|----|---------|-------|-----|
| FE-107 | Waiting for vis-service API | @python-coder | 2026-01-30 |
```

**Reduction**: 20,500 bytes → ~4,000 bytes (80%)

---

## 6. Bugs Format

### Current (verbose)

```markdown
### BacktestPanel

**Status**: [DONE] 12/17 tests passing

**Details**:
The component currently exports a placeholder that returns null.

**Expected Features** (from test file):
- Renders strategy selector dropdown
- Renders initial capital input with validation
- Renders date range picker
- Renders "Run Backtest" button
- Shows loading state during backtest
- Displays results table (trades, metrics)
- Shows equity curve chart
- Handles backtest errors gracefully

**Test File**: `src/components/BacktestPanel.test.tsx`
```

### Compressed (issue tracker format)

```markdown
# Bugs: Frontend

## Summary: 85/262 passing (32%) | 3 critical, 5 high, 12 medium

## Critical (blocks release)

| ID | Component | Issue | Tests | Fix |
|----|-----------|-------|-------|-----|
| BUG-001 | Chart | Wrong props interface | 30/77 | Split ohlcv/bands/signals props |
| BUG-002 | BacktestPanel | Returns null | 12/17 | Implement full interface |
| BUG-003 | App | Missing error boundary | 8/15 | Add ErrorBoundary wrapper |

## High (this sprint)

| ID | Component | Issue | Tests |
|----|-----------|-------|-------|
| BUG-004 | Watchlist | No drag-reorder | 15/22 |
| BUG-005 | SecuritySearch | No keyboard nav | 9/14 |
| BUG-006 | ExportButton | Missing format options | 6/11 |

## Test Gaps by Component

| Component | Passing | Total | Gap |
|-----------|---------|-------|-----|
| Chart | 30 | 77 | Legend, tooltip, zoom, a11y |
| BacktestPanel | 12 | 17 | Strategy UI, results display |
| Watchlist | 15 | 22 | Drag-drop, persistence |
| SecuritySearch | 9 | 14 | Keyboard nav, recent searches |
```

**Reduction**: 7,900 bytes → ~2,000 bytes (75%)

---

## 7. Open Questions Format

### Current (verbose)

```markdown
### ~~OQ-001~~: Commodity Support Approach [RESOLVED]

**Priority**: High (Blocking P0)
**Status**: RESOLVED
**Date**: 2026-01-27
**Owner**: @solution-architect

**Question**: How should commodities be supported - predefined list or
user-searchable? Predefined requires maintenance but offers curated
experience. User-searchable is flexible but may surface invalid symbols.

**Resolution**: User-searchable via yfinance commodity symbols.

**Rationale**:
- yfinance supports commodity futures (GC=F for gold, CL=F for crude)
- No maintenance burden for predefined lists
- Users can discover commodities through search
- Invalid symbols handled by existing error handling

**Implementation Notes**:
- Search endpoint already supports commodity symbols
- No code changes required
- Document supported commodity format in user guide
```

### Compressed (decision log format)

```markdown
# Open Questions

## Status: 9 resolved, 0 open, 3 deferred

## Resolved

| ID | Question | Decision | Date |
|----|----------|----------|------|
| OQ-001 | Commodity support: predefined vs searchable? | Searchable via yfinance (GC=F, CL=F) | 2026-01-27 |
| OQ-002 | LLM provider? | P1: Ollama (local) → P2: OpenAI/Anthropic (cloud) | 2026-01-27 |
| OQ-003 | Squeeze/expansion thresholds? | Configurable: squeeze <20th %ile, expansion >80th %ile | 2026-01-27 |
| OQ-004 | Storage format? | JSON (Bronze/Silver), computed on-demand (Gold) | 2026-01-27 |
| OQ-005 | Cache strategy? | LRU, 50MB limit, 24h TTL, stale-while-revalidate | 2026-01-27 |

## Deferred (P2)

| ID | Question | Reason |
|----|----------|--------|
| OQ-010 | Real-time streaming? | Requires WebSocket infra; revisit for P2 |
| OQ-011 | Mobile app? | Focus on responsive web first |
| OQ-012 | Social features? | Out of scope for trading tool |
```

**Reduction**: 5,400 bytes → ~1,200 bytes (78%)

---

## 8. Standards Format (Single Source of Truth)

### Problem: Duplication

Current standards have significant overlap:
- Handoffs defined in BOTH agent-standards.md AND doc-standards.md
- Worktree workflows repeated with slight variations
- Testing standards partially duplicated in coding-standards.md

### Solution: Modular References

```markdown
# agent-standards.md (compressed)

## Behaviour

1. **Plan first**: Outline approach before coding
2. **Stay in lane**: Only modify files in your `writes:` paths
3. **Handoffs**: See [HANDOFF-FORMAT.md](./HANDOFF-FORMAT.md)
4. **Worktrees**: See [worktree-guide.md](./worktree-guide.md)

## Context Loading

```mermaid
graph LR
    A[Read CLAUDE.md] --> B[Load agent def]
    B --> C[Read context paths]
    C --> D[Execute task]
    D --> E[Write deliverables]
    E --> F[Create handoff]
```

[Rest of essential content without duplication]
```

**Reduction**: 16,000 bytes → ~6,000 bytes (62%)

---

## 9. Unified Context Index

Replace verbose README.md with concise index:

```markdown
# Context Index

## Structure

```
context/
├── agents/          # WHO: Role definitions
├── standards/       # HOW: Process standards
├── rules/           # WHAT: Constraints (EARS, DRY, British English)
└── mcp/             # TOOLS: External capabilities
```

## Quick Reference

| Need | File | Key Content |
|------|------|-------------|
| Agent behaviour | agent-standards.md | Planning, boundaries, handoffs |
| Code patterns | coding-standards.md | Python/TS conventions, commits |
| Testing | testing-standards.md | TDD cycle, coverage, anti-patterns |
| Documentation | doc-standards.md | Artifact types, decision criteria |
| Requirements syntax | rules/EARS-notation.mdc | EARS patterns |
| Avoid AI slop | rules/detecting-ai-slop.mdc | Checklist |

## Framework Adaptation

| Framework | Load Method | Notes |
|-----------|-------------|-------|
| Claude Code | `@agent-name` | Native support |
| Cursor | `.cursorrules` include | Copy .mdc to .cursor/ |
| Aider | `--message` prepend | Include agent def |
| LangChain | Load → system_message | Map frontmatter to config |
| CrewAI | Agent() from YAML | role→backstory, tools→tools |
```

**Reduction**: 13,311 bytes → ~1,500 bytes (89%)

---

## Implementation Checklist

1. [ ] Create compressed templates in `context/standards/templates/`
2. [ ] Migrate agent definitions to new format
3. [ ] Consolidate rules into reference cards
4. [ ] Remove duplication between standards files
5. [ ] Convert verbose artefacts to table format
6. [ ] Update CLAUDE.md to reference compressed formats
7. [ ] Validate agents can still parse new formats

## Migration Notes

- Keep verbose versions as `*.verbose.md` for reference
- New format is the source of truth
- Agents should prefer compressed format
- Human reviewers can request verbose expansion if needed
