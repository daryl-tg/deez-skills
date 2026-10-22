# Symbol search and the ticker bar

The ticker bar is the chart's primary control strip: the symbol picker, a variant
chip, quick-interval buttons, the interval chevron, the chart-type picker, and the
layout picker. Changing any of them re-drives the whole data plane, so each proof
must show the chart actually reloaded — not just that a menu opened. This entry
was SOURCE-corrected on 2026-10-22 against `fcc8e53b12` and NOT driven; last live check 2026-10-12; guest coverage
opened V2 search, attempted an ETHUSDT venue switch, changed interval, and
selected Heikin Ashi. The ETHUSDT reload remained at zero candles because the
backend was down. The hover quick-search result list and memecoin/Pulse rows
were not independently driven in this pass.

## Sub-features

- `sym-search` the symbol dialog opens, searches, and switches symbol.
- `sym-scope` the scope chips filter results (`search-v2`).
- `sym-memecoins` the gated memecoin lane, liquidity-floor refinement, and Pulse
  rows load or report their explicit warning/empty state.
- `tb-interval` quick buttons and the interval chevron change interval.
- `tb-plot` the chart-type picker changes plot type.
- `tb-layout` the layout picker changes the grid.
- `tb-hover` the pickers peek on hover and pin on click.
- `tb-more` the overflow menu opens once the bar has folded something.
- `tb-bar-toggles` the right-hand cluster toggles its drawers (Objects, Journal,
  Heatmap, Replay, News, Terminal, Editor, Super Search).

## How to get to it (user POV)

- Click the symbol button (`BINANCE.F BTCUSDT`), type, pick a result.
- Click `1m` / `1h` directly, or hover the interval chevron for the full list.
- Hover or click `Candle` for chart type, `Layout` for the grid.
- Click a right-cluster button (Objects, Journal, Heatmap, Replay, News, Terminal,
  Editor) directly; at a narrow width the ones that no longer fit move into a
  `⋯` overflow menu.
- Hover the visible symbol control to open `quick-search-dropdown`; its stable
  input is `quick-search-input` and its full-dialog hand-off is
  `quick-search-advanced-button`. V2 quick-search can expose memecoin/Pulse rows
  under `quick-search-v2-memecoin-*` and a liquidity-floor refinement.

## Driving it with control-kiyotaka

Preconditions:

- Baseline from [chart boot](./chart-boot-and-data-plane.md), guest modal dismissed.

- **Open symbol search.** Run
  `./control-kiyotaka browser find role button click --name "BINANCE.F BTCUSDT"`,
  then `./control-kiyotaka browser snapshot -i -c`. On the guest lane this is the
  LEGACY dialog (see Gotchas), whose category buttons are `button "All"`,
  `Equities`, `CME`, `Crypto`, `Forex`, `Commodities`, `Macro`, `Predict`, beside
  `Formula — combine symbols with ÷ − + ×` and `View options`.
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
  `tb-layout-sync-{symbol,interval,crosshair,time,drawings}-btn`; `drawings`
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

  Driven live at `1440 900`, the complete bar was:

  ```
  tb-super-search-btn    tb-symbol-info-btn       tb-interval-pinned-1m-btn
  tb-interval-pinned-1h-btn  tb-interval-chevron-btn  tb-chart-type-trigger-btn
  tb-layout-trigger-btn  tb-indicators-btn        tb-heatmap-trigger-btn
  tb-watchlist-toggle-btn  tb-orderbook-toggle-btn  tb-news-toggle-btn
  tb-alerts-toggle-btn   tb-editor-toggle-btn     tb-panels-trigger-btn
  ```

  **Three handles the map used to name are gone**: `tb-orderbook-toggle-btn` (the
  Terminal toggle was retired and Orderbook took its seat),
  `tb-news-toggle-btn` (News is now `tb-news-toggle-btn`), and
  `tb-tweet-caller-trigger-btn`. `tb-objects-toggle-btn`, `tb-journal-toggle-btn`
  and `tb-replay-toggle-btn` exist only once pinned; by default they are
  `tb-panels-row-{objects,journal,replay}`. Panel seats are generated by one
  component, so the pattern is `tb-<id>-toggle-btn`.

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

  **Driven and confirmed**: a guest boot at `1440 900` carried
  `tb-panels-trigger-btn`, and the menu held `tb-panels-menu` plus rows for
  `replay, heatmap, hlView, calls, watchlist, objects, journal, news, editor`,
  each with its `tb-panels-pin-<id>-btn`, alongside `tb-panels-customize-btn`.
  `goLive` was absent, as it is for any guest. Note the menu lists PINNED entries
  too — it is the full catalog, not only what was folded — so a row's presence
  says nothing about whether that panel is also in the bar.
  A blocked row carries `tb-panels-reason-<id>` explaining why.
