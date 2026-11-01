# Field Notes

Lessons from real brains built with this system. Each note names the pattern, where to put it, and why it earned its place. Start here when you build a brain for one person who works through a chat assistant.

## From a solo agency owner's assistant brain (November 2026)

Built for a busy owner who talks to a ChatGPT assistant on a phone, with Codex and other agents reading the same files through GitHub.

### Patterns worth copying

1. **File every turn, unasked:** Commitments go to open loops with a real date, client facts to the client page, new people to a people file, dates to a key dates file, then one bullet in today's log. The user never says where anything goes.
2. **End with a Logged line:** `Logged: 2 to-dos in open loops, 1 note on the client page, today's log`. One glance proves the filing happened. No save, no line.
3. **Low verbosity everywhere:** Answer first, three lines of context at most, one decision with a recommended pick that "yes" accepts. Top three items only. Expand on request.
4. **Open loops with real dates:** `- [ ] What (owner, due YYYY-MM-DD) · link`, split into "I owe", "Waiting on others", and "To tell". Turn "Tuesday" into a real date with `date`.
5. **An autonomy dial with presets:** Four levels per action type (do it, do it and tell me, ask first, hand to me) and named presets, with a change log. Pair it with four hard rules: no secrets in files, never delete (archive instead), follow the dial for sending and spending, log what you did.
6. **Tell-people mini-prompts:** When a change affects a teammate or client, offer a one-tap message with the draft shown. Under 25 words, at most three a day, and drop it after two "not now" answers.
7. **A question queue:** Each open question has an ID, source, status, and last-asked date, so the assistant never asks the same thing twice.
8. **Learned from edits:** When the user rewrites a draft, add a dated bullet to the voice file. Fold the bullets into the main sections every ten entries.
9. **An inbox doc fallback:** When the assistant cannot write files directly, it appends a dated capture block to one shared doc, then adds a filing receipt once the capture reaches its real home.
10. **GitHub as the cloud copy:** A scheduled GitHub Action syncs the repo with the Drive folder using a three-way compare. When both sides change a file, GitHub wins and the Drive version is saved as a conflict copy to merge by hand. A delete brake and a secret scan guard the sync.

### Pitfalls we hit

1. **One paragraph pasted into many files:** A new rule landed in 21 files and drifted. Give each rule one home and link to it.
2. **Stale "ask first" wording:** A newer save-immediately rule left older ask-first lines behind, so the instructions contradicted themselves. When a rule changes, search for its old wording.
3. **Logs bloated:** One day's log reached 41 entries, some with 600-character lines and filler like "rechecked, nothing new". Keep bullets to one line and skip entries where nothing changed.
4. **One commit per file:** Chat assistants that write through a GitHub file tool make a commit per file, so one capture shows up as seven identical commits. Make the sync tolerate the bursts: a run that loses a push race should exit cleanly and let the next run finish.
5. **Two agents renaming at once:** Two agents ran the same find-and-replace minutes apart and clobbered each other. Give renames and other bulk edits one writer.
6. **The paste-in box hit its limit:** ChatGPT's custom instructions cap near 5,000 characters. Keep the paste-in short, point it at `AGENTS.md`, and let the repo hold the detail.
