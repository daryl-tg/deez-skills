# Servers and channels

The Servers tab lists the spaces the account belongs to, each row showing an
avatar monogram, an unread count, the server name and a channel count. Opening
one shows that server's channel tree grouped by category, with a topics control
beside each channel and the server's Library above them.

## Sub-features

- `servers-grid` lists joined servers.
- `servers-search` filters that list (network-backed).
- `server-channels` shows the channel tree, grouped and unread-first.
- `server-topics` toggles a channel's topic list.
- `server-library` opens the server's shared-document destination.
- `server-manage` opens role and permission management.

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
| `label="channel <name>, muted"` | a muted channel |
| `label="Show <roomId> topics"` | that channel's topics toggle |

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
  it.
- **Open the Library.** Run
  `./control-openfloor device press 'label="Open OpenMarket Library"' --settle`.
- **Return to the server list.** Press the already-selected tab:
  `./control-openfloor device press 'label="Servers"' --settle`. `agent-device
  back` does **not** work on this screen.
- **Proof.** The `--settle` diff plus
  `./control-openfloor device screenshot --out "$PWD/artifacts/<run>/<rev>/channels.png" --normalize-status-bar`.

## Gotchas

- **Opening a channel in a large server can collapse the accessibility tree.**
  In OpenMarket (23 visible channels) the press produced *"Detected an overly
  complex or slow accessibility tree. Fell back to the private-ax snapshot
  backend"* and a 2-node snapshot. While collapsed **every selector fails** with
  `Selector did not match`, including ones that resolved a second earlier.
  Recover with `./control-openfloor app open`, not by retrying. If the claim is
  really about the conversation surface, drive it through a DM instead
  ([conversation-and-composer](./conversation-and-composer.md)) and record the
  substitution as a delta.
- **The server screen's back control has no accessible label** — it appears as a
  bare `[button]` with an empty name, and `agent-device back` fails with *"in-app
  back control is not available"*. Use the selected-tab press.
- **The row's channel count and the screen's header disagree.** The row read
  `OpenMarket, 30 channels` while the screen read `23 CHANNELS`. Do not assert
  either number as the other's value.
- **Server search is network-backed and fails live.** Typing into
  `label="Search servers"` produced *"OpenMarket authentication is temporarily
  unreachable"* and hung on *"Loading OpenMarket servers…"*. Prefer the cached
  list. If search is the point of the proof, `wait text` for a result and report
  the failure rather than photographing the spinner.
- **Home is the only write-safe server, and it currently has no channels** — the
  screen reads *"This server has no visible channels."* Nothing in this file
  makes a production channel writable; posting elsewhere is the operator's call,
  and so is `Manage <server>` even in Home.
