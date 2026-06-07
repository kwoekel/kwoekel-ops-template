#!/bin/bash
# setup.sh — one-command installer for kwoekel-ops-template
# Run once after cloning. Safe to re-run.
set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  Setting up ops repo — please wait...   ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# ── 1. graphify (pipx — package is 'graphifyy' with double y) ─────────────────
echo "→ Installing graphify..."
if command -v pipx &>/dev/null; then
  pipx install graphifyy 2>/dev/null || pipx upgrade graphifyy 2>/dev/null || true
else
  echo "  ⚠️  pipx not found — install pipx then run: pipx install graphifyy"
fi

# ── 2. Claude Code plugins ────────────────────────────────────────────────────
echo "→ Adding plugin marketplaces..."
claude plugin add marketplace context-mode https://github.com/mksglu/context-mode 2>/dev/null || true
claude plugin add marketplace thedotmack https://github.com/thedotmack/claude-mem 2>/dev/null || true

echo "→ Installing plugins..."
PLUGINS=(
  "context-mode@context-mode"
  "claude-mem@thedotmack"
  "superpowers@claude-plugins-official"
  "feature-dev@claude-plugins-official"
  "code-review@claude-plugins-official"
  "code-simplifier@claude-plugins-official"
  "pr-review-toolkit@claude-plugins-official"
  "claude-md-management@claude-plugins-official"
  "skill-creator@claude-plugins-official"
  "context7@claude-plugins-official"
  "claude-code-setup@claude-plugins-official"
  "security-guidance@claude-plugins-official"
  "commit-commands@claude-plugins-official"
  "github@claude-plugins-official"
  "ralph-loop@claude-plugins-official"
)
for plugin in "${PLUGINS[@]}"; do
  claude plugin install "$plugin" 2>/dev/null     && echo "  ✅ $plugin"     || echo "  (already installed: $plugin)"
done

# ── 3. Copy hook scripts to ~/.claude/hooks/ ──────────────────────────────────
echo "→ Installing Claude Code hooks..."
mkdir -p "$HOME/.claude/hooks"
# Overwrite so re-running setup picks up updated hook scripts
cp -f "$REPO_DIR/hooks/"* "$HOME/.claude/hooks/" 2>/dev/null || true
# Restore real $HOME path in any hooks that use the __HOME_DIR__ placeholder
find "$HOME/.claude/hooks" -type f -exec   sed -i "" "s|__HOME_DIR__|$HOME|g" {} \; 2>/dev/null ||   find "$HOME/.claude/hooks" -type f -exec     sed -i "s|__HOME_DIR__|$HOME|g" {} \; 2>/dev/null || true
echo "  ✅ Hooks copied to ~/.claude/hooks/"

# ── 4. Register hooks + safety rules in ~/.claude/settings.json ───────────────
echo "→ Updating global Claude settings..."
python3 "$REPO_DIR/scripts/merge-settings.py"

# ── 5. Register skills ────────────────────────────────────────────────────────
echo "→ Registering skills..."
python3 "$REPO_DIR/skills/sync.py" --write 2>/dev/null || true

# ── 6. Initialize git submodules (token-dashboard) ───────────────────────────
echo "→ Initializing git submodules..."
git -C "$REPO_DIR" submodule update --init --recursive \
  || echo "  ⚠️  Submodule init skipped (optional — token-dashboard unreachable)"

# ── 7. Weekly ops audit launchd agent (Mac only) ─────────────────────────────
if [[ "$OSTYPE" == "darwin"* ]]; then
  echo "→ Setting up weekly ops audit (launchd)..."
  python3 "$REPO_DIR/scripts/install-launchd.py"
fi

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  Setup complete!                        ║"
echo "╠══════════════════════════════════════════╣"
echo "║  Next step:                             ║"
echo "║  python3 scripts/onboard.py --fresh     ║"
echo "║  or --import /path or --import-github   ║"
echo "╚══════════════════════════════════════════╝"
echo ""
