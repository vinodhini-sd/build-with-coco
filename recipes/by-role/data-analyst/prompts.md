# Data Analyst

> For: BI analysts, SQL power users, business intelligence engineers.
> Highest account breadth in usage data — cost-intelligence alone spans 3,066 external accounts.

---

## 1. Explain this query and make it faster

```
Analyze the SQL in my clipboard, explain what it does, identify any performance
issues (missing filters, Cartesian joins, repeated subqueries), and rewrite it
to be more efficient. Show me the execution plan differences.
```

## 2. Find my top spend drivers this month

```
Query my account's warehouse credit usage for the past 30 days. Show me the top
10 warehouses by credits, the top 10 most expensive queries, and flag any queries
that are spilling to remote storage.
```

## 3. Build a dashboard on my data

```
I have tables in {{database}}.{{schema}}. Explore what's there and build me a
Streamlit dashboard with KPI cards, a trend chart, and a filterable data table.
Connect it to my Snowflake account automatically.
```

## 4. Profile a table I'm about to use

```
Profile the table {{database}}.{{schema}}.{{table}} — show me row count, column
cardinality, NULL rates, min/max/avg on numeric columns, and flag any data quality
issues I should know about before doing analysis on it.
```

## 5. Write me a complex SQL report

```
I need a cohort retention report: for each week's new user cohort, show me what %
returned in weeks 1, 2, 4, and 8. My events table is {{database}}.{{schema}}.{{table}}
with USER_ID, EVENT_TYPE, and CREATED_AT columns. Write and run it.
```

## 6. Explain what a query is costing me

```
I ran query ID {{query_id}} recently. Pull the query history, show me how many
credits it consumed, how long it ran, and whether I could optimize it with
clustering or search optimization.
```

## 7. Compare two time periods

```
Compare metrics between two time periods from my {{database}}.{{schema}}.{{table}}.
Show period-over-period change, which segments drove the difference, and any anomalies.
```

## 8. Detect anomalies in my data

```
Look at daily row counts in {{database}}.{{schema}}.{{table}} for the last 90 days.
Flag any days where volume was more than 2 standard deviations from the rolling
7-day average. Show me a chart.
```

## 9. Auto-generate a metrics glossary

```
Scan the tables in {{database}}.{{schema}} and extract all columns that look like
metrics (numeric, named revenue/count/rate/amount/total). For each one, write a
plain English definition I can add to my data catalog.
```

## 10. Optimize my most-used warehouse

```
Look at query performance on my {{warehouse}} warehouse for the past 14 days.
Identify if it's over-provisioned, what the peak concurrency looks like, and
whether I should resize or use auto-scaling.
```

## 11. Find unused tables

```
Query ACCOUNT_USAGE to find tables in {{database}} that haven't been read in the
past 60 days. Show me by schema, sorted by storage size.
```

## 12. Write a parameterized report procedure

```
I run the same report every week but change the date range manually. Turn it into
a stored procedure that takes START_DATE and END_DATE as parameters and returns
the result as a formatted table.
```

## 13. Explain a join I'm getting wrong

```
I'm joining two tables and getting duplicate rows. I'll share my SQL in the next
message. Explain exactly why duplicates are happening and fix it.
```

## 14. Set up automated freshness alerts

```
I need an alert if {{database}}.{{schema}}.{{table}} hasn't received new rows in
the past 2 hours. Set up a Data Metric Function for freshness and show me how to
wire it to a Snowflake alert that emails me.
```

## 15. Convert a spreadsheet into a Snowflake query

```
I have an Excel model I want to recreate as a SQL query. Ask me to describe the
columns, calculations, and logic in the spreadsheet, then help me identify which
Snowflake tables to join and write the full query.
```