- **Popover bodies are lazy now.** Chart type, layout and heatmap load their
  bodies from a loader map behind skeleton frames (`tb-chart-type-frame`,
  `tb-layout-frame`, `tb-panel-standin-heatmap-frame`). After hovering or clicking
  a trigger, POLL for an option testid — the options are absent from the DOM for
  the first frames, which reads exactly like a trigger that did not open.
- **New in the bar, and guest-reachable:** `tb-super-search-btn` opens Super
  Search with no guest gate (proven live: `isSuperSearchOpen` went true with
  `isAuthenticationDialogOpen` false). `tb-news-toggle-btn` (News) is
  guest-WALLED through `handleGuestAccess(FeatureId.NEWS)`. `TBLayersButton`
  (`tb-layers-btn` plus a `tb-layers-*` panel) renders only when `layersEnabled()`
  passes, which is now a COMPOSED gate — the news-fire lane AND a runtime `layers`
  flag, with an anonymous-reader carve-out — so it is absent on a default local
  lane; do not record it missing as drift.
  `TBWatchlistToggle` (`tb-watchlist-toggle-btn`) is guest-WALLED through
  `handleGuestAccess(FeatureId.WATCHLIST)` but IS default-pinned, so it sits in
  the bar on a default boot. The Objects row is walled through
  `FeatureId.TERMINAL`, not an objects id — so a guest is walled there too, and
  `guestLoginFeatureId` reads `terminal`, which looks like the wrong surface.
- **Proof.** For each change: the accessible name of the control after the change,
  the engine read showing bars reloaded, and a screenshot. Restore the original
  symbol, interval and plot type afterwards.

## Gotchas

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
- **`search-v2` is ON for guests now, so the guest lane exercises V2, not the
  legacy dialog.** This inverts the previous rule and it inverts what
  `sym-scope` costs: `GUEST_DEFAULT_FLAGS` in `src/store/feature-flags.ts` ships
  `'search-v2': true` and ranks it above the (empty) fetched map for a guest, so
  a plain guest desktop open runs `isSearchV2 = true`. Proven live: the dialog
  rendered a `search-v2-category-strip` and **zero** `intent-filter-class-*`
  elements. `sym-scope` therefore no longer needs an internal role — it is a
  guest-lane proof.

  **Tell the dialogs apart by testid, not by category labels.** Legacy renders
  `intent-filter-class-<id>-btn`; v2 renders `search-v2-category-<id>-btn`. Check
  which one you got before trusting either recipe, because this flag has now
  flipped twice:

  ```bash
  ./control-kiyotaka browser eval \
    "JSON.stringify({v2:document.querySelectorAll('[data-testid^=search-v2-category-]').length,legacy:document.querySelectorAll('[data-testid^=intent-filter-class-]').length})"
  ```

  The v2 category ids are TWELVE — `all`, `crypto`, `memecoins`, `stocks`,
  `forex`, `commodities`, `indices`, `predictions`, `cme`, `hip4`, `economics`,
  `options` — but a guest sees TEN. `memecoins` and `options` are no longer
  flag-gated: both now require a signed-in session, so their absence on a guest
  lane is correct rather than drift. v2 itself is structural, not flag-driven:
  the dialog falls back to legacy only when opened from a comparison chart, in
  pair mode, from the screener, or on mobile.
  The strip's own testid `search-v2-category-strip` appears **twice** in the DOM,
  so match a specific category id rather than the strip. V2 also carries a views
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
