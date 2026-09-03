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
- `composer-attach` opens the attachment menu (Gallery / Camera / File / Poll).
- `composer-emoji` opens the emoji picker.
- `composer-autocomplete` offers mentions, emoji shortcodes, channel and topic
  references, and slash/app commands as you type.
- `composer-reply` shows and cancels a staged reply.
- `convo-tools` opens Channel tools — the channel's own toolbar.
- `convo-topics` opens the channel's topic list and search.
- `convo-call` shows the call strip and its join control.
- `convo-actions` opens a message's action sheet from a long press.

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
| `label="Add 🤯 reaction"` / `label="Remove 🤯 reaction"` | an existing reaction chip; **`Remove` when the reaction is yours** |
| `label="Open profile for <name>, author"` | the author line, distinct from the avatar |
| `label="Pinned"` | the pin mark on a pinned row |
| `label="Open link preview <title>"` | an unfurl card, a `[link]` |
| `label="Cancel direct message reply"` | dismiss a staged reply (channel twin: `Cancel room reply`) |
| `label="Mention <handle>"`, `label="Insert <glyph> <shortcode>"`, `label="Topic <label>"`, `label="Channel <label>"` | composer autocomplete rows |
| `label="Open attachment menu"` | composer attachment control |
| `label="Direct message Message <name>"` | the composer, a `[text-view]` |
| `label="Open emoji picker"` | composer emoji control |
| `label="Send direct message"` | send; `[disabled]` while the composer is empty |

The **channel** twin of this surface has its own names — do not reuse the DM
ones:

| Handle | What it is |
|---|---|
| `label="Back"` | back to the server tree |
| `label="Open details for channel <name> in server <server>"` | header |
| `label="Join channel voice"` | the voice control |
| `label="Channel tools"` | the channel's toolbar sheet |
| `label="Jump to the first unread message"` | the unread jump |
| `label="New messages below"` | the unread divider |
| `label="Message Message this room"` | the composer, a `[text-view]` |
| `label="Send message"` | send; `[disabled]` while empty |
| `label="Slash command <name>. <description>"` | a slash-command row |
| `label="App command <name> via <hint>. <description>"` | an app-command row |

Channel message rows have **no authored accessible name** — iOS synthesises one
from the visible text, so a row reads
`"<author>[, APP], <Today at 11:47 AM>, <the entire body>"`. That is why the DM
recipe's `Message from <name>` does not match in a channel.

Behind `label="Channel tools"`, all read off a live sheet on 2026-09-03:
`Close channel tools`, `To-dos`, `Members`, `Pins`, `Saved`, `Search`,
`Library`, `Convert to alerts…`, `Topics`, `Copy channel link`,
`Copy channel ID`. Behind its `Topics`, also live: `Close topics`, `View all`,
`Search topics`, `Channel stream, MESSAGES WITHOUT A TOPIC`, and the empty
states `No topics in this room yet.` / `No topics in this channel yet.`

The rest of the topic tooling from commit `72b6e89` is **read from source and
not yet confirmed live**, because the channel driven had no topics to act on:
`New topic name`, `Rename topic`, `In topic <name>. Switch topic`,
`Open topic <name> in another channel`,
`Load more topic matches from other channels`, and
`Peek topic <id>` / `Collapse topic <id>`. Treat those as hints, not handles,
until a channel with topics has been driven.

- **Open a DM.** From the Chats root run
  `./control-openfloor device find "geraldlee"`, then
  `./control-openfloor device wait 'label="Call geraldlee"'` — the transcript
  arrives after a `Loading direct messages…` state. Only then does the tree
  carry `label="Back"` and `label="Send direct message"`.

  Do this on a **hydrated** inbox. Run straight after `app reset`, `find` on a
  still-loading list matched nothing useful and tapped the dock instead, landing
  on Discover. Wait for the row (`wait text "geraldlee"`) before pressing it.
- **Verify the composer's resting state.** Read `[disabled]` off
  `./control-openfloor device snapshot -i`. An empty composer must not offer
  send. There is **no** `--disabled` flag and no `enabled`/`disabled`
  predicate — `is` takes only
  `visible|hidden|exists|editable|selected|focused|text`, so
  `is 'label="Send direct message"' --disabled` fails with `INVALID_ARGS`.
