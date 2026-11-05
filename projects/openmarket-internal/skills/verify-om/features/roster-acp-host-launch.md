# Roster ACP host launch and teardown

*Re-driven 2026-11-06 (nightly), tree `50fcc594b` (origin/main, v0.492.0), guest lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), booted at 19:18Z with no guest 429, host load average 10 falling to about 3.3. `__roster-acp claude /usr/bin/true` from the source CLI exit 2 `om __roster-acp must run in its own process group (spawn it detached) or under the roster guardian.` Evidence: `http://127.0.0.1:8098/vom-nightly-20261106/r1/` (`cli/roster-acp.txt`).*

*Re-driven 2026-11-05 (nightly), tree `3a0ea623e` (origin/main, v0.492.0), guest lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), booted in 2 s at 19:19Z with no guest 429, host load average about 4.4. `__roster-acp claude /usr/bin/true` from the source CLI exit 2 `om __roster-acp must run in its own process group (spawn it detached) or under the roster guardian.` Evidence: `http://127.0.0.1:8098/vom-nightly-20261105/r1/` (`cli/roster-acp.out`).*

*Re-driven 2026-11-04 (nightly), tree `9acb5fb56` (origin/main, v0.491.0), guest lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), booted in 2 s at 19:19Z with no guest 429, host load average about 3.5. `__roster-acp claude /usr/bin/true` from the source CLI exit 2 `om __roster-acp must run in its own process group (spawn it detached) or under the roster guardian.` The teardown ladder was not driven. Evidence: `http://127.0.0.1:8098/vom-nightly-20261104/r1/` (`cli/193`).*

*Re-driven 2026-11-03 (nightly), tree `777ee7f21` (origin/main, v0.488.0), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 2.8; the first `up` died on a guest sign-in 429 (35 minutes) and the lane booted in 3 s at 19:55Z. `control-om om -- __roster-acp claude /usr/bin/true` exit 2 `om __roster-acp must run in its own process group (spawn it detached) or under the roster guardian.` The teardown ladder was not driven. Evidence: `http://127.0.0.1:8098/vom-nightly-20261103/r1/` (`cli/roster-acp.txt`).*

*Re-driven 2026-11-02 (scheduled maintenance), tree `587ce2d0b` (origin/main, v0.480.3), lane on 18168 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 5. On main. The unguarded refusal is reachable from the source CLI, with no compiled build: `control-om om -- __roster-acp claude /usr/bin/true` exits 2 with `om __roster-acp must run in its own process group (spawn it detached) or under the roster guardian.` Not re-driven on main: the detached teardown ladder and a real ACP launch, which still need the compiled daemon.*

*Verified: 2026-10-30, branch `daryl/roster-teardown-footprint` (PR #2231, head `f7b554fbd`, cut from `origin/main` `dfefe0a21`), driven with the branch's `packages/cli/dist/om` and the installed Claude Code 2.1.314. Merged to main as `3498391e7`. The leak it fixes was reproduced first on the installed om 0.478.0.*

`om __roster-acp <brain> <cli>` is the private host the daemon's roster spawns to run a coding agent over the Agent Client Protocol. The daemon wraps it in a guardian (`packages/roster/src/adapters/acp-guardian.ts`) that owns its process group. Anything else that launches the host, a rig or a hand-typed command, used to leave the Claude Code child behind when it killed the host.

## Sub-features

- `host-refusal`: in run mode a host that neither leads its process group nor carries `OM_ROSTER_ACP_GUARDED=1` exits 2 before spawning anything, with the line `om __roster-acp must run in its own process group (spawn it detached) or under the roster guardian.`
- `host-ladder`: a host that leads its group tears the group down on SIGTERM, SIGINT, SIGHUP and stdin end or close, SIGTERM first and SIGKILL 100 ms later, so a child that ignores SIGTERM dies with it.
- `guardian-marker`: the guardian sets `OM_ROSTER_ACP_GUARDED=1` on the host it spawns. `--version` mode is exempt from the refusal.

## How to get to it (user POV)

Nobody types this. A user reaches it through a roster run (see agent-creator-lifecycle.md); a rig author reaches it by spawning `om __roster-acp claude <path to claude>` and driving ACP over stdio.

## Driving it with control-om

The real surface is a spawner. The rig probe at `~/dev-notes-artifacts/om-agents-live-e2e/rig/acp-probe.ts` drives `initialize`, `authenticate` (a loopback gateway that answers 503, so no model call is made) and `session/new`, then kills the host. The driver `~/dev-notes-artifacts/om-local-perf-fixes/run-artifacts/unit1-repro.sh <om> <label>` runs it and lists survivors (`PROBE=<file>` picks the probe variant).

- **The leak, before the fix.** A probe that spawns the host without `detached: true` and calls `child.kill()`. Driven on om 0.478.0 and on the branch binary built before unit 2: 2 s after the probe exited, one Claude Code process (`--permission-prompt-tool stdio`) survived with ppid 1 and the probe's own pgid, which also shows the Agent SDK does not detach Claude Code. SIGKILL is what removes it; the 14 leaked on 2026-10-29 ignored SIGTERM for 45 s.
- **Refusal.** The same probe against the branch binary: the host wrote the refusal line and exited 2 at 0.0 s; no Claude Code process was spawned; the probe then timed out on `initialize`.
- **Ladder.** A probe that spawns `detached: true` and sends only SIGTERM to the host pid: 2 s after exit, no survivor. The fixed rig probe additionally kills the group itself.

## Gotchas

- `canonicalExecutable` refuses a symlinked CLI path; pass `realpath "$(which claude)"`.
- A probe with `--gateway` still spawns a real Claude Code process for about a second; always check `ps -axo pid,ppid,pgid,command | grep -F X-Om-Roster-Broker` afterwards and SIGKILL anything with ppid 1.
- Every run-mode host launch in the product goes through `acp-client.ts`, which spawns the guardian (or, with `registerProcess: null`, the host itself) `detached: true`; nothing in `origin/main` passes `registerProcess: null`.
