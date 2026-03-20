# coco-skills-library

A collection of reusable [Cortex Code](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code) skills for automating data engineering workflows on Snowflake.

## Skills

| Skill | Description | Trigger Phrases |
|---|---|---|
| [dbt-model-generator](skills/dbt-model-generator/SKILL.md) | Auto-generate dbt dimensional models (star schema) from raw Snowflake tables | "generate dbt models", "shift left", "dimensional model", "star schema from raw" |
| [developer-voice](skills/developer-voice/SKILL.md) | Research real developer sentiment from Reddit and community forums, then synthesize into talk tracks, research briefs, or competitive intel grounded in practitioner quotes | "developer voice", "community pulse", "reddit research", "talk track", "what are developers saying", "pain points" |
| [know-your-data](skills/know-your-data/SKILL.md) | Discover data you already have access to in a Snowflake account, understand what it contains, and map it to your roles | "know your data", "know my data", "find data", "data discovery", "what can I access", "explore account" |

## What Are Cortex Code Skills?

Skills are markdown-based workflow definitions that teach Cortex Code how to perform complex, multi-step tasks. They provide structured guidance, tool references, decision logic, and user checkpoints.

## Installation

### Global (all projects)

Copy a skill directory into your global skills folder:

```bash
cp -r skills/dbt-model-generator ~/.snowflake/cortex/skills/dbt-model-generator
```

### Per-project

Copy into your project's `.cortex/skills/` directory:

```bash
mkdir -p .cortex/skills
cp -r skills/dbt-model-generator .cortex/skills/dbt-model-generator
```

## Usage

Once installed, invoke a skill in Cortex Code with:

```
$dbt-model-generator
```

Or simply describe what you need — Cortex Code will match your request to the right skill based on trigger phrases.

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
