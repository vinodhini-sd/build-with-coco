# Find and Fix Cost Optimization Opportunities

> Identify over-provisioned warehouses, spilling queries, and missing clustering keys.

## The Prompt

```
Analyze my account's warehouse usage for the past 30 days. Find warehouses that are
over-provisioned (low avg utilization, including multi-cluster MAX_CLUSTERS settings),
queries that are spilling to remote storage, and tables that would benefit from clustering
keys or search optimization. For each finding, show me the exact ALTER or CREATE statement
to fix it, prioritized by estimated credit savings. Don't execute any changes — show me
the full plan first and wait for my approval before touching anything.
```

## What This Triggers

- Cost intelligence skill (credit consumption analysis)
- Workload performance analysis skill (spill detection, pruning efficiency)
- Clustering key and search optimization recommendations
- Ready-to-run SQL statements for each fix

## Before You Run

- ACCOUNTADMIN or role with access to ACCOUNT_USAGE and INFORMATION_SCHEMA
- At least 30 days of query history for meaningful analysis
- SYSADMIN or equivalent to execute the recommended ALTER statements

## Tips

- Replace "30 days" with a shorter window if you want a quick check
- Say "focus on my ANALYTICS_WH warehouse only" to narrow scope
