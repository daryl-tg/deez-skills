# Drawing tools

The left toolbar holds the drawing tools: trend line, Fibonacci, patterns,
positions, brush, shapes, arrows, text, emoji and the ruler. A user picks a tool,
clicks the chart to place it, and gets a floating toolbar for colour, width,
lock, settings and delete. Created 2026-10-27 from a live drive on product tree
`7290d33d10` (53 behind `origin/main` `df3fdcb62e`), lane `18103`, a real
guest-JWT lane, on CRYPTOCAP BTC.D 1h. Driven: a guest placed a trend line and
deleted it. Re-driven 2026-10-28 on `29c9cda0a2` (`origin/main`, lane
`18103`, no JWT) on COINBASE BTC-USD 1h: the same trend line placed, its
floating toolbar rendered with `toolbar-item-delete-icon-btn` present, and
`press Delete` removed it. Re-driven 2026-10-29 on `78ec9625d9` (`origin/main`,
lane `18103`, no JWT) on CRYPTOCAP BTC.D 1h: a trend line placed, its colour set
from the custom colour popover by typing a hex and clicking outside (kept), a
second typed hex dropped by `Escape` (reverted), a creation cancelled with
`Escape` after one click (no line, no console `TypeError`), and `Delete`
removing the line. Re-driven 2026-11-01 on `120d5d5d32` (`origin/main`, lane
`18103`, no JWT) on BINANCE.F BTCUSDT 1h: the trend line placed with the
`.tool-quick-bar` and all its `tqb-*` handles, the custom colour popover
(`.cpk-hex` read `4DA3FF`; `FF00AA` kept on an outside click, `00FF00` dropped by
`Escape`, the swatch read `rgb(255, 0, 170)` both times), `Delete` removing the
line, a creation cancelled with `Escape` (no line; the console's one `TypeError`
was the guest's `[wrun-registry] package listing unavailable: Failed to fetch`
warning, not the cancel), and a Fibonacci retracement whose settings card
carried the `Fib levels based on log scale` row reading `aria-checked="false"`.
Re-driven 2026-11-03 on `215896e614` (`origin/main`, lane `18103`, a guest
JWT, the gateway name mapped in the browser) on BINANCE.F ETHUSDT 1h: the
trend line placed with two clicks and its `.tool-quick-bar` (the same 15
`tqb-*` handles), `tqb-more-btn` opening `tqb-more-menu` with nine items,
a right-click on the line opening the app's own menu with its
`chart-ctx-drawing-*` rows, and `chart-ctx-drawing-remove` deleting the line
(`.tool-quick-bar` gone). Not driven that day: the colour popover, the
cancelled creation, the fib card and the magnet. Re-driven 2026-11-02 on
`a4488341f6` (`origin/main`, lane `18103`, no JWT) on BINANCE.F SOLUSDT 1h: the trend line placed with two clicks and its
`.tool-quick-bar` (the same `tqb-*` handles plus a `number-input`, and no
`tqb-constrain-btn` on desktop), the custom colour popover (`.cpk-hex` read
`4DA3FF`; `FF00AA` kept on an outside click, `00FF00` dropped by `Escape`, the
swatch read `rgb(255, 0, 170)` both times), `Delete` removing the line, a
cancelled creation with zero `TypeError` lines in the console, the Fibonacci
card's `Fib levels based on log scale` row (`aria-checked="false"`), and the
magnet's strength memory (`Shift+Alt+M` wrote `orange-tc-magnet-strength` =
`weak` into localStorage, which had been `null`). A down-move-up drag followed
by one click left NO selection on this tree; two plain clicks did. Not driven:
the other tools (the vertical line's axis label from titan 1214 included:
`toolbar-item-trendline:tool-submenu-arrow` opened no visible submenu on a
click on 2026-11-01), the Shift constraint (engine-side, frame-only proof),
favorites and their drag reorder (`FAVORITES` wall), the drawing-sync scope,
and whether a guest's drawing persists across a reload. Re-driven 2026-11-04 on
`8436920004` (`origin/main`, lane `18103`, a guest JWT, the gateway resolving)
on COINBASE BTC-USD 1h: the trend line placed with two clicks, its
`.tool-quick-bar` now carrying `tqb-templates-btn` between `tqb-lock-btn` and
`tqb-settings-btn` (16 `tqb-*` handles), the templates list opened from it with
no wall, one `Escape` closing the list with the line still selected and a
second deselecting it, `tqb-more-menu` listing eight rows with no
`tqb-menu-templates`, and `tqb-remove-btn` deleting the line. Not driven that
day: `Save as template…` as a guest, an FRVP's templates, the colour popover,
the cancelled creation, the right-click menu and the magnet.

