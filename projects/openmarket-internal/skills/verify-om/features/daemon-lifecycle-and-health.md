# Daemon lifecycle and health

*Re-driven 2026-11-13 (nightly), tree `298c469dd7` (origin/main, v0.495.0+internal), guest lane on 18185 started through `bootstrap.internal.ts`, booted with no guest 429. `status --format json` (running, `relay.daemon: reachable`), `service status`, the wrapper's `service install` refusal, `--version` `0.495.0+internal`, and first live proof of `db-open-wait` (#2465). Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261113/r1/` (`cli/02`, `cli/08`).*

*Re-driven 2026-11-11 (nightly), tree `0ad4768f66` (origin/main, v0.494.0), guest lane on 18181, booted with no guest 429. `status`, `doctor` (the guest-lane warnings; after two badges were minted for the MCP drive it read `ok:false` on the `account` check, see the README gaps list), `service status`, `service install` refused by the wrapper, `/healthz` (`version 0.494.0`, `auth guest`, 24 lanes with `feed-heartbeat` new), `chat --once /version` (`revision` from `OM_CODE_REVISION`, `daemon 0.494.0, pid <lane>`). First live proof of `proxy-decoded-body` (#2445) on a bare lane on 18183 against a gzip upstream on 18184. Not re-driven: the env opt-out switches, the `/version` mismatch row. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261111/r1/`.*

*Re-driven 2026-11-10 (scheduled maintenance), tree `c9bc93a355` (origin/main, v0.493.1), guest lane on 18161: `env-opt-outs` first driven. `OM_TELEMETRY=off`, and `DO_NOT_TRACK=1` over `OM_TELEMETRY=on`, turned `config show`'s `telemetry.product` to `off (OM_TELEMETRY / DO_NOT_TRACK env)`; `OM_NO_UPDATE_CHECK=1` turned MCP `system_status`'s `version.update_check` from `unknown` to `opted_out`; `OM_NO_AGENT_WIRING=1` turned `doctor`'s `agent_wiring` to `opted out (OM_NO_AGENT_WIRING)`. `OM_PLAIN_CHAT` and `OM_MCP_LAZY` were not driven. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261110/r1/` (`cli/01`-`07`).*

*Re-driven 2026-11-10 (nightly), tree `c9bc93a355` (origin/main, v0.493.1), guest lane on 18143, booted with no guest 429. `status`, `doctor`, `service status`, `service restart` refused by the wrapper (exit 1), `/healthz` (`version 0.493.1`). First live proof of `version-slash` (#2428): `om chat --once /version` (`daemon  0.493.1, pid 5869`; `not running` with the lane down; `revision  nightly20261110` under `OM_CODE_REVISION`), the workspace's `/version` and `/help` rows. The mismatch row is not driven. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261110/r1/` (`cli/version*.txt`, `tui/tui-03-version.txt`).*

*Re-driven 2026-11-09 (scheduled maintenance), tree `0d3d29cd27` (origin/main, v0.493.0), bare lane on 18145 (dummy `OM_API_KEY`, dead service URLs) with a scripted fake model on 18144. `/healthz` (`version 0.493.0`, `auth device`, `last_error null`, `om_home` under `accounts/guest`), `service status`, the wrapper's `service install` refusal (exit 1), `logs --limit 5`. The guest lane on 18143 died at boot on a guest sign-in 429 (`Try again in 35 minute(s)`), the carried product gap. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261109/r1/`.*

*Re-driven 2026-11-09 (nightly), tree `5bfa0ccf6` (origin/main, v0.492.0), guest lane on 18143, booted with no guest 429. `status`, `doctor`, `service status` (`mode: foreground`), `/healthz` (`rss_mb` 381, `slow_sql: []`). Not re-driven: `logs`, the footprint line, `om run` restart behaviour. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261109/r1/` (`cli/01-04`).*

*Re-driven 2026-11-08 (nightly), tree `5590b4d1c` (origin/main, v0.492.0), guest lane on 18141, booted in 2 s with no guest 429. `status` running, `doctor` `ok:true` (binary and llm warns), `/healthz` 0.492.0 guest with `memory.rss_mb` 471 and `slow_sql: []`, the `[footprint] rss 459 MB … pressure normal` lane-log line, `control-om down`. Not re-driven: `service status`, `logs`, the profiler. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261108/r1/` (`cli/01-02`, `cli/05`).*

*Re-driven 2026-11-07 (nightly), tree `05f450fc5` (origin/main, v0.492.0), guest lane on 18141, booted with no guest 429. `status --format json` running (foreground), `doctor --format json` `ok:true` (`binary` warn only), `service status` with every loop `INACTIVE (<reason>)`, the wrapper refusing `service install` (exit 1), `logs --limit 5`, `/healthz` 0.492.0 `auth guest`, `/openapi.json` 200 (1,070,401 bytes). Not re-driven: the profiler. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261107/r1/` (`cli/10-14`, `cli/126-logs`).*

*Re-driven 2026-11-06 (nightly), tree `50fcc594b` (origin/main, v0.492.0), guest lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), booted at 19:18Z with no guest 429, host load average 10 falling to about 3.3. `doctor --format json` `ok:true` with the 14 baseline checks (`contracts` and `stream` `ok`); `/healthz` 0.492.0, `auth: guest`, `last_error: null`, `exits_unmanaged: []`, `om_home` under the lane root, `memory` 390/149/183 MiB, `slow_sql: []`; one `[footprint]` line at boot; `profile` `stacks` before start `not_started`, `x` 400 `bad_request`, two `start` calls with the same `started_at` and `already: false`; `status` and `service status` with every loop `INACTIVE (<reason>)`; `logs --limit 5` `No log lines yet`; the wrapper refused `service install` (exit 1) and `~/Library/LaunchAgents` kept its 3 openmarket entries. Evidence: `http://127.0.0.1:8098/vom-nightly-20261106/r1/` (`cli/doctor.txt`, `cli/healthz.json`, `cli/service-*`).*

*Re-driven 2026-11-05 (nightly), tree `3a0ea623e` (origin/main, v0.492.0), guest lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), booted in 2 s at 19:19Z with no guest 429, host load average about 4.4. `doctor --format json` `ok:true`, `status` running (foreground), `service status`, `logs --limit 40`, the wrapper refusing `service install` (exit 1), `/healthz` version 0.492.0 with `om_home` ending `/accounts/guest`, `/openapi.json` 200 (1,069,488 bytes). Not re-driven: the profiler. Evidence: `http://127.0.0.1:8098/vom-nightly-20261105/r1/` (`cli/doctor.out`, `cli/status.out`, `cli/healthz.json`).*

*Re-driven 2026-11-04 (nightly), tree `9acb5fb56` (origin/main, v0.491.0), guest lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), booted in 2 s at 19:19Z with no guest 429, host load average about 3.5. `doctor --format json` `ok:true`, `status` running (foreground), `service status`, `logs` (one line), the wrapper refusing `service install` (exit 1); `/healthz` `memory.rss_mb` 496 and `slow_sql: []`; the lane log's first `[footprint] rss 434 MB heap_used 140 MB heap_total 181 MB pressure normal`; `agent.log` `remote control dark: guest session`; profiler `stacks` 409 before a `start`; `/openapi.json` 200 (1,065,106 bytes). Not re-driven: profiler `start`. Evidence: `http://127.0.0.1:8098/vom-nightly-20261104/r1/` (`cli/01-02`, `cli/190-192`).*

