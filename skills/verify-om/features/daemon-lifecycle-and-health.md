# Daemon lifecycle and health

The daemon is the product's spine: it boots, serves its HTTP doors, ticks, and
reports what it is doing. A user starts it (`om run` in the foreground, or
`om service` in the background), reads its state with `om status` and
`om doctor`, and tails `om logs` when something looks wrong.

## Sub-features

- `boot` brings the runner up on its bind address and prints its route summary.
- `healthz` answers with version, auth posture, tick counters, lane rows and
  loop states.
- `status` renders the same state as a human rollup.
- `doctor` self-diagnoses the install: binary, version, home, network, key,
  schema, daemon.
- `logs` tails `runner.log` from the home.
- `service-guard` — the wrapper refuses lifecycle mutation on a lane, because
  the product no longer does.

## How to get to it (user POV)

- Run `om run` in a terminal, or install the background service with
  `om service install`.
- Check on it with `om status`, `om doctor`, `om logs`, or the dashboard's
  header pill.

## Driving it with control-om

Preconditions:

- No lane running on the chosen port (`control-om doctor` says `down`).

- **Boot.** Run `control-om up`. It prints the origin within ~20s. The lane's
  own stdout — the route summary, the watches dir, every `[boot]` line — is in
  `.control-om/lane-<port>.log`.
- **Health door.** Run `curl -fsS "$(control-om url /healthz)"`. Assert
  `version`, `auth` (`guest` on a fresh lane), `pid`, `started_at`,
  `alerts_evaluated_total`, `alerts_fired_total`, `last_error: null`,
  `exits_unmanaged: []`. The `om_home` it reports is the ACCOUNT dir, not the
  root you passed: `<lane root>/accounts/guest`. Assert that it sits under the
  lane root and never under `~/.openmarket`; an equality check against
  `OM_HOME` fails on a healthy lane.
- **Human rollup.** Run `control-om om -- status`. Then
  `control-om om -- service status`, which additionally prints the Loops
  block: on a guest lane every library and gardener loop reads
  `INACTIVE (guest session)` or `INACTIVE (off (<setting>))`, which is "off, and
  why", not "stalled".
- **Self-diagnosis.** Run `control-om om -- doctor`. On a fresh lane the
  expected shape is 14 checks: `binary: warn` (dev checkout),
  `version/home/network/api_key/auth/account/schema/daemon/follows: ok`, and
  `contracts/stream/llm/agent_wiring: warn`. The `daemon` check must name the
  lane's pid — that is the check proving the CLI and the daemon agree on which
  home they are in. Four further checks are CONDITIONAL and absent from that
  baseline: `daemon_version`, which appears only when the running daemon and the
  CLI disagree — on a lane that means the tree moved after boot, and the lane
  must be relaunched before anything else is believed — `deleted packages` and
  `suspended packages`, which need registry moderation of something installed
  here, and `schedules`, which runs on every pass but emits rows only for
  unreadable or malformed files under `<home>/schedules/` (a fresh lane has no
  such directory, so it stays silent). Count 14 on a quiet guest lane and treat any of the three
  showing up as a fact about the run, not a broken baseline.
- **Logs.** Run `control-om om -- logs --limit 40`. It reads `runner.log` from
  `<lane root>/accounts/guest/`. The flag has always been `--limit`
  (`cmd/logs.ts:24`); `--lines`, which an earlier version of this file told you
  to type, never existed and fails as `unknown option`.
- **The guard.** Run `control-om om -- service install`. The WRAPPER refuses
  and exits 1; nothing reaches the product and no unit is written. Confirm with
  `ls ~/Library/LaunchAgents | grep -i openmarket`, which must still show only
  the operator's `xyz.openmarket.runner.plist`. Read-only
  `control-om om -- service status` still passes through.
- **Teardown.** Run `control-om down`, then
  `curl -fsS "$(control-om url /healthz)"` must fail and
  `lsof -nP -iTCP:18101 -sTCP:LISTEN` must be empty.
- **Proof.** Keep the `/healthz` body from before and after teardown, the
  `doctor` JSON, and the tail of the lane log.

## Gotchas

- **The product no longer refuses service lifecycle on a lane.** Before the
  accounts refactor (`3a81eb478`) a non-default home shared the machine-global
  unit label and those verbs were refused with a note naming the unit. Now a
  non-default root names a unit of ITS OWN
  (`runner/supervise/unit-name.ts:38`, read by `runner/supervise/index.ts`
  `unitIsAnotherHomes`), so `om service install` on a lane would write a second
  launchd unit that outlives the run. `om service status` no longer prints the
  old note either. The only guard is `control-om`'s — never bypass it with a
  bare `om`.
- `/healthz` serves `503` with the same body when `exits_unmanaged` is non-empty,
  a holding is unprotected, or the daemon is still booting. `curl -fsS` fails on `503`, so a run that treats
  a non-zero curl as "daemon down" will misreport a degraded daemon as a dead
  one. Read the body.
- A lane with nothing to evaluate does not tick on the interval, so
  `last_tick_at` stays at boot and the dashboard header reads `stale`. Expected.
- `[library] could not read the saved watches: registry answered 403` repeats
  every minute in the lane log. That is the guest session failing an
  authenticated registry read, not a fault in the change under test.
- The boot log prints the bind from `OM_BIND`, but the `run` command's own
  `--help` text still says `:31337`. The text is a default, not what this lane
  is serving.
