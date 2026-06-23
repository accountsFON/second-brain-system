---
name: skills-readme
description: Index of all shared AI skills in this vault.
type: reference
updated: YYYY-MM-DD
---

# Skills

Reusable AI prompts and workflows the whole team can use. Each skill is a `.md` file with step-by-step instructions any AI tool can follow.

## How to use

**In Claude Code:** Type `/skill-name` as a slash command. The `.claude/commands/` folder has thin wrappers pointing here.

**In any other AI tool:** Copy the skill file contents and paste as a prompt, or say "read and follow `skills/skill-name.md`."

## Available skills

| Skill | Purpose | When to use |
|-------|---------|-------------|
| [context-loader.md](context-loader.md) | Session-start bootstrap | Every session start |
| [daily-log.md](daily-log.md) | Session-end logging | Every session end |
| [brain-check.md](brain-check.md) | Vault self-audit | Weekly, or when something feels off |
| [intake-processor.md](intake-processor.md) | Process raw docs from Intake/ | When new files land in Intake/ |
| [identify-user.md](identify-user.md) | Resolve operator for attribution | Multi-person vaults, new machine setup |
| [new-client-setup.md](new-client-setup.md) | Create a new client folder | When onboarding a new client |

## Adding a new skill

1. Create a `.md` file in this folder with frontmatter (`name`, `description`, `type: skill`, `updated`)
2. Include: what it does, when to use it, step-by-step instructions, expected output
3. Add a `.claude/commands/[name].md` wrapper (one line: `Read and execute the skill instructions in skills/[name].md`)
4. Register the skill in `context/vault-manifest.md`
5. Update this README
