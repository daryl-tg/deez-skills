# Chart catalog reads

*Re-driven 2026-10-29 (nightly, smoke depth), tree `32ca0d6c7` (origin/main, v0.467.0), lane on 18103: `chart indicator list --query rsi` (`indicators: []`, `scriptSubTypes: ["RSI"]`, and `packages` led by `wrun/@om-core/ichimoku/conversion`) and `chart drawing schema` (`anchorFormat`, `tools`). Evidence: `http://127.0.0.1:8098/vom-nightly-20261029/r1/`.*

*Re-driven 2026-10-28 (scheduled maintenance, smoke depth), tree `186030b63` (origin/main): `chart indicator list --query rsi`, `chart indicator schema rsi` (`@om-core/rsi` 0.1.1) and `chart drawing schema`. Steps not named here keep the record below. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261028/r1/`.*

*Verified: 2026-10-28, tree `a8fa10974` (origin/main, v0.466.0), lane on 18103 with no chart tab. `indicator schema rsi` returned `{target, spec, fields, paint, note}` with `target.kind stock` and `@om-core/rsi` 0.1.1. `nonsense` returned `indicator_unknown` (exit 2). `indicator list --query rsi` returned `{indicators, scriptSubTypes, packages}`, and `drawing schema` returned `{anchorFormat, tools}`. Not driven: the `--chart`/`--workspace` forms, metric ids and `TECHNICAL_SCRIPT --sub-type`. Previous stamp `8fe6a8432` is an ancestor (10 commits).*

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
