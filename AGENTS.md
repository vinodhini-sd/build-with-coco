# AGENTS.md

Context for AI coding agents (Cortex Code, Claude Code, etc.) working in this repo.

## What This Repo Is

`build-with-coco` is a collection of Cortex Code skills and workflow recipes for Snowflake developers.

- **Skills** (`skills/`) — Loaded by Cortex Code to automate complex multi-step workflows
- **Recipes** (`recipes/`) — Copy-paste prompts organized by use case and role

## Skills

### Directory structure

```
skills/<skill-name>/
├── SKILL.md           ← required: triggers + core workflow only
└── references/        ← optional: loaded on demand by CoCo
    └── workflow.md    ← detailed steps, SQL, code templates, etc.
```

### Rules

- **SKILL.md must stay under 500 lines.** When approaching the limit, split detailed content into `references/`.
- **No README.md in skill directories.** The root `README.md` is the only index.
- **Frontmatter is required.** Every SKILL.md must have `name:` and `description:` in YAML frontmatter. The description drives skill triggering — make it clear and include trigger phrases.
- **Context window is a public good.** Only put content in SKILL.md that the model needs in working memory. Move detailed steps, SQL templates, and reference material to `references/`.
- **Progressive disclosure:** `references/` files load only when CoCo determines they're needed. Link explicitly from SKILL.md: "See `references/workflow.md` for full step detail."
- **No extraneous docs.** No CHANGELOG.md, INSTALLATION.md, or QUICK_REFERENCE.md inside skill directories.

### Frontmatter format

```yaml
---
name: my-skill
description: "What this skill does and when to use it. Include trigger phrases: do this, do that."
---
```

### Adding a new skill

1. Create `skills/<skill-name>/`
2. Add `SKILL.md` with YAML frontmatter + workflow body
3. If body exceeds ~300 lines, split detailed content into `references/`
4. Add an entry to the skills table in `README.md`
5. Verify: `./install.sh --project && ls .cortex/skills/<skill-name>/`

### Splitting SKILL.md into references/

When SKILL.md approaches 500 lines:

```markdown
## Step 2: Profile Raw Tables

Profile column types, cardinality, null rates. See [references/workflow.md](references/workflow.md) for full SQL and decision logic.
```

And in `references/workflow.md`:
```markdown
# Workflow Detail

Loaded when executing the generation workflow.

## Step 2: Profile Raw Tables
[full SQL, decision heuristics, templates...]
```

## Recipes

### Directory structure

```
recipes/
├── README.md              ← catalog: browse by use case or by role
├── <use-case>/
│   └── <workflow>.md      ← single workflow recipe
└── by-role/
    └── <role>/
        └── prompts.md     ← multi-prompt cheat sheet for a persona
```

### Single-workflow recipe format

Each file in a use-case directory covers exactly one workflow:

```markdown
# Workflow Title

> One-line description

## The Prompt
[copy-paste ready prompt with {{placeholder}} variables]

## What This Triggers
- [skill or feature invoked]

## Before You Run
- [prerequisite: table, role, tool, access]

## Tips
- [how to customize; common variations]
```

### by-role/ cheat sheet format

Each `by-role/<role>/prompts.md` has 10-15 numbered prompts for a persona. Not a single workflow — a starter library. Each prompt uses `{{placeholder}}` variables and is copy-paste ready.

### Adding a new recipe

1. Find or create the right use-case directory under `recipes/`
2. Create a `.md` file using the four-section format above
3. Use `{{placeholder}}` for anything the user must fill in
4. Add an entry to `recipes/README.md` catalog table
5. Add an entry to the root `README.md` scenario table

## Naming conventions

- **Directories:** `kebab-case` only — no underscores, no spaces, no uppercase
- **Snowflake objects in SQL:** underscores only — hyphens cause SQL syntax errors
- **Placeholders in prompts:** `{{double-braces-kebab-case}}` (e.g., `{{database}}`, `{{project-path}}`)
- **Never hardcode credentials** — use env vars or CoCo's active Snowflake connection

## Install

```bash
./install.sh              # skills + recipes → ~/.snowflake/cortex/
./install.sh skills       # skills only
./install.sh recipes      # recipes only
./install.sh --project    # install into .cortex/ in current directory
```

Skills land in `~/.snowflake/cortex/skills/<skill-name>/`
Recipes land in `~/.snowflake/cortex/recipes/`

## Repo layout

```
build-with-coco/
├── AGENTS.md          ← this file
├── CHANGELOG.md       ← version history
├── README.md          ← human-facing index
├── install.sh         ← installer
├── skills/            ← CoCo skill automations
└── recipes/           ← copy-paste workflow prompts
    ├── by-role/       ← persona cheat sheets (10-15 prompts per role)
    └── <use-case>/    ← scenario-based single-workflow recipes
```
