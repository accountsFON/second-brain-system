---
name: pattern-review
description: Discover recurring positive and negative work patterns, preserve them as noncanonical candidates, and route human approved learning to the right vault source.
type: skill
updated: YYYY-MM-DD
---

**Related Files:** [README.md](README.md) · [brain-check.md](brain-check.md) · [intake-processor.md](intake-processor.md) · [../resources/learning-library/README.md](../resources/learning-library/README.md) · [../resources/learning-library/approval-contract.md](../resources/learning-library/approval-contract.md) · [../context/learned-rules.md](../context/learned-rules.md)

# Pattern Review

Find repeatable lessons in completed work without allowing an agent to train itself on weak, accidental, or self generated examples.

This workflow produces evidence backed candidates. It does not silently change rules, skills, rubrics, templates, examples, or project context.

## When to use

- Weekly for candidate discovery
- Monthly for a human review of accumulated candidates
- Quarterly to recalibrate approved rubrics and exemplars
- When a user supplies a strong project, finished artifact, rubric, or failure example
- When repeated corrections suggest a workflow or verifier may need improvement

## Safety boundary

1. Files in `resources/learning-library/candidates/` are noncanonical observations. Never load them as instructions or examples to imitate.
2. A candidate can never be approved directly. Promotion requires an immutable content addressed `FPRP` proposal followed by an append only `FPRD` human decision bound to that proposal's independently recomputed full digest.
3. One authorization permits the fully enumerated proposal operations once. It does not permit inferred cleanup, a changed proposal, or an unlisted destination.
4. During the default four week shadow period, create reports only. Do not promote candidates or alter canonical guidance because of the scan.
5. Only the designated recurring writer named in `resources/learning-library/README.md` may create scheduled candidate reports. Other agents may run a read only preview or provide evidence to that writer.
6. A scheduler may invoke this skill, but scheduler state, credentials, and machine configuration stay outside the shared vault.
7. Every terminal execution attempt produces an immutable `FPRE` receipt. At most one receipt may consume an authorization digest. Every consumed execution requires a bound `FPRV` validation receipt.
8. Follow `resources/learning-library/approval-contract.md`. Natural language acknowledgment, reactions, candidate status, and agent scores never grant authority.

## Learning layers

Classify each finding before recommending a destination:

| Layer | Use |
|------|-----|
| Hard rule | Safety, security, irreversible actions, legal boundaries, or deterministic auto fails |
| Rubric | Context dependent quality criteria and tradeoffs |
| Approved exemplar | A bounded, annotated example that calibrates judgment |
| Skill | A repeatable workflow method |
| Verifier | A behavior or threshold that can be checked automatically |
| Project or client context | A lesson that should not spread beyond its scope |
| Candidate only | Evidence is incomplete, contradictory, or too narrow |

## Recurring cadence

- **Weekly:** discover and document candidates.
- **Monthly:** a human triages candidate evidence and records dispositions on exact proposals.
- **Quarterly:** review approved rubrics and exemplars for staleness, false positives, and changed conditions.

The first 28 days after activation are shadow mode. Use the period to measure false positives, weak correlations, missed patterns, and source quality.

## Instructions

### 1. Confirm mode and writer

Read `resources/learning-library/README.md`.

- Confirm whether the system is in `shadow` or `active` mode.
- Confirm the designated recurring writer.
- For a scheduled run, stop before writing if the current operator is not that writer.
- If the writer is still TODO, produce a preview in chat and ask the user to designate one before scheduling recurring writes.

### 2. Define the evidence window

Record:

- Absolute start and end dates
- Projects, clients, or workflows included
- Source types included
- Known exclusions or missing sources

Prefer direct evidence:

- Explicit human corrections or praise with reasons
- Revision history and before or after comparisons
- QA findings, test failures, verifier output, and production readback
- Outcome data tied to the work
- Repeated decisions across independent projects

Agent commentary about its own output is weak evidence unless supported by one of the sources above.

### 3. Find bounded candidate patterns

For each possible pattern, capture:

- What repeated
- Whether it is positive, negative, or contrastive
- The narrowest scope the evidence supports
- Why it may have affected the outcome
- What should not be copied or generalized

Treat repeated output from the same agent, artifact, prompt, or project iteration as one evidence family. Repetition inside one family does not create independence.

