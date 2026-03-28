# Known Gotchas by Feature

Feature-specific traps discovered through real POC builds. Check this before building — saves mid-build debugging.

---

## Dynamic Tables

- `TARGET_LAG` must be a quoted string: `TARGET_LAG = '10 MINUTES'` not `TARGET_LAG = 10`
- `DOWNSTREAM` lag means "refresh when upstream refreshes" — don't use it for root tables
- Dynamic tables can't reference other dynamic tables across databases
- `ALTER DYNAMIC TABLE ... REFRESH` forces an immediate refresh but doesn't change the schedule
- Initial refresh can be slow on large source tables — warn the user

## Cortex Agents

- Semantic views must exist before creating the agent — DDL order matters
- `CREATE OR REPLACE SEMANTIC VIEW` requires the base tables to be accessible under the current role
- `DATA_AGENT_RUN` returns JSON — parse it, don't try to use it as a table directly
- Agent tool definitions are case-sensitive for semantic view references
- Cortex Agent responses may vary between invocations — verification should check structure, not exact text

## Snowpipe Streaming

- Channel names are case-sensitive
- `ENABLE_SCHEMA_EVOLUTION` must be set on the target table before opening a channel
- Channels auto-close after 10 minutes of inactivity — reconnect logic needed for long-running producers
- The Java/Python SDK version must match the account's Snowpipe Streaming version
- Row insert order is not guaranteed across channels — use timestamps for ordering

## Iceberg Tables

- External volume must be created before the Iceberg table
- `ALLOW_WRITES = TRUE` on the external volume is required for managed Iceberg tables
- Catalog integration setup varies by provider (Glue, Polaris, REST) — check `iceberg` skill
- Auto-refresh can silently fail if IAM permissions change — check `SHOW ICEBERG TABLES` for refresh status
- Parquet files must match the expected schema exactly — no implicit casting

## Tasks & Streams

- `SCHEDULE` and `AFTER` are mutually exclusive — a task is either root (scheduled) or child (triggered)
- `ALTER TASK ... RESUME` requires EXECUTE TASK privilege, not just ownership
- Streams: `SHOW_INITIAL_ROWS = TRUE` only works at creation time, can't be altered after
- Stream staleness: if a stream isn't consumed within 14 days (default), it goes stale and must be recreated
- Task trees: resume tasks bottom-up (children first, root last). Suspend top-down (root first, children last).

## Cortex AI Functions

- `AI_COMPLETE` model names are case-sensitive: `'llama3.1-70b'` not `'Llama3.1-70b'`
- `AI_CLASSIFY` and `AI_EXTRACT` return JSON — use `::STRING` or `GET_PATH()` to extract values
- Token limits vary by model — large text columns may need truncation
- `AI_EMBED` returns an ARRAY, not a VECTOR — use `::VECTOR(FLOAT, 1024)` to cast for similarity search
- Cortex functions consume credits per call — warn before running on large tables

## Streamlit in Snowflake

- `SHOW` commands fail with `fetch_pandas_all()` — use `session.sql().collect()` and convert manually
- External browser auth doesn't work in apps — use `programmatic_access_token` authenticator
- Streamlit apps run under the app owner's role, not the viewer's role
- `st.experimental_*` functions get deprecated frequently — check current docs
- File uploads are limited to 200MB per file

## Stored Procedures (SQL)

- Variables and parameters need colon prefix inside SQL statements: `:my_var` not `my_var`
- Without the colon, Snowflake treats them as column identifiers → "invalid identifier" error
- This applies to DECLARE variables, LET variables, and procedure parameters
- `RESULTSET` must be accessed with `TABLE(resultset_name)` syntax

## Warehouses

- Some warehouses are DQL-only (SELECT only) — DDL/DML will fail with privilege errors
- Auto-resume warehouses consume credits when any query hits them — suspend for POCs
- `ALTER WAREHOUSE ... RESUME` may take a few seconds — don't immediately run queries after
- Warehouse size doesn't affect DDL speed — use XS for setup, scale up only for data processing

## General

- Hyphens in object names cause SQL syntax errors — always use underscores
- `CREATE OR REPLACE` drops the old object first — use `CREATE IF NOT EXISTS` to preserve data
- `IDENTIFIER()` function is needed when using variables as object names in SQL
- Role hierarchy: ACCOUNTADMIN > SYSADMIN > custom roles — don't build POCs under ACCOUNTADMIN
- `USE ROLE` in a session doesn't persist across sessions — set role in each script/step
