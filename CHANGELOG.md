# Changelog

## [Unreleased]

### Changed
- Renamed `prompts/` → `recipes/` for clarity
- Flattened `recipes/scenarios/` — use-case directories now live directly under `recipes/`
- Renamed `recipes/roles/` → `recipes/by-role/`
- Added `AGENTS.md` — contribution guide for AI coding agents
- Split `skills/dbt-model-generator/SKILL.md` — workflow detail moved to `references/workflow.md`
- Moved `skills/developer-voice` HTML styling spec to `references/html-styling.md`
- Added `skills/poc-builder/references/BUILD_SUMMARY_TEMPLATE.md`
- Removed per-skill `README.md` files (content lives in `SKILL.md` and root `README.md`)
- Fixed `install.sh` prompts install — now recursively copies nested recipe directories
