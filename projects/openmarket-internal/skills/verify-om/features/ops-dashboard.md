# The ops dashboard

*Verified: 2026-10-07, tree `03bd55226` (v0.432.0) — all eight workspace navigation routes and strategy not-found detail opened; onboarding captured with screenshots and accessibility snapshots. Non-empty strategy and receipt rows remain unverified.*

The daemon serves a React SPA at `/`. It **used** to be a read-leaning window
onto daemon state; since v0.400.0 it also authors watches and embeds an agent
chat, each documented in its own entry ([watch authoring](./watch-authoring-ui.md),
[the agent panel](./agent-panel.md)). What remains here is the shell and the
observation surfaces: a daemon status pill, a left nav, and one page per concern
— Overview, Watches, News, Strategies, Channels, Connections, Venues and
Receipts, plus a link out to OM Chat. Overview shows watch counts and fires; a
fresh install also sees an onboarding checklist.

## Sub-features

- `dash-nav` moves between pages and writes a real path (`/alerts`, `/venues`).
  The nav LABEL and the route can disagree: `Watches` lives at `/alerts`.
- `dash-overview` shows daemon health and, on a fresh home, the onboarding
  wizard.
- `dash-watches` lists metric alerts and event watches in one selectable list with
  status and last-update time, under the nav label `Watches` at `/alerts`.
- `dash-tables` renders News, Strategies, Channels, Venues and Receipts from
  their own RPC families.
- `dash-strategy-detail` opens one strategy at `/strategies/<id-or-slug>` from a
  slug link on `/strategies` (added since v0.329).
- `dash-header` reports daemon/check status and when it was last checked. The
  Overview's `Watch fires` metric shows fires since the daemon started.
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
  `agent-browser snapshot -i -c`. A fresh lane shows heading `Your market, in
  view.` and the nav links `Overview`, `Watches`, `News`,
  `Strategies`, `Channels`, `Connections`, `Venues`, `Receipts`,
  `OM Chat (opens in a new tab)` — note `Watches`, renamed from `Alerts`, and
  `Connections`, added in v0.400.0 — inside a `navigation "Main navigation"`
  landmark. Beside them a `Switch to light mode` theme toggle and an
  `Ask your agent` button.

  The Overview page itself was redesigned in v0.400.0 and no longer matches its
  old description. Its H1 is the headline `Your market, in view.`, NOT
  `Overview`; the level-2 page heading is gone; the restart control is
  `Restart daemon` inside a `region "Workspace"`; there is a
  `region "Watch activity"` with a `See all` link; and the onboarding block now
  reads `Welcome to OpenMarket` / `Dismiss welcome` / `Create your first watch`
  with a `Create a watch` link and `More setup options ▸`. The old
  `Pair a notification channel` step is gone: the channel step is renamed
  `Choose where updates arrive` and is now OPTIONAL, the only required step
  being `Create your first watch`. The collapsed view also has `More setup
  options ▸`; expanding it reveals optional `Connect a coding agent` and
  `Connect a trading venue` steps. The channel step offers a plain `Manage
  channels` link. A `copy` button still appears when a terminal or agent setup
  step is active; do not claim it is absent everywhere. The block is also
  state-dependent: it disappears once the home has a watch, so capture it on a
  genuinely fresh lane or not at all. On the fresh guest lane, the onboarding
  block showed `Welcome to OpenMarket`, `Dismiss welcome`, `Create your first
  watch`, and `More setup options ▸`.
- **Navigate by name.** Run
  `agent-browser find role link click --name "Watches"`, then
  `agent-browser get url` → `http://127.0.0.1:18101/alerts`. The label was
  renamed and the route was not, so drive by the label and assert the path. The
  route is a real path, not a hash, so the URL is assertable evidence on its own.
- **Read the list — there is no table any more.** v0.400.0 replaced the
  `/alerts` table with a selectable list, so every column assertion older than
  that is dead: there are no `columnheader` nodes at all. Run
  `agent-browser snapshot -c` on `/alerts` and assert the `region "Watches"`,
  which holds a `checkbox "Select visible watches"`, a `StaticText "N watch(es)"`,
  the line `Open a watch to manage its sources and steps`, and one `listitem`
  per watch carrying `checkbox "Select <label>"`, `link "<label>"`, the source
  count and goal as loose `StaticText`, a `time`, the status word, and a single
  action button reading `Pause` or `Resume` **according to the watch's state** —
  which makes that button the cleanest assertion on the page.
- **The page gained controls above the list**: a `Create watch` button (see
  [watch authoring](./watch-authoring-ui.md)), a
  `navigation "Filter watches by status"` holding `All watches N` / `Enabled N` /
  `Paused N` / `Needs attention N`, a `searchbox "Search watches"`, and a
  `combobox "Folder"` defaulting to `All folders`.
- **The strategy detail route.** `/strategies/<id-or-slug>` is a real route
  (`apps/dashboard/src/app.tsx:58`), reached by clicking a slug on
  `/strategies`. On a guest lane there are no strategies to click, so drive it
  directly: `agent-browser open "$(control-om url /strategies/does-not-exist)"`
  renders the shell with `main` holding only a `Back to Strategies` link, and
  the H1 fallback moved in v0.400.0 — source gives `Strategy details` for
  `/strategies/<id>` and `Watch details` for the new `/alerts/<id>` — and driven
  at v0.400.0 the 404 branch rendered little beyond the shell, inconsistently
  between two reads. Do not pin a heading here; assert the `Back to Strategies`
  link, which is stable. The populated page (signal state, fills, chart,
  transitions timeline, per-strategy digest) is `verified-unreachable` from a
  guest lane: it needs a strategy, which needs a signal and a paired venue.
  Report it that way rather than as empty.
- **Walk the other workspace routes.** `/news` (headings `Daily brief`, `Recent fires`, and
  `Watches`), `/strategies` (heading `Strategy digest`), `/channels`, `/venues`,
  and `/receipts`. Each renders its heading and guest-lane empty state. When
  populated, Receipts also shows `OID`, `Notional`, and `Status` alongside
  `Time`, `Alert`, and `Venue`.
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
- The header pill reports daemon/check state (the fresh lane read `Live · Last
  checked 39s ago`). Fire count is the Overview's separate `Watch fires`
  metric, not part of the pill.
- The header can read `Needs attention` when strategy health reports unmanaged
  exits; it is an additional status branch, not a generic watch status.
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
- The strategy OSS-export swap was renamed in v0.400.0: the empty variant is now
  plain `apps/dashboard/src/strategy-plane.ts` and the real one
  `strategy-plane-full.tsx`, so the old `strategy-plane-absent.ts` no longer
  exists under that name. It and its server-side siblings
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
