#!/bin/bash
# Weekly ops audit — runs Fridays at 1pm via launchd.
# Step 1: fetch-audit-data.py collects JSON cheaply (zero Claude tokens).
# Step 2: passes collected data to claude --print for the full audit.
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null || dirname "$SCRIPT_DIR")"
LOG="$SCRIPT_DIR/run.log"
PYTHON="$(which python3)"

{
  echo "=== Weekly Ops Audit: $(date) ==="

  AUDIT_JSON=$(infisical run \
    --project-config-dir "$REPO_DIR" \
    --env dev \
    -- "$PYTHON" "$SCRIPT_DIR/fetch-audit-data.py" 2>/dev/null)

  echo "$AUDIT_JSON" | claude --print \
    --project-dir "$REPO_DIR" \
    "/ops-audit"

  echo "=== Done: $(date) ==="
} >> "$LOG" 2>&1
