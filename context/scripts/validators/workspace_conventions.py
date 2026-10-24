#!/usr/bin/env python3
from __future__ import annotations

"""Validate workspace conventions (context/rules/workspace-conventions.md).

Enforces:
1. Output locations and naming conventions (Section 1)
2. Conventional commit message format and Agent-Session trailers (Section 2)
3. Agent metrics logging format in artefacts/build/metrics/*.jsonl (Section 3)
4. Interruption logging format in artefacts/build/interruptions/*.jsonl (Section 4) —
   schema defined by context/templates/logging-template.md § Interruption Log
"""

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any

# --- Section 1: Output Locations & Naming Conventions ---

VALID_OUTPUT_TOP_DIRS = {"artefacts", "secrets", "services"}
VALID_ARTEFACT_SUBDIRS = {"architecture", "build", "product", "test-results", "design"}

TEST_RESULT_PATTERN = re.compile(r"^v2-[a-zA-Z0-9-]+-results\.txt$")
REVIEW_PATTERN = re.compile(r"^[a-zA-Z0-9.-]+-review\.md$")
IMPL_DOC_PATTERN = re.compile(r"^[a-zA-Z0-9_-]+-IMPLEMENTATION\.md$")


def validate_output_path(path: str | Path) -> list[str]:
    """Validate that a generated file lands in an allowed directory with correct naming conventions."""
    p = Path(path)
    parts = p.parts
    if not parts:
        return []

    errors: list[str] = []

    # Check top-level directories if relative path given
    if len(parts) >= 2:
        top_dir = parts[0]
        if top_dir == "artefacts":
            sub_dir = parts[1]
            if sub_dir not in VALID_ARTEFACT_SUBDIRS:
                errors.append(
                    f"Invalid artefact subdirectory '{sub_dir}' in '{path}'. "
                    f"Must be one of: {', '.join(sorted(VALID_ARTEFACT_SUBDIRS))}"
                )
            if sub_dir == "test-results" and len(parts) == 3:
                filename = parts[2]
                if not (TEST_RESULT_PATTERN.match(filename) or filename.endswith((".txt", ".json"))):
                    errors.append(
                        f"Test result file '{filename}' should follow 'v2-{{task-id}}-results.txt' convention."
                    )
            if sub_dir == "build" and len(parts) >= 4 and parts[2] == "interruptions":
                filename = parts[3]
                if not filename.endswith(".jsonl"):
                    errors.append(
                        f"Interruption log '{filename}' must be JSONL named '{{task-id}}.jsonl' "
                        "(one rolling log per task)."
                    )
            if sub_dir == "build" and len(parts) >= 4 and parts[2] == "metrics":
                filename = parts[3]
                if not filename.endswith(".jsonl"):
                    errors.append(
                        f"Metrics log '{filename}' must be JSONL "
                        "(artefacts/build/metrics/session-log.jsonl)."
                    )
        elif top_dir == "services":
            if len(parts) >= 3 and parts[2] == "tests":
                # Valid service test directory
                pass
        elif top_dir == "secrets":
            # Secrets directory
            pass
        elif top_dir == "metrics":
            # Metrics are build records, not a top-level output category.
            errors.append(
                f"Metrics logs belong in 'artefacts/build/metrics/', not at the repository root "
                f"(found '{path}')"
            )

    return errors


def validate_output_paths(paths: list[str | Path]) -> list[str]:
    """Validate multiple output paths."""
    all_errors: list[str] = []
    for p in paths:
        all_errors.extend(validate_output_path(p))
    return all_errors


# --- Section 2: Git Commits ---

