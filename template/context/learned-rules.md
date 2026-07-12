---
name: learned-rules
description: Canonical shared corrections and rules every AI agent must follow.
type: context
updated: YYYY-MM-DD
---

**Related Files:** [../CLAUDE.md](../CLAUDE.md) · [../AGENTS.md](../AGENTS.md) · [../GEMINI.md](../GEMINI.md) · [soul.md](soul.md)

# Learned Rules

These rules are captured over time as the team works with AI tools. This file is the canonical shared policy so every agent inherits the same operating discipline regardless of which tool is running.

Local model memory may capture observations and propose corrections, but it does not silently override this file. Promote universal corrections here through a reviewed update.

Routine factual logging is the standing exception to the review requirement. Agents may create the current dated log and append a new attributed entry to the daily and applicable client or project logs without separate approval when the entry covers current work, preserves existing content, and contains no sensitive information. Identity gaps, sensitive details, edits to existing log content, source of truth changes, and external actions still require approval.

**Update this file** whenever a correction or preference crosses the bar of "applies to all tools, not just the one that learned it."

If a rule below conflicts with a user instruction in the current session, the user wins. These rules override default model behavior, not direct user requests.

---

## Hard rules

> Add rules here as the team discovers them. Format: what to do (or not do), why, and when it applies.
>
> Example:
> ### Never overwrite existing content without confirmation
> The vault is a shared source of truth. Conversation is not permission to write. Tell the user what you plan to change, quote the file and section, wait for a clear "yes." Add, never replace. Contradictions require confirmation.

---

## Writing and copy discipline

> Add voice, tone, and formatting rules here as the team discovers them.
>
> Example:
> ### Use plain language over jargon
> If a simpler word works, use it. The vault serves people with different expertise levels.

---

## Tool-specific gotchas

> Add platform quirks and workarounds here.
>
> Example:
> ### Always clean-build before deploying
> Incremental caches can hide errors that only surface in CI. Run a clean build locally before pushing.

---

## Process rules

> Add workflow rules here.
>
> Example:
> ### Log significant work at session end
> Every session that touches the vault must automatically append the daily and applicable scoped logs before closing. Routine factual log additions are preauthorized. The logs are how institutional memory survives.
