# Chart boot and the data plane

Opening `/chart/` mounts the chart engine, starts the Web Worker that owns every
websocket, and draws candles for the last-used symbol. Every other proof in this
map depends on this one working, so verify it first and never assume it. This
entry was last DRIVEN on 2026-11-26 against product tree `1d1a3e1410`
(`origin/main`, 76 commits past `ec531568de`), lane `18108`, a guest JWT
with the backend answering and the gateway reached through the
`KIYO_BROWSER_ARGS` map to `10.1.1.10` (both resolvers answered NXDOMAIN;
`doctor` passed with the map). Boot drew 250 bars on COINBASE BTC-USD 1h
25 s after `open`, with VWAP (`Indicators 1/3`), `Guest Mode` and the
signup modal. **A guest's `/v3` page now opens no `/v2` socket:** a CDP
capture of a reload over 45 s read the `/v3/` dial at 3.1 s and no `/v2/`
socket (see Gotchas). On this dev lane `kiyotaka:v3-endpoint` read `null`:
the `/v3-endpoint` discovery runs on production builds only. The slow pace
at rest is gone (`887347c37c`). Not driven: the first-frame stand-in for
a saved layout's native lines, the late-line price glide and an indicator
pane's own decimals (see `boot-axis-decimals`). Before that, this
entry was last DRIVEN on 2026-11-25 against product tree `ec531568de`
(`origin/main`, 142 commits past `8cd7ad448e`), lane `18107`, a guest JWT
with the backend answering (`doctor` passed twice in two on the tracked
wrapper). Boot drew 250 bars on COINBASE BTC-USD 1h 15 s after `open`, with
VWAP, `Guest Mode`, the signup modal and the Lite charts notice. **A guest
now rides `/v3`:** a CDP capture of a reload's socket opens read the
gateway's `/v3/` dial at 2.5 s and a `/v2/` socket at 3.6 s (see Gotchas).
Also driven: the guest limit card through its dev preview (see
`boot-guest-limit`) and INDEX DXY's price axis at two decimals at every zoom
(see `boot-axis-decimals`). The first BINANCE.F pick made vite re-optimize
a dependency and reload the page (see the README's Baseline
preconditions). Not driven: slow pace at rest (a fast headless lane never
enters it), the index day candles moving live, Solana pool candles on
`/v3`, and the engine's squeeze and flat-line fixes (`1329.98`, `1329.99`).
Before that, this entry was last DRIVEN on 2026-11-24 against product tree `8cd7ad448e`
(`origin/main`, 269 commits past `92f4a841ef`), lane `18106`, a guest JWT
with the backend answering (`doctor` passed twice in two on the tracked
wrapper). **The cold first boot was slow:** the candle predicate stayed
`0` for the whole two-minute budget, then read 250 bars on COINBASE
BTC-USD 1h with `Indicators 0/3` (VWAP not yet mounted), `Guest Mode`, the
Lite charts notice and `[refresh-token] all retries exhausted` (`timeout of
15000ms exceeded`) in the console. A warm reload drew 251 bars at 11 s and
VWAP at 15 s (`Indicators 1/3`, `__BOOT_ERRORS__` empty). So on a fresh
lane poll for longer than two minutes, or reload once before calling a boot
broken. The guest signup modal was recorded as shown during that cold boot
(the `guest-prompt` store's `modalShownThisSession` `true`, `modalSeenAtMs`
set) and did not rise on the reload: it shows once per device and day,
and a reload the same day gets the bar instead. A `Draw by holding`
tutorial sheet (`.dialog-style.dialog-overlay.backdrop-dim`) covered the
ticker bar after the reload until `Escape`. Not driven: the glides, a wake
heal, the perp ticker, and the 2026-11-24 live-feed and gateway-v3 changes
(no user surface then; guests stayed on v2 until `9d2bbbeaa0`). Before that, this
entry was last DRIVEN on 2026-11-21 against product tree `92f4a841ef` (`origin/main`, 103 commits past `7c937b0a1f`),
lane `18104`, a guest JWT with the backend answering (`doctor` passed twice in two on the
tracked wrapper). Boot drew 250 bars on COINBASE BTC-USD 1h with VWAP
(`Guest Mode`, `Indicators 1/3`, `__BOOT_ERRORS__` empty) about 25 s after
`open`, with the countdown under the price tag; the signup modal rose about
12 s later and Lite charts switched itself on (`Keep` cleared the notice).
Also driven: the hover warm's absence (see `boot-intent-warm`: `a8935a39a2`
removed it), the perp ticker on BINANCE.F BTCUSDT (`24H VOLUME $25.40B`,
`OPEN INTEREST $5.62B`, `FUNDING / COUNTDOWN -0.0043% · 03:15:39`), one
vite re-optimise reload on the first Orderbook open, and the tab drifting
hidden before most steps. Not driven: the glides, the countdown on a
delayed feed or a session day size, and a wake heal. Before that, this
entry was last DRIVEN on 2026-11-20 against product tree `7c937b0a1f`
(`origin/main`, 82 commits past `413f86e5af`), lane `18104`, a no-session
lane: Tailscale was stopped, `dboons-nutz` did not resolve and every
`/api/v1` call answered `502`, while the internal gateway was reachable.
`doctor` failed twice on the tracked wrapper (its catalog line reads a `502`
as a failure even when the backend line says unreachable) and passed twice
with the wrapper from the open hub PR #26. Boot drew 250 bars on COINBASE
BTC-USD 1h with VWAP (`Indicators 1/3`, no `Guest Mode` badge,
`__BOOT_ERRORS__` `[]`) 20 s after `open`, with the countdown under the
price tag. Also driven: the hover warm and its press join (see
`boot-intent-warm`), the `Latest` glide with Lite charts off and its cut with
Lite on (see `boot-glide`), the countdown held off on `1M` (see
`boot-countdown`), the perp ticker on BINANCE.F ETHUSDT (`1761.07 +0.37%`,
`24H VOLUME $8.07B`, `OPEN INTEREST $4.34B`, `FUNDING / COUNTDOWN +0.0030% ·
03:38:23`), and the tab drifting hidden at least seven times. Not driven:
the countdown on a delayed feed (the stocks and CME planes are unrouted
here), a wake heal, and every guest-only state. Before that, this
entry was last DRIVEN on 2026-11-19 against product tree `413f86e5af`
(`origin/main`, 184 commits past `cff04f9a01`), lane `18103`, a guest-JWT
lane with the backend answering (`doctor` passed twice in two): boot drew 250
bars on COINBASE BTC-USD 1h with VWAP (`Indicators 1/3`, `Guest Mode`) and
the candle countdown under the price tag with no stored choice (see
`boot-countdown`), the footer's `RTH` word opened its session menu on AAPL
(see `boot-footer-session`), and the tab drifted hidden once more (see
Gotchas). Before that, last DRIVEN on 2026-11-18 against product tree
`cff04f9a01` (`origin/main`, 79 commits past `60b7e6b190`), lane `18103`, a guest-JWT lane on the internal
gateway with the backend answering again (the lane's refresh-token call
`200`): boot drew 250 bars on COINBASE BTC-USD 1h with VWAP (`Indicators
1/3`, `Guest Mode`, `__BOOT_ERRORS__` `[]`), the signup modal came first and
the ink tutorial after it was closed (see Gotchas), the tab drifted hidden
once and `tab t1` brought it back, and the footer connection card read
`Connected` (see `boot-connection-card`). Before that, last DRIVEN on
2026-11-17 against product tree `60b7e6b190`
(`origin/main`, 60 commits past `6bfc742bc8`), lane `18103`, a no-session
lane on the internal gateway: the backend `dboons-nutz` did not resolve
(Tailscale stopped), so no guest token was issued, yet boot drew 250 bars
on COINBASE BTC-USD 1h with VWAP 10 s after `open`, with no `Guest Mode`
badge and no signup modal (see Gotchas and the README's Baseline
preconditions); Go to date's in-place edit, the chart zone's today and the
`Invalid date` refusal (see `boot-go-to-date`). Before that, last DRIVEN on
2026-11-16 against product tree `6bfc742bc8`
(`origin/main`, 187 commits past `c7d4eccfac`), lane `18103`, a guest-JWT
lane on the internal gateway (`tsdb-gateway.int.ore.kiyotaka.ai` resolving
to `10.1.1.10` again, no export and no resolver map): boot to 250 bars on
COINBASE BTC-USD 1h with VWAP about 10 s after `open`, the `/chart/open`
link (see `boot-open-link`) and the history-reach notice in Go to date (see
`boot-go-to-date`). The signup modal raised only after the first
paint, after a first `guest-signup-modal-close-btn` probe had found nothing,
and the ink tutorial raised later still, after a click; re-read the top
overlay before every click. Before that, last DRIVEN on 2026-11-14 against product tree `c7d4eccfac`
(`origin/main`, 62 commits past `963af59de1`), lane `18103`, a guest-JWT lane with the v2 gateway pointed at the public `wss://api.chart.ore.openmarket.xyz/v2/` (see the README's Baseline preconditions): boot to 250 bars on
COINBASE BTC-USD 1h with VWAP 10 s after `open`, the last bar's close and
volume moving between two reads 20 s apart, and the settle dim's ring on two
light loads (see `boot-settle-dim`). Before that, last DRIVEN on 2026-11-13 against product tree `963af59de1`
(`origin/main`, 87 commits past `74ccd3cdcc`), lane `18103`, a guest-JWT lane
with the gateway name mapped to `10.1.1.10` (`doctor` green with the map):
boot to 250 bars on COINBASE BTC-USD 1h with VWAP 12 s after `open`, the
settle dim on a BINANCE.F SOLUSDT pick (see `boot-settle-dim`), and the price
scale's `held` state after a right-button drag zoom (see `boot-scale-held`).
Before that, last DRIVEN on 2026-11-12 against product tree `74ccd3cdcc`
(`origin/main`, 113 commits past `c2c02b7b42`), lane `18103`, a guest-JWT lane
(`doctor` green twice, load 15 on 10 cores): boot to 250 bars on COINBASE
BTC-USD 1h with `__BOOT_ERRORS__` `[]` on a warm reopen (the cold open, while
vite was still optimizing, held one `Failed to fetch dynamically imported
module` entry), the perp live edge on BINANCE.F ETHUSDT (`24H VOLUME $6.21B`,
`OPEN INTEREST $4.74B`, `FUNDING / COUNTDOWN +0.0072% · 05:44:31`), and Go to
date with its history window (see `boot-go-to-date`). Before that, last DRIVEN on 2026-11-10 against product tree `c2c02b7b42`
(`origin/main`, 60 commits past `32dd0c6354`), lane `18103`, a guest-JWT lane
(the gateway on the system resolver, `doctor` green twice, load 8 to 12 on 10
cores): boot to 250 bars on COINBASE BTC-USD 1h within 10 s of `open`,
`Indicators 1/3`, the signup modal on top, and the Lite charts notice reading
its words; then BINANCE.F BTCUSDT, ETHUSDT and SOLUSDT at 1m (405 to 500
bars) and a navigation back from the clip page to 250 bars. Before that, last
DRIVEN on 2026-11-09 against product tree `32dd0c6354`
(`origin/main`, 60 commits past `943281a2eb`), lane `18103`, a guest-JWT lane
(the gateway on the system resolver, `doctor` green three times): boot to 250
bars on COINBASE BTC-USD 1h at 14 s cold (251 at 3.4 s on a warm reload),
`Indicators 1/3`, `__BOOT_ERRORS__` `[]`, no strip or chip. Before that, last
DRIVEN on 2026-11-08 against product tree `943281a2eb`
(`origin/main`, 59 commits past `dced88e06a`), lane `18103`, a guest-JWT lane
with the gateway name resolving through the system resolver again
(`10.1.1.10`, no browser map; `doctor` green on both runs). Proven that day:
boot to 250 candles on COINBASE BTC-USD 1h on the second poll after `open`,
with VWAP, `Vol` and `Indicators 1/3`, `__BOOT_ERRORS__` `[]`, and live
candles on DERIBIT.F ETH_USDC-PERPETUAL, AAPL and BINANCE.F BTCUSDT after
switches. Source since `dced88e06a`, not driven: the worker now pings an idle
crypto feed socket itself after 15 s (`feedIdlePing`), so a hidden tab whose
price title holds still keeps its socket instead of losing it to the feed's
60 s read deadline every few minutes, and a socket up 60 s that drops
redials within 250 to 1,500 ms (`77b44cfcc1`); a close the page makes is
echoed at once (`9ca7ecdd6c`); and a connection-stall episode reports who
ended the socket, with no new text on the strip (`5fb893d920`). Before that,
DRIVEN on 2026-11-07 against product tree `dced88e06a`
(`origin/main`, 81 commits past `8bcd72f8f5`), lane `18103`, a guest-JWT lane
with the gateway name mapped to `10.1.1.10` in the browser (both resolvers
answered NXDOMAIN). Proven that day: boot to 250 candles on COINBASE BTC-USD
1h within about 10 s of `open`, with VWAP and `Indicators 1/3`; the perp live
edge on BINANCE.F ETHUSDT (`24H VOLUME $7.97B`, `OPEN INTEREST $5.29B`,
`FUNDING / COUNTDOWN +0.0058% · 03:39:28`); the strip's `offline` and `back`,
with `back` parked while the tab was hidden (see `boot-strip`); and a Dark to
Light flip. Before that, DRIVEN on 2026-11-06 against product tree `8bcd72f8f5`
(`origin/main`, 119 commits past `87a325f4ab`), lane `18103`, a guest-JWT lane
(`gateway-v3` `false`, `us-equities-full` `true`) with the gateway name mapped
to `10.1.1.10` in the browser (both resolvers answered NXDOMAIN; see the
README). Proven that day: boot to 250 candles on COINBASE BTC-USD 1h within
about 10 s of `open`, with VWAP on the chart; the strip's `offline` and `back`
under the new waits; and the new service notices from an injected notice
(see `boot-strip` and `boot-notices`). Before that, DRIVEN on 2026-11-05 against product tree `87a325f4ab`
(`origin/main`, 123 commits past `8436920004`), lane `18103`, a guest-JWT lane
(`feature-flags` `gateway-v3` read `false`). Proven that day: boot to 250
candles on COINBASE BTC-USD 1h (`window.__BOOT_ERRORS__` `[]`, metadata
`Main, Vol`, `Indicators 0/3`: the VWAP the 2026-11-04 boot drew within 10 s
was missing at first candles and through the first indicator drives, and was
on the chart after a symbol undo and on every reload after it; whether it is a
late guest default or came back with the undo was not traced), the new desktop connection strip through the
browser's offline switch (`offline`, then `back`, then gone; no
`connection-status-chip`), the strip's `long` state with its Reload button when
the gateway name dropped off the system resolver at about 20:33 UTC, and the
perp live edge on BINANCE.F ETHUSDT (`2,417.84 +5.66%`, `24H VOLUME $12.92B`,
`OPEN INTEREST $5.75B`, `FUNDING / COUNTDOWN +0.0055% · 03:16:35`) after a
relaunch with the resolver map. Not driven that day: the wake heal, the ring
dump and the left-pan floor. Before that, DRIVEN on 2026-11-04 against product tree `8436920004`
(`origin/main`, 80 commits past `215896e614`), lane `18103`, a guest-JWT lane
with the gateway name resolving through the system resolver all pass (load 3
at the start, 13 at `doctor`). Proven that day: boot to 250 candles on
COINBASE BTC-USD 1h with VWAP in about 10 s (`activeInterval` `1h`,
`window.__BOOT_ERRORS__` `[]`, no `connection-status-chip`, `Indicators 1/3`)
and the perp live edge on BINANCE.F ETHUSDT (`2289.72 +1.71%`, `24H VOLUME
$5.57B`, `OPEN INTEREST $5.44B`, `FUNDING / COUNTDOWN +0.0100% · 03:14:32`).
Not driven that day: the wake heal, the ring dump and the left-pan floor.
Before that, DRIVEN on 2026-11-03 against product tree `215896e614`
(`origin/main`, 131 commits past `a4488341f6`), lane `18103`, a guest lane
carrying a guest JWT (`jwtStore.isGuest` true), with the browser launched
with a `--host-resolver-rules` map for the gateway name (see Gotchas). Proven
that day: boot to 250 candles on COINBASE BTC-USD 1h with VWAP
(`activeInterval` `1h`, `window.__BOOT_ERRORS__` `[]`, `#skeleton-loader`
gone, no `connection-status-chip`, `Indicators 1/3`) and the perp live edge on
BINANCE.F ETHUSDT (`2252.19 −0.545%`, `24H VOLUME $7.62B`, `OPEN INTEREST
$5.27B`, `FUNDING +0.0033%`). Not driven that day: the wake heal, the ring
dump and the left-pan floor. Before that, DRIVEN on 2026-11-02 against product
tree `a4488341f6` (`origin/main`), lane `18103`, a guest lane with the
operator's `.env.local` linked in and no JWT, on a quiet machine (load 2 to 5 on 10 cores; `pnpm
install --frozen-lockfile` in the fresh worktree took 8 s from the shared
store, the lane answered `up` at once and drew 250 candles in 12 s). Proven:
boot to 250 candles on COINBASE BTC-USD 1h with VWAP (`#skeleton-loader` up
before the candles and gone with them, no `chart-loading-overlay`,
`window.__BOOT_ERRORS__` `[]`, `__kiyoBuildId` `local-…`, a 79-line console
with zero worker-death matches), the spot live edge (`24H VOLUME $190.53M`,
no OI), the perp live edge on BINANCE.F ETHUSDT (`OPEN INTEREST $5.36B`,
`FUNDING / COUNTDOWN +0.0017% · 02:45:36`), the ring after boot
(`v2-socket-route` twice with `route: other, reason: custom, host:
tsdb-gateway.int.ore.kiyotaka.ai`, `ohlcv-cache-read` 3,
`main-cache-painted-marked` 1, no `main-fetch-reserve-*`), no
`connection-status-chip` on the healthy lane, and **the wake heal** on
BINANCE.F SOLUSDT 1m from a 392 s visibility override (5 synthesized blank
slots to 0, the full chain through `main-heal-commit`; see Driving the wake
heal, including the recipe artifact it exposed). Not driven: the left-pan
floor, the Reconnect button (it renders only on a degraded socket), a real
sleep and the process-suspend lane. Earlier, 2026-11-01 on `120d5d5d32`
(`origin/main`, lane `18103`, no JWT, load 3 on 10 cores). Proven: boot to 250
candles on COINBASE BTC-USD 1h with VWAP, `#skeleton-loader` gone and no
`chart-loading-overlay` once candles existed, `window.__BOOT_ERRORS__` `[]`, a
worker console with zero death matches, the spot live edge (`24H VOLUME
$201.58M`, no OI) and the perp live edge on BINANCE.F ETHUSDT (`OPEN INTEREST
$5.31B`, `FUNDING / COUNTDOWN -0.0104% · 02:41:46`). NOT driven this pass: the
wake heal, because the v2 gateway name stopped resolving on the machine at
about 21:55 UTC, before the heal's turn (see Gotchas); the heal's last proof
is 2026-10-29. Earlier, 2026-10-29 on `78ec9625d9` (`origin/main`, lane
`18103`, no JWT): boot to 250 candles on COINBASE BTC-USD 1h with
VWAP, a worker console with zero worker-death matches, the spot live edge, the
perp live edge on BINANCE.F ETHUSDT (`24H VOLUME $6.27B`, `OPEN INTEREST
$5.65B`, `FUNDING +0.0100%`), and the lone-bar wake heal from a 405 s visibility
override on BINANCE.F SOLUSDT 1m: 5 synthesized blank slots at the wake, 0 after
it. Earlier: the same heal on 2026-10-28 on `29c9cda0a2` (COINBASE BTC-USD, 414
s). NOT driven: the process-suspend lane and a real machine sleep.

