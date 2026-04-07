# Known Gotchas — AWS Glue Iceberg Setup

Hard-won lessons from real setup sessions. Each gotcha includes the error, root cause, and fix.

## Quick Index

| # | Symptom | Section |
|---|---------|---------|
| 1 | 0 rows in Athena | File path vs directory path |
| 2 | create-crawler fails | Crawler role requires full ARN |
| 3 | HIVE_BAD_DATA on numeric column | BINARY declared as DOUBLE |
| 4 | HIVE_BAD_DATA on ID column | INT64 declared as STRING |
| 5 | SYNTAX_ERROR: backquoted identifiers | Backticks in Trino DML |
| 6 | IAM propagation delay | Role not found after creation |
| 7 | Athena workgroup not configured | First-time Athena users |
| 8 | Crawler creates too many tables | Over-discovery from broad S3 path |
| 9 | Dropping Iceberg table deletes S3 data | Managed vs external tables |
| 10 | Stale Glue metadata after failed CTAS | Partial table left behind |
| 11 | AccessDenied on Snowflake integration | External ID trust policy (Snowflake-side) |
| 12 | CLD syncs ALL Glue databases | Namespace filtering (Snowflake-side) |

---

## 1. File path vs directory path (0 rows in Athena)

**Symptom**: `SELECT COUNT(*) FROM table` returns 0, but the parquet file exists in S3.

**Root cause**: Glue crawler pointed the table's `Location` at the individual file (e.g., `s3://bucket/data.parquet`). Athena treats the location as a **directory prefix** and looks for files *inside* that path — finding nothing.

**Fix**:
```bash
# Reorganize: move file into its own directory
aws s3 cp s3://bucket/data.parquet s3://bucket/tables/data/data.parquet
# Update or recreate the Glue table with location = s3://bucket/tables/data/
```

**Prevention**: Always organize source data as `s3://bucket/prefix/<table_name>/<files>` before crawling.

---

## 2. Crawler role requires full ARN

**Symptom**: `create-crawler` fails or crawler can't access S3.

**Root cause**: The `--role` parameter was given just the role name (`my-role`) instead of the full ARN.

**Fix**: Always use the full ARN:
```
arn:aws:iam::<ACCOUNT_ID>:role/<ROLE_NAME>
```

---

## 3. BINARY columns declared as DOUBLE → HIVE_BAD_DATA

**Symptom**: Athena CTAS fails with `HIVE_BAD_DATA: Failed to decode` on a numeric-looking column.

**Root cause**: The parquet file stores the column as BINARY (raw bytes), but the Glue table declares it as DOUBLE. Athena can't deserialize raw bytes as a floating-point number.

**Fix**: Declare the column as STRING in the external table, then CAST in the CTAS:
```sql
-- In external table DDL
price STRING
-- In CTAS SELECT
CAST(price AS DOUBLE) AS price
```

---

## 4. INT64 columns declared as STRING → HIVE_BAD_DATA

**Symptom**: Athena CTAS fails on ID or numeric columns that are actually INT64 in parquet but declared as STRING in Glue.

**Root cause**: Parquet stores these as 8-byte integers. Athena can't read raw INT64 bytes as a string.

**Fix**: Declare as BIGINT in the external table:
```sql
-- Wrong
order_id STRING
-- Right
order_id BIGINT
```

---

## 5. Backticks don't work in Athena Trino DML

**Symptom**: `SYNTAX_ERROR: backquoted identifiers are not supported` when running SELECT or CTAS.

**Root cause**: Athena's Trino engine uses ANSI SQL quoting (double quotes), not MySQL-style backticks.

**Fix**:
```sql
-- Wrong (Trino DML)
SELECT `order id` FROM table

-- Right (Trino DML)
SELECT "order id" FROM table
```

**Note**: Backticks DO work in Hive DDL (`CREATE EXTERNAL TABLE`), which is confusing. The split is:
- Hive DDL → backticks OK
- Trino DML (SELECT, CTAS, INSERT) → double quotes only

---

## 6. IAM propagation delay

**Symptom**: `start-crawler` fails with "role not found" immediately after creating the IAM role.

**Root cause**: IAM roles take ~10 seconds to propagate across AWS. Starting the crawler immediately after `create-role` may fail.

**Fix**: Add `sleep 10` between role creation and crawler start, or retry the start-crawler command once after a brief wait.

