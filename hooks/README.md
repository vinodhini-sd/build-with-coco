# SessionStart Hooks

Two hooks that run at Cortex Code session start to surface errors and tips.

Disabled by default — only runs when `COCO_ALERTS=1 cortex` is used, so normal `cortex` sessions start instantly.

## What It Does

**`check-errors.py`** — parallel error checker. Fires all checks concurrently:
- Snowflake task failures (last 24h)
- Snowflake alert failures (last 24h)
- Dynamic table refresh failures (last 6h)
- Copy/pipe load failures (last 24h)
- GitHub PRs with failing CI (parallel per-PR fetches)
- Airflow DAG import errors

**`whats-new-helper.py`** — personalized tips. Reads your local conversation history to detect your user tier and gaps, then shows a relevant nudge, new skill, or version diff.

`session-start.sh` orchestrates both: if errors are found, show those. If all clear, show the tip.

## Setup

### 1. Install the hook files

```bash
mkdir -p ~/.snowflake/cortex/hooks
cp hooks/session-start.sh ~/.snowflake/cortex/hooks/
cp hooks/check-errors.py ~/.snowflake/cortex/hooks/
cp hooks/whats-new-helper.py ~/.snowflake/cortex/hooks/
chmod +x ~/.snowflake/cortex/hooks/session-start.sh
```

### 2. Register the hook in `~/.snowflake/cortex/hooks.json`

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/Users/YOUR_USERNAME/.snowflake/cortex/hooks/session-start.sh",
            "timeout": 40
          }
        ]
      }
    ]
  }
}
```

### 3. Store your Snowflake PAT(s)

```bash
cortex secret store COCO_SF_PAT --prompt
# optional second account:
cortex secret store COCO_SF_PAT_2 --prompt
```

### 4. Set your account config

Add to `~/.zshrc` (or `~/.bashrc`):

```bash
export COCO_SF_ACCOUNT="your-account-identifier"   # e.g. myorg-myaccount
export COCO_SF_USER="YOUR_USERNAME"
export COCO_SF_WAREHOUSE="YOUR_WAREHOUSE"

# Optional second account
export COCO_SF_ACCOUNT_2="your-second-account"
export COCO_SF_USER_2="YOUR_USERNAME_2"
export COCO_SF_WAREHOUSE_2="YOUR_WAREHOUSE_2"
```

### 5. Add the alias

```bash
echo "alias cortex-check='COCO_ALERTS=1 cortex'" >> ~/.zshrc
source ~/.zshrc
```

## Usage

```bash
cortex              # instant startup, no hook
cortex-check        # startup with parallel error checks + tips
```

## Optional: Airflow

Set these env vars if you run Airflow locally (defaults to `localhost:8080`):

```bash
export AIRFLOW_API_URL="http://localhost:8080"
export AIRFLOW_USER="admin"
export AIRFLOW_PASSWORD="admin"
```

## Dependencies

```bash
pip install snowflake-connector-python
```

`gh` CLI must be installed and authenticated for GitHub PR checks.
