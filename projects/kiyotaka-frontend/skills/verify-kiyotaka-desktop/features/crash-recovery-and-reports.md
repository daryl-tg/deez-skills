# Crash recovery and reports

Since 0.1.8, when the page's process ends (a crash, running out of memory, a kill), the shell covers the window with
"This page stopped working" / "Reloading it now…" and reloads the page a second later. The fourth death in ten minutes
is held instead: "This page keeps stopping" / "It stopped 4 times in the last 10 minutes, so OpenMarket stopped
reloading it. Reload to try again." with a Reload button. A load that fails, or a reload that has not committed after
15 s, shows "This page didn't load" / "Check your connection, then reload." with Reload. A committed document lifts the
screen. The title bar's own process always comes back, past the limit every 30 s. Every death of the page, the title
bar or another process (the GPU, the network service), and every failed load becomes a report (`desktop:page-crashed`,
`desktop:process-crashed`, `desktop:page-load-failed`), a page's with its memory over its last minute. From 0.1.9 each
report is kept in `crash-reports.json` in the profile under its own `reportId` and handed to every chart page load that
subscribes through `openmarketDesktop.reports`, until the page acks it once its beacon left; at most 20 are kept, and
one handed to 10 subscribing loads with no ack is dropped. Crashpad uploads a minidump for each crash to Sentry from a
release or internal build. Sources: `desktop/src/main/process-gone.ts`, `crash-reporter.ts`, `index.ts`,
`titlebar.ts`, `desktop/src/preload/index.ts`, and on the page `src/utility/desktop/desktop-analytics.util.ts`; the
contract is `docs/features/desktop/desktop-shell.md#crash-reports`. Last driven 2026-11-12 on product tree `74ccd3cdcc`
(`origin/main`; `desktop/` unchanged since `c2c02b7b42`) by the `crash` scenario, run on its own: 34 of 34 checks in 61 s,
with the console session unlocked and a load average of 12 to 15 on 10 cores; the analytics events read three `app-opened`, ten
`page-crashed`, two `page-load-failed` and one `process-crashed`, and the offline screen read "This page didn't load"
with Reload. Before that, driven 2026-11-10 on product tree
`c2c02b7b42` (`origin/main`, desktop 0.1.10; `desktop/` unchanged since `537639ebca`, whose `desktop/src/` changed since `dced88e06a` only in `ade12fe660`'s view
sizing) by the `crash` scenario: 34 of 34 checks in 44 s, the same as on 2026-11-06 to 2026-11-09, including the
shell's `tsc` build, with the console session locked and a load average of 4 to 5 on 10 cores; `crash-held.png` shows
"This page keeps stopping" with Reload under the bar's Back, Forward and "Stub chart". The lane runs against a stub
chart, not the real one, so the page's own beacon to PostHog and a real Sentry ingest are unproven; so is the page's
keyboard focus after a recovery, and Windows.

## Sub-features

- `crash-reload` a killed page shows the reloading screen, reloads, and the screen goes once the page commits.
- `crash-oom` a dedicated worker and then the page itself run out of memory (V8 capped at 64 MB); the page dies and
  comes back, and on macOS the report reads `crashed`, not `oom`.
- `crash-dump` Crashpad's minidump reaches the minidump endpoint with the release, the environment, the launch id and,
  for the worker, its script in `electron.v8-oom.stack` and `v8-oom-location: Reached heap limit`.
- `crash-hold` the fourth death in ten minutes holds the screen with Reload, does not reload, and the death waits on
  disk.
- `crash-report-handover` the reloaded page gets each report as it loads, by `reportId`, with `handOvers` 1; its ack
  empties the disk; a page that dies before it acks leaves the same `reportId`s to the next page; a page that never
  subscribes costs no hand-over; the held death arrives after a relaunch as its first hand-over.
- `crash-load-failed` a refused load, and a first load while offline, show "This page didn't load"; Reload brings the
  page back.
- `crash-titlebar-gpu` the title bar's and the GPU's process deaths are reported while the page lives, and the bar
  comes back.
- `crash-early` a page killed before its first document commits still comes back.

## How to get to it (user POV)

- Nothing to open: when the chart's tab crashes or runs out of memory, the window shows "This page stopped working"
  and the chart comes back by itself a second later.
- If it keeps crashing, the window stays on "This page keeps stopping" until you click Reload.
- With no connection at launch, the window shows "This page didn't load"; click Reload once you are back online.

## Driving it with control-kiyotaka-desktop

Preconditions:

