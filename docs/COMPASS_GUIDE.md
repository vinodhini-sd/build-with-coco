# Skill Compass Guide

A compass file is a 25–35 line navigation guide that lives alongside `SKILL.md`. It tells an agent or contributor exactly how to invoke a skill, which files matter, what will silently break, and what to load next — without reading the full skill spec.

Inspired by Meta's approach to encoding tribal knowledge for AI agents: [How Meta Used AI to Map Tribal Knowledge in Large-Scale Data Pipelines](https://engineering.fb.com/2026/04/06/developer-tools/how-meta-used-ai-to-map-tribal-knowledge-in-large-scale-data-pipelines/)

---

## The Principle: Compass, Not Encyclopedia

A SKILL.md is an encyclopedia — complete, detailed, authoritative. A COMPASS.md is a compass — it tells you which direction to face. You need both.

Without a compass, agents burn tool calls exploring a 500-line spec to answer "how do I invoke this?" With one, invocation is a single lookup.

**Rule**: Any skill >150 lines needs a COMPASS.md.

---

## The 4-Section Format

```markdown
# [Skill Name] — Compass

## Quick Commands
- Invoke: `$skill-name` or describe the task in plain language
- Trigger phrases: "phrase one", "phrase two"
- Required inputs: {{placeholder}} for anything the user must provide

## Key Files
- `SKILL.md` — core workflow and decision logic
- `references/FILENAME.md` — [one-line description of what it contains]

## Non-Obvious Patterns
- [Gotcha that isn't in the README and will cause silent failure or wrong output]
- [Ordering constraint, naming rule, or behavioral quirk]
- [Default that surprises people]

## See Also
- [related-skill] — [when to use it instead of or before this one]
- [bundled-skill] — [if a CoCo bundled skill is relevant]
```

Keep every line earning its place. If it's in the README or obvious from the skill name, cut it.

---

## The 5 Questions

Answer these per skill before writing the compass:

1. **What does it do?** One sentence. Not what feature it uses — what workflow it completes.
2. **How do you invoke it?** Exact trigger phrases and any required inputs.
3. **What breaks?** Ordering constraints, naming rules, role requirements, silent failure modes.
4. **What does it depend on?** Other skills to run first, required Snowflake objects, env vars.
5. **What's non-obvious that isn't written down anywhere?** This is where the real value is.

Question 5 is the one that matters. If your Non-Obvious Patterns section could have been inferred from the README, rewrite it.

---

## Freshness Rules

Every path in `Key Files` is a contract. When you update a skill:

- Rename a references file → update COMPASS.md
- Add a new non-obvious pattern → add it to COMPASS.md
- Remove a file from references/ → remove it from COMPASS.md

Stale compass files cause more harm than no compass. An agent that follows a broken path wastes more tokens than one that reads from scratch.

**Before merging any skill update**: check that every path in its COMPASS.md still exists.

---

## Critic Checklist

Before merging a COMPASS.md, verify:

- [ ] ≤35 lines (excluding the header)
- [ ] Every path in Key Files exists in the repo right now
- [ ] Non-Obvious Patterns are actually non-obvious — not basic docs
- [ ] See Also references are reachable (installed skill or bundled skill)
- [ ] An agent could invoke the skill correctly using only this file + trigger phrases

If any item fails, revise before merging.

---

## When NOT to Create a Compass

Skip COMPASS.md for skills under 150 lines where SKILL.md is already concise. The compass adds overhead — only create one when the skill is complex enough that a reader needs a map.
