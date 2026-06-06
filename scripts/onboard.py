#!/usr/bin/env python3
"""
Onboarding wizard for kwoekel-ops-template.

Usage:
  python3 scripts/onboard.py --fresh
      Interactive wizard — prompts for all [PLACEHOLDER] values.

  python3 scripts/onboard.py --import /path/to/existing-repo
      Claude analyzes the repo and pre-fills what it can. Wizard handles the rest.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_DIR = Path(__file__).parent.parent.resolve()

PLACEHOLDER_QUESTIONS = [
    ("[YOUR_NAME]",        "Your full name"),
    ("[YOUR_EMAIL]",       "Your email address"),
    ("[YOUR_USERNAME]",    "Your GitHub username"),
    ("[TIMEZONE]",         "Your timezone (e.g. PST, EST, CET)"),
    ("[YOUR_FOCUS_AREAS]", "Your 2-3 focus areas, comma-separated (e.g. Job search, AI consulting)"),
    ("[Focus area 1]",     "Focus area 1 (short label)"),
    ("[Focus area 2]",     "Focus area 2 (short label)"),
    ("[Focus area 3]",     "Focus area 3 (short label — or press Enter to skip)"),
    ("[YOUR_SERVICE_PAGE]","Name of your main services page (or press Enter to skip)"),
]

TARGET_FILES = [
    "CLAUDE.md", "MAP.md", "README.md",
    "context/me.md", "context/goals.md", "context/work.md",
    "memory/MEMORY.md", "memory/overview.md", "memory/glossary.md",
    "connections.md", "endpoints.md", "decisions/log.md",
    "agents/ceo/AGENT.md", "agents/cto/AGENT.md",
    ".gitmodules",
]


def fill_placeholders(replacements: dict):
    """Apply a replacements dict to all target files."""
    for rel in TARGET_FILES:
        path = REPO_DIR / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        changed = False
        for placeholder, value in replacements.items():
            if value and placeholder in text:
                text = text.replace(placeholder, value)
                changed = True
        if changed:
            path.write_text(text, encoding="utf-8")
            print(f"  ✅ Updated {rel}")


def run_fresh_wizard():
    print("\n── Fresh Start Onboarding ─────────────────────────────────────")
    print("Fill in your details. Press Enter to skip optional fields.\n")

    replacements = {}
    for placeholder, prompt in PLACEHOLDER_QUESTIONS:
        value = input(f"{prompt}: ").strip()
        if value:
            replacements[placeholder] = value

    if replacements:
        fill_placeholders(replacements)
        print("\n✅ Done! Open CLAUDE.md to review and fill in any remaining [PLACEHOLDER] blocks.")
    else:
        print("\nNothing entered — no changes made.")


def run_import_wizard(repo_path: str):
    src = Path(repo_path).resolve()
    if not src.exists():
        print(f"Error: path not found: {src}")
        sys.exit(1)

    print(f"\n── Import Mode: analyzing {src.name} ───────────────────────────")
    print("Gathering repo context...")

    # Collect repo context (capped at ~50K chars to stay within context budget)
    context_parts = []
    for fname in ["README.md", "package.json", "pyproject.toml", "CLAUDE.md",
                  "setup.py", "Makefile", "docker-compose.yml", ".env.example"]:
        f = src / fname
        if f.exists():
            content = f.read_text(encoding="utf-8", errors="replace")[:3000]
            context_parts.append(f"=== {fname} ===\n{content}")

    # Folder structure
    try:
        tree = subprocess.run(
            ["find", str(src), "-maxdepth", "3", "-not", "-path", "*/.git/*",
             "-not", "-path", "*/node_modules/*", "-not", "-path", "*/__pycache__/*"],
            capture_output=True, text=True
        ).stdout[:3000]
        context_parts.append(f"=== Folder structure ===\n{tree}")
    except Exception:
        pass

    repo_context = "\n\n".join(context_parts)

    # Load template files to populate
    templates = {}
    for rel in ["CLAUDE.md", "context/me.md", "connections.md", "agents/ceo/AGENT.md"]:
        p = REPO_DIR / rel
        if p.exists():
            templates[rel] = p.read_text(encoding="utf-8")

    template_str = "\n\n".join(f"--- {k} ---\n{v}" for k, v in templates.items())

    prompt = f"""I'm setting up a personal ops repo for a new project. I have:

1. Context from the existing repo I'm importing:
{repo_context}

2. Template files that need their [PLACEHOLDER] blocks filled in:
{template_str}

Please fill in every [PLACEHOLDER] you can confidently infer from the repo context.
For anything you can't determine, leave the [PLACEHOLDER] as-is.
Return ONLY the filled-in template files, each separated by "--- filename ---" headers,
in the same order as the input. No explanation needed.
"""

    print("Asking Claude to analyze the repo and fill in placeholders...")
    try:
        result = subprocess.run(
            ["claude", "--print", prompt],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0 and result.stdout.strip():
            # Parse Claude's response and write back to files
            output = result.stdout
            for rel in templates:
                pattern = rf"---\s*{re.escape(rel)}\s*---\n(.*?)(?=---\s*\w|$)"
                match = re.search(pattern, output, re.DOTALL)
                if match:
                    content = match.group(1).strip()
                    (REPO_DIR / rel).write_text(content + "\n", encoding="utf-8")
                    print(f"  ✅ Pre-filled: {rel}")
        else:
            print("  ⚠️  Claude didn't return usable output — proceeding to manual wizard")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("  ⚠️  Could not run Claude CLI — proceeding to manual wizard")

    print("\nFinishing with interactive wizard for remaining placeholders...")
    run_fresh_wizard()


def main():
    parser = argparse.ArgumentParser(description="Onboarding wizard for kwoekel-ops-template")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--fresh", action="store_true", help="Interactive fresh-start wizard")
    group.add_argument("--import", dest="import_repo", metavar="PATH",
                       help="Import and analyze an existing repo, then run wizard")
    args = parser.parse_args()

    if args.fresh:
        run_fresh_wizard()
    elif args.import_repo:
        run_import_wizard(args.import_repo)


if __name__ == "__main__":
    main()
