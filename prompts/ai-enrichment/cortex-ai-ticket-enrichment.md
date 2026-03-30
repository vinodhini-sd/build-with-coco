# Enrich Support Tickets with AI Classification and Extraction

> Use Cortex AI functions to auto-classify, extract entities, and score sentiment on tickets.

## The Prompt

```
I have a support ticket table at PROD.SUPPORT.RAW_TICKETS with columns (ticket_id,
subject, body, created_at). Use Cortex AI functions to:
1. Classify each ticket into categories (billing, bug, feature_request, how_to, outage)
2. Extract key entities (product_name, error_code, customer_tier)
3. Score sentiment (-1 to 1)
4. Summarize each ticket into a one-liner
Create a Dynamic Table that materializes all enrichments so they stay current as new
tickets arrive.
```

## What This Triggers

- Cortex AI functions skill (CLASSIFY, EXTRACT, SENTIMENT, SUMMARIZE)
- Dynamic Table creation with AI function calls
- Automatic refresh as source data changes
- Enriched output table with all AI columns

## Before You Run

- Cortex AI functions enabled on your account
- Source table with text data (tickets, reviews, feedback — any unstructured text)
- A warehouse with Cortex access

## Tips

- Replace the table, columns, and categories with your actual data
- Works for any text enrichment: customer reviews, chat logs, emails
- Add "also create a Streamlit dashboard showing ticket volume by category" for visualization
- Say "use mistral-large for classification" to specify a model
