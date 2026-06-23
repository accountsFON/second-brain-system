---
name: machines-readme
description: Registry of operator-machine pairs for log attribution. One file per person per machine.
type: reference
updated: YYYY-MM-DD
---

# Machine Registry

This folder stores identity records for every operator and machine that writes to the vault. Each record maps a `(hostname, OS username)` pair to a person and machine name.

**How it works:** When a session needs to attribute a log entry, it reads the live hostname and OS username, finds the matching record here, and uses its `Log attribution` string. If no match exists, the `skills/identify-user.md` skill onboards a new record.

**File naming:** `<person-slug>-<machine-slug>.md` (e.g., `caleb-macbook-pro.md`)

**When to skip this:** Single person, single machine vaults where attribution is obvious. The identify-user skill will tell you.
