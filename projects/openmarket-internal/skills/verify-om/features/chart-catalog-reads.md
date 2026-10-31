# Chart catalog reads

*Re-driven 2026-11-01 (nightly), tree `7ce379c45` (origin/main, v0.480.3), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 2.9. `chart indicator schema rsi` (`@om-core/rsi` 0.1.1, `period` int 14, 1..2500) and `schema nonsense` (exit 2 `indicator_unknown` listing the stock names); `indicator list --query rsi` (`indicators: []`, `scriptSubTypes: ["RSI"]`, `packages` with `wrun/@om-core/rsi/rsi`); `drawing schema` (`anchorFormat` `role=<epochSeconds>:<price>`, `tools` led by `TrendLine`). New for #2234: `chart indicator schema @backquant/order-blocks` exit 2 `kind_retired` (`kScript packages are retired, so a registry reference (@backquant/order-blocks) no longer adds to a chart.`) before any registry call, while the `indicator_unknown` message still lists `a registry kScript (legacy) indicator package (@scope/name)` as an accepted form (README, product gaps). Evidence: `http://127.0.0.1:8098/vom-nightly-20261101/r1/` (`cli/64-68`).*

*Re-driven 2026-10-31 (nightly), tree `dfefe0a21` (origin/main, v0.480.2), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 1.6: `chart indicator schema rsi` (`@om-core/rsi` 0.1.1, `period` int 14, 1..2500) and `schema nonsense` (exit 2 `indicator_unknown` listing the stock names). `indicator list` and `drawing schema` were not re-driven. Evidence: `http://127.0.0.1:8098/vom-nightly-20261031/r1/` (`cli/74-75`).*

*Re-driven 2026-10-30 (scheduled maintenance), tree `3cb50a821` (origin/main, v0.478.0), fresh lane on 18165, host load average about 140. `chart indicator list` 65; `indicator schema rsi` names `@om-core/rsi` 0.1.1; `drawing schema` reads `anchorFormat` `role=<epochSeconds>:<price>`. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261030/r1/`.*
*Re-driven 2026-10-30 (nightly, smoke depth), tree `3cb50a821` (origin/main, v0.478.0), lane on 18163: `chart indicator schema rsi --format json` returned `@om-core/rsi` 0.1.1 (`Relative Strength Index`) with one `period` field (`int`, default 14, min 1, max 2500). With no argument it exits 1 with `missing required argument 'type-or-id'`. Drawing schemas and `indicator list` were not re-driven. Evidence is local only (the `8098` renderer did not answer): `artifacts/vom-nightly-20261030/r1/`.*

*Re-driven 2026-10-29 (scheduled maintenance, smoke depth), tree `7ec575e55` (origin/main, v0.467.0 plus #2194), fresh lane on 18161. `chart indicator list` returned 65 indicators. `chart indicator schema RSI` resolved `@om-core/rsi` 0.1.1, and `chart drawing schema` returned `{anchorFormat, tools}`. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261029/r1/`.*

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
- **A bare `@scope/name` is refused, not described.** Since #2234
  (`4f4903ab9`) `chart indicator schema @scope/name` and
  `chart_indicator_schema {indicatorType:"@scope/name"}` exit 2 `kind_retired`
  before any registry read; the Indicator forms are the metric id
  `wrun/@scope/name/<output>` or `om open <package>`. See
  [kScript retirement](./kscript-retirement.md). The `indicator_unknown` hint
  still names the retired form (a product gap, README).
