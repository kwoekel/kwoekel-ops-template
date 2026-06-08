# Skill: new-from-template

Use this skill when the user wants to start a new project from a shared template — specifically the lead gen framework or the four-phase roadmap in `_templates/`.

## What this does

Copies a template from `_templates/`, fills in all `[PLACEHOLDER]` values with real project-specific information, adds a PROJECT INSTANCE comment linking back to the source template, and writes the result to the right location.

## Steps

### 1. Identify which template(s) to use
Ask (or infer from context):
- `framework` — the two-layer lead gen framework (`_templates/frameworks/lead-gen-framework-template.md`)
- `roadmap` — the four-phase execution roadmap (`_templates/planning/four-phase-roadmap-template.md`)
- Or both (common — most projects use both together)

### 2. Identify the output path
Where should the file live? Default conventions:
- Framework → `projects/<track>/<project-name>/framework.md`
- Roadmap → `projects/<track>/<project-name>/.planning/ROADMAP.md`

Ask the user if not clear from context.

### 3. Collect placeholder values
Ask the user for the values below. Many can be inferred from context — only ask for what you can't confidently fill in yourself.

**Core (always needed):**
- `PROJECT_NAME` — the project or operation name
- `EXECUTION_LEAD` — person responsible for execution
- `STRATEGY_PARTNER` — person responsible for strategy/positioning
- `PRIMARY_CHANNEL` — main marketing channel (e.g. LinkedIn, Instagram)
- `ICP` — ideal client profile description
- `CORE_VALUE_PROP` — one-sentence brand promise

**Service tiers (framework only):**
- `TIER_1_NAME / PRICE` — entry tier name and price
- `TIER_2_NAME / PRICE` — mid tier name and price
- `TIER_3_NAME / PRICE` — full tier name and price
- `ADDON_NAME / PRICE` — add-on module name and price

**Tools (roadmap only):**
- `AUTOMATION_TOOL` — workflow automation platform (e.g. n8n, Make, Zapier)
- `CONTENT_MGMT_TOOL` — content approval/tracking tool (e.g. Airtable, Notion)
- `PUBLISHING_TOOL` — scheduling/publishing tool (e.g. Buffer, Publer)
- `SECRETS_TOOL` — credentials management (e.g. Infisical, 1Password)
- `ADDON_NAME` — add-on module name (roadmap uses this without price)

**Optional:**
- `FRAMEWORK_SOURCE` — source methodology (e.g. "Melissa Henault Lead Gen Method")
- `OPTIMAL_DAYS` — best posting days (default: Tuesday–Thursday)
- `OPTIMAL_TIMES` — best posting times (default: 8–10am or 12–1pm)
- `PROFILE_SPRINT_PRICE` — profile setup one-time price (e.g. $300–500)

### 4. Run the script
Call the Python script with all collected values:

Run from the repo root (the script resolves paths relative to itself):

```bash
python3 _templates/new-from-template.py \
  <framework|roadmap> \
  <output_path> \
  "PROJECT_NAME=<value>" \
  "EXECUTION_LEAD=<value>" \
  ...
```

Run once per template type needed.

### 5. Report results
Tell the user:
- What files were created
- Any unfilled placeholders that need manual attention (the script prints these)

## Notes
- If a target file already exists, treat it as an existing instance — confirm with the user before overwriting it
- Parent directories are created automatically by the script
- Unfilled placeholders stay as `[KEY]` in the output so nothing is silently wrong
