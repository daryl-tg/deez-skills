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
  report those two as blocked on the environment, name the host, and never read it as a shell regression.
- **Warm a freshly started lane before the first shell drive.** A `lane up` starts a cold vite. The first chart load
  after it can fail with `Failed to fetch dynamically imported module` lines and `[VUE_ROUTER_R0011] Unexpected error
  when starting the router` in the lane log, and the page never gets a BTC title. On 2026-11-03 that stopped `returns`
  at `waitForCandles` (`launch.mjs:94`, a 60 s wait for `/BTC/` in the title) after `lane up`, and the `hl` scenario at
  `waitForChart` (`handoff.mjs:230`) after `lane up --testnet`, both before any check. Three Chromium tabs opened at once
  on the cold lane got "Startup is taking longer than expected ... [failed to load external] main.ts" on two pages. On
  the warmed lane the same `returns` and `hl` runs reached their known results. After every `lane up`, load `/chart/` once
  in one browser until the title names BTC, then drive. Open pages one at a time on a cold lane.
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

Rediscovered 2026-11-03 from `desktop/src/main/`, `desktop/src/preload/`, `desktop/tools/verify/`, `desktop/scripts/`,
`desktop/policy/`, `.gitlab-ci.yml`, the web app's `src/pages/desktop/`, `src/utility/desktop/` and their callers, and
`docs/features/desktop/desktop-shell.md`, on product tree `1af9ebbe07` (`origin/main`), 126 commits after the
2026-11-02 discovery on `39b22dd2ec`. Inside `desktop/`, one changed file: `8ce333e5e9` rewrote the comment over
`gaps.mjs`'s `contextMenuRows`. It came with `12906d4136`. Since then the chart page cancels `contextmenu` on the plot
alone (`#main-chart`, `ChartArea.vue` `handleContextMenu`), never in a field, a link or a `[data-allow-context-menu]`
element (`keepsNativeContextMenu`, `src/utility/dom/native-context-menu.util.ts`). The toolbar-stats and bottom-bar menus
share that rule, and `desktop-shell.md` now says so (see [Electron gaps](./electron-gaps.md)). `desktop/src/`,
`desktop/tests/`, `desktop/package.json` (still 0.1.7), the lanes' scenario, check, step and row names and the desktop
CI jobs did not change. On the web side, the sign page, the handoff connector and bridge, the connect dialog and the
desktop pages did not change. In `AuthFormView.vue`, `5027d30d82` moved the 2FA step into `usePendingTwoFA` and drops
it when it expires; the `login-signup-passkey-btn` row and `input[name=email]` are unchanged. `featureCommands.ts` was
reworked (`66a5bcb680`, Show on chart), but the `desktop-app` command keeps its id, aliases and gate. A read of every
testid that `parity.mjs` and `gaps.mjs` use found one dead selector: `global-nav-pulse-btn`, the first of three
alternatives at `parity.mjs:220`. It was already dead on `39b22dd2ec`, and the other two still match. On
2026-11-03 the dev lane had no candle history (the v2 streaming host did not resolve; see Driving conventions), so the
parity sweep, the gaps lane's rows and the right-click rule went undriven, and the console stayed locked. Every path
below exists on `origin/main`. "Live" names the run that last drove the outcome; a row that is pending says so.

