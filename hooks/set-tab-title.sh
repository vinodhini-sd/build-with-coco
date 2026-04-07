#!/bin/bash
# Cortex Code hook: Set terminal tab title from user's first prompt.
# Fires on UserPromptSubmit. Sets title once per session (first prompt only).

set -euo pipefail

INPUT=$(cat)
HOOK_DIR="$(cd "$(dirname "$0")" && pwd)"
STATE_DIR="/tmp/cortex-tab-titles"
mkdir -p "$STATE_DIR"

# Get session ID
SESSION_ID=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('session_id','unknown'))" 2>/dev/null || echo "unknown")
STATE_FILE="${STATE_DIR}/${SESSION_ID}"

# Only set title on first prompt of each session
if [[ -f "$STATE_FILE" ]]; then
  exit 0
fi

# Generate title using the Python helper (avoids all escaping issues)
TITLE=$(echo "$INPUT" | python3 "${HOOK_DIR}/tab-title-helper.py" 2>/dev/null || true)

if [[ -z "$TITLE" ]]; then
  exit 0
fi

# Set terminal tab title via OSC escape sequence
printf '\033]0;%s\007' "$TITLE" > /dev/tty 2>/dev/null || true

# Mark session as titled
echo "$TITLE" > "$STATE_FILE"

# Clean up state files older than 24h
find "$STATE_DIR" -type f -name '[0-9a-f]*' -mtime +1 -delete 2>/dev/null || true

exit 0
