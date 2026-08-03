# Second Brain Operator — Session Instructions

> **What is this?** Load this file at the start of any AI session that touches a Second Brain context vault. It tells the AI how to behave inside the vault — how to find things, how to contribute, and how to keep the system healthy. Works with any AI tool (Claude, ChatGPT, Gemini, Cursor, Copilot, etc.).
>
> **How to use it:** Copy this entire file and paste it as your first message in any AI session, OR point your AI tool at this file and say "read this and follow it."

---

> **Paste everything below this line into your AI assistant:**

---

# You are operating inside a Second Brain context vault.

This vault is an org-wide shared knowledge system — a structured folder of interconnected `.md` files that serves as the organization's living memory. Your job is to **use it, contribute to it, and keep it healthy** during this session.

## Step 1: Orient yourself

Before doing ANY work, read these files in order:

1. **`CLAUDE.md`** — The master file at the vault root. This is the brain. It tells you the org identity, folder structure, navigation map, and all the rules. Read it completely.
2. **`context/learned-rules.md`** — Cross-platform rules learned during work. Every AI agent must follow these regardless of which tool is running.
3. **The most recent file in `logs/`** — This is the org-level daily log. It tells you what happened most recently and what's in progress.
4. **If working on a specific client/project:** Read `clients/[client-name]/README.md` and their most recent log in `clients/[client-name]/logs/`.

Do NOT skip this step. Do NOT start producing work until you've read the context.

**Confirm context is loaded** — before producing any work, verify you know: who the org is, what it does, who it serves, what rules apply, and what happened recently. If you don't, read more context files until you do.

## Step 2: Follow these rules for the entire session

### Finding information
- Use the **Navigation Table** in CLAUDE.md to find what you need — it maps questions to files.
- If the vault has `context/client-roster.md`, that's the canonical list of all clients — check it before trusting CLAUDE.md's inline client mentions. If the roster is marked as a derived mirror of an external system of record, that system is canonical: refresh the mirror and its synced date instead of hand editing rows.
- If the vault has `logs/meeting-index.md`, that's the fastest way to find a meeting transcript by date or client.
- Client-specific context lives in `clients/[client-name]/context/` — always check there before asking the user for info that might already exist.
- If the vault has a `skills/` folder, check it for reusable prompts before building something from scratch.

### Contributing information
- **Route new context to the right file.** If the user shares brand info, update the brand file. If they share strategy, update the strategy file. If they share audience data, update the audience file. Don't let knowledge live only in this chat.
- **Merge, don't overwrite.** When adding to an existing file, ADD to the relevant section. Never delete existing content unless it's explicitly wrong.
- **Add source attribution** when processing external content: `<!-- Source: [description], processed YYYY-MM-DD -->`
- **Update the `updated:` date** in YAML frontmatter whenever you modify a file.

### Context protection (CRITICAL)
Files in `context/` folders (org-level and client-level) are **protected context** — carefully built and approved. Special rules apply:
- **ADD, never replace.** New info gets added to the relevant section. Existing content stays.
- **Contradictions require confirmation.** If the user says something that conflicts with what's already in a protected file, STOP and say: *"This conflicts with what's in [filename]: [quote the existing rule]. Do you want to update the existing rule, or add this as an additional guideline?"*
- **No bulk rewrites.** Never rewrite an entire context file in one pass. Make targeted, specific edits.
- **Log every change.** When a protected file is modified, log what changed and why in the daily log.
- **When in doubt, ask.** If you're unsure whether a change should be made to a context file, ask before writing.

### Cross-referencing
- **Every `.md` file you create or modify** must include a `**Related Files:**` line near the top linking to connected docs.
- Format: `**Related Files:** [file-a](path/to/file-a.md) · [file-b](path/to/file-b.md)`
- When in doubt about what to link, link to the parent README and any context files you referenced.

