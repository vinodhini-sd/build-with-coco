# Replicate Postgres into Snowflake with OpenFlow

> Set up CDC-based replication from a Postgres database into Snowflake using OpenFlow.

## The Prompt

```
Help me replicate tables from a Postgres database into Snowflake using OpenFlow with CDC
enabled. Ask me for the source connection details, which tables to replicate, and the
destination schema. Walk me through the setup and verify the initial load completes.
```

## What This Triggers

- OpenFlow connector deployment and configuration
- CDC (change data capture) setup for incremental sync
- Destination schema creation in Snowflake
- Initial load verification queries

## Before You Run

- OpenFlow must be enabled on your Snowflake account
- You'll need Postgres connection details (host, port, database, credentials)
- A destination database and schema (or CoCo will create one)
- ACCOUNTADMIN or equivalent role for connector setup

## Tips

- Replace the table names with your actual source tables
- If you don't need CDC, say "full load only" instead
- Add "schedule a refresh every 15 minutes" if you want automated sync
