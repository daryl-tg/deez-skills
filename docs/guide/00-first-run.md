# 0. First run

What to do the first time, in order, and what each step buys you. Roughly thirty
minutes for the hub itself, then one session per repository for verification.

## Step 1 — Install the hub

```bash
git clone git@github.com:daryl-tg/deez-skills.git ~/github/deez-skills
cd ~/github/deez-skills
bin/test                 # proves the toolchain before it touches anything
bin/link                 # preview. read it
bin/link --apply
```

Restart Claude Code and Codex. Both read their skill directories at session
start, so nothing installed now is visible until you do.

Details, including the Python requirement and every `bin/link` verb, are in
[chapter 1](./01-setup.md).

## Step 2 — Prove both runtimes see it

```bash
bin/doctor               # should be 0 failures
```

Then check the runtimes themselves, because `doctor` proves the symlinks are
right and cannot prove a runtime loaded them.

In **Claude Code**, `$clanker-mode` should resolve. In **Codex**, ask it to list
skills whose name starts with `principle-`. All thirty-four should appear — they
install on both runtimes precisely so a handoff citing one resolves on either
side.

If a skill is missing on Codex specifically, check that its frontmatter `name`
matches its install name. Codex resolves its catalogue by that field.

## Step 3 — Set up verification, once per repository

**This is the step people skip, and it is the one everything else leans on.**
Until a repository has a verification skill, "prove it works" is an instruction
pointing at nothing.

Do this once per repo, in a session inside that repo:

```
create-verification-skill
```

It interviews the **repo**, not you: how the app starts, how to drive it, what
evidence can be captured, whether two instances can run side by side. It asks
only what it cannot observe. Then it produces three things:

| Artifact | Where | What it is |
|---|---|---|
| `control-<app>` | **in that repo**, committed | The wrapper: `doctor`, `browser`, `cli`, `evidence publish` |
| `skills/verify-<app>/` | in the hub | Launch, doctor, drive, evidence, cleanup |
| `features/` | in the hub, beside it | One file per user-facing feature. The durable part |

The generator then **runs its own instructions once** — launch, doctor, drive
one feature, capture, clean up — and confirms the evidence survived cleanup. A
generated skill that was never executed is a draft, not a deliverable.

Start with three to five features, not everything. The map grows as you touch
new surfaces.

Seed order matches the delivery order: `openmarket-chat` first, then
`openmarket-chat-cloud`, then `openmarket-chat-app`.

## Step 4 — Learn the two verification lanes

This is the part worth ten minutes now rather than a confused hour later.

| | Inner loop | Terminal gate |
|---|---|---|
| Command | `control-<app> doctor`, then replay the recipe | An agent drives `agent-browser` |
| When | After every meaningful edit | Once, at the end of a feature |
| Cost | Near zero | Tokens and wall-clock |
| Produces | Green or red | The artifact pair and a published URL |

Running the terminal gate after every edit is the expensive mistake. Skipping it
at the end because the inner loop was green is the dangerous one.

[Chapter 4](./04-verification.md) has the detail.

## Step 5 — Decide the maintenance cadence

**You do not need a daily maintainer.** That was my assumption too, and the cost
model does not support it — see [chapter 9](./09-keeping-it-honest.md), which
covers what actually triggers a maintenance pass and what is worth automating.

The short version: `control-<app> doctor` is the cheap daily thing, and it runs
inside your normal work anyway. The full `maintain-verification-skill` pass
drives every mapped feature live, so it is triggered by change, not by the
calendar.

## Step 6 — Optional, and not on day one

```bash
bin/hook-install         # fires bin/sync when you edit a skill
```

Leave this until the hub has settled. If another skills repo already installs
its own sync hook, remove that one in the same change: two hooks race over
edits made through the same symlinks and commit to different repos.

## What you have now

`$clanker-mode` routes real work through playbooks that cite principles. Each
repo can prove its own behavior. `bin/doctor` catches drift before it ships.

Next: [The router](./02-the-router.md), or jump to
[Recipes](./08-recipes.md) if you would rather learn by doing.
