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

    def test_canonical_interruption_log_path_passes(self, tmp_path):
        """Test that the one-log-per-task interruption path is accepted."""
        agent = tmp_path / "good_agent.md"
        agent.write_text(f"""---
name: test-agent
model: sonnet
---
{CONTEXT_ACQUISITION_BODY}

## Escalation Protocol

Append to `artefacts/build/interruptions/{{task-id}}.jsonl`.
""")
        errors = validate_agent_definition(agent)
        assert not any("Interruption log path" in e for e in errors)

    def test_legacy_interruption_log_path_rejected(self, tmp_path):
        """Test that legacy per-agent/per-timestamp interruption names are caught."""
        agent = tmp_path / "legacy_agent.md"
        agent.write_text(f"""---
name: test-agent
model: sonnet
---
{CONTEXT_ACQUISITION_BODY}

## Escalation Protocol

Append to `artefacts/build/interruptions/{{agent-name}}-{{task-id}}-{{timestamp}}.jsonl`.
""")
        errors = validate_agent_definition(agent)
        assert any("Interruption log path" in e for e in errors)

    def test_interruption_log_wildcard_allowed(self, tmp_path):
        """Test that reading all interruption logs with a wildcard is allowed."""
        agent = tmp_path / "reader_agent.md"
        agent.write_text(f"""---
name: test-agent
model: sonnet
---
{CONTEXT_ACQUISITION_BODY}

## Context

Read `{{project-root}}/artefacts/build/interruptions/*.jsonl`.
""")
        errors = validate_agent_definition(agent)
        assert not any("Interruption log path" in e for e in errors)

    def test_body_table_source_should_fail_when_file_does_not_exist(self, tmp_path):
        """A body 'Source' naming a phantom rule file is drift and must error."""
        agent = tmp_path / "drifted_agent.md"
        agent.write_text(f"""---
name: test-agent
model: medium
---
{CONTEXT_ACQUISITION_BODY}

#### Task Constraints

| Constraint | Source |
| :--- | :--- |
| Stop and ask the human | `handoff-hygiene.md` |
""")
        errors = validate_agent_definition(agent)
        assert any(
            "handoff-hygiene.md" in e and "doesn't exist" in e for e in errors
        ), f"Expected a phantom body source error, got: {errors}"

    def test_body_table_source_should_fail_when_section_does_not_exist(self, tmp_path):
        """A body 'Source' section that no heading matches must error."""
        agent = tmp_path / "drifted_agent.md"
        agent.write_text(f"""---
name: test-agent
model: medium
---
{CONTEXT_ACQUISITION_BODY}

#### Task Constraints

| Constraint | Source |
| :--- | :--- |
| Stop and ask the human | `tech-writing.md` §Nonexistent Section |
""")
        errors = validate_agent_definition(agent)
        assert any(
            "Nonexistent Section" in e and "doesn't exist" in e for e in errors
        ), f"Expected an unresolved section error, got: {errors}"

    def test_body_table_source_should_pass_when_citations_resolve(self, tmp_path):
        """Resolvable body sources — including numbered and named sections — pass."""
        agent = tmp_path / "attributed_agent.md"
        agent.write_text(f"""---
name: test-agent
model: medium
---
{CONTEXT_ACQUISITION_BODY}

#### Task Constraints

| Constraint | Source |
| :--- | :--- |
| British English spelling | `tech-writing.md` §1 British English |
| GREEN phase must not edit tests | `tdd-workflow.md` §2 Phase 2: GREEN Phase (Implement) |
| Test at the I/O boundary | `context/rules/testing.md` §2 Testing Constraints |
""")
        errors = validate_agent_definition(agent)
        assert errors == [], f"Unexpected errors: {errors}"

    def test_body_citation_should_fail_when_file_does_not_exist(self, tmp_path):
        """An inline `file.md §section` citation to a phantom file must error."""
        agent = tmp_path / "drifted_agent.md"
        agent.write_text(f"""---
name: test-agent
model: medium
---
{CONTEXT_ACQUISITION_BODY}

#### Task Constraints

- Follow the escalation protocol (`escalation.md` §1 Provisioning)
""")
        errors = validate_agent_definition(agent)
        assert any(
            "escalation.md" in e and "doesn't exist" in e for e in errors
        ), f"Expected a phantom citation error, got: {errors}"

    def test_body_citation_should_fail_when_section_does_not_exist(self, tmp_path):
        """An inline citation to a section the rule file lacks must error."""
        agent = tmp_path / "drifted_agent.md"
        agent.write_text(f"""---
name: test-agent
model: medium
---
{CONTEXT_ACQUISITION_BODY}

#### Task Constraints

- Read the phantom phase (`tdd-workflow.md` §9 Phase 9: Phantom Phase)
""")
        errors = validate_agent_definition(agent)
        assert any(
            "Phase 9" in e and "doesn't exist" in e for e in errors
        ), f"Expected an unresolved section error, got: {errors}"

    def test_body_citation_should_pass_when_section_resolves(self, tmp_path):
        """An inline citation that resolves to a real heading passes."""
        agent = tmp_path / "attributed_agent.md"
        agent.write_text(f"""---
name: test-agent
model: medium
---
{CONTEXT_ACQUISITION_BODY}

#### Task Constraints

- British English spelling throughout (`tech-writing.md` §1 British English)
""")
        errors = validate_agent_definition(agent)
        assert errors == [], f"Unexpected errors: {errors}"

    def test_body_citation_error_should_report_file_line_number_when_it_fails(self, tmp_path):
        """Diagnostics must quote the editor's line number, not a body offset."""
        agent = tmp_path / "drifted_agent.md"
        lines = [
            "---",
            "name: test-agent",
            "model: medium",
            "---",
            "",
            "## Context Acquisition",
            "",
            "1. Standards: tech-standards.md",
            "",
            "#### Task Constraints",
            "",
            "- Follow the escalation protocol (`escalation.md` §1 Provisioning)",
        ]
        agent.write_text("\n".join(lines) + "\n")
        errors = validate_agent_definition(agent)
        assert any(f"(line {len(lines)})" in e for e in errors), errors

    def test_body_table_without_source_column_should_be_ignored(self, tmp_path):
        """Tables that carry no 'Source' column are not attribution tables."""
        agent = tmp_path / "plain_agent.md"
        agent.write_text(f"""---
name: test-agent
model: medium
---
{CONTEXT_ACQUISITION_BODY}

| Task Domain | Context Location |
| :--- | :--- |
| Product Features | `{{project-root}}/artefacts/product/` |
""")
        errors = validate_agent_definition(agent)
        assert errors == [], f"Unexpected errors: {errors}"
