#!/bin/bash
# prepare-commit-msg hook — appends Agent-Session footer from agent-metrics.log
#
# Install (once per clone):
#   ln -sf ../../context/scripts/prepare-commit-msg.sh .git/hooks/prepare-commit-msg
#
# Reads stop entries written to artefacts/build/agent-metrics.log since the last
# commit, calculates aggregate metrics, and appends an Agent-Session trailer so
# commit messages record which agent work landed in the commit.
#
# No circular dependency: log entries are written at SubagentStop (before the
# commit runs). The hook reads those entries; the new commit SHA is not in the
# log until the next SubagentStop writes it.

COMMIT_MSG_FILE="$1"
COMMIT_SOURCE="$2"   # message | template | merge | squash | commit | ""

# Don't modify merge or squash commits — they're structural, not agent work
[[ "$COMMIT_SOURCE" == "merge" || "$COMMIT_SOURCE" == "squash" ]] && exit 0

# Don't modify if Agent-Session already present (e.g. manual or amended commit)
grep -q "^Agent-Session:" "$COMMIT_MSG_FILE" 2>/dev/null && exit 0

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG_FILE="$REPO_ROOT/artefacts/build/agent-metrics.log"

[ ! -f "$LOG_FILE" ] && exit 0

# Timestamp of the most recent commit (ISO 8601). If no commits yet, use epoch.
LAST_COMMIT_TS=$(git -C "$REPO_ROOT" log -1 --format="%cI" 2>/dev/null || echo "1970-01-01T00:00:00+00:00")

# Collect stop entries written after the last commit.
# Log line format: timestamp | stop  | agent_id | task | commit | tokens | files
# (awk string comparison on ISO 8601 timestamps works correctly lexicographically)
STOP_ENTRIES=$(awk -F' \| ' -v since="$LAST_COMMIT_TS" '
  NR > 1 && $2 ~ /stop/ && $1 > since { print $0 }
' "$LOG_FILE" 2>/dev/null)

[ -z "$STOP_ENTRIES" ] && exit 0

# Sum approximate token counts (field 6); skip "-" placeholders
TOTAL_TOKENS=$(echo "$STOP_ENTRIES" | awk -F' \| ' '
  $6+0 > 0 { sum += $6+0 }
  END { printf "%.0f", sum+0 }
')

# Format tokens as ~NNK; omit if zero
TOKENS_FMT="-"
if [ "${TOTAL_TOKENS:-0}" -gt 0 ] 2>/dev/null; then
  # bc for decimal; fallback to integer division
  TOKENS_K=$(echo "scale=1; $TOTAL_TOKENS / 1000" | bc 2>/dev/null) \
    || TOKENS_K=$(( TOTAL_TOKENS / 1000 ))
  TOKENS_FMT="~${TOKENS_K}K"
fi

# If no meaningful data, skip (e.g. log entries from empty/aborted agent runs)
HAS_TASK=$(echo "$STOP_ENTRIES" | awk -F' \| ' '$4 != "-" && $4 != "" { found=1 } END { print found+0 }')
if [ "$TOKENS_FMT" = "-" ] && [ "${HAS_TASK:-0}" = "0" ]; then
  exit 0
fi

# Duration: span from earliest start entry to latest stop entry in this window
EARLIEST_START=$(awk -F' \| ' -v since="$LAST_COMMIT_TS" '
  NR > 1 && $2 ~ /start/ && $1 > since { print $1 }
' "$LOG_FILE" 2>/dev/null | sort | head -1)

LATEST_STOP=$(echo "$STOP_ENTRIES" | awk -F' \| ' '{ print $1 }' | sort | tail -1)

DURATION="-"
if [ -n "$EARLIEST_START" ] && [ -n "$LATEST_STOP" ]; then
  # macOS: date -j -f; Linux: date -d
  to_epoch() {
    date -j -f "%Y-%m-%dT%H:%M:%SZ" "$1" +%s 2>/dev/null \
      || date -d "$1" +%s 2>/dev/null \
      || echo ""
  }
  START_SEC=$(to_epoch "$EARLIEST_START")
  STOP_SEC=$(to_epoch "$LATEST_STOP")
  if [ -n "$START_SEC" ] && [ -n "$STOP_SEC" ] && [ "$STOP_SEC" -gt "$START_SEC" ] 2>/dev/null; then
    DIFF=$(( STOP_SEC - START_SEC ))
    if [ "$DIFF" -ge 3600 ]; then
      DURATION="$(( DIFF / 3600 ))h$(( (DIFF % 3600) / 60 ))m"
    else
      DURATION="$(( DIFF / 60 ))m"
    fi
  fi
fi

# agents= value: map known prompt patterns to role names; fall back to claude-code
AGENTS=$(echo "$STOP_ENTRIES" | awk -F' \| ' '
  $4 != "-" && $4 != "" {
    t = $4
    if (t ~ /python.coder/)      { print "python-coder";      next }
    if (t ~ /typescript.coder/)  { print "typescript-coder";  next }
    if (t ~ /functional.tester/) { print "functional-tester"; next }
    if (t ~ /code.reviewer/)     { print "code-reviewer";     next }
    if (t ~ /spec.*compliance/)  { print "spec-reviewer";     next }
    if (t ~ /code.*quality/)     { print "code-quality-reviewer"; next }
    if (t ~ /tech.lead/)         { print "tech-lead";         next }
    if (t ~ /ui.designer/)       { print "ui-designer";       next }
    if (t ~ /visual.designer/)   { print "visual-designer";   next }
    if (t ~ /documentation/)     { print "documentation";     next }
  }
' | sort -u | paste -sd ',' -)
AGENTS="${AGENTS:-claude-code}"

# Append Agent-Session trailer (and Co-Authored-By if not already present)
printf "\nAgent-Session: tool=claude-code model=sonnet agents=%s tokens=%s duration=%s\n" \
  "$AGENTS" "$TOKENS_FMT" "$DURATION" >> "$COMMIT_MSG_FILE"

grep -q "^Co-Authored-By:" "$COMMIT_MSG_FILE" 2>/dev/null || \
  printf "Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>\n" >> "$COMMIT_MSG_FILE"
