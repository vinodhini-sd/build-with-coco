#!/usr/bin/env python3
"""
What's New helper for Cortex Code SessionStart hook.
Diffs bundled skills/plugins between CoCo versions and generates
personalized recommendations based on conversation history and
user retention patterns (churn/returning/power user signals).

Reference: ~/Documents/devrel/analysis/coco_user_patterns_reference.md
"""

import json
import os
import re
from collections import Counter
from pathlib import Path

CORTEX_DATA_DIR = Path.home() / ".local" / "share" / "cortex"
CONVO_DIR = Path.home() / ".snowflake" / "cortex" / "conversations"
MAX_CONVOS = 50
MAX_RECOMMENDATIONS = 3


# ── Version resolution ──────────────────────────────────────────────

def get_installed_versions():
    """Return sorted list of (version_tuple, full_dir_name)."""
    if not CORTEX_DATA_DIR.exists():
        return []
    versions = []
    for d in CORTEX_DATA_DIR.iterdir():
        if d.is_dir() and d.name[0].isdigit():
            m = re.match(r"(\d+)\.(\d+)\.(\d+)", d.name)
            if m:
                ver_tuple = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
                versions.append((ver_tuple, d.name))
    versions.sort(key=lambda x: x[0])
    return versions


def get_version_label(dir_name):
    m = re.match(r"(\d+\.\d+\.\d+)", dir_name)
    return f"v{m.group(1)}" if m else dir_name


# ── Diffing ─────────────────────────────────────────────────────────

def diff_directories(old_dir, new_dir):
    old = set(old_dir.iterdir()) if old_dir and old_dir.exists() else set()
    new = set(new_dir.iterdir()) if new_dir and new_dir.exists() else set()
    old_names = {d.name for d in old if d.is_dir() and not d.name.startswith("_")}
    new_names = {d.name for d in new if d.is_dir() and not d.name.startswith("_")}
    return sorted(new_names - old_names), sorted(old_names - new_names)


def diff_changelog(old_file, new_file):
    old_text = old_file.read_text() if old_file and old_file.exists() else ""
    new_text = new_file.read_text() if new_file and new_file.exists() else ""
    old_lines = set(old_text.splitlines())
    new_entries = []
    for line in new_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- ") and stripped not in old_lines:
            new_entries.append(stripped[2:])
    return new_entries


# ── Skill metadata ──────────────────────────────────────────────────

def read_skill_description(skill_dir):
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return ""
    text = skill_md.read_text(errors="replace")
    m = re.search(r'description:\s*["\'>|]?\s*(.+?)(?:\n[a-z]|\n---|\n#)', text, re.DOTALL)
    if m:
        return m.group(1).strip().replace("\n", " ")[:200]
    return ""


def get_skill_one_liner(desc):
    # Split on sentence-ending period (period followed by space or end), not mid-word dots
    m = re.match(r"(.+?\.)\s", desc)
    first = m.group(1) if m else desc
    first = first.strip()
    # Strip markdown noise like **[REQUIRED]**, **ALL**, etc.
    first = re.sub(r"\*\*\[?[A-Z]+\]?\*\*\s*", "", first)
    if len(first) > 70:
        cut = first[:70].rfind(" ")
        first = first[:cut] + "..." if cut > 20 else first[:70] + "..."
    return first


STOPWORDS = {
    "the", "and", "for", "with", "from", "this", "that", "what", "when",
    "how", "use", "used", "using", "create", "creating", "build", "building",
    "understanding", "about", "into", "your", "you", "can", "are", "not",
    "all", "was", "were", "been", "will", "would", "should", "could",
    "have", "has", "had", "does", "did", "doing", "done", "get", "got",
    "set", "run", "running", "make", "making", "new", "also", "try",
    "check", "show", "list", "view", "update", "add", "manage", "work",
    "working", "specific", "available", "support", "based", "recent",
    "session", "chat", "data", "file", "files", "code", "name", "type",
    "table", "tables", "query", "queries", "snowflake", "cortex",
}


def tokenize(text):
    words = set(re.findall(r"[a-z][a-z0-9_-]{2,}", text.lower()))
    return words - STOPWORDS


