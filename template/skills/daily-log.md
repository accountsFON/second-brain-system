---
name: daily-log
description: Mandatory session-end logging. Creates or updates today's daily log with timestamped, attributed entries.
type: skill
updated: YYYY-MM-DD
---

**Related Files:** [README.md](README.md) · [identify-user.md](identify-user.md) · [../CLAUDE.md](../CLAUDE.md)

# Daily Log

Update today's daily log with everything significant from this session.

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

```markdown
## [H:MM AM/PM] - Description (Name)

- What was done (decisions, files created/modified, research, context added)
- What changed (status updates, strategy shifts, milestones)
- What is next (TODOs, blockers, follow-ups)
```

### 5. Update frontmatter dates

Update the `updated:` field in frontmatter of any files modified during the session.

### 6. Flag unfinished work

Add `> TODO:` placeholders for anything incomplete. Note next steps clearly so the next session can pick up without guessing.

## What to log

- Decisions made and why
- Files created or significantly modified
- Research conducted and key findings
- Strategy changes or pivots
- Client/project milestones
- Context added to the vault
- Blockers encountered
- Next steps

## What NOT to log

- Routine reads (just reading files is not significant)
- Minor formatting fixes
- Anything that did not change the vault state or produce a decision

## Output

One updated log file at `logs/YYYY-MM-DD.md` with a timestamped, attributed section.
