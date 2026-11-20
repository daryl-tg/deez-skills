# Your own numbers: streams and the views that chart them

*Verified: 2026-11-19, tree `daf4518767` (branch `daryl/byod-any-data`, one squashed commit) for every rig drive, and `7d2fae0bf9` for the eval origin pins and the one-column candles fix (tests and the free journey only). It landed on main as #2623 (`178b9ae734`). The landed commit differs from `daf4518767` by two rebases, the goal 13 fixes, and one `feed_list` fix that lists a feed `om feed append` made (owner kind `account`); that fix is proven by tests only. Driven by hand on a local rig (relay harness 18110, mongod 18111, market-data stub 18112, om lane 18113, the made-up Pro account `@rig`): a declared 5 s stream and its relay head; the rows door's 202, by-name, 409 and 422 answers; a unit change and an added column; a one-minute OHLCV feed and a one-second price feed checked bar for bar against the writers' logs; the token command's curl; `om watch show`'s rows. One live agent run on a real model: turns 1 to 3 passed, turn 4 failed before its fix. Not driven on a lane: `om series feeds` against a relay, `chart_indicator_add` FEED reaching a real chart, `chart_indicator_schema` FEED, the fixed turn 4 on a real model. Not re-driven on main. Evidence: `~/Documents/dev-notes/om-byod-any-data/run-artifacts/u17-rig-declared-feed.txt`, `u17-agent-stream-setup.txt`, `reports/goal-11.md`, `reports/goal-13.md`, `reports/goal-8.md`, `reports/goal-8b.md`, `reports/goal-3b.md`.*

A person declares that an inbound watch takes readings: a cadence from 1 second to 1 week, or irregular, and 1 to 8 named columns, each with an optional unit and combine rule. om declares the watch's relay feed with that shape. Rows sent to the rows door, `om event rows` or `reading_push` go straight to the feed, with no journal entry and no daily cap. `watch_create` and `watch_show` answer a `stream_setup` block: the feed, the push command, a curl, the token command and chart views ready for `chart_indicator_add`. `feed_list` (`om series feeds`) lists every feed the home owns. A FEED view draws a feed as any shape the catalog holds, and a fold or column count that does not fit is refused before any card, naming the fold that fits. The chart side of the same feature is verify-kiyotaka's `feed-views-and-candles.md`.

## Sub-features

- `readings-declaration`: `om watch create <label> --inbound --cadence <1s|5s|15s|30s|1m|…|1w> --column <key[:unit[:rule]]>` (repeatable, in order). With no `--cadence` the stream is irregular (`cadence_s` 0). `--cadence` needs a `--column`, and both need `--inbound`. `om watch edit` has no flag for a declaration.
- `stream-setup`: `watch_create`, `watch_edit` and `watch_show` answer `stream_setup {feed, cadence, columns, stored, refused?, change?, rows_door, push_command, curl, token_command, views}`, and create and show carry a `next` block (`reading_push`, one FEED `chart_indicator_add` per offered view, `feed_list`). No ingest token is ever in it.
- `stream-views`: each stream is offered at most two views: a line over time, and one candles view (`ohlc` when open, high, low and close are declared, else `range` over the first price-like column, else the first column; `range` only when a coarser bar interval exists).
- `rows-door`: `POST /ingest/v1/<watch>/rows`. Rows with no `columns` are taken in declared order. Named columns are placed by name. An undeclared column answers 409 `columns_mismatch`. A row of the wrong width answers 422 `invalid_rows`. The daily cap counts events only.
- `declaration-change`: a unit, rule or cadence change keeps the feed's version. An added column starts the next version, and earlier rows keep their columns. `stream_setup.change` says which in one line.
- `token-command`: `om watch rotate-token <watch>` prints the complete rows curl, with the token, once, under `Push readings:`. It needs a terminal.
- `feed-list`: `feed_list` / `om series feeds` answers `{relay: read|signed_out|unreachable, feeds: [{address, title, columns, cadence, stored, owner, state, last_ts}]}`. Owner kinds: `watch`, `series`, `chart`, `account` (a feed `om feed append` made).
- `feed-view-add`: `chart_indicator_add {indicatorType: "FEED", settings: {address, plot, fold, columns, window?, pane?, title?, units?}}` sends one add intent. The card reads `Draw <feed> as a <shape> on chart <n>?` with `DRAWS`, `FEED` and `COLUMNS` rows. CLI: `om chart indicator add --type FEED --address … --plot … --fold … --columns …`.
- `feed-view-refusal`: a shape with no feed, a fold the shape lacks, or a column count the fold refuses is refused before any card. A wrong count names the fold that fits: `candles with one column takes the range fold`.
- `feed-view-schema`: `chart_indicator_schema {indicatorType: "FEED"}` answers the fields and one `plot: fold columns` row per shape, from the catalog.
- `own-data-eval`: `packages/cli/test/evals/own-data`, two journeys (pie, heatmap, text; and the four-turn stream setup), free at tier 1, paid at tier 3.
- `eval-origin-pins`: every eval session pins every outward om origin to dead loopback (`packages/cli/test/evals/_harness/origins.ts`); `packages/cli/test/ux-eval-origins.test.ts` fails on an origin name with no pin.

