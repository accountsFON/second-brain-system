# AGENTS.md

You are working in the source repository for the Second Brain System. This repository publishes a generic vault builder, operator guide, and starter templates. It is not itself a generated organization vault.

Read [README.md](./README.md), then inspect [second-brain-initiate.md](./second-brain-initiate.md), [second-brain-operator.md](./second-brain-operator.md), and only the relevant files under [template/](./template/).

## Quick links for any agent

- **Repository tour:** [README.md](./README.md)
- **Vault builder:** [second-brain-initiate.md](./second-brain-initiate.md)
- **Agent operator guide:** [second-brain-operator.md](./second-brain-operator.md)
- **Starter templates:** [template/](./template/)
- **Platform boundary template:** [template/resources/agent-platform/README.md](./template/resources/agent-platform/README.md)

## Hard rules every agent must follow

1. Keep every published pattern organization neutral. Never commit customer data, credentials, private endpoints, or operator paths.
2. Preserve one canonical workflow source. Platform adapters remain thin.
3. Keep shared project files portable and nonsecret. Machine state and credentials stay local.
4. Update the builder prompt, operator guide, README, and templates together when their contract changes.
5. Verify links, diffs, and secret patterns before release.

## Skills and machine setup

Generated vaults keep canonical workflows in `skills/`. Codex uses `.agents/skills/vault-bridge/SKILL.md` to route named workflows back to that library.

Shared project configuration may contain only portable, nonsecret settings. Credentials, absolute paths, permissions, and personal notifications belong in each operator's home configuration. In a cloud synced vault, configure Codex locally to recognize `.codex` as a project root marker.

## What this vault is

The generated vault, not this source repository, contains the organization specific `CLAUDE.md`, context, and daily logs. Do not invent organization content in this repository.
