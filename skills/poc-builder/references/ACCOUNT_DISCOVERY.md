# Account Discovery Patterns

SQL snippets and CLI commands for finding matching data in a user's Snowflake account.

---

## Search for matching tables by keyword

```bash
# Preferred: semantic search via cortex CLI
cortex search object "<keyword>" --types=table,view

# Example: looking for IoT/sensor data
cortex search object "sensor" --types=table,view
cortex search object "iot" --types=table,view
cortex search object "readings" --types=table,view
```

## Search databases by domain

```sql
-- List all databases (scan names for relevance)
SHOW DATABASES;

-- Targeted search
SHOW DATABASES LIKE '%IOT%';
SHOW DATABASES LIKE '%SENSOR%';
SHOW DATABASES LIKE '%SALES%';
```

## Explore a candidate database

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

## Check access with current role

```sql
-- Current identity
SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE();

-- All roles available
SHOW GRANTS TO USER IDENTIFIER(CURRENT_USER());

-- Try accessing with a specific role
USE ROLE <role>;
DESCRIBE TABLE <db>.<schema>.<table>;
```

## Find a usable warehouse

```sql
-- List warehouses the current role can use
SHOW WAREHOUSES;

-- If current warehouse is DQL-only (SELECT only), look for DDL-capable alternatives
-- Common patterns: COMPUTE_WH, SNOWHOUSE, <TEAM>_WH
```

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
