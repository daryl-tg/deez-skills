# tsdbctl — Market Data CLI

Query tsdb-gateway over WebSocket for time-series
financial data: OHLCV candles, open interest, funding
rates, liquidations, order book snapshots, and more.

## Setup

### Install

If you already have this repository cloned, install from
its root:

```bash
go install ./cmd/tsdbctl
```

If you do not have the repo cloned, install the latest
version by module path:

```bash
go install git.kiyotaka.dev/go-backend/tsdb-gateway/cmd/tsdbctl@latest
```

### Configure

```bash
tsdbctl config init
```

Creates `~/.config/tsdbctl/tsdbctl.yaml`. Multiple
contexts are supported:

```bash
tsdbctl config set-context prod \
  --api-host api.chart.kiyotaka.ai \
  --token eyJ... \
  --auth-method api_key

tsdbctl config use-context prod
tsdbctl config get-contexts
```

## Core workflow

```
tsdbctl get <resource> [key=value ...] [flags]
```

Comma-separated values expand to arrays:
`exchange=BINANCE,BYBIT`.

Examples below focus on query parameters. For agent or
script use, add `--format json -o <path>` unless you
intentionally want `toon` for compact inspection.

## Help and enum discovery

```bash
tsdbctl get --help              # list all resources
tsdbctl get points --help       # points-specific help
tsdbctl get markets -h          # markets-specific help
tsdbctl enum type               # all data types + fields
tsdbctl enum type TRADE         # filter by substring
tsdbctl enum exchange BINANCE   # exchanges matching BINANCE
tsdbctl enum interval           # aggregation intervals
tsdbctl enum category           # SPOT, PERPETUAL, etc.
tsdbctl enum signal             # market signals
tsdbctl enum groupBy            # aggregation functions
```

The `type` enum is special: it shows the response fields
for each type alongside the name. This tells you what
columns your query will return.

## Resources

| Resource | Required | Description |
|----------|----------|-------------|
| `points` | `type` | Time-series data (96% of traffic) |
| `latest-snapshots` | `type` | Latest value per series |
| `exchanges` | `type` | Exchanges for a data type |
| `categories` | `type` | Categories for type+exchange |
| `coins` | `type` | Coins for type+exchange |
| `symbols` | `type` | Raw symbols for type+exchange |
| `block-sizes` | `type` | Book snapshot block sizes |
| `registry` | `type` | Full metadata registry |
| `markets` | — | Market search with metrics |
| `coin-metrics` | `coin` | Coin-level aggregated metrics |
| `polymarket-markets` | — | Polymarket listings |

## Global flags

| Flag | Description |
|------|-------------|
| `-C`, `--context` | Override current context |
| `--config` | Override config file path |
| `--format` | `toon` (default) or `json` |
| `-o`, `--output` | Output file (`-` for stdout) |
| `--timeout` | Override context timeout |
| `--request-id` | Custom request ID for server-side correlation |
| `-v` | Debug logging |
| `-vv` | Trace logging (shows request body) |

## Common keys for points

| Key | Type | Description |
|-----|------|-------------|
| `type` | enum list | Data type (required) |
| `exchange` | enum list | Exchange filter |
| `category` | enum list | PERPETUAL, FUTURE, etc. |
| `coin` | string list | Coin filter (BTC, ETH) |
| `rawSymbol` | string list | Exchange-native symbol |
| `interval` | enum | Bucket size |
| `from` | timestamp | Start (unix seconds) |
| `period` | duration | Window (seconds or `1h`, `30m`) |
| `limit` | int | Max rows |
| `side` | enum | BUY or SELL |
| `blockSize` | float | Book snapshot block size |
| `maxDepth` | int | Book depth levels |

## Transform keys

Collapse multiple series into one aggregated series:

| Key | Type | Description |
|-----|------|-------------|
| `groupBy` | enum | SUM, AVG, OPEN_INTEREST_WEIGHTED_AVG, etc. |
| `groupBy.fields` | enum list | Fields to preserve (SIDE, EXCHANGE) |
| `normalize.quote` | string | Quote currency: `USD` or `coins` |
| `normalize.fundingInterval` | int | Funding interval in ms |

---

## Field naming: what you actually get back

The `tsdbctl enum type` output shows canonical field names,
but the JSON output often differs. Rules:

- Most types use **camelCase** in JSON:
  `rateClose`, `longShortRatio`, `volatilityIndexClose`,
  `impliedVolatility`, `sharesOutstanding`.

- `MARKET_EVENT` is the exception — it uses **snake_case**:
  `event_id`, `event_slug`, `market_slug`,
  `narrative_findings`. The enum says `eventId` etc. but
  the JSON disagrees.

- `_AGG` types sometimes prefix data fields with `last`
  compared to their non-aggregated counterparts.
  `ETF_FLOW.flows` becomes `ETF_FLOW_AGG.flows` (not
  `lastFlows` as the enum claims — the enum is wrong here).
  `CFTC_COT_AGG` does use `last`-prefixed fields:
  `lastDealerLongPosition`, `lastAssetManagerLongPosition`.

- `groupBy` **strips identity fields** from the response.
  A per-symbol OI query returns `exchange`, `coin`,
  `symbol`, `normalizedSymbol`, `category`. A
  `groupBy=SUM` query returns only `open`, `high`, `low`,
  `close`, `interval`, `timestamp`, `type`.

- Every response row includes `type`, `interval`, and
  `timestamp` (nanoseconds). Most include `exchange`,
  `coin`, `symbol`, `normalizedSymbol`, `category` unless
  aggregated away by `groupBy`.

When in doubt, fetch one row with `period=5m limit=1` and
inspect the keys.

## Units and value semantics

These are not documented anywhere but matter:

- **Timestamps** in responses are **unix nanoseconds**.
  The `from` parameter takes **unix seconds**. Easy to
  confuse.

- **`impliedVolatility`**: already percentage points.
  `50.6` means 50.6% IV. Do not multiply by 100.

- **`skew`**: already percentage points. `+11.0` means
  calls trade 11% above puts. Positive = calls premium
  (bullish), negative = puts premium (bearish).

- **`volatilityIndexClose`** (DVOL): index value, not
  a percentage. `51.0` is the DVOL level.

- **`longAccountPct` / `shortAccountPct`**: already
  percentages. `58.6` means 58.6%. Do not multiply by 100.

- **`longShortRatio`**: raw ratio. `1.41` means 1.41
  longs per short.

- **`rate` (margin)**: decimal. `0.00008` means 0.008%.
  Multiply by 100 for percentage display.

- **`rateClose` (funding)**: decimal. `0.000006` means
  0.0006%/h. Multiply by 100 for percentage display.
  Multiply by 8760 then by 100 for annualized percentage.

