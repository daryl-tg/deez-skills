# Browser handoff wallet

"Sign in your browser" is a wallet that signs with the extensions in the user's default browser. The shell opens
`/chart/desktop/sign?r=<request>` in that browser; the page shows what it is about to sign, asks the chosen extension,
and navigates to `openmarket://return?id=<id>&payload=<base64url>`, which resolves the waiting request in the app. A
declined prompt, a wrong account or a wrong chain comes back as a refusal at once. Request kinds are `connect`,
`hl-approve-agent` (with an optional `revoke` worded as a throwaway agent), `hl-approve-builder-fee`,
`hl-usd-class-transfer` (since `b0d7a91522`, 2026-11-01: USDC between the account's own spot and perps balances, the
page titled "Transfer USDC" with Transfer "Spot to perps" or "Perps to spot", Amount and Network rows; the amount must
read exactly as the trading store writes it, at most six fraction digits), `evm-sign-message`, `solana-sign-message`
and `solana-connect`, and every request carries `issuedAt`, the app's clock when it opened the page; an old request
reads expired. It has an EIP-1193 face for Hyperliquid (connect, approveAgent, approveBuilderFee, usdClassTransfer,
personal_sign) and a Wallet Standard face for the 1-click link proof (connect, signMessage, and no transaction
signing). Last driven 2026-11-09 on tree `27fb2d4621` (`origin/main`; nothing on this path changed since `8bcd72f8f5`), with
the console session locked, with the same results as on 2026-11-07 and 2026-11-08: the six sign-page states by hand, `run sign` failing
`desktop-sign-summary` (76 s), `hl` once through the connect and two approveAgent round trips to the `personal_sign`
stall at `handoff.mjs:645` (186 s; three `desktop: external`, three `desktop: return`), and `solana` at the Phantom pin
(`handoff.mjs:95`, 19 s). The testnet lane was warmed in Chromium to a `BTC - USD` title first. On 2026-11-07, with the
console session locked. By hand in Chromium on the dev lane, one state at a time through `about:blank`, a fresh
`hl-approve-agent` request drew the title, summary, origin and no-wallet rows, a day-old one `desktop-sign-expired`, a
truncated `r` `desktop-sign-invalid`, and the transfer kind "Transfer USDC" with "Spot to perps" or (`toPerp: false`)
"Perps to spot" and "25.5 USDC", while `1.2345678` drew `desktop-sign-invalid` in the same session. On a testnet lane
warmed in Chromium first (a `BTC - USD` title; the streaming host did not resolve), with the browser session closed
before each pack, `run sign` onboarded MetaMask 13.50.0 and failed `desktop-sign-summary` after 60 s as before (77 s in
all). The `hl` scenario ran once, 190 s: the connect and two approveAgent round trips went through (three `desktop:
external`, three `desktop: return`), then it timed out at the `personal_sign` request (`handoff.mjs:226` from 238 from
`hlScenario` at 645), `completed: false`. The `solana` scenario stopped at the Phantom pin in 19 s. On 2026-11-06, on
`8bcd72f8f5`, the one `hl` run stopped at the crossed-chain request instead (`handoff.mjs:317` from 619, 196 s). On 2026-11-05, on `bf1c9bac3c`, the sign page was proved by hand in Chromium, one state
at a time: a fresh `hl-approve-agent` request drew
`desktop-sign-page-title` "Authorize a trading key", the summary (key name, agent address, Valid until, Hyperliquid
Testnet, Account), `desktop-sign-origin` and `desktop-sign-no-wallet`; a day-old `issuedAt` drew `desktop-sign-expired`
"This signing request has expired"; a truncated `r` drew `desktop-sign-invalid` "This signing link isn't valid"; and the
`hl-usd-class-transfer` kind drew "Transfer USDC" with Transfer "Spot to perps", Amount "25.5 USDC", Network
"Hyperliquid Testnet" and Account (`toPerp: false` and `100` read "Perps to spot" and "100 USDC"), while an amount of
`1.2345678` drew `desktop-sign-invalid` (on 2026-11-05 only in a fresh browser session; see Gotchas). The `hl`
scenario ran twice, 153 s and 206 s. The first stopped on the very first request, the connect: one `desktop: external
.../desktop/sign?r=...`, then the sign page showed no MetaMask row for 90 s (`desktop-sign-wallet` filtered by
`MetaMask`, `signInBrowser` at `handoff.mjs:307` from `hlScenario` at 495). The lane log held `Failed to fetch
dynamically imported module` lines and a `[VUE_ROUTER_R0011] Unexpected error when starting the router` in that
window, about a minute after the pack made vite reload every open page on the lane (see the [index](./README.md)), so
read it as a page that never booted, not a wallet result; the cause is not isolated. The second went through the connect and two approveAgent round trips
(three `desktop: external`, three `desktop: return`) and then timed out at the `personal_sign` request (`timed out
waiting for the shell to hand the sign page to the browser`, `waitFor` at `handoff.mjs:226` from `nextSignPage` at 238
from `hlScenario` at 645), `completed: false`. On 2026-11-04 one run stopped on the crossed-chain request
(`handoff.mjs:317` from 619, the MetaMask row clicked and no return) and the next reached the `personal_sign` stop; on
2026-11-03 one stopped at the crossed-chain request's wallet row (`handoff.mjs:307`) and the next reached the same
stop. The `personal_sign` stop has repeated on every candle-lane run since 2026-10-27
(`7290d33d10`), at very different loads, so its cause is in the lane or the page, not load or data. Neither stop is
isolated. A `waitForChart` stop (`handoff.mjs:230`) means the page never booted: on 2026-10-28, 2026-11-01 and the
first run of 2026-11-03 that was a dev lane with no candles or a cold vite (see the [index](./README.md)). The
sign-page lane and the `solana` scenario failed at their own preconditions again (see Driving).
The last fully green runs were 2026-10-12 (`hl` on `3a5f33b9a0`,
`solana` on `60e27509cc`, sign lane on `133c5af8ca`). Turn on trading, a relaunch with trading enabled, an order and the
1-click link are blocked on a signed-in OpenMarket account; the order also needs a funded testnet account.

