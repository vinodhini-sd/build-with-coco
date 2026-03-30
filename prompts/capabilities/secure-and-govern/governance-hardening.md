# Harden Data Governance End-to-End

> Classify PII, apply masking policies, set up row access, and score governance maturity.

## The Prompt

```
Harden the governance posture of {{database.schema}}: classify all tables for sensitive
data, apply masking policies to any PII columns you find, and set up row access policies
for role-based filtering. Then generate a governance maturity score and show me what's
still missing. Do each step sequentially and verify before moving on.
```

## What This Triggers

- Data governance skill (full workflow)
- SYSTEM$CLASSIFY on all tables in target schema
- Dynamic masking policy creation and attachment
- Row access policy with role-based filtering
- Governance maturity score assessment

## Before You Run

- Snowflake Enterprise Edition or higher (classification + masking)
- ACCOUNTADMIN or SECURITYADMIN role
- Target database/schema with existing tables
- Understanding of which roles should see which data subsets

## Tips

- Replace `PROD.CORE` and `FACT_SALES` with your actual schema/tables
- Change "ANALYST role can only see their region" to your access pattern
- Add "also create tag-based masking for all EMAIL columns" for broader coverage
