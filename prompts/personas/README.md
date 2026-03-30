# Prompts by Persona

Copy-paste prompts for [Cortex Code](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code), organized by **who you are** — not by Snowflake feature.

Personas are derived from real CoCo usage data: profile names, skill patterns, session depth, and industry signals.

## Catalog

| Persona | File | Best Surface | Typical Session |
|---------|------|-------------|-----------------|
| **Data Analyst** | [data-analyst/prompts.md](data-analyst/prompts.md) | Snowsight UI | 2–5 prompts, quick SQL |
| **Analytics Engineer** | [analytics-engineer/prompts.md](analytics-engineer/prompts.md) | CLI | 8–15 prompts, dbt + DTs |
| **Data Engineer** | [data-engineer/prompts.md](data-engineer/prompts.md) | CLI | 10–20 prompts, pipelines |
| **AI / ML Engineer** | [ai-ml-engineer/prompts.md](ai-ml-engineer/prompts.md) | CLI + Desktop | 15–30 prompts, iterative build |
| **App Developer** | [app-developer/prompts.md](app-developer/prompts.md) | Desktop | 20–60 prompts, full app build |
| **Data Governance Lead** | [data-governance-lead/prompts.md](data-governance-lead/prompts.md) | Snowsight UI | 6–12 prompts, policy + audit |
| **Snowflake Admin / FinOps** | [snowflake-admin/prompts.md](snowflake-admin/prompts.md) | UI + CLI | 6–12 prompts, cost + infra |

## How to Use

1. Find your role above
2. Open the file — 15 prompts, each ready to copy-paste into CoCo
3. Replace `{{placeholders}}` with your actual table/schema/path names
4. CoCo will ask for anything else it needs
