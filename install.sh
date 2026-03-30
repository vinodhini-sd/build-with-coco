#!/usr/bin/env bash
# install.sh — Install skills and/or prompts from build-with-coco
#
# Usage:
#   ./install.sh              # Install everything (skills + prompts)
#   ./install.sh skills       # Install skills only
#   ./install.sh prompts      # Install prompts only
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
PROMPTS_SRC="${SCRIPT_DIR}/prompts"

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
    ((installed++))
  done
}

install_prompts() {
  if [[ ! -d "$PROMPTS_SRC" ]]; then
    echo "⚠ No prompts/ directory found — skipping prompts"
    return
  fi

  local dest="${GLOBAL_DIR}/prompts"
  mkdir -p "$dest"

  # Copy category directories (skip README)
  for category_dir in "$PROMPTS_SRC"/*/; do
    local category_name
    category_name="$(basename "$category_dir")"
    mkdir -p "$dest/$category_name"
    cp "$category_dir"*.md "$dest/$category_name/" 2>/dev/null || true
    local count
    count=$(find "$dest/$category_name" -name '*.md' | wc -l | tr -d ' ')
    echo "  ✓ $category_name ($count prompts)"
    ((installed += count))
  done

  # Copy prompts README
  if [[ -f "$PROMPTS_SRC/README.md" ]]; then
    cp "$PROMPTS_SRC/README.md" "$dest/README.md"
  fi
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
  prompts)
    echo "Installing prompts..."
    install_prompts
    ;;
  all|*)
    echo "Installing skills..."
    install_skills
    echo ""
    echo "Installing prompts..."
    install_prompts
    ;;
esac

echo ""
echo "Done — $installed items installed to $GLOBAL_DIR/"
echo ""
echo "Skills: invoke with \$skill-name in Cortex Code"
echo "Prompts: copy-paste from $GLOBAL_DIR/prompts/ or browse the catalog in prompts/README.md"
