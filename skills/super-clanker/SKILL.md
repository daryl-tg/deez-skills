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
- `deez super-clanker tell <ticket> --text <text>` sends your message straight to
  that Ticket's Worker and revives it if it is idle. The Router's `note` only
  queues a fact for the Worker's next run.
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
- `ui [--state <dir>] [--no-tmux]` opens the board, a terminal screen that
  lists what needs you, every Ticket, memory by process tree and the peer
  Claude sessions. It acts through the verbs above. See "The board" in
  [Operations](references/operations.md).
- `center [--state <dir>]` opens the command center. It shows the Tickets as a
  table, a kanban or a graph, with each Ticket's full dossier, the system tape
  and the Router thread. Its input runs `ask`, or `note` for the selected
  Ticket. `ctrl+v` attaches the image on the clipboard (a screenshot or a
  copied image file), and a dropped image file attaches too. A multi-line
  paste is kept whole. Attachments show as chips; backspace on an empty box
  drops the last one. Images are saved under `<state>/attachments/` and sent
  as paths the Worker opens. It reloads from the state every 2 seconds. A red strip counts stale
  Tickets: `ready` and untouched for 6 hours, waiting on you for 3 days, quiet
  for a day, or `dropped` a day ago with the worktree kept. `a` archives them
  all after a `y`; `r` reviews them one at a time (archive, keep or skip). Kept
  Tickets stay off the strip until they move again.
- The command center counts tokens, not dollars: per Ticket, every model its
  Worker used across all runs (fresh input, cache reads, output), plus the run
  in flight read from the Worker's session transcript. `tokens today` adds the
  Router's wakes.
- `archive <ticket> --reason <text> [--by <person>]` ends a Ticket with the
  outcome `archived`, so the daemon removes its worktree if it is clean.
- A Ticket whose Worker reported `ready` with an open pull or merge request is
  `TO MERGE` in the command center: a cyan `⇡` and `PR #n` or `MR !n` in the
  table, its own kanban lane, and a `to-merge` count in the status strip. `o`
  opens the selected Ticket's review in the browser.
- A merged review closes its Ticket by itself. Every 2 minutes the daemon asks
  `gh` or `glab` about each open Ticket's pull or merge request link. A merged
  one ends the Ticket with outcome `merged` and replies on a terminal thread.
- The daemon removes an ended Ticket's worktree or `work/<ticket>` scratch
  directory (stopped, archived or merged; never a dropped one, which may be
  revived) when nothing would be lost: no uncommitted files and, unless merged,
  no commit that is on no remote. Branches stay.

State lives in `~/.local/state/deez-skills/super/`, or in `$DEEZ_SUPER_STATE`.
It holds `super.db`, `log/`, `inbox/` and `worktrees/<repo>/<ticket>`. Ticket
notes live in `~/Documents/dev-notes/<slug>/`.

## Take over a Worker

After `kill`, or once the Worker's turn has ended, read the session id from
`deez super-clanker show a_…`. In the Worker's worktree, run
`claude --resume <session id>`.

On the board, select the Ticket and press `t`. The board kills a live Worker,
then opens `claude --resume <session id>` in a new tmux window in the
worktree. Outside tmux, it opens the session in the board's own terminal.

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

- A Worker never merges, pushes the default branch or posts. It carries a
  verified change to a pull request or merge request, ready for review, and
  reports `ready` with its URL. A mandate that forbids pushing, or a playbook
  that needs the operator's visual approval first, stops it short of the review,
  per **principle-visual-approval-gates-delivery**.
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
