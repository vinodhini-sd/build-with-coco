---
name: dbt-model-generator
description: "Automatically generate dbt dimensional models (star schema) from raw Snowflake tables. Use when: user wants to generate dbt models, shift left data modeling, automate dimensional modeling, create facts and dimensions from raw data, build a star schema from raw tables, or auto-generate dbt code. Triggers: generate dbt models, shift left, dimensional model, auto model, star schema from raw, dbt from iceberg, dbt from raw."
---

# dbt Model Generator

Automates the creation of dbt dimensional models from raw Snowflake tables. Profiles the data, identifies facts and dimensions, generates staging/dim/fact models with tests, and submits a PR for engineer review.

## Workflow

```
Start
  ↓
Step 1: Collect Parameters
  ↓
Step 2: Discover & Profile Raw Tables
  ↓
Step 3: Classify Columns (Facts vs Dimensions)
  ↓  ⚠️ STOP — User approves classification
Step 4: Generate dbt Project Scaffold
  ↓
Step 5: Generate Models (staging → dims → facts)
  ↓
Step 6: Generate Schema Tests & Docs
  ↓
Step 7: Validate (dbt parse)
  ↓  ⚠️ STOP — User reviews generated models
Step 8: Git Commit & PR
  ↓
Done
```

## Parameters

**Required:**
- `<SOURCE_DATABASE>`: Snowflake database containing raw tables
- `<SOURCE_SCHEMA>`: Schema within the database (or `*` for all schemas)

**Optional:**
- `<SOURCE_TABLE>`: Specific table to model (default: discover all tables in schema)
- `<PROJECT_NAME>`: dbt project name (default: derived from database name)
- `<PROJECT_PATH>`: Where to create the project on disk (default: `~/Documents/coco-dev/<PROJECT_NAME>`)
- `<GITHUB_REPO>`: GitHub repo for PR (format: `owner/repo-name`)
- `<WAREHOUSE>`: Snowflake warehouse (default: `COMPUTE_WH`)
- `<ROLE>`: Snowflake role (default: `SYSADMIN`)

### Step 1: Collect Parameters

**Ask** the user:
```
To generate dimensional models, I need:
1. Source database name?
2. Source schema (or * for all)?
3. Specific table (or all tables in schema)?
4. GitHub repo for the PR (owner/repo)?
```

If the user provided a database/table in their request, extract those values and only ask for missing parameters.

### Step 2: Discover & Profile Raw Tables

**Goal:** Understand every table's structure, row counts, column types, cardinality, and relationships.

**Actions:**

1. **List tables** in the source database/schema:
   ```sql
   SELECT table_schema, table_name, row_count
   FROM <SOURCE_DATABASE>.INFORMATION_SCHEMA.TABLES
   WHERE table_schema = '<SOURCE_SCHEMA>' AND table_type = 'BASE TABLE'
   ORDER BY table_schema, table_name
   ```
   If `<SOURCE_SCHEMA>` is `*`, use `table_schema NOT IN ('INFORMATION_SCHEMA')`.

2. **For each table**, get full column metadata:
   ```sql
   SELECT column_name, data_type, ordinal_position
   FROM <SOURCE_DATABASE>.INFORMATION_SCHEMA.COLUMNS
   WHERE table_schema = '<schema>' AND table_name = '<table>'
   ORDER BY ordinal_position
   ```

3. **Profile each table** — sample data to understand values:
   ```sql
   SELECT * FROM <SOURCE_DATABASE>.<schema>.<table> LIMIT 20
   ```

4. **Check for existing semantic views, tags, or comments** on the tables for additional context.

5. **Identify relationships** across tables by matching column names (e.g., `*_ID` columns that appear in multiple tables).

**Output:** A profiling summary per table: column list, types, approximate cardinality, null rates, candidate keys, foreign key relationships.

### Step 3: Classify Columns (Facts vs Dimensions)

**Goal:** For each source table, determine if it is a fact, dimension, or bridge table, and classify every column.

**Classification rules:**

