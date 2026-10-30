# The ops dashboard

*Re-driven 2026-10-31 (nightly), tree `dfefe0a21` (origin/main, v0.480.2), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 1.6, on a bundle built from this tree (`apps/dashboard/src` unchanged since `3cb50a821`). Every route rendered its H1: `/` (`Your market, in view.`, `Restart daemon`, `region "Watch activity"`), `/alerts` (`Watches`: `Create watch`, `Select visible watches`, one `checkbox "Select <slug>"` and `Pause` per watch, `searchbox "Search watches"`, `combobox "Folder"`), `/alerts/lane-probe` (H1 is the label; `Edit watch`; `Setup`/`History`/`Delivery`/`Settings`; sections `Sources and schedules`, `Connected steps`, `Choose how you hear about updates`), `/news`, `/strategies` (Paper tab: the paragraph, `ACCOUNT`…`REALIZED P&L` plus a second table's `TIME`/`WATCH`/`OUTCOME`/`PRICE`/`REASON` headers, row `verify-book`), `/channels`, `/connections` (`AI model`, `Coding agents`), `/venues`, `/receipts` (`No receipts in the last 24 hours.`), `/agent` (`Conversations`, `What can I help with?`). `/strategies/does-not-exist` flickered again: the 404 text at 3 and 6 s, `Loading…` at 9 and 12 s, the 404 text at 15 s. Clicking the `Watches` link landed on `/alerts`. Evidence: `http://127.0.0.1:8098/vom-nightly-20261031/r1/` (`dash-*.aria.txt`, `dash-*.png`).*

*Re-driven 2026-10-30 (scheduled maintenance), tree `3cb50a821` (origin/main, v0.478.0), fresh lane on 18165, host load average about 140. Every route rendered its H1 on the 2026-10-27 dashboard bundle (the source is unchanged since): `/` ("Your market, in view."), `/alerts`, `/alerts/maint-1030`, `/agent`, `/news`, `/strategies`, `/channels`, `/connections`, `/venues`, `/receipts`. `/strategies/does-not-exist` read `Loading…` at 3 s, the flicker gap. The Overview **Watch fires** tile read 0 after two inbound fires. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261030/r1/` (frames 20-30).*
*Re-driven 2026-10-30 (nightly, smoke depth), tree `3cb50a821` (origin/main, v0.478.0), lane on 18163, with a full `bun run build:dashboard` bundle (692,671 bytes). The nav listed Overview, Watches, News, Strategies, Channels, Connections, Venues, Receipts and `OM Chat (opens in a new tab)`. The H1s were `Your market, in view.`, `Watches` (with `Create watch` and the status filters `All watches 1`, `Enabled 1`, `Paused 0` and `Needs attention 0`), `News`, `Strategies` and `Strategy digest`, `Channels`, `Connections`, `Venues` and `Receipts`. `/alerts/probe-1030` read `working`. On a loaded host `/strategies` was blank for the first 6 s and rendered at 20 s. Not re-driven: the onboarding card, the `/strategies/<unknown>` flicker and the Overview tiles. Evidence is local only (the `8098` renderer did not answer): `artifacts/vom-nightly-20261030/r1/`.*

*Re-driven 2026-10-29 (scheduled maintenance, smoke depth), tree `7ec575e55` (origin/main, v0.467.0 plus #2194), fresh lane on 18161, with one inbound watch. `/` (**Your market, in view.**), `/alerts` (**Watches**), `/alerts/lane-probe`, `/agent`, `/news`, `/strategies`, `/channels`, `/connections`, `/venues` and `/receipts` rendered their headings with no page errors. After one inbound fire, the Overview's `Watch fires` tile still read `0`, with `/healthz` `alerts_fired_total: 0` (the known product gap). `/strategies/does-not-exist` rendered only the shell (217 characters, no heading). Evidence: `http://127.0.0.1:8098/verify-om-maint-20261029/r1/`.*

*Re-driven 2026-10-29 (nightly, smoke depth), tree `32ca0d6c7` (origin/main, v0.467.0), lane on 18103 with one watch: `/`, `/alerts`, `/alerts/probe-1029`, `/agent`, `/news`, `/strategies` (and its Paper tab), `/channels`, `/connections` (read only), `/venues` and `/receipts` rendered their headings and empty states. The Overview's `Watch fires` tile read `0 Since the daemon started` after two inbound fires. It reads `/healthz` `alerts_fired_total`, which counts condition fires only (product gap in the README). `/strategies/<unknown>` was not re-sampled. Evidence: `http://127.0.0.1:8098/vom-nightly-20261029/r1/`.*

*Re-driven 2026-10-28 (scheduled maintenance, smoke depth), tree `186030b63` (origin/main): `/`, `/alerts`, `/alerts/<slug>`, `/agent`, `/connections`, `/channels`, `/news`, `/paper` (shell only), `/receipts`, `/strategies`, `/strategies/does-not-exist` and `/venues` all rendered with no error text. Steps not named here keep the record below. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261028/r1/`.*

*Verified: 2026-10-28, tree `a8fa10974` (origin/main, v0.466.0), fresh lane on 18104. The Overview showed `Your market, in view.`, the onboarding block (`Welcome to OpenMarket`, `Dismiss welcome`, `Create your first watch`, `More setup options ▸`), `Watch activity` with `See all`, `Workspace` with `Restart daemon`, and the nine-link `Main navigation`. `Watches` → `/alerts` showed `Create watch`, the filter chips (`All watches 1`, `Enabled 1`, `Paused 0`, `Needs attention 1`), the search box, `Folder` and a row with `Pause`. The other routes' headings matched: `/news` (columns `AGE`/`HEADLINE`/`WATCH`/`OUTCOME`; `WATCH`/`GOAL`/`STATE`/`LAST ACCEPTED`), `/strategies`, `/channels` (`Connect webhook`), `/venues` and `/receipts` (`No receipts in the last 24 hours.`). `/connections` was read only: Claude Code, Codex and Claude Desktop `Installed, not connected`; Cursor and OpenClaw `Not detected on this machine`. `/strategies/does-not-exist` still flickered, with `Loading…` at 12 s and 24 s over 30 s of 3 s samples, and `money/show` returned 404 `money_not_found`. `apps/dashboard/src` is unchanged since `8fe6a8432`. Previous stamp `8fe6a8432` is an ancestor (10 commits).*

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
  (`apps/dashboard/src/strategy-plane-full.tsx:27`; `app.tsx:99` spreads
  `{strategyRoutes}`), reached by clicking a slug on
  `/strategies`. On a guest lane there are no strategies to click, so drive it
  directly: `agent-browser open "$(control-om url /strategies/does-not-exist)"`
  renders the shell with `main` holding only a `Back to Strategies` link, and
  the H1 fallback moved in v0.400.0 — source gives `Strategy details` for
  `/strategies/<id>` and `Watch details` for the new `/alerts/<id>` — and driven
  at v0.400.0 the 404 branch rendered little beyond the shell, inconsistently
  between two reads. Do not pin a heading here; assert the `Back to Strategies`
  link. **The page does not settle: it flickers.** Driven at `ee8e3a7ab` and
  read every 3 s, `main` showed `No strategy named does-not-exist. Back to
  Strategies.` at 3, 6 and 9 s, `Loading…` at 12 s, the 404 text at 15 to 21 s,
  and `Loading…` again at 25 s. The ~12 s cadence looks like a refetch
  clearing the error state, but the cause is not isolated. The README's product-gap entry has a source hypothesis: a 3 s poll plus `retry: 1` resetting a no-data query to pending. `POST
  /rpc/v1/money/show` answers 404 `money_not_found` every time. The cycle
  explains 2026-10-23's slow `Loading…`, but not 2026-10-22's `Unavailable.`
  (a third branch, not seen since), with `apps/dashboard/src` unchanged across
  all three trees. Sample the text several times over 30 s and assert
  that the 404 text appears. A single read proves nothing. The flicker is a
  product gap (README). The populated page (signal state, fills, chart,
  transitions timeline, per-strategy digest) is `verified-unreachable` from a
  guest lane: it needs a strategy, which needs a signal and a paired venue.
  Report it that way rather than as empty.
- **Walk the other workspace routes.** `/news` (headings `Daily brief`, `Recent fires`, and
  `Watches`), `/strategies` (heading `Strategy digest`), `/channels`, `/venues`,
  and `/receipts`. Each renders its heading and guest-lane empty state. When
  populated, Receipts also shows `OID`, `Notional`, and `Status` alongside
  `Time`, `Alert`, and `Venue`. Driven at `42d044b02`: `/news` Recent fires has
  columns `AGE`, `HEADLINE`, `WATCH`, `OUTCOME` and its Watches table `WATCH`,
  `GOAL`, `STATE`, `LAST ACCEPTED`; `/channels` offers `Connect webhook`;
  `/receipts` reads `No receipts in the last 24 hours.`
- **Connections.** `/connections` (H1 `Connections`) has `heading "AI model"`,
  reading `not connected` on a guest, with a `Connect your first AI provider`
  disclosure, and `heading "Coding agents"` ("Optional. Connect an installed app
  to give it OpenMarket tools and skills."). Each agent row (Claude Code, Codex,
  Cursor, Claude Desktop, OpenClaw) reads `Installed, not connected` with a
  `Connect` button, or `Not detected on this machine` with a disabled one.
  **Never press `Connect` from a lane.** The rows reflect the REAL machine's
  installed apps. `POST /rpc/v1/integrations/connect` runs the CLI's own
  wiring path for that client (`runner/http/integrations-api.ts`), so a press
  from a lane would rewire the operator's real Claude Code or Codex to the
  lane, and that change outlives it. Driven read-only at `42d044b02`.
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
- A plan-usage pill can appear beside daemon status when a signed-in plan nears
  its hold threshold. A fresh guest lane has no plan pressure, so the pill stays
  absent.
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
- **`/paper` is not a route in any lane build, and a link points at it anyway.**
  The standalone Paper page, its nav entry and its route live in
  `apps/dashboard/src/paper-plane.tsx` and mount only when
  `strategyRoutes === null` — the OSS export, where the strategy plane is
  swapped for its empty twin. This build imports `strategy-plane-full`, so the
  condition is never true. Driven: `/paper?account=<id>` renders the shell with
  an EMPTY `main` — no content, no 404 message. The "paper book" link on a
  strategy detail page points there unconditionally
  (`pages/strategy-detail.tsx`), so it dead-ends on a blank page. Reported to
  the operator as a product gap; reach Paper through the `/strategies` tab.
- Nav items are `link` role, not `button`. `find role button --name "Watches"`
  finds nothing — and neither does `find role link --name "Alerts"`, which is
  the failure a stale recipe hits first.
- The whole shell reports as one `generic ... clickable [onclick]` node whose
  accessible name is every nav label run together. Scope snapshots or read the
  children; do not assert on that blob.