| User outcome | Product source path | Guide / sub-feature | Live verification | Prerequisite or gap |
|---|---|---|---|---|
| The shell opens the chart with live candles | `desktop/src/main/index.ts`, `desktop/src/main/channels.ts` | [launch](./shell-launch-and-window.md) `launch-chart` | 2026-11-03, `1af9ebbe07`, the `window` scenario's first launch on production (`76,669.4 ▲ BTC - USD`, candle frame); the dev lane had no history that day (2 bars, `returns` frame); `capture` frames last 2026-10-28 | a `capture` frame needs an unlocked console; the screen was locked 2026-10-29 to 2026-11-03 |
| A second launch focuses the first window | `desktop/src/main/index.ts` | [launch](./shell-launch-and-window.md) `launch-single` | 2026-11-03, `1af9ebbe07`, `window` (`secondInstanceLine`, `secondInstanceExited`, `oneWindow`) | Windows unproven |
| Window position, size and maximized state survive relaunch | `desktop/src/main/window-state.ts`, `desktop/src/main/config.ts` | [launch](./shell-launch-and-window.md) `launch-window-state` | 2026-10-28, `5365748ef3`, `window` 12 of 12; from 2026-10-29 to 2026-11-03 (`1af9ebbe07`) the saved bounds matched on relaunch, but the relaunch's capture was blocked by the lock (9 of 12) | an unlocked console; Windows unproven |
| The sign-in screen renders in the shell, with no passkey row | `src/components/dialogs/login-signup-dialog/AuthFormView.vue`, `src/services/passkey.service.ts` | [launch](./shell-launch-and-window.md) `launch-login`, [sign-in](./browser-signin-and-checkout.md) `signin-no-passkey` | shell 2026-10-28, `5365748ef3`, `capture --prod --path '?login=1'`; Chromium's dialog with its `login-signup-passkey-btn` row 2026-11-03, `1af9ebbe07` (`AuthFormView.vue`'s 2FA-expiry change `5027d30d82` left the rows alone) | the shell frame needs an unlocked console; a full sign-in needs an account |
| Custom title bar: Back, Forward, title, update button, own tooltips; Alt shows the menu bar | `desktop/src/main/titlebar.ts`, `desktop/src/preload/titlebar.ts` | [launch](./shell-launch-and-window.md) `launch-titlebar` | live verification pending | `capture` frames the page view only; unit tests only |
| One-time beta notice on first launch | `desktop/src/main/beta-notice.ts` | [launch](./shell-launch-and-window.md) `launch-beta-notice` | live verification pending | shows only on a packaged release build; no lane packs one |
| Links off the chart leave for the system browser; a `/chart/` `window.open` lands in place | `desktop/src/main/link-policy.ts` | [links](./links-menu-and-channel.md) `links-*` | 2026-10-12, `6e93464b59`; red on every run from 2026-10-27 to 2026-11-03 (`1af9ebbe07`, 64 s) | the `links` lane stops at the onboarding dialog (product-lane gap) |
| Native menu with Back, Forward, Return to OpenMarket, reload, zoom and full screen; macOS dock lifecycle | `desktop/src/main/menu.ts`, `desktop/src/main/navigation.ts` | [links](./links-menu-and-channel.md) `menu-*` | 2026-10-12 for `menu-items`; `menu-history` pending; the View menu's reload, zoom and full-screen items source-read 2026-11-02 | the `links` lane is red; side buttons are Windows and Linux only |
| Native context menu, silent downloads, remembered clipboard and microphone permissions | `desktop/src/main/context-menu.ts`, `desktop/src/main/downloads.ts`, `desktop/src/main/permissions.ts`, `desktop/src/main/permission-consent.ts` | [links](./links-menu-and-channel.md) `in-window-*`, [Electron gaps](./electron-gaps.md) | context menu and the CSV download 2026-11-02, `39b22dd2ec`, gaps guest rows (16 pass in both hosts), under the old document-wide cancel; the chart-only cancel of `12906d4136` is live verification pending (on 2026-11-03 the gaps lane threw in `waitForCandles` before any row, no candle history on the dev lane); permissions pending | the right-click rows need a dev lane with candle history; permission prompts, collisions and failures have unit tests only |
| `openmarket://return` reaches the page, held off the chart | `desktop/src/main/return-url.ts`, `desktop/src/main/returns.ts`, `desktop/src/preload/index.ts` | [returns](./return-channel-and-bridge.md) | 2026-11-03, `1af9ebbe07`, `returns` 20 of 21 in 67 s on a warmed lane (the first run, straight after `lane up`, stopped at `waitForCandles` on a cold vite) | `bridgeTwoMembers` is stale; Windows unproven |
| OS notifications carry the OpenMarket name and icon | `desktop/electron-builder.yml`, `desktop/src/main/index.ts` | [notifications](./notifications-and-identity.md) | 2026-11-03, `1af9ebbe07`, `notify` 12 of 17 in 50 s | banner and dock need a Developer ID build, Screen Recording and an unlocked console (`screenUnlocked`); `bridgeUnchanged` is stale |
| Shell analytics events reach the page's PostHog | `desktop/src/main/analytics.ts`, `src/utility/desktop/desktop-analytics.util.ts` | [notifications](./notifications-and-identity.md) `identity-analytics` | live verification pending (`analytics.onEvent` and the `desktop:analytics` channel source-read 2026-11-02) | no lane observes PostHog; unit tests only |
| Updates download, stage and offer Restart to Update | `desktop/src/main/updater.ts`, `desktop/src/main/update-bridge.ts` | [updates](./updates-and-release.md) `update-*` | 2026-11-03, `1af9ebbe07`, `update` 14 of 15 in 97 s, to the Squirrel.Mac refusal | `launchCheckReadBetaFeed` is stale; staging needs a Developer ID build |
| Title-bar update button, restart dialog and the page's update toast | `desktop/src/main/titlebar.ts`, `desktop/src/main/index.ts`, `src/utility/desktop/shell-version.util.ts` | [updates](./updates-and-release.md) `update-titlebar`, `update-prompt` | live verification pending | no lane drives the bar; ready needs a Developer ID build |
| Emergency switch: policy notice and block screen | `desktop/src/main/policy.ts`, `desktop/policy/` | [updates](./updates-and-release.md) `policy-notice-block` | live verification pending | no lane serves a policy; an unpackaged launch never reads one |
| Release on merge or tag publishes macOS, Windows and Linux builds, feeds and policies | `desktop/scripts/release-tag.mjs`, `desktop/scripts/publish-r2.sh`, `desktop/scripts/policy.mjs`, `.gitlab-ci.yml` | [updates](./updates-and-release.md) `release-*` | unit tests 2026-11-03, `1af9ebbe07` (35 files, 422 of 422 in 2.3 s); the `publish-r2.sh` dry run 2026-11-03 under `/bin/bash` 3.2.57, 13 upload lines and exit 0 (as on 2026-11-02, after `c57cc3af80`'s bash-3.2 loop fix); on 2026-10-30 the subprocess tests timed out under machine load | the real jobs need `mac-runner` (the office Mac mini), the certificate, notary key and bucket; the dry run's `rm` half is skipped unattended (placeholders under the run's scratch folder) |
| OpenMarket Internal QA build on the internal chart | `desktop/src/main/build-site.ts`, `desktop/electron-builder.internal.yml` | [updates](./updates-and-release.md) (Gotchas) | live verification pending | its CI job was removed; a hand-packed build is needed |
| Sign in with your browser: button, waiting screen, PKCE exchange | `desktop/src/main/browser-signin.ts`, `src/components/dialogs/login-signup-dialog/DesktopBrowserSignIn.vue` | [sign-in](./browser-signin-and-checkout.md) `signin-button`, `signin-waiting`, `signin-exchange` | live verification pending | a packaged non-dev build or `OPENMARKET_DESKTOP_BROWSER_SIGNIN=1`, and a real orange |
| Browser sign-in pages `/desktop/return` and `/desktop/signin` | `src/pages/desktop/return.page.vue`, `src/pages/desktop/signin.page.vue` | [sign-in](./browser-signin-and-checkout.md) `signin-return-page`, `signin-start-page` | 2026-11-03, `1af9ebbe07`, Chromium on the dev lane (return valid and invalid; signin lands on `/chart/auth?redirect=/desktop/signin`), on a sequential pass after a cold first pass | none |
| Desktop checkout pays in the browser and comes back | `desktop/src/main/checkout-return.ts`, `src/utility/billing/stripe-handoff.util.ts` | [sign-in](./browser-signin-and-checkout.md) `checkout-shell` | live verification pending | a Stripe session, and a packaged build for `openmarket://checkout` |
| Checkout return page: paid, cancelled, portal, invalid | `src/pages/desktop/checkout-return.page.vue`, `src/utility/desktop/checkout-return.util.ts` | [sign-in](./browser-signin-and-checkout.md) `checkout-return-page` | 2026-11-03, `1af9ebbe07`, Chromium on the dev lane, all four states | none |
| "Download the OpenMarket desktop app" in a browser, hidden in the shell | `src/utility/desktop/desktop-download-gate.util.ts`, `src/composables/superSearch/providers/featureCommands.ts`, `src/components/GlobalNav/ProfilePanel.vue` | [sign-in](./browser-signin-and-checkout.md) `download-door` | 2026-11-03, `1af9ebbe07`, super search in Chromium (the only result for "desktop app", set through the input event once the "Draw by holding" tip was closed with Got it) | the profile row is signed-in only; absence in the shell not driven |
| Connect dialog in the shell: no deep links, WalletConnect first, Sign in your browser | `src/components/dialogs/HLConnectDialog.vue`, `src/components/hyperliquid/link/HLLinkWalletStep.vue`, `src/components/hyperliquid/link/useHLLinkSheet.ts` | [connect dialog](./connect-dialog-in-the-shell.md) | signed-out step 2026-10-12, `1570b59d69`; parity `hl-enable` red in both hosts from 2026-10-27 to 2026-11-02 (`39b22dd2ec`), not run 2026-11-01 or 2026-11-03 (no candle history on the dev lane) | the rows need a signed-in account; `hl-enable` sits inside the sweep's `sym-switch` cascade |
| Sign page shows the request, signs, returns or refuses | `src/pages/desktop/sign.page.vue`, `src/utility/desktop/sign-request.util.ts` | [handoff](./browser-handoff-wallet.md) `sign-page` | 2026-11-03, `1af9ebbe07`, by hand in Chromium: an agent summary, expired and invalid, and the `hl-usd-class-transfer` kind ("Transfer USDC", Spot to perps 25.5 USDC, Perps to spot 100 USDC; a non-canonical amount reads invalid) | the MetaMask lane is red: its request lacks `issuedAt` (again 2026-11-03, 78 s); the Balances door to the transfer needs a signed-in account with trading on, and since `49461bebcd` a wallet outside unified-account mode |
| Handoff wallet connects and signs approveAgent, personal_sign and Solana messages | `src/utility/desktop/handoff-bridge.util.ts`, `src/utility/hyperliquid/wallet/handoff-connector.util.ts`, `src/utility/solana/wallet/handoff-wallet-standard.util.ts` | [handoff](./browser-handoff-wallet.md) `handoff-*` | 2026-11-03, `1af9ebbe07`: on the warmed testnet lane, `hl` connect and two approveAgent round trips (three `desktop: external`, three `desktop: return`), then the `personal_sign` stall at `handoff.mjs:645` in 192 s, as on every candle-lane run since 2026-10-27; one earlier run that day stopped at the crossed-chain request's wallet row (`handoff.mjs:619`) and did not repeat; `solana` 2026-10-12 | the `personal_sign` stall not isolated (same line at every load, with and without the candle stop in between); Phantom pin is stale; the transfer kind's own trip and Turn on trading need an account |
| 1-click link step offers message-signing wallets | `src/store/one-click.ts`, `src/components/onchain/OneClickDialog.vue` | [handoff](./browser-handoff-wallet.md) `handoff-oneclick-link` | live verification pending | Privy and the onchain service; covered by specs only |
| WalletConnect Solana wallet pairs a phone and signs, with the shared Pulse pairing block | `src/utility/solana/wallet/walletconnect-wallet-standard.util.ts`, `src/components/onchain/OnchainWalletConnectPairing.vue` | [WalletConnect Solana](./walletconnect-solana.md) | live verification pending | the wrapper passes no project id; a signed-in account and a phone |
| Every verify-kiyotaka recipe looks the same in the shell as in Chromium | `desktop/tools/verify/parity.mjs` | [parity](./parity-sweep.md) | 2026-11-02, `39b22dd2ec`, guest steps: 9 green, 6 blocked, 12 findings, the same split as 2026-10-29 and 2026-10-31; on 2026-11-01 and 2026-11-03 (`1af9ebbe07`) the sweep threw in `waitForCandles` before any step, no candle history on the dev lane | the dev lane needs its v2 streaming host reachable (it did not resolve on 2026-11-03); signed-in phase undriven; Windows sweep needs a VM |
| Electron-versus-Chrome gaps: keys, gestures, file drops, clipboard, offline | `desktop/tools/verify/gaps.mjs` | [Electron gaps](./electron-gaps.md) | 2026-11-02, `39b22dd2ec`, guest rows: 16 pass in both hosts, under the old document-wide right-click cancel; on 2026-11-01 and 2026-11-03 (`1af9ebbe07`) the lane threw in `waitForCandles` before any row | a dev lane with candle history, to drive the right-click rows under `12906d4136`'s chart-only cancel; the eight `keys-*` rows need an unlocked console; the signed-in rows need the account; the wrapper has no `gaps` verb |
| Download page offers the matching installer | `kiyotaka-landing-page-v2` `app/pages/desktop.vue` | unmapped: another repository | unit 6 captures on the landing branch | belongs to the landing site's own verification |

Retired since 2026-10-12, with source evidence: Switch Channel and the Developer menu (`desktop/src/main/menu.ts` says
there is no Developer menu in any build; `desktop/src/main/channels.ts` has the production channel only; `launch.mjs`
has no `channel` scenario).
