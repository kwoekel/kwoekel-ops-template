#!/usr/bin/env python3
"""
Ingestion engine — deterministic half of the /ingest-project skill.

Handles the mechanical, must-be-reliable parts of pulling a chaotic existing repo
into the generic project framework. Claude does the judgment (mapping, dedupe,
pruning); this script does the accounting so nothing falls through.

Subcommands:
  scaffold  <project_name>
      Copy _templates/project-skeleton/ into projects/<project_name>/.

  inventory <project_name> <source_path>
      Copy the raw source into projects/<name>/_archive/source/ (the safety net),
      then build _archive/INGEST-LEDGER.md with one row per source file, each marked
      verdict=pending. This is the "nothing falls through" baseline.

  verify    <project_name>
      Coverage check. Ingestion is "done" only when every ledger row has a real
      verdict (not pending, not inbox) AND _inbox/ holds no un-triaged content.
      Prints a one-screen report. Exits non-zero if incomplete.

Run from anywhere — paths resolve relative to this script.
"""

import os
import re
import shutil
import sys
from pathlib import Path

REPO_DIR = Path(__file__).parent.parent.resolve()
SKELETON = REPO_DIR / "_templates" / "project-skeleton"
PROJECTS = REPO_DIR / "projects"

# Directories never worth copying into the archive (history / build noise, not content).
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__",
             "dist", "build", ".next", ".cache", ".pytest_cache", ".mypy_cache"}

LEDGER_NAME = "INGEST-LEDGER.md"
VERDICTS_DONE = {"placed", "merged", "pruned"}   # terminal, counts as accounted-for
VERDICTS_OPEN = {"pending", "inbox"}             # still needs a human/Claude decision


def project_dir(name: str) -> Path:
    return PROJECTS / name


def die(msg: str) -> None:
    print(f"error: {msg}")
    sys.exit(1)


# ── scaffold ────────────────────────────────────────────────────────────────
def scaffold(name: str) -> None:
    dest = project_dir(name)
    if dest.exists():
        die(f"projects/{name}/ already exists — refusing to overwrite. "
            f"Delete it first or pick another name.")
    if not SKELETON.exists():
        die(f"skeleton not found at {SKELETON}")
    shutil.copytree(SKELETON, dest)
    print(f"scaffolded projects/{name}/ from the generic skeleton")
    for p in sorted(dest.rglob("*")):
        if p.is_file():
            print(f"  {p.relative_to(REPO_DIR)}")


# ── inventory ───────────────────────────────────────────────────────────────
def _iter_source_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in sorted(filenames):
            yield Path(dirpath) / fn


def inventory(name: str, source: str) -> None:
    dest = project_dir(name)
    if not dest.exists():
        die(f"projects/{name}/ does not exist — run `scaffold {name}` first.")
    src_root = Path(source).expanduser().resolve()
    if not src_root.exists():
        die(f"source path not found: {src_root}")

    archive = dest / "_archive"
    archive_source = archive / "source"
    archive.mkdir(exist_ok=True)

    # 1. Preserve the raw source (the recoverable safety net).
    if archive_source.exists():
        die(f"{archive_source.relative_to(REPO_DIR)} already exists — "
            f"inventory already ran. Delete it to re-run.")
    if src_root.is_dir():
        shutil.copytree(
            src_root, archive_source,
            ignore=shutil.ignore_patterns(*SKIP_DIRS),
        )
        files = list(_iter_source_files(src_root))
    else:
        archive_source.mkdir()
        shutil.copy2(src_root, archive_source / src_root.name)
        files = [src_root]

    # 2. Build the ledger seed — one row per source file, verdict=pending.
    rows = []
    for i, f in enumerate(sorted(files), 1):
        try:
            rel = f.relative_to(src_root)
        except ValueError:
            rel = f.name
        size = f.stat().st_size if f.exists() else 0
        rows.append((f"{i:03d}", str(rel), f"{size:,}"))

    ledger = archive / LEDGER_NAME
    lines = [
        f"# Ingest Ledger — {name}",
        "",
        f"> Source: `{src_root}`",
        f"> Raw copy preserved in `_archive/source/`. **Never loaded into context.**",
        "",
        "Every source file is one row. Ingestion is **done** only when no row is",
        "`pending` or `inbox`. Update the Verdict + Destination columns as you map,",
        "merge, and prune. Then run `python3 scripts/ingest.py verify "
        f"{name}` to confirm.",
        "",
        "Verdicts: `pending` (untouched) · `placed` (→ a slot) · `merged` (→ combined "
        "with another) · `pruned` (dropped, give a reason) · `inbox` (parked, must be "
        "triaged to zero).",
        "",
        "| ID | Source file | Size (B) | Verdict | Destination / reason |",
        "|----|-------------|----------|---------|----------------------|",
    ]
    for rid, rel, size in rows:
        lines.append(f"| {rid} | `{rel}` | {size} | pending | |")
    lines.append("")
    ledger.write_text("\n".join(lines))

    print(f"inventoried {len(rows)} source file(s) into "
          f"{ledger.relative_to(REPO_DIR)}")
    print(f"raw source preserved in {archive_source.relative_to(REPO_DIR)}")
    print(f"\nnext: map each row to a slot, then run "
          f"`python3 scripts/ingest.py verify {name}`")


