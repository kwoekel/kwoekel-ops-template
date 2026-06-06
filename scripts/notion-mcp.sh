#!/bin/bash
set -e

REPO_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

NOTION_TOKEN=$(infisical run \
    --project-config-dir "$REPO_DIR" \
    --env dev \
    -- bash -c 'printf "%s" "$NOTION_TOKEN"' 2>/dev/null)

if [ -z "$NOTION_TOKEN" ]; then
    echo "ERROR: Could not get NOTION_TOKEN from Infisical" >&2
    exit 1
fi

export OPENAPI_MCP_HEADERS="{\"Authorization\": \"Bearer ${NOTION_TOKEN}\", \"Notion-Version\": \"2022-06-28\"}"
exec npx -y @notionhq/notion-mcp-server@latest
