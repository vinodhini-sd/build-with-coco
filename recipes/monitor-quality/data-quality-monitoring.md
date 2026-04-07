# Set Up Data Quality Monitoring with DMFs

> Add automated data quality checks on a table using Snowflake Data Metric Functions.

## The Prompt

```
Set up automated data quality monitoring on {{database}}.{{schema}}.{{table}} using Snowflake
Data Metric Functions. Ask me which columns matter most and whether I want checks to run on a
cron schedule or trigger on DML events, then add monitors for row count anomalies,
NULL rates, freshness, and duplicates. Show me the DMF definitions and how to query the results.
```

## What This Triggers

- Data quality skill invocation
- Custom DMF creation (row count, NULL rate, freshness, duplicates)
- DMF attachment to the target table
- Results querying via SNOWFLAKE.LOCAL.DATA_QUALITY_MONITORING_RESULTS (DMF results API)

## Before You Run

- Target table must exist with known column names
- ACCOUNTADMIN or role with CREATE DATA METRIC FUNCTION privilege
- The table should have recent data for meaningful baseline metrics

## Tips

- Replace `{{database}}.{{schema}}.{{table}}` and column names with your table
- Add "set up a Snowflake Task to alert me via email when checks fail" for notifications
- Say "recommend what I should monitor" if you're unsure which checks to add
