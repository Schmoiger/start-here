"""Tests for validation scripts."""

import json
import sys
from pathlib import Path

from context.scripts.validators.workspace_conventions import (
    INTERRUPTION_BASE_FIELDS,
    INTERRUPTION_TYPE_FIELDS,
    REQUIRED_METRICS_FIELDS,
    VALID_INTERRUPTION_DECISIONS,
    VALID_INTERRUPTION_IMPACTS,
    VALID_INTERRUPTION_TYPES,
    VALID_METRICS_EVENTS,
    VALID_TOKEN_SOURCES,
    is_interruptions_log,
    main as workspace_conventions_main,
    validate_commit_message,
    validate_interruptions_entry,
    validate_interruptions_file,
    validate_metrics_entry,
    validate_metrics_file,
    validate_output_path,
    validate_output_paths,
)
from context.scripts.validators.tech_writing import (
    validate_british_english,
    is_ears_requirement,
    validate_requirements_file,
)
from context.scripts.validators.ui_dev import (
    check_important,
    check_raw_hex,
    check_css_files,
)
from context.scripts.validators.supabase import (
    check_supabase_imports,
    check_migration_audit,
)
from context.scripts.validators.testing import (
    check_forbidden_mocks,
)
from context.scripts.validators.typescript_environment import (
    check_package_lock,
    check_tsconfig_strictness,
    check_workspaces,
)
from context.scripts.validators.ui_testing import (
    check_forbidden_ui_test_deps,
)
from context.scripts.validators.secrets import (
    scan_file_for_secrets,
)
from context.scripts.validators.verify_typst_formatting import check_and_fix_file
from context.scripts.validators.subrepo_freshness import (
    find_subrepos,
    query_upstream_head,
    check_subrepo_freshness,
    main as subrepo_freshness_main,
)
from unittest.mock import patch
import subprocess


class TestConventionalCommits:
    """Tests for conventional commit validator."""

    def test_valid_commit(self, valid_commit):
        """Test that valid commit passes validation."""
        msg = valid_commit.read_text()
        is_valid, error = validate_commit_message(msg)
        assert is_valid, f"Expected valid commit to pass: {error}"
        assert error == ""

    def test_invalid_no_scope(self, invalid_commit_no_scope):
        """Test that commit without scope fails validation."""
        msg = invalid_commit_no_scope.read_text()
        is_valid, error = validate_commit_message(msg)
        assert not is_valid
        assert "Invalid subject line" in error

    def test_invalid_too_long(self, invalid_commit_too_long):
        """Test that commit over 72 chars fails validation."""
        msg = invalid_commit_too_long.read_text()
        is_valid, error = validate_commit_message(msg)
        assert not is_valid
        assert "too long" in error

    def test_invalid_past_tense(self, invalid_commit_past_tense):
        """Test that past tense description fails validation."""
        msg = invalid_commit_past_tense.read_text()
        is_valid, error = validate_commit_message(msg)
        assert not is_valid
        assert "imperative mood" in error

    def test_valid_with_agent_session(self, valid_commit_with_agent_session):
        """Test that agent session metadata is validated."""
        msg = valid_commit_with_agent_session.read_text()
        is_valid, error = validate_commit_message(msg)
        assert is_valid, f"Expected valid agent commit to pass: {error}"

    def test_merge_commit_allowed(self, merge_commit):
        """Test that merge commits don't require validation."""
        # Note: Main script skips merge commits, so we test the detection
        msg = merge_commit.read_text()
        assert msg.startswith('Merge ')

    def test_empty_commit_fails(self):
        """Test that empty commit message fails."""
        is_valid, error = validate_commit_message("")
        assert not is_valid
        # Empty string still fails validation, error message indicates invalid format
        assert "Invalid subject line" in error or "Empty" in error

    def test_invalid_type(self):
        """Test that invalid commit type fails."""
        msg = "invalid(scope): description"
        is_valid, error = validate_commit_message(msg)
        assert not is_valid
        assert "Invalid subject line" in error

    def test_invalid_scope_uppercase(self):
        """Test that uppercase scope fails."""
        msg = "feat(DataService): add feature"
        is_valid, error = validate_commit_message(msg)
        assert not is_valid
        assert "Invalid subject line" in error

    def test_coauthor_format(self):
        """Test Co-Authored-By format validation."""
        msg = """feat(test): valid subject

Co-Authored-By: Invalid Format"""
        is_valid, error = validate_commit_message(msg)
        assert not is_valid
        assert "Co-Authored-By format" in error

    def test_agent_session_requires_coauthor(self):
        """Test that Agent-Session requires Co-Authored-By."""
        msg = """feat(test): valid subject

Agent-Session: tool=cursor model=sonnet agents=python-coder duration=5m tokens=1K/2K"""
        is_valid, error = validate_commit_message(msg)
        assert not is_valid
        assert "require Co-Authored-By" in error


