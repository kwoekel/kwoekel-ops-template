---
status: issues_found
review_type: template-readiness
scope: executable surface (setup.sh, scripts/, hooks/, skills/)
files_reviewed: 9
findings:
  critical: 1
  warning: 3
  info: 5
  total: 9
reviewed_by: gsd-code-review (adapted — no .planning phase present)
date: 2026-06-07
---

# Code Review — Ops Template Readiness

**Question asked:** find bugs that surface when customers use this as a template.

The GSD phase workflow didn't apply (no `.planning/`, single `init` commit), so this is a direct review of the **executable surface** — the files a customer actually runs (`setup.sh`, `scripts/`, `hooks/`, `skills/`). Markdown docs were not line-reviewed.

---

## CRITICAL

### CR-01 — `merge-settings.py` has a Python syntax error; the entire installer aborts

[scripts/merge-settings.py:80](scripts/merge-settings.py#L80)

```python
add_hook("SessionStart", "*", "echo '{"continue": true, "suppressOutput": true}'")
```

The double quotes inside the string are unescaped, so `"echo '{"` closes early and `continue` is parsed as a keyword. The file **fails to compile** — verified:

```
SyntaxError: invalid syntax  (line 80)
```

Blast radius is the whole template:
- [setup.sh:60](setup.sh#L60) runs `python3 merge-settings.py` with **no `|| true`**, and [setup.sh:4](setup.sh#L4) sets `set -e`.
- So setup aborts at step 4. Steps 5 (skill sync), 6 (submodules), 7 (launchd) **never run**, and `~/.claude/settings.json` never receives any hooks or safety deny-rules.

Every customer hits this on first run.

**Fix** — use a single-quoted outer string (and escape the inner single quotes), or build the JSON with `json.dumps`:

```python
add_hook("SessionStart", "*", 'echo \'{"continue": true, "suppressOutput": true}\'')
```

---

## WARNING

### WR-01 — `new-from-template` skill calls a script that doesn't exist

[skills/new-from-template/SKILL.md:58](skills/new-from-template/SKILL.md#L58)

```bash
python3 /Users/[YOUR_USERNAME]/kwoekel/_templates/new-from-template.py ...
```

Three problems in one line:
1. `_templates/new-from-template.py` **does not exist** in the repo (`_templates/` only contains two `.md` templates). The skill is registered (appears twice in `~/.claude/registry.json`), so a customer who invokes it gets a missing-file failure.
2. The path is hardcoded to `/Users/[YOUR_USERNAME]/...` — a literal placeholder that onboarding never fills.
3. The directory is `kwoekel`, but the repo is `kwoekel-ops-template`. Wrong path even after substitution.

**Fix:** ship the `new-from-template.py` script, or rewrite the skill to do the copy/substitution inline and use a repo-relative path.

### WR-02 — Personal project data baked into the skill-detection hooks

[hooks/skill-rules.json:18-20](hooks/skill-rules.json#L18) and [hooks/skill-eval.js:61](hooks/skill-eval.js#L61)

The shipped hooks hardcode Kierra's projects:
- `skill-rules.json` maps `kwoekel`, `kwoekel/projects`, `kwoekel/scheduled-tasks` → personal skills (`daily-job-scout`, `application-tailor`).
- `skill-eval.js` path regex hardcodes `kwoekel|Tampico|RNR|RockNRoll`.

These ship to every customer, won't match their projects, and leak personal context. Not a crash, but it's the kind of leftover that makes a template feel un-finished.

**Fix:** genericize these to placeholders the onboarding wizard fills, or strip the project-specific entries down to generic patterns.

### WR-03 — Setup hard-depends on a third-party personal repo with no failure guard

[setup.sh:68](setup.sh#L68) + [.gitmodules](.gitmodules)

```bash
git -C "$REPO_DIR" submodule update --init --recursive   # no || true
```

The only submodule is `token-dashboard` → `https://github.com/nateherkai/token-dashboard.git` (an individual's repo). It's reachable today, but under `set -e` the moment that repo goes private/deleted/renamed, **the whole setup aborts** at step 6 — and the customer's hooks (step 4) may already be half-applied. A template shouldn't hard-fail on one person's repo.

**Fix:** add `|| echo "  ⚠️ submodule skipped"` after the command, and/or make the token-dashboard submodule optional/vendored.

---

## INFO

### IN-01 — Dead variable in setup.sh
[setup.sh:7](setup.sh#L7) computes `NODE=...` but it's never used (`merge-settings.py` does its own node detection). Remove it.

### IN-02 — `.gitmodules` is a no-op onboarding target
[scripts/onboard.py:39](scripts/onboard.py#L39) lists `.gitmodules` in `TARGET_FILES`, but the file contains no `[PLACEHOLDER]` tokens, so the replace loop never touches it. Either drop it from the list or (if the intent was to repoint the submodule) add a real placeholder for the URL.

### IN-03 — Hooks are copied with `cp -n`, so re-running setup won't update them
[setup.sh:53](setup.sh#L53) uses `cp -n` (no-clobber). The header says "Safe to re-run," but re-running after a template update will **silently skip** any changed hook scripts already in `~/.claude/hooks/`. Document this, or switch to a checksum-aware copy.

### IN-04 — Import mode writes raw model output straight to files
[scripts/onboard.py:145](scripts/onboard.py#L145) writes Claude's stdout directly into `CLAUDE.md` etc. If the model emits a markdown code-fence or any preamble despite the prompt, the file is corrupted with no validation. Low risk (the manual wizard runs after), but consider stripping fences / validating before overwrite.

### IN-05 — `sync.py` rebuilds the README from the customer's *home* registry
[skills/sync.py:11](skills/sync.py#L11) reads `~/.claude/registry.json`, and [setup.sh:64](setup.sh#L64) runs it during install. On a customer machine this regenerates `skills/README.md` from **their entire** registry, not the template's curated skill list, and truncates descriptions to 80 chars mid-word ([sync.py:36](skills/sync.py#L36)). Expected behavior, but worth a note so customers aren't surprised when the table changes on first setup.

---

## Summary

| Sev | ID | One-liner |
|-----|----|-----------|
| 🔴 Critical | CR-01 | `merge-settings.py:80` syntax error → whole installer aborts under `set -e` |
| 🟡 Warning | WR-01 | `new-from-template` skill calls a missing script with a bad hardcoded path |
| 🟡 Warning | WR-02 | Personal project names hardcoded in skill-detection hooks |
| 🟡 Warning | WR-03 | Setup hard-depends on a third-party submodule with no failure guard |
| ⚪ Info | IN-01..05 | Dead var, no-op onboarding target, `cp -n` skips updates, unvalidated import writes, README regen from home registry |

**Fix CR-01 first** — nothing else in the installer runs until it's resolved.
