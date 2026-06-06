#!/usr/bin/env python3
"""
Sync ~/.claude/registry.json skill entries to skills/README.md.
Usage: python3 skills/sync.py --write   (updates the README)
       python3 skills/sync.py           (dry-run, prints diff)
"""
import argparse
import json
from pathlib import Path

REGISTRY = Path.home() / ".claude" / "registry.json"
README = Path(__file__).parent / "README.md"
TABLE_MARKER = "| Skill Name |"


def load_skills() -> list[dict]:
    if not REGISTRY.exists():
        return []
    try:
        data = json.loads(REGISTRY.read_text())
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            return data.get("skills", [])
    except (json.JSONDecodeError, KeyError):
        pass
    return []


def build_table(skills: list[dict]) -> str:
    rows = ["| Skill Name | Category | When to use |",
            "|---|---|---|"]
    for s in sorted(skills, key=lambda x: x.get("name", "")):
        name = s.get("name", "")
        category = s.get("category", "—")
        description = s.get("description", s.get("when_to_use", ""))[:80]
        rows.append(f"| `{name}` | {category} | {description} |")
    return "\n".join(rows)


def update_readme(skills: list[dict], write: bool) -> None:
    if not README.exists():
        print("README.md not found — nothing to update")
        return

    content = README.read_text()
    new_table = build_table(skills)

    # Replace from TABLE_MARKER to end of file (or next --- separator)
    if TABLE_MARKER not in content:
        print("Table marker not found in README — nothing to update")
        return
    idx = content.index(TABLE_MARKER)
    after = content[idx:]
    sep = after.find("\n---\n")
    updated = content[:idx] + new_table + ("\n" + after[sep:] if sep != -1 else "\n")

    if write:
        README.write_text(updated)
        print(f"Updated skills/README.md ({len(skills)} skills)")
    else:
        print(f"Dry run: {len(skills)} skills would be written. Pass --write to apply.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    skills = load_skills()
    if not skills:
        print("No skills found in ~/.claude/registry.json")
        return

    update_readme(skills, args.write)


if __name__ == "__main__":
    main()
