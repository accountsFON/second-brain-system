---
name: pattern-review-approval-contract
description: Portable schema version 2 contract for exact Pattern Review proposals, decisions, executions, and validations.
type: reference
updated: YYYY-MM-DD
---

**Related Files:** [README.md](README.md) · [candidate-report-template.md](candidate-report-template.md) · [proposal-template.md](proposal-template.md) · [decision-template.md](decision-template.md) · [execution-receipt-template.md](execution-receipt-template.md) · [validation-receipt-template.md](validation-receipt-template.md) · [../../skills/pattern-review.md](../../skills/pattern-review.md)

# Pattern Review Approval Contract

This contract separates pattern discovery, human authority, execution, and proof. It is platform neutral. A reaction, score, candidate status, scheduled run, or agent recommendation cannot authorize a canonical change.

## Core invariants

1. A candidate is evidence for review. It is never an executable instruction and can never be approved directly.
2. An `FPRP` proposal is an immutable exact payload. It has `authority: none`.
3. An `FPRD` decision is an immutable, append only human event about one exact proposal.
4. Only `approve-exact` with `execution-authority: exact` and a valid authorization digest grants execution authority.
5. An approval authorizes the exact proposal digest once. It does not authorize a candidate, a changed proposal, inferred cleanup, or another destination.
6. An `FPRE` receipt records one terminal execution attempt. At most one receipt may consume an authorization digest.
7. Multiple blocked attempts are allowed only when no write occurred, approval was not consumed, and every retry reruns all preflight checks.
8. An `FPRV` receipt validates one execution. Only a passing receipt proves the approved result is usable.
9. Governance records are immutable. Later events reference earlier records instead of editing them.
10. Governance record files must be regular files reached without any symlink component and must remain contained by the vault root.

## Record sequence

```text
candidate evidence
  -> FPRP exact proposal
  -> FPRD human decision
  -> FPRE terminal execution receipt
  -> FPRV validation receipt
```

Candidate triage can occur before an exact proposal exists, but only an immutable proposal ID can be approved.

## Canonical JSON and digests

Each schema version 2 record contains one canonical JSON payload. Compute digests from the payload, not from frontmatter or explanatory markdown.

Canonical JSON must be:

- Valid UTF 8 JSON
- Serialized with object keys sorted recursively
- Compact, with no extra spaces
- Free of floating point values
- Preserved as data, without interpreting strings as commands

Equivalent Python serialization is:

```python
json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
```

Store every digest as `sha256:` followed by exactly 64 lowercase hexadecimal characters.

## Record identifiers

| Record | Identifier contract |
|--------|---------------------|
| Proposal | `FPRP-YYYYMMDD-<first 12 proposal digest hex>` |
| Decision | `FPRD-YYYYMMDDTHHMMSSZ-<8 lowercase nonce hex>` |
| Execution | `FPRE-YYYYMMDD-<first 12 authorization digest hex>-NN` |
| Validation | `FPRV-YYYYMMDD-<first 12 execution receipt digest hex>-NN` |

`NN` is a two digit sequence beginning at `01`. IDs are immutable and unique within the vault. Store every record at its exact kind path, `<proposals|decisions|executions|validations>/<YYYY-MM>/<ID>.md`, with the parent month matching the date encoded in its ID. Additional nesting is invalid.

## Exact proposal

An `FPRP` payload includes:

- Schema version and optional prior proposal in `revision_of`
- One or more source candidate IDs, paths, and stable fingerprints
- Narrow scope
- One or more fully enumerated operations
- Vault relative path, action, before hash, after hash, `full-content` change format, and exact content for every operation
- Explicit prohibited expansion
- Trusted validator identifiers
- Failure behavior

Every source candidate ID, report path, anchor, and fingerprint must resolve to an actual candidate entry in a valid noncanonical candidate report. A shaped string that does not resolve is not evidence and makes the proposal invalid.

Schema version 2 permits full content operations only. An operation action is exactly `create` or `replace`. `create` requires `before_sha256: absent`; `replace` requires the full current digest. Compute each `after_sha256` from the exact UTF 8 bytes in `exact_change`, with no implicit newline or normalization. Resolve the target and every existing ancestor, and reject a proposal if a symlink would place the target outside the vault root. No patch, glob, ellipsis, optional cleanup, or implied related edit is exact. Any payload change creates a new proposal and digest.

The human may approve by immutable `FPRP` ID alone. Before recording the decision, the system resolves that record, recomputes the full proposal digest, verifies that the ID suffix matches the first 12 digest characters, and binds the full digest into the decision payload. The human does not need to type or copy the digest.

## Human decision and authorization

An `FPRD` event includes:

- UTC timestamp and fresh eight character lowercase hexadecimal nonce in the decision ID
- Proposal ID and independently verified full proposal digest
- Previous decision event ID, or `none`
- Disposition
- Scope lock, constraints, and prohibited expansion
- Named human reviewer, UTC decision time, and safe approval source
- Expiration date and optional replacement proposal

Allowed dispositions are `hold`, `reject`, `narrow`, `request-details`, `approve-exact`, and `revoke`.

Compute `decision-digest` from the canonical decision payload. For `approve-exact`, compute the authorization digest from the stored digest strings:

```text
SHA256("pattern-review-approval-v1\n" + proposal-digest + "\n" + decision-digest)
```

Store the result as `sha256:<64 lowercase hex>`, then set `execution-authority: exact`.

