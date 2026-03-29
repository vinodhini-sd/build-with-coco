# Know Your Data

Discover data you already have access to in a Snowflake account, understand what it contains, and map it to your roles. Tells you what you can query, what you can't, and who to contact for access.

## What It Does

1. Asks what data and analysis you need, extracts search keywords
2. Searches Snowflake for matching tables and views (semantic search + SHOW/LIKE)
3. Gets your identity, roles, and available warehouses
4. Tests access to each candidate table with each of your roles
5. For blocked tables, finds the owning role and who can grant access
6. Presents a structured access report with quick-start SQL and contact list

## Input

| Parameter | Required | Description |
|-----------|----------|-------------|
| Data description | Yes | What data you're looking for (e.g., "customer feedback", "sales pipeline") |
| Analysis goal | No | What you want to do with the data (e.g., "sentiment analysis", "quarterly trends") |

The skill extracts 3-5 search keywords from your description and runs discovery automatically.

## Output

- **Access report** with 5 sections:
  1. **Your Identity** — User, account, connection
  2. **Your Roles** — All granted roles and who granted them
  3. **Data You CAN Access** — Tables, which role to use, row counts, column summaries, quick-start SQL
  4. **Data You NEED Access To** — Blocked tables, owning roles, who to contact
  5. **Recommended Next Steps** — Which admin to contact first, message template

## Trigger Phrases

```
$know-your-data
```

Also activates on: "know your data", "know my data", "find data", "data discovery", "explore account", "what data", "what tables", "what can I access", "discover data", "search tables"

## Requirements

- **Snowflake**: Active Cortex Code connection

## Installation

**Global (all projects):**

```bash
cp -r skills/know-your-data ~/.snowflake/cortex/skills/know-your-data
```

**Per-project:**

```bash
mkdir -p .cortex/skills
cp -r skills/know-your-data .cortex/skills/know-your-data
```
