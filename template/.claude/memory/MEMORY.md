# Memory Index

This is the persistent memory system for Claude Code sessions. Memories are stored as individual `.md` files in this directory and indexed here.

Each memory file has frontmatter with `name`, `description`, and `metadata.type`. Types:
- **user** - Who the user is, their role, preferences, expertise
- **feedback** - Corrections and confirmed approaches (what to do / not do)
- **project** - Ongoing work, goals, decisions, deadlines
- **reference** - Pointers to external resources and where to find things

## How it works

- Claude auto-saves memories as corrections and preferences are learned
- This file is always loaded at conversation start
- Individual memory files are read when relevant
- Proposed universal learning enters `skills/pattern-review.md` as a noncanonical candidate. It reaches `context/learned-rules.md` only after a separate human promotion decision, so non-Claude tools inherit reviewed policy rather than private memory.

## Memories

> Memories will appear here as the vault is used. Example format:
>
> - [Short description](filename.md) - One line hook explaining the memory
