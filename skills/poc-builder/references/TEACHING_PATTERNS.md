# Teaching Patterns Reference

Cheat sheet for the `poc-builder` skill. SQL snippets, code examples, and lookup tables. All behavioral rules live in SKILL.md — this file is supplementary detail only.

---

## Topic-Only Search Queries

When the user gives just a feature name, use these to find real workflow options:

```bash
# Search Snowflake tutorials
web_search "snowflake {topic} tutorial site:docs.snowflake.com"

# Search quickstarts
web_search "snowflake {topic} quickstart site:quickstarts.snowflake.com"

# Search developer guides
web_search "snowflake {topic} guide site:developers.snowflake.com"

# Check if there's a bundled CoCo skill
# (dynamic-tables, cortex-agent, iceberg, semantic-view, etc.)
```

---

## Account Discovery SQL

### Search for matching tables by keyword

```bash
# Preferred: semantic search via cortex CLI
cortex search object "<keyword>" --types=table,view

# Example: looking for IoT/sensor data
cortex search object "sensor" --types=table,view
cortex search object "iot" --types=table,view
cortex search object "readings" --types=table,view
```

### Search databases by domain

```sql
-- List all databases (scan names for relevance)
SHOW DATABASES;

-- Targeted search
SHOW DATABASES LIKE '%IOT%';
SHOW DATABASES LIKE '%SENSOR%';
SHOW DATABASES LIKE '%SALES%';
```

### Explore a candidate database

```sql
-- List schemas
SHOW SCHEMAS IN DATABASE <db>;

-- List tables in a schema
SHOW TABLES IN <db>.<schema>;

-- Quick shape check
DESCRIBE TABLE <db>.<schema>.<table>;

-- Row count
SELECT COUNT(*) FROM <db>.<schema>.<table>;

-- Sample rows
SELECT * FROM <db>.<schema>.<table> LIMIT 5;
```

### Check access with current role

```sql
-- Current identity
SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE();

-- All roles available
SHOW GRANTS TO USER IDENTIFIER(CURRENT_USER());

-- Try accessing with a specific role
USE ROLE <role>;
DESCRIBE TABLE <db>.<schema>.<table>;
```

### Find a usable warehouse

```sql
-- List warehouses the current role can use
SHOW WAREHOUSES;

-- If current warehouse is DQL-only (SELECT only), look for DDL-capable alternatives
-- Common patterns: COMPUTE_WH, SNOWHOUSE, <TEAM>_WH
```

---

## Guide Parsing Heuristics

### sfquickstarts format

```markdown
author: Author Name
id: guide-slug
summary: One-line summary
categories: Category1,Category2
environments: web
status: Published
feedback link: https://github.com/...
tags: Tag1, Tag2, Tag3
<!-- -->

## Overview
Duration: 5

Guide overview text...

<!-- -->

## Step Title
Duration: 15

Step content with code blocks...

<!-- -->

## Conclusion
Duration: 5

Summary and next steps...
```

**Key parsing rules:**
- Sections separated by `<!-- -->`
- Each section starts with `## Title` followed by `Duration: N`
- First chunk = metadata (frontmatter-style key:value pairs)
- Code blocks use standard markdown fencing
- Steps are sequential

### Extracting steps from a guide

1. Split content on `<!-- -->` delimiters
2. First chunk = metadata (extract title, summary, tags)
3. Each subsequent chunk = one step
4. For each step:
   - Title = first `## ` heading
   - Duration = `Duration: N` line (minutes)
   - Code blocks = all fenced code blocks (note the language)
   - Explanatory text = everything outside code blocks
   - Sub-steps = any `### ` headings within the step

### Extracting data requirements

Look for:
1. **CREATE TABLE statements** → column names, types, shape
2. **INSERT/COPY INTO statements** → sample data, file formats
3. **SELECT statements** → which columns are actually used
4. **External stage references** → data files in S3/GCS/Azure
5. **Variable references** → parameterized values (connection strings, keys)

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
