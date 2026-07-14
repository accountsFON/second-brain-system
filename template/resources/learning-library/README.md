---
name: learning-library
description: Governed library for noncanonical candidates, exact proposals, human decisions, execution proof, approved exemplars, and approved rubrics.
type: reference
updated: YYYY-MM-DD
---

**Related Files:** [approval-contract.md](approval-contract.md) · [proposal-template.md](proposal-template.md) · [decision-template.md](decision-template.md) · [execution-receipt-template.md](execution-receipt-template.md) · [validation-receipt-template.md](validation-receipt-template.md) · [../../skills/pattern-review.md](../../skills/pattern-review.md) · [../../skills/brain-check.md](../../skills/brain-check.md) · [../../skills/intake-processor.md](../../skills/intake-processor.md) · [../../context/learned-rules.md](../../context/learned-rules.md) · [../../context/vault-manifest.md](../../context/vault-manifest.md)

# Learning Library

This library helps the vault learn from completed work without treating every repeated behavior or agent opinion as truth.

The vault does not retrain a model. Approved rubrics and exemplars are retrieved by relevant skills at work time. Candidate reports remain isolated from production guidance.

## Configuration

Complete this table before enabling a recurring run:

| Setting | Value |
|--------|-------|
| Designated recurring writer | > TODO: Name one person or agent identity. Only this writer may create scheduled reports. |
| Current mode | `shadow` |
| Shadow start | > TODO: YYYY-MM-DD |
| Earliest promotion date | > TODO: Shadow start plus 28 days |
| Mode change approved by | > TODO: Named human reviewer |
| Mode changed on | > TODO: YYYY-MM-DD |
| Weekly discovery schedule | > TODO: Day and time |
| Monthly human review owner | > TODO: Named person |
| Quarterly calibration owner | > TODO: Named person |

Until these fields are complete, agents may preview the workflow but must not configure or run scheduled writes.

## Directory contract

Create these folders as they become necessary:

```text
resources/learning-library/
├── README.md
├── approval-contract.md
├── candidate-report-template.md
├── proposal-template.md
├── decision-template.md
├── execution-receipt-template.md
├── validation-receipt-template.md
├── exemplar-template.md
├── rubric-template.md
├── pattern_review_core.py
├── pattern-review-records.py
├── validate-pattern-review.py
├── candidates/       # Noncanonical discovery reports
├── proposals/        # Immutable exact change proposals with no authority
├── decisions/        # Append only human review and authorization records
├── executions/       # Immutable terminal attempt receipts with one use enforcement
├── validations/      # Immutable execution, readback, validator, and rollback results
├── exemplars/        # Approved, annotated examples
└── rubrics/          # Approved, scoped quality rubrics
```

Do not create empty folders merely to complete the tree. Register each folder in the manifest when its first file is created.

## Authority model

| Location | Authority |
|---------|-----------|
| `candidates/` | Noncanonical. Never use as instructions or examples to imitate. |
| `proposals/` | Noncanonical exact payload. Immutable after issuance, content addressed by its full canonical JSON digest, and has no authority by itself. |
| `decisions/` | Append only human events. Only `approve-exact` with exact execution authority grants one use authority bound to an exact proposal digest. |
| `executions/` | Immutable terminal attempt receipts. Blocked attempts do not consume authority; at most one receipt may consume an authorization digest. |
| `validations/` | Immutable validator and live hash receipts bound to an execution receipt digest. |
| `exemplars/` | Approved contextual reference. Load only when a relevant skill links to it. |
| `rubrics/` | Approved quality guidance. Load only within its stated scope. |
| `context/learned-rules.md` | Canonical universal policy. Reserved for approved nonnegotiable rules. |
| `skills/` | Canonical workflow instructions. |

An approved item's source candidate fingerprint remains reserved. Future scans list added support under `Previously known patterns` instead of issuing a new candidate for the same learning.

## Promotion gate

No candidate becomes guidance because an agent scored it highly or saw it repeatedly.

Promotion completion requires:

