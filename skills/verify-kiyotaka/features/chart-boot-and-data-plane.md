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
  `Error initializing worker` and `V2StreamingConnectionUnavailable`. Either one
  present means the data plane is dead and every downstream proof is void.
- **Confirm the live edge.** Run
  `./control-kiyotaka browser eval "(()=>document.body.innerText.slice(0,300).replace(/\s+/g,' '))()"`.
  It carries the symbol, price, `24H VOLUME`, `OPEN INTEREST`, and
  `FUNDING / COUNTDOWN`. `—` in the volume/OI slots means the `/api` proxy is
  down (backend lane), not that the chart is broken.
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
- Candles do **not** need the backend. `:3000` down still draws them; it only
  removes login, workspaces, volume/OI/funding, and the official catalog.
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
  `.dialog-style.dialog-overlay` shell, and it has no close button in its button
  list — it reads as "Back to log in / Forgot your password?". Identify what is on
  top before dismissing: a `[data-testid=guest-signup-modal-close-btn]` probe tells
  the two apart, and the sign-in wall is cleared by reloading the lane, not by a
  close click.
- **The signup modal is time-gated, so an early screenshot is not proof it is
  gone.** It arms only after the first chart paint plus ~8s of visible time, then
  waits for ~2s idle. Poll past that window before deciding the coast is clear.
- **It raises as a modal once per browser session, then downgrades to a bar.** The
  once-per-session latch means a second drive in the same tab gets
  `GuestSignupPromptBar` instead, which is non-blocking and carries different
  testids. Both answer to `--name "Close"`, so the dismiss step still works, but a
  frame comparison across drives is comparing two different surfaces. Discarding
  the browser profile resets the latch and brings the modal back.
