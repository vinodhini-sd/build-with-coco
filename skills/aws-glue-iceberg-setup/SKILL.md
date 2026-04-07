---
name: aws-glue-iceberg-setup
description: "Set up AWS Glue as an Iceberg REST catalog for Snowflake CLD. Covers AWS auth, S3 discovery, Glue DB + crawler, schema validation, and parquet-to-Iceberg conversion via Athena CTAS. Hands off to the bundled iceberg skill for Snowflake-side setup. Triggers: aws glue iceberg, glue crawler, athena CTAS, parquet to iceberg, S3 to iceberg, glue database, athena iceberg conversion, aws iceberg setup."
---

# AWS Glue Iceberg Setup

> Prepare AWS-side infrastructure so Snowflake can query Iceberg tables through a Catalog-Linked Database (CLD).
> This skill covers **AWS only** — phases 1-5. Hand off to the bundled `iceberg` skill for the Snowflake side (catalog integration, external volume, CLD creation).

---

## When to invoke

- User wants to set up AWS Glue as an Iceberg REST catalog for Snowflake
- User has parquet/CSV/JSON data in S3 and wants it queryable as Iceberg in Snowflake
- User needs help converting existing data to Iceberg format via Athena
- User mentions "Glue", "Iceberg", "catalog-linked database" + AWS setup

## What this skill does NOT cover

- Snowflake catalog integration, external volume, or CLD creation → hand off to **`iceberg`** bundled skill
- Lake Formation permissions → we use `EXTERNAL_VOLUME_CREDENTIALS` mode to avoid LF dependency
- Writing/updating Iceberg tables from Snowflake (read-only flow)

---

## Polling pattern (reuse for crawler and Athena)

- Poll interval: **15 seconds**
- Max attempts: **40** (10 minutes)
- Crawler state transitions: `RUNNING` → `STOPPING` → `READY`
- Athena state transitions: `RUNNING` → `SUCCEEDED` or `FAILED`
- On `FAILED`: fetch error reason, present to user, diagnose before retrying

---

## Phase 1 — AWS Authentication

**Goal**: Verify the user has working AWS CLI access to the target account.

### Steps

1. Ask the user which AWS CLI profile to use (or if they need to configure one).

2. Verify credentials:
   ```bash
   aws sts get-caller-identity --profile <PROFILE>
   ```

3. Capture from the output:
   - `AWS_ACCOUNT_ID` — the 12-digit account number
   - `AWS_REGION` — ask the user which region the S3 data lives in

4. Verify S3 access:
   ```bash
   aws s3 ls s3://<BUCKET>/ --profile <PROFILE>
   ```

> **If AWS CLI is not installed**: Direct user to `brew install awscli` (macOS) or `pip install awscli`. If they need to configure a profile: `aws configure --profile <name>`.

### Error recovery

- `ExpiredToken` / `ExpiredTokenException` → "Your AWS session has expired. Run `aws sso login --profile <PROFILE>` or refresh your credentials."
- `InvalidClientTokenId` → "The AWS profile isn't configured correctly. Run `aws configure --profile <PROFILE>` to set it up."
- `AccessDenied` on S3 → "Your IAM user/role doesn't have S3 access to this bucket. Check your IAM policies."

---

## Phase 2 — S3 Data Discovery

**Goal**: Find and inventory the source data files in S3.

### Steps

1. List bucket contents recursively:
   ```bash
   aws s3 ls s3://<BUCKET>/ --recursive --profile <PROFILE>
   ```

2. Identify file formats (parquet, CSV, JSON, ORC) and note their paths.

3. Build a source inventory table:

   | File | Format | Size | S3 Path |
   |------|--------|------|---------|
   | customer_reviews.parquet | parquet | 12.3 KB | s3://bucket/parquet/customer_reviews.parquet |

4. **CRITICAL — Directory structure check**:
   - Athena expects each table's data at a **directory prefix**, not a single file path
   - If files are flat (e.g., `s3://bucket/data.parquet`), they must be reorganized:
     ```bash
     # Copy into directory structure
     aws s3 cp s3://<BUCKET>/data.parquet \
       s3://<BUCKET>/tables/data/data.parquet \
       --profile <PROFILE>
     ```
   - Each table needs its own directory: `s3://bucket/tables/<table_name>/`

