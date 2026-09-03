# Conversation and composer

The conversation surface is shared by DMs and server channels: a scrolling
transcript of avatar-led message rows with reaction chips, a header carrying the
counterpart's name, presence and a call control, and a rounded composer with an
attachment menu, an emoji picker and a send button that stays disabled until
there is something to send.

## Sub-features

- `convo-transcript` renders message rows and day separators.
- `convo-history` loads older messages.
- `convo-reactions` shows existing reactions and adds one.
- `convo-profile` opens a member's profile from their avatar.
- `convo-details` opens conversation details.
- `composer-typing` enables send once text exists.
- `composer-attach` opens the attachment menu.
- `composer-emoji` opens the emoji picker.

## How to get to it (user POV)

- Tap a DM row in the Chats inbox.
- Or tap a channel inside a server.

## Driving it with control-openfloor

Preconditions:

- `./control-openfloor doctor` exits zero, start from the Chats root.
- **Read-only unless the room is Home.** Every other room is production.

Stable handles (read off a DM):

| Handle | What it is |
|---|---|
| `label="Back"` | back to the inbox (present here, unlike the server screen) |
| `label="Open conversation details for <name>, Offline"` | header; **presence is in the label** |
| `label="Call <name>"` | call control |
| `label="Load older messages"` | history control at the top of the transcript |
| `label="Open profile for <name>"` | an avatar |
| `label="Message from <name>"` | a message row |
| `label="Add 🤯 reaction"` | an existing reaction chip |
| `label="Open attachment menu"` | composer attachment control |
| `label="Direct message Message <name>"` | the composer, a `[text-view]` |
| `label="Open emoji picker"` | composer emoji control |
| `label="Send direct message"` | send; `[disabled]` while the composer is empty |

- **Open a DM.** From the Chats root run
  `./control-openfloor device find "geraldlee"`. The settled state carries
  `label="Back"` and `label="Send direct message"`.
- **Verify the composer's resting state.** Run
  `./control-openfloor device is 'label="Send direct message"' --disabled` (or
  read `[disabled]` off `snapshot -i`). An empty composer must not offer send.
- **Read the transcript.** Rows are `Message from <name>`; day separators appear
  as `[cell] "Yesterday"`. Assert the row, not a fixed index — the transcript
  virtualizes.
- **Load history.** Run
  `./control-openfloor device press 'label="Load older messages"' --settle` and
  assert new `Message from …` rows in the diff.
- **Open the attachment menu.** Run
  `./control-openfloor device press 'label="Open attachment menu"' --settle`.
  Opening it is free; picking a file that would send is not.
- **Sending.** Only in Home, and **Home has no visible channels right now**, so
  this is currently unreachable. When it is reachable the shape is:
  `fill 'label="Message #general"' "probe one" --settle`, assert
  `label="Send direct message"` (or its channel equivalent) is no longer
  `[disabled]`, press it, then assert the new row in the transcript and confirm
  it survives `./control-openfloor app reset`. Until then, report send as a
  delta with the attempted command and the unmet precondition.
- **Proof.** The `--settle` diff for the action plus
  `./control-openfloor device screenshot --out "$PWD/artifacts/<run>/<rev>/convo.png" --normalize-status-bar`.

## Gotchas

- **Reach this surface through a DM when you can.** DM transcripts produce rich,
  healthy accessibility trees (46 nodes on a normal conversation). The
  server-channel route into the same surface collapsed the AX tree to 2 nodes in
  a large server; see [servers-and-channels](./servers-and-channels.md). If you
  proved the surface through a DM because the channel route collapsed, that is a
  delta — the channel entry point is not verified by it.
- **Presence is baked into the details label.** `Open conversation details for
  geraldlee, Offline` becomes a different string when they come online. Match on
  `Open conversation details for <name>` with `find`, not the full label.
- **The composer is a `[text-view]`, not a `[text-field]`,** and its label
  repeats the word Message (`"Direct message Message geraldlee"`). Copy it
  exactly.
- **Reaction chips carry the emoji in the label** (`Add 🤯 reaction`). They vary
  per message; read them from a snapshot rather than assuming a set.
- Avatar and row are separate targets with different labels
  (`Open profile for daryl` vs `Message from daryl`) and both appear per row.
  Pressing the avatar navigates away from the transcript.
- Never clear the composer with the keyboard `delete` key — it dispatches onto
  the `v` key. `fill … ""` is rejected outright.
