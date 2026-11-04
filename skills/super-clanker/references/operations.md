# Operations

## One daemon pass

launchd keeps `deez super-clanker daemon` alive. Each pass, about every five seconds:

1. Poll each enabled source that is due.
2. Fan out queued Triggers on subscribed Threads to their Tickets.
3. Stop Workers whose turn has run past `workers.turn_limit_minutes`, as `kill`
   does. A process whose working directory has left the Worker's worktree is not
   the Worker and is left alone. This runs before the reap, so the stopped turn is
   reaped in the same pass.
4. End the Worker of each Ticket ended by the `stop` verb while that Worker still
   runs in the Ticket's worktree or its scratch directory under `work/`: SIGTERM
   to its process group, SIGKILL after five seconds, then a sweep. `stop` itself
   only ends the Ticket; this step ends its process, before the reap and before
   step 6 removes the worktree.
5. Reap finished Worker turns into `worker` Triggers. Reaping, the `kill` verb
   and steps 3 and 4 sweep the Worker's worktree: any process whose working
   directory is the worktree or below it is sent SIGTERM, then SIGKILL after a
   three-second grace. Only the sweeping process and its parent are spared.
6. Remove the worktrees of Tickets ended by the `stop` verb, at most two per
   pass: check `git status`, sweep, then `git worktree remove` without
   `--force` in the main repository. The branch stays. A Ticket ended by a
   `dropped` report keeps its worktree, because it can still be revived. A
   worktree with uncommitted or untracked files stays and is not swept: the pass
   records an error naming it and skips it for ten minutes. Each git command
   times out after ten seconds.
7. Check free memory. Below `workers.min_free_pct` the pass is held: steps 8 to 10
   are skipped and the pass line reads `held=mem<pct>%`. The hold is logged when
   it starts and when it clears, not on every held pass. An unreadable
   `memory_pressure`, or one that takes over five seconds, does not hold.
8. Resume exited Workers that have new inputs.
9. Revive Tickets that have new inputs and whose last Assignment ended: by `kill`,
   by the turn limit, or by a final report, `dropped` included. A Ticket ended by
   `stop` stays ended.
10. Launch pending Assignments up to `workers.max_running`.
11. Ignore Triggers the gate refuses, then wake the Router if any remain.
12. Send replies: terminal ones to the inbox, forge ones through `gh` or `glab`.
13. Write the heartbeat.

The pass line counts `reaped`, `expired` (turns stopped at the limit) and
`removed` (worktrees removed).

`deez super-clanker pass` runs one pass by hand.

The daemon exits on its own when any file under `deezlib/superclanker/` changes,
and launchd starts it again on the new code. A hub update needs no `kick`.

## The board

`deez super-clanker ui` opens the board. It shows what needs you, every
Ticket, memory by process tree and the peer Claude sessions.

Start it from another machine with:

```
ssh -t dboon@dboons-mac-mini '~/github/deez-skills/bin/deez super-clanker ui'
```

The launcher puts `/opt/homebrew/bin` and `~/.local/bin` first on PATH. It
therefore works over a bare `ssh -t`.

### Windows

Outside tmux, the verb creates the tmux session `clanker` if it does not
exist, then attaches to it. The session has two windows:

| Window | Holds |
|---|---|
| `board` | The board. Inside tmux, the title reads `board(!N)` while N items need you. |
| `main` | `claude --continue`, or `claude` if there is nothing to continue. |

The session opens on `board`. Inside tmux, or with `--no-tmux`, the board runs
in the current terminal.

### Venv

The board runs Textual from a separate venv at
`~/.local/share/deez-skills/venvs/ui`. The pin is `ui_launch.TEXTUAL_PIN`,
8.2.8. The launcher builds the venv with `/opt/homebrew/bin/python3` when
it is missing or holds another Textual version. To rebuild it, run
`rm -rf ~/.local/share/deez-skills/venvs/ui`. The next `ui` run creates it
again. The hub and the daemon stay stdlib-only.

### Refresh

| Data | Every |
|---|---|
| Tickets, inbox, daemon health | 2 s |
| `ps` table, peer sessions | 5 s |
| `lsof` (Worker leftovers), `memory_pressure`, spend, Watchdog anomalies | 10 s |
| Log tab for the selected Worker | 5 s, only while the tab is open |

The board opens `super.db` read-only and never writes it. Every change goes
through a `deez super-clanker <verb>` subprocess. If the database cannot be read or is locked, the
board keeps the last good snapshot, and the header shows `STALE (<error>)`.
`refresh failed` appears only when the snapshot function itself raises. If the
state root or the database is missing, it shows `daemon not initialised`.

### Keys

The detail pane has the tabs Report, Log, Router, Memory and Sessions.

| Key | Action | Confirm |
|---|---|---|
| `a` | Focus the ask box in the Router tab (`ask`) | none |
| `r` | Answer the selected Ticket's question (`note`) | none |
| `n` | Send a note to the selected Ticket's Worker (`note`) | none |
| `enter` | Show the selected Ticket in the Report tab (`show`) | none |
| `s` | Stop the selected open Ticket. Asks for a reason first. | `y` |
| `k` | Kill the Worker of the selected Ticket. Only while it is running. | `y` |
| `t` | Take over the selected Ticket | `y` |
| `R` | Retry the selected Ticket (`retry`) | `y` |
| `Q` | Requeue the selected undecided trigger (`requeue`) | none |
| `K` | Kick the daemon (`kick daemon`) | `y` |
| `x` | Kill the selected process in the Memory tab | `y`, or a typed name |
| `escape` | Return focus to the Ticket list | none |
| `e` | Show or hide ended Tickets | none |
| `/` | Filter rows. `-` clears the filter. | none |
| `:` | Run any `super-clanker` verb | `y` for `stop`, `kill`, `retry` and `kick` |
| `?` | Show help | none |
| `q` | Quit | none |

