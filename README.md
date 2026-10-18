# Second Brain System

Build a shared second brain for your whole organization out of plain markdown files. One prompt asks you 14 questions and builds the vault, a session guide keeps every AI tool following the same rules, and the vault keeps growing as your team works.

Built for agencies, startups, consultancies, solo operators, and any team tired of explaining the same context to AI tools over and over.

## Features

- **One prompt builds it:** point an AI tool at an empty folder, answer 14 questions in one pass, and it creates the full vault.
- **One brain for every tool:** `CLAUDE.md` is the master file, and `AGENTS.md` and `GEMINI.md` point Codex, Copilot, Cursor, and Gemini CLI back to it.
- **Session protocol:** every session reads the context first, routes new knowledge to the right file, and logs what happened before it ends.
- **Context protection:** approved context files only grow. A contradiction stops the AI until a person confirms the change.
- **Daily logs with attribution:** timestamped entries record who did the work, the verified result, the status, and links to the deliverable.
- **Starter skills:** reusable workflows for loading context, logging, auditing the vault, processing intake, identifying the operator, setting up clients, and reviewing patterns.
- **Governed learning:** Pattern Review turns recurring wins and mistakes into candidates, and only an exact proposal approved by a named person can change shared rules.
- **Plain files:** markdown and folders that open in any editor, with Obsidian as an optional visual layer.

## Compatibility

