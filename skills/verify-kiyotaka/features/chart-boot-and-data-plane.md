# Chart boot and the data plane

Opening `/chart/` mounts the chart engine, starts the Web Worker that owns every
websocket, and draws candles for the last-used symbol. Every other proof in this
map depends on this one working, so verify it first and never assume it.

## Sub-features

- `boot-mount` the engine mounts and the ticker bar renders.
- `boot-candles` candles reach the engine and draw.
- `boot-live` the live edge updates (price, 24h volume, open interest, funding).
- `boot-worker` the worker is alive, so websockets can open at all.

## How to get to it (user POV)

- Open `http://127.0.0.1:<lane>/chart/`. Nothing to click; the chart restores the
  last symbol (a guest with no stored state lands on `BINANCE.F BTCUSDT PERP` at
  `1h`). Read `chartStore.activeInterval` rather than assuming an interval — a
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
  A healthy guest boot returns ~250 bars. **Assert the bar count, not the overlay
  count**: the same lane returned 4 overlays on one boot and 3 on the next, because
  the restore of the guest's own heatmap/CVD overlays can fail independently of the
  candles (it raises `Error initializing overlay` in the console). `metadata.length`
  is not a stable proof; `metadata[0].rawData.length` is.
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
- **The signup modal is no longer the first overlay a guest meets.** A once-per-
  device `InkTutorialDialog` ("Draw by holding") arms shortly after first paint
  and sits in the SAME `.dialog-style.dialog-overlay` shell, so it blocks clicks
  identically — but it answers to a different testid, and probing the signup
  modal's returns `No element found by testid 'guest-signup-modal-close-btn'`,
  which reads as an undismissable modal. Clear it by its own handle, and expect
  the signup modal to raise the moment you do, because the tutorial was
  suppressing it:

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
