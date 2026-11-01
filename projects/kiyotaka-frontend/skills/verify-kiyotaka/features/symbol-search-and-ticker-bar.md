# Symbol search and the ticker bar

The ticker bar is the chart's primary control strip: the symbol picker, a variant
chip, quick-interval buttons, the interval chevron, the chart-type picker, and the
layout picker. Changing any of them re-drives the whole data plane, so each proof
must show the chart actually reloaded — not just that a menu opened. This entry
was last DRIVEN on 2026-11-02 against product tree `a4488341f6` (`origin/main`),
lane `18103`, a guest lane with no JWT, on a quiet machine (load 2 to 5 on 10
cores). Driven: the V2 dialog (v2 20 testids, legacy 0), an `ETHUSDT` search
whose `Ethereum` row went to BINANCE.F ETHUSDT (464 bars, OI `$5.36B`,
funding `+0.0017%`) and whose bare `ETHUSDT` row STILL charted a BINANCE.O
put (`2 Nov 2026 2,250 Put`, 60 bars; the row arrives in a second batch about
8 s after the fill, a 3 s read listed the `Ethereum` row alone), `BTC.D` (250
bars, `60.36% ▼ BTC.D`), the Predict list through the Browse rail's
`search-v2-view-predictions-btn` (chips `all` pressed, `polymarket`,
`hyperliquid`; 22 rows; the Senate event charted, 143 bars, `25.5¢`) after
the tab's own click was `covered by <div.dialog-style.dialog-overlay>`, the
hover quick search to BINANCE.F SOLUSDT (`quick-search-v2-group-Solana|1-btn`,
250 bars), the `1m` pin (318 bars), the chevron to `5m`, the in-chart menu
back to `1h` (`Undo Change interval`), Heikin Ashi (`plotType=heikinAshi`,
the trigger's label `Heikin Ashi`, `Undo Change chart type`) and its undo,
the one-menu rule (15 chart-type options to 0 when the layout picker opened,
16 cells, four `role=switch` sync rows), the matrix cell's `multi-chart`
wall, the Panels menu (**17** rows, the Trades and Liquidations row gone),
the Options button's `terminal` wall, the footer undo and redo around the
option-put switch (`Undo Change symbol` back to BTC.D, `Redo Change symbol`
to the put, undo again), and the symbol button's logo (`f08ff46099`:
`LogoImage` is `aria-hidden`, so the accessible name is still `COINBASE
BTC-USD` while `textContent` now starts with the logo's letters,
`BTCOINBASEBTC-USD`). Not driven: the Equities tab, the input-method guard
(`ime-key-filter.util.ts` unchanged), the hover peeks, and the quick search
on a Polymarket chart, where `SOLUSDT` listed no `quick-search-v2-group-*`
in 12 s (it listed them at once on BTC.D). Earlier, 2026-11-01 on
`120d5d5d32` (`origin/main`, lane `18103`, no JWT, load 3 on 10 cores).
Driven: the V2 dialog (v2 20 testids, legacy 0, the same nine tabs), an
`ETHUSDT` search whose `Ethereum` row went to BINANCE.F ETHUSDT (440 bars, OI
`$5.31B`, funding) and whose bare `ETHUSDT` row STILL charted a BINANCE.O put
(the gap is not fixed, see below), the Equities tab narrowing `ETH` to 24 ETF
rows, `BTC.D` (250 bars), the Predict tab (chips `all` pressed, a Polymarket
Senate event charted, 119 bars), the hover quick search to BINANCE.F SOLUSDT,
the `1m` pin, the chevron to `5m` (17 options under four sections), the in-chart
interval menu back to `1h` (its `chart-symbol-interval-*` testids), Heikin Ashi
and back, the layout picker (four `role=switch` sync rows, the matrix cell's
`multi-chart` wall), the Panels menu (18 rows, no `tb-panels-reason-*`), the
Options button's `terminal` wall, the input-method guard, and, for the first
time, **the footer undo and redo** (`Undo Change symbol` put COINBASE BTC-USD
back and `Redo Change symbol` re-charted ETHUSDT; an interval step read `Undo
Change interval`) and **the one-menu rule** (opening the layout picker closed a
click-pinned chart-type menu). Earlier, 2026-10-29 on `78ec9625d9` (`origin/main`,
lane `18103`, no JWT): the V2 dialog (v2 20 testids,
legacy 0, nine visible tabs with no `HIP-4`), the new Predict tab with its
venue chips and a Polymarket event picked onto the chart, an `ETHUSDT` search
and a one-click switch to BINANCE.F ETHUSDT (367 bars, OI and funding), the
`1m` and `1h` pinned buttons, Heikin Ashi and back to candle, the layout hover
peek (its sync toggles are now switches) and its `multi-chart` wall, a CRYPTOCAP
`BTC.D` main series, the hover quick-search list (a pick switched to BINANCE.F
SOLUSDT), and the input-method guard, whose composing `Escape` no longer closes
the dialog. Earlier: 2026-10-28 on `29c9cda0a2` (the interval chevron to `5m`,
the in-chart interval menu beside the legend, the Equities tab). Not driven:
the memecoin and Pulse rows (signed-in only) and the third interval menu in
`ChartArea`.

## Sub-features

- `sym-search` the symbol dialog opens, searches, and switches symbol.
- `sym-scope` the scope chips filter results (`search-v2`).
- `sym-memecoins` the gated memecoin lane, liquidity-floor refinement, and Pulse
  rows load or report their explicit warning/empty state.
- `tb-interval` quick buttons, the interval chevron and the in-chart interval
  menu beside the legend change interval. Since `0011621cef` the three interval
  menus share one look.
- `tb-plot` the chart-type picker changes plot type.
- `tb-layout` the layout picker changes the grid.
- `tb-hover` the pickers peek on hover and pin on click.
- `tb-more` the `Panels` menu (`tb-panels-trigger-btn`) is the bar's only
  overflow: every seat the bar folds away is reached as a `tb-panels-row-<id>`
  row there. There is no `⋯` button.
