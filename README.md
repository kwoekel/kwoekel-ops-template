# Ops Template — System Reference

A Claude-powered personal ops system. One repo = one brain for your work. Claude reads this repo at the start of every session and knows who you are, what you're working on, and how to help — without you re-explaining it every time.

---

## The Mental Model

Every session, Claude follows this sequence:

```
1. Read CLAUDE.md        ← who you are, what you're working on, what to load
2. Load context/me.md    ← your voice, communication style, working preferences
3. Identify the task     ← route to the right project or tool based on what you asked
4. Load ONE context file ← only what's needed for this session
5. Do the work
```

This is "selective loading." Claude never reads the whole repo — it reads exactly what the current task needs. This keeps sessions fast and focused.

---

## What Goes Where

| If you have... | It goes in... | Why |
|---|---|---|
| Your personal info, voice, preferences | `context/me.md` | Loaded every session — this is your baseline |
| Career goals, target roles, priorities | `context/goals.md` | Loaded when you're working on career tasks |
| Employment status, availability | `context/work.md` | Loaded when you need Claude to know your situation |
| A project (existing or new) | `projects/<project-name>/` | Each project is self-contained |
| An integration or tool connection | `connections.md` | Single registry — update when auth breaks |
| API endpoint IDs, database IDs | `endpoints.md` | Quick lookup, avoids hunting through docs |
| A scheduled automation | `scheduled-tasks/<name>/` | Each task is isolated in its own folder |
| Something you want Claude to remember across sessions | `memory/` | Indexed in `MEMORY.md`, recalled on demand |
| An architectural decision | `decisions/log.md` | Append-only; explains the why behind the system |
| A reusable workflow or slash command | `.claude/skills/` | Invoked with `/skill-name` |

---

## Folder Reference

### `context/` — Who You Are
Loaded selectively per session. The three files here are the most important in the repo.

- **`me.md`** — Your voice, communication style, personality, working preferences. Claude reads this first every session. Without it, Claude gives generic responses.
- **`goals.md`** — Career or business targets. Load this when working on job search, strategy, or priority setting.
- **`work.md`** — Employment status and availability. Keeps Claude calibrated on your situation.
- **`archives/`** — Old versions of context files. Move here instead of deleting.

### `projects/` — Your Work
Each project lives in its own folder. The standard shape is:

```
projects/<project-name>/
├── CLAUDE.md        ← entry point: purpose, status, how to work here
├── context/
│   ├── overview.md  ← what this project is and why it exists
│   ├── people.md    ← stakeholders, relationships (optional)
│   └── decisions.md ← project-specific decisions
├── planning/
│   └── roadmap.md   ← milestones and status
├── _inbox/          ← unsorted content awaiting triage (empty this regularly)
└── _archive/        ← raw source if ingested + INGEST-LEDGER.md (never read directly)
```

**To start a new project:** type `/new-from-template` in Claude Code.
**To bring in an existing repo:** type `/ingest-project` in Claude Code.

### `memory/` — Cross-Session Recall
Claude's long-term memory. Not loaded by default — consulted when relevant.

- **`MEMORY.md`** — Index. Always start here. One-line pointers to the actual memory files.
- **`overview.md`** — Big picture: current quarter, major priorities.
- **`glossary.md`** — Shorthand, acronyms, internal terms.

### `connections.md` — Tools and Integrations
Every active connection in one table: tool, how it's connected, auth method, status. Update the Status column whenever something breaks or needs a re-auth.

### `endpoints.md` — Frequently Used IDs
Database IDs, folder IDs, channel IDs — things you look up often. Faster than hunting through tool UIs.

### `scheduled-tasks/` — Automations
Each automation has its own folder with a `README.md` (what it does, how it runs) and a `run.sh` (the actual script). Secrets always go through Infisical — never in `.env` files.

### `decisions/log.md` — Why Things Are Built This Way
Append-only log of architectural and strategic decisions. When something seems weird, check here before changing it.

### `skills/README.md` — Slash Commands
Registry of all available skills. Each skill is a workflow Claude can run on demand. Invoke with `/skill-name` in the chat.

### `.claude/skills/` — Skill Definitions
The actual logic behind each skill. Never read these directly — they load automatically when you invoke `/skill-name`.

### `hooks/` — Automated Behaviors
Scripts that run automatically before/after Claude's tool calls. Handles things like read guards, context monitoring, and session state. Set up by `/setup` — don't edit unless you know what you're changing.

### `agents/` — Specialized Lenses
Pre-configured AI roles:
- **`ceo/`** — Strategic thinking: priorities, tradeoffs, ROI
- **`cto/`** — Technical thinking: architecture, implementation

### `_templates/` — Reusable Shapes
Blueprints for creating new projects. Don't edit these directly.
- **`project-skeleton/`** — Default project shape (used by `/new-from-template`)
- **`_examples/`** — Opt-in domain templates (lead-gen, four-phase roadmap)

---

## Skills (Slash Commands)

Type these in Claude Code chat:

| Skill | What it does |
|---|---|
| `/onboard` | First-time setup wizard. Fills all placeholder values across the repo and commits. Run this once after cloning. |
| `/setup` | Optional local tooling installer. Adds graphify, hooks, and weekly ops audit. Claude Code desktop/VS Code only. |
| `/new-from-template` | Creates a new project folder under `projects/` using the standard skeleton. |
| `/ingest-project` | Brings an existing repo into the framework. Organizes, dedupes, and documents everything — nothing gets lost. |

The full skills list lives in `skills/README.md`.

---

## First-Time Setup

1. Clone this repo
2. Open the folder in Claude Code (desktop app or VS Code extension) or claude.ai/code
3. Type `/onboard` in the chat
4. Answer the wizard's questions (or point it at an existing repo to pre-fill)
5. Review the committed files — edit anything that doesn't read right
6. *(Optional, desktop/VS Code only)* Type `/setup` to add local tooling

That's it. The repo is now personalized and ready.

---

## Maintaining It

| When | Do this |
|---|---|
| Tool breaks or auth expires | Update the Status in `connections.md` |
| New project | `/new-from-template` |
| Existing repo to bring in | `/ingest-project` |
| Career priorities change | Edit `context/goals.md` |
| New architectural decision | Append to `decisions/log.md` |
| Something seems broken | Ask Claude — paste the error and say "what does this mean?" |

---

## What NOT to Do

| Don't | Because |
|---|---|
| Store secrets in `.env` files | Use Infisical — it's the single source of truth for all API keys |
| Load all `context/` files at once | Selective loading keeps sessions fast |
| Read `_archive/` folders | Raw ingested content — too large, never useful in normal sessions |
| Create `notes/`, `misc/`, or `tmp/` folders | They become graveyards. See `EXPANSIONS.md` for the decision framework. |
| Add a second `CLAUDE.md` at the root | One canonical entry point only |
