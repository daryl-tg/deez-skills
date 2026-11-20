# Feed views and candles from your own data

A person's own relay feed draws on the chart in two ways: as the main plot, by opening an `OM` `feed:` target, or as a FEED pane. A FEED view takes any shape the kit's catalog holds (line, area, histogram, step, markers, bars, scatter, pie, heatmap, table, tiles, card, meter, candles), changed in its settings dialog with Draw as, Shows and Columns, and it updates live from the relay's stream at intervals from 1 second up. Candles draw from one value (a bar per chart interval) or from the feed's own open, high, low and close columns, in a pane and as the main plot. It landed on main 2026-11-20 as !13599 (squash `b63afe412f`, kit pinned `0.121.1`); the landed commit differs from the driven one by a rebase over 63 commits, the published kit pin, one boot locale key and a ceiling move, proven by tests and the landing gate only. DRIVEN 2026-11-19 on the branch `land/byod-any-data` at `2c2dc7fda0`, before it merged, (kit `0.121.0-byod.6` through three uncommitted pin files), before its final rebase, on lane `18160`, two signed-out browsers with `kiyo.flag-overrides {"feeds":true}`, against a local relay rig (om `daf4518767`, relay `617b265`): one-value candles in a pane at 1 minute and 5 seconds, own OHLC candles at 1 and 5 minutes with one bars read per column, the volume histogram at 5 minutes, a feed as the main plot in candles with RSI and EMA, every shape on one chart, the legend row across shape changes, silences, 15 interval switches, and two-browser latency (report `~/Documents/dev-notes/om-byod-any-data/run-artifacts/reports/goal-12.md`, frames `run-artifacts/final5/review/`). Earlier passes on the same branch: `reports/goal-10b.md` (`ade9c93cdb`), `reports/goal-6f.md` (`109fad1088`). The commit that lands differs from `2c2dc7fda0` by rebases, and the kit the chart lands on differs from `byod.6` by `byod.7`'s fold-naming refusal, which reached the chart by tests only. Not driven: a signed-in browser, so a candle choice surviving a reload of a saved chart is unproven; an agent-built chart document rendering (needs collab deployed); anything in production (nothing is deployed and the production stream switch is off).

## Sub-features

- `feed-main`: an `OM` target `feed:<scope>/<name>:<column>` (one column) or `feed:<scope>/<name>` (no column) draws the feed as the main plot. It lands on Line; Candle in the ticker's chart-type menu draws candles.
- `feed-pane`: a FEED pane over `@<scope>/<name>` with `plot`, `fold` and `columns`. Folds: `time`, `latest`, `grid`, `calendar`, `pair`, `bins`, `rows`, `range`, `ohlc`.
- `feed-settings`: the pane's settings dialog. Draw as picks the shape; Shows picks the fold; Columns picks the columns. A shape that takes one column (histogram over time, markers) says `This shape draws one column` under Columns and greys the rest.
- `feed-legend-row`: every view keeps exactly one legend row with a settings button that reopens the dialog on the view's kind, after a shape change and after Undo. Panels keep their pane slot; a widget changed to a pane opens a new bottom pane.
- `candles-range`: Draw as Candles, Shows `From one value`: one column, a bar per chart interval. At or below the feed's own cadence each reading is a flat dash.
- `candles-ohlc`: Draw as Candles, Shows `From open, high, low and close`: the pickers pre-fill from the column names, volume optional, drawn as a histogram under the candles.
- `seconds-intervals`: 1s, 5s, 15s and 30s for a feed chart. A signed-out viewer's interval menu walls them.
- `feed-silence`: a silence longer than one bar breaks the line in the main and in every pane at the same stamps.
- `feed-stream`: after the first reads, new readings arrive on `GET /api/v2/feeds/stream?feeds=…`, with no polling (except the defect below).

## How to get to it (user POV)

- Symbol search's Yours tab lists the viewer's own feeds and targets `feed:scope/name:column` (signed in only; see symbol search).
- The indicator dialog's feed picker adds a FEED pane (its search is production only).
- The pane's legend gear opens the settings dialog: Draw as, Shows, Columns.
- The ticker's chart-type button switches the main plot between Line and Candle.

## Driving it with control-kiyotaka

### Preconditions

