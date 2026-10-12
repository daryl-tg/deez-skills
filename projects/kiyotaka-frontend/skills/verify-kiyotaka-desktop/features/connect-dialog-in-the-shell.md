# Connect dialog in the shell

Inside the shell the Hyperliquid connect dialog drops every open-in-wallet-app link, since no wallet app browser
exists there. With no extension found, it says "Extensions don't run in the desktop app. Connect from your phone, or
sign with the wallet in your browser." and lists WalletConnect first, then Sign in your browser. Its foot line reads
"The one-time approval signs in your browser. Orders are signed by the trading key in the app." The Solana wallet
surfaces drop their phone links the same way. A browser window is unchanged. The rows were last captured 2026-10-12
on `23b86fd129` by unit 7, with the Sign in your browser row still disabled; unit 9 enabled it on `133c5af8ca`, proved
by `tests/components/dialogs/HLConnectDialog.spec.ts`. The signed-out step was driven in the shell by the parity
sweep's `hl-enable` on `1570b59d69`. The signed-in rows have no live recipe through this wrapper yet.

## Sub-features

- `connect-signed-out` Enable trading in the shell reaches the dialog's signed-out step, the same as in Chromium.
- `connect-rows` signed in, with no extension: WalletConnect, then Sign in your browser, and no open-in-app row.
- `connect-foot` the foot line names the browser approval and the in-app trading key.
- `connect-held` after choosing Sign in your browser, the row reads "Finish in your browser, then come back here".

## How to get to it (user POV)

- Sign in, open a Hyperliquid ticket, choose Enable trading. The wallet step lists WalletConnect and Sign in your
  browser.

## Driving it with control-kiyotaka-desktop

Preconditions:

- Baseline from the [index](./README.md): `lane up`, `doctor` exit `0`.
- A WalletConnect project id in the lane's env, or no WalletConnect row registers and the dialog shows only the
  handoff row. The main checkout's env file has none; unit 7 passed the public production id as
  `VITE_WALLETCONNECT_PROJECT_ID` in the vite process's environment.

- **Signed-out step.** `control-kiyotaka-desktop run parity <dir> hl-enable`. The pair
  `parity-mac-hl-enable-{shell,browser,diff}.png` must be GREEN at the boundary, under 0.5 percent.
- **Wallet rows.** Live verification pending. It needs a signed-in OpenMarket account in the shell. Unit 7 set
  `userStore.user` and opened the dialog with `dialogStore.toggleHLConnectDialog(true)` in the page; that proves the
  rows the dialog draws from discovery, not the path to them, so do not report it as a user-path proof.
- **Spec level.** `control-kiyotaka-desktop cli -- pnpm vitest run --config vitest.node.config.ts
  tests/components/dialogs/HLConnectDialog.spec.ts tests/utility/hyperliquid/wallet/desktop-shell.spec.ts`.
- **Proof.** The parity pair, plus the dialog's DOM order (`hl-connect-walletconnect` before
  `hl-connect-desktop-handoff`) when an account is available.

## Gotchas

- `isDesktopShell()` reads `window.openmarketDesktop`, never the user agent, so a browser tab cannot pass for the
  shell and an injected stub is not the bridge. Check `Object.keys(window.openmarketDesktop)` reads
  `onReturn, version` before trusting a capture.
- The flow entry points render only behind the `hyperliquid-trading` and `pulse` flags; the parity sweep turns them on
  through the dev build's `kiyo.flag-overrides`, which changes no auth state.
- `HLWalletListPanel` keeps its own `isMobileBrowser() && !isDesktopShell()` pick: on a touch screen in the shell it
  opens a wallet's desktop link in a new window, never a phone link in place.
