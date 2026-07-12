---
name: agent-platform
description: Simple boundaries for sharing one knowledge vault across Claude, Codex, and other AI tools.
type: reference
updated: YYYY-MM-DD
---

**Related Files:** [../../AGENTS.md](../../AGENTS.md) · [../../CLAUDE.md](../../CLAUDE.md) · [../../skills/README.md](../../skills/README.md)

# Shared Knowledge Architecture

The vault is one shared brain, not a required automation platform.

## Shared in the vault

- Organization, client, and project knowledge
- Canonical policy and learned rules
- Canonical workflows in `skills/`
- Thin tool adapters
- MCP descriptions and setup instructions
- Attributed logs

## Kept outside the vault

- Credentials and OAuth sessions
- Personal permissions and notifications
- Absolute paths
- Enabled integration choices
- Caches and session state
- Running services

## Skills

Keep each workflow body once in `skills/`. Claude wrappers and the Codex bridge point back to that canonical file.

When a workflow improves, update the canonical skill after user approval. Do not teach only one adapter.

## Shared learning

Private model memory is not shared. After user approval:

1. Put universal corrections in `context/learned-rules.md`.
2. Put workflow improvements in the canonical skill.
3. Put client or project learning in its context file.
4. Record significant work in the attributed daily and applicable scoped logs.

Routine factual log appends are the standing exception to the approval requirement. They are preauthorized when they cover current work, preserve existing content, use resolved identity, and contain no sensitive information. Source of truth changes still require explicit approval.

## Live vault transport

Choose one document system as the live source of truth. Human computers can use its desktop client. Servers can use a supported direct mount or sync client for the same folder.

Keep Git outside every cloud synced folder. If versioned recovery is useful, use a separate checkout that receives one way snapshots from the live vault. Never copy Git back into the live vault, and never run two bidirectional sync engines against the same files.

Before automated writers use the vault, verify both directions, create, edit, rename, delete, restart, cached write recovery, and same file collision behavior. Use the evidence to define a safe writer policy.

## MCP connections

The vault shares the setup guide. Prefer an official provider hosted MCP, use a company hosted MCP for custom shared workflows, and use a local MCP when local access is required.

Claude and Codex may require separate setup and sign in. Keep credentials outside the vault and never place a raw credential in a command argument.