# ── Conversation scanning & user classification ─────────────────────

def scan_conversations(convo_dir, limit=MAX_CONVOS):
    """Build usage profile from conversation JSON files."""
    profile = {
        "tools": Counter(),
        "skills_used": Counter(),
        "titles": [],
        "sql_descriptions": [],
        "session_count": 0,
        "total_conversations": 0,
        # Retention-relevant counters
        "edit_count": 0,       # edit + multi_edit
        "write_count": 0,
        "bash_count": 0,
        "sql_count": 0,
        "skill_count": 0,
        "task_count": 0,       # subagent usage
        "read_count": 0,
        "glob_grep_count": 0,  # codebase search
    }
    if not convo_dir.exists():
        return profile

    all_files = sorted(convo_dir.glob("*.json"), key=os.path.getmtime, reverse=True)
    profile["total_conversations"] = len(all_files)
    files = all_files[:limit]

    for f in files:
        try:
            data = json.loads(f.read_text(errors="replace"))
        except (json.JSONDecodeError, OSError):
            continue

        profile["session_count"] += 1
        title = data.get("title", "")
        if title and not title.startswith("Chat for session:"):
            profile["titles"].append(title)

        for msg in data.get("history", []):
            content = msg.get("content")
            if not isinstance(content, list):
                continue
            for block in content:
                if not isinstance(block, dict) or block.get("type") != "tool_use":
                    continue
                tu = block.get("tool_use", {})
                name = tu.get("name", "")
                if not name:
                    continue
                profile["tools"][name] += 1
                inp = tu.get("input", {})

                # Track retention signals
                if name in ("edit", "multi_edit"):
                    profile["edit_count"] += 1
                elif name == "write":
                    profile["write_count"] += 1
                elif name == "bash":
                    profile["bash_count"] += 1
                elif name == "snowflake_sql_execute":
                    profile["sql_count"] += 1
                    desc = inp.get("description", "")
                    if desc:
                        profile["sql_descriptions"].append(desc)
                elif name in ("glob", "grep"):
                    profile["glob_grep_count"] += 1
                elif name == "read":
                    profile["read_count"] += 1
                elif name == "task":
                    profile["task_count"] += 1

                if name in ("skill", "server_skill"):
                    skill_name = inp.get("command", inp.get("skill_name", ""))
                    if skill_name:
                        profile["skills_used"][skill_name] += 1
                        profile["skill_count"] += 1
    return profile


# User tiers based on conversation history depth
# Aligned with: coco_user_patterns_reference.md
TIER_NEW = "new"           # 0 conversations
TIER_BEGINNER = "beginner" # 1-5 sessions — highest churn risk
TIER_RETURNING = "returning"  # 6-30 sessions — habit forming
TIER_POWER = "power"       # 30+ sessions — daily driver


def classify_user(profile):
    """Classify user into a tier based on conversation history."""
    total = profile["total_conversations"]
    if total == 0:
        return TIER_NEW
    if total <= 5:
        return TIER_BEGINNER
    if total <= 30:
        return TIER_RETURNING
    return TIER_POWER


def detect_gaps(profile):
    """Detect anti-patterns and missing behaviors based on retention signals."""
    gaps = []
    sessions = max(profile["session_count"], 1)

    # Anti-pattern: no edit loop (strongest retention signal, +11.8pp delta)
    if profile["edit_count"] == 0 and profile["write_count"] == 0:
        gaps.append("no_edit_loop")

    # Anti-pattern: read-only / Q&A mode
    if profile["read_count"] > 10 and profile["edit_count"] == 0:
        gaps.append("read_only")

    # Anti-pattern: no bash (run real commands = +16.1pp delta)
    if profile["bash_count"] == 0:
        gaps.append("no_bash")

    # Opportunity: no skills used (skill-dev = 2x retention)
    if profile["skill_count"] == 0:
        gaps.append("no_skills")

    # Opportunity: no agents (task = 2x retention)
    if profile["task_count"] == 0:
        gaps.append("no_agents")

    # Opportunity: no codebase search (glob/grep = +11pp delta)
    if profile["glob_grep_count"] == 0:
        gaps.append("no_search")

    # Opportunity: heavy SQL but no app building
    if profile["sql_count"] > 20 and "developing-with-streamlit" not in profile["skills_used"]:
        gaps.append("sql_no_app")

    return gaps