1. The chart must build against a kit that ships `view-catalog.json`: `src/indicators/controls/feed/feed-view.ts` and `src/utility/marketplace/sell-wizard.util.ts` import `@orangecharts/indicator-kit/view-catalog.json`. The run pinned a local tarball in two places only: the root dependency and `packages/wrun-chart-host`'s `devDependencies` entry. Its `peerDependencies` line stays a semver range; a `file:` pin there makes the install fail. Never commit a local pin.
2. A relay that serves the feed. The run used the om rig: recipe `~/Documents/dev-notes/om-byod-any-data/run-artifacts/rig/README.md`, relay on `127.0.0.1:18110`, six public feeds under `@rig` (see verify-om `own-data-streams-and-views.md`). `bin/rig-up`, then `bin/writers start`.
3. Start the lane with the relay in the vite env: `cd <chart worktree> && VITE_LEDGER_API_ENDPOINT=http://127.0.0.1:18110 KIYO_LANE_PORT=<port> KIYO_SESSION=<name> control-kiyotaka up`, with `.env.local` linked for the run and removed after. `ps eww <vite pid>` shows the variable.
4. In each browser session, route `**relay.openmarket.xyz**` to abort before loading the chart. The first feed request must read `GET http://127.0.0.1:18110/api/v2/feeds/rig/watch.<name>/head?chart=guest-workspace 200`. Count `relay.openmarket.xyz` lines in the network log at the end: 0.
5. Turn feeds on for a signed-out browser: set localStorage `kiyo.flag-overrides` to `{"feeds":true}` and reload. The override works on a dev build. A reload keeps it.
6. A signed-out browser reads with `chart=guest-workspace` as its grant, so the feed must be public (`bin/feed-public @rig/watch.<slug>` on the rig). Reads answer `Access-Control-Allow-Origin: *`.

### Store handles the run used

Load once per page with `control-kiyotaka browser eval`:

```js
const P = () => document.querySelector('#app').__vue_app__.config.globalProperties.$pinia;
const S = () => P()._s.get('chart');
```

- Open a feed as the main plot: `S().updateSymbolExchange({symbol: 'feed:rig/watch.price:price', exchange: 'OM'}, 0, undefined, {recordUndo: true})`.
- Set a seconds interval: `S().switchIntervalAndLoad('5s', 0, {recordUndo: true})`. A signed-out viewer who picks 5 seconds from the menu gets `Verify your email to unlock Second Intervals`, so every seconds interval in the run went through this call.
- Add a FEED pane: `S().addIndicator('FEED', {address: '@rig/watch.abc', scope: 'rig', name: 'watch.abc', title, cadence_s, units: '', version: 1, plot: 'line', color: '#8b5cf6', pane: 'lower', column: '', fold: 'time', columns: ['a']}, 0, undefined, undefined, undefined, {recordUndo: false, enforceIndicatorLimit: false})`. This is the feed picker's own call; the guest walls and the production-only feed search leave no other way in.
- Read what is drawn: `window.tc[0].metadata.find(m => m.id === 'main').rawData` (rows `[t_ms, open, high, low, close, volume]`) and `window.tc[0].metadata.find(m => /FEED/.test(m.id))` (`rawData`, `subsetRange`, `settings.plot`, `settings.fold`, `settings.columns`, `legends`). Rows mounted with `subsetRange` `[0,0]` are not drawn; open the frame.

Every Draw as, Shows, Columns and Undo in the run went through the dialog and the footer Undo. Chart types went through `tb-chart-type-trigger-btn` then `tb-chart-type-option-<type>-btn`, clicked through the DOM because a canvas covered the click point.

### Candles from one value

1. Add a FEED line pane over `@rig/watch.price` (`price`, 1 s). Open its gear, Draw as Candles, Shows `From one value`.
2. At 1 minute: compare each closed candle with `GET …/rig/watch.price/bars?interval_s=60&value=price`. Seen: 48 of 48 equal; the forming candle equalled the fold of the readings so far in 72 of 72 states, with 0 remounts; a new candle held 0.53 s after the minute.
3. At 5 seconds: 587 of 587 closed, 45 of 45 forming states.
4. At 1 second: every candle is a flat dash, one per reading. The Shows tooltip says so.

### Candles from your own OHLC columns

1. Add a FEED pane over `@rig/watch.index` (open, high, low, close, volume, one row a minute). Draw as Candles. Shows defaults to `From open, high, low and close`; the pickers pre-fill 5 of 5.
2. At 1 minute the chart reads rows (`…/rows?from=…&to=…&limit=5000`): 221 of 221 candles equal their row.
3. Switch to 5 minutes with the interval menu. The network log must show one bars read per column, each naming it: `bars?interval_s=300&…&value=open`, `value=high`, `value=low`, `value=close`, `value=volume`. A read with no `value=` draws the first column for every role; that was the bug fixed after goal 10b.
4. Compare by role, from the per-column bars `[t, open, high, low, close, count, combined]`: candle open = the open column's bar open; high = the high column's bar high; low = the low column's bar low; close = the close column's bar close; volume = the volume column's `combined` (its sum). Cross-check with the rows: first open, max high, min low, last close of the minutes in the bucket. Seen: 45 of 45 both ways. Worked: 10:30 volume 948+997+634+289+824 = 3692.
5. As the main plot: `updateSymbolExchange` to `feed:rig/watch.index` (no column), then Candle. Seen: 231 of 231 at 1 minute and 47 of 47 at 5 minutes, volume included. For the price feed, `feed:rig/watch.price:price` lands on Line; Candle then drew 57 of 57 at 1 minute and 12 of 12 at 5 minutes.
6. Add RSI and EMA (`addWrunRegistryPackage`, the `@om-core/rsi` and `@om-core/ema` packages). Their stamps equal the candle stamps (for example 59/59 and 65/65), and RSI moves on a new row.
7. Candle held through Line and back, 1m and back to 5m, a pane added and removed, and a feed-to-feed switch. A signed-out reload opens a fresh default workspace, so it cannot show the choice surviving.

