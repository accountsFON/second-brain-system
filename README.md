# Second Brain System

A plug-and-play system for building a shared "second brain" for any organization using plain markdown files. Works with any AI tool. No vendor lock-in.

**One prompt builds it. Template files bootstrap it. Skills keep it alive.**

---

## Get Started

### Just tell your AI:

> Read https://github.com/accountsFON/second-brain-system and follow the instructions in `second-brain-initiate.md` to build me a second brain vault in this folder.

That's it. The AI reads the repo, asks you 14 questions about your org, and builds the entire vault. Works in Claude, ChatGPT, Gemini, Cursor, Codex, Copilot... any AI tool that can read a URL or files.

### Or clone it first:

```bash
git clone https://github.com/accountsFON/second-brain-system.git
```

Then open `second-brain-initiate.md`, copy everything below the divider, and paste it into your AI tool while pointing at an empty folder.

---

## What is this?

A structured folder of interconnected `.md` files that becomes your organization's living memory. Every AI session reads the context first and knows exactly where to find and store information. Every team member benefits from what everyone else has contributed.

It works with **any AI tool** and any text editor. No proprietary formats. No subscriptions. Just markdown files and folder structure.

## The three pillars

### 1. The Brain (CLAUDE.md + cross-tool shims)

One master file that every tool reads first. `AGENTS.md`, `GEMINI.md`, and `README.md` are thin redirects so Claude, Codex, Gemini, Cursor, and humans all land in the same brain. No tool reads a different truth.

### 2. Persistent Memory (learns across sessions)

Two layers working together:
- **Local memory** (tool specific): captures observations and proposes corrections for review.
- **Learned rules** (`context/learned-rules.md`): canonical shared policy. Every AI reads it, and local memory cannot silently override it.

### 3. Executable Skills (the vault does things)

Plain markdown files in `skills/` that encode repeatable workflows. Not documentation, execution. `daily-log`, `brain-check`, `intake-processor`, `identify-user`. The vault maintains itself.

## What you get

```
your-vault/
├── CLAUDE.md                  # The brain: navigation, rules, org identity
├── AGENTS.md                  # Cross-tool shim for Codex/Copilot/Cursor
├── GEMINI.md                  # Cross-tool shim for Gemini CLI
├── .codex/config.toml         # Portable Codex project settings
├── .agents/skills/            # Thin Codex bridge to canonical skills
├── README.md                  # Human-readable tour
├── context/
│   ├── soul.md                # Identity, voice, values (who the org IS)
│   ├── org-profile.md         # What the org does
│   ├── team.md                # Team members and roles
│   ├── services.md            # What the org offers
│   ├── tools.md               # Platforms and software
│   ├── brand.md               # Visual identity
│   ├── voice.md               # Writing style and tone
│   ├── processes.md           # SOPs and workflows
│   ├── client-roster.md       # All clients at a glance
│   ├── vault-manifest.md      # Master index of everything in the vault
│   ├── learned-rules.md       # Cross-platform rules learned during work
│   └── vault-isolation-rules.md
├── skills/
│   ├── README.md              # Skill index
│   ├── context-loader.md      # Session-start bootstrap
│   ├── daily-log.md           # Session-end logging
│   ├── brain-check.md         # Vault self-audit
│   ├── intake-processor.md    # Process raw docs from Intake/
│   ├── identify-user.md       # Resolve operator for log attribution
│   └── new-client-setup.md    # Set up a new client folder
├── .claude/
│   ├── commands/              # Slash command wrappers (point to skills/)
│   └── memory/
│       └── MEMORY.md          # Persistent memory index (Claude Code)
├── clients/                   # One folder per client
├── projects/                  # Internal projects
├── _client-template/          # Copy for each new client
├── templates/                 # Meeting notes, decision records, briefs
├── resources/
│   ├── assets/                # Logos, brand files
│   ├── machines/              # Operator-machine identity registry
│   └── archive/               # Completed work, processed intake
├── Intake/                    # Drop raw docs here for AI processing
└── logs/                      # Daily logs + meeting index
```

## The files

| File | Purpose | When |
|------|---------|------|
| [`second-brain-initiate.md`](second-brain-initiate.md) | Builds the vault from scratch via guided questionnaire | Run **once** |
| [`second-brain-operator.md`](second-brain-operator.md) | Teaches any AI how to work inside the vault | Load **every session** |
| [`AGENTS.md`](AGENTS.md) | Auto-loaded by Codex, Copilot, Cursor | Automatic |
| [`GEMINI.md`](GEMINI.md) | Auto-loaded by Gemini CLI | Automatic |
| [`template/`](template/) | Starter files the initiate prompt builds from | Reference |

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
- **Mandatory session start**: read CLAUDE.md, read latest daily log, verify context before work
- **Context protection**: never overwrite protected files, contradictions require confirmation
- Route new information to the correct files (not buried in chat)
- Cross-reference every file to related docs
- **Mandatory session end**: update daily logs with timestamped entries, flag unfinished work

### Cross-tool shims — Automatic

`AGENTS.md` and `GEMINI.md` are thin redirect files that point to CLAUDE.md. When Codex opens your vault, it auto-reads `AGENTS.md` and lands in the same brain as Claude. When Gemini CLI opens it, same thing via `GEMINI.md`. Switch tools freely. Same context, same rules.

### Template files — Reference

The `template/` folder contains starter versions of the key files the initiate prompt generates. Use them as reference for what the vault should look like, or copy them directly if you prefer to set up manually instead of using the questionnaire.

## Starter skills (ship with the vault)

