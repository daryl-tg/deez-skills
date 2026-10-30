# Symbol search and the ticker bar

The ticker bar is the chart's primary control strip: the symbol picker, a variant
chip, quick-interval buttons, the interval chevron, the chart-type picker, and the
layout picker. Changing any of them re-drives the whole data plane, so each proof
must show the chart actually reloaded — not just that a menu opened. This entry
was last DRIVEN on 2026-10-29 against product tree `78ec9625d9` (`origin/main`),
lane `18103`, a guest lane with no JWT. Driven: the V2 dialog (v2 20 testids,
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
- `tb-more` the overflow menu opens once the bar has folded something.
- `tb-bar-toggles` the right-hand cluster toggles its panels and drawers
  (Heatmap, Watchlist, Orderbook, News, Alerts, Editor by default; the rest
  through Panels). What each panel shows is in
  [right-side panels](./right-side-panels.md).
- `sym-ime` an input-method composition (pinyin, romaji, an accent popup) in the
  search field is left alone until it commits.
- `sym-cryptocap` a CRYPTOCAP index (`BTC.D`, `TOTAL2`, ...) loads as the main
  series.
- `sym-predict` the Predict tab lists Polymarket and Hyperliquid HIP-4
  prediction markets behind venue chips, and a pick charts the event.
- `sym-quick` hovering the symbol button opens a quick-search list, and a pick
  switches the symbol without the full dialog.
- `tb-undo` the footer's undo and redo buttons put back a symbol switch, a
  compare, an interval, a chart type, a chart setting, the session, the price
  scale or the Volume row, and name the step they will undo. Source only so far
  (`b975aaa639`, `7118982415`, read on `849fb08e95`); see Gotchas.

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
  `quick-search-advanced-button`. V2 quick-search can expose memecoin/Pulse rows
  under `quick-search-v2-memecoin-*` and a liquidity-floor refinement.

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
  where rows become venues. Options enter through the Options tab. Re-drive the
  `ETHUSDT` query before you call the gap closed.
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

  The engine read is `chartStore.plotTypeForChart` — picking `Line` makes it
  `"spline"` — and the trigger's `aria-label` follows the pick, which is the
  cheaper of the two reads.
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

    `ToolbarPanelId` is now **30 ids** (`etfScreener` joined — guest-reachable, no gate) (`src/constants/toolbar-panels.constants.ts`),
  most of them grid panels: `watchlist, scanner, markets, options, orderbook, tape,
  footprint, tradeAndLiquidations, marketStatsPanel, volumeStats, liquidityStats,
  optionsFlowTape, news, events, earnings, alerts, objects, journal` plus
  `marketStats, splits, chartType, replay, heatmap, hlView, calls, goLive, editor,
  chat, trade`. `terminal` is gone. `hlView` and `calls` are door-only: no row, no
  seat, no pin — they mount headless and open from Super Search or a command.

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

- **Undo and redo live in the footer, not the ticker bar (source, read on
  `849fb08e95`, never driven).** `footer-undo-redo` holds `footer-undo-btn` and
  `footer-redo-btn`; `Footer.vue` mounts them with no guest gate. Each button's
  `aria-label` names its step (`Undo <step>`), or reads a bare `Undo` / `Redo`
  while the history is empty or the step namer is still loading; a button that
  cannot act carries `aria-disabled="true"` and stays in the DOM. Keys:
  `Ctrl+Z` / `⌘Z` for undo, the `redo` command for redo (`⌘Y` under the
  TradingView preset), both rebindable. The store is Pinia `undoRedo`
  (`src/store/undo-redo.ts`); the swap steps are `chartSettings`,
  `chartSession`, `chartType`, `chartInterval`, `priceScale` and `volumeRow`
  (`src/store/undo-redo-swap.ts`), and a symbol switch or compare records
  `chartSymbol`. Two interval changes inside 1.5 s merge into one step. A
  `?symbol=` launch and an agent switch record nothing by design. The phone
  drawing bar has its own pair, `mobile-drawing-tools-undo` and
  `mobile-drawing-tools-redo`. Proposed recipe: read `document.title`, switch
  the symbol through the dialog, read
  `$pinia._s.get('undoRedo').undoStack.at(-1)?.action` (expect `chartSymbol`)
  and the button's label, click `footer-undo-btn`, then poll `document.title`
  and the candle predicate back to the first symbol; the replay is async.

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
  the same heads and row style as the ticker-bar chevron menu. It has no testid;
  read the groups by that class.
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
