# build-with-coco

A collection of reusable [Cortex Code](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code) skills and copy-paste prompts for automating data engineering workflows on Snowflake.

## Skills

| Skill | Description | Trigger Phrases |
|---|---|---|
| [dbt-model-generator](skills/dbt-model-generator/SKILL.md) | Auto-generate dbt dimensional models (star schema) from raw Snowflake tables | "generate dbt models", "shift left", "dimensional model", "star schema from raw" |
| [developer-voice](skills/developer-voice/SKILL.md) | Research real developer sentiment from Reddit and community forums, then synthesize into talk tracks, research briefs, or competitive intel grounded in practitioner quotes | "developer voice", "community pulse", "reddit research", "talk track", "what are developers saying", "pain points" |
| [know-your-data](skills/know-your-data/SKILL.md) | Discover data you already have access to in a Snowflake account, understand what it contains, and map it to your roles | "know your data", "know my data", "find data", "data discovery", "what can I access", "explore account" |
| [poc-builder](skills/poc-builder/SKILL.md) | Go from zero to a working POC with any Snowflake guide, blog post, doc link, or topic name. Deep-dives the content, extracts a demo spec, finds matching data in your account, and builds a working POC interactively | "poc builder", "build this", "zero to poc", "try this", "teach me", "walk me through", "prototype this", "run this guide" |

## Prompts

Copy-paste prompts organized by **what you're trying to accomplish**. Browse the full catalog in [`prompts/README.md`](prompts/README.md).

| Job to be Done | Prompts |
|---|---|
| **Connect sources** | [openflow-postgres-replication](prompts/connect-sources/openflow-postgres-replication.md), [iceberg-external-catalog](prompts/connect-sources/iceberg-external-catalog.md) |
| **Build pipelines** | [dbt-health-check-and-deploy](prompts/build-pipelines/dbt-health-check-and-deploy.md), [dynamic-table-pipeline](prompts/build-pipelines/dynamic-table-pipeline.md) |
| **Monitor quality** | [data-quality-monitoring](prompts/monitor-quality/data-quality-monitoring.md) |
| **Optimize costs** | [full-cost-governance-audit](prompts/optimize-costs/full-cost-governance-audit.md), [cost-optimization-sprint](prompts/optimize-costs/cost-optimization-sprint.md) |
| **Secure & govern** | [governance-hardening](prompts/secure-and-govern/governance-hardening.md), [network-security-lockdown](prompts/secure-and-govern/network-security-lockdown.md) |
| **Assess change impact** | [lineage-impact-analysis](prompts/assess-change-impact/lineage-impact-analysis.md), [migration-assessment](prompts/assess-change-impact/migration-assessment.md) |
| **Self-serve analytics** | [semantic-view-plus-agent](prompts/self-serve-analytics/semantic-view-plus-agent.md), [streamlit-sales-dashboard](prompts/self-serve-analytics/streamlit-sales-dashboard.md) |
| **AI enrichment** | [cortex-ai-ticket-enrichment](prompts/ai-enrichment/cortex-ai-ticket-enrichment.md), [ml-churn-prediction](prompts/ai-enrichment/ml-churn-prediction.md) |

## What Are Cortex Code Skills?

Skills are markdown-based workflow definitions that teach Cortex Code how to perform complex, multi-step tasks. They provide structured guidance, tool references, decision logic, and user checkpoints.

## Installation

### Quick install (everything)

```bash
./install.sh
```

### Skills only or prompts only

```bash
./install.sh skills    # skills only
./install.sh prompts   # prompts only
```

### Per-project install

```bash
./install.sh --project   # installs into .cortex/ in current directory
```

### Manual

Copy a skill or prompt directory into your global folder:

```bash
cp -r skills/dbt-model-generator ~/.snowflake/cortex/skills/dbt-model-generator
```

## Usage

Once installed, invoke a skill in Cortex Code with:

```
$dbt-model-generator
```

Or simply describe what you need — Cortex Code will match your request to the right skill based on trigger phrases.

For prompts, just paste them directly into Cortex Code CLI. See each prompt file for the copy-paste block and customization tips.

## dbt-model-generator

Automates the full "shift left" data modeling workflow:

1. **Discover** raw tables in a Snowflake database/schema
2. **Profile** column types, cardinality, relationships
3. **Classify** columns into facts, dimensions, and measures
4. **Generate** dbt models (staging, dimensions, facts) with surrogate keys
5. **Test** with schema.yml (unique, not_null, relationships, accepted_values)
6. **Validate** via `dbt parse`
7. **Submit** a GitHub PR with star schema diagram, profiling stats, and classification rationale

### Parameters

| Parameter | Required | Description |
|---|---|---|
| `SOURCE_DATABASE` | Yes | Snowflake database with raw tables |
| `SOURCE_SCHEMA` | Yes | Schema to scan (or `*` for all) |
| `SOURCE_TABLE` | No | Specific table (default: all in schema) |
| `GITHUB_REPO` | No | GitHub repo for PR (`owner/repo`) |
| `PROJECT_NAME` | No | dbt project name |
| `WAREHOUSE` | No | Snowflake warehouse (default: `COMPUTE_WH`) |
| `ROLE` | No | Snowflake role (default: `SYSADMIN`) |

## Contributing

To add a new skill:

1. Create a directory under `skills/<skill-name>/`
2. Add a `SKILL.md` following the [Cortex Code skill format](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code)
3. Update this README with the skill entry
4. Submit a PR
