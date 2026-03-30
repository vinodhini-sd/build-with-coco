# Build a Natural Language Analytics Layer

> Create a semantic view and wire it to a Cortex Agent so users can ask questions in plain English.

## The Prompt

```
I want business users to query my data using plain English, no SQL. Ask me which table
to use and which dimensions and measures matter most, then create a semantic view and wire
a Cortex Agent to it. Test it with a few sample questions to verify it works.
```

## What This Triggers

- Semantic view skill (DDL generation + creation)
- Cortex Agent skill (agent creation wired to semantic view)
- VQR (Verified Query Representation) suggestion generation
- Sample question testing against the agent

## Before You Run

- Source table with the columns referenced (or adjust to your schema)
- Cortex Analyst enabled on your account
- A warehouse for agent inference

## Tips

- Replace the table, dimensions, and measures with your actual schema
- Add "also add 10 verified queries for common questions" for better accuracy
- Say "deploy the agent to a Streamlit app" to make it user-facing
