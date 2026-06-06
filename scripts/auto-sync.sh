#!/usr/bin/env bash
set -euo pipefail

REPO="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$REPO"

# Skip if not a git repo
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0

# Skip if nothing changed
if [[ -z "$(git status --porcelain)" ]]; then
  exit 0
fi

# Skip detached HEAD
BRANCH="$(git rev-parse --abbrev-ref HEAD)"
if [[ "$BRANCH" == "HEAD" ]]; then
  exit 0
fi

# Stage, commit, and push
git add -A
git commit -m "chore: auto-sync $(date '+%Y-%m-%d %H:%M:%S')" || exit 0
git push origin "$BRANCH"
