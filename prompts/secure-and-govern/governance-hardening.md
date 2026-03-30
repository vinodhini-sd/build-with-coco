# Harden Data Governance End-to-End

> Classify PII, apply masking policies, set up row access, and score governance maturity.

## The Prompt

```
Harden the governance posture of my PROD database:
1. Run sensitive data classification on all tables in PROD.CORE
2. For any columns classified as PII, create and apply masking policies
3. Set up row access policies on FACT_SALES so the ANALYST role can only see their region
4. Generate a governance maturity score and show me what's still missing
Use the data-governance skill and do each step sequentially — verify before moving on.
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
