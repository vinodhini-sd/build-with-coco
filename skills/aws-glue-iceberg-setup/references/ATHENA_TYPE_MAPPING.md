# Athena Type Mapping — Parquet to Iceberg to Snowflake

## When to use this reference

- **Proactively in Phase 4** — After the crawler finishes, load this file and cross-reference every column's Glue-inferred type against the mapping table.
- **Reactively in Phase 5** — When a CTAS fails with HIVE_BAD_DATA, use the debugging steps below to identify and fix the mismatch.

When converting parquet tables to Iceberg via Athena CTAS, type mismatches between the physical parquet encoding and the Glue catalog declaration cause `HIVE_BAD_DATA` errors.

## Parquet → Athena Mappings

| Parquet Physical Type | Parquet Logical Type | Glue Crawler Infers | Correct Athena Type | Notes |
|----------------------|---------------------|--------------------|--------------------|-------|
| BOOLEAN | — | boolean | BOOLEAN | Direct match |
| INT32 | — | int | INT | Direct match |
| INT32 | DATE | date | DATE | Direct match |
| INT64 | — | bigint | BIGINT | Crawler may infer as STRING for ID columns — always use BIGINT |
| INT64 | TIMESTAMP_MILLIS | timestamp | TIMESTAMP | Direct match |
| INT64 | TIMESTAMP_MICROS | timestamp | TIMESTAMP | Direct match |
| INT96 | — | timestamp | TIMESTAMP | Legacy Spark format — crawler usually handles correctly |
| FLOAT | — | float | FLOAT / REAL | Direct match |
| DOUBLE | — | double | DOUBLE | Crawler may infer as STRING if values look like text — use DOUBLE |
| BYTE_ARRAY | UTF8 | string | STRING / VARCHAR | Direct match |
| BYTE_ARRAY | — | binary | BINARY | If you need text, CAST to VARCHAR |
| BINARY | — | binary | STRING | **GOTCHA**: Numeric-looking BINARY columns (e.g., prices) will fail if declared as DOUBLE. Declare as STRING first, then CAST in CTAS. |
| FIXED_LEN_BYTE_ARRAY | DECIMAL | decimal(p,s) | DECIMAL(p,s) | Direct match |

## Complex Types

| Parquet Type | Glue Infers | Athena Type | Snowflake Type | Notes |
|-------------|-------------|-------------|----------------|-------|
| LIST | array<T> | ARRAY<T> | Structured ARRAY | Nested arrays work in Iceberg CTAS |
| MAP | map<K,V> | MAP<K,V> | MAP | Direct match |
| STRUCT | struct<...> | ROW(...) | Structured OBJECT | Trino uses ROW syntax, not STRUCT. Max 1000 sub-columns in Snowflake. |

## Iceberg → Snowflake Type Mapping

After Athena creates Iceberg tables, Snowflake reads them through the CLD. Key mappings (from [Snowflake docs](https://docs.snowflake.com/en/user-guide/tables-iceberg-data-types)):

| Iceberg Type | Snowflake Type | Notes |
|-------------|----------------|-------|
| boolean | BOOLEAN | |
| int | NUMBER(10,0) | |
| long | NUMBER(20,0) | |
| float | REAL | |
| double | REAL | |
| decimal(p,s) | NUMBER(p,s) | |
| date | DATE | |
| time | TIME(6) | Microsecond precision |
| **timestamp** | **TIMESTAMP_NTZ(6)** | **No timezone. This is the key gotcha — Athena TIMESTAMP has no TZ, so Snowflake reads it as NTZ.** |
| **timestamptz** | **TIMESTAMP_LTZ(6)** | **With timezone (UTC). Use if your data has TZ-aware timestamps.** |
| string | VARCHAR | |
| uuid | UUID | |
| binary | BINARY | Requires `2026_02` behavior-change bundle |
| fixed(L) | BINARY(L) | Requires `2026_02` behavior-change bundle |
| struct | Structured OBJECT | Max 1000 sub-columns |
| list | Structured ARRAY | Max 1000 sub-columns |
| map | MAP | Max 1000 sub-columns |

## Debugging Type Mismatches

1. **Check actual parquet schema** (if pyarrow is available — `pip install pyarrow` first):
   ```python
   import pyarrow.parquet as pq
   schema = pq.read_schema('file.parquet')
   for field in schema:
       print(f"{field.name}: {field.type} (physical: {field.physical_type})")
   ```

2. **Check Glue catalog declaration**:
   ```bash
   aws glue get-table --database-name <DB> --name <TABLE> \
     --query 'Table.StorageDescriptor.Columns[].{Name:Name,Type:Type}'
   ```

3. **Compare and fix**: If Glue says `string` but parquet is `INT64`, create a new external table with the correct type, or use explicit CASTs in your CTAS.

## CTAS with Explicit Casts

When types don't match, use explicit casting in the SELECT:

```sql
CREATE TABLE db.table_iceberg
WITH (table_type='ICEBERG', location='s3://bucket/iceberg/table/', is_external=false)
AS SELECT
  CAST(id AS BIGINT) AS id,
  name,
  CAST(price AS DOUBLE) AS price,
  CAST(created_at AS TIMESTAMP) AS created_at
FROM db.table_source
```
