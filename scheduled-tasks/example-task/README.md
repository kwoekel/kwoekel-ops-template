# [Task Name] — Scheduled Task

**Schedule:** [e.g., Daily at 8am / Weekly on Sunday at 6pm]
**Runner:** launchd — `com.[YOUR_USERNAME].[task-name]`

## What It Does
[1-2 sentences describing what this task automates]

## Files
| File | Purpose |
|---|---|
| `run.sh` | Entry point — invoked by launchd |
| `[script].py` | [purpose] |
| `CLAUDE.md` or `SKILL.md` | Skill definition (if Claude-powered) |

## Setup
```bash
# Install the launchd agent (run once):
python3 scripts/install-launchd.py
```

## Logs
Logs write to `run.log` in this directory.

## Manual Run
```bash
bash scheduled-tasks/[task-name]/run.sh
```
