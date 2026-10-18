# Changelog

The repo has no version tags yet, so entries are grouped by date. Dates come from the commit history.

## 2026-10-18

- **README:** rebuilt to the Five One Nine public repo standard, with Features, Compatibility, Quick Start, Use It, How It Works, and repo layout sections.
- **Changelog:** added this file.
- **License:** the copyright line now reads Caleb Cody, Five One Nine Marketing. The license stays MIT.

## 2026-08-03

- **Vault hygiene patterns:** dependency trees and build caches stay out of sync and out of snapshot history, and the snapshot repo gets a private remote.
- **Conflict copies:** merge by content into the canonical file, then archive the copy.
- **Archive TTL:** archived files carry an `archived:` date, and binaries go in a dated asset manifest, so a retention limit can be enforced.
- **Client roster:** can be a derived mirror of an outside system of record, stamped with a synced date.
- **Large projects:** dated plans, designs, handoffs, and notes folders with a docs index and changelog.
- **Pushed logs:** internal financials stay out of any log forwarded to a wider audience, and forwarding dedupes on path plus header.

## 2026-07-13 to 2026-07-14

- **Pattern Review:** governed pattern discovery with candidate reports, a 28 day shadow mode, and one designated writer.
- **Approval system:** schema version 2 records (`FPRP`, `FPRD`, `FPRE`, `FPRV`), a shared canonical JSON module, a record tool, a standard library validator, and a test suite.
- **Daily logs:** each entry now states the verified result, status, next step, and direct links to deliverables.

## 2026-07-11

- **Claude and Codex:** a shared vault pattern with a Codex skill bridge, portable project config, and the `project_root_markers` setup for cloud folders.
- **Lifecycle and credentials:** guidance for keeping credentials, paths, and permissions on each machine, plus per machine automation credentials.
- **MCP:** a redacted configuration and inventory pattern.
- **Completion:** evidence based certification for migrations.
- **Architecture:** simpler cross tool setup and one live vault transport.
- **Logging:** routine factual log appends became automatic and preauthorized.

## 2026-06-23

- **Template files:** shipped real starter files in `template/`.
- **Cross tool entry files:** `AGENTS.md` and `GEMINI.md` point every tool to the same brain.
- **Memory:** `.claude/memory/` plus `context/learned-rules.md` as shared policy.
- **Starter skills:** context loader, daily log, brain check, intake processor, identify user, and new client setup, with `soul.md`, the vault manifest, the machine registry, and a sample daily log.

## 2026-04-09 to 2026-04-14

- **Slash commands:** `.claude/commands/` wrappers that point to `skills/`.
- **Attribution:** every log entry names who wrote it.
- **Client template:** added a content library file and a reports folder.
- **MCP setup:** first credential pattern for MCP servers, later replaced by the redacted pattern.
- **Client roster and meeting index:** a canonical roster file, a meeting index, and a line limit for `CLAUDE.md`.

## 2026-04-07

- **Initial release:** `second-brain-initiate.md` builds the vault from a questionnaire, and `second-brain-operator.md` runs every session.
- **Same day updates:** a README that leads with a plain language AI instruction, repo topics, Obsidian guidance, context protection, `clients/` and `projects/` grouping, a mandatory session protocol, and timestamped log entries.