| Signal | Classification |
|---|---|
| Numeric columns with high cardinality (amounts, quantities, scores) | **Measure** (fact) |
| `*_ID` columns with low-to-medium cardinality | **Foreign Key** to dimension |
| `*_ID` column that is unique per row | **Primary Key / Natural Key** |
| Categorical text with low cardinality | **Dimension attribute** |
| Timestamps / dates | **Date dimension FK** or degenerate dimension |
| Free text (long VARCHAR, reviews, descriptions) | **Degenerate dimension** |
| String-encoded structured data (e.g., `"[2, 3]"`) | **Needs parsing** — note transformation needed |

**For each table, produce:**
- Table role: fact, dimension, or bridge
- For facts: grain statement, list of measures, list of FK relationships
- For dimensions: natural key, list of attributes, SCD type recommendation
- Star schema ASCII diagram showing relationships

**⚠️ MANDATORY STOPPING POINT**: Present the classification to the user:
```
Here is my proposed dimensional model:

[Star schema diagram]

Facts: [list with grain]
Dimensions: [list with keys and attributes]
Measures: [list]

Classification rationale for each column...

Data quality warnings: [any issues found]

Do you approve this model? (Yes / Modify)
```

Do NOT proceed until user approves.

### Step 4: Generate dbt Project Scaffold

**Goal:** Create a complete dbt project if one doesn't already exist.

**Actions:**

1. Check if a dbt project already exists at `<PROJECT_PATH>`. If yes, skip scaffold and add models to existing project.

2. Create directory structure:
   ```
   <PROJECT_PATH>/
   ├── dbt_project.yml
   ├── profiles.yml
   ├── packages.yml
   ├── models/
   │   ├── sources.yml
   │   ├── staging/
   │   ├── dimensions/
   │   └── facts/
   ```

3. **dbt_project.yml**: Configure model materializations:
   - `staging/` → `materialized: view`
   - `dimensions/` → `materialized: table`
   - `facts/` → `materialized: table`

4. **profiles.yml**: Configure Snowflake connection using `<WAREHOUSE>`, `<ROLE>`, `<SOURCE_DATABASE>`, `externalbrowser` auth.

5. **packages.yml**: Include `dbt-labs/dbt_utils` for `generate_surrogate_key`.

6. **sources.yml**: Define all source tables discovered in Step 2.

### Step 5: Generate Models

**Goal:** Generate SQL models following source-based naming conventions.

**Naming convention:** `stg_<source_table>`, `dim_<entity>`, `fact_<business_process>`

#### 5a: Staging Models (`stg_*.sql`)

One staging model per source table. Each must:
- Reference source via `{{ source('...', '...') }}`
- Rename columns to snake_case
- Cast types appropriately (especially string-encoded numbers, dates)
- Parse structured strings (e.g., `"[x, y]"` → separate integer columns)
- Convert unix timestamps to `TIMESTAMP` / `DATE`
- Derive useful computed columns (e.g., `LENGTH(text_column)` as `review_length`)
- Add SQL comments explaining non-obvious transformations

#### 5b: Dimension Models (`dim_*.sql`)

One model per identified dimension. Each must:
- Use `{{ config(materialized='table') }}`
- Generate surrogate key: `{{ dbt_utils.generate_surrogate_key(['natural_key']) }}`
- Select distinct dimension members from staging
- For Type 1 SCD: use `ROW_NUMBER()` ordered by most recent timestamp to pick latest attribute values
- Include a `dim_date` model generated as a date spine from `MIN`/`MAX` dates in the data, with attributes: `full_date`, `year`, `quarter`, `month`, `month_name`, `day_of_month`, `day_of_week`, `day_name`, `week_of_year`, `is_weekend`

#### 5c: Fact Models (`fact_*.sql`)

One model per identified fact table. Each must:
- Use `{{ config(materialized='table') }}`
- Generate surrogate key for the fact row
- Join to all dimension models to resolve surrogate foreign keys
- Include all measures from staging
- Include degenerate dimensions (long text kept on fact, not in a dim)
- Add SQL comments explaining why each column is classified as measure vs degenerate dimension

### Step 6: Generate Schema Tests & Docs

