# [YOUR_NAME]-Ops — Claude Code Template

A personal setup that gives Claude Code a memory, a voice, and a system — one centralized knowledge base that all your ops, agents, and workflows run through.

---

## Quick Start (no terminal required)

**1. Clone the template**

Use GitHub's Code button on [this repo](https://github.com/kwoekel/kwoekel-ops-template) to clone it to your computer, or use your git client of choice. No command line needed.

**2. Open in Claude Code**

Open the cloned folder in:
- **Claude Code desktop app**, or
- **claude.ai/code** in your web browser

**3. Run the setup wizard**

In the Claude Code chat, type:

```
/onboard
```

The wizard will ask you questions conversationally. You can:
- **Start fresh** — answer all questions (5 min)
- **Import an existing repo** — Claude analyzes your project and pre-fills what it can
- **Import from GitHub** — same as above but from a GitHub repo URL

All your files will be generated and committed automatically. No terminal commands needed.

---

## After Setup

Your personal ops repo is now ready. You'll have:

- **CLAUDE.md** — your profile, focus areas, email, timezone
- **context/me.md** — how you like to communicate and work
- **connections.md** — links to tools you use (Notion, Slack, etc.)
- **Memory system** — Claude now remembers context across sessions
- **Skills & workflows** — pre-built planning, code review, and ops tools

You can always edit any of these files later if you need to change something.

---

## Staying Up to Date

If this template gets updated and you want to pull in the changes, run this once after setup to connect your copy to the original:

```bash
git remote add upstream https://github.com/kwoekel/kwoekel-ops-template
```

Then whenever you want to check for updates:

```bash
git fetch upstream
git merge upstream/master
```

If you've edited the same files that changed in the template, Git will flag a conflict and ask you to choose which version to keep. Files you haven't touched will update automatically.

---

## What This Sets Up

| Tool | What it does in plain terms |
|---|---|
| **context-mode** | Stops Claude from filling up its memory with huge chunks of irrelevant output |
| **claude-mem** | Gives Claude a memory that carries over between sessions |
| **graphify** | Lets Claude understand your codebase by querying it, instead of reading every file |
| **token-dashboard** | Shows you how much of Claude's memory budget you're using |
| **Skills & plugins** | Pre-built workflows Claude can use (project planning, code review, ops tools) |

---

## Need Help?

If something breaks during setup, look at the error message and ask Claude Code what it means — paste the error and say "what does this mean and how do I fix it?"
