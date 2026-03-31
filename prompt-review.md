# Prompt Review — build-with-coco

**Reviewed by:** 3-agent specialist team (data engineering, platform/governance, analytics/AI)  
**Date:** 2026-03-31  
**Files reviewed:** 15 scenario prompts + 7 role files (105 prompts)

---

## TL;DR Scorecard

| Category | Verdict |
|---|---|
| `connect-sources` | Mostly solid. 1 minor fix. |
| `build-pipelines` | Good bones. 1 misleading API reference. |
| `assess-change-impact` | Good. 1 lineage scope issue to address. |
| `monitor-quality` | Wrong view name. Fix before publishing. |
| `optimize-costs` | Both need dry-run guardrails moved to prompt body. |
| `secure-and-govern` | Governance hardening needs human-in-the-loop gate. Risk. |
| `self-serve-analytics` | Strong. 1 double-placeholder bug. |
| `ai-enrichment` | 2 API inaccuracies. Fix before publishing. |
| Role files | Uneven. Several cross-persona contaminations; a few cut candidates. |

---

## Scenario Prompts

---

### `connect-sources/openflow-postgres-replication.md`
**Verdict: Keep as-is**

Strongest prompt in the connect-sources category. CoCo is instructed to gather inputs before acting (correct pattern). Minor edge: doesn't distinguish Debezium vs polling CDC — non-blocking.

---

### `connect-sources/iceberg-external-catalog.md`
**Verdict: Needs minor fix**

Two issues:
1. `{{cloud-storage-provider}}` appears inside the prompt body as a literal. A user who pastes this verbatim sends the placeholder to CoCo. Move it to a "fill this in before running" note in Before You Run.
2. IAM trust policy setup (required before Snowflake can assume the S3 role) is a common first-timer stumbling block — mention it in Before You Run.

---

### `build-pipelines/dbt-health-check-and-deploy.md`
**Verdict: Needs minor fix**

`snow dbt deploy` is specific to Snowflake-native dbt execution (dbt Projects on Snowflake) — NOT an alias for `dbt run`. Most dbt practitioners use `dbt build`/`dbt run` against their existing project. A majority of users will hit this and be confused.

Fix: add disambiguation — "If you're on standard dbt Core (not `snow dbt`), use `dbt build` instead." Also: "What This Triggers" claims multi-agent parallel workstreams; compile → test → freshness → deploy are inherently sequential. Remove that claim.

---

### `build-pipelines/dynamic-table-pipeline.md`
**Verdict: Keep as-is (optional note)**

LATERAL FLATTEN, session window logic, 30-min gap detection, target lag — all accurate. Sequential verification pattern (verify HEALTHY before building next layer) is exactly right. Strong prompt.

Optional: add a note that session window logic in DTs has complexity trade-offs vs. streaming processors, so CoCo should surface alternatives if the pattern gets unwieldy.

---

### `assess-change-impact/lineage-impact-analysis.md`
**Verdict: Needs minor fix**

"Dashboards and apps" overpromises. Snowflake's lineage APIs (`OBJECT_DEPENDENCIES`, `ACCESS_HISTORY`) cover **Snowflake-native objects only** — views, DTs, tasks, pipes. External BI tools (Tableau, Looker, Sigma), dbt models, and external Streamlit apps are invisible to these APIs. A user expecting Tableau dashboards to appear in the impact report will be surprised.

Fix: add one sentence in Tips — "Lineage coverage is Snowflake-native objects only; external BI tool dependencies won't appear."

---

### `assess-change-impact/migration-assessment.md`
**Verdict: Keep as-is**

Clean prompt. SnowConvert complexity categories (auto/semi-auto/manual) are accurate. Generic enough for Teradata, Oracle, SQL Server.

---

### `monitor-quality/data-quality-monitoring.md`
**Verdict: Needs minor fix — broken reference**

"What This Triggers" references `DATA_QUALITY_MONITORING_RESULTS` view. The actual access path is `SNOWFLAKE.LOCAL.DATA_QUALITY_MONITORING_RESULTS(...)` or through the DMF results API — not a bare view name. Users who try to query the view by that name will get a "table not found" error immediately.

Also missing: DMF scheduling options (cron vs DML-triggered) — a key configuration decision that CoCo should gather before building.

Fix: correct the view reference; add scheduling options to what CoCo should ask for.

---