## Sub-features

- `boot-mount` the engine mounts and the ticker bar renders.
- `boot-candles` candles reach the engine and draw.
- `boot-live` the live edge updates (price, 24h volume, open interest, funding).
- `boot-worker` the worker is alive, so websockets can open at all.
- `boot-strip` on desktop, a degraded or lost connection raises one yellow
  strip above the ticker bar that says what is wrong and when it is back.
- `boot-connection-card` the footer's connection button opens a card that
  says in words whether orders and prices arrive on time, slow or offline.
- `boot-countdown` a chart with no stored choice shows the candle countdown
  under the last price; a chart where it was switched off stays off, and a
  calendar interval or a delayed feed shows none.
- `boot-footer-session` on a market with extended hours, the footer's `RTH` /
  `ETH` word opens a menu of both sessions with their hours.
- `boot-notices` an admin's service notice shows as a banner over the chart,
  closes into a top-bar pill that opens the status list, and says when it is
  back to normal.
- `boot-go-to-date` the footer's Go to date moves the chart to a past window,
  and that window keeps the live price off the tab title and the price axis;
  a date past the interval's reach keeps the dialog open and says how far
  back that interval goes; an impossible date keeps it open with `Invalid
  date`.
- `boot-open-link` the chat app's link `/chart/open?symbol=…&interval=…`
  lands on the chart at that market and interval.
- `boot-settle-dim` after a pick, a pane whose indicators are still loading
  400 ms after its first candles shows a thin load line along the top of the
  plot until they have drawn; the plot greys only while the pane is held.
- `boot-scale-held` a zoom gesture pauses the price scale's auto fit, the `A`
  says so, and one click fits the axis again.
