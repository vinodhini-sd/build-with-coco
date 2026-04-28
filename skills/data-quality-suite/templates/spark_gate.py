# PySpark Quality Gate Template
# Replace {{placeholder}} values before using.
# Drop this file into your pipeline directory as spark_quality_gate.py
# Usage: from spark_quality_gate import assert_quality

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from typing import Any


class QualityGateError(Exception):
    """Raised when a quality check fails. Pipeline should halt."""
    pass


def assert_quality(
    df: DataFrame,
    table_name: str,
    checks: dict[str, dict[str, Any]],
) -> DataFrame:
    """
    Run data quality checks on a PySpark DataFrame before writing.

    Args:
        df:         PySpark DataFrame to check (before write)
        table_name: Human-readable name for error messages
        checks:     Dict of column_name -> check_config

    Check config keys:
        null_pct (float):      Max allowed null percentage (0.0 = zero nulls, 5.0 = 5%)
        duplicate_pct (float): Max allowed duplicate percentage (0.0 = no duplicates)
        min (number):          Minimum allowed value (inclusive)
        max (number):          Maximum allowed value (inclusive)
        values (set):          Allowed categorical values
        min (int) via __row_count__: Minimum row count for the full table

    Returns:
        The original DataFrame unchanged (pass-through for chaining).

    Raises:
        QualityGateError: If any check fails. Pipeline halts.

    Example:
        df = transform(raw_df)
        assert_quality(df, "silver.orders", checks={
            "__row_count__": {"min": 1},
            "order_id":      {"null_pct": 0, "duplicate_pct": 0},
            "customer_id":   {"null_pct": 0},
            "status":        {"null_pct": 0, "values": {"pending","shipped","delivered"}},
            "order_value":   {"null_pct": 0, "min": 0},
        })
        df.write.format("delta").saveAsTable("silver.orders")
    """
    failures = []
    total_rows = df.count()

    # ── ROW COUNT CHECK ───────────────────────────────────────
    row_count_check = checks.get("__row_count__", {})
    if "min" in row_count_check:
        if total_rows < row_count_check["min"]:
            failures.append(
                f"[{table_name}] row_count = {total_rows} "
                f"(expected >= {row_count_check['min']})"
            )

    if total_rows == 0:
        # Skip column checks on empty DataFrame — all would trivially pass
        if failures:
            raise QualityGateError(
                f"Quality gate FAILED for {table_name}:\n  " + "\n  ".join(failures)
            )
        return df

    # ── COLUMN-LEVEL CHECKS ───────────────────────────────────
    for col_name, col_checks in checks.items():
        if col_name == "__row_count__":
            continue

        # Verify column exists
        if col_name not in df.columns:
            failures.append(f"[{table_name}] Column '{col_name}' not found in DataFrame schema")
            continue

        col = F.col(col_name)

        # NULL PERCENTAGE CHECK
        if "null_pct" in col_checks:
            null_count = df.filter(col.isNull()).count()
            actual_pct = (null_count / total_rows) * 100
            if actual_pct > col_checks["null_pct"]:
                failures.append(
                    f"[{table_name}][{col_name}] null_pct = {actual_pct:.2f}% "
                    f"(threshold: <= {col_checks['null_pct']}%)"
                )

        # DUPLICATE PERCENTAGE CHECK
        if "duplicate_pct" in col_checks:
            distinct_count = df.select(col_name).dropDuplicates().count()
            dupe_count = total_rows - distinct_count
            actual_pct = (dupe_count / total_rows) * 100
            if actual_pct > col_checks["duplicate_pct"]:
                failures.append(
                    f"[{table_name}][{col_name}] duplicate_pct = {actual_pct:.2f}% "
                    f"({dupe_count} duplicate rows, threshold: <= {col_checks['duplicate_pct']}%)"
                )

        # MIN VALUE CHECK
        if "min" in col_checks:
            actual_min = df.agg(F.min(col)).collect()[0][0]
            if actual_min is not None and actual_min < col_checks["min"]:
                failures.append(
                    f"[{table_name}][{col_name}] min_value = {actual_min} "
                    f"(expected >= {col_checks['min']})"
                )

        # MAX VALUE CHECK
        if "max" in col_checks:
            actual_max = df.agg(F.max(col)).collect()[0][0]
            if actual_max is not None and actual_max > col_checks["max"]:
                failures.append(
                    f"[{table_name}][{col_name}] max_value = {actual_max} "
                    f"(expected <= {col_checks['max']})"
                )

        # MEAN CHECK (distribution bounds)
        if "mean_min" in col_checks or "mean_max" in col_checks:
            actual_mean = df.agg(F.mean(col)).collect()[0][0]
            if actual_mean is not None:
                if "mean_min" in col_checks and actual_mean < col_checks["mean_min"]:
                    failures.append(
                        f"[{table_name}][{col_name}] mean = {actual_mean:.4f} "
                        f"(expected >= {col_checks['mean_min']} — possible feature drift)"
                    )
                if "mean_max" in col_checks and actual_mean > col_checks["mean_max"]:
                    failures.append(
                        f"[{table_name}][{col_name}] mean = {actual_mean:.4f} "
                        f"(expected <= {col_checks['mean_max']} — possible feature drift)"
                    )

        # ACCEPTED VALUES CHECK
        if "values" in col_checks:
            allowed = set(str(v) for v in col_checks["values"])
            invalid_df = (
                df.filter(col.isNotNull())
                  .filter(~col.isin(list(allowed)))
            )
            invalid_count = invalid_df.count()
            if invalid_count > 0:
                sample_values = [
                    r[col_name] for r in invalid_df.select(col_name).limit(5).collect()
                ]
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