class TestEARSNotation:
    """Tests for EARS notation validator."""

    def test_valid_requirements(self, valid_requirements):
        """Test that valid EARS requirements pass."""
        errors = validate_requirements_file(valid_requirements)
        assert len(errors) == 0, f"Expected no errors, got: {errors}"

    def test_invalid_requirements(self, invalid_requirements):
        """Test that invalid requirements fail."""
        errors = validate_requirements_file(invalid_requirements)
        assert len(errors) > 0
        assert any("EARS notation" in error for error in errors)

    def test_ubiquitous_pattern(self):
        """Test ubiquitous EARS pattern recognition."""
        assert is_ears_requirement("THE system SHALL fetch data")
        assert is_ears_requirement("the system shall fetch data")  # case insensitive

    def test_event_pattern(self):
        """Test event-driven EARS pattern."""
        assert is_ears_requirement("WHEN user clicks button, THE system SHALL save data")

    def test_state_pattern(self):
        """Test state-driven EARS pattern."""
        assert is_ears_requirement("WHILE offline, THE system SHALL use cached data")

    def test_optional_pattern(self):
        """Test optional EARS pattern."""
        assert is_ears_requirement("IF user is admin, THE system SHALL show controls")

    def test_forbidden_pattern(self):
        """Test forbidden EARS pattern."""
        assert is_ears_requirement("THE system SHALL NOT store passwords in plain text")

    def test_complex_pattern(self):
        """Test complex EARS pattern."""
        assert is_ears_requirement(
            "WHEN user requests data, IF cache is stale, THE system SHALL fetch from API"
        )

    def test_non_ears_requirement(self):
        """Test that non-EARS text is not matched."""
        assert not is_ears_requirement("The system should do something")
        assert not is_ears_requirement("Users must be able to view data")

    def test_code_blocks_ignored(self, tmp_path):
        """Test that code blocks are ignored."""
        req_file = tmp_path / "test.md"
        req_file.write_text("""# Requirements

```python
# This shall not be validated
system.shall_do_something()
```

THE system SHALL validate requirements.
""")
        errors = validate_requirements_file(req_file)
        assert len(errors) == 0


class TestBritishEnglish:
    """Tests for British English validator."""

    def test_valid_british_english(self, valid_british_english):
        """Test that British English passes validation."""
        violations = validate_british_english(valid_british_english)
        assert len(violations) == 0, f"Expected no violations, got: {violations}"

    def test_invalid_american_english(self, invalid_british_english):
        """Test that American English fails validation."""
        violations = validate_british_english(invalid_british_english)
        assert len(violations) > 0
        # Should catch: color, behavior, organize, center, license
        assert len(violations) >= 4

    def test_color_vs_colour(self):
        """Test color/colour detection."""
        # Create temp file with American spelling
        from tempfile import NamedTemporaryFile
        with NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("The color is red\n")
            f.flush()
            violations = validate_british_english(Path(f.name))
            assert len(violations) > 0
            assert any("colour" in v for v in violations)
            Path(f.name).unlink()

    def test_behavior_vs_behaviour(self):
        """Test behavior/behaviour detection."""
        from tempfile import NamedTemporaryFile
        with NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("The behavior is normal\n")
            f.flush()
            violations = validate_british_english(Path(f.name))
            assert len(violations) > 0
            assert any("behaviour" in v for v in violations)
            Path(f.name).unlink()

    def test_organize_vs_organise(self):
        """Test organize/organise detection."""
        from tempfile import NamedTemporaryFile
        with NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("Users can organize their files\n")
            f.flush()
            violations = validate_british_english(Path(f.name))
            assert len(violations) > 0
            assert any("organise" in v for v in violations)
            Path(f.name).unlink()

    def test_code_blocks_ignored(self, tmp_path):
        """Test that code blocks are ignored."""
        test_file = tmp_path / "test.md"
        test_file.write_text("""# Documentation

```python
# color = "red"  # This should be ignored
print("color")
```

The colour is red.
""")
        violations = validate_british_english(test_file)
        assert len(violations) == 0

    def test_inline_code_ignored(self, tmp_path):
        """Test that inline code is ignored."""
        test_file = tmp_path / "test.md"
        test_file.write_text("Use the `color` parameter.\n\nThe colour is red.")
        violations = validate_british_english(test_file)
        # Should only catch "color" if not in inline code
        # Current implementation checks for backticks in line
        assert len(violations) == 0  # Line has backticks, so skipped


