# Data Governance Lead

> For: Compliance officers, data stewards, security engineers.
> `data-governance` spans 2,927 accounts. Healthcare and Public Sector users go deepest on this use case.

---

## 1. Run a full PII classification scan

```
Run SYSTEM$CLASSIFY on all tables in {{database}}.{{schema}}. Show me which columns
are flagged as PII, QUASI_IDENTIFIER, or SENSITIVE. Group results by table and flag
any that don't have masking policies applied.
```

## 2. Apply masking policies to PII columns

```
I have columns flagged as PII (EMAIL, PHONE, SSN, DOB) across multiple tables.
Create masking policies that: show full data to admin roles, show masked data to
analyst roles, show NULL to all others. Apply them to each column.
```

## 3. Set up row access policies

```
My {{database}}.{{schema}}.{{table}} has a region or team column. Set up a row
access policy so each analyst role can only see rows for their own scope. Show me
how to map roles to values and apply the policy.
```

## 4. Audit who has access to what

```
Show me all roles that have SELECT access to tables in {{database}}.{{schema}}.
Flag any roles that have broader access than they should. Produce a report I can
share with my security team.
```

## 5. Review data quality compliance across my schema

```
Pull DMF results from SNOWFLAKE.LOCAL.DATA_QUALITY_MONITORING_RESULTS for all
tables in {{database}}.{{schema}}. Show me which tables are failing quality checks,
group violations by type (freshness, NULL rate, duplicates), and flag any that
affect PII-tagged or compliance-relevant tables. Summarize findings in a format
I can include in a compliance report.
```

## 6. Generate a governance maturity score

```
Evaluate my {{database}} database governance posture: classification coverage,
masking policy coverage, row access policy coverage, object tagging, and audit
logging. Score each dimension and tell me what to fix first.
```

## 7. Create a data lineage audit trail

```
For {{database}}.{{schema}}.{{table}}, trace: what feeds it (upstream), what reads
from it (downstream), who queried it in the last 30 days, and whether any
unmasked PII flows through the pipeline.
```

## 8. Lock down network access

```
Review my account's network policies. Flag any that allow 0.0.0.0/0, identify
service accounts without network policies, and generate the SQL to tighten
access to our corporate IP ranges.
```

## 9. Set up a Trust Center review

```
Run the Security Essentials scanner findings. Show me all critical and high-severity
issues, group them by category (MFA, network, privileges), and give me the
remediation SQL for each one.
```

## 10. Build a regulation-specific compliance report

```
I need a compliance readiness report mapped to {{regulation}} (e.g. GDPR, HIPAA,
PCI-DSS). Query ACCOUNT_USAGE to check PII masking coverage, audit log retention,
network policy enforcement, encryption status, and access reviews. Output findings
structured against the specific requirements of that regulation.
```

## 11. Set up tag-based masking at scale

```
I have many tables. Instead of applying masking policies column by column, set up
tag-based masking: tag any column SENSITIVITY=PII and have the masking policy apply
automatically via a tag-based policy. Walk me through the setup.
```

## 12. Create a data access request workflow

```
Build a Streamlit app where users can request access to sensitive datasets.
Requests get saved to a governance table, emailed to a data steward, and
approved/denied via the app. Approved access triggers a GRANT automatically.
```

## 13. Detect privilege escalation

```
Query ACCOUNT_USAGE.GRANTS_TO_ROLES to find any roles granted to PUBLIC,
any ACCOUNTADMIN grants from the past 30 days, and any roles with MANAGE GRANTS
privilege. Flag as a security risk report.
```

## 14. Set up column-level lineage for sensitive data

```
For columns tagged as PII in {{database}}, trace where they flow: which downstream
views, DTs, or exports include them. Flag any pipeline that moves PII outside
the source schema without masking applied.
```

## 15. Generate data contracts as documentation

```
For each table in {{database}}.{{schema}}, generate a YAML data contract: schema
definition, SLA (freshness, row count bounds), quality checks, owner, and
consumers. Use the actual table metadata and ACCOUNT_USAGE as source of truth.
Note: these are documentation artifacts — they describe expectations but are not
natively enforced by Snowflake. Use alongside DMFs and masking policies for enforcement.
```