- `boot-intent-warm` REMOVED by `a8935a39a2`: a market loads only when it
  is opened. Resting the pointer on a market row (the symbol dialog, Super
  Search, a watchlist row) no longer loads its candles ahead of the click
  (it did from `de79b1d733` to `7c937b0a1f`).
- `boot-glide` `Latest` and `Reset view` slide to a near target and cut to a
  far one; a person's own pick of Auto eases the price range back
  (`0cb582eb9f`, `02de83a38a`).
- `wake-heal` after a hidden or sleeping stretch, the wake backfills every blank
  slot the outage left, including slots before lone bars a trickling feed drew.
- `boot-guest-limit` a network that started too many guest sessions in the
  last hour first gets a quiet human check, then a `One quick check` card
  with a Turnstile box, then a `Guest limit` card that counts down and loads
  the chart by itself, with `Sign in` to skip the wait.
- `boot-first-frame` a saved layout's native lines (VWAP, MA Ribbon) and
  package child panes hold a stand-in picture on the first frame, so the
  price range does not jump when VWAP lands, and the price fit glides when a
  late line lands (`1a07d5df8a`, `38f7e54b74`; source, not driven: a warm
  reload after a first boot, compared against `__disableKiyoNativeStandIn()`
  from `src/utility/chart/native-standin.leaf.ts`).
- `boot-axis-decimals` a quoted market (a US stock, a forex pair, a metal, a
  commodity, an index, an option) prints its own convention's decimals on
  the price axis at every zoom; crypto keeps the zoom's step.

## How to get to it (user POV)

- Open `http://127.0.0.1:<lane>/chart/`. Nothing to click; the chart restores the
  last symbol. The guest default moved to `COINBASE BTC-USD` at `1h`
  (`DEFAULT_REGULAR_METADATA`), so a lane that still opens on
  `BINANCE.F BTCUSDT` is either serving an older checkout or restoring a stored
  guest workspace — read the symbol, never assert a specific one. Read `chartStore.activeInterval` rather than assuming an interval — a
  recipe that hardcodes one silently proves the wrong timeframe.

## Driving it with control-kiyotaka

Preconditions:

- `./control-kiyotaka doctor` exits zero, `chart-schema ok`, `v2 gateway reachable`.

- **Open.** Run `./control-kiyotaka browser set viewport 1440 900` then
  `./control-kiyotaka browser open "$(./control-kiyotaka url)"`.
- **Wait for data, not for time.** Poll
  `./control-kiyotaka browser eval "(()=>{const t=window.tc?.[0];return (t?.metadata?.[0]?.rawData?.length ?? 0)>50})()"`
  until it returns `true`. Budget **at least 2 minutes** on a cold boot: a lane
  whose vite is re-optimizing dependencies has taken ~105s to first candles, and a
  cold boot on an already-installed lane ~85s. A warm reopen in the same browser
  lands in 10-20s.
- **Read the engine.** Run
  `./control-kiyotaka browser eval "(()=>{const t=window.tc[0];return JSON.stringify({bars:t.metadata[0].rawData.length,overlays:t.metadata.length})})()"`.
  A healthy guest boot returns ~250 bars. The current fresh guest starter has a
  VWAP overlay and no default CVD or orderbook heatmap; prediction-market
  workspaces have different defaults. **Assert the bar count, not the overlay
  count**: `metadata.length` is workspace state and is not a stable proof,
  while `metadata[0].rawData.length` is.
- **Confirm the worker is alive.** Run
  `./control-kiyotaka browser console` and assert **zero** matches for
  `Error initializing worker`, `[worker] failed to load worker-impl`,
  `WorkerManager: Failed to create Worker` and `worker parked`. Any of them means
  the data plane is dead and every downstream proof is void.
  Do **not** assert on `V2StreamingConnectionUnavailable`: it is an `Error.name`
  that is deliberately swallowed and never printed, so grepping for it always
  returns zero and the check passes vacuously on a dead lane.
- **Confirm the live edge.** Run
  `./control-kiyotaka browser eval "(()=>document.body.innerText.slice(0,300).replace(/\s+/g,' '))()"`.
  It carries the symbol, price, `24H VOLUME`, `OPEN INTEREST`, and
  `FUNDING / COUNTDOWN`. `—` in those slots means the **v2 gateway lane** did not
  answer, not that `/api` is down: all three ride `V2Service.fetchData` through the
  worker, the same transport as candles. Proven here — a stack whose `/api` calls
  were 500-ing still filled `$8.12B` / `$8.24B` / `+0.0043%`.
  The OI and funding slots exist only on a derivative venue: since
  `3db024ab19` and `cdfa9c212d` one rule (`src/utility/exchange/derivative-venue.leaf.ts`)
  asks open interest, funding and liquidations only where the venue carries
  them (Polymarket and the governed CME venues carry open interest alone), so a
  spot chart such as COINBASE BTC-USD shows `24H VOLUME` and no OI or funding
  by design.
- **Proof.** Dismiss the guest modal and capture in the same step — it re-raises:
  `./control-kiyotaka browser find testid guest-signup-modal-close-btn click` then
  `./control-kiyotaka browser screenshot artifacts/<run>/<rev>/boot-candles.png`,
  with `./control-kiyotaka browser snapshot -i -c` saved beside it. Confirm
  nothing is on top first, with the union rather than a bare dialog count:
  `eval "document.querySelectorAll('.q-dialog, .dialog-style, [role=dialog].open').length"`
  must read `0`.
  Then **open the PNG**: it must show drawn candlesticks, not a dialog. The
  engine read is the side effect; the frame is the only proof pixels arrived.
- **`boot-notices`: service notices (driven 2026-11-06 on `8bcd72f8f5`,
  `c88d56c7c9`).** An admin's notice for the whole app or for named parts
  shows as `service-notice-banner` over the chart; its close
  (`service-notice-banner-close`) folds it into `service-notice-pill` in the
  top bar, whose click opens `service-notice-list`. A guest polls
  `GET /maintenance/notices` every 60 s; a signed-in page also reads them off
  `/auth/alive`. A notice at severity 100 or more opens the old maintenance
  popup instead, and one naming `sign-in` shows as `service-notice-inline` in
  the sign-in card. The footer maintenance line is gone. No dev seam feeds a
  notice and the dev backend serves none, so inject one through the store
  (the next 60 s poll overwrites it):
  `$pinia._s.get('maintenance').setNotices([{id:'qa',parts:[],status:'down',bannerMessage:'QA',resolutionMessage:'',startTimestamp:Date.now()-60000,endTimestamp:null,severity:0}],'poll')`.
  Live: the banner read `data-kind` `active` (`The app is having an outage
  <message> Started 1m ago · Until resolved`); its close left the pill at
  `data-kind` `warn` reading `1`; the pill opened the list with one `active`
  row. The same id again with `endTimestamp` in the past and a
  `resolutionMessage` raised the banner at `resolved` (`Everything is back to
  normal … Lasted 1m · Resolved just now`), gone within 10 s, with the pill
  at `resolved`. Clean up with `setNotices([],'poll')` and empty the store's
  `dismissedNoticeKeys` and `shownBannerIds`, which persist per device.
  A partial notice (`parts:['cme']`) reaches the banner only while that part
  is in use; not driven.
- **`boot-go-to-date`: Go to date and the history window (driven 2026-11-12
  on `74ccd3cdcc`; `3a64fcc3af`, `19d6420302`, `232072c6ab`, `f76258572d`).**
  The footer's calendar button `footer-go-to-date-btn` (`Go to date`) opens a
  `Go to date` dialog: a `YYYY/MM/DD` textbox holding today, hour and minute
  boxes, a month calendar, and `Reset`, `Cancel` and `Apply`. The palette's
  `commands:history-btn` row (`Go to date ⌥ G`, driven) and the time axis's
  right-click `time-axis-ctx-go-to-date` (source) open the same dialog; the
  shortcut list now names it `Go to date`, not `History`. `find role textbox
  fill "2026/11/05" --name "YYYY/MM/DD"` then `find role button click --name
  "Apply" --exact` moved the view to 4-6 Nov and the tab title dropped its
  price to the bare `BTC-USD`: a window of the past keeps the live price off
  the title and the axis, while the top bar keeps the market's price on the
  live price feed (`7ecde328a9`; the 15 s poll is now only the fallback for a
  venue the feed has no frames for, source). The dialog's `Reset` only puts today back in the field.
  The way back to live is `Reset chart`, a hover control the canvas covers, so
  click it in `eval`:
  `document.querySelector('[aria-label="Reset chart"]').click()`; the title
  read `73,777.4 ▲ BTC-USD` again. A first `Apply` was followed by the `Draw by
  holding` tip (close it with `Got it`).
  **A date past the interval's reach is refused in place (driven 2026-11-16
  on `6bfc742bc8`; `cc34a9b534`, `320298b19c`).** On COINBASE BTC-USD `1m`,
  `fill "2020/01/05"` then `Apply` kept the dialog open
  (`manage-history-apply-btn` still there) with `1m charts go back to Nov 5,
  17:24. Pick a later date, or use a larger interval for older dates.`
  (`chart.historyReach.*`, `src/utility/chart/history-cap.util.ts`); the
  calendar greys the days before the reach (source). An app-built custom
  size is judged at its source interval (`320298b19c`, source).
  **The field edits in place, today is the chart's, and a bad date is refused
  (driven 2026-11-17 on `60b7e6b190`; `7712272f20`, `aafd636567`).** The
  dialog's `date-time-picker-date-input` opened on `2026/11/16` while the
  device clock read 17 Nov (UTC+8): "today" is the day in the chart's time
  zone (`user` store `activeTimezone`, here UTC), and the calendar greys the
  days after it. With the month selected (`setSelectionRange(5,7)`), typing
  `09` read `2026/09/16` with the caret at 7: an edit stays where it is typed
  (before, the digits were rebuilt and could read `2026/01/69`). Bare digits
  `20260230` read `2026/02/30` (one slash each), and `manage-history-apply-btn`
  kept the dialog open with a `.date-error` row reading `Invalid date`; a bad
  hour or minute reads `Invalid time` (source). The error words are fixed
  English, not i18n keys (source). Close with `manage-history-cancel-btn`.
- **`boot-open-link`: the chat app's link (driven 2026-11-16 on `6bfc742bc8`;
  `5cb00c2155`).** The `/open` route redirects to `/` keeping only `symbol`
  and `interval` and no hash, and `chartSymbolLinkGuard` launches it like the
  symbol link (`?symbol=BINANCE:BTCUSDT`). `browser open
  "<lane>/chart/open?symbol=BINANCE:ETHUSDT&interval=15m&junk=1#x"` read
  `/chart/` at once and settled on BINANCE ETHUSDT `15m` (471 bars) within
  about 15 s; on the way the symbol button read `COINBASE ETHUSDT` at `1h`
  for a moment, so poll until the exchange and interval both match. The
  symbol names an exchange id split on the first `:`: `BINANCE.F:SOLUSDT`
  (the display name) landed on the default COINBASE BTC-USD `1h`. A bare
  `/chart/open` lands on `/chart/`. On Android and iOS the chart app claims
  the path itself, which a browser lane cannot show.