# ── Recommendation engine ───────────────────────────────────────────

# Skill affinity map: matches new skills to user behavior signals
TOOL_AFFINITY = {
    "dashboard": {
        "tools": ["chart_generation_instructions"],
        "skills": ["chart_generation_instructions"],
        "tool_threshold": {"snowflake_sql_execute": 20},
    },
    "snowpark-connect": {
        "keywords": ["snowpark", "pyspark", "spark", "migration"],
    },
    "network-security": {
        "keywords": ["network", "security", "policy", "firewall", "ip"],
    },
    "data-products": {
        "keywords": ["share", "marketplace", "listing", "cross-account"],
    },
}

MIN_RECOMMEND_SCORE = 3


def score_skill(skill_name, skill_desc, profile):
    """Score a new skill against user profile. Returns (score, reasons)."""
    score = 0
    reasons = []

    all_text = " ".join(profile["titles"] + profile["sql_descriptions"])
    user_keywords = tokenize(all_text)
    skill_keywords = tokenize(skill_desc)
    overlap = user_keywords & skill_keywords
    if overlap:
        score += len(overlap)
        best_title = None
        best_overlap = 0
        for title in profile["titles"][:15]:
            title_kw = tokenize(title)
            n = len(title_kw & skill_keywords)
            if n > best_overlap:
                best_overlap = n
                best_title = title
        if best_title and best_overlap >= 2:
            reasons.append(f'You worked on "{best_title}"')

    affinity = TOOL_AFFINITY.get(skill_name, {})
    for tool in affinity.get("tools", []):
        if profile["tools"].get(tool, 0) > 0:
            score += 2
    for skill in affinity.get("skills", []):
        if profile["skills_used"].get(skill, 0) > 0:
            score += 2
            reasons.append(f"You use {skill} ({profile['skills_used'][skill]}x)")
    for tool, threshold in affinity.get("tool_threshold", {}).items():
        count = profile["tools"].get(tool, 0)
        if count >= threshold:
            score += 2
            reasons.append(f"You run heavy SQL analytics ({count} queries)")
    for kw in affinity.get("keywords", []):
        if kw in user_keywords:
            score += 1

    return score, reasons


def recommend(new_skills, skills_dir, profile, limit=MAX_RECOMMENDATIONS):
    if profile["session_count"] == 0:
        return []

    scored = []
    for skill_name in new_skills:
        sd = skills_dir / skill_name
        desc = read_skill_description(sd)
        one_liner = get_skill_one_liner(desc)
        s, reasons = score_skill(skill_name, desc, profile)
        if s >= MIN_RECOMMEND_SCORE and reasons:
            scored.append((s, skill_name, one_liner, reasons))

    scored.sort(reverse=True)
    return [(name, liner, reasons) for _, name, liner, reasons in scored[:limit]]


# ── Formatting helpers ─────────────────────────────────────────────

DIVIDER = "─" * 56
DIVIDER_LIGHT = "·" * 56


def _header(title):
    """Clean boxed header."""
    return f"""
{DIVIDER}
  {title}
{DIVIDER}"""


def _section(title):
    """Section sub-header."""
    return f"""
  {title}
  {DIVIDER_LIGHT}"""


def _footer():
    """Consistent footer across all tiers."""
    return f"""
{DIVIDER}
  Type $cortex-code-guide for the full feature reference
  Type /help for commands  |  /skill to browse all skills
{DIVIDER}"""


# ── Output formatting ───────────────────────────────────────────────

