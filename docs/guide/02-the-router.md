# 2. The router

`$clanker-mode` is one skill whose job is deciding what happens next.

```
$clanker-mode the reaction picker spacing is off on mobile
```

It classifies the request, opens the matching playbook, and **copies that
playbook's steps into a todo list verbatim** before reasoning about the task.

## Why verbatim matters

An agent that reads a playbook and then writes its own plan quietly loses a
step. Usually it is the verification step, because that one feels redundant
when you already believe the code is right.

Copying the steps in first makes the omission visible. A step you decide to skip
**stays in the list** with `skip: <reason>`. You can disagree with a step. You
cannot silently drop it.

## What it routes to

Twenty-six playbooks in `skills/clanker-mode/playbooks/`. Four are task-shaped
(investigation, bug fix, feature, refactoring). Four are family-specific (OM
Chat and OM Mobile, each with a feature and a completion playbook). Six widen
the middle, where a plain feature is the wrong shape: prototype before the
build, grill me when the open questions are the operator's to answer, perf
issue and forensics when the answer is a number or an artifact, visual parity
for pixel work, feature plan when a feature needs a written plan before the one
pass that builds it. Four run the loops, one predicate at a time (autonomous
run), one metric (hillclimb), one plan of goals (agentic loop), or one
experiment on the agent itself (eval). One films a feature as a continuous UI
motion film (product video). The rest carry a change out the door, opening a
review, driving it green, landing it, cleaning up after it, plus skill authoring
and the session pair of pause and pickup.

The router also holds the table of which repository belongs to which family.
That used to be prose in a CLAUDE.md, where it worked only if the model happened
to read it. Now it is a step.

## Every delegate reads worker.md first

The operator's rules live in skills that load only from a slash command, so a
subagent never sees them on its own. The router makes the first line of every
delegate brief `Read ~/.claude/skills/clanker-mode/worker.md before anything
else.` [That one short file](../../skills/clanker-mode/worker.md) carries the
rules every agent in the run keeps. The
brief's bar is the whole bar. Reversible calls get made and explained, never
asked. Work runs in one pass, checks stay scoped to the change, reserved ports
stay untouched, comments never explain the code, git and reviews carry no
Claude attribution, and reviews open ready. A delegate that starts its own
agent passes the same line on.

## Sticky

Once entered, the mode persists. A follow-up "keep going" stays in it. "New
task" re-runs playbook selection. A casual turn does not drag the machinery in.
Say "stop clanker mode" to opt out.

`bin/deez clanker-hooks --apply` adds session-scoped reminders on follow-ups,
after compaction or resume, and every 20 tool calls. Codex requires trusting
those definitions in `/hooks`. Without running hooks, stickiness is only an
instruction in the transcript.

The active task's playbook and external `resume.md` are registered with
`bin/deez clanker-checkpoint`. Compaction rereads them and continues the existing
checklist. It does not stop delegates, commit WIP or rerun finished steps. See
[session persistence](../../skills/clanker-mode/references/session-persistence.md)
for setup, scope and recovery limits.

## When not to use it

Four skills fire on their own, because forcing ceremony onto a read-only <!-- deez:counts-ok -->
question is how a system becomes annoying enough to abandon:

- **`why`**. Why is this built this way. Git history, review threads, tickets,
  chat, incidents.
- **`teach`**. Explain it properly, at your pace, building diagrams up one part
  at a time.
- **`tutor`**. Quiz and drill you to mastery, with a skill map, spaced review,
  and a final assessment.
- **`unslop`**. Cut AI tells from any prose, including the agent's own replies.

When you cannot name what you are building, run `/reframe` on your own
description first. It ranks the expert terms that would change the build,
borrows words from neighboring fields that solved the same problem, and
rewrites your description with them.

Everything else waits to be routed to.

Next: [Principles](./03-principles.md).