- **`boot-settle-dim`: the dim while indicators load (driven 2026-11-13 on
  `963af59de1`; `3a9d439865`).** The dim shows only after 400 ms, so a fast
  pick can finish under it; read it with a `MutationObserver` or the ring
  rather than a screenshot. Run
  `eval "window.__enableKiyoLazyLoadDebug()"`, then pick a market (driven:
  `venue-row-BINANCE_FUTURES|SOLUSDT-btn`, VWAP on the chart). Proof: the
  observer saw `[data-testid=cached-paint-veil][data-settle-dim]` with
  `cached-paint-updating-chip` reading `Loading indicators...` for about
  280 ms, and `__dumpKiyoLazyLoadDebug()` held `settle-dim-raised`,
  `settle-dim-paint`, `settle-dim-lowered` (`reason` `settled`, `heldMs`
  243) and `settle-hold-refused` (`reason` `audience`).
  **Since `13a73ab4fb` and `8bf9b42de2` the settle dim has no chip and holds
  only a heavy page (re-driven 2026-11-14 on `c7d4eccfac`).** The veil carries
  `data-settle-line` (a 2 px line on its top edge) and, on a pane that is not
  held, `data-settle-free` (the line alone, no grey wash);
  `Loading indicators...` now belongs to the window-cell loader only. A hold
  needs both an internal role and a page load weight of at least 1000 ms on
  two reads in a row (heatmap 200, script 50, indicator 100 per pane), so a
  guest's single chart never asks for one and the ring carries no
  `settle-hold-refused` any more. Driven: `tb-interval-pinned-1h-btn` and
  then `-1m-btn` on BINANCE.F SOLUSDT with VWAP gave `settle-dim-raised`,
  `settle-load-weight` (`weight` 0, `heavy` false) and `settle-dim-lowered`
  (`settled`, `heldMs` 367 and 567, `revealed` empty); a `MutationObserver`
  saw no veil, because the indicators finished inside the 400 ms reveal. A
  heavier set (three indicators, or a grid) is needed to photograph the line.
  **The dim does nothing on a hidden tab:** two loads made while the tab had
  drifted hidden left no `settle-` event at all. Re-front the tab before the
  load. The veil and `cached-paint-updating-chip` remain the stale-frame
  dim's handles; a stale frame shows `Updating` in the chip.
- **`boot-scale-held`: the price scale's paused auto fit (driven 2026-11-13 on
  `963af59de1`; `58ea64190f`).** Read
  `[data-testid=price-scale-corner-auto]`: `data-scale-state` is `auto`,
  `held` or `manual`. A right-button drag zoom on the body (`mouse move 600
  450`, `mouse down right`, four moves up and right, `mouse up right`) set
  it to `held`, `aria-pressed` `false`, class
  `price-scale-corner__toggle--held`; a plain left drag up the body left it
  `auto`. One click on the `A` returned `auto` and `aria-pressed` `true`; it
  never pins `manual`. Press `Escape` after the right-button drag in case a
  context menu opened.

### Driving the wake heal

**Re-driven 2026-11-02 on `a4488341f6`, the visibility-override recipe.**
Guest BINANCE.F SOLUSDT 1m (333 bars), lane `18103`, the gateway resolving
and `POST /api/v1/auth-v2/refresh-token` answering 200 through the lane.
Hidden for 392 s with `__kiyoDropLiveSeriesFrames('.*')` on; 5 NaN rows
written from the last real bar (21:52) plus a lone bar one slot behind now
(21:58), `beforeFlip` reading 6 rows with 5 blank. After the visible flip the
ring read `lifecycle-hidden-return` (`wasHiddenMs 392588`,
`willEmitWake true`), `lifecycle-wake-emit` (`reason: clock-skew`,
`outageStartedAt` the hide time), `wake-received`, `wake-token-refreshed`
(178 ms), `wake-sockets` (`v2Open`, `liveFeedOpen`), `wake-resync-live-drain`
(`none`), `wake-resync-pass` (`trigger: wake`, `mainStartMs` equal to the
last real bar before the hide, `mainPeriodSec 431`), `wake-resync-overlay-window`
(VWAP `full`), `main-heal-commit` (`lane: period`, `mode: wholesale`, `rows:
7`, `heldRows: 6`, `reason: row-width`), `wake-resync-awaited` (238 ms) and
`wake-reconnected`. 80 s after the flip the hole held 0 blank and 6 real bars.
**The recipe's own artifact:** the series read 8 rows after the wake and 10
two minutes later, with the 18:00 to 21:52 history gone from the frame. That
is the synthesis, not the heal: `tc[0].updateData('main', rows, {isPrepend:
false})` REPLACES the main series with `rows` (probed on a fresh COINBASE
BTC-USD 1h boot: 251 rows became 1 after one NaN row was written). Write the
whole series plus the damage (`[...rawData, ...nanRows, loneBar]`) so the
heal is judged on a full chart, and read `rawData.length` before and after.
Earlier passes counted only the hole, so their totals are unknown.

**Re-driven 2026-10-29 on `78ec9625d9`, same recipe.** Guest BINANCE.F
SOLUSDT 1m with a `BITCOIN_DOMINANCE` pane mounted, lane `18103`. Hidden for 405
s with the feed silenced; 5 NaN rows from the last real bar (20:24) to a lone
bar at 20:30. After the visible flip the ring read `lifecycle-hidden-return`
(`wasHiddenMs 405347`), `lifecycle-wake-emit` (`reason: clock-skew`,
`outageStartedAt` the hide time), `wake-received`, `wake-token-refreshed`
(151 ms), `wake-sockets`, `wake-resync-live-drain` (`none`), `wake-resync-pass`
(`mainStartMs` 20:23, one bar before the last real bar), one
`wake-resync-overlay-window` per overlay (VWAP `full`, `not-contiguous`;
`BITCOIN_DOMINANCE` `narrowed`), `main-heal-commit` (`lane: period`,
`mode: wholesale`, `reason: interior-change`), `wake-resync-awaited` and
`wake-reconnected`. 78 s after the flip the hole held 0 blank and 5 real bars.
The commit's `reason` differs run to run (`row-width` on 2026-10-28,
`interior-change` here); assert the blank count, not the reason.

**Driven 2026-10-28 on `29c9cda0a2`, with the visibility-override recipe
below.** Guest COINBASE BTC-USD 1m, lane `18103`, headless Chromium. Hidden for
414 s with `__kiyoDropLiveSeriesFrames('.*')` on; 5 NaN rows written after the
last real bar plus one lone bar one slot behind now. After the visible flip:
`lifecycle-hidden-return`, `lifecycle-wake-emit` (`outageStartedAt` 4 ms after
the hide, `reason: clock-skew`), `wake-received`, `wake-token-refreshed`,
`wake-sockets`, `wake-resync-live-drain`, `wake-resync-pass`
(`mainStartMs` equal to the last real bar before the hide, so the heal ran from
the outage start), `wake-resync-overlay-window`, `main-heal-commit` with
`reason: row-width`, `wake-resync-awaited`, `wake-reconnected`. The 5 blank
slots read 0 blank 80 s after the flip.

Earlier: 2026-10-23: `main` `034978a50f` (the lone-bar heal `8a7d91341a` on
board) with the process-suspend lane below, guest COINBASE BTC-USD 1m, headless
Chromium, 13-minute outage with two dark wakes (4 blank rows at wake, 0 after the
heal) and, on `daryl/wake-outage-carry` `9da7dfbd5c`, a 29.6-minute outage with
three dark wakes past the access token's life (token refreshed in 113 ms, 15 blank
rows at wake, 0 after the heal; the wake pass ran from the hide slot over 1790 s).
The data grew while hidden both times: lone bars from the trickle. 2026-10-22 drove
the synthesized trigger on base `b153a7751a` against `5287b9a644`, in Chromium and
the desktop shell. NOT driven: a real `pmset sleepnow` on a machine with display
sleep (the mini runs caffeinated and carries every lane).

**Process-suspend lane (preferred, no injected bars).** The script is
`dev-notes/desktop-chart-sleep-wake-gap/sleep-rig.mjs <playwright index.mjs>
<chart url> <out dir> <label> <stopMin> <darkWakes> <darkWakeSec>`. It hides the
tab (bringToFront of a cover tab; headless falls back to the visibility override
below), then `SIGSTOP`s every process of that Chromium tree for `stopMin` minutes
per segment, lets it run `darkWakeSec` seconds between segments with the tab still
hidden (the feed reconnects and trickles ticks the worker holds and drains on the
visible flip), then `SIGCONT`s and shows the tab. Playwright has no process
handle: the browser is the node process's one Chrome child (`pgrep -P $$`). While
stopped the gateway drops the idle sockets as a sleeping laptop's would; on macOS
the monotonic clock keeps counting under `SIGSTOP`, so a VISIBLE page would read
the stop as a busy stall, which is why the lane hides the tab (a closed lid
occludes the window anyway). Verdict: NaN closes and slot jumps in
`tc[0].metadata[0].rawData` between the hide time and the wake, 75 s after the
visible flip; the ring should show `wake-resync-hidden-reopen-recorded` per dark
wake, `lifecycle-wake-emit` with `outageStartedAt` = the hide time, narrow
`socket-open` passes, then the `wake` pass `queued-wider` and run from the first
damaged slot, and a `main-heal-commit` with `reason: interior-change`.

- **Hide the page by overriding visibility.** The app reads
  `document.visibilityState`; define it as a getter and dispatch
  `visibilitychange`. More than 60 s hidden makes the visible return a wake
  (`HIDDEN_GAP_RECOVERY_THRESHOLD_MS`).
- **Silence the feed** with `window.__kiyoDropLiveSeriesFrames('.*')` (dev builds;
  `null` restores). Keep it on through the visible flip and restore ~3 s later, so
  the drained hidden batch is dropped like a sleeping device's.
- **Synthesize the lone-bar damage.** While hidden, write the live bridge's
  footprint through the engine: NaN rows (`[ts, NaN, NaN, NaN, NaN]`, flag `1` in
  `syntheticFlags`) from the last real bar, then one real bar one slot behind
  now, via `tc[0].updateData('main', rows, { shouldResetRange: false, isPrepend:
  false, syntheticFlags })`. **`rows` must be the whole series plus the
  damage** (`[...tc[0].metadata[0].rawData, ...nanRows, loneBar]`, with a
  `syntheticFlags` entry per row): with `isPrepend: false` the call replaces
  the main series with exactly `rows`, so writing only the new rows leaves a
  chart of six bars that the heal then fills, and the frame shows an empty
  left side (driven 2026-11-02; a one-row write on a fresh boot took 251 rows
  to 1). Make the hole longer than the 2-bar lookback
  (`WAKE_RESYNC_MAIN_LOOKBACK_BARS`), or both builds heal it: hide ~6.5 min.
