# Shell launch and window

The shell opens one window on the production chart (`https://openmarket.xyz/chart/`, the only channel since 0.1.0-beta.6;
a dev lane overrides it with `OPENMARKET_DESKTOP_URL`), takes a single-instance lock so a second launch focuses the
first window, and remembers the window's position, size and maximized state across launches. The window has no system
title bar: a 36 px bar view above the page carries Back, Forward, the page title and an update button, and draws its
own tooltips; on Windows and Linux the menu bar stays hidden until Alt. A packaged release build shows a one-time
"You're on the OpenMarket desktop beta 🎉" notice on first launch. Last driven 2026-10-31 on product tree `5475ab32d5`
(`origin/main`, desktop 0.1.7) with the console session locked and the machine at a load average of 3 to 6 on 10 cores.
The `window` scenario on production passed 9 of 12 in 104 s, the same split as 2026-10-29 on `30481b57f8`: the first
launch logged `desktop: loaded https://openmarket.xyz/chart/` with the title `76,700.3 ▲ BTC - USD` and a candle frame
(`unit-01-chart.png` shows the 1h BTC-USD candles, not the splash), the second instance focused it, and the saved bounds
matched on relaunch. The three relaunch checks went red because the relaunch is a `capture.js` launch, which a locked
screen leaves with no frame (`relaunchCapture: {}`). No `capture` was attempted on 2026-10-31 for that reason; on
2026-10-29 and 2026-10-30 every `capture` got no frame. The last captures were on 2026-10-28 on `5365748ef3`: the dev-lane
frame showed the boot splash, and the production frames showed candles and the sign-in screen. The `window` scenario was
last 12 of 12 that day. The title bar, the Alt menu bar and the beta notice have no live driver (unit tests in
`desktop/tests/main/` only; the beta notice never shows on a dev lane or an unpackaged launch). Windows and Linux are
unproven on a real machine.

## Sub-features

- `launch-chart` the window loads the chart and candles stream.
- `launch-single` a second launch logs `desktop: second instance, focusing`, exits `0` and leaves one window.
- `launch-window-state` moved, resized and maximized bounds come back on relaunch.
- `launch-login` the sign-in screen renders in the shell with email code, password, Google and X, and no passkey row.
- `launch-titlebar` the bar's Back, Forward, title and update button, disabled while a block or sign-in screen covers
  the window. Live verification pending: `capture` grabs the page view only, so the bar is never in a frame.
- `launch-beta-notice` the one-time beta notice on a packaged release build. Live verification pending: no lane packs
  a non-dev-lane build.

## How to get to it (user POV)

- Open OpenMarket from the dock or taskbar. The chart appears in its own window under the app's own title bar.
- Open it again while it runs. The existing window comes forward.
- Move or maximize the window, quit, and open it again.
- Choose Guest Mode, or open `?login=1`, to see the sign-in screen.

## Driving it with control-kiyotaka-desktop

Preconditions:

- Baseline from the [index](./README.md): lane up on the recorded port, `doctor` exit `0`.

- **Capture the chart.** Run `control-kiyotaka-desktop capture <dir>/shell-chart.png`. It prints the shell's
  `desktop: window bounds` and `desktop: loaded http://127.0.0.1:<port>/chart/` lines, the `capture:` JSON, then a
  checks line that must read every check `true`, with a title such as `79,786.9 ▼ BTC - USD`. Open the PNG: it must
  show candles, not the boot splash (see Gotchas). The PNG and `<dir>/shell-chart.json` survive.
- **Against the deployed chart.** `control-kiyotaka-desktop doctor --prod`, then
  `control-kiyotaka-desktop capture <dir>/shell-chart-prod.png --prod`. The loaded line names
  `https://openmarket.xyz/chart/`.
