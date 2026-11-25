# Your own numbers: streams and the views that chart them

*Re-checked 2026-11-26 (nightly), tree `1c10d34a9` (origin/main, v0.498.1+internal), guest lane on 18184 through `bootstrap.internal.ts`. First live proof of #2710 and #2717's local half: `watch create … --inbound --column a:USD --column b:USD --column n --layout '<json>'` stored `readings.layout` and `stream_setup.layout` and `watch show` printed `Layout: a | USD`; `watch edit --layout` moved it to `Layout: b | count`; `--layout` with no `--column` and bad JSON are refused; three columns with no layout derived `Layout: requests | million`; `watch layout save … --from-chart 1` on the guest is `watch_layout_no_feed`; nine panes are refused with raw schema words (Gotchas). Not driven: a save from a real chart, an install charting the share's layout (needs an account and a registry). (`cli/layout.txt`.)*

*Re-checked 2026-11-25 (nightly), tree `d5ff40419` (origin/main, v0.497.0+internal), guest lane on 18188 through `bootstrap.internal.ts`. #2693's `null` field passes the readings parse (live, up to the guest's no-username refusal); the held-feed `Held:` row and `held_until` are source only (they need a relay at its feed limit). (`cli/readings-null.txt`.) Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261125/r1/`*

*Re-checked 2026-11-22 (nightly), tree `01482928a5` (origin/main, v0.496.0+internal), guest lane on 18188 through `bootstrap.internal.ts`. `watch create x --cadence 1m --column a` exits 2 with `om: --cadence and --column only apply with --inbound`; `series list --format json` answered `{"series": []}`. Not re-driven: a declared stream, the rows door, FEED views. (`cli/40-cadence-refusal.*`, `cli/34-feed-list.out`.) Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261122/r1/`*

*Re-driven 2026-11-21 (nightly), guest lane only, tree `3c4839c59d` (origin/main, v0.496.0+internal), guest lane on 18188 through `bootstrap.internal.ts`, no relay. `watch create "Meter" --slug vom-meter --inbound --cadence 1m --column temp --column hum` answers `stream_setup` (`feed: null`, `cadence: "1m"`, the columns, `rows_door`, `push_command` ``om event rows vom-meter --row "now,$TEMP,$HUM"`` and a `curl`), and `watch show` prints `Readings: every 1m`, the columns and `Push:`. With no signed-in username every push is refused: `om event rows vom-meter --row "now,21.5,40"` exit 1 `feed_unavailable`, the rows door 409 with the same body; a bad cell is `invalid_rows` (422 on the door), a non-JSON body 415 `unsupported_media_type`, another watch's token 401. Not re-driven: anything that needs the relay rig. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261121/r1/` (`cli/g0-*`, `cli/g1-*`).*

