# Daemon lifecycle and health

*Re-driven 2026-11-01 (nightly), tree `7ce379c45` (origin/main, v0.480.3), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 2.9. `up` booted in about 2 s with the guest mint landing at boot; `/healthz` read 0.480.3, `auth: guest`, `memory` (`rss_mb` 689), `slow_sql: []` and `roster.capabilities`; `doctor --format json` `ok: true` (`binary` warn for the dev checkout); `status --format json` `daemon.running: true`, `control: foreground`; `service status` read `running (foreground om run)`, `Service: not installed` and the INACTIVE loops with reasons; `logs` printed `No log lines yet`; the wrapper refused `service install` (exit 1); `POST /rpc/v1/system/profile` `{"action":"stacks"}` before any start answered 409 `not_started`; `GET /openapi.json` 200 with 137 paths and `info.version` 0.480.3. New on this tree (#2223): the guest lane's `agent.log` carries one `channel_error {"surface":"remote","message":"remote control dark: guest session (sign in to drive this machine from the OM Chat cloud page)"}` line at boot, the gate that keeps a guest from dialing the session link at all; the retry ladder past it needs an account and a relay. Evidence: `http://127.0.0.1:8098/vom-nightly-20261101/r1/` (`cli/00-19c`).*

*Re-driven 2026-10-31 (nightly), tree `dfefe0a21` (origin/main, v0.480.2), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 1.6. The first `up` of the night died: the guest sign-in was rate-limited (429) and the daemon exited after its banner with `om: No OpenMarket API key configured` (see the settle bullet below and the README's product gaps); 52 minutes later `up` booted in 2 s. `/healthz` read 0.480.2, `auth: guest`; `doctor --format json` `ok: true`; `status` read `✓ running (PID …) (foreground om run)`; `service status` read `running (foreground om run)`, `Service: not installed`; `logs --limit 3` printed `No log lines yet`; the wrapper refused `service install` (exit 1); `POST /rpc/v1/system/profile` with `action: stacks` before any start answered 409 `not_started`. Evidence: `http://127.0.0.1:8098/vom-nightly-20261031/r1/` (`cli/20-26`, `cli/89f`).*

*Re-driven 2026-10-30 (scheduled maintenance), tree `3cb50a821` (origin/main, v0.478.0), fresh lane on 18165, host load average about 140. `doctor --format json` passed 14 checks; `status` read `running:true`; `/healthz` read 0.478.0 with `om_home` ending `/accounts/guest`; `logs --limit 3` printed `No log lines yet (…/runner.log is empty or missing)`, because the foreground lane writes `.control-om/lane-<port>.log`. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261030/r1/` (`cli/31-doctor.json`).*
*Re-driven 2026-10-30 (nightly, smoke depth), tree `3cb50a821` (origin/main, v0.478.0), lane on 18163, under a host load average near 150. `status --format json` read `daemon.running: false` and `doctor` returned `ok:false` with 14 checks. The `daemon` check failed with `not installed — 1 event watch is not being monitored`, while `/healthz` answered 200 in 2 to 3 s and the dashboard and stream worked. That misread is the CLI's daemon probe timing out (see Gotchas). The other non-ok checks were the expected guest warnings: `binary`, `llm` and `agent_wiring`. `contracts` read `the registry speaks contracts 5.43.0; this om speaks 5.43.0`. Evidence is local only (the `8098` renderer did not answer): `artifacts/vom-nightly-20261030/r1/`.*

*Re-driven 2026-10-29 (scheduled maintenance, smoke depth), tree `7ec575e55` (origin/main, v0.467.0 plus #2194), fresh lane on 18161. `status` (running, foreground `om run`), `doctor` (`ok:true`, binary warn for a dev checkout), `service status` (not installed) and `config show` (masked key). `logs` takes `--limit <n>` (default 5); `--lines` is refused as an unknown option. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261029/r1/`.*

*Re-driven 2026-10-29 (nightly, smoke depth), tree `32ca0d6c7` (origin/main, v0.467.0), lane on 18103: `status`, and `doctor` with 14 checks (`binary`, `llm` and `agent_wiring` warn, as expected for a guest). `contracts` was ok with the detail `the registry speaks contracts 5.42.0; this om speaks 5.43.0`. Also `service status` (loops INACTIVE with reasons) and the `/healthz` keys, still including `memory`, `slow_sql` and `roster`. A profiler `start` sent twice still returned `already: false` with the first `started_at` (product gap). `{"action":"stop"}` is refused `bad_request`: the route takes only `start` and `stacks`. Other steps keep the record below. Evidence: `http://127.0.0.1:8098/vom-nightly-20261029/r1/`.*

*Re-driven 2026-10-28 (scheduled maintenance, smoke depth), tree `186030b63` (origin/main): `status`, `doctor`, `service status` and `logs --limit 5` on 18143, and boot on two more homes. The 18144 boot died at the guest-mint 429 (see [market data reads](./market-data-reads.md)); 18145 booted. The new `control-om doctor` `api key` line was driven on an expired and a valid home. Steps not named here keep the record below. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261028/r1/`.*

*Verified: 2026-10-28, tree `a8fa10974` (origin/main, v0.466.0), lanes on 18103 and 18104. `/healthz` returned 0.466.0, `auth: guest`, `last_error: null` and `exits_unmanaged: []`, with `om_home` ending `/accounts/guest` and the `memory`, `slow_sql: []` and `roster` keys. Doctor ran 14 checks: binary, llm and agent_wiring warned, and contracts and stream were ok. `status` and `service status` showed the INACTIVE Loops, including `paper-exits INACTIVE (no open paper lots)`. `logs --limit 5` printed the empty-file line. The profiler answered 409, 400 and 200; a second `start` returned the first `started_at` with `already: false` again. The wrapper refused `service install` (exit 1), and `~/Library/LaunchAgents` was unchanged. The lane log now carries the `[roster] om-skills defaults unavailable … retrying in Ns` ERROR (see Gotchas). Not driven: `?lite=1`, the boot-time guest-mint failure, the 503 branch, a real slow statement and the `counters.symbol_directory_*` keys (#2173, which need `OM_DATA_TRANSPORT=v3` on `up`). Previous stamp `8fe6a8432` is an ancestor (10 commits).*

The daemon is the product's spine: it boots, serves its HTTP doors, ticks, and
reports what it is doing. A user starts it (`om run` in the foreground, or
`om service` in the background), reads its state with `om status` and
`om doctor`, and tails `om logs` when something looks wrong.

## Sub-features

- `boot` brings the runner up on its bind address and prints its route summary.
- `healthz` returns the full runtime view, including version, auth, tick counters,
  lanes, loops, stalls, subscriptions and contributed status fields.
  `/healthz?lite=1` returns a small presence payload (`pid`, `version`,
  `started_at`, `stalls`). Runtime-specific fields depend on active planes.
  Since v0.466.0 the full body also carries `memory` (`rss_mb`,
  `heap_used_mb`, `heap_total_mb`), `slow_sql` (the newest 10 statements over
  `OM_DB_SLOW_MS`, default 100; `0` turns timing off) and `roster`
  (`{capabilities}`, or `null` when the roster is not wired).
- `profile` — `POST /rpc/v1/system/profile` arms an on-demand sampling profiler
  (`{"action":"start"}`) and reads it back (`{"action":"stacks"}`). There is no
  CLI verb.
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
  `version`, `auth`, `pid`, `started_at`,
  `alerts_evaluated_total`, `alerts_fired_total`, `last_error: null`,
  `exits_unmanaged: []`. The `om_home` it reports is the ACCOUNT dir, not the
  root you passed: `<lane root>/accounts/guest`. Assert that it sits under the
  lane root and never under `~/.openmarket`; an equality check against
  `OM_HOME` fails on a healthy lane.
- **Footprint and the profiler.** `curl -fsS "$(control-om url /healthz)" | jq
  '{memory, slow_sql, roster}'` shows three integer MiB values, `slow_sql: []`
  on a quiet lane, and `roster.capabilities`. Then POST JSON to
  `$(control-om url /rpc/v1/system/profile)`. The lane takes the call with no
  bearer. `{"action":"stacks"}` before any start answers 409 `not_started`,
  and `{"action":"x"}` answers 400 `bad_request`. `{"action":"start"}` answers
  200 `{started_at, already}`, and `stacks` then returns `inclusive`, `self`,
  `samples`, `seconds`, `slow_sql`, `rss_mb` and `started_at`. **A second
  `start` also says `already: false`**, with the first `started_at`
  (`runner/http/rpc/system.ts:403`), so assert on the repeated `started_at`,
  not on `already`. Driven 2026-10-27 at `8fe6a8432`. The profiler stays armed
  until the lane stops.
- **Human rollup.** Run `control-om om -- status`. Then
  `control-om om -- service status`, which additionally prints the Loops
  block: on a guest lane every library and gardener loop reads
  `INACTIVE (guest session)` or `INACTIVE (off (<setting>))`, which is "off, and
  why", not "stalled".
- **Self-diagnosis.** Run `control-om om -- doctor`. On a fresh guest lane this drive returned 14 checks. Contributed checks can
  append conditionally, so treat 14 as this baseline rather than a fixed schema: `binary: warn` (dev checkout),
  `version/home/network/api_key/auth/account/schema/daemon/follows: ok`, and `llm/agent_wiring: warn`.
  `contracts` and `stream` are environment-dependent, not guest-dependent: they
  warn when the registry is unreachable and read `ok` when it answers, so do not
  treat either value as a finding. The `daemon` check must name the
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
- **Give the lane time to settle before you judge it, and do not assume how
  much.** On a fresh lane the daemon's guest mint can FAIL at boot and recover
  by itself. Driven at v0.434.0: at t+0 the lane log carried
  `ERROR [boot] no API key and guest mint failed; reads retry minting per tick`,
  `/healthz` read `auth: "none"`, and `om doctor` returned **`ok: false`** with
  `api_key: fail`; by t+99s `/healthz` read `auth: "guest"` and doctor was
  `ok: true`. This is the designed path, not a fault: boot makes exactly one
  bounded mint attempt and, per its own source comment, logs and continues
  rather than crash-looping the supervisor, leaving `ensureCredential()` on a
  later pass to retry. **That recovery no longer happens on a keyless home:**
  driven 2026-10-31 at `dfefe0a21` and at `3cb50a821`, a lane whose boot mint
  was refused (guest sign-in 429) printed the start banner and then exited 1
  with `om: No OpenMarket API key configured`, because the roster's start
  needs the rooms config (README, known product gaps). `control-om up` reports
  `lane died during boot`; the only recovery is to wait out the window and
  `up` again. The v0.434.0 observation below describes a boot whose mint
  failed but the roster did not throw. **Nothing bounds how long that takes** — there is no
  backoff or SLA constant; recovery lands whenever a background pass retries and
  the auth service answers. So 99s is one observation, not a budget: poll until
  it settles rather than asserting at any fixed moment.
- **One credential file, two independent minters — and doctor is a pure read.**
  In that same window `om coins` returned live market data while the daemon
  reported `api_key: fail`. They are not separate credential systems: there is
  one `credentials.json` per `OM_HOME`, and every data read — a one-shot CLI
  process, stdio MCP, the per-tick daemon client — calls `ensureCredential()`
  for ITSELF, so a CLI command races its own mint and writes the shared file.
  `/healthz`'s `auth` and doctor's `api_key` never mint; they report whatever
  the store held at the instant they read it. So a `fail` there is a snapshot,
  not a verdict on the machinery, and a CLI mint that succeeds alongside it
  shows up on the daemon's NEXT read rather than fixing the one you already
  saw.
- **Logs.** Run `control-om om -- logs --limit 40`. It reads `runner.log` from
  `<lane root>/accounts/guest/`. **On a `control-om` lane the daemon never
  writes that file**: the lane runs `om run` in the foreground, so its own
  lines go to `.control-om/lane-<port>.log`. Read that file for boot,
  subscription and hold lines. What `runner.log` holds depends on what CLI
  processes have run. On a lane no CLI command has logged to, it prints
  `No log lines yet (<home>/runner.log is empty or missing).` (driven at
  `db6e76ef5`). After a CLI command that logs, it prints that command's lines.
  Driven at `42d044b02`, after two `watch remove` calls, it returned exactly
  `INFO [watching] removed <slug> (watch_remove, spec store)` twice. Assert that
  no daemon line (`[boot]`, `[subscriptions]`) appears there, not that the file is
  empty. The flag has always been `--limit`
  (`cmd/logs.ts:24`); `--lines`, which an earlier version of this file told you
  to type, never existed and fails as `unknown option`.
- **The guard.** Run `control-om om -- service install`. The WRAPPER refuses
  and exits 1; nothing reaches the product and no unit is written. Confirm with
  `ls ~/Library/LaunchAgents | grep -i openmarket` taken before and after:
  the list must not change. Do not expect a single file. On this machine it
  already holds the operator's `xyz.openmarket.runner.plist`,
  `com.openmarket.mcp-operator.plist` and
  `com.openmarket.chat-review-server.plist` (driven 2026-10-23). Read-only
  `control-om om -- service status` still passes through.
- **Teardown.** Run `control-om down`, then
  `curl -fsS "$(control-om url /healthz)"` must fail and
  `lsof -nP -iTCP:18101 -sTCP:LISTEN` must be empty.
- **Proof.** Keep the `/healthz` body from before and after teardown, the
  `doctor` JSON, and the tail of the lane log.

## Gotchas

- **On a busy host, the CLI reads a live lane as down.** `status` (`running:false`), `doctor` (`daemon: fail`), `notis` (`this home's daemon is unavailable`) and the chat footer (`om not running ✗`) all ask `/healthz` with a 200 ms plus 1 s budget (`runner/client.ts:87-91`). Driven 2026-10-30 at load average about 150, when `/healthz` took 2 to 3 s. Time `curl -w '%{time_total}' $(control-om url /healthz)` before reading any of those as a regression.
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
- **Fresh-lane log noise at `7ec575e55` (2026-10-29, scheduled maintenance,
  lane 18161).** Neither of the next two entries' lines appeared in 109 log
  lines. The roster logged `INFO [roster] om-skills defaults installed 8
  package(s)` about 4 s after boot, and the library 403 line never showed.
  Instead, each watch and each paper desk produces a repeating `ERROR [library]
  library: where <slug> runs was not reported yet: 404: no such device`, 22 in
  about 4 minutes for `lane-probe` and `paper-desk-<id>`. A guest lane has no
  device record, so this is not a fault in the change under test. One `ERROR
  [outbox] terminal prune failed: database is locked` also appeared once. It is
  unexplained and recorded as an observation, not a gap.
- `[library] could not read the saved watches: registry answered 403` repeats
  every minute in the lane log. That is the guest session failing an
  authenticated registry read, not a fault in the change under test.
- `[roster] om-skills defaults unavailable (registry lookup failed (404) … @om-skills/argue …); retrying in 30s` (then 60, 120 and so on, up to 30 min) is an ERROR on every fresh lane while the production registry does not list the default agents (driven 2026-10-28). `[roster-watcher] … room discovery failed` and `[roster-todo] roster todo rooms unavailable` repeat every 20 s on a guest. Neither is a fault in the change under test. See [agent creator](./agent-creator-lifecycle.md) for the install path.
- The boot log prints the bind from `OM_BIND`, but the `run` command's own
  `--help` text still says `:31337`. The text is a default, not what this lane
  is serving.
