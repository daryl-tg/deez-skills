# Right-side panels

The right-hand cluster of the ticker bar and its `Panels` menu open market
panels to the right of the chart: Orderbook, Alerts, Objects, the ETF screener,
the heatmap switch and Options, among others. Some open for a guest and some
stop at the sign-in wall, and a panel can open with no data when the backend has
none. Created 2026-10-27; last DRIVEN on 2026-11-01 against product tree
`120d5d5d32` (`origin/main`), lane `18103`, a guest lane with no JWT. Driven:
every one of the 18 guest Panels rows with the same split as before (Replay
`chart-actions`, Watchlist `watchlist`, Scanner `terminal`, News `news`, Chat
`community-chat`, Footprint `volume-footprint`, Editor `script-editor`; the
other eleven open with their `panel-header-title`, Objects without one), Tape
prints on BINANCE.F ETHUSDT (`2,253.00 SWEEP 4.5 21:46:23` rows), Orderbook
live levels on BINANCE.F ETHUSDT (`2253.18 ▲ Spread 0.20 · 0.009%`), the
heatmap popover's `role=switch` and its `orderbook-heatmap` wall, the Options
button's `terminal` wall, the alert create wall (`alert-list-create-btn` opens
`alert-add-menu`, then `alert-add-menu-price-btn` raises `alert`), and the ETF
screener (0 rows again). Not proven: Tape and Orderbook on BINANCE.F SOLUSDT
(both empty after 30 s, first with the tab hidden and then visible, before the
gateway outage below), Trades and Liquidations prints (`Waiting for trades` and
`Waiting for liquidations` after 15 s on ETHUSDT while the Tape printed). Earlier,
2026-10-29 on `78ec9625d9` (`origin/main`, lane `18103`, no JWT): every one of
the 18 guest Panels rows, with the same split as 2026-10-28. ETF
screener, Orderbook, Tape, Trades and Liquidations, Alerts, Objects, Journal,
Market Stats, Volume Stats and Liquidity Stats open with no wall. Replay,
Watchlist, Scanner, News, Chat, Footprint and Editor raise the wall, and the
`heatmap` row opens nothing. Also driven: Tape prints on BINANCE.F ETHUSDT,
Orderbook live levels on BINANCE.F SOLUSDT, the heatmap popover's new switch
and its wall, the Options button's wall, and the alert create wall. Not
driven: any panel's signed-in content, Trades and Liquidations prints (none in
10 s), and the Markets, Events, Earnings, Options flow tape and Polymarket
panels, which a guest is not offered.

## Sub-features

- `rp-orderbook` the Orderbook panel opens with Book, Delta and DOM tabs.
- `rp-alerts` the Alerts panel opens, and its create menu walls a guest.
- `rp-objects` the Objects panel opens for a guest.
- `rp-etf` the ETF screener opens with its column sets.
- `rp-heatmap` the heatmap seat opens an on and off switch.
- `rp-options` the Options button opens the Options panel (signed-in).
- `rp-tape` the Tape and the Trades and Liquidations panels open on the chart's
  market.
- `rp-stats` the Market, Volume and Liquidity Stats panels open.
- `rp-journal` the Journal panel opens.
- `rp-walled` the Scanner, Footprint, Chat, News, Watchlist, Editor and Replay
  rows wall a guest with their own feature id.

## How to get to it (user POV)

- Click a seat in the ticker bar (Heatmap, Orderbook, Alerts), or open `Panels`
  and pick a row (Objects, ETF screener and the rest).
- Close a panel with the `×` in its header, or by its seat or row again.

## Driving it with control-kiyotaka

Preconditions: baseline from [chart boot](./chart-boot-and-data-plane.md), with
the top overlay cleared. Use the `DS` store read from
[Super Search and settings](./super-search-and-settings.md) to tell a wall from
an open panel.

- **Open by seat or row.** `find testid tb-<id>-toggle-btn click` for a pinned
  seat, or `find testid tb-panels-trigger-btn click` then
  `find testid tb-panels-row-<id> click`. Read the open panel's header text: the
  panel title (`Orderbook`, `Alerts`, `Objects`, `ETF screener`) is the first
  text in the right-side header.
- **A store read for every panel.** The panels store lists what is open:
  `document.querySelector('#app').__vue_app__.config.globalProperties.$pinia._s.get('panels').items`
  (each item's `content` is the panel type, for example `OrderbookPanel`,
  `Tape`, `TradeAndLiquidations`, `MarketStats`, `VolumeStats`,
  `LiquidityStats`, `Journal`, `Objects`, `EtfScreener`, `Alerts`). The header
  title is `panel-header-title` and its `×` is `panel-header-close-btn`; Objects
  has no `panel-header-title`. A walled row leaves `items` empty and sets
  `dialog.isAuthenticationDialogOpen`.