*Verified: 2026-11-20, merged main `2d01b6b5d4` (#2623, #2633, and #2644 for the feed listing), relay `9199a77`, collab `18845f6`, indicator kit `0.121.1` from npm. Lane on 18151 through `control-om` (public entry), signed in to the made-up account `@rig`, on a local relay, mongod and collab rig. Driven, 11 of 11 claims: the rows door, `om event rows` and `reading_push` over MCP stdio with no journal row, the 409, 422 and 401 answers, `stream_setup` from create, show and `watch_edit`, a unit change and an added column on the relay head, a 1 s price feed and a 1 m OHLCV feed bar for bar (51 of 51 `check-bars.ts` runs, 0 bars mismatched), the kit's catalog against main's contracts, `chart indicator schema FEED`, one FEED view per family stored by collab and removed (11 of 11), `feed_column_unknown`, the `columns_unchecked` warning, the stored title and cadence, three `om chat --once` turns on a real model (anthropic `claude-opus-5-5`), and the eval origin gate. A second slice on the same tree drove `om series feeds` against the relay, its `Left out` line and its `Incomplete` fallback. Not driven: a drawn chart, real auth and tharamine (collab ran its own `App` against a made-up stand-in), the interactive TUI, `approvals.writes: ask`, the `signed_out` cause of `columns_unchecked`, `om watch rotate-token` at a terminal. Evidence root `~/Documents/dev-notes/om-2026-11-20-e2e-verify/run-artifacts/s4/` (`c1-*` to `c11-*`, `x1-feed-list.txt`, `rig-scripts/`), and `run-artifacts/s3/evidence/c11-series-feeds.txt` for the listing. Gallery `http://127.0.0.1:8098/om-1120-e2e/s4/`.*

*Verified: 2026-11-19, tree `daf4518767` (branch `daryl/byod-any-data`, one squashed commit) for every rig drive, and `7d2fae0bf9` for the eval origin pins and the one-column candles fix (tests and the free journey only). It landed on main as #2623 (`178b9ae734`). The landed commit differs from `daf4518767` by two rebases, the goal 13 fixes, and one `feed_list` fix that lists a feed `om feed append` made (owner kind `account`); that fix is proven by tests only. Driven by hand on a local rig (relay harness 18110, mongod 18111, market-data stub 18112, om lane 18113, the made-up Pro account `@rig`): a declared 5 s stream and its relay head; the rows door's 202, by-name, 409 and 422 answers; a unit change and an added column; a one-minute OHLCV feed and a one-second price feed checked bar for bar against the writers' logs; the token command's curl; `om watch show`'s rows. One live agent run on a real model: turns 1 to 3 passed, turn 4 failed before its fix. Not driven on a lane: `om series feeds` against a relay, `chart_indicator_add` FEED reaching a real chart, `chart_indicator_schema` FEED, the fixed turn 4 on a real model. Not re-driven on main. Evidence: `~/Documents/dev-notes/om-byod-any-data/run-artifacts/u17-rig-declared-feed.txt`, `u17-agent-stream-setup.txt`, `reports/goal-11.md`, `reports/goal-13.md`, `reports/goal-8.md`, `reports/goal-8b.md`, `reports/goal-3b.md`.*

A person declares that an inbound watch takes readings: a cadence from 1 second to 1 week, or irregular, and 1 to 8 named columns, each with an optional unit and combine rule. om declares the watch's relay feed with that shape. Rows sent to the rows door, `om event rows` or `reading_push` go straight to the feed, with no journal entry and no daily cap. `watch_create` and `watch_show` answer a `stream_setup` block: the feed, the push command, a curl, the token command and chart views ready for `chart_indicator_add`. `feed_list` (`om series feeds`) lists every feed the home owns. A FEED view draws a feed as any shape the catalog holds, and a fold or column count that does not fit is refused before any card, naming the fold that fits. Since #2633 a column the feed does not hold is refused by the feed's own columns. The chart side of the same feature is verify-kiyotaka's `feed-views-and-candles.md`.

## Sub-features

- `readings-declaration`: `om watch create <label> --inbound --cadence <1s|5s|15s|30s|1m|…|1w> --column <key[:unit[:rule]]>` (repeatable, in order). With no `--cadence` the stream is irregular (`cadence_s` 0). `--cadence` needs a `--column`, and both need `--inbound`. `om watch edit` has no flag for a declaration; `watch_edit` over `om mcp serve --stdio` takes `{id_or_slug, source: {kind: "inbound", readings}}`. Nine columns are refused. `1w` is taken and `2w` is refused.
- `stream-setup`: `watch_create`, `watch_edit` and `watch_show` answer `stream_setup {feed, cadence, columns, stored, refused?, change?, rows_door, push_command, curl, token_command, views}`, and create and show carry a `next` block (`reading_push`, one FEED `chart_indicator_add` per offered view, `feed_list`). No ingest token is ever in it.
- `stream-views`: each stream is offered at most two views: a line over time, and one candles view (`ohlc` when open, high, low and close are declared, else `range` over the first price-like column, else the first column; `range` only when a coarser bar interval exists).
- `rows-door`: `POST /ingest/v1/<watch>/rows`. Rows with no `columns` are taken in declared order. Named columns are placed by name. An undeclared column answers 409 `columns_mismatch`. A row of the wrong width answers 422 `invalid_rows`. No token or a wrong token answers 401. The daily cap counts events only.
- `readings-null` (#2693, live 2026-11-25): a `--row` or CSV field spelled `null`, in any case, is a missing reading, as an empty field and a JSONL `null` already were. On a guest lane `om event rows nd --row 'now,null,5'`, `'now,NULL,6'` and a CSV row `now,Null,7` passed the parse and stopped at the account check (`om: readings go to a feed under your account, and no account with a username is signed in`), while `'now,abc,5'` still answers `om: --row 1: 'abc' is not a number`. Before #2693 `null` failed with `'null' is not a number`. Accepting the rows needs a home with a username.
- `declaration-change`: a unit, rule or cadence change keeps the feed's version. An added column starts the next version, and earlier rows keep their columns. `stream_setup.change` says which in one line.
- `feed-layout` (#2710, #2717; live 2026-11-26 up to the account): a stream's feed carries its chart layout, `readings.layout {main, panes:[{plot, fold, columns, title, window, pane}]}`, at most 8 panes. Set it with `--layout '<json>'` on `watch create … --inbound` (it needs the `--column` flags it draws: `--layout needs the --column flags it draws`; bad JSON: `--layout: not JSON (<parser words>)`) or on `watch edit <w>`. With no layout one is derived: each measure its own pane, columns grouped by unit or by a shared name suffix, a multi-column pane titled by its measure (`requests`, `output_million` and `cache_million` read `Layout: requests | million`). `watch show` prints `Layout: <main> | <pane> | …` and `stream_setup.layout` carries it. `om watch layout save <watch> --from-chart <id>` saves a chart's main column and FEED panes; a guest is `watch_layout_no_feed` `Watch '<w>' has no feed yet: it lives under a signed-in username.` (hint `Sign in with om login, then save again.`); `watch_layout_not_your_chart`, `watch_layout_nothing_drawn`, `watch_layout_feed_unread` and `watch_layout_moves_steps` are source only. A watch with no declared readings gets them declared first. `om install` and `om watch install` chart the installer's own feed from the share's layout (`--no-chart` skips it; source).
- `token-command`: `om watch rotate-token <watch>` prints the complete rows curl, with the token, once, under `Push readings:`. It needs a terminal.
- `feed-list`: `feed_list` / `om series feeds` answers `{relay: read|signed_out|unreachable, feeds: [{address, title, columns, cadence, stored, owner, state, last_ts, observed_cadence_s, late_s}], not_on_relay}`. Owner kinds: `watch`, `series`, `chart`, `account` (a feed `om feed append` made).
  - Since #2644 the list is what the relay holds. A feed made outside this home lists with owner `account`.
  - A home record the relay does not hold is left out, named in `not_on_relay`, and counted on one line: `Left out: 2 home records the relay does not hold (om feed delete <name> drops one)`.
  - A listing that fails prints `Incomplete: the relay did not list your feeds, so these are this home's records only` and answers `relay: "unreachable"` with the home records.
  - `observed_cadence_s` and `late_s` are explained in [account-feeds.md](account-feeds.md) (`show`).
  - The text rows need `--format text`. Through the public entry the default prints JSON.
- `feed-view-add`: `chart_indicator_add {indicatorType: "FEED", settings: {address, plot, fold, columns, window?, pane?, title?, units?}}` sends one add intent. The card reads `Draw <feed> as a <shape> on chart <n>?` with `DRAWS`, `FEED` and `COLUMNS` rows. CLI: `om chart indicator add --type FEED --address … --plot … --fold … --columns …`.
- `feed-view-refusal`: a shape with no feed, a fold the shape lacks, or a column count the fold refuses is refused before any card. A wrong count names the fold that fits: `candles with one column takes the range fold`. An unknown plot answers `sankey is not a feed plot; feed plots:` and 14 kinds.
- `feed-column-unknown` (#2633): a column the feed does not hold exits 2 with `feed_column_unknown`: `@rig/watch.<slug> has no column zz; its columns are temp, hum, co2`. Candles by role and candles from one value are checked the same way. Nothing reaches collab. The relay sees one head read per call.
- `columns-unchecked` (#2633): when the head cannot be read the view is sent with a warning, and nothing is refused on a guess. With no feed yet: `columns_unchecked: the relay holds no feed there yet, so the columns of … were not checked`. With the relay down: `the relay did not answer`.
- `feed-view-record` (#2633): the stored record carries the feed's title (`e2e1120 s4 meter`, not `watch.<slug>`) and the head's cadence. A caller's `title` is stored as given.
- `feed-view-schema`: `chart_indicator_schema {indicatorType: "FEED"}` answers the fields and one `plot: fold columns` row per shape, from the catalog: 14 plots, 9 folds, 14 note rows.
- `kit-parity`: `view-catalog.json` and `view-fixtures.json` (61 cases) in the npm kit are byte-equal to what main's contracts render, and the kit's 21 views deep-equal `CHART_VIEWS_V1`.
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

**The 2026-11-20 copy, with a collab half.** `run-artifacts/s4/rig-scripts/` in that day's evidence root is the same rig on other ports, plus collab. It holds no keys.

| Port | Piece |
| --- | --- |
| 18151 | om lane, `control-om up`, signed in as `@rig` |
| 18152 | relay harness on the real relay tree |
| 18153 | mongod, one-node `rs0` |
| 18154 | candle stub for `OM_BASE_URL` (`data-stub.ts`) |
| 18155 | collab harness, collab's own `App` (`collab/collab-harness.ts`) |
| 18156 | made-up auth and tharamine stand-in (`collab/upstream-stub.ts`) |

- `bin/rig-up` runs `mongo-up`, `relay-up`, `lane-up` and `lane-egress`. Start the collab pair after it.
- With the stand-in and collab up, `bin/om chart list` shows the workspace and `bin/om chart select 6650b0b0b0b0b0b0b0b0b0b0` attaches the lane. `bin/om chart indicator add` then stores the view.
- "Stored by collab" on this rig means collab accepted the intent and wrote the workspace through to the stand-in.
- To move the rig to other ports, change the port defaults in `env.sh`, the four writers and checkers, `relay/env.ts` and `relay/server.ts`, and the absolute import paths in `relay/server.ts`, `lane-seed.ts`, `edit-readings.ts` and `collab-harness.ts`.
- `bin/om-model <args>` is `bin/om` with the three model-lane names unset, for a real-model `om chat` call.

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
7. No bearer, or a wrong one. See 401.
8. `bun mcp-call.ts reading_push '{"watch":"<slug>","rows":[[null,26.3,51]]}'` drives the tool over `om mcp serve --stdio` on the lane home. See `accepted: 1`.
9. Side effects after pushes through all three doors: the lane's sqlite reads 0 rows for the watch in `watch_history` and `watch_intake`, `events.md` has no entry, and `om watch show` reads `Model reads today: 0` (`bin/journal-count`).

### Change a declaration

`om watch edit` has no flag for it. Drive the real tool over MCP stdio: `bun mcp-call.ts watch_edit '{"id_or_slug":"<slug>","source":{"kind":"inbound","readings":{"cadence_s":5,"columns":[…]}}}'` (driven 2026-11-20; the stdio servant lists `watch_edit` among 272 tools). The older route runs the handler with the rig's script: `OM_HOME=$RIG_LANE_HOME OM_BIND=127.0.0.1:18113 bun edit-readings.ts <slug> '<readings json>'`.

1. Change `temp`'s unit to °F. `stream_setup.change` reads `@rig/watch.meter keeps its version; its units and rules update at its next reading.` The next push sends `PUT 200`; the head stays version 1 with `temp` in °F.
2. Add `co2`. `change` reads `New columns start version 2 of @rig/watch.meter at its next reading; rows sent before keep their columns.` The head reads version 2 with `temp`, `hum`, `co2`. Earlier rows read with `co2` null.

### OHLCV and one-second feeds, bar for bar

1. Create a one-minute watch with columns `open`, `high`, `low`, `close`, `volume` and a one-second watch with one `price` column (`bin/om watch create "<Label>" --inbound --cadence 1m|1s --column …`).
2. Fill them: `bin/writers start ohlcv price`, or `bun stream-writer.ts <slug> <columns> <cadence> <backfill s> 0` from the rig folder after `source env.sh`.
3. Read the heads. See `cadence_s 60` with `open first, high max, low min, close last, volume sum`, and `cadence_s 1, floor_s 1` with `price last`.
4. `bun check-bars.ts <watch> <column> <interval_s>` pages `GET /api/v2/feeds/rig/watch.<name>/bars?interval_s=<n>&value=<column>` (each bar is `[t, open, high, low, close, count, combined]`) and recomputes every bucket from the writers' own logs. It exits 1 on a mismatch. Seen on `daf4518767`: price at 60 s, 33 bars, 0 mismatched, 1,981 rows logged and 1,981 on the relay; index `high` and `volume` at 300 s, 41 bars each, 0 mismatched.
5. On main, 2026-11-20: a 1 s feed took 302 live posts over 301 s after a 1,800 row backfill, and a 1 m OHLCV feed took 6 live posts after a 240 row backfill. `check-bars.ts` exited 0 on 51 of 51 runs: `price` at 11 intervals from 5 s to 1 w, and each of 5 OHLCV columns at 8 intervals from 60 s to 1 w. The relay refuses an interval below a feed's floor.
6. Worked check: bucket 1795070700, highs 1004.43, 1004.7, 1002.98, 1003.45, 1005.76 give max 1005.76; volumes 896+151+501+373+948 = 2869. Both equal the relay's bar.

### The token for another machine

1. `bin/om watch rotate-token meter` off a terminal exits 2 with `requires confirmation`. That is by design.
2. In a pseudo-terminal, answer yes. It prints the rows curl under `Push readings:`.
3. Run that curl with `TEMP=76.1 HUM=48.5 CO2=615`. See `202 {"accepted":1,…}` and the row on the relay.

### List feeds

1. `bin/om series feeds --format json`. In a fresh home with no account it answers `{"relay":"signed_out","feeds":[]}` (driven on the branch in a scratch home).
2. On the rig, `bin/om feed append <name> --values '{"usd":12.5}' --cadence 1h`, then `bin/om series feeds --format json`. See `relay: "read"`, each watch feed with owner `{kind: "watch"}` and the appended feed with owner `{kind: "account", feed}` (driven on main 2026-11-20).
3. Read the list against the relay's own scope listing, `GET /api/v2/feeds?scope=@rig` as the owner. They are equal. A feed put on the relay by another client lists as `account`. A chart series' feed lists as `{kind: "chart", series}`.
4. Make a home record the relay does not hold: an inbound watch with a declaration and no reading yet, or a feed removed on the relay behind om's back. It is left out of the rows, named in `not_on_relay`, and counted on the `Left out:` line.
5. Point the CLI call at a proxy that answers 503 to the scope listing only (`run-artifacts/s3/rig/listing-fail-proxy.ts`), or at a dead port: `OM_LEDGER_ORIGIN=http://127.0.0.1:<port> bin/om series feeds --format text`. See the `Incomplete:` line, the home records, and `relay: "unreachable"`.

### A FEED view, its refusal and its schema

On 2026-11-20 the adds reached the rig's collab and were stored. No chart drew anything: the chart side is driven through the chart store instead (verify-kiyotaka). Steps 5 to 9 need the collab half and `chart select`.

1. `bin/om chart indicator add --type FEED --address @rig/watch.abc --plot pie --fold latest --columns a,b,c`. It passes validation and reaches the daemon call; with no chart attached it fails there. The card, when raised, reads `Draw @rig/watch.abc as a pie on chart 0?`, `DRAWS  pie: slices of a whole`, `FEED  @rig/watch.abc`, `COLUMNS  a, b, c`.
2. A fold the shape lacks on `--plot pie` answers `{"error":"invalid_options","message":"Input validation failed: settings.fold: pie takes the latest fold"}`, before any card (driven at `7425f8cb5a` in a scratch home).
3. One column on `ohlc`: `--plot candles --fold ohlc --columns temp` should answer a refusal ending `settings.columns: candles with one column takes the range fold`. Through the real gate in the free journey it reads `Schema validation failed: settings.columns: candles with one column takes the range fold`. Retry with `--fold range`.
4. `bin/om chart indicator schema FEED --format json`. It should answer `spec: "declared"`, the fields `address`, `plot`, `columns`, `window`, `fold`, `pane`, `title`, `units`, and a `note` with one row per shape, for example `candles: range 1, ohlc 4-5 (open, high, low, close, volume)` and `histogram: time 1, bins 1`. About 1,500 characters. Proven by `packages/cli/src/actions/collab/indicator-schema.test.ts`, and driven on a lane 2026-11-20: 1,493 bytes, 14 plots, 9 folds, and note rows equal to rows derived from the kit catalog (`schema-vs-catalog.ts`).
5. One view per family, each stored by collab with the asked plot, fold and columns, then removed with `bin/om chart indicator remove --id <FEED id>`:
   - `--plot line --fold time --columns temp,hum`
   - `--plot bars --fold latest --columns temp,hum,co2`
   - `--plot pie --fold latest --columns temp,hum,co2`
   - `--plot heatmap --fold grid --columns temp,hum,co2`
   - `--plot scatter --fold pair --columns temp,hum`
   - `--plot table --fold rows --columns temp,hum,co2`
   - `--plot tiles --fold latest --columns temp,hum,co2`
   - `--plot card --fold latest --columns temp,hum`
   - `--plot meter --fold latest --columns temp`
   - `--plot candles --fold range --columns price` on the price feed
   - `--plot candles --fold ohlc --columns open,high,low,close,volume` on the index feed
6. `--columns temp,zz` on the meter feed. See `feed_column_unknown`, exit 2, with the feed's columns. The collab version does not move and the stub sees 0 writes.
7. Declare a stream and push nothing. Add a view on it. See the `columns_unchecked` warning and the view stored. Stop the relay harness and add a view on a feed that exists. See `the relay did not answer`. A column the feed lacks is sent too in both states.
8. Read a stored record. See the feed's title and the head's cadence. `--params 'title=<mine>'` is stored as given.
9. `--plot sankey`. See the 14-kind refusal.
10. `bun kit-compare.ts` after `npm pack @orangecharts/indicator-kit@0.121.1` checks the kit's catalog and fixtures against main's contracts. The package is private on npm and needs this machine's login.

### The own-data journeys

1. Free half, alone on a quiet machine: `bun test packages/cli/test/evals/own-data`. See 15 pass, 6 skip at `7d2fae0bf9`. It runs the real runtime, desk, composer handoff, build gate, tool plane, `watch_create`, `reading_push`, `feed_list` and FEED adds with scripted model turns. Turn 4 scripts the refused `ohlc` add, then the `range` retry, and one `candles/range` intent reaches the stub chart.
2. Paid half: `OM_EVAL_SEED_HOME=<copy> scripts/evals.sh own-data 3`. The copy needs only an empty `om.sqlite` with the chat lane's two vault rows and `vault.key` (the `om-live-eval-seed-safely` recipe), never a whole home. A tier 3 run talks to the copy's model provider and nothing else: the chart is an in-process stub, and the harness pins the relay, collab, the registry, the data API and every other om origin to dead loopback. `feed_list` answers `relay: unreachable` with the journey's stand-in `@person1` key, and `reading_push` rows stay queued in the copy.
3. On main with a real model (2026-11-20, `om chat --once` through `bin/om-model`, 3 of 6 budgeted turns, $4.24 at list price by the product's own usage rows):
   - "I have a temperature, humidity and CO2 sensor posting every 5 seconds; set it up and chart temperature as candles". Tool trail `watch_kit`, `watch_compose`, `watch_create`, `tool_search`, `chart_open`, `chart_indicator_add`. The add was `{plot: candles, fold: range, columns: [temperature]}`, first try.
   - The journey's OHLCV sentence declared `index` at 60 s with `first`, `max`, `min`, `last`, `sum` rules and stored `candles` over `ohlc`.
   - "Chart the humidity as candles too." The model sent `range` with `[humidity]`, first try, so the refused `ohlc` add and its retry did not occur.
   - Under the default `approvals.writes: auto` neither `watch_create` nor a FEED add raised a card.
4. The origin gate: `bun test packages/cli/test/ux-eval-origins.test.ts`, 3 pass. From an empty environment `pinEvalOrigins({})` leaves 33 names on loopback and 0 off it. It scans the sources and the env registry for `(OM|OPENMARKET|TYPESAFE|PEN)_…(URL|ORIGIN)` names and fails on one with no pin. A session that needs a real origin passes it explicitly, for example `origins: { OM_LEDGER_ORIGIN: "http://127.0.0.1:<port>" }`.

## Gotchas

- **Always export `OM_LEDGER_ORIGIN` to the rig.** With it unset, `ledgerOriginFromEnv` (`packages/cli/src/runner/feeds/ledger-client.ts`) falls back to the production relay. On 2026-11-19 a tier 3 stream journey, run before the pins existed, sent a head read and a declaration `PUT` for `@person1/watch.temperature-and-humidity-sensor` (refused 400 `feed_invalid`) and two head reads to production with a made-up unsigned key. Nothing was stored, by inference only. The pins fix the eval harness; a hand-built lane or a script still needs the export.
- Still open to the same leak on `2d01b6b5d4`: `packages/cli/test/evals/watchlists/journeys.test.ts` and `_harness/compose-corpus-harness.ts` build their own env and hold 0 references to `pinEvalOrigins`. Hosts with no env override (Firecrawl, xAI, Google News, the X API, the Hyperliquid mainnet constant) cannot be pinned this way.
- `bin/writers stop` kills the wrapper shell and leaves the bun writer running. Kill writers by pid before a silence or a rotation.
- The seed pokes the daemon at `OM_BIND`. `lane-up` runs it with `OM_BIND=127.0.0.1:18113`; without it the poke reaches the operator's daemon on 31337.
- Watch feeds are declared private. Run `bin/feed-public` before a signed-out browser reads one.
- `om series publish --yes` declares the feed and pushes its rows, then exits 2 `registry_unreachable` on the rig, because the registry is a dead port. The relay half is what the rig proves.
- Run eval folders alone. Under a load of 14 to 27, `compose`'s execution tests time out and look like failures.
- **Known, not verified-good: a view charted before the feed's first reading is stored with `cadence_s` 0.**
  - Repro: `om watch create "x" --inbound --cadence 5s --column v`, then `om chart indicator add --type FEED --address @rig/watch.x --plot line --fold time --columns v` before any row is pushed. The same happens with the relay stopped on a feed that exists.
  - Expected 5, the cadence the watch declares, since the title already comes from local facts.
  - It is the normal agent path: 2 of 3 views in the real-model run were stored with cadence 0.
  - Cause: `readHomeFeed` returns only the title when the head read fails (`packages/cli/src/runner/feeds/home-feeds.ts:220-231`, cadence only at `:236`). `checkFeedViewColumns` passes a cadence only when the relay answered (`packages/cli/src/actions/collab/_feed-view-columns.ts:88`). The settings default it to 0 (`packages/cli/src/actions/collab/_chart-targets.ts:272`).
  - Effect on a drawn chart is unknown. Evidence `c9-01-title-cadence-plot.txt`, `c6-01-families.txt`.
- **Known, not verified-good: the rows door names generic columns when a value is text.** `{"rows": [[null, "warm", 47]]}` on a watch declaring `temp`, `hum` answers 422 `row 0 must be [ts, v1, ...]`. A wrong-width row on the same watch names `[ts, temp, hum]`. Evidence `c1-02-c2-rows-door-http.txt`.
- **Known, not verified-good: nine columns on a three-column feed are counted, not checked.** The schema refusal `gives 9 columns; a feed gives at most 8` fires before the column check, so it counts names the feed does not hold. Nothing is sent. Evidence `c7-01-unknown-columns.txt`.
- **Known, not verified-good: the `Left out` line advises a verb that cannot drop what it counts.** For an inbound watch that has not pushed yet, `om feed delete watch.<slug>` answers `feed_daemon_owned`. For an authored series not yet published, `om feed delete <name>` answers `feed_not_found`. The text line names neither record; only `not_on_relay` does. Cause: `packages/cli/src/runner/feeds/home-feeds.ts:275` counts every local record, and `leftOutLine` in `packages/cli/src/cmd/series.ts` gives one hint for all. Evidence `run-artifacts/s3/evidence/c11-series-feeds.txt`.
- `om watch create` with nine columns answers raw schema words: `source.readings.columns: Too big: expected array to have <=8 items`.
- Nine layout panes do the same (live 2026-11-26): `watch edit <w> --layout '<9 panes>'` exits 2 with a raw Zod issue array (`"code": "too_big"`, `"maximum": 8`, path `sources.0.readings.layout.panes`); `--format json` wraps it as `request_failed`. README Known product gaps.
- The `--cadence` error lists `1M, 3M, 6M, 1Y` as accepted. Whether a stream takes them was not probed.
- The rig's `env.sh` pins `OPENMARKET_LLM_BASE_URL`, so `om llm status` reads `openai-compatible`, `usable`, from the env profile, and hides a seeded sign-in. Unset the three model-lane names on the `om chat` call only (`bin/om-model`). The daemon can stay pinned, because `om chat --once` runs the model in the CLI process.
- The plain channel reads a card's answer as a line from stdin. That is inferred from `packages/cli/src/agent/channels/cli.ts` and was never exercised.
- A worktree with dashboard stubs has no Watches table to capture. Use the relay's own answers in a browser, or rendered text.
- Known, not verified-good: a unit change relabels earlier rows in place without saying so (the meter's first rows in °C read as °F); `reading_push` accepts rows stamped hours ahead with no word; `om watch create`'s receipt still prints a classifier row for a declared stream (`om watch show` hides it since goal 13, by test only); markers and histogram over time take one column; the hosted endpoint refuses FEED with `feed_view_unavailable`.
- Chart-side known defects (hourly feed at one month, RSI and EMA across a silence, a line on an OHLCV feed drawing the open, the 10-second head read, pie labels, tile plus signs, raw ISO times) are listed in verify-kiyotaka's `feed-views-and-candles.md`.
- Unverified:
  - a candle choice surviving a reload of a saved chart (no signed-in browser was used);
  - an agent-built chart document rendering in the chart (needs collab deployed; collab storing the view is driven on the rig since 2026-11-20);
  - production behaviour: nothing is deployed, the relay MR is held for review, and the production stream switch is off;
  - the refused `ohlc` add and its `range` retry on a real model: on 2026-11-20 the model sent `range` first try, so only the free journey has run the refusal;
  - a FEED add under `approvals.writes: ask`, where the card shows before the refusal;
  - the `signed_out` cause of `columns_unchecked` (two of the four causes in `_feed-view-columns.ts` are driven).
- The live turn 4 failure, for the record: the model sent `{plot: candles, fold: ohlc, columns: [temperature]}`, got a refusal naming only what `ohlc` needs, found no FEED schema, and told the user candles were impossible. Each of those three gaps is fixed and pinned by a test.