- `tb-bar-toggles` the right-hand cluster toggles its panels and drawers
  (Heatmap, Watchlist, Orderbook, News, Alerts, Editor by default; the rest
  through Panels). What each panel shows is in
  [right-side panels](./right-side-panels.md).
- `tb-one-menu` only one chrome menu is open at a time (`1082148171`,
  `src/composables/useOneOpenMenu.ts`): chart type, layout, interval, Panels,
  heatmap, quick search and the top-bar menus register, and the one that opens
  closes the rest.
- `sym-ime` an input-method composition (pinyin, romaji, an accent popup) in the
  search field is left alone until it commits.
- `sym-cryptocap` a CRYPTOCAP index (`BTC.D`, `TOTAL2`, ...) loads as the main
  series.
- `sym-predict` the Predict tab lists Polymarket and Hyperliquid HIP-4
  prediction markets behind venue chips, and a pick charts the event.
- `sym-quick` hovering the symbol button opens a quick-search list, and a pick
  switches the symbol without the full dialog.
- `tb-undo` the footer's undo and redo buttons (`footer-undo-btn`,
  `footer-redo-btn`; there is no `tb-undo` testid) put back a symbol switch, a
  compare, an interval, a chart type, a chart setting, the session, the price
  scale or the Volume row, and name the step they will undo. Driven 2026-11-01
  and 2026-11-02 for symbol, interval and chart type; see Gotchas.

## How to get to it (user POV)

- Click the symbol button (`tb-symbol-info-btn`; it reads the current market,
  `COINBASE BTC-USD` on a default guest boot), type, pick a result.
- Click `1m` / `1h` directly, or hover the interval chevron for the full list.
- Hover or click `Candle` for chart type, `Layout` for the grid.
- Click a right-cluster button (Heatmap, Watchlist, Orderbook, News, Alerts,
  Editor) directly. Everything else, and anything that no longer fits, is in the
  `Panels` menu; there is no `⋯` overflow button.
- Type `BTC.D`, `TOTAL2` or `dominance` in the symbol dialog for a CRYPTOCAP
  index.
- Open the symbol dialog, click `Predict`, pick a venue chip (All, Polymarket,
  Hyperliquid) and a market to chart a prediction market.
- Hover the visible symbol control to open `quick-search-dropdown`; its stable
  input is `quick-search-input` and its full-dialog hand-off is
  `quick-search-advanced-button`. The memecoin lane answers only a pasted
  Solana mint there (signed-in; see Gotchas), and a failed search shows
  `quick-search-failed` with `quick-search-retry-btn`.

## Driving it with control-kiyotaka

Preconditions:

- Baseline from [chart boot](./chart-boot-and-data-plane.md), guest modal dismissed.

- **Open symbol search.** Run
  `./control-kiyotaka browser find testid tb-symbol-info-btn click`; its
  accessible name is the current market, so a `--name` handle breaks on every
  switch. On the guest lane this is the V2 dialog (see Gotchas): a category tab
  strip (`All`, `Crypto`, `Equities`, `Forex`, `Commodities`, `Indices`,
  `Predict`, `CME`, `Economy`; the `HIP-4` tab is gone since `93b3a757c0` and
  HIP-4 lives under `Predict`), a Browse rail (`All`, `Hyperliquid`,
  `CME Group`, `Tokenized stocks`, `Predictions`), Refine (Exchange, Quote),
  `Compare on chart`, and an Assets column with a Favorites tab
  (`search-v2-assets-tab-favorites-btn`).
- **Drive the search field by its testid, `symbol-selection-search-input`.** The
  placeholder is not stable and is CONDITIONAL on context: the ratio hint
  (`Search, or type a ratio like SPY/GLD`) renders only on the main-chart path with
  formulas available, while other contexts read `Search by symbol or name`,
  `Search prediction markets`, or an options-parent string. Never match on it. The field also carries no `aria-label`, so its computed accessible
  name is the **current symbol** — it snapshots as `textbox "BTCUSDT"`, then `textbox "BTCUSDT Clear"`
  once it has content, and it changes every time the symbol does. Nothing about
  it is a stable handle. The placeholder is:

  ```bash
  ./control-kiyotaka browser find testid symbol-selection-search-input fill "ETHUSDT"
  ```

  `Search symbols...` never appears on this dialog. Three different keys carry
  that text, and the one a desktop driver is likeliest to trip over is
  `navbar.quickSymbolSearch.searchPlaceholder`, which belongs to
  `QuickSymbolSearchDropdown.vue` — a separate surface that opens when you HOVER
  the symbol button rather than click it. The others are
  `searchPlaceholderMobile` and a `searchSymbols` label. Matching any of them
  against the clicked dialog finds nothing.