- **`rp-orderbook`.** `tb-orderbook-toggle-btn` opened `Orderbook` with
  `Book / Delta / DOM` and no wall. On 2026-10-28 (`tb-panels-row-orderbook`,
  COINBASE BTC-USD) it drew live levels on both sides and an imbalance line
  (`48.1% bid · 51.9% ask`). Re-driven 2026-10-29 on BINANCE.F SOLUSDT with
  `tb-orderbook-toggle-btn`: live asks and bids on both sides with amount and
  total columns, and the mid price with `Spread 0.01 · 0.010%`. Re-driven
  2026-11-01 on BINANCE.F ETHUSDT (`tb-panels-row-orderbook`): asks and bids
  with amount and total, `2253.18 ▲`, `Spread 0.20 · 0.009%`. **The book is a
  canvas**: the panel's handles are `orderbook-source-btn` (the venue picker,
  `22a2ad32d4`) and `orderbook-canvas`, so `innerText` holds no levels; prove
  it from the frame, or from the mid-price line, which is DOM text. On
  BINANCE.F SOLUSDT the same day the book stayed blank for 25 s with the tab
  visible; it was live there on 2026-10-29, so treat an empty SOL book as
  unproven rather than broken until re-driven on a healthy gateway.
- **`rp-alerts`.** `tb-alerts-toggle-btn` opened `Alerts` (`Active` and
  `History` tabs, `No alerts yet`). Its handles are `alert-list-search-input`,
  `alert-list-create-btn`, `alert-list-select-mode-btn`,
  `alert-list-settings-btn` and `alert-list-tab-{active,history}-btn`.
  `alert-list-create-btn` opens an `ALERT ON` menu. Its `Price` item is
  `alert-add-menu-price-btn`, and for a guest that click raises the `alert` wall.
  The menu item has no accessible role. Click it with
  `eval "document.querySelector('[data-testid=alert-add-menu-price-btn]').click()"`,
  because `find text "Price"` matches a covered element.
- **`rp-objects`.** `tb-panels-row-objects` opened `Objects`
  (`Nothing on this chart yet`) with no wall.
- **`rp-etf`.** `tb-panels-row-etfScreener` opened `etf-screener-panel` with
  `etf-screener-screen-btn` (`Largest ETFs`), `-filters-btn`, `-columns-btn`,
  `etf-screener-tab-{overview,performance,flows,dividends,holdings,risk,technicals}-btn`,
  `-add-filter-btn` and `etf-screener-sort-<column>-btn`. The rows come from
  `POST /api/v1/etf/screener`.
- **`rp-heatmap`.** `tb-heatmap-trigger-btn` opens a `Heatmap` popover. Since
  `8b8b211759` its `tb-heatmap-toggle-btn` is the app-wide pill: a
  `<button role="switch">` read by `aria-checked` (`false`, text `OFF`, driven
  2026-10-29), and a symbol with no heatmap marks it `aria-disabled="true"`
  rather than `disabled`. Turning it on as a guest raised the
  `orderbook-heatmap` wall. A signed-in popover also carries explainer terms
  and `tb-heatmap-options-settings-btn`, `-denomination-<d>-btn`,
  `-resolution-{hd,4k}-btn`, `-scheme-*`, `-display-*` and `-shape-*` (source,
  not driven).
- **`rp-options`.** `tb-options-btn` (`Options`) was visible to the guest. A
  click raised the `terminal` wall.
- **`rp-tape`, driven 2026-10-28.** `tb-panels-row-tape` opened `Tape` on
  COINBASE BTC-USD with a rate readout (`1.6/s`, `4.5/s`) and `PRICE / SIZE /
  TIME` heads, but its body still read `Waiting for trades...` after 20 s.
  `tb-panels-row-tradeAndLiquidations` opened `Trade & Liquidations` on BINANCE
  BTCUSDT, not the chart's COINBASE market, reading `Waiting for trades...` and
  `Waiting for liquidations...` at 5 s. The panels open; prints were not proved.
  **Re-driven 2026-10-29 on BINANCE.F ETHUSDT: Tape prints arrived.** Within
  5 s the Tape read `ETHUSDT 132/s` with rows such as `2,361.39 SWEEP 7.2
  20:18:06`, green and red by side, `SWEEP` tags on aggressive fills. So the
  empty Tape of 2026-10-28 was the COINBASE BTC-USD market, not the panel.
  Trades and Liquidations on the same market still read `Waiting for trades...`
  and `Waiting for liquidations...` after 10 s. Its settings show size
  thresholds (`TRADES VOLUME 50%`, `THRESHOLDS 4`), so it may list only prints
  above them. Not proved either way. Re-driven 2026-11-01 on BINANCE.F ETHUSDT
  (`120d5d5d32`): the Tape printed within 20 s (`SWEEP` rows, header `2.0/s`)
  while Trades and Liquidations still read both `Waiting for …` lines after
  15 s. Source on `849fb08e95` and `120d5d5d32`: the panel filters by its own
  size thresholds times its multiplier, unchanged. On BINANCE.F SOLUSDT the
  Tape read `Waiting for trades...` for 30 s (tab hidden, then fronted); on
  2026-10-29 it printed there, so re-drive SOL on a healthy gateway before
  calling it. Read `document.body.innerText` for the `Waiting for` lines: the
  `panel-header-title`'s container text is only the title.
