# Second Brain System

A plug-and-play system for building a shared "second brain" for any organization using plain markdown files. Works with any AI tool. No vendor lock-in.

**One prompt builds it. One skill keeps it running.**

---

## Get Started

### Just tell your AI:

> Read https://github.com/accountsFON/second-brain-system and follow the instructions in `second-brain-initiate.md` to build me a second brain vault in this folder.

That's it. The AI reads the repo, asks you 14 questions about your org, and builds the entire vault. Works in Claude, ChatGPT, Gemini, Cursor — any AI tool that can read a URL or files.

### Or clone it first:

```bash
git clone https://github.com/accountsFON/second-brain-system.git
```

Then open the `second-brain-initiate.md` file, copy everything below the divider, and paste it into your AI tool while pointing at an empty folder.

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

## The two files

| File | Purpose | When |
|------|---------|------|
| [`second-brain-initiate.md`](second-brain-initiate.md) | Builds the vault from scratch via guided questionnaire | Run **once** |
| [`second-brain-operator.md`](second-brain-operator.md) | Teaches any AI how to work inside the vault | Load **every session** |

### `second-brain-initiate.md` — Build the vault

Paste into any AI tool pointed at an empty folder. It:
- Asks 14 questions about your org (takes ~5 min)
- Creates the full vault structure with CLAUDE.md at the root
- Populates context files with your answers
- Creates shared AI skills the whole team can use
- Sets up client/project templates and an intake pipeline
- Builds out your first client folder

### `second-brain-operator.md` — Run every session

Load as your first message in any AI session. It teaches the AI to:
- Read CLAUDE.md and the latest daily log before starting work
- Route new information to the correct files (not buried in chat)
- Cross-reference every file to related docs
- Update daily logs with significant work
- Process raw docs from the Intake folder
- Follow naming conventions and file standards

## Why it works

Most organizational knowledge dies in chat threads, email chains, and someone's head. This system captures it in files that every future session — by any person, with any tool — can read and build on.

- **Start a session** — AI reads the full org context before doing anything
- **Do the work** — AI routes new knowledge to the right files, not just the chat
- **End the session** — daily log captures what happened for whoever comes next

The vault compounds. Every session makes the next one smarter.

## Who is this for

- **Agencies** managing multiple clients
- **Startups** building institutional knowledge from day one
- **Consultancies** that need context continuity across engagements
- **Any team** tired of repeating themselves to AI tools

## Supercharge it with Obsidian

The vault is plain markdown and works anywhere. But if you want a visual layer, open it as an [Obsidian](https://obsidian.md) vault. You get:

- **Graph View** — see how every file connects to every other file in a visual web
- **Backlinks** — click any file and instantly see everything that references it
- **Quick Search** — find anything across the entire vault in milliseconds
- **Live Preview** — edit markdown with a clean visual editor
- **Daily Notes** — Obsidian's daily notes plugin maps perfectly to the `logs/` folder

Obsidian is free, works on Mac/Windows/Linux/mobile, and syncs via any cloud drive (Google Drive, Dropbox, OneDrive, iCloud). Your vault is already Obsidian-compatible out of the box.

**To get started:** Download [Obsidian](https://obsidian.md), click "Open folder as vault", and point it at your vault folder. That's it.

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

*Built by [Five One Nine Marketing](https://github.com/accountsFON) for teams who are tired of repeating themselves.*

