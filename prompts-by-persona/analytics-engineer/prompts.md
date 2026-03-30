# Analytics Engineer

> For: dbt practitioners, data modelers, semantic layer builders.
> `dbt-projects-on-snowflake` spans 543 accounts with avg 40 prompts in deep sessions.

---

## 1. Deploy my dbt project to Snowflake

```
I have a dbt project at {{/path/to/dbt_project}}. Validate it compiles, check test
coverage across all models, then deploy it to Snowflake using snow dbt deploy.
Show me the deployment status.
```

## 2. Build a semantic view from my star schema

```
I have fact and dimension tables in {{database}}.{{schema}}. Create a semantic view
that defines dimensions and metrics (revenue, order count, avg order value).
Include verified queries.
```

## 3. Trace what breaks if I rename a column

```
I need to rename {{table}}.{{column}} to a new name. Trace all downstream dbt
models, views, and apps that reference this column. Give me a migration checklist.
```

## 4. Generate dbt models from raw tables

```
Explore my {{raw_schema}} schema and generate dbt staging, intermediate, and mart
models following best practices. Create sources.yml, schema.yml with tests, and
a README explaining the data flow.
```

## 5. Debug a failing dbt model

```
My model {{database}}.{{schema}}.{{table}} is failing with a duplicate key error.
Analyze the model SQL, find the root cause, and suggest a fix. Run the fixed
version to verify.
```

## 6. Build a Dynamic Table pipeline

```
Replace my scheduled task that refreshes {{database}}.{{schema}}.{{table}} with
a Dynamic Table. Set target lag to 5 minutes. Make sure the DAG is correct
and the DT is in a healthy state.
```

## 7. Add data quality tests to all my models

```
Scan my dbt project and add generic tests (not_null, unique, accepted_values,
relationships) to every model that's missing them. Generate the YAML updates.
```

## 8. Create a lineage doc for my pipeline

```
Starting from my raw source table, trace the full lineage to my reporting mart.
Show me the dependency graph, identify any bottlenecks, and flag stale nodes.
```

## 9. Migrate my dbt Core project to Snowflake-native

```
I use dbt Core with CLI. Help me understand the trade-offs of switching to
snow dbt deploy (Snowflake-native execution). What would I gain/lose? Walk me
through the migration steps.
```

## 10. Set up incremental models correctly

```
My incremental model is doing full refreshes every run. Diagnose why, fix the
incremental logic, and add a unique_key to prevent duplicates.
```

## 11. Validate my semantic layer with sample questions

```
I have a semantic view at {{database}}.{{schema}}.{{semantic_view}}. Generate 10
test questions a business user would ask, run them through Cortex Analyst, and
flag any that return wrong or inconsistent results.
```

## 12. Auto-document my dbt project

```
Generate documentation for all undocumented models and columns in my dbt project.
Use the table/column names and existing tests as context. Write in plain English,
not technical jargon.
```

## 13. Build a slowly changing dimension

```
I need a Type 2 SCD for a customer dimension that tracks when segments change.
Create the Dynamic Table or merge procedure that handles inserts, updates, and
preserves history with VALID_FROM / VALID_TO columns.
```

## 14. Check for data drift between environments

```
Compare row counts and NULL rates for all tables in {{prod_database}}.{{schema}}
vs {{staging_database}}.{{schema}}. Flag any that differ by more than 5%.
This is my pre-deploy checklist.
```

## 15. Audit my incremental models for correctness

```
Run dbt ls --select config.materialized:incremental and for each model: check
that the incremental_strategy matches its source update pattern, flag any that
are missing a unique_key, and list any that haven't had a full-refresh in over
30 days based on run_results.json history.
```
