# WalletConnect Solana wallet

In the shell only, a Wallet Standard wallet named WalletConnect pairs a phone wallet over WalletConnect's Solana
namespace and offers `standard:connect`, `standard:disconnect`, `standard:events`, `solana:signMessage`,
`solana:signTransaction` and `solana:signAndSendTransaction`. Pulse, the 1-click link proof and the subscribe lane
find it the way they find any Solana wallet, and the pairing code draws in the Pulse ticket's QR. It registers only
when `isDesktopShell()` holds and a WalletConnect project id is set. Live verification pending: unit 10's lane launch
on 2026-10-12 was refused by the session's permission classifier, so no `unit-10-qr.png` exists, and pairing,
signing and a swap need a phone wallet. The behavior is proved by
`tests/utility/solana/wallet/walletconnect-wallet-standard.spec.ts` (19 cases) on `c2c02c810e`.

## Sub-features

- `wc-sol-register` the wallet registers in the shell with a project id, and not in a browser or without one.
- `wc-sol-qr` choosing WalletConnect on Pulse's own-wallet row draws the pairing QR and opens the relay socket.
- `wc-sol-pair` a phone wallet approves the session and the row shows its address.
- `wc-sol-sign` a message, a transaction and a swap sign on the phone.

## How to get to it (user POV)

- Open Pulse on a Solana token, open the ticket's wallet menu, and choose WalletConnect. Scan the code with Phantom
  or Solflare on a phone.

## Driving it with control-kiyotaka-desktop

Preconditions:

- `lane up` with `VITE_WALLETCONNECT_PROJECT_ID` in the vite process's environment, then `doctor` exit `0`. The main
  checkout's env file carries no WalletConnect id; the production id is public and is read from the deployed
  `app-core` chunk. The wrapper does not pass it today, so this precondition is unmet through the wrapper.
- A signed-in account, with the Solana flag and the sanctions read loaded, for Pulse's connect.

- **QR in the shell.** Live verification pending. Launch the shell against the lane with Playwright's Electron
  launcher on a fresh profile, open the ticket's wallet menu, choose Connect WalletConnect, and pass when
  `[data-testid="pulse-pairing-qr"]` is visible and a websocket to the WalletConnect relay is open. SDK 2.25.0's
  default relay is `relay.walletconnect.org`.
- **Pairing and signing, operator.** `control-kiyotaka-desktop cli -- env WALLETCONNECT_PROJECT_ID=<public id> node
  qa/walletconnect-solana/pair.mjs` prints a QR. Scan it with a phone wallet, approve the message and the v0 transfer
  of 0 lamports to self, which is signed and never sent. Exit `0` and a last JSON line with `signatureValid: true`
  settle whether a versioned transaction crosses WalletConnect intact.
- **Spec level.** `control-kiyotaka-desktop cli -- pnpm vitest run --config vitest.node.config.ts
  tests/utility/solana/wallet/walletconnect-wallet-standard.spec.ts`.
- **Proof.** The QR capture with the relay socket in the network log; for pairing, the operator's screenshot of the
  connected row and the probe's verdict.

## Gotchas

- Copying the main checkout's env file into a worktree, and injecting the production id, were refused by the
  permission classifier in unit 10. The wrapper's `lane up` reads the env file in place with `node --env-file`; the
  project id still has to reach the vite process some other way the operator approves.
- The pairing has the 180 s pairing budget, not the 60 s own-wallet connect budget.
- A restored session is resumed only if the phone answers a relay ping within 10 s; a locked phone is asked to scan
  again.
- The QR channel is shared with the Hyperliquid connector, so an open HL connect dialog would draw the Solana code.
