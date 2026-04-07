# Know Your Data — Compass

## Quick Commands
- Invoke: `$know-your-data` or describe the discovery goal
- Trigger phrases: "know your data", "know my data", "find data", "data discovery", "what can I access", "explore account", "what tables do I have"
- No required inputs — runs against the active Snowflake connection and current role

## Key Files
- `SKILL.md` — full workflow: role switching, schema scan, table profiling, role-to-table mapping

## Non-Obvious Patterns
- Switches roles automatically to widen visibility — uses SHOW GRANTS to find accessible roles, then switches to each to surface tables that the base role can't see
- INFORMATION_SCHEMA and SHOW TABLES return different columns and scope; the skill queries both and reconciles them
- Output is a role-to-table map, not just a flat table list — tells the user which role gives access to which tables
- Skips system schemas (INFORMATION_SCHEMA, SNOWFLAKE) by default to avoid noise

## See Also
- `poc-builder` — natural hand-off after discovery; once the user knows what data they have, poc-builder can build a workflow on top of it
