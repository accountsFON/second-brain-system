---
name: context-loader
description: Session-start context bootstrap. Reads the brain file, latest log, and client context to orient the AI before work begins.
type: skill
updated: YYYY-MM-DD
---

**Related Files:** [README.md](README.md) · [daily-log.md](daily-log.md) · [../CLAUDE.md](../CLAUDE.md)

# Context Loader

Load the full vault context at session start so you can work with full organizational awareness.

## When to use

**Every session start.** This is step 1. Do not produce any work until context is loaded.

## Instructions

### 1. Read the brain

Read `CLAUDE.md` at the vault root. This gives you:
- Who the org is
- Folder structure and navigation
- All rules to follow
- Client/project roster

### 2. Read the latest daily log

Find the most recent file in `logs/` (sorted by date). This tells you:
- What happened last
- What is in progress
- What was flagged for follow-up

### 3. Read client/project context (if applicable)

If this session involves a specific client or project:
- Read `clients/[name]/README.md`
- Read their most recent log in `clients/[name]/logs/`
- Scan their `context/` subfolder for relevant files

### 4. Confirm context loaded

Before doing any work, verify you know:
- Who the org is and what it does
- What happened recently
- What rules apply
- If working on a client: who they are, what the engagement covers, what happened last

If any of these are unclear, read more context files until they are. Do not guess. Do not start work with partial context.

## Output

A brief confirmation to the user: what context you loaded, what the current state is, and whether anything was flagged in the latest log that needs attention.
