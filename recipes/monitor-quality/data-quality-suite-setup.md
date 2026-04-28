# Set Up a Multi-Framework Data Quality Suite

> Configure quality checks, monitoring, and pipeline gates across your entire data stack — Snowflake, dbt, Spark, and Snowpark — in one session.

## The Prompt

```
Set up a multi-framework data quality suite for {{database}}.{{schema}}.
Ask me which frameworks we're using (Snowflake DMFs, dbt, Great Expectations,
Soda Core, Snowpark inline gates, PySpark inline gates), which pipeline layers
to cover (bronze/silver/gold/feature), and whether I want continuous monitoring,
pipeline gates, or both. Then generate the right checks and config files for each.
```

## What This Triggers

- `data-quality-suite` skill invocation
- Customer config check (`customer-config.md`)
- Framework routing based on answers
- Check generation for each framework:
  - DMFs: DDL for NULL_COUNT, DUPLICATE_COUNT, FRESHNESS, ROW_COUNT + custom DMFs
  - dbt: `schema.yml` with `not_null`, `unique`, `accepted_values`, `relationships` tests
  - GX: `expectations_{{table}}.py` with expectation suite + checkpoint
  - Soda: `soda_checks_{{table}}.yml` with all check types
  - Snowpark: `quality_gate.py` inserted before each `save_as_table()` call
  - PySpark: `spark_quality_gate.py` inserted before each `.write.` call

## Before You Run

- For DMFs: requires `CREATE DATA METRIC FUNCTION` privilege or ACCOUNTADMIN
- For dbt: `dbt-core >= 1.5` installed and `profiles.yml` configured
- For GX: `pip install great-expectations` (>= 0.18)
- For Soda: `pip install soda-core-{{connector}}`
- For Snowpark/Spark gates: provide the pipeline file path

## Tips

- Replace `{{database}}.{{schema}}` with your target. Add `{{table}}` for a single table.
- Say "only Snowflake" to skip non-Snowflake frameworks
- Say "feature layer only" to apply ML-specific checks (distribution bounds, freshness SLA)
- After setup, say "add a circuit breaker to halt my pipeline on DMF violation" for automated pipeline suspension

---

## Bonus Prompt: Add Gates to an Existing Pipeline

```
Add quality gates to my existing {{framework}} pipeline at {{file_path}}.
Check for nulls on {{column_list}}, row count > 0, and status in {{value_list}}.
Insert the gate before each table write and raise an error on failure.
```

Swap `{{framework}}` for `Snowpark` or `PySpark`.