class TestMetricsLogging:
    """Tests for metrics logging validator."""

    def test_valid_metrics(self, valid_metrics):
        """Test that valid metrics pass validation."""
        errors = validate_metrics_file(valid_metrics)
        assert len(errors) == 0, f"Expected no errors, got: {errors}"

    def test_invalid_metrics(self, invalid_metrics):
        """Test that invalid metrics fail validation."""
        errors = validate_metrics_file(invalid_metrics)
        assert len(errors) > 0

    def test_metrics_log_location_under_build(self):
        """Test that metrics logs are build records at artefacts/build/metrics/."""
        assert validate_output_path("artefacts/build/metrics/session-log.jsonl") == []

    def test_metrics_log_requires_jsonl_suffix(self):
        """Test that output path validation requires a .jsonl metrics log."""
        errors = validate_output_path("artefacts/build/metrics/session-log.log")
        assert any(".jsonl" in e for e in errors)

    def test_metrics_log_rejects_repository_root(self):
        """Test that a repository-root metrics/ directory is rejected."""
        errors = validate_output_path("metrics/session-log.jsonl")
        assert any("artefacts/build/metrics/" in e for e in errors)

    def test_missing_required_field(self):
        """Test that missing required field is caught."""
        entry = {
            "ts": "2025-01-28T09:00:00Z",
            "task": "TEST-001",
            # Missing 'agent', 'event', 'tokens'
        }
        errors = validate_metrics_entry(entry, 1)
        assert len(errors) >= 3  # Should catch all missing fields
        assert any("agent" in e for e in errors)
        assert any("event" in e for e in errors)
        assert any("tokens" in e for e in errors)

    def test_invalid_timestamp(self):
        """Test that invalid timestamp format is caught."""
        entry = {
            "ts": "2025-01-28",  # Missing time and timezone
            "task": "TEST-001",
            "agent": "test-agent",
            "event": "start",
            "tokens": {"in": 100, "out": 50, "source": "api_response"}
        }
        errors = validate_metrics_entry(entry, 1)
        assert len(errors) > 0
        assert any("timestamp" in e.lower() for e in errors)

    def test_invalid_event(self):
        """Test that invalid event type is caught."""
        entry = {
            "ts": "2025-01-28T09:00:00Z",
            "task": "TEST-001",
            "agent": "test-agent",
            "event": "invalid-event",
            "tokens": {"in": 100, "out": 50, "source": "api_response"}
        }
        errors = validate_metrics_entry(entry, 1)
        assert len(errors) > 0
        assert any("event" in e.lower() for e in errors)

    def test_invalid_token_source(self):
        """Test that invalid token source is caught."""
        entry = {
            "ts": "2025-01-28T09:00:00Z",
            "task": "TEST-001",
            "agent": "test-agent",
            "event": "start",
            "tokens": {"in": 100, "out": 50, "source": "invalid"}
        }
        errors = validate_metrics_entry(entry, 1)
        assert len(errors) > 0
        assert any("source" in e.lower() for e in errors)

    def test_missing_tokens_fields(self):
        """Test that missing token fields are caught."""
        entry = {
            "ts": "2025-01-28T09:00:00Z",
            "task": "TEST-001",
            "agent": "test-agent",
            "event": "start",
            "tokens": {"source": "api_response"}  # Missing 'in' and 'out'
        }
        errors = validate_metrics_entry(entry, 1)
        assert len(errors) > 0
        assert any("'in' and 'out'" in e for e in errors)

    def test_handoff_requires_to_field(self):
        """Test that handoff event requires 'to' field."""
        entry = {
            "ts": "2025-01-28T09:00:00Z",
            "task": "TEST-001",
            "agent": "test-agent",
            "event": "handoff",
            # Missing 'to' field
            "tokens": {"in": 100, "out": 50, "source": "api_response"}
        }
        errors = validate_metrics_entry(entry, 1)
        assert len(errors) > 0
        assert any("'to' field" in e for e in errors)

    def test_empty_file_valid(self, tmp_path):
        """Test that empty metrics file is valid."""
        empty_file = tmp_path / "metrics" / "empty.jsonl"
        empty_file.parent.mkdir(exist_ok=True)
        empty_file.write_text("")
        errors = validate_metrics_file(empty_file)
        assert len(errors) == 0

    def test_invalid_json(self, tmp_path):
        """Test that invalid JSON is caught."""
        bad_file = tmp_path / "metrics" / "bad.jsonl"
        bad_file.parent.mkdir(exist_ok=True)
        bad_file.write_text("not valid json\n")
        errors = validate_metrics_file(bad_file)
        assert len(errors) > 0
        assert any("Invalid JSON" in e for e in errors)