### `optimize-costs/cost-optimization-sprint.md`
**Verdict: Needs minor fix — risk**

The prompt asks CoCo to produce `ALTER WAREHOUSE ...` statements. This is good — but the dry-run guardrail ("just show me the plan") lives in the Tips section, not the prompt body. A user who doesn't read Tips could execute a remediation that downsizes a production warehouse mid-day.

Also missing: multi-cluster warehouse configs. Remediating an over-provisioned multi-cluster warehouse (reduce `MAX_CLUSTERS`) is different from single-cluster right-sizing. Enterprise users will hit this gap.

Fix: **Move the dry-run instruction into the prompt body as the default**. "Don't execute any changes — show me the plan first and wait for my approval."

---

### `optimize-costs/full-cost-governance-audit.md`
**Verdict: Needs minor fix**

Multi-agent parallel audit is a genuine CoCo power pattern. `SYSTEM$CLASSIFY` for PII detection is accurate. One issue: `SYSTEM$CLASSIFY` is slow on large schemas — running it account-wide with no scope limit can kick off a very long job.

Fix: add a scope placeholder — "limit PII scan to `{{database}}.{{schema}}`" with a note that account-wide classification on large schemas may take several minutes.

---

### `secure-and-govern/governance-hardening.md`
**Verdict: Needs minor fix — risk flag**

"Apply masking policies to any PII columns you find" means CoCo will modify column-level access in production without per-column human review. If classification produces a false positive, production queries silently return masked values instead of errors — BI dashboards go dark with no error.

The "verify before moving on" clause helps but there's no explicit human gate specifically for the masking application step.

Fix: add a mandatory confirmation checkpoint — **"Show me the list of columns and policies you plan to create. Wait for my explicit approval before applying any masking policies."** This is the difference between a supervised workflow and a risky one.

Also add: masking takes effect immediately at query time for all users — BI consumers will see `****` instead of real values as soon as the policy is applied. Mention this so users aren't caught off guard.

---

### `secure-and-govern/network-security-lockdown.md`
**Verdict: Needs minor fix**

The "Don't execute anything destructive — show me the plan" guardrail is well placed. The issue: "verify that all service accounts have network policies assigned" conflates account-level policies (`SHOW NETWORK POLICIES`) with user-level policies (queried via `SHOW USERS` + `DESCRIBE USER <name>` → `network_policy` attribute). These are different operations. CoCo may stop at `SHOW NETWORK POLICIES` and miss that a service account has no user-level policy override.

Fix: clarify the service account check means inspecting user-level `network_policy` attribute per user, not just listing account-level policies.

---

### `self-serve-analytics/semantic-view-plus-agent.md`
**Verdict: Keep / minor fix**

Solid. The "ask me which table / dimensions / measures" pattern is good prompt design. One gap: the prompt doesn't distinguish Cortex Analyst (the NL-to-SQL layer on a semantic view) from Cortex Agents (which can wrap Cortex Analyst as a tool). A user who doesn't know this will be confused why they're building both.

Fix: one parenthetical — "Cortex Analyst handles natural language queries on the semantic view; the Agent is the interface layer that calls it."

---

### `self-serve-analytics/streamlit-sales-dashboard.md`
**Verdict: Needs minor fix — bug**

Double-placeholder issue: if both `{{database.schema.table}}` and a second placeholder appear in the same prompt body as literals, they're sent verbatim to CoCo. CoCo handles this fine but it's sloppy. Consolidate into one "ask me for my table" instruction rather than using placeholders in the prompt body.

---

### `ai-enrichment/cortex-ai-ticket-enrichment.md`
**Verdict: Needs minor fix — API inaccuracy**

The Tips section says: "Specify `AI_CLASSIFY` with a `model` parameter to use a different underlying model." `AI_CLASSIFY` does **not** accept a `model` parameter — model selection is not exposed at the function level for most Cortex AI functions. This is wrong and will confuse users who try it.

Fix: remove the `model` parameter tip for `AI_CLASSIFY`.

---

### `ai-enrichment/ml-churn-prediction.md`
**Verdict: Needs minor fix — terminology and API**

Two issues:
1. The prompt references "experiment tracking" — this terminology implies MLflow-style run logging. Snowflake's Model Registry tracks model versions and metadata but doesn't expose experiment tracking in the MLflow sense. The correct framing is "register the trained model in the Model Registry."
2. `compute pool` vs `warehouse` conflation: churn model training via Snowpark ML runs on a warehouse, not a compute pool (compute pools are for SPCS container workloads). Using both interchangeably will confuse users.

