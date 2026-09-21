# The ops dashboard

The daemon serves a React SPA at `/`. It is the read-leaning window onto daemon
state: a header pill with tick freshness and fire count, a left nav, and one
page per concern — Overview, Watches, News, Strategies, Channels, Venues,
Receipts, plus a link out to OM Chat. A fresh install sees an onboarding
checklist on Overview instead of an empty dashboard.

## Sub-features

- `dash-nav` moves between pages and writes a real path (`/alerts`, `/venues`).
  The nav LABEL and the route can disagree: `Watches` lives at `/alerts`.
- `dash-overview` shows daemon health and, on a fresh home, the onboarding
  wizard.
- `dash-watches` lists metric alerts and event watches in one table with status
  and last-fired, under the nav label `Watches` at `/alerts`.
- `dash-tables` renders News, Strategies, Channels, Venues and Receipts from
  their own RPC families.
- `dash-strategy-detail` opens one strategy at `/strategies/<id-or-slug>` from a
  slug link on `/strategies` (added since v0.329).
- `dash-header` shows tick freshness and today's fire count.
- `dash-restart` restarts the daemon it is pointed at.

## How to get to it (user POV)

- Run `om dashboard`, which prints the URL and opens a browser.
- Or open the daemon's bind address directly.

## Driving it with control-om

Preconditions:

- `control-om doctor` reports `dashboard dist present`. Without the bundle the
  daemon does not boot at all, so a missing SPA is never the symptom you see.
- A browser session of your own: `export AGENT_BROWSER_SESSION=verify-om-<run>`
  and `agent-browser set viewport 1440 900`.

- **Open the root.** Run `agent-browser open "$(control-om url /)"` then
  `agent-browser snapshot -i -c`. A fresh lane shows heading `Overview`
  (level 1 and level 2), the nav links `Overview`, `Alerts`, `News`,
  `Strategies`, `Channels`, `Venues`, `Receipts`, `OM Chat` — note `Watches`,
  renamed from `Alerts` since v0.329 — a `restart` button, and the onboarding
  block: heading `Welcome to OpenMarket`, button
  `Dismiss welcome`, heading `Pair a notification channel`, buttons `copy`,
  `Discord`, `More setup options ▸`.
- **Navigate by name.** Run
  `agent-browser find role link click --name "Watches"`, then
  `agent-browser get url` → `http://127.0.0.1:18101/alerts`. The label was
  renamed and the route was not, so drive by the label and assert the path. The
  route is a real path, not a hash, so the URL is assertable evidence on its own.
- **Read a table.** Run `agent-browser snapshot -c` on `/alerts`. The table's
  column headers are `LABEL`, `SOURCES`, `GOAL`, `STATUS`, `LAST FIRED`,
  `ACTIONS` (`KIND` and `RULE` were replaced by `SOURCES` and `GOAL` since
  v0.329), and a watch created on this lane appears as a row whose SOURCES cell
  is a count and whose STATUS reads `working` once it has fired. The old KIND
  column's information did not move to another column — the metric-alert vs
  event-watch distinction is now a `title` tooltip on the SOURCES cell, so it
  is not in an accessibility snapshot at all.
- **The strategy detail route.** `/strategies/<id-or-slug>` is a real route
  (`apps/dashboard/src/app.tsx:58`), reached by clicking a slug on
  `/strategies`. On a guest lane there are no strategies to click, so drive it
  directly: `agent-browser open "$(control-om url /strategies/does-not-exist)"`
  renders the shell with `main` holding only a `Back to Strategies` link, and
  the H1 falls back to `OpenMarket` because the page-name map has no entry for
  the parameterised path. The populated page (signal state, fills, chart,
  transitions timeline, per-strategy digest) is `verified-unreachable` from a
  guest lane: it needs a strategy, which needs a signal and a paired venue.
  Report it that way rather than as empty.
- **Walk the rest.** `/news` (headings `Daily brief`, `Recent fires`),
  `/strategies` (heading `Strategy digest`, columns `SLUG`, `SIGNAL (KIND)`),
  `/channels`, `/venues`, `/receipts` (columns `TIME`, `ALERT`, `VENUE`). Each
  renders its heading and its empty state on a fresh lane.
- **Prove a cross-surface change.** Create or fire something through the CLI,
  then reload the page and assert the row. The dashboard polls every 3s, so a
  reload is not required, but a reload makes the evidence unambiguous.
- **Proof.** Capture the pair per page you are claiming:
  `agent-browser snapshot -c` into `<page>.aria.txt` and
  `agent-browser screenshot <page>.png`. Both must show the nav and the page
  heading so the frame identifies itself.

## Gotchas

- **Do not click `restart` unless restarting the lane is the point.** It
  restarts whatever daemon the page is pointed at.
- The header pill tracks TICK AGE, not health. A lane that just ticked reads
  `live · tick 22s ago`; the same idle lane a minute later reads
  `stale · tick 1m ago`. Both are normal — an idle lane has nothing to evaluate,
  so it does not tick on the interval. `/healthz` `last_tick_at` says the same
  thing without the colour.
- The SPA is bundled into the daemon at module load from
  `apps/dashboard/dist/assets/app.js`. Editing `apps/dashboard/src` changes
  nothing a lane serves until `bun run build:dashboard` runs — and
  `bun run dashboard:stubs` writes *stub* assets, which boot the daemon and
  render nothing useful. Check which of the two you have before reporting a
  blank page.
- For UI iteration the dashboard has its own Vite dev server
  (`cd apps/dashboard && bun run dev`) that proxies `/rpc/*`, `/healthz` and
  `/events/v1` to `127.0.0.1:31337` — the **operator's** daemon, by default. It
  is not a lane and this skill does not drive it.
- `apps/dashboard/src/strategy-plane-absent.ts` and its server-side siblings
  (`openapi-strategy-absent.ts`, `rpc/registry-strategy-absent.ts`) are a
  BUILD-TIME swap for the separate Apache-2.0 OSS export, performed by
  `release/export-manifest.ts`, mirroring the existing `rooms-gui`/`-absent`
  pattern. No lane `control-om` drives ever uses them: Strategies stays an
  unconditional nav item and route pair. Do not read those filenames as a
  runtime toggle.
- Nav items are `link` role, not `button`. `find role button --name "Watches"`
  finds nothing — and neither does `find role link --name "Alerts"`, which is
  the failure a stale recipe hits first.
- The whole shell reports as one `generic ... clickable [onclick]` node whose
  accessible name is every nav label run together. Scope snapshots or read the
  children; do not assert on that blob.
