# Data Engineer / Platform Engineer

> For: Pipeline builders, ingestion specialists, infra-as-code practitioners.
> `openflow` (392 accounts), `iceberg` + `snowpark-python` + `dynamic-tables` cluster.

---

## 1. Set up OpenFlow CDC from Postgres

```
I need real-time CDC replication from my Postgres database into Snowflake schema
{{database}}.{{schema}}. Configure the OpenFlow connector, enable CDC, and verify
the initial load.
```

## 2. Build an Iceberg table over my S3 data lake

```
I have Parquet files at {{s3://your-bucket/path/}} managed by a Glue catalog.
Create the external volume, catalog integration, and Iceberg tables in Snowflake.
Verify I can query the data and auto-refresh is working.
```

## 3. Migrate a Spark workload to Snowpark Connect

```
I have a PySpark job at {{/path/to/spark_job.py}}. Analyze it for Snowflake
compatibility, rewrite it as a Snowpark job, and help me validate the output
matches the original.
```

## 4. Create a Snowpark UDF/UDTF

```
I need a Python UDTF that parses JSON event payloads and returns flattened rows.
Build it with Snowpark, deploy it, and test it on a sample from
{{database}}.{{schema}}.{{table}}.
```

## 5. Build a streaming ingestion pipeline

```
Set up Snowpipe Streaming to ingest events from my Kafka topic into
{{database}}.{{schema}}.{{table}}. Show me the Kafka connector config, the pipe
definition, and how to monitor lag.
```

## 6. Optimize a slow pipeline stage

```
My nightly ETL on {{warehouse}} is taking too long. Pull the slowest queries from
QUERY_HISTORY for this warehouse, profile the top 3 bottlenecks, and give me
specific fixes — clustering keys, partition pruning improvements, query rewrites,
or spill reduction. Show before/after query profiles.
```

## 7. Build a multi-layer Dynamic Table pipeline over Iceberg

```
I have raw Iceberg tables in {{database}}.{{schema}} from S3. Build a two-layer
Dynamic Table pipeline on top: a staging layer that cleans and casts types, and a
mart layer that aggregates for reporting. Set appropriate target lags and verify
each layer reaches a HEALTHY state before building the next.
```

## 8. Debug a failing Snowflake Task

```
My task {{database}}.{{schema}}.{{task_name}} failed. Pull the task history, find
the error, diagnose the root cause, and fix it. Verify the next run succeeds.
```

## 9. Build a data quality gate in my pipeline

```
Before any table in {{database}} gets refreshed, check: row count > yesterday's
count, NULL rate on key columns < 1%, no duplicates on primary key. If checks
fail, abort the pipeline and alert me. Use DMFs.
```

## 10. Set up schema change monitoring

```
Alert me when any table in {{database}}.{{schema}} has a column added, removed,
or renamed. Use ACCOUNT_USAGE.COLUMNS compared to a snapshot from 24 hours ago.
```

## 11. Create a Snowpark stored procedure

```
I need a stored procedure that reads from {{database}}.{{schema}}.{{source_table}},
deduplicates, applies transformations, and merges into
{{database}}.{{schema}}.{{target_table}}. Build it in Python Snowpark with proper
error handling.
```

## 12. Load data with COPY INTO and inline transformations

```
I have files landing in a Snowflake stage at {{stage_path}}. Set up a COPY INTO
pipeline that reads the files, applies column transformations and type casting
inline, and lands data into {{database}}.{{schema}}.{{table}}. Include error
handling for malformed rows and a Snowflake Task to run it on a schedule.
```

## 13. Validate my migration from another data warehouse

```
I migrated tables to Snowflake. Compare row counts, column NULL rates, and a
sample of values between the source export files and the Snowflake landing tables.
Flag any discrepancies.
```

## 14. Set up a complete DCM project

```
I want to manage my Snowflake database schema as code. Create a DCM project
with proper three-tier role patterns, DEFINE TABLE/SCHEMA statements, and
a manifest.yml. Show me how to deploy and rollback changes.
```

## 15. Inspect and manage a complex Task DAG

```
Show me the full dependency graph for tasks in {{database}}.{{schema}}, including
which tasks are currently suspended, which are in a failed state, and the full
execution order. If any tasks are failing, diagnose the root cause and help me
resume them without re-running already-completed upstream tasks.
```
