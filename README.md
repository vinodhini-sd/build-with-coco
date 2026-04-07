# build-with-coco

A collection of reusable [Cortex Code](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code) skills and copy-paste prompts for automating data engineering workflows on Snowflake.

## Skills

| Skill | Description | Trigger Phrases |
|---|---|---|
| [dbt-model-generator](skills/dbt-model-generator/SKILL.md) | Auto-generate dbt dimensional models (star schema) from raw Snowflake tables | "generate dbt models", "shift left", "dimensional model", "star schema from raw" |
| [developer-voice](skills/developer-voice/SKILL.md) | Research real developer sentiment from Reddit and community forums, then synthesize into talk tracks, research briefs, or competitive intel grounded in practitioner quotes | "developer voice", "community pulse", "reddit research", "talk track", "what are developers saying", "pain points" |
| [know-your-data](skills/know-your-data/SKILL.md) | Discover data you already have access to in a Snowflake account, understand what it contains, and map it to your roles | "know your data", "know my data", "find data", "data discovery", "what can I access", "explore account" |
| [poc-builder](skills/poc-builder/SKILL.md) | Go from zero to a working POC with any Snowflake guide, blog post, doc link, or topic name. Deep-dives the content, extracts a demo spec, finds matching data in your account, and builds a working POC interactively | "poc builder", "build this", "zero to poc", "try this", "teach me", "walk me through", "prototype this", "run this guide" |

## Recipes

Copy-paste prompts in two categories — browse by role or by scenario. Full catalog in [`recipes/README.md`](recipes/README.md).

**By role** (`recipes/by-role/`): [data-engineer](recipes/by-role/data-engineer/prompts.md), [analytics-engineer](recipes/by-role/analytics-engineer/prompts.md), [data-analyst](recipes/by-role/data-analyst/prompts.md), [ai-ml-engineer](recipes/by-role/ai-ml-engineer/prompts.md), [app-developer](recipes/by-role/app-developer/prompts.md), [data-governance-lead](recipes/by-role/data-governance-lead/prompts.md), [snowflake-admin](recipes/by-role/snowflake-admin/prompts.md)

| Scenario | Prompts |
|---|---|
| **Connect sources** | [openflow-postgres-replication](recipes/connect-sources/openflow-postgres-replication.md), [iceberg-external-catalog](recipes/connect-sources/iceberg-external-catalog.md) |
| **Build pipelines** | [dbt-health-check-and-deploy](recipes/build-pipelines/dbt-health-check-and-deploy.md), [dynamic-table-pipeline](recipes/build-pipelines/dynamic-table-pipeline.md) |
| **Monitor quality** | [data-quality-monitoring](recipes/monitor-quality/data-quality-monitoring.md) |
| **Optimize costs** | [full-cost-governance-audit](recipes/optimize-costs/full-cost-governance-audit.md), [cost-optimization-sprint](recipes/optimize-costs/cost-optimization-sprint.md) |
| **Secure & govern** | [governance-hardening](recipes/secure-and-govern/governance-hardening.md), [network-security-lockdown](recipes/secure-and-govern/network-security-lockdown.md) |
| **Assess change impact** | [lineage-impact-analysis](recipes/assess-change-impact/lineage-impact-analysis.md), [migration-assessment](recipes/assess-change-impact/migration-assessment.md) |
| **Self-serve analytics** | [semantic-view-plus-agent](recipes/self-serve-analytics/semantic-view-plus-agent.md), [streamlit-sales-dashboard](recipes/self-serve-analytics/streamlit-sales-dashboard.md) |
| **AI enrichment** | [cortex-ai-ticket-enrichment](recipes/ai-enrichment/cortex-ai-ticket-enrichment.md), [ml-churn-prediction](recipes/ai-enrichment/ml-churn-prediction.md) |

## Repo Structure

```
build-with-coco/
├── skills/
│   ├── dbt-model-generator/
│   │   ├── SKILL.md
│   │   ├── COMPASS.md           # 25–35 line navigation guide
│   │   └── references/
│   │       └── workflow.md
│   ├── developer-voice/
│   │   ├── SKILL.md
│   │   ├── COMPASS.md
│   │   └── references/
│   │       └── html-styling.md
│   ├── know-your-data/
│   │   ├── SKILL.md
│   │   └── COMPASS.md
│   ├── aws-glue-iceberg-setup/
│   │   ├── SKILL.md
│   │   ├── COMPASS.md
│   │   └── references/
│   └── poc-builder/
│       ├── SKILL.md
│       ├── COMPASS.md
│       └── references/
│           ├── ACCOUNT_DISCOVERY.md
│           ├── BUILD_SUMMARY_TEMPLATE.md
│           ├── GUIDE_PARSING.md
│           ├── KNOWN_GOTCHAS.md
│           └── TEACHING_PATTERNS.md
├── recipes/
│   ├── by-role/             # prompts organized by job role
│   ├── connect-sources/
│   ├── build-pipelines/
│   ├── monitor-quality/
│   ├── optimize-costs/
│   ├── secure-and-govern/
│   ├── assess-change-impact/
│   ├── self-serve-analytics/
│   ├── ai-enrichment/
│   └── README.md
├── docs/
│   └── COMPASS_GUIDE.md     # how to write COMPASS.md files
├── AGENTS.md                # agent contribution guide
├── install.sh
└── hooks/                   # session hooks (optional)
    ├── check-errors.py
    ├── session-start.sh
    ├── set-tab-title.sh
    ├── tab-title-helper.py
    ├── whats-new-helper.py
    └── README.md
```

## What Are Cortex Code Skills?

Skills are markdown-based workflow definitions that teach Cortex Code how to perform complex, multi-step tasks. They provide structured guidance, tool references, decision logic, and user checkpoints.

## Installation

### Quick install (everything)

```bash
./install.sh
```

### Skills only or recipes only

```bash
./install.sh skills    # skills only
./install.sh recipes   # recipes only
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

## Contributing

To add a new skill:

1. Create a directory under `skills/<skill-name>/`
2. Add a `SKILL.md` following the [Cortex Code skill format](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code)
3. Update this README with the skill entry
4. Submit a PR
