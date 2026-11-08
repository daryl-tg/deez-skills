# OpenMarket desktop shell verification map

The maintained source for proving the desktop shell's user-facing behavior. Read this index before driving, then use
the matching feature file as the recipe. The contract the recipes prove is the web repo's
`docs/features/desktop/desktop-shell.md`; the lanes they run live in `desktop/tools/verify/` and `qa/`.

## Baseline preconditions

- A kiyotaka-frontend checkout that carries `desktop/`, with `pnpm install` done at its root.
- `KIYO_DESKTOP_LANE_PORT` set to a free port from `18097`-`18197`, preflighted with `lsof`, recorded for the run.
  The default is `18144`. Bind `127.0.0.1`; never pick a port by scanning for a free one.
- `control-kiyotaka-desktop lane up` (or `lane up --testnet` for wallet recipes), then `control-kiyotaka-desktop doctor`
  exits `0`. Recipes against the deployed chart use `doctor --prod` instead.
- Never drive a lane, a shell or a profile this run did not start.

## Driving conventions

- **Turnstile screens are captured, never automated.** Cloudflare Turnstile fails with Playwright attached and passes
  in a plain launch. The sign-in screen and anything behind it go through `control-kiyotaka-desktop capture`, which is
  `desktop/tools/verify/capture.js` in a plain launch. No recipe attaches Playwright, CDP or agent-browser to a shell
  window that shows Turnstile.
- **One packaged copy on disk for a scheme-return lane.** Before `returns` or `notify`, the only
  `xyz.openmarket.desktop` bundle on disk is this checkout's `desktop/dist-app/`. `doctor` lists every copy, and the
  wrapper refuses those scenarios while another exists.
- **A relaunch on a populated profile is a plain launch.** Once the chart's service worker registers, Playwright's
  Electron launcher can leave a worker paused and `firstWindow()` times out with an empty URL. The lanes attach
  Playwright only to a first launch on a fresh profile.
- **A dev lane is a launch that honours `OPENMARKET_DESKTOP_URL`**: an unpackaged launch, or a packaged build that
  `pnpm package:dev` marked with `devLane: true`. Release packaging never sets the marker.
- Each lane runs on its own fresh profile under `desktop/.verify-userdata/`. No recipe touches the installed
  profiles `~/Library/Application Support/OpenMarket` or `OpenMarket Dev`.
- **Open every frame.** A shell window that goes hidden (the unattended mini hides it 30 to 40 s after launch) stops
  `requestAnimationFrame`, so the boot splash never drops; `capture` still passes on a priced title. A splash frame
  proves nothing about the chart. See [launch](./shell-launch-and-window.md).
- **A locked console gives `capture` no frame.** With `CGSSessionScreenIsLocked` true (`ioreg -n Root -d1 -a | grep -A1
  CGSSessionScreenIsLocked`), `capturePage()` rejects and `capture.js` never quits. That breaks every `capture`, the
  `window` relaunch, parity's `login-wall` shell half, `notify`'s `screenUnlocked` and the gaps lane's key rows.
  Playwright-attached frames still draw. Report those boxes as blocked on the lock, and stop only the shell holding your
  own `capture-profile`.
- **A machine far over its cores fails the shell lanes before their checks.** Read `uptime` and `sysctl -n hw.ncpu`
  first. On 2026-10-30 the mini ran at a load average of 55 to 185 on 10 cores, from other agents' sessions. Under that
  load, `window`, `links` and `returns` each died on a Playwright launch or `firstWindow()` 30 s timeout with no
  summary. One `pnpm package:dev` took about 45 minutes, most of it ad-hoc codesigning. A cold vite took 166 s once
  and longer than 180 s the next time, so `lane up` gave up at its wait and doctor then read `/chart/` as `000`. The
  desktop unit suite's subprocess tests timed out even when run alone. In Chromium, the chart route reached the guest
  button only after several minutes, then showed "Taking a bit longer than usual..." with no candles. Report those
  boxes as blocked on load with the load figures. Never stop another run's processes to make room; stop only your own
  sequence and its builder. For contrast, on 2026-10-31 at a load average of 3 to 6 on the same machine, `lane up`
  answered in seconds, `window` took 104 s, `returns` 71 s with its pack, `notify` 47 s, `update` 99 s with both packs,
  and the Chromium chart route settled in about five seconds.
