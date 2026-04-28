-- ============================================================
-- DMF Setup Template
-- Usage: Replace {{placeholder}} values before executing.
-- Run in order: 1) CREATE custom DMFs, 2) ALTER TABLE to attach
-- ============================================================

-- ============================================================
-- SECTION 1: Custom DMF Definitions
-- Skip this section if using only system DMFs (NULL_COUNT, etc.)
-- ============================================================

-- Custom DMF: Accepted values check
-- Replace {{dmf_schema}}, {{column_name}}, {{values_csv}}
CREATE OR REPLACE DATA METRIC FUNCTION {{dmf_schema}}.DMF_ACCEPTED_VALUES_{{column_name}}(
    arg_t TABLE(col_value VARCHAR)
)
RETURNS NUMBER
AS
$$
    SELECT COUNT_IF(col_value NOT IN ({{values_csv}}) AND col_value IS NOT NULL)
    FROM arg_t
$$;

-- Custom DMF: Numeric range check (value must be between min and max)
-- Replace {{dmf_schema}}, {{column_name}}, {{min_value}}, {{max_value}}
CREATE OR REPLACE DATA METRIC FUNCTION {{dmf_schema}}.DMF_RANGE_CHECK_{{column_name}}(
    arg_t TABLE(col_value NUMBER)
)
RETURNS NUMBER
AS
$$
    SELECT COUNT_IF(col_value < {{min_value}} OR col_value > {{max_value}})
    FROM arg_t
$$;

-- Custom DMF: Regex format check (e.g. email, phone, ID format)
-- Replace {{dmf_schema}}, {{column_name}}, {{regex_pattern}}
CREATE OR REPLACE DATA METRIC FUNCTION {{dmf_schema}}.DMF_FORMAT_CHECK_{{column_name}}(
    arg_t TABLE(col_value VARCHAR)
)
RETURNS NUMBER
AS
$$
    SELECT COUNT_IF(NOT REGEXP_LIKE(col_value, '{{regex_pattern}}') AND col_value IS NOT NULL)
    FROM arg_t
$$;

-- ============================================================
-- SECTION 2: Attach System DMFs to Table
-- System DMFs are built-in — no need to CREATE them.
-- ============================================================

-- Row count monitoring (table level)
ALTER TABLE {{database}}.{{schema}}.{{table}}
    ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.ROW_COUNT
    ON ()
    SCHEDULE = '{{schedule}}';
-- Default schedule: 'USING CRON 0 */6 * * * America/Los_Angeles'
-- Trigger on DML instead: SCHEDULE = 'TRIGGER_ON_CHANGES'

-- Freshness monitoring (timestamp column)
-- Replace {{timestamp_column}} with your most recent-update column
ALTER TABLE {{database}}.{{schema}}.{{table}}
    ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.FRESHNESS
    ON ({{timestamp_column}})
    SCHEDULE = '{{schedule}}';

-- Null count — primary key column
ALTER TABLE {{database}}.{{schema}}.{{pk_column_table}}
    ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.NULL_COUNT
    ON ({{pk_column}})
    SCHEDULE = '{{schedule}}';

-- Duplicate count — primary key column
ALTER TABLE {{database}}.{{schema}}.{{pk_column_table}}
    ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.DUPLICATE_COUNT
    ON ({{pk_column}})
    SCHEDULE = '{{schedule}}';

-- Null count — additional key columns
-- Repeat this block for each column that must be non-null
ALTER TABLE {{database}}.{{schema}}.{{table}}
    ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.NULL_COUNT
    ON ({{required_column}})
    SCHEDULE = '{{schedule}}';

-- ============================================================
-- SECTION 3: Attach Custom DMFs
-- Run AFTER Section 1 creates the custom DMFs.
-- ============================================================

-- Attach accepted values check
ALTER TABLE {{database}}.{{schema}}.{{table}}
    ADD DATA METRIC FUNCTION {{dmf_schema}}.DMF_ACCEPTED_VALUES_{{column_name}}
    ON ({{column_name}})
    SCHEDULE = '{{schedule}}';

-- Attach range check
ALTER TABLE {{database}}.{{schema}}.{{table}}
    ADD DATA METRIC FUNCTION {{dmf_schema}}.DMF_RANGE_CHECK_{{column_name}}
    ON ({{numeric_column}})
    SCHEDULE = '{{schedule}}';

-- ============================================================
-- SECTION 4: Verify Attachment
-- Run after attaching to confirm all DMFs are scheduled.
-- ============================================================

SELECT
    ref_entity_name,
    metric_name,
    schedule,
    schedule_status,
    argument_names
FROM TABLE(
    INFORMATION_SCHEMA.DATA_METRIC_FUNCTION_REFERENCES(
        REF_ENTITY_NAME => '{{database}}.{{schema}}.{{table}}',
        REF_ENTITY_DOMAIN => 'TABLE'
    )
)
ORDER BY metric_name;

-- ============================================================
-- SECTION 5: Query Results (after first DMF run)
-- ============================================================

SELECT
    measurement_time,
    table_name,
    metric_name,
    value,
    argument_names
FROM TABLE(SNOWFLAKE.LOCAL.DATA_QUALITY_MONITORING_RESULTS(
    REF_ENTITY_NAME => '{{database}}.{{schema}}.{{table}}',
    REF_ENTITY_DOMAIN => 'TABLE'
))
ORDER BY measurement_time DESC, metric_name
LIMIT 100;

-- Check expectation pass/fail status
SELECT
    measurement_time,
    metric_name,
    value,
    expectation_expression,
    expectation_violated
FROM SNOWFLAKE.LOCAL.DATA_QUALITY_MONITORING_EXPECTATION_STATUS
WHERE ref_entity_name = '{{database}}.{{schema}}.{{table}}'
ORDER BY measurement_time DESC
LIMIT 50;
