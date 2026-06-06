# EXPANSIONS — When and How to Grow This Repo

This repo ships deliberately sized. Add only what's needed, when it's needed.

> The structure should look like a well-run operation — not a hoarder's basement.
> When you can't find something, consolidate. Don't add another folder.

---

## What's Here and Why

| Folder / File | Purpose | Add content when |
|---|---|---|
| `context/` | Permanent identity — who [YOUR_NAME] is, voice, goals, status | Only update existing files; new files need a strong reason |
| `memory/` | Session recall — people, project snapshots, glossary, overview | Cross-session facts that don't belong in context/ |
| `decisions/log.md` | Append-only architectural and strategic decisions | After every meaningful architectural or strategic call |
| `connections.md` | Registry of every active integration | Every time a new tool is wired in or auth changes |
| `endpoints.md` | Frequently used IDs and URLs | When a new Notion DB, Drive folder, or URL is regularly referenced |
| `projects/` | Active workstreams with their own CLAUDE.md | Workstream runs 3+ weeks and needs scoped context |
| `references/` | Frameworks, SOPs, API guides (research-once, saved-forever) | A framework or API gets used 3+ times |
| `docs/` | Strategy and spec documents | Cross-project strategy brainstorms, design specs |
| `audits/` | Dated ops audit snapshots | After each weekly ops audit run |
| `skills/` | Claude skill library + sync tooling | An automation runs 3+ times in a month |
| `agents/` | Sub-agents for repeatable multi-step tasks | Task is too long for one context window |
| `scheduled-tasks/` | Cron-based automations | Task runs weekly or more without human input |
| `scripts/` | Utility and one-off scripts | Supports multiple tasks or runs ad hoc |
| `_templates/` | Reusable prompt and doc scaffolds | You copy-paste the same prompt 3+ times |
| `_tools/` | Generated outputs and tool artifacts | A tool generates files you keep but never read manually |

---

## The Three Questions (before adding any folder)

1. **Is this conceptually new?** Or does it fit an existing folder?
2. **Will I touch this 3+ times in the next month?** If not, it's premature.
3. **Could a future skill route here naturally?** If yes, the system will use it.

**Two yeses = add. One yes = wait.**

---

## Folder Boundary Definitions

**context/ vs memory/**
- `context/` = who [YOUR_NAME] IS — permanent, slow-changing identity (voice, goals, status)
- `memory/` = what Claude should RECALL — people notes, project snapshots, running glossary

**projects/ vs scheduled-tasks/**
- `projects/` = workstreams with strategy, docs, and human decision points
- `scheduled-tasks/` = automations that run without human input on a schedule

**references/ vs docs/**
- `references/` = generic reusable knowledge (frameworks, SOPs, API guides)
- `docs/` = project-specific strategy and specs

**scripts/ vs scheduled-tasks/**
- `scripts/` = utility scripts, one-off tools, helpers used manually
- `scheduled-tasks/` = fully packaged cron automations with their own runner and README

**connections.md vs endpoints.md**
- `connections.md` = HOW you connect (tool, auth method, MCP/CLI, status)
- `endpoints.md` = WHERE you connect (specific database IDs, page IDs, URLs)

---

## Anti-Patterns — What Not to Add

- **No `notes/`, `misc/`, `tmp/`, or `inbox/`** — graveyards. Use `memory/` for ongoing facts, `context/archives/` for old files.
- **No folder-of-folders for organization theater** — flat with good naming beats deep nesting.
- **No parallel decision logs** — `decisions/log.md` is the one. No `decisions.md` at root.
- **No pre-created empty folders** — add when you have real content in hand.
- **No raw dumps into `references/`** — interpreted facts and summaries only.
- **No second `CLAUDE.md` at root** — one canonical entry point. Projects can have scoped files.
- **Never read `_tools/graphify/GRAPH_REPORT.md` directly** — 12MB+. Use the graphify CLI.
- **Never duplicate context/me.md** — if you need a lightweight reference, link to it.

---

## Cadences

- `decisions/log.md` — after every meaningful architectural or strategic decision
- `connections.md` — whenever a new tool is wired in or auth changes
- `endpoints.md` — whenever a new Notion DB, Drive folder, or URL gets regularly used
- `memory/` — after sessions where new persistent facts emerge about people or projects
- `audits/` — after each weekly ops audit run
- `skills/README.md` — auto-updated by `weekly-ops-audit` via `python3 skills/sync.py --write`
- `CLAUDE.md` — review quarterly; update focus areas and projects when priorities shift
- `context/` — slow-moving; edit only when something fundamental changes

---

## How to Tell When It's Time to Add a Folder

Three questions. Two yeses = add. One yes = wait.
If you add it, log the decision in `decisions/log.md`.
If you're not sure, read `GUARDRAILS.md` first.
