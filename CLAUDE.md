# [YOUR_NAME] Ops — Claude Entry Point

**[YOUR_NAME] | [YOUR_FOCUS_AREAS]**
**Timezone:** [TIMEZONE] | **Email:** [YOUR_EMAIL]
**Tools:** [list your key tools here]

**Focus areas:**
1. [Focus area 1]
2. [Focus area 2]
3. [Focus area 3]

---

## Session Boot

Run in order every session:

1. Load `context/me.md` — always, every session (voice, comm style, working prefs).
2. Identify the task area → load ONE entry from the routing table below.
3. Stop. Do not load additional context files unless the task explicitly requires them.

---

## Task Routing

| Task | Load |
|------|------|
| Writing in [YOUR_NAME]'s voice (posts, emails, applications) | `context/me.md` (step 1, already loaded) |
| [Project 1 description] | `projects/[project-1]/CLAUDE.md` |
| [Project 2 description] | `projects/[project-2]/CLAUDE.md` |
| [Project 3 description] | `projects/[project-3]/CLAUDE.md` |
| Scheduled task work | `scheduled-tasks/<task-name>/` — load that task's file only |
| Debugging integrations / checking what's connected | `connections.md` |
| Look up an endpoint ID | `endpoints.md` |
| Architecture decisions / why something was built | `decisions/log.md` |
| Career focus / target roles | `context/goals.md` |
| Employment status / availability | `context/work.md` |
| People notes, project snapshots, or terms | `memory/MEMORY.md` → specific file |
| Navigating the repo or finding a file | `MAP.md` |

---

## Before You Build Anything New

Run this check before creating any file, folder, or skill:

1. **Check MAP.md** — does a home already exist for this?
2. **Check skills/README.md** — does a skill for this already exist?
3. **Run the 3-question test** (EXPANSIONS.md) before any new folder
4. **Log the decision** in `decisions/log.md` if it's architectural

If you're adding a skill:
- Check `skills/README.md` first
- Run `python3 skills/sync.py --write` after registering in `~/.claude/registry.json`
- Log in `decisions/log.md`

If you're modifying CLAUDE.md or MAP.md:
- Read GUARDRAILS.md first
- Commit separately with prefix `structure:`

---

## Self-Maintenance Schedule

| Cadence | What runs | What it maintains |
|---|---|---|
| Every session | Session boot (`context/me.md`) | Voice and style consistency |
| Every Friday | `weekly-ops-audit` | 4Cs health + repo drift detection + skills sync |
| Quarterly | Review `context/goals.md` | Targets stay current |
| Quarterly | Review CLAUDE.md focus areas | Projects and priorities stay accurate |
| When a tool breaks | Update `connections.md` status | Integration registry stays honest |

---

## What NOT to Load

- `_tools/graphify/GRAPH_REPORT.md` — 12MB+, will explode context. Use graphify CLI.
- All `context/` files at once — always selective by task.
- `skills/` SKILL.md files directly — invoke via `Skill("name")`.
- `memory/` wholesale — use `memory/MEMORY.md` index first, then the specific file.
- `scheduled-tasks/` wholesale — load one task directory at a time.

---

## Skills Registry

> Invoke via `Skill("skill-name")` — never read SKILL.md files directly.
> Full categorized table → `skills/README.md`

---

## Connections Quick-Reference

> Full details, auth methods, and status → `connections.md`
> Endpoint IDs → `endpoints.md`

| Task | Use |
|---|---|
| [Your tool 1] | [How to invoke it] |
| [Your tool 2] | [How to invoke it] |
| Secrets | `infisical` CLI — single source of truth for all API keys |

---

## Never Do These

| Don't | Because |
|---|---|
| Read `_tools/graphify/GRAPH_REPORT.md` | 12MB+, destroys context |
| Load all `context/` files at once | Selective loading is the whole point |
| Read skill files directly | `Skill()` loads automatically |
| Load all of `scheduled-tasks/` | Many dirs × file reads = massive waste |
| Create `notes/`, `misc/`, `tmp/` | Graveyards. See `EXPANSIONS.md`. |
| Add a second root CLAUDE.md | One canonical entry point only |