- A checkout with `desktop/` at 0.1.9 or later and `doctor` reporting the Electron binary. No lane is needed: the
  scenario serves its own stub chart and minidump endpoint on `127.0.0.1` port 0 (an OS-picked port, outside the
  reserved ranges), sets `OPENMARKET_DESKTOP_URL` and `OPENMARKET_DESKTOP_CRASH_URL` itself, and ignores the
  wrapper's lane URL. It does not pack, so the one-packaged-copy rule does not apply.
- Each launch uses a fresh profile under `desktop/.verify-userdata/`. `tools/verify/quiet-mac.cjs` keeps the window
  from activating the app, so the run does not take the keyboard from whoever is at the machine.

- **Run it.** `control-kiyotaka-desktop run launch <dir> crash`. It builds the shell with `tsc`, launches it unpackaged
  under Playwright with `--js-flags=--max-old-space-size=64`, and walks seven stages: kill the page; run a worker and
  then the page out of memory; kill until the hold, then three crash-loop rounds (Reload, kill about 3 s after load),
  one round with acks withheld, a `?nosub` page, quit and relaunch; refuse a load and click Reload, kill the title bar,
  SIGKILL the GPU; launch offline and Reload; kill the page while its first response is held. The shell logs
  `desktop: page process gone, <reason> <code>, reload|hold` for each death.
- **Pass.** The summary's `crash.checks` all true, 34 of them: `chartLoaded`, `reloadingScreenShown`,
  `reloadedAfterKill`, `reportOnReload`, `reportAckedOffDisk`, `firstReported`, `firstCarriesMemory`,
  `screenGoneAfterReload`, `reloadedAfterWorkerOom`, `workerOomReported`, `dumpUploaded`, `dumpNamesTheWorker`,
  `heldScreenShown`, `noReloadWhileHeld`, `reportsKeptOnDisk`, `loopDeathsReportedByReportId`, `unackedSentAgain`,
  `loopEndsWithOneHeld`, `unsubscribedPageCostsNothing`, `heldReportAfterRelaunch`, `allDeathsReported`,
  `diskEmptiedAfterDelivery`, `failedScreenShown`, `reloadButtonReloads`, `loadFailureReported`, `titlebarReported`,
  `titlebarBack`, `gpuReported`, `offlineLaunchScreenShown`, `reloadAfterOfflineLaunch`,
  `screenGoneAfterOfflineReload`, `firstResponseHeld`, `earlyDeathComesBack` and `screenGoneAfterEarlyDeath`, and
  `pass: true`. If `reloadedAfterKill` fails the lane returns after the first stage with only its checks.
- **Read.** `firstReportAfterMs` (1315 ms on 2026-11-06), `dump` (`sentry[release]` `openmarket-desktop@0.1.9`,
  `sentry[environment]` `desktop-dev`, a minidump of about 770 KB), `crashLoop` (one `reportId` per round, each with
  `handOvers` 1), `heldReport` (`action: hold`, `recentCrashes` 7, the memory fields) and `events`.
- **Proof.** The JSON summary and three frames: `crash-reloading.png` ("This page stopped working"), `crash-held.png`
  ("This page keeps stopping" with "It stopped 4 times…" and Reload) and `crash-load-failed.png` ("This page didn't
  load" with Reload). Each frame is a Playwright screenshot of the title bar's view, so it draws on a locked console.
- **Unit level.** `desktop/tests/main/process-gone.test.ts`, `crash-reporter.test.ts` and `report-hand-over.test.ts`
  run in `control-kiyotaka-desktop cli -- pnpm --filter @openmarket/desktop test`. Not a live proof.

## Gotchas

- The frames show the stub chart's title ("Stub chart") or its `127.0.0.1:<port>/chart/` URL, never the real chart.
  A recovery over the real chart has no driver: the lane cannot crash the production page on demand without its stub.
- The scenario asserts the report reached a page and was acked, using the stub's own `fetch` to its server. The real
  page's `startDesktopReports` beacon (`sendOwnBudgetBeacon` to `/i/v0/e/`) and its PostHog fields (`$os`, `docRid`,
  `tabId`) are covered by `tests/utility/desktop/desktop-analytics.reports.spec.ts` only.
- Crashpad's upload to the real Sentry project is rate-limited to one an hour and only from a release or internal
  build; the lane's dump goes to its own stub endpoint.
- `reloadingScreenShown` polls a short window and `reportOnReload` must arrive within 6 s; under heavy machine load
  read a red on those two against the load figures before calling it a regression.
- The returns lane's `bridgeTwoMembers` and the notify lane's `bridgeUnchanged` still expect a two-member bridge; the
  `reports` member is one more reason they read red (see [returns](./return-channel-and-bridge.md)).
