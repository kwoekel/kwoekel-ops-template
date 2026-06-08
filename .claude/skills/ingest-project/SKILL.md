---
name: ingest-project
description: Ingest an existing, chaotic repo into this template's generic project framework. Reads every part of a source repo, organizes it into a lean standard project folder, proposes dedupes and prunes for your approval, and proves nothing was lost via an accounting ledger. Use when someone wants to bring a scattered or duplicated repo under projects/.
disable-model-invocation: true
---

# Ingest Project

Takes a messy, real-world repo and turns it into a clean project under `projects/<name>/`,
following the generic project framework. The promise: **every part of the source gets
ingested somewhere** — placed, merged, pruned (with a reason), or parked in `_inbox/` —
and the engine proves it.

This skill writes files and runs a script. It is manual (`disable-model-invocation`):
it only runs when the user types `/ingest-project`.

## The split

- **`scripts/ingest.py` does the accounting** (deterministic, reliable): scaffold the
  destination, preserve a raw copy of the source, build the ledger, and run the final
  coverage check. Never hand these steps to judgment.
- **You (Claude) do the judgment**: read the content, decide where each piece belongs,
  spot duplicates, propose what to prune. Never delete or merge without approval.

## The flow

### Step 1 — Get the source

Ask for the project name and the source. The source is either:
- a **local path** (read with Read/Glob), or
- a **GitHub URL** (clone it locally first so the script can archive it:
  `git clone <url> /tmp/<name>-src`; if private/unreachable, say so and stop).

### Step 2 — Scaffold + inventory (script)

From the repo root:

```bash
python3 scripts/ingest.py scaffold <name>
python3 scripts/ingest.py inventory <name> <source_path>
```

This creates `projects/<name>/` from the generic skeleton, copies the raw source into
`projects/<name>/_archive/source/` (the safety net — never loaded in normal sessions),
and writes `_archive/INGEST-LEDGER.md` with one row per source file, all `pending`.

### Step 3 — Map every item

Read the source content. For each ledger row, decide its destination slot:

| Source content looks like… | Goes to |
|---|---|
| What the project is, who it's for, current state | `context/overview.md` |
| Stakeholders, clients, contacts | `context/people.md` |
| Why a choice was made / past decisions | `context/decisions.md` |
| Milestones, status, TODOs, phases | `planning/roadmap.md` |
| The one-paragraph "how to work here" / entry orientation | `CLAUDE.md` |
| Can't tell yet | `_inbox/` (park it — temporary) |

Large files often split across several slots — break them into sections and account for
each section in the ledger (add sub-rows like `004a`, `004b` if needed). Nothing is too
small to account for.

### Step 4 — Dedupe + prune (propose, then apply)

As you map, flag:
- **Duplicates / overlap** — "rows 002 and 007 say the same thing → merge into
  `context/overview.md`, drop the rest."
- **Stale / dead content** — "this references a 2023 tool you no longer use → prune."

Present these as a single review batch and **wait for approval**. The raw source is safe
in `_archive/source/`, so approved prunes lose nothing recoverable. Only after the user
signs off, write the organized files and record each verdict in the ledger:

- `placed` → the slot path
- `merged` → which row/slot it folded into
- `pruned` → a one-line reason (required)
- `inbox` → still parked (must reach zero before done)

### Step 5 — Fill the framework

Write real content into the project's slots — `CLAUDE.md` purpose/status, `overview.md`,
`people.md`, `decisions.md`, `roadmap.md`. Replace every `[PLACEHOLDER]`. Delete skeleton
slot files that genuinely don't apply (e.g. `people.md` for a solo project), and record
that in the ledger so the coverage check stays honest.

### Step 6 — Triage the inbox to zero

Go through everything in `_inbox/`. Each item gets a real slot or a prune. The inbox must
end **empty** (only its `README.md` may remain).

### Step 7 — Verify (script)

```bash
python3 scripts/ingest.py verify <name>
```

Ingestion is **done** only when this exits clean: every ledger row has a terminal verdict
(`placed` / `merged` / `pruned`), every prune has a reason, and `_inbox/` is clear. If it
reports gaps, fix them and re-run until it shows `COMPLETE ✅`. Never call the ingest done
while verify is red.

### Step 8 — Wire it in + commit

1. Add the project to the root `MAP.md` Task Routing table and Projects map.
2. Show the user the coverage report and the new project structure.
3. Commit with the `project:` prefix:

```
project: ingest <name> into the project framework

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
```

## Notes

- **Never read `_archive/` in a normal session.** It exists to prove completeness and to
  recover mistaken prunes — it is not project context. It's marked never-read in `MAP.md`.
- If the project matches a domain blueprint in `_templates/_examples/` (e.g. it really is
  a lead-gen consultancy), you can pull that template's structure into `planning/` on top
  of the generic skeleton — but the generic skeleton is always the base.
- Re-running `inventory` on a project that already has `_archive/source/` is blocked on
  purpose. To start over, delete `projects/<name>/` first.