class TestInterruptionsLogging:
    """Tests for interruption log validator (logging-template.md § Interruption Log)."""

    @staticmethod
    def _question(**overrides):
        entry = {
            "id": "a1f3",
            "ts": "2026-10-23T14:05:11Z",
            "agent": "python-coder",
            "task_id": "TASK-004",
            "type": "question",
            "question": "Which schema applies to the audit fields?",
            "blocker": "AC-2 cannot be met without it",
            "answered_by": "orchestrator",
            "resolution": "Use the schema in logging-template.md",
        }
        entry.update(overrides)
        return entry

    def test_valid_interruptions(self, valid_interruptions):
        """Test that a valid per-task log passes validation."""
        errors = validate_interruptions_file(valid_interruptions)
        assert errors == [], f"Expected no errors, got: {errors}"

    def test_invalid_interruptions(self, invalid_interruptions):
        """Test that a malformed log fails validation."""
        errors = validate_interruptions_file(invalid_interruptions)
        assert len(errors) > 0

    def test_missing_required_field(self):
        """Test that a missing base field is caught."""
        entry = self._question()
        del entry["task_id"]
        errors = validate_interruptions_entry(entry, 1)
        assert any("task_id" in e for e in errors)

    def test_null_outcome_fields_allowed(self):
        """Test that unresolved outcome fields may be null (log-at-blocking moment)."""
        entry = self._question(answered_by=None, resolution=None)
        assert validate_interruptions_entry(entry, 1) == []

    def test_invalid_type(self):
        """Test that an unknown record type is caught."""
        entry = self._question(type="approval")
        errors = validate_interruptions_entry(entry, 1)
        assert any("Invalid type" in e for e in errors)

    def test_invalid_timestamp(self):
        """Test that a non-UTC or non-ISO timestamp is caught."""
        entry = self._question(ts="2026-10-23 14:05:11")
        errors = validate_interruptions_entry(entry, 1)
        assert any("timestamp" in e.lower() for e in errors)

    def test_agent_at_prefix_rejected(self):
        """Test that the agent name must be recorded without '@'."""
        entry = self._question(agent="@python-coder")
        errors = validate_interruptions_entry(entry, 1)
        assert any("without '@'" in e for e in errors)

    def test_invalid_decision(self):
        """Test that a tool_approval decision must be approved or denied."""
        entry = {
            "id": "b7c2",
            "ts": "2026-10-23T14:05:19Z",
            "agent": "python-coder",
            "task_id": "TASK-004",
            "type": "tool_approval",
            "tool": "supabase",
            "action": "db push --linked",
            "decision": "maybe",
            "decision_by": "user",
        }
        errors = validate_interruptions_entry(entry, 1)
        assert any("Invalid decision" in e for e in errors)

    def test_invalid_impact(self):
        """Test that escalation impact is one of high, medium, low."""
        entry = {
            "id": "c9d4",
            "ts": "2026-10-23T15:01:02Z",
            "agent": "solution-architect",
            "task_id": "TASK-004",
            "type": "escalation",
            "impact": "critical",
            "escalated_to": "human",
            "options": ["frontmatter-only", "body-table"],
            "resolution": "frontmatter-only",
            "decided_by": "human",
        }
        errors = validate_interruptions_entry(entry, 1)
        assert any("Invalid impact" in e for e in errors)

    def test_options_must_be_array(self):
        """Test that escalation options must be a non-empty array."""
        entry = {
            "id": "c9d4",
            "ts": "2026-10-23T15:01:02Z",
            "agent": "solution-architect",
            "task_id": "TASK-004",
            "type": "escalation",
            "impact": "high",
            "escalated_to": "human",
            "options": "frontmatter-only",
            "resolution": "frontmatter-only",
            "decided_by": "human",
        }
        errors = validate_interruptions_entry(entry, 1)
        assert any("'options'" in e for e in errors)


    def test_mixed_tasks_rejected(self, tmp_path):
        """Test that a log may not mix records from different tasks."""
        log = tmp_path / "TASK-004.jsonl"
        log.write_text(
            json.dumps(self._question()) + "\n"
            + json.dumps(self._question(id="a1f4", task_id="TASK-005")) + "\n"
        )
        errors = validate_interruptions_file(log)
        assert any("multiple tasks" in e for e in errors)

    def test_legacy_filename_rejected(self, tmp_path):
        """Test that per-agent/per-timestamp log names are rejected as drift."""
        legacy = tmp_path / "python-coder-TASK-004-20261023T140511Z.jsonl"
        legacy.write_text(json.dumps(self._question()) + "\n")
        errors = validate_interruptions_file(legacy)
        assert any("one rolling log per task" in e for e in errors)

    def test_duplicate_ids_rejected(self, tmp_path):
        """Test that record ids must be unique within a log."""
        log = tmp_path / "TASK-004.jsonl"
        log.write_text(json.dumps(self._question()) + "\n" + json.dumps(self._question()) + "\n")
        errors = validate_interruptions_file(log)
        assert any("Duplicate record id" in e for e in errors)

    def test_resolution_ref_must_resolve(self, tmp_path):
        """Test that a resolution record must reference an existing record id."""
        log = tmp_path / "TASK-004.jsonl"
        log.write_text(
            json.dumps(self._question()) + "\n"
            + json.dumps(
                {
                    "id": "d5e6",
                    "ts": "2026-10-23T15:10:00Z",
                    "agent": "python-coder",
                    "task_id": "TASK-004",
                    "type": "resolution",
                    "ref": "zzzz",
                    "resolution": "Use the schema in logging-template.md",
                    "decided_by": "orchestrator",
                }
            )
            + "\n"
        )
        errors = validate_interruptions_file(log)
        assert any("does not match any record id" in e for e in errors)

    def test_resolution_record_resolves(self, tmp_path):
        """Test that a resolution record referencing a real id passes."""
        log = tmp_path / "TASK-004.jsonl"
        log.write_text(
            json.dumps(self._question(answered_by=None, resolution=None)) + "\n"
            + json.dumps(
                {
                    "id": "d5e6",
                    "ts": "2026-10-23T15:10:00Z",
                    "agent": "python-coder",
                    "task_id": "TASK-004",
                    "type": "resolution",
                    "ref": "a1f3",
                    "resolution": "Use the schema in logging-template.md",
                    "decided_by": "orchestrator",
                }
            )
            + "\n"
        )
        assert validate_interruptions_file(log) == []

    def test_empty_file_valid(self, tmp_path):
        """Test that an empty log is valid."""
        log = tmp_path / "TASK-004.jsonl"
        log.write_text("")
        assert validate_interruptions_file(log) == []

    def test_invalid_json(self, tmp_path):
        """Test that invalid JSON is caught."""
        log = tmp_path / "TASK-004.jsonl"
        log.write_text("not valid json\n")
        errors = validate_interruptions_file(log)
        assert any("Invalid JSON" in e for e in errors)

    def test_interruptions_path_detection(self):
        """Test that only artefacts/build/interruptions/ paths route to this validator."""
        assert is_interruptions_log("artefacts/build/interruptions/TASK-004.jsonl")
        assert not is_interruptions_log("artefacts/build/interruptions/nested/TASK-004.jsonl")
        assert not is_interruptions_log("artefacts/build/metrics/session-log.jsonl")

    def test_interruption_log_requires_jsonl_suffix(self):
        """Test that output path validation requires a .jsonl interruption log."""
        assert validate_output_path("artefacts/build/interruptions/TASK-004.jsonl") == []
        errors = validate_output_path("artefacts/build/interruptions/TASK-004.log")
        assert any(".jsonl" in e for e in errors)

    def test_main_auto_detects_interruptions_log(self, tmp_path, monkeypatch, capsys):
        """Test that a bare interruption log path routes to the interruption validator."""
        log_dir = tmp_path / "artefacts" / "build" / "interruptions"
        log_dir.mkdir(parents=True)
        log = log_dir / "TASK-004.jsonl"
        log.write_text(json.dumps(self._question()) + "\n")

        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr(sys, "argv", ["workspace_conventions.py", str(log)])

        assert workspace_conventions_main() == 0
        assert "interruption logging format" in capsys.readouterr().out

    def test_main_auto_detects_metrics_log(self, tmp_path, monkeypatch, capsys):
        """Test that a bare metrics path still routes to the metrics validator."""
        metrics_dir = tmp_path / "artefacts" / "build" / "metrics"
        metrics_dir.mkdir(parents=True)
        log = metrics_dir / "session-log.jsonl"
        log.write_text(
            json.dumps(
                {
                    "ts": "2025-01-28T09:00:00Z",
                    "task": "DS-001",
                    "agent": "python-coder",
                    "event": "start",
                    "tokens": {"in": 1200, "out": 450, "source": "api_response"},
                }
            )
            + "\n"
        )

        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr(sys, "argv", ["workspace_conventions.py", str(log)])

        assert workspace_conventions_main() == 0
        assert "metrics logging format" in capsys.readouterr().out


