# Cortex Code Hooks

Session hooks that run automatically on startup and on each prompt. Drop them into `~/.snowflake/cortex/hooks/` and register them in `hooks.json`.

## What's Included

| File | Event | What it does |
|---|---|---|
| `session-start.sh` | `SessionStart` | Unified orchestrator: runs error alerts if configured, then What's New |
| `check-errors.py` | (called by session-start.sh) | Checks Snowflake tasks, alerts, dynamic tables, copy/pipe loads, GitHub CI, Airflow |
| `whats-new-helper.py` | (called by session-start.sh) | Diffs CoCo versions, surfaces new skills, gives tier-based tips |
| `set-tab-title.sh` | `UserPromptSubmit` | Sets terminal tab title from first prompt in session |
| `tab-title-helper.py` | (called by set-tab-title.sh) | Extracts and cleans the prompt into a short title |

## Installation

```bash
mkdir -p ~/.snowflake/cortex/hooks
cp hooks/*.sh hooks/*.py ~/.snowflake/cortex/hooks/
chmod +x ~/.snowflake/cortex/hooks/*.sh
```

Then register in `~/.snowflake/cortex/hooks.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/YOU/.snowflake/cortex/hooks/session-start.sh",
            "timeout": 40
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/YOU/.snowflake/cortex/hooks/set-tab-title.sh",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

Replace `/Users/YOU` with your actual home path.

## Configuration

### Tab title (no config needed)

`set-tab-title.sh` works out of the box. It reads the first prompt of each session, strips conversational filler, and sets the terminal tab title via OSC escape sequences.

### What's New (no config needed)

`whats-new-helper.py` automatically detects your installed CoCo version, diffs skills between versions, and classifies you as new/beginner/returning/power user based on local conversation history. No env vars required.

### Error alerts (optional, off by default)

`check-errors.py` polls Snowflake and GitHub for failures. It only runs when `COCO_ALERTS=1` is set. Configure by exporting these in your shell profile (`.zshrc` / `.bashrc`):

**Primary Snowflake account:**

```bash
export COCO_SF_ACCOUNT=your_account_identifier   # e.g. myorg-myaccount
export COCO_SF_USER=your_username
export COCO_SF_WAREHOUSE=COMPUTE_WH              # optional
```

Store your PAT via the Cortex secret store (never paste it in plain text):

```bash
cortex secret store COCO_SF_PAT --prompt
```

**Secondary Snowflake account (optional):**

```bash
export COCO_SF_ACCOUNT_2=your_second_account
export COCO_SF_USER_2=your_second_username
export COCO_SF_WAREHOUSE_2=COMPUTE_WH
```

```bash
cortex secret store COCO_SF_PAT_2 --prompt
```

**Airflow (optional, localhost only):**

```bash
export AIRFLOW_API_URL=http://localhost:8080
export AIRFLOW_USER=admin
export AIRFLOW_PASSWORD=your_password
```

The `"<KEY_NAME>"` syntax in `session-start.sh` is Cortex Code's secret injection — it substitutes stored secrets at runtime without ever writing them to a file.

To activate alerts for a session:

```bash
COCO_ALERTS=1 cortex
```

## What the alerts check

- Snowflake tasks failed in the last 24h (primary + secondary account)
- Snowflake alerts in FAILED / CONDITION_FAILED / ACTION_FAILED state
- Dynamic table refresh failures in the last 6h
- Copy/pipe load failures in the last 24h
- Open GitHub PRs with failing CI (across all your repos)
- Airflow DAG import errors (local instance)

All checks run in parallel. If nothing needs attention, What's New runs instead.
