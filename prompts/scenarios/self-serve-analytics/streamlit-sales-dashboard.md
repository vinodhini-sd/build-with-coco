# Build a Sales Dashboard in Streamlit

> Stand up a multi-page Streamlit in Snowflake app with KPIs, charts, and filters.

## The Prompt

```
Build a Streamlit in Snowflake dashboard for my data. Ask me for the use case, source
table, and which KPIs, dimensions, and filters to include, then build a polished app with
metric cards and charts and deploy it.
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
