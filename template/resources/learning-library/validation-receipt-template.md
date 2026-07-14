---
name: YYYY-MM-DD-learning-validation
description: Immutable validation receipt tied to one learning execution.
type: learning-validation
schema-version: 2
status: failed
authority: none
validation-id: FPRV-YYYYMMDD-123456789abc-01
execution-id: FPRE-YYYYMMDD-123456789abc-01
validation-digest: sha256:[64 lowercase hex characters]
validated-by: TODO
validation-date: YYYY-MM-DD
updated: YYYY-MM-DD
---

**Related Files:** [README.md](README.md) · [approval-contract.md](approval-contract.md) · [proposal-template.md](proposal-template.md) · [decision-template.md](decision-template.md) · [execution-receipt-template.md](execution-receipt-template.md) · [../../skills/pattern-review.md](../../skills/pattern-review.md)

> Template note: Save one receipt under `validations/YYYY-MM/FPRV-YYYYMMDD-[execution-receipt-digest-prefix]-NN.md` and update these links for the new folder depth. The 12 character segment is the first 12 hexadecimal characters of the bound execution `receipt-digest`. `NN` is the next two digit validation sequence for that execution. The record is immutable.

# Learning Validation Receipt

Validation is separate from approval and execution. An exact approval permits the stated operation once. Only a passing validation receipt proves that the approved result is usable.

## Validation receipt payload

Use valid JSON. Compute `validation-digest` from the compact UTF 8 JSON form with keys sorted, no extra spaces, and no floating point values.

```json
{
  "schema_version": 2,
  "validation_id": "FPRV-YYYYMMDD-123456789abc-01",
  "execution_id": "FPRE-YYYYMMDD-123456789abc-01",
  "result": "failed",
  "validated_at": "YYYY-MM-DDTHH:MM:SSZ",
  "validator_results": [
    {
      "id": "trusted-validator-id",
      "result": "failed",
      "evidence": "Safe result or receipt reference."
    }
  ],
  "live_hashes": [
    {
      "path": "vault/relative/path.md",
      "sha256": "sha256:[64 lowercase hex characters]"
    }
  ]
}
```

## Validation conclusion

- `validated_at` is at or after the bound execution `completed_at`.
- A passing receipt covers every validator named by the proposal.
- Every receipt live hash for an executed operation matches the proposal after hash.
- The validation ID prefix matches the bound execution receipt digest.
- A failed receipt does not silently roll back, broaden, or retry the approved operation.
- Additional validation runs create new immutable sequence records. They never edit an earlier receipt.
- Validation times are nondecreasing by sequence. A passing receipt is the final validation attempt.
- Approved guidance is usable only when a passing validation receipt resolves to the exact consumed execution.
- Historical receipts remain structural evidence. A current audit orders successful validated executions by completion time, enforces before to after continuity for each path, and compares actual bytes only with the latest successful validated state.