- **`flows` (ETF)**: millions of USD. `71.1` means
  $71.1M inflow. Negative = outflow.

- **`premiumRate` (ETF)**: decimal premium/discount vs NAV.

- **`volume` with `normalize.quote=USD`**: USD-denominated.
  A daily BTC volume of `7.2e9` means $7.2B.

- **`volume` with `normalize.quote=coins`**: coin units.

- **`liquidations`**: USD value when `normalize.quote=USD`
  is applied.

- **CFTC COT positions**: contract counts, not USD.

- **Bitfinex `longPos`/`shortPos`**: coin units (BTC).

## TRADE_AGG vs TRADE_SIDE_AGNOSTIC_AGG

`TRADE_AGG` returns **two rows per timestamp** — one for
`side=BUY`, one for `side=SELL`. This means you get
buy-volume and sell-volume candles separately. The
`normalize.quote=USD` transform is commonly applied (73%
of production queries).

`TRADE_SIDE_AGNOSTIC_AGG` merges buy+sell into **one row
per timestamp** with no `side` field. Never uses
transforms. Use this when you only need combined OHLCV and
don't care about buy/sell split.

When using `TRADE_AGG` for price analysis, either filter
to one side or take the close from the latest-timestamped
row. Both sides share the same OHLC; only volume differs.

## Order book snapshots

`BLOCK_BOOK_SNAPSHOT_AGG` and `SYNTHETIC_BLOCK_BOOK_SNAPSHOT_AGG`
return `bids` and `asks` as flat arrays:

```
[price, size, price, size, price, size, ...]
```

Parse as pairs: `[(data[0], data[1]), (data[2], data[3]), ...]`.
Bids are sorted descending (best bid first), asks ascending
(best ask first). Sizes are in base currency unless
`normalize.quote=USD` is applied.

Requires `blockSize` (price bucket width) and `maxDepth`
(number of levels). Use `tsdbctl get block-sizes
type=BLOCK_BOOK_SNAPSHOT_AGG` to discover valid block sizes,
though the output may be sparse.

For **current** book state, use `latest-snapshots` not
`points`. The `points` resource returns time-bucketed
snapshots that collapse the book into just `s` (a timestamp)
with no bid/ask data.

```bash
tsdbctl get latest-snapshots \
  type=BLOCK_BOOK_SNAPSHOT_AGG \
  exchange=BINANCE_FUTURES rawSymbol=BTCUSDT \
  blockSize=25 maxDepth=50 normalize.quote=USD
```

For cross-exchange book aggregation, query each exchange
separately and merge in your script. `groupBy=SUM` on
`points` works for historical snapshots but loses price
level information.

## Polymarket

Five ways to access Polymarket data:

**1. `markets` with `exchange=POLYMARKET`** — richest
view. Returns grouped prediction markets with live
pricing, volume, liquidity, OI, and nested sub-markets.

```bash
# Top 50 Polymarket markets by default ranking
tsdbctl get markets exchange=POLYMARKET type=TRADE \
  pageSize=50 --format json -o polymarket.json

# Filter to crypto-tagged markets
tsdbctl get markets exchange=POLYMARKET type=TRADE \
  tagSlugs=crypto pageSize=20 --format json \
  -o polymarket_crypto.json
```

Top-level fields per row:
- `title`, `fullName`: market name
- `coin`, `rawSymbol`, `normalizedSymbol`: slug-based
  identifiers (e.g. `hungary-parliamentary-election-winner`)
- `volume24h`: 24h volume in USD
- `totalVolume`: lifetime volume in USD
- `liquidity`: current liquidity in USD
- `closed`: `"true"` or `"false"` (string, not bool)
- `availableSince`, `availableTo`: nanosecond timestamps
- `tags`: JSON array of `{id, label, slug}` objects.
  Common tag slugs: `crypto`, `politics`, `sports`,
  `elections`, `finance`, `economics`
- `predictionMarkets`: JSON array of sub-markets

Each sub-market in `predictionMarkets` contains:
- `question`: the yes/no question
- `slug`: URL slug, also the key for trade data
- `lastPrice`: current probability (0.0–1.0)
- `oneDayPriceChange`: 24h price delta
- `prices`: array of recent hourly prices
- `openInterest`, `oneDayOIChange`
- `totalVolume`, `buyVolume24H`, `sellVolume24H`
- `uniqueTraders`: total unique traders
- `conditionId`: hex ID for raw trade/book queries
- `outcomes`: typically `["Yes", "No"]`
- `geoLocations`: array of `{country, country_code}`
- `orderPriceMinTickSize`: minimum price increment

Pagination: `pageSize` (default 10, max unclear) +
`pageOffset`. Filter by `tagSlugs` for topic-specific
markets. The `predictionMarkets` field is nested —
use `--format toon` for compact LLM-friendly output.

**2. `polymarket-markets`** — Polymarket-native API.
Lighter metadata, different field set.

```bash
tsdbctl get polymarket-markets \
  lite=true closed=false limit=50

tsdbctl get polymarket-markets \
  closed=false tags=crypto limit=20

tsdbctl get polymarket-markets slug=us-election-2024
```

Keys: `lite` (bool), `closed` (bool), `archived` (bool),
`limit` (int), `offset` (int), `slug` (string list),
`tags` (string list), `conditionId` (string list),
`marketId` (int list), plus various timestamp filters
(`closedTimeFrom`, `createdAtFrom`, etc.).

`lite=true` returns: `id`, `question`, `slug`,
`conditionId`, `active`.
`lite=false` adds: `description`.

**3. `MARKET_EVENT`** — AI-generated event analysis tied
to Polymarket markets.

```bash
tsdbctl get points type=MARKET_EVENT \
  exchange=POLYMARKET period=48h --format json \
  -o market_events.json
```

Fields (snake_case, unlike other types):
- `title`: AI-generated headline
- `intensity`: 1-5 significance score
- `event_slug`, `market_slug`: Polymarket identifiers
- `narrative_findings`: AI commentary text
- `markets`: JSON array of related markets, each with
  `market_id`, `question`, `anomalies`,
  `composite_anomaly_score`, `signal_probabilities`,
  `z_score`

No `interval` needed. Use `period` for the time window.

**4. Raw trade data** via `TRADE_SIDE_AGNOSTIC_AGG`
with `exchange=POLYMARKET`.

**`rawSymbol` must be a hex `conditionId`, not a slug.**
The symbols table contains only `0x...` hex IDs
(779k+ entries). Slugs like
`will-silver-si-hit-by-end-of-february` silently
return zero rows — no error, just empty output.

To get the hex ID for a market you found by name,
look it up through one of the discovery resources:

