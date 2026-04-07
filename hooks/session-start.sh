#!/bin/bash
# Cortex Code SessionStart hook — unified orchestrator.
# Priority: Alerts > What's New / Tip of the session.
# If any Snowflake or GitHub alerts are found, show them and stop.
# If all clear, fall through to the What's New helper.
#
# Only runs when COCO_ALERTS=1 is set:
#   COCO_ALERTS=1 cortex          (one-off)
#   alias cortex-check='COCO_ALERTS=1 cortex'   (add to ~/.zshrc)

set -euo pipefail

INPUT=$(cat)
HOOK_DIR="$(cd "$(dirname "$0")" && pwd)"

# Only run if COCO_ALERTS=1 is set — skip for normal sessions
if [[ -z "${COCO_ALERTS:-}" ]]; then
  exit 0
fi

# Only run on fresh session startup (not resume/clear/compact)
SOURCE=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('source',''))" 2>/dev/null || echo "")
if [[ "$SOURCE" != "startup" ]]; then
  exit 0
fi

# Inject PAT secrets for Snowflake auth (stored via: cortex secret store COCO_SF_PAT --prompt)
# COCO_SF_PAT_2 is optional — only needed if you configure a second Snowflake account
ALERTS=$(COCO_SF_PAT="<COCO_SF_PAT>" COCO_SF_PAT_2="<COCO_SF_PAT_2>" python3 "${HOOK_DIR}/check-errors.py" 2>/dev/null || true)

if [[ -n "$ALERTS" ]]; then
  # Something needs attention — show alerts only, skip What's New
  echo "$ALERTS"
else
  # All clear — show What's New / tip of the session
  python3 "${HOOK_DIR}/whats-new-helper.py" 2>/dev/null || true
fi

exit 0
