# Workflow: Great Expectations

Loaded when: user requests GX specifically, OR data is in a non-Snowflake/non-Spark source (Pandas, S3 CSV, local files).

Works with any GX-supported datasource: Snowflake, Spark, Pandas, S3, PostgreSQL, BigQuery, Redshift, Azure Blob, local files.

---

## Prerequisites

- Python 3.8+ with GX installable (`pip install great-expectations`)
- Access to the datasource (connection string, file path, or Snowflake connection)
- Target table or file accessible from the Python environment

---

## Steps

### Step 1: Install / Verify GX

```bash
# Check if already installed
python -c "import great_expectations; print(great_expectations.__version__)"

# Install if missing
pip install great-expectations
```

Target GX version: `>=0.18` (uses the new fluent datasource API). Warn the user if they have an older version — the API changed significantly.

---

### Step 2: Determine Datasource Type

Ask the user which datasource to connect to:

| Datasource | Connection info needed |
|---|---|
| Snowflake | Active CoCo connection (uses env vars) |
| Spark | SparkSession object name in their script |
| Pandas / local file | File path |
| PostgreSQL | Connection string |
| S3 CSV/Parquet | S3 URI + AWS credentials |

Use the fluent datasource API (GX 0.18+). See `templates/gx_expectations.py` for the full setup pattern.

---

### Step 3: Profile the Data

Before generating expectations, get column stats:

**For Snowflake:**
```sql
DESCRIBE TABLE {{database}}.{{schema}}.{{table}};
SELECT
    COUNT(*) AS row_count,
    COUNT(DISTINCT {{pk_column}}) AS unique_pk
FROM {{database}}.{{schema}}.{{table}};
```

**For Pandas/local:**
```python
df = pd.read_parquet("{{file_path}}")
df.describe()
df.dtypes
df.isnull().sum()
```

---

### Step 4: Generate Expectation Suite

Load `templates/gx_expectations.py` and populate for the user's datasource and columns.

Present the expectation suite before generating the file:

```
I'll create an expectation suite with:

  Table-level:
  - expect_table_row_count_to_be_between(min=1000, max=None)
  - expect_table_columns_to_match_set(["customer_id", "status", ...])

  Column: customer_id
  - expect_column_values_to_not_be_null()
  - expect_column_values_to_be_unique()

  Column: status
  - expect_column_values_to_not_be_null()
  - expect_column_values_to_be_in_set(["active", "inactive", "pending"])

  Column: order_value
  - expect_column_values_to_not_be_null()
  - expect_column_mean_to_be_between(min_value=10, max_value=500)

Proceed? (yes / add more columns / adjust values)
```

**STOP — await confirmation before generating files.**

---

### Step 5: Write the Expectation Suite File

Generate the Python script from the template. Write to `{{output_path}}/expectations_{{table_name}}.py`.

---

### Step 6: Set Up Checkpoint

A checkpoint runs the suite against the datasource and reports pass/fail.

```python
checkpoint = context.add_or_update_checkpoint(
    name="{{table_name}}_checkpoint",
    validations=[
        {
            "batch_request": batch_request,
            "expectation_suite_name": "{{suite_name}}",
        }
    ],
)
result = checkpoint.run()
print(result.success)
```

Show the user how to run the checkpoint:
```bash
python expectations_{{table_name}}.py
```

---

### Step 7: CI Integration (Optional)

If the user wants to run GX in CI:

```yaml
# GitHub Actions example
- name: Run data quality checks
  run: python expectations_{{table_name}}.py
  env:
    SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
    SNOWFLAKE_USER: ${{ secrets.SNOWFLAKE_USER }}
```

---

## Output

- `expectations_{{table_name}}.py` — runnable GX expectation suite
- Checkpoint configured and runnable
- (Optional) CI/CD integration snippet

---

## Error Handling

| Error | Cause | Fix |
|---|---|---|
| `ImportError: great_expectations` | Not installed | `pip install great-expectations` |
| `ConnectionError` on Snowflake | Auth or network issue | Check CoCo connection is active |
| `AttributeError: fluent` | Old GX version (< 0.18) | `pip install --upgrade great-expectations` |
| Expectations fail on first run | Data doesn't match generated thresholds | Profile actual data values first, adjust expectations |
| `suite not found` | Checkpoint references wrong suite name | Check suite name matches exactly (case-sensitive) |
