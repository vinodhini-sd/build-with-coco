# Workflow: Soda Core

Loaded when: user has Soda Core installed or requests YAML-based checks, OR data is in a non-Snowflake source that GX doesn't cover well (Databricks, Hive, Trino, MySQL, MS SQL, etc.).

Soda Core supports 20+ source connectors with a simple YAML interface.

---

## Prerequisites

- Python 3.8+
- Soda Core + connector for the target datasource
- Target datasource accessible from the Python environment

---

## Steps

### Step 1: Install Soda Core

```bash
# Base + connector for your datasource
pip install soda-core-snowflake     # Snowflake
pip install soda-core-spark-df      # Spark DataFrames
pip install soda-core-postgres      # PostgreSQL
pip install soda-core-bigquery      # BigQuery
pip install soda-core-databricks    # Databricks SQL
pip install soda-core-dask          # Pandas/Dask DataFrames
```

Check `customer-config.md → ENABLED_FRAMEWORKS` — if Soda is enabled, ask which connector.

```bash
# Verify
soda --version
```

---

### Step 2: Configure Datasource Connection

Generate the datasource config file (`soda_datasource.yml`):

**Snowflake example:**
```yaml
data_source {{datasource_name}}:
  type: snowflake
  account: ${SNOWFLAKE_ACCOUNT}
  user: ${SNOWFLAKE_USER}
  private_key_path: ${SNOWFLAKE_PRIVATE_KEY_PATH}
  database: {{database}}
  schema: {{schema}}
  warehouse: {{warehouse}}
  role: {{role}}
```

**PostgreSQL example:**
```yaml
data_source {{datasource_name}}:
  type: postgres
  host: ${POSTGRES_HOST}
  port: 5432
  database: {{database}}
  schema: {{schema}}
  username: ${POSTGRES_USER}
  password: ${POSTGRES_PASSWORD}
```

Credentials always use `${ENV_VAR}` format — never hardcode in the YAML.

---

### Step 3: Profile Columns

Run a quick profile to inform check generation:

```bash
soda scan -d {{datasource_name}} -c soda_datasource.yml --profile {{table_name}}
```

Or use a SQL DESCRIBE if the datasource is Snowflake:
```sql
DESCRIBE TABLE {{database}}.{{schema}}.{{table}};
```

---

### Step 4: Generate checks.yml

Load `templates/soda_checks.yml` and populate for the target table and columns.

Present the checks before writing:

```
I'll create soda_checks_{{table_name}}.yml with:

  {{table_name}}:
  - row_count > 0
  - missing_count(customer_id) = 0
  - duplicate_count(customer_id) = 0
  - missing_count(status) = 0
  - invalid_count(status) = 0:
      valid values: [active, inactive, pending]
  - freshness(created_at) < 26h
  - schema:
      name: Expected schema for {{table_name}}
      columns:
        - name: customer_id
          type: VARCHAR
        - name: status
          type: VARCHAR

Proceed? (yes / adjust / add business rules)
```

**STOP — await confirmation before writing.**

---

### Step 5: Write checks.yml

Write to `{{output_path}}/soda_checks_{{table_name}}.yml`.

---

### Step 6: Run Scan

```bash
soda scan -d {{datasource_name}} \
  -c soda_datasource.yml \
  soda_checks_{{table_name}}.yml
```

Show results. Green = pass, Red = fail with row counts.

---

### Step 7: Integrate into Pipeline (Optional)

**Python (inside Airflow DAG, Prefect task, etc.):**
```python
from soda.scan import Scan

scan = Scan()
scan.set_data_source_name("{{datasource_name}}")
scan.add_configuration_yaml_file("soda_datasource.yml")
scan.add_sodacl_yaml_file("soda_checks_{{table_name}}.yml")
scan.execute()

if scan.has_check_failures():
    raise ValueError(f"Soda checks failed: {scan.get_error_logs_text()}")
```

---

## Output

- `soda_datasource.yml` — datasource connection config (credentials from env vars)
- `soda_checks_{{table_name}}.yml` — check definitions
- (Optional) Python integration snippet for pipeline gate

---

## Error Handling

| Error | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: soda` | Not installed | `pip install soda-core-{{connector}}` |
| `Connection refused` | Wrong host/port | Check datasource config, test connection manually |
| `Permission denied` | User lacks SELECT on table | Check schema permissions |
| `Invalid check syntax` | YAML formatting issue | Validate YAML indentation |
| Freshness check always fails | `created_at` not updating (stale table) | Real quality issue — report to data owner |
| Schema check fails | Column removed upstream | Investigate schema change, update check or fix upstream |
