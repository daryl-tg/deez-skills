# Roster ACP host launch and teardown

*Verified: 2026-10-30, branch `daryl/roster-teardown-footprint` (PR #2231, head `f7b554fbd`, cut from `origin/main` `dfefe0a21`), driven with the branch's `packages/cli/dist/om` and the installed Claude Code 2.1.314. Pending on main until the PR merges. The leak it fixes was reproduced first on the installed om 0.478.0.*

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