- **Read the verdict from the engine and the ring.** After the wake, count NaN
  closes in `tc[0].metadata[0].rawData` between the last real bar and the lone
  bar. With `window.__enableKiyoLazyLoadDebug()` on, `__dumpKiyoLazyLoadDebug()`
  returns a JSONL STRING, not an array: line one is a `{"kind":"kiyo-perf-dump",
  "version":2,...}` header, and every later line is one `{seq, ms, event,
  details}` entry. Parse it with
  `__dumpKiyoLazyLoadDebug().split('\n').filter(Boolean).slice(1).map(JSON.parse)`.
  An entry's `ms` is page time (`performance.now()`, about `124767` on a lane
  booted two minutes earlier), not epoch time. A filter such as
  `e.ms >= hideAt` with an epoch `hideAt` drops every entry and reads as no wake
  at all. Filter by event name, or compare against `performance.now()`.
  `lifecycle-wake-emit` carries `outageStartedAt`, and `wake-resync-pass` carries
  `mainStartMs` and `lastBarMs`. Driven 2026-10-27 on `7290d33d10`: a 66 s
  visibility override (getter on `document.visibilityState` and `document.hidden`,
  then `visibilitychange`) produced `lifecycle-wake-emit` with `outageStartedAt`
  equal to the hide time and the chain `wake-received`, `wake-token-refreshed`,
  `wake-sockets`, `wake-resync-live-drain`, `wake-resync-pass`,
  `wake-resync-overlay-window`, `wake-resync-overlay-recheck`,
  `wake-resync-awaited`, `wake-reconnected`. Its `reason` read `clock-skew`, not a
  hidden-gap reason, on that override. No damage was synthesized, so that run
  proves the wake fires, not the heal.
  Measured: base kept 2-4 blank slots (heal from `lastBar - 2 bars`); the fix
  left 0 (heal from the outage start).
- **Frame it.** Wheel over the plot until the engine viewport
  (`metadata[0].viewport.endTs - startTs`) spans ~30 bars, re-read before each
  shot; a fixed wheel count over- or under-shoots. Dismiss `Got it` first.
