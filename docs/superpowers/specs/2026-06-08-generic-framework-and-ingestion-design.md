# Generic Project Framework + Ingestion Engine — Design

**Date:** 2026-06-08
**Status:** Approved, building

## Problem

Two gaps in the template today:

1. The `_templates/` frameworks (lead-gen framework, four-phase roadmap) are deeply
   lead-gen/consulting-specific. They don't generalize to other project types, so the
   "framework" a new project gets is unusable for most work.
2. There is no flow that ingests an existing, chaotic repo into the project framework.
   `/onboard`'s import mode only mines a source repo for the *owner's identity*; it
   discards the actual project content. `new-from-template` only scaffolds greenfield
   projects. Nothing organizes scattered content, dedupes it, or proves nothing was lost.

## Goal

- A **generic, best-practice project framework** (the destination shape) that fits any
  project, with a client/business-ops center of gravity.
- An **ingestion engine** that reads a chaotic repo, maps every part into that framework,
  proposes dedupes and prunes (with approval), and proves completeness — without bloating
  context.

## Decisions

- **Project type focus:** Mostly client/business ops (not code-heavy).
- **Per-project shape:** Lean standard folder (small fixed set of slots), not a single
  file and not a full mirror of the root template.
- **Prune safety:** Propose, user approves. Originals preserved until sign-off.
- **Completeness proof:** Full accounting ledger, stored in an archive zone that is never
  loaded into context (same treatment as graphify's `GRAPH_REPORT.md`).

## Part A — Generic project framework (destination)

Each project under `projects/<name>/` uses this lean standard folder:

```
projects/<name>/
├── CLAUDE.md          ← entry: purpose, status, how to work here, what NOT to do, key files
├── context/
│   ├── overview.md    ← what it is, who it's for, current state
│   ├── people.md      ← stakeholders / clients / contacts (optional)
│   └── decisions.md   ← project-level decision log (append-only)
├── planning/
│   └── roadmap.md     ← generic milestones/status (any number of phases)
├── _inbox/            ← unsorted ingested content awaiting triage → must reach empty
└── _archive/          ← NEVER loaded into context
    ├── INGEST-LEDGER.md   ← full accounting manifest
    └── source/            ← preserved raw original (the safety net)
```

Lives as a skeleton in `_templates/project-skeleton/`. Generic is the default.

The existing lead-gen framework + four-phase roadmap move to `_templates/_examples/`
as **opt-in domain blueprints** — not deleted, just no longer the default.

## Part B — Ingestion engine (`/ingest-project` skill)

Point it at a local path or GitHub URL. Steps:

1. **Inventory** — `scripts/ingest.py` walks the source, builds a manifest of every
   file/section. This is the ledger seed and the "nothing falls through" baseline.
2. **Map** — Claude classifies each piece into a framework slot, or marks it unsorted
   → `_inbox/`.
3. **Dedupe + prune (propose only)** — Claude finds overlapping/duplicated and stale
   content, presents a review batch. Nothing merges or prunes until the user approves.
4. **Place** — write the lean organized files; copy raw source into `_archive/source/`;
   write `INGEST-LEDGER.md` recording every item's verdict.
5. **Verify** — ingestion is "done" only when **every ledger item has a verdict AND
   `_inbox/` is empty**. Produces a one-screen coverage report.

### Completeness without context bloat

`INGEST-LEDGER.md` records, per source item: `placed → slot` / `merged → target` /
`pruned → reason` / `inbox`. It lives in `_archive/`, marked "never read directly" in
`MAP.md` like the graphify report. Raw source sits beside it as recoverable source of
truth. Neither loads in a normal session.

### Script vs. Claude split

- **`scripts/ingest.py` (deterministic):** walk source, build manifest, copy to archive,
  run final coverage check (every manifest item has a verdict; `_inbox/` empty).
- **Claude (judgment):** map content to slots, propose merges, justify prunes.

## Files touched

- New `_templates/project-skeleton/` — generic shape.
- Move `_templates/frameworks/` + `_templates/planning/` → `_templates/_examples/`.
- New `.claude/skills/ingest-project/SKILL.md`.
- New `scripts/ingest.py`.
- Update `MAP.md` — new project shape + archive-zone never-read rule.
- Update `.claude/skills/new-from-template/SKILL.md` + `_templates/new-from-template.py`
  — default to generic skeleton; domain templates become opt-in.
- Register `ingest-project` in `~/.claude/registry.json`; run `skills/sync.py --write`.
- Log decision in `decisions/log.md`.

## Out of scope

- Changing `/onboard` (it stays identity-only; `/ingest-project` is the content path).
- Automatic pruning without approval.
- Code-repo-specific conventions (architecture maps, dependency graphs).
