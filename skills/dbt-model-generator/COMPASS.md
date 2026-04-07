# dbt Model Generator — Compass

## Quick Commands
- Invoke: `$dbt-model-generator` or "generate dbt models from {{database}}.{{schema}}"
- Trigger phrases: "generate dbt models", "shift left", "dimensional model", "star schema from raw"
- Required: SOURCE_DATABASE, SOURCE_SCHEMA — everything else (warehouse, role, project name) is optional

## Key Files
- `SKILL.md` — full workflow: discover → profile → classify → generate → test → validate → PR
- `references/workflow.md` — detailed SQL for profiling, cardinality checks, and classification logic

## Non-Obvious Patterns
- Always runs DESCRIBE TABLE before querying — never assumes column names from table names alone
- Output is three model layers: staging (raw rename + cast) + dimensions + facts — not a single model
- PR description includes a Mermaid star schema diagram auto-generated from the classified columns
- Surrogate keys are SHA2 hashes of natural key columns, not sequences — works across dbt adapters

## See Also
- `poc-builder` — natural next step if the user wants to build a full pipeline on top of the generated models