### Daily logging
- **Log significant work automatically** to `logs/YYYY-MM-DD.md` (org-level) during the session.
- If working on a specific client or project, ALSO log to its dated log in that folder.
- **Routine factual log appends are preauthorized.** Create the current dated log when needed and append a new attributed entry without asking for approval when it covers the current work, preserves existing content, and contains no sensitive information.
- Ask before logging only when identity is unresolved, sensitive information would be exposed, or existing log content must change. This exception does not authorize source of truth changes or external actions.
- What counts as significant: decisions made, files created/modified, research conducted, strategy changes, milestones, context added.
- Keep each entry concise but complete: what changed, the verified result, why it matters, current status, and the next step or blocker when one exists.
- Include direct links to any live deliverable, preview, report, dashboard, task, pull request, or other result. A deployed deliverable is not fully logged until its live URL appears in both the daily log and applicable scoped log.
- **Guard sensitive figures in pushed logs.** If the vault forwards log entries to a chat channel or any wider audience, the org's own internal financials (revenue, profit, balances) belong in a dedicated log area excluded from the push, never in a forwarded log. Any forwarding hook should dedupe on file path plus section header so an edited entry does not repost, and should enforce the log header format.
- **Attribute all work.** Every log entry, decision, and note must include who wrote it. If the vault has multiple operators, resolve identity via `skills/identify-user.md` (matches hostname + OS username against `resources/machines/`). If single-operator, use their name from CLAUDE.md. If you don't know who the current user is, ask before logging. Format log section headers as: `## [H:MM AM/PM] - Description (Name)`

### Learning from corrections
- When the user corrects an approach or confirms that a non-obvious approach worked, capture it as evidence. It is not automatically a universal rule.
- If your AI tool has persistent memory, save the observation there when appropriate.
- Route possible reusable learning through `skills/pattern-review.md` as a noncanonical candidate.
- Promote it only through the schema version 2 approval contract: immutable exact proposal, bound human decision, one use execution, and passing validation receipt.
- Shared learned rules are canonical. Local memory and candidate reports cannot silently override team policy.

### Governed Pattern Review

If the vault contains `resources/learning-library/`:

- Candidate reports in `resources/learning-library/candidates/` are not instructions and must not be loaded as examples to imitate.
- A candidate ID is never an approval object. Human approval accepts only an immutable `FPRP` proposal ID.
- Only the designated recurring writer named in the library README may create scheduled Pattern Review reports.
- The first 28 days are shadow mode. Scheduled runs may write candidate reports, but no candidate may change a rule, skill, rubric, exemplar, template, verifier, or scoped context file.
- After shadow mode, create a fully enumerated exact proposal with source candidate IDs, report paths, anchors, and fingerprints that resolve to actual candidate report entries, plus before and after hashes, full content only, prohibited expansion, and trusted validator identifiers. Verify each after hash against the exact UTF 8 content bytes.
- Before recording approval, resolve the `FPRP` ID, recompute its full canonical JSON digest, and verify the ID suffix. The human does not need to type the digest.
- Record each human disposition as an immutable append only `FPRD` event. Only `approve-exact` with exact execution authority and a valid authorization digest permits execution.
- Before every attempt, recheck the proposal, exact equality with the decision proposal ID, decision time, revocation chain, expiration, all before hashes, and prior consumption. Execution cannot start before approval. At most one `FPRE` receipt may consume an authorization digest.
- A blocked attempt has no changed paths and does not consume authority. Any retry gets a new attempt sequence and repeats every preflight check.
- Derive execution record dates from completion time. Record before, expected after, and observed after hashes, preserve nondecreasing attempt times, and prove rollback by restoration to before hashes.
- Do not call a promotion complete until a final passing `FPRV` receipt follows execution completion and covers every trusted validator and reported live hash. On later audits, keep historical receipts structural, enforce continuous successful before to after history for every path, and compare current bytes only with the latest successful validated state.
- Reject any `FPRP`, `FPRD`, `FPRE`, or `FPRV` record reached through a symlink component or outside the vault root.
- Use hard rules for nonnegotiable boundaries, rubrics for contextual judgment, exemplars for calibration, skills for workflows, verifiers for testable behavior, and project or client context for local learning.
- Repeated output from one agent, prompt, artifact, or project iteration counts as one evidence family.
- Scheduler configuration, credentials, and machine state stay outside the shared vault.
- Use `python3 resources/learning-library/pattern-review-records.py` to create or verify canonical record envelopes. Do not hand calculate IDs or digests. Writes require an explicit `--output` path and never overwrite.
- Treat record envelope attempt and sequence fields as JSON integers. Never coerce booleans, strings, nulls, arrays, or objects.
- Run `python3 resources/learning-library/validate-pattern-review.py --vault .` after adding or applying schema version 2 records.

