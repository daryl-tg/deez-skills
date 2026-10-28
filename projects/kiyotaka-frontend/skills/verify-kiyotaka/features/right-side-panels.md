# Right-side panels

The right-hand cluster of the ticker bar and its `Panels` menu open market
panels to the right of the chart: Orderbook, Alerts, Objects, the ETF screener,
the heatmap switch and Options, among others. Some open for a guest and some
stop at the sign-in wall, and a panel can open with no data when the backend has
none. Created 2026-10-27; last DRIVEN on 2026-10-28 against product tree
`29c9cda0a2` (`origin/main`), lane `18103`, a guest lane with no JWT. Driven:
every one of the 18 guest Panels rows. Orderbook (now with live book levels),
Tape, Trades and Liquidations, Market Stats, Volume Stats, Liquidity Stats,
Journal, Objects, the ETF screener and Alerts open with no wall; Scanner,
Footprint, Chat, News, Watchlist, Editor and Replay raise the wall; plus the
alert create wall, the heatmap popover and its wall, and the Options button's
wall. Not driven: any panel's signed-in content, Tape or Trades and
Liquidations prints (none arrived within 20 s), and the Markets, Events,
Earnings, Options flow tape and Polymarket panels, which a guest is not offered.

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
  (`48.1% bid · 51.9% ask`).
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
- **`rp-heatmap`.** `tb-heatmap-trigger-btn` opens a `Heatmap` popover with
  `tb-heatmap-toggle-btn` reading `OFF`. Turning it on as a guest raised the
  `orderbook-heatmap` wall.
- **`rp-options`.** `tb-options-btn` (`Options`) was visible to the guest. A
  click raised the `terminal` wall.
- **`rp-tape`, driven 2026-10-28.** `tb-panels-row-tape` opened `Tape` on
  COINBASE BTC-USD with a rate readout (`1.6/s`, `4.5/s`) and `PRICE / SIZE /
  TIME` heads, but its body still read `Waiting for trades...` after 20 s.
  `tb-panels-row-tradeAndLiquidations` opened `Trade & Liquidations` on BINANCE
  BTCUSDT, not the chart's COINBASE market, reading `Waiting for trades...` and
  `Waiting for liquidations...` at 5 s. The panels open; prints were not proved.
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
  Use `tb-panels-row-<id>`, or close the panel first.
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
