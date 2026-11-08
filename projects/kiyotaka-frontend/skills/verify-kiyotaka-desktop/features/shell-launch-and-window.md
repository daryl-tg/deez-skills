# Shell launch and window

The shell opens one window on the production chart (`https://openmarket.xyz/chart/`, the only channel since 0.1.0-beta.6;
a dev lane overrides it with `OPENMARKET_DESKTOP_URL`), takes a single-instance lock so a second launch focuses the
first window, and remembers the window's position, size and maximized state across launches. The window has no system
title bar: a 36 px bar view above the page carries Back, Forward, the page title and an update button, and draws its
own tooltips; on Windows and Linux the menu bar stays hidden until Alt. A packaged release build shows a one-time
"You're on the OpenMarket desktop beta 🎉" notice on first launch. When the page's process dies, the bar's view covers the window with a recovery screen and the
page reloads; see [crash recovery and reports](./crash-recovery-and-reports.md). Since 0.1.10 (`ade12fe660`) the two
views fill what the screen shows of the window, never the raw content size: in full screen they fit the display,
maximized its work area, and they lay out again on a resize, on entering or leaving full screen, on maximize and
unmaximize, and on every display change (`desktop/src/main/view-area.ts`); some Linux desktops (Mint Cinnamon) report a
content size past the screen, which cut the page's right edge and footer in full screen through 0.1.9. Last driven
2026-11-09 on product tree `27fb2d4621` (`origin/main`, desktop 0.1.10 from `920afc7199`) with the console session
locked and the machine at a load average of 5 to 19 on 10 cores. The `window` scenario on production passed 9 of 12 in
107 s, the same split as every run since 2026-10-29: the first launch logged `desktop: loaded
https://openmarket.xyz/chart/` with the title `75,782.7 ▼ BTC - USD` and a candle frame (`unit-01-chart.png` shows
the 1h BTC-USD candles with VWAP, not the splash), the second instance focused it (`desktop: second instance,
focusing`, exit 0, one window), and the saved bounds (moved to 120,110 at 1280 by 800, maximized) matched on relaunch.
The three relaunch checks (`relaunchBtcTitle`, `relaunchCanvas`, `relaunchMaximized`) went red because the relaunch is
a `capture.js` launch, which a locked screen leaves with no frame (`relaunchCapture: {}`). No `capture` was attempted
from 2026-10-31 to 2026-11-09 for that reason; on 2026-10-29 and 2026-10-30 every `capture` got no frame. The last
captures were on 2026-10-28 on `5365748ef3`: the dev-lane frame showed the boot splash, and the production frames
showed candles and the sign-in screen. The `window` scenario was last 12 of 12 that day. No lane drives the title bar's buttons or the view sizing, but on 2026-11-09 a scratch Playwright drive of the unpackaged shell on the dev lane proved
them (see `launch-titlebar` and `launch-view-area`). The Alt menu bar and the beta notice have no live driver (unit tests in `desktop/tests/main/` only; the beta notice never shows on a dev
lane or an unpackaged launch). Windows and Linux are unproven on a real machine.

## Sub-features

- `launch-chart` the window loads the chart and candles stream.
- `launch-single` a second launch logs `desktop: second instance, focusing`, exits `0` and leaves one window.
- `launch-window-state` moved, resized and maximized bounds come back on relaunch.
- `launch-login` the sign-in screen renders in the shell with email code, password, Google and X, and no passkey pill.
  Since `4b8f78a775` (2026-11-03, after `1af9ebbe07`) the dialog is one card: Email me a code, Sign in with a password
  instead, "Or continue with" and a row of outlined pills (Passkey, Google, X in a browser; Google and X in the shell,
  where `PasskeyService.isSupported()` is false under the bridge). Since `37afa417b0` (2026-11-04, after `8436920004`)
  the Turnstile widget (`login-signup-turnstile`) sits between the address and "Email me a code", and an unticked
  Cloudflare checkbox keeps the button off with "Complete the security check above to continue." under the fields.
  The shell frame of the new card is not yet captured.
- `launch-view-area` the bar and page views fill the visible window: the display in full screen, its work area when
  maximized, re-laid on full screen, maximize and display changes. Windowed, resized and maximized live on macOS
  2026-11-09 (`27fb2d4621`, scratch drive, no lane reads the bounds): the bar view was `{0,0,W,36}` and the page view
  `{0,36,W,H-36}` at 1400 by 900, at 1280 by 800, and maximized on the 1920 by 1080 display (work area 1920 by 1050,
  page 1920 by 1014), and again after unmaximize. Full screen is still pending: `setFullScreen(true)` left
  `isFullScreen()` false for 12 s on the locked console. The Linux cut shows only on some Linux desktops;
  `desktop/tests/main/view-area.test.ts` covers it.
