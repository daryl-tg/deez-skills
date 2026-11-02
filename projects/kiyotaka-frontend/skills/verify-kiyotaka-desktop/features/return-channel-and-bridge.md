# Return channel and bridge

The shell owns the `openmarket://` scheme. A browser that navigates to `openmarket://return?id=<id>&payload=<base64url>`
hands the result to the running app: macOS through `open-url`, Windows and a cold start through the launch arguments.
The main process tries three parsers in order, sign-in (`openmarket://oauth/callback`), checkout
(`openmarket://checkout`) and return; anything none of them takes is dropped as `desktop: dropped openmarket://<host>`.
A return logs `desktop: return <id>` and reaches the page through `window.openmarketDesktop.onReturn` only while the
window shows a chart page. The bridge's members are `version`, `onReturn`, `updates` and `analytics`, plus
`browserSignIn: true` on a build that signs in through the browser (`desktop/contract.json`). Last driven 2026-11-03
by the `returns` scenario on tree `1af9ebbe07` (`origin/main`, the shell's `desktop/src/` unchanged since `30481b57f8`)
against the dev lane: 20 of 21 checks in 67 s including the `pnpm package:dev` pack, the same split as on every run
from 2026-10-27 to 2026-11-02. The first run that day, straight after `lane up`, threw in `waitForCandles`
(`launch.mjs:94`, no BTC title in 60 s) before any check: the cold vite's first chart load failed its dynamic imports
and the router never started (see the [index](./README.md)). The re-run on the warmed lane is the result above. The shell logged `desktop: dropped openmarket://elsewhere`, a `desktop: return <id>` line for `abc`,
`second`, the handoff's uuid, `before-subscribe`, `held` and `cold`, and `desktop: external .../desktop/sign?r=...` (a
`solana-connect` request) for the handoff step. The red one, `bridgeTwoMembers`, still expects `onReturn, version` and
read `analytics, browserSignIn, onReturn, updates, version` (`version` 0.1.7); that is a stale lane assertion, not a
regression. `unit-03-return.png` showed the `onReturn {"id":"abc",...}` banner over a chart with no history (two bars at
`76,683.3`, "Reconnecting...", the "Draw by holding" tip), because the dev lane's streaming host did not resolve that day;
on 2026-11-02 it showed the 1h candles under the banner. On 2026-11-01 the same frame had no candles ("Reconnecting...", the "Draw
by holding" tip) because the dev lane had no live data that day; the scenario's checks need a canvas, not a price, so
a green `returns` says nothing about candles, and only the frame does. Windows registration
and delivery are unproven on a real machine. The sign-in and checkout links are covered in
[browser sign-in and checkout](./browser-signin-and-checkout.md).

## Sub-features

- `returns-parse` a malformed or other-host URL is dropped by scheme and host only.
- `returns-deliver` a return reaches the page's subscriber; one sent before any subscriber is queued for the first.
- `returns-held` a return that arrives while the window shows an OAuth page is held until the chart is back.
- `returns-argv` a second instance's argv carries a return, the Windows path.
- `returns-cold` a cold start through `open -a` logs the return before the window exists, then the chart takes it.
- `bridge-shape` `window.openmarketDesktop` has `analytics` (`onEvent`), `onReturn`, `updates` (`onState`, `check`,
  `restart`) and `version`, and `browserSignIn` on a packaged build (or with `OPENMARKET_DESKTOP_BROWSER_SIGNIN=1`).
  The preload (`desktop/src/preload/index.ts`) carries them over the IPC channels `desktop:return`,
  `desktop:analytics`, `desktop:update-state`, `desktop:check-for-updates` and `desktop:restart-to-update`; the lanes
  read the members, never the channels (source, 2026-11-02).

## How to get to it (user POV)

- Choose Sign in your browser in a wallet or sign-in flow, finish in the browser, and accept the browser's "Open
  OpenMarket?" prompt. The app picks up where it left off.

## Driving it with control-kiyotaka-desktop

Preconditions:

- Baseline from the [index](./README.md): `lane up`, `doctor` exit `0`.
- `doctor` lists no OpenMarket bundle outside this checkout's `desktop/dist-app/`. The wrapper refuses otherwise.

- **Run it.** `control-kiyotaka-desktop run launch <dir> returns`. It packs the app with `pnpm package:dev`, launches
  `desktop/dist-app/mac-arm64/OpenMarket.app` on a fresh profile against the lane, and logs
  `desktop: loaded http://127.0.0.1:<port>/chart/`, `desktop: dropped openmarket://elsewhere`, and a
  `desktop: return <id>` line per delivery.
- **Pass.** Every check true except `bridgeTwoMembers` until the lane learns the new bridge: `packagedProfileOpenMarket`,
  `packaged`, `packagedDevLaneLoadsOverride`, `bridgeVersion`, `otherHostDropped`, `returnLine`,
  `callbackGotSentRecord`, `unsubscribedGotNothing`, `unknownIdIgnoredByChart`, `oneWindow`, `canvas`,
  `secondInstanceArgvDelivered`, `handoffOpenedSignPage`, `pendingRequestResolved`,
  `sentBeforeSubscribeConsumedByChart`, `offChartHeld`, `heldDeliveredOnChart`, `coldStartReturnBeforeWindow`,
  `coldStartLoaded` and `coldStartConsumedByChart`. Read the summary's `bridge.keys` to judge `bridge-shape` yourself.
  The page console logs `desktop handoff: ignored return <id>` for a return no request waits on.
- **Proof.** The lane's JSON summary, `unit-03-return.png` (the chart after the first delivery), and
  `unit-03-cold-start.log` with `unit-03-cold-start-renderer.log`.

## Gotchas

- **One packaged copy.** With two `xyz.openmarket.desktop` bundles on disk, `open openmarket://...` went to the other
  copy, which launched with no `--user-data-dir`; with the copy moved aside, `open` failed `kLSApplicationNotFoundErr`.
  Playwright launches the executable directly, so a bundle in a new place is not registered until `open` or `lsregister`
  sees it.
- Only a packaged build registers the scheme. A dev launch (`pnpm start`) registers nothing, so an unpackaged shell
  never receives `open openmarket://...`.
- A packaged app ignores `-r` preloads, so no listener can be injected before load; the lane reads the chart's own
  subscription and the page's console instead.
- The bridge follows the window. While an OAuth page is in the window the preload still runs there, which is why the
  main process holds returns until a chart page is back.
- The `returns` scenario has no sign-in or checkout step; those links have no shell driver.
