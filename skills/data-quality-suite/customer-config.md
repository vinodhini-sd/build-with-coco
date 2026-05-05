# Customer Configuration

> **This is the file you fork and edit.**
> Everything else in this skill stays as-is. Customize here, and the skill adapts.

---

## ENABLED_FRAMEWORKS

Check the frameworks your team uses. Unchecked frameworks are skipped during routing.

```
[x] dmf          — Snowflake Data Metric Functions (continuous monitoring)
[x] dbt          — dbt schema tests (any adapter)
[ ] gx           — Great Expectations (Python pipelines, non-Snowflake sources)
[ ] soda         — Soda Core (YAML-based, 20+ source connectors)
[x] snowpark     — Inline quality gates for Snowpark Python pipelines
[ ] spark        — Inline quality gates for PySpark pipelines
```

**To enable a framework:** change `[ ]` to `[x]`.
**Note:** DMF and Snowpark are enabled by default. Enable GX or Soda if your team uses them. Enable Spark if you have PySpark pipelines outside Snowflake.

---

## LAYER_STANDARDS

Defines the minimum checks required before data can move to the next layer.
The skill enforces these standards when generating checks for each layer.

```yaml
bronze:
  required:
    - schema_validation       # column names and types match expected
    - row_count_gt_zero       # table is not empty
    - freshness               # data loaded within acceptable window
  optional:
    - source_null_check       # nulls on source PK columns

silver:
  required:
    - all_bronze_checks
    - null_check_key_columns  # nulls on business-critical columns
    - uniqueness_on_pk        # no duplicate primary keys
    - referential_integrity   # FK columns resolve to parent tables
  optional:
    - value_set_checks        # categorical columns use expected values

gold:
  required:
    - all_silver_checks
    - business_rule_checks    # domain-specific rules (revenue > 0, etc.)
    - cross_table_consistency # row counts consistent with upstream
  optional:
    - sla_freshness           # stricter freshness SLA for downstream

feature:
  required:
    - all_silver_checks
    - freshness_sla           # feature table updated within X hours
    - distribution_bounds     # mean and stddev within expected range
    - null_guard_all_features # no nulls on any feature column
  optional:
    - cardinality_check       # distinct value count matches training baseline
    - leakage_review          # flag joins with future timestamps
```

**To add a custom check:** add a new key under `optional` or `required` and describe it in `CUSTOM_CHECKS` below.

---

## THRESHOLD_DEFAULTS

Rules for setting thresholds. The skill uses these when generating check definitions.

```yaml
null_tolerance:
  primary_key_columns: 0          # zero nulls allowed
  foreign_key_columns: 0          # zero nulls allowed
  metric_columns: 0               # zero nulls allowed
  dimension_columns: 5%           # up to 5% allowed (e.g. optional attributes)
  free_text_columns: skip         # skip null checks on free-text fields

row_count:
  method: historical_percentile   # use p5 of last 30 days as lower bound
  fallback: gt_zero               # if no history, just check > 0
  alert_on_drop_pct: 20           # alert if row count drops >20% vs previous run

freshness:
  bronze_max_age_hours: 26        # slightly over 24h to account for delays
  silver_max_age_hours: 13        # twice-daily pipeline
  gold_max_age_hours: 25          # daily reporting
  feature_max_age_hours: 6        # ML inference needs fresh features

distribution_bounds:
  method: rolling_30d_mean_stddev # use rolling 30-day mean ± N*stddev
  n_stddev: 3                     # alert if value drifts > 3σ
  min_history_days: 14            # need at least 14 days to compute bounds

duplicate_tolerance:
  primary_key_columns: 0          # zero duplicates on PK
  metric_columns: skip            # skip duplicate checks on metrics
```

---

## ORG_STANDARDS

Snowflake-specific settings and naming conventions.

```yaml
snowflake:
  default_warehouse: TRANSFORMING    # warehouse to use for DMF execution
  default_role: TRANSFORMER          # role that owns DMF objects
  dmf_schema: QUALITY_MONITORING     # schema where custom DMFs are created
  dmf_schedule: "USING CRON 0 */6 * * * America/Los_Angeles"  # every 6 hours

dbt:
  project_path: ~/dbt               # default path to look for dbt project
  profile: default                  # dbt profile to use

naming:
  dmf_prefix: DMF_                  # custom DMFs named DMF_<check_type>
  test_tag: dq_suite                # tag added to generated dbt tests

ownership:
  dq_owner_column: OWNED_BY         # column in metadata tables tracking ownership
  alert_channel: "#data-quality"    # Slack channel for quality alerts (if configured)
```

---

## CUSTOM_CHECKS

Add org-specific business rule checks here. The skill reads these and includes them in generated check files.

```yaml
# Example custom checks — replace with your actual rules

# custom_checks:
#   - name: revenue_is_positive
#     description: "ORDER_REVENUE must be > 0 for all completed orders"
#     applies_to: gold
#     frameworks: [dbt, soda, gx]
#     sql: "SELECT COUNT(*) FROM {{table}} WHERE STATUS = 'completed' AND REVENUE <= 0"
#     threshold: 0
#
#   - name: customer_id_format
#     description: "CUSTOMER_ID must match pattern CUS-[0-9]+"
#     applies_to: [silver, gold]
#     frameworks: [gx, soda]
#     pattern: "^CUS-[0-9]+$"
#     column: customer_id
```

---

## NOTES FOR CUSTOMIZATION

- **Forking:** Copy this entire skill directory and modify `customer-config.md` for your team's standards.
- **Versioning:** Commit `customer-config.md` to your team's repo so threshold changes are tracked in git.
- **Threshold review:** Schedule a quarterly review of `THRESHOLD_DEFAULTS`. Stale thresholds are the #1 cause of meaningless alerts.
- **Team onboarding:** Point new engineers to this file first. It documents your DQ standards more concisely than any wiki page.
