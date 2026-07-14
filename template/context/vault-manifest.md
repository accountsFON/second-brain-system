---
name: vault-manifest
description: Master index of every file and folder in the vault. The L0 entrypoint for discovery.
type: context
updated: YYYY-MM-DD
---

**Related Files:** [../CLAUDE.md](../CLAUDE.md) · [soul.md](soul.md) · [learned-rules.md](learned-rules.md) · [../skills/pattern-review.md](../skills/pattern-review.md) · [../resources/learning-library/README.md](../resources/learning-library/README.md)

# Vault Manifest

This is the master inventory. Every top-level folder and key file is registered here. If it is not in this manifest, future sessions will not find it.

**Rule:** Any new folder under `clients/`, `projects/`, or any new file in `context/`, `skills/`, `resources/`, or `templates/` must be added here in the same session it is created.

---

## Root files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | The brain. Navigation, rules, org identity. Read first every session. |
| `AGENTS.md` | Bootstrap shim for Codex, Copilot, Cursor. Points to CLAUDE.md. |
| `GEMINI.md` | Bootstrap shim for Gemini CLI. Points to CLAUDE.md. |
| `README.md` | Human-readable tour of the vault. |
| `.codex/config.toml` | Portable, nonsecret Codex project settings. |
| `.agents/skills/vault-bridge/SKILL.md` | Thin Codex router to canonical workflows in `skills/`. |

## Folders

| Folder | Purpose |
|--------|---------|
| `context/` | Org-level identity, voice, team, services, tools, rules |
| `skills/` | Reusable AI skills and prompts |
| `clients/` | One folder per client (if applicable) |
| `projects/` | Internal projects (if applicable) |
| `_client-template/` | Copy this to create a new client. Never edit directly. |
| `templates/` | Reusable document templates (meeting notes, decision records, briefs) |
| `resources/` | Shared assets, archive, reference material |
| `resources/agent-platform/` | Shared, generated, and machine local platform boundaries |
| `resources/learning-library/` | Governed pattern candidates, decisions, approved exemplars, and rubrics |
| `Intake/` | Raw document drop zone. Process with intake-processor skill. |
| `logs/` | Daily logs and meeting transcripts |

## Context files

| File | Purpose |
|------|---------|
| `context/soul.md` | Identity, voice, values. Who the org is and how it sounds. |
| `context/org-profile.md` | What the org does, history, mission |
| `context/team.md` | Team members, roles, contact info |
| `context/services.md` | What the org offers |
| `context/tools.md` | Platforms and software the team uses |
| `context/brand.md` | Visual identity |
| `context/voice.md` | Writing style and tone |
| `context/processes.md` | SOPs and workflows |
| `context/client-roster.md` | Canonical list of all clients |
| `context/learned-rules.md` | Cross-platform rules learned during work |
| `context/vault-manifest.md` | This file |
| `context/vault-isolation-rules.md` | Rules preventing cross-contamination with other vaults |

## Skills

| Skill | Purpose |
|-------|---------|
| `skills/context-loader.md` | Session-start context bootstrap |
| `skills/daily-log.md` | Mandatory session-end logging |
| `skills/brain-check.md` | Vault self-audit (staleness, broken refs, manifest drift) |
| `skills/pattern-review.md` | Evidence based learning discovery and human governed promotion |
| `skills/intake-processor.md` | Process raw docs from Intake/ |
| `skills/new-client-setup.md` | Set up a new client folder from template |
| `skills/identify-user.md` | Resolve who is operating this session for attribution |

## Learning library

| File | Purpose |
|------|---------|
| `resources/learning-library/README.md` | Authority, writer, shadow mode, cadence, and promotion contract |
| `resources/learning-library/candidate-report-template.md` | Noncanonical recurring discovery report template |
| `resources/learning-library/decision-template.md` | Human decision and promotion authorization template |
| `resources/learning-library/exemplar-template.md` | Approved annotated example template |
| `resources/learning-library/rubric-template.md` | Approved scoped quality rubric template |

Create and register `candidates/`, `decisions/`, `exemplars/`, and `rubrics/` when their first files are added. Candidate reports remain noncanonical.

## Clients

> Register each client folder here as it is created.
>
> | Client | Folder | Tier |
> |--------|--------|------|
> | Example Corp | `clients/example-corp/` | full-service |

## Projects

> Register each project folder here as it is created.
