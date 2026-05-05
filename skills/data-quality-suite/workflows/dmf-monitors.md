# Workflow: Snowflake DMF Monitors

Loaded when: data lives in Snowflake + continuous monitoring selected, OR Snowpark pipeline output tables need monitoring.

---

## Prerequisites

- Active Snowflake connection with `CREATE DATA METRIC FUNCTION` privilege (or ACCOUNTADMIN)
- Target table(s) must exist with data
- Warehouse available for DMF execution (check `customer-config.md → ORG_STANDARDS.snowflake.default_warehouse`)

---

## Steps

### Step 1: Discover Target Tables

```sql
-- If schema provided, list all tables
SHOW TABLES IN SCHEMA {{database}}.{{schema}};

-- Describe each target table before generating checks
DESCRIBE TABLE {{database}}.{{schema}}.{{table}};
```

Collect: column names, types, whether any DMFs are already attached.

Check existing DMFs:
```sql
SELECT
    ref_entity_name,
    metric_name,
    schedule,
    schedule_status
FROM information_schema.data_metric_function_references(
    ref_entity_name => '{{database}}.{{schema}}.{{table}}',
    ref_entity_domain => 'TABLE'
);
```

---

### Step 2: Profile Columns → Recommend DMFs

Classify every column by type and recommend DMFs:

| Column type | Recommended DMFs |
|---|---|
| PK / unique ID | `NULL_COUNT`, `DUPLICATE_COUNT` |
| FK / foreign key | `NULL_COUNT`, `REFERENTIAL_INTEGRITY_COUNT` |
| Numeric metric | `NULL_COUNT` + custom range bounds |
| Timestamp / date | `NULL_COUNT`, `FRESHNESS` |
| Categorical / status | `NULL_COUNT` + custom `ACCEPTED_VALUES` |
| Any column | `NULL_COUNT` (always) |
| Table-level | `ROW_COUNT` (always) |

Also check `customer-config.md → LAYER_STANDARDS` for the target layer's required checks.

---

### Step 3: Generate DDL

Load `templates/dmf_setup.sql` and replace placeholders with actual values.

Present the full DDL to the user:

```
I'll attach the following DMFs to {{database}}.{{schema}}.{{table}}:

  TABLE LEVEL:
  - ROW_COUNT — alert if drops >20% vs previous run
  - FRESHNESS — alert if no new rows within {{freshness_hours}} hours

  COLUMN LEVEL ({{col1}}):
  - NULL_COUNT — threshold: 0 nulls allowed
  - DUPLICATE_COUNT — threshold: 0 duplicates

  COLUMN LEVEL ({{col2}} — categorical):
  - NULL_COUNT — threshold: 0 nulls
  - Custom ACCEPTED_VALUES — values: [...]

Schedule: every 6 hours (CRON 0 */6 * * * America/Los_Angeles)

Proceed? (yes / adjust / skip columns)
```

**STOP — await user confirmation before executing any DDL.**

---

### Step 4: Execute DDL

After approval, run the DDL from `templates/dmf_setup.sql`. Execute in this order:
1. CREATE custom DMFs (if any)
2. ALTER TABLE to attach system DMFs
3. ALTER TABLE to attach custom DMFs

---

### Step 5: Verify Attachment

```sql
-- Confirm all DMFs are attached and scheduled
SELECT
    metric_name,
    schedule,
    schedule_status
FROM information_schema.data_metric_function_references(
    ref_entity_name => '{{database}}.{{schema}}.{{table}}',
    ref_entity_domain => 'TABLE'
);
```

Expected: all attached DMFs show `schedule_status = 'STARTED'`.

---

### Step 6: Query First Results

DMFs run on schedule. Show the user how to query results:

```sql
-- Check results after first run
SELECT
    measurement_time,
    metric_name,
    value
FROM TABLE(SNOWFLAKE.LOCAL.DATA_QUALITY_MONITORING_RESULTS(
    ref_entity_name => '{{database}}.{{schema}}.{{table}}',
    ref_entity_domain => 'TABLE'
))
ORDER BY measurement_time DESC
LIMIT 50;
```

Tell the user: "DMFs will run on their first scheduled trigger. Check back in ~6 hours, or force a manual trigger by running an `ALTER TABLE ... REFRESH` if your role allows it."

---

## Output

- Custom DMF definitions (if any) created in `{{dmf_schema}}`
- DMFs attached to target table(s) with schedule
- User shown results query to bookmark

---

## Error Handling

| Error | Cause | Fix |
|---|---|---|
| `Insufficient privileges` | Missing `CREATE DATA METRIC FUNCTION` privilege | Ask ACCOUNTADMIN to grant, or use ad-hoc assessment instead |
| `DMF already attached` | DMF exists from previous run | Check current config; ALTER TABLE to update schedule if needed |
| `Table not found` | Wrong database/schema/table name | SHOW TABLES to verify |
| `NO_RESULTS` from monitoring view | DMF hasn't run yet | Wait for first scheduled trigger (~6 hours) |
| `schedule_status = SUSPENDED` | Missing EXECUTE TASK privilege | Grant `EXECUTE MANAGED TASK` to the role |
