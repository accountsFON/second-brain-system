# Second Brain: Org-Wide Shared Context Vault

## What is this file?

This is a **starter prompt**. Paste it into any AI assistant (Claude, ChatGPT, Gemini, etc.) while pointing at an empty folder, and it will walk you through building a shared "second brain" for your entire organization. No technical setup required. No existing files needed. Just an empty folder and this prompt.

The result: a structured folder of plain `.md` (markdown) files that becomes the single source of truth for your entire team — accessible by any person, any AI tool, any text editor.

---

## How to use this file

1. **Create an empty folder** anywhere your team can access (Google Drive, Dropbox, OneDrive, a shared server, a git repo — anywhere).
2. **Open an AI assistant** (Claude Code, Claude.ai, ChatGPT, Cursor, etc.) and point it at that empty folder as its working directory.
3. **Paste everything below the line** into the AI chat.
4. **Answer the questionnaire** it gives you.
5. **Let it build** the vault structure and starter files.
6. **Share the folder** with your team. Everyone reads CLAUDE.md first.

That's it. The vault grows from there.

---

> **Paste everything below this line into your AI assistant:**

---

# Build Our Shared Context Vault

You are helping me build an **org-wide shared context vault** — a "second brain" for my organization. It will live as a folder of plain markdown (`.md`) files that the entire team can access and contribute to. It works with any AI tool (Claude, ChatGPT, Gemini, Cursor, Copilot, etc.) and any text editor. No vendor lock-in. Just files and folders.

**The current working directory is empty. You will create everything from scratch.**

## What this system is

A structured folder of interconnected `.md` files with a master `CLAUDE.md` at the root. This file is the navigation guide, rulebook, and entry point. Every person or AI session that touches this vault reads CLAUDE.md first and knows exactly where to find and store information.

This is not a wiki you read once. It's a **living operational context layer** — it makes every person and every AI session smarter because they inherit the full organizational picture before starting work. It grows as the team works, and because of clear rules in CLAUDE.md, it stays organized no matter who's contributing.

## Design principles

1. **CLAUDE.md is the brain** — Under 120 lines. Navigation guide + rules + folder map. Links out to everything.
2. **One truth per file** — Each file owns one topic. No mega-docs. Files link to each other.
3. **Cross-referencing is mandatory** — Every file includes a `**Related Files:**` line linking to connected docs. The vault is a web, not a list.
4. **Context is layered** — Org-level context at the root. Each client/project gets a subfolder mirroring the same structure, inheriting org defaults but overriding with specifics.
5. **Daily logs capture institutional memory** — One file per day (org-level and per-client/project). Significant work, decisions, context shared. This is how continuity survives across sessions, team members, and tools.
6. **TODO placeholders, never invented details** — Missing info gets `> TODO:` callouts. Never fabricate.
7. **Start minimal, grow organically** — Only create files we have content for now. The structure expands as context arrives.
8. **Works everywhere** — Plain markdown only. Obsidian wikilinks or other tool-specific syntax are optional enhancements, never required.
9. **Anyone can contribute** — The rules are simple enough that any team member or AI agent can follow them without training.

## Your task

### Phase 1: Questionnaire

Before building anything, ask me a focused questionnaire. I want to start fast — not fill out a 50-question form. Present ALL questions at once so I can answer in one pass.

**Section 1: The Organization (6 questions)**
1. What's the organization's name?
2. Who runs it? (name and title)
3. How many people on the team?
4. What does the org do? (industry, services or products, core offering — a few sentences is fine)
5. Do you have existing brand guidelines? (colors, fonts, logo, voice/tone, key messaging — share whatever you have, or say "not yet")
6. What tools and platforms does the team use day-to-day? (Slack, Google Workspace, Figma, HubSpot, Basecamp, etc.)

**Section 2: Clients / Projects (4 questions)**
7. Does the org serve external clients, manage internal projects, or both?
8. How many active clients/projects right now?
9. List the top 3-5 with a one-liner each (name + what you do for them).
10. Which one should we build out first as the template?

