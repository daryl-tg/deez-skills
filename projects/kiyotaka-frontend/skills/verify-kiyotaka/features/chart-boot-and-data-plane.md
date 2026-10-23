# Chart boot and the data plane

Opening `/chart/` mounts the chart engine, starts the Web Worker that owns every
websocket, and draws candles for the last-used symbol. Every other proof in this
map depends on this one working, so verify it first and never assume it. This
entry was DRIVEN on 2026-10-23 against product tree `2a1ed750db` on a real
guest-JWT lane: 250 candles, two metadata rows, 1h, the COINBASE default, a
clean worker console, and the absence of OI/funding on spot; coverage
was boot to 250 candles, the two-row overlay set, interval, the default market,
and a screenshot. The worker-death console grep and the live ticker values were
NOT re-run this pass; their last live check was 2026-10-06.

## Sub-features

- `boot-mount` the engine mounts and the ticker bar renders.
- `boot-candles` candles reach the engine and draw.
- `boot-live` the live edge updates (price, 24h volume, open interest, funding).
- `boot-worker` the worker is alive, so websockets can open at all.
- `wake-heal` after a hidden or sleeping stretch, the wake backfills every blank
  slot the outage left, including slots before lone bars a trickling feed drew.

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
- **Proof.** Dismiss the guest modal and capture in the same step — it re-raises:
  `./control-kiyotaka browser find testid guest-signup-modal-close-btn click` then
  `./control-kiyotaka browser screenshot artifacts/<run>/<rev>/boot-candles.png`,
  with `./control-kiyotaka browser snapshot -i -c` saved beside it. Confirm
  nothing is on top first, with the union rather than a bare dialog count:
  `eval "document.querySelectorAll('.q-dialog, .dialog-style, [role=dialog].open').length"`
  must read `0`.
  Then **open the PNG**: it must show drawn candlesticks, not a dialog. The
  engine read is the side effect; the frame is the only proof pixels arrived.

## Driving the wake heal

Last driven 2026-10-22: base `b153a7751a` against the fix branch
`daryl/wake-heal-interior-hole` (`5287b9a644`, not yet on `main`), guest
COINBASE BTC-USD 1m, in headless Chromium and in the desktop shell. NOT driven: a
real OS sleep with macOS dark wakes; the trigger below is synthesized.

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
  false, syntheticFlags })`. Make the hole longer than the 2-bar lookback
  (`WAKE_RESYNC_MAIN_LOOKBACK_BARS`), or both builds heal it: hide ~6.5 min.
- **Read the verdict from the engine and the ring.** After the wake, count NaN
  closes in `tc[0].metadata[0].rawData` between the last real bar and the lone
  bar. With `window.__enableKiyoLazyLoadDebug()` on, `__dumpKiyoLazyLoadDebug()`
  returns an ARRAY of `{event, details}`: `lifecycle-wake-emit` carries
  `outageStartedAt`, and `wake-resync-pass` carries `mainStartMs` and `lastBarMs`.
  Measured: base kept 2-4 blank slots (heal from `lastBar - 2 bars`); the fix
  left 0 (heal from the outage start).
- **Frame it.** Wheel over the plot until the engine viewport
  (`metadata[0].viewport.endTs - startTs`) spans ~30 bars, re-read before each
  shot; a fixed wheel count over- or under-shoots. Dismiss `Got it` first.
- The script is kept with the run's notes
  (`dev-notes/desktop-chart-sleep-wake-gap/lone-bar-repro.mjs`, and
  `desktop-repro.mjs` for the shell, which must pick the window whose URL holds
  `/chart/`: the title bar's `data:` view loads first).

## Gotchas

- **Zero bars plus `v2 streaming websocket connection failed` is almost never the
  socket.** The worker owns the websockets, so a dead worker presents as a
  connection failure. Check `doctor`'s `chart-schema` line first: a sibling
  `orange-shared` behind this repo's pin kills `worker-impl` at module scope.
- The chart answers HTTP and mounts `window.tc` well before it has data. Asserting
  on mount alone passes on a permanently empty chart.
- Candles do **not** need the backend. `:3000` down still draws them **and still
  fills volume/OI/funding** (those ride the v2 gateway too); it removes login,
  workspaces, and the official catalog.
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
  `.dialog-style.dialog-overlay` shell, and it reads as "Back to log in / Forgot
  your password?". Identify what is on top before dismissing: a
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
- **The signup modal is no longer the first overlay a guest meets.** A once-per-
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
  main checkout, so a lane started from a new worktree boots with no gateway URLs
  and reads "Retrying data request..." forever. Copy it in before `up`.
- **A wake stalls at the token refresh when the backend is unreachable.** Every
  wake refreshes first; with `VITE_BACKEND_PROXY_TARGET` down (Tailscale off on
  this machine) the refresh 502s and retries, the ring stops at `wake-received`,
  and no heal ever runs. Check
  `curl -X POST http://127.0.0.1:<lane>/api/v1/auth-v2/refresh-token` returns
  200 before any wake recipe.
- **`control-kiyotaka` may be absent.** It is git-excluded tooling and a fresh
  clone or worktree lacks it; start the lane with
  `pnpm exec vite --host 127.0.0.1 --port <lane> --strictPort` and record the pid.
