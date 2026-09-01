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

Twelve playbooks in `skills/clanker-mode/playbooks/`. Four are task-shaped
(investigation, bug fix, feature, refactoring), four are family-specific (OM
Chat and OM Mobile, each with a feature and a completion playbook), and the rest
cover loops, skill authoring, opening a review, and session pickup.

The router also holds the table of which repository belongs to which family.
That used to be prose in a CLAUDE.md, where it worked only if the model happened
to read it. Now it is a step.

## Sticky

Once entered, the mode persists. A follow-up "keep going" stays in it; "new
task" re-runs playbook selection; a casual turn does not drag the machinery in.
Say so to opt out.

## When not to use it

Three skills fire on their own, because forcing ceremony onto a read-only
question is how a system becomes annoying enough to abandon:

- **`why`** — why is this built this way. Git history, review threads, tickets,
  chat, incidents.
- **`teach`** — explain it properly, at your pace, building diagrams up one part
  at a time.
- **`unslop`** — cut AI tells from any prose, including the agent's own replies.

Everything else waits to be routed to.

Next: [Principles](./03-principles.md).
