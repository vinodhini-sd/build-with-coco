# Developer Voice — Compass

## Quick Commands
- Invoke: `$developer-voice` or describe the research goal
- Trigger phrases: "developer voice", "community pulse", "reddit research", "talk track", "what are developers saying about {{topic}}", "pain points"
- Input: a topic, feature name, product, or competitor

## Key Files
- `SKILL.md` — full workflow: source selection, quote extraction, synthesis, output formatting
- `references/html-styling.md` — dark-theme HTML template for the styled research report output

## Non-Obvious Patterns
- Always grounded in verbatim quotes — summaries without direct quotes are rejected; every claim must cite a source URL
- Two output modes: talk track (narrative for a presentation) or research brief (structured intel doc) — ask the user which before generating
- Reddit is the primary source; community forums and GitHub issues are secondary; LinkedIn and blog posts are tertiary
- Search window matters: recent posts (last 6 months) weighted higher for fast-moving topics like AI/LLM features

## See Also
- `community-channel-analysis` bundled CoCo skill — if installed, use it for structured cross-platform analysis; developer-voice is for practitioner-quote-grounded synthesis