- **Read the transcript.** Rows are `Message from <name>`; day separators appear
  as `[cell] "Yesterday"`. Assert the row, not a fixed index — the transcript
  virtualizes.
- **Load history.** Run
  `./control-openfloor device press 'label="Load older messages"' --settle` and
  assert new `Message from …` rows in the diff.
- **Open the attachment menu.** Run
  `./control-openfloor device press 'label="Open attachment menu"' --settle`.
  The diff adds `Gallery`, `Camera`, `File`, `Poll` and
  `Close attachment menu`. Opening it is free; picking a file that would send is
  not.
- **Open Channel tools.** Run
  `./control-openfloor device press 'label="Channel tools"' --settle`, then
  `press 'role=button label="Topics"'` for the topic list. Both are read-only to
  open. Leave with `Close channel tools` / `Close topics`.
- **Prove `composer-typing` without sending.** Fill the composer, assert send
  is no longer `[disabled]`, then clear it. Verified 2026-09-03 in OpenMarket's
  empty `testing-123345556` channel:

  ```
  ./control-openfloor device snapshot -i               # take the [text-view] ref
  ./control-openfloor device fill '@e10' "probe" --settle
  ./control-openfloor device snapshot -i               # "Send message" no longer [disabled]
  ./control-openfloor device type $'\b\b\b\b\b'     # one backspace per character
  ./control-openfloor device snapshot -i               # [disabled] again, no draft left
  ```

  Prefer a channel whose transcript reads `No messages in this room yet.` so a
  stray draft cannot be mistaken for a real one.
- **Sending.** Only in Home, and **Home still has no visible channels**
  (re-checked 2026-09-03), so a real send remains unreachable in this lane.
  When it is reachable the shape is: fill the composer, assert send is enabled,
  press it, assert the new row in the transcript, and confirm it survives
  `./control-openfloor app reset`. Until then, report send as a delta with the
  attempted command and the unmet precondition — and note that
  `composer-typing` is proven while `send` is not.
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
- **`fill` by the composer's label silently does nothing.** The label matches an
  `[other]` wrapper before it matches the `[text-view]`, and the fill reports
  success while the field stays empty and send stays `[disabled]`. **Fill the
  `[text-view]`'s own ref**, taken from `snapshot -i`.
- **The composer is a `[text-view]`, not a `[text-field]`,** and its accessible
  name is its own label plus its placeholder: `"Direct message Message
  geraldlee"` in a DM, `"Message Message this room"` in a channel. Once it has
  text the wrapper drops to `"Direct message"` / `"Message"` and the text-view
  reads the content. Copy the empty-state form exactly, and re-read it after
  typing.
- **The composer has unavailable states with their own names.** While a DM is
  reconnecting it reads `"Direct message Reconnect before composing"` and
  `Send direct message` is **absent entirely**, not disabled. Wait for
  `label="Call <name>"` or `Load older messages` before asserting composer
  state.
- **Reaction chips carry the emoji in the label** (`Add 🤯 reaction`). They vary
  per message; read them from a snapshot rather than assuming a set.
- Avatar and row are separate targets with different labels
  (`Open profile for daryl` vs `Message from daryl`) and both appear per row.
  Pressing the avatar navigates away from the transcript.
- **Clear the composer with `device type $'\b'`, one per character.** Verified
  2026-09-03. Do **not** press the on-screen keyboard's `delete` key —
  `press 'label="delete"'` dispatches onto the `v` key instead. `fill … ""` is
  still rejected outright.
- **Long-pressing a message row opens its action sheet** (`onLongPress` →
  `onActions`), which is one step from a reaction or a deletion. Use `press`,
  and treat `convo-actions` as read-only-to-open.
- **The emoji picker's rows are shortcodes, not glyphs** (`heart`, `heart_eyes`),
  and this session met an AX-tree collapse right after driving it — a 1-node
  snapshot with *"No snapshot backend could read this screen"*, recovered only
  by `app reset`. Open it, snapshot it, and leave by resetting rather than by
  toggling it closed.
- Every DM handle in this file re-verified live 2026-09-03 on `f2c3f88`; the channel handles were read the same day.
