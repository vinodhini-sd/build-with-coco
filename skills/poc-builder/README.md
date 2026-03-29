# POC Builder

Go from zero to a working POC with any Snowflake guide, blog post, doc link, social post, GitHub repo, or topic name. Extracts a full demo spec, finds matching data in your account, and builds a working POC interactively.

## What It Does

1. **Ingest** — Fetches the source content, extracts a complete demo spec (workflow, architecture, steps, prerequisites)
2. **Research** — Cross-references bundled CoCo skills and current Snowflake docs to catch stale syntax
3. **Data & Environment** — Either searches your account for matching tables or generates synthetic data. You pick where to build.
4. **Build** — Executes steps interactively with cost awareness and adaptive pacing
5. **Verify & Document** — Runs structured verification, generates 3 artifacts, offers cleanup options

## Input

| Input Type | Example |
|------------|---------|
| Quickstart guide | `https://quickstarts.snowflake.com/guide/...` |
| Snowflake docs | `https://docs.snowflake.com/en/...` |
| Blog post | Engineering blog, dev.to, Medium article |
| Social post | LinkedIn or Twitter/X post showing a workflow |
| GitHub repo | Repository URL or README link |
| Topic name | "Dynamic Tables", "Cortex Agents", etc. |

## Output

Three artifacts saved to `./poc-[workflow-slug]/`:

1. **Build Summary** (`poc-[slug]-summary.md`) — What was built, architecture diagram, objects created, verification SQL, cleanup SQL, scaling notes
2. **Source Code** (`poc-[slug]/`) — All SQL and Python files organized by step
3. **CoCo Prompts** (`poc-[slug]-prompts.md`) — 3-5 short prompts teammates can paste to replicate or extend the POC

Also offers to draft internal (Slack/email) and external (LinkedIn) sharing blurbs.

## Trigger Phrases

```
$poc-builder
```

Also activates on: "poc builder", "build this", "build a poc", "zero to poc", "try this", "teach me", "walk me through", "prototype this", "implement this guide", "follow along", "run this guide"

## Requirements

- **Snowflake**: Active Cortex Code connection
- **Internet access**: For fetching source content and checking docs

## Installation

**Global (all projects):**

```bash
cp -r skills/poc-builder ~/.snowflake/cortex/skills/poc-builder
```

**Per-project:**

```bash
mkdir -p .cortex/skills
cp -r skills/poc-builder .cortex/skills/poc-builder
```
