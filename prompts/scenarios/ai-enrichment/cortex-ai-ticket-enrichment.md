# Enrich Support Tickets with AI Classification and Extraction

> Use Cortex AI functions to auto-classify, extract entities, and score sentiment on tickets.

## The Prompt

```
Use Cortex AI functions to enrich the text data in {{database.schema.table}}. Ask me
which column contains the text and what categories or entities to extract, then classify,
extract entities, score sentiment, and summarize each row. Materialize the results as a
Dynamic Table so enrichments stay current as new data arrives.
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
- Say "classify into 3 categories: Billing, Technical, General" to seed CoCo with your taxonomy upfront
