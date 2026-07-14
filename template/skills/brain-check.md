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
- Confirm candidates were never approved directly
- Confirm every issued proposal has a valid canonical JSON digest and matching `FPRP` ID, fully enumerated operations, before and after hashes, exact content, trusted validators, and prohibited expansion
- Confirm every proposal source candidate resolves to a real candidate report entry with matching path, anchor, and fingerprint
- Confirm candidate shaped headings that do not exactly match the candidate heading contract are reported as malformed
- Confirm schema version 2 proposals use full content only and each after hash matches the exact UTF 8 content bytes
- Confirm proposal actions are only create or replace, with absent before state for create and a full digest for replace
- Confirm proposal and execution targets remain within the vault after resolving existing symlinks
- Confirm every `FPRD` decision is append only, uses a UTC timestamp plus eight character nonce ID, has a valid decision digest, and names a human reviewer and date
- Confirm only `approve-exact` decisions have exact execution authority and a valid authorization digest bound to the verified `FPRP` and decision digests
- Confirm every execution proposal ID exactly equals its decision proposal ID, independently of digest equality
- Confirm all other decision dispositions have no execution authority and `authorization-digest: none`
- Confirm decision event chains follow the allowed root and transition table, replacement proposal rules, and expiry rules, and that a revoke blocks unused authority
- Confirm no more than one `FPRE` receipt consumes each authorization digest
- Confirm every blocked receipt has `approval_consumed: false` and no changed paths
- Confirm every attempt ID uses the authorization digest prefix and a unique two digit sequence
- Confirm the execution ID date, `executed-date`, and parent month match `completed_at`
- Confirm every retry repeated proposal, decision, decision time, revocation, expiration, before hash, and prior consumption checks
- Confirm attempt times are nondecreasing and do not overlap
- Confirm changed paths use before, expected after, and observed after hashes with correct executed, partial, and rolled back semantics
- Confirm every completed promotion has a passing `FPRV` receipt whose ID binds the execution receipt digest and whose validator coverage and live hashes match the proposal
- Confirm validation never predates execution completion, successful path histories are continuous, and current live bytes match only the latest successful validated state for each path
- Confirm validation times are nondecreasing and any passing receipt is final
- Confirm every `FPRP`, `FPRD`, `FPRE`, and `FPRV` record file is contained by the vault and has no symlink component
- Flag candidate reports past their `review-by` date
- Flag approved rubrics or exemplars past their `review-on` date
- Confirm the recurring Pattern Review has one designated writer
- During shadow mode, flag any canonical change attributed to a recurring candidate scan
- Flag duplicate or conflicting guidance across learned rules, skills, rubrics, and exemplars

When the repository validator is available, run:

```bash
python3 resources/learning-library/validate-pattern-review.py --vault /path/to/vault
```

Treat validator failure as an integrity finding. It does not replace human review of the pattern itself.

This is an integrity check only. Use `skills/pattern-review.md` for discovery and promotion review.

## Output

A summary report with:
- Issues found, grouped by check
- Severity (broken link vs. cosmetic staleness)
- Suggested fixes for each issue

Do NOT auto-fix. Present findings and let the user decide what to act on.