## How to get to it (user POV)

- CLI: `om watch create "Meter" --inbound --cadence 5s --column temp:°C --column hum:%`, then the printed `om event rows meter --row "now,$TEMP,$HUM"`.
- From another machine: `om watch rotate-token meter` in a terminal, then the printed curl.
- In `om chat`: "I have a temperature and humidity sensor that posts every 5 seconds. Set it up so I can chart it." The desk opens the composer, whose `inbound` handoff hands back `watch_create` with the readings declared. Then "Chart the temperature as candles too."
- `om series feeds` to see what is there; `om chart indicator add --type FEED …` to draw one.

## Driving it with control-om

### The rig

The recipe is `~/Documents/dev-notes/om-byod-any-data/run-artifacts/rig/README.md`. Its `scripts/` folder holds a copy of every script, with no keys or data, because the live rig sits in a session scratchpad that a reboot clears. Rebuild from that copy with the README's five steps.

| Port | Piece |
| --- | --- |
| 18110 | relay harness: the relay worktree's real feeds door, `FEEDS_ENABLED` and `FEEDS_STREAM_ENABLED` on, its own RSA key, owner `@rig` on tier `pro` |
| 18111 | mongod, one-node replica set `rs0` |
| 18112 | market-data stub for `OM_BASE_URL` (synthetic candles for wrun runs) |
| 18113 | om lane, `control-om up --port 18113`, seeded with the made-up `@rig` key |

1. `bin/rig-up`: starts mongod, the relay harness, then the stub and the lane, then runs `bin/lane-egress`. About 30 s. See `0 not on loopback`.
2. `bin/rig-status`: listeners, relay and lane health, the six feeds' heads, running writers.
3. `bin/writers start [name…]`: the live writers (`price`, `ohlcv`, `meter`, `abc`, `hourly`, `irregular`). A start never backfills.
4. Use `bin/om <args>` for every CLI call. It is `control-om om --` with the rig's env.
5. `bin/rig-down`: stops the writers and everything the rig started, keeps the data, prints the four ports.

Before the first push, prove the lane points at the rig: `ps eww <lane pid>` shows `OM_LEDGER_ORIGIN=http://127.0.0.1:18110`, `OM_BASE_URL=http://127.0.0.1:18112`, `OM_BIND=127.0.0.1:18113` and the other outward URLs at `http://127.0.0.1:9`. `OM_API_KEY` must be unset: it replaces the stored key.

The relay's own request log (`logs/relay-requests.log`, every request with query and status) is the judge for every step below. Read a private feed's head with the owner JWT from the rig's `relay/creds.json`, or make it public first with `bin/feed-public @rig/watch.<slug>`. Never paste either into evidence.

### Declare a stream and read its setup

1. `bin/om watch create "Meter" --inbound --cadence 5s --column temp:°C --column hum:% --format json`. See `stream_setup` with `feed: "@rig/watch.meter"`, `cadence: "5s"`, `columns: ["temp","hum"]`, `stored: null`, `rows_door: "http://127.0.0.1:18113/ingest/v1/meter/rows"`, `push_command: "om event rows meter --row \"now,$TEMP,$HUM\""`, a curl reading `$OM_INGEST_TOKEN`, `token_command: "om watch rotate-token meter"`, and `views`. Grep the answer for `omit_`: none.
2. `bin/om watch show meter` before any reading. See `Meter · waiting for its first reading`, `Status: waiting for its first reading`, `Push: om event rows meter --row "now,$TEMP,$HUM"` and `From another machine: om watch rotate-token meter`. No `om init` or `judging paused` line.
3. Run the `push_command` three times with `TEMP` and `HUM` set. Exit 0 each. The relay log reads `GET …/head 404`, `PUT 201`, `POST …/rows 200`.
4. Read the head. See `version 1, cadence_s 5, floor_s 5`, values `temp °C last` and `hum % last`.
5. `bin/om watch show meter` after readings. On an older commit (`3a8248deb8`, 60 readings at 1 Hz) it read `meter · taking readings`, `Last reading: just now`, `Feed: @rig/watch.meter`, `Stored: one reading per 1s`, and the journal stayed empty. Not re-read on `daf4518767`.

### The rows door and its refusals

