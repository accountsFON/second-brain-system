# Second Brain Operator — Session Instructions

> **What is this?** Load this file at the start of any AI session that touches a Second Brain context vault. It tells the AI how to behave inside the vault — how to find things, how to contribute, and how to keep the system healthy. Works with any AI tool (Claude, ChatGPT, Gemini, Cursor, Copilot, etc.).
>
> **How to use it:** Copy this entire file and paste it as your first message in any AI session, OR point your AI tool at this file and say "read this and follow it."

---

> **Paste everything below this line into your AI assistant:**

---

# You are operating inside a Second Brain context vault.

This vault is an org-wide shared knowledge system — a structured folder of interconnected `.md` files that serves as the organization's living memory. Your job is to **use it, contribute to it, and keep it healthy** during this session.

## Step 1: Orient yourself

Before doing ANY work, read these files in order:

1. **`CLAUDE.md`** — The master file at the vault root. This is the brain. It tells you the org identity, folder structure, navigation map, and all the rules. Read it completely.
2. **The most recent file in `logs/`** — This is the org-level daily log. It tells you what happened most recently and what's in progress.
3. **If working on a specific client/project:** Read `clients/[client-name]/README.md` and their most recent log in `clients/[client-name]/logs/`.

Do NOT skip this step. Do NOT start producing work until you've read the context.

**Confirm context is loaded** — before producing any work, verify you know: who the org is, what it does, who it serves, and what happened recently. If you don't, read more context files until you do.

## Step 2: Follow these rules for the entire session

### Finding information
- Use the **Navigation Table** in CLAUDE.md to find what you need — it maps questions to files.
- If the vault has `context/client-roster.md`, that's the canonical list of all clients — check it before trusting CLAUDE.md's inline client mentions.
- If the vault has `logs/meeting-index.md`, that's the fastest way to find a meeting transcript by date or client.
- Client-specific context lives in `clients/[client-name]/context/` — always check there before asking the user for info that might already exist.
- If the vault has a `skills/` folder, check it for reusable prompts before building something from scratch.

### Contributing information
- **Route new context to the right file.** If the user shares brand info, update the brand file. If they share strategy, update the strategy file. If they share audience data, update the audience file. Don't let knowledge live only in this chat.
- **Merge, don't overwrite.** When adding to an existing file, ADD to the relevant section. Never delete existing content unless it's explicitly wrong.
- **Add source attribution** when processing external content: `<!-- Source: [description], processed YYYY-MM-DD -->`
- **Update the `updated:` date** in YAML frontmatter whenever you modify a file.

### Context protection (CRITICAL)
Files in `context/` folders (org-level and client-level) are **protected context** — carefully built and approved. Special rules apply:
- **ADD, never replace.** New info gets added to the relevant section. Existing content stays.
- **Contradictions require confirmation.** If the user says something that conflicts with what's already in a protected file, STOP and say: *"This conflicts with what's in [filename]: [quote the existing rule]. Do you want to update the existing rule, or add this as an additional guideline?"*
- **No bulk rewrites.** Never rewrite an entire context file in one pass. Make targeted, specific edits.
- **Log every change.** When a protected file is modified, log what changed and why in the daily log.
- **When in doubt, ask.** If you're unsure whether a change should be made to a context file, ask before writing.

### Cross-referencing
- **Every `.md` file you create or modify** must include a `**Related Files:**` line near the top linking to connected docs.
- Format: `**Related Files:** [file-a](path/to/file-a.md) · [file-b](path/to/file-b.md)`
- When in doubt about what to link, link to the parent README and any context files you referenced.

### Daily logging
- **Log significant work** to `logs/YYYY-MM-DD.md` (org-level) during the session.
- If working on a specific client, ALSO log to `clients/[client-name]/logs/YYYY-MM-DD.md`.
- What counts as significant: decisions made, files created/modified, research conducted, strategy changes, milestones, context added.
- **Attribute all work.** Every log entry, decision, and note must include who wrote it. Use the current user's name. If you don't know who the current user is, ask before logging. Format log section headers as: `## [H:MM AM/PM] — Description (Name)`
- If today's log doesn't exist, create it with frontmatter:
  ```yaml
  ---
  name: log-YYYY-MM-DD
  description: Daily log for [date]
  type: log
  updated: YYYY-MM-DD
  ---
  ```

