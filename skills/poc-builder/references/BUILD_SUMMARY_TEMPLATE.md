# Build Summary Template

Template for the `poc-[workflow-slug]-summary.md` artifact generated at the end of every POC build.

Save to: `./poc-[workflow-slug]-summary.md`

---

```markdown
# POC: [Workflow Title — describes what it does, not which feature]

**Built on:** [date]
**Source:** [URL]
**Data:** [own data table or synthetic]
**Environment:** [database.schema]

## Workflow
[What the pipeline does end-to-end]

## Features used
- [Feature 1]: [role in the workflow]
- [Feature 2]: [role in the workflow]

## Architecture
[source] → [ingestion] → [transform] → [output]
<!-- ASCII diagram showing how the pieces connect.
     Keep it simple: boxes and arrows, not a 50-line diagram. -->

## Prerequisites & Permissions
- **Role:** [role used] — needs [specific privileges]
- **Warehouse:** [warehouse] — [size, DDL-capable]
- **External access:** [any external stages, APIs, packages]
<!-- Include everything someone else would need to reproduce this from scratch. -->

## What was built
- [Object type] [fully.qualified.name]: [purpose]
- [Object type] [fully.qualified.name]: [purpose]

## How to verify
[SQL]

## How to clean up
<!-- IMPORTANT: Run drops in this order to avoid dependency errors.
     First suspend/drop tasks, then streams, then everything else.
     Only include DROP SCHEMA if the POC created the schema.
     If you built in a pre-existing schema, drop individual objects instead. -->
ALTER TASK IF EXISTS [db.schema.task] SUSPEND;
DROP TASK IF EXISTS [db.schema.task];
DROP STREAM IF EXISTS [db.schema.stream];
DROP PIPE IF EXISTS [db.schema.pipe];
DROP VIEW IF EXISTS [db.schema.view];
DROP TABLE IF EXISTS [db.schema.table];
DROP STAGE IF EXISTS [db.schema.stage];
-- DROP SCHEMA IF EXISTS [db.schema];  -- ONLY if this POC created the schema
-- Only include warehouse/role drops if the POC created them

## Scaling Notes
<!-- One paragraph. What would change for production?
     Consider: warehouse sizing, clustering keys, partition pruning, task frequency, data volume.
     Example: "This POC used 28K rows on XS warehouse. For production volumes (10M+ rows),
     consider clustering on EVENT_TS, scaling to MEDIUM warehouse, and tightening task schedule." -->
```
