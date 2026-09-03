# Servers and channels

The Servers tab lists the spaces the account belongs to, each row showing an
avatar monogram, an unread count, the server name and a channel count. Opening
one shows that server's channel tree grouped by category, with a topics control
beside each channel and the server's Library above them.

## Sub-features

- `servers-grid` lists joined servers.
- `servers-search` filters that list (network-backed).
- `server-channels` shows the channel tree, grouped by category in the server's
  own arrangement — **not unread-first**.
- `server-topics` toggles a channel's topic list.
- `server-library` opens the server's shared-document destination.
- `server-manage` opens role and permission management.
- `server-mute` mutes a channel from a long-press on its row — **a production
  write; read the muted state, do not toggle it**.

## How to get to it (user POV)

- Tap **Servers** in the bottom dock.
- Tap a server row to see its channels.
- Tap a channel to open its conversation.

## Driving it with control-openfloor

Preconditions:

- `./control-openfloor doctor` exits zero.
- Start from the Chats root (`./control-openfloor app open`).

Stable handles:

| Handle | What it is |
|---|---|
| `label="Search servers"` | server search field |
| `label="Add a server"` | create/join control |
| `label="HO, Home, 0 channels"` | a server row: `"<monogram>, <name>, <n> channels"`, prefixed by unread count when non-zero |
| `label="Manage <server>"` | roles and permissions |
| `label="Open <server> Library"` | the server's Library |
| `label="channel <name>"` | a channel row, e.g. `label="channel random-riffs"` |
| `label="Show <roomId> topics"` / `label="Hide <roomId> topics"` | that channel's topics toggle, by current state |
| `label="Muted"` | the bell-off mark inside a muted row |

A channel row's label is a **composite that grows with live state**, joined by
`, ` in this order:

```
channel <name>[, <n> unread mentions][, unread][, <n> unread in topics][, <n> open topics][, muted]
```

`channel testing-123345556` and `channel go-tasks, unread` were both read off
the same tree on 2026-09-03; the count-bearing segments come from the source's
own label builder. **Never exact-match a channel row** — three of those segments
carry counts that drift. `find "channel go-tasks"` is the safe form.

- **Open the tab.** Run
  `./control-openfloor device press 'label="Servers"' --settle`. The settled
  diff shows `label="Search servers"` and the server rows.
- **Open a server.** Match on the stable part:
  `./control-openfloor device find "Home"` or
  `./control-openfloor device find "OpenMarket, 30 channels"`. The screen
  becomes the channel tree; the header reads `<n> CHANNELS` and
  `label="Manage <server>"` appears.
- **Open a channel.** Run
  `./control-openfloor device press 'label="channel random-riffs"' --settle`,
  then verify with `./control-openfloor device wait text "random-riffs"`. See
  the AX-collapse gotcha below before building a proof on this step.
- **Toggle topics.** Run
  `./control-openfloor device press 'label="Show b088135760c3 topics"' --settle`.
  The room id in that label is the stable half; the channel name is not part of
  it. Re-verified 2026-09-03 — and worth stating because the source reads
  `` `Show ${room.name} topics` ``, where `room.name` **is** the room id, not the
  display name. Reading that line without knowing so suggests the opposite.
  The settled diff flips the label to `Hide <roomId> topics` and opens a panel
  in one of four states: rows, `Loading topics…`, `No open topics`, or
  `Topics unavailable · tap to retry`.
- **Open the Library.** Run
  `./control-openfloor device press 'label="Open OpenMarket Library"' --settle`.
  The screen carries `label="Back to server"` (**ambiguous — needs
  `role=button`**), `label="+ New"`, `label="Search server Library"`,
  `label="Add documents to this Library"`, `label="Open archive"`, and
  `label="Expand <folder>"` rows over a `DOCUMENTS` section. This is the
  *space's* library; the account's own is
  [your-library-and-todos](./your-library-and-todos.md).
- **Return to the server list.** Press the already-selected tab:
  `./control-openfloor device press 'label="Servers"' --settle`. `agent-device
  back` does **not** work on this screen.
- **Proof.** The `--settle` diff plus
  `./control-openfloor device screenshot --out "$PWD/artifacts/<run>/<rev>/channels.png" --normalize-status-bar`.

## Gotchas

- **The accessibility tree can collapse, but not where this file used to say.**
  Opening `channel random-riffs` from the OpenMarket tree (25 visible channels)
  on 2026-09-03 produced a **rich, healthy tree** — messages, reaction chips,
  link previews, composer — so the old "expect a 2-node snapshot in a large
  server" claim did not reproduce and is no longer the default expectation.
  Collapse is real but intermittent, and this session met it elsewhere: a
  1-node snapshot with *"No snapshot backend could read this screen"* after
  driving the emoji picker. Two things to know when it happens:
  **every selector fails** with `Selector did not match`, and **`app open` does
  not recover it** — it cannot even find the shell and dies with *"app shell
  never appeared"*. `./control-openfloor app reset` does. If you end up proving
  the conversation surface through a DM instead
  ([conversation-and-composer](./conversation-and-composer.md)), that is a
  delta: the channel entry point is not verified by it.
- **The server screen's back control has no accessible label** — it appears as a
  bare `[button]` with an empty name, and `agent-device back` fails with *"in-app
  back control is not available"*. Use the selected-tab press: the server screen
  is one of the few pushed routes that **keeps** the dock. This is a product
  accessibility gap, reported to the operator, not something to work around
  quietly: a screen-reader user gets an unnamed button.
- **The row's channel count and the screen's header disagree, and here is why.**
  The grid tile counts `item.rooms.length` — every room in the space — while the
  channel-tree header counts `visibleChannels.length`, which drops alert-home
  channels via `alertHomeHiddenFor`. So the row is "all rooms" and the header is
  "channels you can see". On 2026-09-03 that read `OpenMarket, 32 channels` over
  `25 CHANNELS` (30 vs 23 the day before — the numbers move, the gap does not).
  Never assert either as the other's value.
- **Long-pressing a channel row opens the attention drawer.** The row carries
  `accessibilityHint="Long-press to mute this channel"` and its `onLongPress`
  opens `AttentionDrawer`, where picking a level calls
  `mutes.setChannelAttention` — a production write. Opening the drawer is a
  read; choosing in it is not, and it is the operator's call, the same posture
  as `server-manage`. Use `press` on channels so you never open it by accident.
- **Server search is local and instant — the old "network-backed" warning was a
  misattribution.** `filteredServers` in `src/rooms/rooms-screen.tsx` is a pure
  client-side `.filter()` over the already-loaded servers, matching a server's
  name or any of its room titles; typing makes no request. The
  *"OpenMarket authentication is temporarily unreachable"* string lives in
  `src/auth/auth-backend.ts` and is an auth failure, and
  *"Loading OpenMarket servers…"* is gated on the initial directory fetch
  (`directoryStatus === 'loading' && servers.length === 0`). An earlier run
  caught a directory hiccup while also touching search and blamed the field. If
  you want to prove the loading or error state, drive it right after `app open`
  while the directory is still fetching — not by typing.
- **Home is the only write-safe server, and it still has no channels.**
  Re-checked 2026-09-03: the row reads `HO, Home, 0 channels` and the screen
  reads *"This server has no visible channels."* Nothing in this file makes a
  production channel writable; posting elsewhere is the operator's call, and so
  is `Manage <server>` even in Home. `server-manage` therefore has a confirmed
  handle and no verified screen behind it.