> See `references/KNOWN_GOTCHAS.md` → "File path vs directory path" for details on this issue.

### **STOP** — Present the S3 inventory to the user. Ask: "These are the files I found. Which ones should we convert to Iceberg? Any to skip?"

---

## Phase 3 — Glue Database & Crawler Setup

**Goal**: Create a Glue database and crawler to auto-discover table schemas.

### 3.1 Create the Glue database

```bash
aws glue create-database \
  --database-input '{"Name":"<DB_NAME>"}' \
  --profile <PROFILE> \
  --region <REGION>
```

> **Note**: Glue database names must be lowercase and can only contain letters, numbers, and underscores. Hyphens are not allowed.

### 3.2 Create an IAM role for the crawler

The crawler needs an IAM role with:
- `AWSGlueServiceRole` managed policy (for Glue operations)
- S3 read access to the source bucket

```bash
# Create the role with Glue trust policy
aws iam create-role \
  --role-name <CRAWLER_ROLE_NAME> \
  --assume-role-policy-document '{
    "Version":"2012-10-17",
    "Statement":[{
      "Effect":"Allow",
      "Principal":{"Service":"glue.amazonaws.com"},
      "Action":"sts:AssumeRole"
    }]
  }' \
  --profile <PROFILE>

# Attach Glue service policy
aws iam attach-role-policy \
  --role-name <CRAWLER_ROLE_NAME> \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole \
  --profile <PROFILE>

# Add inline S3 read policy
aws iam put-role-policy \
  --role-name <CRAWLER_ROLE_NAME> \
  --policy-name s3-read-access \
  --policy-document '{
    "Version":"2012-10-17",
    "Statement":[{
      "Effect":"Allow",
      "Action":["s3:GetObject","s3:ListBucket","s3:GetBucketLocation"],
      "Resource":["arn:aws:s3:::<BUCKET>","arn:aws:s3:::<BUCKET>/*"]
    }]
  }' \
  --profile <PROFILE>
```

> **IAM propagation delay**: After creating the role, wait ~10 seconds before starting the crawler. IAM roles take time to propagate. Starting immediately may fail with "role not found."

### 3.3 Create and run the crawler

```bash
aws glue create-crawler \
  --name <CRAWLER_NAME> \
  --role "arn:aws:iam::<ACCOUNT_ID>:role/<CRAWLER_ROLE_NAME>" \
  --database-name <DB_NAME> \
  --targets '{"S3Targets":[{"Path":"s3://<BUCKET>/<PREFIX>/"}]}' \
  --schema-change-policy '{"UpdateBehavior":"UPDATE_IN_DATABASE","DeleteBehavior":"LOG"}' \
  --recrawl-policy '{"RecrawlBehavior":"CRAWL_EVERYTHING"}' \
  --profile <PROFILE> \
  --region <REGION>
```

> **GOTCHA**: The `--role` parameter requires the **full ARN**, not just the role name. Using just the name silently fails or errors.

> **Crawler target path**: After Phase 2 reorganization, use the **parent directory** that contains all table subdirectories (e.g., `s3://bucket/tables/`), not individual table paths. The crawler will create one table per subdirectory.

Start the crawler (after ~10s IAM propagation delay):
```bash
sleep 10
aws glue start-crawler --name <CRAWLER_NAME> \
  --profile <PROFILE> --region <REGION>
```

Poll until complete (see Polling pattern above):
```bash
aws glue get-crawler --name <CRAWLER_NAME> \
  --profile <PROFILE> --region <REGION> \
  --query 'Crawler.State'
```

### Error recovery

- `EntityNotFoundException` → Database or crawler name is wrong. Check spelling.
- `InvalidInputException` on role → Role ARN is malformed or doesn't exist. Verify with `aws iam get-role`.
- Crawler stuck in `RUNNING` after 10 minutes → Check the AWS Glue console for errors. Common cause: S3 permissions on the crawler role.
- `AlreadyExistsException` → Database or crawler already exists. This is OK — use the existing one or delete and recreate.

---

## Phase 4 — Schema Discovery & Validation

**Goal**: Verify Glue tables were created correctly and fix type mismatches.

> **Load `references/ATHENA_TYPE_MAPPING.md` now** — cross-reference every column's Glue-inferred type against the mapping table.