## Sub-features

- `sign-page` the page decodes the request, shows its summary before any wallet (a trading key, a builder fee, a USDC
  transfer between spot and perps, a message, or a connect), signs, and returns; a tampered request offers no wallet,
  and an old one reads "This signing request has expired".
- `sign-refusals` `rejected`, `wrong-account` and `wrong-chain` go back on the return URL and settle the app's call.
- `handoff-hl-connect` the registry's `desktop-handoff:browser` row connects through the page, and a relaunch
  restores it with no browser trip.
- `handoff-hl-approve` approveAgent signs through the page and recovers to the wallet's account.
- `handoff-personal-sign` `personal_sign` signs through the `evm-sign-message` kind.
- `handoff-solana` the Wallet Standard face connects and signs a link-proof message with a valid Ed25519 signature.
- `handoff-oneclick-link` the 1-click link step (`one-click-link-choose`, `one-click-link-wallet`) lists the handoff
  wallet among the wallets that sign messages, as the linked wallet only.

## How to get to it (user POV)

- In the Link Hyperliquid sheet choose Sign in your browser. The browser opens OpenMarket's sign page; choose your
  wallet, approve, and allow the browser to open OpenMarket.

## Driving it with control-kiyotaka-desktop

Preconditions:

- `control-kiyotaka-desktop lane up --testnet`, then `doctor` exit `0`.
- No OpenMarket bundle on disk outside this checkout's `desktop/dist-app/`.
- The pinned MetaMask zip and Phantom CRX download once into `node_modules/.cache/desktop-sign/` and
  `node_modules/.cache/desktop-handoff/`, checked by sha256.