class TestTypstFormatting:
    """Tests for Typst markdown formatting validator."""

    def test_valid_formatting(self, tmp_path):
        """Test that well-formatted markdown passes."""
        md_file = tmp_path / "valid.md"
        md_file.write_text(
            "# Title\n\n"
            "## Table of Contents\n\n"
            "---\n\n"
            "## Section One\n\n"
            "Some text here.\n\n"
            "```mermaid\ngraph TD\nA --> B\n```\n\n\n"
            "---\n\n"
            "## Section Two\n"
        )
        errors = check_and_fix_file(md_file, fix=False)
        assert len(errors) == 0

    def test_mermaid_insufficient_blank_lines(self, tmp_path):
        """Test that mermaid fence without 2 trailing blanks fails and can be fixed."""
        md_file = tmp_path / "mermaid_bad.md"
        md_file.write_text(
            "# Title\n\n"
            "---\n\n"
            "## Diagrams\n\n"
            "```mermaid\ngraph TD\nA --> B\n```\n"
            "Next paragraph without blank lines.\n"
        )
        errors = check_and_fix_file(md_file, fix=False)
        assert len(errors) == 1
        assert "Mermaid diagram fence must be followed by at least 2 blank lines" in errors[0]

        # Fix and re-check
        check_and_fix_file(md_file, fix=True)
        errors_after = check_and_fix_file(md_file, fix=False)
        assert len(errors_after) == 0
        content = md_file.read_text()
        assert "```\n\n\nNext paragraph" in content

    def test_section_heading_without_separator(self, tmp_path):
        """Test that level 2 heading without --- separator fails and can be fixed."""
        md_file = tmp_path / "heading_bad.md"
        md_file.write_text(
            "# Title\n\n"
            "## Section Without Rule\n\n"
            "Some content.\n"
        )
        errors = check_and_fix_file(md_file, fix=False)
        assert len(errors) == 1
        assert "must be preceded by '---' horizontal rule" in errors[0]

        # Fix and re-check
        check_and_fix_file(md_file, fix=True)
        errors_after = check_and_fix_file(md_file, fix=False)
        assert len(errors_after) == 0
        content = md_file.read_text()
        assert "---\n\n## Section Without Rule" in content

    def test_typst_skip_blocks_ignored(self, tmp_path):
        """Test that headings inside typst-skip blocks are not flagged."""
        md_file = tmp_path / "skipped.md"
        md_file.write_text(
            "# Title\n\n"
            "<!-- typst-skip-start -->\n"
            "## Skipped Heading\n"
            "<!-- typst-skip-end -->\n"
        )
        errors = check_and_fix_file(md_file, fix=False)
        assert len(errors) == 0

    def test_headings_in_code_blocks_ignored(self, tmp_path):
        """Test that headings inside code blocks are not flagged."""
        md_file = tmp_path / "code_block.md"
        md_file.write_text(
            "# Title\n\n"
            "---\n\n"
            "## Real Heading\n\n"
            "```yaml\n"
            "## Heading In Code\n"
            "key: value\n"
            "```\n\n\n"
            "---\n\n"
            "## Another Heading\n"
        )
        errors = check_and_fix_file(md_file, fix=False)
        assert len(errors) == 0


