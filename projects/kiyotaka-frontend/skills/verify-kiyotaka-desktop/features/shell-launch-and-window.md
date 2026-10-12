# Shell launch and window

The shell opens one window on the chart for its channel, production by default, takes a single-instance lock so a
second launch focuses the first window, and remembers the window's position, size and maximized state across launches.
`launch-chart` was driven on 2026-10-12 against product tree `d554bfb38c` through this wrapper's `lane up`, `doctor`
and `capture` (unit 12). The window-state and single-instance checks were last driven by the `window` scenario on
`6e93464b59` (unit 5's regression run) and first proved by unit 1. `launch-login` was driven the same day on
`d554bfb38c` through `capture --path '?login=1'`, on the lane and with `--prod`; the parity sweep drove it on
`1570b59d69`. Windows is unproven on a real machine.

## Sub-features

- `launch-chart` the window loads the chart and candles stream.
- `launch-single` a second launch logs `desktop: second instance, focusing`, exits `0` and leaves one window.
- `launch-window-state` moved, resized and maximized bounds come back on relaunch.
- `launch-login` the sign-in screen renders with Google, X and Turnstile passing.

## How to get to it (user POV)

- Open OpenMarket from the dock or taskbar. The chart appears in its own window.
- Open it again while it runs. The existing window comes forward.
- Move or maximize the window, quit, and open it again.

## Driving it with control-kiyotaka-desktop

Preconditions:

- Baseline from the [index](./README.md): lane up on the recorded port, `doctor` exit `0`.

- **Capture the chart.** Run `control-kiyotaka-desktop capture <dir>/shell-chart.png`. It prints the shell's
  `desktop: window bounds` and `desktop: loaded http://127.0.0.1:<port>/chart/` lines, the `capture:` JSON, then a
  checks line that must read every check `true`, with a title such as `83,214.3 ▲ BTC - USD`. The PNG and
  `<dir>/shell-chart.json` survive.
- **Against the deployed chart.** `control-kiyotaka-desktop doctor --prod`, then
  `control-kiyotaka-desktop capture <dir>/shell-chart-prod.png --prod`. The loaded line names
  `https://openmarket.xyz/chart/`.
- **The sign-in screen.** `control-kiyotaka-desktop capture <dir>/shell-login-prod.png --prod --path '?login=1'`.
  Open the PNG: the dialog shows Use a passkey, Google and X, and Turnstile reading Success! with no banner under it.
  The same verb without `--prod` captures the lane's sign-in screen.
- **Single instance and window state.** `control-kiyotaka-desktop run launch <dir> window`. It passes with 12 checks,
  among them `secondInstanceLine`, `oneWindow`, `relaunchBoundsEqualMoved` and `relaunchMaximized`, and saves
  `unit-01-chart.png` and `unit-01-relaunch.png`.
- **Proof.** The PNG, its JSON report, and the doctor output with its exit code.

## Gotchas

- A fresh guest profile shows the "Draw by holding" tip over the chart. Candles show on both sides of it; the lanes
  leave it, because it is what a new user sees.
- **Only production proves Turnstile.** The dev lane's env carries Cloudflare's test sitekey, so its widget reads
  Success! over a red "For testing only. If seen, report to site owner" strip whatever the host. Prove a Turnstile
  claim with `--prod`.
- No backend means no candles: the env file is missing or the dev backend is down, and the chart reads "Retrying data
  request...". `doctor`'s backend line catches the second; `lane up` refuses the first.
- `capture` settles 60 s after load. A cold lane compiles the module graph on the first page load, so lower
  `CAPTURE_SETTLE_MS` only on a warm lane.
- The `window` scenario's relaunch is a plain launch through `capture.js`. Playwright on a populated profile can stall
  on a paused service worker and time out with an empty URL.
- An unpackaged launch keeps its profile in `OpenMarket Dev`; an installed build uses `OpenMarket`. Every recipe here
  passes `--user-data-dir`, so neither is touched.