- **Read the result shape.** Results group by asset class, each group capped with a
  `See all <Class>` row; the right-hand rail previews the highlighted symbol and
  its venues. Picking a symbol takes two steps when the venue matters: the row,
  then the venue in the rail (`ETHTetherBINANCE.FPERP2,482.68↓ 1.44%`, a `generic`
  node — click it by ref).
  **On the v2 dialog one click can be enough.** Clicking an asset row for a
  single-venue match switches the symbol and closes the dialog outright — the
  venue rail is a second step only when the match spans venues. Proven live:
  `asset-row-ethereum|eth-btn` took the chart to ETHUSDT with no rail click.

  **The result rows themselves do not need refs.** The asset column carries
  `asset-row-<asset.id>-btn`, where the id is usually
  `<name>|<ticker>` lowercased (`asset-row-ethereum|eth-btn`) but NOT always —
  predictions use `pred:<rawSymbol>`, economics `fred:<symbol>` or
  `econ:<exchange>:<symbol>`, and a single-asset path falls back to the bare coin.
  Read the testid off the DOM rather than composing it and its symbol
  rows carry `symbol-row-<EXCHANGE>|<SYMBOL>-btn`
  (`symbol-row-BINANCE|WBETHUSDT-btn`), both stable across re-renders. Only the
  venue rail is ref-driven, so re-snapshot before that click alone rather than
  before every one.

  **Drift, driven 2026-10-12 on tree `1570b59d69` (the desktop parity sweep's `sym-results` and `sym-switch`, in the
  shell and in Chromium):** searching `ETH` listed `asset-row-Ethereum|1-btn`, `asset-row-ETH|3-btn`,
  `asset-row-Ether Continuous|1-btn` and `asset-row-Ether.fi|1-btn`. Each id kept the name's case and carried a number
  after the bar; none had the lowercased `<name>|<ticker>` form composed above. Click by prefix,
  `[data-testid^=asset-row-Ethereum]`, and fall back to the first `venue-row-` in the rail when the dialog stays open.
  **Driven 2026-10-29 on `78ec9625d9`:** an `ETHUSDT` query listed
  `asset-row-Ethereum|1-btn` (`ETH Ethereum · Crypto 2,369.10`) and, second, a
  bare `asset-row-ETHUSDT|1-btn` (`ETHUSDT ETHUSDT · Crypto`, no price). That
  second row is NOT the perp: its click charted `BINANCE.O ETH/USDT 31 Oct 2026
  2,300 Put` (13 bars). Take the `Ethereum` row, which went straight to
  BINANCE.F ETHUSDT (367 bars) with no rail step, and assert the ticker text
  after every pick. **Likely fixed by `50d301f61f` (source, read on
  `849fb08e95`):** option contracts are never venues of an asset now. Every
  scoped request carries the venue include-list (`VENUE_CATEGORIES` in
  `src/utility/symbol-selection/venue-categories.util.ts`, every wire category
  minus OPTION, COMBO and UTA), and `transformMarketAssets` drops an option row
  where rows become venues. Options enter through the Options tab. **Re-driven
  2026-11-01 on `120d5d5d32`: NOT fixed.** The same `ETHUSDT` query listed the
  same two rows, and the bare `asset-row-ETHUSDT|1-btn` click charted
  `BINANCE.O ETH/USDT 2 Nov 2026 2,250 Put` (36 bars after 60 s, title
  `16.4000 ▲ ETH - 261102 - 2250 - P`). `50d301f61f` guards the venue lists, but
  this bare-ticker asset id resolves through another path. Product gap, open;
  take the `Ethereum` row and assert the ticker text after every pick.
- **The dialog opens through a loading frame (source, `4ee72fc314`,
  `dd3daa34c6`).** While the dialog's code loads, a `symbol-selection-frame`
  (`aria-busy="true"`) stands in and grows into the dialog, and presses made
  then are queued and answered. A `find testid symbol-selection-search-input`
  sent at once can meet the frame. Wait until the frame is gone or a
  `search-v2-category-*` tab exists, then fill.
- **Prove the switch reached the engine**, not just the label: poll the candle
  predicate again and read
  `./control-kiyotaka browser eval "(()=>JSON.stringify({title:document.title,bars:window.tc[0].metadata[0].rawData.length}))()"`.
  `document.title` follows the symbol. Bars must climb back above 50 — a label
  change with an empty chart is a failed switch.
- **Interval.** Run `./control-kiyotaka browser find role button click --name "1h"`
  for a quick button, or drive the pinned testids directly —
  `tb-interval-pinned-1h-btn` and `tb-interval-pinned-1m-btn` both exist. For the full list use `button "Interval"` — that is the
  chevron, and interval binds hover-open to the chevron only, so a snapshot after
  a plain click on the label proves nothing.
