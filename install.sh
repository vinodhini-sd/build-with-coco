#!/usr/bin/env bash
# install.sh — Install skills, recipes, and/or hooks from build-with-coco
#
# Usage:
#   ./install.sh              # Install everything (skills + recipes + hooks)
#   ./install.sh skills       # Install skills only
#   ./install.sh recipes      # Install recipes only
#   ./install.sh hooks        # Install hooks only
#   ./install.sh --project    # Install into current project (.cortex/) instead of global

set -euo pipefail

GLOBAL_DIR="${HOME}/.snowflake/cortex"
PROJECT_MODE=false
INSTALL_TARGET="${1:-all}"

# Check for --project flag
for arg in "$@"; do
  if [[ "$arg" == "--project" ]]; then
    PROJECT_MODE=true
    GLOBAL_DIR=".cortex"
  fi
done

# Strip --project from INSTALL_TARGET if it was the first arg
if [[ "$INSTALL_TARGET" == "--project" ]]; then
  INSTALL_TARGET="all"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SRC="${SCRIPT_DIR}/skills"
PROMPTS_SRC="${SCRIPT_DIR}/recipes"
HOOKS_SRC="${SCRIPT_DIR}/hooks"

installed=0

install_skills() {
  if [[ ! -d "$SKILLS_SRC" ]]; then
    echo "⚠ No skills/ directory found — skipping skills"
    return
  fi

  local dest="${GLOBAL_DIR}/skills"
  mkdir -p "$dest"

  for skill_dir in "$SKILLS_SRC"/*/; do
    local skill_name
    skill_name="$(basename "$skill_dir")"
    cp -r "$skill_dir" "$dest/$skill_name"
    echo "  ✓ $skill_name"
    (( ++installed ))
  done
}

install_recipes() {
  if [[ ! -d "$PROMPTS_SRC" ]]; then
    echo "⚠ No recipes/ directory found — skipping recipes"
    return
  fi

  local dest="${GLOBAL_DIR}/recipes"
  mkdir -p "$dest"

  # Copy category directories (skip README)
  for category_dir in "$PROMPTS_SRC"/*/; do
    local category_name
    category_name="$(basename "$category_dir")"
    mkdir -p "$dest/$category_name"
    cp -r "$category_dir"* "$dest/$category_name/" 2>/dev/null || true
    local count
    count=$(find "$dest/$category_name" -name '*.md' | wc -l | tr -d ' ')
    echo "  ✓ $category_name ($count recipes)"
    ((installed += count))
  done

  # Copy recipes README
  if [[ -f "$PROMPTS_SRC/README.md" ]]; then
    cp "$PROMPTS_SRC/README.md" "$dest/README.md"
  fi
}

install_hooks() {
  if [[ ! -d "$HOOKS_SRC" ]]; then
    echo "⚠ No hooks/ directory found — skipping hooks"
    return
  fi

  local dest="${GLOBAL_DIR}/hooks"
  mkdir -p "$dest"

  cp -r "$HOOKS_SRC"/. "$dest/"
  local count
  count=$(find "$dest" -maxdepth 1 -type f | wc -l | tr -d ' ')
  echo "  ✓ hooks ($count files)"
  (( installed += count ))
}

echo ""
echo "build-with-coco installer"
echo "========================="
if $PROJECT_MODE; then
  echo "Mode: project-local (.cortex/)"
else
  echo "Mode: global (~/.snowflake/cortex/)"
fi
echo ""

case "$INSTALL_TARGET" in
  skills)
    echo "Installing skills..."
    install_skills
    ;;
  recipes)
    echo "Installing recipes..."
    install_recipes
    ;;
  hooks)
    echo "Installing hooks..."
    install_hooks
    ;;
  all|*)
    echo "Installing skills..."
    install_skills
    echo ""
    echo "Installing recipes..."
    install_recipes
    echo ""
    echo "Installing hooks..."
    install_hooks
    ;;
esac

echo ""
echo "Done — $installed items installed to $GLOBAL_DIR/"
echo ""
echo "Skills: invoke with \$skill-name in Cortex Code"
echo "Recipes: copy-paste from $GLOBAL_DIR/recipes/ or browse the catalog in recipes/README.md"
echo "Hooks: installed to $GLOBAL_DIR/hooks/ — configure in your Cortex Code settings"
