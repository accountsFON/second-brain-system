---
name: brain-check
description: Vault self-audit. Checks structure, staleness, cross-references, learning governance, and intake backlog.
type: skill
updated: YYYY-MM-DD
---

**Related Files:** [README.md](README.md) · [pattern-review.md](pattern-review.md) · [../context/vault-manifest.md](../context/vault-manifest.md) · [../resources/learning-library/README.md](../resources/learning-library/README.md) · [../CLAUDE.md](../CLAUDE.md)

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

If the AI tool has a persistent memory system, compare it against `context/learned-rules.md`. Route possible differences to `skills/pattern-review.md` as noncanonical candidates. Do not treat private memory as evidence that a shared rule has changed.

### 9. Learning library integrity

If `resources/learning-library/` exists:

- Confirm every candidate report says `canonical: false` and `authority: none`
- Flag duplicate fingerprints or substantively identical claims across candidate reports
- Confirm candidates are not linked from session bootstrap files as instructions
- Confirm each promoted rubric or exemplar links to a human decision record
- Confirm every promotion decision names a reviewer, approval date, scope, destination, and next review date
- Flag candidate reports past their `review-by` date
- Flag approved rubrics or exemplars past their `review-on` date
- Confirm the recurring Pattern Review has one designated writer
- During shadow mode, flag any canonical change attributed to a recurring candidate scan
- Flag duplicate or conflicting guidance across learned rules, skills, rubrics, and exemplars

This is an integrity check only. Use `skills/pattern-review.md` for discovery and promotion review.

## Output

A summary report with:
- Issues found, grouped by check
- Severity (broken link vs. cosmetic staleness)
- Suggested fixes for each issue

Do NOT auto-fix. Present findings and let the user decide what to act on.