*Re-driven 2026-11-03 (nightly), tree `777ee7f21` (origin/main, v0.488.0), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 2.8; the first `up` died on a guest sign-in 429 (35 minutes) and the lane booted in 3 s at 19:55Z. `doctor` `ok:true`, `status` running (foreground), `service status` (`Library mirror: INACTIVE (guest session)`), `logs` `{"lines":[]}`, the wrapper refusing `service install` (exit 1); `/healthz` footprint (`rss_mb` 452) and `slow_sql: []`; the lane log's first `[footprint] rss 664 MB heap_used 157 MB heap_total 194 MB pressure normal`; `agent.log` `remote control dark: guest session`; profiler `stacks` 409 `not_started`, `start` 200 twice with the same `started_at` and `already:false`, `stacks` 15 samples; `{"action":"stop"}` is refused `bad_request` (only `start` and `stacks` exist); `/openapi.json` 200 (1.06 MB). Evidence: `http://127.0.0.1:8098/vom-nightly-20261103/r1/` (`cli/50-54`, `cli/220-223`).*

*Re-driven 2026-11-02 (scheduled maintenance), tree `587ce2d0b` (origin/main, v0.480.3), lane on 18168 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 5. Boot in seconds with no 429. `doctor --format json` `ok:true`; `status` running, foreground; `/healthz` carries `memory`, `slow_sql`, `roster`, `subscriptions`; `service status` not installed, foreground pid; the wrapper refused `service restart` (exit 1). **The `[footprint]` line is on main**: `rss 396 MB heap_used 154 MB heap_total 195 MB pressure normal` at the first heartbeat. `logs --limit 20` read `No log lines yet` (a foreground lane writes to the lane log, not `runner.log`). Not driven: the profiler POSTs.*

