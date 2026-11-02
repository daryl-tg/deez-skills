# Operations

## One daemon pass

launchd keeps `deez super daemon` alive. Each pass, about every five seconds:

1. Poll each enabled source that is due.
2. Fan out queued Triggers on subscribed Threads to their Tickets.
3. Reap finished Worker turns into `worker` Triggers.
4. Resume exited Workers that have new inputs.
5. Launch pending Assignments up to `workers.max_running`.
6. Ignore Triggers the gate refuses, then wake the Router if any remain.
7. Send replies: terminal ones to the inbox, forge ones through `gh` or `glab`.
8. Write the heartbeat.

`deez super pass` runs one pass by hand.

## Backoff

After n consecutive failed wakes, the daemon waits
min(600, 30 × 2^(n−1)) seconds after the last one before waking again. The
pass line then reads `wake=backoff`. A failed wake leaves its Triggers queued.
A wake running past 600 seconds is expired.

## The Watchdog

launchd runs `deez super watchdog` every `watchdog.interval_seconds`. It wakes
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

`deez super watchdog --digest` prints it without a model call.

## Paths

Under the state root:

| Path | Holds |
|---|---|
| `log/daemon.log` | One line per eventful pass |
| `log/launchd.err.log`, `log/watchdog.err.log` | launchd stderr for each agent |
| `log/<assignment>.json`, `.err`, `.reaped` | One Worker turn; later turns add `.<n>` |
| `inbox/terminal-<thread>.log` | Replies on a terminal Thread |
| `daemon.heartbeat`, `daemon.lock.d/pid` | Daemon liveness |
| `router.session`, `watchdog.session` | Resumable session ids |

## Recovery

- **Daemon down.** Read `deez super log launchd` for the last error. Then run
  `deez super kick daemon`.
- **Stalled ticket.** Read `deez super show <ticket>` and its last report.
  Then run `deez super retry <ticket>`.
- **Unreaped turn.** Run `deez super reap`.
- **Undecided trigger.** It was recorded `unavailable`. Run
  `deez super requeue <trigger>`, and the next pass wakes the Router with it.
- **Expired Router session.** Every wake fails while `router.session` names a
  session `claude --resume` cannot find. Delete that file. The next wake opens
  a fresh session with the queued backlog.
