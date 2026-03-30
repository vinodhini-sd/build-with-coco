# Validate, Test, and Deploy a dbt Project

> Run a full health check on a dbt project and deploy it to Snowflake.

## The Prompt

```
I have a dbt project at ~/my_dbt_project. Spin up a team to: (1) validate the project
compiles cleanly, (2) check test coverage across all models, (3) list any models that
reference sources with stale data, (4) deploy the project to Snowflake using snow dbt deploy.
Summarize findings before deploying.
```

## What This Triggers

- dbt project validation (compile check)
- Test coverage analysis across all models
- Source freshness inspection
- `snow dbt deploy` for Snowflake-native deployment
- Multi-agent team for parallel workstreams

## Before You Run

- A dbt project directory with `dbt_project.yml`
- Snowflake connection configured in dbt profiles
- `snow` CLI installed (for `snow dbt deploy`)
- Appropriate role with CREATE privileges on target schema

## Tips

- Replace `~/my_dbt_project` with your actual project path
- Remove the deploy step if you just want a health check: "Don't deploy yet, just report findings"
- Add "fix any compilation errors you find" for auto-remediation
