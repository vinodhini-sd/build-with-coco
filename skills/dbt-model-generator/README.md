# dbt Model Generator

Auto-generate dbt dimensional models from raw Snowflake tables. Profiles your data, recommends a modeling pattern (star schema, OBT, or wide denormalized), generates staging/dim/fact models with tests, and submits a PR for engineer review.

## What It Does

1. Discovers and profiles raw tables in a Snowflake schema (column types, cardinality, null rates, relationships)
2. Recommends a modeling pattern based on the data shape
3. Generates a complete dbt project: staging models, dimensions, facts, schema tests, and docs
4. Validates with `dbt parse` (optional `dbt run`)
5. Commits and opens a GitHub PR with a star schema diagram and profiling rationale

## Input

| Parameter | Required | Description |
|-----------|----------|-------------|
| `SOURCE_DATABASE` | Yes | Snowflake database containing raw tables |
| `SOURCE_SCHEMA` | Yes | Schema to scan (or `*` for all schemas) |
| `SOURCE_TABLE` | No | Specific table (default: all tables in schema) |
| `GITHUB_REPO` | No | GitHub repo for the PR (`owner/repo`) |
| `PROJECT_NAME` | No | dbt project name (default: derived from database name) |
| `WAREHOUSE` | No | Snowflake warehouse (default: active connection's warehouse) |
| `ROLE` | No | Snowflake role (default: active connection's role) |

## Output

- **dbt project** — Full scaffold with `dbt_project.yml`, staging models, dimension/fact models, and `schema.yml` tests
- **GitHub PR** — Includes star schema diagram, profiling stats, and column classification rationale
- **Validation report** — `dbt parse` results (and optional `dbt run` output)

## Trigger Phrases

```
$dbt-model-generator
```

Also activates on: "generate dbt models", "shift left", "dimensional model", "star schema from raw", "auto model", "dbt from raw", "one big table", "OBT", "wide table"

## Requirements

- **Snowflake**: Active Cortex Code connection
- **dbt**: `dbt-core>=1.7,<2.0` with `dbt-snowflake>=1.7,<2.0`
- **Python**: 3.9+
- **Runtime**: `uv` (preferred), `pipx`, or `pip`
- **Git**: `git` CLI + `gh` CLI for PR creation

## Installation

**Global (all projects):**

```bash
cp -r skills/dbt-model-generator ~/.snowflake/cortex/skills/dbt-model-generator
```

**Per-project:**

```bash
mkdir -p .cortex/skills
cp -r skills/dbt-model-generator .cortex/skills/dbt-model-generator
```
