# OpenFloor verification map

The maintained source for verifying user-facing behavior on the OpenFloor iOS
simulator lane. Read this index before driving, then use the matching feature
file as the recipe.

Handles below were read off a live simulator on **2026-09-02** (iPhone 17 Pro,
iOS 26.5, `sh.openmarket.openfloor`, Metro on 8081).

## Baseline preconditions

- Metro is up on its **assigned** port `8081`, bundling *this* checkout.
  `pnpm start` if it is not.
- `./control-openfloor doctor` exits zero and reports the working tree, a booted
  simulator, and the app installed.
- `./control-openfloor app open` returns a snapshot containing
  `[other] "Primary navigation"` — that is the app shell, not the dev launcher.
- The account is signed in. Signing in is not part of any recipe here; a signed
  out app shows `/sign-in` and every recipe below is unreachable.
- Never drive a simulator whose Metro doctor reported `FOREIGN`.

## Driving conventions

- Start every recipe from the Chats root unless its preconditions say otherwise.
  `./control-openfloor app open` lands there.
- Prefer accessible names over coordinates. Commands go through
  `./control-openfloor device <verb>`, repo commands through
  `./control-openfloor cli -- <command>`.
- Continue from the `--settle` diff; refs go stale after every mutation.
- Treat every command as literal. Keep quoted labels and flags unchanged.
- **Never exact-match a label containing an unread count.** They drift live.
  Use `find "<stable substring>"`.
- Restore anything you mutate. Never remove proof artifacts.

## Proof and skip reporting

- Capture the user action and the resulting state, not only the final screen.
- UI proof is a **pair**: the `--settle` diff (diffable, survives a restyle) and
  a screenshot (what a human reads). Both should show app identity.
- Persistence proof is a third observation: `./control-openfloor app reset` — a
  real `simctl terminate` — then re-navigate and re-read the value.
- CLI proof includes the command, stdout, stderr, and exit code.
- Publish with `./control-openfloor evidence publish <run-id> <revision>` and
  hand back the returned `127.0.0.1:8100` URL.
- Report an unreachable path with the attempted command and the unmet
  precondition. **Never report a skipped entry point as verified via another
  path** — if the server-channel route collapsed the AX tree and you proved the
  conversation surface through a DM instead, that is a delta, not a pass.

## Feature entry contract

An H1 title, one paragraph of user-visible behavior, then exactly four H2s in
order: `Sub-features`, `How to get to it (user POV)`,
`Driving it with control-openfloor`, `Gotchas`.

Keep implementation detail out. Name only user paths, stable handles, required
state, commands, and observable proof.

## Features

- [Chats inbox](./chats-inbox.md) — the unified DM + server rollup inbox, its
  search, filter, alerts and new-conversation launcher.
- [Servers and channels](./servers-and-channels.md) — the server grid, a
  server's channel tree, topics and its Library.
- [Conversation and composer](./conversation-and-composer.md) — the shared
  message surface: transcript, reactions, attachments, composer states.
- [Appearance and settings](./appearance-and-settings.md) — the You tab,
  settings tree, and the App theme palette/accent/light-dark dials.
- [Tab navigation and parking](./tab-navigation-and-parking.md) — the five-tab
  dock, back behavior, and the parking model routes rely on.