- The script is kept with the run's notes
  (`dev-notes/desktop-chart-sleep-wake-gap/lone-bar-repro.mjs`, and
  `desktop-repro.mjs` for the shell, which must pick the window whose URL holds
  `/chart/`: the title bar's `data:` view loads first).

- **`boot-guest-limit`: the guest limit card (driven 2026-11-25 on
  `ec531568de`, the dev preview only; `8dc63c5c5d`).** The real trigger is
  a refused guest refresh (`src/services/refresh-token.service.ts`), which an
  agent cannot raise, so a dev lane opens the card with a query: `browser
  open "$(./control-kiyotaka url)?guest-limit=check"` (or `=wait`). The
  preview waits 23 minutes and never retries. Read the stage at once, before
  the candle predicate: the check stage gives up after 20 s
  (`4 × TURNSTILE_WAIT_MS`) with no token and falls back to the wait stage.
  `eval "document.querySelector('[data-testid=guest-limit-dialog]
  [data-stage]')?.dataset.stage"` read `check` 2 s after `open`, with the
  title `One quick check`, `Many guest sessions started on this network in
  the last hour. Confirm you are a person to continue.`,
  `guest-limit-turnstile` (empty headless: no widget drew) and
  `guest-limit-or-sign-in` (`or Sign in`). The wait stage reads `Guest
  limit`, `Too many new guests on this network`, `Many guest sessions
  started here in the last hour. Sign in to keep going, or wait and the
  chart loads by itself.`, `guest-limit-sign-in`, `guest-limit-countdown`
  (`Trying again in 23 min`), `guest-limit-support-btn` (`Contact Support`)
  and `Join Discord`. `data-stage` sits on an inner `div`, not on the
  `guest-limit-dialog` node. Close it with `dialog-close-btn`. The quiet
  check before the card (`src/utility/auth/guest-check.util.ts`) draws
  nothing.
- **`boot-axis-decimals`: a quoted market's axis (driven 2026-11-25 on
  `ec531568de`, INDEX DXY 1h; `ec531568de`).** Open DXY from the V2 dialog
  (type `dxy`, click the row whose text starts `DXY USD Index`), wait for
  candles, and shoot the axis; then drag the price axis (`mouse down` at
  `1395 800`, moves up to `1395 100`, `mouse up`, repeated) to zoom in, and
  the other way to zoom out. All three frames read two decimals: `104.80` …
  `101.60` at rest, `112.00` … `94.00` zoomed out, `103.15` and `103.14`
  zoomed deep in, while the ticker bar read `103.802`. The rule
  (`pane-market-decimals.util.ts`) reads the last close of
  `tc[0].metadata[0].rawData`: an index 2, a US stock 2 from $1 and 4 below,
  GBP/JPY 3, EUR/USD 5, gold 2, silver 3 (source; only the index driven).
  Formula panes, Treasury yields and a Value Precision other than `Default`
  keep their own rules. Since `d6bfa51f8a` an indicator pane keeps its own
  decimals on every market (RSI `70.00`, not `70.00000` on GBP/JPY; source,
  not driven: a guest's Add is walled). `Reset chart` puts the scale back.

## Gotchas

- **Lite charts turns on by itself on this lane (driven 2026-11-09 and
  2026-11-10).** A fresh device under software GL flips the preset about 12 s
  into the boot and leaves a staying notice at the bottom of the frame. Since
  `bf17ae49cd` the notice waits for its words, so a raw `perfHints.` key on it
  is a regression; `Keep` stores the decision and the notice does not return. Read
  `localStorage['kiyo:pref:light-charts']` and clear the notice before a capture;
  see `set-lite` in the Super Search guide.
- **A wake or tab return asks only what the saved copy cannot prove (source,
  `d4113f01da`; not driven).** Do not assert a full refetch on a return. A pane is
  no longer rebuilt under a live gesture, and is rebuilt for a new live alias only
  where frames ride it (`058530d565`, `e57fcac9c4`, source).

- **A stale cached frame paints dimmed until the fresh rows land (source,
  `e33ea4c250`, read on `849fb08e95`, never driven).** When the cached tail is
  more than 3 bars behind (`PAINT_WALL_AGE_BARS`), the chart draws it at its
  true time under `cached-paint-veil` with an `Updating` chip
  (`cached-paint-updating-chip`), and the debug ring logs `cache-paint-dim`
  `armed` then `cleared`. To see it, switch away from a 1m chart and back after
  more than 3 minutes and poll both testids; the veil is short-lived on a fast
  backend.

- **The behind-pane catch-up is not the wake heal.** Since `1b9406ba56` a pane
  that boot left behind a newer saved layout (an indicator's settings differ)
  is caught up in place by `src/utility/chart/swr-behind-pane-heal.lazy.ts`, with
  its own counter in the debug dump. It runs at boot reconciliation, not on a
  wake, so do not read its events as `wake-*` evidence. Source only; it needs a
  stale saved workspace, which a guest lane does not have.

- **Never edit the lane's tree while a suspended run sleeps.** Vite pushes a
  `page reload` for a `.ts` edit; the stopped renderer takes it on its next
  `SIGCONT`, the chart reloads fresh and the outage is gone (2026-10-23, sleep-2).
  Finish edits, then start the run, or serve the run from a lane whose tree stays
  still.
- **A production build exposes no `window.tc`.** Every engine read above is a
  dev-lane read; a rig pointed at `openmarket.xyz` times out waiting for candles.
  Read the served build instead: `window.__kiyoBuildId` is `<pipeline iid>-<short
  sha>` and names the production commit (2026-10-23: retail served `18638-6fafc7ce`,
  a commit before the pick that carried the heal).

- **Zero bars plus `v2 streaming websocket connection failed` is almost never the
  socket.** The worker owns the websockets, so a dead worker presents as a
  connection failure. Check `doctor`'s `chart-schema` line first: a sibling
  `orange-shared` behind this repo's pin kills `worker-impl` at module scope.
- The chart answers HTTP and mounts `window.tc` well before it has data. Asserting
  on mount alone passes on a permanently empty chart.
- Candles do **not** need the backend. `:3000` down still draws them **and still
  fills volume/OI/funding** (those ride the v2 gateway too); it removes login,
  workspaces, and the official catalog.
  **`doctor`'s `backend :3000` line is not the backend this lane uses** when
  `.env.local` sets `VITE_BACKEND_PROXY_TARGET` to a remote box. Driven
  2026-10-27: doctor printed `:3000 DOWN — guest lane only` while the proxied
  remote backend issued a real guest JWT and served a SEEDED catalog (241
  official indicators). Probe the lane's own proxy instead, for example
  `curl -s -X POST http://127.0.0.1:<lane>/api/v1/scripts/query -H 'Content-Type: application/json' -d '{"limit":1}'`.
- **With the backend unreachable the lane has no session at all, not a guest
  one (driven 2026-11-17).** The `/api/v1` and `/api/v2` proxies follow
  `VITE_BACKEND_DOMAIN` (`http://dboons-nutz:3000` in `.env.local`;
  `VITE_BACKEND_PROXY_TARGET` serves only the other `/api` paths), and with Tailscale stopped that name did
  not resolve: every `/api/v1` call answered `502` (`getaddrinfo ENOTFOUND
  dboons-nutz` in the lane log). Candles, symbol search, Super Search, the
  Tape and the Orderbook all worked, but `jwt` read `isGuest: false` with no
  token, there was no `Guest Mode` badge and no signup modal, and every
  guest wall became `Verify your email to unlock <feature>` with an empty
  address (`We'll send a 6 digit code to .`), because `handleGuestAccess`
  reads an account that is neither a guest nor verified. A guest wall is
  then not proved, and a guest-only choice (the layout tab colour) does
  nothing. The Indicators dialog sat on skeletons for about 20 s, then read
  `Couldn't load all official indicators` with `Retry` over a fallback list
  whose testids end `-openmarket` instead of the catalog's names. Record such
  a pass as a no-session pass. **Seen again 2026-11-20 on `7c937b0a1f`**
  with the same cause: `Verify your email to unlock Watchlist` and `…
  Indicator Editor`, each with an empty address; the settings pages' nav
  listed all ten items with `Sign Out` at the foot (a guest's lists four);
  the Indicators dialog still listed 19 rows under the failed Official
  shelf. The tracked `doctor` fails such a lane on its catalog line; hub PR
  #26 holds the fix. The public backend (`https://openmarket.xyz`)
  answers `/api/v1` but refuses the lane's dev `Origin` with `403 Not
  allowed by CORS`; do not spoof the production origin to get past it.
- Guest emits a benign `401`; `:3000` down adds `[refresh-token] 502` and
  `http proxy error: /api/v1/... ECONNREFUSED`. None of these are the bug.
- The canvas is WebGL and invisible to the a11y tree — a snapshot alone can never
  prove the chart drew.
- **`[role=dialog]` is the wrong thing to count.** The guest signup modal, the one
  that actually eats clicks, carries **no** `role=dialog` at all — it is a bare
  `div.dialog-style.dialog-overlay` — so a bare `[role=dialog]` count never rises
  when it raises. Count `.q-dialog, .dialog-style, [role=dialog].open`: that union
  reads `1` while the modal is up and `0` once it is dismissed. (A clean desktop
  boot reads `0` on **both** counts; do not expect a standing `1` from a
  mobile-sheet component.) When something blocks a click, `agent-browser` also names
  the covering element (`covered by <div.dialog-style.dialog-overlay>`), which is
  the faster signal.
- **Three different buttons answer to the accessible name `Close`, and the matcher
  picks the wrong one.** A guest boot carries `objects-close-btn`,
  `outage-corner-card-collapse-btn` (the "We're fixing a problem" corner card) and
  `guest-signup-modal-close-btn`. `find role button click --name "Close" --exact`
  resolves to one of the first two, which sit UNDER the signup overlay, so the drive
  dies with `covered by <div.dialog-style.dialog-overlay>` and reads as the modal
  being undismissable. Dismiss it by testid, which is unambiguous:

  ```bash
  ./control-kiyotaka browser find testid guest-signup-modal-close-btn click
  ```
- **The signup modal is not the only overlay that blocks a mid-drive click.** Any
  guest-walled control (`promptGuestLogin`) raises the sign-in dialog in the same
  `.dialog-style.dialog-overlay` shell, since `4b8f78a775` a sheet with the
  extra class `login-signup-overlay`. Its visible heading is the walled
  feature's name (`Watchlist`, `Chart Actions`, `Share Your Chart`) over
  `Sign in or create an account`; a testid listing of the overlay starts with
  `login-signup-welcome-spoken` and `auth-mascot` (driven 2026-11-04; the
  hidden `forgot-password-*` pane that used to come first is gone). Identify
  what is on top before dismissing: a
  `[data-testid=guest-signup-modal-close-btn]` probe tells the two apart — it is
  absent on the wall, present on the signup modal.
  **The wall has no close button, but `Escape` clears it.** It carries no close
  control in its button list, which reads as undismissable; pressing `Escape`
  takes `dialogStore.isAuthenticationDialogOpen` back to `false`, leaves the
  overlay count at `0`, and the very next click lands normally. Reloading the lane
  also works and costs a 45-115s re-boot, so reach for `Escape` first:

  ```bash
  ./control-kiyotaka browser press Escape
  ```
- **The ink tutorial's dismissal is permanent by any route.** X, Escape, the
  backdrop and a swipe all write the seen flag, so a second run on the same
  browser profile meets only the signup modal — a recipe that expects two
  overlays every time is wrong after the first run.
- **OI and FUNDING do not render on the default market — confirmed live.** The guest default is
  COINBASE BTC-USD, which is SPOT, and `isOiSupported`/`isFrSupported` are
  futures-only — so the live edge carries price, change and `24H VOLUME` only. A
  recipe that asserts `OPEN INTEREST` or `FUNDING / COUNTDOWN` on a default boot
  fails on a healthy lane. Switch to a perp (e.g. BINANCE.F BTCUSDT) to prove
  those two. At narrow widths the cells fold into `tb-ms-price-trigger`.
- **The signup modal now waits 15s after the last blocking surface.** A
  `GUEST_PROMPT_SURFACE_GAP_MS` of 15000 was added, so it does NOT raise the
  moment you dismiss the ink tutorial — allow 15s of no pointer or key input
  before concluding it is gone. The gate also treats the indicator and layouts
  dialogs as blocking.
- **The ink tutorial has input-sensitive gates.** It needs ~4s of no press or key
  and ~1.5s of no pointer movement, retries on a long interval, and never opens in
  a screenshot-render context — so a driver that clicks continuously can delay it
  indefinitely. Poll for `ink-tutorial` rather than assuming a fixed delay. Its
  "once per device" scope is localStorage for guests but per-account when signed
  in. `ink-tutorial-close` resolves on mobile too (the sheet reuses the testid).
- **The signup modal is no longer the first overlay a guest meets** (but on
  2026-11-18 the order was reversed: the signup modal was up at first
  candles and the ink tutorial raised once it was closed; clear whichever is
  on top by its own testid). A once-per-
  device `InkTutorialDialog` ("Draw by holding") arms shortly after first paint
  and sits in the SAME `.dialog-style.dialog-overlay` shell, so it blocks clicks
  identically — but it answers to a different testid, and probing the signup
  modal's returns `No element found by testid 'guest-signup-modal-close-btn'`,
  which reads as an undismissable modal. Clear it by its own handle, and expect
  the signup modal to raise the moment you do, because the tutorial was
  suppressing it:

  `ink-tutorial-close` is DESKTOP ONLY (mobile uses a sheet), and there is also an
  `ink-tutorial-got-it` button. The tutorial's card now carries
  `role="dialog" aria-modal="true"` while the shell stays `.dialog-style`, so the
  documented union still counts it — but a bare `[role=dialog]` count now rises
  for the tutorial and still not for the signup modal.

  ```bash
  ./control-kiyotaka browser find testid ink-tutorial-close click
  ./control-kiyotaka browser find testid guest-signup-modal-close-btn click
  ```

  Its card testids are `ink-tutorial`, `ink-tutorial-close` and
  `ink-tutorial-card-<tool>`. Two overlays in a row is the normal first boot, so
  re-read the overlay count after each dismissal rather than shooting.
  **The order is not fixed.** Driven 2026-10-27 on a fresh profile: the SIGNUP
  MODAL raised first, and the ink tutorial raised only after it was dismissed. A
  loop that reads the top overlay's testids and dismisses whichever is there
  (`ink-tutorial-close`, else `guest-signup-modal-close-btn`, else `Escape`)
  handles both orders.
- **The signup modal is time-gated, so an early screenshot is not proof it is
  gone.** It arms only after the first chart paint plus ~8s of visible time, then
  waits for ~2s idle. Poll past that window before deciding the coast is clear.
- **The latch is per TAB, and the modal burns the bar's day too.** Showing the
  modal writes a sessionStorage latch AND marks the prompt bar as shown for that
  local day, so a second drive in the same tab on the same day gets **neither**
  surface — not a bar. `control-kiyotaka browser open` lands in a fresh tab, which
  resets the latch and brings the modal back, which is why it can reappear
  mid-session after a reopen. `GuestSignupPromptBar` (non-blocking, different
  testids) is the only surface a MOBILE guest gets, and it arrives on the first
  eligible tick rather than a later day; on desktop it still needs a later local
  day, so a frame comparison across drives can be comparing two different
  surfaces.
- **The modal waits for you to get out of the way, then pops.** Its gate suppresses
  firing while any `.dialog-style` / `.q-dialog` is open, so it deliberately holds
  until the driver closes whatever it opened and then raises over the next step.
  That is the common way a mid-run capture photographs the modal.
- **A hidden page applies no live ticks.** The worker holds the batch and drains
  it on the visible flip, so the tail stays frozen while hidden and jumps on
  return. Toggling the feed while hidden can never draw lone bars; synthesize the
  damage instead (see Driving the wake heal).
- **A fresh worktree has no `.env.local`.** It is gitignored and lives only in the
  main checkout, so a lane started from a new worktree boots with no
  `VITE_DEV_TOKEN` and no backend proxy target. Driven 2026-10-27: the chart reads
  `Retrying data request...` and `Reconnecting…` forever, `rawData.length` stays
  `0`, and the console carries `Backend error: unauthenticated` from the gateway
  (`Error fetching main data`, `Initial candle fetch failed after chart wiring`)
  plus `[refresh-token] all retries exhausted` 502s. `doctor` stays green through
  all of it. Link or copy it in before `up`:
  `ln -s <main checkout>/.env.local .env.local`, then restart the lane. With it,
  the same lane drew 250 candles in about 30 s.
- **A wake stalls at the token refresh when the backend is unreachable.** Every
  wake refreshes first; with `VITE_BACKEND_PROXY_TARGET` down (Tailscale off on
  this machine) the refresh 502s and retries, the ring stops at `wake-received`,
  and no heal ever runs. Check
  `curl -X POST http://127.0.0.1:<lane>/api/v1/auth-v2/refresh-token` returns
  200 before any wake recipe.
- **`control-kiyotaka` is not in the product tree.** It is git-excluded there
  and a fresh clone or worktree lacks it; on 2026-11-01 the only copy outside
  the hub (`dev-notes/openmarket-landing-revamp/capture-app/`) hung on an
  iCloud read, so the wrapper was regenerated as the hub's tracked
  `bin/control-kiyotaka` beside this map (its delivery is the ordinary review
  path, not the map sync). It resolves the checkout from `KIYO_REPO` or the
  caller's `git rev-parse --show-toplevel`, takes `KIYO_LANE_PORT` and
  `KIYO_SESSION`, launches `node node_modules/vite/bin/vite.js --config
  qa/verification/vite.config.ts --host 127.0.0.1 --port <lane> --strictPort`
  with `VITE_BACKEND_PROXY_ORIGIN=http://localhost:8080`, and its `doctor`
  adds a `load` line and probes the backend through the lane's own `/api/v1`
  proxy instead of `:3000`. Without it, start the lane by that `node` command
  and record the pid.
- **The headless tab drifts to `visibilityState: hidden` mid-drive.** Driven
  2026-10-27: with one tab in the session, the page went `hidden` twice within
  ten minutes. `requestAnimationFrame` stopped, the footer UTC clock froze, and
  the app ran its hidden path while every `eval` kept answering. Screenshots
  still captured, which hides the problem. Read `document.visibilityState` before
  a capture, and bring the tab back with
  `./control-kiyotaka browser tab t1` (the tab id from `browser tab list`;
  `tab 1` is rejected, the id must be `t1`). A return after more than 60 s hidden
  is a real wake, so expect the wake chain in the ring. Re-confirmed 2026-11-01:
  the tab was `hidden` within a minute of `open`, the footer clock froze at
  `21:20:54` across three panel frames, and `tab t1` brought it back; the ring
  then logged 13 `lifecycle-hidden-return` rows over the pass. Again
  2026-11-18: the clock froze at `20:13:48`, the Orderbook opened with an
  empty body and no TPO hover card would show; `tab t1` brought the ladder and
  the card back. Again 2026-11-19: the Orderbook opened with only its column
  heads while `visibilityState` read `hidden`; `tab t1` filled the ladder.
  Again 2026-11-20: at least seven drifts in one pass. Two drives that
  failed once (an `Escape` that left the legend's `More` menu open, and a
  bare letter over the toolbar that opened nothing) were each followed by a
  `hidden` read and passed after `tab t1`. Read `visibilityState` and run
  `tab t1` before every drive step, not only before a capture.
- **The v2 gateway is a tailnet-only name; when it stops resolving, every live
  surface goes quiet while candles still paint (seen 2026-11-01).** From about
  21:55 UTC `tsdb-gateway.int.ore.kiyotaka.ai` returned NXDOMAIN from the
  system resolver and from `1.1.1.1` and `8.8.8.8`; only `100.100.100.100`
  answered (`10.1.1.10`), and `tailscale dns status` listed no split route for
  it. The lane then logged `v2 Streaming socket error` and `v2 Orderbook socket
  error` by the hundred, the ring filled with `v2-socket-error`, `-redial` and
  `-flip`, three wakes ended in `wake-failed`, `connection-status-chip` read
  `Reconnecting…`, OI and funding read `—`, and Tape and Orderbook stayed
  empty; the forming candle still ticked on the socket that survived. A reload
  drew 440 candles from the OHLCV cache (`ohlcv-cache-read`,
  `main-cache-painted-marked`) with no `cached-paint-veil`, because the cached
  tail was the current bar. `doctor`'s `v2 gateway` line flipped to
  `UNREACHABLE`, so run `doctor` before reading an empty live panel as a
  regression, and never drive the wake heal during it: the heal needs the
  backfill.
- **On 2026-11-03 the gateway name stopped resolving through the system
  resolver while the tailnet answered it, and a resolver map in the browser
  was enough to drive.** About two minutes after `up`, `nc` and `curl` failed
  with `nodename nor servname provided` (getaddrinfo), while `nslookup
  tsdb-gateway.int.ore.kiyotaka.ai 100.100.100.100` and a plain `nslookup`
  both answered `10.1.1.10` and `curl --resolve
  tsdb-gateway.int.ore.kiyotaka.ai:443:10.1.1.10 https://…/` returned `302`.
  The page stuck at 1 bar with `Can't reach live data. Retrying...` and
  `v2 Streaming socket error`, and a re-run of `doctor` flipped `v2 gateway` to
  `UNREACHABLE`. Relaunching the session's browser with
  `--host-resolver-rules=MAP tsdb-gateway.int.ore.kiyotaka.ai 10.1.1.10`
  appended to the wrapper's software-GL args drew 250 candles in 30 s and kept
  every live surface working for the whole pass. The wrapper has no switch for
  extra args, so call `agent-browser --session "$KIYO_SESSION" --args
  "--use-angle=swiftshader,--enable-unsafe-swiftshader,--host-resolver-rules=MAP
  tsdb-gateway.int.ore.kiyotaka.ai 10.1.1.10" …` for every browser command of
  the run. A `control-kiyotaka browser …` call in between relaunches the
  browser without the map and lands on `about:blank`. `doctor` keeps reading
  `UNREACHABLE` because its probe uses the system resolver, so record that
  you drove past it. Read the address from `nslookup … 100.100.100.100` on the
  day rather than copying `10.1.1.10`. **On 2026-11-06 the tailnet resolver
  answered NXDOMAIN too**, and `10.1.1.10` still served the gateway
  (`curl --resolve tsdb-gateway.int.ore.kiyotaka.ai:443:10.1.1.10
  https://tsdb-gateway.int.ore.kiyotaka.ai/v2/` answered `400`, the websocket
  path without an upgrade). With that address in `KIYO_BROWSER_ARGS`, `doctor`
  passed and the lane drew live candles all pass. So try the last known
  address before calling the pass blocked.
- **`boot-connection-card` (driven 2026-11-18 on `cff04f9a01`;
  `2ad3af4310`).** `find testid footer-connection-btn click` opens the card:
  `connection-status-headline` `Connected`, `connection-status-help` `Orders
  and prices arrive on time.`, the root's `data-net` `good` (`slow` on a slow
  network) and `connection-leg-ping` `Ping 13 ms`. `trade-network-mark`, the
  slow-network mark on desktop ticket title bars, needs a trading session.
- **`boot-countdown` (driven 2026-11-19 on `413f86e5af`; `de94b0271b`).**
  The countdown is drawn on the canvas, so the proof is the pixel frame: the
  DOM corner `price-scale-corner-countdown` stays empty. With no stored
  choice the tag under the last price read `11:02` on the boot COINBASE
  BTC-USD 1h, `10:23` on INDEX DXY 1h and `38:40` on AAPL 1h. AAPL showed it
  because this seat leaves the stocks plane unrouted (see the README's
  Baseline preconditions), so no delayed tier applies. **Since `fc0f54ec54`
  a delayed feed shows the countdown too (source, not driven):** the engine
  reads a feed clock that is server time less the served delay (CME 10
  minutes, the stocks tape 15), so the tag reaches `00:00` when the bar
  closes on the user's screen. No word or tooltip beside it says so yet.
  The older claim here, that a delayed feed holds it off, is stale. Only a
  calendar interval (`1M`, `3M`, `6M`, `1Y`) still holds it off
  (`shownCandleCountdown` in `src/utility/chart/candle-countdown.util.ts`).
  **Driven 2026-11-20 on `7c937b0a1f`:** on HYPERLIQUID.F BTC, after
  `tb-interval-option-1M-btn` (26 bars) the price tag showed no countdown
  while `price-scale-corner-countdown` still read `aria-pressed` `true`;
  back on 1h the tag read `36:12`. The
  Super Search setting row and Apply to all charts read the same default
  (source).
- **`boot-intent-warm` is removed (`a8935a39a2`; absence driven 2026-11-21
  on `92f4a841ef`).** `src/utility/chart/market-intent-warm.request.ts` is
  deleted and the symbol dialog, Super Search and the watchlist no longer
  warm a row under the pointer. With `__enableKiyoLazyLoadDebug()` and
  `__enableKiyoLazyLoadVerboseTicks()` on, the symbol dialog filled with
  `ETHUSDT` and two real `mouse move` calls resting on the `WBETH` row and
  then the `ETH` row (2.5 s each), the dump's 558 lines held no row whose
  `details.lane` is `market-intent` and no `dispatched`, `fetched` or
  `fresh-skip` line. The recipe below is the 2026-11-20 one, kept for the
  ring's handles; it no longer reproduces.
  **As driven 2026-11-20 on `7c937b0a1f` (`de79b1d733`, `0d9aee7ad3`,
  `b27e0f8d6c`).** The only observable was the debug ring.
  `eval "window.__enableKiyoLazyLoadDebug()"`, then
  `eval "window.__enableKiyoLazyLoadVerboseTicks()"`: without verbose ticks
  the dump folds a second's `interval-prefetch` rows into one
  `kscript-tick-rollup` count with a single exemplar, so `dispatched` and
  `fetched` are lost. `window.__dumpKiyoLazyLoadDebug()` returns a string of
  JSON lines; match the rows whose `details.lane` is `market-intent`. Open
  the symbol dialog, fill `ETHUSDT`, and move the pointer onto a row with
  two real `mouse move` calls (rows are `[data-flat-index]`; the first sat
  at `594 334`). Read: `dispatched` then `fetched` for `BINANCE` `WBETHUSDT`
  `1h`, and on the first row `dispatched` then `fresh-skip` for
  `BINANCE_FUTURES` `ETHUSDT` `1h` (it had been warmed a moment before).
  Moving between rows logged `aborted` with `reason` `superseded`. A
  `mouse down`, `mouse up` on the row logged `kept` with `reason` `press`
  and the chart switched to BINANCE.F ETHUSDT. Turn the ticks off after
  (`__disableKiyoLazyLoadVerboseTicks()`). Not driven: the Super Search
  cursor's warm (`kept`, `pick`), the `ineligible` rows for a stock or CME
  row, a touch pointer (`pointer-gated`), and the `switch-prefetch-join`
  ring the product doc names (no such row was in the dump).
- **`boot-glide` (`0cb582eb9f`, `02de83a38a`; driven 2026-11-20 on
  `7c937b0a1f`).** Sample the view each frame with a
  `requestAnimationFrame` loop over `window.tc[0].lastProcessedRange`
  (`startKey`, `endKey`). Drag the plot back (`mouse down` at `600 450`,
  moves to `900 450`, `mouse up`): the range read `325..580` and
  `chart-nav-scroll-latest` appeared. `press "Alt+Shift+ArrowRight"` with
  Lite charts off stepped `348`, `367`, `381`, `390`, `394`, `395..649`
  over about 500 ms, and the Latest button left at the end. **With Lite
  charts on, which is this lane's own default, the same press cut in one
  step** (`86..341` to `145..399`): the glide is off under the
  fewer-frames lever (source: also on heatmap and volume-candle plots, with
  OS Reduce Motion, and past three spans). Turn Lite off through
  `light-charts-chip` then `light-charts-turn-off`, and back on through the
  Performance page (see `set-lite`). The nav overlay buttons
  (`chart-nav-scroll-left`, `-right`, `-zoom-in`, `-zoom-out`, `-reset`)
  were covered by the canvas for a `find testid` click; `mouse wheel` did
  not move the range. Not driven: `Reset view` (`Alt+R`), a far target's
  cut, and the Auto ease.
- **`boot-footer-session` (driven 2026-11-19 on `413f86e5af`;
  `5b02dfdcb9`).** The session word is a menu button, not a flip. On AAPL 1h,
  `footer-session-toggle-btn` (text `RTH`, `aria-label` `Regular hours`,
  `data-session` `regular`, `aria-haspopup` `menu`) opened
  `footer-session-menu` (`role=menu`) with `footer-session-menu-row-regular`
  (`RTH · 09:30 to 16:00 New York`, `aria-checked` true) and
  `footer-session-menu-row-extended` (`ETH · 04:00 to 20:00 New York`).
  Picking ETH set `data-session` `extended` and the word `ETH`, and the chart
  reloaded (252 to 254 bars). A session the interval cannot use is disabled,
  with a caption that it needs an intraday interval (source,
  `FooterChartSessionMenu.vue`). `footer-back-adjust-toggle-btn` needs a CME
  continuous chart, which this seat cannot open. Since `7ef0ab4bc6` a pane's
  B-ADJ choice is kept per pane in localStorage `chart.backAdjustMemory`
  through a detour to another market (source).
- **A yellow strip replaced the chip (driven 2026-11-06 on `8bcd72f8f5`;
  `b2623958e8`, waits from `c16de1bf2e`).** `connection-strip`
  (`src/components/banners/ConnectionStrip.vue`, mounted in `ChartArea.vue`;
  since `22fc0cede7` also on the phone's Chart tab, where 30 s of `long`
  reloads the page once with a 5 min cooldown) carries `data-state` and the
  children `connection-strip-lead` and `connection-strip-body`:

  | `data-state` | Lead | When |
  |---|---|---|
  | `stall` | `Your network is slow` | degraded for 15 s (was 3 s) |
  | `offline` | `You're offline` | the browser is offline, confirmed for 3 s |
  | `long` | `Still reconnecting`, plus `connection-strip-reload` (`Reload`) | 30 s into the stall, or at once when nothing retries |
  | `back` | `Back to live` / `Caught up.` | for 2 s after recovery |

  The footer's Wi-Fi meter turns amber after 5 s pending and a pane's live
  label waits 5 s. Since `1e45e23e73` the strip says reconnecting only on
  transport evidence (a down socket, a failed dial, a stalled worker), never
  on a tab-return catch-up, and since `69247f4c27` a socket found dead on a
  tab return is said at once (source). The `stall` and `long` waits are not
  driven: they need a blocked socket host, not `set offline`.
  Live 2026-11-07 on `dced88e06a`: `offline` within 6 s and `back` (`Back to
  live` / `Caught up.`) within 1 s of `set offline off`, but **`back` stayed
  up for over 20 s while the tab had drifted hidden**, and the node was gone
  the moment the tab was re-fronted. Read `document.visibilityState` before
  calling a stuck `back` a regression. Since `6a61d91e3d` a stall of 3 s or
  more that clears inside the 15 s wait is reported as a quiet episode, with
  nothing on screen (source).
  Live 2026-11-06: `./control-kiyotaka browser set offline on` raised
  `offline` (`You're offline` / `The chart catches up when your connection is
  back.`) at the 5 s poll (none at 4 s); `set offline off` showed `back`
  within 1 s. On 2026-11-05: `offline` within 2 s; `set offline off` showed
  `back` for about 2 s and then no node. When the
  gateway name stopped resolving the strip stood at `long` with the Reload
  button. `connection-status-chip` was absent the whole time:
  `ConnectionStatusChip.vue` shows only when the strip does not, so on desktop
  the chip bullets below describe the mobile shell. A healthy lane has neither
  node. The same commit embeds the data worker in the bundle, so it starts
  without a separate download. Since `af8856d595` any worker message counts as
  liveness, and an `exhausted` worker that stayed silent gets one more
  replacement every 300 s of visible time (source).
- **The connection chip has a `Slow network` state and a worker watchdog
  (source, `0c4e1493f7`, `7e92b90d2f`; read on `215896e614`, not driven).**
  `useConnectionLatency.ts` adds the status `slowNetwork` (label `Slow
  network`) while `dataWorkerHealth` is `slow`; `stalled` and `replacing` read
  `reconnecting` and suppress `connection-status-reconnect` (the button needs
  the worker `ok`), and `exhausted` reads `disconnected` with
  `connection-status-reload`. The watchdog
  (`src/utility/perf/data-worker-watchdog.util.ts`) replaces a data worker
  silent for 30 s of visible time or without its implementation for 40 s. Its
  commit says it is on in production and opt-in in dev, so a lane may never
  show it. Since `734d51a814` the chip shows one glyph per state, read from
  its `data-glyph` (`signal-none` connecting, `signal-weak` for `slowNetwork`
  and high latency, `retry` reconnecting, `signal-off` offline, `alert`
  disconnected) with a tone class `conn-chip--<tone>`, and a slow start also
  reads `Slow network`; since `c16de1bf2e` a degraded state must last 15 s
  before the chip shows, the strip's own rule (source). A healthy guest lane has no `connection-status-chip` node at all
  (driven 2026-11-04).
- **Boot shows one loader now (source, `d4c822292e`, `c798f8a110`; driven
  2026-11-01).** The `index.html` start screen (`#skeleton-loader`) stays up
  until the first candles paint (`skeleton-loader:route-painted`, `.sk-cut`
  removes the fade), `ChartLoadingOverlay` leaves the DOM in the same update,
  and the strips whose input lands after the first paint keep their boxes. Live:
  by the time `rawData.length` passed 50 the skeleton was gone and no
  `chart-loading-overlay` existed. A frame with the skeleton over drawn candles
  is a bug, not timing.
- **Table reads can route to the v3 gateway with a v2 fallback (source,
  `5acf997da4`, read on `120d5d5d32`).** A refused or hung v3 dial falls back
  to v2 and cools down for 60 s (ring `gateway-v3-lane-fallback` with
  `dial-failed`, `did-not-open` or `cool-down`; `v3-read-bounced` on a re-send),
  and a lane that never reopens fails after 50 s with `data plane unavailable
  (gate acquire timeout on <lane>)`. Whether a guest rides v3 depends on
  `gatewayProtocolFor`. **A guest rides v3 from its first dial since
  `9d2bbbeaa0` and `0fdc88b40f`:** `GUEST_DEFAULT_FLAGS` maps `gateway-v3`
  to `GUEST_GATEWAY_V3_DEFAULT` (`true`, `src/utility/boot/gateway-v3.util.ts`),
  a boot with no saved signed-in session dials by that constant and never by
  the `kiyo:gateway-v3` mirror, and only a `kiyo.flag-overrides` entry beats
  it; no kill switch reaches a guest, so the way back to v2 is a release.
  Driven 2026-11-25 on `ec531568de`: `isOn('gateway-v3')` `true`, and a CDP
  capture of a reload's `Network.webSocketCreated` events (auto-attached to
  the workers) read `wss://tsdb-gateway…/v3/?dial=…` at 2.5 s, then
  `wss://tsdb-gateway…/v2/?dial=…` at 3.6 s, so a v2 socket still opened
  beside it then. **Since `ddfe3af943` a `/v3` page opens no `/v2` socket
  for its session (driven 2026-11-26 on `1d1a3e1410`).** A v2 slot opens
  only when a read needs it (the exchange list with no venue) and closes
  after 120 s idle, and the page posts its login to the worker
  (`V2_SET_TOKEN`) on each new token and every 30 s while a `/v3` lane is
  open (`0d2da5f7c1`, source). Live: a CDP capture of a reload's
  `Network.webSocketCreated` events over 45 s read the vite socket,
  `wss://tsdb-gateway…/v3/?dial=…` at 3.1 s and the two `ap-sin3` sockets,
  and no `/v2/` socket. Since `4f44df83b8` a production build reads the
  `/v3` host from orange's `GET /api/v1/v3-endpoint` (kept 1 h in
  `localStorage` `kiyotaka:v3-endpoint`); a dev lane skips the discovery
  and dials the v2 host's `/v3` twin (`kiyotaka:v3-endpoint` read `null`
  on 2026-11-26). (From `b5d0fe6b0f` to `9d2bbbeaa0` a guest stayed on v2; a live
  guest read `isOn('gateway-v3')` `false` on 2026-11-05.) Read a `—` in the live edge as
  a silent lane, or as a hidden tab (on 2026-11-05 the ticker's price slot read
  `—` while the tab was hidden and the price as soon as it was re-fronted).