## Sub-features

- `dt-place` a tool places a drawing on the chart.
- `dt-toolbar` the floating toolbar appears for the selected drawing.
- `dt-delete` the selected drawing is removed.
- `dt-colour` the floating toolbar's colour popover keeps a typed colour on an
  outside click and drops it on `Escape`.
- `dt-cancel` `Escape` during a creation leaves no drawing behind.
- `dt-context` a right-click on a drawing opens the app's menu for it (settings,
  clone, copy, lock, hide, order, show on, delete) above the chart's own rows.
- `dt-templates` the floating toolbar's templates button lists the drawing's
  saved looks, saves one, makes the current look the default for new drawings
  or resets it; `Escape` closes one layer at a time.

## How to get to it (user POV)

- Click a tool in the left toolbar, then click two points on the chart.
- Select a drawing to get its floating toolbar. `Delete` removes it.
- In the floating toolbar, click the `+` swatch to pick a custom colour or type
  a hex; click away to keep it, press `Escape` to drop it.

## Driving it with control-kiyotaka

Preconditions: baseline from [chart boot](./chart-boot-and-data-plane.md), with
the top overlay cleared.

- **Handles.** The toolbar is `left-toolbar`. Each tool is
  `toolbar-item-<tool>:tool` with `-icon-btn` and `-submenu-arrow` children, for
  example `toolbar-item-trendline:tool-icon-btn`,
  `toolbar-item-fibonacciretracement:tool-icon-btn` and
  `toolbar-item-rectangle:tool-icon-btn`. The cursor is
  `toolbar-item-default-icon-btn`, then `toolbar-item-ruler`. Hide and show the
  bar with `toolbar-hide-btn` and `toolbar-show-btn`.
- **`dt-place`.** `find testid "toolbar-item-trendline:tool-icon-btn" click`,
  then `browser mouse move 400 400`, `mouse down`, `mouse up`, then the same at
  `800 300`. Quote the testid: it contains a colon.
- **`dt-toolbar`.** After placement the floating toolbar shows colour swatches,
  text colour, width, line style, lock, settings, more and delete
  (`toolbar-item-delete-icon-btn`). The chart shows the line, an `+ Add Text`
  label and a dimensions tag (`78 x 0.092 (+0.15%)` on the driven run).
- **The floating toolbar's handles, driven 2026-10-29.** It is
  `.tool-quick-bar` and every control has a `tqb-` testid:
  `tqb-swatch-color-{0,1,2,custom}-btn` (line colour, with
  `tqb-swatch-glyph-color`), `tqb-swatch-fontColor-{0,1,2,custom}-btn` (text
  colour), `tqb-cycle-lineStyle-btn`, `tqb-lock-btn`, `tqb-templates-btn`
  (since `20b0fce8b3`, only on a drawing with settings), `tqb-settings-btn`,
  `tqb-more-btn` and `tqb-remove-btn`. `toolbar-item-delete-icon-btn` is the
  LEFT toolbar's trash, not this bar's.
- **`dt-colour`, driven 2026-10-29.** `find testid tqb-swatch-color-custom-btn
  click` opens `.cpk-popover` with a hex field `.cpk-hex` (it read `4DA3FF`).
  Select its text, `type ".cpk-hex" "FF00AA"`, and do NOT press Enter. Click
  outside (the empty ticker-bar strip at `640 62`): the popover closed and
  `tqb-swatch-color-0-btn` became `rgb(255, 0, 170)` with class `--on`, and the
  frame shows the line in that pink. Reopen, type `00FF00`, `press Escape`: the
  popover closed and the swatch stayed `rgb(255, 0, 170)`. Read the colour from
  the swatch's inline `style`; the glyph's computed background is transparent.
  Source: `662faad117`.
