# Retired kScript package kinds

*Re-driven 2026-11-10 (nightly), tree `c9bc93a355` (origin/main, v0.493.1), guest lane on 18143, booted with no guest 429. `search rsi --kind kscript-indicator` exits 2 `kind_retired`. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261110/r1/` (`cli/ks-search.txt`).*

*Re-driven 2026-11-09 (scheduled maintenance), tree `0d3d29cd27` (origin/main, v0.493.0), bare lane on 18145 (dummy `OM_API_KEY`, dead service URLs) with a scripted fake model on 18144. `search rsi --kind kscript-indicator` exit 2 `kind_retired`. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261109/r1/`.*

*Re-driven 2026-11-09 (nightly), tree `5bfa0ccf6` (origin/main, v0.492.0), guest lane on 18143, booted with no guest 429. `search rsi --kind kscript-indicator` exit 2 `kind_retired`, `open @om-core/rsi --print` 0.3.4. Citation `cmd/search.ts:130` corrected. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261109/r1/` (`cli/48-49`).*

*Re-driven 2026-11-08 (nightly), tree `5590b4d1c` (origin/main, v0.492.0), guest lane on 18141, booted in 2 s with no guest 429. `search rsi --kind kscript-indicator --format json` exit 2 `kind_retired`; `open @om-core/rsi --print --format json` `wrun-indicator` 0.3.4. Not re-driven: the `install`/`publish` refusals and the MCP tools. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261108/r1/` (`cli/50-51`).*

*Re-driven 2026-11-07 (nightly), tree `05f450fc5` (origin/main, v0.492.0), guest lane on 18141, booted with no guest 429. `search rsi --kind kscript-indicator --format json` exit 2 `kind_retired`; `open @om-core/rsi --print --format json` resolved the `wrun-indicator` 0.3.4. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261107/r1/` (`cli/70-71`).*

*Re-driven 2026-11-06 (nightly), tree `50fcc594b` (origin/main, v0.492.0), guest lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), booted at 19:18Z with no guest 429, host load average 10 falling to about 3.3. `search rsi --kind kscript-indicator` exit 2 `kind_retired`; `open @om-core/rsi --print --format json` `kind: wrun-indicator`, 0.3.4, publisher text wrapped in `<untrusted-publisher-text>`. Not re-driven: the `install`/`publish <dir>` refusals. Evidence: `http://127.0.0.1:8098/vom-nightly-20261106/r1/` (`cli/search-kscript.txt`, `cli/open-rsi.txt`).*

*Re-driven 2026-11-05 (nightly), tree `3a0ea623e` (origin/main, v0.492.0), guest lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), booted in 2 s at 19:19Z with no guest 429, host load average about 4.4. `search rsi --kind kscript-indicator` exit 2 `kind_retired`; `open @om-core/rsi --print --format json` `kind: wrun-indicator`, 0.3.4; MCP `package_open {ref:"@om-core/rsi"}` answered with the publisher text withheld. Not re-driven: the `install`/`publish <dir>` refusals. Evidence: `http://127.0.0.1:8098/vom-nightly-20261105/r1/` (`cli/search-kscript.out`, `cli/open-rsi.out`, `cli/mcp-guest.json`).*

*Re-driven 2026-11-04 (nightly), tree `9acb5fb56` (origin/main, v0.491.0), guest lane on 18163. `search rsi --kind kscript-indicator` exit 2 `kind_retired` with the `--kind wrun-indicator` hint; `install @backquant/order-blocks` exit 2 `package_deleted`; `open @om-core/rsi --print --format json` `wrun-indicator` 0.3.4; over MCP `package_search {kind:"kscript-indicator"}` `kind_retired` and **`package_open {ref:"@om-core/rsi"}` answered** (`wrun-indicator` 0.3.4, publisher text withheld), so last night's 30 s `tool_failed` did not recur. `chart indicator schema nonsense` still lists `a registry kScript (legacy) indicator package (@scope/name)` (README gap). Not re-driven: the `<dir>` refusals. Evidence: `http://127.0.0.1:8098/vom-nightly-20261104/r1/` (`cli/151`, `cli/162-165`, `cli/111-mcp2.json`).*

*Re-driven 2026-11-03 (nightly), tree `777ee7f21` (origin/main, v0.488.0), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 2.8; the first `up` died on a guest sign-in 429 (35 minutes) and the lane booted in 3 s at 19:55Z. `search rsi --kind kscript-indicator` exit 2 `kind_retired` with the `--kind wrun-indicator` hint; `install @backquant/order-blocks` exit 2 `package_deleted` (the row is gone, so the registry-ref refusal stays unreachable); over MCP `package_search {kind:"kscript-indicator"}` `kind_retired` (text withheld); `open @om-core/rsi --print --format json` `wrun-indicator` 0.3.4. **`package_open {ref:"@om-core/rsi"}` over MCP answered `tool_failed` after 30 s in two fresh sessions** while the CLI read answered (README gap). The `<dir>` publish and install refusals were not re-driven. Evidence: `http://127.0.0.1:8098/vom-nightly-20261103/r1/` (`cli/kscript-*.txt`, `cli/132`, `cli/236`, `cli/31-32-mcp-*.json`).*

