---
name: developer-voice
description: "Research what real developers are saying about a topic on Reddit and community forums, then synthesize into a narrative talk track or content brief grounded in practitioner quotes. Use when: building talk tracks, researching community sentiment, preparing for a talk or blog, competitive analysis, understanding developer pain points, creating feature narratives. Triggers: developer voice, community pulse, reddit research, practitioner sentiment, talk track, field research, community intel, what are developers saying, pain points, feature narrative."
tools: ["Bash", "Read", "Write", "WebFetch", "web_search", "ask_user_question"]
---

# Developer Voice

Research real developer sentiment from Reddit and community forums on any topic, then synthesize it into a structured narrative artifact (talk track, content brief, or research report) grounded in actual practitioner quotes.

## When to Use

- Before writing a blog post, talk, or demo -- understand the existing conversation
- Building a talk track for a conference session or webinar
- Competitive intelligence: what are devs saying about X vs Y?
- Feature launch prep: understand objections before they come up
- Product feedback: surface real pain points for PM/engineering
- Sales enablement: build objection-handling docs with real quotes

## Workflow

### Step 1: Clarify the Research Brief

Ask the user these questions (use AskUserQuestion tool):

1. **Topic**: What feature, product, or concept to research? (e.g., "Snowflake Dynamic Tables", "Iceberg vs Delta", "streaming in the warehouse")
2. **Output format**: What artifact do they want?
   - `talk-track` -- A narrative with story arc: problems → promise → reality check → our answer → get started (DEFAULT)
   - `research-brief` -- Structured findings: pain points, requirements, sentiment, quotes
   - `competitive-intel` -- Side-by-side comparison of community sentiment on competing approaches
3. **Angle** (optional): Any specific framing? (e.g., "focus on cost concerns", "compare with Databricks", "emphasis on getting started")
4. **Snowflake tie-in**: Should the narrative include how Snowflake addresses the findings? (default: yes)

If the user already provided the topic inline (e.g., `$developer-voice Dynamic Tables`), skip asking for the topic and just confirm the output format.

### Step 2: Research -- Cast a Wide Net

Run **at least 6 parallel web searches** to cover different angles. Use `web_search` with queries like:

```
site:reddit.com {topic} problems issues challenges data engineering
site:reddit.com {topic} experience review production
site:reddit.com {topic} vs alternative comparison
site:reddit.com {topic} getting started migration
site:reddit.com {topic} cost performance benchmark
site:reddit.com {topic} Snowflake experience
```

Also search without `site:reddit.com` for broader coverage (Hacker News, Stack Overflow, blog posts with comments).

**IMPORTANT**: Run searches in parallel (batch all web_search calls in one message) for speed.

### Step 3: Extract & Categorize

Read through all results and extract into these buckets:

1. **Pain Points** -- What problems are people experiencing? What's broken?
2. **Requirements** -- What do teams actually need? What are they looking for?
3. **Failure Modes** -- Where are teams failing? What goes wrong?
4. **What's Working** -- Positive experiences, benchmarks, success stories
5. **Quotes** -- Save the best 8-12 direct quotes with attribution (subreddit, role if mentioned)
6. **Sentiment** -- Overall community temperature: positive, mixed, negative, skeptical?

### Step 4: Build the Narrative

Structure depends on the chosen output format:

#### For `talk-track` (default):

Follow this 5-part story arc:

**Part 1: The Problems Today**
- Lead with empathy. Describe the pain points using the community's own language.
- Include 2-3 Reddit quotes that capture the frustration.
- End with a summary box of core pain points.

**Part 2: How {Topic/Approach} Helps**
- Explain what the technology/approach is in plain terms (no marketing).
- Map it directly to the pain points from Part 1.
- Include community quotes showing where it works.

**Part 3: The Reality Check (Honest Caveats)**
- This is the credibility section. Don't hide downsides.
- Surface the complaints, limitations, and gotchas from the community.
- Include quotes from skeptics and people who hit problems.
- Frame as "eyes wide open" -- acknowledging tradeoffs builds trust.

**Part 4: How Snowflake Addresses This** (if Snowflake tie-in = yes)
- Map each problem/caveat from Part 3 to a specific Snowflake capability.
- Include performance benchmarks or cost comparisons if found.
- Use a comparison grid (DIY vs Snowflake) when applicable.
- Keep it factual, not salesy. Let the architecture speak.

**Part 5: How to Get Started**
- 4-6 concrete steps, starting small (one table, one POC).
- Include sample SQL or commands where applicable.
- End with a key message summary.

#### For `research-brief`:

Use a structured report format:
- Executive Summary (3-4 sentences)
- Pain Points (bulleted, with quotes)
- Requirements Matrix (table: requirement × frequency)
- Failure Modes (bulleted, with quotes)
- Positive Signals (bulleted, with quotes)
- Sentiment Summary
- Implications for Our Messaging
- Sources

#### For `competitive-intel`:

Use a comparison format:
- Market Context
- Side-by-side sentiment table (Product A vs Product B)
- Where A Wins (with quotes)
- Where B Wins (with quotes)
- Common Complaints About Both
- Opportunities / Gaps
- Sources

### Step 5: Generate the Artifact

Create an HTML file with clean, professional styling:

- Use color-coded callout boxes for different sections (problems = red-tint, solutions = blue-tint, caveats = yellow-tint, get-started = green-tint)
- Style Reddit quotes as blockquotes with attribution
- Use tables for comparisons and matrices
- Include purple "talk notes" as delivery hints (for talk-track format)
- Make it responsive and printable
- Save to `~/{Topic_Slug}_Developer_Voice.html`

Open the file in the browser with `open` command.

### Step 6: Offer Follow-ups

After presenting the artifact, ask if they want:
- A `.docx` version for Google Docs upload
- Specific sections expanded or rewritten
- Additional research on a sub-topic that emerged
- The quotes extracted as a standalone reference sheet

## Style Guidelines

- **Voice**: Casual, technical, concise. Write like you're explaining to a smart developer friend.
- **No marketing language**: Never use "revolutionary", "game-changing", "seamlessly", "leverage". Say what the thing actually does.
- **Quotes are king**: Every major claim should be backed by a real practitioner quote. This is what makes the content credible.
- **Honesty over advocacy**: The reality-check section is not optional. Hiding downsides destroys credibility with technical audiences.
- **Concrete over abstract**: Sample SQL, specific numbers, named tools -- not vague platitudes.
- **Attribution**: Always note the subreddit and role/context when available (e.g., "r/dataengineering, data architect at a bank").

## HTML Styling Reference

For consistent HTML output, use the color scheme, callout patterns, and typography in [references/html-styling.md](references/html-styling.md).

## Notes

- Reddit is the primary source but not the only one. HN, SO, and blog comment sections are fair game.
- Run at least 6 searches. More angles = better coverage. Don't stop at the first page of results.
- If a topic is too niche for Reddit (few results), broaden to general community forums or technical blogs.
- The skill works for any technology topic, not just Snowflake features. It can research "Kubernetes operator patterns" or "dbt vs Dataform" just as well.
- For Snowflake-specific topics, always check if there's a relevant Snowflake feature that addresses community pain points -- even if the user didn't ask for a Snowflake angle.