- **`dt-cancel`, driven 2026-10-29.** Click
  `toolbar-item-trendline:tool-icon-btn`, click the chart once, move, then
  `press Escape`: no line was left and `browser console` held no `TypeError`
  (before `662faad117` a cancelled creation threw on a null tool).
- **The floating toolbar's more menu (driven 2026-11-03).** `find testid
  tqb-more-btn click` opens `tqb-more-menu`, its rows inside
  `.tqb-menu-scroll`, each led by an icon: `tqb-menu-clone`, `-copy`,
  `-front`, `-back` and `-show-on-{all,andAbove,andBelow,only}`: eight rows
  on 2026-11-04. The `-templates` row moved out to `tqb-templates-btn`
  (`20b0fce8b3`). A guest got no `tqb-menu-sync-<scope>` row.
- **`dt-templates`: the bar's templates list (driven 2026-11-04).** `find
  testid tqb-templates-btn click` sets its `aria-expanded` to `true` and opens
  `.settings-templates-menu--bar`, whose rows are the settings card's own:
  `settings-templates-empty` (`No saved templates`),
  `settings-template-save-as` (`Save as template…`),
  `settings-template-save-default` (`Use these settings for new ones`, with
  `settings-template-default-note`) and `settings-template-reset-defaults`; a
  saved look adds `settings-template-<id>`, `-rename` and `-delete` (source).
  There is no `settings-templates-trigger` on the bar. A guest met no wall on
  opening it. Since `9033deb4d9` one `Escape` closes one layer: the first
  closed the list (`aria-expanded` back to `false`) with `.tool-quick-bar`
  still up, the second deselected the line; `tqb-more-menu` closes the same
  way. An Escape from the drawing's own text field still ends the edit and
  deselects (source). An FRVP's templates now open this same list instead of
  its settings panel (`useFrvpProfileDoor`, source).
- **`dt-context`: the right-click menu on a drawing (driven 2026-11-03).**
  Move the pointer onto the line (`mouse move 600 350` for a line from `400
  400` to `800 300`), then `mouse down right` and `mouse up right`. The app's
  own menu opens with a `TREND LINE` section,
  `chart-ctx-drawing-{settings,clone,copy,lock,hide,order,show-on,remove}`,
  and a `CHART` section (`chart-ctx-paste`, `-copy-price`,
  `-add-to-watchlist`, `-reset-view`, `-add-alert`, `-grid`, `-settings`,
  `-report-problem`, `-remove-indicators`). Every row leads with an icon
  (`5c2d8603a6`). A guest got no `chart-ctx-drawing-alert` or `-sync` row.
  `chart-ctx-drawing-remove` deletes the line. Since `12906d4136` the chart
  cancels the browser menu only on `#main-chart`, and text fields keep the
  native menu (source).
- **`dt-delete`.** `press Delete` removed the selected line. To reselect a line
  after an outside click, click on the line itself; `.tool-quick-bar` returns.
- **Proof.** A screenshot with the line and its floating toolbar, then one
  without it. The engine keeps drawings under `window.tc[0]._drawingManager`,
  but no count has been read from it: on 2026-10-28 its `drawingSets`,
  `drawingRenderSets` and `drawingHitBoxes` read `0` before the placement, with
  the line on screen, and after the delete alike. The frames are the proof.
  `toolbar-item-delete-icon-btn` is not a literal in source (the id is built at
  runtime), but it resolved live on 2026-10-28.

## Gotchas

- **Place with two clicks, not a drag (driven 2026-11-02).** `mouse move 400
  400`, `mouse down`, `mouse up`, then `mouse move 800 300`, `mouse down`,
  `mouse up`. A `down`, `move`, `up` drag followed by a click left no selected
  drawing and no `.tool-quick-bar` on `a4488341f6`; the two-click sequence
  placed the line at once. The hex field takes the top-level verb,
  `./control-kiyotaka browser fill .cpk-hex "FF00AA"`; `find css` is not a
  locator (`role, text, label, placeholder, alt, title, testid, first, last,
  nth` are).
