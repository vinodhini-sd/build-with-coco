# Teaching Patterns Reference

Cheat sheet for the `poc-builder` skill. All behavioral rules live in SKILL.md — this file is supplementary detail only.

**See also:**
- `references/ACCOUNT_DISCOVERY.md` — Table search, role checking, warehouse finding
- `references/GUIDE_PARSING.md` — sfquickstarts format, extraction heuristics
- `references/KNOWN_GOTCHAS.md` — Feature-specific traps and workarounds

---

## Column Mapping Patterns

### Building a column map

```
Guide's expected schema          User's actual schema
──────────────────────          ────────────────────
CREATE TABLE sensor_data (       DESCRIBE TABLE iot_lab.sensors.readings;
  device_id VARCHAR,       →     DEVICE_NAME VARCHAR
  timestamp TIMESTAMP,     →     READING_TS TIMESTAMP_NTZ
  temperature FLOAT,       →     VALUE FLOAT (where SENSOR_TYPE='temperature')
  humidity FLOAT           →     VALUE FLOAT (where SENSOR_TYPE='humidity')
);
```

### Mapping strategies

| Scenario | Strategy |
|----------|----------|
| 1:1 column match | Direct substitution |
| Type mismatch | Add CAST() |
| Missing column | Constant or NULL, explain the gap |
| Extra columns | Ignore — only map what the workflow needs |
| Filtered subset | Add WHERE clause |
| Different granularity | GROUP BY or window functions |

### Presenting the mapping

Show as a table and ask for confirmation:

```
| Guide expects      | Your column        | Notes              |
|-------------------|--------------------|---------------------|
| device_id (STRING) | DEVICE_NAME (VARCHAR) | Direct match     |
| reading_ts (TIMESTAMP) | READING_TS (TIMESTAMP_NTZ) | Compatible |
| sensor_value (FLOAT) | VALUE (FLOAT)    | Direct match        |
```

---

## Environment Setup SQL

### SNOWFLAKE_LEARNING_DB check

```sql
SHOW DATABASES LIKE 'SNOWFLAKE_LEARNING_DB';
```

**If exists:**
```sql
USE DATABASE SNOWFLAKE_LEARNING_DB;
CREATE SCHEMA IF NOT EXISTS <workflow>_lab;
USE SCHEMA <workflow>_lab;
```

**If not (fallback):**
```sql
USE WAREHOUSE COMPUTE_WH;
CREATE DATABASE IF NOT EXISTS <workflow>_lab;
USE DATABASE <workflow>_lab;
CREATE SCHEMA IF NOT EXISTS <workflow>_lab;
USE SCHEMA <workflow>_lab;
```

### Warehouse: DDL vs DQL

Some warehouses are DQL-only. If DDL fails:
```
Error: Insufficient privileges to operate on warehouse 'SNOWADHOC'
```

Switch: `USE WAREHOUSE SNOWHOUSE;` (or COMPUTE_WH, or user's preferred WH)

---

## Adaptation Hints by Workflow Type

### Streaming (e.g., Snowpipe Streaming V2)
- Find tables with timestamp + value columns
- Adapt channel/pipe config to target user's table
- Map SDK's row schema to user's column schema

### Analytics (e.g., Cortex AI functions)
- Find tables with text columns (NLP) or numeric columns (ML)
- Adapt function calls to user's columns

### Pipeline (e.g., Dynamic Tables, Tasks)
- Find existing source tables
- Adapt transformations to user's schema
- Verify pipeline produces meaningful results on real data

### Agent (e.g., Cortex Agents)
- Find tables suitable for text-to-SQL
- Build semantic views over user's real tables
- Create agents that answer questions about their data

---

## Common Errors

| Error | Likely Cause | Recovery |
|-------|-------------|----------|
| `Object does not exist` | Skipped a previous step | Go back and run it |
| `Insufficient privileges` | Wrong role | Try higher-privilege role |
| `SQL compilation error` | Syntax issue | Check typos, missing commas |
| `Warehouse suspended` | Auto-suspended | `ALTER WAREHOUSE <wh> RESUME` |
| `Database/Schema does not exist` | Environment not set up | Run setup step |
| `Timeout` | Large dataset or complex query | Add LIMIT, optimize, increase timeout |

### When the guide's code doesn't work

1. Check if the guide is outdated
2. Fetch latest docs via `web_fetch` for the specific feature
3. Check bundled CoCo skill for correct syntax
4. Adapt to current syntax
5. Explain what changed and why
