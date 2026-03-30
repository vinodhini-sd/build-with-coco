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

## 6. Optimize my most expensive pipeline

```
My nightly ETL pipeline on {{warehouse}} takes too long. Profile the queries,
identify the bottlenecks, and suggest optimizations — clustering, partitioning,
query rewrite, or parallelization.
```

## 7. Set up a complete Iceberg lakehouse

```
Design and build a lakehouse architecture: raw Iceberg tables from S3, staging
Dynamic Tables for cleansing, and mart-layer Dynamic Tables for reporting.
Include governance (masking, row access) from the start.
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

## 12. Configure external tables on S3

```
I have CSV files landing in {{s3://your-bucket/path/}} partitioned by date. Set
up an external table with auto-refresh, the correct file format, and a view that
makes it queryable like a regular Snowflake table.
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

## 15. Monitor pipeline health across my account

```
Build a Streamlit app that shows: task run history, failed/succeeded status,
pipeline lag, and row delta per table. Connect to ACCOUNT_USAGE.TASK_HISTORY
and my pipeline metadata tables.
```
