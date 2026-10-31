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
Not driven: the other tools (the vertical line's new axis label from titan 1214
included: `toolbar-item-trendline:tool-submenu-arrow` opened no visible
submenu on a click), favorites (`FAVORITES` wall), the drawing-sync scope, and
whether a guest's drawing persists across a reload.

## Sub-features

- `dt-place` a tool places a drawing on the chart.
- `dt-toolbar` the floating toolbar appears for the selected drawing.
- `dt-delete` the selected drawing is removed.
- `dt-colour` the floating toolbar's colour popover keeps a typed colour on an
  outside click and drops it on `Escape`.
- `dt-cancel` `Escape` during a creation leaves no drawing behind.

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
  colour), `tqb-cycle-lineStyle-btn`, `tqb-lock-btn`, `tqb-settings-btn`,
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

- **Fib levels can follow a log scale (source, `679091780e`; the row driven
  2026-11-01).** The Fibonacci retracement and the trend-based fib extension
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
