#!/bin/bash
# install.sh — one-line curl-pipe-bash installer for kwoekel-ops-template
# Run from the root of any existing repo:
#   curl -fsSL https://raw.githubusercontent.com/kwoekel/kwoekel-ops-template/simplified-template/scripts/install.sh | bash
# Safe to re-run. Never overwrites existing files. Never prompts.

set -e

TEMPLATE_REPO="https://github.com/kwoekel/kwoekel-ops-template.git"
TEMPLATE_BRANCH="simplified-template"
TEMPLATE_DIR="/tmp/ops-template-install"
DEST="$PWD"

# ── 0. Sanity check ────────────────────────────────────────────────────────────
if [[ ! -d "$DEST/.git" && ! -d "$DEST" ]]; then
  echo "ERROR: Could not determine target directory."
  exit 1
fi

# ── 1. Scan existing files BEFORE any changes (for manifest) ──────────────────
echo "→ Scanning existing files..."

# Build exclusion patterns for binary extensions
BINARY_EXTS="png jpg jpeg gif ico svg mp4 mp3 zip tar gz pdf woff woff2 ttf eot bin exe dmg"

# Collect files into array, excluding .git, node_modules, temp dir, and binaries
mapfile -t EXISTING_FILES < <(
  find "$DEST" -type f \
    ! -path "$DEST/.git/*" \
    ! -path "$DEST/node_modules/*" \
    ! -path "$TEMPLATE_DIR/*" \
  | sort
)

# Filter out binary files by extension
declare -a TEXT_FILES=()
for f in "${EXISTING_FILES[@]}"; do
  ext="${f##*.}"
  is_binary=0
  for bext in $BINARY_EXTS; do
    if [[ "${ext,,}" == "$bext" ]]; then
      is_binary=1
      break
    fi
  done
  if [[ "$is_binary" -eq 0 ]]; then
    TEXT_FILES+=("$f")
  fi
done

# ── 1b. Write ingest manifest (immediately after scan, before any files are copied) ──
echo "→ Writing ingest manifest..."
MANIFEST="$DEST/_inbox/INGEST_MANIFEST.md"
mkdir -p "$DEST/_inbox"

{
  echo "# Ingest Manifest"
  echo "Generated: $(date '+%Y-%m-%d %H:%M:%S')"
  echo ""
  for f in "${TEXT_FILES[@]}"; do
    rel="${f#$DEST/}"
    if [[ -f "$f" ]]; then
      size_bytes=$(wc -c < "$f" 2>/dev/null || echo 0)
      if (( size_bytes >= 1048576 )); then
        size_str="$(echo "scale=1; $size_bytes / 1048576" | bc) MB"
      elif (( size_bytes >= 1024 )); then
        size_str="$(echo "scale=1; $size_bytes / 1024" | bc) KB"
      else
        size_str="${size_bytes} B"
      fi
      echo "- $rel ($size_str)"
    fi
  done
} > "$MANIFEST"

echo "  + $MANIFEST"

# ── 2. Download template ───────────────────────────────────────────────────────
echo "→ Downloading ops template..."
rm -rf "$TEMPLATE_DIR"
if ! git clone --depth 1 --branch "$TEMPLATE_BRANCH" "$TEMPLATE_REPO" "$TEMPLATE_DIR" 2>&1; then
  echo "ERROR: Failed to download template. Check your internet connection."
  exit 1
fi

# ── 3. Create framework directories ───────────────────────────────────────────
echo "→ Creating framework directories..."
for dir in context memory projects decisions audits references scheduled-tasks docs _inbox _archive; do
  mkdir -p "$DEST/$dir"
done

# ── 4. Copy template files (never overwrite) ──────────────────────────────────
echo "→ Copying template files..."

copy_if_missing() {
  local src="$1"
  local dst="$2"
  if [[ ! -e "$dst" ]]; then
    mkdir -p "$(dirname "$dst")"
    cp "$src" "$dst"
    echo "  + $dst"
  fi
}

# Top-level framework files
for fname in CLAUDE.md MAP.md GUARDRAILS.md EXPANSIONS.md connections.md endpoints.md; do
  if [[ -f "$TEMPLATE_DIR/$fname" ]]; then
    copy_if_missing "$TEMPLATE_DIR/$fname" "$DEST/$fname"
  fi
done

# Skills
for skill in onboard new-from-template; do
  skill_src="$TEMPLATE_DIR/.claude/skills/$skill/SKILL.md"
  skill_dst="$DEST/.claude/skills/$skill/SKILL.md"
  if [[ -f "$skill_src" ]]; then
    copy_if_missing "$skill_src" "$skill_dst"
  fi
done

# Scripts
for sname in merge-settings.py setup.sh; do
  if [[ -f "$TEMPLATE_DIR/scripts/$sname" ]]; then
    copy_if_missing "$TEMPLATE_DIR/scripts/$sname" "$DEST/scripts/$sname"
  fi
done

# Hooks directory (copy each file individually)
if [[ -d "$TEMPLATE_DIR/hooks" ]]; then
  mkdir -p "$DEST/hooks"
  for hook_src in "$TEMPLATE_DIR/hooks/"*; do
    [[ -f "$hook_src" ]] || continue
    hook_dst="$DEST/hooks/$(basename "$hook_src")"
    copy_if_missing "$hook_src" "$hook_dst"
  done
fi

# Stub context/memory files
for stub in context/me.md context/goals.md context/work.md memory/MEMORY.md; do
  if [[ -f "$TEMPLATE_DIR/$stub" ]]; then
    copy_if_missing "$TEMPLATE_DIR/$stub" "$DEST/$stub"
  fi
done

# ── 6. Wire up Claude Code (non-interactive) ───────────────────────────────────
echo "→ Wiring up Claude Code hooks..."
mkdir -p "$HOME/.claude/hooks"

for hook_src in "$DEST/hooks/"*; do
  [[ -f "$hook_src" ]] || continue
  hook_name="$(basename "$hook_src")"
  hook_dst="$HOME/.claude/hooks/$hook_name"
  if [[ -e "$hook_dst" ]]; then
    echo "  ⚠  Skipping $hook_name — already exists in ~/.claude/hooks/ (not overwriting)"
  else
    cp "$hook_src" "$hook_dst"
    echo "  + ~/.claude/hooks/$hook_name"
  fi
done

# Merge settings
if [[ -f "$DEST/scripts/merge-settings.py" ]]; then
  echo "→ Updating ~/.claude/settings.json..."
  python3 "$DEST/scripts/merge-settings.py" || echo "  ⚠  merge-settings.py failed — run manually if needed"
fi

# ── 7. Clean up ───────────────────────────────────────────────────────────────
echo "→ Cleaning up..."
rm -rf "$TEMPLATE_DIR"

# ── 8. Done ───────────────────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  Install complete!                      ║"
echo "╠══════════════════════════════════════════╣"
echo "║  Open Claude Code in this directory     ║"
echo "║  and run /onboard to organize your      ║"
echo "║  repo intelligently.                    ║"
echo "╚══════════════════════════════════════════╝"
echo ""
