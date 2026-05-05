# Data Quality Suite — Compass

## Quick Commands
- Invoke: `$data-quality-suite` or describe the task in plain language
- Trigger phrases: "data quality", "quality checks", "quality gates", "dq suite", "dbt tests", "great expectations", "soda checks", "snowpark gate", "spark gate", "quality framework", "add quality monitoring"
- Required inputs: data location (`{{database}}.{{schema}}` or file path), pipeline layer, monitoring style (continuous / gate / both)

## Key Files
- `SKILL.md` — routing logic, layer standards, stopping points
- `customer-config.md` — **fork this file to customize** enabled frameworks, layer standards, thresholds
- `workflows/dmf-monitors.md` — Snowflake DMF: profile → recommend → attach → schedule
- `workflows/dbt-tests.md` — dbt: classify columns → generate schema.yml → validate
- `workflows/gx-suite.md` — Great Expectations: datasource → suite → checkpoint → CI
- `workflows/soda-checks.md` — Soda Core: config → checks.yml → scan
- `workflows/snowpark-gates.md` — Snowpark: insert quality_gate() before each write
- `workflows/spark-gates.md` — PySpark: insert assert_quality() at DataFrame write points
- `templates/` — runnable code/SQL for each framework (use `{{placeholder}}` vars)

## Non-Obvious Patterns
- Always read `customer-config.md` FIRST — it controls which frameworks are enabled and layer standards
- DMFs require ACCOUNTADMIN or CREATE DATA METRIC FUNCTION privilege — check before generating DDL
- dbt tests workflow works against ANY dbt adapter, not just Snowflake
- GX workflow is the only one that works standalone for non-Snowflake, non-Spark sources (Pandas, S3, etc.)
- Feature layer requires distribution bounds checks (mean ± 3σ) — not in bronze/silver standards
- Templates use `{{double-braces-kebab-case}}` — never angle brackets

## See Also
- `lineage` bundled skill — trace upstream root cause after a quality check fails
- `data-governance` bundled skill — investigate failed task/query history
- `data-quality` bundled skill — Snowflake-native DMF workflows (more detail than dmf-monitors.md)
- `dbt-model-generator` skill — generate dbt models with schema tests auto-attached
