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
- [Links, menu and channel](./links-menu-and-channel.md)
- [Return channel and bridge](./return-channel-and-bridge.md)
- [Notifications and app identity](./notifications-and-identity.md)
- [Updates and release](./updates-and-release.md)
- [Connect dialog in the shell](./connect-dialog-in-the-shell.md)
- [Browser handoff wallet](./browser-handoff-wallet.md)
- [WalletConnect Solana wallet](./walletconnect-solana.md)
- [Parity sweep](./parity-sweep.md)

## Surface inventory

Discovered 2026-10-12 from `desktop/src/`, `desktop/tools/verify/`, the web app's desktop modules and the program's
unit reports, on product tree `d554bfb38c` (`daryl/desktop-shell`). "Live" names the run that last drove the outcome.

| User outcome | Product source path | Guide / sub-feature | Live verification | Prerequisite or gap |
|---|---|---|---|---|
| The shell opens the chart with live candles | `desktop/src/main/index.ts`, `desktop/src/main/channels.ts` | [launch](./shell-launch-and-window.md) `launch-chart` | 2026-10-12, `d554bfb38c`, through this wrapper's `capture` | none |
| A second launch focuses the first window | `desktop/src/main/index.ts` | [launch](./shell-launch-and-window.md) `launch-single` | 2026-10-12, `6e93464b59`, `window` scenario | Windows unproven |
| Window position, size and maximized state survive relaunch | `desktop/src/main/window-state.ts`, `desktop/src/main/config.ts` | [launch](./shell-launch-and-window.md) `launch-window-state` | 2026-10-12, `6e93464b59`, `window` scenario | Windows unproven |
| The sign-in screen renders with Turnstile passing | `src/components/dialogs/login-signup-dialog/AuthFormView.vue` | [launch](./shell-launch-and-window.md) `launch-login` | 2026-10-12, `d554bfb38c`, wrapper `capture --prod --path '?login=1'`; parity `login-wall` on `1570b59d69` judged by eye (F2) | a full sign-in needs an account |
| Links off the chart leave for the system browser | `desktop/src/main/link-policy.ts` | [links](./links-menu-and-channel.md) `links-external` | 2026-10-12, `6e93464b59`, `links` scenario | none |
| Native menu, hidden Developer menu, macOS dock lifecycle | `desktop/src/main/menu.ts` | [links](./links-menu-and-channel.md) `menu-*` | 2026-10-12, `6e93464b59`, `links` scenario | packaged hiding is unit-tested only |
| Switch Channel relaunches onto staging | `desktop/src/main/channels.ts`, `desktop/src/main/config.ts` | [links](./links-menu-and-channel.md) `channel-switch` | 2026-10-12, `6e93464b59`, `channel` scenario | `kiyotaka.dev` has no DNS on the mini; the window URL is the proof |
| `openmarket://return` reaches the page, held off the chart | `desktop/src/main/return-url.ts`, `desktop/src/main/returns.ts`, `desktop/src/preload/index.ts` | [returns](./return-channel-and-bridge.md) | 2026-10-12, `133c5af8ca`, `returns` scenario | Windows unproven |
| OS notifications carry the OpenMarket name and icon | `desktop/electron-builder.yml`, `desktop/src/main/index.ts` | [notifications](./notifications-and-identity.md) | 2026-10-12, `13e5d12723`, `notify` scenario, 14 of 17 | banner and dock captures need a Developer ID build and Screen Recording |
| Updates download, stage and offer Restart to Update | `desktop/src/main/updater.ts` | [updates](./updates-and-release.md) `update-*` | 2026-10-12, `6e93464b59`, `update` scenario to the Squirrel.Mac refusal | staging and relaunch need a Developer ID build |
| A `desktop-v*` tag publishes signed installers and feeds | `desktop/scripts/release-tag.mjs`, `desktop/scripts/publish-r2.sh`, `.gitlab-ci.yml` | [updates](./updates-and-release.md) `release-*` | source and dry runs only | no runner, certificate, notary key, Windows route or bucket yet |
| Connect dialog in the shell: no deep links, WalletConnect first, Sign in your browser | `src/components/dialogs/HLConnectDialog.vue` | [connect dialog](./connect-dialog-in-the-shell.md) | 2026-10-12, `23b86fd129`, unit 7 capture | the drive sets a signed-in user in the page |
| Sign page shows the request, signs, returns or refuses | `src/pages/desktop/sign.page.vue`, `src/utility/desktop/sign-request.util.ts` | [handoff](./browser-handoff-wallet.md) `sign-page` | 2026-10-12, `133c5af8ca`, `desktop-sign.mjs` 16 checks | none |
| Handoff wallet connects and signs approveAgent, personal_sign and Solana messages | `src/utility/desktop/handoff-bridge.util.ts`, `src/utility/hyperliquid/wallet/handoff-connector.util.ts`, `src/utility/solana/wallet/handoff-wallet-standard.util.ts` | [handoff](./browser-handoff-wallet.md) `handoff-*` | 2026-10-12, `3a5f33b9a0` (hl) and `60e27509cc` (solana) | Enable trading, the order and the 1-click link need a signed-in account |
| 1-click link step offers message-signing wallets | `src/store/one-click.ts`, `src/components/onchain/OneClickDialog.vue` | [handoff](./browser-handoff-wallet.md) `handoff-oneclick-link` | live verification pending | Privy and the onchain service; covered by specs only |
| WalletConnect Solana wallet pairs a phone and signs | `src/utility/solana/wallet/walletconnect-wallet-standard.util.ts` | [WalletConnect Solana](./walletconnect-solana.md) | live verification pending | the lane launch was refused by the permission classifier; pairing needs a phone |
| Every verify-kiyotaka recipe looks the same in the shell as in Chromium | `desktop/tools/verify/parity.mjs` | [parity](./parity-sweep.md) | 2026-10-12, `1570b59d69`, 15 green, 4 green at boundary, 2 findings, 6 blocked | Windows sweep needs a VM |
| Download page offers the matching installer | `kiyotaka-landing-page-v2` `app/pages/desktop.vue` | unmapped: another repository | unit 6 captures on the landing branch | belongs to the landing site's own verification |
