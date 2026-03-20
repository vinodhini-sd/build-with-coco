---
name: know-your-data
description: "Discover data you already have access to in a Snowflake account, understand what it contains, and map it to your roles. Use when: searching for data, exploring your account, understanding available tables, what data do I have, what can I query, data discovery, know my data, explore my account, what tables exist, help me find data. Triggers: know your data, know my data, find data, data discovery, explore account, what data, what tables, what can I access, discover data, search tables."
tools: ["Bash", "snowflake_sql_execute", "ask_user_question"]
---

# Know Your Data

Discover data in a Snowflake account, map it to the user's roles, and identify who can grant missing access.

## Workflow

```
Ask what data & analysis needed
        |
Search Snowflake for matching tables/views
        |
Get user identity, roles, and warehouse
        |
For each candidate table:
  - Try access with each user role
  - Record: accessible (role) or blocked (needed role)
        |
For blocked tables:
  - Find owning role
  - Find role admins/grantors
        |
Present access report + contact list
```

### Step 1: Gather Requirements

**Ask the user** (use AskUserQuestion tool):

1. **What data are you looking for?** (e.g., "customer feedback", "sales pipeline", "product usage metrics")
2. **What analysis do you want to perform?** (e.g., "sentiment analysis on community feedback", "quarterly revenue trends")

From the answers, extract **3-5 search keywords** to use in Step 2.

If the user already stated what they need in the conversation, skip asking and extract keywords directly.

**Output:** List of search keywords.

### Step 2: Search for Data

Run searches **in parallel** using multiple keyword variations:

```sql
-- Via cortex CLI (preferred, uses Snowscope semantic search):
cortex search object "<keyword>" --types=table,view

-- Also try related terms. For "community feedback" also search:
-- "community", "feedback", "reviews", "survey", etc.
```

**Also search for databases** that match the domain:
```sql
SHOW DATABASES LIKE '%<KEYWORD>%';
```

**Collect** all candidate objects. Deduplicate. Rank by relevance:
- Exact name match > partial match > comment match
- Prefer tables with more rows over empty tables
- Prefer tables in non-TEMP databases

**Output:** Ranked list of candidate tables with their fully qualified names, column summaries, and row counts.

**STOP**: Present top 5-10 candidates to user. Ask: "Which of these look relevant? Should I search for anything else?"

### Step 3: Get User Identity & Roles

Run **in parallel**:

```sql
-- 1. Current user and session info
SELECT CURRENT_USER() AS "USER", CURRENT_ROLE() AS "ROLE", CURRENT_WAREHOUSE() AS "WAREHOUSE";

-- 2. All roles granted to user
SHOW GRANTS TO USER <username>;

-- 3. Available warehouses (needed for queries)
SHOW WAREHOUSES;
```

**Parse the results:**
- Extract all roles (filter for `granted_on = 'ROLE'` rows)
- Note which roles were granted by whom (the `granted_by` column)
- Identify usable warehouses

**Output:** User identity, list of roles, available warehouses.

### Step 4: Test Access Per Table

For each candidate table from Step 2, determine access:

**4a. Try DESCRIBE with each user role:**

```sql
USE ROLE <role>;
USE WAREHOUSE <warehouse>;
DESCRIBE TABLE <database>.<schema>.<table>;
```

If DESCRIBE succeeds, the table is **accessible** via that role. Also run:
```sql
SELECT COUNT(*) FROM <database>.<schema>.<table>;
```
to confirm query access and get row count.

**4b. If no role works**, find who owns the table:

```sql
-- Check table owner from SHOW TABLES output (already captured in Step 2)
-- The 'owner' column shows the owning role
```

**4c. Check if the owning role is in the user's role hierarchy:**

```sql
SHOW GRANTS TO ROLE <owning_role>;
-- Look for parent roles the user might have
```

**Categorize each table:**

| Category | Meaning |
|----------|---------|
| ACCESSIBLE | User can query via one of their roles |
| NEEDS_ROLE | User needs a specific role they don't have |
| UNKNOWN | Cannot determine access path |

**Output:** Access matrix: table -> category -> role needed -> owning role.

### Step 5: Find Role Admins

For each role the user **needs but doesn't have**:

```sql
-- Find who can grant the role (who has it with GRANT OPTION, or who is admin)
SHOW GRANTS OF ROLE <needed_role>;

-- Find SECURITYADMIN holders (they can grant any role)
SHOW GRANTS OF ROLE SECURITYADMIN;

-- Find USERADMIN holders (they can manage users/roles)
SHOW GRANTS OF ROLE USERADMIN;

-- If the role was granted by a specific admin role, find holders of that role
SHOW GRANTS OF ROLE <granting_admin_role>;
```

**Extract** actual usernames (filter `granted_to = 'USER'`) for each admin role.

**Output:** For each needed role: list of people who can grant it.

### Step 6: Present Access Report

Present a structured report with these sections:

---

**Section 1: Your Identity**
- User, account, connection name

**Section 2: Your Roles**
| Role | Granted By |
|------|-----------|
| ... | ... |

**Section 3: Data You CAN Access**
| Table | Role to Use | Rows | Description |
|-------|------------|------|-------------|
| DB.SCHEMA.TABLE | ROLE_NAME | 1,234 | Column summary |

Include a **Quick Start** SQL block:
```sql
USE ROLE <best_role>;
USE WAREHOUSE <warehouse>;
SELECT * FROM <table> LIMIT 10;
```

**Section 4: Data You NEED Access To**
| Table | Owning Role | Role You Need | Who to Contact |
|-------|------------|---------------|---------------|
| DB.SCHEMA.TABLE | OWNER_ROLE | NEEDED_ROLE | user1, user2, user3 |

**Section 5: Recommended Next Steps**
- Which admin to contact first (prefer the role's direct grantor over SECURITYADMIN)
- Suggested message template for requesting access

---

**STOP**: Ask user if they want to:
1. Query the accessible data now
2. Get more detail on any specific table
3. Search for additional data

## Stopping Points

- After Step 2: Confirm the right tables were found
- After Step 6: Review report, decide next action

## Notes

- Always use `cortex search object` first (semantic search) before falling back to SHOW/LIKE queries
- Run independent queries in parallel to minimize wait time
- Some tables may be accessible via role hierarchy even if not directly granted -- check parent roles
- SECURITYADMIN can grant any role, but prefer contacting the specific role's admin first
- If warehouse access fails, try `SHOW WAREHOUSES` with different roles to find one that works
- Cache role and warehouse info across steps to avoid redundant queries