| Skill | What it does |
|-------|-------------|
| **context-loader** | Reads the brain file, latest log, and client context. Session-start bootstrap. |
| **daily-log** | Creates or updates today's log with timestamped, attributed entries. Mandatory at session end. |
| **brain-check** | Audits the vault: staleness, broken links, manifest drift, orphaned files, intake backlog. |
| **intake-processor** | Reads a raw doc from Intake/, extracts key info, routes it to the right vault files, archives the original. |
| **identify-user** | Resolves who is operating the current session by matching hostname + OS username against a registry. For multi-person or multi-machine vaults. |
| **new-client-setup** | Copies the client template, asks setup questions, populates initial files, registers in the roster. |

## Why it works

Most organizational knowledge dies in chat threads, email chains, and someone's head. This system captures it in files that every future session, by any person, with any tool, can read and build on.

- **Start a session**: AI reads the full org context before doing anything
- **Do the work**: AI routes new knowledge to the right files, not just the chat
- **End the session**: daily log captures what happened for whoever comes next
- **Switch tools**: AGENTS.md and GEMINI.md ensure the new tool picks up where the old one left off
- **Learn from mistakes**: corrections saved in memory and learned-rules compound across every future session

The vault compounds. Every session makes the next one smarter.

## Who is this for

- **Agencies** managing multiple clients
- **Startups** building institutional knowledge from day one
- **Consultancies** that need context continuity across engagements
- **Solo operators** who use multiple AI tools and want persistent context
- **Any team** tired of repeating themselves to AI tools

## Supercharge it with Obsidian

The vault is plain markdown and works anywhere. But if you want a visual layer, open it as an [Obsidian](https://obsidian.md) vault. You get:

- **Graph View**: see how every file connects to every other file
- **Backlinks**: click any file and instantly see everything that references it
- **Quick Search**: find anything across the entire vault in milliseconds
- **Live Preview**: edit markdown with a clean visual editor
- **Daily Notes**: maps perfectly to the `logs/` folder

Obsidian is free, works on Mac/Windows/Linux/mobile, and syncs via any cloud drive (Google Drive, Dropbox, OneDrive, iCloud). Your vault is already Obsidian-compatible out of the box.

**To get started:** Download [Obsidian](https://obsidian.md), click "Open folder as vault", and point it at your vault folder.

## Claude Code Integration

If your team uses Claude Code, the vault automatically provides slash commands for every skill. Type `/daily-log`, `/brain-check`, `/intake-processor`, etc. The commands in `.claude/commands/` are thin one-line wrappers that point to the skill files in `skills/`. One source of truth, no duplication.

The `.claude/memory/` directory can hold Claude observations across sessions. Universal rules are reviewed before promotion to canonical `context/learned-rules.md` so other tools inherit approved policy.

**Adding a new skill:** Create the `.md` file in `skills/`, then add a wrapper in `.claude/commands/` with:
```
Read and execute the skill instructions in skills/[name].md

Do exactly what the skill file says. Do not summarize the skill. Run it.
```

## Codex Integration

Codex reads `AGENTS.md` for durable instructions and `.agents/skills/vault-bridge/SKILL.md` for shared workflows. The bridge points back to `skills/`, so Claude and Codex execute the same canonical instructions.

For a cloud synced vault, each operator adds this to their local `~/.codex/config.toml` and restarts Codex:

```toml
project_root_markers = [".git", ".codex"]
```

Keep personal configuration at home. Shared `.codex/config.toml` must not contain credentials, absolute paths, permissions, native notifications, or telemetry commands.

Lifecycle hooks are optional. If you add automated logging or notifications, treat hooks as thin platform adapters. Keep state local, seed the current log baseline on the first observed event even when session start was missed, use deterministic event identifiers, and release local locks before network calls. Start with no live destination and prove historical replay, retry, and concurrent duplicate safety first. The generic checklist lives in [`template/resources/agent-platform/README.md`](template/resources/agent-platform/README.md).

### MCP Servers (optional, for technical teams)

If your team uses external tools (ad platforms, CRMs, project management APIs), you can connect them to Claude Code via MCP servers. A good pattern:

1. **Code on GitHub** (private repos): each MCP server is its own repo
2. **Docs in the vault**: `resources/mcp-servers/` with setup guides per server
3. **Keep shared definitions nonsecret**: store commands, URLs, and environment variable names in the vault.
4. **Credentials stay local**: each team member uses environment variables, Keychain, or a team password manager.
5. **Setup skill**: a `skills/mcp-setup.md` that walks team members through installation

## Design principles

1. **CLAUDE.md is the brain**: concise navigation file, links to everything. When a section grows long, extract it to `context/` and link back.
2. **One truth per file**: no mega-docs, everything cross-referenced.
3. **Context is layered**: org-level at root, client/project folders inherit and override.
4. **Four-file bootstrap**: CLAUDE.md + AGENTS.md + GEMINI.md + README.md. Every tool lands in the same brain.
5. **Memory that learns**: local observations propose corrections, and reviewed learned rules distribute approved policy.
6. **Skills are executable**: not documentation, workflows. The vault does things, not just stores things.
7. **Daily logs with timestamps and attribution**: institutional memory that survives across sessions, people, and tools.
8. **Sessions are active, not passive**: mandatory protocol. Read context first, route knowledge during, log everything at the end.
9. **Context is protected**: approved content cannot be casually overwritten. Contradictions require confirmation.
10. **Start minimal**: only create files you have content for. Grow organically.
11. **Works everywhere**: plain markdown, no tool lock-in.
12. **Shared and local stay separate**: knowledge and portable adapters are shared. Credentials, paths, permissions, notifications, and caches are machine local.

---

## License

MIT. Use it however you want.

---

*Built by [Five One Nine Marketing](https://github.com/accountsFON) for teams who are tired of repeating themselves.*