- **Sign page by hand.** Build `hl-approve-agent` requests with `issuedAt: Date.now()`, an `agentName` of
  `openmarket valid_until <ms>`, `hyperliquidChain: 'Testnet'` and `signatureChainId: '0x1'`, base64url the JSON, and
  open `http://127.0.0.1:<port>/chart/desktop/sign?r=<b64>` with `control-kiyotaka-desktop browser`. A fresh request shows
  `desktop-sign-page-title` "Authorize a trading key", `desktop-sign-summary` (key name, agent address, Valid until,
  network), `desktop-sign-origin`, and with no extension `desktop-sign-no-wallet`. `issuedAt` a day old shows
  `desktop-sign-expired`; a truncated `r` shows `desktop-sign-invalid`. No wallet is asked in any of these.
- **The transfer kind by hand.** Build `{ kind: 'hl-usd-class-transfer', id, issuedAt: Date.now(), address, amount:
  '25.5', toPerp: true, nonce: issuedAt, hyperliquidChain: 'Testnet', signatureChainId: '0x1' }` the same way. It
  shows `desktop-sign-page-title` "Transfer USDC" and `desktop-sign-summary` with Transfer "Spot to perps", Amount
  "25.5 USDC", Network "Hyperliquid Testnet" and Account; `toPerp: false` reads "Perps to spot". An amount the trading
  store would not write (`'1.2345678'`, seven fraction digits) shows `desktop-sign-invalid`. The page draws these on
  any lane; the request's `hyperliquidChain` names the network.
- **Re-front before each read.** agent-browser's tab drifts to hidden and the boot splash waits on
  `requestAnimationFrame`, so a read that finds `#skeleton-loader` still present after a minute is the hidden tab, not
  the page. Run `browser --session <s> tab t1` before every poll (on 2026-11-01 the expired state read empty for 60 s
  on the first pass and after two polls once re-fronted).
- **Sign page lane.** `control-kiyotaka-desktop run sign <dir>` signs with MetaMask, 16 checks when green, among them
  `the signature recovers to the requested account` and `a tampered request raises no MetaMask prompt`. On 2026-10-27
  and again on every run to 2026-11-04 it onboarded MetaMask (13.50.0) and then failed `desktop-sign-summary` after
  60 s:
  `qa/tests/e2e/desktop-sign.mjs` builds its request with no `issuedAt`, which
  `src/utility/desktop/sign-request.util.ts` rejects, so the page shows `desktop-sign-invalid`. That is a product-lane
  gap.
- **EIP-1193 face.** `control-kiyotaka-desktop run handoff <dir> hl`. The shell logs
  `desktop: external http://127.0.0.1:<port>/chart/desktop/sign?r=...` for each request and `desktop: return <id>`
  for each answer. When green, all 16 checks pass, among them `pageHandsBackWrongChain`, `refusalSettlesAtOnce`,
  `personalSignatureRecoversToOwner`, and the silent relaunch with no `desktop: external` line. On 2026-10-27, twice,
  three requests went out and came back, then `timed out waiting for the shell to hand the sign page to the browser`
  at `handoff.mjs:645`, the `personal_sign` request; no summary checks beyond `completed: false`. Cause not isolated.
  On 2026-10-28, twice, it stopped before the first request: `page.waitForFunction: Timeout 90000ms exceeded` in
  `waitForChart` (`handoff.mjs:230`), `completed: false`. On 2026-10-29 and 2026-10-31 it was back to the
  `handoff.mjs:645` stop. On 2026-11-01 it was the `waitForChart` stop again, on a lane with no candles. On 2026-11-02, with candles, it was
  the `handoff.mjs:645` stop again after 3 min 6 s; `unit-09-handoff-prompt.png` is the only frame it leaves.
  `waitForChart` waits for a BTC title and a canvas, not for history: on 2026-11-03 a lane with 2 bars passed it once
  warm, and a cold lane failed it. Read a `waitForChart` stop as a page that never booted, warm the lane (see the
  [index](./README.md)) and run again before reading it as the scenario's.
- **The lanes on 2026-11-08 and 2026-11-09** read the same as on 2026-11-07: `run sign` 77 and 76 s, `hl` the `personal_sign` stop after
  187 and 186 s, `solana` the Phantom pin in 19 s.
