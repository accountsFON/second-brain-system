# Second Brain System

A plug-and-play system for building a shared "second brain" for any organization using plain markdown files. Works with any AI tool. No vendor lock-in.

**One prompt builds it. One skill keeps it running.**

---

## What is this?

A structured folder of interconnected `.md` files that becomes your organization's living memory. Every AI session reads the context first and knows exactly where to find and store information. Every team member benefits from what everyone else has contributed.

It works with **any AI tool** — Claude, ChatGPT, Gemini, Cursor, Copilot, or any text editor. No proprietary formats. No subscriptions. Just markdown files and folder structure.

## What you get

```
your-vault/
├── CLAUDE.md                  # The brain — navigation, rules, org identity
├── context/                   # Org-level knowledge (team, services, brand, voice, tools)
├── skills/                    # Shared AI prompts the whole team can use
├── _client-template/          # Copy this for each new client or project
├── templates/                 # Meeting notes, decision records, campaign briefs
├── resources/                 # Shared assets and archive
├── Intake/                    # Drop raw docs here for AI processing
└── logs/                      # Daily logs — institutional memory
```

## Quick Start

### 1. Create an empty folder

Anywhere your team can access — Google Drive, Dropbox, OneDrive, a git repo.

### 2. Build the vault

Open any AI tool, point it at the empty folder, and paste the contents of **[`second-brain-initiate.md`](second-brain-initiate.md)** (everything below the divider line).

Answer 14 questions. The AI builds the entire vault.

### 3. Use it

Every session after that, load **[`second-brain-operator.md`](second-brain-operator.md)** as your first message. It teaches the AI how to:

- Read context before starting work
- Route new information to the right files
- Cross-reference everything
- Update daily logs
- Keep the vault healthy

## The two files

| File | Purpose | When |
|------|---------|------|
| [`second-brain-initiate.md`](second-brain-initiate.md) | Builds the vault from scratch via guided questionnaire | Run **once** |
| [`second-brain-operator.md`](second-brain-operator.md) | Teaches any AI how to work inside the vault | Load **every session** |

## Why it works

Most organizational knowledge dies in chat threads, email chains, and someone's head. This system captures it in files that every future session — by any person, with any tool — can read and build on.

- **Start a session** → AI reads the full org context before doing anything
- **Do the work** → AI routes new knowledge to the right files, not just the chat
- **End the session** → daily log captures what happened for whoever comes next

The vault compounds. Every session makes the next one smarter.

## Who is this for

- **Agencies** managing multiple clients
- **Startups** building institutional knowledge from day one
- **Consultancies** that need context continuity across engagements
- **Any team** tired of repeating themselves to AI tools

## Design principles

1. **CLAUDE.md is the brain** — concise navigation file, links to everything
2. **One truth per file** — no mega-docs, everything cross-referenced
3. **Context is layered** — org-level at root, client/project folders inherit and override
4. **Daily logs** — institutional memory that survives across sessions and people
5. **Start minimal** — only create files you have content for, grow organically
6. **Works everywhere** — plain markdown, no tool lock-in

---

## License

MIT — use it however you want.

---

*Built for teams who are tired of repeating themselves.*
