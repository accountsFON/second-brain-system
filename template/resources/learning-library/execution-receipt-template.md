---
name: YYYY-MM-DD-learning-execution
description: Immutable terminal receipt for one exact learning proposal execution attempt.
type: learning-execution
schema-version: 2
status: blocked
authority: none
execution-id: FPRE-YYYYMMDD-123456789abc-01
proposal-id: FPRP-YYYYMMDD-123456789abc
proposal-digest: sha256:[64 lowercase hex characters]
decision-id: FPRD-YYYYMMDDTHHMMSSZ-1234abcd
decision-digest: sha256:[64 lowercase hex characters]
authorization-digest: sha256:[64 lowercase hex characters]
receipt-digest: sha256:[64 lowercase hex characters]
executed-date: YYYY-MM-DD
updated: YYYY-MM-DD
---

**Related Files:** [README.md](README.md) · [approval-contract.md](approval-contract.md) · [proposal-template.md](proposal-template.md) · [decision-template.md](decision-template.md) · [validation-receipt-template.md](validation-receipt-template.md) · [../../skills/pattern-review.md](../../skills/pattern-review.md)

> Template note: Save one terminal attempt receipt under `executions/YYYY-MM/FPRE-YYYYMMDD-[authorization-digest-prefix]-NN.md` and update these links for the new folder depth. The 12 character segment is the first 12 hexadecimal characters of the authorization digest. `NN` is the next two digit attempt number for that authorization. The record is immutable.

# Learning Execution Receipt

Write one receipt after an execution attempt reaches a terminal result. Queue and progress events may live elsewhere, but this record preserves the final safe evidence.

## Execution receipt payload

Use valid JSON. Compute `receipt-digest` from the compact UTF 8 JSON form with keys sorted, no extra spaces, and no floating point values.

```json
{
  "schema_version": 2,
  "execution_id": "FPRE-YYYYMMDD-123456789abc-01",
  "proposal_id": "FPRP-YYYYMMDD-123456789abc",
  "proposal_digest": "sha256:[64 lowercase hex characters]",
  "decision_id": "FPRD-YYYYMMDDTHHMMSSZ-1234abcd",
  "decision_digest": "sha256:[64 lowercase hex characters]",
  "authorization_digest": "sha256:[64 lowercase hex characters]",
  "result": "blocked",
  "approval_consumed": false,
  "started_at": "YYYY-MM-DDTHH:MM:SSZ",
  "completed_at": "YYYY-MM-DDTHH:MM:SSZ",
  "task_receipt": {
    "system": "safe execution coordinator",
    "task_id": "safe task identifier",
    "run_ids": []
  },
  "changed_paths": []
}
```

## Required preflight on every attempt

Before any write, including after an earlier blocked attempt, recheck:

- Proposal ID and full proposal digest
- Decision ID and full decision digest
- Exact equality between this proposal ID and the proposal ID bound by the decision, even if payload digests match
- Recomputed authorization digest
- `approve-exact` disposition and exact execution authority
- No later `revoke` event
- Authorization expiration
- Every operation before hash
- Every operation path still resolves within the vault root after following existing symlinks
- No prior consumed execution for the authorization digest

## One use behavior

Every nonblocked `changed_paths` item uses this shape:

```json
{
  "path": "vault/relative/path.md",
  "before_sha256": "absent or sha256:[64 lowercase hex characters]",
  "expected_after_sha256": "sha256:[64 lowercase hex characters]",
  "observed_after_sha256": "sha256:[64 lowercase hex characters]"
}
```

- `blocked` before any write uses `approval_consumed: false` and an empty `changed_paths` array.
- Multiple immutable blocked receipts are allowed when each attempt has a new sequence number and reruns every preflight check.
- `executed`, `partial`, and `rolled-back` use `approval_consumed: true`.
- `executed` lists every approved path, and every observed after hash equals the expected proposal hash.
- `partial` lists every affected approved path. Its observed value may be a digest, `absent`, or `unknown` when readback cannot establish state.
- `rolled-back` lists every affected approved path, and every observed after value equals its proposal before hash, including `absent` for a rolled back creation.
- Duplicate changed paths are invalid.
- At most one receipt may use `approval_consumed: true` for an authorization digest.
- After a consumed receipt exists, no later attempt is allowed.
- An uncertain write is `partial`, never a silent retry.
- The execution ID date and `executed-date` come from `completed_at`.
- Attempt times are nondecreasing, and attempts do not overlap.

## Safe result summary

State what happened, who executed it, and whether any write occurred. Do not include credentials, private configuration, or raw sensitive output.
