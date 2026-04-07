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
3. **If working on a specific client/project:** Read `[client-name]/README.md` and their most recent log in `[client-name]/logs/`.

Do NOT skip this step. Do NOT start producing work until you've read the context.

## Step 2: Follow these rules for the entire session

### Finding information
- Use the **Navigation Table** in CLAUDE.md to find what you need — it maps questions to files.
- Client-specific context lives in `[client-name]/context/` — always check there before asking the user for info that might already exist.
- If the vault has a `skills/` folder, check it for reusable prompts before building something from scratch.

### Contributing information
- **Route new context to the right file.** If the user shares brand info, update the brand file. If they share strategy, update the strategy file. If they share audience data, update the audience file. Don't let knowledge live only in this chat.
- **Merge, don't overwrite.** When adding to an existing file, ADD to the relevant section. Never delete existing content unless it's explicitly wrong.
- **Add source attribution** when processing external content: `<!-- Source: [description], processed YYYY-MM-DD -->`
- **Update the `updated:` date** in YAML frontmatter whenever you modify a file.

### Cross-referencing
- **Every `.md` file you create or modify** must include a `**Related Files:**` line near the top linking to connected docs.
- Format: `**Related Files:** [file-a](path/to/file-a.md) · [file-b](path/to/file-b.md)`
- When in doubt about what to link, link to the parent README and any context files you referenced.

### Daily logging
- **Log significant work** to `logs/YYYY-MM-DD.md` (org-level) during the session.
- If working on a specific client, ALSO log to `[client-name]/logs/YYYY-MM-DD.md`.
- What counts as significant: decisions made, files created/modified, research conducted, strategy changes, milestones, context added.
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
- Rename the copied folder to `[client-name]/` (lowercase, hyphens).
- Always create a first daily log entry documenting the setup.

### Using skills
- Check `skills/README.md` for available skills and when to use each one.
- Skills are reusable prompts — follow their instructions step by step.
- If a skill would help the current task, suggest it to the user.

### Processing intake documents
- If the user drops files in `Intake/` or mentions raw documents to process, use `skills/intake-processor.md` (if it exists) or follow this flow:
  1. Read the raw document
  2. Identify what type of info it contains
  3. Route extracted info to the correct context files (merge, don't overwrite)
  4. Add source attribution
  5. Move the original to `resources/archive/intake-processed/` with date prefix
  6. Log what was processed

## Step 3: Before ending the session

1. **Update today's daily log** with everything significant that happened.
2. **Update any status columns** in README files or CLAUDE.md that changed.
3. **Update `updated:` dates** in frontmatter of any files you modified.
4. **Flag any critical gaps** you noticed — tell the user what TODO items are most important to fill.

## Principles

- **The vault is the source of truth** — not this chat. Anything important gets written to a file.
- **One truth per file** — if a file grows past 300 lines, suggest splitting it.
- **The vault is a web** — every file connects to related files. Orphaned files are a bug.
- **Start sessions by reading, end sessions by writing** — read context first, log everything at the end.
- **Be a good citizen** — leave the vault better than you found it. Fix small issues (broken links, missing dates, missing cross-references) as you encounter them.

---

*This operator skill is part of the Second Brain system. For initial vault setup, use `second-brain-initiate.md`.*
