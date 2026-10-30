# Browser handoff wallet

"Sign in your browser" is a wallet that signs with the extensions in the user's default browser. The shell opens
`/chart/desktop/sign?r=<request>` in that browser; the page shows what it is about to sign, asks the chosen extension,
and navigates to `openmarket://return?id=<id>&payload=<base64url>`, which resolves the waiting request in the app. A
declined prompt, a wrong account or a wrong chain comes back as a refusal at once. Request kinds are `connect`,
`hl-approve-agent` (with an optional `revoke` worded as a throwaway agent), `hl-approve-builder-fee`,
`evm-sign-message`, `solana-sign-message` and `solana-connect`, and every request carries `issuedAt`, the app's clock
when it opened the page; an old request reads expired. It has an EIP-1193 face for Hyperliquid (connect, approveAgent,
approveBuilderFee, personal_sign) and a Wallet Standard face for the 1-click link proof (connect, signMessage, and no
transaction signing). Last driven 2026-10-31 on tree `5475ab32d5` (`origin/main`), with the console session locked
and the machine at a load average of 3 to 6. The sign page's summary, expired and invalid states were proved by hand in
Chromium again: a fresh `hl-approve-agent` request drew `desktop-sign-page-title` "Authorize a trading key", the
summary (key name, agent address, Valid until, Hyperliquid Testnet), `desktop-sign-origin` and
`desktop-sign-no-wallet`; a day-old `issuedAt` drew `desktop-sign-expired` "This signing request has expired"; a
truncated `r` drew `desktop-sign-invalid` "This signing link isn't valid". The `hl` scenario ran once and matched
2026-10-27 (`7290d33d10`) and 2026-10-29 (`30481b57f8`): the connect and two approveAgent round trips went through,
three `desktop: external` lines each answered by `desktop: return <id>`, then it timed out at the `personal_sign`
request (`timed out waiting for the shell to hand the sign page to the browser`, `waitFor` at `handoff.mjs:226` from
`nextSignPage` at 238 from `hlScenario` at 645), after 3 min 6 s. Three runs at very different loads stop at the same
line, so the cause is in the lane or the page, not load; it is not isolated. On 2026-10-28 (`5365748ef3`) it stopped
earlier, twice, at `waitForChart` (`handoff.mjs:230`) before any request; that stall has not recurred. The sign-page
lane and the `solana` scenario failed at their own preconditions again (see Driving).
The last fully green runs were 2026-10-12 (`hl` on `3a5f33b9a0`,
`solana` on `60e27509cc`, sign lane on `133c5af8ca`). Turn on trading, a relaunch with trading enabled, an order and the
1-click link are blocked on a signed-in OpenMarket account; the order also needs a funded testnet account.

## Sub-features

- `sign-page` the page decodes the request, shows its summary before any wallet, signs, and returns; a tampered
  request offers no wallet, and an old one reads "This signing request has expired".
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
- **Sign page lane.** `control-kiyotaka-desktop run sign <dir>` signs with MetaMask, 16 checks when green, among them
  `the signature recovers to the requested account` and `a tampered request raises no MetaMask prompt`. On 2026-10-27
  and again on 2026-10-28, 2026-10-29 and 2026-10-31 it onboarded MetaMask and then failed `desktop-sign-summary` after
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
  `handoff.mjs:645` stop.
- **Wallet Standard face.** `control-kiyotaka-desktop run handoff <dir> solana`. When green, all 7 checks pass; the
  wallet's features are exactly `solana:signMessage`, `standard:connect` and `standard:events`. On 2026-10-27,
  2026-10-28, 2026-10-29 and 2026-10-31 it stopped at `Phantom CRX is not the pinned 26.32.0 build`.
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