**Section 3: Workflow (4 questions)**
11. Who will use this vault? (list roles — e.g., "3 strategists, 1 designer, 2 devs, 1 ops person")
12. What types of work happen most often? (campaigns, development, design, reporting, strategy, sales, support, etc.)
13. What information do you wish you had at the start of every work session?
14. What falls through the cracks today? (lost context, undocumented decisions, tribal knowledge, handoff gaps, etc.)

### Phase 2: Build the vault

Based on my answers, **create all folders and files directly in the current working directory.** This is a clean start — build everything from scratch.

Create this structure:

#### 1. `CLAUDE.md` — The master file (under 120 lines)

This is the most important file. Include:
- **Vault purpose** — what this vault is and who it's for
- **Org identity** — 3-5 line summary from my answers
- **Folder structure** — documented table showing every top-level folder and its purpose
- **Navigation table** — maps "what info do I need?" to "which file has it?"
- **Rules** — daily logging, cross-referencing, intake processing, how to add new clients/projects
- **Context protection rule** — context files are protected. Add to them, never overwrite. If new info contradicts existing content, stop and ask the user before changing. No bulk rewrites. Log every change.
- **How to use this vault** — step-by-step for any team member or AI starting a session
- **Wiring rule** — every new `.md` file must include `**Related Files:**` links near the top

#### 2. `context/` — Org-level context (only files I provided content for)

| File | Purpose |
|------|---------|
| `org-profile.md` | Who we are, what we do, mission, history |
| `team.md` | Team members, roles, responsibilities, contact info |
| `services.md` | What we offer — services, products, capabilities |
| `tools.md` | Platforms, software, and tools the team uses |
| `brand.md` | Visual identity — colors, fonts, logo rules |
| `voice.md` | Writing style, tone, vocabulary, messaging guidelines |
| `processes.md` | How we work — SOPs, standards, workflows |

Only create files I gave you content for. The rest get created later as context arrives.

#### 3. `skills/` — Shared AI skills and prompts for the whole team

This is a library of reusable prompts and instructions that any team member can invoke in any AI tool. Each skill is a `.md` file with clear instructions an AI can follow.

Create these starter skills based on my answers:

| File | Purpose |
|------|---------|
| `README.md` | How to use skills — explains the folder, how to invoke them, how to add new ones |
| `context-loader.md` | "Read all org context files and summarize what you know before starting work" — the universal session-start skill |
| `intake-processor.md` | "Process a raw document from Intake/ — extract key info and route it to the correct context files" |
| `daily-log.md` | "Create or update today's daily log — summarize significant work, decisions, and context shared this session" |
| `new-client-setup.md` | "Set up a new client/project folder — copy the template, ask the setup questions, populate initial files" |
| `brain-check.md` | "Audit the vault — check for orphaned files, stale dates, empty TODO placeholders, broken links, missing cross-references" |

Each skill file should contain:
- **What it does** (one paragraph)
- **When to use it** (trigger conditions)
- **Instructions** (step-by-step what the AI should do)
- **Output** (what gets created or updated)

Adapt skill names and add more based on the org's actual work (e.g., a "campaign-brief" skill for a marketing org, a "sprint-planning" skill for a dev shop, a "client-report" skill for a consulting firm).

#### 4. `_client-template/` (or `_project-template/`)

A template folder that gets copied for each new client or project. Adapt the naming based on my answers (clients vs. projects vs. accounts).

```
_client-template/
├── README.md              (overview — copy and fill in)
├── context/
│   ├── profile.md         (who they are, what we do for them)
│   ├── brand.md           (their brand specifics)
│   ├── messaging.md       (their messaging, value props, positioning)
│   ├── audience.md        (their target audience, personas, ICP)
│   └── competitors.md     (competitive landscape)
├── campaigns/
│   └── _template.md       (campaign/sprint/project brief template)
├── creative/
│   └── _template.md       (creative/design asset template)
├── deliverables/
│   └── _template.md       (reports, presentations, final outputs template)
├── logs/
│   └── .gitkeep           (daily logs go here — YYYY-MM-DD.md)
└── ops/
    └── _template.md       (process/checklist template)
```

