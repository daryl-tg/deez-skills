# Connect dialog in the shell

Since `72633c0a7a` (2026-10-23) the Hyperliquid connect dialog is a thin shell over the "Link Hyperliquid" sheet, one
link flow for every broker, which reads the account before any signature. Inside the desktop shell its wallet step drops
every open-in-wallet-app link, the install row and the rescan row, since no wallet app browser or extension exists
there. With no extension found it leads with "Extensions don't run in the desktop app..." and lists WalletConnect
(`hl-connect-walletconnect`) first, then Sign in your browser (`hl-connect-desktop-handoff`), with the
`hl-connect-signs-in-browser` line naming the browser approval and the in-app trading key. Choosing Sign in your browser
opens a separate handoff screen (`hl-link-handoff`, "Finish in your browser, then come back here"). Choosing
WalletConnect opens the pairing screen (`hl-link-pairing`, `hl-connect-wc-qr`). A browser window is unchanged. The
signed-out step ("Turn on trading" reaching `signedOutStep` with `signInOffered`) was last proved by the parity sweep's
`hl-enable` on `1570b59d69` (2026-10-12). On 2026-10-27 (tree `7290d33d10`) and 2026-10-28 (`5365748ef3`), the step
failed on a click timeout in both hosts. That is a sweep cascade, not a shell difference (see
[parity](./parity-sweep.md)), so this pass proves nothing about the dialog. The signed-in rows, the handoff screen and
the pairing screen have no live recipe through this wrapper; `tests/components/dialogs/HLConnectDialog.spec.ts` covers
them.

## Sub-features

- `connect-signed-out` Turn on trading in the shell reaches the sheet's signed-out step, the same as in Chromium.
- `connect-rows` signed in, with no extension: WalletConnect, then Sign in your browser, and no open-in-app, install or
  rescan row.
- `connect-foot` `hl-connect-signs-in-browser` names the browser approval and the in-app trading key.
- `connect-handoff-screen` after choosing Sign in your browser, the `hl-link-handoff` screen reads "Finish in your
  browser, then come back here".
- `connect-pairing` the WalletConnect pairing screen with its QR, Copy, and refresh on expiry.

## How to get to it (user POV)

- Sign in, open a Hyperliquid ticket or the ticker bar's wallet button, and choose Turn on trading. The Link
  Hyperliquid sheet's wallet step lists WalletConnect and Sign in your browser.

## Driving it with control-kiyotaka-desktop

Preconditions:

- Baseline from the [index](./README.md): `lane up`, `doctor` exit `0`.
- A WalletConnect project id in the lane's env, or no WalletConnect row registers and the sheet shows only the
  handoff row. The main checkout's env file has none; unit 7 passed the public production id as
  `VITE_WALLETCONNECT_PROJECT_ID` in the vite process's environment.

- **Signed-out step.** `control-kiyotaka-desktop run parity <dir> hl-enable`. It clicks `tb-wallet-btn`, waits for
  `hl-connect-dialog`, and passes on `signedOutStep` and `signInOffered` with the pair
  `parity-mac-hl-enable-{shell,browser,diff}.png` under 0.5 percent.
- **Wallet rows.** Live verification pending. It needs a signed-in OpenMarket account in the shell. Unit 7 set
  `userStore.user` and opened the dialog from the page; that proves the rows the dialog draws from discovery, not the
  path to them, so do not report it as a user-path proof.
- **Spec level.** `control-kiyotaka-desktop cli -- pnpm vitest run --config vitest.node.config.ts
  tests/components/dialogs/HLConnectDialog.spec.ts tests/utility/hyperliquid/wallet/desktop-shell.spec.ts`.
- **Proof.** The parity pair, plus the sheet's DOM order (`hl-connect-walletconnect` before
  `hl-connect-desktop-handoff`) when an account is available.

## Gotchas

- `isDesktopShell()` reads `window.openmarketDesktop`, never the user agent, so a browser tab cannot pass for the
  shell and an injected stub is not the bridge. Check `Object.keys(window.openmarketDesktop)` reads
  `analytics, onReturn, updates, version` (plus `browserSignIn` on a packaged build) before trusting a capture.
- The button reads "Turn on trading" and the sheet's title "Link Hyperliquid"; "Enable trading" is gone.
- The flow entry points render only behind the `hyperliquid-trading` and `pulse` flags; the parity sweep turns them on
  through the dev build's `kiyo.flag-overrides`, which changes no auth state.
- `docs/features/desktop/desktop-shell.md` (around lines 132 to 140) still describes a "Use WalletConnect" footer and a
  held row. The product doc is stale there; this guide follows the source.