- **The lanes on 2026-11-07.** `run sign` failed `desktop-sign-summary` (no `issuedAt`, 77 s); `run handoff hl` stopped
  once at the `personal_sign` request (`handoff.mjs:645`) after 190 s; `run handoff solana` stopped at the Phantom pin in
  19 s. On 2026-11-06 `run sign` failed the same way (71 s), `hl` stopped once at the crossed-chain request
  (`handoff.mjs:317` from 619) after 196 s, and `solana` was not run.
- **The three lanes on 2026-11-05.** `run sign` onboarded MetaMask 13.50.0 and failed `desktop-sign-summary` after
  60 s as before (no `issuedAt`, 79 s in all); `run handoff hl` stopped once on the connect request's wallet row
  (`handoff.mjs:307` from 495, a page that never booted after the pack's reload) and once at the `personal_sign` stop
  (645); `run handoff solana` stopped at the Phantom pin in 22 s. Only `hl` reached a wallet prompt. On 2026-11-04 the
  `hl` pair was the crossed-chain stop (`handoff.mjs:317` from 619) and the `personal_sign` stop.
- **Wallet Standard face.** `control-kiyotaka-desktop run handoff <dir> solana`. When green, all 7 checks pass; the
  wallet's features are exactly `solana:signMessage`, `standard:connect` and `standard:events`. On every run from
  2026-10-27 to 2026-11-05 it stopped at `Phantom CRX is not the pinned 26.32.0 build` (`handoff.mjs:95`).
- **Proof.** The lane summaries and their PNGs, among them `unit-09-handoff-prompt.png` and
  `unit-09-oneclick-signmessage.png`; for the hand drive, one frame per state plus the testids read.

## Gotchas

- The lanes replace the system browser with Playwright Chromiums carrying real extensions on seeds made for the run.
  Seeds and passwords live only in the lane process; the profiles are deleted on exit. Never copy a lane screenshot
  that shows a seed.
- The `hl` scenario drives the face through the app's own modules imported by their dev-server URLs, which works only
  on a dev lane. It proves the provider, the bridge, the round trip and the venue boundary, not the Turn on trading
  button.
- MetaMask 13.50 draws dapp prompts in its side panel, which Playwright does not expose; the lane opens the pending
  prompt's route in a tab. The signature is still MetaMask's own.
- The Phantom pin ages: the Web Store serves only the current build, so a fresh machine fails the sha256 check until
  the pin is bumped. Onboarding stops before Phantom's username screen, which would register a name with Phantom.
- A closed browser tab sends nothing back. The app's sign budget is the backstop for a sign request, and the caller's
  connect budget for a connect.
- `docs/features/desktop/desktop-shell.md`'s request-kind table and its `eth_signTypedData_v4` row (around lines 250
  to 260 and 401) still name five kinds and two typed-data types; `hl-usd-class-transfer` and
  `HyperliquidTransaction:UsdClassTransfer` are described in `docs/features/hyperliquid/account-panel.md` (around line
  914) instead. The product doc is stale there; this guide follows the source.
- The transfer's door in the app is the Balances sheet's Transfer (`hl-balances-transfer`, `hl-transfer-amount`,
  `hl-transfer-max`), signed-in with trading on, so the trip from the shell to the page is pending; only the page's
  states are proved. Since `49461bebcd` (2026-11-02's tree) the Balances tab withholds Transfer for a wallet in
  Hyperliquid's unified account or portfolio margin mode (the venue refuses `usdClassTransfer` there), so a
  signed-in drive of that trip needs a wallet in the default mode.
- A long-lived browser session can stop booting pages. On 2026-11-05 the session kept open across two packs drew five
  sign states, then sat on `#skeleton-loader` for the bad-amount request for two minutes with the tab visible, twice;
  the body read "Startup is taking longer than expected" and the console held `Failed to fetch dynamically imported
  module`. `browser close`, a fresh session warmed on `/chart/` and the same URL drew `desktop-sign-invalid` at once.
  The cause is not isolated. Read a stuck page in a long-lived session as the session, not the sign page.
