# Decisions Log

Append-only record of automation decisions, strategic choices, and scope calls.
Written to by `/level-up` after each session. Also used by `/audit` to score Cadence.

Format per entry:
```
## YYYY-MM-DD — [Decision title]
**Candidate:** what was surfaced
**EAD outcome:** Eliminate / Automate / Delegate
**Autonomy level:** L0–L4
**KPI bucket:** More customers / More value per customer / Less cost
**Metric:** specific number being moved
**Artifact:** what was built or linked
**Notes:** anything worth remembering
```

---

## [YYYY-MM-DD] — Initialized decisions log

**Notes:** Log created from kwoekel-ops-template. Begin recording decisions here.

---

## 2026-06-08 — Generic project framework + ingestion engine

**Candidate:** The `_templates/` frameworks were lead-gen-specific and unusable for most
projects, and nothing ingested existing chaotic repos into `projects/` — `/onboard` only
mines source repos for owner identity, `new-from-template` only scaffolds greenfield.
**EAD outcome:** Automate (the organize/dedupe/prune flow) + Eliminate (lead-gen as default).
**Autonomy level:** L2 — engine proposes dedupes/prunes; user approves before anything merges or prunes.
**KPI bucket:** Less cost (time to organize a messy repo; context kept lean).
**Metric:** Source items accounted-for = 100% (verify gate), `_inbox/` triaged to zero.
**Artifact:**
- `_templates/project-skeleton/` — new generic, best-practice default project shape.
- Lead-gen framework + four-phase roadmap moved to `_templates/_examples/` (opt-in).
- `/ingest-project` skill + `scripts/ingest.py` (scaffold / inventory / verify).
- `INGEST-LEDGER.md` accounting in each project's `_archive/`, marked never-read in MAP.
- `new-from-template` re-pointed to the generic skeleton as default.
**Notes:** Completeness is proven by a per-source-item ledger living in an archive zone
that never loads into context — full accountability with zero per-session cost. Raw source
preserved in `_archive/source/` so approved prunes are always recoverable. Spec:
`docs/superpowers/specs/2026-06-08-generic-framework-and-ingestion-design.md`.
