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

## MCP configuration

- Treat every AI client as a separate configuration target. Claude private configuration does not automatically transfer to Codex.
- Keep shared MCP files portable and free of literal credentials.
- Prefer hosted OAuth when supported.
- Retrieve static credentials from an operating system credential store at process start and pass them through the child environment.
- Never place a raw credential in a command argument.
- Inventory with a redacted audit that prints names, scopes, field names, and placement counts, never commands, arguments, headers, or values.

## Optional lifecycle adapters

Lifecycle hooks are platform adapters, not the source of truth. When a team adds logging or notification automation:

1. Normalize platform events into a neutral event schema.
2. Store session state outside the synced vault.
3. On the first observed event, record the current log baseline before looking for additions. Do this even when the platform missed its normal session start event.
4. Build a deterministic event identifier from stable content such as vault identifier, log path, section anchor, and content hash.
5. Commit local state and release local locks before any network request.
6. Give each machine a separate credential. Keep the raw value in an operating system credential store or approved password manager.
7. When central authentication is required, store only a high entropy token hash, bind it to the registered person and machine, and support individual revocation.
8. Use a central idempotency store before several machines can deliver the same notification.
9. Start in shadow mode with no production destination configured.

Before live delivery, prove that a large historical log emits zero new events, one new section emits once, an identical retry emits none, concurrent copies produce one central record, and one machine credential cannot submit for another identity.