# ── verify ──────────────────────────────────────────────────────────────────
_ROW_RE = re.compile(r"^\|\s*([A-Za-z0-9]+)\s*\|.*?\|.*?\|\s*([a-zA-Z]+)\s*\|(.*)\|\s*$")


def _parse_ledger(ledger: Path):
    rows = []
    for line in ledger.read_text().splitlines():
        m = _ROW_RE.match(line)
        if m:
            rows.append({"id": m.group(1),
                         "verdict": m.group(2).strip().lower(),
                         "dest": m.group(3).strip()})
    return rows


def _inbox_untriaged(dest: Path):
    inbox = dest / "_inbox"
    if not inbox.exists():
        return []
    keep = {"readme.md", ".gitkeep"}
    return [p for p in inbox.rglob("*")
            if p.is_file() and p.name.lower() not in keep]


def verify(name: str) -> None:
    dest = project_dir(name)
    ledger = dest / "_archive" / LEDGER_NAME
    if not ledger.exists():
        die(f"no ledger at {ledger.relative_to(REPO_DIR)} — run inventory first.")

    rows = _parse_ledger(ledger)
    if not rows:
        die("ledger has no parseable rows — check the table format wasn't broken.")

    counts = {}
    for r in rows:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    open_rows = [r for r in rows if r["verdict"] in VERDICTS_OPEN
                 or r["verdict"] not in (VERDICTS_DONE | VERDICTS_OPEN)]
    pruned_no_reason = [r for r in rows if r["verdict"] == "pruned" and not r["dest"]]
    untriaged = _inbox_untriaged(dest)

    total = len(rows)
    accounted = total - len(open_rows)
    print(f"Ingest coverage — {name}")
    print(f"  source items:   {total}")
    print(f"  accounted for:  {accounted}/{total}")
    for v in sorted(counts):
        print(f"    {v:<8} {counts[v]}")
    print(f"  _inbox/ untriaged files: {len(untriaged)}")

    problems = []
    if open_rows:
        problems.append(f"{len(open_rows)} row(s) still pending/inbox "
                        f"(IDs: {', '.join(r['id'] for r in open_rows[:10])}"
                        f"{'…' if len(open_rows) > 10 else ''})")
    if pruned_no_reason:
        problems.append(f"{len(pruned_no_reason)} pruned row(s) missing a reason "
                        f"(IDs: {', '.join(r['id'] for r in pruned_no_reason[:10])})")
    if untriaged:
        problems.append(f"{len(untriaged)} file(s) still in _inbox/ "
                        f"({', '.join(p.name for p in untriaged[:5])}"
                        f"{'…' if len(untriaged) > 5 else ''})")

    if problems:
        print("\n  INCOMPLETE — nothing has fallen through, but these need a verdict:")
        for p in problems:
            print(f"    - {p}")
        sys.exit(1)

    print("\n  COMPLETE ✅  every source item has a terminal verdict and _inbox/ is clear.")


# ── entry ───────────────────────────────────────────────────────────────────
def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    args = sys.argv[2:]
    if cmd == "scaffold" and len(args) == 1:
        scaffold(args[0])
    elif cmd == "inventory" and len(args) == 2:
        inventory(args[0], args[1])
    elif cmd == "verify" and len(args) == 1:
        verify(args[0])
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
