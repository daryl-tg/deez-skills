# A quiet feed is told once, and a rule reads a feed

*Verified: 2026-11-20, merged main `2d01b6b5d4` (#2642), real relay `9199a77`, in real time. Lane on 18161, hand-started on `bootstrap.internal.ts`, signed in to the made-up account `@rig`, with a webhook listener as the channel. Driven, 10 of 10 claims: one `Quiet:` and one `Back:` notice per feed across twelve 300 s passes and a restart, the 24 h first-sight rule, a watch's own feed left untold, `feeds.quiet_notices off`, one relay listing per pass, `observed_cadence_s` and `late_s`, a timer check reading a feed and firing once per reading, the assistant's `create_watch` with `feed_check` behind the owner's card, both money guards, and the job recipes served in three places and run against the rig. No model call. Stand-ins: the key check and the rooms relay for the assistant path only. Not driven: the 24 h edge itself, the providers' own schedulers, the host name `relay.openmarket.xyz`. One defect outside the claims is recorded in [timer-data-check.md](timer-data-check.md). Evidence root `~/Documents/dev-notes/om-2026-11-20-e2e-verify/run-artifacts/s5/` (`evidence/`, `rig/`). Gallery `http://127.0.0.1:8098/om-1120-e2e/s5/`.*

An assistant's job pushes numbers into an `agent.*` feed on a cadence. When the feed goes quiet the owner hears once, and once more when it is back. A timer check can read a feed's newest reading and fire once per reading, with no model call. An assistant can set such a rule up, but only behind the owner's card. The hosted guide and both chart skills carry one recipe per provider for running the job.

## Sub-features

- `quiet-notice`: a feed with a cadence that the relay lists as stale gets one notice: `Quiet: @<scope>/<name>, no reading for 10 min (expected every 1 min).`
  - Nothing is sent at lagging, and nothing more at stale to offline.
  - The notice is a `notis_notices` row titled `Feed quiet`, one outbox row delivered in 1 attempt, and one post to the channel.
  - `watching_overview` shows the same line under attention while the feed is quiet.
- `back-notice`: the first pass that sees the feed live again sends `Back: @<scope>/<name>.`, titled `Feed back`, once. The attention line goes.
- `first-sight`: a feed first seen stale with a reading 16 minutes old is told in that pass. One first seen stale with a reading 25 h old gets standing `{quiet: true, told: false}`, no notice, and no `Back:` line later. The rule's edge is 24 h.
- `daemon-feeds-skipped`: a `watch.*` feed never enters the standing and gets no notice.
- `switch`: `om config set feeds.quiet_notices off`. Passes then send nothing, read no listing, and wipe the standing. The loop reads `inactive`, reason `feeds.quiet_notices is off`.
- `one-listing-per-pass`: each pass with notices on makes exactly one `GET /api/v2/feeds?scope=%40<scope>` on the relay and no other relay request.
- `restart`: the standing survives a restart. The boot pass tells no feed twice.
- `cadence-facts`: `om feed show` and `om series feeds` answer `observed_cadence_s` and `late_s`. Their meaning is in [account-feeds.md](account-feeds.md) (`show`).
- `feed-rule`: a timer check whose read names a feed, `read: {"<key>": {"feed": "@<scope>/<name>"}}`. The recipe and the slot rows are in [timer-data-check.md](timer-data-check.md) (`feed-read`).
- `assistant-feed-check`: `change create_watch` with `feed_check {feed, key, op, value, every}` answers `daemon_asks_you`. The card and the door are in [assistant-bridge-and-wakes.md](assistant-bridge-and-wakes.md).
- `money-guards`: `watching_agent_feed_money` and `feed_money_read`. Both are in [account-feeds.md](account-feeds.md).
- `job-recipes`: the section `Run a job on your assistant's computer` has rows for Grok Bot, a Claude Code cloud scheduled task, and Hermes or OpenClaw. It is served by the hosted `/llms.txt`, the hosted `skill_read chart-actions` and the daemon `skill_read chart-actions`.
  - Grok Bot: a routine calls `feed_append` on `agent.<name>`. No key.
  - The other two: POST `{"rows": [[stamp, v1, …]]}` to `…/api/v2/feeds/@<user>/<name>/rows` with the push key from `om feed key`.

## How to get to it (user POV)

- Nothing to run for the notices. They are on by default and arrive on the home's default channel.
- `om config set feeds.quiet_notices off` to stop them.
- `om feed show @<you>/agent.<name>` to read how late a feed is.
- Ask an assistant connected to the hosted om face to "tell me when my step count drops below 5000", then `om approve <id>`.

## Driving it with control-om

### The rig

Every script is in the evidence root's `rig/` folder. The relay harness makes its own keys and `relay/creds.json` at start.

| Port | Piece | Script |
| --- | --- | --- |
| 18161 | om lane, internal entry, hand-started | `bin/lane-up`, `bin/lane-down` |
| 18162 | relay harness on the real relay tree | `bin/relay-up` |
| 18163 | mongod 8.2.6 replica set | `bin/mongo-up` |
| 18164 | key-check gateway stand-in | `gateway.ts` |
| 18165 | rooms relay stand-in | `wsrelay.ts` |
| 18166 | hosted om face from source | `bin/hosted-up` |
| 18168 | webhook listener, logs to `logs/hook.jsonl` | `hook.ts` |

1. Edit `rig/env.sh` first. `RIG`, `RIG_SP`, `RIG_OM` and `RIG_RELAY_TREE` name this run's scratchpad and worktrees, and several scripts import the om tree by absolute path.
2. `bin/mongo-up`, `bin/relay-up`, `bun hook.ts`, then `bin/lane-up`. It seeds the made-up account with `lane-seed.ts` and starts `bootstrap.internal.ts run`.
3. `bin/om <args>` is the CLI on the internal entry with the lane's `OM_HOME` and `OM_BIND`.
4. `bin/om setup webhook --name desk --webhook-url http://127.0.0.1:18168/hook --allow-private-network`.
5. Hold `caffeinate -i -s -t <seconds>` for the drive and stop it after.
6. Only the assistant path needs `gateway.ts`, `wsrelay.ts` and `bin/hosted-up`.

### Time

The quiet loop has no interval switch. A pass runs at boot and every 300 s (`HOUSEKEEPING_INTERVAL_MS`, `packages/cli/src/runner/index.ts:626`). Plan the drive around real passes.

- Push old stamps as rows: `bin/om feed append agent.<name> --rows '[[<old ts>,50]]' --columns mood --cadence 1m`. The real relay's own rule then moves the feed: lagging past 2 cadences, stale past 10, offline at 900 s of silence.
- Never backdate a store.
- `passpoll.sh <out>` logs each change of `/healthz` `lanes["feed-quiet"].next_due_at` and the loop's verdict. `standpoll.sh <out>` logs each change of the standing and the notice count.

### Quiet, back, and the feeds that are not told

1. `bin/om feed append agent.<quiet> --values '{"mood":44}' --cadence 1m --title '<t>'`, push once more, then stop.
2. Before the first pass, make a feed with one row 25 h old and one with a row 12 minutes old (`--rows`, `--cadence 1m`).
3. Make a watch's own feed: `bin/om watch create '<label>' --slug <slug> --inbound --cadence 1m --column v`, and push one row.
4. Read each pass with `c1-dump.sh`. It prints the `feed_quiet` rows of `notis_notices`, the outbox rows and the listener's `Feed` posts.
5. See the 12-minute feed told at the first pass, the 25 h feed not told, and the `agent.<quiet>` feed told at the pass after it turns stale, about 10 minutes after its last push.
6. See no notice for the `watch.*` feed, though the relay lists it stale and then offline.
7. Push to the quiet feed again. The next pass sends one `Back:` line. The pass after sends nothing.
8. The standing is `meta` key `feeds.quiet_standing` in the lane's sqlite. A notice's `origin_id` is `feed_quiet:<address>:<ms>`.
9. `bin/lane-down`, `bin/lane-up`. The boot pass sends nothing.

### The switch

1. `bin/om config set feeds.quiet_notices off`. Append a new feed that is already stale.
2. Wait two passes. See no notice row, no post, standing `{}`, and `/healthz` `loops[]` reading `{"name":"feed-quiet","verdict":"inactive","reason":"feeds.quiet_notices is off"}`.
3. The relay log has no `GET /api/v2/feeds?scope=%40rig` at those passes.
4. `bin/om config set feeds.quiet_notices on`. The next pass tells every quiet feed.

### One listing per pass

`bun c5-table.ts <passpoll out> logs/relay-requests.log <standpoll out>` matches each pass to the relay's listing reads. The daemon's reads show as `scope=%40rig`, a hand `curl` as `scope=@rig`, which separates the two.

### Cadence and lateness

1. `bin/om feed append agent.<name> --rows '<six rows 120 s apart, the last 300 s old>' --columns load --cadence 1m`.
2. `bin/om feed show @rig/agent.<name> --format json`. See `observed_cadence_s: 120` and `late_s` equal to now minus `last_ts` minus 60.
3. A live feed carries no `late_s`. A one-row feed has `observed_cadence_s: null`.

### The job recipes

1. `curl http://127.0.0.1:18166/llms.txt` and find the section. Read `skill_read {name: "chart-actions", section: "Run a job on your assistant's computer"}` on the hosted face (`hmcp.ts`) and over MCP stdio on the lane (`mcp-stdio.ts`).
2. Claude Code and Hermes rows: `bin/om feed key agent.<name> --yes --format json`, then POST a row to the relay harness with `Authorization: Bearer <key>`. See 200 and the row. A wrong key answers 401.
3. Grok Bot row: `change {"name":"feed_append","args":{"name":"agent.<name>","values":{…},"cadence":"5m"}}` through the hosted face. See the feed on the relay.

## Gotchas

- **Off then on re-tells.** The off passes wipe the standing, so the first pass after `on` told seven feeds, four of which had been told once already. Evidence `evidence/c4-digest.txt`.
- **A watch's feed going quiet tells nobody.** The claim's reason is that watch status covers it. Here the watch row in `watching_overview` read `live` for an hour while its declared 1 m feed was offline. Evidence `evidence/c3-watch-status.txt`.
- The daemon log has no line for a quiet notice. It shows `[outbox] drained sent=N` at the telling pass. The text is in `notis_notices`, the outbox and the channel.
- `/healthz` `lanes["feed-quiet"].last_pass_at` stays `null` after 12 passes. `next_due_at` and `loops[].lastBeatAt` move.
- The hosted guide writes the POST address with no scheme (`relay.openmarket.xyz/api/…`). Both skills write `https://`. No recipe names the header for the push key. `Authorization: Bearer <key>` worked.
- A 1 m feed check beside a slower job warns after every gap. See [timer-data-check.md](timer-data-check.md).
- `control-om doctor` exits non-zero on a hand-started lane for `lane launch UNKNOWN`.
- Every frame is a rendered transcript. The source lane serves the stub dashboard.
