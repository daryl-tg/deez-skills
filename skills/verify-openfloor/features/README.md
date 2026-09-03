# OpenFloor verification map

The maintained source for verifying user-facing behavior on the OpenFloor iOS
simulator lane. Read this index before driving, then use the matching feature
file as the recipe.

Handles below were read off a live simulator on **2026-09-03** (iPhone 17 Pro,
iOS 26.5, `sh.openmarket.openfloor`, Metro on 8081, app at `f2c3f88`).

## Baseline preconditions

- Metro is up on its **assigned** port `8081`, bundling *this* checkout.
  `pnpm start` if it is not.
- `./control-openfloor doctor` exits zero and reports the working tree, a booted
  simulator, and the app installed.
- `./control-openfloor app open` returns a snapshot containing
  `[other] "Primary navigation"` — that is the app shell, not the dev launcher.
- **The dev-client Tools button is off.** If the snapshot contains
  `[other] "gearshape.fill"`, the floating gear is on and it swallows taps in
  the top-right of the Chats header — `Filter chats` opens the Expo dev menu
  instead of the drawer. Turn it off once per simulator: open the dev menu
  (Cmd+D in the Simulator, or press the gear), scroll to **Tools button**, and
  switch it off. It stays off across launches.
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
  Use `find "<stable substring>"` — but remember `find` matches by *contains*,
  so a short word can hit body copy on another part of the screen.
- **Prefer `~sN`-pinned refs from a `--settle` diff over bare `@eN`.** Each
  `./control-openfloor device …` invocation is its own `agent-device` call, so a
  ref read in one shell command can be stale in the next and press whatever now
  sits at those coordinates.
- **A wrapped header back control matches twice.** `Back`, `Back to chats`,
  `Back to settings`, `Back to server` and `Appearance` each match an `[other]`
  and a `[button]`; a bare press fails with `AMBIGUOUS_MATCH`. Qualify with
  `role=button`.
- **Only the tab roots and the server screen show the dock.** Everywhere else
  the selected-tab press is unavailable — use the screen's own back control.
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

## Known gaps in this map

Named so nobody mistakes silence for coverage. Each is a real user-facing
surface with no entry of its own yet:

- **Channel tools and topic tooling** are documented as handle tables inside
  [conversation-and-composer](./conversation-and-composer.md) rather than as
  their own entries. The topic surfaces from commit `72b6e89` (topic search
  across channels, moving messages into a topic, topic peek) have confirmed
  handles and no recipe.
- **Conversation details and member profiles** (`convo-details`,
  `convo-profile`) have handles confirmed live but neither screen has been
  opened, so nothing behind those labels is verified.
- **Friends, Apps, Follows, Help, Chat notifications, Profile, Advanced,
  invites, and the new-group / new-server / connections flows** are reachable
  from mapped screens and unmapped themselves.

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
- [Discover and public rooms](./discover-public-rooms.md) — the third dock tab:
  the public-room directory, its search, and joined rooms.
- [Your Library and to-dos](./your-library-and-todos.md) — the fourth dock tab:
  personal notes and folders, shared documents, open to-dos.
- [Alerts](./alerts.md) — the Chats header beacon, the alerts board, and a
  feed's trigger history.
- [Activity and requests](./activity-and-requests.md) — the notifications bell:
  mentions, replies, and friend requests.