1. `bin/mint-token meter`. It saves the token to the rig's `run/token-meter` and never prints it. Rotating revokes the token a running writer holds, so stop that writer first.
2. `POST http://127.0.0.1:18113/ingest/v1/meter/rows` with the bearer and `{"rows": [[null, 24.2, 47]]}`. See 202; the relay row is `[<ts>, 24.2, 47]`.
3. `{"columns": ["hum","temp"], "rows": [[null, 46, 23.3]]}`. See 202, placed by name: `[<ts>, 23.3, 46]`.
4. `{"columns": ["temp","co2"], …}`. See 409 `columns_mismatch`, `this watch's feed has the columns temp, hum`.
5. A row one value short. See 422, `row 0 must be [ts, temp, hum]`.
6. The daily cap never binds this door: 2,107 one-second rows into one watch in 35 minutes all answered 202. Two rows inside one 5 s slot both answer 202; the relay keeps the later one.

### Change a declaration

`om watch edit` has no flag for it. Run the `watch_edit` handler with the rig's script: `OM_HOME=$RIG_LANE_HOME OM_BIND=127.0.0.1:18113 bun edit-readings.ts <slug> '<readings json>'`.

1. Change `temp`'s unit to °F. `stream_setup.change` reads `@rig/watch.meter keeps its version; its units and rules update at its next reading.` The next push sends `PUT 200`; the head stays version 1 with `temp` in °F.
2. Add `co2`. `change` reads `New columns start version 2 of @rig/watch.meter at its next reading; rows sent before keep their columns.` The head reads version 2 with `temp`, `hum`, `co2`. Earlier rows read with `co2` null.

### OHLCV and one-second feeds, bar for bar

1. Create a one-minute watch with columns `open`, `high`, `low`, `close`, `volume` and a one-second watch with one `price` column (`bin/om watch create "<Label>" --inbound --cadence 1m|1s --column …`).
2. Fill them: `bin/writers start ohlcv price`, or `bun stream-writer.ts <slug> <columns> <cadence> <backfill s> 0` from the rig folder after `source env.sh`.
3. Read the heads. See `cadence_s 60` with `open first, high max, low min, close last, volume sum`, and `cadence_s 1, floor_s 1` with `price last`.
4. `bun check-bars.ts <watch> <column> <interval_s>` pages `GET /api/v2/feeds/rig/watch.<name>/bars?interval_s=<n>&value=<column>` (each bar is `[t, open, high, low, close, count, combined]`) and recomputes every bucket from the writers' own logs. It exits 1 on a mismatch. Seen on `daf4518767`: price at 60 s, 33 bars, 0 mismatched, 1,981 rows logged and 1,981 on the relay; index `high` and `volume` at 300 s, 41 bars each, 0 mismatched.
5. Worked check: bucket 1795070700, highs 1004.43, 1004.7, 1002.98, 1003.45, 1005.76 give max 1005.76; volumes 896+151+501+373+948 = 2869. Both equal the relay's bar.

### The token for another machine

1. `bin/om watch rotate-token meter` off a terminal exits 2 with `requires confirmation`. That is by design.
2. In a pseudo-terminal, answer yes. It prints the rows curl under `Push readings:`.
3. Run that curl with `TEMP=76.1 HUM=48.5 CO2=615`. See `202 {"accepted":1,…}` and the row on the relay.

### List feeds

1. `bin/om series feeds --format json`. In a fresh home with no account it answers `{"relay":"signed_out","feeds":[]}` (driven on the branch in a scratch home).
2. On the rig it should list each watch feed with owner `{kind: "watch"}`, and a feed `om feed append` made with owner `{kind: "account", feed}`. Not driven on a lane: `packages/cli/test/feed-list.test.ts` proves the watch and series owners, and `packages/cli/test/feed-append.test.ts` proves the account owner. A first lane drive should add a feed with `om feed append` and read it back here.
3. A relay that does not answer gives `relay: "unreachable"` with each feed's local facts. A relay `feed_not_found` keeps that feed's local facts.

### A FEED view, its refusal and its schema

All three are proven at action level and through the free journey; none reached a real chart from a lane. `chart_indicator_add` needs a chart tab and collab; the chart side is driven through the chart store instead (verify-kiyotaka).

1. `bin/om chart indicator add --type FEED --address @rig/watch.abc --plot pie --fold latest --columns a,b,c`. It passes validation and reaches the daemon call; with no chart attached it fails there. The card, when raised, reads `Draw @rig/watch.abc as a pie on chart 0?`, `DRAWS  pie: slices of a whole`, `FEED  @rig/watch.abc`, `COLUMNS  a, b, c`.
2. A fold the shape lacks on `--plot pie` answers `{"error":"invalid_options","message":"Input validation failed: settings.fold: pie takes the latest fold"}`, before any card (driven at `7425f8cb5a` in a scratch home).
3. One column on `ohlc`: `--plot candles --fold ohlc --columns temp` should answer a refusal ending `settings.columns: candles with one column takes the range fold`. Through the real gate in the free journey it reads `Schema validation failed: settings.columns: candles with one column takes the range fold`. Retry with `--fold range`.
4. `bin/om chart indicator schema FEED --format json`. It should answer `spec: "declared"`, the fields `address`, `plot`, `columns`, `window`, `fold`, `pane`, `title`, `units`, and a `note` with one row per shape, for example `candles: range 1, ohlc 4-5 (open, high, low, close, volume)` and `histogram: time 1, bins 1`. About 1,500 characters. Proven by `packages/cli/src/actions/collab/indicator-schema.test.ts`; not driven on a lane.

