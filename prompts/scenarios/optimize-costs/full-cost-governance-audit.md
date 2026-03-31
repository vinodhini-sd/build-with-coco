# Audit Account Costs, Governance Gaps, and Unclassified PII

> Run a parallel audit across cost, masking policies, and data classification in one shot.

## The Prompt

```
Run a full audit of my Snowflake account: find my top 10 most expensive warehouses by
credit consumption this month, check which tables have no masking or row access policies
applied, and identify unclassified PII columns in {{database}}.{{schema}} (scope the PII
scan to a specific database and schema — account-wide classification on large schemas can
take several minutes). Spawn parallel agents for each workstream and give me a combined
summary at the end.
```

## What This Triggers

- Cost intelligence skill (warehouse credit analysis)
- Data governance skill (policy coverage audit)
- Sensitive data classification skill (PII detection)
- Multi-agent team with parallel execution
- Combined summary report

## Before You Run

- ACCOUNTADMIN or a role with access to ACCOUNT_USAGE views
- Snowflake Enterprise Edition or higher (for classification features)
- At least one database with tables to audit

## Tips

- Add "include serverless costs too" to cover Cortex, tasks, and pipes
- Replace "this month" with "last 90 days" for a broader trend view
- Add "export findings to a Google Sheet" if you want a shareable artifact
