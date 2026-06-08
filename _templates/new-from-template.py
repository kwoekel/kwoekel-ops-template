#!/usr/bin/env python3
"""
Create a new project file from a template in _templates/.

Usage:
  python3 _templates/new-from-template.py <framework|roadmap> <output_path> "KEY=value" ["KEY2=value2" ...]

Example:
  python3 _templates/new-from-template.py framework \\
    projects/ai-monetization/acme/framework.md \\
    "PROJECT_NAME=Acme Lead Gen" "EXECUTION_LEAD=Jane Doe"

- Replaces every [KEY] placeholder with its provided value.
- Unfilled [KEY] placeholders are left as-is (nothing is silently wrong) and reported.
- Adds a PROJECT INSTANCE comment linking back to the source template.
- Parent directories are created automatically.
"""

import re
import sys
from pathlib import Path

REPO_DIR = Path(__file__).parent.parent.resolve()

# Opt-in domain blueprints. The DEFAULT project shape is the generic skeleton in
# _templates/project-skeleton/ — scaffold it with `python3 scripts/ingest.py scaffold <name>`.
# These single-file templates are only for projects that genuinely match the domain.
TEMPLATES = {
    "framework": REPO_DIR / "_templates" / "_examples" / "lead-gen-framework-template.md",
    "roadmap":   REPO_DIR / "_templates" / "_examples" / "four-phase-roadmap-template.md",
}


def parse_kv(args: list[str]) -> dict:
    replacements = {}
    for arg in args:
        if "=" not in arg:
            print(f"Error: argument is not KEY=value: {arg!r}")
            sys.exit(1)
        key, value = arg.split("=", 1)
        replacements[key.strip()] = value
    return replacements


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    template_type = sys.argv[1]
    output_path = sys.argv[2]
    replacements = parse_kv(sys.argv[3:])

    if template_type not in TEMPLATES:
        print(f"Error: unknown template type {template_type!r}. Choose: {', '.join(TEMPLATES)}")
        sys.exit(1)

    src = TEMPLATES[template_type]
    if not src.exists():
        print(f"Error: template file not found: {src}")
        sys.exit(1)

    text = src.read_text(encoding="utf-8")

    # Replace [KEY] placeholders
    for key, value in replacements.items():
        text = text.replace(f"[{key}]", value)

    # Prepend a PROJECT INSTANCE marker linking back to the source template
    rel_src = src.relative_to(REPO_DIR)
    marker = f"<!-- PROJECT INSTANCE — generated from {rel_src} -->\n"
    text = marker + text

    # Report any remaining unfilled placeholders
    remaining = sorted(set(re.findall(r"\[[A-Z_0-9]+\]", text)))

    out = Path(output_path)
    if not out.is_absolute():
        out = REPO_DIR / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")

    print(f"✅ Created {out}")
    if remaining:
        print(f"⚠️  {len(remaining)} placeholder(s) still need manual attention:")
        for key in remaining:
            print(f"     {key}")


if __name__ == "__main__":
    main()
