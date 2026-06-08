---
name: onboard
description: Interactive conversational wizard that personalizes this ops template for a new owner. Fills [PLACEHOLDER] values across the repo and commits the result. Use when someone has just cloned the template and wants to set it up.
disable-model-invocation: true
---

# Onboarding Wizard

The front door for anyone who just cloned this template. It turns the blank
template into *their* personal ops repo — conversationally, with no terminal
commands required. Works in both the Claude Code desktop app and claude.ai.

## What this does

1. **Choose a path** — fresh start, import a local repo, or import from GitHub
2. **Gather context** — if importing, analyze the source so values can be pre-filled
3. **Fill the gaps** — ask only about what couldn't be confidently inferred
4. **Commit** — write every file and make one git commit

This skill only fills `[PLACEHOLDER]` tokens. It never deletes existing content.

## The flow

### Step 1 — Pick a mode

Ask the user which one fits (use AskUserQuestion):

- **Fresh start** — answer all placeholder questions from scratch (~5 min)
- **Import a local repo** — read an existing project's files and pre-fill what you can
- **Import from GitHub** — same, but pull the repo from a GitHub URL

### Step 2 — Gather context (import modes only)

If importing, build a picture of the owner before asking anything:

- Read the source's `README`, `package.json`, `pyproject.toml`, `CLAUDE.md`, and similar
- Scan the folder structure
- Infer name, email, GitHub handle, timezone, tech stack, and focus areas

For **local import**, read from the filesystem with the Read/Glob tools.
For **GitHub import**, fetch the repo's files via WebFetch. If the repo is private
or unreachable, say so plainly and offer to switch to fresh mode.

### Step 3 — Fill the placeholders

Fill `[PLACEHOLDER]` values across the template files, using inferred values where
confident and asking the user only for the rest. Files that contain placeholders:

- `CLAUDE.md` — name, email, focus areas, timezone, tooling
- `context/me.md` — communication style and working preferences
- `context/goals.md` — career / business targets
- `connections.md` — tools in use (Notion, Slack, etc.)
- `memory/MEMORY.md`, `decisions/log.md`, and any `agents/*/AGENT.md`

The placeholder values you will need:

- Full name
- Email address
- GitHub username
- Timezone (PST, EST, CET, UTC, …)
- 2–3 focus areas (e.g. "Job search, AI consulting")
- The three main focus areas, labeled individually (skip if same as above)
- (Optional) Main services / portfolio page name

If you cannot confidently infer a value, ask for it. Never invent personal details.

### Step 4 — Show and confirm

Before committing, show the user what was filled in (especially inferred values)
so they can correct anything. Then write all files with the Write tool.

### Step 5 — Commit

```
Initial setup: personalized ops repo

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
```

## After the wizard

Tell the user:

1. **Review `CLAUDE.md`** and confirm everything reads correctly
2. **Add their voice** to longer sections like `context/me.md` that need real prose
3. **Connect tools** in `connections.md` if they use Notion, Slack, etc.
4. **(Optional, Claude Code only)** run **`/setup`** to install local tooling —
   graphify, plugins, hooks, and the weekly ops audit. Web users can skip this;
   all core features work without it.

## Re-running

Safe to re-run. It only touches remaining `[PLACEHOLDER]` tokens, so already-filled
values are left alone. To undo a run: `git reset HEAD~1` (undo the commit) or
`git reset --hard` (revert to the clean template).

## Notes

- Everything happens inside Claude Code or claude.ai — no terminal needed.
- This is a manual command (`disable-model-invocation`): it runs only when the
  user types `/onboard`, never automatically, because it writes files and commits.
