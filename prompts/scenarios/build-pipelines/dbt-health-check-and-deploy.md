# Validate, Test, and Deploy a dbt Project

> Run a full health check on a dbt project and deploy it to Snowflake.

## The Prompt

```
Run a full health check on my dbt project at {{project-path}}: check it compiles cleanly,
review test coverage across all models, and flag any models with stale sources. Summarize
findings, then ask me whether to deploy. If deploying, use snow dbt deploy for Snowflake-native
execution — or dbt build if I'm on standard dbt Core without snow dbt configured.
```

## What This Triggers

- dbt project validation (compile check)
- Test coverage analysis across all models
- Source freshness inspection
- `snow dbt deploy` for Snowflake-native deployment (or `dbt build` for standard dbt Core)

## Before You Run

- A dbt project directory with `dbt_project.yml`
- Snowflake connection configured in dbt profiles
- `snow` CLI installed (for `snow dbt deploy`)
- Appropriate role with CREATE privileges on target schema

## Tips

- Replace `~/my_dbt_project` with your actual project path
- Remove the deploy step if you just want a health check: "Don't deploy yet, just report findings"
- Add "fix any compilation errors you find" for auto-remediation
