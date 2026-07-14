---
name: YYYY-MM-DD-learning-decision
description: Immutable human decision event for one exact learning proposal.
type: learning-decision
schema-version: 2
status: recorded
authority: human-decision
execution-authority: none
decision-id: FPRD-YYYYMMDDTHHMMSSZ-1234abcd
decision-digest: sha256:[64 lowercase hex characters]
authorization-digest: none
proposal-id: FPRP-YYYYMMDD-123456789abc
proposal-digest: sha256:[64 lowercase hex characters]
previous-event-id: none
disposition: hold
decided-by: TODO
decided-date: YYYY-MM-DD
approval-source: TODO
updated: YYYY-MM-DD
---

**Related Files:** [README.md](README.md) · [approval-contract.md](approval-contract.md) · [proposal-template.md](proposal-template.md) · [execution-receipt-template.md](execution-receipt-template.md) · [validation-receipt-template.md](validation-receipt-template.md) · [../../skills/pattern-review.md](../../skills/pattern-review.md)

> Template note: Save one event under `decisions/YYYY-MM/FPRD-YYYYMMDDTHHMMSSZ-[nonce].md` and update these links for the new folder depth. Use the UTC decision timestamp plus a fresh eight character lowercase hexadecimal nonce. Never edit a recorded event. A later decision names it in `previous_event_id`.

# Learning Decision

Schema version 2 decisions bind a human disposition to an immutable exact proposal. They never approve a candidate report directly.

## Canonical decision payload

Use valid JSON. Compute `decision-digest` from the compact UTF 8 JSON form with keys sorted, no extra spaces, and no floating point values.

```json
{
  "schema_version": 2,
  "decision_id": "FPRD-YYYYMMDDTHHMMSSZ-1234abcd",
  "proposal_id": "FPRP-YYYYMMDD-123456789abc",
  "proposal_digest": "sha256:[64 lowercase hex characters]",
  "previous_event_id": "none",
  "disposition": "approve-exact",
  "scope_lock": "The exact proposal scope.",
  "constraints": [
    "Any additional limit stated by the human reviewer."
  ],
  "prohibited_expansion": [
    "The proposal does not authorize any other edit."
  ],
  "decided_by": "Named human reviewer",
  "decided_at": "YYYY-MM-DDTHH:MM:SSZ",
  "approval_source": "Safe task, message, or meeting receipt.",
  "expires_date": "YYYY-MM-DD",
  "replacement_proposal": "none"
}
```

The system must resolve the `FPRP` ID, recompute its full proposal digest, verify the ID suffix, and place that digest in this payload. The human does not need to type or copy the digest.

## Authorization digest

For `approve-exact`, compute:

```text
SHA256("pattern-review-approval-v1\n" + proposal-digest + "\n" + decision-digest)
```

Store the result as `sha256:` followed by 64 lowercase hexadecimal characters in `authorization-digest`, then set `execution-authority: exact`.

Every other disposition uses `authorization-digest: none` and `execution-authority: none`.

`narrow` and `request-details` require `replacement_proposal: pending` or a distinct existing `FPRP` ID whose `revision_of` names the source proposal. Every other disposition requires `replacement_proposal: none`. An `approve-exact` expiration date cannot precede its decision date.

## Decision effect

- `hold` keeps the unchanged proposal available for a later decision.
- `reject` ends the proposal with no authority.
- `narrow` ends the proposal and requires a new narrower proposal.
- `request-details` ends the proposal and requires a new proposal containing the added detail.
- `approve-exact` grants one use authority for that proposal digest only.
- `revoke` removes an unused exact approval before execution begins.

A root event may be `hold`, `reject`, `narrow`, `request-details`, or `approve-exact`, never `revoke`. `hold` may move to any disposition except `revoke`. `approve-exact` may move only to `revoke`. `reject`, `narrow`, `request-details`, and `revoke` are terminal. Reapproval after revocation requires a new revised proposal.

## Scope lock

Restate the narrowest decided scope and all added constraints.

## Prohibited expansion

State what the decision does not authorize. Broad candidate approval, batch approval, inferred cleanup, and a different proposal revision are invalid.

## Next action

Name the replacement proposal, exact execution, or review step. A decision record never performs the change itself.