- **The sign-in screen.** `control-kiyotaka-desktop capture <dir>/shell-login-prod.png --prod --path '?login=1'`.
  Open the PNG: "Sign in or create an account", Email me a code, Sign in with a password instead, then Google and X.
  There is no Use a passkey row in the shell; the same dialog in Chromium shows one, which is the proof of
  `src/services/passkey.service.ts` refusing passkeys under the bridge. No Turnstile widget shows for clean traffic.
- **Single instance and window state.** `control-kiyotaka-desktop run launch <dir> window`. It passes with 12 checks,
  `loadedLine`, `btcTitle`, `canvas`, `secondInstanceLine`, `secondInstanceExited`, `oneWindow`,
  `maximizedBeforeQuit`, `relaunchLoadedLine`, `relaunchBtcTitle`, `relaunchCanvas`, `relaunchBoundsEqualMoved` and
  `relaunchMaximized`, and saves `unit-01-chart.png` and `unit-01-relaunch.png`.
- **Unit level for the bar and the notice.** `control-kiyotaka-desktop cli -- pnpm --filter @openmarket/desktop test`
  (35 files, 422 tests on 2026-10-27) covers `titlebar`, `beta-notice`, `navigation` and `user-agent`. That is not a
  live proof.
- **Proof.** The PNG, its JSON report, and the doctor output with its exit code.

## Gotchas

- **A priced title does not prove the frame.** The route drops the boot splash after a double
  `requestAnimationFrame` (`src/main.ts`), and rAF stops while the window is hidden. On the unattended mini the shell
  window goes `document.visibilityState === 'hidden'` 30 to 40 s after launch. A production boot finishes before that;
  a dev-lane boot often does not, so on 2026-10-27 both dev-lane captures passed every check, with a priced title and
  15 canvases, while their PNGs showed the splash at 54 and 82 percent. Open the PNG. For a dev-lane frame, run with
  the console session awake and the window unobscured, or take the frame from `--prod`.
- **A locked screen gives no frame at all.** With the console session locked (`ioreg -n Root -d1 -a | grep -A1
  CGSSessionScreenIsLocked` reads `<true/>`), `capturePage()` rejects with "Current display surface not available for
  capture". `capture.js` has no catch, so the shell logs `desktop: loaded` and then never quits, and `capture` hangs.
  On 2026-10-29 this happened to every capture and to the `window` scenario's relaunch, and on 2026-10-31 to the
  relaunch again: `relaunchCapture` was `{}`, so `relaunchBtcTitle`, `relaunchCanvas` and `relaunchMaximized` went
  red. Read the lock state before a run and skip `capture` when it is locked; the hang is certain. Stop only your own
  shell, with `pkill -TERM -f 'user-data-dir=<checkout>/desktop/.verify-userdata/control/capture-profile'`. Report the
  frame as blocked on the lock. It is not a product regression. Unlocking the screen is the operator's job.
- **Turnstile is a soft gate now.** auth-service hides the widget for clean traffic, so the sign-in capture usually
  shows no widget at all. When a widget does show, only `--prod` proves it: the dev lane's env carries Cloudflare's
  test sitekey, which reads Success! over a red "For testing only" strip.
- Plain Chromium on the dev lane shows a first-run "See what moves price." onboarding dialog over a fresh guest chart.
  The shell frames on 2026-10-27 caught the chart before it appeared.
- No backend means no candles: the env file is missing or the dev backend is down, and the chart reads "Retrying data
  request...". `doctor`'s backend line catches the second; `lane up` refuses the first.
- `capture` settles 60 s after load. A cold lane compiles the module graph on the first page load, so lower
  `CAPTURE_SETTLE_MS` only on a warm lane.
- The `window` scenario's relaunch is a plain launch through `capture.js`. Playwright on a populated profile can stall
  on a paused service worker and time out with an empty URL.
- An unpackaged launch keeps its profile in `OpenMarket Dev`; an installed build uses `OpenMarket`. Every recipe here
  passes `--user-data-dir`, so neither is touched.
