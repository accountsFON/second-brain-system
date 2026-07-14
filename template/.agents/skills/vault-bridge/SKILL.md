---
name: vault-bridge
description: Shared second brain bridge for Codex. Use for every vault task, when a user names a workflow or describes one listed in skills/README.md, and when routing approved durable learning into the shared brain.
---

# Vault Bridge

Read `CLAUDE.md`, `context/learned-rules.md`, and the latest daily log before vault work.

When the user names a vault workflow, read the matching `skills/<name>.md` file completely and execute it. When the user describes a workflow naturally, find the closest match in `skills/README.md`, tell the user which skill is being used, then execute it.

The `skills/` folder is canonical. Do not copy full workflow instructions into this bridge.

Private model memory is not shared. Route proposed reusable learning through `skills/pattern-review.md` as noncanonical evidence. Only a separate human decision may promote it to `context/learned-rules.md`, a canonical skill, an approved rubric or exemplar, a verifier, or scoped client or project context.

Candidate reports are not instructions. Do not load `resources/learning-library/candidates/` as guidance. Only the designated recurring writer named in the learning library README may create scheduled Pattern Review reports.