class TestWorkspaceOutputLocations:
    """Tests for workspace output locations validator."""

    def test_valid_output_paths(self):
        """Test valid directory structure and file naming."""
        paths = [
            "artefacts/build/tasks.md",
            "artefacts/architecture/architecture.md",
            "artefacts/test-results/v2-001-results.txt",
            "services/auth/tests/test_auth.py",
        ]
        errors = validate_output_paths(paths)
        assert len(errors) == 0

    def test_invalid_artefact_subdir(self):
        """Test invalid artefact subdirectory."""
        paths = ["artefacts/invalid_sub/tasks.md"]
        errors = validate_output_paths(paths)
        assert len(errors) > 0
        assert "Invalid artefact subdirectory" in errors[0]

    def test_invalid_test_result_name(self):
        """Test test result not following convention."""
        paths = ["artefacts/test-results/bad_results.md"]
        errors = validate_output_paths(paths)
        assert len(errors) > 0
        assert "v2-{task-id}-results.txt" in errors[0]


class TestUIDev:
    """Tests for UI development invariants validator."""

    def test_important_forbidden(self, tmp_path):
        """Test that !important is flagged."""
        p = tmp_path / "Component.tsx"
        content = "const styles = { color: 'red !important' };"
        violations = check_important(p, content)
        assert len(violations) > 0
        assert "!important" in violations[0][1]

    def test_raw_hex_forbidden(self, tmp_path):
        """Test that raw hex colours are flagged."""
        p = tmp_path / "Button.tsx"
        content = "<button className=\"bg-[#1a2b3c]\">Click</button>"
        violations = check_raw_hex(p, content)
        assert len(violations) > 0
        assert "raw hex colour" in violations[0][1]

    def test_css_files_restriction(self, tmp_path):
        """Test that multiple/scoped CSS files are flagged."""
        css_dir = tmp_path / "frontend" / "src"
        css_dir.mkdir(parents=True)
        (css_dir / "index.css").write_text("/* main */")
        (css_dir / "Button.css").write_text("/* scoped */")
        violations = check_css_files(css_dir)
        assert len(violations) == 1
        assert "component-scoped CSS/SCSS" in violations[0]


class TestSupabase:
    """Tests for Supabase invariants validator."""

    def test_supabase_import_outside_database_service(self, tmp_path):
        """Test that importing supabase in app code is flagged."""
        app_file = tmp_path / "services" / "billing" / "charge.py"
        app_file.parent.mkdir(parents=True)
        app_file.write_text("import supabase\nclient = supabase.create_client()")
        violations = check_supabase_imports([app_file])
        assert len(violations) == 1
        assert "imported outside database service" in violations[0]

    def test_supabase_import_inside_database_service_allowed(self, tmp_path):
        """Test that importing supabase inside database service is allowed."""
        db_file = tmp_path / "services" / "database_service" / "client.py"
        db_file.parent.mkdir(parents=True)
        db_file.write_text("import supabase\nclient = supabase.create_client()")
        violations = check_supabase_imports([db_file])
        assert len(violations) == 0

    def test_migration_audit_row_required(self, tmp_path):
        """Test that migration SQL requires audit row insert."""
        migration_file = tmp_path / "supabase" / "migrations" / "20260915_init.sql"
        migration_file.parent.mkdir(parents=True)
        migration_file.write_text("CREATE TABLE users (id serial primary key);")
        violations = check_migration_audit([migration_file])
        assert len(violations) == 1
        assert "schema_migrations" in violations[0]

        # Add audit row
        migration_file.write_text(
            "CREATE TABLE users (id serial primary key);\n"
            "INSERT INTO schema_migrations (migration_file, applied_at) VALUES ('20260915_init.sql', now());"
        )
        violations_after = check_migration_audit([migration_file])
        assert len(violations_after) == 0


class TestTestingInvariants:
    """Tests for testing invariants validator."""

    def test_forbidden_interaction_mock(self, tmp_path):
        """Test that interaction assertions on internal collaborators are flagged."""
        test_file = tmp_path / "test_service.py"
        content = "mock_service.assert_called_once_with('data')"
        violations = check_forbidden_mocks(test_file, content)
        assert len(violations) == 1
        assert "interaction-based assertion prohibited" in violations[0][1]

    def test_exempt_interaction_mock(self, tmp_path):
        """Test that mocks with # io-boundary marker are exempt."""
        test_file = tmp_path / "test_service.py"
        content = "mock_network.assert_called_once_with('url')  # io-boundary"
        violations = check_forbidden_mocks(test_file, content)
        assert len(violations) == 0


class TestTypeScriptEnvironment:
    """Tests for TypeScript environment invariants validator."""

    def test_package_lock_flagged(self, tmp_path):
        """Test that package-lock.json is flagged."""
        lock = tmp_path / "package-lock.json"
        lock.write_text("{}")
        violations = check_package_lock(tmp_path)
        assert len(violations) == 1
        assert "package-lock.json is strictly forbidden" in violations[0]

    def test_tsconfig_strictness(self, tmp_path):
        """Test that strict compiler options are enforced."""
        tsconfig = tmp_path / "tsconfig.json"
        tsconfig.write_text("""{
            "compilerOptions": {
                "strict": false,
                "noImplicitAny": true
            }
        }""")
        violations = check_tsconfig_strictness(tsconfig)
        assert any("compilerOptions.strict" in v for v in violations)
        assert any("compilerOptions.strictNullChecks" in v for v in violations)

    def test_workspaces_validation(self, tmp_path):
        """Test that subprojects are registered in root package.json."""
        root_pkg = tmp_path / "package.json"
        root_pkg.write_text("""{
            "workspaces": ["frontend"]
        }""")
        sub_pkg = tmp_path / "packages" / "common" / "package.json"
        sub_pkg.parent.mkdir(parents=True)
        sub_pkg.write_text("{}")
        violations = check_workspaces(tmp_path)
        assert len(violations) == 1
        assert "must be listed in root package.json workspaces" in violations[0]


