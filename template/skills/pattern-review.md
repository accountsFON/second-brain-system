---
name: pattern-review
description: Discover recurring positive and negative work patterns, preserve them as noncanonical candidates, and route human approved learning to the right vault source.
type: skill
updated: YYYY-MM-DD
---

**Related Files:** [README.md](README.md) · [brain-check.md](brain-check.md) · [intake-processor.md](intake-processor.md) · [../resources/learning-library/README.md](../resources/learning-library/README.md) · [../context/learned-rules.md](../context/learned-rules.md)

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
2. A candidate becomes usable guidance only after an explicit human decision is recorded with the decision template.
3. Promotion changes one named canonical destination. Do not copy the same instruction into several files.
4. During the default four week shadow period, create reports only. Do not promote candidates or alter canonical guidance because of the scan.
5. Only the designated recurring writer named in `resources/learning-library/README.md` may create scheduled candidate reports. Other agents may run a read only preview or provide evidence to that writer.
6. A scheduler may invoke this skill, but scheduler state, credentials, and machine configuration stay outside the shared vault.

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
- **Monthly:** a human rejects, holds, merges, narrows, or approves candidates.
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
6. Keep it as a candidate until human approval is recorded.

For a negative example, use the smallest useful excerpt. Explain the failure, show the corrected version when available, and never place an unlabeled failed deliverable in the approved example library.

### 8. Record the human decision

Use `resources/learning-library/decision-template.md` and save one decision per reviewed candidate under:

`resources/learning-library/decisions/YYYY-MM-DD-[candidate-id].md`

Allowed decisions:

- Reject
- Hold for more evidence
- Merge with another candidate
- Narrow to project or client context
- Promote to a rubric
- Promote to an exemplar
- Promote to a skill
- Promote to a verifier
- Promote to a hard rule

Promotion requires a named human reviewer, date, approved scope, exact destination, and explicit authorization.

### 9. Apply an approved promotion

Skip this step in shadow mode.

After explicit approval:

1. Update the single canonical destination named in the decision.
2. Use `exemplar-template.md` or `rubric-template.md` when that is the destination.
3. Link dependent skills or templates to the canonical source instead of duplicating the text.
4. Add or update a verifier when the behavior is objectively testable.
5. Run the validation plan from the decision.
6. Record what changed, who approved it, and when it should be reviewed again.
7. Log the promotion through the vault's normal logging workflow.

## Output

A Pattern Review run produces:

- One noncanonical candidate report
- Evidence links, counterevidence, confidence, and scope for every candidate
- No canonical edits during discovery or shadow mode
- A separate human decision record when review occurs
- Targeted canonical changes only after explicit promotion approval