Fix: replace "experiment tracking" with "Model Registry registration"; clarify warehouse vs compute pool.

---

## Role Prompt Files

---

### `roles/data-engineer/prompts.md`

**Strongest:** #1 (OpenFlow CDC), #8 (debug failing Task), #9 (DMF quality gate with thresholds), #13 (validate migration), #14 (DCM project setup)

**Cut or fix:**
- **#6 (optimize expensive pipeline)** — "Takes too long" with no schema/query context will result in 3 turns of clarifying questions before any work starts. Needs a starting anchor.
- **#12 (external tables on S3)** — Legacy pattern when Iceberg is available. Low-value in 2026; consider replacing.
- **#15 (pipeline health Streamlit app)** — Visualization is an analytics/admin concern, not a DE's primary workflow. Wrong persona.
- **#7 (full Iceberg lakehouse architecture)** — Too large as a single prompt. Will produce a vague architectural overview, not executable steps. Scope it down.

**Gaps:** No prompt for `COPY INTO` with stage transformations (one of the most common DE tasks). No batch Snowpipe prompt (vs Snowpipe Streaming in #5). No Task DAG management (resume/suspend/graph inspection at scale).

---

### `roles/analytics-engineer/prompts.md`

**Strongest:** #4 (generate dbt models from raw tables), #11 (validate semantic layer with Cortex Analyst), #13 (Type 2 SCD with DTs), #3 (trace column rename impacts), #15 (audit incremental models)

**Cut or fix:**
- **#6 (build a Dynamic Table pipeline)** — DT pipeline authoring is a data engineer task. Analytics engineers work in dbt. Wrong persona.
- **#9 (migrate dbt Core to snow dbt deploy)** — Needs more grounding; produces generic trade-offs discussion without actionable migration steps.
- **#14 (data drift between environments)** — Mixing row count drift and NULL rate drift in one pass produces unfocused output. Scope more tightly.

**Gaps:** No VQR (Verified Query Representation) generation/testing prompt. No `dbt source freshness` workflow. No `dbt test` failure investigation beyond #5 (duplicate keys). No dbt exposures / documenting downstream consumers.

---

### `roles/data-analyst/prompts.md`

**Strongest:** Cohort retention analysis, funnel analysis, ad-hoc SQL → Cortex Analyst migration

**Cut:**
- **#13** — No-op prompt (asks CoCo to "run a query" with no context, will immediately ask for everything upfront). Remove.
- **#15** — Contains a broken `[upload/describe]` placeholder that will confuse CoCo. Fix or cut.

**Gaps:** No prompt for working with shared data (Marketplace or internal listings). No natural language to SQL via Cortex Analyst as a standalone workflow.

---

### `roles/ai-ml-engineer/prompts.md`

**Strongest:** Document processing pipeline, batch inference with Snowpark ML, Cortex Agent with RAG

**Cut or fix:**
- **#14** — References `CLASSIFY_TEXT` which is deprecated; current function is `AI_CLASSIFY`. Wrong.
- **#12** — Describes "fine-tuning" a Cortex model. Cortex LLM functions don't support fine-tuning; the correct concept is prompt engineering or model selection via `AI_COMPLETE`. Wrong framing.

**API fix:** Several prompts reference `EMBED_TEXT` — the correct function signatures are `EMBED_TEXT_768` and `EMBED_TEXT_1024` (dimension-specific). `EMBED_TEXT` alone doesn't resolve.

**Gaps:** No prompt for using `AI_FILTER` for dataset labeling / pre-filtering. No prompt for vector search with Cortex Search.

---

### `roles/app-developer/prompts.md`

**Strongest:** Fix SHOW command error (common SiS gotcha), build Native App with trial experience, Streamlit component debugging

**Cut or fix:**
- **#11** — References `EMBED_TEXT` (see above — should be `EMBED_TEXT_768` or `EMBED_TEXT_1024`).
- **#14** — "Take a browser screenshot" pattern doesn't work for apps deployed inside Snowflake (SiS). Remove or scope to local dev only.

**Gaps:** No prompt for Native App installation/upgrade workflows from the consumer side. No prompt for Snowflake CLI app deployment (`snow app run`).

---

### `roles/snowflake-admin/prompts.md`

**Strongest:** #2 (find over-provisioned warehouses — technically precise: <20% utilization, <2 concurrency), #15 (warehouse rightsizing — exact views named, projected savings), #13 (investigate credit spike — multi-source incident response), #11 (privilege drift audit — specific patterns named), #10 (cross-account org reporting)

**Cut or fix:**
- **#5 (set up an integration)** — Lists four completely different integrations (Kafka / S3 / Azure Event Hub / notification service) separated by slashes. CoCo will immediately ask "which one?" — unusable as-is. Split into separate prompts or cut.
- **#6 + #12** — Near-duplicates. Both query ACCOUNT_USAGE grouped by warehouse/role/user for credit attribution. Consolidate.

**Gaps:** No user management prompt (bulk creation, login/password policies, MFA enforcement). No replication/failover group configuration. No Task graph admin at scale (suspend entire DAGs, find runaway tasks).

---

### `roles/data-governance-lead/prompts.md`

**Strongest:** #1 (full PII classification with `SYSTEM$CLASSIFY`), #11 (tag-based masking at scale — architecturally correct pattern), #13 (privilege escalation detection — precise query targets), #7 (lineage audit trail for sensitive data), #14 (column-level PII lineage)

**Cut or fix:**
- **#5 (DMF setup)** — DMF infrastructure setup is a data engineer task. A governance lead reads DMF results for compliance; they don't build the DMF. Wrong persona. Move to DE role or the monitor-quality scenario.
- **#10 + #6 + #9** — Three prompts that amount to "give me a governance posture summary." Redundant. Consolidate into one.
- **#15 (generate data contracts as YAML)** — YAML data contracts are not a native Snowflake concept. The output is documentation, not a deployable artifact — but the prompt implies CoCo creates something functional. Add a clear disclaimer or cut it.

**Gaps:** No prompt for projection policies (different from masking — prevents column from appearing in `SELECT *` results entirely). No object tagging workflow beyond masking. No data residency / cross-region compliance prompt (a major gap for Healthcare and Public Sector users).

---

## Priority Fix List

| Priority | File | Issue |
|---|---|---|
| P0 | `ai-enrichment/cortex-ai-ticket-enrichment.md` | `AI_CLASSIFY` doesn't accept `model` param — will confuse users |
| P0 | `monitor-quality/data-quality-monitoring.md` | Wrong DMF results view name — will fail immediately |
| P0 | `roles/ai-ml-engineer/prompts.md` #14 | `CLASSIFY_TEXT` is deprecated |
| P0 | `roles/ai-ml-engineer/prompts.md` #12 | "Fine-tuning" is factually wrong for Cortex LLMs |
| P1 | `secure-and-govern/governance-hardening.md` | Missing human-in-the-loop gate before applying masking (risk) |
| P1 | `optimize-costs/cost-optimization-sprint.md` | Dry-run guardrail stuck in Tips — move to prompt body |
| P1 | `build-pipelines/dbt-health-check-and-deploy.md` | `snow dbt deploy` vs `dbt run` confusion |
| P1 | `roles/snowflake-admin/prompts.md` #5 | Four different integrations in one prompt — unusable |
| P2 | `connect-sources/iceberg-external-catalog.md` | `{{placeholder}}` in prompt body; IAM trust policy gap |
| P2 | `assess-change-impact/lineage-impact-analysis.md` | External BI tools won't appear in lineage results |
| P2 | `ai-enrichment/ml-churn-prediction.md` | "Experiment tracking" misnaming; compute pool vs warehouse |
| P2 | `roles/ai-ml-engineer/prompts.md` | `EMBED_TEXT` → `EMBED_TEXT_768`/`EMBED_TEXT_1024` |
| P2 | `roles/data-governance-lead/prompts.md` #5 | Wrong persona — DMF setup is a DE task |
| P3 | `optimize-costs/full-cost-governance-audit.md` | Add scope placeholder for SYSTEM$CLASSIFY |
| P3 | `monitor-quality/data-quality-monitoring.md` | Add DMF scheduling options to what CoCo gathers |
| P3 | `self-serve-analytics/streamlit-sales-dashboard.md` | Double-placeholder in prompt body |
| P3 | `roles/snowflake-admin/prompts.md` #6+#12 | Near-duplicate credit attribution prompts — consolidate |
| P3 | `secure-and-govern/network-security-lockdown.md` | Account-level vs user-level policy conflation |
