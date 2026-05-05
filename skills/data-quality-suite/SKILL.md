---
name: data-quality-suite
description: "Multi-framework data quality suite. Sets up quality checks, gates, and monitoring across Snowflake DMFs, dbt tests, Great Expectations, Soda Core, Snowpark pipelines, and PySpark pipelines. Use when: data quality, quality checks, quality gates, dq suite, test suite, gx, great expectations, soda core, soda checks, dbt tests, dbt schema tests, quality framework, monitor my data, check my data, add quality checks, quality gate pipeline, null checks, freshness checks, row count checks, feature quality, pipeline quality, quality suite."
---

# Data Quality Suite

Multi-framework DQ suite. Covers Snowflake DMFs, dbt, Great Expectations, Soda Core, Snowpark, and Spark — in one skill, with a single config file teams can fork and customize.

---

## Step 0: Load Customer Config

**Before asking anything**, read `customer-config.md` in this skill directory.

It controls:
- Which frameworks are enabled (`ENABLED_FRAMEWORKS`)
- What each pipeline layer must pass (`LAYER_STANDARDS`)
- How thresholds are set (`THRESHOLD_DEFAULTS`)
- Org-specific standards (`ORG_STANDARDS`)

If `customer-config.md` is unmodified (default values), note that to the user and proceed with all frameworks available.

---

## Step 1: Routing Questions

Ask these three questions before routing. All three answers are needed.

**Q1 — Where does the data live?**
- `snowflake` — data is in Snowflake tables/views
- `dbt` — this is a dbt project (any adapter)
- `spark` — PySpark pipeline, data in S3/HDFS/Delta
- `snowpark` — Snowpark Python pipeline writing to Snowflake
- `mixed` — combination (ask which components)

**Q2 — Which pipeline layer?**
- `bronze` / `raw` — raw ingest, source data
- `silver` / `staging` — cleaned, conformed
- `gold` / `serving` — business-ready, downstream consumers
- `feature` — ML feature tables
- `all` — apply standards to all layers

**Q3 — Monitoring style?**
- `continuous` — scheduled checks that run independently of pipeline (DMFs, Soda scheduled scans)
- `gate` — blocking checks embedded in the pipeline (fail the job on violation)
- `both` — continuous background monitoring + pipeline gates

---

## Step 2: Framework Routing

Use the table below to determine which workflow(s) to load. Load the workflow file and follow it.

| Data location | Monitoring style | Framework | Load workflow |
|---|---|---|---|
| `snowflake` | `continuous` | Snowflake DMFs | `workflows/dmf-monitors.md` |
| `snowflake` | `gate` | Snowpark inline | `workflows/snowpark-gates.md` |
| `snowflake` | `both` | DMFs + Snowpark | Both |
| `dbt` | any | dbt schema tests | `workflows/dbt-tests.md` |
| `spark` | `continuous` | Soda Core | `workflows/soda-checks.md` |
| `spark` | `gate` | PySpark inline | `workflows/spark-gates.md` |
| `spark` | `both` | Soda + PySpark | Both |
| `snowpark` | `continuous` | DMFs on output tables | `workflows/dmf-monitors.md` |
| `snowpark` | `gate` | Snowpark inline | `workflows/snowpark-gates.md` |
| `mixed` | any | Ask which components, load multiple | Multiple |

**Framework overrides from customer-config.md:** If a framework is disabled in `ENABLED_FRAMEWORKS`, skip it and route to the next enabled option.

**GX path:** If the user specifically requests Great Expectations (regardless of data location), load `workflows/gx-suite.md`. GX is framework-agnostic and works with Snowflake, Spark, and Pandas sources.

---

## Step 3: Layer Standards

Before generating any checks, confirm which layer standards apply. Reference `customer-config.md → LAYER_STANDARDS`.

Default standards if not customized:

| Layer | Minimum checks required |
|---|---|
| Bronze/raw | Schema validation, row count > 0, freshness |
| Silver/staging | + null checks on key columns, uniqueness on PKs, FK integrity |
| Gold/serving | + business rule checks, cross-table row count consistency |
| Feature | + distribution bounds (mean ± 3σ), null guards on all features, freshness SLA |

---

## Step 4: Present Plan Before Writing

**Always present a summary before generating any files or DDL:**

```
Here's what I'll generate:
- Framework: [framework name]
- Layer: [layer]
- Checks: [list of checks]
- Output: [file(s) that will be created/modified]

Proceed? (yes / adjust checks / change framework)
```

Do not write files or execute DDL until the user confirms.

---

## Stopping Points

| Point | Gate |
|---|---|
| Before generating DDL / SQL | Show check plan, await approval |
| Before writing to an existing file | Show diff, await approval |
| Before attaching DMFs | Show full DDL list, await approval |
| Before creating GX checkpoint | Show expectation suite, await approval |
| Before modifying a Snowpark/Spark file | Show exactly what lines will change, await approval |

---

## Workflow Files

Each framework has a dedicated workflow file with full step-by-step detail:

- `workflows/dmf-monitors.md` — Snowflake Data Metric Functions: profile → recommend → attach → schedule
- `workflows/dbt-tests.md` — dbt schema tests: classify columns → generate schema.yml → validate
- `workflows/gx-suite.md` — Great Expectations: datasource → expectations → checkpoint → CI
- `workflows/soda-checks.md` — Soda Core: config → checks.yml → scan → integrate
- `workflows/snowpark-gates.md` — Snowpark inline gates: read file → insert quality_gate() → pre/post write
- `workflows/spark-gates.md` — PySpark inline gates: read file → insert assert_quality() → fail-fast

## Templates

Ready-to-use code and SQL templates (with `{{placeholder}}` variables):

- `templates/dmf_setup.sql` — DMF creation + table attachment DDL
- `templates/dbt_schema_tests.yml` — dbt schema.yml with full test coverage
- `templates/gx_expectations.py` — GX expectation suite for any datasource
- `templates/soda_checks.yml` — Soda checks.yml covering all check types
- `templates/snowpark_gate.py` — `quality_gate()` function for Snowpark pipelines
- `templates/spark_gate.py` — `assert_quality()` function for PySpark pipelines

---

## Cross-Skill Integration

After identifying quality failures, proactively:
- **Trace root cause upstream**: load the `lineage` bundled skill
- **Investigate failed queries or tasks**: load the `data-governance` bundled skill
- **For ML feature quality drift**: suggest Evidently AI or custom DMFs with distribution bounds
