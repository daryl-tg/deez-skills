# Session persistence

Clanker activation is saved per runtime and session, independently of the chat
history. Hook registrations belong to this hub; OMX and Herdr state remain
owned by their packages.

## Setup

From the hub root:

```bash
bin/deez clanker-hooks
bin/deez clanker-hooks --apply
```

The first command previews changes. The second preserves existing settings and
hooks, backs up changed files, then adds only Clanker handlers to Claude's
`settings.json` and Codex's `hooks.json`. It never installs `bin/sync` or pushes
anything. Runtime roots honor `DEEZ_CLAUDE_HOME` and `DEEZ_CODEX_HOME`, like
`bin/link`.

Codex requires reviewing and trusting the new definitions through `/hooks`.
The installer does not forge trust records or bypass that review. Restart or
resume the runtime to load new hooks. In a conversation that predates their
installation, invoke Clanker once to establish activation; the hooks do not
mine old transcripts for prior invocations.

Both runtimes support `UserPromptSubmit` and `SessionStart` with source
`compact` or `resume`, which carry the reminder into subsequent model requests.
Periodic `PreToolUse` reminders cover long tool runs between user messages.
Claude additionally uses `UserPromptExpansion` for direct slash commands.
See the [OpenAI hooks reference](https://learn.chatgpt.com/docs/hooks) and
[Claude hooks reference](https://code.claude.com/docs/en/hooks).

## Activation and scope

Start a prompt with `$clanker-mode`, `/clanker-mode`, or "use clanker mode".
Explicit enable/enter/turn-on phrases also work. Activation survives "keep going",
new tasks, casual questions, task completion, compaction and resuming the same
session. An unrelated session or runtime remains inactive. Worktree changes do
not move the session marker into the product repository.

Start a prompt with "stop clanker mode", "disable clanker mode", "exit clanker
mode", "turn off clanker mode", or "normal mode" to opt out. `$clanker-mode off`
and `/clanker-mode off` work too. `/clear` deactivates the current session.
Mentioning or quoting the skill in a question does not turn it on.

Session files are private local JSON under
`~/.local/state/deez-skills/clanker/<runtime>/`. Set `DEEZ_CLANKER_STATE` to use
another state directory. The filename hashes the runtime-provided session ID;
neither cwd nor a global boolean controls activation. The ID is an indexing key,
not proof of permission or workflow authority. No transcript content is copied.

## Durable task checkpoint

After choosing a playbook, write `resume.md` in
`~/Documents/dev-notes/<task-slug>/`, then register it. Use the runtime and
session ID supplied by the hook, the selected playbook filename and actual
absolute note path:

```bash
bin/deez clanker-checkpoint --runtime codex --session <session-id> \
  --playbook feature.md --resume-note /absolute/dev-notes/task/resume.md
```

The helper validates an already-active session, an existing Clanker playbook and
an existing note outside the hub. It saves their pointers without ingesting the
note into the reminder. A new task updates the pointer to its own note.

The note holds:

- Goal, definition of done and current user constraints.
- Runtime, worktree, branch and selected playbook.
- Checklist steps with completed, pending and skipped status; skips have reasons.
- Verification results and evidence paths, with unverified claims labeled.
- Pending user decisions or approvals, owned services and delegates.
- Next action and relevant source or map paths.

Compaction rereads the skill, playbook and note and continues the same checklist.
It does not use the explicit pause workflow. The note preserves progress, while
source, service state and current user instructions establish what is true now.

## Limits

These hooks restore guidance; they do not guarantee an agent obeys every rule.
Hooks disabled by the runtime or awaiting Codex trust cannot inject reminders.
Missing or corrupt local state is reported without blocking a tool or a user
turn. Missing checkpoint pointers remain a visible recovery gap. A resumed
conversation with no marker needs a fresh explicit activation.