A confirm dialog takes `y` to accept, and `n` or `escape` to cancel.
The `s` dialog warns that the worktree is removed if it is clean, and that any
process in it dies.

### Takeover

`t` asks for `y`. It kills a live Worker with `kill`, waits up to 10 s for the
process to exit, then resumes the session. In tmux, it opens `claude --resume
<session id>` in a new window named for the Ticket slug, in the worktree. Outside
tmux, the board suspends and runs the session in the same terminal.

`t` refuses when:

- the Ticket is already taken over from this board
- the Ticket has no session id or no worktree
- the Ticket is no longer on the board
- another takeover is running
- `claude` is not on PATH (checked inside tmux, before it kills anything)

A later input to the Ticket can revive a killed Worker.

### Memory kill

The Memory tab lists the largest process trees, with the trees under peer
sessions. Each row shows its group: `worker`, `peer` or `other`. `x` works only
while the Memory table has focus.

A kill is refused, and nothing is signalled, when any of these is true:

- The pid is 1 or lower.
- The process is not running.
- The protected set is unavailable. This happens when the port probe fails,
  or when the process table is newer than the protected set. The board shows
  `protection unavailable`.
- The process belongs to another user.
- The process is a Worker. Use `k`.
- The tree contains a protected process.

The protected set is:

- the board and its ancestors
- the tree of the tmux pane `clanker:main`
- any process whose command contains `super-clanker daemon` or
  `super-clanker watchdog`
- the listeners on ports 8097, 8098, 31337 and 31338

Right before it signals, the board reads a fresh process table and checks the
protection and the peer sessions again. If a peer session was added or removed
under the target, nothing is killed. The kill sends SIGTERM to every process in
the tree. After 3 s it sends SIGKILL to the survivors. If the pid now has
another command or parent, nothing is killed.

Confirmation depends on the tree:

- A tree with no peer session needs `y`.
- A tree with one peer session needs that session's name, typed exactly.
- A tree with several peer sessions needs `kill <N> sessions`, where N is the
  number of sessions.

## Backoff

After n consecutive failed wakes, the daemon waits
min(600, 30 × 2^(n−1)) seconds after the last one before waking again. The
pass line then reads `wake=backoff`. A failed wake leaves its Triggers queued.
A wake running past 600 seconds is expired.

## The Watchdog

launchd runs `deez super-clanker watchdog` every `watchdog.interval_seconds`. It wakes
its model only when the digest is not empty. The digest kinds, in order:

1. daemon down
2. unreaped turn
3. long turn
4. stalled ticket
5. unanswered question
6. undecided
7. failed wakes
8. source errors
9. orphan worktree

`deez super-clanker watchdog --digest` prints it without a model call.

## Paths

Under the state root:

| Path | Holds |
|---|---|
| `log/daemon.log` | One line per eventful pass; rotated to `daemon.log.1` past 5 MiB, one previous file kept |
| `daemon.held` | Free-memory percentage while the daemon is holding launches; empty otherwise |
| `log/launchd.err.log`, `log/watchdog.err.log` | launchd stderr for each agent |
| `log/<assignment>.json`, `.err`, `.reaped` | One Worker turn; later turns add `.<n>` |
| `inbox/terminal-<thread>.log` | Replies on a terminal Thread |
| `daemon.heartbeat`, `daemon.lock.d/pid` | Daemon liveness |
| `watchdog.session` | Resumable Watchdog session id |
| `nudge` | Written by `ask`, `note`, `reply`, Router verbs and pushed reports; the daemon starts its next pass when it changes |

## Workers config

`[workers]` in `sources.toml`:

| Key | Default | Meaning |
|---|---|---|
| `max_running` | 3 | Concurrent Workers |
| `turn_limit_minutes` | 120 | A live Worker turn older than this is stopped |
| `min_free_pct` | 30 | Free memory below this holds resume, revive and launch |

## Recovery

- **Daemon down.** Read `deez super-clanker log launchd` for the last error. Then run
  `deez super-clanker kick daemon`.
- **Stalled ticket.** Read `deez super-clanker show <ticket>` and its last report.
  Then run `deez super-clanker retry <ticket>`.
- **Unreaped turn.** Run `deez super-clanker reap`.
- **Undecided trigger.** It was recorded `unavailable`. Run
  `deez super-clanker requeue <trigger>`, and the next pass wakes the Router with it.
- **Held pass.** The pass line reads `held=mem<pct>%`. Run `memory_pressure` to
  see free memory. Launches resume on their own once it reaches
  `workers.min_free_pct`; lower the key to launch sooner.
- **Worktree that will not be removed.** The stopped Ticket's worktree has
  uncommitted or untracked files. A pass reports it as an error, then leaves it
  alone for ten minutes; the Watchdog lists it as an orphan. Inspect it, commit or
  discard what is there, and leave it: the first pass after the ten minutes
  sweeps and removes it, and any shell or editor still open in it dies then. To
  drop it by hand, run `git worktree remove --force <path>` in the main
  repository.
