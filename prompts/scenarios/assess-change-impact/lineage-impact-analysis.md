# Trace Downstream Impact Before a Schema Change

> Map all dependencies before changing a column type or dropping a table.

## The Prompt

```
Before I make a breaking schema change to {{database.schema.table}}, trace all downstream
dependencies — dynamic tables, views, dashboards, and apps that read from it. Tell me
exactly what would break and give me a migration plan. Don't make any changes yet.
```

## What This Triggers

- Lineage skill invocation
- ACCESS_HISTORY and OBJECT_DEPENDENCIES analysis
- Column-level downstream tracing
- Impact report (what breaks, what needs migration)
- Migration plan generation

## Before You Run

- ACCOUNTADMIN or role with access to ACCOUNT_USAGE.ACCESS_HISTORY
- Enterprise Edition (for column-level lineage)
- The table you're planning to modify must have query history

## Tips

- Replace the table/column with your actual planned change
- Works for any breaking change: column drops, type changes, table renames
- Add "also check if any Cortex Agents or semantic views reference this" for full coverage
- Lineage covers Snowflake-native objects only — views, dynamic tables, tasks, pipes. External BI tools (Tableau, Looker, Sigma) and dbt models won't appear in results
