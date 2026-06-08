# _archive — NEVER loaded into context

This folder is the project's safety net and accounting record. It is **never read in a
normal session** — treat it like `_tools/graphify/GRAPH_REPORT.md`. Loading it would
bloat context for no reason.

## Contents

```
_archive/
├── INGEST-LEDGER.md   ← full accounting: every source item and its verdict
└── source/            ← preserved raw copy of the original ingested repo
```

## When to touch it

- **To prove nothing was lost:** open `INGEST-LEDGER.md` and check every item has a
  verdict (`placed` / `merged` / `pruned` / `inbox`).
- **To recover something that was pruned by mistake:** pull it from `source/`.

Otherwise, leave it alone. The organized, deduped, pruned content lives in the project's
real slots — that's what sessions load.

This README is a placeholder so the folder exists in git. The ingest engine fills the
rest. If this project was not ingested from an existing repo, this folder can be deleted.
