"""Unit tests and schema sanity checks for multi-runtime session telemetry.

Covers:
1. Synthetic unit tests (zero-dependency, always run):
   - Protobuf wire format parsing & varint decoding.
   - Antigravity SQLite extraction & index watermarking.
   - GitHub Copilot workspace matching, JSONL parsing & byte-offset seeking.
   - Claude Code session JSONL extraction.
   - Commit message trailer injection and error surfacing.
2. Live runtime location sanity checks:
   - Differentiates between:
     a) Not installed (skipped)
     b) Installed but unused/idle (skipped with diagnostic note)
     c) Installed with sessions but broken/drifted schema (fails test with alert)
"""

import json
import os
import sqlite3
import tempfile
import pytest
from pathlib import Path

import importlib.util

_script_path = Path(__file__).resolve().parent.parent / "prepare-commit-msg.py"
_spec = importlib.util.spec_from_file_location("prepare_commit_msg", _script_path)
_mod = importlib.util.module_from_spec(_spec)
import sys
sys.modules[_spec.name] = _mod
_spec.loader.exec_module(_mod)


AntigravityExtractor = _mod.AntigravityExtractor
ClaudeExtractor = _mod.ClaudeExtractor
CopilotExtractor = _mod.CopilotExtractor
ExtractionResult = _mod.ExtractionResult
_decode_varint = _mod._decode_varint
format_tokens = _mod.format_tokens
parse_protobuf_fields = _mod.parse_protobuf_fields
select_extractor = _mod.select_extractor
update_commit_message = _mod.update_commit_message

ClineExtractor = _mod.ClineExtractor
EXTRACTORS = _mod.EXTRACTORS
short_model = _mod.short_model



# =============================================================================
# 1. Synthetic Unit Tests
# =============================================================================

def test_format_tokens():
    """Verify human-readable token formatting."""
    assert format_tokens(500) == "500"
    assert format_tokens(1000) == "1.0K"
    assert format_tokens(14500) == "14.5K"
    assert format_tokens(1_000_000) == "1.00M"
    assert format_tokens(2_450_000) == "2.45M"


def test_protobuf_wire_format_parsing():
    """Verify raw protobuf wire decoding for varints and length-delimited strings."""
    # Encode varint 150 -> 0x96 0x01
    # Field 1 (wire_type 0 = varint) -> key = (1 << 3) | 0 = 8 -> 0x08 0x96 0x01
    # Field 2 (wire_type 2 = length-delimited) -> key = (2 << 3) | 2 = 18 -> 0x12, len 5, "hello"
    raw = bytes([0x08, 0x96, 0x01, 0x12, 0x05, 0x68, 0x65, 0x6C, 0x6C, 0x6F])
    fields = parse_protobuf_fields(raw)

    assert len(fields) == 2
    assert fields[0] == (1, "varint", 150)
    assert fields[1] == (2, "length_delimited", b"hello")


def _encode_varint(value: int) -> bytes:
    """Helper to encode an integer as protobuf varint."""
    res = bytearray()
    while True:
        b = value & 0x7F
        value >>= 7
        if value > 0:
            res.append(b | 0x80)
        else:
            res.append(b)
            break
    return bytes(res)


def _encode_field(field_num: int, wire_type: int, payload: bytes) -> bytes:
    """Helper to encode a protobuf tag and payload."""
    tag = (field_num << 3) | wire_type
    tag_bytes = _encode_varint(tag)
    if wire_type == 0:
        return tag_bytes + payload
    elif wire_type == 2:
        return tag_bytes + _encode_varint(len(payload)) + payload
    return tag_bytes + payload