Each `_template.md` should contain a fillable template with sections, placeholders, and instructions — not just an empty file.

#### 5. First client/project folder

Copy the template, rename it for the client/project I chose, and populate it with whatever context I provided.

#### 6. `templates/` — Reusable document templates

| File | Purpose |
|------|---------|
| `meeting-notes.md` | Standard meeting notes template (date, attendees, agenda, decisions, action items) |
| `decision-record.md` | Decision log template (what was decided, why, who, alternatives considered) |
| `campaign-brief.md` | Campaign/project brief template (adapt to org type) |

#### 7. `resources/` — Shared reference material

```
resources/
├── README.md              (what goes here — frameworks, guides, reference docs)
├── assets/                (logos, brand files, shared creative — add files as needed)
│   └── README.md          (asset inventory and naming conventions)
└── archive/               (completed projects, old campaigns — move here, don't delete)
    └── README.md          (archive policy)
```

#### 8. `Intake/` — Raw document drop zone

```
Intake/
└── README.md              (explains: drop any raw doc here, then run the intake-processor skill)
```

#### 9. `logs/` — Org-level daily logs

Create today's log (`logs/YYYY-MM-DD.md`) documenting the vault creation — what was built, what context was captured, what's still TODO.

### Phase 3: Verify and orient

After building everything, give me:

1. **Full tree view** of every file and folder created
2. **CLAUDE.md walkthrough** — highlight each section and what it does
3. **"Add a new client/project" instructions** — exact steps
4. **"Share with the team" guide** — what to tell team members, where they start, the 2-minute orientation
5. **Priority list** — what to fill in next for maximum value (ranked)
6. **Skills inventory** — list every skill created and when to use each one

## File conventions (enforce these in CLAUDE.md)

- **YAML frontmatter** on every `.md` file (except CLAUDE.md itself):
  ```yaml
  ---
  name: descriptive-name
  description: One-line description of what this file contains
  type: context | campaign | creative | ops | log | reference | skill | template
  updated: YYYY-MM-DD
  ---
  ```
- **Date format:** YYYY-MM-DD everywhere
- **File naming:** lowercase-kebab-case.md
- **Folder naming:** lowercase-kebab-case (no spaces)
- **Links:** relative paths from CLAUDE.md (e.g., `[Team](context/team.md)`)
- **Cross-references:** `**Related Files:** [file-a](path/to/file-a.md) · [file-b](path/to/file-b.md)` near the top of every file
- **Missing info:** `> TODO: [describe what's needed]` — never invent or assume
- **Daily logs:** `logs/YYYY-MM-DD.md` — log significant work, decisions, context shared
- **Navigation tables:** Use markdown tables in CLAUDE.md and README files to map files to purpose and status
- **No empty files:** If you don't have content for a file, don't create it. Use the template to show what WILL exist.
- **Status tracking:** Use a Status column in tables (`Active`, `Complete`, `Planned`, `Paused`, `Archived`)

## What makes this system work

The power is in the **rules**, not any single file. When every file links to related files, when every session starts by reading CLAUDE.md, when every decision gets logged, when new context gets routed to the right file instead of buried in a chat thread — the vault becomes a shared memory that compounds over time.

The more the team uses it, the smarter every future session becomes. For any person. With any tool.

## After the vault is built

This prompt builds the vault. For ongoing sessions, use `second-brain-operator.md` — a companion skill that teaches any AI how to behave inside the vault (read context first, follow the rules, log daily, route info to the right files). Load it at the start of every session.

## Visualize it with Obsidian (recommended)

Once the vault is built, open the folder as an [Obsidian](https://obsidian.md) vault for a visual layer on top of your markdown files:

- **Graph View** — see how every file connects to every other file
- **Backlinks** — click any file and see everything that references it
- **Quick Search** — find anything across the vault instantly
- **Daily Notes** — maps perfectly to the `logs/` folder
- **Live Preview** — edit markdown with a clean visual editor

Obsidian is free, works on all platforms, and syncs via any cloud drive. Your vault is already Obsidian-compatible — just open the folder.

---

*Start with Phase 1. Ask me the questionnaire.*