---

## 7. Athena workgroup not configured

**Symptom**: `start-query-execution` fails with an error about missing output location or workgroup.

**Root cause**: First-time Athena users may not have a default workgroup configured with an output location.

**Fix**: Either specify `--result-configuration` explicitly in every query, or configure the primary workgroup:
```bash
aws athena update-work-group \
  --work-group primary \
  --configuration-updates '{"ResultConfigurationUpdates":{"OutputLocation":"s3://<RESULTS_BUCKET>/"}}' \
  --profile <PROFILE> --region <REGION>
```

---

## 8. Crawler creates too many tables

**Symptom**: Crawler discovers more tables than expected, creating entries for subdirectories you didn't intend as separate tables.

**Root cause**: The S3 target path is too broad. If `s3://bucket/` has many subdirectories, the crawler creates one table per directory.

**Fix**: Use more specific S3 target paths. Point the crawler at the exact parent directory containing your data directories, not the bucket root.

---

## 9. Dropping Iceberg table deletes S3 data

**Symptom**: After `DROP TABLE`, the Iceberg data files in S3 are gone.

**Root cause**: Athena-managed Iceberg tables (created with `is_external = false`) are **managed tables**. Dropping them deletes the underlying S3 data.

**Fix**: This is by design for managed tables. Before dropping:
- Verify you have the data elsewhere, OR
- Convert to an external Iceberg table first (not directly supported — copy data instead)

**Prevention**: In Phase 5.8, always verify the Iceberg table is correct before dropping the source.

---

## 10. Stale Glue metadata after failed CTAS

**Symptom**: Re-running CTAS fails with "table already exists" even though the first CTAS failed.

**Root cause**: A failed CTAS may leave a partial table entry in the Glue catalog and/or orphaned data files in S3.

**Fix**:
```sql
-- Drop the partial table
DROP TABLE IF EXISTS <DB_NAME>.<TABLE>_iceberg;
```
Then clean up any orphaned files in the S3 Iceberg location before retrying:
```bash
aws s3 rm s3://<BUCKET>/iceberg/<TABLE>/ --recursive --profile <PROFILE>
```

---

> **Note**: Gotchas #11 and #12 below apply to the **Snowflake side** (handled by the `iceberg` bundled skill). They're included here so you can warn the user during handoff.

## 11. Each Snowflake integration generates a unique external ID

**Symptom**: Catalog integration works but external volume gets `AccessDenied`, or vice versa.

**Root cause**: Both the catalog integration AND external volume generate their own `IAM_USER_ARN` + `EXTERNAL_ID` pairs. All of them must be in the IAM trust policy.

**Fix**: After creating each integration in Snowflake, run:
```sql
DESCRIBE CATALOG INTEGRATION <name>;
-- Look for: GLUE_AWS_IAM_USER_ARN, GLUE_AWS_EXTERNAL_ID

DESCRIBE EXTERNAL VOLUME <name>;
-- Look for: STORAGE_AWS_IAM_USER_ARN, STORAGE_AWS_EXTERNAL_ID
```
Collect ALL ARN and external ID values. Add every one to the trust policy's `Principal.AWS` array and `Condition.StringEquals.sts:ExternalId` array:
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"AWS": ["<ARN_1>", "<ARN_2>", "<ARN_3>"]},
    "Action": "sts:AssumeRole",
    "Condition": {
      "StringEquals": {
        "sts:ExternalId": ["<EXT_ID_1>", "<EXT_ID_2>", "<EXT_ID_3>"]
      }
    }
  }]
}
```

---

## 12. CLD syncs ALL Glue databases (not just one)

**Symptom**: Tables from unexpected Glue databases appear in the CLD, and some fail with S3 access errors.

**Root cause**: Without namespace filtering, the CLD discovers every table the catalog integration can see across all Glue databases.

**Impact**: Non-blocking — tables outside the external volume's S3 scope just fail to read. The tables you care about still work.

**Mitigation**: 
- Scope the IAM role's Glue permissions to specific databases:
  ```json
  "Resource": ["arn:aws:glue:<REGION>:<ACCOUNT>:database/<DB_NAME>",
               "arn:aws:glue:<REGION>:<ACCOUNT>:table/<DB_NAME>/*"]
  ```
- Filter by schema in Snowflake queries: `SELECT * FROM my_cld.target_db.table_name;`
