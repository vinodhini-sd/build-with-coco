# Assess Teradata-to-Snowflake Migration Complexity

> Run SnowConvert on SQL scripts to categorize conversion effort and flag manual rewrites.

## The Prompt

```
I'm migrating SQL workloads from {{source-platform}} to Snowflake. My SQL scripts are in
{{sql-directory}}. Run a SnowConvert assessment — categorize by conversion complexity
(auto, semi-auto, manual), flag any dialect-specific syntax that needs rewriting, and
generate a summary report with estimated migration effort.
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
- Files should be valid SQL from a supported source platform: Teradata, Oracle, or SQL Server

## Tips

- Replace `~/migration/teradata_sql/` with your actual script directory
- Works for other source platforms too: "migrating from Oracle" or "from SQL Server"
- Add "convert the auto-convertible scripts and save to ~/migration/snowflake_sql/" for execution
