# Operations

## One daemon pass

launchd keeps `deez super-clanker daemon` alive. Each pass, about every five seconds:

1. Poll each enabled source that is due.
2. Fan out queued Triggers on subscribed Threads to their Tickets.
3. Stop Workers whose turn has run past `workers.turn_limit_minutes`. This runs
   before the reap, so the stopped turn is reaped in the same pass.
4. Reap finished Worker turns into `worker` Triggers. Reaping, and the
   `stop` verb, sweep the Worker's worktree: any process whose working directory is the worktree or
   below it is sent SIGTERM, then SIGKILL after a three-second grace.
5. Remove the worktree of each Ticket ended by the `stop` verb: sweep it, then
   `git worktree remove` without `--force` in the main repository. The branch
   stays. A Ticket ended by a `dropped` report keeps its worktree, because it can
   still be revived. A worktree with uncommitted changes stays too: the pass
   records an error naming it and tries again after ten minutes.
6. Check free memory. Below `workers.min_free_pct` the pass is held: steps 7 to 9
   are skipped and the pass line reads `held=mem<pct>%`. The hold is logged when
   it starts and when it clears, not on every held pass. An unreadable
   `memory_pressure` does not hold.
7. Resume exited Workers that have new inputs.
8. Revive stopped Tickets that have new inputs.
9. Launch pending Assignments up to `workers.max_running`.
10. Ignore Triggers the gate refuses, then wake the Router if any remain.
11. Send replies: terminal ones to the inbox, forge ones through `gh` or `glab`.
12. Write the heartbeat.

The pass line counts `reaped`, `expired` (turns stopped at the limit) and
`removed` (worktrees removed).

`deez super-clanker pass` runs one pass by hand.

The daemon exits on its own when any file under `deezlib/superclanker/` changes,
and launchd starts it again on the new code. A hub update needs no `kick`.

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
| `router.session`, `watchdog.session` | Resumable session ids |

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
- **Expired Router session.** Every wake fails while `router.session` names a
  session `claude --resume` cannot find. Delete that file. The next wake opens
  a fresh session with the queued backlog.
- **Held pass.** The pass line reads `held=mem<pct>%`. Run `memory_pressure` to
  see free memory. Launches resume on their own once it reaches
  `workers.min_free_pct`; lower the key to launch sooner.
- **Worktree that will not be removed.** The ended Ticket's worktree has
  uncommitted changes, and each pass reports it as an error and the Watchdog as an
  orphan. Inspect it, commit or discard what is there, and the next pass removes
  it. To drop it by hand, run `git worktree remove --force <path>` in the main
  repository.