```bash
# Option A: polymarket-markets (fastest, lite mode)
tsdbctl get polymarket-markets \
  slug=my-market-slug lite=true \
  -o pm_lookup.json
# → conditionId column has the 0x... value

# Option B: markets resource (richer metadata)
tsdbctl get markets exchange=POLYMARKET \
  type=TRADE pageSize=50 --format json \
  -o pm_markets.json
# → each predictionMarkets[] entry has conditionId
```

Then use the `conditionId` as `rawSymbol`:

```bash
tsdbctl get points type=TRADE_SIDE_AGNOSTIC_AGG \
  exchange=POLYMARKET \
  rawSymbol=0x4adf6423... \
  interval=HOUR period=168h \
  -o pm_trades.json
```

Prices are probabilities (0.0–1.0). Volume is in the
market's denomination.

**Raw tick data** is also available via the `TRADE`
type. Each row is one fill with `price`, `amount`,
`side`, plus `id` (trade hash) and `symbol` (token
ID). Use `rawSymbol=<conditionId>` to filter by
market outcome:

```bash
tsdbctl get points type=TRADE \
  exchange=POLYMARKET \
  rawSymbol=0xfcde02af... \
  period=3600 limit=100 \
  -o pm_ticks.json
```

Response fields: `price` (probability 0–1), `amount`
(outcome token quantity), `side` (BUY/SELL), `id`
(unique trade hash), `symbol` (token-level hex ID,
different from conditionId).

**5. Book snapshots** via `BLOCK_BOOK_SNAPSHOT_AGG`
or `BOOK_SNAPSHOT_AGG` with `exchange=POLYMARKET`.
Polymarket has extensive order book coverage — 829k+
symbol entries in the `BOOK_SNAPSHOT_AGG` registry.

Use `blockSize=0.001` for `BLOCK_BOOK_SNAPSHOT_AGG`
on probability markets. Bids/asks are flat arrays
like other book types, but prices are probabilities
(0-1) and sizes are in the market's denomination.

Same rule: `rawSymbol` must be a hex `conditionId`,
not a slug. Look it up via `polymarket-markets` or
`markets` first (see step 4 above).

```bash
# Block-aggregated book for a specific outcome
tsdbctl get points type=BLOCK_BOOK_SNAPSHOT_AGG \
  exchange=POLYMARKET \
  rawSymbol=0xfcde02af... \
  blockSize=0.001 maxDepth=10 \
  interval=MINUTE period=5m --format json \
  -o pm_book.json

# Raw book snapshots (no block aggregation)
tsdbctl get points type=BOOK_SNAPSHOT_AGG \
  exchange=POLYMARKET \
  rawSymbol=0xfcde02af... \
  interval=MINUTE period=5m --format json \
  -o pm_rawbook.json
```

## Market signals

The `markets` resource supports signal-based filtering.
Valid signals (from `tsdbctl enum signal`):

```
HIGH_LONG_FUNDING_RATE
HIGH_SHORT_FUNDING_RATE
HIGH_VOLATILITY
LARGE_OI_INCREASE
PASSED_ATH
RANGE_BOUND
TRENDING
VOLUME_SPIKE
```

```bash
tsdbctl get markets signal=VOLUME_SPIKE pageSize=10
tsdbctl get markets signal=PASSED_ATH pageSize=5
```

Only these exact values work. `PRICE_SPIKE`, `OI_SPIKE`,
`LIQUIDATION_SPIKE` etc. are not valid and return errors.

## coin-metrics fields

`coin-metrics` returns a single snapshot row per coin with
these fields:

- `price`, `pricePercentageChange24H`
- `marketcap`
- `totalVolume24H`
- `totalOpenInterest24H`,
  `openInterestPercentageChange24H`
- `oiwaFundingRate24H`,
  `oiwaFundingRatePercentageChange24H`
- `atrPercent`
- `pctFromATH` (available on `markets` resource)

`oiwaFundingRate24H` is a decimal (not percentage).
Multiply by 100 for display.

## Rate limiting

The gateway enforces per-connection rate limits. When
making many sequential queries (>10 in quick succession),
you may get `too many requests` errors. Add small delays
between requests in scripts, or batch related queries.

---

## Tick (non-AGG) types

Most types come in pairs: a raw **tick** type and an
`_AGG` aggregate. The tick type returns individual
data points (each trade, each OI snapshot, each funding
rate tick) with no time bucketing. No `interval`
parameter — you get every row within the time window.

Tick types work with `points` just like AGG types.
Use `period` and `limit` to control the volume.

Common tick types and their fields:

| Type | Fields |
|------|--------|
| `TRADE` | `price`, `amount`, `quoteAmount`, `side` |
| `OPEN_INTEREST` | `openInterest` |
| `FUNDING_RATE` | `fundingRate` |
| `LIQUIDATION` | `price`, `amount`, `side` |
| `LONG_SHORT_RATIO` | `longShortRatio`, `longAccountPct`, `shortAccountPct`, plus `topTraders*` variants |
| `BOOK_SNAPSHOT` | `bids`, `asks` |
| `BOOK_CHANGE` | `side`, `price`, `amount` |
| `BOOK_TOP` | `bids`, `asks` |
| `IMPLIED_VOLATILITY` | `impliedVolatility` |
| `SKEW` | `skew` |
| `PREDICTED_FUNDING_RATE` | `predictedFundingRate` |

Tick data is dense — a 1-minute window of `TRADE` on
BTCUSDT returns hundreds of rows. Always use `limit`
or short `period` values to avoid pulling excessive
data.

```bash
# Individual BTC trades (last 10 seconds, max 5)
tsdbctl get points type=TRADE \
  exchange=BINANCE_FUTURES rawSymbol=BTCUSDT \
  period=10s limit=5

# Raw OI snapshots (tick-level, last minute)
tsdbctl get points type=OPEN_INTEREST \
  exchange=BINANCE_FUTURES rawSymbol=BTCUSDT \
  period=1m limit=5

# Individual liquidation events
tsdbctl get points type=LIQUIDATION \
  exchange=BINANCE_FUTURES rawSymbol=BTCUSDT \
  period=1h limit=10
```

The full list of tick types is visible via
`tsdbctl enum type` — every entry without an `_AGG`
suffix that has a matching `_AGG` counterpart is a
tick type. Some types (like `BOOK_TOP`, `VWAP`, `EMA`)
exist only in one form.

---

## Type reference — production traffic

Based on 1.27M requests (March 2026). Types listed by
frequency with typical intervals, transforms, and examples.

### TRADE_AGG — 49.4%

OHLCV candlestick data split by side.

**Fields:** `open`, `high`, `low`, `close`, `volume`,
`firstTimestamp`, `lastTimestamp`, `side`.