For every model, create a `schema.yml` with:

**Tests:**
- `unique` + `not_null` on all surrogate keys and natural keys
- `relationships` tests between fact FKs and dimension PKs
- `accepted_values` on categorical/enum columns where the domain is known
- `not_null` on measures

**Documentation:**
- Column-level `description` for every column in every model

### Step 7: Validate

**Actions:**

1. Install packages:
   ```bash
   uv run --with dbt-snowflake dbt deps --profiles-dir <PROJECT_PATH>
   ```

2. Parse/compile the project:
   ```bash
   uv run --with dbt-snowflake dbt parse --profiles-dir <PROJECT_PATH>
   ```

3. **If parse fails:** Fix errors and retry (max 3 attempts).

4. Report results:
   ```
   ✅ dbt parse: X models, Y tests, Z sources — 0 errors
   ```

5. **If Snowflake connection is available**, also run:
   ```bash
   uv run --with dbt-snowflake dbt run --profiles-dir <PROJECT_PATH>
   uv run --with dbt-snowflake dbt test --profiles-dir <PROJECT_PATH>
   ```

**⚠️ MANDATORY STOPPING POINT**: Present all generated models to the user for review before proceeding to Git/PR.

### Step 8: Git Commit & PR

**Goal:** Commit to a feature branch and open a PR with rich context for the reviewing engineer.

**Actions:**

1. **Initialize git** if not already a repo (`git init`), add `.gitignore` (exclude `target/`, `dbt_packages/`, `logs/`, `.user.yml`).

2. **Ensure remote is set** to `<GITHUB_REPO>`:
   ```bash
   git remote add origin https://github.com/<GITHUB_REPO>.git
   ```

3. **Create feature branch** per source table:
   - Branch name: `feature/dim-model-<source_table_lowercase>`

4. **Commit** with descriptive message listing all models, measures, and dimensions.

5. **Push** branch and **create PR** via `gh pr create` with body containing:
   - Summary of models generated
   - Star schema ASCII diagram
   - Data profiling stats (row counts, cardinality)
   - Classification rationale (why each column was assigned its role)
   - Data quality warnings found during profiling
   - Test plan checklist (`dbt deps` / `compile` / `run` / `test`)

**PR body template:**
```markdown
## Summary
- AI-generated star schema from `<SOURCE_DATABASE>.<SOURCE_SCHEMA>.<SOURCE_TABLE>`
- [N] staging models, [N] dimensions, [N] fact tables, [N] schema tests

## Star Schema
[ASCII diagram]

## Data Profiling
| Table | Rows | Columns | Candidate Keys |
|---|---|---|---|

## Column Classification Rationale
| Column | Classification | Reason |
|---|---|---|

## Data Quality Warnings
- [any issues found]

## Test Plan
- [ ] `dbt deps`
- [ ] `dbt compile`
- [ ] `dbt run`
- [ ] `dbt test`
- [ ] Spot-check joins and transformations
```

## Stopping Points

- ✋ Step 3: User approves fact/dimension classification and star schema design
- ✋ Step 7: User reviews generated models before Git operations
- ✋ Step 8: PR created — link presented to user

## Output

- Complete dbt project with staging, dimension, and fact models
- `schema.yml` files with tests and column documentation
- GitHub PR on a feature branch ready for engineer review

## Troubleshooting

| Issue | Solution |
|---|---|
| `dbt parse` fails | Check column name quoting — mixed-case columns from Iceberg/Parquet need double quotes (e.g., `"reviewText"`) |
| Snowflake connection fails during `dbt compile` | Use `dbt parse` for offline validation; connection only needed for `dbt run` |
| `gh pr create` permission denied | Token needs `Contents (R&W)` and `Pull requests (R&W)` fine-grained permissions |
| String-encoded data (e.g., `"[2, 3]"`) | Use `TRY_CAST` + `REGEXP_SUBSTR` in staging model for safe parsing |
| `HELPFUL`-style array strings | Parse with `regexp_substr(col, '\\d+', 1, 1)` and `regexp_substr(col, '\\d+', 1, 2)` |