- **A green `doctor` is not candles.** `doctor` reads the lane's REST health (`/api/v1/health/services`); the chart's
  candles come over the v2 streaming socket (`VITE_V2_WEB_SOCKET_DOMAIN`, an internal `tsdb-gateway` host reached over
  the Tailscale route from the mini). On 2026-11-01 health read `ok` while that host answered nothing, so every host on
  the dev lane read "Can't reach live data. Retrying..." with no candles, the lane log repeated `v2 Streaming socket
  error`, and both the parity sweep and the gaps lane threw in `waitForCandles` before any step. The production shell
  had candles. The pages, the sign page, the returns, notify and update scenarios need no candles and ran. On
  2026-11-02 `nc -z tsdb-gateway.int.ore.kiyotaka.ai 443` succeeded before the first drive, Chromium on the lane read a
  priced title, and the sweep, the gaps lane and the `hl` scenario ran their steps. **A priced title is not candles
  either.** On 2026-11-03 the host did not resolve at all (`nc: getaddrinfo: nodename nor servname provided`), the lane
  log held 117 `v2 Streaming socket error` lines, and Chromium on the lane still read a ticking priced title
  (`76,718.5 ▲ BTC - USD`) over two giant bars and a "Reconnecting..." pill: the engine held 2 bars. The sweep and
  the gaps lane wait for the engine's own predicate, more than 50 bars (`window.tc[0].metadata[0].rawData.length`,
  `parity.mjs` and `gaps.mjs` `waitForCandles`), and both threw at 180 s before any step. Before a sweep or the gaps
  lane, run `nc -z tsdb-gateway.int.ore.kiyotaka.ai 443` and read that bar count in a browser on the lane; under 50,
  report those two as blocked on the environment, name the host, and never read it as a shell regression. On 2026-11-04 the
  host answered again: `nc -z` succeeded, the engine held 250 bars, and the sweep and the gaps lane ran their steps. On
  2026-11-05 it did not resolve again, the engine held 0 bars under a `BTC - USD` title, and the two lane logs held 358
  `v2 Streaming socket error` lines; the sweep and the gaps lane were not run. On 2026-11-06 and 2026-11-07 it did not
  resolve either (`nc -z` before the first drive and again after the last), and the engine held 1 bar under a ticking
  title (`75,760.2 ▼ BTC - USD` on 2026-11-07, under "Your network is slow" and "Loading chart..."); the sweep and the
  gaps lane were not run. On 2026-11-08 `nc -z` succeeded before the first drive and after the last, the engine held
  250 bars, and both ran their steps. On 2026-11-09 `nc -z` succeeded before the first drive and after the last, and
  the engine held 250 bars.
- **Warm a freshly started lane before the first shell drive.** A `lane up` starts a cold vite. The first chart load
  after it can fail with `Failed to fetch dynamically imported module` lines and `[VUE_ROUTER_R0011] Unexpected error
  when starting the router` in the lane log, and the page never gets a BTC title. On 2026-11-03 that stopped `returns`
  at `waitForCandles` (`launch.mjs:94`, now `:97`, a 60 s wait for `/BTC/` in the title) after `lane up`, and the `hl` scenario at
  `waitForChart` (`handoff.mjs:230`) after `lane up --testnet`, both before any check. Three Chromium tabs opened at once
  on the cold lane got "Startup is taking longer than expected ... [failed to load external] main.ts" on two pages. On
  the warmed lane the same `returns` and `hl` runs reached their known results. After every `lane up`, load `/chart/` once
  in one browser until the title names BTC, then drive. Open pages one at a time on a cold lane.