Before assigning a new candidate ID, search existing candidates, decisions, approved exemplars, and approved rubrics for the same mechanism, scope, and intended destination. Give each candidate a stable fingerprint based on those three elements. If the fingerprint or claim already exists, do not mint a new candidate. Record the new evidence as an update to the existing candidate, or mark the relationship as `extends`, `narrows`, `contradicts`, or `supersedes` when the new claim is materially different.

### 4. Test alternative explanations

Search for:

- Counterexamples
- Similar work where the pattern was absent
- Work where the pattern appeared but the outcome differed
- Changed constraints that could explain the result
- Selection bias, survivorship bias, or missing feedback

If contradictory evidence is not available, state that gap. Never infer that no contradiction exists merely because none was found.

### 5. Assess promotion readiness

For broad guidance, the normal minimum is:

- Three independent occurrences
- Evidence from at least two projects or contexts
- At least one human or measurable outcome signal
- Counterevidence considered
- A defined scope and proposed review date

A human may approve a documented exception. A single occurrence may still justify a project specific note, a regression test, or a safety fix without becoming a universal rule.

Score each candidate from 1 to 5 on:

- Evidence quality
- Source independence
- Outcome strength
- Scope clarity
- Contradiction risk, where 5 means high risk

Do not turn the total into automatic approval. The score helps a human compare candidates.

### 6. Write the candidate report

Use `resources/learning-library/candidate-report-template.md` and save the report under:

`resources/learning-library/candidates/YYYY-MM-DD-pattern-review.md`

Every candidate must include:

- Candidate ID
- Stable fingerprint
- Duplicate search result and relationship to any existing candidate or approved item
- Pattern statement
- Evidence links and dates
- Independent evidence count
- Counterexamples and alternative explanations
- Outcome signals
- Confidence and scope
- Recommended destination
- Proposed propagation map
- Validation plan
- Review and expiry dates

Mark the report `canonical: false`. State that no source of truth changed.

List repeat evidence under `Previously known patterns`. Reuse the existing fingerprint, link the prior record, and exclude those entries from `candidate-count`. Set `duplicate-count` to the number of known pattern entries.

### 7. Handle supplied strong examples

When a user provides a project or artifact they consider excellent:

1. Preserve or link the original source.
2. Record constraints, audience, and verified outcome.
3. Extract reusable decisions, not surface appearance alone.
4. Add a `Do not copy` section for context specific choices.
5. Test the proposed lesson against at least one average and one weak comparison when available.
6. Keep it as a candidate until an exact proposal is separately authorized and validated.

For a negative example, use the smallest useful excerpt. Explain the failure, show the corrected version when available, and never place an unlabeled failed deliverable in the approved example library.

### 8. Prepare an immutable exact proposal

Candidate triage does not grant authority. Create a proposal only when review has produced an exact bounded change.

For a possible canonical change, use `resources/learning-library/proposal-template.md` and save one proposal under:

`resources/learning-library/proposals/YYYY-MM/FPRP-YYYYMMDD-[digest-prefix].md`

The proposal must contain:

- One or more source candidate IDs, report paths, and stable fingerprints
- Narrow scope and explicit prohibited expansion
- Fully enumerated vault relative operations
- Before and expected after hash for every operation
- Complete full content payload for every operation. Schema version 2 does not permit patch payloads.
- An after hash computed from the exact UTF 8 bytes of each full content payload
- Trusted validator identifiers
- Failure behavior

Resolve every source candidate ID to its exact candidate report entry. Verify the report path, `#candidate-id` fragment, and fingerprint before issuing the proposal. A string that merely looks like a candidate ID is not a valid source.

Compute the full proposal digest from the canonical JSON payload and derive the `FPRP-YYYYMMDD-<first 12 digest hex>` ID using `resources/learning-library/approval-contract.md`. Once issued, do not edit the proposal. Any change creates a new content addressed proposal that names the earlier record in `revision_of`.

The proposal remains noncanonical and has no authority.

Write every `FPRP`, `FPRD`, `FPRE`, and `FPRV` governance record as a regular file at its exact kind and month path. Reject a record path with any symlink component or any resolved location outside the vault root.

### 9. Record the human decision

Use `resources/learning-library/decision-template.md` and save each immutable proposal decision event under:

`resources/learning-library/decisions/YYYY-MM/FPRD-YYYYMMDDTHHMMSSZ-[nonce].md`

Allowed decisions:

- `hold`
- `reject`
- `narrow`
- `request-details`
- `approve-exact`
- `revoke`

Only disposition `approve-exact` with `execution-authority: exact` grants write authority. It requires a named human reviewer, UTC timestamp, immutable `FPRP` ID, independently recomputed full proposal digest, expiration date, scope lock, constraints, prohibited expansion, and safe approval source. The system must be outside shadow mode.

