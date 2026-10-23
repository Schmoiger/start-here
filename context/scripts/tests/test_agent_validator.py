"""Tests for agent definition validator."""

from context.scripts.validators.agent_definitions import (
    CONTEXT_ACQUISITION_HEADING,
    REPO_ROOT,
    validate_agent_definition,
)

# Minimal body satisfying the canonical shape. Used as a baseline so each
# negative test fails for exactly one reason.
CONTEXT_ACQUISITION_BODY = """
## Context Acquisition

Before executing any operations, consume the following required context files in sequence:
1. Standards: tech-standards.md
2. Rules: bash-environment.md
3. Skills: tdd-workflow.md
"""


class TestAgentValidator:
    """Tests for agent definition validator."""

    def test_valid_agent(self, valid_agent):
        """Test that a canonical agent definition passes with no errors."""
        errors = validate_agent_definition(valid_agent)
        assert errors == [], f"Unexpected errors: {errors}"

    def test_no_frontmatter(self, invalid_agent_no_frontmatter):
        """Test that agent without frontmatter fails."""
        errors = validate_agent_definition(invalid_agent_no_frontmatter)
        assert len(errors) > 0
        assert any("frontmatter" in e.lower() for e in errors)

    def test_hardcoded_paths(self, invalid_agent_hardcoded_paths):
        """Test that hardcoded paths are caught."""
        errors = validate_agent_definition(invalid_agent_hardcoded_paths)
        assert len(errors) > 0
        assert any("hardcoded" in e.lower() for e in errors)

    def test_missing_required_sections(self, invalid_agent_missing_sections):
        """Test that a body without 'Context Acquisition' is caught."""
        errors = validate_agent_definition(invalid_agent_missing_sections)
        assert len(errors) > 0
        assert any("Context Acquisition" in e for e in errors)

    def test_context_acquisition_section_passes(self, tmp_path):
        """Test that the canonical frontmatter-driven shape is accepted."""
        agent = tmp_path / "canonical_agent.md"
        agent.write_text(f"""---
name: test-agent
model: medium
tools:
  - context7 MCP: library documentation
standards:
  - coding-standards.md
rules:
  - bash-environment.md
skills:
  - tdd-workflow.md
---
{CONTEXT_ACQUISITION_BODY}

---

## Workflow

### 1. Intake Validation

Check the prompt headers.
""")
        errors = validate_agent_definition(agent)
        assert errors == []

    def test_legacy_required_sections_rejected(self, tmp_path):
        """Test that the legacy 'Required Standards'/'Required Rules' body is rejected."""
        agent = tmp_path / "legacy_agent.md"
        agent.write_text("""---
name: test-agent
model: sonnet
---

## Required Standards (Read First!)

1. context/standards/tech-standards.md

---

## Required Rules (Must Follow!)

1. context/rules/bash-environment.md
""")
        errors = validate_agent_definition(agent)
        assert any("Context Acquisition" in e for e in errors)

    def test_agent_template_scaffold_passes_validation(self, tmp_path):
        """Test that the shipped agent template satisfies its own validator.

        Guards template/validator drift: if the template's headings or
        frontmatter keys change, this fails before any agent is authored from it.
        """
        template = REPO_ROOT / "context" / "templates" / "agent-template.md"
        content = template.read_text()

        replacements = {
            "{name}": "template-parity-agent",
            "{One sentence purpose. Trigger condition. Output path.}": (
                "Verifies that the agent template satisfies the validator."
            ),
            "{small|medium|large}": "medium",
            "{tool-name}: {purpose/runtime-scope}": "context7 MCP: library documentation",
            "{path/to/standard.md}": "tech-standards.md",
            "{path/to/rule.md}": "bash-environment.md",
            "{path/to/skill.md}": "tdd-workflow.md",
        }
        for placeholder, value in replacements.items():
            content = content.replace(placeholder, value)

        assert "{path/to/" not in content, "unresolved referenced-file placeholder"
        assert CONTEXT_ACQUISITION_HEADING in content

        agent = tmp_path / "template-parity-agent.md"
        agent.write_text(content)

        errors = validate_agent_definition(agent)
        assert errors == [], f"Template scaffold fails its own validator: {errors}"

    def test_invalid_yaml_frontmatter(self, tmp_path):
        """Test that invalid YAML frontmatter is caught."""
        bad_agent = tmp_path / "bad_agent.md"
        bad_agent.write_text("""---
name: test
invalid yaml: [unclosed
---

## Role
Test
""")
        errors = validate_agent_definition(bad_agent)
        assert len(errors) > 0
        assert any("YAML" in e for e in errors)

    def test_missing_required_fields(self, tmp_path):
        """Test that missing required frontmatter fields are caught."""
        incomplete_agent = tmp_path / "incomplete_agent.md"
        incomplete_agent.write_text(f"""---
name: test-agent
# Missing 'model'
---
{CONTEXT_ACQUISITION_BODY}
""")
        errors = validate_agent_definition(incomplete_agent)
        assert len(errors) > 0
        assert any("model" in e for e in errors)

    def test_relative_paths_flagged(self, tmp_path):
        """Test that relative paths to artefacts are flagged."""
        bad_agent = tmp_path / "bad_agent.md"
        bad_agent.write_text(f"""---
name: test-agent
model: sonnet
---
{CONTEXT_ACQUISITION_BODY}

## Workflow

1. Read from ./artefacts/requirements.md
2. Write to ./artefacts/output.md
""")
        errors = validate_agent_definition(bad_agent)
        assert len(errors) > 0
        assert any("relative paths" in e.lower() for e in errors)

    def test_reminders_without_attribution(self, tmp_path):
        """Test that reminders without attribution are caught."""
        bad_agent = tmp_path / "bad_agent.md"
        bad_agent.write_text(f"""---
name: test-agent
model: sonnet
---
{CONTEXT_ACQUISITION_BODY}

## Critical Reminders (from standards above)

- Use uv run for Python
- Write tests before code
""")
        errors = validate_agent_definition(bad_agent)
        assert len(errors) > 0
        # Should catch reminders without (file:line) attribution
        assert any("attribution" in e.lower() for e in errors)

    def test_proper_attribution_passes(self, tmp_path):
        """Test that properly attributed reminders pass."""
        good_agent = tmp_path / "good_agent.md"
        good_agent.write_text(f"""---
name: test-agent
model: sonnet
---
{CONTEXT_ACQUISITION_BODY}

## Critical Reminders (from standards above)

- Use uv run for Python (tech-standards.md:34)
- Write tests before code (testing-standards.md:12)

## Workflow

Use {{project-root}}/artefacts/
""")
        errors = validate_agent_definition(good_agent)
        attribution_errors = [e for e in errors if "attribution" in e.lower()]
        assert len(attribution_errors) == 0

    def test_project_root_placeholders_allowed(self, tmp_path):
        """Test that {project-root} placeholders are allowed."""
        good_agent = tmp_path / "good_agent.md"
        good_agent.write_text(f"""---
name: test-agent
model: sonnet
---
{CONTEXT_ACQUISITION_BODY}

## Workflow

1. Read from {{project-root}}/artefacts/requirements.md
2. Write to {{project-root}}/artefacts/output.md
""")
        errors = validate_agent_definition(good_agent)
        path_errors = [e for e in errors if
                      "hardcoded" in e.lower() or
                      "relative paths" in e.lower()]
        assert len(path_errors) == 0

    def test_nonexistent_standards_flagged(self, tmp_path):
        """Test that references to nonexistent standards are caught."""
        bad_agent = tmp_path / "bad_agent.md"
        bad_agent.write_text(f"""---
name: test-agent
model: sonnet
standards: [nonexistent-standard.md]
---
{CONTEXT_ACQUISITION_BODY}
""")
        errors = validate_agent_definition(bad_agent)
        assert len(errors) > 0
        assert any("doesn't exist" in e for e in errors)

    def test_nonexistent_rules_flagged(self, tmp_path):
        """Test that references to nonexistent rules are caught."""
        bad_agent = tmp_path / "bad_agent.md"
        bad_agent.write_text(f"""---
name: test-agent
model: sonnet
rules: [nonexistent-rule.md]
---
{CONTEXT_ACQUISITION_BODY}
""")
        errors = validate_agent_definition(bad_agent)
        assert any("doesn't exist" in e for e in errors)

    def test_nonexistent_skills_flagged(self, tmp_path):
        """Test that references to nonexistent skills are caught."""
        bad_agent = tmp_path / "bad_agent.md"
        bad_agent.write_text(f"""---
name: test-agent
model: sonnet
skills: [nonexistent-skill.md]
---
{CONTEXT_ACQUISITION_BODY}
""")
        errors = validate_agent_definition(bad_agent)
        assert any("doesn't exist" in e for e in errors)