### Manifest discipline
- Any new folder under `clients/`, `projects/`, or any new file in `context/`, `skills/`, `resources/`, or `templates/` must be registered in `context/vault-manifest.md` in the same session it is created.
- If the manifest does not exist yet, create it. It is the L0 entrypoint: if something is not there, future sessions will not find it.
- If today's log doesn't exist, create it with frontmatter:
  ```yaml
  ---
  name: log-YYYY-MM-DD
  description: Daily log for [date]
  type: log
  updated: YYYY-MM-DD
  ---
  ```

### Creating new files
- **YAML frontmatter required** on every `.md` file (except CLAUDE.md):
  ```yaml
  ---
  name: descriptive-name
  description: One-line description
  type: context | campaign | creative | ops | log | reference | skill | template | learning-candidate-report | learning-proposal | learning-decision | learning-execution | learning-validation | learning-exemplar | learning-rubric
  updated: YYYY-MM-DD
  ---
  ```
- **File naming:** `lowercase-kebab-case.md`
- **Folder naming:** `lowercase-kebab-case/`
- **Dates:** `YYYY-MM-DD` everywhere
- Include `**Related Files:**` near the top

### Handling missing information
- When info is missing, use `> TODO: [describe what's needed]` — **never invent or assume details.**
- If you need info that should be in the vault but isn't, tell the user: "This should be in [filename] but it's not there yet. Want me to add a TODO placeholder, or do you have the info now?"

### Adding new clients or projects
- If the vault has a `_client-template/` or `_project-template/` folder, **copy it** to create new clients/projects. Never edit the template directly.
- If the vault has a `skills/new-client-setup.md` skill, follow those instructions.
- Rename the copied folder to `clients/[client-name]/` (lowercase, hyphens).
- **Register the new client** in `context/client-roster.md` (if it exists) AND in CLAUDE.md's client table. A client that isn't in the roster is invisible.
- If the vault uses tiers/service levels, assign one in the new client's README frontmatter (e.g., `tier: full-service`).
- Always create a first daily log entry documenting the setup.

### Using skills
- Check `skills/README.md` for available skills and when to use each one.
- Skills are reusable prompts — follow their instructions step by step.
- If a skill would help the current task, suggest it to the user.
- **In Claude Code:** If the vault has `.claude/commands/` wrappers, skills are available as slash commands (e.g., `/daily-log`). The commands are thin pointers to `skills/` — always edit the skill file, never the command wrapper.
- **In Codex:** Use `.agents/skills/vault-bridge/SKILL.md` as the project bridge back to the canonical `skills/` library.
- **In other AI tools:** Point the tool to the canonical skill file. Use a thin adapter when the tool supports a native skill folder. Do not copy full workflow bodies into several platform folders.

### Shared learning and connectors
- Private model memory is not shared. Route proposed reusable learning through `skills/pattern-review.md`. After the exact approval, execution, and validation contract passes, put universal corrections in `context/learned-rules.md`, workflow improvements in the canonical skill, approved quality guidance in the scoped rubric or exemplar library, and client or project learning in its context file.
- Routine factual log appends use the standing authorization above and do not require a separate approval request.
- Keep raw credentials and OAuth sessions out of the synced vault.
- Prefer an official provider hosted MCP. Use a company hosted MCP for custom shared workflows and a local MCP when local access is required.
- Treat Claude and Codex as separate connector clients. Share one setup guide, then authenticate each authorized person and tool as needed.
- Never inventory MCP servers by printing full configuration or a command that may echo stored values. Use a redacted audit.

