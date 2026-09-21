# Market data reads

*Verified: 2026-09-21, tree `b46838460` (v0.390.1) — enum and a live points series driven.*

The reason the daemon exists: `om` answers questions about markets from the
OpenMarket Data API. A user lists what is available (coins, exchanges, symbols,
enum domains) and then pulls history — candles, open interest, funding,
liquidations, heatmaps — with `om points`. These are pure reads, and a guest
lane's machine-minted key is enough for them.

## Sub-features

- `data-enum` lists the API's enum domains and their live values.
- `data-inventory` lists coins, exchanges, markets, symbols and tenors.
- `data-points` fetches a historical series for one type/exchange/symbol.
- `data-metric` computes scalar metrics over the same data.
- `data-resolve` turns a phrase into order-ready venue/symbol fields.

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
- `om usage` reports the quota these reads consume. A long drive can exhaust it.
