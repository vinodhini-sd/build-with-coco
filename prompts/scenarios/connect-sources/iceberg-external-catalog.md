# Query Your Data Lake via Iceberg Tables

> Connect Snowflake to S3 Parquet data managed by AWS Glue, using Apache Iceberg tables.

## The Prompt

```
Set up Iceberg tables in Snowflake to query my existing data lake. Ask me for the cloud
storage provider, storage path, IAM role or access credentials, and catalog type (e.g.
AWS Glue, Unity Catalog), then create the external volume, catalog integration, and Iceberg
tables. Verify I can query the data and that auto-refresh is working.
```

## What This Triggers

- Iceberg skill invocation
- External volume creation (S3 storage)
- Catalog integration (AWS Glue)
- Iceberg table creation and verification
- Auto-refresh configuration and testing

## Before You Run

- S3 bucket with Parquet/Iceberg data
- AWS Glue catalog managing the tables
- IAM role ARN with trust policy configured to allow Snowflake to assume it — Snowflake provides the external ID during integration creation; the trust policy must already exist before this prompt will complete
- ACCOUNTADMIN role (for integration objects)

## Tips

- Replace `s3://my-bucket/data/events/` with your actual S3 path
- For Unity Catalog instead of Glue, say "managed by Databricks Unity Catalog"
- Add "enable ALLOW_WRITES" if you need Snowflake to write back to the lake
