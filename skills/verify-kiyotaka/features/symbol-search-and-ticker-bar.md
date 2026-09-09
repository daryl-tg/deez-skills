# Symbol search and the ticker bar

The ticker bar is the chart's primary control strip: the symbol picker, a variant
chip, quick-interval buttons, the interval chevron, the chart-type picker, and the
layout picker. Changing any of them re-drives the whole data plane, so each proof
must show the chart actually reloaded — not just that a menu opened.

## Sub-features

- `sym-search` the symbol dialog opens, searches, and switches symbol.
- `sym-scope` the scope chips filter results (`search-v2`).
- `tb-interval` quick buttons and the interval chevron change interval.
- `tb-plot` the chart-type picker changes plot type.
- `tb-layout` the layout picker changes the grid.
- `tb-hover` the pickers peek on hover and pin on click.

## How to get to it (user POV)

- Click the symbol button (`BINANCE.F BTCUSDT`), type, pick a result.
- Click `1m` / `1h` directly, or hover the interval chevron for the full list.
- Hover or click `Candle` for chart type, `Layout` for the grid.

## Driving it with control-kiyotaka

Preconditions:

- Baseline from [chart boot](./chart-boot-and-data-plane.md), guest modal dismissed.

- **Open symbol search.** Run
  `./control-kiyotaka browser find role button click --name "BINANCE.F BTCUSDT"`,
  then `./control-kiyotaka browser snapshot -i -c`. The search field's accessible
  name is `Search symbols...` while its visible placeholder reads *"Search by
  symbol or name"* — match the accessible name, not the pixels. The current symbol
  sits in a nested textbox as a chip (`BTCUSDT`). Scope chips are
  `button "All"`, `Equities`, `CME`, `Crypto`, `Forex`, `Commodities`, `Macro`,
  `Predict`.
- **Read the result shape.** Results group by asset class, each group capped with a
  `See all <Class>` row; the right-hand rail previews the highlighted symbol and
  its venues (`1 VENUE`, *"click a venue to open"*), and the footer carries the
  match count (`24 results`). Picking a symbol takes two steps when the venue
  matters: the row, then the venue in the rail.
- **Search and switch.** Run
  `./control-kiyotaka browser fill "$(...)" ` against the `Search symbols...`
  textbox by ref from the snapshot, then click the result row by its accessible
  name. Re-snapshot first — the rows are new refs.
- **Prove the switch reached the engine**, not just the label: poll the candle
  predicate again and read
  `./control-kiyotaka browser eval "(()=>JSON.stringify({title:document.title,bars:window.tc[0].metadata[0].rawData.length}))()"`.
  `document.title` follows the symbol. Bars must climb back above 50 — a label
  change with an empty chart is a failed switch.
- **Interval.** Run `./control-kiyotaka browser find role button click --name "1h"`
  for a quick button. For the full list use `button "Interval"` — that is the
  chevron, and interval binds hover-open to the chevron only, so a snapshot after
  a plain click on the label proves nothing.
- **Chart type / layout.** `button "Candle"` and `button "Layout"`. Both peek on
  hover (~150ms) and pin on click, with a ~200ms leave-close bridge; drive
  `hover` then `snapshot` if the claim is about the peek.
- **Proof.** For each change: the accessible name of the control after the change,
  the engine read showing bars reloaded, and a screenshot. Restore the original
  symbol and interval afterwards.

## Gotchas

- **A label change is not a symbol change.** The ticker bar updates optimistically;
  the engine reload is the real event. Always re-assert the candle predicate.
- The pickers are hover-driven. `agent-browser` `click` does not emit the hover
  sequence, so a click-only drive can miss a peek-only state — and touch and the
  agent puppet deliberately never hover-open.
- Scope chips and the views rail exist only under the `search-v2` flag. If they are
  absent, the flag is off for this session — report that, do not route around it.
- The whole ticker bar's ghost-ids log as unregistered on a guest boot. Use ARIA
  names.
- Switching symbol on the authed lane writes to the account's autosaving
  workspace. Use a throwaway account or restore the original symbol.
