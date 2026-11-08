# kiyotaka-frontend verification map

The maintained source for verifying user-facing chart behavior. Read this index
before driving, then use the matching feature file as the recipe.

Maintenance pass: 2026-11-09 (nightly). Source read AND live drive on the same
tree, `origin/main` `32dd0c6354` (60 commits past the 2026-11-08 tree
`943281a2eb`). Lane `18103` in a detached worktree with the operator's
`.env.local` linked in and a fresh `pnpm install` (10 s), a guest-JWT lane
(`isGuest` true) driven through the hub's tracked `bin/control-kiyotaka`; load
3 at the start and 13 at `doctor`, the gateway on the system resolver (no
browser map). `doctor` passed three times. Driven: the main guest path of every
guide (the watchlist, editor and voice ones to their walls or absence), plus what
changed: the search rail (`Stocks`, `Futures`, `Predictions`, the new Exchanges
section), the renamed strip and placeholder, the Lite charts switch, chip and
auto-on notice, the settings nav's new Performance page, Order Book Profile's
`Grouping mode`, the settings search's three `Escape` steps, the heatmap
popover's pills, a trend line across an interval switch and Full chart's exit.
Product gaps: the bare ticker row still opens a Binance option (`BINANCE.O BTC/USDT
25 Dec 2026 80,000 Put`), and on a cold boot the Lite charts notice can read raw
keys. Evidence (local, `evidence check` passed):
`~/dev-notes-artifacts/maintain-verification-skill/run-artifacts/vk-nightly-20261109/r1/`.

Previous pass: 2026-11-08 (nightly). Source read AND live drive on the same
tree, `origin/main` `943281a2eb` (59 commits past the 2026-11-07 tree
`dced88e06a`). Lane `18103` in a detached worktree with the operator's
`.env.local` linked in and a fresh `pnpm install` (11 s), a guest-JWT lane
(`isGuest` true) driven through the hub's tracked `bin/control-kiyotaka`;
load 3 at the start and 13 on 10 cores at `doctor`. **The gateway name
resolved through the system resolver again** (`10.1.1.10`), so `doctor`
passed twice with no browser map. Driven: the main guest path of every
guide (the watchlist, editor and voice ones to their walls or absence), plus
what changed: the stock legend's feed chip, now one control reading
`Trades` (no timing span or `Live ›` without the stocks gate) with its menu;
the heatmap popover's kind pills and their wall; Open Interest's new `Plot
type` (Candles to Line) through the new ComboBox; the drawing card's
ComboBoxes; and the footer's timezone offsets. Product gap: the bare ticker
row still opens a Binance option, now seen on `BTCUSDT` (`BINANCE.O BTC/USDT
27 Nov 2026 77,000 Put`; `ETHUSDT` listed no bare row). Evidence (local,
`evidence check` passed):
`~/dev-notes-artifacts/maintain-verification-skill/run-artifacts/vk-nightly-20261108/r1/`.

Previous pass: 2026-11-07 (nightly). Source read AND live drive on the same
tree, `origin/main` `dced88e06a` (81 commits past the 2026-11-06 tree
`8bcd72f8f5`). Lane `18103` in a detached worktree with the operator's
`.env.local` linked in and a fresh `pnpm install` (9 s), a guest-JWT lane
(`gateway-v3` `false`, `us-equities-full` `true`) driven through the hub's
tracked `bin/control-kiyotaka`; load 13 on 10 cores at `doctor`. **Both
resolvers answered NXDOMAIN for the gateway name again**; `10.1.1.10` answered
`400` three times in three, and with `KIYO_BROWSER_ARGS` mapping the name
there `doctor` passed on its first run and the lane drew live candles all
pass. Driven: the main guest path of every guide (the watchlist and voice
ones to their walls), plus what changed: the new NinjaTrader Super Search row
is absent for a guest, the symbol dialog shows no `Yours` tab on a pane with
no om series, the Orderbook's DOM ladder and the crypto Tape carry no delay
notice, POLYGON AAPL wears no `Delayed` label on this lane, and the Panels
menu marks the open Tape with a `tb-panels-row-tape-on` node. The tab drifted
hidden four times; a `back` strip stayed up while hidden (see the boot
guide). Product gap: the bare `ETHUSDT · Crypto` row still opens a Binance
option, now a call (`ETH-261109-2275-C`). Evidence (local, `evidence check`
passed):
`~/dev-notes-artifacts/maintain-verification-skill/run-artifacts/vk-nightly-20261107/r1/`.

Previous pass: 2026-11-06 (nightly). Source read AND live drive on the same
tree, `origin/main` `8bcd72f8f5` (119 commits past the 2026-11-05 tree
`87a325f4ab`). Lane `18103` in a detached worktree with the operator's
`.env.local` linked in and a fresh `pnpm install` (10 s), a guest-JWT lane
(`gateway-v3` `false`, `us-equities-full` `true`) driven through the hub's
tracked `bin/control-kiyotaka`; load 3 to 11 on 10 cores. **Both the system
resolver and the tailnet resolver answered NXDOMAIN for the gateway name**;
the last known address `10.1.1.10` still served it, so the pass drove with
`KIYO_BROWSER_ARGS` mapping the name there (see Baseline preconditions).
Driven: the main guest path of every guide (the watchlist and voice ones to
their walls), plus what changed: US stocks opened to guests (one search row
per stock, the bare ticker, no seconds intervals, the stock Tape's chrome
with the stocks gate routed, the `4.53.0` `The US tape.` spotlight from its
Release Notes badge), service notices (banner, pill, list, back to normal)
from an injected notice, the in-place settings search and the Daily session
default on a session volume profile, Super Search's covers and `Drawing
tool` tag, and the strip's `offline` and `back` under the new waits.
**Lane gap: the stock Tape needs the stocks gate, which the operator's
`.env.local` does not route, and with it routed the gate answered nothing for
this guest** (no print, AAPL candles stalled; see Baseline preconditions).
Product gap: the bare `ETHUSDT · Crypto` row still opens a Binance option put
(`ETH-261113-2250-P`). Evidence (local, `evidence check` passed):
`~/dev-notes-artifacts/maintain-verification-skill/run-artifacts/vk-nightly-20261106/r1/`.

Previous pass: 2026-11-05 (nightly). Source read AND live drive on the same
tree, `origin/main` `87a325f4ab` (123 commits past the 2026-11-04 tree
`8436920004`). Lane `18103` in a detached worktree with the operator's
`.env.local` linked in and a fresh `pnpm install`, a guest-JWT lane
(`gateway-v3` read `false`) driven through the hub's tracked
`bin/control-kiyotaka`; load 5 to 16 on 10 cores. **At about 20:33 UTC the
gateway name left the system resolver** and the TCP probe of its address
flapped (one in five failed); the rest of the pass drove with
`KIYO_BROWSER_ARGS` holding the resolver map, after `doctor` passed on its
fifth run (see Baseline preconditions). Driven: the main guest path of every
guide except the watchlist and voice recipes behind their walls, plus what
changed: the desktop connection strip (`offline`, `back`, and `long` with its
Reload when the gateway went), the TPO `Chart session` default and its
city-clock list, the dollar-pair lead for a typed currency and the quick
search's `XAUUSD`, Carbon's translucent volume, the sign-in card's Turnstile
hold on clean traffic, and the clip page's private state after the clip
rewrite. Product gap: the bare `ETHUSDT · Crypto` row still opens a Binance
option put (`ETH-261113-2275-P`). Not driven: a public clip (no id), a capped
store picture (the dev backend serves square covers only), the wake heal.
Evidence (local, `evidence check` passed):
`~/dev-notes-artifacts/maintain-verification-skill/run-artifacts/vk-nightly-20261105/r1/`.

Previous pass: 2026-11-04 (nightly). Source read AND live drive on the same
tree, `origin/main` `8436920004` (80 commits past the 2026-11-03 tree
`215896e614`). Lane `18103` in a detached worktree with the operator's
`.env.local` linked in and a fresh `pnpm install` (10 s), a guest-JWT lane
driven through the hub's tracked `bin/control-kiyotaka`, the gateway name
resolving through the system resolver all pass (no browser map needed). Load 3
at the start, 13 at `doctor`. Driven: the main guest path of every guide
except the voice and watchlist recipes behind their walls, plus what changed:
the rebuilt one-card sign-in sheet and its password pane, the drawing bar's
`tqb-templates-btn` and the one-layer `Escape`, the spot pane's gate on Open
Interest, Funding and Liquidations, the pane merge's guest wall (no Plus
prompt any more), the new 2FA panel behind `?twofa=true`, and the absence of
the connection chip. Product gaps: the bare `ETHUSDT · Crypto` row still
opens a BINANCE.O put; the spot pane's `Needs … data` words never reached the
engine or the page on a guest's programmatic mount (the status layer wrote
`No data in range` and `Slow network` over them; the dialog path is
signed-in only, so this is unconfirmed); the guest `CME` tab read `CME
contracts aren’t loading right now` twice (cause not traced). Evidence
(local, `evidence check` passed):
`~/dev-notes-artifacts/maintain-verification-skill/run-artifacts/vk-nightly-20261104/r1/`.

Previous pass: 2026-11-03 (nightly). Source read AND live drive on the same
tree, `origin/main` `215896e614` (131 commits past the 2026-11-02 tree
`a4488341f6`). Lane `18103` in a detached worktree with the operator's
`.env.local` linked in and a fresh `pnpm install` (9 s), a guest lane that
this time carried a guest JWT (`isGuest` true), driven through the hub's
tracked `bin/control-kiyotaka` (now merged, so the installed skill has its
`bin/`). Load 4 to 12 on 10 cores. **About two minutes after `up` the gateway
name stopped resolving through the system resolver** while the tailnet DNS
still answered it; the page stuck at 1 bar and a re-run of `doctor` read `v2
gateway UNREACHABLE`. A browser launched with a `--host-resolver-rules` map
for that one name drove the whole pass with live data (see Baseline
preconditions). Driven: the main guest path of every guide, but not the wake heal,
the Predict tab, the Preferences page or the input-method guard, plus what
changed: the Indicators dialog's split view and
pane, shorthand search, the legend menu's eight rows and the pin move's wall,
the regrouped chart-type menu, the Tape markets menu's `Follow the chart`
row, the drawing right-click menu, Release Notes' scroll box, and the new
sign-in return flags (`?oauth=true`, `?twofa=true`). Product gaps: the bare
`ETHUSDT · Crypto` row still opens a BINANCE.O put; **`SPY / GLD` charts the
NYSE ETFs again** (closed). Evidence (local, `evidence check` passed):
`~/dev-notes-artifacts/maintain-verification-skill/run-artifacts/vk-nightly-20261103/r1/`.

Previous pass: 2026-11-02 (nightly). Source read AND live drive on the same
tree, `origin/main` `a4488341f6` (90 commits past the 2026-11-01 tree
`120d5d5d32`). A quiet machine (load 2 to 5 on 10 cores): lane `18103` in a
detached worktree with the operator's `.env.local` linked in and a fresh
`pnpm install` (8 s from the shared store), a guest lane with no JWT, driven
through the `control-kiyotaka` from the hub's open wrapper branch (PR #11 is
not merged, so the installed skill still has no `bin/`). Driven: every
guest-reachable sub-feature of the nine guides again on a gateway that
resolved all pass, plus the wake heal (392 s hidden, 5 blank slots to 0, the
full ring chain; it exposed a recipe artifact, see the boot guide), the
rebuilt Tape with its docked Liquidations on ETHUSDT and SOLUSDT, the
Orderbook on both (it mounts only while the tab is visible), the 17-row
Panels menu, the pane move's `indicators` wall, the `liquidations` and `Tape
sounds` palette rows, the Preferences page's `appearance-mode-*` handles, the
magnet's strength memory, and a new guest route, the clip page
(`/chart/clip/<id>`, its private state). Product gaps: the bare `ETHUSDT ·
Crypto` row still opens a BINANCE.O put, and `SPY / GLD` now charts a
BINANCE.F `SPYUSDT` perp over NYSE GLD. Evidence (local, `evidence check`
passed):
`~/dev-notes-artifacts/maintain-verification-skill/run-artifacts/vk-nightly-20261102/r1/`.

Previous pass: 2026-11-01 (nightly). Source read AND live drive on the same
tree, `origin/main` `120d5d5d32` (153 commits past the 2026-10-30 tree
`849fb08e95`; the 2026-10-31 pass was killed before it wrote anything). A quiet
machine (load 3 on 10 cores): lane `18103` in a detached worktree with the
operator's `.env.local` linked in, a guest lane with no JWT, driven through a
regenerated `control-kiyotaka` (now the hub's tracked `bin/control-kiyotaka`;
the old copy hung on an iCloud read). Driven: every guest-reachable sub-feature
of the nine guides again, and for the first time the footer undo and redo
(`tb-undo`), the one-menu rule, the interval menus' testids, the docked
settings card's Float/Dock toggle, the `?wrunRef=` wall, the Explore row's
`workspace` wall, the Gray row's `light-mode` wall, the Preferences page (13
languages), the fib log-scale row, and the absence of every retired kScript
handle. **The v2 gateway name stopped resolving on the machine at about 21:55
UTC**, two hours into the pass (tailnet-only DNS; see Baseline preconditions),
so the wake heal, a SOL Tape and Orderbook re-check and the left-pan floor were
not driven and stay stamped 2026-10-29. Product gaps found: the bare `ETHUSDT ·
Crypto` row still opens a BINANCE.O put, and `SPY / GLD` now charts Solana
tokenized stocks. Evidence (local, `evidence check` passed):
`~/dev-notes-artifacts/maintain-verification-skill/run-artifacts/vk-nightly-20261101/r1/`.

Previous pass: 2026-10-30 (nightly). Source read on `origin/main`
`849fb08e95` (135 commits past the 2026-10-29 tree `78ec9625d9`); the inventory
and the guides carry what that read found, each labelled source. **The live
pass was blocked**: with the machine's load average between 100 and 220 on 10
cores from other sessions, lane `18103` passed `doctor` five times but the
guest page never drew a candle in five boots over two and a half hours (see the
load bullet in Baseline preconditions). Nothing on `849fb08e95` was driven, so
every "last driven" stamp below is still the 2026-10-29 drive on `78ec9625d9`.
Logs (no frames): `~/dev-notes-artifacts/maintain-verification-skill/run-artifacts/vk-nightly-20261030/r1/`.

Previous pass: 2026-10-29 (nightly). Source read and live drive on the same
tree, `origin/main` `78ec9625d9` (56 commits past the 2026-10-28 tree
`29c9cda0a2`). Lane `18103` in a detached worktree with the operator's
`.env.local` linked in, a guest lane with no JWT whose backend proxy is a remote
dev box with a seeded catalog. Driven: every guest-reachable sub-feature of the
nine guides again, the lone-bar wake heal, and the new outcomes a guest can
reach: the Predict tab (Polymarket and HIP-4 behind venue chips, a Polymarket
event charted), the hover quick-search list, the self-explaining indicator
settings rows and the Ask block's hide and show, the Volt theme row, the drawing
colour popover's keep and revert and a cancelled creation, the heatmap and
layout-sync switches, and the input-method guard (the composing `Escape` gap is
fixed). Not driven: anything behind sign-in (no agent credentials), the
Super Search Guides section (the dev backend answers `surface:false`), and
voice, which stays absent on a guest. Evidence (local, `evidence check`
passed): `~/dev-notes-artifacts/maintain-verification-skill/run-artifacts/vk-nightly-20261029/r1/`.

## Baseline preconditions

- Launch the lane on its **assigned** port (`18097`–`18197`), bound to
  `127.0.0.1`: `./control-kiyotaka up`. Never pick a free port, never `8080`.
  `doctor` reporting `lane FOREIGN` means another checkout holds the default
  port — a neighbouring worktree's live lane, not residue. Do not reclaim it:
  take another slot with `KIYO_LANE_PORT`, and set `KIYO_SESSION` too so your
  browser commands cannot drive the neighbour's tab.
  Every later command in the run needs the same two variables exported.
- `./control-kiyotaka doctor` exits zero. The `chart-schema` line must read `ok`,
  or `not-aliased <version> (dev serves node_modules)` when there is no sibling
  `orange-shared` checkout, which is also fine.
- **The lane needs the operator's `.env.local`.** A new worktree has none, and
  the guest boot then gets `Backend error: unauthenticated` from the gateway and
  zero candles while `doctor` stays green. Link it in before `up` (see
  [chart boot](./chart-boot-and-data-plane.md) Gotchas). With it, `doctor`'s
  `backend :3000 DOWN` line is about `:3000` only; the lane talks to whatever
  `VITE_BACKEND_PROXY_TARGET` names.
- **Read `uptime` before you plan a pass. A loaded machine cannot boot a dev
  lane, and nothing in `doctor` says so.** On 2026-10-30, with the load average
  between 100 and 220 on 10 cores from other sessions, every `doctor` passed while the page
  showed `Startup is taking longer than expected` (the chart route never marked
  itself booted, `window.__BOOT_ERRORS__` empty), the guest's
  `POST /api/v1/auth-v2/refresh-token` through the lane took 18 to 50 s against
  the app's 15 s timeout (`[refresh-token] all retries exhausted`), the data
  worker died with an empty `Error initializing worker:` and parked, and
  `agent-browser` wedged with `os error 35` three times. The same request
  straight to the backend took under 2 s. Exporting the backend's IP as
  `VITE_BACKEND_PROXY_TARGET` before `up` (the process env overrides
  `.env.local`) cut the lane's proxy time to under 4 s, because Node's own
  lookup of the tailnet hostname took about 4 s under that load, but the boot
  still stalled. When the load average is far above the core count, report the
  pass blocked rather than reading those failures as product regressions.
- **When the gateway name stops resolving through the system resolver, map it
  in the browser (driven 2026-11-03).** That day `nc` and `curl` failed with
  `nodename nor servname provided` for `tsdb-gateway.int.ore.kiyotaka.ai`
  while `nslookup tsdb-gateway.int.ore.kiyotaka.ai 100.100.100.100` answered
  `10.1.1.10` and `curl --resolve …:443:10.1.1.10` got `302`. Close the
  session's browser and drive every browser command of the run through
  `agent-browser --session "$KIYO_SESSION" --args
  "--use-angle=swiftshader,--enable-unsafe-swiftshader,--host-resolver-rules=MAP
  tsdb-gateway.int.ore.kiyotaka.ai <address>"`, with the address read from the
  tailnet resolver that day. Re-set the viewport after the relaunch. The
  lane's own `/api` proxy did not need the name.
  **Since the wrapper reads `KIYO_BROWSER_ARGS` this is one export (driven
  2026-11-05).** `doctor` prints the fix itself when the system resolver has
  lost the name and the tailnet resolver answers: export
  `KIYO_BROWSER_ARGS='--host-resolver-rules=MAP
  tsdb-gateway.int.ore.kiyotaka.ai <address>'`, run `agent-browser close
  --session "$KIYO_SESSION"`, and every `control-kiyotaka browser …` then
  launches with the map; `doctor` reads `reachable at <address> through the
  browser's KIYO_BROWSER_ARGS map`. Its probe is one TCP connect: on
  2026-11-05 the address answered about four connects in five, and `doctor`
  failed four runs in a row over eight minutes (three of them reading
  `UNREACHABLE (system resolver and tailnet resolver …)`, two of those with
  the map already set) before passing on the fifth. Re-run it before calling
  the lane down.
  **When the tailnet resolver has lost the name too, try the last known
  address (driven 2026-11-06).** That day `nslookup
  tsdb-gateway.int.ore.kiyotaka.ai 100.100.100.100` answered NXDOMAIN, so
  `doctor` printed `UNREACHABLE (system resolver and tailnet resolver
  100.100.100.100)` and no fix. `curl -s -o /dev/null -w '%{http_code}'
  --resolve tsdb-gateway.int.ore.kiyotaka.ai:443:10.1.1.10
  https://tsdb-gateway.int.ore.kiyotaka.ai/v2/` answered `400` (the websocket
  path, no upgrade) three times in three; with
  `KIYO_BROWSER_ARGS='--host-resolver-rules=MAP tsdb-gateway.int.ore.kiyotaka.ai
  10.1.1.10'` exported, `doctor` passed on its first run and the lane drew
  live candles all pass. The same held on 2026-11-07: NXDOMAIN on both
  resolvers, `400` three times in three at `10.1.1.10`, and `doctor` green on
  the first run with the map. On 2026-11-08 the system resolver answered
  `10.1.1.10` again and `doctor` passed twice with no map, so read the line
  each run rather than carrying the map forward.
