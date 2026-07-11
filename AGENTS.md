# AGENTS.md

You are reading a shared context vault. This file is the entry point for Codex, GitHub Copilot, Cursor agents, and any tool that auto-loads `AGENTS.md`.

**The full operating context lives in [CLAUDE.md](./CLAUDE.md).** Read that file first, every session, before doing any work. The name is historical; the contents are tool-agnostic.

## Quick links for any agent

- **Brain entrypoint:** [CLAUDE.md](./CLAUDE.md)
- **Vault map:** [context/vault-manifest.md](./context/vault-manifest.md)
- **Org identity:** [context/org-profile.md](./context/org-profile.md)
- **Learned rules (must follow):** [context/learned-rules.md](./context/learned-rules.md)
- **Skills library:** [skills/README.md](./skills/README.md)
- **Human-readable tour:** [README.md](./README.md)

## Hard rules every agent must follow

1. **Read CLAUDE.md before doing any work.** Then read `context/learned-rules.md` and the most recent daily log in `logs/`.
2. **Never modify vault data without explicit user confirmation.** Tell the user exactly what you plan to change. Wait for a clear yes. Add, do not replace.
3. **Attribute every log entry.** Include who wrote it. If unsure who the current user is, ask before logging.
4. **Use absolute dates (YYYY-MM-DD).** Convert any relative date in user messages before writing.
5. **Log significant work** to today's daily log at session end.
6. **Follow any additional rules in CLAUDE.md.** The rules there override default model behavior.

## Skills and machine setup

Canonical workflows live in `skills/`. Codex uses `.agents/skills/vault-bridge/SKILL.md` to route named workflows back to that library.

Shared project configuration may contain only portable, nonsecret settings. Credentials, absolute paths, permissions, and personal notifications belong in each operator's home configuration. In a cloud synced vault, configure Codex locally to recognize `.codex` as a project root marker.

## What this vault is

This is an org-wide shared second brain. Every team member and every AI tool reads from it before doing work, so every session starts with full organizational context. If you cannot see `CLAUDE.md`, ask the user where the working directory is. Do not invent context.
