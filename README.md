# [YOUR_NAME]-Ops — Claude Code Template

A personal setup that gives Claude Code a memory, a voice, and a system — one centralized knowledge base that all your ops, agents, and workflows run through.

---

## Before You Start

Make sure you have these installed:

- **Git** — [download here](https://git-scm.com/downloads)
- **Python 3** — [download here](https://www.python.org/downloads/) (most Macs already have it)
- **Claude Code** — [install here](https://claude.ai/code) (the desktop app or CLI)

Not sure if you have them? Open your Terminal (on Mac: press `Cmd + Space`, type `Terminal`, hit Enter) and run:

```bash
git --version
python3 --version
```

If both print a version number, you're good.

---

## Setup (takes about 5 minutes)

**Step 1 — Open your Terminal**

On Mac: `Cmd + Space` → type `Terminal` → press Enter

**Step 2 — Copy and run these commands one at a time**

Replace `[YOUR-NAME]` with your actual name (no spaces, e.g. `alex-ops`):

```bash
git clone [this-repo-url] [YOUR-NAME]-ops
cd [YOUR-NAME]-ops
bash setup.sh
python3 scripts/onboard.py --fresh
```

Each command does one thing:
- `git clone` — downloads the template to your computer
- `cd` — moves into the folder you just created
- `bash setup.sh` — installs the tools this system uses
- `python3 scripts/onboard.py --fresh` — runs a wizard that sets up your personal details

The wizard will ask you questions. Just answer them — no coding required.

---

## After Setup — Fill In Your Details

Open the files below and replace the `[PLACEHOLDER]` text with your real information. Each file has instructions inside it.

| File | What to fill in |
|---|---|
| `CLAUDE.md` | Your name, focus areas, timezone, and email |
| `context/me.md` | How you like to communicate, your working style |
| `connections.md` | Any tools you use (Notion, Slack, etc.) |
| `endpoints.md` | Any API IDs or webhook URLs you reference often |

To open a file: in your Terminal, type `open CLAUDE.md` and it will open in a text editor.

---

## Already Have a Repo You Want to Import?

If you have an existing project folder you want Claude to learn from:

```bash
python3 scripts/onboard.py --import /path/to/your/repo
```

Or import directly from GitHub:

```bash
python3 scripts/onboard.py --import-github owner/repo
```

Replace `owner/repo` with the GitHub username and repo name (e.g. `ACME/my-project`).

Claude will read the repo and pre-fill your context files automatically.

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
