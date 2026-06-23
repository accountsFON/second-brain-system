---
name: brain-check
description: Vault self-audit. Checks for staleness, broken cross-references, manifest drift, orphaned files, and intake backlog.
type: skill
updated: YYYY-MM-DD
---

**Related Files:** [README.md](README.md) · [../context/vault-manifest.md](../context/vault-manifest.md) · [../CLAUDE.md](../CLAUDE.md)

# Brain Check

Audit the vault's health. Find problems before they compound.

## When to use

- Weekly or biweekly as routine maintenance
- After a burst of new content
- When something feels "off" (can't find a file, context seems stale)
- Before onboarding a new team member

## Checks to run

### 1. Manifest drift

Compare `context/vault-manifest.md` against the actual folder tree.
- Every folder under `clients/`, `projects/` should be registered
- Every file in `context/`, `skills/`, `resources/`, `templates/` should be registered
- Flag anything in the manifest that no longer exists (dead entries)
- Flag anything on disk that is not in the manifest (unregistered)

### 2. Staleness

Scan files with `updated:` or `last-verified:` in frontmatter.
- Flag files not updated in 30+ days that contain metrics, status, or campaign data
- Flag files not updated in 90+ days that contain client context
- Informational only: not every old file is stale. Context that doesn't change (brand, org profile) ages fine.

### 3. Broken cross-references

Scan `**Related Files:**` lines across the vault.
- Check that every linked path resolves to a real file
- Flag broken links with the source file and the dead target

### 4. Orphaned files

Find `.md` files that are:
- Not in the manifest
- Not linked from any other file
- Not in `logs/` (logs are exempt, they link forward not backward)

### 5. Empty TODOs

Find `> TODO:` placeholders across the vault. List them grouped by file. These are promises the vault made to itself.

### 6. Intake backlog

Check `Intake/` for unprocessed files. Flag anything sitting there longer than the SLA defined in CLAUDE.md (default: 7 days).

### 7. Client roster integrity

If the vault has `context/client-roster.md`:
- Every folder in `clients/` should appear in the roster
- Every entry in the roster should have a matching folder
- Flag mismatches in either direction

### 8. Learned rules sync (if applicable)

If the AI tool has a persistent memory system, compare it against `context/learned-rules.md`. Flag rules that exist in memory but not in learned-rules (candidates for promotion) and rules in learned-rules that seem outdated.

## Output

A summary report with:
- Issues found, grouped by check
- Severity (broken link vs. cosmetic staleness)
- Suggested fixes for each issue

Do NOT auto-fix. Present findings and let the user decide what to act on.
