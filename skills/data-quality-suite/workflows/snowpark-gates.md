# Workflow: Snowpark Inline Quality Gates

Loaded when: user has a Snowpark Python pipeline and wants blocking quality gates (fail-fast on bad data).

This inserts a `quality_gate()` function call directly into existing Snowpark code before each table write.

---

## Prerequisites

- Snowpark Python pipeline file(s) accessible (provide path or paste code)
- Active Snowflake session in the pipeline
- `snowflake-snowpark-python >= 1.5`

---

## Steps

### Step 1: Read the Pipeline File

Ask the user for the file path:
```
"Which Snowpark pipeline file should I add quality gates to? (e.g. ~/pipelines/orders_pipeline.py)"
```

Read the file. Identify:
1. All `write.save_as_table()` or `.write.mode().save_as_table()` calls
2. The `session` variable name
3. The DataFrame variable name at each write point
4. The target table names

---

### Step 2: Map Write Points

Show the user what was found:

```
Found 3 write points in {{file_path}}:

  Line 47: orders_df.write.save_as_table("ORDERS_CLEAN")
  Line 89: customers_df.write.mode("overwrite").save_as_table("CUSTOMERS_SILVER")
  Line 112: metrics_df.write.save_as_table("DAILY_METRICS")

I'll add a quality_gate() call before each write.

Which columns should I check for each table? (Or say "auto-detect" and I'll use PK/NOT NULL columns from the schema.)
```

---

### Step 3: Auto-Detect Columns (if requested)

If the user says "auto-detect", query the target table schema:

```sql
DESCRIBE TABLE {{database}}.{{schema}}.{{target_table}};
```

Apply classification logic (same as dbt-tests.md Step 3) to identify:
- PK columns → null + duplicate checks
- Required columns → null checks
- Numeric metrics → range bounds from `customer-config.md → THRESHOLD_DEFAULTS`
- Categorical columns → value set checks

---

### Step 4: Generate Gate Code

Load `templates/snowpark_gate.py`. Show the user exactly what will be inserted:

```python
# === DQ GATE: Before writing to ORDERS_CLEAN ===
quality_gate(session, orders_df, "ORDERS_CLEAN", checks={
    "order_id":    {"nulls": 0, "duplicates": 0},
    "customer_id": {"nulls": 0},
    "status":      {"nulls": 0, "values": {"pending","processing","shipped","delivered","cancelled"}},
    "order_value": {"nulls": 0, "min": 0},
})
# === END DQ GATE ===
```

Present all gate additions at once before modifying the file.

**STOP — await user confirmation before modifying the file.**

---

### Step 5: Insert Gates into File

Read the file content. Insert the gate function definition at the top of the file (after imports), and insert gate calls before each write point identified in Step 2.

Also add the import if not already present:
```python
from quality_gate import quality_gate  # or inline the function
```

---

### Step 6: Add the quality_gate Function

Copy `templates/snowpark_gate.py` to the same directory as the pipeline file (or offer to inline it).

```bash
cp templates/snowpark_gate.py {{pipeline_dir}}/quality_gate.py
```

---

### Step 7: Verify

Run a dry-run validation:
```bash
python -c "import ast; ast.parse(open('{{file_path}}').read()); print('Syntax OK')"
```

Show the user the modified pipeline sections for review.

---

## Output

- Modified pipeline file with `quality_gate()` calls before each write
- `quality_gate.py` helper file in the pipeline directory
- User shown exactly what was changed

---

## Error Handling

| Error | Cause | Fix |
|---|---|---|
| `QualityGateError: nulls in customer_id` | Real data quality issue | Investigate upstream; do NOT just loosen the threshold |
| `QualityGateError: value not in set` | Unexpected categorical value | Check if new value is legitimate; add to set or fix upstream |
| `Session not found` | Session variable named differently | Check the file for `session =` or `get_active_session()` |
| `AttributeError: DataFrame` | Snowpark API version mismatch | Check `snowflake-snowpark-python` version |
| Gate fires on empty DataFrame | Upstream table empty | Real quality issue — empty table should fail the pipeline |