def test_antigravity_synthetic_extraction(tmp_path):
    """Verify AntigravityExtractor against an in-memory or synthetic SQLite database."""
    db_path = tmp_path / "test-conv.db"
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    # Create expected Antigravity schema
    cur.execute("CREATE TABLE trajectory_metadata_blob (id text PRIMARY KEY, data blob)")
    cur.execute("CREATE TABLE gen_metadata (idx integer PRIMARY KEY, data blob)")

    repo_root = "/Users/test/my-repo"
    # Store trajectory metadata linking to repo
    meta_payload = f"meta file://{repo_root} conversation_id".encode("utf-8")
    cur.execute("INSERT INTO trajectory_metadata_blob VALUES ('main', ?)", (meta_payload,))

    # Construct synthetic protobuf turn
    # Field 4: token usage submessage
    #   Field 2 (varint): prompt = 1000
    #   Field 5 (varint): cached = 4000
    #   Field 3 (varint): output = 250
    #   Field 9 (varint): thinking = 50
    f4_bytes = (
        _encode_field(2, 0, _encode_varint(1000))
        + _encode_field(5, 0, _encode_varint(4000))
        + _encode_field(3, 0, _encode_varint(250))
        + _encode_field(9, 0, _encode_varint(50))
    )

    # Field 19: model = "gemini-flash"
    f19_bytes = _encode_field(19, 2, b"gemini-flash")

    # Field 1: top turn metadata
    f1_bytes = _encode_field(4, 2, f4_bytes) + f19_bytes

    # Top-level message: field 1 length-delimited
    row0_blob = _encode_field(1, 2, f1_bytes)

    cur.execute("INSERT INTO gen_metadata VALUES (0, ?)", (row0_blob,))
    conn.commit()
    conn.close()

    extractor = AntigravityExtractor()
    extractor.search_dirs = [str(tmp_path)]

    # 1. First extraction from index -1
    res = extractor.extract_delta(repo_root, {"last_idx": -1})
    assert res.error is None
    assert res.tokens_in == 5000  # 1000 prompt + 4000 cached
    assert res.tokens_out == 250
    assert res.thinking_tokens == 50
    assert res.model == "gemini-flash"
    assert res.watermark_updates["last_idx"] == 0

    # 2. Second extraction with watermark at index 0 (no new rows)
    res2 = extractor.extract_delta(repo_root, res.watermark_updates)
    assert res2.error is None
    assert res2.tokens_in == 0
    assert res2.tokens_out == 0


def test_copilot_synthetic_extraction(tmp_path):
    """Verify CopilotExtractor against synthetic VS Code workspace storage."""
    repo_root = "/Users/test/copilot-repo"
    ws_dir = tmp_path / "workspaceStorage" / "mock_hash"
    chat_dir = ws_dir / "chatSessions"
    chat_dir.mkdir(parents=True)

    # Create workspace.json linking to repo
    ws_json = ws_dir / "workspace.json"
    ws_json.write_text(json.dumps({"folder": f"file://{repo_root}"}))

    # Create session JSONL file
    session_file = chat_dir / "session-1.jsonl"
    turn1 = {
        "result": {
            "metadata": {
                "promptTokens": 12500,
                "outputTokens": 350,
                "resolvedModel": "gpt-5-mini",
                "toolCallRounds": [{"thinking": {"tokens": 80}}],
            }
        }
    }
    session_file.write_text(json.dumps(turn1) + "\n")

    extractor = CopilotExtractor()
    extractor.search_dirs = [str(tmp_path / "workspaceStorage")]

    # First extraction
    res = extractor.extract_delta(repo_root, {"offset": 0})
    assert res.error is None
    assert res.tokens_in == 12500
    assert res.tokens_out == 350
    assert res.thinking_tokens == 80
    assert res.model == "gpt-5-mini"
    assert res.watermark_updates["offset"] > 0

    # Append second turn to session file
    turn2 = {
        "result": {
            "metadata": {
                "promptTokens": 2000,
                "completionTokens": 100,
            }
        }
    }
    with open(session_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(turn2) + "\n")

    # Incremental extraction from previous offset
    res2 = extractor.extract_delta(repo_root, res.watermark_updates)
    assert res2.error is None
    assert res2.tokens_in == 2000
    assert res2.tokens_out == 100


