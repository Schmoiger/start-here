# Multi-Agent Orchestration Guide

This document is your agent knowledge base. Reference it when coordinating workflows.

## Core Principles

**Context Isolation**: Each agent has its own focus and tools. Don't ask an agent to do work outside its domain.

**Filesystem as Shared Memory**: All agents read/write to `./artifacts/`. This is the single source of truth for context.

**Sequential Dependency**: Agents should run in order:
1. python-coder (create backend)
2. typescript-coder (create frontend, consumes Python APIs)
3. functional-tester (write tests for both)
4. ui-tester (test user workflows)
5. security-tester (audit everything)
6. gcp-devops (configure infrastructure)

**No Nested Spawning**: Agents cannot spawn other agents. The main Claude Code session is the orchestrator.

## Agent Roles

### python-coder
**When to use**: Building or modifying Python modules, functions, classes.

**Tools**: Read, Write, Edit, Bash, Glob, Grep

**Context**: Reads `./artifacts/python/` and `./artifacts/api-contract.json`

**Constraints**:
- Type hints on all functions (Python 3.10+)
- Assume pytest for testing
- Keep modules under 300 lines
- Document public APIs with docstrings

**Output**: Code to `./artifacts/python/`, updated `README.md`

---

### typescript-coder
**When to use**: Building frontend or backend TypeScript, integrating with Python APIs.

**Tools**: Read, Write, Edit, Bash, Glob, Grep

**Context**: Reads Python APIs from `./artifacts/python/README.md` and `./artifacts/api-contract.json`

**Constraints**:
- Strict mode tsconfig, no `any` types
- Keep modules under 250 lines
- Import from Python only via documented contracts
- Document public exports with JSDoc

**Output**: Code to `./artifacts/typescript/`, updated `README.md`

---

### functional-tester
**When to use**: Writing pytest tests, vitest/jest tests, generating test reports.

**Tools**: Read, Write, Edit, Bash, Glob, Grep

**Context**: Reads `./artifacts/python/` and `./artifacts/typescript/` READMEs

**Constraints**:
- Never modify production code
- Aim for 80%+ coverage
- Include happy path + edge cases
- Run tests and capture output

**Output**: Tests to `./artifacts/*/tests/`, results to `./artifacts/test-results/`

---

### ui-tester
**When to use**: Testing user workflows, end-to-end testing, accessibility checks.

**Tools**: Chrome DevTools MCP only (Read, Write, Bash for logging)

**Context**: Reads `./artifacts/ui-test-scenarios.md` and component docs

**Constraints**:
- Use Chrome DevTools ONLY, no external frameworks
- Test user workflows, not implementation details
- Capture screenshots on failure

**Output**: Results to `./artifacts/ui-test-results/`

---

### security-tester
**When to use**: Security audit, threat modelling, dependency scanning.

**Tools**: Read, Write, Glob, Grep (prompt-based reasoning)

**Context**: Reads all code in `./artifacts/python/` and `./artifacts/typescript/`

**Framework**:
- OWASP Top 10 assessment
- Input validation & sanitisation
- Auth/authz patterns
- Secrets & credentials handling
- Dependency vulnerabilities
- Data exposure & error handling

**Output**: Findings to `./artifacts/security-audit/`

---

### gcp-devops
**When to use**: Infrastructure-as-code, deployment config, GCP resource setup.

**Tools**: Read, Write, Edit, Bash, Glob, Grep

**Context**: Reads `./artifacts/requirements.md` and Python/TypeScript READMEs

**Constraints**:
- Use Terraform for IaC
- GCP resources only (Cloud Run, Cloud Build, Firestore, etc.)
- Follow least privilege + encryption best practices
- Include monitoring & logging

**Output**: Terraform configs to `./artifacts/gcp/terraform/`, guides and checklists

---

## Workflow Patterns

### Pattern 1: Sequential Build
```
requirements.md (user creates)
    ↓
@python-coder creates backend
    ↓
@typescript-coder creates frontend (reads Python README)
    ↓
@functional-tester writes tests (reads both READMEs)
```

### Pattern 2: Parallel Testing
```
@functional-tester tests Python
    ↑          ↑
    │          └─ @ui-tester tests frontend
    │
@security-tester audits both
```

### Pattern 3: Infrastructure Last
```
All code written + tested
    ↓
@gcp-devops creates infrastructure (reads all READMEs)
    ↓
Deploy to staging
```

## Communication Between Agents

**Agent → Artifact Updates**:
- Python coder writes to `./artifacts/python/README.md` with exported functions
- TypeScript coder reads that README, updates `./artifacts/typescript/README.md`
- Both follow the API contract in `./artifacts/api-contract.json`

**Test Results as Feedback**:
- Tests write to `./artifacts/test-results/` with pass/fail summary
- If failures, functional-tester notes them but doesn't fix (coders handle fixes)
- Rerun agent to iterate

**Example API Contract** (`./artifacts/api-contract.json`):
```json
{
  "services": {
    "UserValidator": {
      "module": "validators/user.py",
      "exports": [
        {
          "name": "validate_email",
          "signature": "(email: str) -> bool",
          "description": "Validate email format"
        }
      ]
    }
  }
}
```

## Common Commands in Claude Code

```bash
# Initialize agent environment
./coordinate.sh init

# List available agents
./coordinate.sh list

# Show workflow diagram
./coordinate.sh workflow
```

## Invoking Agents

In Claude Code terminal, use `@agent-name` syntax:

```
@python-coder write a function to validate email addresses

@typescript-coder create a TypeScript client that calls the email validator from Python

@functional-tester write pytest tests for the email validator and vitest tests for the TypeScript client

@security-tester audit the code for OWASP vulnerabilities

@gcp-devops create a Cloud Run deployment for this application

@ui-tester test the login flow end-to-end in Chrome
```

## Best Practices

**1. Always define requirements first**
Edit `./artifacts/requirements.md` before asking agents to build.

**2. Create API contracts early**
Define `./artifacts/api-contract.json` so TypeScript coder knows what Python exports.

**3. Check agent output**
Review each agent's README updates in `./artifacts/*/README.md` before proceeding to next agent.

**4. Let agents fail gracefully**
If tests fail, tester reports it. Don't auto-fix; let the coder iterate.

**5. Use filesystem as validation**
If an agent didn't produce expected files in `./artifacts/`, the work wasn't done.

## Troubleshooting

**Agent says it can't find files**:
→ Ensure `./artifacts/` directory structure exists. Run `./coordinate.sh init`.

**TypeScript coder says "no Python README"**:
→ python-coder needs to run first and write `./artifacts/python/README.md`.

**Tests fail but agent doesn't fix code**:
→ That's correct! functional-tester reports failures; coders fix them. Re-invoke the coder with failure details.

**Security audit finds issues in code I thought was clean**:
→ Read `./artifacts/security-audit/remediation-guide.md`. Share findings with relevant coder agent.

**GCP DevOps can't validate Terraform**:
→ Ensure you have a valid GCP project and credentials set up. Run `gcloud auth login` first.

## Further Reading

- [Claude Code Documentation](https://code.claude.com/docs)
- [Claude Code Subagents Guide](https://code.claude.com/docs/en/sub-agents)
- [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk)
