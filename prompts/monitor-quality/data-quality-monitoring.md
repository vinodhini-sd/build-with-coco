# Set Up Data Quality Monitoring with DMFs

> Add automated data quality checks on a table using Snowflake Data Metric Functions.

## The Prompt

```
Set up data quality monitoring on PROD.CORE.FACT_SALES using Snowflake Data Metric Functions.
Add checks for: row count anomalies (compare to 7-day avg), NULL rates on REVENUE and
CUSTOMER_ID columns, freshness (alert if no new rows in 2 hours), and duplicate detection
on TRANSACTION_ID. Show me the DMF definitions and how to query results.
```

## What This Triggers

- Data quality skill invocation
- Custom DMF creation (row count, NULL rate, freshness, duplicates)
- DMF attachment to the target table
- Results querying via DATA_QUALITY_MONITORING_RESULTS view

## Before You Run

- Target table must exist with known column names
- ACCOUNTADMIN or role with CREATE DATA METRIC FUNCTION privilege
- The table should have recent data for meaningful baseline metrics

## Tips

- Replace `PROD.CORE.FACT_SALES` and column names with your table
- Add "set up a Snowflake Task to alert me via email when checks fail" for notifications
- Say "recommend what I should monitor" if you're unsure which checks to add
