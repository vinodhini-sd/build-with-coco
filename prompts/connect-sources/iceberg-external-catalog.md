# Query Your Data Lake via Iceberg Tables

> Connect Snowflake to S3 Parquet data managed by AWS Glue, using Apache Iceberg tables.

## The Prompt

```
Set up Apache Iceberg tables in Snowflake that read from my existing data lake on S3.
I have Parquet files at s3://my-bucket/data/events/ managed by an AWS Glue catalog.
Create the external volume, catalog integration, and Iceberg tables. Verify I can query
the data and that auto-refresh is working. Ask me for the IAM role ARN and bucket details.
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
- IAM role ARN with trust policy for Snowflake
- ACCOUNTADMIN role (for integration objects)

## Tips

- Replace `s3://my-bucket/data/events/` with your actual S3 path
- For Unity Catalog instead of Glue, say "managed by Databricks Unity Catalog"
- Add "enable ALLOW_WRITES" if you need Snowflake to write back to the lake
