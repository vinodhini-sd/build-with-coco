# Workflow: PySpark Inline Quality Gates

Loaded when: user has a PySpark pipeline and wants blocking quality checks embedded directly in the pipeline code.

Inserts an `assert_quality()` function call before each DataFrame write. Works with any PySpark target: S3, Delta, Hive, Iceberg, HDFS.

---

## Prerequisites

- PySpark pipeline file(s) accessible (provide path or paste code)
- PySpark 3.x
- Access to describe the target schema (if auto-detecting columns)

---

## Steps

### Step 1: Read the Pipeline File

Ask the user for the file path:
```
"Which PySpark pipeline file should I add quality gates to?"
```

Read the file. Identify:
1. All `.write.` calls: `.write.parquet()`, `.write.saveAsTable()`, `.write.format().save()`, `.writeTo().append()`, etc.
2. The DataFrame variable at each write point
3. The target table or path name

---

### Step 2: Map Write Points

Present findings:

```
Found 2 write points in {{file_path}}:

  Line 63: orders_clean.write.format("delta").saveAsTable("silver.orders")
  Line 98: features_df.write.parquet("s3://{{bucket}}/features/customer_features/")

I'll add an assert_quality() call before each write.

Which columns should I check? (Or say "auto-detect" to infer from the DataFrame schema.)
```

---

### Step 3: Auto-Detect Columns (if requested)

If the user says "auto-detect", inspect the DataFrame schema in the code:

```python
# CoCo reads the pipeline and looks for .schema or .printSchema() calls
# Or infer from column names in transformations
```

If schema isn't detectable from code, ask the user to provide column names or run:
```python
df.printSchema()
df.describe().show()
```

Apply classification logic:
- Columns ending in `_id` → null + duplicate checks
- Numeric columns → null + min/max bounds
- String columns with `status`, `type`, `state` → value set check
- Timestamp columns → null check + freshness (max age)

---

### Step 4: Generate Gate Code

Load `templates/spark_gate.py`. Show the user exactly what will be inserted:

```python
# === DQ GATE: Before writing silver.orders ===
assert_quality(orders_clean, "silver.orders", checks={
    "order_id":    {"null_pct": 0, "duplicate_pct": 0},
    "customer_id": {"null_pct": 0},
    "status":      {"null_pct": 0, "values": {"pending","shipped","delivered","cancelled"}},
    "order_value": {"null_pct": 0, "min": 0},
    "__row_count__": {"min": 1},
})
# === END DQ GATE ===
```

Present all gate additions at once.

**STOP — await user confirmation before modifying the file.**

---

### Step 5: Insert Gates into File

Read the file. Insert:
1. The `assert_quality` import at the top (after existing imports)
2. Gate calls immediately before each identified write point

---

### Step 6: Add the assert_quality Function

Copy `templates/spark_gate.py` to the same directory as the pipeline file:

```bash
cp templates/spark_gate.py {{pipeline_dir}}/spark_quality_gate.py
```

---

### Step 7: Verify Syntax

```bash
python -m py_compile {{file_path}} && echo "Syntax OK"
```

---

### Step 8: Offer GX Spark Alternative

After inserting inline gates, offer:

```
For more advanced checks (statistical profiling, HTML reports, CI integration),
I can also set up a Great Expectations Spark datasource alongside these inline gates.
Say "add GX too" to load that workflow.
```

---

## Output

- Modified pipeline file with `assert_quality()` calls before each write
- `spark_quality_gate.py` helper file in the pipeline directory

---

## Error Handling

| Error | Cause | Fix |
|---|---|---|
| `AssertionError: null_pct in customer_id = 0.02` | Real nulls in data | Investigate upstream; fix data or add null-handling logic |
| `AssertionError: row_count = 0` | Upstream filter removed all rows | Pipeline logic bug — check JOIN conditions or filters |
| `AnalysisException` on column name | Column renamed or schema evolved | Update gate column name to match current schema |
| Gate passes but data is wrong | Threshold too loose | Tighten bounds using `customer-config.md → THRESHOLD_DEFAULTS` |
| PySpark version mismatch | API changed in PySpark 3.x | Check `pyspark.__version__`; adjust API calls |
