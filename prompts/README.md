# Prompts

Copy-paste prompts for [Cortex Code](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code). Two ways to browse: by **role** (who you are) or by **scenario** (what you're trying to do).

## How to Use

Paste any prompt into Cortex Code CLI or desktop app. CoCo will ask for the specifics it needs — table names, schemas, configs.

## By Role

| Role | File |
|---|---|
| Data Engineer | [roles/data-engineer/prompts.md](roles/data-engineer/prompts.md) |
| Analytics Engineer | [roles/analytics-engineer/prompts.md](roles/analytics-engineer/prompts.md) |
| Data Analyst | [roles/data-analyst/prompts.md](roles/data-analyst/prompts.md) |
| AI / ML Engineer | [roles/ai-ml-engineer/prompts.md](roles/ai-ml-engineer/prompts.md) |
| App Developer | [roles/app-developer/prompts.md](roles/app-developer/prompts.md) |
| Data Governance Lead | [roles/data-governance-lead/prompts.md](roles/data-governance-lead/prompts.md) |
| Snowflake Admin | [roles/snowflake-admin/prompts.md](roles/snowflake-admin/prompts.md) |

## By Scenario

| Scenario | Prompt | What It Does |
|---|---|---|
| **Connect sources** | [openflow-postgres-replication](scenarios/connect-sources/openflow-postgres-replication.md) | Replicate Postgres tables into Snowflake via OpenFlow with CDC |
| **Connect sources** | [iceberg-external-catalog](scenarios/connect-sources/iceberg-external-catalog.md) | Query S3 data lake via Iceberg tables + AWS Glue catalog |
| **Build pipelines** | [dbt-health-check-and-deploy](scenarios/build-pipelines/dbt-health-check-and-deploy.md) | Validate, test, and deploy a dbt project to Snowflake |
| **Build pipelines** | [dynamic-table-pipeline](scenarios/build-pipelines/dynamic-table-pipeline.md) | Build a multi-layer dynamic table pipeline from raw events |
| **Monitor quality** | [data-quality-monitoring](scenarios/monitor-quality/data-quality-monitoring.md) | Set up DMF-based data quality checks with anomaly detection |
| **Optimize costs** | [full-cost-governance-audit](scenarios/optimize-costs/full-cost-governance-audit.md) | Audit top warehouse costs + unprotected tables + unclassified PII |
| **Optimize costs** | [cost-optimization-sprint](scenarios/optimize-costs/cost-optimization-sprint.md) | Find over-provisioned warehouses, spilling queries, missing clustering |
| **Secure & govern** | [governance-hardening](scenarios/secure-and-govern/governance-hardening.md) | Classify PII, apply masking policies, add row access, score maturity |
| **Secure & govern** | [network-security-lockdown](scenarios/secure-and-govern/network-security-lockdown.md) | Audit network policies for overly permissive rules |
| **Assess change impact** | [lineage-impact-analysis](scenarios/assess-change-impact/lineage-impact-analysis.md) | Trace downstream dependencies before a breaking schema change |
| **Assess change impact** | [migration-assessment](scenarios/assess-change-impact/migration-assessment.md) | Assess Teradata-to-Snowflake migration complexity with SnowConvert |
| **Self-serve analytics** | [semantic-view-plus-agent](scenarios/self-serve-analytics/semantic-view-plus-agent.md) | Create a semantic view + Cortex Agent for natural language queries |
| **Self-serve analytics** | [streamlit-sales-dashboard](scenarios/self-serve-analytics/streamlit-sales-dashboard.md) | Build and deploy a Streamlit sales analytics dashboard |
| **AI enrichment** | [cortex-ai-ticket-enrichment](scenarios/ai-enrichment/cortex-ai-ticket-enrichment.md) | Enrich support tickets with sentiment, classification, entities, summaries |
| **AI enrichment** | [ml-churn-prediction](scenarios/ai-enrichment/ml-churn-prediction.md) | Build a churn prediction model with Snowpark ML + Model Registry |

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