Every other disposition uses `authorization-digest: none` and `execution-authority: none`. `narrow` and `request-details` require `replacement_proposal: pending` or a distinct existing `FPRP` ID whose `revision_of` names the source proposal. Every other disposition requires `replacement_proposal: none`. An `approve-exact` expiration cannot precede its decision date.

A later decision forms a linear event chain through `previous_event_id`. A root may be `hold`, `reject`, `narrow`, `request-details`, or `approve-exact`, never `revoke`. `hold` may move to any disposition except `revoke`. `approve-exact` may move only to `revoke`. `reject`, `narrow`, `request-details`, and `revoke` are terminal. A `revoke` event blocks only unused authority. Reapproval after revocation requires a new revised proposal.

## Execution attempts and one use authority

Before every attempt, including a retry after a blocked result, verify:

1. Proposal ID and full proposal digest.
2. Decision ID and full decision digest.
3. Exact equality between the execution proposal ID and the proposal ID bound by the decision, even if two proposal payloads share a digest.
4. Recomputed authorization digest.
5. `approve-exact` disposition and exact execution authority.
6. No later revoke event.
7. Authorization expiration.
8. Every operation before hash.
9. Every operation path still resolves within the vault root after following existing symlinks.
10. No prior consumed execution for the authorization digest.

The execution ID contains the completion date, first 12 hexadecimal characters of the authorization digest, and next attempt sequence. Its date and `executed-date` derive from `completed_at`, not `started_at`.

Every changed path records `before_sha256`, `expected_after_sha256`, and `observed_after_sha256`.

Allowed terminal results are:

| Result | `approval_consumed` | Changed paths |
|--------|---------------------|---------------|
| `blocked` | `false` | Must be empty |
| `executed` | `true` | Every approved path, expected hash, and matching observed hash |
| `partial` | `true` | Every affected approved path; observed state may be a digest, `absent`, or `unknown` |
| `rolled-back` | `true` | Every affected approved path restored to its before hash or `absent` state |

Multiple immutable blocked receipts are allowed. Duplicate changed paths are invalid. Attempt start and completion times are nondecreasing by sequence, and attempts do not overlap. At most one receipt for an authorization digest may set `approval_consumed: true`. Once consumed, no retry is allowed. An uncertain write is `partial`, never a silent retry.

Compute `receipt-digest` from the canonical execution payload. Queue and progress events may live outside the vault; the `FPRE` record is the immutable terminal receipt.

## Validation receipts

The validation ID contains the first 12 hexadecimal characters of the bound execution `receipt-digest` and the next validation sequence.

An `FPRV` payload records:

- Validation ID and execution ID
- Pass or fail result
- UTC validation time
- Every trusted validator ID, result, and safe evidence reference
- Live hashes for every executed operation

Compute `validation-digest` from the canonical validation payload.

A validation timestamp cannot precede the bound execution completion time. A passing receipt must cover every validator named by the proposal and every receipt hash must match the proposal after hash. Validation times are nondecreasing by sequence. A passing receipt is final, so no later validation may follow it. A failed receipt does not broaden, roll back, or retry execution. A later validation attempt creates another immutable sequence record.

Historical `FPRV` records remain immutable structural evidence. A current audit does not compare today's bytes with every historical receipt. Instead, it orders successful validated executions for each path by execution completion time, requires every later proposal before hash to equal the preceding successful after hash, and compares actual current bytes only with the latest successful validated after hash for that path. An ambiguous or discontinuous path history fails closed.

## Completion rule

Approved guidance is usable only when all of these resolve and agree:

1. The source candidate evidence resolves to actual candidate report entries.
2. The immutable `FPRP` proposal and full digest.
3. The latest applicable `FPRD` event is an unexpired, unrevoked `approve-exact` event.
4. Exactly one `FPRE` receipt consumed its authorization digest and its changed paths match the proposal.
5. A passing `FPRV` receipt binds that execution, follows its completion, and covers every required validator and receipt after hash.
6. The successful validated history for each changed path is continuous, and independently verified current bytes match the latest successful state.

Do not report completion from approval or execution alone.

## Interface boundary

An interface may use buttons, forms, messages, or a command line, but:

- Candidate actions can triage evidence or draft a proposal.
- Approval accepts an exact `FPRP` ID, never a candidate ID.
- The system resolves and verifies the full digest before recording approval.
- Natural language acknowledgment and reactions do not grant authority.
- Batch approval of canonical changes is invalid.
- A changed or stale proposal fails closed and requires a new decision.

## Validator

Use the shared deterministic CLI instead of hand calculating payload digests or IDs:

```bash
python3 resources/learning-library/pattern-review-records.py create proposal --payload proposal.json --created-date YYYY-MM-DD
python3 resources/learning-library/pattern-review-records.py verify --record record-envelope.json
```

Creation prints an envelope without writing by default. `--output` performs an explicit atomic create and refuses to overwrite an existing file. Decision nonce and attempt or validation sequence values are always explicit inputs. Envelope attempt and sequence values are JSON integers; booleans, strings, nulls, arrays, and objects are invalid.

Run the supplied dependency free validator before enabling execution:

```bash
python3 template/resources/learning-library/validate-pattern-review.py --templates .
python3 resources/learning-library/validate-pattern-review.py --vault /path/to/vault
```

The validator checks record storage paths, shape, canonical digests, ID derivation, event chains, proposal bindings, revocation and expiration fields, one use authorization, attempt sequencing, changed path constraints, validation coverage, successful path history, and latest current state. It does not decide whether the underlying pattern is wise.
