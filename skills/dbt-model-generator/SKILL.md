---
name: dbt-model-generator
description: "Automatically generate dbt dimensional models from raw Snowflake tables. Use when: user wants to generate dbt models, shift left data modeling, automate dimensional modeling, create facts and dimensions from raw data, build a star schema from raw tables, or auto-generate dbt code. Triggers: generate dbt models, shift left, dimensional model, auto model, star schema from raw, dbt from iceberg, dbt from raw, one big table, OBT, wide table."
---

# dbt Model Generator

Automates the creation of dbt models from raw Snowflake tables. Profiles the data, recommends a modeling pattern (star schema, OBT, or wide denormalized), generates staging/dim/fact models with tests, and submits a PR for engineer review.

## Requirements

- **dbt**: `dbt-core>=1.7,<2.0` with `dbt-snowflake>=1.7,<2.0`
- **Python**: 3.9+
- **Runtime**: `uv` (preferred), `pipx`, or `pip` — skill auto-detects what's available
- **Git**: `git` CLI + `gh` CLI for PR creation
- **Snowflake**: Active CoCo connection or environment-variable-based auth

## Workflow

```
Start
  ↓
Step 1: Collect Parameters
  ↓
Step 2: Discover & Profile Raw Tables
  ↓
Step 3: Recommend Modeling Pattern
  ↓  ⚠️ STOP — User approves pattern + classification
Step 4: Generate dbt Project Scaffold
  ↓
Step 5: Generate Models (staging → dims → facts / OBT)
  ↓
Step 6: Generate Schema Tests & Docs
  ↓
Step 7: Validate (dbt parse + optional dbt run)
  ↓  ⚠️ STOP — User reviews generated models
Step 8: Git Commit & PR
  ↓
Done
```

## Parameters

**Required:**
- `<SOURCE_DATABASE>`: Snowflake database containing raw tables
- `<SOURCE_SCHEMA>`: Schema within the database (or `*` for all schemas)

**Optional:**
- `<SOURCE_TABLE>`: Specific table to model (default: discover all tables in schema)
- `<PROJECT_NAME>`: dbt project name (default: derived from database name)
- `<PROJECT_PATH>`: Where to create the project on disk (default: `~/Documents/coco-dev/<PROJECT_NAME>`)
- `<GITHUB_REPO>`: GitHub repo for PR (format: `owner/repo-name`)
- `<WAREHOUSE>`: Snowflake warehouse (default: use active CoCo connection's warehouse)
- `<ROLE>`: Snowflake role (default: use active CoCo connection's role)

Full step-by-step detail, SQL queries, dbt templates, column classification rules, and troubleshooting in [references/workflow.md](references/workflow.md).