def test_commit_message_updating(tmp_path):
    """Verify commit message trailer injection and error surfacing."""
    msg_file = tmp_path / "COMMIT_EDITMSG"

    # 1. Human commit without Agent-Session -> untouched
    msg_file.write_text("feat: human commit without trailer\n")
    assert not update_commit_message(str(msg_file), "tokens=10K/1K")
    assert "tokens=" not in msg_file.read_text()

    # 2. Agent commit -> append tokens
    msg_file.write_text(
        "feat: agent commit\n\nAgent-Session: tool=antigravity model=gemini-flash agents=coder\n"
    )
    assert update_commit_message(str(msg_file), "tokens=15.0K/1.2K")
    content = msg_file.read_text()
    assert "Agent-Session: tool=antigravity model=gemini-flash agents=coder tokens=15.0K/1.2K" in content

    # 3. Existing tokens replacement
    assert update_commit_message(str(msg_file), "tokens=error(schema_drift)")
    assert "tokens=error(schema_drift)" in msg_file.read_text()
    assert "15.0K" not in msg_file.read_text()


# =============================================================================
# 2. Live Runtime Location Sanity Checks
# =============================================================================

def test_live_antigravity_storage_sanity():
    """Verify local Antigravity IDE storage structure if installed.
    
    Discriminates:
    - Skipped if Antigravity is not installed.
    - Skipped if installed but no conversation DBs exist.
    - Fails if databases exist but gen_metadata / protobuf schema cannot be parsed.
    """
    extractor = AntigravityExtractor()
    if not extractor.is_available():
        pytest.skip("Antigravity IDE storage not found on this machine.")

    # Search for conversation databases
    dbs = []
    for s_dir in extractor.search_dirs:
        if os.path.isdir(s_dir):
            dbs.extend(Path(s_dir).glob("*.db"))

    if not dbs:
        pytest.skip("Antigravity is installed, but no conversation databases were found to validate.")

    # Validate that at least one DB has the expected schema
    tested = 0
    for db_path in dbs[:5]:
        try:
            conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
            cur = conn.cursor()
            cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name IN ('trajectory_metadata_blob', 'gen_metadata')"
            )
            tables = {row[0] for row in cur.fetchall()}
            conn.close()
            if "gen_metadata" in tables:
                tested += 1
        except sqlite3.Error as e:
            pytest.fail(f"Antigravity database {db_path} could not be read: {e}")

    if tested == 0:
        pytest.fail("Antigravity databases exist, but none contained the expected gen_metadata table (schema drift).")


def test_live_copilot_storage_sanity():
    """Verify local VS Code Copilot Chat storage structure if installed.
    
    Discriminates:
    - Skipped if VS Code workspaceStorage is not installed.
    - Skipped if installed but no chat session files exist.
    - Fails if session files exist but cannot be parsed as valid JSONL.
    """
    extractor = CopilotExtractor()
    if not extractor.is_available():
        pytest.skip("VS Code workspaceStorage not found on this machine.")

    session_files = []
    for s_dir in extractor.search_dirs:
        if os.path.isdir(s_dir):
            session_files.extend(Path(s_dir).glob("*/chatSessions/*.jsonl"))

    if not session_files:
        pytest.skip("VS Code workspaceStorage exists, but no Copilot chat sessions were found to validate.")

    # Validate JSON parsing on found sessions
    tested = 0
    for sf in session_files[:5]:
        try:
            with open(sf, "r", encoding="utf-8") as f:
                for idx, line in enumerate(f):
                    if line.strip():
                        json.loads(line)
                    if idx > 20:
                        break
            tested += 1
        except Exception as e:
            pytest.fail(f"Copilot session file {sf} failed JSON parsing: {e}")

    assert tested > 0, "No valid Copilot session files could be parsed."


def test_live_claude_storage_sanity():
    """Verify local Claude Code storage structure if installed.
    
    Discriminates:
    - Skipped if ~/.claude/projects is not installed.
    - Skipped if installed but no project sessions exist.
    - Fails if session files exist but fail JSON parsing.
    """
    extractor = ClaudeExtractor()
    if not extractor.is_available():
        pytest.skip("Claude Code storage (~/.claude/projects) not found on this machine.")

    claude_dir = Path(os.path.expanduser("~/.claude/projects"))
    jsonl_files = list(claude_dir.glob("*/*.jsonl")) + list(claude_dir.glob("*/*/*.jsonl"))

    if not jsonl_files:
        pytest.skip("Claude Code directory exists, but no session JSONL files were found.")

    tested = 0
    for jf in jsonl_files[:5]:
        try:
            with open(jf, "r", encoding="utf-8") as f:
                for idx, line in enumerate(f):
                    if line.strip():
                        json.loads(line)
                    if idx > 20:
                        break
            tested += 1
        except Exception as e:
            pytest.fail(f"Claude Code session file {jf} failed JSON parsing: {e}")

    assert tested > 0, "No valid Claude Code session files could be parsed."