- **Chart type.** `button "Candle"` peeks on hover and pins on click; the entries
  (`Hollow Candle`, `Heikin Ashi`, `Line`, `Line with Markers`, `Step Line`,
  `HLC Area`, `Area`, `Baseline`) do snapshot, so `hover` then `snapshot` proves
  the peek. **Click them by testid, not by their text.** Every entry carries
  `tb-chart-type-option-<value>-btn` — `candle`, `hollowCandle`, `heikinAshi`,
  `ohlcBar`, `volumeCandle`, `columns`, `highLow`, `spline`, `markerLine`,
  `stepLine`, `hlcArea`, `area`, `baseline`, `footprint`, `tpo` (fifteen, well
  past the eight the a11y names suggest). Use the stable option testid rather than
  text matching; the entries are generic nodes and a text click can race the
  popover closing. Pair the hover with the option testid.

  ```bash
  ./control-kiyotaka browser find testid tb-chart-type-trigger-btn hover
  ./control-kiyotaka browser find testid tb-chart-type-option-heikinAshi-btn click
  ```

  The engine read is `chartStore.mergedAllCharts[0].metadata.plotType` —
  picking `Line` makes it `"spline"`, Heikin Ashi `"heikinAshi"` (driven
  2026-11-02; `chartStore.plotTypeForChart` is not a function on
  `a4488341f6`) — and the trigger's `aria-label` follows the pick (`Heikin
  Ashi`), which is the cheaper of the two reads. The pick records `Undo Change
  chart type` in the footer.
- **Layout.** `button "Layout"` peeks on hover and pins on click, same as chart
  type — a click-only drive forfeits the `tb-hover` half of the proof. Its contents are invisible to the
  a11y tree: the grid groups (1, 2, 3, 4, 5, 6, 8, 9, 12, 16), the custom N×N
  matrix and the SYNC toggles all snapshot as unnamed `generic` nodes. Drive them
  by `data-testid` instead — `tb-layout-entry-2H-btn`, `tb-layout-entry-3x3-btn`,
  `tb-layout-matrix-cell-<col>-<row>-btn`, and up to five sync toggles —
  `tb-layout-sync-{symbol,interval,crosshair,time,drawings}-btn`, which since
  `8b8b211759` are `role=switch` pills read by `aria-checked` (driven
  2026-10-29: `crosshair` `true`, the rest `false`), beside a
  `tb-layout-sync-one-chart-hint` reading `Sync takes effect once the layout has
  two or more charts.`; `drawings`
  renders only for a sub-workspace, so a default single-chart boot shows four (the full set is built in
  `src/composables/chart/useMonitorPicker.ts`). The matrix key is
  `${col}-${row}`, zero-indexed and **column-first**: the first row of cells reads
  `0-0`, `1-0`, `2-0`, `3-0`:

  ```bash
  ./control-kiyotaka browser find testid tb-layout-entry-2H-btn click
  ```

  **As a guest the grid never applies** — see Gotchas.
- **Two independent fold mechanisms decide what is in the bar, and the Panels
  button is permanent again.** `TBPanelsMenu` renders unconditionally
  (`TickerBar.vue`), so `tb-panels-trigger-btn` is always present — the earlier
  `v-if="hasFolded"` rule is gone. What lives beside it is decided by:

  1. **Pin-fold**, independent of viewport: only `TOOLBAR_DEFAULT_PINS` —
     `heatmap`, `watchlist`, `orderbook`, `news`, `alerts`, `editor` — sit
     directly in the bar by default. Everything else pinnable starts folded into
     the Panels menu (`src/store/toolbar-panels.ts`, `isInBar()`). Pins persist as
     DEPARTURES from that default set, so a stored map picks up new defaults.
  2. **Width-fold**, the ladder in `src/composables/chart/useTickerBarFit.ts`,
     which sheds further rungs as the bar narrows.

  Driven live at `1440 900` on 2026-10-27 (guest), the complete bar was:

  ```
  tb-symbol-info-btn         tb-interval-pinned-1m-btn  tb-interval-pinned-1h-btn
  tb-interval-chevron-btn    tb-chart-type-trigger-btn  tb-layout-trigger-btn
  tb-indicators-btn          tb-options-btn             tb-heatmap-trigger-btn
  tb-watchlist-toggle-btn    tb-orderbook-toggle-btn    tb-news-toggle-btn
  tb-alerts-toggle-btn       tb-editor-toggle-btn       tb-panels-trigger-btn
  ```

  **`tb-super-search-btn` is gone** (`TBSuperSearchButton.vue` was deleted). Super
  Search now opens from the top navbar capsule `global-nav-search-btn`
  (`Ask anything ⌘K`); the ticker bar keeps only `tb-super-search-full-btn`, and
  only in full-chart mode. `tb-options-btn` (`Options`) sits after Indicators and
  was visible to a guest on this lane. `tb-terminal-*` and
  `tb-tweet-caller-trigger-btn` are gone. `tb-objects-toggle-btn`,
  `tb-journal-toggle-btn` and `tb-replay-toggle-btn` exist only once pinned; by
  default they are `tb-panels-row-{objects,journal,replay}`. Panel seats are
  generated by one component (`TBPanelToggle.vue`), so the pattern is
  `tb-<id>-toggle-btn` and the ids never appear as literals in source.

  **Opening a right-side panel narrows the bar and width-folds the toggles.**
  Driven 2026-10-27: with Orderbook, Alerts, Objects or the ETF screener open,
  the bar dropped every panel seat (`tb-heatmap-trigger-btn` through
  `tb-editor-toggle-btn`) and kept only symbol, intervals, chart type, layout,
  Indicators, Options and Panels. A `find testid tb-alerts-toggle-btn` then fails
  with `No element found`. Close the panel, or use `tb-panels-row-<id>`.

    `ToolbarPanelId` is **29 ids** on `a4488341f6` (`tradeAndLiquidations` left
  with `ad67d47c62`; `etfScreener` had joined — guest-reachable, no gate)
  (`src/constants/toolbar-panels.constants.ts`),
  most of them grid panels: `watchlist, scanner, markets, options, orderbook, tape,
  footprint, marketStatsPanel, volumeStats, liquidityStats,
  optionsFlowTape, news, events, earnings, alerts, objects, journal` plus
  `marketStats, splits, chartType, replay, heatmap, hlView, calls, goLive, editor,
  chat, trade`. `terminal` is gone. `hlView` and `calls` are door-only: no row, no
  seat, no pin — they mount headless and open from Super Search or a command.
  A stored `tradeAndLiquidations` pin seats the Tape
  (`TOOLBAR_RETIRED_PIN_SUCCESSORS`).

  A pin persists to user settings plus a localStorage mirror and survives a
  reload even for a guest, so a recipe that pins must unpin.

  **Only heatmap has a stand-in now.** `tb-panel-standin-heatmap-btn` holds the
  seat until its real host arms; a click that early arms the host and replays itself, so an
  immediate assertion after the first click can read as a no-op.

  **Driven and confirmed 2026-10-27**: a guest boot at `1440 900` carried
  `tb-panels-trigger-btn`, and the menu held `tb-panels-menu` plus 18 rows:
  `replay, heatmap, watchlist, scanner, etfScreener, news, chat, orderbook, tape,
  footprint, tradeAndLiquidations, alerts, objects, journal, editor,
  marketStatsPanel, volumeStats, liquidityStats`, alongside
  `tb-panels-customize-btn`. No `tb-panels-reason-*` rendered. (The 2026-10-23
  pass listed `hlView` and `calls` rows; they were absent this time.)
  **Driven 2026-11-02 on `a4488341f6`: 17 rows**, the same list without
  `tradeAndLiquidations` (`replay, heatmap, watchlist, scanner, etfScreener,
  news, chat, orderbook, tape, footprint, alerts, objects, journal, editor,
  marketStatsPanel, volumeStats, liquidityStats`), each row with a
  `tb-panels-pin-<id>-btn` beside it.
  `goLive` was absent, as it is for any guest. Note the menu lists PINNED entries
  too — it is the full catalog, not only what was folded — so a row's presence
  says nothing about whether that panel is also in the bar.
  A blocked row carries `tb-panels-reason-<id>` explaining why.
- **The chart-type popover stays mounted and hidden after its first open.**
  Driven 2026-10-27: once opened, every `tb-chart-type-option-*` stays in the DOM
  inside `.tb-panel-dropdown` with `visibility: hidden` and `opacity: 0`, so
  `find testid tb-chart-type-option-candle-btn click` locates it and then fails
  with `covered by <canvas.titan-charts-main-grid>`. A trigger `click` after a
  hover-open TOGGLES it shut.
  **Driven 2026-10-28, the visibility poll is not a reliable gate.** The poll
  read `hidden` while the popover was on screen in the same second's frame, and
  `find testid … click` failed with `covered by` even then. What worked: click
  the trigger until the popover is on screen (take a screenshot), read the
  option's rect, and click its centre with `browser mouse move <x> <y>`,
  `mouse down`, `mouse up`. Then read `chartStore.plotTypeForChart`. A hover-open
  followed by an immediate `find testid` click did work once (Heikin Ashi), so
  try it first.
- **Chart-type and layout options are EAGER — wait for the hover peek, not a
  chunk.** A one-day-old note here said the bodies were lazy and told you to poll
  for a chunk; that lane was reverted on 2026-10-23 and `tb-chart-type-frame`,
  `tb-layout-frame` and `tb-popover-skeleton` no longer exist. Driven: straight
  after `hover` the option count is `0`, and about two seconds later all **15**
  `tb-chart-type-option-*` testids are present at once. What you are waiting on is
  the popover's hover-peek delay. A `click` on the trigger opens it just as well
  and is the more reliable door for a driver.
- **Guest reach of the bar, driven 2026-10-27:** `global-nav-search-btn` opens
  Super Search with no guest gate (`super-search-overlay` mounted,
  `isAuthenticationDialogOpen` false). `tb-news-toggle-btn` (News) is
  guest-WALLED (`news`), and so are `tb-editor-toggle-btn` (`script-editor`) and
  `tb-options-btn` (`terminal`). `tb-orderbook-toggle-btn` and
  `tb-alerts-toggle-btn` OPEN their panels for a guest. `TBLayersButton`
  (`tb-layers-btn` plus a `tb-layers-*` panel) renders only when `layersEnabled()`
  passes, which is now a COMPOSED gate — the news-fire lane AND a runtime `layers`
  flag, with an anonymous-reader carve-out — so it is absent on a default local
  lane; do not record it missing as drift.
  `TBWatchlistToggle` (`tb-watchlist-toggle-btn`) is guest-WALLED through
  `handleGuestAccess(FeatureId.WATCHLIST)` but IS default-pinned, so it sits in
  the bar on a default boot. **The Objects row is no longer walled.** Driven
  2026-10-27: `tb-panels-row-objects` opened the Objects panel for a guest
  (`Nothing on this chart yet`) with no wall; source dropped its
  `guestFeature: FeatureId.TERMINAL`.
- **Proof.** For each change: the accessible name of the control after the change,
  the engine read showing bars reloaded, and a screenshot. Restore the original
  symbol, interval and plot type afterwards.

- **`sym-predict`, driven 2026-10-29 on `78ec9625d9`.** Open the dialog and
  click the VISIBLE Predict tab (the first DOM match is the hidden twin):
  `eval "[...document.querySelectorAll('[data-testid=search-v2-category-predictions-btn]')].find(e=>e.offsetParent).click()"`.
  The venue chips are `intent-filter-predict-venues` holding
  `intent-filter-predict-venue-{all,polymarket,hyperliquid}-btn` with
  `aria-pressed` (`All` pressed on open). The chips render only when two or more
  venues are offered. Rows are `prediction-row-pred:<slug>-btn` with a
  `prediction-row-favorite-pred:<slug>-btn` star beside each. Polymarket rows
  carry an event slug
  (`prediction-row-pred:what-price-will-ethereum-hit-in-october-2026-btn`),
  HIP-4 rows an outcome id (`prediction-row-pred:o19041-btn`, `ETH above 2,350.9
  by Oct 29, 06:00 UTC`). The Hyperliquid chip pressed `true` and listed only
  `o<id>` rows. A Polymarket row click closed the dialog and charted the event:
  the ticker read `POLYMARKET What price will Ethereum hit in October?`, 101
  bars, the title `71.0¢ Will Ethereum reach $2,400 in October?`, and the plot
  head shows `Event view` plus one outcome chip per strike (`↑ 2,400 71.0¢`,
  `↓ 2,300 46.5¢`, ... `More (10)`). No wall: nothing in the dialog, the row or
  `src/utility/symbol-selection/prediction-preview.util.ts` is gated. A pick
  hydrates the full event (bounded 1.5 s) before the chart switches; the list
  itself comes from the gateway preview (`7d9aa13638`). The query box keeps
  whatever was typed before, so clear it if the rows look narrowed.
- **`sym-quick`, driven 2026-10-29 on `78ec9625d9`.** Hover `tb-symbol-info-btn`
  (with the pointer first moved off it) and `quick-search-dropdown` opens: the
  placeholder `Change symbol…`, the current-symbol pill
  `quick-search-current-pill` (`quick-search-current-pill-clear-btn`), the
  token row `quick-search-token-<id>-btn` (`futures`, `cme`, `usdc`, `forex`,
  `hl`, `binance`, `spot`, `perp`, `stocks`, `usdt`, `commodities`, `bybit`,
  `crypto`, then `quick-search-tokens-more-btn`) and the hand-off to the full
  dialog, `quick-search-advanced-button`. Fill `quick-search-input` and the rows
  are `quick-search-v2-group-<id>-btn` with an expander
  `quick-search-v2-expander-<id>-btn`; `SOLUSDT` listed
  `quick-search-v2-group-crypto:SOL-btn` (`SOLUSDT Solana · Perp +1.24% 13
  markets`). Its click switched the chart to BINANCE.F SOLUSDT, 250 bars. The
  dropdown node stays in the DOM after it closes, so assert the switch on the
  engine and the title, not on the node's absence.

## Gotchas

- **Undo and redo live in the footer, not the ticker bar. Driven 2026-11-01 on
  `120d5d5d32`, guest, no JWT.** On a fresh boot `footer-undo-btn` read
  `aria-label="Undo"` with `aria-disabled="true"` and the store's `undoStack`
  was empty. After the `Ethereum` row switched COINBASE BTC-USD to BINANCE.F
  ETHUSDT the stack held one `chartSymbol` entry and the label read `Undo
  Change symbol`; the click put the title back to `… BTC - USD` (250 bars) and
  the redo button read `Redo Change symbol` with `aria-disabled="false"`; its
  click re-charted ETHUSDT (440 bars). A `1m` pin then recorded `chartInterval`
  (`Undo Change interval`), and its undo returned `activeInterval` to `1h`. The
  undo of the option-put switch above also restored ETHUSDT. Read the store as
  `document.querySelector('#app').__vue_app__.config.globalProperties.$pinia._s.get('undoRedo')`
  (fields `undoStack`, `redoStack`, `hasUndo`, `canUndo`,
  `isUndoingOrRedoing`). `footer-undo-redo` holds `footer-undo-btn` and
  `footer-redo-btn`; `Footer.vue` mounts them with no guest gate. Each button's
  `aria-label` names its step (`Undo <step>`), or reads a bare `Undo` / `Redo`
  while the history is empty or the step namer is still loading; a button that
  cannot act carries `aria-disabled="true"` and stays in the DOM. Keys:
  `Ctrl+Z` / `⌘Z` for undo, the `redo` command for redo (`⌘Y` under the
  TradingView preset), both rebindable. The store is Pinia `undoRedo`
  (`src/store/undo-redo.ts`); the swap steps are `chartSettings`,
  `chartSession`, `chartType`, `chartInterval`, `priceScale`, `volumeRow`,
  `drawingsLocked`, `drawingsHidden` and `chartSymbol`
  (`src/store/undo-redo-swap.ts`); a symbol switch or compare records
  `chartSymbol`. Since `973144b2c7` a window cell drops the interval, session
  and chart-type steps recorded before it became a window (`'lost'`), so the
  next Undo reaches the step under them; a guest never reaches a window. Two interval changes inside 1.5 s merge into one step. A
  `?symbol=` launch and an agent switch record nothing by design. The phone
  drawing bar has its own pair, `mobile-drawing-tools-undo` and
  `mobile-drawing-tools-redo`. Recipe (driven): read `document.title`, switch
  the symbol through the dialog, poll
  `$pinia._s.get('undoRedo').undoStack.at(-1)?.action` for `chartSymbol` and the
  button's label, click `footer-undo-btn`, then poll `document.title` and the
  candle predicate back to the first symbol (about 3 s); then read
  `footer-redo-btn`'s label, click it, and poll the title forward again. Wait
  2 s between interval clicks when counting steps (the 1.5 s merge).
- **One chrome menu at a time, driven 2026-11-01.** A click on
  `tb-chart-type-trigger-btn` showed 15 `tb-chart-type-option-*` rows; a click
  on `tb-layout-trigger-btn` closed them (0 visible) while the 16
  `tb-layout-matrix-cell-*` cells showed. A recipe that opens one picker and
  then hovers or clicks another must re-open the first. The source also says a
  focused quick-search box (`held`) blocks hover-opens elsewhere; on
  2026-11-01 a hover on the chart-type trigger while `quick-search-input` held
  a typed query still showed its options, so that half is not proven; drive
  the dropdown's pick before touching another trigger.
- **The hover quick search stays open and can cover the left toolbar.** After a
  pick from `quick-search-dropdown` the dropdown's `scope-token-line` was still
  in the DOM, and a later `find testid "toolbar-item-trendline:tool-icon-btn"
  click` failed with `covered by <div.scope-token-line.v2-tokens>`. Move the
  pointer onto the chart and press `Escape` before clicking a tool.
- **The bare `ETHUSDT` row arrives in a second batch (driven 2026-11-02 on
  `a4488341f6`).** Three seconds after the fill the list held only
  `asset-row-Ethereum|1-btn`; at eight seconds it held `asset-row-ETHUSDT|1-btn`
  (`ETHUSDT ETHUSDT · Crypto`, no price), `Lido Staked Ether`, `WBETH`,
  `BETH` and `METH` rows too. The bare row's click still charted `BINANCE.O
  ETH/USDT 2 Nov 2026 2,250 Put` (60 bars, title `9.40000 ▼ ETH - 261102 -
  2250 - P`), so the gap is open on this tree as well; nothing under
  `src/utility/symbol-search-v2/` or `symbol-selection/` that resolves an
  asset row changed in `120d5d5d32..a4488341f6`. Wait for the second batch
  before counting rows, and take the `Ethereum` row.
- **The Predict tab's own click can be covered; the Browse rail is the other
  door (driven 2026-11-02).** `find testid search-v2-category-predictions-btn
  click` failed with `covered by <div.dialog-style.dialog-overlay>` while the
  dialog itself was the only overlay (the strip's first DOM copy is the hidden
  twin). `search-v2-view-predictions-btn` (the rail's `Predictions`) opened
  the same list: `intent-filter-predict-venue-{all,polymarket,hyperliquid}-btn`
  with `all` pressed, 22 `prediction-row-pred:*-btn` rows, and a JS `.click()`
  on a Polymarket row charted the event (`POLYMARKET Which Senate Swing
  States will Republicans win?`, 143 bars, `25.5¢`).
- **Memecoins left the `All` tab and the quick search (source, `9ffb5345bf`,
  `eb1f3b83be`, `89adcfc7d5`; read on `a4488341f6`).** The lane answers only
  to the Memecoins tab (signed-in) or a pasted Solana mint
  (`memecoinLaneAsked` in `QuickSymbolSearchDropdown.vue`,
  `isMemecoinAddressBox` in `SymbolSelectionDialog.vue`; an address pasted
  with text around it is normalised). `quick-search-v2-memecoins-tail-btn`
  and `openMemecoinsInFullDialog` are deleted; the `quick-search-v2-memecoin-*`
  rows this guide's user-POV line names are gone with them. New quick-search
  handles: `quick-search-failed` and `quick-search-retry-btn` when a search
  failed with an empty list, and the full dialog's Retry re-sends with
  `retry: true`. Plain words no longer rewrite to token-catalog venues
  (`matchImplicitExchangesByPrefix`) and carried-over tokenized pools are
  stripped (`withoutTokenCatalogVenues`), so a tokenized stock pool no longer
  shows for a plain ticker.
- **The symbol button wears the market's logo (source, `f08ff46099`; driven
  2026-11-02).** `tb-symbol-info-btn` carries `tb-symbol-logo` (`LogoImage`,
  `aria-hidden="true"`, `alt=""`), so the accessible name is unchanged
  (`COINBASE BTC-USD`, `BINANCE.F ETHUSDT`) while the button's `textContent`
  starts with the logo's fallback letters (`BTCOINBASEBTC-USD`,
  `ETBINANCE.FETHUSDT`). Read the name or `document.title`, never the text.
  `tb-symbol-market-toggle-btn` is gone. The button is wider with the logo
  (134 to 234 px), so the width-fold can shed a rung earlier at `1440`.
- **The top-bar Layouts menu has testids (source, `f4c9e56e82`).**
  `layouts-menu-recent-held`, `-open-tab`, `-layout`, `-search`, `-grid`,
  `-pinned`, `-close-<id>`, `-keep-<id>-btn` and `-scratch` in
  `LayoutsMenu.vue`; the rows keep their first position. It is not the
  ticker-bar `tb-layout-*` picker and is not driven. `global-nav-create-btn`
  (`NavCreateButton.vue`) renders only with the Board flag on; absent for a
  guest (driven), as is `stock-feed-chip`.

- **`sym-ime`, driven 2026-10-29 on `78ec9625d9` with synthetic events.** The
  testid sits on the `INPUT` itself, so dispatch on
  `document.querySelector('[data-testid=symbol-selection-search-input]')` (there
  is no inner `input`; a `... input` selector reads `null`). Focus it, dispatch
  `compositionstart`, set the value to `eth` and dispatch an `input` with
  `isComposing: true`: the box stays `eth`. A composing `Escape`
  (`{key:'Escape', code:'Escape', keyCode:229, isComposing:true}`) now leaves the
  dialog OPEN. `compositionend` plus a plain `input` then uppercases the box to
  `ETH` once, and a plain `Escape` (`code:'Escape'`, no `isComposing`) closes it.
  The fix is `f79e403616`: `installImeKeyFilter()` in `src/main.ts` adds a
  capture-phase `window` keydown filter
  (`src/utility/dom/ime-key-filter.util.ts`) that stops a composing key before
  `Dialog.vue`'s `handleDialogKeydown` sees it. **Set `code` on the synthetic
  event.** The filter returns early when `event.code` is empty, so a composing
  `Escape` built without `code` still closes the dialog (driven). A real key
  always carries a `code`, so that is a recipe trap, not a product gap. Earlier:
  2026-10-28 on `29c9cda0a2`, where the composing `Escape` DID close the dialog.
  A real input method was never driven.
- **In-chart interval menu, driven 2026-10-28.** Click the interval chip beside
  the legend symbol (`5m ▾` at about `240,112` on a `1440 900` frame). It opens
  `.csb__dropdown-group` sections (`SECONDS`, `MINUTES`, `HOURS`, `DAYS`) with
  the same heads and row style as the ticker-bar chevron menu. **Driven
  2026-11-01: it has testids after all.** The chip is
  `chart-symbol-interval-toggle-btn`, the sections
  `chart-symbol-interval-section-<id>` and the rows
  `chart-symbol-interval-<interval>-btn` (21 interactive nodes on
  `120d5d5d32`); `chart-symbol-interval-1h-btn` put the interval back to `1h`
  (`chartStore.activeInterval`). The ticker-bar chevron menu has the same
  shape: `tb-interval-chevron-btn` opens `tb-interval-section-{seconds,minutes,
  hours,days}` (each with a `-toggle-btn`) and `tb-interval-option-<interval>-btn`
  rows (17 visible); `tb-interval-option-5m-btn` switched to `5m` (273 bars).
  The `ChartArea` menu, a third copy, still uses the `pm-csb__dropdown-group`
  class.
- **A venue-rail row needs a real pointer click.** Driven 2026-10-27: a JS
  `.click()` on a `.venue-row__identity` or `.venue-panel__row` did not commit,
  and a rail row in the virtual list can sit below the dialog's visible bottom,
  where a pointer click lands outside and just closes the dialog. Read the row's
  rect, make sure it is on screen, then `browser mouse move <x> <y>`,
  `mouse down`, `mouse up`. An `asset-row-*` click by JS does commit.
  On 2026-10-28 a JS `.click()` on `venue-row-COINBASE|BTC-USD-btn` did commit,
  so try it first and fall back to the pointer. Which rows a query lists also
  depends on what the dialog last previewed: the same `BTC-USD` query listed
  `venue-row-COINBASE|BTC-USD-btn` once and only `asset-row-Bitcoin|1-btn` the
  next time. Read the rows, never compose them.
- **`sym-cryptocap`, driven 2026-10-27.** Searching `BTC.D` lists
  `symbol-row-CRYPTOCAP|BTC.D-btn` and `asset-row-CRYPTOCAP|BTC.D-btn` (Bitcoin
  Dominance). Clicking the visible asset row switched the chart to `CRYPTOCAP
  BTC.D`: 250 bars, a percent price axis, the title `60.45% ▲ BTC.D`, the VWAP
  legend reading `not on crypto index charts` with a `1 indicator paused on crypto
  index charts` card (`Remove all` / `Show`), and the counter at `0/3`. Source:
  `src/utility/symbol-search-v2/crypto-index-search.util.ts`; the product doc is
  `docs/features/data/cryptocap-indices.md`.
- **A label change is not a symbol change.** The ticker bar updates optimistically;
  the engine reload is the real event. Always re-assert the candle predicate.
- **An empty result list is usually the symbol DIRECTORY, not the search.** The
  dialog can open, accept the fill, and still read `ALL MARKETS 0 results` with
  `Network issue. Results may be out of date. Retry`, because the exchange/coin
  directory rides the v2 websocket and the console carries
  `Failed to fetch exchanges` / `Failed to get exchange info list:
  V2 WebSocket connection timeout`. `doctor`'s `v2 gateway reachable` is a TCP
  probe of the gateway host and passes while those calls time out, so it does not
  clear this. With zero results, `sym-search` — the actual symbol switch — is
  unreachable; report it with the console signature rather than reporting the
  dialog as broken.
- **The chart-type entries DO carry accessible names, as `generic` nodes.** They
  snapshot as `generic "Hollow Candle"`, `generic "Heikin Ashi"`, `generic
  "Step Line"` and so on, so `find role button --name` misses them while the name
  is right there. Click them by their text, not by a button role.
- The pickers are hover-driven. `agent-browser` `click` does not emit the hover
  sequence, so a click-only drive can miss a peek-only state — and touch and the
  agent puppet deliberately never hover-open.
- **Picking a multi-chart grid is guest-unreachable.** The picker opens and the
  cells respond, but the selection raises a `Multi-Chart Layouts / Sign in or
  create an account` wall instead of applying —
  `promptGuestLogin(FeatureId.MULTI_CHART)` in `src/store/dialog.ts`. Only the
  picker opening is provable on the guest lane; report the grid itself as
  unreachable rather than photographing a click that did nothing.
  Two details a recipe trips on. The free multichart limit is **1 for a guest**,
  so every entry above one chart already renders `locked` before the click — but
  that is no longer absolute: under `free-tier-v2` a signed-in free account can
  reach 16, and the flag reads off for guests only because a guest never fetches
  it. And the 1x1 matrix
  cell (`tb-layout-matrix-cell-0-0-btn`) is the one allowed cell: from the default
  single-chart guest boot it raises **nothing at all** — no wall, no dialog,
  `guestLoginFeatureId` stays `null` — because the layout it selects is the one
  already applied. Do not use it to prove a wall; prove the wall on any multi-cell
  (`tb-layout-matrix-cell-1-1-btn`), which reliably reads `multi-chart`.
  `src/constants/authFeatures.constants.ts` is the registry of every surface that
  behaves this way — read it before mapping something as guest-reachable.
- **The guest lane exercises V2, not the legacy dialog, and no flag decides
  it.** `search-v2` graduated: `GUEST_DEFAULT_FLAGS` is `{}`, and `isSearchV2` is
  `useGroupedMode && !isMobile && !pairMode && screenerTokens === undefined &&
  !isComparisonChart` (`SymbolSelectionDialog.vue`). Proven live 2026-10-27: the
  dialog rendered 22 `search-v2-category-*` testids and **zero**
  `intent-filter-class-*` elements, so `sym-scope` is a guest-lane proof.

  **Tell the dialogs apart by testid, not by category labels.** Legacy renders
  `intent-filter-class-<id>-btn`; v2 renders `search-v2-category-<id>-btn`. Check
  which one you got before trusting either recipe, because this flag has now
  flipped twice:

  ```bash
  ./control-kiyotaka browser eval \
    "JSON.stringify({v2:document.querySelectorAll('[data-testid^=search-v2-category-]').length,legacy:document.querySelectorAll('[data-testid^=intent-filter-class-]').length})"
  ```

  The v2 category tabs are ELEVEN — `all`, `crypto`, `memecoins`, `stocks`,
  `forex`, `commodities`, `indices`, `predictions`, `cme`, `economics`,
  `options` (`CATEGORY_ORDER` in `src/constants/symbol-search-v2.constants.ts`
  plus `cme`, `economics` and `options` pushed in `CategoryStrip.vue`) — but a
  guest sees NINE — driven 2026-10-29: `All, Crypto, Equities, Forex,
  Commodities, Indices, Predict, CME, Economy`. `hip4` was removed by
  `93b3a757c0` and its typed prefix with it; `search-v2-category-hip4-btn` reads
  `0`. `memecoins` and `options` are no longer
  flag-gated: both now require a signed-in session, so their absence on a guest
  lane is correct rather than drift. v2 itself is structural, not flag-driven:
  the dialog falls back to legacy only when opened from a comparison chart, in
  pair mode, from the screener, or on mobile.
  The strip's own testid `search-v2-category-strip` appears **twice** in the DOM,
  and so does every category button — **the FIRST match is the hidden copy**
  (zero-size rect). Driven 2026-10-27: `querySelector(...).click()` on
  `search-v2-category-stocks-btn` marked the hidden twin selected and the visible
  strip stayed on `All`. The buttons are `role=tab`, labelled by their text
  (`Equities` for id `stocks`, `Predict` for `predictions`,
  `Economy` for `economics`), so drive them with
  `find role tab click --name "Equities" --exact`. A `--name` lookup with role
  `button` finds nothing. Proof: the visible `[role=tab][aria-selected=true]` and
  the rows (an `ETH` query narrowed to ETHA, ETHU, ETHE and the other ETH ETFs). V2 also carries a views
  rail — `search-v2-view-{all,hyperliquid,cme,tokenized,predictions}-btn` — which
  the map previously treated as internal-only and which a guest can drive.

  If you do land on legacy, its ids are not its labels: the `Macro` pill is
  `intent-filter-class-economics-btn`, and `intent-filter-class-macro-btn` does
  not exist. The other seven match (`all`, `equities`, `cme`, `crypto`, `forex`,
  `commodities`, `predict`).
- v2's `ScopeChips` is not a fixed row of category buttons at all. It renders only
  the active, removable filter tokens, so there is no persistent `All` chip to
  match on.
- **`data-ghost-id` and `data-testid` are different attributes, and only one is
  broken.** A guest boot does log `[ghost-id-audit] 11 expected ghost-id(s) NOT
  registered`, so ghost-ids are not a handle — but the ticker bar carries a full,
  stable set of `data-testid`s (`tb-symbol-info-btn`, `tb-interval-pinned-1h-btn`,
  `tb-interval-chevron-btn`, `tb-chart-type-trigger-btn`, `tb-layout-trigger-btn`,
  `tb-indicators-btn`, `tb-editor-toggle-btn`, `tb-orderbook-toggle-btn`, every
  `tb-layout-entry-*`). Prefer ARIA names where they exist; reach for
  `find testid` for the controls that have none, rather than concluding there is
  no handle.
- Switching symbol on the authed lane writes to the account's autosaving
  workspace. Use a throwaway account or restore the original symbol.
