# 2. The router

`$clanker-mode` is one skill whose job is deciding what happens next.

```
$clanker-mode the reaction picker spacing is off on mobile
```

It classifies the request, opens the matching playbook, and **copies that
playbook's steps into a todo list verbatim** before reasoning about the task.

## Why verbatim matters

The failure it prevents is subtle. An agent reads a playbook, understands it,
then writes its own plan — and the plan quietly loses a step. Usually the
verification step, because that is the one that feels redundant when you already
believe the code is right.

Copying the steps in first makes the omission visible. A step you decide to skip
**stays in the list** with `skip: <reason>`. You can disagree with a step; you
cannot silently drop it.

## What it routes to

Twenty-six playbooks in `skills/clanker-mode/playbooks/`. Four are task-shaped
(investigation, bug fix, feature, refactoring). Four are family-specific (OM
Chat and OM Mobile, each with a feature and a completion playbook). Six widen
the middle, where a plain feature is the wrong shape: prototype before the
build, grill me when the open questions are the operator's to answer, perf
issue and forensics when the answer is a number or an artifact, visual parity
for pixel work, feature plan when a feature needs a written plan before the one pass that builds it.
Four run the loops, one predicate at a time (autonomous run), one metric
(hillclimb), one plan of goals (agentic loop), or one experiment on the agent
itself (eval). One films a feature as a continuous UI motion film (product
video). The rest carry a change out the door, opening a review, driving it
green, landing it, cleaning up after it, plus skill authoring and the session
pair of pause and pickup.

The router also holds the table of which repository belongs to which family.
That used to be prose in a CLAUDE.md, where it worked only if the model happened
to read it. Now it is a step.

## Sticky

Once entered, the mode persists. A follow-up "keep going" stays in it; "new
task" re-runs playbook selection; a casual turn does not drag the machinery in.
Say "stop clanker mode" to opt out.

This now has a runtime implementation. `bin/deez clanker-hooks --apply` adds
session-scoped reminders on follow-ups, after compaction or resume, and every
20 tool calls. Codex requires trusting those definitions in `/hooks`. Without
running hooks, stickiness is only an instruction in the transcript.

The active task's playbook and external `resume.md` are registered with
`bin/deez clanker-checkpoint`. Compaction rereads them and continues the existing
checklist. It does not stop delegates, commit WIP or rerun finished steps. See
[session persistence](../../skills/clanker-mode/references/session-persistence.md)
for setup, scope and recovery limits.

## When not to use it

Three skills fire on their own, because forcing ceremony onto a read-only <!-- deez:counts-ok -->
question is how a system becomes annoying enough to abandon:

- **`why`** — why is this built this way. Git history, review threads, tickets,
  chat, incidents.
- **`teach`** — explain it properly, at your pace, building diagrams up one part
  at a time.
- **`unslop`** — cut AI tells from any prose, including the agent's own replies.

Everything else waits to be routed to.

Next: [Principles](./03-principles.md).