- **Shift squares and snaps (source, `87e6a66297`, titan alpha.1220 and
  later; not driven).** Holding Shift squares a rectangle, rounds an ellipse,
  snaps a line to 45° steps and straightens a drag, TradingView-style. It is
  engine-side, so the only proof is a frame. On a phone the same constraint is
  a latch: `tqb-constrain-btn` (`Align 45°`) in the quick bar, a drawing-bar
  tile and the Super Search row `tools:drawing-constrain`, all rendered only
  when `isMobile` and the tool is constrainable (the fib retracement shows
  none). A desktop guest sees none of them (driven: `tqb-constrain-btn`
  absent).
- **The magnet remembers its strength (source, `38af41350d`; driven
  2026-11-02).** The toolbar magnet, `Shift+Alt+M` and the Super Search
  `magnet` toggle restore the last strength instead of always `weak`
  (`useMagnetMode.ts`, localStorage `orange-tc-magnet-strength`): the first
  press on a fresh profile wrote `weak`.
- **Favourite tools reorder by drag (source, `38af41350d`).** A favourite row
  carries `data-favorite-tool`, lifts 4 px and drops through
  `userStore.reorderFavoriteTools` (`ToolsItemWidget.vue`). A guest meets the
  `FAVORITES` wall first.
- **Positions and defaults (source, `4e48acdc82`, `3ed1679add`).** A new
  position tool starts from the last account size and risk
  (`tool-style-memory.ts`). The settings card's "save as default" goes through
  `saveToolDefaultStyle` and reports with the drawing's name; a tool with an
  empty default lane (Image) shows the row off with a note (`defaultLaneEmpty`,
  `dialogs.settingsTemplates.defaultKeepsNote`). Order-flow tools on a US
  stock's Live price feed ask to switch to Trades first (`dc92b520b5`), which
  a guest never reaches.
- **Fib levels can follow a log scale (source, `679091780e`; the row driven
  2026-11-01 and 2026-11-02).** The Fibonacci retracement and the trend-based fib extension
  carry a `Fib levels based on log scale` switch in their settings card (key
  `levelsOnLogScale`, off by default, `offWhenAbsent` so old fibs show it too;
  Reset turns it off). The row has no testid, so match its label. Reach it by
  placing `toolbar-item-fibonacciretracement:tool-icon-btn` with two clicks and
  opening `tqb-settings-btn`: the card is a floating panel, not a `.q-dialog`
  (the overlay union read `0`), headed `FIBONACCI RETRACEMENT` with `Templates`
  and `Reset`, sections `FILL`, `STROKE`, `TEXT`, `CORNER`, `Levels`,
  `POSITION` and `SHOW ON`; the log-scale row's switch read
  `aria-checked="false"`. Flipping it and comparing level prices is still
  undriven. No settings gate was found for a guest.
- **Vertical and cross lines keep their axis labels at rest (source, titan
  1214 via `612ec349cf`; not driven).** A `highlight` flag, on by default, draws
  the vertical line's time label (settings row `Time label`) and the cross
  line's `Price and time labels` when the drawing is not selected; host markers
  such as session breaks stay `readOnly` with no label. The tools sit in the
  trend-line submenu; `toolbar-item-trendline:tool-submenu-arrow` needs a
  hover-intent pass (`useHoverIntent`), and a bare click on it listed nothing
  on 2026-11-01.
- **The hover quick search can cover the toolbar's top tools.** After a pick in
  `quick-search-dropdown`, its `scope-token-line` stayed in the DOM and
  `find testid "toolbar-item-trendline:tool-icon-btn" click` failed with
  `covered by <div.scope-token-line.v2-tokens>`. Move the pointer onto the chart
  and press `Escape` before the tool click; the retry then placed the line.
- **The settings card is not the colour popover.** `tqb-settings-btn` opens
  the floating card above; `tqb-swatch-color-custom-btn` opens `.cpk-popover`.
  Close the card with `Escape` before reading swatches, or the popover probe
  reads the card.

- **Tools have no accessible names.** Every tool reads `More tools` in the a11y
  tree. Use the testids.
- **A guest's drawing is not proof of persistence.** Guests have no saved
  workspace, so do not report a reload that loses a guest drawing as a bug.
