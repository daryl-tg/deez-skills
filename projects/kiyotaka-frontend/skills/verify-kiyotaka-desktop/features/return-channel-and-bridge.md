# Return channel and bridge

The shell owns the `openmarket://` scheme. A browser that navigates to `openmarket://return?id=<id>&payload=<base64url>`
hands the result to the running app: macOS through `open-url`, Windows and a cold start through the launch arguments.
The main process tries three parsers in order, sign-in (`openmarket://oauth/callback`), checkout
(`openmarket://checkout`) and return; anything none of them takes is dropped as `desktop: dropped openmarket://<host>`.
A return logs `desktop: return <id>` and reaches the page through `window.openmarketDesktop.onReturn` only while the
window shows a chart page. The bridge's members are `version`, `onReturn`, `updates`, `analytics` and, from 0.1.9,
`reports`, plus `browserSignIn: true` on a build that signs in through the browser (`desktop/contract.json`). Last
driven 2026-11-07 by the `returns` scenario on tree `dced88e06a` (`origin/main`, desktop 0.1.9; `desktop/src/` last
changed in `236b4c3eca`, the crash reports) against the dev lane, warmed in Chromium first (a priced BTC title, but 1 bar
in the engine: the streaming host did not resolve): 20 of 21 checks in 69 s including the `pnpm package:dev` pack, the
same split as on every run from 2026-10-27 (72 s on `8bcd72f8f5` on 2026-11-06). On 2026-11-03 the first
run straight after `lane up` threw in `waitForCandles` (then `launch.mjs:94`, now `:97`; no BTC title in 60 s) before
any check, because the cold vite's first chart load failed its dynamic imports and the router never started (see the [index](./README.md)).
The shell logged `desktop: dropped openmarket://elsewhere`, a `desktop: return <id>` line for `abc`, `second`, the
handoff's uuid, `before-subscribe`, `held` and `cold`, and `desktop: external .../desktop/sign?r=...` (a
`solana-connect` request) for the handoff step. The red one, `bridgeTwoMembers`, still expects `onReturn, version`
while the bridge holds `analytics, browserSignIn, onReturn, reports, updates, version` (`launch.mjs:435`; `bridgeVersion`
on the next line read 0.1.9 on 2026-11-07 and passes); that is a stale lane assertion, not a regression. On 2026-11-04
`unit-03-return.png` showed the `onReturn {"id":"abc",...}` banner over the 1h candles, with the guest signup prompt
("See what moves price.") over the chart. On 2026-11-01, 2026-11-03 and from 2026-11-05 to 2026-11-07 the same frame had no history (two
bars under "Reconnecting..." or, from 2026-11-05, "Your network is slow" and an empty plot under the "Draw by holding"
tip) because the dev lane's
streaming host was unreachable; the scenario's checks need a canvas, not a price, so a green `returns` says nothing about candles, and only
the frame does. Windows registration
and delivery are unproven on a real machine. The sign-in and checkout links are covered in
[browser sign-in and checkout](./browser-signin-and-checkout.md).

## Sub-features

- `returns-parse` a malformed or other-host URL is dropped by scheme and host only.
- `returns-deliver` a return reaches the page's subscriber; one sent before any subscriber is queued for the first.
- `returns-held` a return that arrives while the window shows an OAuth page is held until the chart is back.
- `returns-argv` a second instance's argv carries a return, the Windows path.
- `returns-cold` a cold start through `open -a` logs the return before the window exists, then the chart takes it.
- `bridge-shape` `window.openmarketDesktop` has `analytics` (`onEvent`), `onReturn`, `reports` (`onReport`, `ack`;
  from 0.1.9), `updates` (`onState`, `check`, `restart`) and `version`, and `browserSignIn` on a packaged build (or
  with `OPENMARKET_DESKTOP_BROWSER_SIGNIN=1`). The preload (`desktop/src/preload/index.ts`) carries them over the IPC
  channels `desktop:return`, `desktop:analytics`, `desktop:report`, `desktop:report-ready`, `desktop:report-ack`,
  `desktop:update-state`, `desktop:check-for-updates` and `desktop:restart-to-update`; the lanes read the members,
  never the channels. The `returns` summary's `bridge.keys` read all six on 2026-11-06; what `reports` carries is
  proved by the [crash lane](./crash-recovery-and-reports.md).

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
