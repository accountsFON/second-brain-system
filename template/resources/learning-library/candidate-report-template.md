---
name: pattern-review-YYYY-MM-DD
description: Noncanonical candidate report for the stated evidence window.
type: learning-candidate-report
schema-version: 2
updated: YYYY-MM-DD
status: candidate
canonical: false
authority: none
writer: TODO
evidence-window: YYYY-MM-DD to YYYY-MM-DD
candidate-count: 0
duplicate-count: 0
review-by: YYYY-MM-DD
---

**Related Files:** [README.md](README.md) · [proposal-template.md](proposal-template.md) · [approval-contract.md](approval-contract.md) · [../../skills/pattern-review.md](../../skills/pattern-review.md)

> Template note: After saving a report under `candidates/`, update these links for the new folder depth.

# Pattern Review Candidate Report

> NONCANONICAL: This report contains observations for human review. Do not load it as policy, a rubric, a skill, or an example to imitate. No source of truth changes because this report exists.

Every candidate section heading must exactly match `## Candidate PR-YYYY-MM-DD-NN: Nonempty title`. Candidate like malformed headings are invalid and must be reported, not ignored.

## Run record

| Field | Value |
|------|-------|
| Mode | `shadow` or `active` |
| Designated writer | TODO |
| Evidence window | YYYY-MM-DD to YYYY-MM-DD |
| Included scope | TODO |
| Exclusions and missing sources | TODO |
| Reports or candidates checked for duplication | TODO |

## Run summary

- Sources reviewed: TODO
- Candidate patterns found: TODO
- Previously known patterns found: TODO
- Candidates held for weak evidence: TODO
- No canonical changes made: Yes

---

## Candidate PR-YYYY-MM-DD-01: [Short name]

**Fingerprint:** `[mechanism]-[scope]-[destination]`

### Duplicate search

- Existing candidates checked: TODO
- Existing decisions, exemplars, and rubrics checked: TODO
- Relationship: New | Duplicate | Extends | Narrows | Contradicts | Supersedes
- Related candidate or approved item: TODO
- If duplicate: Do not issue this candidate ID. Move the evidence to an existing candidate update section instead.

### Pattern statement

State the observed positive, negative, or contrastive pattern in one precise paragraph.

### Scope

- Applies to: TODO
- Does not yet apply to: TODO
- Pattern type: Positive | Negative | Contrastive
- Proposed destination: Hard rule | Rubric | Exemplar | Skill | Verifier | Project context | Candidate only

### Evidence

| ID | Date | Project or context | Evidence and outcome signal | Source path or link | Evidence family |
|----|------|--------------------|-----------------------------|---------------------|-----------------|
| E1 | YYYY-MM-DD | TODO | TODO | TODO | F1 |

### Counterevidence and alternative explanations

- Counterexample searched: TODO
- Contradictory result: TODO
- Alternative cause: TODO
- Missing evidence: TODO
- Why this may be coincidence: TODO

### Independence and sample size

- Raw occurrences: TODO
- Independent evidence families: TODO
- Projects or contexts represented: TODO
- Repeated output collapsed into one family: TODO

### Assessment

| Dimension | Score, 1 to 5 | Reason |
|----------|---------------:|--------|
| Evidence quality | TODO | TODO |
| Source independence | TODO | TODO |
| Outcome strength | TODO | TODO |
| Scope clarity | TODO | TODO |
| Contradiction risk | TODO | TODO |

**Confidence:** Low | Medium | High

### Portable lesson

Describe the reusable decision or criterion. Do not copy surface details that depend on the original context.

### Do not copy

List context specific choices, accidental details, and unsupported generalizations.

### Proposed propagation map

| Destination | Proposed change | Why this is the canonical location | Dependent files that should link, not duplicate |
|------------|-----------------|------------------------------------|-------------------------------------------------|
| TODO | TODO | TODO | TODO |

### Validation plan

- Artifact or workflow to test: TODO
- Expected evidence: TODO
- Failure or rollback condition: TODO
- Human judgment still required: TODO

### Review dates

- Human review by: YYYY-MM-DD
- Expire or reassess by: YYYY-MM-DD

### Promotion readiness

- [ ] Three independent occurrences
- [ ] At least two projects or contexts
- [ ] Human or measurable outcome signal
- [ ] Counterevidence considered
- [ ] Scope is explicit
- [ ] Canonical destination is named
- [ ] Validation and review dates are defined

**Recommendation:** Reject | Hold | Merge | Narrow | Consider drafting an exact `FPRP` proposal after shadow mode

## Previously known patterns

### KNOWN-YYYY-MM-DD-01: [Short name]

- Fingerprint: `[existing fingerprint]`
- Matches: TODO
- New evidence: TODO
- Action: Evidence update only. Do not count as a candidate.