# =============================================================================
# Cline extractor
# =============================================================================

def _make_cline_session(root: Path, session_id: str, cwd: str, messages, model="deepseek/test-model", provider="openrouter"):
    """Create a synthetic Cline session tree under <root>/sessions/<session_id>/."""
    sdir = root / "sessions" / session_id
    sdir.mkdir(parents=True)
    meta = {
        "version": 1,
        "session_id": session_id,
        "source": "vscode",
        "status": "running",
        "provider": provider,
        "model": model,
        "cwd": cwd,
        "workspace_root": cwd,
        "metadata": {"title": "test"},
    }
    (sdir / f"{session_id}.json").write_text(json.dumps(meta))
    (sdir / f"{session_id}.messages.json").write_text(json.dumps(messages))
    return sdir


def test_cline_extract_delta_counts_assistant_metrics(tmp_path, monkeypatch):
    """Verify incremental extraction sums assistant-message metrics only."""
    fake_home = tmp_path / "cline"
    monkeypatch.setenv("CLINE_DATA_DIR", str(fake_home))
    repo = tmp_path / "repo"
    repo.mkdir()
    messages = [
        {"role": "user", "content": [{"type": "text", "text": "u1"}], "ts": 1},
        {"role": "assistant", "content": [{"type": "text", "text": "a1"}], "ts": 2,
         "modelInfo": {"id": "deepseek/test-model", "provider": "openrouter"},
         "metrics": {"inputTokens": 100, "cacheReadTokens": 200, "cacheWriteTokens": 0, "outputTokens": 25}},
        {"role": "user", "content": [{"type": "text", "text": "u2"}], "ts": 3},
        {"role": "assistant", "content": [{"type": "text", "text": "a2"}], "ts": 4,
         "modelInfo": {"id": "deepseek/test-model", "provider": "openrouter"},
         "metrics": {"inputTokens": 30, "cacheReadTokens": 0, "cacheWriteTokens": 40, "outputTokens": 10}},
    ]
    _make_cline_session(fake_home, "sess001", str(repo), messages)

    ext = ClineExtractor()
    r = ext.extract_delta(str(repo), {})

    assert r.error is None
    assert r.tokens_in == 370  # (100+200) + (30+0+40); user turns are excluded
    assert r.tokens_out == 35
    assert r.model == "deepseek/test-model"
    assert r.runtime == "cline"

    # Watermark makes the next commit delta-free (idempotent).
    r2 = ext.extract_delta(str(repo), r.watermark_updates)
    assert r2.error is None
    assert r2.tokens_in == 0
    assert r2.tokens_out == 0


def test_cline_extract_delta_accepts_wrapped_messages(tmp_path, monkeypatch):
    """Verify object-enveloped message files (compacted sessions) are parsed."""
    fake_home = tmp_path / "cline"
    monkeypatch.setenv("CLINE_DATA_DIR", str(fake_home))
    repo = tmp_path / "repo"
    repo.mkdir()
    payload = {
        "sessionId": "sess001",
        "messages": [
            {"role": "assistant", "content": [], "ts": 1,
             "modelInfo": {"id": "deepseek/x", "provider": "openrouter"},
             "metrics": {"inputTokens": 20, "cacheReadTokens": 5, "cacheWriteTokens": 0, "outputTokens": 3}},
        ],
    }
    sdir = _make_cline_session(fake_home, "sess001", str(repo), [])
    (sdir / "sess001.messages.json").write_text(json.dumps(payload))

    r = ClineExtractor().extract_delta(str(repo), {})
    assert r.error is None
    assert r.tokens_in == 25
    assert r.tokens_out == 3
    assert r.model == "deepseek/x"