Returns two rows per candle (BUY + SELL). Volume differs
between sides; OHLC is the same.

**Intervals:** 15m (34%), 5m (20%), 1h (16%), 1m (11%),
4h (9%), 30m (5%), 1d (1%).

**Transforms:** `normalize.quote=USD` (73%),
`normalize.quote=coins` (17%), none (10%).

```bash
tsdbctl get points type=TRADE_AGG \
  exchange=BINANCE_FUTURES rawSymbol=BTCUSDT \
  interval=FIFTEEN_MINUTES period=1800 \
  normalize.quote=USD

tsdbctl get points type=TRADE_AGG \
  exchange=BINANCE_FUTURES rawSymbol=BTCUSDT \
  interval=DAY period=720h \
  normalize.quote=USD
```

### TRADE_SIDE_AGNOSTIC_AGG — 24.6%

Buy+sell merged. One row per candle, no `side` field.
Never uses transforms.

**Fields:** `open`, `high`, `low`, `close`, `volume`,
`firstTimestamp`, `lastTimestamp`.

```bash
tsdbctl get points type=TRADE_SIDE_AGNOSTIC_AGG \
  exchange=BINANCE_FUTURES rawSymbol=BTCUSDT \
  interval=FIFTEEN_MINUTES period=1800
```

### OPEN_INTEREST_AGG — 7.4%

**Fields:** `open`, `high`, `low`, `close`.

Cross-exchange aggregation is the primary use case.

**Transforms:** `groupBy=SUM normalize.quote=USD` (47%),
per-symbol `normalize.quote=USD` (32%),
`groupBy=SUM normalize.quote=coins` (15%).

```bash
# Cross-exchange BTC OI
tsdbctl get points type=OPEN_INTEREST_AGG \
  coin=BTC category=PERPETUAL,FUTURE \
  exchange=DERIBIT,BINANCE_FUTURES,OKEX_SWAP,BYBIT,HYPERLIQUID_FUTURES \
  interval=HOUR period=48h \
  groupBy=SUM normalize.quote=USD

# Per-symbol
tsdbctl get points type=OPEN_INTEREST_AGG \
  exchange=BINANCE_FUTURES rawSymbol=BTCUSDT \
  interval=HOUR period=24h \
  normalize.quote=USD
```

### LIQUIDATION_AGG — 4.0%

**Fields:** `liquidations`, `side` (when
`groupBy.fields=SIDE`).

Without `groupBy.fields=SIDE`, liquidations are summed
across both sides. With it, you get separate BUY and SELL
rows. `side=BUY` means shorts were liquidated (forced buy).
`side=SELL` means longs were liquidated (forced sell).

```bash
tsdbctl get points type=LIQUIDATION_AGG \
  category=PERPETUAL coin=BTC \
  exchange=DERIBIT,BINANCE_FUTURES,OKEX_SWAP,BYBIT,HYPERLIQUID_FUTURES \
  interval=HOUR period=48h \
  groupBy=SUM groupBy.fields=SIDE normalize.quote=USD
```

### FUNDING_RATE_AGG — 3.9%

**Fields:** `rateOpen`, `rateHigh`, `rateLow`, `rateClose`.

Values are decimals. A `rateClose` of `0.000006` means
0.0006%/h. To annualize: multiply by 8760 * 100.

`normalize.fundingInterval=3600000` normalizes to hourly
regardless of exchange-specific intervals. Without it,
rates reflect each exchange's native interval (typically
8h for most, 1h for Hyperliquid).

`groupBy=OPEN_INTEREST_WEIGHTED_AVG` produces a single
cross-exchange rate weighted by each exchange's OI.

```bash
tsdbctl get points type=FUNDING_RATE_AGG \
  category=PERPETUAL coin=BTC \
  exchange=DERIBIT,BINANCE_FUTURES,OKEX_SWAP,BYBIT,HYPERLIQUID_FUTURES \
  interval=HOUR period=48h \
  groupBy=OPEN_INTEREST_WEIGHTED_AVG \
  normalize.fundingInterval=3600000
```

### LONG_SHORT_RATIO_AGG — 0.3%

**Fields:** `longShortRatio`, `longAccountPct`,
`shortAccountPct`, plus `topTraders*` variants for
account-level and position-level ratios, plus `last*`
prefixed snapshots.

All percentage fields are already in percent (58.6 means
58.6%). The ratio is raw (1.41 means 1.41:1 long:short).

Interesting divergence signal: retail `longAccountPct` vs
`topTradersPositionLongAccountPct`. When retail is long
but top traders are net short, it often precedes
mean-reversion.

```bash
tsdbctl get points type=LONG_SHORT_RATIO_AGG \
  exchange=BINANCE_FUTURES rawSymbol=BTCUSDT \
  interval=HOUR period=48h
```

### BLOCK_BOOK_SNAPSHOT_AGG — 1.6%

See "Order book snapshots" section above.

### IMPLIED_VOLATILITY_OPTION_SUMMARY_AGG

**Fields:** `impliedVolatility`.

Value is percentage points. `50.6` means 50.6% IV.

```bash
tsdbctl get points \
  type=IMPLIED_VOLATILITY_OPTION_SUMMARY_AGG \
  exchange=DERIBIT rawSymbol=BTC_ATM \
  interval=HOUR period=48h
```

### SKEW_OPTION_SUMMARY_AGG

**Fields:** `skew`.

Value is percentage points. `+11.0` means 25-delta calls
are 11% more expensive than 25-delta puts. Positive =
calls premium (bullish skew). Use `rawSymbol=BTC_25` for
25-delta skew.

```bash
tsdbctl get points type=SKEW_OPTION_SUMMARY_AGG \
  exchange=DERIBIT rawSymbol=BTC_25 \
  interval=FOUR_HOURS period=48h
```

### VOLATILITY_INDEX_AGG

**Fields:** `volatilityIndexOpen`, `volatilityIndexHigh`,
`volatilityIndexLow`, `volatilityIndexClose`.

Deribit DVOL. Raw index value, not a percentage.

```bash
tsdbctl get points type=VOLATILITY_INDEX_AGG \
  exchange=DERIBIT rawSymbol=btc_usd \
  interval=HOUR period=48h
```

### CME_OPEN_INTEREST_AGG

**Fields:** `open`, `high`, `low`, `close` (contract OI),
`valueOpen`..`valueClose` (USD value),
`priceOpen`..`priceClose` (contract price).

```bash
tsdbctl get points type=CME_OPEN_INTEREST_AGG \
  exchange=CME rawSymbol=BTC \
  interval=DAY period=720h
```

### ETF_FLOW_AGG

**Fields:** `flows`.

