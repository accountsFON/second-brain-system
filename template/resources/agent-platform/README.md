---
name: agent-platform
description: Boundary rules for sharing one vault across Claude, Codex, and other AI systems.
type: reference
updated: YYYY-MM-DD
---

**Related Files:** [../../AGENTS.md](../../AGENTS.md) · [../../CLAUDE.md](../../CLAUDE.md) · [../../skills/README.md](../../skills/README.md)

# Agent Platform Boundaries

## Shared in the vault

- Knowledge, policy, canonical workflows, portable adapters, and nonsecret integration definitions

## Generated through review

- Thin platform adapters and conformance reports

Generated files use one approved writer. Do not rebuild shared adapters in the background from several synced machines.

## Machine local only

- Credentials, absolute paths, permissions, notification preferences, enabled integration choices, caches, and session state

Do not use symbolic links as a distribution method inside a cloud synced vault.