VALID_COMMIT_TYPES = r"(feat|fix|test|refactor|docs|chore|perf)"
COMMIT_SUBJECT_PATTERN = re.compile(rf"^{VALID_COMMIT_TYPES}\([a-z][a-z0-9-]*\): .{{1,}}$")
COAUTHOR_PATTERN = re.compile(r"^Co-Authored-By: .+ <.+@.+\..+>$")
AGENT_SESSION_PATTERN = re.compile(
    r"^Agent-Session: tool=[a-z0-9-]+ model=[a-z0-9.-]+ agents=[a-z0-9,-]+"
    r"( duration=\d+[mh])?"
    r"( dispatch=(human|orchestrator))?"
    r"( interactions=\d+)?"
    r"( approvals=\d+)?"
    r"( tokens=\d+(\.\d+)?K?/\d+(\.\d+)?K?)?$"
)
TOOL_FIELD_PATTERN = re.compile(r"\btool=([a-z0-9-]+)")
MODEL_FIELD_PATTERN = re.compile(r"\bmodel=([a-z0-9.-]+)")


# -----------------------------------------------------------------------------
# Runtime telemetry corroboration for Agent-Session tool=/model=
# -----------------------------------------------------------------------------

_RUNTIME_TELEMETRY_MODULE = None


def _load_runtime_telemetry():
    """Import prepare-commit-msg.py (the hook) to reuse its runtime extractors."""
    global _RUNTIME_TELEMETRY_MODULE
    if _RUNTIME_TELEMETRY_MODULE is not None:
        return _RUNTIME_TELEMETRY_MODULE
    hook_path = Path(__file__).resolve().parent.parent / "prepare-commit-msg.py"
    spec = importlib.util.spec_from_file_location("prepare_commit_msg", hook_path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod  # required: module-level @dataclass resolves via __module__
    spec.loader.exec_module(mod)
    _RUNTIME_TELEMETRY_MODULE = mod
    return mod


def corroborate_agent_session(declared_tool: str, declared_model: str, repo_root: str) -> tuple[bool, str]:
    """Check declared tool=/model= against runtime session telemetry.

    Tools without a framework extractor (unknown third-party tools such as
    'cursor') are not adjudicated. Framework tools must be corroborated by an
    active runtime session: a model the runtime contradicts — or cannot confirm
    at all — is rejected.
    """
    try:
        mod = _load_runtime_telemetry()
    except Exception as exc:
        return False, f"cannot be corroborated: telemetry module unavailable ({exc})"

    extractor_cls = mod.EXTRACTORS.get(declared_tool.lower())
    if extractor_cls is None:
        # Third-party tool with no canonical telemetry store.
        return True, ""

    try:
        extractor = extractor_cls()
        available = extractor.is_available()
    except Exception as exc:
        return False, f"tool='{declared_tool}' cannot be corroborated: extractor error ({exc})"

    if not available:
        return False, f"tool='{declared_tool}' cannot be corroborated: no {declared_tool} runtime telemetry found"

    try:
        result = extractor.extract_delta(repo_root, {})
    except Exception as exc:
        return False, f"tool='{declared_tool}' cannot be corroborated: extraction error ({exc})"

    if result.error:
        return False, f"tool='{declared_tool}' cannot be corroborated: {result.error}"

    runtime_model = mod.short_model(result.model)
    if not runtime_model:
        return False, f"tool='{declared_tool}' cannot be corroborated: runtime reported no model"
    if runtime_model != declared_model:
        return False, (
            f"model='{declared_model}' contradicts runtime telemetry for "
            f"tool='{declared_tool}' (actual: {runtime_model}); write model= via prepare-commit-msg"
        )
    return True, ""


def validate_commit_message(msg: str, repo_root: str | None = None) -> tuple[bool, str]:
    """Validate commit message against conventional commits and agent trailers."""
    lines = msg.strip().split("\n")
    if not lines or not lines[0].strip():
        return False, "Empty commit message"

    subject = lines[0]
    if not COMMIT_SUBJECT_PATTERN.match(subject):
        return False, (
            f"Invalid subject line: '{subject}'\n"
            "Expected: {type}({scope}): {description}\n"
            "Valid types: feat, fix, test, refactor, docs, chore, perf\n"
            "Scope: lowercase, alphanumeric with hyphens\n"
            "Example: feat(auth): add token refresh endpoint"
        )

    if len(subject) > 72:
        return False, f"Subject line too long ({len(subject)} chars, max 72): {subject}"

    description = subject.split(": ", 1)[1] if ": " in subject else ""
    if description:
        first_word = description.split()[0].lower()
        if first_word.endswith(("ed", "ing")):
            return False, (
                f"Description should use imperative mood: '{description}'\n"
                "Use 'add' not 'added', 'fix' not 'fixing'"
            )

    has_coauthor = False
    for line in lines:
        if line.startswith("Co-Authored-By:"):
            has_coauthor = True
            if not COAUTHOR_PATTERN.match(line):
                return False, f"Invalid Co-Authored-By format: {line}"

    has_agent_session = False
    declared_tool = ""
    declared_model = ""
    for line in lines:
        if line.startswith("Agent-Session:"):
            has_agent_session = True
            if not AGENT_SESSION_PATTERN.match(line):
                return False, (
                    f"Invalid Agent-Session format: {line}\n"
                    "Expected: Agent-Session: tool=<tool> model=<model> agents=<agents>"
                    " [duration=45m] [dispatch=orchestrator] [interactions=0] [approvals=2]"
                    " [tokens=8.2K/5.1K]\n"
                    "Triplet: tool, model, agents from context/agents"
                )
            tool_m = TOOL_FIELD_PATTERN.search(line)
            model_m = MODEL_FIELD_PATTERN.search(line)
            if tool_m:
                declared_tool = tool_m.group(1)
            if model_m:
                declared_model = model_m.group(1)

    if has_agent_session and not has_coauthor:
        return False, "Agent commits require Co-Authored-By line when Agent-Session is present"

    # tool=/model= are hook-owned: a hand-written model that runtime telemetry
    # contradicts, or cannot confirm, must be rejected (see commit-message-template.md).
    if has_agent_session and declared_tool and declared_model:
        ok, reason = corroborate_agent_session(
            declared_tool,
            declared_model,
            repo_root or str(Path.cwd()),
        )
        if not ok:
            return False, reason

    return True, ""


# --- Section 3: Metrics Logging ---

REQUIRED_METRICS_FIELDS = ["ts", "task", "agent", "event", "tokens"]
VALID_METRICS_EVENTS = ["start", "handoff", "escalate", "complete", "blocked"]
VALID_TOKEN_SOURCES = ["api_response", "estimated", "unavailable"]


def validate_metrics_entry(entry: dict[str, Any], line_num: int) -> list[str]:
    """Validate a single metrics log entry."""
    errors: list[str] = []

    for field in REQUIRED_METRICS_FIELDS:
        if field not in entry:
            errors.append(f"Line {line_num}: Missing required field '{field}'")

    if errors:
        return errors

    ts = entry.get("ts", "")
    if not (ts.endswith(("Z", "]")) or "+" in ts):
        errors.append(
            f"Line {line_num}: Invalid timestamp format '{ts}', expected ISO 8601 (e.g., 2025-01-28T09:00:00Z)"
        )

    event = entry.get("event", "")
    if event not in VALID_METRICS_EVENTS:
        errors.append(
            f"Line {line_num}: Invalid event '{event}', must be one of: {', '.join(VALID_METRICS_EVENTS)}"
        )

    tokens = entry.get("tokens", {})
    if not isinstance(tokens, dict):
        errors.append(f"Line {line_num}: 'tokens' must be an object")
    else:
        if "in" not in tokens or "out" not in tokens:
            errors.append(f"Line {line_num}: 'tokens' must have 'in' and 'out' fields")

        if "source" not in tokens:
            errors.append(f"Line {line_num}: 'tokens' must have 'source' field")
        elif tokens["source"] not in VALID_TOKEN_SOURCES:
            errors.append(
                f"Line {line_num}: Invalid token source '{tokens['source']}', "
                f"must be one of: {', '.join(VALID_TOKEN_SOURCES)}"
            )

        for key in ["in", "out"]:
            if key in tokens and not isinstance(tokens[key], (int, float)):
                errors.append(f"Line {line_num}: tokens.{key} must be a number")

    if event in ["handoff", "escalate"] and "to" not in entry:
        errors.append(f"Line {line_num}: '{event}' event requires 'to' field")

    return errors


def validate_metrics_file(file_path: Path) -> list[str]:
    """Validate metrics log file."""
    all_errors: list[str] = []
    try:
        content = file_path.read_text()
        if not content.strip():
            return []

        for line_num, line in enumerate(content.strip().split("\n"), 1):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError as e:
                all_errors.append(f"Line {line_num}: Invalid JSON - {e}")
                continue
            all_errors.extend(validate_metrics_entry(entry, line_num))
    except (OSError, UnicodeDecodeError) as e:
        all_errors.append(f"Error reading file: {e}")

    return all_errors


# --- Section 4: Interruptions Logging ---
#
# Schema source of truth: context/templates/logging-template.md § Interruption Log.
# One rolling log per task at artefacts/build/interruptions/{task-id}.jsonl; each
# line is a single JSON object, appended and never rewritten.

INTERRUPTIONS_DIRNAME = "interruptions"

INTERRUPTION_BASE_FIELDS = ["id", "ts", "agent", "task_id", "type"]
VALID_INTERRUPTION_TYPES = ["question", "tool_approval", "escalation", "resolution"]
VALID_INTERRUPTION_IMPACTS = ["high", "medium", "low"]
VALID_INTERRUPTION_DECISIONS = ["approved", "denied"]

INTERRUPTION_TYPE_FIELDS = {
    "question": ["question", "blocker", "answered_by", "resolution"],
    "tool_approval": ["tool", "action", "decision", "decision_by"],
    "escalation": ["impact", "escalated_to", "options", "resolution", "decided_by"],
    "resolution": ["ref", "resolution", "decided_by"],
}

# Outcome fields may be null when the record is written at the moment of blocking;
# a `resolution` record is then appended with `ref` pointing at that record's `id`.
INTERRUPTION_NULLABLE_FIELDS = {"answered_by", "resolution", "decision", "decision_by", "decided_by"}

INTERRUPTION_TS_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")


def is_interruptions_log(path: str | Path) -> bool:
    """Return True when the path is an interruption log under artefacts/build/interruptions/."""
    parts = Path(path).parts
    return len(parts) >= 3 and parts[-3:-1] == ("build", INTERRUPTIONS_DIRNAME)


def validate_interruptions_entry(entry: dict[str, Any], line_num: int) -> list[str]:
    """Validate a single interruption log record."""
    errors: list[str] = []

    for field in INTERRUPTION_BASE_FIELDS:
        if field not in entry:
            errors.append(f"Line {line_num}: Missing required field '{field}'")
        elif not isinstance(entry[field], str) or not entry[field].strip():
            errors.append(f"Line {line_num}: Field '{field}' must be a non-empty string")

    if errors:
        return errors

    ts = entry["ts"]
    if not INTERRUPTION_TS_PATTERN.match(ts):
        errors.append(
            f"Line {line_num}: Invalid timestamp '{ts}', "
            "expected ISO 8601 UTC (e.g. 2026-10-23T14:05:11Z)"
        )

    agent = entry["agent"]
    if agent.startswith("@"):
        errors.append(
            f"Line {line_num}: 'agent' must be the agent name without '@' (got '{agent}')"
        )

    record_type = entry["type"]
    if record_type not in VALID_INTERRUPTION_TYPES:
        errors.append(
            f"Line {line_num}: Invalid type '{record_type}', "
            f"must be one of: {', '.join(VALID_INTERRUPTION_TYPES)}"
        )
        return errors

    for field in INTERRUPTION_TYPE_FIELDS[record_type]:
        if field not in entry:
            errors.append(f"Line {line_num}: '{record_type}' record requires '{field}'")
            continue

        value = entry[field]
        if value is None:
            if field not in INTERRUPTION_NULLABLE_FIELDS:
                errors.append(
                    f"Line {line_num}: '{record_type}' record requires a value for '{field}'"
                )
            continue

        if field == "options":
            if (
                not isinstance(value, list)
                or not value
                or not all(isinstance(option, str) and option.strip() for option in value)
            ):
                errors.append(
                    f"Line {line_num}: 'options' must be a non-empty array of strings"
                )
        elif not isinstance(value, str) or not value.strip():
            errors.append(
                f"Line {line_num}: '{field}' must be a non-empty string or null"
            )

    if record_type == "tool_approval":
        decision = entry.get("decision")
        if decision is not None and decision not in VALID_INTERRUPTION_DECISIONS:
            errors.append(
                f"Line {line_num}: Invalid decision '{decision}', "
                f"must be one of: {', '.join(VALID_INTERRUPTION_DECISIONS)}"
            )

    if record_type == "escalation":
        impact = entry.get("impact")
        if impact is not None and impact not in VALID_INTERRUPTION_IMPACTS:
            errors.append(
                f"Line {line_num}: Invalid impact '{impact}', "
                f"must be one of: {', '.join(VALID_INTERRUPTION_IMPACTS)}"
            )

    return errors


def validate_interruptions_file(file_path: Path) -> list[str]:
    """Validate an interruption log: one JSON object per line, one log per task."""
    errors: list[str] = []

    try:
        content = file_path.read_text()
    except (OSError, UnicodeDecodeError) as e:
        return [f"Error reading file: {e}"]

    if not content.strip():
        return errors

    records: list[tuple[int, dict[str, Any]]] = []
    for line_num, line in enumerate(content.splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError as e:
            errors.append(f"Line {line_num}: Invalid JSON - {e}")
            continue
        if not isinstance(entry, dict):
            errors.append(f"Line {line_num}: Each line must be a JSON object")
            continue
        errors.extend(validate_interruptions_entry(entry, line_num))
        records.append((line_num, entry))

    # One rolling log per task: the filename stem must match every record's task_id.
    # This also rejects the legacy '{agent-name}-{task-id}-{timestamp}.jsonl' naming.
    stem = file_path.stem
    task_ids = sorted(
        {entry["task_id"] for _, entry in records if isinstance(entry.get("task_id"), str)}
    )
    for task_id in task_ids:
        if task_id != stem:
            errors.append(
                f"File '{file_path.name}' must be named '{task_id}.jsonl' — "
                "one rolling log per task, not per agent or per timestamp"
            )

    if len(task_ids) > 1:
        errors.append(
            f"Log contains records for multiple tasks ({', '.join(task_ids)}) — "
            "one rolling log per task"
        )

    # Record ids must be unique so a resolution record can reference exactly one ask.
    seen_ids: dict[str, int] = {}
    for line_num, entry in records:
        record_id = entry.get("id")
        if not isinstance(record_id, str) or not record_id.strip():
            continue
        if record_id in seen_ids:
            errors.append(
                f"Line {line_num}: Duplicate record id '{record_id}' "
                f"(first seen on line {seen_ids[record_id]})"
            )
        else:
            seen_ids[record_id] = line_num

    # A resolution record must point at an ask that exists in this log.
    for line_num, entry in records:
        if entry.get("type") != "resolution":
            continue
        ref = entry.get("ref")
        if isinstance(ref, str) and ref.strip() and ref not in seen_ids:
            errors.append(
                f"Line {line_num}: 'ref' value '{ref}' does not match any record id in this log"
            )

    return errors


# --- CLI Interface ---


def _auto_detect(args: list[str]) -> int:
    """Validate bare path arguments by inferring the artefact kind."""
    first = args[0]
    p = Path(first)
    if "COMMIT_EDITMSG" in first or (
        len(args) == 1 and p.suffix == ".txt" and p.exists() and "(" in p.read_text()[:50]
    ):
        msg = p.read_text()
        if msg.startswith(("Merge ", "Revert ")):
            return 0
        is_valid, err = validate_commit_message(msg, repo_root=str(Path.cwd()))
        if not is_valid:
            print(f"❌ Invalid commit message:\n{err}", file=sys.stderr)
            return 1
        print("✅ Commit message valid")
        return 0

    if p.suffix == ".jsonl":
        if is_interruptions_log(p):
            errors = validate_interruptions_file(p)
            if errors:
                print(f"❌ Interruption logging violations in {p.name}:", file=sys.stderr)
                for err in errors:
                    print(f"  {err}", file=sys.stderr)
                return 1
            print(f"✅ {p.name} follows interruption logging format")
            return 0

        errors = validate_metrics_file(p)
        if errors:
            print(f"❌ Metrics logging violations in {p.name}:", file=sys.stderr)
            for err in errors:
                print(f"  {err}", file=sys.stderr)
            return 1
        print(f"✅ {p.name} follows metrics logging format")
        return 0

    errors = validate_output_paths(args)
    if errors:
        print("❌ Output path violations:", file=sys.stderr)
        for err in errors:
            print(f"  {err}", file=sys.stderr)
        return 1
    print("✅ Output paths conform to workspace conventions")
    return 0


def main() -> int:
    argv = sys.argv[1:]
    known_subcommands = {"commit-msg", "metrics", "interruptions", "paths"}
    # A bare existing path is validated by inference; explicit subcommands, flags,
    # and mistyped subcommands still fall through to argparse.
    if argv and argv[0] not in known_subcommands and Path(argv[0]).exists():
        return _auto_detect(argv)

    parser = argparse.ArgumentParser(
        description="Validate workspace conventions (commits, metrics, interruptions, output paths)"
    )
    subparsers = parser.add_subparsers(dest="subcommand")

    commit_parser = subparsers.add_parser("commit-msg", help="Validate commit message")
    commit_parser.add_argument("file", help="Path to commit message file")

    metrics_parser = subparsers.add_parser("metrics", help="Validate metrics JSONL file")
    metrics_parser.add_argument("file", help="Path to metrics file")

    interruptions_parser = subparsers.add_parser(
        "interruptions", help="Validate interruption log JSONL file"
    )
    interruptions_parser.add_argument("file", help="Path to interruption log file")

    paths_parser = subparsers.add_parser("paths", help="Validate output file paths")
    paths_parser.add_argument("files", nargs="+", help="File paths to validate")

    args = parser.parse_args()

    # Subcommand routing
    if args.subcommand == "commit-msg":
        p = Path(args.file)
        if not p.exists():
            print(f"File not found: {p}", file=sys.stderr)
            return 1
        msg = p.read_text()
        if msg.startswith(("Merge ", "Revert ")):
            return 0
        is_valid, err = validate_commit_message(msg, repo_root=str(Path.cwd()))
        if not is_valid:
            print(f"❌ Invalid commit message:\n{err}", file=sys.stderr)
            return 1
        print("✅ Commit message valid")
        return 0

    if args.subcommand == "metrics":
        p = Path(args.file)
        if not p.exists():
            print(f"File not found: {p}", file=sys.stderr)
            return 1
        errors = validate_metrics_file(p)
        if errors:
            print(f"❌ Metrics logging violations in {p.name}:", file=sys.stderr)
            for err in errors:
                print(f"  {err}", file=sys.stderr)
            return 1
        print(f"✅ {p.name} follows metrics logging format")
        return 0

    if args.subcommand == "interruptions":
        p = Path(args.file)
        if not p.exists():
            print(f"File not found: {p}", file=sys.stderr)
            return 1
        errors = validate_interruptions_file(p)
        if errors:
            print(f"❌ Interruption logging violations in {p.name}:", file=sys.stderr)
            for err in errors:
                print(f"  {err}", file=sys.stderr)
            return 1
        print(f"✅ {p.name} follows interruption logging format")
        return 0

    if args.subcommand == "paths":
        errors = validate_output_paths(args.files)
        if errors:
            print("❌ Output path violations:", file=sys.stderr)
            for err in errors:
                print(f"  {err}", file=sys.stderr)
            return 1
        print("✅ Output paths conform to workspace conventions")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