### The own-data journeys

1. Free half, alone on a quiet machine: `bun test packages/cli/test/evals/own-data`. See 15 pass, 6 skip at `7d2fae0bf9`. It runs the real runtime, desk, composer handoff, build gate, tool plane, `watch_create`, `reading_push`, `feed_list` and FEED adds with scripted model turns. Turn 4 scripts the refused `ohlc` add, then the `range` retry, and one `candles/range` intent reaches the stub chart.
2. Paid half: `OM_EVAL_SEED_HOME=<copy> scripts/evals.sh own-data 3`. The copy needs only an empty `om.sqlite` with the chat lane's two vault rows and `vault.key` (the `om-live-eval-seed-safely` recipe), never a whole home. A tier 3 run talks to the copy's model provider and nothing else: the chart is an in-process stub, and the harness pins the relay, collab, the registry, the data API and every other om origin to dead loopback. `feed_list` answers `relay: unreachable` with the journey's stand-in `@person1` key, and `reading_push` rows stay queued in the copy.
3. The origin gate: `bun test packages/cli/test/ux-eval-origins.test.ts`, 3 pass. It scans the sources and the env registry for `(OM|OPENMARKET|TYPESAFE|PEN)_…(URL|ORIGIN)` names and fails on one with no pin. A session that needs a real origin passes it explicitly, for example `origins: { OM_LEDGER_ORIGIN: "http://127.0.0.1:<port>" }`.

## Gotchas

- **Always export `OM_LEDGER_ORIGIN` to the rig.** With it unset, `ledgerOriginFromEnv` (`packages/cli/src/runner/feeds/ledger-client.ts`) falls back to the production relay. On 2026-11-19 a tier 3 stream journey, run before the pins existed, sent a head read and a declaration `PUT` for `@person1/watch.temperature-and-humidity-sensor` (refused 400 `feed_invalid`) and two head reads to production with a made-up unsigned key. Nothing was stored, by inference only. The pins fix the eval harness; a hand-built lane or a script still needs the export.
- Still open to the same leak: `packages/cli/test/evals/watchlists/journeys.test.ts` and `_harness/compose-corpus-harness.ts` build their own env. Hosts with no env override (Firecrawl, xAI, Google News, the X API, the Hyperliquid mainnet constant) cannot be pinned this way.
- `bin/writers stop` kills the wrapper shell and leaves the bun writer running. Kill writers by pid before a silence or a rotation.
- The seed pokes the daemon at `OM_BIND`. `lane-up` runs it with `OM_BIND=127.0.0.1:18113`; without it the poke reaches the operator's daemon on 31337.
- Watch feeds are declared private. Run `bin/feed-public` before a signed-out browser reads one.
- `om series publish --yes` declares the feed and pushes its rows, then exits 2 `registry_unreachable` on the rig, because the registry is a dead port. The relay half is what the rig proves.
- Run eval folders alone. Under a load of 14 to 27, `compose`'s execution tests time out and look like failures.
- Known, not verified-good: a unit change relabels earlier rows in place without saying so (the meter's first rows in °C read as °F); `reading_push` accepts rows stamped hours ahead with no word; `om watch create`'s receipt still prints a classifier row for a declared stream (`om watch show` hides it since goal 13, by test only); markers and histogram over time take one column; the hosted endpoint refuses FEED with `feed_view_unavailable`.
- Chart-side known defects (hourly feed at one month, RSI and EMA across a silence, a line on an OHLCV feed drawing the open, the 10-second head read, pie labels, tile plus signs, raw ISO times) are listed in verify-kiyotaka's `feed-views-and-candles.md`.
- Unverified:
  - a candle choice surviving a reload of a saved chart (no signed-in browser was used);
  - an agent-built chart document rendering in the chart (needs collab deployed; collab storing the view was proved in its own int test);
  - production behaviour: nothing is deployed, the relay MR is held for review, and the production stream switch is off;
  - the fourth live agent turn after its fix: only the free journey has run it.
- The live turn 4 failure, for the record: the model sent `{plot: candles, fold: ohlc, columns: [temperature]}`, got a refusal naming only what `ohlc` needs, found no FEED schema, and told the user candles were impossible. Each of those three gaps is fixed and pinned by a test.