- `launch-titlebar` the bar's Back, Forward, title and update button, disabled while a block or sign-in screen covers
  the window. Live 2026-11-09 (`27fb2d4621`, scratch drive, no lane): Back and Forward start disabled, Back turns on after a page navigation; clicking Back returned to
  `/chart/` and turned Forward on, clicking Forward returned to the page; hovering a button draws the bar's own `#tip` (Back, Forward, "Check for updates") and it
  hides when the pointer leaves; `#title` carried the page's title (`75,768.3 ▼ BTC - USD`); clicking `#update` in an unpackaged launch logs `desktop: update check skipped,
  unpackaged` and leaves the label unchanged. The disabled state under a block or sign-in screen is still undriven. `capture` grabs the page view only, so the bar is never in a frame. The crash
  lane's frames are screenshots of the bar's own view, which grows to cover the window for a recovery screen: on
  2026-11-06 they showed Back, Forward, the page title ("Stub chart", or the URL while the load failed) and a round
  arrow at the right above the screen. That proves the bar draws; its buttons and tooltips are still undriven.
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
  Open the PNG: "Sign in or create an account", Email me a code, Sign in with a password instead, "Or continue with",
  then Google and X pills. There is no Passkey pill in the shell; the same dialog in Chromium shows one
  (`login-signup-passkey-btn`, "Passkey", read on `/chart/auth` on 2026-11-04), which is the proof of
  `src/services/passkey.service.ts` refusing passkeys under the bridge. No Turnstile widget shows for clean traffic;
  when Cloudflare asks for its checkbox, it shows between the address and "Email me a code", and the button stays off
  until it is ticked (see [sign-in](./browser-signin-and-checkout.md)).
- **Single instance and window state.** `control-kiyotaka-desktop run launch <dir> window`. It passes with 12 checks,
  `loadedLine`, `btcTitle`, `canvas`, `secondInstanceLine`, `secondInstanceExited`, `oneWindow`,
  `maximizedBeforeQuit`, `relaunchLoadedLine`, `relaunchBtcTitle`, `relaunchCanvas`, `relaunchBoundsEqualMoved` and
  `relaunchMaximized`, and saves `unit-01-chart.png` and `unit-01-relaunch.png`.
- **Title bar and view bounds (no lane; a scratch script).** Launch through Playwright exactly as `launch.mjs` does:
  `_electron.launch({ args: ['.', '--user-data-dir=<fresh dir under desktop/.verify-userdata/>'], cwd: 'desktop', env: { ...process.env, OPENMARKET_DESKTOP_URL: '<lane>' } })`,
  on a built `desktop/dist` and a fresh profile only. The bar is the window whose URL starts `data:text/html`: read and click `#back`, `#forward`, `#update`, `#title`, hover then read
  `#tip`. Bounds come from the main process: `app.evaluate(() => { const win = globalThis.openmarketShell.window(); return win.contentView.children.map((v) => v.getBounds()); })`,
  beside `win.getContentSize()`, `win.isFullScreen()`, `win.isMaximized()` and `screen.getDisplayMatching(win.getBounds())`. The bar is the child 36 px tall; compare the page with `viewArea` in
  `desktop/src/main/view-area.ts`. Stop on any Turnstile screen.
- **Unit level for the bar and the notice.** `control-kiyotaka-desktop cli -- pnpm --filter @openmarket/desktop test`
  (39 files, 469 tests on 2026-11-08) covers `titlebar`, `view-area`, `beta-notice`, `navigation` and `user-agent`. That is not a
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
  test sitekey, which reads Success! over a red "For testing only" strip. On 2026-11-05 that sitekey put
  `XXXX.DUMMY.TOKEN.XXXX` in the widget's hidden `cf-turnstile-response` with no box drawn, so the dev lane never shows
  the disabled "Email me a code" and its "Complete the security check above to continue." line; that state is
  source-read only (`AuthFormView.vue` `humanCheckPending`).
- A fresh guest chart shows the guest signup prompt ("See what moves price.", Join for free,
  `guest-signup-modal-close-btn`, `GuestSignupPromptDialog.vue`) some seconds after it loads, in Chromium and in the
  shell (the `returns` frame on 2026-11-04). It is not the first-run onboarding, which never starts for a guest. The
  shell frames on 2026-10-27 caught the chart before it appeared.
- No backend means no candles: the env file is missing or the dev backend is down, and the chart reads "Retrying data
  request...". `doctor`'s backend line catches the second; `lane up` refuses the first.
- `capture` settles 60 s after load. A cold lane compiles the module graph on the first page load, so lower
  `CAPTURE_SETTLE_MS` only on a warm lane.
- The `window` scenario's relaunch is a plain launch through `capture.js`. Playwright on a populated profile can stall
  on a paused service worker and time out with an empty URL.
- An unpackaged launch keeps its profile in `OpenMarket Dev`; an installed build uses `OpenMarket`. Every recipe here
  passes `--user-data-dir`, so neither is touched.
