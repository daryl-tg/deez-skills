# Right-side panels

The right-hand cluster of the ticker bar and its `Panels` menu open market
panels to the right of the chart: Orderbook, the Tape with its docked
Liquidations, Alerts, Objects, the ETF screener, the heatmap switch and Options,
among others. Some open for a guest and some stop at the sign-in wall, and a
panel can open with no data when the backend has none. Created 2026-10-27; last
DRIVEN on 2026-11-07 against product tree `dced88e06a` (`origin/main`, 81
commits past `8bcd72f8f5`), lane `18103`, a guest-JWT lane with the gateway
name mapped in the browser. Driven that day on COINBASE BTC-USD: the Panels
menu's 17 rows plus a `tb-panels-row-tape-on` node while the Tape was open
(see Gotchas), the seven walls unchanged (`chart-actions`, `watchlist`,
`terminal`, `news`, `community-chat`, `volume-footprint`, `script-editor`),
the rows that open with no wall (`orderbook`, `etfScreener`, `journal`,
`alerts`, `marketStatsPanel`, `volumeStats`, `liquidityStats`, `heatmap`),
the Orderbook's DOM ladder drawing live with no delay notice, and the crypto
Tape printing (`crypto-tape-last-price` `75,755.95▼`, `tape-liquidations`,
no `tape-delay-notice`). On POLYGON AAPL the Tape fell back to `AAPL/USD`
`No trades match filters` (stocks gate unrouted). Before that, DRIVEN on
2026-11-06 against product tree `8bcd72f8f5` (`origin/main`, 119
commits past `87a325f4ab`), lane `18103`, a guest-JWT lane with the gateway
name mapped in the browser. Driven that day: the guest stock Tape on POLYGON
AAPL (see `rp-stock-tape`; it mounts only with the stocks gate routed, and no
print arrived), the Panels menu on AAPL (16 rows, no `orderbook`), the crypto
Tape on COINBASE BTC-USD printing with its docked Liquidations, the Orderbook
there (`orderbook-canvas`), the `watchlist` wall from its row, and Alerts from
its seat with no wall. Before that, DRIVEN on 2026-11-05 against product tree `87a325f4ab` (`origin/main`, 123
commits past `8436920004`), lane `18103`, a guest-JWT lane. Driven that day:
the Panels menu's 17 rows on COINBASE BTC-USD, the same seven walls
(`chart-actions`, `watchlist`, `terminal`, `news`, `community-chat`,
`volume-footprint`, `script-editor`) and `tb-options-btn`'s `terminal` wall,
the rows that open with no wall (`heatmap`, `etfScreener`, `objects`,
`journal`, `marketStatsPanel`, `volumeStats`, `liquidityStats`), the Orderbook
and the Tape on BINANCE.F ETHUSDT (`orderbook-canvas`; `crypto-tape-last-price`
`2,418.50▲` with `tape-liquidations`; the Tape row took the Orderbook's place),
and Alerts from `tb-panels-row-alerts` with its History tab (no
`alert-history-undelivered` row). Before that, DRIVEN on 2026-11-04 against product tree `8436920004` (`origin/main`), lane
`18103`, a guest-JWT lane with the gateway resolving. Driven that day: the
Panels menu's 17 rows on COINBASE BTC-USD (`replay`, `heatmap`, `watchlist`,
`scanner`, `etfScreener`, `news`, `chat`, `orderbook`, `tape`, `footprint`,
`alerts`, `objects`, `journal`, `editor`, `marketStatsPanel`, `volumeStats`,
`liquidityStats`), the Orderbook on BINANCE.F ETHUSDT (`orderbook-source-btn`,
`orderbook-canvas`), the Tape printing there (`2,287.17▼`) with its docked
Liquidations (13 `tape-liquidations-row`, `Prints` and `Levels`), and the
alert create wall (`alert`). The panel source in
`215896e614..8436920004` changed no testid. Before that,
DRIVEN on 2026-11-03 against product tree `215896e614` (`origin/main`), lane
`18103`, a guest-JWT lane with the gateway name mapped in the browser (see the
README). Driven that day: every Panels row on BINANCE.F ETHUSDT (17 rows; 16
on the NYSE `SPY / GLD` formula, which offers no `orderbook` row), the same
seven walls and ten opening rows, the Orderbook ladder live on ETHUSDT, the
Tape printing (`crypto-tape-last-price` `2,251.54▼`) with its docked
Liquidations list, the markets menu's `tape-markets-follow-btn` (`Follow the
chart · Binance Futures ETHUSDT`) and its size floor with `aria-pressed`
(`all` true), and the alert create wall (`alert`). Not driven that day: the
heatmap switch's wall, the Options button, the ETF rows and the Tape's
Heatmap view. Before that, DRIVEN on 2026-11-02 against product tree
`a4488341f6` (`origin/main`), lane `18103`, a guest lane with no JWT, on a quiet machine (load 2 to 5 on 10
cores). Driven: the Panels menu's **17** rows (the Trades and Liquidations panel
is retired, `ad67d47c62`; its saved rows load as Tapes), the same seven walls
(Replay `chart-actions`, Watchlist `watchlist`, Scanner `terminal`, News
`news`, Chat `community-chat`, Footprint `volume-footprint`, Editor
`script-editor`), the ten rows that open (`ETF screener`, `Orderbook`, `Tape`,
`Alerts`, `Journal`, `Market Stats`, `Volume Stats`, `Liquidity Stats`, and
Objects without a title), the rebuilt Tape (`crypto-tape-panel`) printing on
BINANCE.F ETHUSDT (2 rows at 6 s) and on BINANCE.F SOLUSDT (25 rows at 4 s)
with its Trades and Heatmap views, its markets menu and its docked Liquidations
in both the Prints and Levels views, the Orderbook ladder on ETHUSDT and on
SOLUSDT (within 5 s, but only once the tab was visible; see Gotchas), the
`heatmap` row opening the popover whose switch raised `orderbook-heatmap`, the
Options button's `terminal` wall, the alert create wall
(`alert-list-create-btn`, `alert-add-menu`, `alert-add-menu-price-btn` raising
`alert`), the ETF screener (0 rows again) and the Objects panel's handles.
Not proven: the Tape's sound control (the panel DOM carried no `tape-sound-*`
for a guest; Super Search lists the `Tape sounds` row), and anything signed
in. Earlier, 2026-11-01 on `120d5d5d32` (`origin/main`, lane `18103`, no JWT):
every one of the then 18 guest Panels rows with the same split as before (Replay
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
- `rp-tape` the Tape opens on the chart's market: live prints with a venue
  glyph and a tag icon, a Heatmap view, a markets menu, and a docked
  Liquidations section with Prints and Levels views. It is the one tape for
  every market; the Trades and Liquidations panel is retired (`ad67d47c62`).
- `rp-stock-tape` on a US stock the Tape is the stock Tape, open to guests
  since `bda0563ab1` on the 15-minute delayed lane: Time and sales with an
  exchange pick, docked Dark pool and Option flow sections that resize, and a
  detail card beside a Dark pool, Option flow or Heatmap row.
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
- **An open panel adds a `-on` node to its row (driven 2026-11-07).** With
  the Tape open, `[data-testid^=tb-panels-row-]` matched 18 nodes: the 17 rows
  and `tb-panels-row-tape-on` inside the Tape row (`TBPanelsMenu.vue` marks
  any `row.isOn`). Count rows with `:not([data-testid$=-on])`.
- **Delay notices on panels are per screen (source, `63c1fa257a`).** The
  Orderbook (`orderbook-delay-notice`, `orderbook-dom-delay-notice`,
  `orderbook-delta-delay-notice`), the fallback trades stream
  (`tape-delay-notice`) and the alert forms show their own delay line only
  for a delayed CME, stock-tape or OPRA plane that no chart on screen already
  labels, and always on mobile. Crypto shows none (driven 2026-11-07). The
  DOM ladder also caps each side at 5000 rows and starts governed CME
  groupings at the finest served size (`9d09f1365d`, source).
- **The row count follows the chart's market (driven 2026-11-03).** On
  BINANCE.F ETHUSDT the menu listed 17 `tb-panels-row-*`; on the NYSE `SPY /
  GLD` formula it listed 16, without `orderbook`. Count on a crypto perp
  before reading a missing row as drift.
- **A DOM read for every panel (driven 2026-11-02).** Read the open panels as
  the `panel-header-title` texts
  (`[...document.querySelectorAll('[data-testid=panel-header-title]')].map(e=>e.textContent.trim())`)
  beside the dialog store's `isAuthenticationDialogOpen` and
  `guestLoginFeatureId`. The header's `×` is `panel-header-close-btn`; Objects
  has no `panel-header-title` (its handles are `objects-views-trigger-btn`,
  `objects-collapse-all-btn`, `objects-search-toggle-btn` and
  `objects-docked-settings`). A walled row opens nothing and sets
  `isAuthenticationDialogOpen`. The Pinia `panels` store's `$state` holds only
  `lastUsedId` on `a4488341f6`; its `items` getter, which earlier passes read,
  was not re-read.
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
  it from the frame. Re-driven 2026-11-02 on `a4488341f6`, ETHUSDT and
  SOLUSDT: the panel opens with `segmented-{book,delta,dom}-btn`,
  `orderbook-source-btn` (its `aria-label` reads `Source: Binance Futures`;
  its text is empty), `ob-sidebar-collapse-btn` and
  `ob-sidebar-toggle-settings-btn`, and `orderbook-canvas` mounted within 5 s
  with asks and bids on both sides; the mid row is painted in the canvas too
  and read the price with `Imbalance 44.7% bid · 55.3% ask` on 2026-11-02 (a
  `/Spread/` match on `innerText` finds nothing). On 2026-11-03 the frame of
  the same ETHUSDT ladder showed `2251.09 ▲` over `Spread 0.20 · 0.009%`
  instead, with no imbalance line, so read the mid row off the frame rather
  than asserting either text. **The ladder does not mount
  while the tab is hidden**: the same open with `document.visibilityState`
  `hidden` showed the header and the tabs but no `orderbook-canvas` for 40 s on
  ETHUSDT and 24 s on SOLUSDT, and `tab t1` plus a reopen drew it in 5 s both
  times. The 2026-11-01 "blank SOL book" was that, not the gateway. Read
  `visibilityState` before any Orderbook assertion.
- **`rp-alerts`.** `tb-alerts-toggle-btn` opened `Alerts` (`Active` and
  `History` tabs, `No alerts yet`). Its handles are `alert-list-search-input`,
  `alert-list-create-btn`, `alert-list-select-mode-btn`,
  `alert-list-settings-btn` and `alert-list-tab-{active,history}-btn`.
  `alert-list-create-btn` opens an `ALERT ON` menu. Its `Price` item is
  `alert-add-menu-price-btn`, and for a guest that click raises the `alert` wall.
  The menu item has no accessible role. Click it with
  `eval "document.querySelector('[data-testid=alert-add-menu-price-btn]').click()"`,
  because `find text "Price"` matches a covered element.
  **A failed delivery now shows (source, `1d48f6b088`).** A fired alert that
  could not reach Telegram raises a `kscript-alert-delivery-failed-content`
  notice (toast, notification panel and compact row), its History card reads
  `Not delivered to Telegram` (`alert-history-undelivered`), and opening the
  History tab re-reads the rows. A Telegram or webhook save can be refused
  with a named reason. A guest cannot fire an alert, so on 2026-11-05 the
  History tab opened (`aria-selected` `true`) with no undelivered row; the
  notice itself is not driven.
- **A US stock's Tape docks an Option flow section (source, `4a1cce27a2`,
  `bd1ad5dff9`, `7441f653fd`).** Under Dark pool the stock Tape now docks
  option trades of $1M premium or more in their own section with its own dock
  setting (`Option flow section` in the Tape's settings menu; the old `Opts`
  toggle is gone). In a short panel every docked section keeps its head and
  two rows and the live rows give way first. Late-report prints no longer
  enter Dark pool or the Tape's last price. The Option flow section shows by
  default (`496e83f2ed`). Since `bda0563ab1` a guest reads `us-equities-full`
  ON (it is in `GUEST_DEFAULT_FLAGS`), so a guest gets the stock Tape; see
  `rp-stock-tape` below.
- **`rp-stock-tape` (driven 2026-11-06 on `8bcd72f8f5`, chrome only).** Chart
  POLYGON AAPL from its one search row (`asset-row-AAPL|4-btn`), then open
  `Panels` → `tb-panels-row-tape`. **The stock Tape needs the stocks gate
  routed, and the operator's `.env.local` does not route it.** Without
  `VITE_STOCKS_V2_WEB_SOCKET_DOMAIN` the Tape's market lookup fails at once
  (the dump's `stock-tape-lookup` line: `outcome failed`, `v2 streaming
  websocket connection failed`) and the panel falls back to the old trades
  stream: an `AAPL/USD` head over `No trades match filters`, with no
  `stock-tape-*` handle. To see the stock Tape, export the two stocks lines
  from the product's `.env.sample`
  (`VITE_STOCKS_V2_WEB_SOCKET_DOMAIN=wss://stream.stocks.openmarket.xyz/v2/`,
  `VITE_STOCKS_LIVE_FEED_URL=wss://stream.stocks.openmarket.xyz/ws`) before
  `up`; the process env wins over `.env.local`. With them the panel mounted:
  `stock-tape-panel`, `stock-tape-ticker` `AAPL`, `stock-tape-delay-line`
  `Delayed 15 minutes · Real-time` (`stock-tape-get-realtime-btn`),
  `stock-tape-venue-selector-btn` `All venues`, `stock-tape-waiting`
  `Waiting for trades...`, `stock-tape-dark-pool` (`Today`, `Prints` and
  `Levels`, `stock-tape-dark-pool-resize-handle`), and
  `stock-tape-option-flow` (`No option trades of $1M premium or more`,
  `stock-tape-option-flow-resize-handle`). The venue menu
  (`stock-tape-venue-menu`) held only `stock-tape-venue-menu-all-btn` (checked):
  the venues come from the prints. **No print arrived**: the gate answered
  nothing for this guest (`StreamMarkets timed out after 15000ms`), the Dark
  pool read `Dark pool prints did not load`, and the AAPL chart itself stalled
  on `Still loading... slow network` at 0 bars, so relaunch without the two
  exports for the rest of a pass. Not driven: a venue pick
  (`localStorage['stockTape.venuePicks']`, kept per pane), the row cards
  (`stock-tape-dark-pool-card`, `stock-tape-option-flow-card`,
  `stock-tape-heatmap-card`), a resize, and the off-exchange no-side rule.
  The crypto Tape shares the `stock-tape-row*` handles (`stock-tape-list`,
  `stock-tape-row-price`), so a `stock-tape-row` count is not a stock proof:
  read `stock-tape-panel` or `stock-tape-ticker`.
  **Dark pool prints on the followed chart (source, `c106437eb7`,
  `841ea60455`; not driven).** While the stock Tape is in Trades view with
  its Dark pool section open and the gate armed, the chart the Tape follows
  gets an auto-mounted `Dark pool prints` layer that is not in the
  Indicators list. Its legend row (`.is-wrun-app-layer`) carries only an eye,
  always shown; hiding it adds `.is-wrun-app-layer-hidden` and writes the
  panel setting `darkPoolOnChart` (default on). Collapsing the section, the
  Heatmap view, Dark pool off or a parked panel remove the layer. A capped
  day reads `stock-tape-dark-pool-cut` (`Not every print of this day is
  shown: …`). Needs a printing stocks gate, which this lane lacks.
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
- **`rp-tape`, rebuilt as one tape (`ad67d47c62`, `4dae9e6136`,
  `ba8e2cc280`; driven 2026-11-02 on `a4488341f6`).** `tb-panels-row-tape`
  opens `Tape` (`src/components/trades/Trades.vue` mounts
  `CryptoTapePanel.vue` for a crypto market): `crypto-tape-panel` with
  `crypto-tape-name`, `crypto-tape-last-price` (`2,263.61▼`),
  `crypto-tape-markets-line`, and `crypto-tape-waiting` (`Waiting for
  trades...`) or `crypto-tape-failed` while it has nothing. Rows are
  `stock-tape-row` with `stock-tape-row-time`, `-price`, `-size` and a venue
  glyph; the **`SWEEP` text is gone**: `stock-tape-row-tag` is an icon whose
  `aria-label` reads `Sweep ×N`, `Block` or `N fills`, and the old rate
  readout (`2.0/s`) is gone too. On BINANCE.F ETHUSDT 2 rows printed within
  6 s; on BINANCE.F SOLUSDT 25 rows within 4 s (last `94.43▼`), so the
  2026-11-01 "empty SOL tape" was the gateway outage. The head carries the
  view tabs `stock-tape-tab-trades-btn` and `stock-tape-tab-heatmap-btn`
  (`aria-pressed`; the Heatmap view fills `crypto-tape-heatmap-host`) and
  `tape-markets-btn`, which opens `tape-markets-menu`: a size floor
  (`tape-markets-show-{all,10k,50k,100k}-btn`, `Show All trades / $10K+ /
  $50K+ / $100K+`), `tape-markets-follow-btn` (`Follow the chart`),
  `tape-markets-chart-market` (`Binance Futures ETHUSDT`) and
  `tape-markets-add-btn` (`Add a market (10 at most)`). Docked below the
  prints is `tape-liquidations` with `tape-liquidations-head`
  (`Liquidations Today Prints Levels`), `-range-btn` (`Today`),
  `-view-prints-btn` and `-view-levels-btn`, `-collapse-btn`, `-list`, `-row`
  (with `-row-time`, `-row-price`, `-row-icon`, `-row-value`; 13 rows on
  ETHUSDT, 16 on SOLUSDT) and, in the Levels view, `-level` (16). The Super
  Search row answers `liquidations`, `trades and liquidations` and the former
  name `Trade & Liquidations` (`providers/panels.ts`). The sound control
  (`tape-sound-settings`, `-toggle`, `-picker`, `-volume`, `-option-*`) was not
  in the panel DOM for a guest; its palette row is `tape-toggle:sound` (`Tape
  sounds`, see [Super Search](./super-search-and-settings.md)). The old
  `CEXTradesStream.vue` (with `tape-pace-rate`) is now only the fallback for
  markets the new Tape cannot read: CME, OPRA, formulas and on-chain pools
  (source). `src/components/tradeAndLiquidations/` is deleted; a stored
  `tradeAndLiquidations` pin seats the Tape (`TOOLBAR_RETIRED_PIN_SUCCESSORS`
  in `src/constants/toolbar-panels.constants.ts`) and a saved row converts
  through `src/utility/panels/trade-liquidations-to-tape.util.ts`. The earlier
  history follows.
  **Driven 2026-10-28.** `tb-panels-row-tape` opened `Tape` on
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
  or `tb-replay-locked` until Replay is pinned. Re-driven 2026-11-02 on
  `a4488341f6` with the same seven ids. The `heatmap` row opened nothing
  visible on 2026-10-28; on 2026-11-02 `tb-panels-row-heatmap` opened the
  heatmap popover (`tb-heatmap-toggle-btn`, `role=switch`,
  `aria-checked="false"`) and the switch's click raised `orderbook-heatmap`,
  the same as `tb-heatmap-trigger-btn`.
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
- **A guest is offered 17 Panels rows** (driven 2026-11-02 on `a4488341f6`):
  `replay, heatmap, watchlist, scanner, etfScreener, news, chat, orderbook, tape,
  footprint, alerts, objects, journal, editor, marketStatsPanel, volumeStats,
  liquidityStats`. `tradeAndLiquidations` left the list with `ad67d47c62`
  (18 rows from 2026-10-27 to 2026-11-01); `markets`, `events`, `earnings`,
  `options` and `optionsFlowTape` are not offered.
- **The Orderbook is the hidden-tab canary (driven 2026-11-02).** The headless
  tab drifted to `visibilityState: hidden` right after `browser open` and
  again mid-pass; the Tape kept printing and every `eval` answered, but the
  Orderbook ladder never mounted its canvas until the tab was fronted. When
  `orderbook-canvas` is absent, read `document.visibilityState` before anything
  else, run `browser tab` and then `browser tab t1`, read it again, and reopen
  the panel.
- **The US options alert lane is retired (source, `b059e70852`).** An alert on
  a US option or a US stocks tape is refused with one flat sentence
  (`dialogs.alertCreate.blocked.opra`) and no way out; `opraAlertDoorVerdict`
  answers `opra-closed` for every tier and flag, and the `opra-alerts` flag and
  the `alert-create-opra-way-out` / `alert-dialog-opra-way-out` handles are
  gone. A guest meets the `alert` wall first, so it is not guest-driven.
- **The `Panels` row list is the full catalog.** It lists pinned panels too, so a
  row being there says nothing about the bar.
- **The Options button's visibility is a runtime flag.** Source puts it behind
  `isOptionsPanelOn()`. It rendered for a guest on this lane, but expect it to be
  absent where that flag is off.