1. A candidate report with linked evidence and counterevidence.
2. An immutable `FPRP` exact proposal whose candidate IDs, report paths, anchors, and fingerprints resolve to real candidate report entries, with fully enumerated operations, before and after hashes, exact content, trusted validators, and prohibited expansion.
3. A separate append only `FPRD` decision naming the human reviewer and binding the immutable proposal ID and its independently recomputed full digest.
4. Disposition `approve-exact`, `execution-authority: exact`, an unexpired authorization digest, and no later revoke event. Every other disposition has no execution authority.
5. An immutable `FPRE` terminal receipt. Blocked attempts have no changed paths and do not consume authority; at most one receipt may consume an authorization digest.
6. A passing `FPRV` receipt whose timestamp follows execution completion, whose ID binds the execution receipt digest, and whose validator coverage and receipt hashes match the proposal.
7. A continuous successful validated history for every changed path, with independently computed current bytes matching only the latest successful state.
8. A normal vault log entry after the approved change is applied.

A candidate can be triaged, held, rejected, or narrowed, but it can never be approved directly. A human may approve an immutable `FPRP` ID without typing its digest, but the system must resolve and recompute the full digest before creating the decision. Any change to an issued proposal creates a new content addressed proposal and requires a new human decision.

The full portable contract is in [approval-contract.md](approval-contract.md). It governs proposal digesting, append only decisions, one use authorization, terminal execution receipts, validation receipts, retries, and failure handling.

## Deterministic record tools

Use the supplied command line tools instead of calculating identifiers or digests by hand:

```bash
python3 resources/learning-library/pattern-review-records.py create proposal --payload proposal.json --created-date YYYY-MM-DD
python3 resources/learning-library/pattern-review-records.py create decision --payload decision.json --nonce 1234abcd
python3 resources/learning-library/pattern-review-records.py create execution --payload execution.json --attempt 1
python3 resources/learning-library/pattern-review-records.py create validation --payload validation.json --execution-receipt-digest sha256:[64 lowercase hex] --sequence 1
python3 resources/learning-library/pattern-review-records.py verify --record record-envelope.json
python3 resources/learning-library/validate-pattern-review.py --vault /path/to/vault
```

Creation prints a deterministic JSON envelope by default. Add `--output path.json` for an explicit atomic create. The output parent must already exist, and the tool refuses to overwrite any file. Decision creation requires an explicit nonce, and execution and validation creation require explicit sequence numbers. There are no random or implicit write defaults.

Envelope attempt and sequence fields are JSON integers. Boolean, string, null, array, and object values are rejected without coercion.

Map each verified envelope into its immutable markdown record:

| Envelope kind | `record_id` destination | `record_digest` destination | Additional bound value |
|---------------|-------------------------|-----------------------------|------------------------|
| `proposal` | `proposal-id` | `proposal-digest` | `created_date` |
| `decision` | `decision-id` | `decision-digest` | `authorization_digest` and `execution_authority` |
| `execution` | `execution-id` | `receipt-digest` | `attempt` |
| `validation` | `validation-id` | `validation-digest` | `execution_receipt_digest` and `sequence` |

Copy the envelope payload without changing it. Run the vault validator after the markdown record is created. If any payload value changes, discard the stale envelope and create a new one.

The standard broad promotion threshold is three independent occurrences across at least two projects or contexts. Repeated output from one agent, prompt, artifact, or iteration counts as one evidence family. A human may approve a documented exception.

## Four week shadow period

The first 28 days are report only:

- Candidate discovery is allowed.
- Human reviewers may reject, merge, narrow, or hold candidates.
- No candidate may change a rule, skill, rubric, exemplar, template, verifier, or project context because of the recurring scan.
- Record false positives, missed patterns, source gaps, and contradictions.
- The system remains in shadow mode until a human explicitly approves activation after the 28 day minimum, updates the mode fields above, and logs the change.

## One recurring writer

Use one designated writer for the scheduled Pattern Review. This avoids duplicate reports and write collisions in a shared or synced vault.

- Other agents may provide read only analysis or evidence.
- The writer identity belongs in the configuration table above.
- Scheduler configuration and credentials stay outside the vault.
- Changing the writer requires a human approved update to this file.

## Review cadence

- Weekly candidate discovery
- Monthly human decisions
- Quarterly rubric and exemplar calibration

Expired guidance is not silently deleted. Mark it retired, record why, and preserve the decision history.
