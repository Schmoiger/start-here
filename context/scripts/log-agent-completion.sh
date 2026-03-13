#!/bin/bash
# Logs agent lifecycle events to artefacts/build/agent-metrics.log
# Called by Claude Code SubagentStart and SubagentStop hooks — receives JSON on stdin
#
# Log columns: timestamp | event | agent_id | task | commit | tokens | files

INPUT=$(cat)
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

EVENT=$(echo "$INPUT" | jq -r '.hook_event_name // "unknown"' 2>/dev/null)
AGENT_ID=$(echo "$INPUT" | jq -r '.agent_id // "unknown"' 2>/dev/null)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG_FILE="$REPO_ROOT/artefacts/build/agent-metrics.log"

if [ ! -f "$LOG_FILE" ]; then
  echo "timestamp | event | agent_id | task | commit | tokens | files" > "$LOG_FILE"
fi

if [ "$EVENT" = "SubagentStart" ]; then
  GIT_HEAD=$(git -C "$REPO_ROOT" rev-parse --short HEAD 2>/dev/null || echo "-")
  echo "$TIMESTAMP | start | $AGENT_ID | - | $GIT_HEAD | - | -" >> "$LOG_FILE"

elif [ "$EVENT" = "SubagentStop" ]; then
  LAST_MSG=$(echo "$INPUT" | jq -r '.last_assistant_message // ""' 2>/dev/null)
  TRANSCRIPT=$(echo "$INPUT" | jq -r '.agent_transcript_path // ""' 2>/dev/null)

  # Approximate token count from self-reported usage in final message
  TOKENS=$(echo "$LAST_MSG" | grep -oE 'total_tokens: [0-9]+' | grep -oE '[0-9]+' | tail -1)
  TOKENS="${TOKENS:--}"

  # Task name: extract from first prompt line in transcript (e.g. "Task T1f" or "Spec review T3")
  TASK="-"
  if [ -n "$TRANSCRIPT" ] && [ -f "$TRANSCRIPT" ]; then
    TASK=$(grep -o '"You are implementing Task [^\\]*\|"Spec \(compliance \)\?review [^\\]*\|"Quick spec [^\\]*\|"T[0-9][^\\]*' "$TRANSCRIPT" 2>/dev/null \
      | head -1 \
      | sed 's/^"//; s/[.\\].*//' \
      | cut -c1-40)
    TASK="${TASK:--}"
  fi

  # Commit SHA: from agent's self-reported output or current HEAD
  COMMIT=$(echo "$LAST_MSG" | grep -oE '`[a-f0-9]{7,10}`' | tr -d '`' | head -1)
  if [ -z "$COMMIT" ]; then
    COMMIT=$(git -C "$REPO_ROOT" rev-parse --short HEAD 2>/dev/null || echo "-")
  fi

  # Files touched: Write and Edit tool calls in transcript
  FILES="-"
  if [ -n "$TRANSCRIPT" ] && [ -f "$TRANSCRIPT" ]; then
    FILES=$(grep -oE '"(Write|Edit)"[^}]*"file_path":"[^"]*"' "$TRANSCRIPT" 2>/dev/null \
      | grep -oE '"file_path":"[^"]*"' \
      | grep -oE '"[^"]*"$' \
      | tr -d '"' \
      | sed "s|$REPO_ROOT/||" \
      | sort -u \
      | tr '\n' ',' \
      | sed 's/,$//')
    FILES="${FILES:--}"
  fi

  echo "$TIMESTAMP | stop  | $AGENT_ID | $TASK | $COMMIT | $TOKENS | $FILES" >> "$LOG_FILE"
fi