class TestUITesting:
    """Tests for UI testing invariants validator."""

    def test_banned_dependencies_flagged(self, tmp_path):
        """Test that full puppeteer, playwright, and cypress are banned."""
        pkg = tmp_path / "package.json"
        pkg.write_text("""{
            "devDependencies": {
                "puppeteer": "^22.0.0",
                "playwright": "^1.40.0"
            }
        }""")
        violations = check_forbidden_ui_test_deps(pkg)
        assert len(violations) == 2
        assert any("puppeteer is banned" in v for v in violations)
        assert any("playwright is banned" in v for v in violations)

    def test_puppeteer_core_allowed(self, tmp_path):
        """Test that puppeteer-core is permitted."""
        pkg = tmp_path / "package.json"
        pkg.write_text("""{
            "devDependencies": {
                "puppeteer-core": "^22.0.0"
            }
        }""")
        violations = check_forbidden_ui_test_deps(pkg)
        assert len(violations) == 0


class TestSecrets:
    """Tests for secrets invariants validator."""

    def test_private_key_flagged(self, tmp_path):
        """Test that private key block is flagged."""
        key_file = tmp_path / "key.pem"
        key_file.write_text("-----BEGIN RSA PRIVATE KEY-----\nMIIE...\n-----END RSA PRIVATE KEY-----")
        violations = scan_file_for_secrets(key_file)
        assert len(violations) == 1
        assert "Private key block" in violations[0]

    def test_env_file_with_secret_flagged(self, tmp_path):
        """Test that .env file with secrets is flagged."""
        env_file = tmp_path / ".env"
        env_file.write_text("API_SECRET_KEY='supersecret123456789012345'")
        violations = scan_file_for_secrets(env_file)
        assert len(violations) == 1
        assert ".env files with credentials are strictly forbidden" in violations[0]