def format_upgrade(old_label, new_label, added_skills, removed_skills,
                   changelog_entries, recommendations, skills_dir,
                   tier, gaps, profile):
    """Format the version upgrade message, tailored by user tier."""
    lines = [_header(f"Cortex Code updated  {old_label} -> {new_label}")]

    if added_skills:
        lines.append(_section(f"New Skills ({len(added_skills)})"))
        lines.append("")
        for s in added_skills:
            desc = read_skill_description(skills_dir / s)
            liner = get_skill_one_liner(desc) if desc else s
            lines.append(f"    + {s:<22s} {liner}")
        lines.append("")

    if removed_skills:
        lines.append(_section("Removed"))
        lines.append("")
        for s in removed_skills:
            lines.append(f"    - {s}")
        lines.append("")

    if changelog_entries:
        lines.append(_section("What Changed"))
        lines.append("")
        for entry in changelog_entries[:5]:
            lines.append(f"    * {entry}")
        lines.append("")

    if recommendations:
        lines.append(_section("Recommended for You"))
        lines.append("")
        for name, liner, reasons in recommendations:
            reason_text = reasons[0] if reasons else ""
            lines.append(f"    {name}")
            lines.append(f"    {reason_text} -- this skill can help.")
            lines.append(f'    Try: "${name}"')
            lines.append("")

    # Tier-specific nudges on upgrade
    nudges = _get_nudges(tier, gaps, profile)
    if nudges:
        lines.append(_section("Worth Trying"))
        lines.append("")
        for nudge in nudges[:2]:
            lines.append(f"    {nudge}")
        lines.append("")

    lines.append(_footer())
    return "\n".join(lines)


def format_welcome_new(version_label, total_skills):
    """Brand new user — helpful, not pushy. Three clear starting points."""
    return f"""{_header(f"Welcome to Cortex Code {version_label}")}

  {total_skills} skills ready to help. Here are a few things
  you can ask right away:
{_section("Check for problems and help fix them")}

    "Are any of my Snowflake tasks failing? Show me the errors
     and help me fix them."

    "Check data quality on #DB.SCHEMA.MY_TABLE -- flag any
     nulls, duplicates, or stale rows and suggest fixes."
{_section("Scan for drift and keep things healthy")}

    "Has the schema changed on any of my key tables recently?
     Show me what shifted and whether anything downstream broke."

    "Compare row counts and freshness across my production
     tables -- highlight anything that looks off."
{_section("Build a dashboard to review your data")}

    "Build me a Streamlit app that shows my warehouse costs
     by day so I can spot spikes."

    "Create a dashboard from #DB.SCHEMA.ORDERS that shows
     revenue trends, top customers, and daily volume."
{_footer()}"""


def format_welcome_beginner(version_label, total_skills, gaps, profile):
    """Beginner (1-5 sessions) — address specific retention gaps."""
    lines = [_header(f"Welcome back  |  Cortex Code {version_label}")]

    nudges = _get_nudges(TIER_BEGINNER, gaps, profile)
    if nudges:
        lines.append(_section("Based on your recent sessions, try these next"))
        lines.append("")
        for nudge in nudges[:3]:
            lines.append(f"    {nudge}")
        lines.append("")
    else:
        lines.append(_section("Keep the momentum going"))
        lines.append("")
        lines.append('    You can teach CoCo your team\'s workflow so it')
        lines.append('    runs the same way every session. Try:')
        lines.append('    "$skill-development"')
        lines.append("")

    lines.append(_footer())
    return "\n".join(lines)


def format_welcome_returning(version_label, total_skills, gaps, profile):
    """Returning user (6-30 sessions) — push toward power user behaviors."""
    lines = [_header(f"Welcome back  |  Cortex Code {version_label}")]

    nudges = _get_nudges(TIER_RETURNING, gaps, profile)
    if nudges:
        lines.append(_section("Level up your workflow"))
        lines.append("")
        for nudge in nudges[:2]:
            lines.append(f"    {nudge}")
        lines.append("")

    lines.append(_footer())
    return "\n".join(lines)


