---
name: daily-log
description: Automatic routine logging. Appends today's daily and applicable scoped logs with timestamped, attributed entries.
type: skill
updated: YYYY-MM-DD
---

**Related Files:** [README.md](README.md) · [identify-user.md](identify-user.md) · [../CLAUDE.md](../CLAUDE.md)

# Daily Log

Update today's daily and applicable client or project logs with everything significant from this session.

## Standing authorization

Routine factual logging is preauthorized. Create the current dated log when it is missing and append new attributed entries without asking for approval when they cover the current session, leave existing content untouched, and contain no sensitive information.

Ask before logging only when identity is unresolved, sensitive information would be exposed, or existing log content must change. This authorization does not cover source of truth changes or external actions.

## When to use

**Every session end.** This is not optional. The daily log is how institutional memory survives across sessions, people, and tools.

## Instructions

### 1. Resolve identity

If the vault has multiple operators, run `skills/identify-user.md` first to get the correct attribution. If single-operator, use the operator's name from CLAUDE.md.

### 2. Get the current time

Run the appropriate command for the local timezone:
- macOS/Linux: `TZ='America/New_York' date '+%I:%M %p'` (adjust timezone)
- Windows: `Get-Date -Format 'h:mm tt'`

Never guess the time.

### 3. Create or update the log file

**Path:** `logs/YYYY-MM-DD.md`

If the file does not exist, create it:

```markdown
---
name: log-YYYY-MM-DD
description: Daily log for YYYY-MM-DD
type: log
updated: YYYY-MM-DD
---

# Daily Log: YYYY-MM-DD
```

### 4. Add a timestamped entry

Keep the entry concise but complete. State what changed, the verified result, why it matters, current status, and the next step or blocker when one exists. Include direct links to any live deliverable, preview, report, dashboard, task, pull request, or other useful result. A deployed deliverable is not fully logged until its live URL appears in both the daily log and applicable scoped log.

```markdown
## [H:MM AM/PM] - Description (Name)

- What changed and the verified result
- Why it matters
- Current status and what is next
- Live result: [Open the deliverable](https://example.com/result)
```

### 5. Append the applicable scoped log

If the work belongs to a client or project, append the same factual outcome to its dated log. Follow the folder's existing log naming convention.

### 6. Update frontmatter dates

Update the `updated:` field in frontmatter of any files modified during the session.

### 7. Flag unfinished work

Add `> TODO:` placeholders for anything incomplete. Note next steps clearly so the next session can pick up without guessing.

## What to log

- Decisions made and why
- Files created or significantly modified
- Research conducted and key findings
- Strategy changes or pivots
- Client/project milestones
- Direct links to live deliverables and other useful results
- Context added to the vault
- Blockers encountered
- Next steps

## What NOT to log

- Routine reads (just reading files is not significant)
- Minor formatting fixes
- Anything that did not change the vault state or produce a decision

## Output

The updated daily log at `logs/YYYY-MM-DD.md` and, when applicable, the matching client or project log, each with a timestamped, attributed section.
