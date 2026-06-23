---
name: identify-user
description: Resolve who is operating this session for log attribution. Use when the vault is synced across multiple people and computers.
type: skill
updated: YYYY-MM-DD
---

**Related Files:** [README.md](README.md) · [daily-log.md](daily-log.md) · [../CLAUDE.md](../CLAUDE.md) · [../resources/machines/README.md](../resources/machines/README.md)

# Identify User

Resolve the current operator and machine for log attribution. Required in any vault synced across multiple people or computers (Google Drive, Dropbox, OneDrive, iCloud, git).

## The Problem

A synced vault is the same files on every computer. "Who am I?" cannot be stored as one value because every machine would read the same answer. Identity must be resolved at runtime.

## The Rule

**Match on the pair `(hostname + OS username)`. Both must equal the live values for a record to count as a match. Anything else means onboard. Never guess.**

| Situation | What happens |
|---|---|
| Brand new machine | No record matches. Onboard, ask the operator. |
| Machine reassigned (new OS login) | Username differs. Onboard the new operator. |
| Shared machine, several OS accounts | Each account is its own record. Correct attribution per account. |
| Two machines, same hostname, different users | Username distinguishes them. Correct. |
| Identical hostname AND username on two machines | Cannot disambiguate. Stop and ask, then set a unique hostname. |

## When to use

- Setting up the vault on a new computer
- About to write a daily log, decision record, or any attributed entry
- An entry is missing its "Logged by" line
- Two or more people share the vault and entries are ambiguous
- You cannot tell which operator the current session is running as

**Skip when:** single person, single machine, or the platform already records the author (git commits, CMS with logins).

## How to read the live values

| Need | macOS | Linux | Windows (PowerShell) |
|---|---|---|---|
| Hostname | `scutil --get ComputerName` | `hostname` | `$env:COMPUTERNAME` |
| OS username | `whoami` | `whoami` | `$env:USERNAME` |
| OS version | `sw_vers` | `uname -a` | `(Get-CimInstance Win32_OperatingSystem).Caption` |
| Hardware model | `sysctl -n hw.model` | `cat /sys/class/dmi/id/product_name` | `(Get-CimInstance Win32_ComputerSystem).Model` |

On macOS, use `scutil --get ComputerName` (the stable friendly name) for both writing and matching.

## Resolution flow

1. Read the live **hostname** and **OS username**.
2. Scan `resources/machines/*.md` for a record whose `Hostname` and `OS username` fields both equal the live values.
3. **Exactly one match:** use its `Log attribution` string. Done.
4. **No match:** onboard (see below). Do not attribute to any partial match.
5. **More than one match:** stop and ask the operator. Duplicates are a data error.

## Onboarding a new operator and machine

1. Capture automatically: hostname, OS username, OS version, hardware model.
2. Ask the operator (never invent these):
   - "Who is operating this machine?" (gives you `<Person>`)
   - "What should this machine be called in logs?" (suggest a default from the hardware model)
3. Write a record using the template below to `resources/machines/`.
4. Confirm the resolved footer back to the operator.

### Machine record template

Save as `resources/machines/<person-slug>-<machine-slug>.md`:

```markdown
---
name: machine-<person-slug>-<machine-slug>
description: Identity record for <Person>'s <Machine Name>. Created YYYY-MM-DD.
type: reference
updated: YYYY-MM-DD
---

# Machine: <Person> - <Machine Name>

| Field | Value |
|---|---|
| Hostname | <live hostname> |
| OS username | <live username> |
| Operator | <Person> |
| Machine name | <Machine Name> |
| OS | <macOS / Windows / Linux version> |
| Created | YYYY-MM-DD |
| Log attribution | `_Logged by: <Person> - <Machine Name>_` |
```

## Applying attribution

End every attributed entry with the record's footer on its own line:

```
_Logged by: Caleb - Work Laptop_
```

For agent-written entries, keep the agent visible: `_Logged by: Claude (Caleb - Work Laptop)_`.

## Setup in your vault

1. Create `resources/machines/` inside the synced vault.
2. Add one line to your CLAUDE.md rules: "Attribute every log entry. Resolve identity via `skills/identify-user.md` before writing."
3. Wrap as a slash command if your platform supports it (e.g., `.claude/commands/identify-user.md`).

Nothing in this skill hardcodes a person, OS, or path. It works in any vault.
