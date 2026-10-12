# Browser handoff wallet

"Sign in your browser" is a wallet that signs with the extensions in the user's default browser. The shell opens
`/chart/desktop/sign?r=<request>` in that browser; the page shows what it is about to sign, asks the chosen extension,
and navigates to `openmarket://return?id=<id>&payload=<base64url>`, which resolves the waiting request in the app. A
declined prompt, a wrong account or a wrong chain comes back as a refusal at once. It has an EIP-1193 face for
Hyperliquid (connect, approveAgent, approveBuilderFee, personal_sign) and a Wallet Standard face for the 1-click link
proof (connect, signMessage, and no transaction signing). Last driven 2026-10-12: the `hl` scenario on `3a5f33b9a0`
(16 checks, MetaMask 13.50.0) and the `solana` scenario on `60e27509cc` (7 checks, Phantom 26.32.0) by unit 9, and
the sign page lane on `133c5af8ca` (16 checks). The Enable trading button, a relaunch with trading enabled, an order
and the 1-click link are blocked on a signed-in OpenMarket account; the order also needs a funded testnet account.

## Sub-features

- `sign-page` the page decodes the request, shows its summary before any wallet, signs, and returns; a tampered
  request offers no wallet.
- `sign-refusals` `rejected`, `wrong-account` and `wrong-chain` go back on the return URL and settle the app's call.
- `handoff-hl-connect` the registry's `desktop-handoff:browser` row connects through the page, and a relaunch
  restores it with no browser trip.
- `handoff-hl-approve` approveAgent signs through the page and recovers to the wallet's account.
- `handoff-personal-sign` `personal_sign` signs through the `evm-sign-message` kind.
- `handoff-solana` the Wallet Standard face connects and signs a link-proof message with a valid Ed25519 signature.
- `handoff-oneclick-link` the 1-click link step lists the handoff wallet among the wallets that sign messages.

## How to get to it (user POV)

- In the connect dialog choose Sign in your browser. The browser opens OpenMarket's sign page; choose your wallet,
  approve, and allow the browser to open OpenMarket.

## Driving it with control-kiyotaka-desktop

Preconditions:

- `control-kiyotaka-desktop lane up --testnet`, then `doctor` exit `0`.
- No OpenMarket bundle on disk outside this checkout's `desktop/dist-app/`.
- The pinned MetaMask zip and Phantom CRX download once into `node_modules/.cache/desktop-sign/` and
  `node_modules/.cache/desktop-handoff/`, checked by sha256.

- **Sign page alone.** `control-kiyotaka-desktop run sign <dir>`. All 16 checks pass, among them
  `the signature recovers to the requested account` and `a tampered request raises no MetaMask prompt`. It saves
  `unit-08-sign-summary.png`, `unit-08-sign-return.png` and `unit-08-sign-tampered.png`.
- **EIP-1193 face.** `control-kiyotaka-desktop run handoff <dir> hl`. The shell logs
  `desktop: external http://127.0.0.1:<port>/chart/desktop/sign?r=...` for each request and `desktop: return <id>`
  for each answer. All 16 checks pass, among them `pageHandsBackWrongChain`, `refusalSettlesAtOnce`,
  `personalSignatureRecoversToOwner`, and the silent relaunch with no `desktop: external` line. Hyperliquid testnet
  answers the posted approval with `Must deposit before performing actions`, which names the signer and is the
  expected boundary for an unfunded account.
- **Wallet Standard face.** `control-kiyotaka-desktop run handoff <dir> solana`. All 7 checks pass; the wallet's
  features are exactly `solana:signMessage`, `standard:connect` and `standard:events`.
- **Proof.** The lane summaries and their PNGs, among them `unit-09-handoff-prompt.png` and
  `unit-09-oneclick-signmessage.png`.

## Gotchas

- The lanes replace the system browser with Playwright Chromiums carrying real extensions on seeds made for the run.
  Seeds and passwords live only in the lane process; the profiles are deleted on exit. Never copy a lane screenshot
  that shows a seed.
- The `hl` scenario drives the face through the app's own modules imported by their dev-server URLs, which works only
  on a dev lane. It proves the provider, the bridge, the round trip and the venue boundary, not the Enable trading
  button.
- MetaMask 13.50 draws dapp prompts in its side panel, which Playwright does not expose; the lane opens the pending
  prompt's route in a tab. The signature is still MetaMask's own.
- The Phantom pin ages: the Web Store serves only the current build, so a fresh machine fails the sha256 check until
  the pin is bumped. Onboarding stops before Phantom's username screen, which would register a name with Phantom.
- A closed browser tab sends nothing back. The app's sign budget is the backstop for a sign request, and the caller's
  connect budget for a connect.
