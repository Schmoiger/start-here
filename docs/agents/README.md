# Claude Code Multi-Agent Orchestration Setup

You've got everything needed to run six specialised agents in Claude Code. This uses Claude's native subagent system, not external frameworks.

## What You Have

### Subagent Definitions (`.md` files for Claude Code)
- `python-coder.md` - Python development
- `typescript-coder.md` - TypeScript development
- `functional-tester.md` - Testing (pytest + vitest/jest)
- `ui-tester.md` - UI testing with Chrome DevTools
- `security-tester.md` - Security audits and threat modelling
- `gcp-devops.md` - Infrastructure-as-code with Terraform

### Knowledge Base
- `CLAUDE.md` - Condensed guide for agent coordination (copy this into your project!)

### Utilities
- `coordinate.sh` - Helper script for initialising agent directories
- `*.prompty` files - Legacy prompty format (for reference; Claude Code uses `.md` files instead)

## How to Set Up

### Step 1: Copy subagent files to your project
Place all `.md` files into your project's `.claude/agents/` directory:

```bash
mkdir -p your-project/.claude/agents
cp python-coder.md your-project/.claude/agents/
cp typescript-coder.md your-project/.claude/agents/
cp functional-tester.md your-project/.claude/agents/
cp ui-tester.md your-project/.claude/agents/
cp security-tester.md your-project/.claude/agents/
cp gcp-devops.md your-project/.claude/agents/
```

### Step 2: Add CLAUDE.md to your project root
This is your coordinated knowledge base that agents will reference:

```bash
cp CLAUDE.md your-project/
```

### Step 3: Initialise agent working directories
Either run the helper or create manually:

```bash
# Option A: Use the script
cp coordinate.sh your-project/
cd your-project
chmod +x coordinate.sh
./coordinate.sh init

# Option B: Create manually
mkdir -p your-project/artifacts/{python,typescript,test-results,ui-test-results/screenshots,security-audit,gcp/terraform}
```

### Step 4: Open your project in Claude Code
```bash
cd your-project
claude
```

## How to Use

In Claude Code, invoke agents using `@agent-name` syntax:

```
@python-coder write a function to validate email addresses

@typescript-coder create a TypeScript API client that imports the validator from Python

@functional-tester write comprehensive tests for both the Python and TypeScript code

@security-tester perform a security audit of the codebase

@gcp-devops create a Terraform configuration for deploying to Cloud Run
```

## The Flow

1. **Design Phase**
   - Create `./artifacts/requirements.md` with your project specs
   - Define API contracts in `./artifacts/api-contract.json`

2. **Development Phase**
   - `@python-coder` writes backend code
   - `@typescript-coder` writes frontend/client code

3. **Testing Phase**
   - `@functional-tester` writes and runs tests
   - `@ui-tester` tests user workflows

4. **Security Phase**
   - `@security-tester` audits code and identifies vulnerabilities

5. **Infrastructure Phase**
   - `@gcp-devops` creates Terraform configs for deployment

## Key Principles

**All context is in `./artifacts/`**
Agents read/write from a shared filesystem directory. This is your single source of truth.

**Agents don't spawn other agents**
The main Claude Code session orchestrates everything. Agents are isolated specialists.

**Sequential dependencies**
Each agent's output becomes the next agent's input. TypeScript coder reads Python README, etc.

**Test failures are reports, not fixes**
When `@functional-tester` finds failing tests, it reports them. The relevant coder then fixes the code.

## Why This Approach

You're using Claude Code's native architecture instead of external orchestration frameworks like LangGraph. This means:

- **Zero external dependencies** - Just Claude Code + your tools
- **Clear agent boundaries** - Each agent has explicit tools and constraints
- **Filesystem-based memory** - No database, just `./artifacts/`
- **Lean system prompts** - CLAUDE.md provides condensed knowledge, not massive prompts
- **Native parallelisation** - Claude Code handles multiple agent invocations

This maps directly to how Claude natively thinks about work decomposition.

## Customisation

Want to add a new agent? Create a new `.md` file in `.claude/agents/`:

```markdown
---
name: my-agent
description: What this agent does and when to use it
allowed_tools:
  - Read
  - Write
  - Bash
---

You are a [role]. Your job is to [responsibility].

## Context Paths
- Read X from `./artifacts/...`

## Constraints
- Rule 1
- Rule 2

## Deliverables
- Write output to `./artifacts/...`

## Task
{$ARGUMENTS}
```

Then invoke it as `@my-agent your task here`.

## Troubleshooting

**Agent can't find files?**
→ Run `./coordinate.sh init` to set up directory structure.

**Agents not appearing in Claude Code?**
→ Make sure subagent files are in `.claude/agents/` with `.md` extension.

**TypeScript coder says "no Python README"?**
→ Let python-coder run first. It writes `./artifacts/python/README.md`.

**Need more detail on coordination?**
→ Read `CLAUDE.md`. It's your knowledge base.

## Next Steps

1. Copy all files to your project
2. Run `claude` to open Claude Code
3. Run `./coordinate.sh init` to set up directories
4. Start with `@python-coder` for backend work
5. Refer to `CLAUDE.md` for patterns and best practices

Good luck! You're using the same patterns that power Claude Code's own agent architecture.
