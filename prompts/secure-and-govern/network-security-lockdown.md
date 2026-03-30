# Audit Network Policies for Security Gaps

> Review network policies, find overly permissive rules, and generate a tighter config.

## The Prompt

```
Review my account's network security posture. List all current network policies and rules,
check if there are any overly permissive CIDR ranges (like 0.0.0.0/0), and verify that
all service accounts have network policies assigned. Recommend a tighter configuration
and generate the SQL to implement it. Don't execute anything destructive — just show me the plan.
```

## What This Triggers

- Network security skill invocation
- SHOW NETWORK POLICIES / SHOW NETWORK RULES enumeration
- CIDR range analysis for overly broad access
- Service account policy assignment audit
- SQL generation for tighter policies (no execution)

## Before You Run

- SECURITYADMIN or ACCOUNTADMIN role
- Existing network policies (or CoCo will note there are none)

## Tips

- Add "include my current IP in the allowlist" to avoid locking yourself out
- Say "also check for SaaS rules coverage" if you use Snowflake partner tools
- Add "assign the tighter policy to my DEV_USER account" to apply selectively