def format_welcome_power(version_label, total_skills, profile, skills_dir=None):
    """Power user (30+ sessions) — surface untried skills with clear value."""
    lines = [_header(f"Cortex Code {version_label}  |  {profile['total_conversations']} sessions")]

    untried = _find_untried_skills(profile, skills_dir) if skills_dir else []
    if untried:
        lines.append(_section("Speed up your workflow"))
        lines.append("")
        for name, one_liner in untried[:2]:
            lines.append(f"    ${name}")
            lines.append(f"    {_skill_value_pitch(name, one_liner)}")
            lines.append("")
    else:
        lines.append("")
        lines.append("  You've explored most of the skill library.")
        lines.append("  Type /skill to see the full list.")
        lines.append("")

    lines.append(_footer())
    return "\n".join(lines)


def _find_untried_skills(profile, skills_dir):
    """Find bundled skills the power user hasn't invoked, scored by relevance."""
    if not skills_dir or not skills_dir.exists():
        return []
    used = set(profile["skills_used"].keys())
    candidates = []
    for d in skills_dir.iterdir():
        if not d.is_dir() or d.name.startswith("_"):
            continue
        if d.name in used:
            continue
        desc = read_skill_description(d)
        if not desc:
            continue
        score, _ = score_skill(d.name, desc, profile)
        if score >= MIN_RECOMMEND_SCORE:
            candidates.append((score, d.name, get_skill_one_liner(desc)))
    candidates.sort(reverse=True)
    return [(name, liner) for _, name, liner in candidates]


# Maps skill names to outcome-focused pitches for power users.
# Tells them what the skill does FOR THEM, not what it IS.
SKILL_VALUE_MAP = {
    "dashboard": "Skip the manual chart building -- describe what you want to see and get a live dashboard in seconds.",
    "cost-intelligence": "Find exactly where your credits are going and get actionable recommendations to cut waste.",
    "data-quality": "Catch nulls, duplicates, and stale data before your stakeholders do. Sets up monitors automatically.",
    "data-governance": "Audit who has access to what, find unmasked PII, and get your governance posture scored.",
    "lineage": "Trace any column back to its source or forward to everything that depends on it. Great for impact analysis.",
    "dynamic-tables": "Replace your refresh-loop pipelines with declarative tables that manage their own updates.",
    "semantic-view": "Define your metrics once in a semantic layer so Cortex Analyst answers questions consistently.",
    "machine-learning": "Train, deploy, and monitor ML models without leaving Snowflake. Handles the full lifecycle.",
    "cortex-agent": "Build AI agents that can query your data, call tools, and answer domain questions autonomously.",
    "developing-with-streamlit": "Turn any SQL query into a polished interactive app your team can use immediately.",
    "iceberg": "Work with Apache Iceberg tables natively in Snowflake -- catalog integrations, external volumes, auto-refresh.",
    "skill-development": "Codify your team's best practices into reusable skills that run the same way every time.",
    "cortex-ai-functions": "Classify, extract, summarize, or translate data at scale using built-in AI functions -- no model hosting needed.",
    "snowpark-python": "Deploy Python UDFs and stored procedures directly to Snowflake without managing infrastructure.",
    "deploy-to-spcs": "Containerize any app and deploy it to Snowpark Container Services with one command.",
    "trust-center": "Review security findings, CIS benchmarks, and vulnerability scans across your entire account.",
    "integrations": "Set up API, storage, and notification integrations without digging through the docs.",
    "network-security": "Manage network policies and rules to lock down access -- see what's allowed and what's exposed.",
    "workload-performance-analysis": "Find slow queries, spilling joins, and missed pruning opportunities -- get specific tuning recommendations.",
    "organization-management": "Get a bird's-eye view of all accounts, spending, security posture, and auth health across your org.",
    "cost-intelligence": "Find exactly where your credits are going and get actionable recommendations to cut waste.",
    "checking-freshness": "Instantly check if your tables are up to date before making decisions on stale data.",
    "profiling-tables": "Deep-dive a table's structure, distributions, and quality stats in one command.",
    "declarative-sharing": "Share data products across Snowflake accounts with versioning -- no manual GRANT juggling.",
    "snowflake-notebooks": "Create and edit Snowflake workspace notebooks with SQL, Python, and markdown cells.",
    "data-cleanrooms": "Run privacy-safe overlap analysis and audience activation across organizations.",
}


