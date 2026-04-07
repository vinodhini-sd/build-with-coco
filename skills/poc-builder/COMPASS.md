# POC Builder — Compass

## Quick Commands
- Invoke: `$poc-builder` or describe the POC goal in plain language
- Trigger phrases: "poc builder", "build this", "zero to poc", "try this", "teach me", "walk me through", "prototype this", "run this guide"
- Input: any URL (quickstart, docs, blog, GitHub, social post) or a topic name

## Key Files
- `SKILL.md` — full workflow: ingestion, research pass, data/env setup, build, verify, artifacts
- `references/KNOWN_GOTCHAS.md` — feature-specific traps (Dynamic Tables, Cortex Agents, Iceberg, etc.)
- `references/ACCOUNT_DISCOVERY.md` — how to find matching tables in the user's account
- `references/GUIDE_PARSING.md` — how to extract a demo spec from different input types
- `references/TEACHING_PATTERNS.md` — pacing, check-ins, how to adapt to user experience level
- `references/BUILD_SUMMARY_TEMPLATE.md` — artifact template (summary.md, source code, prompts.md)

## Non-Obvious Patterns
- Runs a proactive research pass before building — invokes bundled CoCo skills (iceberg, dynamic-tables, etc.) to catch stale syntax before it becomes a mid-build error
- Data question is opt-in, not presumptuous — ask neutrally whether to use their data or synthetic; don't assume they want to share schema info
- Runs a 5-check verification protocol after every build: objects exist, queries return results, no orphaned dependencies, cleanup SQL is valid, artifacts are written
- Pacing adapts to user responses — no explicit Accelerator/Tutorial mode switch; infer from how they reply

## See Also
- `know-your-data` — run first if user needs to discover what data they have before picking a POC workflow