*Re-driven 2026-11-02 (scheduled maintenance), tree `587ce2d0b` (origin/main, v0.480.3), lane on 18168 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 5. `search rsi --kind kscript-indicator`, `chart indicator schema @backquant/order-blocks`, `publish <dir> --dry-run` and `install <dir>` all exit 2 `kind_retired` with the guide's messages; `open @om-core/rsi --print` → `kind:"wrun-indicator"`, version `0.3.4`.*

*Re-driven 2026-11-02 (nightly), tree `2567b7974` (origin/main, v0.480.3), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 4. Re-driven whole: `search rsi --kind kscript-indicator` and `search demo --kind kscript-library` exit 2 `kind_retired` in 0.5 s; `publish <dir> --dry-run` and `--validate` on a `kscript-indicator` manifest exit 2 `kind_retired` with the `om wrun create` hint; `install <dir>` exit 2 naming `@demo/x`; `chart indicator schema @backquant/order-blocks` exit 2 `kind_retired`; over MCP `package_search {kind:"kscript-indicator"}` `kind_retired` (text withheld) and `chart_indicator_schema` `kind_retired` with the `package_open` hint; `open @om-core/rsi --print --format json` `wrun-indicator` 0.3.4 with the `wrunRef` URL, the text form printing the URL alone, and `package_open` the same fields. A default `search rsi` still returned no `hidden`, so that count stays source-only, and the `indicator_unknown` hint still names the kScript form (README gap). Evidence: `http://127.0.0.1:8098/vom-nightly-20261102/r1/` (`cli/182-191b`, `cli/210-mcp-calls.json`).*

*Verified: 2026-11-01 (nightly), tree `7ce379c45` (origin/main, v0.480.3), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 2.9. Driven: `search rsi --kind kscript-indicator` and `search demo --kind kscript-library` (exit 2 `kind_retired`, no request sent); `publish <dir> --dry-run` and `publish <dir> --validate` on local manifests declaring each retired kind (exit 2 `kind_retired`, before the cover, the terms or any upload); `install <dir>` on the same directory (exit 2 `kind_retired` naming `@demo/x`); `chart indicator schema @backquant/order-blocks` (exit 2 `kind_retired`); over MCP stdio `package_search {kind:"kscript-indicator"}`, `chart_indicator_schema {indicatorType:"@backquant/order-blocks"}` and `chart_indicator_add {workspaceId, chartIndex, indicatorType:"@backquant/order-blocks"}` (each `isError` `kind_retired`); `om open @om-core/rsi --print` and `package_open {ref:"@om-core/rsi"}` (success: `kind: wrun-indicator`, `version 0.3.4`, `chart_url`, `wrun_ref`, no `script_id`); a default `search rsi` (`total: 42`, no `hidden` key). Not driven: a registry install or `om open` of a kScript ref (`@backquant/order-blocks` answers `package_deleted`, so the registry no longer lists one), and a default search with `hidden > 0`. Evidence: `http://127.0.0.1:8098/vom-nightly-20261101/r1/` (`cli/33`, `cli/60-64`, `cli/30b-30c`, `cli/90*`).*

Since #2234 (`4f4903ab9`, v0.480.3) om no longer publishes, installs, opens,
charts or lists a kScript (legacy) package. A user who still holds a
`kscript-indicator` or `kscript-library` manifest, or who references one by
`@scope/name`, is told the kind is retired and pointed at an Indicator instead,
on every verb and before any byte leaves the machine. `om open` resolves
Indicator packages only. None of it needs an account.

## Sub-features

- `search-kind-refused`: `om search <words> --kind kscript-indicator` (or
  `kscript-library`) exits 2 `kind_retired` with no request sent; a default
  search leaves retired rows out and counts them as `hidden`.
- `publish-refused`: `om publish <dir>` on a manifest whose `kind` is retired
  exits 2 `kind_retired` before the cover, the terms or any upload, with
  `--dry-run` and `--validate` alike.
- `install-refused`: `om install <dir>` on such a manifest exits 2
  `kind_retired` naming the package.
- `chart-ref-refused`: `om chart indicator schema @scope/name`,
  `chart_indicator_schema` and `chart_indicator_add` with a bare registry
  reference refuse `kind_retired` before any registry read.
- `open-indicator-only`: `om open <package>` and `package_open` resolve
  `wrun-indicator` packages only; the result's `kind` is always
  `wrun-indicator` and `script_id` is gone.

## How to get to it (user POV)

- `om search rsi --kind kscript-indicator`, `om publish <dir>` or
  `om install <dir>` on an old kScript package directory.
- `om chart indicator schema @scope/name`, or in chat an agent calling
  `chart_indicator_add` with a `@scope/name`.