def _skill_value_pitch(name, one_liner):
    """Return an outcome-focused pitch for a skill, falling back to one_liner."""
    return SKILL_VALUE_MAP.get(name, one_liner)


def format_session_nudge(version_label, tier, gaps, profile, skills_dir):
    """Multi-line rotating nudge for repeat sessions (same version, not first run).
    Returns a formatted tip block or empty string if nothing to suggest."""

    # Collect all possible nudges as (title, body, prompt) tuples
    candidates = []

    # Gap-based nudges
    if "no_edit_loop" in gaps:
        candidates.append((
            "Let CoCo edit your files directly",
            "CoCo is most useful when it can read, change, and save your actual code.\n"
            "    Point it at a real file and describe what you want different.",
            '"Read my app.py and refactor the DB calls to use connection pooling"',
        ))
    if "no_skills" in gaps:
        candidates.append((
            "Teach CoCo your workflow with a custom skill",
            "Skills let you package a multi-step process so it runs the same\n"
            "    way every session. Your team can share them too.",
            '"$skill-development"',
        ))
    if "no_agents" in gaps:
        candidates.append((
            "Use a team of agents for complex tasks",
            "CoCo can spin up multiple agents that research, build, and test\n"
            "    in parallel -- finishing in minutes what would take you an hour.",
            '"Use a team to research, implement, and test this feature"',
        ))
    if "no_bash" in gaps:
        candidates.append((
            "Run commands and let CoCo fix what breaks",
            "CoCo can execute shell commands, read the output, and iterate\n"
            "    until everything passes. Great for builds, tests, and deploys.",
            '"Run pytest and fix any failing tests"',
        ))
    if "sql_no_app" in gaps:
        candidates.append((
            "Turn your SQL into a Streamlit app",
            f"You've run {profile['sql_count']} queries so far. Any of them can become\n"
            "    an interactive dashboard your team can use right away.",
            '"$developing-with-streamlit"',
        ))
    if "read_only" in gaps:
        candidates.append((
            "Go beyond reading -- let CoCo make changes",
            "You've been reading files but haven't let CoCo edit yet.\n"
            "    The real power is in the edit loop: read, change, verify, repeat.",
            '"Read my config.yaml and update it for production"',
        ))
    if "no_search" in gaps:
        candidates.append((
            "Pull in live docs and web results mid-conversation",
            "CoCo can search the web, fetch documentation, and use what it finds\n"
            "    to give you accurate, up-to-date answers.",
            '"Look up the latest Cortex AI functions and show me examples"',
        ))

    # Untried skill nudges — value-focused
    untried = _find_untried_skills(profile, skills_dir) if skills_dir else []
    for name, one_liner in untried[:3]:
        pitch = _skill_value_pitch(name, one_liner)
        candidates.append((
            f"${name}",
            f"    {pitch}",
            f'"${name}"',
        ))

    # General tips (always available as filler)
    candidates.append((
        "Auto-inject table context with #TABLE",
        "Type #DB.SCHEMA.TABLE anywhere in your prompt and CoCo\n"
        "    automatically pulls in column names and sample rows.",
        '"Show me data quality issues on #ANALYTICS.PUBLIC.ORDERS"',
    ))
    candidates.append((
        "Keep long sessions fast with /compact",
        "Running low on context? /compact shrinks the conversation\n"
        "    while keeping the important state intact.",
        "Type /compact when things slow down",
    ))

    if not candidates:
        return ""

    # Rotate based on total conversation count
    idx = profile["total_conversations"] % len(candidates)
    title, body, prompt = candidates[idx]

    return f"""
{DIVIDER}
  Cortex Code {version_label}  |  Tip of the session
{DIVIDER}

  {title}

    {body}

    >>> {prompt}

{DIVIDER}"""


