# Build a Multi-Layer Dynamic Table Pipeline

> Create a chain of dynamic tables that parse, sessionize, and aggregate raw events.

## The Prompt

```
Build a multi-layer dynamic table pipeline on top of my raw events table. Ask me for the
source table and schema, then create a parsing layer, a sessionization layer, and a daily
aggregation layer with appropriate target lags. Verify each layer refreshes successfully
before building the next one.
```

## What This Triggers

- Dynamic tables skill invocation
- VARIANT flattening with LATERAL FLATTEN
- Session window logic (30-min gap detection)
- Aggregation pipeline with target lag configuration
- Sequential verification of each DT refresh

## Before You Run

- A raw events table with VARIANT column (or adjust column names)
- A warehouse for DT refresh compute
- CREATE DYNAMIC TABLE privileges on the target schema

## Tips

- Replace table/column names with your actual schema
- Adjust target lag values: "1 minute" for near-real-time, "downstream" for cost savings
- Add "include a DT for user-level lifetime metrics" to extend the pipeline