Values are in millions of USD. `71.1` = $71.1M inflow.
Negative = outflow. The enum claims `lastFlows` but the
actual JSON field is `flows`.

```bash
tsdbctl get points type=ETF_FLOW_AGG \
  rawSymbol=IBIT,FBTC,GBTC,ARKB,BITB \
  issuer=BLACKROCK,FIDELITY,GRAYSCALE,ARK,BITWISE \
  interval=DAY period=720h
```

### ETF_METRICS_AGG

**Fields:** `aum`, `sharesOutstanding`, `holdings`.

```bash
tsdbctl get points type=ETF_METRICS_AGG \
  rawSymbol=IBIT interval=DAY period=168h
```

### ETF_PREMIUM_RATE_AGG

**Fields:** `premiumRate`.

Decimal premium/discount vs NAV.

```bash
tsdbctl get points type=ETF_PREMIUM_RATE_AGG \
  coin=BTC issuer=BLACKROCK rawSymbol=IBIT \
  interval=HOUR period=168h
```

### VWAP

**Fields:** `vwap`.

```bash
tsdbctl get points type=VWAP \
  exchange=BINANCE rawSymbol=BTCUSDT \
  interval=FOUR_HOURS period=168h
```

### EMA

**Fields:** `ema`.

```bash
tsdbctl get points type=EMA \
  exchange=BINANCE rawSymbol=BTCUSDT \
  interval=DAY period=720h
```

### BINANCE_SPOT_MARGIN_RATE_AGG

**Fields:** `rate`.

Decimal. `0.00008` means 0.008%.

```bash
tsdbctl get points type=BINANCE_SPOT_MARGIN_RATE_AGG \
  exchange=BINANCE rawSymbol=USDT \
  interval=FOUR_HOURS period=168h
```

### CFTC_COT_AGG

**Fields:** `lastDealerLongPosition`,
`lastDealerShortPosition`,
`lastAssetManagerLongPosition`,
`lastAssetManagerShortPosition`,
`lastHedgeFundLongPosition`,
`lastHedgeFundShortPosition`,
`lastOtherReportableLongPosition`,
`lastOtherReportableShortPosition`,
`lastNonReportableLongPosition`,
`lastNonReportableShortPosition`,
`lastLastUpdatedDate`.

Values are contract counts, not USD.

Hedge funds are typically net short (basis trade: long
spot/ETF, short futures). Asset managers net long.

```bash
tsdbctl get points type=CFTC_COT_AGG \
  exchange=CME rawSymbol=BTC \
  interval=FOUR_HOURS period=336h
```

### BITFINEX_POSITION_AGG

**Fields:** `longPos`, `shortPos`.

Values in coin units (BTC, ETH, etc.).

```bash
tsdbctl get points type=BITFINEX_POSITION_AGG \
  exchange=BITFINEX rawSymbol=BTCUSD \
  interval=DAY period=336h
```

### CRYPTO_NARRATIVE_FINDING

AI-generated narrative analysis linking news events to
specific coins. Each finding describes a market-moving
development — regulatory changes, protocol upgrades,
corporate treasury moves, ETF activity, partnerships,
geopolitical events — and ties it to a coin symbol.

Covers 50+ coins. Typical volume is ~200 findings per
week, with BTC, SOL, ETH, and trending tokens getting
the most coverage. Findings are grouped by
`narrativeId`; a single narrative can produce multiple
findings across related coins.

**Fields (snake_case in JSON, unlike enum output):**
- `finding_id`: unique finding identifier
- `symbol`: coin symbol (BTC, ETH, SOL, etc.)
- `narrative_id`: groups related findings
- `narrative_name`: headline summary
- `event`: detailed description of the development
- `tweet_ids`: JSON array of source tweet IDs

No `interval` needed. Filter by `coin=` (not
`rawSymbol=`). Omit the coin filter to get all
narratives across the market.

```bash
# All narratives from the past week
tsdbctl get points type=CRYPTO_NARRATIVE_FINDING \
  period=168h --format json -o narratives.json

# BTC-specific narratives
tsdbctl get points type=CRYPTO_NARRATIVE_FINDING \
  coin=BTC period=168h --format json -o narratives_btc.json

# Recent narratives (last 2 hours)
tsdbctl get points type=CRYPTO_NARRATIVE_FINDING \
  period=2h --format json -o narratives_recent.json
```

Useful for sentiment analysis, identifying catalysts
behind price moves, or screening which coins have
active news flow.

### MARKET_EVENT

See "Polymarket" section above. Fields use snake_case.

### HISTORICAL_RETURN

**Fields:** `returnPercentage`.

Returns seem to represent something other than simple
daily price change — values can be implausibly high (e.g.
+16% daily for extended periods). Treat with caution
until the semantics are clarified. May be cumulative
or cross-asset averaged when `groupBy=AVG` is used.

```bash
tsdbctl get points type=HISTORICAL_RETURN \
  exchange=BINANCE_FUTURES rawSymbol=BTCUSDT \
  interval=DAY period=720h
```

### TPO_AGG

Volume profile / time-price opportunity. Returns one row
per session with a `levels` field containing a JSON array
of price-level objects.

**Fields:** `levels` (JSON array), `period_start`,
`period_end`.

Each level: `{"price": 68799, "block_ids": [42],
"buy_volume": 500.2, "sell_volume": 503.9}`.
Some levels only have `sell_volume` or `buy_volume`.

Use `tpoSession=DAILY` for daily sessions. The POC
(point of control) is the price level with the highest
total volume.

```bash
tsdbctl get points type=TPO_AGG \
  exchange=BINANCE_FUTURES rawSymbol=BTCUSDT \
  interval=FIFTEEN_MINUTES period=24h \
  tpoSession=DAILY

# Cross-exchange
tsdbctl get points type=TPO_AGG coin=BTC \
  exchange=BINANCE_FUTURES,OKEX_SWAP,BYBIT \
  interval=HOUR period=24h \
  tpoSession=DAILY groupBy=SUM
```

### VOLUME_PROFILE_AGG

**Fields:** `profile` (flat array).

Flat array of triplets: `[price, buy_vol, sell_vol,
price, buy_vol, sell_vol, ...]`. Parse as groups of 3.
Volumes are in coin units with `normalize.quote=coins`.

```bash
tsdbctl get points type=VOLUME_PROFILE_AGG \
  exchange=BINANCE_FUTURES rawSymbol=BTCUSDT \
  interval=HOUR period=24h \
  normalize.quote=coins
```

### VOLUME_DELTA

Cumulative volume delta (buy - sell pressure).

**Fields:** `delta`, `cumulative_delta`.

Negative cumulative delta = net selling pressure over
the period. Delta is the per-candle difference.