def _get_nudges(tier, gaps, profile):
    """Generate actionable nudges based on user gaps and tier."""
    nudges = []

    if tier == TIER_BEGINNER:
        if "no_edit_loop" in gaps:
            nudges.append(
                'CoCo can edit your actual files -- point it at something real:\n'
                '    "Read my app.py and add error handling to the API calls"'
            )
        if "no_bash" in gaps:
            nudges.append(
                'Let CoCo run commands and fix what breaks:\n'
                '    "Run dbt build, fix any failures, and show me what changed"'
            )
        if "no_search" in gaps:
            nudges.append(
                'CoCo can search your codebase to answer questions:\n'
                '    "Find all files that reference CUSTOMERS and show how they join"'
            )
        if "no_skills" in gaps:
            nudges.append(
                'Package your workflow into a reusable skill:\n'
                '    "$skill-development" walks you through creating your first one'
            )

    elif tier == TIER_RETURNING:
        if "no_skills" in gaps:
            nudges.append(
                'Automate your most common workflow with a custom skill:\n'
                '    "$skill-development" -- e.g., a dbt runner, PR reviewer, or daily briefing'
            )
        if "no_agents" in gaps:
            nudges.append(
                'Parallelize complex work with a team of agents:\n'
                '    "Use a team to research, implement, and test this feature"'
            )
        if "sql_no_app" in gaps:
            nudges.append(
                f'You\'ve run {profile["sql_count"]} queries -- any of them can become a dashboard:\n'
                '    "$developing-with-streamlit" to build an interactive app from your SQL'
            )
        if "no_edit_loop" in gaps:
            nudges.append(
                'CoCo is most powerful when it edits your files directly:\n'
                '    "Read my config and update the connection settings for production"'
            )

    elif tier == TIER_POWER:
        if "sql_no_app" in gaps:
            nudges.append(
                f'You run a lot of SQL ({profile["sql_count"]} queries). Turn your best ones\n'
                '    into a Streamlit app your team can use: "$developing-with-streamlit"'
            )
        if "no_agents" in gaps:
            nudges.append(
                'Teams of agents can parallelize big tasks -- research, build, and test\n'
                '    all at once: "Use a team to build and test this end to end"'
            )

    return nudges


# ── Main ────────────────────────────────────────────────────────────

def main():
    versions = get_installed_versions()
    if not versions:
        return

    current_ver_tuple, current_dir_name = versions[-1]
    current_label = get_version_label(current_dir_name)
    current_path = CORTEX_DATA_DIR / current_dir_name
    current_skills_dir = current_path / "bundled_skills"

    state_file = Path.home() / ".snowflake" / "cortex" / ".whats-new-state"
    last_seen_dir = None
    if state_file.exists():
        last_seen_dir = state_file.read_text().strip()

    is_upgrade = last_seen_dir and last_seen_dir != current_dir_name
    is_first_run = not last_seen_dir

    # Scan conversations and classify user
    profile = scan_conversations(CONVO_DIR)
    tier = classify_user(profile)
    gaps = detect_gaps(profile)

    all_skills = [d.name for d in current_skills_dir.iterdir()
                  if d.is_dir() and not d.name.startswith("_")]
    total = len(all_skills)

    if is_upgrade:
        old_path = CORTEX_DATA_DIR / last_seen_dir
        old_skills_dir = old_path / "bundled_skills"
        old_label = get_version_label(last_seen_dir)

        added, removed = diff_directories(old_skills_dir, current_skills_dir)
        changelog = diff_changelog(
            old_path / "CHANGELOG.md",
            current_path / "CHANGELOG.md",
        )
        recs = recommend(added, current_skills_dir, profile)
        output = format_upgrade(old_label, current_label, added, removed,
                                changelog, recs, current_skills_dir,
                                tier, gaps, profile)
    elif is_first_run:
        # First run — tier-specific welcome
        if tier == TIER_NEW:
            output = format_welcome_new(current_label, total)
        elif tier == TIER_BEGINNER:
            output = format_welcome_beginner(current_label, total, gaps, profile)
        elif tier == TIER_RETURNING:
            output = format_welcome_returning(current_label, total, gaps, profile)
        else:
            output = format_welcome_power(current_label, total, profile, current_skills_dir)
    else:
        # Repeat session, same version — show a short rotating nudge
        output = format_session_nudge(
            current_label, tier, gaps, profile, current_skills_dir
        )

    if output:
        print(output)

    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(current_dir_name)


if __name__ == "__main__":
    main()
