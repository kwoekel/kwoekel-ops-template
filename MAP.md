# [YOUR_NAME] Ops — Navigation Map
**[YOUR_NAME] | [YOUR_FOCUS_AREAS]**
Last updated: [DATE]

> This file is the visual index of the entire repo. It does not load content — it routes.
> Claude: read this when you need to find something. Don't load what you don't need.

---

## Session Boot

```
Every session → Load context/me.md first, always.
Then identify task → load ONE entry from Task Routing below.
Stop. Do not load more.
```

---

## Task Routing

| I need to... | Load this | Notes |
|---|---|---|
| Write in [YOUR_NAME]'s voice | `context/me.md` | Already loaded in boot |
| [Project 1] | `projects/[project-1]/CLAUDE.md` | |
| [Project 2] | `projects/[project-2]/CLAUDE.md` | |
| Run a scheduled task | `scheduled-tasks/<name>/` — that task's file only | One at a time |
| Debug an integration | `connections.md` | |
| Look up an endpoint ID | `endpoints.md` | |
| Review architectural decisions | `decisions/log.md` | |
| Work on a skill | See Skills Registry | Invoke via `Skill("name")` |

---

## File Map

### Identity & Context
```
context/
├── me.md               ← WHO [YOUR_NAME] IS — voice, tone, comm style, working prefs
├── goals.md            ← Career targets, priorities, hard requirements
├── work.md             ← Current employment status and availability
└── archives/           ← Superseded context files
```

### Memory (Session Recall)
```
memory/
├── MEMORY.md           ← Index. Start here.
├── overview.md         ← Big picture: world + current quarter priorities
└── glossary.md         ← Acronyms, shorthand, project paths
```

### Operations
```
connections.md          ← Every active integration: tool, connection method, auth, status
endpoints.md            ← Frequently used IDs: databases, folders, channels
decisions/
└── log.md              ← Append-only: architectural and strategic decisions
```

### Projects
```
projects/
├── [project-1]/        ← [Description]
│   └── CLAUDE.md
├── [project-2]/
│   └── CLAUDE.md
└── example-project/    ← Template example — replace with real projects
    └── CLAUDE.md
```

### Automations
```
scheduled-tasks/
├── _config/            ← Shared config
├── _lib/               ← Shared library code
├── weekly-ops-audit/   ← Runs every Friday — repo health + skills sync
└── example-task/       ← Template stub — replace with real tasks
```

### Skills & Agents
```
skills/
├── README.md           ← Skills registry — invoke via Skill("name")
├── sync.py             ← Auto-syncs ~/.claude/registry.json → README.md
└── new-from-template/

agents/
├── ceo/AGENT.md        ← Strategic lens
└── cto/AGENT.md        ← Technical lens
```

### Scripts & Utilities
```
scripts/
├── setup.sh            ← One-command installer (run once after clone)
├── onboard.py          ← Onboarding wizard (fresh start or import existing repo)
├── merge-settings.py   ← Merges hooks + safety rules into ~/.claude/settings.json
├── install-launchd.py  ← Sets up weekly-ops-audit launchd agent (Mac)
├── auto-sync.sh        ← Git auto-sync utility
└── notion-mcp.sh       ← Starts the Notion MCP server
```

### Tool Artifacts (Never Read Directly)
```
_tools/
└── graphify/
    └── GRAPH_REPORT.md  ← 12MB+. NEVER read directly. Use: graphify query / graphify path
```

### Hooks
```
hooks/                  ← Claude Code hook scripts — copied to ~/.claude/hooks/ by setup.sh
```

### Config
```
.claude/settings.json   ← Claude Code tool config + PreToolUse hooks (project-level)
token-dashboard/        ← Git submodule: token analytics (open dashboard.html in browser)
```
