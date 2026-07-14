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

## The four pillars

### 1. The Brain (CLAUDE.md + cross-tool shims)

One master file that every tool reads first. `AGENTS.md`, `GEMINI.md`, and `README.md` are thin redirects so Claude, Codex, Gemini, Cursor, and humans all land in the same brain. No tool reads a different truth.

### 2. Persistent Memory (learns across sessions)

Two layers working together:
- **Local memory** (tool specific): captures observations and proposes corrections for review.
- **Learned rules** (`context/learned-rules.md`): canonical shared policy. Every AI reads it, and local memory cannot silently override it.

### 3. Executable Skills (the vault does things)

Plain markdown files in `skills/` that encode repeatable workflows. Not documentation, execution. `daily-log`, `brain-check`, `pattern-review`, `intake-processor`, `identify-user`. The vault maintains itself.

### 4. Governed Pattern Review (learns without self promotion)

A recurring scan finds positive and negative patterns across finished work, but writes them only as noncanonical candidates. One designated writer runs the recurring report. The first four weeks are shadow mode. Candidates can never be approved directly. Promotion uses an immutable exact proposal, an append only human decision bound to its digest, one use execution authority, and a passing validation receipt.

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
│   ├── pattern-review.md      # Governed pattern discovery and promotion
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
│   ├── archive/               # Completed work, processed intake
│   └── learning-library/      # Candidates, decisions, exemplars, rubrics
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
- **Mandatory session end**: update daily logs with timestamped outcomes, useful result links, and unfinished work
- **Automatic routine logging**: factual additions to the current daily and applicable client or project logs need no separate approval

### Cross-tool shims — Automatic

`AGENTS.md` and `GEMINI.md` are thin redirect files that point to CLAUDE.md. When Codex opens your vault, it auto-reads `AGENTS.md` and lands in the same brain as Claude. When Gemini CLI opens it, same thing via `GEMINI.md`. Switch tools freely. Same context, same rules.

### Template files — Reference

The `template/` folder contains starter versions of the key files the initiate prompt generates. Use them as reference for what the vault should look like, or copy them directly if you prefer to set up manually instead of using the questionnaire.

## Starter skills (ship with the vault)

| Skill | What it does |
|-------|-------------|
| **context-loader** | Reads the brain file, latest log, and client context. Session-start bootstrap. |
| **daily-log** | Automatically appends today's daily and applicable scoped logs with concise verified outcomes, current status, next steps, and useful result links. Mandatory at session end. |
| **brain-check** | Audits structure, staleness, broken links, manifest drift, intake backlog, and learning governance. |
| **pattern-review** | Finds recurring positive and negative patterns, writes noncanonical candidates, and governs exact proposals, human decisions, executions, and validation proof. |
| **intake-processor** | Reads a raw doc from Intake/, extracts key info, routes it to the right vault files, archives the original. |
| **identify-user** | Resolves who is operating the current session by matching hostname + OS username against a registry. For multi-person or multi-machine vaults. |
| **new-client-setup** | Copies the client template, asks setup questions, populates initial files, registers in the roster. |

## Pattern Review: safe reusable learning

The learning library separates four kinds of guidance:

- **Hard rules** protect nonnegotiable boundaries and deterministic failures.
- **Rubrics** guide context dependent quality decisions.
- **Approved exemplars** calibrate judgment with annotated examples and clear limits.
- **Candidate patterns** hold unapproved observations for review.

Weekly discovery reports include evidence, counterexamples, source independence, outcome signals, confidence, scope, and a proposed destination. Repeated output from the same agent, prompt, artifact, or project iteration counts as one evidence family.

Broad promotion normally requires three independent occurrences across at least two projects or contexts. A human can approve a documented exception, but the recurring scan never approves itself.

The first 28 days are report only shadow mode. After that period, a named human can approve only an immutable `FPRP` exact proposal, never a candidate. The system resolves the proposal ID, recomputes its full canonical JSON digest, and records a bound `FPRD` decision. The human does not need to type the digest.

An `approve-exact` decision creates one use authority. Each terminal attempt gets an immutable `FPRE` receipt. Blocked attempts can retry only when no write occurred and all proposal, exact decision binding, revocation, expiration, before hash, and prior consumption checks run again. At most one execution may consume the authorization. A passing `FPRV` receipt must follow execution completion and cover every trusted validator and reported hash. Later audits preserve historical receipts as structural evidence, enforce continuous successful path history, and compare current bytes only with the latest successful validated state.

The public templates define the vendor neutral schema and include a dependency free validator:

```bash
python3 template/resources/learning-library/pattern-review-records.py --help
python3 template/resources/learning-library/validate-pattern-review.py --templates .
python3 resources/learning-library/validate-pattern-review.py --vault /path/to/vault
python3 -m unittest discover -s tests -v
```

