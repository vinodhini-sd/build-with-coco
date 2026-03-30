# App Developer (Streamlit / React / SPCS)

> For: Dashboard builders, internal tool developers, product engineers.
> `developing-with-streamlit` = 8,959 sessions across 1,012 accounts. Heaviest edit/write tool users.

---

## 1. Build a Streamlit app from scratch

```
Build a Streamlit app connected to {{database}}.{{schema}}.{{table}} with:
KPI cards, a time series chart of daily metrics, and a filterable data table.
Deploy it to Snowflake.
```

## 2. Debug why my Streamlit app is crashing

```
My app at {{/path/to/app.py}} keeps crashing with this error: [paste error].
Read the file, diagnose the issue, fix it, and run it locally to confirm it works.
```

## 3. Add authentication and role-based filtering

```
My Streamlit app shows all data. Update it to detect the logged-in user's
Snowflake role and filter the data accordingly — restricted roles see their
scope only, admin role sees everything.
```

## 4. Build a form-based data entry app

```
I need a Streamlit app where users can submit new records. It should validate
inputs (required fields, email format, date ranges), insert into
{{database}}.{{schema}}.{{table}}, and show a confirmation receipt.
```

## 5. Convert a Streamlit app to a React app

```
My Streamlit app at {{/path/to/app/}} is getting too slow with large datasets.
Rebuild it as a React + TypeScript app that calls Snowflake SQL API for data.
Generate the full project structure.
```

## 6. Deploy a containerized app to SPCS

```
I have a FastAPI app in {{/path/to/app/}} with a Dockerfile. Build the image, push
it to the Snowflake image registry, create the compute pool and service, and
verify it's running. Show me the endpoint URL.
```

## 7. Add caching to my slow Streamlit app

```
My app runs a heavy SQL query every time the page loads. Add st.cache_data
with a 15-minute TTL, add a manual refresh button, and show the cache age
in the UI so users know when data was last updated.
```

## 8. Build a multi-page Streamlit app

```
Extend my app to have 3 pages: Overview (KPIs), Drilldown (filterable table),
and Settings (user preferences saved to a Snowflake table). Use st.navigation
for routing and keep state across pages.
```

## 9. Build a Notebook-based analysis workflow

```
Create a Snowflake Notebook that: loads data from {{database}}.{{schema}}, does
exploratory analysis with pandas and Altair charts, trains a simple model,
and outputs predictions to a new table. Make it self-contained and shareable.
```

## 10. Create an admin dashboard for my pipeline

```
Build a Streamlit app that shows Snowflake Task history, success/failure rates,
last run time, and row deltas per table. Pull from ACCOUNT_USAGE.TASK_HISTORY
and my own pipeline metadata. Add a button to manually trigger a task.
```

## 11. Add AI features to an existing app

```
My app at {{/path/to/app/}} shows records from a support table. Add:
- Sentiment badge on each record (using AI_SENTIMENT)
- Auto-summary on detail page (using AI_SUMMARIZE)
- Smart search using vector similarity (using EMBED_TEXT)
```

## 12. Fix a Streamlit SHOW command error

```
My app uses session.sql("SHOW WAREHOUSES").fetch_pandas_all() and it's failing.
Fix it to use the correct pattern for SHOW commands in Streamlit and verify it works.
```

## 13. Build a data approval workflow

```
I need a Streamlit app where data stewards can review AI-generated classifications,
approve or reject each one, and the decisions get written back to a review table.
Include bulk approve/reject.
```

## 14. Run my app and fix what's broken

```
My Streamlit app at {{/path/to/app.py}} has issues I can't easily spot in code.
Open it in a browser, screenshot what it looks like, identify anything broken or
wrong visually, fix the code, and reload to confirm.
```

## 15. Build a chatbot UI in Streamlit

```
Create a Streamlit chat interface (using st.chat_message) that sends user messages
to a Cortex Agent, streams the response back in real time, and maintains a
conversation history across the session.
```
