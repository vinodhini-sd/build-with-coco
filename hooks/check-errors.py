#!/usr/bin/env python3
"""
Session start error checker for Cortex Code.
Checks your Snowflake account(s) for failures across:
  - Snowflake tasks
  - Snowflake alerts
  - Dynamic table refreshes
  - Copy/pipe loads
  - GitHub PRs with failing CI
  - Airflow DAG import errors

Uses PAT auth via env vars — no browser prompt.
Silent if all clear; prints an Alerts block if anything needs attention.

Required env vars:
  COCO_SF_ACCOUNT    Snowflake account identifier (e.g. myorg-myaccount)
  COCO_SF_USER       Snowflake username
  COCO_SF_WAREHOUSE  Snowflake warehouse to use for queries
  COCO_SF_PAT        Snowflake Programmatic Access Token
                     (store with: cortex secret store COCO_SF_PAT --prompt)

Optional — second Snowflake account (e.g. a separate data platform account):
  COCO_SF_ACCOUNT_2
  COCO_SF_USER_2
  COCO_SF_WAREHOUSE_2
  COCO_SF_PAT_2

Optional — Airflow (defaults to localhost:8080):
  AIRFLOW_API_URL
  AIRFLOW_USER
  AIRFLOW_PASSWORD
"""

import json
import os
import subprocess
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor

DIVIDER = "─" * 56

# Primary Snowflake account — required
ACCOUNT   = os.environ.get("COCO_SF_ACCOUNT", "")
USER      = os.environ.get("COCO_SF_USER", "")
WAREHOUSE = os.environ.get("COCO_SF_WAREHOUSE", "")

# Secondary Snowflake account — optional
ACCOUNT_2   = os.environ.get("COCO_SF_ACCOUNT_2", "")
USER_2      = os.environ.get("COCO_SF_USER_2", "")
WAREHOUSE_2 = os.environ.get("COCO_SF_WAREHOUSE_2", "")


def _connect():
    """Return a Snowflake connector for the primary account or None on failure."""
    pat = os.environ.get("COCO_SF_PAT", "").strip()
    if not pat or not ACCOUNT or not USER:
        return None
    try:
        import snowflake.connector
        conn = snowflake.connector.connect(
            account=ACCOUNT,
            user=USER,
            authenticator="programmatic_access_token",
            token=pat,
            warehouse=WAREHOUSE,
            login_timeout=10,
        )
        return conn
    except Exception:
        return None


def _connect_2():
    """Return a Snowflake connector for the secondary account or None on failure."""
    pat = os.environ.get("COCO_SF_PAT_2", "").strip()
    if not pat or not ACCOUNT_2 or not USER_2:
        return None
    try:
        import snowflake.connector
        conn = snowflake.connector.connect(
            account=ACCOUNT_2,
            user=USER_2,
            authenticator="programmatic_access_token",
            token=pat,
            warehouse=WAREHOUSE_2,
            login_timeout=10,
        )
        return conn
    except Exception:
        return None


def _query(conn, sql):
    """Run a query and return list of dicts. Empty list on any error."""
    try:
        import snowflake.connector
        cur = conn.cursor(snowflake.connector.DictCursor)
        cur.execute(sql)
        return cur.fetchall()
    except Exception:
        return []


def check_task_failures(conn):
    """Account-wide task failures in last 24h."""
    rows = _query(conn, """
        SELECT
            DATABASE_NAME || '.' || SCHEMA_NAME || '.' || NAME AS task_name,
            LEFT(COALESCE(ERROR_MESSAGE, ''), 120) AS error_message,
            TO_CHAR(SCHEDULED_TIME, 'HH24:MI Mon DD') AS when_failed
        FROM SNOWFLAKE.ACCOUNT_USAGE.TASK_HISTORY
        WHERE STATE = 'FAILED'
          AND SCHEDULED_TIME >= DATEADD('hours', -24, CURRENT_TIMESTAMP())
        ORDER BY SCHEDULED_TIME DESC
        LIMIT 10
    """)
    return rows


def check_alert_failures(conn):
    """Alerts that failed in last 24h."""
    rows = _query(conn, """
        SELECT
            DATABASE_NAME || '.' || SCHEMA_NAME || '.' || NAME AS alert_name,
            STATE,
            LEFT(COALESCE(ERROR_MESSAGE, ''), 120) AS error_message,
            TO_CHAR(COMPLETED_TIME, 'HH24:MI Mon DD') AS when_failed
        FROM SNOWFLAKE.ACCOUNT_USAGE.ALERT_HISTORY
        WHERE STATE IN ('FAILED', 'CONDITION_FAILED', 'ACTION_FAILED')
          AND COMPLETED_TIME >= DATEADD('hours', -24, CURRENT_TIMESTAMP())
        ORDER BY COMPLETED_TIME DESC
        LIMIT 10
    """)
    return rows


