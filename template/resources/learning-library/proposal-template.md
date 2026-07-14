---
name: YYYY-MM-DD-learning-proposal
description: Exact immutable proposal for one bounded learning change.
type: learning-proposal
schema-version: 2
status: proposed
authority: none
proposal-id: FPRP-YYYYMMDD-123456789abc
proposal-digest: sha256:[64 lowercase hex characters]
created-by: TODO
created-date: YYYY-MM-DD
updated: YYYY-MM-DD
---

**Related Files:** [README.md](README.md) · [approval-contract.md](approval-contract.md) · [candidate-report-template.md](candidate-report-template.md) · [decision-template.md](decision-template.md) · [execution-receipt-template.md](execution-receipt-template.md) · [validation-receipt-template.md](validation-receipt-template.md) · [../../skills/pattern-review.md](../../skills/pattern-review.md)

> Template note: Save a completed proposal under `proposals/YYYY-MM/FPRP-YYYYMMDD-[digest-prefix].md` and update these links for the new folder depth. Once issued, the record is immutable. Any change requires a new proposal that names this one in `revision_of`.

# Exact Learning Proposal

> NONCANONICAL: A candidate is evidence, not an approval object. This exact proposal has no authority by itself. A bound `approve-exact` `FPRD` may grant one use execution authority, but the proposed destination does not become canonical until a consumed `FPRE` and final passing `FPRV` verify the live result.

## Canonical approval payload

Use valid JSON. Compute `proposal-digest` from the compact UTF 8 JSON form with keys sorted, no extra spaces, and no floating point values. The digest excludes frontmatter and explanatory prose. The final 12 characters in `proposal-id` are the first 12 hexadecimal characters of the full digest value.

```json
{
  "schema_version": 2,
  "revision_of": "none",
  "source_candidates": [
    {
      "id": "PR-YYYY-MM-DD-NN",
      "path": "resources/learning-library/candidates/YYYY-MM-DD-pattern-review.md#PR-YYYY-MM-DD-NN",
      "fingerprint": "scope::subject::portable-mechanism::outcome"
    }
  ],
  "scope": "The narrowest supported scope.",
  "operations": [
    {
      "action": "create",
      "path": "vault/relative/path.md",
      "before_sha256": "absent",
      "after_sha256": "sha256:[64 lowercase hex characters]",
      "change_format": "full-content",
      "exact_change": "The complete new content."
    }
  ],
  "prohibited_expansion": [
    "A clear statement of what this proposal does not authorize."
  ],
  "validation": [
    "trusted-validator-id",
    "target-hash-readback"
  ],
  "failure_behavior": "Block before a write when a precondition fails."
}
```

## Human summary

Explain the proposed learning, why the evidence supports this scope, and why the enumerated operations are the smallest useful change.

## Preconditions

- Every destination path is vault relative.
- Every source candidate ID, report path, `#candidate-id` fragment, and fingerprint resolves to an actual entry in a valid candidate report.
- `create` requires `before_sha256: absent`. `replace` requires the full digest of the existing content.
- Resolve every destination and its existing ancestors before proposing. Reject a path if any symlink would place it outside the vault root.
- Schema version 2 permits `full-content` operations only.
- Every `after_sha256` is the SHA 256 digest of the exact UTF 8 bytes in `exact_change`, with no implicit newline or normalization.
- Validation entries are trusted validator identifiers, not arbitrary commands supplied by a candidate.
- Candidate reports and prior governance records remain unchanged.
- No glob, inferred cleanup, or unlisted file is authorized.

## Approval question

Ask the designated human to hold, reject, narrow, request details, or approve this exact `FPRP` proposal. The human may approve by immutable proposal ID alone. Never ask whether the source candidate itself is approved.
