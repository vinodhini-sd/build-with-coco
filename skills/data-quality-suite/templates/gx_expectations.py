# Great Expectations Expectation Suite Template
# Replace {{placeholder}} values before running.
# Requires: great-expectations >= 0.18 (fluent datasource API)
# Install: pip install great-expectations

import great_expectations as gx
import os

# ============================================================
# STEP 1: Initialize or load GX context
# ============================================================
context = gx.get_context()

# ============================================================
# STEP 2: Add datasource
# Choose ONE block below based on your datasource type.
# ============================================================

# --- SNOWFLAKE DATASOURCE ---
snowflake_datasource = context.sources.add_or_update_snowflake(
    name="{{datasource_name}}",
    account=os.environ["SNOWFLAKE_ACCOUNT"],
    user=os.environ["SNOWFLAKE_USER"],
    # Use one of: password, private_key_path, or private_key_passphrase
    password=os.environ.get("SNOWFLAKE_PASSWORD"),
    database="{{database}}",
    schema="{{schema}}",
    warehouse="{{warehouse}}",
    role="{{role}}",
)

# --- PANDAS / LOCAL FILE DATASOURCE ---
# pandas_datasource = context.sources.add_or_update_pandas(name="{{datasource_name}}")

# --- SPARK DATASOURCE ---
# from pyspark.sql import SparkSession
# spark = SparkSession.builder.getOrCreate()
# spark_datasource = context.sources.add_or_update_spark(name="{{datasource_name}}", spark_config={})

# ============================================================
# STEP 3: Add data asset and batch request
# ============================================================

# For Snowflake table
data_asset = snowflake_datasource.add_table_asset(
    name="{{asset_name}}",
    table_name="{{table_name}}",
)
batch_request = data_asset.build_batch_request()

# For Pandas (local file)
# import pandas as pd
# df = pd.read_parquet("{{file_path}}")
# data_asset = pandas_datasource.add_dataframe_asset(name="{{asset_name}}")
# batch_request = data_asset.build_batch_request(dataframe=df)

# ============================================================
# STEP 4: Create or update expectation suite
# ============================================================

suite_name = "{{suite_name}}_suite"
suite = context.add_or_update_expectation_suite(expectation_suite_name=suite_name)

validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite_name=suite_name,
)

# ============================================================
# STEP 5: Table-level expectations
# ============================================================

# Table must not be empty
validator.expect_table_row_count_to_be_between(
    min_value={{min_row_count}},   # e.g. 1000
    max_value=None,                # None = no upper bound
)

# Schema must match expected columns (set to fail on unexpected columns)
validator.expect_table_columns_to_match_set(
    column_set=["{{col1}}", "{{col2}}", "{{col3}}"],
    exact_match=False,  # False = extra columns are OK
)

# ============================================================
# STEP 6: Primary key column
# ============================================================

# {{pk_column}} — no nulls, all unique
validator.expect_column_values_to_not_be_null(column="{{pk_column}}")
validator.expect_column_values_to_be_unique(column="{{pk_column}}")

# ============================================================
# STEP 7: Categorical / status column
# ============================================================

validator.expect_column_values_to_not_be_null(column="{{status_column}}")
validator.expect_column_values_to_be_in_set(
    column="{{status_column}}",
    value_set={"{{value_1}}", "{{value_2}}", "{{value_3}}"},
)

# ============================================================
# STEP 8: Numeric metric column
# ============================================================

validator.expect_column_values_to_not_be_null(column="{{metric_column}}")
validator.expect_column_values_to_be_between(
    column="{{metric_column}}",
    min_value=0,      # replace with actual business minimum
    max_value=None,   # set if there's a known maximum
)
validator.expect_column_mean_to_be_between(
    column="{{metric_column}}",
    min_value={{mean_min}},  # e.g. 10.0
    max_value={{mean_max}},  # e.g. 500.0
)

# ============================================================
# STEP 9: Timestamp / freshness column
# ============================================================

validator.expect_column_values_to_not_be_null(column="{{timestamp_column}}")
# Freshness check: max timestamp should be recent
import datetime
validator.expect_column_max_to_be_between(
    column="{{timestamp_column}}",
    min_value=(datetime.datetime.utcnow() - datetime.timedelta(hours={{max_age_hours}})).isoformat(),
    max_value=None,
)

# ============================================================
# STEP 10: String format check (regex)
# ============================================================

# Uncomment and customize for format-validated columns (e.g. email, ID)
# validator.expect_column_values_to_match_regex(
#     column="{{format_column}}",
#     regex=r"{{regex_pattern}}",  # e.g. r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
# )

# ============================================================
# STEP 11: Distribution bounds (feature tables)
# ============================================================

# Uncomment for ML feature columns — check mean is within expected range
# validator.expect_column_mean_to_be_between(
#     column="{{feature_column}}",
#     min_value={{feature_mean_min}},
#     max_value={{feature_mean_max}},
# )
# validator.expect_column_stdev_to_be_between(
#     column="{{feature_column}}",
#     min_value=0,
#     max_value={{feature_stddev_max}},
# )

# ============================================================
# STEP 12: Save suite and run checkpoint
# ============================================================

validator.save_expectation_suite(discard_failed_expectations=False)

checkpoint = context.add_or_update_checkpoint(
    name="{{checkpoint_name}}",
    validations=[
        {
            "batch_request": batch_request,
            "expectation_suite_name": suite_name,
        }
    ],
)

result = checkpoint.run()

if not result.success:
    print("QUALITY CHECK FAILED")
    for validation_result in result.run_results.values():
        for expectation_result in validation_result["validation_result"]["results"]:
            if not expectation_result["success"]:
                print(f"  FAIL: {expectation_result['expectation_config']['expectation_type']}")
                print(f"        Column: {expectation_result['expectation_config']['kwargs'].get('column', 'table-level')}")
                print(f"        Result: {expectation_result['result']}")
    raise SystemExit(1)

print("All quality checks passed.")