def test_cline_extract_delta_session_switch_resets(tmp_path, monkeypatch):
    """Verify a new session_id resets the index pointer and counts from zero."""
    fake_home = tmp_path / "cline"
    monkeypatch.setenv("CLINE_DATA_DIR", str(fake_home))
    repo = tmp_path / "repo"
    repo.mkdir()
    messages = [
        {"role": "assistant", "content": [{"type": "text", "text": "a1"}], "ts": 1,
         "modelInfo": {"id": "deepseek/test-model", "provider": "openrouter"},
         "metrics": {"inputTokens": 50, "cacheReadTokens": 0, "cacheWriteTokens": 0, "outputTokens": 5}},
    ]
    _make_cline_session(fake_home, "sess001", str(repo), messages)

    ext = ClineExtractor()
    stale = {"session_id": "some-other-session", "last_idx": 99, "total_in": 9999, "total_out": 999}
    r = ext.extract_delta(str(repo), stale)

    assert r.error is None
    assert r.tokens_in == 50
    assert r.tokens_out == 5
    assert r.watermark_updates["session_id"] == "sess001"
    assert r.watermark_updates["last_idx"] == 0


def test_cline_extract_delta_falls_back_to_session_model(tmp_path, monkeypatch):
    """Verify session-json model is used when assistant messages omit modelInfo."""
    fake_home = tmp_path / "cline"
    monkeypatch.setenv("CLINE_DATA_DIR", str(fake_home))
    repo = tmp_path / "repo"
    repo.mkdir()
    messages = [
        {"role": "assistant", "content": [{"type": "text", "text": "a1"}], "ts": 1,
         "metrics": {"inputTokens": 10, "cacheReadTokens": 0, "cacheWriteTokens": 0, "outputTokens": 5}},
    ]
    _make_cline_session(fake_home, "sess001", str(repo), messages, model="deepseek/fallback-model")

    r = ClineExtractor().extract_delta(str(repo), {})
    assert r.model == "deepseek/fallback-model"


def test_cline_extract_delta_error_paths(tmp_path, monkeypatch):
    """Verify schema-drift guards surface as error results, never exceptions."""
    fake_home = tmp_path / "cline"
    monkeypatch.setenv("CLINE_DATA_DIR", str(fake_home))
    repo = tmp_path / "repo"
    repo.mkdir()

    # No matching session for this repo.
    r = ClineExtractor().extract_delta(str(repo), {})
    assert r.error == "cline_session_not_found"

    # Session exists but messages file is missing.
    _make_cline_session(fake_home, "sess001", str(repo), [])
    sdir = fake_home / "sessions" / "sess001"
    (sdir / "sess001.messages.json").unlink()
    r = ClineExtractor().extract_delta(str(repo), {})
    assert r.error == "cline_messages_not_found"

    # Messages file exists but is not a parseable message list (schema drift).
    (sdir / "sess001.messages.json").write_text(json.dumps({"messages": {}}))
    r = ClineExtractor().extract_delta(str(repo), {})
    assert r.error == "cline_messages_schema_drift"


def test_cline_find_active_session_matches_repo_and_picks_newest(tmp_path, monkeypatch):
    """Verify sessions are associated to a repo via cwd and the newest wins."""
    fake_home = tmp_path / "cline"
    monkeypatch.setenv("CLINE_DATA_DIR", str(fake_home))
    repo = tmp_path / "repo"
    other = tmp_path / "other"
    repo.mkdir()
    other.mkdir()
    _make_cline_session(fake_home, "old-repo", str(repo), [])
    _make_cline_session(fake_home, "new-other", str(other), [])
    _make_cline_session(fake_home, "new-repo", str(repo), [])

    # Pin mtimes so ordering is deterministic: new-repo newest.
    base = fake_home / "sessions"
    os.utime(base / "old-repo" / "old-repo.json", (1_000_000, 1_000_000))
    os.utime(base / "new-other" / "new-other.json", (2_000_000, 2_000_000))
    os.utime(base / "new-repo" / "new-repo.json", (3_000_000, 3_000_000))

    ext = ClineExtractor()
    active = ext.find_active_session(str(repo))
    assert active is not None
    assert os.path.basename(active[0]) == "new-repo.json"
    # Session for a different repo is never returned.
    other_active = ext.find_active_session(str(other))
    assert os.path.basename(other_active[0]) == "new-other.json"