```bash
tsdbctl get points type=VOLUME_DELTA \
  exchange=BINANCE_FUTURES rawSymbol=BTCUSDT \
  interval=FIFTEEN_MINUTES period=6h
```

### OPTION_SUMMARY_IV_AGG

Full IV surface across all strikes and expirations.

**Fields:** `markIv`, `bidIv`, `askIv`.

Returns one row per strike/expiry combination. Symbols
are like `BTC-10APR26-60000-C`. Parse the symbol to
extract strike and type (C/P). Values are percentage
points.

Returns thousands of rows per query — use short periods.

```bash
tsdbctl get points type=OPTION_SUMMARY_IV_AGG \
  exchange=DERIBIT interval=HOUR period=6h
```

### OPTION_OPEN_INTEREST_AGG

Per-strike options open interest.

**Fields:** `oiClose`, `underlyingPriceClose`.

Symbols encode strike and type:
`BTC-10APR26-60000-P`. Parse to aggregate by strike
for max-pain analysis. OI is in BTC.

```bash
tsdbctl get points type=OPTION_OPEN_INTEREST_AGG \
  exchange=DERIBIT coin=BTC \
  interval=HOUR period=6h
```

### PREDICTED_FUNDING_RATE_AGG

Predicted next funding rate in OHLC format.

**Fields:** `open`, `high`, `low`, `close`.

Values are decimals like funding rates. Use with
`coin=` filter (not `rawSymbol`).

```bash
tsdbctl get points type=PREDICTED_FUNDING_RATE_AGG \
  coin=BTC interval=HOUR period=48h
```

### HYPERLIQUID_LIQUIDATION_AGG

Liquidation heatmap data for Hyperliquid.

**Fields:** `levels` (flat array).

Flat `[price, size, price, size, ...]` pairs like book
snapshots. Price is the liquidation price bucket, size
is the notional amount. `maxDepth` controls how many
levels. Can return thousands of levels.

```bash
tsdbctl get points type=HYPERLIQUID_LIQUIDATION_AGG \
  coin=BTC interval=FIFTEEN_MINUTES \
  maxDepth=1500 period=6h
```

### TREASURY_INFO_AGG

Corporate BTC treasury holdings. Covers public companies
holding BTC on their balance sheets.

**Fields (snake_case in JSON):** `last_holdings`,
`last_asset_nav`, `last_marketcap`, `last_mnav`,
`last_enterprise_value`, and more.

`last_holdings` is BTC count. `last_mnav` is the ratio
of market cap to NAV (>1 = premium, <1 = discount).
Returns rows for dozens of entities (MSTR, MARA, RIOT,
TSLA, etc.).

```bash
tsdbctl get points type=TREASURY_INFO_AGG \
  coin=BTC interval=DAY period=720h
```

### BINANCE_FUTURES_INSURANCE_BALANCE_AGG

Binance Futures insurance fund balance.

**Fields:** `usdtBalance`, `btcBalance` (btcBalance
may be absent in newer rows).

Declining insurance fund can signal elevated liquidation
risk on the platform.

```bash
tsdbctl get points \
  type=BINANCE_FUTURES_INSURANCE_BALANCE_AGG \
  interval=DAY period=720h
```

### BYBIT_LENDING_INFO_AGG / BYBIT_BORROW_INFO_AGG

Bybit lending and borrowing rates.

**Lending fields:** `apy`, `usageRate`.
**Borrowing fields:** `annual7DInterestRate`,
`annual30DInterestRate`, `annual90DInterestRate`,
`hourly*` variants, `minBorrowAmount`, `maxBorrowAmount`.

APY and rates are decimals. `usageRate` of 0.56 means
56% utilization.

```bash
tsdbctl get points type=BYBIT_LENDING_INFO_AGG \
  exchange=BYBIT rawSymbol=BTC \
  interval=DAY period=168h

tsdbctl get points type=BYBIT_BORROW_INFO_AGG \
  exchange=BYBIT rawSymbol=BTC \
  interval=DAY period=168h
```

### ETF_NAV_AGG

**Fields:** `nav`.

Net asset value per share. IBIT NAV around $39-40 at
current BTC prices.

```bash
tsdbctl get points type=ETF_NAV_AGG \
  rawSymbol=IBIT interval=DAY period=168h
```

### HISTORICAL_VOLATILITY_AGG

**Fields:** `historicalVolatility`.

Realized vol. Values are percentage points (43.6 =
43.6% annualized realized volatility).

```bash
tsdbctl get points type=HISTORICAL_VOLATILITY_AGG \
  coin=BTC interval=DAY period=720h
```

### MARGIN_DEBT_GROWTH_AGG

**Fields:** `marginDebtGrowth`.

Daily rate of change in margin debt. Small decimal
values (e.g. -0.0036 = -0.36% daily change).

```bash
tsdbctl get points type=MARGIN_DEBT_GROWTH_AGG \
  coin=BTC interval=DAY period=720h
```

### TOKEN_SUPPLY_AGG

**Fields:** `marketcap`, `circulatingSupply`,
`totalSupply`, `maxSupply`, `totalValueLocked`,
`fullyDilutedValuation`, `cgMarketcapRank`,
`totalVolume`, `usdPrice`, `chain`, `contractAddress`,
and more.

Returns multiple rows per timestamp when a coin exists
on multiple chains. `coin=BTC` returns both native and
wrapped variants.

```bash
tsdbctl get points type=TOKEN_SUPPLY_AGG \
  coin=BTC interval=DAY period=168h
```

### SECTOR_DOMINANCE_AGG

**Fields:** `marketcapDominance`, `volumeDominance`.

No coin/symbol filter available. Returns aggregate
dominance metrics without sector labels (data may be
incomplete).

### HYPERLIQUID_LIQUIDATION_EVENT_AGG

Individual liquidation events on Hyperliquid.

**Fields:** `size`, `closedPnl`, `side`.

Sparse — only populated when liquidations occur.

```bash
tsdbctl get points \
  type=HYPERLIQUID_LIQUIDATION_EVENT_AGG \
  coin=BTC interval=FIFTEEN_MINUTES period=6h
```

### PREMIUM_INDEX_KLINE_AGG

Futures premium/discount vs spot index price.

**Fields:** `open`, `high`, `low`, `close`.

Small decimal values. Negative = futures below spot
(backwardation). `-0.00054` means futures are 0.054%
below spot.

```bash
tsdbctl get points type=PREMIUM_INDEX_KLINE_AGG \
  exchange=BINANCE_FUTURES rawSymbol=BTCUSDT \
  interval=HOUR period=24h
```

### BINANCE_OI_AND_VOLUME_SUM_AGG

Binance Futures aggregate OI and volume for a symbol.