### Every shape on one chart

Add 15 views over `@rig/watch.abc` (a, b, c at 1 s) and `@rig/watch.hourly`, one per shape and fold: lines `time` a b c; area, step, markers `time` one column; histogram `time` one column; bars, pie, tiles, card `latest` a b c; meter `latest` a; heatmap `grid` a b c; heatmap `calendar` on `load` with `window: {kind: 'last', count: 600}`; scatter `pair` a b; histogram `bins` a; table `rows` with `window: {kind: 'last', count: 20}`. Seen at 1440×2800: 15 of 15 drew, 14 of 15 changed within 30 s (pixel diff per pane), and the calendar changed when its hourly row landed. Changing Lines to Histogram keeps `a`, says `This shape draws one column`, and greys b and c. The table lists newest rows first.

### The legend row across shape changes

For six changes in the dialog's Draw as (heatmap to meter, pie to card, card to line, line to pie, table to meter, meter to heatmap), each followed by the footer Undo: count the visible legend rows with a settings button and click the gear. Seen: 12 of 12 states had exactly one row, and 12 of 12 reopened the dialog on the view's kind. The log format is in `run-artifacts/final5/legend-row-switches.txt`.

### Silences and interval switches

1. Main `feed:rig/watch.price:price` at 1s plus a FEED line pane over the same feed. Kill the price writer by pid (not `bin/writers stop`, which leaves the bun writer running), wait 40 s, start it again.
2. Seen: 39 empty 1 s rows at the same stamps in main and pane; both lines break and keep their spacing. In goal 6f a 240 s silence drew one gap with no stroke.
3. Cycle 1s, 5s, 15s, 30s, 1m, 1s three times with `switchIntervalAndLoad`. Seen: 15 of 15 drew main and pane to their newest row.

### Two-browser latency

1. Two signed-out sessions on the same feed chart, both tabs visible.
2. Push with the rig's `bin/push-1hz <watch> <seconds>`: one row a second, value = stamp mod 1e6, `sent_ms` per post in `logs/push-*.jsonl`.
3. In each page, a 25 ms recorder reads the overlay's `rawData` and stamps `Date.now()` the first time a row holds its pushed value and its index is inside the drawn range. Same machine, same clock.
4. Seen in goal 12: push to drawn p95 325 ms and 325 ms, p50 298 and 299 ms, max 349 and 350 ms, 0 of 180 missing, at load 8.2 to 12.1 on 10 cores. A 60-row batch drew 50 and 52 ms after its POST, with no reload.
5. Earlier: p95 328 to 341 ms at load 14.9 to 19.6 (goal 6f); p95 782 and 732 ms at load 20 to 27 with another session's typecheck running (goal 10b), where relay-stored to drawn was p95 26 ms. The bound is the om lane's 250 ms wake gather and the machine's load, not the chart.

## Gotchas

- Known defects, not verified-good:
  - an hourly feed at one month opens with its data off the left edge, later months empty;
  - RSI and EMA draw straight across a silence while the price line breaks;
  - Line on an OHLCV feed target with no column draws the `open` column, not the close;
  - a feed main plot opened while its feed is silent reads the feed's head every 10 s for good, in every viewer, after live readings arrive on the stream (cause not proven); a feed opened while live makes no head reads;
  - pie slices have no labels;
  - tiles show plus signs and capital labels ("+93", A, B, C);
  - the table and the heatmap axis show raw ISO times;
  - also seen: a card covers the line's live end and its title reads `Card … ok`; a feed main plot opened with few rows keeps a tiny window until Reset chart; a FEED pane's legend can trail its newest reading by one; the ticker price trails by up to a second, as on market charts.
- Unverified:
  - a candle choice surviving a reload of a saved chart, a second tab or a share-link viewer (needs a signed-in session);
  - an agent-built chart document rendering in the chart (`chart_indicator_add` from om, then the chart reading collab's document; needs collab deployed);
  - production behaviour: nothing is deployed, the relay change is held for review, and the production stream switch is off;
  - the fourth live agent turn after its om fix (one-column candles from chat): only om's free journey has run it.
- 5s, 15s and 30s are Plus-only for a signed-in account; a signed-out viewer meets the verify-email wall. A store add can exceed the guest's 3-indicator cap and raise `Plus workspace · locked`; remove the extra view.
- `browser press Escape` once left a tab `hidden`; read `document.visibilityState` before a frame.
- The rig and its helper scripts (`scratchpad/chart-verify/12/`) live in a session scratchpad that a reboot clears. The rig's script copy is in `run-artifacts/rig/scripts/`.
- The older guest-lane FEED recipe against production feeds (a `fetch` rewrite of `chart=`, head polled every 10 s) is in `indicators.md`; it predates this branch.