- `om open @om-core/rsi --print` for the Indicator path that still works.

## Driving it with control-om

Preconditions: a lane the run started. The refusals need no network; `om open`
needs the registry.

- **Search.** `control-om om -- search rsi --kind kscript-indicator --format json`
  exits 2 with `{"error":"kind_retired","message":"kScript packages are
  retired, so the search lists no kscript-indicator packages.","hint":"Use an
  Indicator instead: om search <words> --kind wrun-indicator.","details":{"kind":"kscript-indicator"}}`.
  `--kind kscript-library` reads the same with its own kind. A default
  `search rsi --format json` returns `{results, total}`; `hidden: N` appears
  only when a retired row was dropped (`cmd/search.ts:130`), and the text form
  then ends `N shown (K retired kScript package(s) left out)`. Production
  returned no retired row on 2026-11-01, so `hidden` is source-only.
- **Publish.** Write a directory holding only `om-package.json` with
  `{"spec_version":"1.1","kind":"kscript-indicator","name":"@demo/x","version":"1.0.0"}`
  and run `control-om om -- publish <dir> --dry-run --format json`. It exits 2
  with `error: kind_retired`, the message `kScript packages are retired. Publish
  a wrun indicator instead (om wrun create @you/<name> <dir>).`, a hint that
  walks `om wrun create` → `om wrun build` → `om publish <dir>/dist/package`, and
  `details.registry_code: kind_retired`. `--validate` reads the same. The check
  reads the raw manifest header only, so the rest of the manifest need not be
  valid.
- **Install.** `control-om om -- install <dir> --format json` on the same
  directory exits 2 with `@demo/x is a kScript package, and kScript packages are
  retired.` and the `om search <words> --kind wrun-indicator` hint. A name that
  fails the package-name grammar reads `This package` instead.
- **Chart reference.** `control-om om -- chart indicator schema
  @backquant/order-blocks --format json` exits 2 `kind_retired`: `kScript
  packages are retired, so a registry reference (@backquant/order-blocks) no
  longer adds to a chart.`, hint `Add an Indicator package by its metric id
  (wrun/@scope/name/<output>), or open it on a fresh chart with om open
  <package>.`, `details.indicatorType`. Over MCP stdio ([recipe](./mcp-stdio.md))
  `chart_indicator_schema {"indicatorType":"@backquant/order-blocks"}` answers
  the same with the hint `Call the package_open tool`, and `chart_indicator_add`
  does too when `workspaceId` is passed (`{"workspaceId":"ws_x","chartIndex":0,
  "indicatorType":"@backquant/order-blocks"}`); without `workspaceId` a guest
  lane answers `no_active_workspace` first. `package_search
  {"query":"demo","kind":"kscript-indicator"}` is `isError` `kind_retired` in
  under a millisecond, its message withheld on MCP (`[publisher text withheld
  on MCP; read it with the om CLI or in om chat]`).
- **Open an Indicator.** `control-om om -- open @om-core/rsi --print --format
  json` returns `{kind:"wrun-indicator", package, version, title, description,
  chart_url, resolved_via:"search", wrun_ref}` with `chart_url`
  `https://openmarket.xyz/chart/?wrunRef=%40om-core%2Frsi%40<version>`; the
  text form with `--print` prints the URL alone. `package_open {"ref":"@om-core/rsi"}`
  over MCP returns the same fields with the publisher text withheld. Assert
  `kind` and the `wrunRef` query, not the version.
- **Proof.** Keep each command, its JSON and its exit code, and the MCP
  transcript. The absence of a registry request is the claim for the
  refusals; a tcpdump is overkill, the 0 ms answer is enough.

## Gotchas

- `om open` and `package_open` of a kScript reference cannot be driven from a
  guest lane: the verb searches the registry for a `wrun-indicator` of that
  name first and reads the kind only on a miss, and production answered
  `package_deleted` for `@backquant/order-blocks` on 2026-11-01 (the kScript
  rows are gone from the registry). The registry-ref `om install @scope/name`
  refusal needs a row the same way. Report both as unreachable, not passing.
- The `indicator_unknown` message (`om chart indicator schema nonsense`) still
  lists `a registry kScript (legacy) indicator package (@scope/name)` among the
  accepted forms (`actions/collab/_indicator-series.ts:59`), while the same
  verb refuses that form `kind_retired`. Stale copy after #2234; a product gap
  (README), not drift here.
- `PACKAGE_KINDS` no longer lists either kind, so `om search --help`'s `--kind`
  list and `docs/TOOLS.md` omit them. `om enum` has no package-kind domain to
  check.
- `om alerts kscript sunset` and `om alerts twins` stay (staff-only `alerts`),
  and `om wrun list`'s stock `@om-core/accumulate` is a `wrun-indicator`,
  unaffected.
- The CLI's exit code for every refusal here is the shared handler's default 2;
  no command sets its own. Over MCP the payload is `isError` with `error:
  kind_retired` and the publisher-text message withheld.
