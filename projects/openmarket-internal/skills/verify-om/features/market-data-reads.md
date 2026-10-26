# Market data reads

*Verified: 2026-10-26, tree `ee8e3a7ab` (origin/main, v0.464.0), lane on 18103: doctor `api_key`/`network` ok. `enum` included `exchanges`, `types` and `intervals`; `exchanges` included `BINANCE` and `HYPERLIQUID`. `points` returned 3 `Point` wrappers, and `--type OHLCV` gave `is not a valid value`. `instruments` on the default transport gave exit 2 `invalid_query` with the v3 hint. With `OM_DATA_TRANSPORT=v3`, `instruments BINANCE BTCUSDT` returned `arm: crypto` with one row and `option-chain DERIBIT BTC` returned `expiries`. `usage plans` returned empty `providers`. Not driven: the typed-door `HISTORICAL_RETURN`/`TOKEN_UNLOCKS` reads (socket-only, new this range). Previous stamp `42d044b02` is an ancestor of this tree (46 commits).*

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
- **Proof.** Keep the exact command and the JSON (truncated to the first point
  or two is fine, but keep the full `id` block) plus the exit code.

## Gotchas

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
- **Enum discovery has two more forms.** `om enum --list` is the domain index
  (`domains[]` with `name`, `count`, `dynamic`, `sample`). `om enum --domain
  exchange_id --query BIN --limit 3` pages one domain (`total`, `offset`,
  `next_offset`). See [local reads and discovery](./local-reads-and-discovery.md).
