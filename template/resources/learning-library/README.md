---
name: learning-library
description: Governed library for noncanonical pattern candidates, human decisions, approved exemplars, and approved rubrics.
type: reference
updated: YYYY-MM-DD
---

**Related Files:** [../../skills/pattern-review.md](../../skills/pattern-review.md) · [../../skills/brain-check.md](../../skills/brain-check.md) · [../../skills/intake-processor.md](../../skills/intake-processor.md) · [../../context/learned-rules.md](../../context/learned-rules.md) · [../../context/vault-manifest.md](../../context/vault-manifest.md)

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
├── candidate-report-template.md
├── decision-template.md
├── exemplar-template.md
├── rubric-template.md
├── candidates/       # Noncanonical discovery reports
├── decisions/        # Human review and promotion records
├── exemplars/        # Approved, annotated examples
└── rubrics/          # Approved, scoped quality rubrics
```

Do not create empty folders merely to complete the tree. Register each folder in the manifest when its first file is created.

## Authority model

| Location | Authority |
|---------|-----------|
| `candidates/` | Noncanonical. Never use as instructions or examples to imitate. |
| `decisions/` | Governance record. A decision authorizes a named destination but is not itself the destination. |
| `exemplars/` | Approved contextual reference. Load only when a relevant skill links to it. |
| `rubrics/` | Approved quality guidance. Load only within its stated scope. |
| `context/learned-rules.md` | Canonical universal policy. Reserved for approved nonnegotiable rules. |
| `skills/` | Canonical workflow instructions. |

An approved item's source candidate fingerprint remains reserved. Future scans list added support under `Previously known patterns` instead of issuing a new candidate for the same learning.

## Promotion gate

No candidate becomes guidance because an agent scored it highly or saw it repeatedly.

Promotion requires:

1. A candidate report with linked evidence and counterevidence.
2. A separate decision record naming the human reviewer.
3. Explicit authorization, approved scope, and one canonical destination.
4. A validation plan and future review date.
5. A normal vault log entry after the approved change is applied.

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
