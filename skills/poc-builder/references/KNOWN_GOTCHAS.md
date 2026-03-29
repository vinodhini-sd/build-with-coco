# Known Gotchas by Feature

Feature-specific traps discovered through real POC builds. Check this before building — saves mid-build debugging.

---

## Dynamic Tables

- `TARGET_LAG` must be a quoted string: `TARGET_LAG = '10 MINUTES'` not `TARGET_LAG = 10`
- `DOWNSTREAM` lag means "refresh when upstream refreshes" — don't use it for root tables
- Dynamic tables can't reference other dynamic tables across databases
- `CREATE OR REPLACE DYNAMIC TABLE` drops change tracking history — the DT does a full refresh on the next cycle, which can be expensive on large sources. Use `ALTER DYNAMIC TABLE` to modify properties without reset when possible.
- `ALTER DYNAMIC TABLE ... REFRESH` forces an immediate refresh but doesn't change the schedule
- Initial refresh can be slow on large source tables — warn the user

## Cortex Agents

- Semantic views must exist before creating the agent — DDL order matters
- `CREATE OR REPLACE SEMANTIC VIEW` requires the base tables to be accessible under the current role
- `DATA_AGENT_RUN` (older API) and `CORTEX_AGENT` (newer API) both exist — check which one the account supports. Newer accounts use `CORTEX_AGENT`.
- `DATA_AGENT_RUN` / `CORTEX_AGENT` returns JSON — parse it, don't try to use it as a table directly
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
- Auto-refresh can silently fail if IAM permissions change — check `SHOW TABLES` with `TABLE_TYPE` filter or `INFORMATION_SCHEMA.TABLES` for refresh status (`SHOW ICEBERG TABLES` does not exist as a command)
- Parquet files must match the expected schema exactly — no implicit casting

## Tasks & Streams

- `SCHEDULE` and `AFTER` are mutually exclusive — a task is either root (scheduled) or child (triggered)
- `ALTER TASK ... RESUME` requires EXECUTE TASK privilege, not just ownership
- Streams: `SHOW_INITIAL_ROWS = TRUE` only works at creation time, can't be altered after
- Stream staleness: if a stream isn't consumed within 14 days (default), it goes stale and must be recreated
- Task trees: resume tasks bottom-up (children first, root last). Suspend top-down (root first, children last).
- `TASK_HISTORY()` in `INFORMATION_SCHEMA` only retains 7 days. For longer history, use `SNOWFLAKE.ACCOUNT_USAGE.TASK_HISTORY` (45-minute latency).

## Cortex AI Functions

- `AI_COMPLETE` model names are case-sensitive: `'llama3.1-70b'` not `'Llama3.1-70b'`
- `AI_CLASSIFY` and `AI_EXTRACT` return JSON — use `::STRING` or `GET_PATH()` to extract values
- Token limits vary by model — large text columns may need truncation
- `AI_EMBED` returns an ARRAY, not a VECTOR — use `::VECTOR(FLOAT, 1024)` to cast for similarity search
- Cortex functions consume credits per call — warn before running on large tables
- `AI_COMPLETE` options like `temperature`, `max_tokens` are silently ignored if the model doesn't support them — no error, just unexpected output

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
- Multi-cluster warehouses with `SCALING_POLICY = 'ECONOMY'` can queue DML unexpectedly — POC builds assume single-cluster behavior

## General

- Hyphens in object names cause SQL syntax errors — always use underscores
- `CREATE OR REPLACE` drops the old object first — use `CREATE IF NOT EXISTS` to preserve data
- `IDENTIFIER()` function is needed when using variables as object names in SQL
- Role hierarchy: ACCOUNTADMIN > SYSADMIN > custom roles — don't build POCs under ACCOUNTADMIN
- `USE ROLE` in a session doesn't persist across sessions — set role in each script/step
- `SHOW GRANTS TO USER` only shows directly granted roles, not inherited privileges from the role hierarchy — use `SHOW GRANTS TO ROLE <role>` for transitive privilege checking