def check_dynamic_table_failures(conn):
    """Dynamic table refresh failures in last 6h (view has up to 3h latency)."""
    rows = _query(conn, """
        SELECT
            DATABASE_NAME || '.' || SCHEMA_NAME || '.' || NAME AS table_name,
            STATE,
            LEFT(COALESCE(STATE_MESSAGE, ''), 120) AS state_message,
            TO_CHAR(REFRESH_START_TIME, 'HH24:MI Mon DD') AS when_failed
        FROM SNOWFLAKE.ACCOUNT_USAGE.DYNAMIC_TABLE_REFRESH_HISTORY
        WHERE STATE IN ('FAILED', 'UPSTREAM_FAILED')
          AND REFRESH_START_TIME >= DATEADD('hours', -6, CURRENT_TIMESTAMP())
        ORDER BY REFRESH_START_TIME DESC
        LIMIT 10
    """)
    return rows


def check_copy_failures(conn):
    """Copy/pipe load failures in last 24h."""
    rows = _query(conn, """
        SELECT
            COALESCE(PIPE_NAME, TABLE_NAME) AS object_name,
            STATUS,
            LEFT(COALESCE(FIRST_ERROR_MESSAGE, ''), 120) AS error_message,
            TO_CHAR(LAST_LOAD_TIME, 'HH24:MI Mon DD') AS when_failed,
            ERROR_COUNT,
            ROW_COUNT
        FROM SNOWFLAKE.ACCOUNT_USAGE.COPY_HISTORY
        WHERE STATUS = 'Load failed'
          AND LAST_LOAD_TIME >= DATEADD('hours', -24, CURRENT_TIMESTAMP())
        ORDER BY LAST_LOAD_TIME DESC
        LIMIT 10
    """)
    return rows


AIRFLOW_API_URL  = os.environ.get("AIRFLOW_API_URL", "http://localhost:8080")
AIRFLOW_USER     = os.environ.get("AIRFLOW_USER", "admin")
AIRFLOW_PASSWORD = os.environ.get("AIRFLOW_PASSWORD", "admin")


