# Developer Voice

Research what real developers are saying about any topic on Reddit and community forums, then synthesize it into a narrative artifact grounded in practitioner quotes.

## What It Does

1. Clarifies the research brief (topic, output format, angle, Snowflake tie-in)
2. Runs 6+ parallel web searches across Reddit, Hacker News, Stack Overflow, and blogs
3. Extracts pain points, requirements, failure modes, positive signals, and direct quotes
4. Builds a structured narrative in the chosen format
5. Generates a styled HTML report with color-coded sections and attributed quotes

## Input

| Parameter | Required | Description |
|-----------|----------|-------------|
| Topic | Yes | Feature, product, or concept to research (e.g., "Dynamic Tables", "Iceberg vs Delta") |
| Output format | No | `talk-track` (default), `research-brief`, or `competitive-intel` |
| Angle | No | Specific framing (e.g., "focus on cost concerns", "compare with Databricks") |
| Snowflake tie-in | No | Include how Snowflake addresses findings (default: yes) |

## Output

- **HTML report** — Styled document with color-coded sections (pain points, solutions, caveats, get-started) and attributed Reddit/community quotes. Saved to `~/{Topic_Slug}_Developer_Voice.html`

### Output Formats

| Format | Structure |
|--------|-----------|
| `talk-track` | 5-part story arc: Problems → Promise → Reality Check → Our Answer → Get Started |
| `research-brief` | Executive summary, pain points, requirements matrix, failure modes, sentiment |
| `competitive-intel` | Side-by-side sentiment comparison, where each wins, common complaints, gaps |

## Trigger Phrases

```
$developer-voice
```

Also activates on: "developer voice", "community pulse", "reddit research", "practitioner sentiment", "talk track", "field research", "what are developers saying", "pain points", "feature narrative"

## Requirements

- **Snowflake**: Active Cortex Code connection (for Snowflake tie-in features)
- **Internet access**: Web search and fetch for Reddit/community research

## Installation

**Global (all projects):**

```bash
cp -r skills/developer-voice ~/.snowflake/cortex/skills/developer-voice
```

**Per-project:**

```bash
mkdir -p .cortex/skills
cp -r skills/developer-voice .cortex/skills/developer-voice
```
