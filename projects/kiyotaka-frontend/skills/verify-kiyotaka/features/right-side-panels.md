# Right-side panels

The right-hand cluster of the ticker bar and its `Panels` menu open market
panels to the right of the chart: Orderbook, Alerts, Objects, the ETF screener,
the heatmap switch and Options, among others. Some open for a guest and some
stop at the sign-in wall, and a panel can open with no data when the backend has
none. Created 2026-10-27 from a live drive on product tree `7290d33d10` (53
behind `origin/main` `df3fdcb62e`), lane `18103`, a real guest-JWT lane. Driven:
Orderbook, Alerts and its create menu, Objects, the ETF screener, the heatmap
popover and Options. Not driven: Scanner, Tape, Footprint, Trades and
Liquidations, the stats panels, Journal, Chat and Replay, which are all listed
in the Panels menu.

## Sub-features

- `rp-orderbook` the Orderbook panel opens with Book, Delta and DOM tabs.
- `rp-alerts` the Alerts panel opens, and its create menu walls a guest.
- `rp-objects` the Objects panel opens for a guest.
- `rp-etf` the ETF screener opens with its column sets.
- `rp-heatmap` the heatmap seat opens an on and off switch.
- `rp-options` the Options button opens the Options panel (signed-in).

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
- **`rp-orderbook`.** `tb-orderbook-toggle-btn` opened `Orderbook` with
  `Book / Delta / DOM` and no wall.
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
- **Proof.** The panel header, the store read showing no wall (or the walled
  id), and a screenshot. Close each panel before opening the next.

## Gotchas

- **An open panel width-folds the ticker bar.** With any of these panels open,
  every panel seat leaves the bar and `find testid tb-alerts-toggle-btn` fails.
  Use `tb-panels-row-<id>`, or close the panel first.
- **The ETF screener can open empty for a data reason.** On 2026-10-27 the
  proxied dev backend answered `{"total":0,"universe":0,...}`, and the panel read
  `No ETFs match this screen / 0 of 0 ETFs`. That is the backend's data, not the
  panel. Probe the endpoint before reporting it.
- **The Orderbook book can be blank on a headless lane.** The panel opened with
  no levels drawn. That pass did not prove whether the book stream or rendering
  was the cause, so do not claim book data from that frame.
- **The `Panels` row list is the full catalog.** It lists pinned panels too, so a
  row being there says nothing about the bar.
- **The Options button's visibility is a runtime flag.** Source puts it behind
  `isOptionsPanelOn()`. It rendered for a guest on this lane, but expect it to be
  absent where that flag is off.
