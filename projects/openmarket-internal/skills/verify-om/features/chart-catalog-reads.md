# Chart catalog reads

*Verified: 2026-10-23, tree `42d044b02` (origin/main, v0.462.0): on a guest lane with no chart tab open, `chart indicator schema rsi` returned `target {kind:"stock", type:"rsi", package:"@om-core/rsi", version:"0.1.1"}` and one field `period` (int, default 14, 1..2500, step 1); `--keys period --format json` returned the same; `nonsense` returned `indicator_unknown` listing the stock names; `chart indicator list --query rsi` returned `scriptSubTypes ["RSI"]` and the `@om-core/rsi` and `@om-core/ichimoku` packages; `chart drawing schema trend_line` returned `invalid_options` `unknown drawing tool 'trend_line'`. Not driven: anything with `--chart`/`--workspace` (needs a live chart workspace), the `wrun/@scope/name/output` metric-id form, and `TECHNICAL_SCRIPT --sub-type`.*

A user (or an agent) asks what an indicator or drawing tool accepts before
putting it on a chart: its settings, their kinds, defaults and ranges, and which
package draws it. These are catalog reads. They need no chart open, unlike the
chart verbs that change a workspace, which need a human's GUI chart tab.

## Sub-features

- `chart-indicator-schema`: `om chart indicator schema <type>` describes one
  indicator's settings (new in v0.462.0, `chart_indicator_schema`).
- `chart-indicator-list`: `om chart indicator list [--query t]` lists the
  indicator catalog without a workspace.
- `chart-drawing-schema`: `om chart drawing schema [tool]` lists drawing tools
  or describes one.

## How to get to it (user POV)

- `om chart indicator schema rsi` before `om chart indicator add`.
- In chat, the agent calls `chart_indicator_schema` to check setting names.

## Driving it with control-om

Preconditions: a lane the run started. No chart, workspace or account needed.

- **Describe a stock indicator.** `control-om om -- chart indicator schema rsi
  --format json`. Assert `target.kind` `stock`, `target.package`
  `@om-core/rsi`, and a `fields[]` entry with `key` `period`, `kind` `int` and
  numeric `default`/`min`/`max`. Assert the shape, not the version.
- **Filter keys.** `--keys period` returns only that field.
- **Unknown type.** `chart indicator schema nonsense --format json` returns
  `indicator_unknown`, and its message lists the accepted stock names.
- **The catalog.** `control-om om -- chart indicator list --query rsi
  --format json` returns `indicators`, `scriptSubTypes` and `packages`. Each
  package row carries `id` (`wrun/@om-core/rsi/rsi`), `placement` and `params`.
- **Drawing tools.** `control-om om -- chart drawing schema` with no tool lists
  every supported tool. An unknown tool returns `invalid_options` with a hint to
  run it bare.

## Gotchas

- Driven non-interactively (stdout piped), `chart indicator schema rsi` printed
  JSON even without `--format json`. Source also has a text renderer (a head
  line, then one row per setting), so pass `--format json` explicitly rather
  than relying on either.
- `--chart <n>` or `--workspace <id>` switches these verbs to the workspace
  document (`indicatorId` form). A headless lane has no workspace, so that form
  belongs with the chart mutation verbs, which stay `live verification pending`.
- `trend_line` is not a tool name. Take names from the bare `drawing schema`
  listing rather than guessing.