The human may approve by immutable `FPRP` ID alone. Resolve that exact proposal, recompute its full digest, verify the ID suffix, and write the full digest into the `FPRD` decision. Do not require the human to type or copy the digest.

Every other disposition sets `execution-authority: none` and `authorization-digest: none`. A decision is about an exact proposal, not about approving a candidate.

For `narrow` and `request-details`, set `replacement_proposal` to `pending` or a distinct existing `FPRP` ID whose `revision_of` names the source proposal. Every other disposition requires `none`. Root and transition rules are defined in the approval contract. A revoke can follow only an unused `approve-exact` event and is terminal.

Create the `FPRD` ID from the UTC decision timestamp and a fresh eight character lowercase hexadecimal nonce. Compute the decision digest from canonical JSON. For `approve-exact`, derive the separate authorization digest from the verified proposal and decision digests. Decisions are append only. A later event names the previous event and forms a linear chain.

### 10. Execute or block one attempt

Skip this step in shadow mode.

Before every attempt, including a retry after a blocked result:

1. Verify the proposal ID and full proposal digest.
2. Verify the decision ID, full decision digest, and authorization digest.
3. Verify the execution proposal ID exactly equals the proposal ID bound by the decision, even when payload digests match.
4. Verify `approve-exact`, exact execution authority, expiration, and the absence of a later revoke event.
5. Verify the attempt starts on or after the approval decision time.
6. Verify every operation before hash.
7. Resolve every operation path again and reject any symlink route outside the vault root.
8. Verify no prior `FPRE` receipt consumed the authorization digest.
9. Reserve the authorization through one execution coordinator before any write so concurrent executors cannot both consume it.
10. Apply only the enumerated proposal operations, or block without writing.
11. Write an immutable terminal receipt under `executions/YYYY-MM/FPRE-YYYYMMDD-[authorization-digest-prefix]-NN.md`. Derive the ID date and `executed-date` from `completed_at`.
12. For each affected path, record its before hash, expected after hash, and observed after hash.
13. Compute `receipt-digest` from its canonical JSON payload.

A blocked attempt uses `approval_consumed: false` and an empty changed path list. Another blocked attempt may use the next sequence only after repeating every preflight check. Attempt times are nondecreasing and cannot overlap. Executed, partial, and rolled back attempts consume authority. Executed paths must match every proposal path and expected hash. Partial receipts name affected paths and may use `unknown` only when readback cannot establish observed state. Rolled back receipts prove every affected path returned to its before hash or absent state. Duplicate changed paths are invalid. At most one terminal receipt may consume an authorization digest, and no retry is allowed after consumption.

### 11. Validate and close the execution

After a consumed attempt:

1. Read back every executed path.
2. Require the validation timestamp to be at or after execution completion.
3. Run every validator named in the proposal.
4. Compare every receipt live hash to the proposal after hash.
5. At receipt creation, independently hash the actual live vault target bytes and compare those computed hashes to the proposal. Never treat receipt supplied hashes as sufficient proof at that moment.
6. Create `resources/learning-library/validations/YYYY-MM/FPRV-YYYYMMDD-[execution-receipt-digest-prefix]-NN.md` from the validation receipt template.
7. Include every trusted validator ID, result, safe evidence reference, and live hash.
8. Compute the validation digest from canonical JSON.
9. Log a successful promotion through the vault's normal logging workflow only after a passing receipt resolves.

Do not claim completion without a passing validation receipt backed by independently computed live target hashes. Validation times are nondecreasing, cannot precede execution completion, and a passing receipt must be final. A failed validation never broadens or retries the approved operation. A later validation run uses a new immutable sequence record.

On later audits, keep historical `FPRV` receipts structural. Order successful validated executions for each path by completion time, require each next proposal before hash to equal the previous successful after hash, and compare actual current bytes only with the latest successful validated state. Reject ambiguous or discontinuous histories.

## Output

A Pattern Review run produces:

- One noncanonical candidate report
- Evidence links, counterevidence, confidence, and scope for every candidate
- No canonical edits during discovery or shadow mode
- Immutable exact proposals for promotion ready candidates selected by a human
- Append only human decisions, with authority bound to one proposal digest
- Immutable terminal execution receipts with one use authorization enforcement
- Validation receipts with trusted validator results and live hash evidence
- Targeted canonical changes only after the full approval contract passes