def check_airflow_dag_errors():
    """Return list of DAG import errors from local Airflow. Empty list on any error."""
    try:
        import base64
        url = f"{AIRFLOW_API_URL}/api/v1/importErrors?limit=10"
        creds = base64.b64encode(f"{AIRFLOW_USER}:{AIRFLOW_PASSWORD}".encode()).decode()
        req = urllib.request.Request(url, headers={"Authorization": f"Basic {creds}"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
        errors = data.get("import_errors", [])
        return [
            {
                "filename": e.get("filename", "unknown"),
                "stack_trace": e.get("stack_trace", ""),
            }
            for e in errors
        ]
    except Exception:
        return []


def check_github_prs():
    """Return list of open PRs with failing CI. Fetches CI status in parallel."""
    try:
        result = subprocess.run(
            [
                "gh", "search", "prs",
                "--author", "@me",
                "--state", "open",
                "--limit", "20",
                "--json", "title,url,repository,number",
            ],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode != 0:
            return []
        prs = json.loads(result.stdout)

        def fetch_ci(pr):
            repo = pr.get("repository", {}).get("nameWithOwner", "")
            number = pr.get("number")
            if not repo or not number:
                return None
            ci_result = subprocess.run(
                ["gh", "pr", "view", str(number), "--repo", repo,
                 "--json", "title,url,statusCheckRollup"],
                capture_output=True, text=True, timeout=8,
            )
            if ci_result.returncode != 0:
                return None
            pr_data = json.loads(ci_result.stdout)
            checks = pr_data.get("statusCheckRollup") or []
            if any(
                c.get("state") in ("FAILURE", "ERROR")
                or c.get("conclusion") in ("FAILURE", "TIMED_OUT")
                for c in checks
            ):
                return pr_data
            return None

        with ThreadPoolExecutor(max_workers=8) as ex:
            results = list(ex.map(fetch_ci, prs))
        return [r for r in results if r]
    except Exception:
        return []


def format_alerts(task_failures, alert_failures, dt_failures, copy_failures,
                  pr_failures, airflow_errors=None):
    airflow_errors = airflow_errors or []
    total = sum([
        len(task_failures), len(alert_failures),
        len(dt_failures), len(copy_failures), len(pr_failures), len(airflow_errors)
    ])
    if total == 0:
        return ""

    lines = [
        f"\n{DIVIDER}",
        "  ! Alerts — needs your attention",
        DIVIDER,
    ]

    if task_failures:
        lines.append(f"\n  Snowflake Tasks  ({len(task_failures)} failed in last 24h)\n")
        for t in task_failures:
            name = t.get("TASK_NAME") or t.get("task_name", "unknown")
            when = t.get("WHEN_FAILED") or t.get("when_failed", "")
            msg  = t.get("ERROR_MESSAGE") or t.get("error_message", "")
            lines.append(f"    ! {name}")
            if when: lines.append(f"      Failed at {when}")
            if msg:  lines.append(f"      {msg.strip()[:100]}")
            lines.append("")

    if alert_failures:
        lines.append(f"  Snowflake Alerts  ({len(alert_failures)} failed in last 24h)\n")
        for a in alert_failures:
            name  = a.get("ALERT_NAME") or a.get("alert_name", "unknown")
            state = a.get("STATE") or a.get("state", "")
            when  = a.get("WHEN_FAILED") or a.get("when_failed", "")
            msg   = a.get("ERROR_MESSAGE") or a.get("error_message", "")
            lines.append(f"    ! {name}  [{state}]")
            if when: lines.append(f"      Failed at {when}")
            if msg:  lines.append(f"      {msg.strip()[:100]}")
            lines.append("")

    if dt_failures:
        lines.append(f"  Dynamic Tables  ({len(dt_failures)} failed in last 6h)\n")
        for d in dt_failures:
            name  = d.get("TABLE_NAME") or d.get("table_name", "unknown")
            state = d.get("STATE") or d.get("state", "")
            when  = d.get("WHEN_FAILED") or d.get("when_failed", "")
            msg   = d.get("STATE_MESSAGE") or d.get("state_message", "")
            lines.append(f"    ! {name}  [{state}]")
            if when: lines.append(f"      Failed at {when}")
            if msg:  lines.append(f"      {msg.strip()[:100]}")
            lines.append("")

    if copy_failures:
        lines.append(f"  Copy/Pipe Loads  ({len(copy_failures)} failed in last 24h)\n")
        for c in copy_failures:
            name   = c.get("OBJECT_NAME") or c.get("object_name", "unknown")
            when   = c.get("WHEN_FAILED") or c.get("when_failed", "")
            msg    = c.get("ERROR_MESSAGE") or c.get("error_message", "")
            errors = c.get("ERROR_COUNT") or c.get("error_count", "")
            lines.append(f"    ! {name}  ({errors} errors)")
            if when: lines.append(f"      Failed at {when}")
            if msg:  lines.append(f"      {msg.strip()[:100]}")
            lines.append("")

    if pr_failures:
        lines.append(f"  GitHub PRs  ({len(pr_failures)} with failing CI)\n")
        for pr in pr_failures:
            lines.append(f"    ! {pr.get('title', 'untitled')}")
            lines.append(f"      {pr.get('url', '')}")
            lines.append("")

    if airflow_errors:
        lines.append(f"  Airflow DAGs  ({len(airflow_errors)} import errors)\n")
        for e in airflow_errors:
            fname   = e.get("filename", "unknown")
            short   = fname.split("/")[-1]
            trace   = e.get("stack_trace", "")
            summary = next(
                (ln.strip() for ln in reversed(trace.splitlines()) if ln.strip()), ""
            )
            lines.append(f"    ! {short}")
            if summary: lines.append(f"      {summary[:100]}")
            lines.append("")

    lines.append(DIVIDER)
    return "\n".join(lines)


def main():
    import snowflake.connector

    # Each function opens its own connection so threads don't share state
    def primary_checks():
        conn = _connect()
        if not conn:
            return [], [], [], []
        try:
            return (
                check_task_failures(conn),
                check_alert_failures(conn),
                check_dynamic_table_failures(conn),
                check_copy_failures(conn),
            )
        finally:
            conn.close()

    def secondary_checks():
        conn = _connect_2()
        if not conn:
            return []
        try:
            return check_task_failures(conn)
        finally:
            conn.close()

    # All four check groups run in parallel
    with ThreadPoolExecutor(max_workers=4) as ex:
        f_primary   = ex.submit(primary_checks)
        f_secondary = ex.submit(secondary_checks)
        f_github    = ex.submit(check_github_prs)
        f_airflow   = ex.submit(check_airflow_dag_errors)

        task_failures, alert_failures, dt_failures, copy_failures = f_primary.result()
        secondary_task_failures = f_secondary.result()
        pr_failures    = f_github.result()
        airflow_errors = f_airflow.result()

    all_task_failures = task_failures + secondary_task_failures

    output = format_alerts(all_task_failures, alert_failures, dt_failures,
                           copy_failures, pr_failures, airflow_errors)
    if output:
        print(output)


if __name__ == "__main__":
    main()
