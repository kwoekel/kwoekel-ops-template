---
name: weekly-ops-audit
description: Weekly audit of the ops repo and Claude Code agent harness — run manually every Friday or invoke via a scheduled task
---

You are auditing this Claude Code agent harness for the past week. Pre-parsed system data is provided below as JSON — do NOT read files yourself.

## Input Data

The following JSON was pre-computed by fetch-audit-data.py:

```
{{AUDIT_DATA_JSON}}
```

## Step 0 — 4Cs System Health (run before harness checks)

Quick read-only check of system context — takes 2 minutes, surfaces drift before it causes problems.

**Context** — Is the CLAUDE.md and context still accurate?
- Does `context/current-priorities.md` reflect this week's actual focus?
- Does `context/work.md` reflect current employment status?
- Is `context/goals.md` still pointing at the right targets?
- Flag anything that reads stale or contradicts recent sessions.

**Connections** — Are integrations healthy?
- Read `context/connections.md` — are there any ⚠️ or ❌ status entries?
- Were any MCP tools failing or timing out this week (check error events in audit data)?
- Is Infisical injection still working for scheduled tasks?
- Update `connections.md` Status column for anything that changed this week.

**Capabilities** — Are skills earning their place?
- (Covered in Step 1 skill coverage section below)
- Also flag: any skills in registry.json that haven't been used in 3+ weeks

**Cadence** — Is the rhythm still working?
- Are scheduled tasks running on their intended schedule (check logs)?
- Any tasks that fired but produced no useful output?
- Is the weekly audit itself running consistently?

Add a **4Cs Summary** section to the Notion report:
```
Context: OK / [what needs updating]
Connections: OK / [what's broken or stale]
Capabilities: [N unused skills flagged]
Cadence: OK / [what's off-schedule]
```

---

## Step 1 — Run these checks using the JSON above

**Hook health**
- Are all 3 hooks (pre-tool.sh, post-tool.sh, stop.sh) present and executable?
- Did any `budget_halt` events fire this week? If yes, how many and in which sessions?
- Did any `budget_warning` events fire? Flag if warnings are frequent (>3/session on average).

**Permission drift**
- Are there tools appearing in `tool_considered` events that are NOT listed in registry.json? If yes, list them — they may need to be added to the registry.
- Are there any `permission_denied` events? List the tool and session.

**Skill coverage**
- Which skills from registry.json were used this week (appear in `tool_selected` events)?
- Which skills were NOT used at all? Flag any that have been unused for 2+ consecutive weeks (note: you only have 1 week of data per run — flag if unused this week and add a note to monitor).

**Budget health**
- Average tool calls per session this week.
- Sessions that hit the warning threshold (60 calls).
- Sessions that hit the hard limit (80 calls).

**Error signals**
- Any `error` events in the log? List them with their session_id and timestamp.

## Step 3 — Write the gap report

Create a Notion page under your audit parent page (page ID: `[YOUR_NOTION_AUDIT_PARENT_ID]` — set this in `endpoints.md`) titled "Weekly Ops Audit — [date]" with the following sections:

### System Health
- Hooks: OK / Issues found
- Permissions: OK / Drift detected
- Budget: Average X tool calls/session, N warnings, N halts

### What Needs Attention
(Only include if issues found — skip section if all clear)
- List each issue with: what it is, why it matters, what to do

### Skill Usage This Week
- Used: [list]
- Unused: [list] — monitor next week

### Primitive Coverage (rate each as: Healthy / Needs work / Not yet implemented)
- Tool registry
- Permission tiers
- Session logging
- Budget tracking
- Weekly audit (this one)
- Deferred: workflow state machine, idempotency, streaming events, multi-agent coordination, memory system

### One Recommendation
The single highest-leverage improvement to make before next Sunday's audit.

Keep everything scannable — bullets, not paragraphs.

After creating the page, notify with:
osascript -e 'display notification "Weekly ops audit is ready in Notion" with title "Ops Audit" sound name "Glass"'
