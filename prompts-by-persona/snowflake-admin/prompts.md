# Snowflake Admin / FinOps

> For: Account admins, platform ops, FinOps leads.
> `cost-intelligence` is the 2nd most widely adopted external skill by account breadth — 3,066 accounts.
> Short sessions (6–12 prompts) but high frequency and broad reach.

---

## 1. Show me my account's full credit spend this month

```
Break down my Snowflake credit consumption for the past 30 days: by warehouse,
by user, by query type (compute vs. serverless), and by feature (Cortex, Search,
Snowpipe). Flag anything that looks anomalous.
```

## 2. Find over-provisioned warehouses

```
Look at my warehouse utilization for the past 14 days. Identify any warehouses
where average utilization is below 20%, peak concurrency never exceeds 2,
or AUTO_SUSPEND is set too high. Give me the ALTER WAREHOUSE statements to right-size them.
```

## 3. Set up resource monitors and budget alerts

```
I want to alert when any single warehouse exceeds a daily credit threshold and when
total account spend exceeds 80% of my monthly budget. Create resource monitors
with appropriate triggers and suspend if we hit 100%.
```

## 4. Find my most expensive queries

```
Pull the top 20 most expensive queries by credit cost from the past 7 days.
For each one: show the warehouse, user, query text summary, and whether it could
be optimized with clustering, search optimization, or a query rewrite.
```

## 5. Set up a Snowflake integration

```
I need to connect Snowflake to [Kafka / S3 / Azure Event Hub / my notification service].
Walk me through creating the storage or notification integration, setting the correct
IAM policies, and verifying the connection works.
```

## 6. Audit my account's cost attribution

```
I have multiple teams sharing one Snowflake account. Show me how to attribute costs
per team using resource monitors, query tags, or custom tagging. Generate a
weekly cost allocation report by team.
```

## 7. Find serverless feature spend

```
Break down my serverless costs: Snowpipe, Tasks, Cortex AI functions, Cortex Search,
automatic clustering, materialized views. Show me which are growing month-over-month
and flag any that are unexpectedly high.
```

## 8. Review my account's security posture

```
Run a Trust Center scan on my account. Show me critical and high-severity findings,
group by category (MFA, network policies, privilege escalation), and give me
the exact SQL to remediate each one.
```

## 9. Optimize my storage costs

```
Show me tables consuming the most storage in my account. Flag tables with zero
or low query frequency in the past 60 days, tables with no clustering that could
benefit from compression, and Time Travel settings I can reduce.
```

## 10. Set up cross-account org reporting

```
I manage multiple Snowflake accounts in my org. Pull ORGANIZATION_USAGE data
to show total credits by account, month-over-month spend trend, and which
accounts are approaching their contracted limits.
```

## 11. Check for privilege drift

```
Audit GRANTS_TO_ROLES for any roles granted to PUBLIC, ACCOUNTADMIN grants
added in the last 30 days, and roles with CREATE USER or MANAGE GRANTS
privilege. Generate a cleanup script for anything that shouldn't be there.
```

## 12. Break down credit spend by team and project

```
Query ACCOUNT_USAGE.QUERY_HISTORY for the past 30 days. Group credits consumed
by warehouse, role, and user. Identify the top 5 cost drivers and show me
which queries are responsible — with query hash, avg execution time, and count.
```

## 13. Investigate a credit spike

```
My account used 3x more credits than usual recently. Diagnose why: pull query
history, warehouse events, task runs, and Snowpipe activity for that period.
Show me exactly what caused the spike.
```

## 14. Configure network policies for a new integration

```
I'm adding a new SaaS tool that needs to access Snowflake. Create a network
rule for its IP range, add it to our existing hybrid network policy, and
verify existing users aren't blocked. Show me how to test it safely.
```

## 15. Identify warehouse rightsizing opportunities

```
For every warehouse in my account, pull 30 days of WAREHOUSE_METERING_HISTORY
and QUERY_HISTORY. Calculate avg queue time, avg execution time, spill rate,
and idle time. Recommend size changes (up or down) with projected credit savings.
```
