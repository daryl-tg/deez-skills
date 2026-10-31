# Market data reads

*Re-driven 2026-11-01 (nightly), tree `7ce379c45` (origin/main, v0.480.3), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 2.9. `coins`; `exchanges` 45 with `LIGHTER`; `enum --domain exchange_id` still 35 (`--query BIN --limit 3` → `total: 3`); `points … --exchange BINANCE … --lookback 3h` returned one `series` of `{Point}` elements; `points --exchange BYBIT_FUTURES` exit 2 with the API's `"BYBIT_FUTURES" is not a valid value` (README, product gaps); `metric get --exchange BYBIT_FUTURES` read `selector.exchange: BYBIT` (the alias) and answered `ok: false`, `error: no_recent_trade` for `rsi` on BTC there (`last_print_at_sec: null`, `window_hours: 64`) while the home's `last-plan-refusal.json` recorded a `data_type` plan refusal at that moment (README, product gaps: the guest plan's 403 on the trade read surfaced as "no recent trade"); `metric get` with an unknown param → exit 2 `invalid_query` (`unknown param "quote" for open_interest_delta_pct (takes: bars); quote is a selector field`); `metric get --metric rsi --symbol BTC --interval 1h` with no `--exchange` read Binance with `listing_note`; `metric series` without `--exchange` exit 1; `--symbol AAPL --exchange POLYGON` exit 2 `venue_not_served`; `resolve BTC` bound `HYPERLIQUID_FUTURES` exact and `resolve "bitcoin dip to 55000"` led with the Polymarket slug; `metric list`; `markets --exchange LIGHTER` rows; `symbols --exchange BINANCE --type TRADE_AGG` (`rawSymbols`), `normalized-symbols --exchange BINANCE --type TRADE_AGG` (`normalizedSymbols`; without `--type` it is refused `invalid_options`), `block-sizes --exchange BINANCE`; `instruments BINANCE BTCUSDT --limit 3` on the default transport exit 2 `invalid_query` (v3 only); `tenors` still 500. Over MCP stdio: `points` with `exchanges:["BYBIT_FUTURES"]`, `rawSymbol` and `interval:"HOUR"` (the MCP schema takes the enum word; `1h` is refused `invalid_arguments`) answered `id.exchange: BYBIT`; `metric_get {queries:[{metric:"rsi"}], selector:{symbol:"BTC"}}` carried `listing_note` and `interval_note`; `markets {exchanges:["LIGHTER"]}` refused `invalid_arguments` with the `This input cannot address a venue outside the set` sentence. Evidence: `http://127.0.0.1:8098/vom-nightly-20261101/r1/` (`cli/40-49`, `cli/21b`, `cli/90*`).*

*Re-driven 2026-10-31 (nightly), tree `dfefe0a21` (origin/main, v0.480.2), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 1.6, with #2202 on main. `coins`; `exchanges` lists 45 with `unselectable` naming `LIGHTER` among others, and `markets --exchange LIGHTER` still returns rows; `enum --domain exchange_id` still 35. `metric get --metric open_interest_delta_pct --params quote=USD …` exit 2 `invalid_query` `unknown param "quote" for open_interest_delta_pct (takes: bars); quote is a selector field`. `metric get --metric rsi --symbol BTC --interval 1h` with no `--exchange` read Binance and carried `listing_note: No venue named — reading BTC on Binance (BTCUSDT); say a venue to change it.`; `metric series` without `--exchange` exits 1 `required option '--exchange <id>' not specified`. `metric get --exchange BYBIT_FUTURES` read `selector.exchange: BYBIT` (the alias), but `points --exchange BYBIT_FUTURES` exit 2 with the API's `"BYBIT_FUTURES" is not a valid value` (README, product gaps). `metric get --symbol AAPL --exchange POLYGON` exit 2 `venue_not_served` (`POLYGON market data is not served here`), so the `unknown_symbol` spelling hint is unreachable on a guest lane. `resolve "bitcoin dip to 55000"` led with `will-bitcoin-dip-to-55000…`; `resolve BTC` bound `HYPERLIQUID_FUTURES` exact. `tenors` still 500. Over MCP stdio: `points` with `exchanges:["BYBIT_FUTURES"]` and `rawSymbol` answered a series whose `id.exchange` is `BYBIT`; `metric_series` and `metric_get` with `selector:{symbol:"BTC"}` answered with `listing_note` (and `metric_get` an `interval_note`); `markets {exchanges:["LIGHTER"]}` was refused `invalid_arguments` with the new sentence `This input cannot address a venue outside the set … It does NOT mean the venue has no data`. Evidence: `http://127.0.0.1:8098/vom-nightly-20261031/r1/` (`cli/50-59b`, `cli/68-69`, `cli/95-96b`).*

*Re-driven 2026-10-30 (scheduled maintenance), tree `3cb50a821` (origin/main, v0.478.0), fresh lane on 18165, host load average about 140. `coins` 4,176; `exchanges` 45; `enum --domain exchange_id` 35; `resolve BTC` bound `HYPERLIQUID_FUTURES`; `metric list`; `markets --exchange LIGHTER` rows; `tenors` still 500 `server_error`. New this pass: `block-sizes --exchange BINANCE`, `symbols --type TRADE_AGG --exchange BINANCE` (`rawSymbols`) and `normalized-symbols --type TRADE_AGG` (`normalizedSymbols`). `--type` takes a `data_type` value (`enum --domain data_type`, 13 values); `PERPETUAL_FUTURE` is refused `invalid_options`. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261030/r1/` (`cli/12`, `cli/14`, `cli/15`).*
*Re-driven 2026-10-30 (nightly, smoke depth), tree `3cb50a821` (origin/main, v0.478.0), lane on 18163. `coins` returned 4,176 rows and `exchanges` returned **45**, down from 48 on 2026-10-29. `LIGHTER`, `VARIATIONAL` and `VARIATIONAL_SWAP` are still listed and `CRYPTOCAP` is not; which three venues dropped was not recorded. `enum --domain exchange_id` still holds 35 values. Not re-driven: `points`, `resolve`, `metric`, `markets`, `tenors` and v3. Evidence is local only (the `8098` renderer did not answer): `artifacts/vom-nightly-20261030/r1/`.*

*Re-driven 2026-10-29 (scheduled maintenance, smoke depth), tree `7ec575e55` (origin/main, v0.467.0 plus #2194), fresh lane on 18161. `coins` returned 4,170 rows and `exchanges` 48; `enum` still lists 35 `exchange_id` values. The mapped `points` recipe returned `{series}`. `points` without `--type` is refused with `required option '--type <data-type>'`, and without `--lookback` with `required option '--lookback <duration>'`. `resolve BTC` bound `HYPERLIQUID_FUTURES`, and `markets --exchange LIGHTER` returned rows. `metric list` returned `{metrics}`. `tenors` still returned a 500 `server_error`. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261029/r1/`.*

*Re-driven 2026-10-29 (nightly, smoke depth), tree `32ca0d6c7` (origin/main, v0.467.0), fresh lane home on 18103. `coins` returned 4,170 rows (`{coins}`), and `exchanges` returned 48. `points --type TRADE_SIDE_AGNOSTIC_AGG --exchange BINANCE --raw-symbol BTCUSDT --interval MINUTE --lookback 10m` returned `{series}`; without `--lookback` it was refused before any request. `resolve BTC` bound `HYPERLIQUID_FUTURES`. `markets --exchange LIGHTER` returned rows, while `enum` still lists 35 `exchange_id` values. `metric list` returned `{metrics}`. `tenors` still returned a 500 `server_error`. Evidence: `http://127.0.0.1:8098/vom-nightly-20261029/r1/`.*

*Verified: 2026-10-28 (scheduled maintenance), tree `186030b63` (origin/main), fresh lane home on 18145. `coins` returned 4,165 rows and `exchanges` 48 (BINANCE, HYPERLIQUID and LIGHTER present). `points --type TRADE_SIDE_AGNOSTIC_AGG --exchange BINANCE --raw-symbol BTCUSDT --interval 1h --lookback 3h` returned one series of 3 points. A reused home on 18143 refused all market reads with an expired key, and a first fresh home on 18144 hit the guest-mint 429 (Gotchas). `metric`, `screen`, `markets`, `resolve` and `tenors` were not re-driven. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261028/r1/` (`cli/m-*.txt`, `cli/13.txt`, `cli/14.txt`).*

*Nightly record: 2026-10-28, tree `a8fa10974` (origin/main, v0.466.0), lane on 18103. `enum` returned the live lists. `coins` returned `{coins}`, and `exchanges` returned `{exchanges, refusedTypes, unselectable}` with 48 venues, including `LIGHTER`, `VARIATIONAL` and `VARIATIONAL_SWAP`. `points` returned one `series` of `{Point}` elements, and `--type OHLCV` gave `is not a valid value` (exit 2). With `OM_DATA_TRANSPORT=v3`: `instruments BINANCE BTCUSDT --limit 3` returned `{exchange, arm:"crypto", rows}`, `option-chain DERIBIT BTC --neighbor-strikes 1` returned `expiries`, and `exchanges` returned 30 venues. Newly driven: `resolve BTC`, `metric list`/`get`/`series`/`screen` and `markets` (see Resolve, metrics and markets). `tenors` returned `server_error` 500 three times. Not driven: the typed-door reads (fx/index candles, ETF flow, FRED) and the daemon's `counters.symbol_directory_*`. Previous stamp `8fe6a8432` is an ancestor (10 commits).*

The reason the daemon exists: `om` answers questions about markets from the
OpenMarket Data API. A user lists what is available (coins, exchanges, symbols,
enum domains) and then pulls history — candles, open interest, funding,
liquidations, heatmaps — with `om points`. These are pure reads, and a guest
lane's machine-minted key is enough for them.

## Sub-features

- `data-enum` lists the API's enum domains and their live values.
- `data-inventory` lists coins, exchanges, markets, symbols and tenors.
- `data-points` fetches a historical series for one type/exchange/symbol.
- `data-metric` lists and computes scalar metrics and per-bar metric history;
  `metric screen` evaluates a metric across a symbol set.
- `data-resolve` turns a phrase into order-ready venue/symbol fields;
  chart symbol lookup is a separate directory read.

## How to get to it (user POV)

- `om coins`, `om exchanges`, `om markets`, `om enum`.
- `om points --type <TYPE> --exchange <EX> --raw-symbol <SYM> --interval <IV> --lookback <DUR>`.

## Driving it with control-om

Preconditions:

- A lane the run started, with network. `control-om om -- doctor` must report
  `api_key: ok` and `network: ok` — that is the JSON `status` field
  (`--format json`, `.checks[] | select(.name=="api_key") | .status`); text mode
  prints `✓ api_key <sentence>` instead. A guest lane gets the key automatically; no
  login is involved.

- **Read the domains first.** Run `control-om om -- enum --format json`. It
  returns `exchanges`, `types`, `intervals` and the rest as live lists. Every
  later flag value comes from here rather than from memory.
- **Inventory.** Run `control-om om -- coins --format json` and
  `control-om om -- exchanges --format json`. Both return large arrays;
  assert the shape and a couple of known members (`BINANCE`, `HYPERLIQUID`),
  not the whole list.
- **A series.** Run
  `control-om om -- points --type TRADE_SIDE_AGNOSTIC_AGG --exchange BINANCE --raw-symbol BTCUSDT --interval 1h --lookback 3h --format json`.
  The result is `{"series":[{"id":{...},"points":[...]}]}` where `id` carries
  `type`, `rawSymbol`, `exchange`, `normalizedSymbol`, `category`, `interval`,
  `coin`.

  **Each element of `points` is `{"Point": {...}}` — a capital-P wrapper, not a
  flat candle.** The CLI passes the server's envelope through verbatim
  (`packages/sdk/src/endpoints/points.ts:59-77`), so the fields live at
  `.series[0].points[0].Point.open`, and `timestamp` is itself an object
  `{"s": <epoch seconds>, "ns"?: <n>}`, not a number. Assert
  `.Point.close` and `.Point.timestamp.s`; `.points[0].open` is `undefined` and
  a defensive `point.get("Point", point)` in a probe will hide which shape you
  actually got.
- **Assert on structure, never on price.** The values move every hour. A test
  that pins a close is a test that fails tomorrow for the wrong reason. Assert
  the envelope, the id echo, the point count against the lookback, and that
  timestamps ascend.
- **Resolve, metrics and markets** (driven 2026-10-28, guest lane):
  - `control-om om -- resolve BTC --format json` binds `{venue:"hyperliquid",
    exchange_id:"HYPERLIQUID_FUTURES", match:"exact"}` with order
    `constraints`.
  - `metric list --metric rsi --format json` is a local registry read
    (`package @om-core/rsi`).
  - `metric get --metric rsi --symbol BTCUSDT --exchange BINANCE --interval 1h
    --format json` returns `values[{ok, value, data_age_seconds}]`.
    `metric series … --bars 3` returns `series` as `[epoch, value]` pairs.
    **These take `--symbol`, not `--raw-symbol`** (`points` takes
    `--raw-symbol`), and leaving it out fails as `required option '--symbol
    <sym>'`.
  - `metric screen --metric rsi --top-n 3 --by VOLUME_24H --exchange
    BINANCE_FUTURES --interval 1h --format json` returns `universe`, `scanned`
    and `rows`. It needs `--exchange`, and `--by` takes the upper-case field
    (`volume24h` fails as `universe.by: Invalid input`).
  - `markets --symbol-filter BTC --page-size 3 --format json` returns
    `symbols[]` with 24 h fields. `--exchange LIGHTER` also returns rows (see
    Gotchas).
  - `tenors` answered `server_error` (500) on 2026-10-28, a service fault, so
    its shape stays unproven.
- **Proof.** Keep the exact command and the JSON (truncated to the first point
  or two is fine, but keep the full `id` block) plus the exit code.

## Gotchas

- **A reused lane home carries an expired guest key, and `doctor` still says
  `api_key: ok`.** The lane home is `home-<port>`, so the same port on a later
  day reuses yesterday's home. Guest keys last one hour. On 2026-10-28,
  `home-18143` from the previous day answered `coins` and `exchanges` with
  `api_key_invalid` (401, exit 2). `config key-info` showed `"expired": true`,
  and the doctor check read `Data API key configured`. The credential keeper's
  re-mint failed as well (`guest token refresh has failed for ~3m` in the lane
  log). Before a market read, run `control-om om -- config key-info --format
  json` and require `"expired": false`. Doctor's `api_key` line proves only
  that a key is present. Otherwise use a port whose home does not exist yet.
- **Guest sign-in is rate-limited.** A fresh home on 18144 failed to boot.
  `coins` reported `missing_api_key … could not start guest mode (HTTP 429):
  Too many guest sign-ins. Try again in 16 minute(s)`, and the daemon then
  exited with `om: No OpenMarket API key configured`. Same-morning runs (the
  nightly, other lanes) share the limit. Wait out the stated window and retry
  on a fresh port. A fresh home on 18145 booted at 09:51 and every read below
  passed.

- `--type` takes API enum values. `OHLCV` and `OHLCV_AGG` are both rejected
  server-side with `parsing list "type": ... is not a valid value`; candles are
  `TRADE_SIDE_AGNOSTIC_AGG`.
- The symbol flag is `--raw-symbol` (exchange-native) or `--normalized-symbol`
  or `--coin`. `--symbol` does not exist and fails as `unknown option`.
- `--lookback` is required. Omitting it fails before any request goes out.
- `metric list`, `metric get`, `metric series`, and `metric screen` are separate
  read paths. `resolve` binds order-ready instruments; it is not the chart
  symbol-directory lookup.
- `normalize.quote` USD-normalization is only applied to a whitelist of data
  types; funding rates and other dimensionless types return raw. A "wrong"
  normalized number may be the documented behavior — see `AGENTS.md`
  § Common pitfalls.
- The `Point` wrapper is easy to assert past by accident. A probe written as
  `list(p.get("Point", p))` prints plausible candle keys whichever shape came
  back, so it proves nothing about the envelope. Read the raw element once.
- These calls leave the machine. A failing `points` on an otherwise healthy lane
  is usually the network or the upstream API, not the change under test — check
  `control-om om -- doctor` before filing it.
- `om usage` reports the quota these reads consume. Since v0.408.1 it also has
  an `om usage llm` subcommand (`--since`, `--by provider|watch|model|day|hour`)
  reading a LOCAL token/cost ledger — a different question entirely, and not the
  Data API quota. Bare `om usage` is unchanged. A long drive can exhaust it.
- **`om usage plans` is not a Data API read either.** It reports each signed-in
  MODEL provider's plan (Anthropic, OpenAI Codex): its usage windows and the hold
  every model call reads before it dials (`actions/data/usage-plans.ts`, header).
  `--refresh` re-reads the usage pages and `--clear <provider>` lifts a
  provider's cap. A guest has no model provider, so it returns
  `{"providers":[],"cleared":null,"clear_lifted":null}` (driven 2026-10-23). An
  earlier pass filed it here as "Data API plan tiers". It lives in the
  market-data source folder, but it answers a model question.
- **`instruments` and `option-chain` are v3-socket reads.** On the default
  transport (`auto`, which never resolves to v3) both exit 2 `invalid_query` with
  `the catalog is served over the v3 socket only, and this install's data
  transport is not v3.` The hint names `om config set data.transport v3`, or
  `OM_DATA_TRANSPORT=v3 with OM_DATA_V3_URL`. On a guest lane,
  `OM_DATA_TRANSPORT=v3` alone on the CLI call was enough (driven 2026-10-23):
  `instruments BINANCE BTCUSDT --limit 3` returned `{exchange, arm:"crypto",
  rows[1], received, truncated}` and `option-chain DERIBIT BTC --neighbor-strikes
  1` returned `expiries`. Per source (`runner/v2/url.ts`), a home that sets
  `OM_BASE_URL` without `OM_DATA_V3_URL` resolves no v3 endpoint and falls back
  to the same refusal. #2114 changed only the signed-in path.
- **The `exchange_id` domain is narrower than `om exchanges`** (driven
  2026-10-28). On `auto`, `exchanges` listed 48 venues. (45 on 2026-10-30, a service-side count that moves.) `enum --list`
  reported `exchange_id` with 35, and `enum --domain exchange_id --query
  LIGHTER` gave `total: 0`. The CLI `markets --exchange LIGHTER` returned rows,
  but MCP `markets` with `exchanges:["LIGHTER"]` was refused with
  `"LIGHTER" is not a valid exchange_id`. This is a product gap (README). Do
  not take a venue from `exchanges` into an MCP call without checking the
  domain. Under `OM_DATA_TRANSPORT=v3`, `exchanges` returned 30 venues, and
  #2173 makes it refetch a cached directory that has no venue classes.
- **Enum discovery has two more forms.** `om enum --list` is the domain index
  (`domains[]` with `name`, `count`, `dynamic`, `sample`). `om enum --domain
  exchange_id --query BIN --limit 3` pages one domain (`total`, `offset`,
  `next_offset`). See [local reads and discovery](./local-reads-and-discovery.md).
