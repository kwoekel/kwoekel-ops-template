# One-Line Install + Repo Ingest Design

**Date:** 2026-06-09
**Branch:** simplified-template
**Purpose:** Enable clients (or Kierra as consultant) to run a single command in a Codespace terminal that installs the ops framework into an existing messy repo and reorganizes it into best-practice structure.

---

## What This Is

A two-stage system:

1. **`curl | bash install.sh`** — deterministic scaffolding (bash)
2. **`/onboard` skill in ingest mode** — intelligent consolidation (Claude Code)

The bash script handles what's mechanical and safe. Claude Code handles what requires judgment — reading content, finding redundancy, synthesizing, and routing.

**Target environment:** GitHub Codespaces running against an existing git repo. Bash, git, and Python3 are always available. No additional tooling required.

---

## Stage 1: `install.sh` (bash)

### Entry point

```bash
curl -fsSL https://raw.githubusercontent.com/[your-github-username]/kwoekel-ops-template/simplified-template/scripts/install.sh | bash
```

> **Note:** Replace `[your-github-username]` with the actual GitHub username before distributing this to clients. The repo must be public (or the client must have access) for the raw URL to resolve.

### What it does

1. Downloads the `simplified-template` branch to a temp dir (`/tmp/ops-template-install`)
2. Creates any missing framework directories in the current repo:
   - `context/`, `memory/`, `projects/`, `decisions/`, `audits/`, `references/`, `scheduled-tasks/`, `docs/`, `_inbox/`, `_archive/`
3. Copies template files only where nothing already exists:
   - `CLAUDE.md`, `MAP.md`, `GUARDRAILS.md`, `EXPANSIONS.md`
   - `.claude/skills/onboard/SKILL.md`
   - `.claude/skills/new-from-template/SKILL.md`
   - `scripts/merge-settings.py`, `scripts/setup.sh`
   - `hooks/` directory (all hook files)
   - Stub files: `connections.md`, `endpoints.md`, `context/me.md`, `context/goals.md`, `context/work.md`, `memory/MEMORY.md`
4. Scans every pre-existing file in the repo (excluding `.git/`, `node_modules/`, binary files) and writes `_inbox/INGEST_MANIFEST.md` — a flat list of paths and file sizes for everything that was already there before the install
5. Wires up Claude Code:
   - Copies hooks to `~/.claude/hooks/` — skips any file that already exists and prints a warning (no interactive prompts; `curl | bash` runs non-interactively)
   - Runs `merge-settings.py` to update `~/.claude/settings.json`
6. Cleans up temp dir
7. Prints: "Done — open Claude Code in this directory and run `/onboard` to organize your repo"

### What it does NOT do

- Move, rename, or delete any existing client files
- Read or analyze file content
- Make any routing decisions

### Idempotency

Safe to re-run. Template files only copy if the destination doesn't exist. Manifest regenerates from current state.

---

## Stage 2: `/onboard` skill — ingest mode

Triggered when `/onboard` runs and detects `_inbox/INGEST_MANIFEST.md`. Enters ingest mode instead of the normal fresh-start flow.

### Phase 1 — Read everything

Reads every file listed in the manifest in full. No routing decisions yet. Goal: build a complete picture of what exists, what topics are covered, and what the repo was originally for.

### Phase 2 — Cluster by content

Groups files by topic/theme overlap. Examples:
- "3 files contain overlapping project context"
- "2 files are both integration/tool lists"
- "4 files all contain goal or target information"

Identifies what's unique vs what's duplicated across files within each cluster.

### Phase 3 — Map clusters to framework locations

For each content cluster, determines the correct framework destination:

| Content type | Framework location |
|---|---|
| Who the person is, voice, communication style | `context/me.md` |
| Career goals, targets, aspirations | `context/goals.md` |
| Employment status, availability | `context/work.md` |
| Tool integrations, API connections | `connections.md` |
| Endpoint IDs, database IDs, URLs | `endpoints.md` |
| Active project work | `projects/<name>/CLAUDE.md` |
| Terminology, people, glossary | `memory/` |
| Architectural decisions | `decisions/log.md` |
| Scheduled or recurring tasks | `scheduled-tasks/` |

For ambiguous clusters, asks the user one question at a time to resolve before proceeding.

### Phase 4 — Synthesize (not move)

Files are not moved — their content is **read, deduplicated, and written into the correct framework file.**

- Multiple files mapping to the same destination → content is merged, duplicates removed, unique context preserved
- Contradictions between files → flagged for user to resolve before writing
- Before executing any writes, presents a confirmation summary: "From X source files I've synthesized these Y framework files — [list]. Does this look right?"
- User approves before any files are written

### Phase 5 — Archive originals, fill CLAUDE.md

After user confirms synthesis:

1. Moves all original source files to `_archive/` organized by their original path structure (nothing deleted — always recoverable)
2. Fills CLAUDE.md placeholders using context learned during ingest (name, email, timezone, tools, focus areas)
3. Deletes `_inbox/INGEST_MANIFEST.md`

---

## End State

After both stages complete:

- Framework directory structure is in place
- Client's existing content is consolidated, deduplicated, and filed into the correct framework locations
- CLAUDE.md is filled out
- Claude Code hooks and settings are wired up
- Original source files preserved in `_archive/` as a safety net
- Repo is ready for normal ops use

---

## What This Is Not

- This does not delete anything (originals always go to `_archive/`, never deleted)
- This does not touch `.git/`, `node_modules/`, or binary files
- The bash script does not make any content decisions — that is exclusively Claude Code's job
- This is not a one-size-fits-all file mover — it reads content and synthesizes intelligently

---

## Files to Create or Modify

| File | Action |
|---|---|
| `scripts/install.sh` | Create new — the curl-installable bootstrap script |
| `.claude/skills/onboard/SKILL.md` | Modify — add ingest mode detection and 5-phase flow |
| `scripts/setup.sh` | No change — still used for local hook wiring after fresh clone |

---

## Agents

- **`debugger`** — for diagnosing install failures (path issues, settings merge conflicts, hook copy errors)
- **`code-reviewer`** — review `install.sh` before shipping (safe file operations, idempotency, no destructive actions)