- **The stock Tape needs the stocks gate routed, and the operator's
  `.env.local` does not route it (driven 2026-11-06).** It has no
  `VITE_STOCKS_V2_WEB_SOCKET_DOMAIN` (and its CME line is commented out), so
  the stocks plane is unrouted: a US stock still charts (POLYGON candles over
  v2), but the Tape's market lookup fails at once and the panel falls back to
  the old trades stream (`AAPL/USD`, `No trades match filters`). To see the
  stock Tape, export `VITE_STOCKS_V2_WEB_SOCKET_DOMAIN` and
  `VITE_STOCKS_LIVE_FEED_URL` from the product's `.env.sample` before `up`
  (the process env wins over `.env.local`; never edit the operator's file).
  With them routed on 2026-11-06 the stock Tape's chrome mounted, but the gate
  answered nothing for this guest (`StreamMarkets timed out after 15000ms`),
  no print arrived and the AAPL chart stalled at 0 bars, so relaunch without
  the exports for the rest of a pass. See the right-side panels guide,
  `rp-stock-tape`.
- **A fresh headless device gets Lite charts by itself (driven 2026-11-09).** The
  software GL lane counts as a weak class, so about 12 s into a boot with no
  stored decision `kiyo:pref:light-charts` becomes `1` and a staying
  `.q-notification` (`Keep`, `Turn off`) sits at the bottom of the frame. Clear
  it before a capture and record the state in any drag or performance read. See
  `set-lite` in the Super Search guide.
- **The stores are not window globals.** `chartStore`, `dialogStore` and
  `jwtStore` in these recipes are Pinia stores: read them as
  `document.querySelector('#app').__vue_app__.config.globalProperties.$pinia._s.get('<id>')`
  with the ids `chart`, `dialog` and `jwt` (`typeof chartStore` is
  `undefined` in the page).
- **Keep the tab visible.** A headless tab drifts to `visibilityState: hidden`
  mid-drive, which freezes rAF and runs the app's hidden path. Since the sign-in
  card became an animated sheet (`4b8f78a775`) this also strands its exit: an
  `Escape` on a hidden tab sets `isAuthenticationDialogOpen` to `false` but
  leaves `.login-signup-overlay` in the DOM as `dialog-style--leaving` (pointer
  events off, its animations parked), so the overlay union reads `1` and a
  dismiss helper sees a wall that is already gone. Re-front the tab and read
  again (driven 2026-11-04: it drifted hidden five times in one pass). Check
  `document.visibilityState` before each capture, and re-front with
  `./control-kiyotaka browser tab` then `./control-kiyotaka browser tab t1`
  (a `tab t1` sent straight after an `open` did not take on 2026-11-02; read
  the state back). The Orderbook is the canary: its ladder never mounts while
  the tab is hidden, while the Tape keeps printing and every `eval` answers.
- Viewport set to `1440 900` before any layout assertion.
- Candles present: `window.tc[0].metadata[0].rawData.length > 50`. Budget two
  minutes on a cold boot.
- Interval read, never assumed: `chartStore.activeInterval` (a guest with no
  stored state lands on `1h`).
- The catalog endpoint serves AND is seeded. `doctor`'s `catalog` line probes
  `/scripts/query` and catches a `500`, but a `200` only means the endpoint
  answered: an unseeded local mongo serves `200` with zero official rows. The
  seeded check is in the dialog, under `Browse all indicators` — a header reading
  `OFFICIAL INDICATORS 0` plus a banner naming
  `node scripts/seed-official-catalog.mjs` means `ind-catalog` is unreachable, and
  that is an operator-stack blocker, not drift.
- `doctor`'s `freshness` line read before anything else. A clean tree on `main`
  says nothing about whether it is CURRENT: a checkout hundreds of commits behind
  `origin/main` serves stale code while every other doctor line reads green, and
  a whole pass can then describe an app nobody is running. This has happened —
  one pass drove a tree 324 commits behind, so its live evidence and its
  source findings were about different code. When the line says BEHIND, either
  bring the checkout forward first (the operator's call, not yours) or label
  every finding with which tree it came from.
- `doctor` run twice on a freshly-`up`ed lane, with the second run believed. Its
  first transform probe compiles the module graph cold and has exceeded the
  budget, printing `the tree does not compile` about a healthy tree.
- BOTH first-load overlays cleared: the once-per-device ink tutorial
  (`find testid ink-tutorial-close click`) and the signup modal. The order varies
  (2026-10-27: signup modal first, ink tutorial after it), so read the top
  overlay and dismiss what is there. They share the
  `.dialog-style.dialog-overlay` shell, so probing only the signup modal's testid
  on a fresh device reports `No element found` and reads as a stuck modal.
- Guest signup modal dismissed
  (`find testid guest-signup-modal-close-btn click`) — dismiss it immediately
  before each capture, never once up front. Do **not** drive it by the name
  `Close`: three buttons answer to that name and the matcher picks one under the
  overlay.
- Nothing on top:
  `eval "document.querySelectorAll('.q-dialog, .dialog-style, [role=dialog].open').length"`
  reads `0`. Do **not** count bare `[role=dialog]`: the signup modal and both
  app dialogs are `.dialog-style` overlays carrying no `role=dialog`, so that
  count stays `0` whether or not something is on top.
  The union does not see an indicator's settings card either: since
  2026-10-28 it docks at the right of the chart as `[data-testid=settings-panel]`
  and the union reads `0` while it is open. Probe it by testid.
- **`jwtStore.isGuest` is not a guest check.** A lane started by
  `control-kiyotaka up` can carry NO JWT at all: `jwtMetadata` stays absent, so
  `isGuest` AND `isLoggedIn` both read `false` and the role is `null`, while the
  UI still says `Guest Workspace`. Record which state you drove.

  **The flag-override recipe a previous pass recorded here is DEAD.**
  `GUEST_DEFAULT_FLAGS` was emptied — `search-v2`, `option-chain`, `pulse`,
  `wrun-registry`, `free-tier-v2`, `voice-control` and the rest were all
  graduated out of the flag system during October 2026. Setting
  `kiyo.flag-overrides` for any of them does nothing. Delete that step from any
  recipe that still carries it. The table now lives in
  `src/constants/guest-default-flags.constants.ts` and holds two entries:
  `gateway-v3: false` (since `b5d0fe6b0f`), which keeps a guest on the v2
  wire, and **`us-equities-full: true` (since `bda0563ab1`)**, which gives a
  guest the US stocks surfaces a free account gets on the 15-minute delayed
  lane. A guest's `feature-flags` store read `isOn('gateway-v3')` `false` and
  `isOn('us-equities-full')` `true` on 2026-11-06. A listed key is the
  guest's final answer from boot.

  What replaced them is a **signed-in check**, not a flag: most graduated gates
  read `isSignedInSession()`, which needs a real JWT `id` and a non-guest role.
  On 2026-11-03 the same `up` gave a lane WITH a guest JWT (`isGuest` true,
  `isLoggedIn` false), so read the state on every run.
  So a no-JWT lane and a real guest both fail them, and the practical split is
  now signed-in versus not:

  - The V2 symbol dialog is **structural**, not flag-gated: V2 renders whenever
    the dialog is opened from a main chart on desktop and is not pair/screener/
    comparison mode. Guests get V2 there. The legacy `intent-filter-class-*`
    dialog appears only in those excluded contexts.
  - Surfaces that now need a signed-in session include the `memecoins` and
    `options` category tabs, Events/Earnings panels, the Pulse lane, the 4x4
    free-tier grids, and voice control.

  Source-verified on `fcc8e53b12`; not driven.
- **Identify the overlay before dismissing it — there are now two, and they
  alternate.** A guest boot raises the ink tutorial AND the signup modal, and the
  signup modal re-raises ~15s after the last blocking surface closes, so a
  multi-step drive gets interrupted repeatedly. Three drives were lost this pass
  clicking `guest-signup-modal-close-btn` while the INK TUTORIAL was the thing on
  top. Read what is there, then dismiss that:

  ```bash
  ./control-kiyotaka browser eval \
    "(()=>{const d=[...document.querySelectorAll('.dialog-style,.q-dialog')];return JSON.stringify(d.map(x=>[...x.querySelectorAll('[data-testid]')].map(y=>y.dataset.testid)[0]))})()"
  ```

  A `covered by <div.dialog-style.dialog-overlay>` failure means re-read, not
  retry.
- **An authed lane cannot be self-served.** Driven 2026-10-23: the local dev
  stack's login form does not do password auth by default — it sends a
  **6-digit sign-in code by email**, which the harness cannot read. On 2026-10-27
  the form also offered `login-signup-use-password-btn` and a passkey, but no
  agent has credentials for either. So every "authed lane" claim in
  this map is currently unverifiable by an agent alone, and a guest-walled
  surface can only ever be proven as far as its wall. Ask the operator for a code
  or a password-capable account before planning an authed run; do not burn a pass
  discovering this again.
  Since `906df31d1b` (2026-10-29) the product repo's own project-local skill
  (`.claude/skills/verify-kiyotaka/SKILL.md` and `sign-in.md`) describes a
  signed-in route: `agent-browser --restore kiyo-verify-auth-<target>` carries a
  saved login per target (`local`, `int`, `prod`), and `local` re-signs in from
  an `agent-browser auth` profile named `kiyo-local`. That profile is bound to
  port `8097`, the operator's port, which this map never drives, and on
  2026-10-30 `agent-browser auth list` printed `No auth profiles saved` and no
  `kiyo-verify-auth-*` file existed. So the route does not reach an agent lane
  yet; an operator-saved profile for an agent port would open it.
- **`browser eval` returns JSON with escaped quotes.** A store read such as
  `{"open":true}` comes back as `"{\"open\":true}"`, so a shell `case` or
  `grep` on `"open":true` never matches. Strip the backslashes (`tr -d '\\'`)
  before matching. On 2026-11-01 a helper that compared the raw string skipped
  every `Escape`, the first wall stayed up, and seven Panels rows read as walled
  by the previous row's id until the match was fixed.
- **The v2 gateway is a tailnet-only name, and it can stop resolving mid-pass.**
  `tsdb-gateway.int.ore.kiyotaka.ai` is NXDOMAIN on public DNS; only the
  tailnet resolver `100.100.100.100` answers it, and `tailscale dns status`
  shows no split route for it on this machine. On 2026-11-01 it resolved at
  05:00 local and stopped at about 21:55 UTC: `doctor`'s `v2 gateway` line
  flipped to `UNREACHABLE`, `connection-status-chip` read `Reconnecting…`, the
  console filled with `v2 Streaming socket error` / `v2 Orderbook socket
  error`, OI and funding read `—`, the live panels sat on `Waiting for …`, and
  a reload still painted candles from the OHLCV cache. Re-run `doctor` before
  reading any empty live surface as a regression, and do not start the wake
  heal while the line is red.
- **The counter reads `Indicators n/3`, with the word.** The SKILL's "bare
  `2/3`" is stale: on `120d5d5d32` `tb-indicators-btn` read `Indicators 1/3`
  at boot and `Indicators 3/3` with three overlays.
- Never drive an instance this verification run did not start.

## Driving conventions

- Start every recipe from the baseline unless its preconditions say otherwise.
- Prefer ARIA roles and accessible names over CSS selectors or DOM position.
  Where a control has no accessible name — layout grid cells, Panels rows, drawing
  tools — fall back to `find testid <data-testid>`, which this app populates well,
  rather than concluding there is no handle. Chart-type entries DO carry names, but
  as `generic` nodes, so match their text rather than a button role.
- **A name is not a handle if several controls share it.** A guest boot carries
  three buttons named `Close`; `--name "Close" --exact` picks one of the two that
  sit under the signup overlay and the drive dies as `covered by
  <div.dialog-style.dialog-overlay>`. Where a name is ambiguous, use the testid.
- Never key on an accessible name that is really *content*. The symbol-search
  field's name is the current symbol; match its placeholder instead.
- Browser actions run through `control-kiyotaka browser`, terminal actions
  through `control-kiyotaka cli -- <command>`.
- Treat every command as literal. Keep quoted names and flags unchanged.
- `agent-browser`'s fill text is **positional**:
  `find <locator> <value> fill "<text>"`. There is no `--text` flag; passing one
  types the literal string `--TEXT <text>` into the field and the failure looks
  like a search that returned nothing.
- Check an exit code unpiped. `cmd | tail` reports `tail`'s status, which has
  produced both a false "the wrapper swallows failures" finding and a false
  `doctor` pass in this map's own history.
- Assert engine state (`window.tc`) for anything the a11y tree cannot see. The
  chart canvas is WebGL and carries no accessible structure.
- Restore seeded state after a mutation. Never remove proof artifacts.

## Lanes

Each entry names the lane it needs. **Guest** needs only the lane; **authed**
needs the operator's local stack (`:3000`, `:4001`) plus a login, and mutates a
real account's autosaving workspace — use a throwaway account.

A guest-lane surface can still stop at a sign-in wall partway through: the entry
point opens, the control responds, and the *commit* raises
`Sign in or create an account`. `src/constants/authFeatures.constants.ts` is the
registry of every gated surface — 44 ids in the `FeatureId` enum (counted
2026-11-02 on `a4488341f6`; 45 on 2026-10-29, `TRADE_LIQUIDATIONS` left with
the panel), among them `MULTI_CHART`, `MONITOR`,
`SCRIPT_EDITOR`, `TERMINAL`, `INDICATORS`, `WORKSPACE`, `ALERT`, `WATCHLIST`,
`FAVORITES`, `ONE_SECOND_INTERVAL`, `TAPE_MODE` and `LAYOUTS` — and
`promptGuestLogin` is what raises the wall. Read it before mapping something as
guest-reachable, and report the wall as the unmet precondition rather than
photographing a click that did nothing. Clear the wall with `Escape` before the
next step: it has no close button but it is not sticky, and
`dialogStore.guestLoginFeatureId` names the surface that raised it.

## Proof and skip reporting

- Capture the user action and the resulting state, not only the final screen.
- Chart proof is a **triple**: the engine-state read, the accessible name, and a
  screenshot. The first is the side effect, the last is the only thing that
  proves pixels were drawn.
- CLI proof includes the command, stdout, stderr, and exit code.
- Frames and `evidence-manifest.json` go in `artifacts/<run-id>/<revision>/`;
  validate with `./control-kiyotaka evidence check <run-id> <revision>` and hand
  back that path. There is no publish step on this seat. Never hand back a lane
  URL.
- Report an unreachable path with the attempted command and the unmet
  precondition. Never report a skipped entry point as verified via another path.

## Feature entry contract

An H1 title, one paragraph of user-visible behavior, then exactly four H2s in
order: `Sub-features`, `How to get to it (user POV)`,
`Driving it with control-kiyotaka`, `Gotchas`.

Keep implementation detail out. Name only user paths, stable handles, required
state, commands, and observable proof.

## Which dialog am I on?

No flag picks the dialog any more. `search-v2` graduated and
`GUEST_DEFAULT_FLAGS` holds only `gateway-v3: false` and `us-equities-full:
true`, neither of which picks the dialog. On 2026-11-09 on `32dd0c6354`, 2026-11-08 on `943281a2eb` and
2026-11-07 on `dced88e06a` a guest open read `v2` 20, `legacy` 0, as on 2026-11-05 on `87a325f4ab`. The dialog is V2 when it opens from a main chart
on desktop and is not in pair, screener or comparison mode. Every lane, guest
included, gets V2 there, so `sym-scope` is a guest proof. The legacy
`intent-filter-class-*` dialog appears only in the excluded contexts and on
mobile. Source-verified on `df3fdcb62e` (`isSearchV2` in
`src/components/symbolSelection/SymbolSelectionDialog.vue`) and driven
2026-10-27 on `7290d33d10` and 2026-10-28 on `29c9cda0a2`: a guest open read
`v2` 22, `legacy` 0 both times. On 2026-10-29 on `78ec9625d9` it read `v2` 20,
`legacy` 0: the `hip4` tab and its hidden twin are gone (`93b3a757c0`).

The gate has changed three times, so read it off the DOM at the start of any
symbol run:

```bash
./control-kiyotaka browser eval \
  "JSON.stringify({v2:document.querySelectorAll('[data-testid^=search-v2-category-]').length,legacy:document.querySelectorAll('[data-testid^=intent-filter-class-]').length})"
```

## Features

- [Chart boot and the data plane](./chart-boot-and-data-plane.md) — guest (the
  wake heal recipe needs the backend reachable for the wake's token refresh)
- [Indicators](./indicators.md) — guest (the official catalog needs a SEEDED
  backend, not a login: the operator's remote dev backend is seeded; a fresh
  local stack needs `node scripts/seed-official-catalog.mjs`)
- [Symbol search and the ticker bar](./symbol-search-and-ticker-bar.md) — guest
- [Script editor and kScript](./script-editor-and-kscript.md) — guest proves the
  read-only drawer through Super Search and the toggle's wall; kScript is
  retired on this tree (no engine, no date, no flag), so the authed rows are
  TypeScript Indicators only
- [Watchlist](./watchlist.md) — guest proves the wall ONLY; every sub-feature
  behind it is unverified because this stack cannot be signed into by an agent
- [Voice control](./voice-control.md) — NOT guest-reachable: the `voice-control`
  flag graduated to `isSignedInSession()`, so the override is dead and a guest
  lane has no mic, chip or seam at all
- [Super Search and settings](./super-search-and-settings.md) — guest (Super
  Search, theme and formula rows, Keyboard Shortcuts, Release Notes, and the
  shared sign-in wall with its feature ids)
- [Right-side panels](./right-side-panels.md) — guest for Orderbook, the Tape
  with its docked Liquidations (the Trades and Liquidations panel is retired),
  the three stats panels, Journal, Alerts, Objects, the ETF screener and the
  heatmap popover; Options, alert creation and seven Panels rows stop at the
  wall
- [Drawing tools](./drawing-tools.md) — guest
- [Clip guest page](./clip-guest-page.md) — guest (`/chart/clip/<id>`; the
  private state is driven, a public clip needs an id)

## Surface inventory

Re-discovered 2026-11-09 from kiyotaka-frontend source on `origin/main`
`32dd0c6354` (60 commits past `943281a2eb`), and the live column re-stamped
from the same day's drive where a row was driven. Against `943281a2eb`: the
router, the 44 gate ids, `GUEST_DEFAULT_FLAGS`, the panel registry and the
flag registry have no diff; among the Super Search providers only `settings.ts`
changed (a row title). New user-facing files: `src/utility/chart/lite/` with
`LiteChartsSettingRow.vue` and `PerformanceSettingsPage.vue`,
`TBHeatmapPanelOptionsBody.vue`, `family-logo.util.ts`, the shared `Button`,
`CloseButton`, `ConfirmDialog` and `SearchField` (`CustomButton.vue`,
`SearchInput.vue` and `StockFeedSwitchDialog.vue` deleted). New rows: Lite
charts, the search rail's exchanges, Order Book Profile grouping, the Options
heatmap knobs, the session feed's long and sub-minute bars, wrun twins' built-in
words, the shared search field and dialog language, and Full chart's exit; the
stock venue label, the dark pool layer, the screenshot and clip privacy
changes and the marketplace relist extend existing rows. Previous discovery:
re-discovered 2026-11-08 from kiyotaka-frontend source on `origin/main`
`943281a2eb` (59 commits past `dced88e06a`), and the live column re-stamped
from the same day's drive where a row was driven. Against `dced88e06a`: the
router, the 44 gate ids, `GUEST_DEFAULT_FLAGS` and the Super Search
providers have no diff. Deleted: `TBSourceDropdown.vue` (the heatmap's
Source menu). New user-facing files: `useHeatmapKinds.ts`,
`heatmap-last-type.util.ts`, `open-interest/plot-type.ts`,
`display-timezone-offset.util.ts`, `stock-legend-delay.util.ts`,
`dark-pool-chart-settings.util.ts`, `useOpenWhenLoaded.ts` and the in-place
screenshot utilities. New rows: Open Interest's plot type, the heatmap by
kind, the footer timezone offsets, ComboBox menus with one-width panels, and
CVD's grey no-side bars; the merged stock chip, the dark pool settings box,
the wrun `nothing to draw` note, the socket keepalive, the in-place
screenshot and the forex starter list extend existing rows. The 2026-11-07
discovery follows.

Previous discovery: re-discovered 2026-11-07 from kiyotaka-frontend source on `origin/main`
`dced88e06a` (81 commits past `8bcd72f8f5`), and the live column re-stamped
from the same day's drive where a row was driven. Against `8bcd72f8f5`: the
router, the 44 gate ids and `GUEST_DEFAULT_FLAGS` have no diff; the Super
Search providers gained `ninjatrader.ts` (36 files) and `settings.ts` routes
`ninjatrader` and `tradovate` to the Connections page. New component file:
`NinjaTraderConnectDialog.vue`. New rows: NinjaTrader as the futures lane's
second broker, a relay feed as the chart's main plot, the share dialog's
account lines, and governed search rows that draw no figures; the Yours tab
(`cadb450cdb`, now on `main`), the Tape-driven dark pool layer
(`c106437eb7`, `841ea60455`) and the delay labels on every surface
(`63c1fa257a`, `688e2ff054`) extend existing rows. The 2026-11-06 discovery
follows.

Previous discovery: re-discovered 2026-11-06 from kiyotaka-frontend source on `origin/main`
`8bcd72f8f5` (119 commits past `87a325f4ab`), and the live column re-stamped
from the same day's drive where a row was driven. Against `87a325f4ab`: the
router and the 44 gate ids have no diff; the Super Search providers are still
35 files (`indicators`, `tools`, `feeds`, `wrunRegistry` and
`createLocalProvider` modified for covers and the drawing-tool kind);
`GUEST_DEFAULT_FLAGS` moved to `src/constants/guest-default-flags.constants.ts`
and gained `us-equities-full: true`. New component files: the service-notice
banner, pill, host, inline and list (`src/components/banners/`), the
`UsTapeLaunchHero.vue` spotlight, `TapeRowCard.vue` and
`TapeDockResizeHandle.vue`; deleted: `FooterMaintenance.vue`. The rows below
carry each, plus three new rows (service notices, the restore removal notice,
the settings search). Every new source path was checked against `8bcd72f8f5`.
The 2026-11-05 discovery follows.
Re-discovered 2026-11-05 from kiyotaka-frontend source on `origin/main`
`87a325f4ab` (123 commits past `8436920004`), and the live column re-stamped
from the same day's drive where a row was driven. Against `8436920004`: the
router, the 44 gate ids and the panel registry have no diff; the Super Search
providers are still 35 files (`symbols` modified, and `useSuperSearch.ts`
now offers its `Open symbol search` row as a backup while a device holds no
market name list); `GUEST_DEFAULT_FLAGS` gained its one entry, `gateway-v3:
false`. New component files: `ConnectionStrip.vue`, `StockGoLiveCard.vue`,
`ClipVideoPlayer.vue` and `AlertDeliveryFailedNotice.vue`; deleted: the clip
poster player and its scene, hand and overlay layers. The rows below carry
each, plus six new rows (dollar pairs, the strip, alert delivery failures,
store picture zoom, the search words, futures contract picks). Every new
source path was checked against `87a325f4ab`. The 2026-11-04 discovery
follows. Re-discovered 2026-11-04 from kiyotaka-frontend source on `origin/main`
`8436920004` (80 commits past `215896e614`), and the live column re-stamped
from the same day's drive where a row was driven. Against `215896e614`: no
diff in the router, the 35 Super Search provider files, the 44 gate ids, the
panel registry, the flag registry or `GUEST_DEFAULT_FLAGS` (`{}`). The range
rebuilt the sign-in card (`LoginSignupDialog.vue` with `LoginCodePanel.vue`
and `TwoFAVerifyPanel.vue`), added the drawing bar's templates button,
replaced the CME ghost bars with one delayed tag (`CmeDelayBadge.vue`;
`CmeDelayGhostBars.vue` is deleted), opened pane merge to every plan, gated
spot panes on derivative data, gave the connection chip one glyph per state,
and ran the first-run steps on phones; the rows below carry each. Every new
source path was checked against `8436920004`. The 2026-11-03 discovery
follows. Re-discovered 2026-11-03 from kiyotaka-frontend source on `origin/main`
`215896e614` (131 commits past `a4488341f6`), and the live column re-stamped
from the same day's drive where a row was driven. Against `a4488341f6`: the
router changed only the Chart route's sign-in return handling
(`signInReturnGuard`); the Super Search providers are still 35 files, with
`featureCommands`, `settings` and `symbols` modified; the 44 gate ids, the
panel registry and `GUEST_DEFAULT_FLAGS` (`{}`) have no diff; the flag
registry gained `wrun-converging-prefix` (57 to 58, dark). The new
component files of the range are the Show on chart panel and footer door,
four Indicators dialog parts (add pill, pane menu, pane picture, pop menu),
`ScrollCueBar.vue`, `RithmicLaunchHero.vue`, `MobileScrollToLatestButton.vue`
and a futures ticket figure. Every source path below was checked against
`215896e614`. The 2026-11-02 discovery follows. Re-discovered 2026-11-02 from
kiyotaka-frontend source on `origin/main` `a4488341f6` (90 commits past
`120d5d5d32`), and the live column re-stamped from the same day's drive on
that tree. The rows come from the router
(`src/router/routes.ts`: the Board gained `clips`, `clips/:id`, `setup/:key`
and `c/:slug`, and a guest-reachable top-level `/clip/:id` joined), the Super
Search providers (35 files, none added or removed; eight modified: academy,
indicators, memecoins, panels, settings, symbols, tape, tools), the 44 gate
ids in `src/constants/authFeatures.constants.ts` (`TRADE_LIQUIDATIONS` left),
the panel registry (`src/constants/panels.constants.ts` lost
`TradeAndLiquidations`), the flag registry
(`packages/wrun-chart-host/src/constants/feature-flags.constants.ts` lost
`script-offers` and `opra-alerts`, 59 to 57; `GUEST_DEFAULT_FLAGS` in
`src/store/feature-flags.ts` is still `{}`), the Ask command catalog (three
one-line diffs; the do lane is now picked from the feature registry by
`src/ask/pick/`, and `src/ask/decide/route.ts` and `parts.ts` are deleted)
and the commits in `120d5d5d32..a4488341f6`, not from the guides. Every
source path was checked against `a4488341f6`; the Trades and Liquidations
component, the kScript read-only viewer (`KScriptLegacyNotice.vue`) and
`src/ask/decide/parts.ts` that the 2026-11-01 rows cited are deleted and
their rows rewritten below. Gates were read from those registries and a usage grep, not from
each component; "gate not checked" says so where nothing was found. "Live"
names the run that last drove the outcome. An `unmapped` row has no recipe yet
and has never been driven by this map. Most of them stop at a sign-in wall, and
no agent can sign in on this stack (see Baseline preconditions).

| User outcome | Product source path | Guide / sub-feature | Live verification | Prerequisite or gap |
|---|---|---|---|---|
| Chart opens and draws candles from the worker-owned feed | `src/pages/chart.vue`, `src/workers/worker-manager.ts`, `src/workers/services/websocket.worker.service.ts` | [boot](./chart-boot-and-data-plane.md) `boot-mount`, `boot-candles`, `boot-worker` | 2026-11-09, `32dd0c6354`, 250 bars on COINBASE BTC-USD 1h with VWAP at 14 s cold, `Indicators 1/3`, `__BOOT_ERRORS__` `[]`; before that 2026-11-08, `943281a2eb`, 250 bars on COINBASE BTC-USD 1h with VWAP, `Indicators 1/3`, `__BOOT_ERRORS__` `[]`, the gateway name on the system resolver; before that 2026-11-07, `dced88e06a`, 250 bars on COINBASE BTC-USD 1h with VWAP, `Indicators 1/3`; before that 2026-11-05, `87a325f4ab`, guest-JWT lane, 250 bars on COINBASE BTC-USD 1h, `__BOOT_ERRORS__` `[]`; before that 2026-11-04, `8436920004`, guest-JWT lane, the gateway resolving, 250 bars, `__BOOT_ERRORS__` `[]`, no chip; the ring not dumped (2026-11-02 for `v2-socket-route`) | the operator's `.env.local` in the lane's tree; the one-loader handoff (`d4c822292e`) seen only as its end state; since `a03b0af8ce` a socket whose Cloudflare path fails, stalls or crawls redials a direct host for 10 minutes (`VITE_{CME,OPRA,STOCKS}_GATE_DIRECT_URL`, ring `edge-route-change`), not driven; since `77b44cfcc1` the worker pings an idle feed socket itself (`feedIdlePing`, 15 s), so a hidden tab whose price title holds still keeps it, and a page-made close is echoed at once (`9ca7ecdd6c`): source, not driven; a wake or tab return asks only the candles the saved copy cannot prove (`d4113f01da`) and a pane is not rebuilt under a live gesture (`058530d565`): source, not driven |
| Ticker shows live price, 24h volume, OI and funding | `src/services/live-feed.service.ts`, `src/components/TickerBar/TBMarketStats.vue` | [boot](./chart-boot-and-data-plane.md) `boot-live` | 2026-11-07, `dced88e06a` (perp BINANCE.F ETHUSDT `2228.41 -0.93%`, `24H VOLUME $7.97B`, `OPEN INTEREST $5.29B`, `FUNDING / COUNTDOWN +0.0058% · 03:39:28`); before that 2026-11-05, `87a325f4ab` (perp BINANCE.F ETHUSDT `2,417.84 +5.66%`, OI `$5.75B`, funding `+0.0055% · 03:16:35`; a hidden tab reads `—` in the price slot); before that 2026-11-04, `8436920004` (perp BINANCE.F ETHUSDT `2289.72 +1.71%`, OI `$5.44B`, funding `+0.0100%`); the spot edge 2026-11-02 | OI and funding exist only on derivatives, and since `3db024ab19` and `cdfa9c212d` a spot venue is not even asked (`src/utility/exchange/derivative-venue.leaf.ts`); a tab that drifts `hidden` freezes the slots; both read `—` during the gateway outage; since `53d871d60a` the 24h change reads the gateway reference first (it matched the search row within 0.02 points); a hidden tab shows `—` in the price slot |
| A woken tab backfills the candles it missed | `src/composables/chart/useVisiblityChanges.ts`, `src/utility/chart/wake-resync-overlay-plan.util.ts` | [boot](./chart-boot-and-data-plane.md) `wake-heal` | 2026-11-02, `a4488341f6`, the lone-bar heal on BINANCE.F SOLUSDT 1m from a 392 s visibility override (5 blank slots to 0, `main-heal-commit` `row-width`, the token refreshed in 178 ms); the recipe's `updateData` write had replaced the series, so the heal was judged on a six-bar chart (see the boot guide) | the wake's token refresh needs the backend proxy reachable and the heal needs the gateway; `fc079a95eb` closes the v3 lanes at the start of a wake (`closeV3LanesAfterSleep`, no ring event of its own); a real sleep and the process-suspend lane not driven |
| Indicators dialog opens, searches and adds an overlay | `src/components/dialogs/IndicatorDialogV2.vue`, `src/store/chart.add-indicator.ts` | [indicators](./indicators.md) `ind-dialog`, `ind-add` | 2026-11-08, `943281a2eb`, an `Open Interest` search (`Official 8`, `Community 2`) whose row Add raised `indicators`; before that 2026-11-07, `dced88e06a`, an `rsi` search (`Official 4`, `Community 12`); before that 2026-11-05, `87a325f4ab`, an `rsi` search (`Official 4`, `Community 12`, `See all 243`) and the `RSI` row's `indicators` wall; before that 2026-11-04, `8436920004`, an `open interest` search (`Official 8`, `Community 2`); the split view, `poc` and the `RSI` wall 2026-11-03 | a dialog-path mount needs a signed-in session; a retired kScript row refuses with a toast (source); the favourite star works on every row that can take one and reads disabled, with its reason in the title, on the rest (`f6ba61116e`); a guest's favourite write is walled; the sentence lane (`indicator-list-sentence`, `indicator-sentence-no-fit`) never engaged for a guest (two sentences tried); the pane's door menu (`indicator-pane-door-*`) not opened; since `ee1fae1b4d` the search field is the shared `SearchField` (source) |
| The legend's settings, visibility and close controls work | `src/components/chart/ChartLegends.vue`, `src/store/chart.indicator-mgmt.ts` | [indicators](./indicators.md) `ind-legend` | 2026-11-03, `215896e614`; the docked card (10 `setting-term` rows) from the legend menu's `indicator-menu-settings`; the menu's eight rows incl. `indicator-menu-scale` and `-fold` | pin and window doors depend on the type (source); close the card with `overlay-settings-close-btn` |
| Indicator settings rows explain themselves | `src/components/common/SettingTerm.vue`, `src/components/common/IndicatorSettingsForm.vue` | [indicators](./indicators.md) `ind-legend` | 2026-11-03, `215896e614`, 10 terms on `BITCOIN_DOMINANCE`; the hover card 2026-10-29 | `setting-term-learn-more` needs a docs origin; the ticker-bar heatmap popover's terms need a signed-in session; a row now hides only while its value has no effect (`d9727ce894`, `0c0f2ec4e5`, `587939bdaa`), not driven; a 10-row card has no settings search (see the settings search row) |
| Search a long built-in's settings in place (`1235632725`, `fb01153fbe`) | `src/composables/settings/useSettingsSearch.ts`, `src/utility/settings/settings-search-match.util.ts`, `src/components/dialogs/OverlaySettingsDialog.vue` | [indicators](./indicators.md) `ind-settings-search` | 2026-11-09, `32dd0c6354`, a programmatic `SESSION_VOLUME_PROFILE`: `Escape` cleared the words, left the search, then closed the card; before that 2026-11-06, `8bcd72f8f5`, a programmatic `SESSION_VOLUME_PROFILE` (62 rows): `wid` left 6, `zzzz` showed `settings-search-empty` | `Cmd+F` and the two-step `Escape` not driven; TPO and footprint always get the field (source) |
| Official indicators are listed | `src/services/indicator-catalog.service.ts`, `src/composables/chart/useIndicatorCatalogV2.ts` | [indicators](./indicators.md) `ind-catalog` | 2026-11-03, `215896e614`, seeded remote dev backend (`See all 193`, three shelf cards) | a seeded backend; a fresh local stack needs `node scripts/seed-official-catalog.mjs`; the builtin seen marks (`e491d0feb9`) are a network side effect with no surface |
| The indicators-per-chart cap holds | `src/store/chart.add-indicator.ts`, `src/composables/chart/useSuiteApplication.ts`, `packages/wrun-chart-host/src/constants/feature-limits.constants.ts` | [indicators](./indicators.md) `ind-limit` | 2026-11-05, `87a325f4ab`, display only (`Indicators 1/3` then `2/3` on two programmatic mounts); before that 2026-11-03, `215896e614`, display only (`Indicators 3/3` after two programmatic adds over VWAP) | the cap is per tier (free 3, plus 10), and enforcement runs only on the dialog path, which a guest cannot take |
| Symbol search finds and switches a market; scope chips filter | `src/components/symbolSelection/SymbolSelectionDialog.vue`, `src/components/symbolSearchV2/CategoryStrip.vue` | [symbol search](./symbol-search-and-ticker-bar.md) `sym-search`, `sym-scope`, `sym-stock` | 2026-11-09, `32dd0c6354`; v2 20 / legacy 0, the bare `asset-row-BTCUSDT\|1-btn` charted `BINANCE.O BTC/USDT 25 Dec 2026 80,000 Put`, `venue-row-BINANCE_FUTURES\|BTCUSDT-btn` charted BINANCE.F BTCUSDT (381 bars), `asset-row-AAPL\|4-btn` charted AAPL (252 bars), `venue-row-BINANCE_FUTURES\|ETHUSDT-btn` charted BINANCE.F ETHUSDT (250 bars); before that 2026-11-08, `943281a2eb`; v2 20 / legacy 0, the `Ethereum` row charted DERIBIT.F ETH_USDC-PERPETUAL (356 bars), `venue-row-BINANCE_FUTURES\|BTCUSDT-btn` charted BINANCE.F BTCUSDT (357 bars), `asset-row-AAPL\|4-btn` charted AAPL (252 bars); before that 2026-11-07, `dced88e06a`; v2 20 / legacy 0, no `search-v2-category-yours-btn`, `venue-row-BINANCE_FUTURES\|ETHUSDT-btn` charted BINANCE.F ETHUSDT (333 bars), `asset-row-AAPL\|4-btn` charted POLYGON `AAPL/USD` (252 bars); before that 2026-11-06, `8bcd72f8f5`; v2 20 / legacy 0; `AAPL` listed one stock row (`asset-row-AAPL\|4-btn`) that charted POLYGON `AAPL/USD` with the bare ticker; before that 2026-11-05, `87a325f4ab`; the `Ethereum` row to BINANCE.F ETHUSDT; the Equities tab 2026-11-01; the `CME` tab failed for the guest 2026-11-04 (`CME contracts aren’t loading right now`, twice) | the bare ticker row is still a product gap: on 2026-11-08 an `ETHUSDT` query listed no bare row, but the bare `asset-row-BTCUSDT\|1-btn` charted `BINANCE.O BTC/USDT 27 Nov 2026 77,000 Put`; before that, the bare `ETHUSDT · Crypto` asset row STILL opens a Binance ETH put, re-confirmed 2026-11-04, 2026-11-05 and 2026-11-06 (`BINANCE_OPTIONS` `ETH-261113-2250-P`): product gap (`resolveEnterTargetVenue` filters no instrument category); the memecoin lane answers only a pasted Solana mint (`9ffb5345bf`); continuous `6A1!`, `6S1!` and `6N1!` now resolve their lead contract (`84153ce7aa`), not driven (a guest's `NQ1!` fill listed no row on an earlier pass) |
| A CRYPTOCAP index (BTC.D, TOTAL2 ...) is the main series | `src/utility/symbol-search-v2/crypto-index-search.util.ts`, `src/utility/chart/crypto-index-format.util.ts` | [symbol search](./symbol-search-and-ticker-bar.md) `sym-cryptocap` | 2026-11-03, `215896e614`, BTC.D 250 bars (`60.30% ▲ BTC.D`) through `asset-row-CRYPTOCAP\|BTC.D-btn` | the alert gate and refusals in `docs/features/data/cryptocap-indices.md` are not driven |
| Browse and chart prediction markets: the Predict tab with Polymarket and HIP-4 venue chips | `src/components/symbolSearchV2/CategoryStrip.vue`, `src/components/symbolSelection/component/IntentFilter.vue`, `src/utility/symbol-selection/prediction-preview.util.ts`, `src/utility/symbol-selection/discovery-category.util.ts` | [symbol search](./symbol-search-and-ticker-bar.md) `sym-predict` | 2026-11-02, `a4488341f6`, the three chips (`all` pressed) through the Browse rail's `search-v2-view-predictions-btn` (the tab's own click was covered); a Polymarket Senate event charted (143 bars, `25.5¢`) | none for a guest; the `HIP-4` tab was folded into Predict by `93b3a757c0` |
| Hover quick-search switches the symbol without the full dialog | `src/components/TickerBar/QuickSymbolSearchDropdown.vue` | [symbol search](./symbol-search-and-ticker-bar.md) `sym-quick` | 2026-11-05, `87a325f4ab`, the list opened on hover and a typed `XAUUSD` listed its forex row first; before that 2026-11-03, `215896e614`, `SOLUSDT` to BINANCE.F SOLUSDT through `quick-search-v2-group-Solana\|1-btn` (a provisional `unresolved:crypto:SOL` group came first, at 5 s) | the memecoin and Pulse rows need a signed-in session |
| Memecoin lane, liquidity floor and Pulse rows | `src/components/symbolSelection/component/MemecoinRow.vue`, `src/components/symbolSearchV2/RefineControls.vue`, `src/components/pulse/PulseRow.vue` | [symbol search](./symbol-search-and-ticker-bar.md) `sym-memecoins` | live verification pending; the lane's absence for a guest driven 2026-11-02 (`pepe` lists no memecoin row) | a signed-in session (the `memecoins` tab and Pulse need it); since `9ffb5345bf` and `eb1f3b83be` the lane answers only the Memecoins tab or a pasted Solana mint (`quick-search-v2-memecoins-tail-btn` deleted) |
| Interval, chart type and layout pickers re-drive the chart | `src/components/TickerBar/TBIntervalSelector.vue`, `src/components/TickerBar/TBChartTypeSelector.vue`, `src/components/TickerBar/TBLayoutPicker.vue`, `src/utility/stocks/stock-seconds.util.ts` | [ticker bar](./symbol-search-and-ticker-bar.md) `tb-interval`, `tb-plot`, `tb-layout`, `sym-stock` | 2026-11-07, `dced88e06a` (`tb-interval-pinned-1m-btn` to `1m`, 431 bars, `Undo Change interval` back to `1h`); before that 2026-11-06, `8bcd72f8f5` (`tb-interval-option-15m-btn`; the chevron menu on AAPL with no seconds section, 12 options, against BTC's `tape` and `1s` to `30s`); 2026-11-04, `8436920004` (`tb-interval-pinned-1m-btn` and its undo); 2026-11-03, `215896e614` (Heikin Ashi and the regrouped menu, `tb-layout-entry-2H-btn` walling `multi-chart`) | a multi-chart grid needs a signed-in session; the `ChartArea` interval menu not opened; a saved seconds interval landing on `1m` on a stock not driven |
| Pickers peek on hover; the bar folds into the Panels menu | `src/components/TickerBar/TBChartTypeSelector.vue`, `src/composables/chart/useTickerBarFoldedControl.ts`, `src/composables/chart/useTickerBarFit.ts` | [ticker bar](./symbol-search-and-ticker-bar.md) `tb-hover`, `tb-more`, `tb-one-menu` | 2026-11-02, `a4488341f6` (the Panels menu's 17 rows; opening the layout picker closed a click-pinned chart-type menu); the peeks 2026-10-29 | there is no `⋯` button; a narrow viewport was not driven; the quick search's `held` block on hover-opens not proven |
| The right-hand cluster toggles its panels | `src/components/TickerBar/TBPanelToggle.vue`, `src/components/TickerBar/TBPanelsMenu.vue` | [ticker bar](./symbol-search-and-ticker-bar.md) `tb-bar-toggles` | 2026-11-03, `215896e614` (`tb-panels-row-watchlist`, `-news` and `-editor` walled); the seats themselves 2026-11-02 | Watchlist, News and Editor wall a guest; an open panel folds every seat away |
| The script editor drawer opens | `src/components/scriptEditor/shell/EditorDrawer.vue`, `src/components/TickerBar/TBEditorToggle.vue` | [editor](./script-editor-and-kscript.md) `ks-open` | 2026-11-09, `32dd0c6354`, `super-search-result-panels:Editor-btn` opened the drawer (`kscript-run-btn`, no `kscript-save-btn`) and the Panels row raised `script-editor`; before that 2026-11-08, `943281a2eb`, `super-search-result-panels:Editor-btn` opened the drawer (`kscript-run-btn`, no `kscript-save-btn`) and the Panels row raised `script-editor`; before that 2026-11-07, `dced88e06a`, `super-search-result-panels:Editor-btn` opened the drawer (`kscript-run-btn`, no venue banner on crypto); before that 2026-11-05, `87a325f4ab`, through Super Search (`New indicator`, `No indicators yet`, `No script open`) with no wall; before that 2026-11-04, `8436920004`, through Super Search (`New indicator`, `No script open`, no wall); the Panels `editor` row walled `script-editor` 2026-11-03 | the ticker-bar toggle and the Panels row raise the sign-in wall for a guest |
| An own TypeScript Indicator runs, or reports its problem; a kScript document opens nowhere (a 3 s toast at every door) | `src/store/script.ts`, `src/components/scriptEditor/shell/KScriptWorkspace.vue`, `src/store/editor-shell.ts` | [editor](./script-editor-and-kscript.md) `ks-run`, `ks-lint` | live verification pending (the retired handles' absence driven 2026-11-02) | a signed-in session; the browser kScript engine, the analysis worker, the grammar and the read-only kScript viewer are deleted (`722911b50f`, `4f7be7723c`) |
| A protected or WRUN script returns from the hosted lane | `src/workers/services/kscript-ws.worker.service.ts` (the cloud answers `KSCRIPT_RETIRED` for a kScript document) | [editor](./script-editor-and-kscript.md) `ks-protected` | live verification pending | a signed-in session; `protected-kscript-cache.service.ts` is deleted (`722911b50f`); since `a169947dca` an indicator that draws nothing says so in its legend (`nothingDrawn`, `nothingDrawnReach`) and a slow sandbox worker is waited on for up to 180 s (source) |
| WRUN launch box and Pine conversion create a draft | `src/components/wrun/launch/KataPineBox.vue`, `src/components/scriptEditor/shell/PineConvertDialog.vue` | [editor](./script-editor-and-kscript.md) `ks-wrun-launch` | live verification pending | a signed-in session and the entitlement |
| OPRA data in user scripts | `packages/wrun-chart-host/src/utility/chart/opra-user-scripts-gate.util.ts`, `src/utility/chart/opra-user-scripts-gate.util.ts`, `src/utility/options/opra-user-scripts-rejudge.util.ts` | unmapped (a source note in [editor](./script-editor-and-kscript.md) Gotchas) | live verification pending | the `opra-user-scripts` gate answers on since `61f23cdf65` (the flag record still exists, marked launched); a signed-in session plus the OPRA entitlement and tier |
| Watchlist panel opens; a guest gets the sign-in wall | `src/components/watchlist/Watchlist.vue`, `src/components/TickerBar/TBPanelToggle.vue` | [watchlist](./watchlist.md) `wl-open` | 2026-11-09, `32dd0c6354`, `tb-panels-row-watchlist` raised the `watchlist` wall; before that 2026-11-08, `943281a2eb`, `tb-panels-row-watchlist` raised the `watchlist` wall; before that 2026-11-07, `dced88e06a`, `tb-watchlist-toggle-btn` raised the `watchlist` wall; before that 2026-11-05, `87a325f4ab`, the wall from `tb-panels-row-watchlist`; before that 2026-11-04, `8436920004`, the wall from the Watchlist seat (the one-card sheet headed `Watchlist`); the Panels row 2026-11-03 | none for the wall; the seeded Forex list is `USD/JPY`, `USD/CAD`, `USD/CHF` since `827ba9d2e8` (source) |
| Lists are picked, added to, pruned, reordered, imported and capped | `src/components/watchlist/WatchlistListMenu.vue`, `src/store/watchlist.ts`, `src/composables/watchlist/useWatchlistImport.ts`, `src/constants/watchlist-limits.constants.ts`, `src/ask/commands/rows/watchlist.ts` | [watchlist](./watchlist.md) `wl-lists` to `wl-limits`, `wl-ask-add` | live verification pending | a signed-in session; an absolute `24h chg` column (`chg24hAbs`, `625bc087a5`) joined the column library (source) |
| A spoken command changes symbol, interval and indicators | `src/components/voiceControl/VoiceControlNavButton.vue`, `src/utility/voice-control/voice-control-gate.util.ts`, `src/utility/voice-control/voice-grammar.util.ts`, `src/utility/voice-control/chart-target.util.ts` | [voice](./voice-control.md) `vc-*` | 2026-10-12, `7347b94e69`, through the rig seam with the flag forced; absence on a guest re-confirmed 2026-11-02 | a signed-in session; the microphone and multi-chart targeting were never driven; absence re-confirmed 2026-11-03 (no `[data-testid^=voice]` node); absence re-confirmed 2026-11-08 (`window.__voiceControl` undefined, no `voice` or `mic` testid); absence re-confirmed 2026-11-09 on `32dd0c6354` (`window.__voiceControl` undefined) |
| Super Search palette opens and runs rows | `src/composables/superSearch/useSuperSearch.ts`, `src/components/GlobalNav/NavSearchField.vue`, `src/components/superSearch/SuperSearchResultRow.vue` | [Super Search](./super-search-and-settings.md) `ss-open`, `ss-rows` | 2026-11-09, `32dd0c6354`; `dark` toggled `body--dark` and back, `heatmap` listed the indicator rows and the commands, `editor` listed `panels:Editor`, the clear control reads `Clear`, `super-search-keycap` read `⌘ K`; before that 2026-11-08, `943281a2eb`; `dark` toggled `body--dark` and back, `heatmap` listed the heatmap indicator rows and the `heatmapMagnifier` and `openHeatmapPanel` commands; before that 2026-11-07, `dced88e06a`; `ninjatrader` lists only `symbols:open-search` for a guest, `editor` lists `panels:Editor`; before that 2026-11-06, `8bcd72f8f5`; `anchored vwap` (an indicator row with its cover, a tool row tagged `Drawing tool`, the Enter hint `Draw` then `Add`), `editor`, `release notes`; before that 2026-11-05, `87a325f4ab`; `carbon`; the directory, `hide candles`, `show candles` 2026-11-04; `volt`, `gray`, `terracotta`, `SPY / GLD` 2026-11-03 | per-provider gates; `Mod+J` not driven; the Ask starters need a signed-in session; since `215896e614` the `trade-history` and `open-trades` rows are gone for `show-on-chart` rows listed only while an own account draws (source) |
| A help question lists user-guide sections under Guides | `src/composables/superSearch/useSuperSearch.ts`, `src/components/superSearch/SuperSearchDialog.vue` | [Super Search](./super-search-and-settings.md) `ss-guides` | live verification pending; attempted 2026-11-02, `a4488341f6`: `No results found` (`/ask/config` read `surface:false` on 2026-11-01) | the backend's `/api/v1/ask/config` must answer `surface:true` (the dev backend answered `false`) |
| Themes: dark and light, the colour themes (Volt, Percept ...); Gray and Cream appearance | `src/composables/superSearch/providers/themes.ts`, `src/utility/theme/appearance-modes-flag.util.ts` | [Super Search](./super-search-and-settings.md) `ss-theme` | 2026-11-09, `32dd0c6354`, `themes:mode:dark` flipped `body--light` to `body--dark` and back; before that 2026-11-07, `dced88e06a`, `themes:mode:dark` flipped `body--light` to `body--dark` and back; before that 2026-11-05, `87a325f4ab`, Carbon applied (`themes:color:CarbonCore`, `theme-carbon`) with translucent volume bars; before that 2026-11-03, `215896e614`, Volt applied (`theme-kiyotaka`) and Terracotta restored (`theme-percept`), Gray raising `light-mode`; the Preferences page 2026-11-02 | Gray and Cream are listed on every desktop and wall a guest (`light-mode`); a pick past the wall needs a signed-in session |
| Compare mode and formula charts | `src/composables/superSearch/providers/formulas.ts`, `src/utility/symbol-selection/plot-typed-formula.util.ts` | [Super Search](./super-search-and-settings.md) `ss-formula` | 2026-11-03, `215896e614`, the row charted `NYSE SPY / GLD` again (252 bars, title `SPY / USD / GLD / USD`) | the 2026-11-01 and 2026-11-02 gap (Solana tokens, then a BINANCE.F perp) is closed on `215896e614`, closing commit not traced; the compare overlay path not driven |
| Keyboard shortcuts | `src/pages/settings/KeyboardShortcuts.vue`, `src/components/dialogs/SettingsPagesDialog.vue` | [Super Search](./super-search-and-settings.md) `set-shortcuts` | 2026-11-09, `32dd0c6354`, `Meta+/` opened it (nav `shortcuts`, `performance`, `language`, `notes`); before that 2026-11-05, `87a325f4ab`, `Meta+/` opened it (nav `shortcuts`, `language`, `notes`); before that 2026-11-04, `8436920004`, `Meta+/` opened it (nav `shortcuts`, `language`, `notes`) | the `Reset all` overlap fix needs a customised shortcut, not driven; since `664d7f0a8d` Cmd/Ctrl+C is left to the browser when the last press landed in a text selection (source) |
| Release notes, and a release's spotlight replayed from its badge | `src/pages/settings/ReleaseNotes.vue`, `src/components/banners/UsTapeLaunchHero.vue`, `src/constants/releases.constant.ts` | [Super Search](./super-search-and-settings.md) `set-notes` | 2026-11-09, `32dd0c6354`, `4.53.0 Latest Spotlight The US tape.` first; before that 2026-11-07, `dced88e06a`, 82 versions, `4.53.0 Latest Spotlight The US tape.` first; before that 2026-11-06, `8bcd72f8f5`, 82 versions, `4.53.0 Latest Spotlight The US tape.` first; its badge opened the spotlight and `Open AAPL on Trades` charted POLYGON `AAPL/USD`; before that 2026-11-05, `87a325f4ab`, `4.49.0` newest; the scroll box 2026-11-03 | `4.52.0` (`Trade futures.`), `4.51.0` and `4.50.0` are audience-filtered; a guest never gets a spotlight at boot (no account creation date); announcements are not rendered (`src/store/announcements.ts`) |
| Guest sign-in wall and feature-aware signup prompt; since `4b8f78a775` one sign-in card, a sheet with a welcome line and provider pills | `src/components/dialogs/LoginSignupDialog.vue`, `src/components/dialogs/login-signup-dialog/AuthFormView.vue`, `src/store/dialog.ts`, `src/store/guest-prompt.ts` | [Super Search](./super-search-and-settings.md) `guest-wall` | 2026-11-05, `87a325f4ab`, the sheet from the camera's `screenshot` wall with `login-signup-turnstile`; `Email me a code` disabled empty, enabled after an email on clean traffic (not submitted); before that 2026-11-04, `8436920004`, the sheet from the Watchlist seat (`login-signup-welcome-spoken`, `auth-mascot`), its password pane, `Escape`, the `alert`, `indicators` (pane merge) walls; 2026-11-03, `215896e614`, the doors in this table's walls (`indicators`, `multi-chart`, `light-mode`, `alert`, `chart-actions`, `watchlist`, `terminal`, `news`, `community-chat`, `volume-footprint`, `script-editor`) | none for a guest lane |
| Sign in, sign up, code request with Turnstile, reset and verify | `src/pages/auth/auth.page.vue`, `src/components/dialogs/LoginCodePanel.vue` (`login-code-email-chip`, `login-code-welcome-handle`; `login-code-resend-btn` deleted) | unmapped | live verification pending | no agent-readable sign-in code or password; Turnstile fails under Playwright; a first factor's pending 2FA answer reaches the 2FA step and an expired pending 2FA sign-in restarts (`8aa30c96ab`, `5027d30d82`, source) |
| First-run onboarding: look and ask steps | `src/components/onboarding/FirstRunOnboarding.vue`, `src/components/onboarding/FirstRunLook.vue`, `src/components/onboarding/FirstRunAsk.vue` | unmapped | live verification pending | runs for a new account; a guest gets a light look (source); a Watchlist step joined as step 4 and after every Ask end (`243b283433`, `95596540de`, `src/components/onboarding/FirstRunWatchlist.vue`); since `ae42b69f6a` the steps also run on phones (`src/components/onboarding/phone/`, `first-run-ask-head`), a phone viewport this map does not drive |
| Delete and restore account | `src/pages/DeleteAccount.vue`, `src/components/dialogs/RestoreAccountDialog.vue` | unmapped | live verification pending | a signed-in throwaway account |
| Settings dialog: profile, security, appearance, timezone, trade and workspace settings | `src/components/dialogs/SettingsPagesDialog.vue` | unmapped (the guest pages are `set-shortcuts`, `set-notes` and the Preferences page below) | live verification pending | `ACCOUNT_SETTINGS` wall; 2FA needs `TWO_FACTOR`; the Trade page's fill-sound and idle menus are ComboBoxes since `18c8a69659` (source) |
| Pick a display language (13 locales since `ca141ab144`: pt-BR, fr, de, it, pl joined) and an appearance mode from the Preferences page | `src/pages/settings/LanguageSettings.vue`, `src/constants/locale.constants.ts`, `src/components/GlobalNav/LanguageButton.vue`, `src/composables/superSearch/providers/settings.ts` | [Super Search](./super-search-and-settings.md) `set-shortcuts` (the dialog's `settings-pages-nav-language-btn` page) | 2026-11-02, `a4488341f6`, the page opened for a guest: 13 `language-option-*`, `appearance-mode-{dark,gray,light,cream}`, 8 `preferences-theme-*` | a language pick hard-reloads the page (source) and was not clicked; Gray and Cream wall `light-mode` |
| Approve a device sign-in and see where it started | `src/pages/auth/authorize.page.vue`, `src/services/device-auth.service.ts` (`050bfc5940`) | unmapped | live verification pending | the route has no signed-in meta, so a guest reaches the shell; approving needs a device code and an account |
| Guided tour | `src/components/tour/GuidedTour.vue`, `src/store/guidedTour.ts` | unmapped | live verification pending | excludes guests; the Super Search command needs a verified email |
| Referrals | `src/pages/settings/Referral.vue` | unmapped | live verification pending | `REFERRALS` wall; the page lists every referral code and sums their counts (`163569b8cb`, `referral-code-row`, `referral-code-joined`) |
| Support center and contact | `src/components/dialogs/ReachOutPopoverContent.vue`, `src/components/dialogs/SupportInboxDialog.vue` | unmapped | live verification pending | `SUPPORT_CENTER` wall |
| Plus subscription, upgrade, trial and payment status | `src/pages/console/ConsoleSubscription.vue`, `src/components/dialogs/UpgradeDialog.vue`, `src/pages/PaymentStatus.vue` | unmapped | live verification pending | signed-in; `BILLING`; flags `free-trial`, `prepaid-plus-cn`, `plus-usdc-autopay`; a purchase refusal now names its reason (`849fb08e95`, `src/utility/billing/purchase-refusal.util.ts`), a failed renewal says paid access is paused (`bbb391f233`), and a partner discount badge follows the term (`b3a3ee935d`) |
| Developer console: plans, API keys, agents, usage | `src/pages/console/ConsoleLayout.vue` | unmapped | live verification pending | signed-in; `API_KEY`; flag `api-console` |
| Connect an AI agent | `src/components/dialogs/ConnectAgentDialog.vue`, `src/components/footer/FooterAgents.vue` | unmapped | live verification pending | `AGENTS`; flag `agents-surface` |
| Alerts panel opens; creating an alert | `src/components/alert/AlertSidebar.vue`, `src/components/alert/AddAlertMenu.vue` | [panels](./right-side-panels.md) `rp-alerts` | 2026-11-09, `32dd0c6354`, the panel from `tb-panels-row-alerts` with no wall; before that 2026-11-07, `dced88e06a`, the panel from `tb-panels-row-alerts` with no wall; before that 2026-11-05, `87a325f4ab`, the panel from `tb-panels-row-alerts` and its History tab (no `alert-history-undelivered`); before that 2026-11-04, `8436920004`, the panel, `alert-list-create-btn`, `alert-add-menu-price-btn` walling `alert` | creating, listing and delivery need a signed-in session; the US options alert lane is retired with one flat refusal (`b059e70852`; the `opra-alerts` flag is gone) |
| Notifications panel | `src/components/GlobalNav/NotificationPanel.vue` | unmapped | live verification pending | `NOTIFICATION` wall; a fired alert opens its market from its toast, notification row and web push (`9f12f38b7d`, `src/components/notification/content/fired-alert-open.util.ts`) |
| Drawing tools and the floating toolbar | `src/components/toolsSidebar/ToolsSidebar.vue`, `src/components/toolsSidebar/FloatingToolbar.vue` | [drawing tools](./drawing-tools.md) `dt-*` | 2026-11-09, `32dd0c6354`, trend line (two clicks), 16 `tqb-*`, `tool-props-lineStyle-select` still `Solid` after a `1m` switch (the card's value; the line's pixels not compared); before that 2026-11-08, `943281a2eb`, trend line (two clicks), 16 `tqb-*`, the gear's card with its `Style` ComboBox set to `Dashed` (`dt-settings`); before that 2026-11-07, `dced88e06a`, trend line (two clicks), 16 `tqb-*`, `Delete` removed it; before that 2026-11-05, `87a325f4ab`, trend line (two clicks), 16 `tqb-*` handles, `tqb-more-menu` eight rows, `tqb-remove-btn`; before that 2026-11-04, `8436920004`, trend line (two clicks), `tqb-templates-btn` and its list (`20b0fce8b3`), the one-layer `Escape` (`9033deb4d9`), `tqb-more-menu` (eight rows, no `-templates`), `tqb-remove-btn`; the right-click menu 2026-11-03; the colour popover, fib row and magnet 2026-11-02 | favorites and their drag reorder need `FAVORITES`; drawing sync (`drawings-sync:<scope>`), the Shift constraint (`87e6a66297`, engine-side), the log-scale flip and the vertical and cross lines' resting axis labels (titan 1214) not driven; a flipped or mirrored Bar Pattern's points and paste (`59f8cd229b`) not driven |
| Object tree | `src/components/objects/ObjectsLayout.vue` | [panels](./right-side-panels.md) `rp-objects` | 2026-11-09, `32dd0c6354`, opens with no wall; before that 2026-11-05, `87a325f4ab`, opens with no wall; before that 2026-11-03, `215896e614`, opens with no wall (no `panel-header-title`); the handles 2026-11-02 | none |
| Replay | `src/components/replay/ReplayOverlay.vue`, `src/composables/chart/useReplayToggle.ts` | [panels](./right-side-panels.md) `rp-walled` (the wall only) | 2026-11-09, `32dd0c6354`, the Panels row raised `chart-actions`; before that 2026-11-07, `dced88e06a`, the Panels row raised `chart-actions`; before that 2026-11-05, `87a325f4ab`, the Panels row raises the `chart-actions` wall; before that 2026-11-03, `215896e614`, the Panels row raises the `chart-actions` wall | a signed-in session, then the tier budget in `useReplayToggle` |
| Multi-chart grid, monitors and Trinity layouts | `src/composables/chart/useMonitorPicker.ts`, `src/components/chart/TrinityBar.vue` | unmapped (the picker is `tb-layout`) | live verification pending | `MULTI_CHART`, `MONITOR` walls; Trinity is a Super Search command |
| Workspace tabs: new, rename, duplicate, delete, import, share | `src/components/GlobalNav/workspace-tabs/WorkspaceTabStrip.vue`, `src/components/GlobalNav/workspace-tabs/WorkspaceNewTabMenu.vue` | unmapped | live verification pending | `WORKSPACE` wall; mutates an autosaving workspace; since `47879b68c1` a layout saved in another tab is adopted instead of raising the conflict banner (two signed-in tabs) |
| Layouts window rebuilt as lists plus an Explore catalogue of templates (`5db5e38f15`); community publish | `src/components/dialogs/LayoutsDialog.vue`, `src/components/layouts/explore/ExplorePane.vue`, `src/components/dialogs/ApplyLayoutDialog.vue`, `src/components/dialogs/LayoutPublishDialog.vue` | [Super Search](./super-search-and-settings.md) `guest-wall` (the Explore row) | 2026-11-02, `a4488341f6`, the Super Search `Explore` row raised the `workspace` wall for a guest | `WORKSPACE` and `INDICATORS` walls inside the dialog (source); `LayoutsCoverFlow.vue`, `WorkspaceDetailView.vue` and `LayoutMenuRow.vue` are deleted; Explore shows each template's own capture and its share of this week's uses (`c4a50b5d69`), ranked in the server's order (`922ede51f6`), source |
| Right-side panel grid and panel picker | `src/components/panels/RightSideGrid.vue`, `src/constants/panels.constants.ts` | [panels](./right-side-panels.md) (the toggles are `tb-bar-toggles`) | 2026-11-09, `32dd0c6354`, 17 rows on BINANCE.F BTCUSDT plus `tb-panels-row-tape-on`, the seven walls unchanged, Orderbook, Alerts, ETF screener, Market Stats, Journal and Objects with no wall; on AAPL 16 rows with `tb-panels-row-heatmap` `aria-disabled`; before that 2026-11-08, `943281a2eb`, 17 rows on BINANCE.F BTCUSDT plus `tb-panels-row-tape-on`, the `watchlist` and `script-editor` walls, Market Stats with no wall; before that 2026-11-07, `dced88e06a`, 17 rows on COINBASE BTC-USD plus `tb-panels-row-tape-on` while the Tape was open, the seven walls unchanged; before that 2026-11-05, `87a325f4ab`, 17 rows on COINBASE BTC-USD; seven walls and the rest open; before that 2026-11-04, `8436920004`, 17 rows on COINBASE BTC-USD; ten open and seven walled 2026-11-03 | signed-in content of each panel |
| Scanner and Markets panels (the old Terminal tabs; the Terminal toggle is retired) | `src/constants/panels.constants.ts` | [panels](./right-side-panels.md) `rp-walled` (Scanner's wall only) | 2026-11-09, `32dd0c6354`, Scanner raised `terminal`; before that 2026-11-07, `dced88e06a`, Scanner raised `terminal`; before that 2026-11-05, `87a325f4ab`, Scanner raises the `terminal` wall; before that 2026-11-03, `215896e614`, Scanner raises the `terminal` wall | a signed-in session; Markets is not offered to a guest and needs an eligible chart |
| Orderbook ladder, DOM, delta and heatmap | `src/components/orderbook/Orderbook.vue`, `src/composables/chart/useHeatmapToggle.ts` | [panels](./right-side-panels.md) `rp-orderbook`, `rp-heatmap` | 2026-11-09, `32dd0c6354`, `orderbook-canvas` and `orderbook-source-btn` on BINANCE.F BTCUSDT; before that 2026-11-08, `943281a2eb`, `orderbook-canvas` and `orderbook-source-btn` on BINANCE.F BTCUSDT; before that 2026-11-07, `dced88e06a`, the DOM ladder live on COINBASE BTC-USD, no `orderbook-*delay-notice`; before that 2026-11-05, `87a325f4ab`, `orderbook-canvas` on BINANCE.F ETHUSDT once the tab was re-fronted; before that 2026-11-04, `8436920004`, the ladder on BINANCE.F ETHUSDT (`orderbook-canvas`); the mid row 2026-11-03; the heatmap wall 2026-11-02 | `ORDERBOOK_DELTA`, `ORDERBOOK_HEATMAP` walls; the ladder does not mount while the tab is hidden (40 s blank); the CME first-paint seed (`795ed05bfe`) and a venue pick in `orderbook-source-btn` not driven; the book heatmap's colour scale follows the data (`4eb1324155`, canvas only, source) |
| Options panel: Levels, Flow, Volatility and Chain; Options Heatmap | `src/components/TickerBar/TBOptionsButton.vue`, `src/utility/options/options-panel-gate.util.ts`, `src/indicators/controls/options-heatmap/data-source.ts`, `src/composables/superSearch/providers/panels.ts` | [panels](./right-side-panels.md) `rp-options` | 2026-11-09, `32dd0c6354`, `tb-options-btn` raises the `terminal` wall; before that 2026-11-05, `87a325f4ab`, `tb-options-btn` raises the `terminal` wall; before that 2026-11-02, `a4488341f6`, the button's `terminal` wall | a signed-in session; flag `options-panel`; OPRA data needs flag `opra`; the Options Heatmap's dealer-flow basis (`7ccb568d29`) and node-size and ink sliders (`b6a26346c4`) need OPRA or CME options data |
| Option chain browser page | `src/pages/options/OptionsChainPage.vue` | unmapped | live verification pending | signed-in route |
| Options flow tape | `src/components/options/OptionsFlowTape.vue` | unmapped | live verification pending | a launch needs a resolved chain (`launchable`) |
| ETF screener | `src/components/etf-screener/EtfScreenerPanel.vue` | [panels](./right-side-panels.md) `rp-etf` | 2026-11-09, `32dd0c6354`, opens with no wall; before that 2026-11-07, `dced88e06a`, opens with no wall; before that 2026-11-05, `87a325f4ab`, opens with no wall (rows not read); before that 2026-11-03, `215896e614`, opens with no wall (rows not read) | the dev backend's ETF universe was empty again; saving a screen needs an account |
| OPRA and CME data purchase, registration and terms | `src/components/options/CmeTermsDoor.vue`, `src/components/options/OpraDelayDoor.vue`, `src/components/options/OpraRealtimeCard.vue`, `src/components/dialogs/market-data/MarketDataPurchaseFlow.vue` | unmapped | live verification pending | `BILLING`; flag `opra`; a purchase; the real-time US stocks add-on is priced at $19 a month (`a0a6189c82`); the CME declaration asks each country's own postal address and refuses one it cannot file (`95d04c8db5`, `src/components/options/CmeAttestationPage.vue`, `usePostalAddressForm.ts`) |
| Tape mode and the 1s interval | `src/composables/chart/useTapeMode.ts` | unmapped | live verification pending | `ONE_SECOND_INTERVAL`; `TAPE_MODE` on mobile |
| Footprint and TPO, including the TPO outline display mode; TPO follows the chart's session with sessions on their city clocks (`b9cc632661`, `af3004b625`) | `src/composables/chart/chartTypePick.ts`, `src/components/dialogs/TimePriceOpportunityDialog.vue`, `src/indicators/controls/tpoSettingsTabs.ts`, `packages/wrun-chart-host/src/indicators/controls/tpo-session.util.ts` | [indicators](./indicators.md) `ind-legend` (the TPO session bullet); the rest unmapped (the Footprint panel's wall is `rp-walled`) | partial, 2026-11-05 on `87a325f4ab`: a guest's programmatic TPO stored `tradingHour` `null` and its card listed `Chart session` first, then the New York, Tokyo and London sessions; the profile itself and the footprint not driven | `VOLUME_FOOTPRINT` (the Panels row raised it 2026-10-29), `TIME_PRICE_OPPORTUNITY` walls; the regular TPO now marks each profile's open and close block (`cb070d70a5`, `src/indicators/controls/tpo-open-close.util.ts`, Color tab `highlightOpen` / `highlightClose`); the footprint gained a Candle position setting (`candlePosition`, `bb06598aef`), a Mid stats row (`b496ab5650`) and a Row size auto that follows symbol and interval (`5055c750d6`), source |
| The Tape (one tape for every market, with its docked Liquidations and a Heatmap view; the Trades and Liquidations panel is retired, `ad67d47c62`); market, volume and liquidity stats | `src/components/trades/Trades.vue`, `src/components/trades/CryptoTapePanel.vue`, `src/components/trades/TapeLiquidations.vue`, `src/components/trades/TapeSoundSettings.vue`, `src/utility/panels/trade-liquidations-to-tape.util.ts`, `src/components/tradingVolume/Stats.vue` | [panels](./right-side-panels.md) `rp-tape`, `rp-stats` | 2026-11-09, `32dd0c6354`, `crypto-tape-panel` on COINBASE BTC-USD (`75,849.8▼`) with `tape-liquidations`, no `tape-delay-notice`; before that 2026-11-07, `dced88e06a`, `crypto-tape-panel` on COINBASE BTC-USD (`75,755.95▼`) with `tape-liquidations`, no `tape-delay-notice`; before that 2026-11-06, `8bcd72f8f5`, the Tape printing on COINBASE BTC-USD (`75,891.40`) with `Liquidations` (`No liquidations today`); before that 2026-11-05, `87a325f4ab`, on BINANCE.F ETHUSDT (`2,418.50▲`) with `tape-liquidations`; 2026-11-03: the markets menu's `tape-markets-follow-btn`; the stats panels opened | the sound control (`tape-sound-*`, `ba8e2cc280`) was not in a guest's panel DOM; the old `CEXTradesStream` is the fallback for CME, OPRA, formulas, on-chain pools and a US stock whose tape lookup failed (driven 2026-11-06: an unrouted stocks gate showed `AAPL/USD`, `No trades match filters`); the crypto Tape uses the `stock-tape-row*` testids too; the whole family sits on `Waiting for …` during a gateway outage |
| News feed and synoptic streams; the header's Sort menu and Customize (`0d62414892`) | `src/components/topic-feed/TopicFeedPanel.vue` (`topic-feed-sort-btn`) | unmapped (the wall is `rp-walled`) | live verification pending | `NEWS` wall (driven 2026-11-03); flags `feeds`, `synoptic-streams`; Synoptic posts can be pinned on a chart, chosen per chart (`eb8c278a1d`) |
| Add a paid Live Series feed from the indicator detail panel, buy it, see publisher-tier prices (`3d003b1c67`) | `src/components/dialogs/indicator-dialog-v2/IndicatorDetailPanel.vue`, `src/components/dialogs/marketplace/EmbeddedCheckoutDialog.vue`, `src/services/feeds.service.ts`, `src/utility/chart/feed-catalog.util.ts` | unmapped | live verification pending | flag `feeds`; adding walls a guest on `INDICATORS`; buying needs a signed-in session |
| A kick dialog names the session that took over, with its device label (`b97be8f4b6`) | `src/components/dialogs/SessionKickedDialog.vue`, `src/components/dialogs/SessionTakeoverDetails.vue`, `src/composables/live/useSessionTakeover.ts` | unmapped | live verification pending | a second session on the same account; a guest gets no superseded frame |
| Market events, earnings calendar and the chart event lane | `src/components/earnings/EarningsPanel.vue`, `src/components/chart/ChartEventLane.vue` | unmapped | live verification pending | a signed-in session |
| Tweet callers bar | `src/components/tweet-callers/TweetCallerBar.vue` | unmapped | live verification pending | `TWEET_CALLERS` wall |
| Journal | `src/components/journal/JournalLayout.vue` | [panels](./right-side-panels.md) `rp-journal` | 2026-11-09, `32dd0c6354`, opens with no wall; before that 2026-11-07, `dced88e06a`, opens with no wall; before that 2026-11-05, `87a325f4ab`, opens with no wall; before that 2026-11-03, `215896e614`, opens with no wall | writes are gated on a guest session (source); entries need an account |
| Hyperliquid account dock, trade rail and order ticket; the Balances tab as one list of holdings by account, named wallets and moving funds between them (`47525136bd`, `b0d7a91522`) | `src/components/hyperliquid/trade/HLTradeTicketPanel.vue`, `src/components/hyperliquid/account-panel/HLAccountDock.vue`, `src/components/hyperliquid/account-panel/HLBalancesTab.vue`, `src/components/dialogs/HLTransferSheet.vue`, `src/components/trading-hub/AccountMenu.vue` | unmapped (the desktop map covers the shell's wallet handoff) | live verification pending | flag `ems-hyperliquid`; a funded testnet wallet; the account menu now reaches HIP-3 (`40a1989b6e`) and is signed-in only; each TP/SL leg shows its estimated p&l on every venue (`9c4f8d1354`, `src/utility/trading/leg-pnl.util.ts`) and the desktop positions strip hides from its X or the bottom bar (`42e5d7bb2d`, `src/components/footer/FooterPositionsToggle.vue`); the Transfer sheet reads both wallets and hides on a unified account, and View-as follows the chart in the account drawer (`49461bebcd`, `491a767b82`, `b5b985d075`, `65d202b563`) |
| Trading hub, CEX connect, paper trading and new venues | `src/components/trading-hub/TradingHubDialog.vue`, `src/components/dialogs/CexConnectDialog.vue`, `src/components/cex/link/`, `src/utility/cex/paper/paper-flag.util.ts` | unmapped | live verification pending | flags `trading-hub`, `paper-trading`, `robinhood-trading`, `lighter-execution`, `variational-markets`; paper trading also needs a signed-in user; paper now runs on Binance futures, Bybit and Hyperliquid perp charts with funding and a server-synced book (`96c64ceeb2`, `9051480dae`, `c30e9afe1c`, source); CME futures order entry with live-quote paper fills and fill markers (`d0017347a8`, `eb57b298b1`) |
| Trading Volume page | `src/components/trading-hub/VolumePage.vue`, `src/composables/tradingVolume/useTradingVolume.ts` | unmapped | live verification pending | flag `TradingVolume` (dark in production) |
| Pulse board, token overview and onchain swap | `src/pages/pulse/PulsePage.vue`, `src/components/tokenOverview/TokenOverviewPanel.vue` | unmapped | live verification pending | a signed-in session |
| Marketplace store, purchases and seller hub; publish, key, price and manage a feed from the Sell tab (`182e34b3d0`) | `src/components/marketplace/MarketplaceStoreLayout.vue`, `src/components/marketplace/sellerHub/feeds/SellerHubFeeds.vue`, `src/services/feeds-publish.service.ts` | unmapped | live verification pending | signed-in route; the feed screens need flag `feeds` and a seller session; the creator docs link is the public guide (`9c8e4fb26f`); a paused Indicator relists at a new price, and registry refusals are worded (`45873d66d2`, source) |
| Sharing hub and the My access page | `src/components/sharing/SharingHost.vue`, `src/pages/MyAccessPage.vue` | unmapped | live verification pending | flags `sharing-hub`, `my-access`; signed-in route |
| Kata AI assistant | `src/components/kata/KataPanel.vue` | unmapped | live verification pending | `KATA` wall |
| Ask: plan cards and apply; reading each part of a request in any language and the common questions (`88a347d270`, `217811fe2c`) | `src/ask/execute/plan.ts`, `src/ask/pick/` (`8826196f40`: Jev picks the do lane from the feature registry; `decide/route.ts` and `decide/parts.ts` are deleted), `src/ask/extract/language.ts`, `src/composables/superSearch/useSuperSearch.ts` | unmapped | live verification pending | a signed-in session (a guest gets no plan card, driven 2026-10-28, and no starters, 2026-11-02); a how-to question now gets the Apply card and fragments get command chips (`e21fa5b62c`), both on the signed-in Ask lane; zoom-reset and go-to-date are Ask-only verbs (`e973f00e50`) |
| Community chat and DMs | `src/components/chat/CommunityChat.vue` | unmapped (the wall is `rp-walled`) | live verification pending | `COMMUNITY_CHAT` wall (driven 2026-11-03) |
| Go live, streams and spectating | `src/components/collab/GoLiveButton.vue`, `src/pages/LiveStreams.vue` | unmapped | live verification pending | `GO_LIVE`, `FOLLOWING`; signed-in routes |
| Author profiles and people search | `src/pages/AuthorProfile.vue`, `src/composables/superSearch/providers/people.ts` | unmapped | live verification pending | `AUTHOR_PROFILE`; people search needs a signed-in session and flag `people-search` |
| Board (Academy) | `src/pages/academy/AcademyPage.vue` | unmapped | live verification pending | signed-in route; flag `om-board`, default off |
| Chart clips: record a voiced clip (a video of the pane with a chart snapshot since `54331e6699`), post it to the Board, replay it | `src/components/clips/ClipRecordButton.vue`, `src/clips/recorder/useClipRecorder.ts`, `src/components/academy/AcademyAttachmentCard.vue`, `src/composables/academy/useChartClipsFlag.ts` | unmapped | live verification pending | flags `om-board` AND `chart-clips` (`02c3fa9c01`) and a server flag; signed-in; no clip button for a guest (2026-10-28, 2026-11-02); since `6b7ef2cd2a` a clip replays the author's surfaces, typed text, clicks and keys, with no voice holds; phase 6 (`d5d9e33713`) adds the Board's clip wall (`/board/clips`, `clips/:id`, `setup/:key`, `c/:slug`; a guest open of `/chart/board/clips` landed on `/chart/`, driven 2026-11-02) and the gesture, hand and camera fixes (`ec8e001d2d`, `479b782d5c`, `f63becdf6a`, `79b1c41da2`, `f6e068a812`); since `501a37fc9c` a recording whose private lines cannot be hidden is refused or discarded (`src/clips/recorder/clip-privacy.ts`, source) |
| A clip's public page: the clip as a video (`54331e6699`), title, author, market and Copy link; a private or unknown clip says so | `src/pages/ClipGuestPage.vue`, `src/components/clips/ClipVideoPlayer.vue`, `src/services/academy-guest.service.ts`, `src/router/routes.ts` (`ClipGuest`, `authorized: false`) | [clip guest page](./clip-guest-page.md) `clip-private` | 2026-11-09, `32dd0c6354`, `/chart/clip/zzz` private state with `clip-guest-home-link` back to the chart; before that 2026-11-08, `943281a2eb`, `/chart/clip/zzz` private state with `clip-guest-home-link`; before that 2026-11-07, `dced88e06a`, `/chart/clip/zzz` private state and its home link back to the chart; before that 2026-11-05, `87a325f4ab`, `/chart/clip/zzz` private state, no `clip-video-player`, no wall; before that 2026-11-04, `8436920004`, `/chart/clip/zzz` rendered `clip-guest-page` with `clip-guest-private` and `clip-guest-home-link`, no wall | a published clip id for the player; Take over, Open the chart and Reply go to `/auth?redirect=/board/clips/<id>` |
| A stuck data socket heals itself, and the connection chip offers Reconnect and Reload (`e2967128e2`) | `src/components/common/ConnectionStatusChip.vue`, `src/composables/live/useConnectionLatency.ts`, `src/utility/v2/socket-storm-census.util.ts` | [boot](./chart-boot-and-data-plane.md) Gotchas | 2026-11-05, `87a325f4ab`: on desktop the yellow `connection-strip` (`offline`, `back`, and `long` with `connection-strip-reload` during a real gateway loss); the chip stayed absent; before that live verification pending; the chip's absence on a healthy lane driven 2026-11-04 | since `734d51a814` one glyph per state (`data-glyph`, `conn-chip--<tone>`) and a slow start reads `Slow network`; since `7728b5fcf6` a method storm is counted at the wire, 150 in 30 s (source); a degraded socket (`reconnectEligible`: status `reconnecting`, the candle socket not open, an establish timeout or failure); the 2026-11-01 gateway outage is the state that shows it; since `0c4e1493f7` the chip also reads `Slow network` (`slowNetwork`) while the data worker is slow, suppresses Reconnect while it is stalled or replacing, and offers Reload when it is exhausted (source) |
| The top-bar Layouts menu keeps its rows where they first draw (`f4c9e56e82`) | `src/components/GlobalNav/layouts/LayoutsMenu.vue` | unmapped | live verification pending | handles `layouts-menu-{recent-held,open-tab,layout,search,grid,pinned,close-<id>,keep-<id>-btn,scratch}` (source); saved layouts need a signed-in session |
| Screenshot and chart-data export; symbol watermark | `src/components/dialogs/ScreenshotDialog.vue`, `src/components/dialogs/ExportChartDataDialog.vue`, `src/components/chart/SymbolWatermarkHost.vue` | unmapped (the guest wall is `guest-wall`) | live verification pending | `SCREENSHOT` wall (driven 2026-10-29); since `d4a385ff9d` a Playwright lane counts as a screenshot renderer only with `__omScreenshotRenderer` planted, so `?screenshot=1` there gets the free-tier clamp; since `96282b0cfd` a picture is taken in place without freezing the page (`src/utility/screenshot/in-place-capture.util.ts`; the off-by-default `screenshot-legacy-capture` flag keeps the old path): source, the dialog is walled for a guest; since `1abaabad8d` a picture names who sees it, and `cc10dab607` and `b2dfd0bbf1` keep its temporary changes off the live chart (source, the dialog is walled) |
| Simple mode, light charts and Layers | `src/composables/chart/useSimpleMode.ts`, `src/store/layers.ts` | unmapped | live verification pending | `SIMPLE_MODE`; flag `layers` |
| Strategy tester | `src/components/strategy-tester/StrategyTesterPanel.vue` | unmapped | live verification pending | gate not checked |
| History cap and Manage history | `src/utility/chart/history-cap.util.ts`, `src/components/dialogs/ManageHistoryDialog.vue` | unmapped | live verification pending | `CHART_HISTORY` wall |
| Beta invite and partner landings | `src/pages/BetaInvite.vue`, `src/pages/Partners.vue` | unmapped | live verification pending | an invite id; a partner referral |
| Script registry SSO handoff | `src/pages/RegistrySso.vue` | unmapped | live verification pending | a signed-in session |
| App commands as Super Search rows (hide candles, swap candle colours ...) | `src/composables/superSearch/providers/askCommands.ts`, `src/ask/commands/catalog.ts`, `src/ask/commands/rows/chart.ts` | [Super Search](./super-search-and-settings.md) `ss-ask-commands` | 2026-11-03, `215896e614`, `candles-visible:off` then `:on` for a guest (`metadata[0].isHidden` true then false) | each row's own `available()`; `alert lines` lists nothing for a guest |
| Package share links: `?indicator=` and a chartless `?wrunRef=` | `src/router/guards/wrun-ref-root-link.guard.ts`, `src/utility/sharing/indicator-share-link.util.ts` | [indicators](./indicators.md) `ind-share-link` | 2026-11-02, `a4488341f6`, `?wrunRef=@om-core/trend-candles` stripped from the URL, the `indicators` wall, the package stashed in `sessionStorage` | the dialog opening on the package needs a signed-in session |
| Open Interest Profile Net and Split display modes | `src/indicators/controls/MetricProfileSettings.vue`, `src/utility/chart/metric-profile.util.ts` | [indicators](./indicators.md) `ind-legend` | 2026-10-28, `29c9cda0a2`, the `Display mode` field (`Net`) on a programmatic mount | `Split` not opened; a dialog-path add needs a signed-in session |
| The symbol search leaves an input-method composition alone | `src/utility/dom/ime-composition.util.ts`, `src/components/symbolSelection/SymbolSelectionDialog.vue` | [symbol search](./symbol-search-and-ticker-bar.md) `sym-ime` | 2026-11-01, `120d5d5d32`, synthetic composition events; a composing `Escape` with `code` set keeps the dialog open, `compositionend` uppercases to `ETH`, a plain `Escape` closes it | a real input method not driven; a synthetic composing `Escape` without `code` still closes the dialog (the filter skips an empty `code`) |
| Built-in options indicators open as window cells | `packages/wrun-chart-host/src/utility/chart/window-owner.leaf.ts`, `src/composables/chart/useIndicatorMenu.ts` | unmapped (a source note in [indicators](./indicators.md) Gotchas) | live verification pending | options data needs a signed-in session |
| Saved chart themes: delete from the theme row with Undo | `src/components/dialogs/ChartThemeRow.vue`, `src/store/my-themes.ts` | unmapped | live verification pending | a saved theme, probably account-only (source not read far enough) |
| Trade prediction markets through a Polymarket lane; create the deposit wallet, approve trading on it and fund it from a sheet (`b27526f353`, `4ea9f85b26`, `ae9e5ae7a6`) | `src/composables/superSearch/providers/polymarket.ts`, `src/components/dialogs/PolymarketConnectDialog.vue`, `src/components/polymarket/link/PmLinkFundBlock.vue`, `src/components/polymarket/trade/PredictionTicketPanel.vue`, `src/components/polymarket/account/PredictionAccountPanel.vue`, `src/utility/polymarket/pm-venue-flag.util.ts` | unmapped | live verification pending; no `Link Polymarket` row for a guest (2026-10-28); a guest can chart Polymarket events through the Predict tab (`sym-predict`, 2026-11-01) | flag `polymarket-execution` and a signed-in session; a linked Polymarket account; since `004429d11c` a user links with a wallet and trades through a session key, `10c9c26834` redeems a resolved market from Positions, `95330816c9` makes market orders one field; `7fe104cb52` withdraws pUSD from the deposit wallet in-app (`src/components/dialogs/PmWithdrawSheet.vue`, `dialogStore.pmWithdrawSheet`) and `c9554d855d` makes the deposit address the copy control in one funding card |
| "What should we build next" feedback banner | `src/components/banners/BuildNextBanner.vue`, `src/utility/feedback/prompted-question-schedule.util.ts` | unmapped | live verification pending; absent for a guest (2026-10-28) | a signed-in account past its signup day, then the prompt schedule |
| Undo and redo chart changes from the footer: symbol switches and compares, interval, chart type, chart settings, session, price scale and the Volume row, each step named in the button | `src/components/footer/FooterUndoRedo.vue`, `src/composables/chart/useUndoRedoControls.ts`, `src/store/undo-redo.ts`, `src/store/undo-redo-swap.ts`, `src/utility/undo/undo-step-label.ts` | [ticker bar](./symbol-search-and-ticker-bar.md) `tb-undo` | 2026-11-07, `dced88e06a`: `Undo Change symbol` back from the option and from AAPL, `Undo Change interval`; before that 2026-11-05, `87a325f4ab`: `Undo Change symbol` back from the option put and from EUR/USD, `Redo Change symbol` forward again; before that 2026-11-04, `8436920004`: `Undo Change symbol` back from the option put to COINBASE BTC-USD and `Undo Change interval` back to `1h`; `Undo Change chart type` 2026-11-03 | none for a guest (`Footer.vue` mounts the pair with no gate); chart settings, session, price scale, Volume, `drawingsLocked` and `drawingsHidden` steps not driven; the phone drawing bar has its own pair (`a7cc3ed7e6`) |
| Moving average ribbon built-in | `src/indicators/controls/ma-ribbon/index.ts`, `src/indicators/controls/ma-ribbon/MaRibbonSettings.vue` | [indicators](./indicators.md) `ind-add` | 2026-11-03, `215896e614`, a programmatic `MA_RIBBON` mount read in the legend; the four SMA lines 2026-11-01 | a dialog-path add needs a signed-in session |
| Merge an off-chart pane into another (open to every plan since `ee80751357`; the Plus prompt is gone) | `packages/wrun-chart-host/src/constants/feature-limits.constants.ts` (`paneMerge`), `src/utility/chart/pane-merge.util.ts`, `src/instances/titan-charts.ts` | [indicators](./indicators.md) Gotchas | the wall only, 2026-11-04 on `8436920004`: a guest's `legends.mergePaneBtn` click on the Agg. Funding Rate pane raised `indicators`, no Plus text | a signed-in session for the target picker and the merge (`settings.hostPaneId`) |
| A spot pane refuses Open Interest, Funding Rate and Liquidations and says which data it lacks (`cdfa9c212d`) | `src/store/chart.ts` (`RESTRICTED_MODES` spot row, `handleIndexModeErrorMessage`), `src/constants/tradfi.constants.ts` (`SPOT_BLOCKED_INDICATORS`), `src/utility/exchange/derivative-venue.leaf.ts` | [indicators](./indicators.md) Gotchas | partial, 2026-11-04 on `8436920004`: a guest's programmatic mounts on COINBASE BTC-USD went gated hidden, but the engine message read `No data in range` / `Slow network` and no `Needs … data` text showed (possible product gap) | the dialog-path add needs a signed-in session; the aggregated and sector versions stay allowed (Agg. Open Interest drew) |
| Move an indicator between the price pane and its own pane (`66450484c2`, `fbb32ff5c2`: VWAP and the MA ribbon, from the legend menu or the chart right-click menu) | `src/composables/chart/useIndicatorMenu.ts`, `src/components/chart/IndicatorMenu.vue`, `src/components/chart/ChartContextMenu.vue` | [indicators](./indicators.md) Gotchas | the wall only, 2026-11-02 on `a4488341f6`: `indicator-menu-pane-move` (`Move to new pane`) in the legend's `indicator-menu` raised the `indicators` wall and the ribbon stayed `onchart` | `promptGuestLogin(FeatureId.INDICATORS)` guards the move; on 2026-11-03 the pin move (`Move to price pane` on the Bitcoin Dominance pane) raised the same wall; a signed-in session, then the overlay's `type` and the Objects panel's `PANE n` badge as proof |
| A late indicator read says why in its legend row, with a counter and Retry | `src/utility/chart/indicator-status-chips.util.ts`, `src/utility/chart/legend-chip-label.util.ts` | [indicators](./indicators.md) `ind-legend` | live verification pending | needs a stalled read (5 s with evidence, 15 s without); no deterministic guest trigger found |
| A stale cached frame paints dimmed at its true time until the fresh rows land | `src/utility/chart/cached-paint-dim.util.ts`, `src/components/chart/ChartArea.vue` | [boot](./chart-boot-and-data-plane.md) `boot-candles` | live verification pending | a cached tail more than 3 bars old (`PAINT_WALL_AGE_BARS`); handles `cached-paint-veil`, `cached-paint-updating-chip` |
| kScript retired (`722911b50f`, `d7500721fc`, `4f7be7723c`): a kScript document opens nowhere (a 3 s toast at every door); a saved retired row leaves the chart at restore; a lossy twin conversion toasts a settings reset | `src/components/scriptEditor/shell/KScriptWorkspace.vue`, `src/store/editor-shell.ts`, `src/utility/chart/kscript-retired-rows.util.ts`, `src/components/chart/KscriptSunsetNotice.vue`, `src/utility/chart/kscript-sunset.util.ts` | [editor](./script-editor-and-kscript.md) Gotchas | live verification pending; the old chip, toast, card and frozen-bar handles confirmed absent 2026-11-02 on `a4488341f6` | a signed-in session with a saved kScript document; the read-only viewer and the frozen bar are deleted too (`4f7be7723c`); there is no date, mode or flag any more |
| US stocks consolidated tape: open to guests since `bda0563ab1` on the delayed lane; one search row per stock and the bare ticker (`a743605d03`, `8bcf77ee46`), no seconds intervals (`8465b1e6fb`), the feed chip, the go-live card on a delayed stock (`stock-go-live-card`, `e1f0b7f6ec`), the stock Tape (`Time and sales` with an exchange pick kept per pane, `4d47a06e31`) with Dark pool and Option flow sections that resize (`3e017f5fb8`), row cards (`13df67d37c`, `8ee5f2ea3c`) and a Heatmap view; dark pool prints on the chart (`daf25b86f0`), since `c106437eb7` and `841ea60455` an eye-only `Dark pool prints` legend row the open Dark pool section mounts on the chart the Tape follows (`useDarkPoolChartLayer.ts`; the eye writes `darkPoolOnChart`; collapse, Heatmap or Dark pool off removes it); the `4.53.0` launch spotlight (`1e65ffe94c`) | `src/constants/guest-default-flags.constants.ts`, `src/components/chart/StockFeedChip.vue`, `src/components/trades/StockTapePanel.vue`, `src/components/trades/StockTapeDarkPool.vue`, `src/components/trades/TapeRowCard.vue`, `src/components/trades/TapeDockResizeHandle.vue`, `src/components/trades/StockTapeHeatmap.vue`, `src/utility/stocks/us-equities-flag.util.ts` | [panels](./right-side-panels.md) `rp-stock-tape`; [symbol search](./symbol-search-and-ticker-bar.md) `sym-stock`; [Super Search](./super-search-and-settings.md) `set-notes` | partial, 2026-11-08 on `943281a2eb`: `asset-row-AAPL\|4-btn` charted AAPL, the merged feed chip read `Trades` with no timing span and no `Live ›` (stocks gate unrouted), and its menu listed `stock-feed-row-trades-all`, `stock-feed-addon-row` and the Price only group; before that, 2026-11-06 on `8bcd72f8f5`: the search row, the bare ticker, `stock-feed-chip`, the interval menu, the spotlight, and the stock Tape's chrome with the stocks gate routed (`stock-tape-delay-line`, `stock-tape-venue-selector-btn`, `stock-tape-dark-pool`, `stock-tape-option-flow`, both resize handles) | live verification pending for prints, the venue pick, the row cards, a resize, the Heatmap view and the on-chart dark pool lane: the operator's `.env.local` routes no stocks gate, and with `.env.sample`'s gate routed the gate answered nothing for this guest (`StreamMarkets timed out`) and the AAPL chart stalled; the go-live card, the feed switch and the purchase need a signed-in session; since `f8eff0c288` and `688e9254cc` the chip and the delay tag are one control (`stock-feed-chip-delay`, `stock-feed-chip-realtime`, Go live as `Live ›`); since `183e61b6ee` the dark pool prints row has a settings box (`Smallest print`, `Smallest flag`; source); since `445f656ade` the POLYGON vendor code is never printed as a venue: AAPL's head reads `EQUITIES · TRADES · ALL US EXCHANGES` (driven 2026-11-09); since `04f374a678` the dark pool layer stays on a full chart (source) |
| CME and Rithmic futures order entry; Rithmic order routing from the chart; the account panel's Fills tab and windowed Orders and Fills tables (`1c88224eff`) | `src/components/futures/FuturesTradeTicketPanel.vue`, `src/components/futures/FuturesAccountPanel.vue`, `src/store/rithmic-trading.ts`, `src/composables/superSearch/providers/rithmic.ts` | unmapped | live verification pending | flags `futures-trading`, `futures-byof-chart` and `futures-byof-history` together; Rithmic is dark (`aaf4fec58c`); a signed-in session and a venue account; `2a4ccfcefa` adds Rithmic ticket actions, a trailing stop, a Balances tab, a reconnect line and a sign-in sheet (`src/components/dialogs/RithmicConnectDialog.vue`), plus a futures order-confirmation setting and its palette row (`trade:futures-order-confirm`); one-press Rithmic trading with opt-in confirmations, Stay connected (on by default, kept 7 days), one Web Lock per Rithmic login, and the `4.52.0` launch spotlight behind the futures flag (`1620e44838`, `c8bda7a3b8`, `f01364a6a7`, `12f71dc90b`, `src/components/banners/RithmicLaunchHero.vue`); since `ffd247abed` a refused Rithmic login offers Message support and the Rithmic-login step comes first, and Stay connected Off holds across tabs (`b61a49a6f9`, `e15a04361f`, source) |
| CME user-authored chart studies (browser only) | `packages/wrun-chart-host/src/utility/chart/cme-user-scripts-gate.util.ts`, `src/utility/chart/cme-user-scripts-entitlement.util.ts` | unmapped (the CME twin of the OPRA row) | live verification pending | dark flag `cme-user-scripts`, an entitlement and a signed-in session |
| Sign-in return flags are spent from the address; `?twofa=true` opens the authenticator-code step (`dd6c6f4161`, `0a0d1b8313`) | `src/router/guards/sign-in-return.guard.ts`, `src/router/routes.ts` | [Super Search](./super-search-and-settings.md) `auth-return` | 2026-11-05, `87a325f4ab`: `/chart/?twofa=true` left a clean address and showed `twofa-verify-code-input`; before that 2026-11-04, `8436920004`: `/chart/?twofa=true` left a clean address, one navigation entry and `isOAuthTwoFADialogOpen` true, now the 2FA panel (`twofa-verify-code-input`, one field); `?oauth=true` 2026-11-03 | finishing the OAuth or 2FA sign-in needs a real account; the two-tab reload loop it fixes was not driven |
| Show on chart: pick what your own trading draws on every venue (`66a5bcb680`) | `src/components/footer/FooterShowOnChart.vue`, `src/components/chart/show-on-chart/ShowOnChartPanel.vue`, `src/composables/chart/useOwnChartPanes.ts`, `src/composables/superSearch/providers/featureCommands.ts` | unmapped | live verification pending; absent for a guest (no `footer-show-on-chart-btn`, driven 2026-11-03) | an own account drawing on a pane (a Hyperliquid wallet, an exchange credential or paper account, or a Rithmic session); handles `show-on-chart-panel`, `show-on-chart-row-<kind>`, `show-on-chart-group-<id>-btn`, `show-on-chart-hide-all-btn`, `show-on-chart-labels-btn` (source) |
| A US stock's Options chain row under its feeds (`9a0149e404`) | `src/components/symbolSelection/component/StockFeedBlock.vue`, `src/components/symbolSelection/component/VenuePanel.vue`, `src/utility/symbol-selection/option-chain-gate.util.ts` | unmapped (a source note in [symbol search](./symbol-search-and-ticker-bar.md) Gotchas) | live verification pending | `isSignedInSession()` and flag `opra`; the row routes to the signed-in `OptionsChain` page; a guest gets no row (source) |
| Liquidation profiles drawn like the reference with cluster labels, and the liquidation heatmap's Running total (`b273fa04f1`) | `src/components/TickerBar/TBHeatmapPanel.vue` (`tb-heatmap-running-total-btn`) | unmapped | live verification pending | the button shows only for a liquidation heatmap and is disabled in the `heatmap` display mode (source); the heatmap popover's settings need a signed-in session |
| A delayed market wears one quiet `Delayed N min` tag in its legend, and no band covers the newest bars (`b3503ffaba`) | `src/components/chart/CmeDelayBadge.vue` (`cme-delay-badge`; `CmeDelayGhostBars.vue` and `cme-delay-ghost*` deleted) | unmapped | live verification pending | a delayed CME chart; on 2026-11-04 the guest's `CME` tab failed to list contracts, so no CME chart was reached; since `63c1fa257a` and `688e2ff054` (source) one label per screen on CME, the stocks tape and OPRA: stocks and OPRA say `Delayed 15 minutes` verbatim, CME rows `{mins}m`; a panel shows its own notice (`orderbook-delay-notice`, `orderbook-dom-delay-notice`, `orderbook-delta-delay-notice`, `tape-delay-notice`, `watchlist-delay-notice`, `alert-create-cme-delay-notice`) only when no chart on screen labels the plane; POLYGON AAPL on a guest lane with no stocks gate wore no label anywhere (2026-11-07); the card's `stock-feed-add-realtime-btn` (stocks) and `opra-delay-notice-line` (OPRA) are existing handles; on a US stock the feed chip carries the words since `f8eff0c288` and `cme-delay-badge` stays hidden; on 2026-11-08 AAPL on a lane with no stocks gate showed neither |
| A session profile's Session pick shows each session's hours on its own city's clock, with an Asia / London / New York split (`ad5f2d57d3`, `c0da940874`, `907a3d6364`); an intraday session profile defaults to Daily (`13acd4683c`) | `src/indicators/controls/session-volume-profile/session-profile-fields.ts`, `src/utility/chart/market-sessions.util.ts`, `src/utility/chart/custom-session-window.util.ts` | [indicators](./indicators.md) `ind-session-default` | partial, 2026-11-06 on `8bcd72f8f5`: a programmatic `SESSION_VOLUME_PROFILE` on BTC `15m` read `Session Daily` (`settings.session` `86400000`, `sessionType` `null`) | the city-clock list and the `Sessions` split (30m or less) not driven; the `1d` fallback to Targeted not driven; the dropdown has no testids, match by label; CME session picks name only CME trade dates |
| A market order's TP/SL draws on the chart before it is sent; legs that wait on their entry share its fate (`740b798d59`, `f93d35895e`) | `src/composables/hyperliquid/useHLTicketDraftLine.ts`, `src/store/hyperliquid-trading.ts` | unmapped | live verification pending | a signed-in trading account (the Hyperliquid row's prerequisites) |
| A typed currency leads with its dollar pair; a typed metal or forex pair is listed at once (`105356d766`, `0b49c541a9`) | `src/utility/symbol-search-v2/forex-spot.util.ts`, `src/utility/symbol-search-v2/universe-quick-rows.util.ts` | [symbol search](./symbol-search-and-ticker-bar.md) `sym-forex` | 2026-11-05, `87a325f4ab`: `JPY` led `USD/JPY`, `eur` led `EUR/USD` (charted FX_OTC), the quick search's `XAUUSD` led its forex row within 1.5 s | none |
| NinjaTrader as the futures lane's second broker: a Super Search `Link NinjaTrader` row, the Connections page reached by `ninjatrader` or `tradovate`, a connect sheet, two-broker tickets (`3dd3e5d0c3`) | `src/components/dialogs/NinjaTraderConnectDialog.vue`, `src/composables/superSearch/providers/ninjatrader.ts`, `src/composables/superSearch/providers/settings.ts`, `src/utility/futures/ninjatrader-flags.util.ts`, `src/store/ninjatrader-trading.ts` | [Super Search](./super-search-and-settings.md) Gotchas (the guest absence only) | the guest absence only, 2026-11-07 on `dced88e06a`: `ninjatrader` listed no row and the guest settings nav has no Connections page | live verification pending: flags `futures-trading` and `futures-ninjatrader` (web only, off in the desktop shell), the trading hub active on desktop, a signed-in session and a NinjaTrader account; the sheet's handles are `ninjatrader-connect-dialog` and `ninjatrader-connect-{username,submit,linked,queued,error}` (source) |
| A relay feed drawn as the chart's main plot, by column, on one shared feed session (`7aa2979a78`) | `src/composables/chart/useFeedMainSeries.ts`, `src/composables/chart/feed-main-state.ts`, `src/indicators/controls/feed/feed-session-core.ts`, `src/components/chart/ChartEmptySeriesOverlay.vue` | unmapped | live verification pending | the `feeds` flag (forced on in a dev lane by `DEV_FORCED_FLAGS`, off for a production guest) and a feed address `OM` `feed:@scope/name#column`; the main plot is a line, a refusal shows on the empty-series card (source) |
| The share dialog's account lines: Fills, Positions and Orders switches, and clip recording that refuses an uncropped capture while NinjaTrader data shows (`3dd3e5d0c3`) | `src/utility/screenshot/screenshot-account-lines.util.ts`, `src/clips/recorder/clip-capture.ts` | unmapped | live verification pending | a signed-in session with a futures account line; keys `kiyotaka.screenshot-fills`, `-positions`, `-orders` (source) |
| A search row on a gate-governed plane (a CME future, a stock tape) draws no price, change or sparkline (`63c1fa257a`) | `packages/wrun-chart-host/src/utility/options/option-venue-disclosure.util.ts` (`rowFiguresAllowed`), `src/components/symbolSelection/component/AssetRow.vue`, `VenueRow.vue` | [symbol search](./symbol-search-and-ticker-bar.md) Gotchas | live verification pending; on 2026-11-07 `asset-row-AAPL\|4-btn` kept `342.96 ↓ 0.36%` because its venue POLYGON is not gate-governed | a CME row (the guest `CME` tab failed on 2026-11-04) or a stock-tape venue row |
| A degraded connection raises a yellow strip: slow, offline, still reconnecting with Reload, back to live (`b2623958e8`); waits of 5 s (icon), 15 s (strip) and 30 s (Reload), reconnecting said only on transport evidence, and the strip on the phone's Chart tab (`c16de1bf2e`, `1e45e23e73`, `69247f4c27`, `22fc0cede7`) | `src/components/banners/ConnectionStrip.vue`, `src/utility/live/connection-strip.util.ts`, `src/utility/live/connection-self-heal.util.ts` | [boot](./chart-boot-and-data-plane.md) `boot-strip` | 2026-11-07, `dced88e06a`: `offline` within 6 s, `back` at once; `back` stood while the tab was hidden and cleared when it was re-fronted; 2026-11-06, `8bcd72f8f5`: `offline` at the 5 s poll and `back` within 1 s through the browser's offline switch; 2026-11-05, `87a325f4ab`: `long` with `connection-strip-reload` during a real gateway loss | `stall` and the 30 s `long` not driven (they need a slow or blocked socket host); the phone strip and its one self-reload not driven |
| Service notices: an admin's status notice as a banner, closed into a top-bar pill that opens the status list, "back to normal", the severity-100 popup and the sign-in inline line (`c88d56c7c9`; the footer maintenance line is deleted) | `src/components/banners/service-notice/ServiceNoticeGate.ts`, `src/components/banners/ServiceNoticeBanner.vue`, `src/components/banners/ServiceNoticePill.vue`, `src/composables/useServiceNotices.ts`, `src/utility/service-notices-polling.ts`, `src/store/maintenance.ts` | [boot](./chart-boot-and-data-plane.md) `boot-notices` | 2026-11-06, `8bcd72f8f5`, a notice injected through the `maintenance` store: banner `active`, pill `warn`, the list's one row, then banner and pill `resolved` | the dev backend serves no notice, so the feed (`GET /maintenance/notices` every 60 s, `/auth/alive` signed in) is not driven; a partial notice, the severity-100 popup and the sign-in inline line not driven |
| A restore that takes a saved row off a chart says so once: a retired kScript row, an indicator or a drawing this build cannot draw (`fd0cf9a5de`, `bd80751b9b`) | `src/utility/chart/restore-removal-notice.util.ts`, `src/utility/chart/restore-removal-notice-show.util.ts` | unmapped | live verification pending | needs a saved workspace holding such a row (no UI trigger); once per removal per device (`localStorage['kiyo:restore-removal-seen']`); close is `restore-removal-notice-close` (source) |
| A failed alert delivery shows as a notice and a `Not delivered` History line; a refused Telegram save says why (`1d48f6b088`) | `src/components/notification/content/AlertDeliveryFailedNotice.vue`, `src/components/alert/HistoryCard.vue` | [panels](./right-side-panels.md) `rp-alerts` | live verification pending; the History tab opened with no undelivered row 2026-11-05 | a guest cannot create or fire an alert (`alert` wall) |
| Store pictures cap their zoom; a capped strip's page opens without the flight (`ad2c5fc913`, `422b70b2ba`) | `src/components/dialogs/indicator-dialog-v2/store-picture-fit.ts` | [indicators](./indicators.md) `ind-dialog` | live verification pending; attempted 2026-11-05: the dev backend served only 112 x 112 square covers, so no `[data-picture-fit]` node | a backend serving the Official strip thumbnails |
| The Indicators search selects its words after an add so the next name replaces them (`2fba2696fa`) | `src/components/dialogs/indicator-dialog-v2/IndicatorSearchBar.vue` | [indicators](./indicators.md) `ind-dialog` | live verification pending; a guest's Add raised the `indicators` wall first (2026-11-05) | a signed-in session |
| Trade a smaller related futures contract from a full-size chart; the ticket offers only contracts the account may trade (`5f5ce41666`, `1794d15972`) | `src/components/futures/FuturesTradeTicketPanel.vue`, `src/components/chart/CmeContinuousChip.vue` | unmapped | live verification pending | a signed-in futures account |
| Phone chart scroll-to-latest button (`45b569a60c`) | `src/components/chart/MobileScrollToLatestButton.vue` (`chart-nav-scroll-latest-mobile`) | unmapped | live verification pending | the phone shell; this map drives desktop at 1440 x 900 |
| Desktop sign page | `src/pages/desktop/sign.page.vue` | [desktop map](../../verify-kiyotaka-desktop/features/browser-handoff-wallet.md) `sign-page` | 2026-10-12, `133c5af8ca`, in the desktop map | none |
| Desktop browser sign-in and checkout returns | `src/pages/desktop/signin.page.vue`, `src/pages/desktop/return.page.vue`, `src/pages/desktop/checkout-return.page.vue` | unmapped (belongs with the desktop map) | live verification pending | the desktop shell |
| Open Interest and Agg. Open Interest draw as Candles or a Line (`254c5ce876`) | `src/indicators/controls/open-interest/plot-type.ts`, `src/indicators/controls/open-interest/OpenInterestSettings.vue`, `src/indicators/controls/aggregated-open-interest/AggregatedOpenInterestSettings.vue` | [indicators](./indicators.md) `ind-oi-plot` | 2026-11-08, `943281a2eb`, a programmatic `OPEN_INTEREST` on BINANCE.F BTCUSDT went from `plotType` `candle` to `spline` through `combo-box-option-spline` (357 rows kept, the pane drawn as a line) | Agg. Open Interest not driven; a dialog-path add needs a signed-in session |
| Pick a heatmap by kind (Order Book, Hyperliquid, Options) and its variant; turning it on brings back the pane's last kind (`50075ec0bd`) | `src/components/TickerBar/TBHeatmapPanel.vue`, `src/composables/useHeatmapKinds.ts`, `src/utility/chart/heatmap-last-type.util.ts` | [panels](./right-side-panels.md) `rp-heatmap` | partial, 2026-11-09, `32dd0c6354`: `Order Book` and `Options` pills on COINBASE BTC-USD and BINANCE.F BTCUSDT, a pill click raised `orderbook-heatmap`; on AAPL the Panels row is `aria-disabled` and opens nothing; before that partial, 2026-11-08, `943281a2eb`: `Order Book` and `Options` pills on BINANCE.F BTCUSDT, a pill click raised `orderbook-heatmap` | turning a heatmap on, a variant pick and the last-kind restore need a signed-in session; `TBSourceDropdown.vue` deleted; since `72f6560bd3` the pills are always listed and a kind the market lacks holds dimmed with a Tooltip (source, no held pill seen) |
| The footer's timezone menu labels each zone with its offset at this instant; chart times read the zone's offset at each instant (`2cad385819`) | `src/components/footer/timezone/TimeZone.vue`, `src/utility/chart/display-timezone-offset.util.ts` | [Super Search and settings](./super-search-and-settings.md) `set-timezone` | 2026-11-09, `32dd0c6354`: the list read `UTC-8 Los Angeles`; before that 2026-11-08, `943281a2eb`: `Los Angeles` listed `UTC-8`; the pick set the footer to `UTC-8` and `12:06:18` against `20:06` UTC, no wall | an axis time across a clock change not driven |
| Menus in settings cards are ComboBoxes; floating panels keep one width; a frame opens with its body (`18c8a69659`, `978f9741dd`) | `src/components/common/ComboBox.vue`, `src/components/objects/ToolPropertiesEditor.vue`, `src/composables/common/useOpenWhenLoaded.ts` | [indicators](./indicators.md) settings card; [drawing tools](./drawing-tools.md) `dt-settings` | 2026-11-08, `943281a2eb`: the OI card's three ComboBoxes and the trend line card's `Style` ComboBox, no native `select` | the gear's `aria-busy` wait shows only on a cold chunk (not seen warm); the Trade settings' menus need a signed-in trading context |
| CVD flow dominance and CVD draw a bar grey where a leg did not trade or has no venue, and keep every leg (`943281a2eb`) | `src/indicators/controls/cvd-flow-dominance/flow-side.ts` | [indicators](./indicators.md) Gotchas | live verification pending | a market and window where one leg is missing; not driven; pinned at 0.1.2 by `152645efa7` (a missing or zero leg draws no side, source) |
| Lite charts: a per-device preset of four engine levers for slow computers, switched from Settings Performance, the chart settings Display page or its chip; default-on for a weak device with a staying Keep / Turn off notice (`14e97da372`, `e46bf72484`, `b62ef4c998`, `fe722ed806`) | `src/utility/chart/lite/lite-hint.ts`, `src/utility/chart/lite/lite-preset.ts`, `src/utility/chart/light-charts.util.ts`, `src/components/settings/LiteChartsSettingRow.vue`, `src/components/settings/PerformanceSettingsPage.vue` | [Super Search and settings](./super-search-and-settings.md) `set-lite` | 2026-11-09, `32dd0c6354`: on a fresh software-GL device the preset turned on by itself about 12 s into the boot (`kiyo:pref:light-charts` `1`, a staying notice), `light-charts-setting-row` flipped it off and on, `light-charts-chip` opened `light-charts-card` and `light-charts-turn-off` turned it off with a `Lite charts off` notice | the Display page's copy and the phone drawer not driven; product gap: on a cold boot the notice read raw `perfHints.liteCharts.*` keys (boot bundle lacks them, the notice fires 5 s after mount regardless of first paint) |
| The search rail names kinds Stocks, Futures, Options and lists the top exchanges; tabs, presets and the Exchange menu lead with general markets (`32dd0c6354`, `2d6c7e7894`) | `src/components/symbolSearchV2/ViewsRail.vue`, `src/components/symbolSearchV2/CategoryStrip.vue`, `src/constants/symbol-search-v2.constants.ts`, `src/utility/symbol-search-v2/family-logo.util.ts` | [symbol search](./symbol-search-and-ticker-bar.md) `sym-rail` | 2026-11-09, `32dd0c6354`: four kind rows, the seven `search-v2-rail-exchange-*` rows, NASDAQ and NYSE narrowing the list with `search-v2-refine-exchange-btn` reading `NYSE` | the `Options` row needs a signed-in session with OPRA |
| Full chart: the pane's exit sits below the hover toolbar (`cd1f34ff89`) | `src/components/chart/ChartPaneActionBar.vue`, `src/styles/full-chart-mode.scss` | [ticker bar](./symbol-search-and-ticker-bar.md) `tb-full-chart` | 2026-11-09, `32dd0c6354`: `chart-pane-expand-btn` entered the mode, named `Exit full chart` at about `(1325, 52)`; `Escape` left it | none |
| Order Book Profile holds its grouping at every zoom in `Fixed` mode (`0f3c552e1f`) | `src/indicators/controls/orderbook-profile/OrderbookProfileSettings.vue`, `src/utility/chart/orderbook-profile-grouping.util.ts` | [indicators](./indicators.md) `ind-ob-grouping` | 2026-11-09, `32dd0c6354`: a programmatic `ORDERBOOK_PROFILE` on BINANCE.F BTCUSDT, `Grouping mode` set to `Fixed` (`settings.groupingMode` `fixed`) | the drawn bands not compared across a zoom; a dialog-path add needs a signed-in session |
| Shared search fields and dialogs: one clear control, one close and confirm language (`ee1fae1b4d`) | `src/components/common/SearchField.vue`, `src/components/common/CloseButton.vue`, `src/components/common/ConfirmDialog.vue`, `src/components/common/Button.vue` | [indicators](./indicators.md) `ind-settings-search`; [Super Search and settings](./super-search-and-settings.md) | partial, 2026-11-09, `32dd0c6354`: the settings search's three `Escape` steps and `settings-search-clear-btn`, `super-search-clear-btn` named `Clear` | the signed-in dialogs on the new `ConfirmDialog` not driven |
| The Options heatmap's knobs in the heatmap panel (`72f6560bd3`) | `src/components/TickerBar/TBHeatmapPanelOptionsBody.vue`, `src/composables/useOptionsHeatmapPanelControls.ts` | [panels](./right-side-panels.md) `rp-heatmap` | live verification pending | a signed-in session with OPRA or CME options data |
| A session feed builds 3D and longer bars from OpenMarket's finished daily rows, and live candles below a minute (`760f05c8c0`, `4153316e09`) | `src/session-feed/session-official-days.ts`, `src/session-feed/session-buckets.ts`, `src/components/chart/SessionFeedChip.vue` | unmapped | live verification pending | a signed-in Rithmic session with CME entitlement |
| A built-in's wrun twin names its chart lines and Style headings in the built-in's own words, on one row per setting and a single colour look (`9143158f71`, `173e9a7e46`, `537639ebca`, `6e8a12ab4b`) | `packages/wrun-chart-host/src/utility/wrun/wrun-output-words.util.ts`, `packages/wrun-chart-host/src/utility/wrun/wrun-style-names.util.ts`, `src/utility/wrun/wrun-builtin-line-words.util.ts` | unmapped | live verification pending | a signed-in session with a mounted wrun twin |