**Fields:** `sumOpenInterest` (BTC),
`sumOpenInterestNotional` (USD), `sumVolume` (BTC),
`sumVolumeNotional` (USD).

```bash
tsdbctl get points \
  type=BINANCE_OI_AND_VOLUME_SUM_AGG \
  exchange=BINANCE_FUTURES \
  interval=HOUR period=24h
```

### BINANCE_PROOF_OF_RESERVES_AGG

**Fields:** `ratio`, `binance_liability`,
`customer_liability`.

Ratio >1 means Binance holds more than customer
liabilities. Sparse data — may return only 1 row.

```bash
tsdbctl get points \
  type=BINANCE_PROOF_OF_RESERVES_AGG \
  coin=BTC interval=DAY period=720h
```

### BINANCE_INSURANCE_BALANCE_AGG

Per-coin insurance fund balances (all Binance pairs).

**Fields:** `balance`.

Returns one row per coin per timestamp. 651+ coins.
For the futures-specific USDT/BTC insurance fund, use
`BINANCE_FUTURES_INSURANCE_BALANCE_AGG` instead.

```bash
tsdbctl get points \
  type=BINANCE_INSURANCE_BALANCE_AGG \
  interval=DAY period=720h
```

### OKEX_MARGIN_LENDING_RATIO_AGG

OKX margin lending utilization per symbol.

**Fields:** `ratio`.

Higher ratio = higher utilization. 166+ symbols.

```bash
tsdbctl get points \
  type=OKEX_MARGIN_LENDING_RATIO_AGG \
  exchange=OKEX interval=DAY period=168h
```

### BITFINEX_MARGIN_RATES_AGG

**Fields:** `frr` (flash return rate),
`fundingAmount`, `fundingUsed`.

```bash
tsdbctl get points type=BITFINEX_MARGIN_RATES_AGG \
  exchange=BITFINEX interval=DAY period=168h
```

### BITFINEX_ACTIVE_CREDIT_SIZE_AGG

**Fields:** `activeCreditSize`.

Total active credit on Bitfinex margin.

### BYBIT_COLLATERAL_INFO_AGG

**Fields:** `initialLTV`, `liquidationLTV`,
`marginCallLTV`, `collateralLimit`.

Bybit collateral parameters for a given asset.

### BYBIT_MARGIN_BORROW_RATE_AGG

**Fields:** `dailyInterestRate`, `collateralRatio`,
`isBorrowable`, `isMarginCollateral`,
`liquidationOrder`, `maxBorrowAmount`.

### ETHENA_COLLATERAL_INFO_AGG

Ethena protocol collateral data. Fields vary by
exchange — some rows only have `lastUpdatedDate`,
others include `collateral` amounts. Filter by
exchange for meaningful data:

```bash
tsdbctl get points \
  type=ETHENA_COLLATERAL_INFO_AGG \
  exchange=BINANCE interval=DAY period=720h
```

### BOOK_TOP

Real-time top-of-book (best bid/ask + a few levels).

**Fields:** `bids`, `asks` (flat arrays).

Same format as other book types. Returns many rows
(2000+ for 5min). No `interval` needed.

```bash
tsdbctl get points type=BOOK_TOP \
  exchange=BINANCE_FUTURES rawSymbol=BTCUSDT \
  period=5m
```

### BOOK_SNAPSHOT_AGG

Full order book snapshots at intervals.

**Fields:** `bids`, `asks` (flat arrays).

Like `BLOCK_BOOK_SNAPSHOT_AGG` but without block-size
aggregation. Raw price levels.

```bash
tsdbctl get points type=BOOK_SNAPSHOT_AGG \
  exchange=BINANCE_FUTURES rawSymbol=BTCUSDT \
  interval=FIFTEEN_MINUTES period=1h
```

### BOOK_WALL

Detects large resting orders (walls) in the order book
by analyzing book snapshots over time. Tracks wall
appearance, duration, quantity, distance from mid price,
and whether the wall was touched.

**Fields:** `side`, `price`, `quantity`, `distance`,
`distance_percentage`, `quantity_percentile`, `duration`,
`first_seen_at`, `last_seen_at`, `disappeared_at`,
`present`, `touched`, `first_touched_at`,
`last_touched_at`, `touches`, `min_touch_price`,
`max_touch_price`, plus `_avg`/`_min`/`_max` variants
of quantity, distance, and distance_percentage.

**Required parameters:** `side` (BUY or SELL),
`blockSize` (price bucket width for wall detection —
25 for BTC, 5-10 for ETH), `interval` (MINUTE
recommended). Omitting `side` causes a server crash.

```bash
# BUY walls (support) for BTC
tsdbctl get points type=BOOK_WALL \
  exchange=BINANCE_FUTURES rawSymbol=BTCUSDT \
  interval=MINUTE period=30m \
  blockSize=25 maxDepth=50 side=BUY

# SELL walls (resistance)
tsdbctl get points type=BOOK_WALL \
  exchange=BINANCE_FUTURES rawSymbol=BTCUSDT \
  interval=MINUTE period=30m \
  blockSize=25 maxDepth=50 side=SELL
```

### Aggregated OI/Volume (latest-snapshots)

`AGGREGATED_OPEN_INTEREST_AGG` and
`AGGREGATED_VOLUME_AGG` return no data via `points`
but work via `latest-snapshots`:

```bash
tsdbctl get latest-snapshots \
  type=AGGREGATED_OPEN_INTEREST_AGG coin=BTC
```

---

## US equities and ETFs

Traditional equity exchanges are available as data
sources: NYSE, NYSE_ARCA, NYSE_AMERICAN, NASDAQ, IEX,
CBOE, FINRA, CONSOLIDATED_TAPE_ASSOCIATION. Coverage
is limited to crypto-adjacent instruments — not the
full stock universe:

- **Crypto ETFs:** IBIT, FBTC, GBTC, ARKB, BITB,
  BRRR, BTCO, BTCW, HODL, EZBC (BTC); ETHA, ETHE,
  ETHV, ETHW, FETH, EZET, QETH (ETH); SSK (SOL)
- **Index ETFs:** SPY, QQQ
- **Commodity ETFs:** GLD

Data is sourced from Polygon.io (the response shows
`exchange=POLYGON` regardless of which exchange you
query). All symbols use the `rawSymbol=TICKER/USD`
convention for `points` queries, though `coin=TICKER`
also works.

