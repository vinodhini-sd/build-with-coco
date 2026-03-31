# AI / ML Engineer

> For: AI builders, Cortex power users, model trainers.
> `cortex-agent` spans 909 accounts. Fastest-growing category. Deep sessions avg 56–70 prompts.

---

## 1. Build a Cortex Agent with tools

```
Create a Cortex Agent that can answer questions about my business data. Give it
tools: a semantic view for metrics, a web search tool, and a SQL tool for ad-hoc
queries. Deploy it and test with 5 sample questions.
```

## 2. Build an AI functions pipeline

```
I have a table {{database}}.{{schema}}.{{table}} with text columns. For each row:
classify it into categories, extract sentiment, pull out entity mentions, and
summarize in 1 line. Store results in a Dynamic Table for continuous processing.
```

## 3. Train a churn prediction model

```
Find tables in my account with customer activity data (sessions, purchases,
support tickets). Build a feature engineering pipeline, train an XGBoost model
using Snowpark ML, register it in the Model Registry, and show me how to run
inference on new customers.
```

## 4. Set up a semantic view for Cortex Analyst

```
I want business users to ask natural language questions about my fact and dimension
tables. Create a semantic view with dimensions and metrics, add verified queries,
and test it with 10 representative business questions.
```

## 5. Build a document processing pipeline

```
I have PDFs in a Snowflake stage. Use AI_PARSE_DOCUMENT to extract text, then
run AI_EXTRACT to pull structured fields (invoice number, date, amount, vendor).
Store results in a table and build a simple review UI.
```

## 6. Create a RAG pipeline with Cortex Search

```
I have product documentation in a stage. Set up Cortex Search on the content,
then build a Cortex Agent that uses it as a knowledge base to answer product
questions. Test with 5 tricky questions from real user feedback.
```

## 7. Deploy a model to production

```
I have a trained model at {{/path/to/model.pkl}}. Log it into the Snowflake Model
Registry, set up a model endpoint, and build a Snowpark function that scores new
customers using it. Show me how to monitor inference latency.
```

## 8. Set up Feature Store for my ML pipeline

```
I have customer features spread across multiple tables. Create a Snowflake Feature
Store with feature views and entities. Show me how to materialize features and
generate training datasets with point-in-time correctness.
```

## 9. Build a multi-turn chatbot

```
Build a Streamlit chatbot that maintains conversation history, connects to Cortex
Complete, and uses my product FAQ data as context. Deploy it in Snowflake so my
team can use it.
```

## 10. Benchmark Cortex models for my use case

```
I have sample labeled records in {{database}}.{{schema}}.{{table}}. Test
AI_CLASSIFY with at least 3 different prompting strategies. Measure accuracy
against my ground truth. Show me which approach works best.
```

## 11. Set up continuous model monitoring

```
My model is deployed. Set up monitoring to track: prediction distribution drift
(PSI), feature drift for the top 10 features, and model performance against
actuals. Alert me when any metric exceeds threshold.
```

## 12. Build a multi-agent research workflow

```
Spawn a team of 3 agents: one searches my Snowflake data for patterns, one
searches the web for industry benchmarks, one synthesizes both and writes a
report. Use CoCo's multi-agent coordination to run them in parallel.
```

## 13. Create an AI-powered data catalog

```
Scan all tables in {{database}}.{{schema}}. For each table and column, use
AI_COMPLETE to generate a plain English description based on column names, sample
values, and relationships. Store results and build a searchable Streamlit catalog.
```

## 14. Build and evaluate a custom text classifier

```
I have labeled examples in {{database}}.{{schema}}.{{table}}. Use AI_CLASSIFY
to build a classifier for my custom taxonomy. Benchmark at least 3 different
category definitions and prompting strategies against my labeled ground truth,
report precision and recall for each, then deploy the best-performing
configuration as a reusable Snowpark UDF.
```

## 15. Build an agentic data pipeline debugger

```
Create a Cortex Agent that, given a failing task or pipeline name, autonomously
pulls task history, queries ACCOUNT_USAGE for errors, reads the relevant SQL,
diagnoses the issue, and proposes a fix. No human in the loop.
```