The record CLI deterministically creates or verifies proposal, decision, execution, and validation envelopes. It prints without writing by default. An explicit `--output` uses atomic create and refuses to overwrite, so different agents can share one implementation instead of hand calculating hashes. Attempt and sequence fields must be JSON integers and are never coerced from other types.

Scheduled reports still use one designated writer to prevent duplicate reports and write collisions. Scheduler credentials and machine configuration stay outside the vault.

## Why it works

Most organizational knowledge dies in chat threads, email chains, and someone's head. This system captures it in files that every future session, by any person, with any tool, can read and build on.

- **Start a session**: AI reads the full org context before doing anything
- **Do the work**: AI routes new knowledge to the right files, not just the chat
- **End the session**: daily log captures what happened for whoever comes next
- **Switch tools**: AGENTS.md and GEMINI.md ensure the new tool picks up where the old one left off
- **Learn safely**: corrections and outcomes become candidates first, then humans promote the useful ones into the right canonical layer

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

### Live sync for humans and server agents

Choose one document system as the live source of truth. Human computers can use the provider desktop client. An always on server can use a supported direct mount or sync client for that same folder. Both sides then read and write the same live documents.

Keep Git outside every cloud synced vault. If you want version history in GitHub, copy the live vault into a separate checkout with a one way snapshot job. Never copy that checkout back into the live vault, never place `.git` inside a cloud folder, and never run two bidirectional sync engines against the same files.

## Claude Code Integration

If your team uses Claude Code, the vault automatically provides slash commands for every skill. Type `/daily-log`, `/brain-check`, `/pattern-review`, `/intake-processor`, etc. The commands in `.claude/commands/` are thin one-line wrappers that point to the skill files in `skills/`. One source of truth, no duplication.

The `.claude/memory/` directory can hold Claude observations across sessions. Proposed reusable learning enters Pattern Review as noncanonical evidence. Universal rules reach `context/learned-rules.md` only after the full chain completes: immutable exact proposal, bound human `approve-exact` decision, one use execution, and passing live validation. Other tools then inherit verified policy.

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

The vault is the shared knowledge layer, not a required automation platform. Running services, credentials, personal permissions, notifications, and session state stay outside it.

### MCP Servers (optional, for technical teams)

If your team uses external tools, the vault should share what each connector does, who owns it, how each tool connects, how an authorized person signs in, and how to verify it.

Prefer an official provider hosted MCP. Use a company hosted MCP for custom shared workflows. Use a local MCP when it needs that computer's files or applications. Claude and Codex may require separate one time setup, but the same vault guide can cover both.

Credentials and OAuth sessions stay outside the vault. Never store a raw credential in a shared file or command argument.

Inventory must be redacted by design. Do not tell an agent to print a complete MCP config or run a list command that may echo stored arguments and headers. A safe audit reports only server names, scopes, field names, and placement counts.

## Design principles

1. **CLAUDE.md is the brain**: concise navigation file, links to everything. When a section grows long, extract it to `context/` and link back.
2. **One truth per file**: no mega-docs, everything cross-referenced.
3. **Context is layered**: org-level at root, client/project folders inherit and override.
4. **Four-file bootstrap**: CLAUDE.md + AGENTS.md + GEMINI.md + README.md. Every tool lands in the same brain.
5. **Memory that learns**: local observations propose corrections, and reviewed learned rules distribute approved policy.
6. **Skills are executable**: not documentation, workflows. The vault does things, not just stores things.
7. **Daily logs with timestamps, attribution, outcomes, and useful links**: institutional memory that survives across sessions, people, and tools.
8. **Sessions are active, not passive**: mandatory protocol. Read context first, route knowledge during, log everything at the end.
9. **Context is protected**: approved content cannot be casually overwritten. Contradictions require confirmation.
10. **Start minimal**: only create files you have content for. Grow organically.
11. **Works everywhere**: plain markdown, no tool lock-in.
12. **Shared and local stay separate**: knowledge and portable adapters are shared. Credentials, paths, permissions, notifications, and caches are machine local.
13. **Routine logging is preauthorized**: agents append factual current work to daily and applicable scoped logs automatically. Sensitive content, edits to existing entries, and source of truth changes still require approval.
14. **Completion is evidence based**: every capability and operator machine gets an explicit pass gate. Missing evidence stays pending, and a narrow green test never certifies the full migration.
15. **One live document transport**: humans and agents share one live vault through supported clients or mounts. Git may receive a one way recovery snapshot but never competes as a second writable source.
16. **Evidence proposes, humans authorize exact changes**: recurring Pattern Review reports are noncanonical, use one designated writer, begin with four weeks of shadow mode, never allow candidate approval, and require bound execution and validation proof.

---

## License

MIT. Use it however you want.

---

*Built by [Five One Nine Marketing](https://github.com/accountsFON) for teams who are tired of repeating themselves.*
