---
name: setup
description: Optional one-time installer of local tooling for this template (graphify, plugins, hooks, weekly ops audit). Use after /onboard, only in the Claude Code desktop app or VS Code extension. Not for claude.ai web users.
disable-model-invocation: true
---

# Local Tooling Setup

A thin, friendly wrapper around `scripts/setup.sh`. The script does the actual
installing (it is deterministic and safe to re-run); this skill picks the right
moment to run it and explains the results in plain language.

**Do not reimplement the install steps here.** All install logic lives in
`scripts/setup.sh`. This skill's only jobs are: confirm the platform, run the
script, and interpret the output for the user.

## Step 1 — Confirm the platform

Ask where the user is running (AskUserQuestion):

- **Claude Code (desktop app or VS Code extension)** → continue to Step 2.
- **claude.ai (web browser)** → stop. The web version has no terminal, so nothing
  can be installed. Tell them: all core features (onboarding, skills, memory) work
  without this step. If they later open the repo in the Claude Code desktop app,
  they can run `/setup` then.

## Step 2 — Run the installer

From the repo root, run:

```bash
bash scripts/setup.sh
```

The script is non-blocking by design — every step has a fallback, so a missing
tool (e.g. `pipx` or Node) prints a warning and the rest continues. It installs:

| Step | What it sets up | If it fails |
|---|---|---|
| graphify | Codebase knowledge-graph CLI (via pipx) | Warns; install pipx then `pipx install graphifyy` |
| Plugins | Curated Claude Code plugins (context-mode, claude-mem, etc.) | Skips ones already installed |
| Hooks | Copies repo hooks into `~/.claude/hooks/` | Skipped silently if unavailable |
| Settings | Merges hook + safety rules into `~/.claude/settings.json` | — |
| Skills index | Refreshes `skills/README.md` (skills already auto-load) | Non-blocking |
| Submodules | Initializes `token-dashboard` | Warns if unreachable |
| Weekly audit | launchd agent for the weekly ops audit (**Mac only**) | Skipped on non-Mac |

## Step 3 — Report

Read the script's output and tell the user, in plain language:

- ✅ what installed successfully and what it now unlocks
- ⚠️ what was skipped or warned, and the one command to fix it if they want it
- That the repo is fully usable regardless — this step is purely additive

Never present this as "setup failed." Worst case, some optional tools were skipped.

## Notes

- Manual command (`disable-model-invocation`): runs only when the user types
  `/setup`, never automatically, because it mutates the global `~/.claude/` config.
- Safe to re-run anytime — re-running picks up updated hooks and newly available tools.