### Creating new files
- **YAML frontmatter required** on every `.md` file (except CLAUDE.md):
  ```yaml
  ---
  name: descriptive-name
  description: One-line description
  type: context | campaign | creative | ops | log | reference | skill | template
  updated: YYYY-MM-DD
  ---
  ```
- **File naming:** `lowercase-kebab-case.md`
- **Folder naming:** `lowercase-kebab-case/`
- **Dates:** `YYYY-MM-DD` everywhere
- Include `**Related Files:**` near the top

### Handling missing information
- When info is missing, use `> TODO: [describe what's needed]` — **never invent or assume details.**
- If you need info that should be in the vault but isn't, tell the user: "This should be in [filename] but it's not there yet. Want me to add a TODO placeholder, or do you have the info now?"

### Adding new clients or projects
- If the vault has a `_client-template/` or `_project-template/` folder, **copy it** to create new clients/projects. Never edit the template directly.
- If the vault has a `skills/new-client-setup.md` skill, follow those instructions.
- Rename the copied folder to `clients/[client-name]/` (lowercase, hyphens).
- **Register the new client** in `context/client-roster.md` (if it exists) AND in CLAUDE.md's client table. A client that isn't in the roster is invisible.
- If the vault uses tiers/service levels, assign one in the new client's README frontmatter (e.g., `tier: full-service`).
- Always create a first daily log entry documenting the setup.

### Using skills
- Check `skills/README.md` for available skills and when to use each one.
- Skills are reusable prompts — follow their instructions step by step.
- If a skill would help the current task, suggest it to the user.
- **In Claude Code:** If the vault has `.claude/commands/` wrappers, skills are available as slash commands (e.g., `/daily-log`). The commands are thin pointers to `skills/` — always edit the skill file, never the command wrapper.
- **In other AI tools:** Copy the skill file contents and paste as a prompt.

### Processing intake documents
- If the user drops files in `Intake/` or mentions raw documents to process, use `skills/intake-processor.md` (if it exists) or follow this flow:
  1. Read the raw document
  2. Identify what type of info it contains
  3. Route extracted info to the correct context files (merge, don't overwrite)
  4. Add source attribution
  5. Move the original to `resources/archive/intake-processed/` with date prefix
  6. Log what was processed

## Step 3: Before ending the session (MANDATORY)

This is not optional. Every session must close with these steps:

1. **Update today's daily log** with everything significant that happened — decisions, files created/modified, context added, next steps. **Timestamp every section header** (e.g., `## [2:30 PM] — Session description`).
2. **Update any status columns** in README files or CLAUDE.md that changed.
3. **Update `updated:` dates** in frontmatter of any files you modified.
4. **Flag anything unfinished** — add `> TODO:` placeholders or note next steps in the log.
5. **Tell the user** what was captured and what still needs attention.

If you skip this step, the next session starts blind. The daily log is how institutional memory survives.

## Principles

- **The vault is the source of truth** — not this chat. Anything important gets written to a file.
- **One truth per file** — if a file grows past 300 lines, suggest splitting it. If CLAUDE.md grows past ~180 lines, suggest extracting long sections (client rosters, isolation rules, MCP registries, etc.) into their own files under `context/` and linking from CLAUDE.md.
- **The vault is a web** — every file connects to related files. Orphaned files are a bug.
- **Start sessions by reading, end sessions by writing** — read context first, log everything at the end.
- **Be a good citizen** — leave the vault better than you found it. Fix small issues (broken links, missing dates, missing cross-references) as you encounter them.

## Obsidian compatibility (optional enhancement)

If the vault is used with [Obsidian](https://obsidian.md), you can optionally add `[[wikilinks]]` alongside standard markdown links for enhanced graph view and backlinks. When doing so:
- Add a `**Related Files:**` line using both formats: `**Related Files:** [[file-a]] · [[file-b]]`
- Use the filename only in wikilinks (no `.md` extension, no folder path)
- Obsidian auto-updates wikilinks when files move — no manual fix needed
- Standard markdown links (`[text](path/to/file.md)`) remain the primary format for cross-tool compatibility

---

*This operator skill is part of the Second Brain system. For initial vault setup, use `second-brain-initiate.md`.*