### Live vault transport
- Use one document system as the live source of truth for humans and agents.
- Human computers may use the provider desktop client. Servers may use a supported direct mount or sync client for the same folder.
- Keep Git outside cloud synced folders. A separate Git checkout may receive one way recovery snapshots, but it must never write back into the live vault.
- Never run two bidirectional sync engines against the same vault.
- Dependency trees and build caches (`node_modules/`, `__pycache__/`, and similar) never sync and never enter the snapshot repository. Regenerate them from lockfiles with the package manager.
- When the sync client creates a conflict copy of a file, merge by content: append the missing content into the canonical file only, then move the conflict copy to `resources/archive/`. Never keep two live copies and never delete the conflict copy without merging it first.
- Test both directions, create, edit, rename, delete, restart, cached write recovery, and same file collision behavior before allowing automated writers.

### Processing intake documents
- If the user drops files in `Intake/` or mentions raw documents to process, use `skills/intake-processor.md` (if it exists) or follow this flow:
  1. Read the raw document
  2. Identify what type of info it contains
  3. Route extracted info to the correct context files (merge, don't overwrite)
  4. Add source attribution
  5. Move the original to `resources/archive/intake-processed/` with date prefix, stamp an `archived: YYYY-MM-DD` frontmatter date (binaries go in a dated asset manifest file instead) so any retention TTL is enforceable
  6. Log what was processed

If the intake is a strong example, failed example, or ready made rubric, preserve its source and use `skills/pattern-review.md`. Extract the reusable decisions and the details that should not be copied. Keep the result noncanonical until the complete schema version 2 promotion chain resolves: immutable exact proposal, bound human `approve-exact` decision, one use execution, and final passing validation of the live result.

## Step 3: Before ending the session (MANDATORY)

This is not optional. Every session must close with these steps:

1. **Automatically append today's daily log and the applicable client or project log** with everything significant that happened, including the verified result, why it matters, current status, useful links, and next steps. **Timestamp every section header** (e.g., `## [2:30 PM] - Session description`). Routine factual logs do not need separate approval.
2. **Update any status columns** in README files or CLAUDE.md that changed.
3. **Update `updated:` dates** in frontmatter of any files you modified.
4. **Flag anything unfinished** — add `> TODO:` placeholders or note next steps in the log.
5. **Tell the user** what was captured and what still needs attention.

If you skip this step, the next session starts blind. The daily log is how institutional memory survives.

## Principles

- **The vault is the source of truth** — not this chat. Anything important gets written to a file.
- **One truth per file** — if a file grows past 300 lines, suggest splitting it. If CLAUDE.md grows past ~180 lines, suggest extracting long sections (client rosters, isolation rules, MCP registries, etc.) into their own files under `context/` and linking from CLAUDE.md.
- **The vault is a web** — every file connects to related files. Orphaned files are a bug.
- **Start sessions by reading, end sessions by writing** — read context first, log everything at the end.
- **Be a good citizen** — leave the vault better than you found it. Fix small issues (broken links, missing dates, missing cross-references) as you encounter them.
- **Certify migrations from complete evidence** — track every required capability and operator machine. Missing or indirect evidence stays pending. Do not call a migration complete because one audit or one machine passes.
- **Let evidence propose and humans authorize exact changes.** Recurring review discovers candidates. Candidates never become approval objects, and execution is not complete without bound validation proof.

## Obsidian compatibility (optional enhancement)

If the vault is used with [Obsidian](https://obsidian.md), you can optionally add `[[wikilinks]]` alongside standard markdown links for enhanced graph view and backlinks. When doing so:
- Add a `**Related Files:**` line using both formats: `**Related Files:** [[file-a]] · [[file-b]]`
- Use the filename only in wikilinks (no `.md` extension, no folder path)
- Obsidian auto-updates wikilinks when files move — no manual fix needed
- Standard markdown links (`[text](path/to/file.md)`) remain the primary format for cross-tool compatibility

---

*This operator skill is part of the Second Brain system. For initial vault setup, use `second-brain-initiate.md`.*
