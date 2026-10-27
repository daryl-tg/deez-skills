# Drawing tools

The left toolbar holds the drawing tools: trend line, Fibonacci, patterns,
positions, brush, shapes, arrows, text, emoji and the ruler. A user picks a tool,
clicks the chart to place it, and gets a floating toolbar for colour, width,
lock, settings and delete. Created 2026-10-27 from a live drive on product tree
`7290d33d10` (53 behind `origin/main` `df3fdcb62e`), lane `18103`, a real
guest-JWT lane, on CRYPTOCAP BTC.D 1h. Driven: a guest placed a trend line and
deleted it. Not driven: the other tools, favorites (`FAVORITES` wall), the
drawing-sync scope, and whether a guest's drawing persists across a reload.

## Sub-features

- `dt-place` a tool places a drawing on the chart.
- `dt-toolbar` the floating toolbar appears for the selected drawing.
- `dt-delete` the selected drawing is removed.

## How to get to it (user POV)

- Click a tool in the left toolbar, then click two points on the chart.
- Select a drawing to get its floating toolbar. `Delete` removes it.

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
- **`dt-delete`.** `press Delete` removed the selected line.
- **Proof.** A screenshot with the line and its floating toolbar, then one
  without it. The engine keeps drawings under `window.tc[0]._drawingManager`,
  but this pass did not take a count from it, so the frames are the proof.

## Gotchas

- **Tools have no accessible names.** Every tool reads `More tools` in the a11y
  tree. Use the testids.
- **A guest's drawing is not proof of persistence.** Guests have no saved
  workspace, so do not report a reload that loses a guest drawing as a bug.