- **The candle cache was reset once (source, `a3f815101e`).** The OHLCV cache
  database moved to version 5, so the first load of a browser profile on this
  tree drops the old store and boots cold (no `ohlcv-cache-read`); reloads after
  that read the cache again.
- **Left pans after a symbol switch keep loading (source, `47056ca94c`,
  `7268a45a6c`, `bf5f78f037`, `120d5d5d32`; not driven).** The engine's
  lazy-load boundary resets on every switch (`lazy-load-left-boundary-reset`),
  a pan swallowed behind a switch's held gate slots is replayed
  (`lazy-load-round-unsent`), and the left-exhaustion latch is shared by index-
  and time-mode rounds (`lazy-load-left-exhausted`, 60 s TTL, released by a
  socket reopen or a wake). Proof would be `rawData.length` growing on a wheel
  pan left after a same-interval switch; the gateway outage took the slot.
- **A guest boot may show no overlay at all for a while.** On 2026-11-01 the
  first candles arrived with the overlay union at `0`; the signup modal came up
  about two minutes in (`guestVisitCount` 1, `modalShownThisSession` false until
  then) and the ink tutorial AFTER it, during the first dialog drive. Read the
  top overlay before every click; `dismiss` nothing on faith. On 2026-11-02 the
  signup modal (`guest-signup-prompt-modal`) was up about 20 s after the first
  candles and no ink tutorial appeared on the reused browser profile.
