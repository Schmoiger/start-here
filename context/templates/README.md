# Templates

Reusable templates for project artefacts. Copy and customise for new files.

## Document Templates

| Template | Purpose | Output Location |
|----------|---------|-----------------|
| `requirements-template.md` | EARS-format requirements | `artefacts/product/` |
| `user-stories-template.md` | Compressed user stories | `artefacts/product/` |
| `tasks-template.md` | Task tracking matrix | `artefacts/build/` |
| `bugs-template.md` | Bug tracker format | `artefacts/build/` |
| `troubleshooting-template.md` | Issue resolution notes | `artefacts/build/` |

## Agent Templates

| Template | Purpose |
|----------|---------|
| `agent-template.md` | Define a new specialist agent |
| `domain-orchestrator-template.md` | Domain-level task routing |
| `meta-orchestrator-template.md` | Repository-level orchestration |
| `task-prompt-template.md` | Spawn agent with consistent structure |
| `task-context-template.md` | Complex task context file |

## Handoff & Review

| Template | Purpose |
|----------|---------|
| `handoff-template.md` | Inter-agent handoff document |
| `handoff-schema.json` | JSON schema for validation |
| `review-template.md` | Code/tech review template |
| `review-schema.json` | JSON schema for validation |

## Git & PR

| Template | Purpose |
|----------|---------|
| `commit-message-template.md` | Conventional commit format |
| `pr-description-template.md` | Pull request description |

## Usage

### Using Templates

```bash
# Copy template to create new file
cp context/templates/bugs-template.md artefacts/build/bugs.md

# Edit placeholders marked with {curly_braces}
```

### Creating Task Prompts

Use `task-prompt-template.md` when spawning agents. The template directs agents to read their definition from `context/agents/{agent-name}.md` (never inline definitions).

### Handoffs Between Agents

Use `handoff-template.md` or JSON format. See "Handoff Format" below for details.

### Code/Tech Reviews

Use `review-template.md` or JSON format. See "Review Format" below for details.

## Handoff Format

**Purpose**: Token-efficient inter-agent state transfer.

**Format Options**:
- **JSON** (recommended): Use `handoff-schema.json` for validation
- **Markdown**: Use `handoff-template.md` for prose format

**Token Efficiency**:
| Format | Tokens | Reduction |
|--------|--------|-----------|
| Prose markdown | ~2,380 | Baseline |
| Comprehensive JSON | ~1,316 | 45% |
| Minimal JSON | ~443 | 81% |

**Key Principles**:
- Keep summary under 500 characters
- Reference shared docs, don't duplicate content
- Use task objects with status tracking
- Include blockers only when status ≠ "ready"

**Validation**:
```bash
npx ajv validate -s context/templates/handoff-schema.json -d path/to/HANDOFF.json
```

**File Location**:
```
{project-root}/artefacts/build/HANDOFF.json
```

## Review Format

**Purpose**: Compressed code/tech reviews that reduce verbosity by 63-91%.

**Format Options**:
- **JSON** (for agents): Use `review-schema.json` for validation and issue tracking
- **Compressed prose** (for humans): Use `review-template.md` for audit trails

**Token Efficiency**:
| Format | Tokens | Reduction |
|--------|--------|-----------|
| Verbose prose | ~4,600 | Baseline |
| Comprehensive JSON | ~1,700 | 63% |
| Compressed prose | ~395 | 91% |

**Issue Format** (JSON):
```json
{
  "id": "CR-001",
  "severity": "critical",
  "location": "file.py:41",
  "problem": "One sentence describing issue (max 200 chars)",
  "fix": "One sentence describing fix (max 200 chars)"
}
```

**Issue Format** (Prose):
```markdown
**CR-001** `file.py:41` Problem description.
→ Fix instruction.
```

**Severity Categories**:
- `critical`: Fix before deploy (crashes, data corruption, security)
- `high`: Fix this sprint (significant bugs, poor patterns)
- `medium`: Fix next sprint (tech debt, minor issues)
- `low`: Fix when convenient (nitpicks, style)

**File Location**:
```
{project-root}/artefacts/review/code-review.json
{project-root}/artefacts/review/code-review.md
```

## Schema Validation

All JSON schemas are located in this directory:
- `handoff-schema.json`: Validates handoff documents
- `review-schema.json`: Validates review documents

**Usage**:
```bash
# Validate handoff
npx ajv validate -s context/templates/handoff-schema.json -d artefacts/build/HANDOFF.json

# Validate review
npx ajv validate -s context/templates/review-schema.json -d artefacts/review/code-review.json
```

## Naming Convention

- Templates use `-template.md` or `-template.yaml` suffix
- All templates use kebab-case (e.g., `task-prompt-template.md`)
- Generated files remove `-template` suffix
- Use kebab-case for all multi-word names

## Template Standards

All templates should:
- ✅ Use British English spelling (artefacts, colour, etc.)
- ✅ Follow EARS notation for requirements (when applicable)
- ✅ Include file purpose in header comment
- ✅ Mark all placeholders clearly with `{curly_braces}`
- ✅ Be token-efficient (no verbose explanations in templates)
- ✅ Reference relevant standards from `context/standards/`

## See Also

- `context/standards/doc-standards.md` - Documentation structure and style
- `context/standards/workflow-standards.md` - Development workflow processes
- `context/rules/` - Non-negotiable formatting rules
