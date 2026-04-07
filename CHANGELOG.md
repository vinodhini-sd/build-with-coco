# Changelog

## [Unreleased]

### Added
- Added `COMPASS.md` navigation files to all 5 skills (`poc-builder`, `dbt-model-generator`, `developer-voice`, `know-your-data`, `aws-glue-iceberg-setup`) — 25–35 line files encoding quick commands, key files, non-obvious patterns, and cross-references for each skill
- Added `docs/COMPASS_GUIDE.md` — best practice guide for writing skill compass files, including the 4-section template, 5-question framework, freshness rules, and critic checklist

### Changed
- Updated `AGENTS.md` — added COMPASS.md to skill directory structure, rules, adding-a-skill steps, and keeping-docs-in-sync checklist
- Updated `README.md` — repo structure tree now includes COMPASS.md and `docs/` directory

---

### Added (previous)
- Added `hooks/` directory with 6 session automation hooks:
  - `hooks/check-errors.py` — detects Snowflake errors and fires session alerts
  - `hooks/session-start.sh` — runs on session start, sets environment context
  - `hooks/set-tab-title.sh` — sets terminal tab title from session intent
  - `hooks/tab-title-helper.py` — extracts short intent label from first prompt
  - `hooks/whats-new-helper.py` — detects new Snowflake features (What's New feed)
  - `hooks/README.md` — setup guide and required env vars (`COCO_SF_*`)
- `install.sh` now installs hooks via `install_hooks()` — copies to `~/.snowflake/cortex/hooks/`
- Added `./install.sh hooks` subcommand for hooks-only install

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
