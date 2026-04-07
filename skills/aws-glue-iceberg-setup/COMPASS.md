# AWS Glue Iceberg Setup — Compass

## Quick Commands
- Invoke: `$aws-glue-iceberg-setup` or describe the integration goal
- Trigger phrases: "set up Glue Iceberg", "aws glue iceberg catalog", "connect Glue to Snowflake", "Glue catalog integration"
- Required: AWS account ID, S3 bucket for external volume, target Snowflake database

## Key Files
- `SKILL.md` — full workflow: IAM role + trust policy, external volume, catalog integration, Iceberg table creation, validation
- `references/KNOWN_GOTCHAS.md` — AWS-specific traps: IAM ordering, ALLOW_WRITES, partition evolution, schema mismatch failures
- `references/ATHENA_TYPE_MAPPING.md` — Glue/Athena type → Snowflake type mapping table (use when creating Iceberg tables from existing Glue schemas)

## Non-Obvious Patterns
- IAM trust policy must exist BEFORE creating the storage integration — Snowflake generates a principal ARN during storage integration creation; you need the ARN to write the trust policy, but the integration creation itself requires the IAM role to already exist. Bootstrap order: create IAM role (no trust policy yet) → create storage integration → copy principal ARN → update trust policy
- ALLOW_WRITES = TRUE on the external volume is required for managed Iceberg tables; read-only external volumes silently fail on INSERT/MERGE with a misleading permissions error
- Glue catalog setup and Polaris/REST catalog setup differ significantly in the CATALOG_INTEGRATION DDL — confirm which catalog type before generating SQL

## See Also
- `iceberg` bundled CoCo skill — handles Snowflake-side Iceberg operations (auto-refresh, table health, catalog-linked databases); aws-glue-iceberg-setup is for the AWS infrastructure wiring
