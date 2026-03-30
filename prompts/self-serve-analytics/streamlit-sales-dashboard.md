# Build a Sales Dashboard in Streamlit

> Stand up a multi-page Streamlit in Snowflake app with KPIs, charts, and filters.

## The Prompt

```
Build me a Streamlit in Snowflake app for our sales team. It should have:
- A KPI header row (total revenue, deal count, avg deal size, win rate)
- A bar chart of revenue by region
- A line chart of monthly revenue trend
- Filters for date range, region, and product category
Use PROD.ANALYTICS.FACT_SALES as the data source. Make it look polished with proper
formatting and a clean layout.
```

## What This Triggers

- Streamlit skill (full app generation)
- Snowpark DataFrame queries for KPIs and charts
- Altair/Plotly chart generation
- Streamlit sidebar filter widgets
- Deployment to Snowflake (SiS)

## Before You Run

- Streamlit in Snowflake enabled on your account
- Source table with sales data (revenue, region, date, product columns)
- A warehouse for the Streamlit app to run on

## Tips

- Replace the table and column names with your actual schema
- Add "also add a drill-down page for individual deals" for a multi-page app
- Say "add a tab for sales rep leaderboard" to extend functionality
- Add "beautify it with custom CSS — dark theme, branded colors" for styling