- **The whole order-flow family goes quiet in a gateway outage (seen
  2026-11-01, ~21:55 UTC on).** When `tsdb-gateway.int.ore.kiyotaka.ai` stops
  resolving, Tape, Orderbook and Trades and Liquidations all sit on their
  waiting states, `connection-status-chip` reads `Reconnecting…`, and the
  console carries `v2 Orderbook socket error` and `v2 Streaming socket error`.
  `doctor`'s `v2 gateway` line says `UNREACHABLE`; check it before reading an
  empty panel as a regression. See [chart boot](./chart-boot-and-data-plane.md)
  Gotchas for the DNS detail.
- **`rp-stats`, driven 2026-10-28.** `tb-panels-row-marketStatsPanel`,
  `-volumeStats` and `-liquidityStats` opened `Market Stats`, `Volume Stats` and
  `Liquidity Stats` with no wall. Liquidity Stats drew data
  (`BOOK LIQUIDITY $27.3M`, bid and ask volume, a two-line chart). It can show
  `liquidity-stats-retry-btn` on a data failure.
- **`rp-journal`, driven 2026-10-28.** `tb-panels-row-journal` opened `Journal`
  with no wall. Source gates its writes on a guest session, so expect a
  read-only or empty list.
- **`rp-walled`, driven 2026-10-28.** The Panels rows and the ids they raise:
  `scanner` → `terminal`, `footprint` → `volume-footprint`, `chat` →
  `community-chat`, `news` → `news`, `watchlist` → `watchlist`, `editor` →
  `script-editor`, `replay` → `chart-actions`. A guest's Replay row raises the
  sign-in wall, not the upgrade dialog, and there is no `tb-replay-toggle-btn`
  or `tb-replay-locked` until Replay is pinned. The `heatmap` row opened nothing
  visible and no wall; use `tb-heatmap-trigger-btn`.
- **Proof.** The panel header, the store read showing no wall (or the walled
  id), and a screenshot. Close each panel before opening the next.

## Gotchas

- **An open panel width-folds the ticker bar.** With any of these panels open,
  every panel seat leaves the bar and `find testid tb-alerts-toggle-btn` fails.
  Use `tb-panels-row-<id>`, or close the panel first. With no panel open the
  seats are back: on 2026-11-01 `[data-testid$="-toggle-btn"]` listed
  `tb-watchlist-`, `tb-orderbook-`, `tb-news-`, `tb-alerts-` and
  `tb-editor-toggle-btn` (plus the unrelated `chart-symbol-interval-toggle-btn`
  and `footer-chat-toggle-btn`), and `tb-watchlist-toggle-btn` raised the
  `watchlist` wall.
- **Read the wall through the store, and unescape it.** `browser eval` returns
  the dialog store's JSON with escaped quotes; a shell `case` on `"open":true`
  never matches and the Escape is skipped, after which every later row click
  lands on the previous wall and reads as walled by the wrong id. Strip the
  backslashes before matching. One 2026-11-01 pass misread six rows that way.
- **The ETF screener can open empty for a data reason.** On 2026-10-27 and
  again on 2026-10-28 the
  proxied dev backend answered `{"total":0,"universe":0,...}`, and the panel read
  `No ETFs match this screen / 0 of 0 ETFs`. That is the backend's data, not the
  panel. Probe the endpoint before reporting it.
- **The Orderbook book was blank on 2026-10-27 and drew levels on 2026-10-28.**
  Same lane and backend, so the blank frame was not a headless limit. Wait a few
  seconds after the open and read the frame before claiming book data either way.
- **`tb-heatmap-trigger-btn` needs a click.** On 2026-10-28 a `hover` did not
  render `tb-heatmap-toggle-btn`; a click opened the popover.
- **A guest is offered 18 Panels rows**, the same on 2026-10-27 and 2026-10-28:
  `replay, heatmap, watchlist, scanner, etfScreener, news, chat, orderbook, tape,
  footprint, tradeAndLiquidations, alerts, objects, journal, editor,
  marketStatsPanel, volumeStats, liquidityStats`. `markets`, `events`,
  `earnings`, `options` and `optionsFlowTape` are not offered.
- **The `Panels` row list is the full catalog.** It lists pinned panels too, so a
  row being there says nothing about the bar.
- **The Options button's visibility is a runtime flag.** Source puts it behind
  `isOptionsPanelOn()`. It rendered for a guest on this lane, but expect it to be
  absent where that flag is off.
