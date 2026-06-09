# Personal Ops — Claude Entry Point

> **Setup status:** If this file still contains `[PLACEHOLDER]` tokens, run `/onboard` to complete setup.
> Once setup is done, this file is your permanent ops profile. Edit it directly anytime.

---

**Name:** [YOUR_FULL_NAME]
**Email:** [YOUR_EMAIL_ADDRESS]
**Timezone:** [YOUR_TIMEZONE — e.g. PST, EST, CET]
**What I do:** [ONE_LINE_SUMMARY — e.g. "Freelance ops consultant + job seeker"]
**Key tools:** [TOOLS_YOU_USE — e.g. Notion, Slack, GitHub, Linear]

**Current focus:**
1. [FOCUS_AREA_1 — e.g. Job search: senior ops roles at Series B startups]
2. [FOCUS_AREA_2 — e.g. Client work: 2 active accounts]
3. [FOCUS_AREA_3 — e.g. Building: personal automation stack]

---

## Session Boot

Run in order every session:

1. Load `context/me.md` — always, every session. This is voice, tone, communication style.
2. Identify the task → load ONE entry from the routing table below.
3. Stop. Do not load additional files unless the task explicitly requires them.

---

## Task Routing

| If the task is... | Load this |
|---|---|
| Writing in my voice (posts, emails, applications) | `context/me.md` (already loaded in step 1) |
| [PROJECT_1_NAME — e.g. Client: Acme account] | `projects/[project-1-folder]/CLAUDE.md` |
| [PROJECT_2_NAME — e.g. Job search pipeline] | `projects/[project-2-folder]/CLAUDE.md` |
| [PROJECT_3_NAME — e.g. Newsletter] | `projects/[project-3-folder]/CLAUDE.md` |
| Running a scheduled task | `scheduled-tasks/<task-name>/` — that task's file only |
| Debugging a broken integration | `connections.md` |
| Looking up an endpoint or database ID | `endpoints.md` |
| Career goals or target roles | `context/goals.md` |
| My employment status or availability | `context/work.md` |
| Why something was built a certain way | `decisions/log.md` |
| People, project notes, or terminology | `memory/MEMORY.md` → then the specific file |
| Finding a file or navigating the repo | `MAP.md` |

---

## Before Building Anything New

Run this check before creating any file, folder, or skill:

1. **Check `MAP.md`** — does a home already exist for this?
2. **Check `skills/README.md`** — does a skill for this already exist?
3. **Check `EXPANSIONS.md`** — run the 3-question test before any new folder
4. **Log the decision** in `decisions/log.md` if it's architectural

If adding an in-repo skill (most common):
- Create it at `.claude/skills/<name>/SKILL.md` — Claude Code auto-discovers it
- Check `skills/README.md` first to avoid duplicating something that already exists
- Run `python3 skills/sync.py --write` to update the human-readable index
- Log the decision in `decisions/log.md`

If adding a global skill (external, shared across all your repos):
- Register in `~/.claude/registry.json` then run `python3 skills/sync.py --write`

If modifying `CLAUDE.md` or `MAP.md`:
- Read `GUARDRAILS.md` first
- Commit separately with prefix `structure:`

---

## Connections Quick-Reference

Full details → `connections.md` | Endpoint IDs → `endpoints.md`

| Task | Use |
|---|---|
| [TOOL_1 — e.g. Project management] | [HOW — e.g. Notion MCP] |
| [TOOL_2 — e.g. Communication] | [HOW — e.g. Slack MCP] |
| Fetch API secrets or tokens | `infisical` CLI — never from `.env` files |

---

## Self-Maintenance

| Cadence | What runs | What it maintains |
|---|---|---|
| Every session | Session boot: `context/me.md` | Voice and style consistency |
| Every Friday | `weekly-ops-audit` skill | Repo health + skills sync |
| Quarterly | Review `context/goals.md` | Targets stay current |
| Quarterly | Review CLAUDE.md focus areas | Projects and priorities stay accurate |
| When a tool breaks | Update `connections.md` status | Integration registry stays honest |

---

## What NOT to Load

- `_tools/graphify/GRAPH_REPORT.md` — 12MB+, destroys context. Query via `graphify` CLI only.
- All `context/` files at once — selective loading is the whole point.
- Skill files directly — invoke via `Skill("name")`, never read `SKILL.md` files.
- `memory/` wholesale — use `MEMORY.md` index first, then the specific file.
- `scheduled-tasks/` wholesale — load one task directory at a time.
- Any `_archive/` folder — raw ingested content, never useful in a normal session.

---

## Never Do These

| Don't | Because |
|---|---|
| Read `_tools/graphify/GRAPH_REPORT.md` | 12MB+, destroys context window |
| Load all `context/` files at once | Selective loading is the whole point |
| Read skill files directly | `Skill()` loads them automatically |
| Store secrets in `.env` files | Infisical is the single source of truth |
| Create `notes/`, `misc/`, or `tmp/` folders | They become graveyards — see `EXPANSIONS.md` |
| Add a second `CLAUDE.md` at the repo root | One canonical entry point only |