def test_cline_registry_and_selection(tmp_path, monkeypatch):
    """Verify the Cline extractor is registered and selectable by declared tool."""
    fake_home = tmp_path / "cline"
    monkeypatch.setenv("CLINE_DATA_DIR", str(fake_home))
    _make_cline_session(fake_home, "sess001", str(tmp_path), [])
    assert ClineExtractor.name == "cline"
    assert EXTRACTORS["cline"].name == "cline"
    sel = select_extractor("cline", str(tmp_path))
    assert isinstance(sel, ClineExtractor)


def test_short_model_strips_provider_prefix():
    """Verify short model ids drop any provider prefix for the Agent-Session trailer."""
    assert short_model("deepseek/deepseek-v4-flash-0731") == "deepseek-v4-flash-0731"
    assert short_model("claude") == "claude"
    assert short_model(None) is None


def test_update_commit_message_injects_tool_and_model(tmp_path):
    """Verify the hook rewrites tool=/model= on the Agent-Session line."""
    msg = tmp_path / "COMMIT_EDITMSG"
    msg.write_text(
        "feat(harness): test\n\n"
        "Agent-Session: tool=cursor model=sonnet agents=python-coder\n\n"
        "Co-Authored-By: Agent <a@b.c>\n"
    )
    assert update_commit_message(str(msg), "tokens=10.0K/1.0K", tool="cline", model="deepseek-v4-flash-0731")
    content = msg.read_text()
    assert "tool=cline" in content
    assert "model=deepseek-v4-flash-0731" in content
    assert "tokens=10.0K/1.0K" in content


def test_update_commit_message_removes_stale_tokens(tmp_path):
    """Verify tokens= is dropped when the runtime reports no new tokens."""
    msg = tmp_path / "COMMIT_EDITMSG"
    msg.write_text(
        "feat(harness): test\n\n"
        "Agent-Session: tool=cline model=deepseek-v4-flash-0731 agents=python-coder tokens=1.0K/2.0K\n\n"
        "Co-Authored-By: Agent <a@b.c>\n"
    )
    assert update_commit_message(str(msg), None, tool="cline", model="deepseek-v4-flash-0731")
    content = msg.read_text()
    assert "tokens=1.0K/2.0K" not in content
    assert "tool=cline" in content
    assert "model=deepseek-v4-flash-0731" in content


def test_live_cline_storage_sanity():
    """Verify local Cline storage structure if installed.

    Discriminates:
    - Skipped if the Cline sessions directory is not installed.
    - Skipped if installed but no session files exist.
    - Fails if session files exist but drift from the expected schema.
    """
    extractor = ClineExtractor()
    if not extractor.is_available():
        pytest.skip("Cline sessions directory not found on this machine.")

    session_dirs = []
    for s_dir in extractor.search_dirs:
        if s_dir and os.path.isdir(s_dir):
            session_dirs.extend(Path(s_dir).glob("*/"))
    session_dirs = [d for d in session_dirs if d.is_dir()]

    if not session_dirs:
        pytest.skip("Cline sessions directory exists, but no session files were found.")

    tested = 0
    for session_dir in session_dirs[:5]:
        sj = session_dir / f"{session_dir.name}.json"
        if not sj.exists():
            continue
        try:
            meta = json.loads(sj.read_text())
            sid = meta.get("session_id") or meta.get("sessionId")
            assert sid, "session json missing session_id/sessionId"
            mpath = session_dir / f"{sid}.messages.json"
            if mpath.exists():
                data = json.loads(mpath.read_text())
                msgs = data if isinstance(data, list) else data.get("messages")
                assert isinstance(msgs, list), "messages.json must contain a message list"
            tested += 1
        except Exception as e:
            pytest.fail(f"Cline session file {sj} failed schema sanity: {e}")

    assert tested > 0, "No valid Cline session files could be parsed."



