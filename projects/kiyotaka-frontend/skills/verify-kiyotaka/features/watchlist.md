# Watchlist

A right-side grid panel holding the account's saved lists of markets as a live
table — price, change, a trend sparkline and configurable columns. The user
switches lists from a chip in the hotbar, clicks a row to open that market on the
active chart, adds symbols through the shared symbol picker, removes them with a
hover ×, drags rows to reorder, and can import TradingView lists. Read-only
built-in lists (seven seeded "starter" lists, hotlists, sector and flagged views)
sit beside the user's own in the same picker.

This entry was created on 2026-10-23 against product tree `2a1ed750db`. **Only
the guest-side is driven**: the three doors and the sign-in wall were proven
live. Everything behind the wall is source-derived and UNVERIFIED, because this
stack cannot be signed into by an agent — see Gotchas.

## Sub-features

- `wl-open` the panel opens and closes from the ticker-bar seat; a guest gets the
  sign-in wall instead.
- `wl-lists` the list picker switches, creates, renames, duplicates, clears,
  exports and deletes lists.
- `wl-add` symbols are added through the shared symbol picker, or from the chart.
- `wl-open-row` a plain row click opens that market on the active chart.
- `wl-remove` the hover × removes a row, with an 8s Undo toast.
- `wl-reorder` dragging a row reorders it and flips the list to Manual order.
- `wl-import` the TradingView import sheet creates lists from pasted text or a
  `.txt` file.
- `wl-limits` 250 symbols per list, 50 lists per account.

## How to get to it (user POV)

- Click the watchlist icon in the ticker bar — it is one of the six default pins.
- Or open the Panels menu and pick the Watchlist row.
- Or click the watchlist button in the chart legend, which adds the chart's own
  market to a list rather than opening the panel.
- Alt+Shift+W toggles the panel; Alt+W adds the chart's market.

## Driving it with control-kiyotaka

Preconditions: baseline from [chart boot](./chart-boot-and-data-plane.md). The
panel needs `:3000` — list CRUD rides `/api/v1/watchlists` through orange to
tharamine, while prices ride the v2 gateway. With `:3000` down the lists never
load; with the gateway down the rows render but every cell stays a dash.

- **`wl-open` — and read the state before you click.** The pane can already be
  open at boot for a signed-in desktop user, so a blind click CLOSES it. Read
  `aria-pressed` on the seat, or the store, first:

  ```bash
  ./control-kiyotaka browser eval \
    "(()=>{const P=document.querySelector('#app').__vue_app__.config.globalProperties.\$pinia._s;return JSON.stringify({open:P.get('panels').isOpen('WatchlistPane'),pressed:document.querySelector('[data-testid=tb-watchlist-toggle-btn]')?.getAttribute('aria-pressed')})})()"
  ```

  Open proves out as `panels.isOpen('WatchlistPane') === true` plus a
  `watchlist-pane` containing `.watchlist`. **Wait for `.watchlist`, not the panel
  chrome** — the body mounts only after the first chart paint, with a 30s cap.
  If the seat is missing (folded), the fallback door is `tb-panels-trigger-btn`
  then `tb-panels-row-watchlist`.
- **The guest wall is the one thing proven live here.** Driven on
  `2a1ed750db`: clicking `tb-watchlist-toggle-btn` left the panel shut and set
  `dialogStore.isAuthenticationDialogOpen = true` with
  `guestLoginFeatureId = "watchlist"`. `chart-legend-watchlist-btn` raises the
  same wall. A guest still SEES the seat and the Panels row — visibility is not
  permission, so do not read either as the feature being reachable.
- **`wl-add`** opens the shared symbol picker from `watchlist-add-symbol-btn`
  (absent on read-only lists). Fill `symbol-selection-search-input`, tick a row's
  `*-screener-checkbox-*`, then `symbol-selection-apply-btn`, whose label reads
  "Add (n)". **Nothing is written until Apply** — Cancel, Escape and click-outside
  all discard, which makes the discard path a good negative check.
- **`wl-remove`** is `watchlist-row-remove-btn` inside the row. It is
  opacity-hidden until hover and absent on read-only lists, and it ignores
  double-clicks. Undo lives in an 8s toast with no testid — match the text.