*Re-driven 2026-11-02 (nightly), tree `2567b7974` (origin/main, v0.480.3), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 4. The first `up` at 19:23Z died the way the 2026-10-31 record describes: the boot mint was refused (one `coins` read then said `HTTP 429: Too many guest sign-ins. Try again in 15 minute(s)`), the lane printed its banner and exited `om: No OpenMarket API key configured`. After the window a fresh root booted in about 2 s with the mint landing: `/healthz` read 0.480.3, `auth: guest`, `last_error: null`, `om_home` ending `/accounts/guest`, `memory` (`rss_mb` 620), `slow_sql: []` and `roster.capabilities`; the eight `@om-core` defaults installed 4 s after boot. `control-om doctor` passed; `om doctor --format json` `ok:true` with 14 checks (`binary`, `llm`, `agent_wiring` warn; `contracts` and `stream` ok; `daemon` ok). `status` `✓ running (PID 89937) (foreground om run)`; `service status` listed the INACTIVE loops (`guest session`, `no Firecrawl key`); `logs --limit 5` printed the CLI's own `watch_remove` line and no daemon line; the wrapper refused `service install` (exit 1) and `~/Library/LaunchAgents` kept its 3 entries; the profiler answered 409 `not_started`, 400 `bad_request`, 200 `start`, `stacks` with `samples`, and a second `start` repeated the first `started_at` with `already: false`; `GET /openapi.json` 200, 137 paths, `info.version` 0.480.3. Evidence: `http://127.0.0.1:8098/vom-nightly-20261102/r1/` (`cli/35-39`, `cli/47-48`, `cli/146`).*

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
- `footprint-line` (PR #2231, on main since `3498391e7`): on the first runner heartbeat (30 s after boot) and every tenth after it (every 5 min) the daemon logs `[footprint] rss N MB heap_used N MB heap_total N MB pressure normal|warn|critical`; Linux reports `some10=N%` from `/proc/pressure/memory`, elsewhere the field is omitted.
- `status` renders the same state as a human rollup.
- `doctor` self-diagnoses the install: binary, version, home, network, key,
  schema, daemon.
- `logs` tails `runner.log` from the home.
- `db-open-wait` (#2465): an `om` process that opens the home's database while another process holds a brief lock waits for it, then succeeds, instead of failing with `database is locked`.
- `edition`: `om --version` prints `<version>+internal` from the internal entry and the bare version from a public build; the help header prints `om v<version>` either way.
- `service-guard` — the wrapper refuses lifecycle mutation on a lane, because
  the product no longer does.
- `version-slash` (#2428): `/version` in `om chat` (and `/help` on every
  surface) prints `om <version>`, then `revision`, `built`, `bun`, `platform`,
  `binary` and `daemon`. A source run reads `not embedded in this build` for
  `revision` and `built` unless `OM_CODE_REVISION` is set. `daemon` reads
  `<version>, pid <n>`, `this process` inside the daemon, or `not running`; a
  daemon on another build adds `not this om's <version>`, and a service daemon
  adds `om service restart`. No model is needed.
- `env-opt-outs` (`shared/env-vars.ts`, `shared/product-telemetry.ts:189-205`,
  `runner/update-check.ts:220`): `OM_TELEMETRY=off` or `DO_NOT_TRACK` turns
  product telemetry off (`DO_NOT_TRACK` wins over `OM_TELEMETRY=on`);
  `OM_NO_UPDATE_CHECK=1` stops update checks; `OM_NO_AGENT_WIRING` skips agent
  wiring at init and daemon start; `OM_PLAIN_CHAT=1` keeps `om chat` out of the
  TUI; `OM_MCP_LAZY` picks lazy or eager tool loading for `om mcp serve`.
- `proxy-decoded-body` (#2445, v0.494.0): a body the daemon proxies from an
  upstream that compressed it (`/api/v1/*` to the Data API, `/api/rooms/*` to
  the chat service) arrives readable, with no `Content-Encoding` and a
  `Content-Length` that matches the unpacked bytes. Before the fix the stale
  header made a browser refuse every `/api/rooms/*` read
  (`ERR_CONTENT_DECODING_FAILED`).

## How to get to it (user POV)

- Run `om run` in a terminal, or install the background service with
  `om service install`.
- Check on it with `om status`, `om doctor`, `om logs`, or the dashboard's
  header pill.
- In `om chat`, type `/version` to see which build you run and the daemon's.

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
- **Footprint line in the log.** (PR #2231, on main since `3498391e7`.) Within 60 s of `up`, `grep '\[footprint\]' .control-om/lane-<port>.log` shows one line; a second lands 5 min later. On 2026-10-30 a source lane on 18103 logged `rss 447 MB heap_used 137 MB heap_total 178 MB pressure normal` at +30 s, then at +5 min and +10 min, and `sysctl -n kern.memorystatus_vm_pressure_level` read 1 at the time, which is `normal`. A source lane writes this to the lane log, not to `runner.log`; a daemon under launchd writes it to `runner.log`.
- **Footprint and the profiler.** `curl -fsS "$(control-om url /healthz)" | jq
  '{memory, slow_sql, roster}'` shows three integer MiB values, `slow_sql: []`
  on a quiet lane, and `roster.capabilities`. Then POST JSON to
  `$(control-om url /rpc/v1/system/profile)`. The lane takes the call with no
  bearer. `{"action":"stacks"}` before any start answers 409 `not_started`,
  and `{"action":"x"}` answers 400 `bad_request`. `{"action":"start"}` answers
  200 `{started_at, already}`, and `stacks` then returns `inclusive`, `self`,
  `samples`, `seconds`, `slow_sql`, `rss_mb` and `started_at`. **A second
  `start` also says `already: false`**, with the first `started_at`
  (`runner/http/rpc/system.ts:404`), so assert on the repeated `started_at`,
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
- **The lock wait.** Hold a write lock on the lane's `om.sqlite` from `sqlite3` (`BEGIN EXCLUSIVE;`, a `CREATE TABLE IF NOT EXISTS` probe, `.system sleep 4`, `ROLLBACK;`) and run `control-om om -- config set computer.asks never` 0.2 s in. Driven 2026-11-13 on `298c469dd7`: unlocked the call took 0.93 s; locked it finished at +4.18 s, after the release, with exit 0.
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
- **`/version`.** `control-om om -- chat --once /version` runs without a
  model and prints the rows above; expect `daemon  <lane version>, pid <lane
  pid>`. Prefix `OM_CODE_REVISION=<x>` to see `revision  <x>`. With the lane
  down it reads `daemon    not running`. In the workspace, type `/version` in
  the composer: the same rows land in the transcript.
- **Opt-out switches.** `control-om om` inherits the caller's environment, so
  prefix the variable on the CLI call; `control-om up --env K=V` is only for
  the daemon's own behaviour. Run each check once without the variable as the
  control:

  ```bash
  OM_TELEMETRY=off control-om om -- config show | grep telemetry.product
  #   telemetry.product: off (OM_TELEMETRY / DO_NOT_TRACK env): …   (unset: on (default))
  DO_NOT_TRACK=1 OM_TELEMETRY=on control-om om -- config show | grep telemetry.product
  #   off (OM_TELEMETRY / DO_NOT_TRACK env)
  OM_NO_AGENT_WIRING=1 control-om om -- doctor
  #   {"name":"agent_wiring","status":"ok","detail":"opted out (OM_NO_AGENT_WIRING)"}
  #   (unset: warn, "✗ claude-code · ✗ codex · ✗ claude-desktop — no chat badge")
  ```

  `OM_NO_UPDATE_CHECK` shows only in the `system_status` action's
  `version.update_check`. `om status` (text or `--format json`) has no version
  block, and `/healthz` reads `update_available: false` either way. Call it over
  MCP stdio (see [mcp-stdio.md](mcp-stdio.md)) with and without the variable:
  `tools/call {"name":"system_status","arguments":{}}` gives `unknown` unset and
  `opted_out` with `OM_NO_UPDATE_CHECK=1`. `om status --json` printed nothing
  parseable on stdout; the verb takes `--format json`.
- **Proxied bodies (`proxy-decoded-body`).** Start a loopback upstream that
  answers one path with a gzipped JSON body plus `Content-Encoding: gzip` and
  its compressed `Content-Length`, a second path with plain JSON, and 502 for
  everything else. Boot a bare lane with `--env OM_API_KEY=om_dummy_proto --env
  OM_BASE_URL=http://127.0.0.1:<upstream>` and the other service URLs dead.
  `/api/v1/<path>` maps to `<upstream>/v1/<path>`.
  `curl -si http://127.0.0.1:<lane>/api/v1/nightly-gzip` answered 200 with no
  `Content-Encoding`, `Content-Length: 45` and the JSON in clear, while the
  upstream's own answer carried `Content-Encoding: gzip` and
  `Content-Length: 65`. The plain path kept its `Content-Length: 21`. Not
  driven: `/api/rooms/*` and attachment or Range reads.

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
- `ERROR [roster-todo] roster todo records server modes unavailable` and `ERROR [roster-watcher] roster watcher source auto room discovery failed` each repeat every 20 s on a guest lane started through `bootstrap.internal.ts` (10 of each in about 3 minutes, observed 2026-11-15 at `5a4cb146d4`). A guest has no rooms account, so the roster's ticket and room reads fail (`packages/roster/src/todo-record-watch.ts:398`, `packages/roster/src/watcher.ts:1823`). They are not a fault in the change under test; the repeat itself is a product gap (README, known product gaps).
- `[roster] om-skills defaults unavailable (registry lookup failed (404) … @om-skills/argue …); retrying in 30s` (then 60, 120 and so on, up to 30 min) is an ERROR on every fresh lane while the production registry does not list the default agents (driven 2026-10-28). `[roster-watcher] … room discovery failed` and `[roster-todo] roster todo rooms unavailable` repeat every 20 s on a guest. Neither is a fault in the change under test. See [agent creator](./agent-creator-lifecycle.md) for the install path.
- The boot log prints the bind from `OM_BIND`, but the `run` command's own
  `--help` text still says `:31337`. The text is a default, not what this lane
  is serving.
