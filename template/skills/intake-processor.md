---
name: intake-processor
description: Process raw documents from the Intake/ drop zone. Extract key info and route it to the correct vault files.
type: skill
updated: YYYY-MM-DD
---

**Related Files:** [README.md](README.md) · [pattern-review.md](pattern-review.md) · [../CLAUDE.md](../CLAUDE.md) · [../context/vault-manifest.md](../context/vault-manifest.md) · [../resources/learning-library/README.md](../resources/learning-library/README.md)

# Intake Processor

Process a raw document that was dropped into the `Intake/` folder. Extract useful information and route it to the correct vault files.

## When to use

- A new file appears in `Intake/`
- The user says "process this document" or "I dropped something in Intake"
- The brain-check skill flags intake backlog

## Instructions

### 1. Read the raw document

Read the file in `Intake/`. Identify what type of information it contains:
- Client info (brand, audience, competitors, messaging)
- Meeting notes or transcript
- Strategy document or research
- Asset inventory or content library
- Process documentation
- Reference material
- Strong project example, finished artifact, existing rubric, or failure example offered for reusable learning

### 2. Identify the destination

Based on the content type, determine where the extracted info belongs:
- Client context? Route to `clients/[name]/context/`
- Org-level context? Route to `context/`
- Meeting transcript? Route to `logs/` and update `logs/meeting-index.md`
- Reference material? Route to `resources/`
- Template or process? Route to `templates/` or `context/processes.md`
- Supplied example or rubric? Preserve the source, then route the proposed learning through `skills/pattern-review.md`. Do not place it directly in approved rubrics, exemplars, skills, or learned rules.

### 3. Extract and merge

Pull the key information from the document and add it to the destination files.
- **Merge, do not overwrite.** Add to existing sections. Never delete what is already there.
- **Add source attribution:** `<!-- Source: [filename], processed YYYY-MM-DD -->`
- **Use TODO placeholders** for anything unclear or incomplete
- **Cross-reference** the new content with related files

For a supplied learning example, also capture:

- Why the user considers it strong or weak
- Audience, constraints, and date
- Verified outcome or feedback
- Reusable decisions
- Details that should not be copied
- Comparison artifacts, if available

Create a noncanonical candidate report from the Pattern Review template after approval. During shadow mode, stop there.

### 4. Confirm with the user

Before writing, tell the user:
- What you found in the document
- Where you plan to route each piece
- Any ambiguities or conflicts with existing content
- Whether any proposed learning will remain a noncanonical candidate or has a separate human promotion decision

Wait for approval before writing.

### 5. Archive the original

After processing, move the original file to `resources/archive/intake-processed/` with a date prefix:
`resources/archive/intake-processed/YYYY-MM-DD-original-filename.ext`

### 6. Log the processing

Add an entry to today's daily log:
- What was processed
- Where the content was routed
- Any TODOs flagged

## Output

- Updated vault files with the extracted content merged in
- A noncanonical Pattern Review candidate when the intake contains a supplied example, rubric, or reusable lesson
- Original file archived
- Daily log entry documenting what was processed
