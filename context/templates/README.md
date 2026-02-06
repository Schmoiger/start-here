# Templates

Reusable templates for project artefacts. Copy and customise for new files.

See `context/standards/context-framework.md` for sharing formats, prioritisation, and terse format guidance.

## Document Templates

| Template | Purpose | Output Location |
|----------|---------|-----------------|
| `requirements-template.md` | EARS-format requirements | `artefacts/product/` |
| `user-stories-template.md` | Compressed user stories | `artefacts/product/` |
| `tasks-template.md` | Task tracking matrix | `artefacts/build/` |
| `bugs-template.md` | Bug tracker format | `artefacts/build/` |
| `domain-rules-template.yaml` | Domain-specific rules, blockers, terminology | `services/{domain}/context/` |

## Agent Templates

| Template | Purpose |
|----------|---------|
| `agent-template.md` | Define a new specialist agent |
| `task-prompt-template.md` | Spawn agent with consistent structure |

## Handoff & Review

| Template | Purpose |
|----------|---------|
| `handoff-template.md` | Inter-agent handoff (markdown, for humans + agents) |
| `handoff-schema.json` | Inter-agent handoff (JSON schema, for agent-to-agent) |
| `review-template.md` | Code/tech review (markdown, for humans + agents) |
| `review-schema.json` | Code/tech review (JSON schema, for agent-to-agent) |

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
- **JSON** (recommended for agent-to-agent): Use `handoff-schema.json` for validation
- **Markdown** (for agent-to-human): Use `handoff-template.md` for prose format

**Key Principles**:
- Keep summary under 500 characters
- Reference shared docs, don't duplicate content
- Use task objects with status tracking
- Include blockers only when status is not "ready"

**Validation**:
```bash
npx ajv validate -s context/templates/handoff-schema.json -d path/to/HANDOFF.json
```

**File Location**:
```
{project-root}/artefacts/build/HANDOFF.json
```

## Review Format

**Purpose**: Compressed code/tech reviews.

**Format Options**:
- **JSON** (for agents): Use `review-schema.json` for validation and issue tracking
- **Compressed prose** (for humans): Use `review-template.md` for audit trails

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
> Fix instruction.
```

**Severity Categories**: See `context/standards/context-framework.md` for severity definitions.

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

- Templates use `-template.md` suffix
- All templates use kebab-case (e.g., `task-prompt-template.md`)
- Generated files remove `-template` suffix

## See Also

- `context/standards/context-framework.md` - Sharing formats, prioritisation, terse formats
- `context/standards/doc-standards.md` - Documentation structure and style
- `context/standards/workflow-standards.md` - Development workflow processes
