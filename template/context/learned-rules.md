---
name: learned-rules
description: Cross-platform mirror of corrections and rules learned during work. Every AI agent must follow these.
type: context
updated: YYYY-MM-DD
---

**Related Files:** [../CLAUDE.md](../CLAUDE.md) · [../AGENTS.md](../AGENTS.md) · [../GEMINI.md](../GEMINI.md) · [soul.md](soul.md)

# Learned Rules

These rules are captured over time as the team works with AI tools. They are stored here so every agent (Claude, Codex, Gemini, Cursor, Copilot, ChatGPT, others) inherits the same operating discipline regardless of which tool is running.

If your AI tool has a persistent memory system (like Claude's auto-memory), that memory is the live source. This file is the cross-platform snapshot so non-memory tools stay in sync.

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
> Every session that touches the vault must update the daily log before closing. The log is how institutional memory survives.
