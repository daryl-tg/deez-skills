---
name: super-clanker
description: "Operate or extend super-clanker, the local Router that turns events into clanker-mode Workers. Load to ask it for work, read status, take over a Worker, or change policy."
---

# super-clanker

super-clanker is a local Super-agent Router above **clanker-mode**. It takes
as little of the operator's attention as it can and gives back as much value.
It is continuous across the terminal, GitHub, GitLab and OM Chat, productive on
many Tickets at once, proactive under written rules, and persistent across
restarts. Each Worker is a clanker-mode lead for one Ticket.

## Talk to it

`deez` is `~/github/deez-skills/bin/deez`. Put that `bin` on PATH or spell the
path out; the daemon already does so for the Router and the Workers.

- `deez super-clanker ask <text>` hands the Router a request on the terminal thread.
- `deez super-clanker status` lists Tickets, last reports and what needs attention.
- `deez super-clanker inbox` prints the Router's replies on the terminal thread.
- `deez super-clanker show <id>` prints one object and the ids of its neighbours.

## Operate it

- `init [--force]` writes a first `sources.toml` and the example rule.
- `install [--apply] [--state <dir>]` plans or applies the daemon and Watchdog agents.
- `pass` runs one daemon pass and prints its line.
- `daemon` runs passes until stopped. launchd runs it.
- `watchdog [--digest]` ticks the Watchdog, or prints its anomaly digest.
- `retry <ticket>` ends a stalled assignment and queues a fresh one.
- `requeue <trigger>` puts a decided trigger back in the Router's queue.
- `kill <assignment>` stops a Worker process.
- `kick [daemon|watchdog]` restarts that launchd agent.
- `log <daemon|launchd|watchdog|id> [--lines N]` prints the tail of a log, a
  Worker turn's result and stderr, or a wake's or tick's result.
- `rules [<name>]` lists the policy rules or prints one.
- `policy set <rule> --mode <off|observe|auto>` changes one rule's mode.

State lives in `~/.local/state/deez-skills/super/`, or in `$DEEZ_SUPER_STATE`.
It holds `super.db`, `log/`, `inbox/` and `worktrees/<repo>/<ticket>`. Ticket
notes live in `~/Documents/dev-notes/<slug>/`.

## Take over a Worker

After `kill`, or once the Worker's turn has ended, read the session id from
`deez super-clanker show a_…`. In the Worker's worktree, run
`claude --resume <session id>`.

Every process in that worktree dies on `kill`, on `stop`, and when a later turn
of the Ticket is reaped, your shell, editor and `claude --resume` included.
Leave the worktree before you run `stop` or `kill`.

## Change the policy

In `sources.toml`, `[accept]` holds `mode` and `policy_version`. `[router]`
holds the model and the wake and reply limits. `[workers]` holds the model,
`max_running`, `turn_limit_minutes` and `min_free_pct`. `[watchdog]` holds its
model, interval and thresholds. Each
`[sources.<name>]` holds `enabled`, `mode`, `senders`, `bots`, `scopes`,
`mentions` and `poll_seconds`.

A rule is `policy/rules/<name>.md`: a title line, then `mode: off`, `observe`
or `auto`. Every rule starts in `observe`. Promote one to `auto` only after
reading the `would accept` decisions it recorded.

## What never happens

- A Worker never pushes, opens a review, posts or merges. It stops at a
  verified local candidate, per **principle-visual-approval-gates-delivery**.
- A Worker proceeds on reversible work without asking and reports `waiting`
  before anything outward-facing, per **principle-never-block-on-reversible-work**.
- The Router never edits code. It decides and dispatches.
- Inferred work starts in observe mode.
- A branch is never deleted. Removing an ended ticket's worktree leaves its branch.

## References

- [Domain](references/domain.md): objects, ids, state machines.
- [Authorization](references/authorization.md): the gate, modes, the `waiting` loop.
- [Operations](references/operations.md): the pass, the Watchdog, logs, recovery.
- [Example rule](references/rules/silent-repro.md), which `init` copies.