- **`wl-reorder` is real pointer events, not HTML5 drag.** Listeners are on
  `document` and a drag starts after 6px of travel, so a synthetic `dragstart`
  does nothing: press, several moves, release. It needs an owned list, no active
  filter or search, non-aggregated mode and 2+ rows. On drop the list flips to
  Manual sort — assert `watchlistPane.settings.sortByList[<id>].key === 'manual'`
  as well as the new order.
- **`wl-import`** avoids the OS file chooser via the paste path:
  `watchlist-hotbar-import-btn` → `watchlist-transfer-paste-link` →
  `watchlist-transfer-paste` + `watchlist-transfer-name` →
  `watchlist-transfer-paste-import`, then wait for `watchlist-transfer-open`.
  The parser caps at 256KB / 2000 entries and runs in the browser; only catalog
  lookups leave.
- **Row ids are the stored backend key, case-preserved.** `watchlist-row-<key>`
  where key is `EXCHANGE|RAWSYMBOL` exactly as stored — `POLYGON|AAPL/USD`,
  `COMEX|GC1!`, `HYPERLIQUID_HIP3|xyz:AAPL`, and three-part
  `POLYMARKET|<eventSlug>|<conditionId>`. `|`, `/`, `:` and `!` are all legal.
  Never compose one from a symbol you typed; read it off the DOM or the store.
  Group-coins mode changes them to `watchlist-row-agg:<class>:<NAME>`.
- **Rows are virtualized** — the DOM holds only the rendered window, so count and
  order from the store, never from `querySelectorAll`.
- **Proof.** For each change: the store read naming the list and its symbols, the
  row testid in the DOM, and a screenshot of the pane.

## Gotchas

- **An agent cannot sign into this stack, so everything past the wall is
  unverified.** Driven 2026-10-23: submitting the login form for the local dev
  account does NOT do password auth — it sends a **6-digit sign-in code by
  email**, which the harness cannot read. The account named in the operator's
  notes as the watchlist login behaves this way. Until someone supplies a code or
  an account that takes a password, `wl-lists`, `wl-add`, `wl-open-row`,
  `wl-remove`, `wl-reorder`, `wl-import` and `wl-limits` are all
  `verified-unreachable` with that as the unmet prerequisite. This caps every
  authed claim in the whole map, not just this entry.
- **Driving this mutates the real account.** Lists, symbols, order, sections,
  flags and notes all write to the server; pane settings PATCH user settings on a
  1.5s debounce; opening or closing the panel rewrites the workspace's terminal
  document; a pin writes user settings. Prefer a throwaway list and delete it;
  otherwise invert every change (or Undo within 8s) and restore the original list
  and panel state.
- **A plain row click has chart side effects.** It opens that market on the active
  chart and persists the workspace symbol. Use Shift/Cmd+click when you only mean
  to select.
- **Creating a list auto-opens the symbol picker.** Close it before asserting
  anything else.
- **The built-in lists are read-only.** Starter (`starter:overview` and six
  siblings), hotlists, sector and flagged views have no add button, no ×, no grip
  and no Remove in the row menu. A reorder or remove recipe aimed at one proves
  nothing — switch to an owned list first.
- **A signed-in but email-UNVERIFIED account hits the same gate with a different
  prompt**: `isVerifyEmailPromptOpen` rather than `isAuthenticationDialogOpen`.
  Asserting the auth dialog on such a lane fails even though the panel correctly
  stayed shut.
- **Starter lists contain governed CME rows** (`COMEX|GC1!`, `NYMEX|CL1!`). Those
  open the data-terms flow instead of the chart until the account is entitled.
- **Desktop only.** The panel is not offered on mobile; phones get a separate
  overlay with `mobile-watchlist-*` testids and no importer.
- **The in-repo doc is stale on reorder.** `docs/features/workspace/watchlist.md`
  says Manual sort must be chosen first; the code lets any sort reorder and flips
  to manual on drop. Trust the code.
- **Another tab can change the lists underneath you.** The store re-reads on tab
  focus and on collab `WATCHLISTS_CHANGED` hints, so do not leave a second driver
  attached.
- Prior art worth reading before writing a new rig: `qa/watchlist-v2/rig-lib.mjs`
  carries open helpers and store probes.