- **A pack reloads every page on the lane.** The lane's vite watches the whole checkout, so `pnpm package:dev` writing
  `desktop/dist-app/**/LICENSES.chromium.html` logs `[vite] (client) page reload desktop/dist-app/...` and reloads
  every page open on the lane at that moment, such as the Chromium session you warmed with. `returns`, `notify`,
  `update`, `handoff` and the sweep each pack first. On 2026-11-05 the first `hl` run's sign page never booted, with
  `Failed to fetch dynamically imported module` and `VUE_ROUTER_R0011` in the lane log a minute after that reload (stop
  at `handoff.mjs:307`); the cause is not isolated. Close your browser session before a lane that packs, warm a fresh
  one afterwards, and read a stop right after a pack as a page that never booted.
- **Headless Chromium runs Lite charts; the shell here does not.** Since `b62ef4c998` a software GPU turns Lite charts on with a staying toast ("Lite charts is on.", Keep,
  Turn off) and a bolt in the legend (`src/utility/chart/lite/lite-hint.ts`). Playwright's headless Chromium took that path on 2026-11-09 (toast and bolt in its frames; the class was not read), and a sweep pair differed by about 2.5 percent, the toast's size. Read a pixel diff against a Chromium host with that first.
- **A search field takes the first Escape.** Since `ee1fae1b4d` an Escape in a `SearchField` that holds words clears them and stops there; only the next one closes the dialog (live in the shell on the Indicators dialog 2026-11-09). A recipe that types then presses one Escape leaves the dialog up.
- **Name the parity steps.** `run parity <dir>` with no steps runs the signed-in phase too, which signs in as the
  operator's real account and writes layouts. An unattended run names the guest steps; see [parity](./parity-sweep.md).
