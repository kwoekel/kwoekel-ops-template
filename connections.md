# Connections Registry

Live table of every active integration. Update Status when something breaks or auth is refreshed.

| Domain | Tool / Service | How Connected | Auth Method | Used By | Status |
|--------|---------------|---------------|-------------|---------|--------|
| **Productivity** | [Tool] | [MCP / CLI / Plugin] | [Token/OAuth via X] | [task-name] | ✅ Active |
| **Dev** | GitHub | `gh` CLI (primary) | OAuth / token | Code context, PRs | ✅ Active |
| **Secrets** | Infisical | CLI + env injection | Service token | All scheduled tasks | ✅ Active |

> Add a row for every tool you wire in. Status = ✅ Active / ⚠️ Auth needed / ❌ Broken

---

## Task Routing

| Task | Use this tool/MCP |
|---|---|
| [Task description] | [Tool / MCP name] |
| Fetch API secrets / tokens | `infisical` CLI — never from .env |

---

## Notes

- **Default to CLIs where available** (`gh` for GitHub, `infisical` for secrets) — use MCPs as fallback.
- **Infisical is the single source of truth** for all API keys — never stored in .env or code.
- When auth breaks, check the source OAuth connection first before assuming a code bug.

## Last verified: [DATE]