### 4.1 List discovered tables

```bash
aws glue get-tables --database-name <DB_NAME> \
  --profile <PROFILE> --region <REGION> \
  --query 'TableList[].{Name:Name,Cols:StorageDescriptor.Columns[].{N:Name,T:Type},Location:StorageDescriptor.Location}'
```

### 4.2 Validate each table's schema

For each table, compare the Glue-inferred types against actual parquet column types. Common mismatches:

| Parquet Physical Type | Glue Infers | Athena Expects | Fix |
|----------------------|-------------|----------------|-----|
| BINARY | string | string | Declare as STRING (not DOUBLE even if it looks numeric) |
| INT64 | bigint | bigint | Declare as BIGINT (not STRING) |
| DOUBLE | double | double | Keep as DOUBLE |
| BYTE_ARRAY (UTF8) | string | string | Keep as STRING |

> See `references/ATHENA_TYPE_MAPPING.md` for the full mapping table including complex types.

### 4.3 Verify row counts

For each table, check the crawler's table location:
```bash
aws glue get-table --database-name <DB_NAME> --name <TABLE> \
  --profile <PROFILE> --region <REGION> \
  --query 'Table.StorageDescriptor.Location'
```

If the location points to a **file** (ends in `.parquet`) instead of a **directory prefix** (ends in `/`), Athena will return 0 rows. Fix by reorganizing files per Phase 2 step 4.

### **STOP** — Present discovered tables and their schemas to the user. Ask: "Here are the tables and column types the crawler found. Do these look correct, or should we fix any types before converting to Iceberg?"

---

## Phase 5 — Parquet-to-Iceberg Conversion via Athena

**Goal**: Convert Glue external tables to Iceberg format using Athena CTAS.

### 5.0 Verify Athena engine version

Iceberg CTAS requires **Athena engine version 3** (Trino-based). Verify the workgroup uses engine v3:
```bash
aws athena get-work-group --work-group primary \
  --profile <PROFILE> --region <REGION> \
  --query 'WorkGroup.Configuration.EngineVersion'
```

If the result shows `Athena engine version 2` or earlier, the user must update their workgroup or create a new one with engine v3.

### 5.1 Set up Athena output location

```bash
# Create results bucket if it doesn't exist
aws s3 mb s3://<ACCOUNT_ID>-<REGION>-athena-results \
  --profile <PROFILE> --region <REGION>
```

### 5.2 IAM permissions for Athena CTAS

Athena CTAS **writes** Iceberg data files to S3. The IAM identity running Athena needs S3 write access to the Iceberg output location. If using the default Athena workgroup, your user/role needs:

```json
{
  "Effect": "Allow",
  "Action": ["s3:PutObject", "s3:GetObject", "s3:ListBucket", "s3:GetBucketLocation", "s3:DeleteObject"],
  "Resource": ["arn:aws:s3:::<BUCKET>/iceberg/*", "arn:aws:s3:::<BUCKET>"]
}
```

> This is separate from the crawler role. The crawler only reads source data; Athena writes the Iceberg output.

### 5.3 Run CTAS for each table

Use Athena's `StartQueryExecution` API to convert each table. Athena creates **Iceberg v2** tables by default:

```bash
aws athena start-query-execution \
  --query-string "
    CREATE TABLE <DB_NAME>.<TABLE>_iceberg
    WITH (
      table_type = 'ICEBERG',
      location = 's3://<BUCKET>/iceberg/<TABLE>/',
      is_external = false,
      format = 'PARQUET',
      write_compression = 'ZSTD'
    ) AS SELECT * FROM <DB_NAME>.<TABLE>
  " \
  --query-execution-context '{"Database":"<DB_NAME>"}' \
  --result-configuration '{"OutputLocation":"s3://<RESULTS_BUCKET>/"}' \
  --profile <PROFILE> --region <REGION>
```