- **The connection chip carries Reconnect and Reload buttons now (source,
  `e2967128e2`; read on `a4488341f6`, absent on the healthy lane).**
  `connection-status-chip` (`src/components/common/ConnectionStatusChip.vue`)
  is `role="status"` with a `data-status` attribute and ignores pointer events
  itself; inside it `connection-status-reconnect` (`Reconnect`) renders when
  the status is `reconnecting`, the candle socket is not `open`, the last
  failure is not a kick and at least one establish timed out or failed
  (`reconnectEligible` in `useConnectionLatency.ts`), and
  `connection-status-reload` (`Reload`) after a Reconnect whose dial also
  expired, and since `0c4e1493f7` also when the data worker is `exhausted`
  (see the watchdog bullet). The chip shows after 2 s of degraded state and hides a cold-boot
  `reconnecting` until the first healthy observation unless the reach state is
  `unreachable`. Reconnect marks the edge host suspect and writes the ring
  event `v2-socket-route-forced`; every dial writes `v2-socket-route` (`slot,
  route, reason, host, suspectUntil, pinnedUntil`) and localStorage
  `kiyotaka:v2-route` persists the edge-or-direct decision. Console warnings
  start `Connection chip:` and `Reconnect:`. On a healthy lane the chip is
  absent (`null`), so a guest lane proves only absence; an outage like the
  2026-11-01 one is where the buttons appear.
- **A window cell's loader names the window (source, `301ef7e764`).**
  `chartArea.loadingWindow` = `Loading {name}...` applies to wrun window cells
  only and falls back to `Loading indicators...`; a plain chart still reads
  `Loading chart...` and `Loading candles...`, and `pane-loading-overlay.util.ts`
  keeps a window cell from ever showing those. The OI fallback stamp is gone
  from the options heatmap chip. `584eae0ca8` stops re-downloading held rows
  (`main-cache-reserve.util.ts`, `overlay-held-source.util.ts`; ring
  `main-fetch-reserve-ineligible`, `main-cache-reserve-released`, and
  `main-fetch-reserve-miss` or `-served` only on a warm reopen); none seen on
  a cold boot.
- **The hidden tab, re-confirmed 2026-11-02, and the Orderbook is its canary.**
  The tab read `hidden` within a minute of `browser open` and again after
  every later `open`; the footer clock froze (`21:13:34` across four panel
  frames), the Tape kept printing, every `eval` answered, and the Orderbook
  never mounted `orderbook-canvas` until the tab was fronted (40 s on ETHUSDT,
  24 s on SOLUSDT; 5 s once visible). A `tab t1` sent straight after an `open`
  did not take; `browser tab` (the list) and then `tab t1` did, so read
  `document.visibilityState` back before trusting it. See [right-side
  panels](./right-side-panels.md).
- **Two routes outside the chart, driven 2026-11-02.** `/chart/clip/<id>` is
  the only clip surface a guest reaches ([clip guest page](./clip-guest-page.md));
  without the `/chart/` base vite answers with its base-URL hint page instead
  of the app. `/chart/board/clips` sends a guest back to `/chart/`. Either
  `open` reloads the tab, so dismiss the overlays and re-front it before the
  next chart drive.