class TestSubrepoFreshness:
    """Tests for subrepo freshness validator."""

    def test_find_subrepos(self, tmp_path):
        subrepo_dir = tmp_path / "test-subrepo"
        subrepo_dir.mkdir(parents=True)
        gitrepo_file = subrepo_dir / ".gitrepo"
        gitrepo_file.write_text(
            "[subrepo]\n"
            "remote = https://github.com/example/test-upstream.git\n"
            "branch = main\n"
            "commit = a1b2c3d4e5f6\n"
            "parent = 112233445566\n"
            "method = merge\n"
            "cmdver = 0.4.9\n"
        )
        subrepos = find_subrepos(tmp_path)
        assert len(subrepos) == 1
        config = subrepos[0]
        assert config.name == "test-subrepo"
        assert config.remote == "https://github.com/example/test-upstream.git"
        assert config.branch == "main"
        assert config.commit == "a1b2c3d4e5f6"
        assert config.parent == "112233445566"

    def test_query_upstream_head_success(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(
                args=["git", "ls-remote"],
                returncode=0,
                stdout="a1b2c3d4e5f6refs/heads/main\n",
                stderr="",
            )
            head = query_upstream_head("https://github.com/example/repo.git", "main")
            assert head == "a1b2c3d4e5f6refs/heads/main"

    def test_query_upstream_head_failure(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(
                args=["git", "ls-remote"],
                returncode=128,
                stdout="",
                stderr="fatal: remote not found",
            )
            head = query_upstream_head("https://github.com/example/nonexistent.git", "main")
            assert head is None

    def test_subrepo_fresh_when_commit_matches(self, tmp_path):
        subrepo_dir = tmp_path / "test-subrepo"
        subrepo_dir.mkdir(parents=True)
        (subrepo_dir / ".gitrepo").write_text(
            "[subrepo]\nremote = https://github.com/example/repo.git\nbranch = main\ncommit = a1b2c3d4e5f6\n"
        )
        with (
            patch(
                "context.scripts.validators.subrepo_freshness.query_upstream_head",
                return_value="a1b2c3d4e5f6",
            ),
            patch(
                "context.scripts.validators.subrepo_freshness.get_modified_files",
                return_value={"test-subrepo/some_file.py"},
            ),
        ):
            is_fresh, issues = check_subrepo_freshness(repo_root=tmp_path)
            assert is_fresh is True
            assert len(issues) == 0

    def test_subrepo_stale_with_changes_fails(self, tmp_path):
        subrepo_dir = tmp_path / "test-subrepo"
        subrepo_dir.mkdir(parents=True)
        (subrepo_dir / ".gitrepo").write_text(
            "[subrepo]\nremote = https://github.com/example/repo.git\nbranch = main\ncommit = a1b2c3d4e5f6\n"
        )
        with (
            patch(
                "context.scripts.validators.subrepo_freshness.query_upstream_head",
                return_value="different_new_sha_9999",
            ),
            patch(
                "context.scripts.validators.subrepo_freshness.get_modified_files",
                return_value={"test-subrepo/some_file.py"},
            ),
        ):
            is_fresh, issues = check_subrepo_freshness(repo_root=tmp_path)
            assert is_fresh is False
            assert len(issues) == 1
            assert "out of sync with upstream" in issues[0]
            assert "git subrepo pull test-subrepo" in issues[0]

    def test_subrepo_stale_without_changes_passes(self, tmp_path):
        subrepo_dir = tmp_path / "test-subrepo"
        subrepo_dir.mkdir(parents=True)
        (subrepo_dir / ".gitrepo").write_text(
            "[subrepo]\nremote = https://github.com/example/repo.git\nbranch = main\ncommit = a1b2c3d4e5f6\n"
        )
        with (
            patch(
                "context.scripts.validators.subrepo_freshness.query_upstream_head",
                return_value="different_new_sha_9999",
            ),
            patch(
                "context.scripts.validators.subrepo_freshness.get_modified_files",
                return_value={"other-directory/unrelated.md"},
            ),
        ):
            is_fresh, issues = check_subrepo_freshness(repo_root=tmp_path)
            assert is_fresh is True
            assert len(issues) == 0

    def test_subrepo_check_all_forces_stale_detection(self, tmp_path):
        subrepo_dir = tmp_path / "test-subrepo"
        subrepo_dir.mkdir(parents=True)
        (subrepo_dir / ".gitrepo").write_text(
            "[subrepo]\nremote = https://github.com/example/repo.git\nbranch = main\ncommit = a1b2c3d4e5f6\n"
        )
        with (
            patch(
                "context.scripts.validators.subrepo_freshness.query_upstream_head",
                return_value="different_new_sha_9999",
            ),
            patch(
                "context.scripts.validators.subrepo_freshness.get_modified_files",
                return_value=set(),
            ),
        ):
            is_fresh, issues = check_subrepo_freshness(repo_root=tmp_path, check_all=True)
            assert is_fresh is False
            assert len(issues) == 1

    def test_subrepo_unreachable_network_handling(self, tmp_path):
        subrepo_dir = tmp_path / "test-subrepo"
        subrepo_dir.mkdir(parents=True)
        (subrepo_dir / ".gitrepo").write_text(
            "[subrepo]\nremote = https://github.com/example/repo.git\nbranch = main\ncommit = a1b2c3d4e5f6\n"
        )
        with (
            patch(
                "context.scripts.validators.subrepo_freshness.query_upstream_head",
                return_value=None,
            ),
            patch(
                "context.scripts.validators.subrepo_freshness.get_modified_files",
                return_value={"test-subrepo/file.py"},
            ),
        ):
            is_fresh, issues = check_subrepo_freshness(repo_root=tmp_path, allow_offline=False)
            assert is_fresh is False
            assert "Unable to reach upstream remote" in issues[0]

            is_fresh, issues = check_subrepo_freshness(repo_root=tmp_path, allow_offline=True)
            assert is_fresh is True

    def test_main_cli_success(self, tmp_path, monkeypatch):
        subrepo_dir = tmp_path / "test-subrepo"
        subrepo_dir.mkdir(parents=True)
        (subrepo_dir / ".gitrepo").write_text(
            "[subrepo]\nremote = https://github.com/example/repo.git\nbranch = main\ncommit = a1b2c3d4e5f6\n"
        )
        monkeypatch.chdir(tmp_path)
        with (
            patch(
                "context.scripts.validators.subrepo_freshness.query_upstream_head",
                return_value="a1b2c3d4e5f6",
            ),
            patch(
                "context.scripts.validators.subrepo_freshness.get_modified_files",
                return_value={"test-subrepo/file.py"},
            ),
            patch("sys.argv", ["subrepo_freshness.py"]),
        ):
            exit_code = subrepo_freshness_main()
            assert exit_code == 0


class TestLoggingTemplateDocs:
    """Tests that the canonical logging template matches the enforced schema.

    context/templates/logging-template.md is the single home for both log
    schemas. These tests fail when a validator gains a field or value that the
    template does not document, so the docs cannot silently drift from code.
    """

    TEMPLATES = Path(__file__).resolve().parents[3] / "context" / "templates"

    def test_template_documents_metrics_schema(self):
        """Test that every enforced metrics field and value appears in the template."""
        text = (self.TEMPLATES / "logging-template.md").read_text()
        for token in REQUIRED_METRICS_FIELDS + VALID_METRICS_EVENTS + VALID_TOKEN_SOURCES:
            assert f"`{token}`" in text, f"logging-template.md omits '{token}'"

    def test_template_documents_interruption_schema(self):
        """Test that every enforced interruption field and value appears in the template."""
        text = (self.TEMPLATES / "logging-template.md").read_text()
        tokens = (
            INTERRUPTION_BASE_FIELDS
            + VALID_INTERRUPTION_TYPES
            + VALID_INTERRUPTION_IMPACTS
            + VALID_INTERRUPTION_DECISIONS
        )
        for fields in INTERRUPTION_TYPE_FIELDS.values():
            tokens += fields
        for token in tokens:
            assert f"`{token}`" in text, f"logging-template.md omits '{token}'"

    def test_agent_template_references_logging_template(self):
        """Test that the agent template points at the schema instead of restating it."""
        text = (self.TEMPLATES / "agent-template.md").read_text()
        assert "context/templates/logging-template.md" in text