> **Table properties** (from [AWS docs](https://docs.aws.amazon.com/athena/latest/ug/querying-iceberg-creating-tables.html)):
> - `format` — defaults to `PARQUET`. Explicit is better for cross-engine clarity.
> - `write_compression` — defaults to `ZSTD` in recent Athena. Snowflake reads ZSTD and SNAPPY.
> - `vacuum_min_snapshots_to_keep` — set explicitly if you plan to run VACUUM later.

For partitioned tables (recommended for large datasets):
```sql
CREATE TABLE db.table_iceberg
WITH (
  table_type = 'ICEBERG',
  location = 's3://bucket/iceberg/table/',
  is_external = false,
  format = 'PARQUET',
  write_compression = 'ZSTD'
)
AS SELECT * FROM db.table_source
```

To add partitioning (use Iceberg hidden partitioning transforms):
```sql
CREATE TABLE db.orders_iceberg
WITH (
  table_type = 'ICEBERG',
  location = 's3://bucket/iceberg/orders/',
  is_external = false,
  partitioning = ARRAY['month(order_date)']
)
AS SELECT * FROM db.orders
```

> **Partition transforms** supported: `year()`, `month()`, `day()`, `hour()`, `bucket(N, col)`, `truncate(N, col)`.
> For small datasets (<1M rows), skip partitioning — the overhead isn't worth it.

Then poll for completion (see Polling pattern above):
```bash
aws athena get-query-execution \
  --query-execution-id <ID> \
  --profile <PROFILE> --region <REGION> \
  --query 'QueryExecution.Status.State'
```

On FAILED, get the error:
```bash
aws athena get-query-execution \
  --query-execution-id <ID> \
  --profile <PROFILE> --region <REGION> \
  --query 'QueryExecution.Status.StateChangeReason'
```

### 5.4 Handle type mismatch errors

If CTAS fails with `HIVE_BAD_DATA` or similar:

1. Drop the failed Iceberg table (if partially created)
2. Create a new external table with corrected column types
3. Re-run CTAS with explicit column casting

Example with column-level fixes:
```sql
CREATE TABLE db.table_iceberg
WITH (
  table_type = 'ICEBERG',
  location = 's3://bucket/iceberg/table/',
  is_external = false
) AS
SELECT
  CAST(id AS BIGINT) AS id,
  name,
  CAST(price AS DOUBLE) AS price
FROM db.table_source
```

### 5.5 Athena SQL dialect notes

- **Athena Trino engine uses double quotes** for identifiers: `"column name"` (NOT backticks)
- Backticks work in Hive DDL (`CREATE EXTERNAL TABLE`) but NOT in Trino DML (`SELECT`, `CTAS`)
- If a column name has spaces, use: `SELECT "order id" FROM ...`

### 5.6 Verify converted tables

After all CTAS queries complete, verify row counts:
```sql
SELECT COUNT(*) FROM <DB_NAME>.<TABLE>_iceberg;
```

Run this for each table to confirm data was fully converted.

### 5.7 Table maintenance (for ongoing use)

Athena supports OPTIMIZE and VACUUM for Iceberg tables:

```sql
-- Compact small files (run periodically for tables with frequent writes)
OPTIMIZE db.table_iceberg REWRITE DATA USING BIN_PACK;

-- Expire old snapshots and delete orphaned files
VACUUM db.table_iceberg;
```

> **Limits**: OPTIMIZE can only process 100 partitions per query — use a WHERE clause on partition columns to stay under the limit. VACUUM can delete up to 20,000 objects per execution.

For CTAS one-time conversions, maintenance is not urgent — but document it for the user if they plan to write to these tables later.

### 5.8 Clean up source tables (optional)

> **STOP** — Ask the user before proceeding. Dropping source tables is destructive.

> **WARNING**: Dropping an Athena-managed Iceberg table (`is_external = false`) **deletes the underlying S3 data**. Only drop if you're sure the Iceberg table is the one you want to keep.

Once Iceberg tables are verified, you can drop the original external tables:
```sql
DROP TABLE <DB_NAME>.<TABLE>;
-- Optionally rename Iceberg table
ALTER TABLE <DB_NAME>.<TABLE>_iceberg RENAME TO <DB_NAME>.<TABLE>;
```

---

## Cost awareness

- **Athena CTAS**: Charged per bytes scanned from the source table. For large datasets, this can be significant. Warn the user before converting tables >100GB.
- **Glue Crawler**: Charged per DPU-hour. A single crawl of a small bucket is typically <$1, but large buckets with many files can cost more.
- **S3 storage**: Iceberg conversion creates new data files. The source parquet AND Iceberg files coexist until you clean up the source.

---

## Handoff to Snowflake

Once all tables are converted to Iceberg in Glue, hand off to the **bundled `iceberg` skill** with these collected variables:

| Variable needed by `iceberg` skill | Source |
|------------------------------------|--------|
| `AWS_ACCOUNT_ID` | Phase 1 |
| `AWS_REGION` | Phase 1 |
| `S3_BUCKET` | Phase 2 |
| `ICEBERG_OUTPUT_PREFIX` (e.g., `iceberg/`) | Phase 5 |
| `GLUE_DB_NAME` | Phase 3 |
| `IAM_ROLE_ARN` for Snowflake (may differ from crawler role) | User must provide or create |
| `TABLE_NAMES[]` — list of converted Iceberg tables | Phase 5 |

Tell the user:
> AWS side is ready. Your Iceberg tables are registered in Glue database `<DB_NAME>`.
> Next step: set up the Snowflake catalog integration, external volume, and CLD.
> I'll hand off to the Iceberg skill for that.

Then invoke the `iceberg` bundled skill.

> **Important**: The IAM role for Snowflake's catalog integration and external volume is typically a **separate role** from the Glue crawler role. The Snowflake role needs `glue:GetTable`, `glue:GetTables`, `glue:GetDatabase`, `glue:GetDatabases`, `glue:GetCatalog` plus S3 read access. The `iceberg` skill will guide through this.

> **Snowflake type mapping note**: Athena `TIMESTAMP` (without timezone) maps to Iceberg `timestamp`, which Snowflake reads as `TIMESTAMP_NTZ(6)` (microsecond precision, no timezone). If your data has timezone-aware timestamps, use `TIMESTAMP WITH TIME ZONE` in Athena — Snowflake maps Iceberg `timestamptz` to `TIMESTAMP_LTZ(6)`. See `references/ATHENA_TYPE_MAPPING.md` for the full Iceberg→Snowflake mapping.

---

## Stopping points summary

| After Phase | Gate | What to confirm |
|-------------|------|-----------------|
| Phase 2 | **STOP** | Which files to convert, directory structure OK |
| Phase 4 | **STOP** | Table schemas correct, types validated |
| Phase 5.8 | **STOP** | Before dropping source tables (destructive) |

---

## Variables to collect

| Variable | Example | Phase |
|----------|---------|-------|
| `AWS_PROFILE` | `Contributor-123456789012` | 1 |
| `AWS_ACCOUNT_ID` | `123456789012` | 1 |
| `AWS_REGION` | `us-west-2` | 1 |
| `S3_BUCKET` | `avalanche-dataset` | 2 |
| `S3_DATA_PREFIX` | `parquet/` | 2 |
| `GLUE_DB_NAME` | `avalanche_db` | 3 |
| `CRAWLER_ROLE_NAME` | `glue-crawler-role` | 3 |
| `CRAWLER_ROLE_ARN` | `arn:aws:iam::123456789012:role/glue-crawler-role` | 3 |
| `CRAWLER_NAME` | `avalanche-crawler` | 3 |
| `TABLE_NAMES[]` | `[customer_reviews, order_history, ...]` | 4 |
| `ICEBERG_OUTPUT_PREFIX` | `iceberg/` | 5 |
| `ATHENA_RESULTS_BUCKET` | `123456789012-us-west-2-athena-results` | 5 |

---

## Error handling summary

| Error | Phase | Cause | Fix |
|-------|-------|-------|-----|
| `ExpiredToken` | 1 | AWS session expired | `aws sso login --profile <PROFILE>` |
| `AccessDenied` on S3 | 1 | Missing S3 permissions | Check IAM policies |
| `AlreadyExistsException` | 3 | DB/crawler exists | Use existing or delete first |
| Crawler stuck `RUNNING` | 3 | S3 permission or network issue | Check Glue console |
| `HIVE_BAD_DATA` | 5 | Type mismatch in CTAS | Fix types per `ATHENA_TYPE_MAPPING.md` |
| `TABLE_NOT_FOUND` | 5 | Glue table name mismatch | Verify with `get-tables` |
| `SYNTAX_ERROR: backquoted identifiers` | 5 | Backticks in Trino DML | Use double quotes |
