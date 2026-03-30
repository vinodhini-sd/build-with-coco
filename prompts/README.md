# Prompts

Copy-paste prompts for [Cortex Code](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code). Organized by **what you're trying to accomplish**, not by Snowflake feature.

## How to Use

Paste any prompt into Cortex Code CLI or desktop app. Adjust table/schema names to match your account. CoCo will ask for anything else it needs.

## Catalog

| Job to be Done | Prompt | What It Does |
|---|---|---|
| **Connect sources** | [openflow-postgres-replication](connect-sources/openflow-postgres-replication.md) | Replicate Postgres tables into Snowflake via OpenFlow with CDC |
| **Connect sources** | [iceberg-external-catalog](connect-sources/iceberg-external-catalog.md) | Query S3 data lake via Iceberg tables + AWS Glue catalog |
| **Build pipelines** | [dbt-health-check-and-deploy](build-pipelines/dbt-health-check-and-deploy.md) | Validate, test, and deploy a dbt project to Snowflake |
| **Build pipelines** | [dynamic-table-pipeline](build-pipelines/dynamic-table-pipeline.md) | Build a multi-layer dynamic table pipeline from raw events |
| **Monitor quality** | [data-quality-monitoring](monitor-quality/data-quality-monitoring.md) | Set up DMF-based data quality checks with anomaly detection |
| **Optimize costs** | [full-cost-governance-audit](optimize-costs/full-cost-governance-audit.md) | Audit top warehouse costs + unprotected tables + unclassified PII |
| **Optimize costs** | [cost-optimization-sprint](optimize-costs/cost-optimization-sprint.md) | Find over-provisioned warehouses, spilling queries, missing clustering |
| **Secure & govern** | [governance-hardening](secure-and-govern/governance-hardening.md) | Classify PII, apply masking policies, add row access, score maturity |
| **Secure & govern** | [network-security-lockdown](secure-and-govern/network-security-lockdown.md) | Audit network policies for overly permissive rules |
| **Assess change impact** | [lineage-impact-analysis](assess-change-impact/lineage-impact-analysis.md) | Trace downstream dependencies before a breaking schema change |
| **Assess change impact** | [migration-assessment](assess-change-impact/migration-assessment.md) | Assess Teradata-to-Snowflake migration complexity with SnowConvert |
| **Self-serve analytics** | [semantic-view-plus-agent](self-serve-analytics/semantic-view-plus-agent.md) | Create a semantic view + Cortex Agent for natural language queries |
| **Self-serve analytics** | [streamlit-sales-dashboard](self-serve-analytics/streamlit-sales-dashboard.md) | Build and deploy a Streamlit sales analytics dashboard |
| **AI enrichment** | [cortex-ai-ticket-enrichment](ai-enrichment/cortex-ai-ticket-enrichment.md) | Enrich support tickets with sentiment, classification, entities, summaries |
| **AI enrichment** | [ml-churn-prediction](ai-enrichment/ml-churn-prediction.md) | Build a churn prediction model with Snowpark ML + Model Registry |

## Prompt Format

Each prompt file has four sections:

- **The Prompt** — copy-paste ready, works as-is in CoCo
- **What This Triggers** — which CoCo skills and features get invoked
- **Before You Run** — prerequisites (tables, roles, access)
- **Tips** — how to customize for your account

## Contributing

1. Pick the job category that fits (or propose a new one)
2. Create a `.md` file following the format above
3. Add an entry to the catalog table in this README
4. Submit a PR
