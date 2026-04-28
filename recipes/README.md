# Recipes

Copy-paste prompts for [Cortex Code](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code). Two ways to browse: by **role** (who you are) or by **scenario** (what you're trying to do).

## How to Use

Paste any prompt into Cortex Code CLI or desktop app. CoCo will ask for the specifics it needs — table names, schemas, configs.

## By Role

| Role | File |
|---|---|
| Data Engineer | [by-role/data-engineer/prompts.md](by-role/data-engineer/prompts.md) |
| Analytics Engineer | [by-role/analytics-engineer/prompts.md](by-role/analytics-engineer/prompts.md) |
| Data Analyst | [by-role/data-analyst/prompts.md](by-role/data-analyst/prompts.md) |
| AI / ML Engineer | [by-role/ai-ml-engineer/prompts.md](by-role/ai-ml-engineer/prompts.md) |
| App Developer | [by-role/app-developer/prompts.md](by-role/app-developer/prompts.md) |
| Data Governance Lead | [by-role/data-governance-lead/prompts.md](by-role/data-governance-lead/prompts.md) |
| Snowflake Admin | [by-role/snowflake-admin/prompts.md](by-role/snowflake-admin/prompts.md) |

## By Scenario

| Scenario | Prompt | What It Does |
|---|---|---|
| **Connect sources** | [openflow-postgres-replication](connect-sources/openflow-postgres-replication.md) | Replicate Postgres tables into Snowflake via OpenFlow with CDC |
| **Connect sources** | [iceberg-external-catalog](connect-sources/iceberg-external-catalog.md) | Query S3 data lake via Iceberg tables + AWS Glue catalog |
| **Build pipelines** | [dbt-health-check-and-deploy](build-pipelines/dbt-health-check-and-deploy.md) | Validate, test, and deploy a dbt project to Snowflake |
| **Build pipelines** | [dynamic-table-pipeline](build-pipelines/dynamic-table-pipeline.md) | Build a multi-layer dynamic table pipeline from raw events |
| **Monitor quality** | [data-quality-monitoring](monitor-quality/data-quality-monitoring.md) | Set up DMF-based data quality checks with anomaly detection |
| **Monitor quality** | [data-quality-suite-setup](monitor-quality/data-quality-suite-setup.md) | Configure a multi-framework DQ suite across DMFs, dbt, GX, Soda, Snowpark, and PySpark |
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