- **A lane red in both hosts, or against a moved contract, is a lane gap.** Several checks in `desktop/tools/verify/`
  and `qa/tests/e2e/desktop-sign.mjs` trail the product (the two-member bridge, the feed's first request, the sign
  request's `issuedAt`, the guest tip). Each guide names its known reds; judge the rest yourself.
- Treat every command as literal. Keep quoted names and flags unchanged.

## Proof and skip reporting

- A shell claim is a frame plus the shell's own words: the `capture:` JSON, a `desktop:` log line, or the lane's
  named check in its JSON summary. A chart frame alone proves it drew, not which URL or build drew it.
- A capture passes only with a priced window title (`83,214.3 ▲ BTC - USD`). `BTC - USD` alone is a chart with no
  data, and it still has canvases.
- Evidence goes under `~/Documents/dev-notes/<task>/run-artifacts/<unit>/`. Never hand back an `18097`-`18197` URL.
- Report a blocked box with the attempted command and the unmet precondition: no signed-in account, no funded testnet
  account, no Developer ID build, no Windows VM, no phone wallet, no Screen Recording grant. Never report a box as
  verified through a different entry point.

## Feature entry contract

An H1 title, one paragraph of user-visible behavior with its provenance (date, product tree, what was driven, what
remains unverified), then exactly four H2s in order: `Sub-features`, `How to get to it (user POV)`,
`Driving it with control-kiyotaka-desktop`, `Gotchas`.

## Features

- [Shell launch and window](./shell-launch-and-window.md)
- [Crash recovery and reports](./crash-recovery-and-reports.md)
- [Links and menu](./links-menu-and-channel.md)
- [Return channel and bridge](./return-channel-and-bridge.md)
- [Notifications and app identity](./notifications-and-identity.md)
- [Updates and release](./updates-and-release.md)
- [Browser sign-in, checkout return and the download door](./browser-signin-and-checkout.md)
- [Connect dialog in the shell](./connect-dialog-in-the-shell.md)
- [Browser handoff wallet](./browser-handoff-wallet.md)
- [WalletConnect Solana wallet](./walletconnect-solana.md)
- [Parity sweep](./parity-sweep.md)
- [Electron gaps](./electron-gaps.md)

## Surface inventory

Rediscovered 2026-11-09 from `desktop/src/main/`, `desktop/src/preload/`, `desktop/tools/verify/`, `desktop/scripts/`,
`desktop/policy/`, `desktop/contract.json`, `.gitlab-ci.yml`, the web app's `src/pages/desktop/`, `src/utility/desktop/`
and their callers, `desktop/README.md` and `docs/features/desktop/desktop-shell.md`, on product tree `27fb2d4621`
(`origin/main`), 62 commits after the 2026-11-08 discovery on `537639ebca`. `desktop/` did not change, so no scenario, check or
step was renamed. On the web side `ee1fae1b4d` moves the app's search boxes onto one `SearchField` (a held word takes the first
Escape; the Indicators dialog and the pairing screen's wallet list are on that path) and `b62ef4c998` adds Lite charts, on by
default on weak devices (the parity sweep's Chromium host took it on 2026-11-09); `FuturesTradeTicketPanel.vue` changed in CSS only, so the NinjaTrader doors did not move; the desktop pages and the wallet
utilities did not change. `.gitlab-ci.yml` did not change. A read of every literal and dynamic testid that `parity.mjs`, `gaps.mjs`, `handoff.mjs`, `launch.mjs` and
`qa/tests/e2e/desktop-sign.mjs` use found none that went dead since `537639ebca` (the `si-settings` step's row moved page; see [parity](./parity-sweep.md)). On 2026-11-09 the dev lane had candle
history (250 bars), so the parity sweep and the gaps lane ran; the console stayed locked. Scratch Playwright drives of the unpackaged shell proved the title bar, the view sizing and the download door's absence for the first time. Every path below exists
on `origin/main`. "Live" names the run that last drove the outcome; a row that is pending says so.

| User outcome | Product source path | Guide / sub-feature | Live verification | Prerequisite or gap |
|---|---|---|---|---|
| The shell opens the chart with live candles | `desktop/src/main/index.ts`, `desktop/src/main/channels.ts` | [launch](./shell-launch-and-window.md) `launch-chart` | 2026-11-09, `27fb2d4621`, the `window` scenario's first launch on production (`75,782.7 ▼ BTC - USD`, candle frame) and the dev lane's `returns` frame (250 bars); `capture` frames last 2026-10-28 | a `capture` frame needs an unlocked console; the screen was locked 2026-10-29 to 2026-11-09 |
| A second launch focuses the first window | `desktop/src/main/index.ts` | [launch](./shell-launch-and-window.md) `launch-single` | 2026-11-09, `27fb2d4621`, `window` (`secondInstanceLine`, `secondInstanceExited`, `oneWindow`) | Windows unproven |
| The shell's requests name it: `OpenMarketDesktop/<version>` in the user agent, for server logs and analytics | `desktop/src/main/user-agent.ts` | [launch](./shell-launch-and-window.md) (unit level) | live verification pending (source-read 2026-11-09, `27fb2d4621`; `user-agent` unit test) | no lane reads the sent header |
| Window position, size and maximized state survive relaunch | `desktop/src/main/window-state.ts`, `desktop/src/main/config.ts` | [launch](./shell-launch-and-window.md) `launch-window-state` | 2026-10-28, `5365748ef3`, `window` 12 of 12; from 2026-10-29 to 2026-11-09 (`27fb2d4621`) the saved bounds matched on relaunch, but the relaunch's capture was blocked by the lock (9 of 12) | an unlocked console; Windows unproven |
| The bar and page fill what the screen shows of the window in full screen and maximized, and lay out again on full screen, maximize and display changes | `desktop/src/main/view-area.ts`, `desktop/src/main/index.ts` | [launch](./shell-launch-and-window.md) `launch-view-area` | windowed, resized and maximized live 2026-11-09, `27fb2d4621`, scratch drive reading the views' bounds; full screen pending (`setFullScreen(true)` did not take on the locked console); `desktop/tests/main/view-area.test.ts` in the package suite | full screen needs an unlocked console; the Linux cut it fixes shows only on some Linux desktops, unproven on a real machine; no lane reads the bounds, the recipe is a scratch script |
| The sign-in screen renders in the shell, with no passkey row | `src/components/dialogs/login-signup-dialog/AuthFormView.vue`, `src/services/passkey.service.ts` | [launch](./shell-launch-and-window.md) `launch-login`, [sign-in](./browser-signin-and-checkout.md) `signin-no-passkey` | shell 2026-10-28, `5365748ef3`, `capture --prod --path '?login=1'`, before `4b8f78a775`'s one-card rebuild; Chromium's card with its `login-signup-passkey-btn` "Passkey" pill 2026-11-05, `bf1c9bac3c` | the shell frame of the one-card dialog needs an unlocked console; a full sign-in needs an account |
| "Email me a code" waits for Cloudflare's checkbox, shown under the address | `src/components/dialogs/login-signup-dialog/AuthFormView.vue`, `src/composables/useTurnstile.ts` | [sign-in](./browser-signin-and-checkout.md) `signin-human-check` | placement 2026-11-09, `27fb2d4621`, Chromium on the dev lane (`login-signup-turnstile` between the address and `login-signup-submit-btn`; the button off with no address and on once one was typed, not submitted); the disabled state, its message and, since `45a3754bef`, the code step's own check (`login-signup-code-turnstile`) when the address's check left no token are source-read | a sitekey that asks for the checkbox; the shell frame needs an unlocked console |
| Custom title bar: Back, Forward, title, update button, own tooltips; Alt shows the menu bar | `desktop/src/main/titlebar.ts`, `desktop/src/preload/titlebar.ts` | [launch](./shell-launch-and-window.md) `launch-titlebar` | buttons and tooltips 2026-11-09, `27fb2d4621`, scratch drive (Back and Forward enabled by history, Back and Forward navigated, the bar's own tooltips, `#update` in an unpackaged launch logged `update check skipped`); the disabled state under a screen pending | no lane clicks the bar; the Alt menu bar is Windows and Linux; `capture` frames the page view only |
| A dead page comes back behind "This page stopped working"; a page that keeps dying is held with Reload; a failed load offers Reload | `desktop/src/main/process-gone.ts`, `desktop/src/main/index.ts`, `desktop/src/main/titlebar.ts` | [crash](./crash-recovery-and-reports.md) `crash-reload`, `crash-oom`, `crash-hold`, `crash-load-failed`, `crash-titlebar-gpu`, `crash-early` | 2026-11-09, `27fb2d4621`, `crash` 34 of 34 in 46 s on a stub chart | a recovery over the real chart has no driver; Windows unproven |
| Every crash and failed load is kept on disk and reaches a page as a report it acks; Crashpad uploads a dump | `desktop/src/main/process-gone.ts`, `desktop/src/main/crash-reporter.ts`, `desktop/src/preload/index.ts`, `src/utility/desktop/desktop-analytics.util.ts` | [crash](./crash-recovery-and-reports.md) `crash-report-handover`, `crash-dump` | 2026-11-09, `27fb2d4621`, `crash` (reports by `reportId` through a crash loop, a lost ack and a relaunch; the dump at the stub endpoint) | the page's real beacon to PostHog and Sentry's ingest are spec-only |
| One-time beta notice on first launch | `desktop/src/main/beta-notice.ts` | [launch](./shell-launch-and-window.md) `launch-beta-notice` | live verification pending | shows only on a packaged release build; no lane packs one |
| Links off the chart leave for the system browser; a `/chart/` `window.open` lands in place | `desktop/src/main/link-policy.ts` | [links](./links-menu-and-channel.md) `links-*` | 2026-10-12, `6e93464b59`; red on every run from 2026-10-27 to 2026-11-09 (`27fb2d4621`) | the `links` lane clicks the watermark under the guest signup prompt (`guest-signup-modal-close-btn`) without closing it (product-lane gap) |
| Native menu with Back, Forward, Return to OpenMarket, reload, zoom and full screen; macOS dock lifecycle | `desktop/src/main/menu.ts`, `desktop/src/main/navigation.ts` | [links](./links-menu-and-channel.md) `menu-*` | 2026-10-12 for `menu-items`; `menu-history` pending; the View menu's reload, zoom and full-screen items source-read 2026-11-02 | the `links` lane is red; side buttons are Windows and Linux only |
| Native context menu, silent downloads, remembered clipboard and microphone permissions | `desktop/src/main/context-menu.ts`, `desktop/src/main/downloads.ts`, `desktop/src/main/permissions.ts`, `desktop/src/main/permission-consent.ts` | [links](./links-menu-and-channel.md) `in-window-*`, [Electron gaps](./electron-gaps.md) | context menu and the CSV download 2026-11-09, `27fb2d4621`, gaps guest rows (16 pass in both hosts, as on 2026-11-04 and 2026-11-08, under `12906d4136`'s chart-only cancel): fields and the editor get the native edit menu, selected text Copy, the plot none; permissions pending | permission prompts, collisions and failures have unit tests only |
| `openmarket://return` reaches the page, held off the chart | `desktop/src/main/return-url.ts`, `desktop/src/main/returns.ts`, `desktop/src/preload/index.ts` | [returns](./return-channel-and-bridge.md) | 2026-11-09, `27fb2d4621`, `returns` 20 of 21 in 106 s on a warmed lane with 250 bars; `bridge.keys` read the six members, `reports` included | `bridgeTwoMembers` is stale; Windows unproven |
| OS notifications carry the OpenMarket name and icon | `desktop/electron-builder.yml`, `desktop/src/main/index.ts` | [notifications](./notifications-and-identity.md) | 2026-11-09, `27fb2d4621`, `notify` 12 of 17 | banner and dock need a Developer ID build, Screen Recording and an unlocked console (`screenUnlocked`); `bridgeUnchanged` is stale |
| Shell analytics events reach the page's PostHog | `desktop/src/main/analytics.ts`, `src/utility/desktop/desktop-analytics.util.ts` | [notifications](./notifications-and-identity.md) `identity-analytics` | live verification pending (`analytics.onEvent` and the `desktop:analytics` channel source-read 2026-11-02) | no lane observes PostHog; unit tests only |
| Updates download, stage and offer Restart to Update | `desktop/src/main/updater.ts`, `desktop/src/main/update-bridge.ts` | [updates](./updates-and-release.md) `update-*` | 2026-11-09, `27fb2d4621`, `update` 14 of 15, to the Squirrel.Mac refusal (327 s with `notify` at load 15 to 19, feed on `18150`) | `launchCheckReadBetaFeed` races the policy watcher's first request (red on every run from 2026-10-27 to 2026-11-09 but 2026-11-07); staging needs a Developer ID build |
| Title-bar update button, restart dialog and the page's update toast | `desktop/src/main/titlebar.ts`, `desktop/src/main/index.ts`, `src/utility/desktop/shell-version.util.ts` | [updates](./updates-and-release.md) `update-titlebar`, `update-prompt` | live verification pending | no lane drives the bar; ready needs a Developer ID build |
| Emergency switch: policy notice, block screen and its manual download | `desktop/src/main/policy.ts`, `desktop/policy/`, `desktop/src/preload/titlebar.ts` | [updates](./updates-and-release.md) `policy-notice-block` | live verification pending | no lane serves a policy; an unpackaged launch never reads one |
| Release on merge or tag publishes macOS, Windows and Linux builds, feeds and policies | `desktop/scripts/release-tag.mjs`, `desktop/scripts/publish-r2.sh`, `desktop/scripts/policy.mjs`, `.gitlab-ci.yml` | [updates](./updates-and-release.md) `release-*` | unit tests 2026-11-09, `27fb2d4621` (39 files, 469 of 469); the `publish-r2.sh` dry run 2026-11-05 on `bf1c9bac3c` under `/bin/bash` 3.2.57, 13 upload lines and exit 0; on 2026-10-30 the subprocess tests timed out under machine load | the real jobs need `mac-runner` (the office Mac mini), the certificate, notary key and bucket; the dry run's `rm` half is skipped unattended (placeholders under the run's scratch folder) |
| OpenMarket Internal QA build on the internal chart | `desktop/src/main/build-site.ts`, `desktop/electron-builder.internal.yml` | [updates](./updates-and-release.md) (Gotchas) | live verification pending | its CI job was removed; a hand-packed build is needed |
| Sign in with your browser: button, waiting screen, PKCE exchange | `desktop/src/main/browser-signin.ts`, `src/components/dialogs/login-signup-dialog/DesktopBrowserSignIn.vue` | [sign-in](./browser-signin-and-checkout.md) `signin-button`, `signin-waiting`, `signin-exchange` | live verification pending | a packaged non-dev build or `OPENMARKET_DESKTOP_BROWSER_SIGNIN=1`, and a real orange |
| Browser sign-in pages `/desktop/return` and `/desktop/signin` | `src/pages/desktop/return.page.vue`, `src/pages/desktop/signin.page.vue` | [sign-in](./browser-signin-and-checkout.md) `signin-return-page`, `signin-start-page` | 2026-11-09, `27fb2d4621`, Chromium on the dev lane (return valid and invalid; signin lands on `/chart/auth?redirect=/desktop/signin`) | none |
| Desktop checkout pays in the browser and comes back | `desktop/src/main/checkout-return.ts`, `src/utility/billing/stripe-handoff.util.ts` | [sign-in](./browser-signin-and-checkout.md) `checkout-shell` | live verification pending | a Stripe session, and a packaged build for `openmarket://checkout` |
| Checkout return page: paid, cancelled, portal, invalid | `src/pages/desktop/checkout-return.page.vue`, `src/utility/desktop/checkout-return.util.ts` | [sign-in](./browser-signin-and-checkout.md) `checkout-return-page` | 2026-11-09, `27fb2d4621`, Chromium on the dev lane, all four states | none |
| "Download the OpenMarket desktop app" in a browser, hidden in the shell | `src/utility/desktop/desktop-download-gate.util.ts`, `src/composables/superSearch/providers/featureCommands.ts`, `src/components/GlobalNav/ProfilePanel.vue` | [sign-in](./browser-signin-and-checkout.md) `download-door` | 2026-11-09, `27fb2d4621`, super search in Chromium (the only result for "desktop app"), and in the shell through a scratch drive: no row, "No results found", while a control query returned 72 rows | the profile row is signed-in only |
| Connect dialog in the shell: no deep links, WalletConnect first, Sign in your browser | `src/components/dialogs/HLConnectDialog.vue`, `src/components/hyperliquid/link/HLLinkWalletStep.vue`, `src/components/hyperliquid/link/useHLLinkSheet.ts` | [connect dialog](./connect-dialog-in-the-shell.md) | signed-out step 2026-10-12, `1570b59d69`; parity `hl-enable` red in both hosts on every sweep with steps from 2026-10-27 to 2026-11-09 (`27fb2d4621`); not run 2026-11-05 to 2026-11-07 (no candles) | the rows need a signed-in account; `hl-enable` sits inside the sweep's cascade, which since `ee1fae1b4d` starts at the dialog the sweep's one Escape no longer closes |
| The pairing screen's wallet list: search on its own row, Escape clears the words, then closes | `src/components/dialogs/HLWalletListPanel.vue`, `src/components/hyperliquid/link/HLLinkPairing.vue` | [connect dialog](./connect-dialog-in-the-shell.md) `connect-pairing` | live verification pending (source-read 2026-11-09, `27fb2d4621`, `ee1fae1b4d`) | a signed-in account and a WalletConnect project id |
| Sign page shows the request, signs, returns or refuses | `src/pages/desktop/sign.page.vue`, `src/utility/desktop/sign-request.util.ts` | [handoff](./browser-handoff-wallet.md) `sign-page` | 2026-11-09, `27fb2d4621`, by hand in Chromium: an agent summary, expired and invalid, and the `hl-usd-class-transfer` kind ("Transfer USDC", Spot to perps and Perps to spot, 25.5 and 100 USDC; `1.2345678` invalid) | the MetaMask lane is red: its request lacks `issuedAt` (again 2026-11-09, 76 s); the Balances door to the transfer needs a signed-in account with trading on, and since `49461bebcd` a wallet outside unified-account mode |
| Handoff wallet connects and signs approveAgent, personal_sign and Solana messages | `src/utility/desktop/handoff-bridge.util.ts`, `src/utility/hyperliquid/wallet/handoff-connector.util.ts`, `src/utility/solana/wallet/handoff-wallet-standard.util.ts` | [handoff](./browser-handoff-wallet.md) `handoff-*` | 2026-11-09, `27fb2d4621`: on the warmed testnet lane, `hl` once, through connect and two approveAgent round trips, then the `personal_sign` stall at `handoff.mjs:645`, as on every run that got that far since 2026-10-27; on 2026-11-06 the one run stopped at the crossed-chain request instead (`handoff.mjs:317` from 619); `solana` 2026-10-12 | neither stop isolated; Phantom pin is stale (again 2026-11-08); the transfer kind's own trip and Turn on trading need an account |
| 1-click link step offers message-signing wallets | `src/store/one-click.ts`, `src/components/onchain/OneClickDialog.vue` | [handoff](./browser-handoff-wallet.md) `handoff-oneclick-link` | live verification pending | Privy and the onchain service; covered by specs only |
| WalletConnect Solana wallet pairs a phone and signs, with the shared Pulse pairing block | `src/utility/solana/wallet/walletconnect-wallet-standard.util.ts`, `src/components/onchain/OnchainWalletConnectPairing.vue` | [WalletConnect Solana](./walletconnect-solana.md) | live verification pending | the wrapper passes no project id; a signed-in account and a phone |
| NinjaTrader's connect doors read "Available on openmarket.xyz" in the shell, which opens no NinjaTrader link, token or socket | `src/utility/futures/ninjatrader-flags.util.ts`, `src/composables/futures/futures-broker-pick.ts`, `src/components/trading-hub/AccountMenu.vue`, `src/components/futures/FuturesTradeTicketPanel.vue`, `src/pages/settings/Connections.vue`, `src/utility/trading-hub/account-status.util.ts` | unmapped | live verification pending (source-read 2026-11-09, `27fb2d4621`: `FuturesTradeTicketPanel.vue` changed in CSS only; `trading-hub-account-menu-web-only-ninjatrader`, `futures-ticket-web-only-ninjatrader`, `connections-ninjatrader-hint`, the hub card's `webOnly` line; `futuresTrading.brokers.ninjatrader.webOnly`). Attempted 2026-11-09 in the shell as a guest with `kiyo.flag-overrides` `{"futures-trading":true,"futures-ninjatrader":true,"trading-hub":true}`: the Trade button appeared, but the Futures tab read "CME contracts aren’t loading right now", so no CME pane opened, and super search for "ninjatrader" listed only the open-search row | a CME-family pane (the guest CME list is empty on this lane) or a signed-in session for `connections-ninjatrader-hint`; the flags are off for a guest |
| Every verify-kiyotaka recipe looks the same in the shell as in Chromium | `desktop/tools/verify/parity.mjs` | [parity](./parity-sweep.md) | 2026-11-09, `27fb2d4621`, guest steps on a lane with 250 bars: 0 green, 6 blocked, 21 findings (10, 6 and 11 on 2026-11-08). `ind-search` leaves the dialog open because a search field now takes the first Escape, and every later chart step times out; Chromium's Lite charts toast makes every finished pair differ by about 2.5 percent; blocked on the environment 2026-11-05 to 2026-11-07 (no candle history) | the sweep needs a second Escape and a Lite charts decision in both hosts (`parity.mjs`, product-lane gaps); the dev lane needs its v2 streaming host reachable; signed-in phase undriven; Windows sweep needs a VM |
| Electron-versus-Chrome gaps: keys, gestures, file drops, clipboard, offline | `desktop/tools/verify/gaps.mjs` | [Electron gaps](./electron-gaps.md) | 2026-11-09, `27fb2d4621`, guest rows: 16 pass in both hosts, as on 2026-11-04 and 2026-11-08; blocked on the environment 2026-11-05 to 2026-11-07 | the eight `keys-*` rows need an unlocked console; the signed-in rows need the account; the wrapper has no `gaps` verb; `contextmenu-editor`'s starter-list fallback names a dead testid |
| Download page offers the matching installer | `kiyotaka-landing-page-v2` `app/pages/desktop.vue` | unmapped: another repository | unit 6 captures on the landing branch | belongs to the landing site's own verification |

Retired since 2026-10-12, with source evidence: Switch Channel and the Developer menu (`desktop/src/main/menu.ts` says
there is no Developer menu in any build; `desktop/src/main/channels.ts` has the production channel only; `launch.mjs`
has no `channel` scenario).
