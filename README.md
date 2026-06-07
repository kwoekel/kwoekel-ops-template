# [YOUR_NAME]-Ops — Claude Code Template

> **Placeholders:** Everything in `[BRACKETS]` is a placeholder you fill in.
> `[YOUR_NAME]` → your actual name (e.g. `Alex`).
> `-Ops` is a fixed suffix — keep it as-is. It identifies the repo type, not a person.
> All other `[BRACKETS]` in `CLAUDE.md` are also placeholders.

A self-installing personal ops repo for Claude Code. Clone → run setup → fill in your details.

## Quick Start

```bash
git clone [this-repo-url] [YOUR-NAME]-ops
cd [YOUR-NAME]-ops
bash setup.sh
python3 scripts/onboard.py --fresh
```

## What You Get

- Session boot + task routing framework (`CLAUDE.md`)
- Context-saving tools: context-mode, claude-mem, graphify
- Skills: GSD project framework, superpowers craft skills, ops tools
- Weekly ops audit (runs Fridays via launchd on Mac)
- Token usage dashboard
- Two-mode onboarding wizard (fresh start or import existing repo)

## Import an Existing Repo

```bash
python3 scripts/onboard.py --import /path/to/your/repo
```

Claude analyzes the repo and pre-fills context files. The wizard handles anything it can't auto-detect.

You can also import directly from GitHub:

```bash
python3 scripts/onboard.py --import-github owner/repo
```

`--import-github` accepts `owner/repo` or a full GitHub repo URL.

## Tools Installed by `setup.sh`

| Tool | What it does |
|---|---|
| context-mode | Sandboxes large outputs so they don't blow up context |
| claude-mem | Persistent cross-session memory |
| graphify | Knowledge graph of your codebase — query instead of reading raw files |
| token-dashboard | Visual token usage analytics |
| Claude Code plugins | Skills, code review, GSD, superpowers, and more |

## After Setup

1. In `CLAUDE.md`, replace `[YOUR_NAME]` with your name and fill in all other `[PLACEHOLDER]` blocks
2. Fill in `context/me.md` with your voice and working preferences
3. Add tool connections to `connections.md`
4. Add endpoint IDs to `endpoints.md`
5. Run `python3 skills/sync.py --write` after adding custom skills