```bash
# SPY daily candles (last 30 days)
tsdbctl get points type=TRADE_SIDE_AGNOSTIC_AGG \
  exchange=NYSE rawSymbol=SPY/USD \
  interval=DAY period=720h --format json \
  -o spy.json

# NVDA daily candles
tsdbctl get points type=TRADE_SIDE_AGNOSTIC_AGG \
  exchange=NASDAQ rawSymbol=NVDA/USD \
  interval=DAY period=720h --format json \
  -o nvda.json

# IBIT via coin filter
tsdbctl get points type=TRADE_SIDE_AGNOSTIC_AGG \
  exchange=NYSE coin=IBIT \
  interval=DAY period=720h --format json \
  -o ibit.json

# Discover available symbols on an exchange
tsdbctl get symbols type=TRADE_SIDE_AGNOSTIC_AGG \
  exchange=NYSE

# Search via the markets resource
tsdbctl get markets exchange=NYSE pageSize=20 \
  --format json -o nyse_markets.json
tsdbctl get markets exchange=NASDAQ pageSize=20 \
  --format json -o nasdaq_markets.json
```

The `markets` resource returns richer metadata for
equities: `lastPrice`, `priceChange24h`, `volume24h`,
`pctFromATH`, and a `prices` array of recent hourly
prices. No order book data for equity exchanges.

**Gotcha:** the `symbols` and `registry` resources
list `rawSymbol` without the `/USD` suffix, but
`points` queries require it. Use `coin=` to avoid
this mismatch.

## Metadata queries

```bash
tsdbctl get categories type=TRADE_AGG exchange=BINANCE
tsdbctl get coins type=TRADE_AGG exchange=BINANCE
tsdbctl get symbols type=TRADE_AGG exchange=BINANCE_FUTURES
tsdbctl get exchanges type=FUNDING_RATE_AGG
tsdbctl get block-sizes type=BLOCK_BOOK_SNAPSHOT_AGG
tsdbctl get registry type=TRADE_AGG exchange=BINANCE_FUTURES
tsdbctl get coin-metrics coin=BTC,ETH
tsdbctl get markets signal=VOLUME_SPIKE pageSize=10
tsdbctl get markets coin=BTC category=PERPETUAL
```

## Output formats

Two formats: `toon` (default) and `json`.

**JSON** — one JSON object per line (NDJSON). Pass
`--format json` explicitly for scripts and reusable
artifacts. Nested fields like `markets`,
`predictionMarkets`, `tags`, `tweet_ids`, `levels`,
and `prices` are native JSON objects/arrays. A single
`json.loads()` per line gives you everything fully
parsed.

```bash
tsdbctl get points type=TRADE_AGG exchange=BINANCE \
  rawSymbol=BTCUSDT interval=HOUR period=7200 \
  --format json -o trades.json
```

**Toon** — token-optimized notation. This is the CLI
default. It strips JSON syntax overhead while
preserving structure through indentation. Arrays show
element counts inline (e.g. `levels[732]:`,
`prices[24]:`). It is smaller than JSON for nested
structures. Use toon when feeding data into an LLM
context or when token budget matters.

```bash
tsdbctl get points type=MARKET_EVENT \
  exchange=POLYMARKET period=48h \
  --format toon -o events.toon
```

CSV is no longer supported. A summary line is printed
to stderr: `7 points written to out/file.json in 119 ms`.

## Connectivity

```bash
tsdbctl ping
tsdbctl ping --count 5
```

## Batch fetching (multi-coin)

When fetching the same type for multiple coins, loop
in Python rather than comma-separating coins in one
query. Comma syntax returns interleaved rows that
need per-coin parsing afterward:

```python
COINS = ["BTC", "ETH", "SOL", "XRP", "DOGE"]
for coin in COINS:
    subprocess.run([
        "tsdbctl", "get", "points",
        "type=FUNDING_RATE_AGG",
        f"coin={coin}", "category=PERPETUAL",
        "interval=HOUR", "period=2160h",
        "groupBy=OPEN_INTEREST_WEIGHTED_AVG",
        "normalize.fundingInterval=3600000",
        "--format", "json",
        "-o", f"{coin.lower()}_funding_hourly.json",
    ])
```

This gives one clean file per coin with no
post-processing needed to separate them.

## Aligning multiple series

Two queries with identical `period` and `interval` can
return different row counts. Funding rates have gaps,
OI snapshots miss hours, ETF data is weekday-only.
Always join on timestamp, never assume positional
alignment. Intersect the timestamp sets before
iterating, or build dicts keyed by timestamp and
take the intersection.

## TRADE_AGG: one-row price trick

`TRADE_AGG` returns two rows per candle (BUY + SELL).
For price-only analysis, add `side=BUY` to get one
row per timestamp:

```bash
tsdbctl get points type=TRADE_AGG \
  exchange=BINANCE_FUTURES rawSymbol=BTCUSDT \
  interval=DAY period=2160h \
  normalize.quote=USD side=BUY
```

Or use `TRADE_SIDE_AGNOSTIC_AGG` if you don't need
the buy/sell volume split at all.

## Agent guidelines

- **Always write to files, never stdout.** Use
  `--format json -o result.json` or
  `--format toon -o result.toon`, not `-o -`. Stdout
  pollutes the conversation context with large data
  dumps that waste tokens and obscure errors. Read
  the file afterward with `head`, `wc -l`, or `jq`
  to verify it. Write output files in the working
  directory or a subdirectory, not `/tmp/`. Files in
  `/tmp/` are invisible to the user and hard to find
  later.
- **Prefer reusable scripts.** When running more than
  two tsdbctl commands, or when the task involves
  fetching data and then analyzing it, write a Python
  script and run that. In the tsdbctl workspace, use
  `hypotheses/<name>/phase*.py` for hypothesis phases,
  `scripts/lib/` for reusable helpers, and `scripts/`
  for one-off utilities. Keep scripts re-runnable and
  parameterized where possible.
- **Enum short forms work.** Prefixed enums accept the
  short form: `issuer=BLACKROCK` resolves to
  `ISSUER_BLACKROCK`, `tpoSession=DAILY` resolves to
  `TPO_SESSION_DAILY`. Use the short form in scripts
  and examples.
- **Inspect JSON keys before parsing.** Field names in
  JSON responses don't always match the enum output.
  Fetch one row first and check the actual keys before
  building a parser around assumed field names.
- **Pass `--format json`** for programmatic parsing in
  scripts. The CLI default is `toon`, which is useful
  for compact human or LLM inspection but is not JSON.

## Important notes

- Enum values are case-sensitive: `BINANCE_FUTURES`,
  not `binance_futures`. Use `tsdbctl enum` to check.
- `period` accepts Go durations (`1h`, `30m`) or raw
  seconds.
- `from` is unix seconds. Omit for trailing window
  ending at now.
- `from` + `period` → `[from, from + period)`.
- `period` alone → `[now - period, now)`.
- Output timestamps are unix nanoseconds.
- Floats use full decimal notation, not scientific.