| Requirement | Details |
|---|---|
| **AI tool** | One that can read files and write to a local folder: Claude Code, Codex, Gemini CLI, Cursor, or GitHub Copilot |
| **Chat apps** | ChatGPT, Claude.ai, and similar chat apps can run the questionnaire and draft each file, and you save the files into the folder yourself |
| **Editor** | Any text editor. [Obsidian](https://obsidian.md) adds graph view and backlinks |
| **Storage** | One shared folder in a single document system, such as Google Drive, Dropbox, OneDrive, or a shared server |
| **Python** | Python 3, standard library only, for the Pattern Review record tool, validator, and tests. The rest of the vault needs nothing installed |
| **Tested on** | The 36 tests in `tests/` and the template validator pass on macOS 26.5.1 with Python 3.10.17 (October 2026) |

A few things to know before you start:

- **Tool coverage:** the builder's final clean session check covers Claude and Codex, from the vault root and from one nested client or project folder. Gemini CLI, Cursor, and Copilot get entry files (`GEMINI.md` and `AGENTS.md`) with no built-in check yet. Reports from those tools are welcome in [Issues](https://github.com/accountsFON/second-brain-system/issues).
- **Windows and Linux:** the vault is plain markdown and should work anywhere. The Python checks have only been run on macOS so far.
- **Cloud folders and Git:** keep any Git checkout outside Google Drive, Dropbox, OneDrive, and iCloud, because cloud sync corrupts Git internals. Clone this repo somewhere local, and build your vault in the shared folder.
- **Codex in a cloud folder:** a cloud synced vault has no `.git`, so each Codex user adds `.codex` to `project_root_markers` in their own `~/.codex/config.toml`. See [Codex Integration](#codex-integration).
- **Pattern Review takes a month to open:** the learning library starts in a 28 day report only shadow mode, and no candidate can change a rule during that window.

## Quick Start

Open your AI tool in an empty folder and tell it:

> Read https://github.com/accountsFON/second-brain-system and follow the instructions in `second-brain-initiate.md` to build me a second brain vault in this folder.

The AI reads the builder prompt, asks you 14 questions about your organization, and builds the vault. It also copies the learning library files from this repo, so the tool needs to reach the repo by URL or a local clone.

**Prefer to paste it yourself?** Clone the repo to a local folder outside any cloud drive:

```bash
git clone https://github.com/accountsFON/second-brain-system.git
```

Open [second-brain-initiate.md](second-brain-initiate.md), copy everything below the line that says **Paste everything below this line into your AI assistant**, and paste it into your AI tool while it points at the empty vault folder. Give the tool read access to the clone so it can copy the files under `template/resources/learning-library/`.

## Use It

1. Create an empty folder in the document system your team already shares.
2. Open your AI tool with that folder as its working directory.
3. Give it the Quick Start instruction above, or paste the builder prompt.
4. Answer the 14 questions in one pass: six about the organization, four about clients or projects, and four about workflow. Question 11 names the one person or agent that writes scheduled Pattern Review reports.
5. Let it build. When it finishes, it gives you a tree of every file, a `CLAUDE.md` walkthrough, steps for adding a client, a team orientation guide, a ranked list of what to fill in next, and the Pattern Review setup.
6. Share the folder with your team. Everyone starts at `CLAUDE.md`.
7. At the start of each AI session, load [second-brain-operator.md](second-brain-operator.md) by pasting it or pointing the tool at it. The session reads context first and logs its work before it ends.

## What It Builds

```
your-vault/
├── CLAUDE.md                  # The brain: navigation, rules, org identity
├── AGENTS.md                  # Entry file for Codex, Copilot, and Cursor
├── GEMINI.md                  # Entry file for Gemini CLI
├── README.md                  # Tour for people opening the folder
├── .codex/config.toml         # Portable Codex project settings
├── .agents/skills/            # Thin Codex bridge to the skills folder
├── .claude/
│   ├── commands/              # Slash command wrappers that point to skills/
│   └── memory/MEMORY.md       # Local observation index for Claude Code
├── context/
│   ├── soul.md                # Identity, voice, and values
│   ├── vault-manifest.md      # Master index of everything in the vault
│   ├── learned-rules.md       # Shared rules every AI tool follows
│   └── ...                    # org-profile, team, services, tools, brand, voice,
│                              # processes, and client-roster, once you have content
├── skills/                    # Shared workflows (listed below)
├── clients/                   # One folder per client
├── projects/                  # Internal projects
├── _client-template/          # Copy for each new client
├── templates/                 # Meeting notes, decision records, briefs
├── resources/
│   ├── assets/                # Logos and brand files
│   ├── machines/              # Operator and machine identity registry
│   ├── agent-platform/        # Shared and local configuration boundary
│   ├── archive/               # Completed work and processed intake
│   └── learning-library/      # Pattern Review templates, record tool, validator
├── Intake/                    # Drop raw docs here for processing
└── logs/                      # Daily logs and the meeting index
```

The builder only creates context files you gave it content for, plus three it always creates: `soul.md`, `vault-manifest.md`, and `learned-rules.md`. Missing details become `> TODO:` placeholders.

## Starter Skills

| Skill | What it does |
|---|---|
| **context-loader** | Reads the brain file, the latest log, and client context at session start |
| **daily-log** | Appends today's daily log and any client or project log with verified outcomes, status, next steps, and result links |
| **brain-check** | Audits structure, stale dates, broken links, manifest drift, intake backlog, and learning governance |
| **pattern-review** | Finds recurring patterns, writes candidate reports, and runs the exact proposal, decision, execution, and validation chain |
| **intake-processor** | Reads a raw doc from `Intake/`, routes what matters to the right files, and archives the original |
| **identify-user** | Resolves who is operating the session by matching hostname and OS username against `resources/machines/` |
| **new-client-setup** | Copies the client template, asks setup questions, fills in the first files, and registers the client in the roster |

The builder adds skills that fit your work, like a campaign brief skill for a marketing team or a sprint planning skill for a dev shop.

## Session Protocol and Context Protection

The operator guide gives every session three phases:

- **Session start:** read `CLAUDE.md`, `context/learned-rules.md`, the latest daily log, and the client or project context, then confirm the context is loaded before producing work.
- **During the session:** route new knowledge to its file, add `**Related Files:**` links, register new files in the manifest, and use `> TODO:` for anything missing.
- **Session end:** append the daily log and any scoped log, update status columns and `updated:` dates, and flag unfinished work.

Files in `context/` folders are protected. The AI adds to them, makes targeted edits only, logs every change, and stops to quote the existing rule when something new contradicts it. Routine factual log entries are preauthorized when the operator's identity is resolved, existing content stays untouched, and nothing sensitive is included.

## Pattern Review

Pattern Review is the vault's learning loop, and it is built so the vault can't promote its own ideas. The learning library holds four kinds of guidance:

- **Hard rules:** fixed boundaries and deterministic failures.
- **Rubrics:** guidance for quality calls that depend on context.
- **Approved exemplars:** annotated examples with stated limits.
- **Candidate patterns:** unapproved observations waiting for review.

A recurring scan finds positive and negative patterns across finished work and writes them as candidates, with evidence, counterexamples, confidence, scope, and a proposed destination. One designated writer runs the scheduled report. Repeated output from the same agent, prompt, artifact, or project iteration counts as one evidence family, and broad promotion normally needs three independent occurrences across at least two projects or contexts.

The first 28 days are report only shadow mode. After that, a named person approves an immutable `FPRP` exact proposal. The system recomputes the proposal's canonical JSON digest and records a bound `FPRD` decision, so the person never types a hash.

An `approve-exact` decision authorizes one execution, recorded in an `FPRE` receipt. The promotion is complete once a passing `FPRV` validation receipt covers every trusted validator and reported hash. The full contract lives in [approval-contract.md](template/resources/learning-library/approval-contract.md).

The tradeoff is ceremony. Promotion takes several records and a human decision, which is slower than editing a rules file by hand. In exchange, every change to shared guidance traces back to evidence and a named approver.

## Obsidian

Open the vault folder in [Obsidian](https://obsidian.md) with **Open folder as vault** for a visual layer:

- **Graph View:** see how every file connects.
- **Backlinks:** see everything that references the file you're reading.
- **Quick Search:** find anything across the vault.
- **Daily Notes:** maps onto the `logs/` folder.

Standard markdown links stay the primary format so every tool can follow them. Obsidian `[[wikilinks]]` can be added alongside them as an extra.

## Live Sync for People and Server Agents

Pick one document system as the live source of truth. People can use the provider's desktop client, and an always on server can use a supported direct mount or sync client for the same folder. Everyone then reads and writes the same live files.

For version history in GitHub, copy the live vault into a separate checkout outside the cloud folder with a one way snapshot job, and give that repo a private remote. Never copy the checkout back into the live vault, and never run two bidirectional sync engines against the same files. Dependency trees and build caches (`node_modules/`, `__pycache__/`) stay out of the vault and out of the snapshot. When the sync client makes a conflict copy, merge the missing content into the canonical file and archive the copy.

## Claude Code Integration

Every skill can run as a slash command, like `/daily-log` or `/brain-check`, through thin wrappers the builder creates in `.claude/commands/`. Each wrapper points to its file in `skills/`, which stays the single source of truth. Claude Code also reads `CLAUDE.md` automatically when it opens the vault.

To add a skill, create the `.md` file in `skills/`, then add a wrapper in `.claude/commands/` containing:

```
Read and execute the skill instructions in skills/[name].md

Do exactly what the skill file says. Do not summarize the skill. Run it.
```

`.claude/memory/` can hold Claude's observations across sessions. Reusable learning from memory enters Pattern Review as a candidate, and it reaches `context/learned-rules.md` only after the full approval chain completes.

## Codex Integration

Codex reads `AGENTS.md` for instructions and [.agents/skills/vault-bridge/SKILL.md](template/.agents/skills/vault-bridge/SKILL.md) for shared workflows. The bridge routes back to `skills/`, so Claude and Codex run the same canonical instructions.

For a cloud synced vault, each operator adds this to their own `~/.codex/config.toml` and restarts Codex:

```toml
project_root_markers = [".git", ".codex"]
```

The shared [.codex/config.toml](template/.codex/config.toml) holds portable settings only. Credentials, absolute paths, permissions, notifications, and telemetry commands stay in each person's home configuration.

## MCP Servers

For teams that connect outside tools, the vault holds the setup guide: what each connector does, who owns it, how each AI tool connects, how an authorized person signs in, and how to verify it.

- **Order of preference:** an official provider hosted MCP first, a company hosted MCP for custom shared workflows, and a local MCP when it needs that computer's files or apps.
- **Credentials:** raw credentials and OAuth sessions stay outside the vault and out of command arguments.
- **Audits:** report server names, scopes, field names, and placement counts. Printing a full MCP config or running a list command can echo stored secrets.

## How It Works

[second-brain-initiate.md](second-brain-initiate.md) is the builder. Its top section explains how to use it, and everything below the paste line is the prompt: the 14 questions, the folder spec, the file conventions, and the Phase 3 verification list. [second-brain-operator.md](second-brain-operator.md) is the session guide, covering orientation, the rules for finding and adding information, context protection, logging, Pattern Review handling, and the mandatory session end.

The [template/](template/) folder holds starter versions of the files the builder generates, including [learned-rules.md](template/context/learned-rules.md), [vault-manifest.md](template/context/vault-manifest.md), the [starter skills](template/skills/), and the [agent platform boundary](template/resources/agent-platform/README.md). Pattern Review records are built by [pattern_review_core.py](template/resources/learning-library/pattern_review_core.py), a shared canonical JSON module. [pattern-review-records.py](template/resources/learning-library/pattern-review-records.py) creates or verifies record envelopes, prints by default, and writes only to an explicit `--output` path that it refuses to overwrite. [validate-pattern-review.py](template/resources/learning-library/validate-pattern-review.py) checks the templates or a live vault, and [tests/test_pattern_review_validator.py](tests/test_pattern_review_validator.py) covers the validator.

## Run the Checks

From the repo root:

```bash
python3 template/resources/learning-library/pattern-review-records.py --help
python3 template/resources/learning-library/validate-pattern-review.py --templates .
python3 -m unittest discover -s tests -v
```

Inside a generated vault, validate its records with:

```bash
python3 resources/learning-library/validate-pattern-review.py --vault .
```

See [CHANGELOG.md](CHANGELOG.md) for what changed and when.

```
second-brain-system/
├── second-brain-initiate.md   builder prompt, run once
├── second-brain-operator.md   session guide, load every session
├── AGENTS.md                  contributor rules for repo agents
├── GEMINI.md                  Gemini CLI entry, points to AGENTS.md
├── template/                  starter files the builder copies from
│   ├── .agents/ .claude/ .codex/
│   ├── context/               soul, manifest, learned rules
│   ├── logs/                  sample daily log
│   ├── resources/             agent platform, learning library, machines
│   └── skills/                starter skills
├── tests/                     Pattern Review validator tests
├── CHANGELOG.md
├── LICENSE
└── README.md
```

## Design Principles

1. **`CLAUDE.md` is the brain:** a concise navigation file that links to everything. Long sections move to `context/`.
2. **One truth per file:** every file owns one topic and links to related files.
3. **Layered context:** org context at the root, and client or project folders inherit and override it.
4. **Four file bootstrap:** `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, and `README.md` send every tool and person to the same brain.
5. **Memory that learns:** local observations propose corrections, and reviewed learned rules carry approved policy.
6. **Executable skills:** skills are workflows the AI runs.
7. **Logs with timestamps, attribution, outcomes, and links:** memory that survives across sessions, people, and tools.
8. **Active sessions:** read first, route knowledge during, log at the end.
9. **Protected context:** approved content only changes with confirmation.
10. **Start minimal:** create files when there's content for them.
11. **Shared and local stay separate:** knowledge and portable adapters are shared, and credentials, paths, permissions, notifications, and caches stay on each machine.
12. **Evidence based completion:** every capability and operator machine gets an explicit pass gate, and missing evidence stays pending.
13. **One live transport:** people and agents share one live vault through supported clients or mounts, and Git receives only a one way recovery snapshot.
14. **Evidence proposes, people authorize exact changes:** candidates start in shadow mode, and promotion needs bound execution and validation proof.

## Made by Five One Nine Marketing

Second Brain System was built by **Caleb Cody**, founder and CEO of [Five One Nine Marketing](https://www.fonmarketing.com). Five One Nine is a growth partner for businesses that want a clear marketing strategy, the systems to run it, and AI built into how the work gets done. We run our own shared vault on this system, and we build tools like this in-house so a small team can punch well above its weight.

**The team:** Caleb Cody, Founder and CEO · Mollie Huebner, Operations Manager and Creative Director · Julio Aleman, Lead Developer and AI Engineer

**From a client, Zach Goodfellow:**

> "You'll have a hard time finding people more passionate about helping you build your business than Five One Nine."

Your strategy. Your system. Your growth partner. **[Let's talk](https://www.fonmarketing.com/contact)**

## License

[MIT](LICENSE). Free to use, change, and share.
