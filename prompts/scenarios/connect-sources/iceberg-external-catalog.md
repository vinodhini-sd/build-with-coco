# Query Your Data Lake via Iceberg Tables

> Connect Snowflake to your data lake via Apache Iceberg — works with S3/Glue, ADLS/Unity Catalog, or GCS.

## The Prompt

```
Set up Iceberg tables in Snowflake to query my existing data lake. Ask me for the cloud
storage provider, storage path, IAM role or access credentials, and catalog type (e.g.
AWS Glue, Unity Catalog), then create the external volume, catalog integration, and Iceberg
tables. Verify I can query the data and that auto-refresh is working.
```

## What This Triggers

- Iceberg skill invocation
- External volume creation (cloud storage — S3, ADLS, or GCS)
- Catalog integration (AWS Glue, Unity Catalog, or REST catalog)
- Iceberg table creation and verification
- Auto-refresh configuration and testing

## Before You Run

- Cloud storage location with Parquet/Iceberg data (S3, Azure Blob, or GCS)
- Catalog managing the tables (AWS Glue, Databricks Unity Catalog, or REST-compatible)
- Cloud credentials configured to allow Snowflake access:
  - **AWS**: IAM role ARN with trust policy — Snowflake provides the external ID during integration creation; the trust policy must exist before this prompt completes
  - **Azure**: Service principal with Storage Blob Data Reader on the container
  - **GCS**: Service account with Storage Object Viewer
- ACCOUNTADMIN role (for integration objects)

## Tips

- Tell CoCo "I'm on S3 with Glue" or "Azure ADLS with Unity Catalog" to skip the interactive questions
- Add "enable ALLOW_WRITES" if you need Snowflake to write back to the lake
- Add "use a REST catalog" if your catalog exposes an Iceberg REST endpoint
