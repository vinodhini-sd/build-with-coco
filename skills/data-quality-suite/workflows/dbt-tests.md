# Workflow: dbt Schema Tests

Loaded when: data is in a dbt project (any adapter — Snowflake, BigQuery, Databricks, Postgres, Redshift, etc.).

---

## Prerequisites

- dbt project exists (locally or accessible path)
- `dbt-core >= 1.5` installed
- Active dbt profile configured (`~/.dbt/profiles.yml`)
- Target model(s) built or source tables defined

---

## Steps

### Step 1: Locate dbt Project

Check `customer-config.md → ORG_STANDARDS.dbt.project_path` for the configured path.

If not set, ask: "Where is your dbt project? (e.g. `~/my-dbt-project`)"

```bash
# Verify project exists
ls {{project_path}}/dbt_project.yml
ls {{project_path}}/models/
```

Identify the target model(s):
- If user specified a model name: locate `models/**/{{model_name}}.sql`
- If user specified a schema: find all `.sql` files in the matching subdirectory
- If user wants full coverage: list all models

---

### Step 2: Describe Source Columns

For each target model, get column details. Two methods:

**If Snowflake adapter (or data is queryable via active connection):**
```sql
DESCRIBE TABLE {{database}}.{{schema}}.{{model_name}};
```

**If no live connection, parse the SQL:**
Read the model's `.sql` file. Extract column names and aliases from the `SELECT` statement.

---

### Step 3: Classify Columns → Recommend Tests

For each column, classify and recommend tests:

| Classification | How to identify | Tests to add |
|---|---|---|
| Primary key | Named `id`, `_id`, `pk`, or listed in `unique_key` in model config | `not_null` + `unique` |
| Foreign key | Named with `_id` suffix, references another model | `not_null` + `relationships` |
| Categorical / status | Type VARCHAR, low distinct count (< 20), named `status`, `type`, `state` | `not_null` + `accepted_values` |
| Required metric | Numeric column, business-critical (e.g. `amount`, `revenue`, `count`) | `not_null` |
| Optional field | Nullable by design | skip `not_null` |
| Timestamp | Type TIMESTAMP, DATETIME, DATE | `not_null` (if required) |

Apply layer standards from `customer-config.md → LAYER_STANDARDS` for the target layer.

---

### Step 4: Generate schema.yml

Load `templates/dbt_schema_tests.yml` and populate with column classifications.

Present the generated YAML to the user before writing:

```
I'll add these tests to models/{{path}}/schema.yml:

  {{model_name}}:
    - customer_id: not_null, unique
    - status: not_null, accepted_values [active, inactive, pending]
    - order_value: not_null
    - created_at: not_null
    - notes: (skipped — optional field)

Proceed? (yes / adjust values / skip columns)
```

**STOP — await user confirmation before writing the file.**

---

### Step 5: Write or Merge schema.yml

**If schema.yml already exists for this model:** read it first, merge new tests without overwriting existing ones. Never delete existing test definitions.

**If schema.yml does not exist:** create it using the template.

```bash
# Verify the output looks correct
cat {{project_path}}/models/{{path}}/schema.yml
```

---

### Step 6: Validate with dbt parse

```bash
cd {{project_path}}
dbt parse
```

A clean parse confirms no YAML syntax errors. If it fails, show the error and fix the YAML.

---

### Step 7: Optional — Run Tests

If the user wants to run tests immediately:

```bash
dbt test --select {{model_name}}
```

Show test results. For failures, identify the failing column and check + suggest root cause.

---

## Output

- `models/{{path}}/schema.yml` — created or updated with test definitions
- dbt parse passes with no errors
- (Optional) dbt test results

---

## Error Handling

| Error | Cause | Fix |
|---|---|---|
| `schema.yml already exists` | Existing file | Read + merge, never overwrite |
| `YAML syntax error` on parse | Indentation issue | Show line number, fix indentation |
| `node not found` | Model name mismatch | List models with `dbt ls` |
| `Compilation Error` on test run | Accepted values out of sync with data | Query distinct values, update accepted_values list |
| `relationship test fails` | FK column has orphaned values | This is a real quality issue — report it |
| `unique test fails` | Duplicate PKs exist | Report the duplicates, investigate upstream |
