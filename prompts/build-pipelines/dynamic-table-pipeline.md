# Build a Multi-Layer Dynamic Table Pipeline

> Create a chain of dynamic tables that parse, sessionize, and aggregate raw events.

## The Prompt

```
I have a raw table ANALYTICS.RAW.EVENTS with columns EVENT_ID, USER_ID, EVENT_TYPE,
EVENT_DATA (variant), CREATED_AT. Build me a dynamic table pipeline:
- DT_EVENTS_PARSED: flatten EVENT_DATA into typed columns
- DT_USER_SESSIONS: sessionize events per user (30-min gap)
- DT_DAILY_METRICS: daily aggregate of sessions, events, unique users
Set target lag to 1 minute for parsed, 5 minutes for sessions, downstream for metrics.
Verify each DT refreshes successfully before creating the next one.
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
