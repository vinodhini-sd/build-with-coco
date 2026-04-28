# Snowpark Quality Gate Template
# Replace {{placeholder}} values before using.
# Drop this file into your pipeline directory as quality_gate.py
# Usage: from quality_gate import quality_gate

from snowflake.snowpark import Session
from snowflake.snowpark import DataFrame
from snowflake.snowpark import functions as F
from typing import Any


class QualityGateError(Exception):
    """Raised when a quality check fails. Pipeline should halt."""
    pass


def quality_gate(
    session: Session,
    df: DataFrame,
    table_name: str,
    checks: dict[str, dict[str, Any]],
) -> DataFrame:
    """
    Run data quality checks on a Snowpark DataFrame before writing.

    Args:
        session:    Active Snowflake session
        df:         DataFrame to check (before write)
        table_name: Human-readable name for error messages
        checks:     Dict of column_name -> check_config

    Check config keys:
        nulls (int):      Max allowed null count. 0 = zero nulls allowed.
        duplicates (int): Max allowed duplicate count. 0 = no duplicates.
        min (number):     Minimum allowed value (inclusive).
        max (number):     Maximum allowed value (inclusive).
        values (set):     Allowed categorical values.
        min_rows (int):   Minimum row count for the full table.

    Returns:
        The original DataFrame unchanged (pass-through for chaining).

    Raises:
        QualityGateError: If any check fails. Pipeline halts.

    Example:
        df = transform(raw_df)
        quality_gate(session, df, "ORDERS_CLEAN", checks={
            "__row_count__":  {"min_rows": 1},
            "order_id":       {"nulls": 0, "duplicates": 0},
            "customer_id":    {"nulls": 0},
            "status":         {"nulls": 0, "values": {"pending","shipped","delivered"}},
            "order_value":    {"nulls": 0, "min": 0},
        })
        df.write.save_as_table("MY_DB.SILVER.ORDERS_CLEAN")
    """
    failures = []

    # ── ROW COUNT CHECK ───────────────────────────────────────
    row_count_check = checks.get("__row_count__", {})
    if "min_rows" in row_count_check:
        actual_count = df.count()
        if actual_count < row_count_check["min_rows"]:
            failures.append(
                f"[{table_name}] row_count = {actual_count} "
                f"(expected >= {row_count_check['min_rows']})"
            )

    # ── COLUMN-LEVEL CHECKS ───────────────────────────────────
    for col_name, col_checks in checks.items():
        if col_name == "__row_count__":
            continue

        # Verify column exists
        if col_name not in [c.name.upper() for c in df.schema]:
            failures.append(f"[{table_name}] Column '{col_name}' not found in DataFrame schema")
            continue

        col = F.col(col_name)

        # NULL CHECK
        if "nulls" in col_checks:
            null_count = df.filter(col.isNull()).count()
            if null_count > col_checks["nulls"]:
                failures.append(
                    f"[{table_name}][{col_name}] null_count = {null_count} "
                    f"(threshold: <= {col_checks['nulls']})"
                )

        # DUPLICATE CHECK
        if "duplicates" in col_checks:
            total = df.count()
            distinct = df.select(col_name).dropDuplicates().count()
            dupe_count = total - distinct
            if dupe_count > col_checks["duplicates"]:
                failures.append(
                    f"[{table_name}][{col_name}] duplicate_count = {dupe_count} "
                    f"(threshold: <= {col_checks['duplicates']})"
                )

        # MIN VALUE CHECK
        if "min" in col_checks:
            actual_min = df.select(F.min(col)).collect()[0][0]
            if actual_min is not None and actual_min < col_checks["min"]:
                failures.append(
                    f"[{table_name}][{col_name}] min_value = {actual_min} "
                    f"(expected >= {col_checks['min']})"
                )

        # MAX VALUE CHECK
        if "max" in col_checks:
            actual_max = df.select(F.max(col)).collect()[0][0]
            if actual_max is not None and actual_max > col_checks["max"]:
                failures.append(
                    f"[{table_name}][{col_name}] max_value = {actual_max} "
                    f"(expected <= {col_checks['max']})"
                )

        # ACCEPTED VALUES CHECK
        if "values" in col_checks:
            allowed = set(str(v) for v in col_checks["values"])
            invalid_count = (
                df.filter(col.isNotNull())
                  .filter(~col.isin(list(allowed)))
                  .count()
            )
            if invalid_count > 0:
                # Show a sample of invalid values for debugging
                invalid_sample = (
                    df.filter(col.isNotNull())
                      .filter(~col.isin(list(allowed)))
                      .select(col_name)
                      .limit(5)
                      .collect()
                )
                sample_values = [r[0] for r in invalid_sample]
                failures.append(
                    f"[{table_name}][{col_name}] {invalid_count} rows with unexpected values. "
                    f"Sample: {sample_values}. Allowed: {sorted(allowed)}"
                )

    # ── RESULT ────────────────────────────────────────────────
    if failures:
        failure_report = "\n  ".join(failures)
        raise QualityGateError(
            f"Quality gate FAILED for {table_name}. "
            f"{len(failures)} check(s) failed:\n  {failure_report}"
        )

    return df  # pass-through for chaining
