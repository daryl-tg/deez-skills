# Return channel and bridge

The shell owns the `openmarket://` scheme. A browser that navigates to `openmarket://return?id=<id>&payload=<base64url>`
hands the result to the running app: macOS through `open-url`, Windows and a cold start through the launch arguments.
The main process parses the URL once, drops anything else on the scheme as `desktop: dropped openmarket://<host>`,
logs `desktop: return <id>`, and delivers the record to the page through `window.openmarketDesktop.onReturn` only while
the window shows a chart page. The bridge has exactly two members, `version` and `onReturn`. Last driven 2026-10-12 by
the `returns` scenario on `133c5af8ca` (unit 9, 21 checks) against a dev lane, through the chart's own boot
subscription; first proved by unit 3. Windows registration and delivery are unproven on a real machine.

## Sub-features

- `returns-parse` a malformed or other-host URL is dropped by scheme and host only.
- `returns-deliver` a return reaches the page's subscriber; one sent before any subscriber is queued for the first.
- `returns-held` a return that arrives while the window shows an OAuth page is held until the chart is back.
- `returns-argv` a second instance's argv carries a return, the Windows path.
- `returns-cold` a cold start through `open -a` logs the return before the window exists, then the chart takes it.
- `bridge-shape` `window.openmarketDesktop` has `version` and `onReturn` and nothing else.

## How to get to it (user POV)

- Choose Sign in your browser in the app, finish in the browser, and accept the browser's "Open OpenMarket?" prompt.
  The app picks up where it left off.

## Driving it with control-kiyotaka-desktop

Preconditions:

- Baseline from the [index](./README.md): `lane up`, `doctor` exit `0`. The production chart has no handoff bridge
  until this branch deploys, so this recipe needs the dev lane.
- `doctor` lists no OpenMarket bundle outside this checkout's `desktop/dist-app/`. The wrapper refuses otherwise.

- **Run it.** `control-kiyotaka-desktop run launch <dir> returns`. It packs the app with `pnpm package:dev`, launches
  `desktop/dist-app/mac-arm64/OpenMarket.app` on a fresh profile against the lane, and logs
  `desktop: loaded http://127.0.0.1:<port>/chart/`, `desktop: dropped openmarket://elsewhere`, and a
  `desktop: return <id>` line per delivery.
- **Pass.** All 21 checks true, among them `bridgeTwoMembers`, `otherHostDropped`, `unknownIdIgnoredByChart`,
  `pendingRequestResolved`, `sentBeforeSubscribeConsumedByChart`, `offChartHeld`, `heldDeliveredOnChart`,
  `secondInstanceArgvDelivered`, `packagedDevLaneLoadsOverride` and `coldStartConsumedByChart`. The page console logs
  `desktop handoff: ignored return <id>` for a return no request waits on.
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
