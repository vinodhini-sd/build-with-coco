# Assess Teradata-to-Snowflake Migration Complexity

> Run SnowConvert on SQL scripts to categorize conversion effort and flag manual rewrites.

## The Prompt

```
I'm migrating from Teradata to Snowflake. I have 50 SQL scripts in ~/migration/teradata_sql/.
Run a SnowConvert assessment on them — categorize by conversion complexity (auto, semi-auto,
manual), flag any Teradata-specific syntax that needs rewriting, and estimate the overall
migration effort. Generate a summary report.
```

## What This Triggers

- SnowConvert assessment skill
- SQL file scanning and parsing
- Complexity categorization (auto / semi-auto / manual)
- Teradata-specific syntax flagging
- Summary report generation

## Before You Run

- SQL files in a local directory
- SnowConvert available (or CoCo will guide installation)
- Files should be valid Teradata SQL

## Tips

- Replace `~/migration/teradata_sql/` with your actual script directory
- Works for other source platforms too: "migrating from Oracle" or "from SQL Server"
- Add "convert the auto-convertible scripts and save to ~/migration/snowflake_sql/" for execution
