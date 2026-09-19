# Open World

A per-server 2D space you walk around in: an avatar, click-to-walk movement,
presence bubbles for whoever else is there, and a channel bound to the place
you are standing in. The newest surface in the app, and the only one the shell
fixture cannot reach.

## Sub-features

- The **Open World** entry row in the sidebar, above the channel sections.
- The world canvas: avatar rendering, click-to-walk, camera follow.
- Presence: other occupants and their bubbles.
- The bound channel for a location, and its "Create a #world channel to talk
  here" empty state.
- Transport connect / retry, and the offline banner when it cannot reach the
  relay.

## How to get to it (user POV)

Under a server in the sidebar, above your channels, there is an **Open World**
row. You click it and the pane becomes a place rather than a list of messages —
your avatar standing in a room, other people's avatars where they are, and a
channel for talking to whoever is nearby.

## Driving it with control-om-chat

**Not through the shell fixture.** `?view=` has no `world` value, and the shell
fixture never stubs the world session port, so the sidebar row is inert there —
clicking it leaves the route on `#/room/ops` and mounts nothing. The surface
has its own harness:

```bash
export AGENT_BROWSER_SESSION=verify-world
agent-browser set viewport 1440 900
agent-browser open "$(./control-om-chat url \
  'mocks/world-solo/index.html?worldprobe=1')"
```

That mounts `WorldView` directly over a stub session port. **`#946` rebuilt
this surface** — the OpenScape 3D town and channel-chat alpha, then `#947`,
`#948` and `#953` on top — so the observations below replace the older ones.
Measured on lane 18120 at `ea0ee262`:

```bash
agent-browser eval '(()=>document.querySelectorAll("canvas").length)()'
#   2, not 0   (unchanged)
agent-browser eval '(()=>document.querySelector(".world-status")?.textContent.trim())()'
#   "world offline, retrying"
agent-browser eval '(()=>document.querySelector(".world-chat-connection")?.textContent.trim())()'
#   "Chat: reconnecting"
agent-browser eval '(()=>document.querySelector(".world-conversation")?.textContent.trim())()'
#   "ExpandHideNo #world channel"
```

**Do not reach for `.world-status-area` as the cheap second observation any
more.** The element still exists (`WorldView.tsx:739`) but it is filled through
a **ref**, imperatively, from the running renderer — so with the solo harness
offline it stays **empty**, and an assertion on `#west-bank-street` now fails
against a perfectly healthy rig. Use `.world-status` for liveness instead.

**`.world-chat` and `.world-chat-empty` are gone.** The string *"Create a
#world channel to talk here"* appears nowhere in the source; only an orphaned
`.world-chat-empty` rule survives in `world.css:203`, which is why a grep for
the class still finds something. The unbound state now reads **"No #world
channel"** inside `.world-conversation`, alongside its own **Expand** and
**Hide** controls, and the chat is an overlay (`.world-chat-overlay`) with a
separate connection line (`.world-chat-connection`).

New in the same rebuild, all present in the solo harness: a `.world-minimap`,
two `.world-view-control` buttons named **"Follow player"** and **"Enter
fullscreen"**, and four `.world-look` swatches — **Blue, Green, Amber,
Violet**.

## Gotchas

- **The solo harness has no transport.** It comes up reading *"world offline,
  retrying"*, *"Chat: reconnecting"* and *"No #world channel"*. That is the harness,
  not a regression — it proves rendering, layout, and the bound-channel empty
  state, and nothing about movement sync, presence, or the wire. Anything about
  two occupants seeing each other needs a real relay.
- **Two canvases, not one.** Assert `>= 1` or exactly 2; a `querySelector`
  written as if there were a single canvas will still pass while testing the
  wrong layer.
- **The world's real source root is `packages/chat-ui/src/world/`.** Both
  `src/world/WorldView.tsx` and `apps/cloud/src/world/WorldView.tsx` are
  one-line re-export shims, so `#946`'s stat showing a dozen `apps/cloud/src/
  world/*` files changed by one line each is the shims being written, not the
  feature. Read the 843-line file under `packages/chat-ui/`.
- The sidebar row is a `treeitem` inside its own `tree` named "Open World", not
  a button and not part of the `DESK` tree. `find role button` will not match
  it, and in the shell fixture matching it buys you nothing anyway.
- This file is the exception to the map's "three fixture entry points" table.
  If you are verifying a change that touches both the world and ordinary chat,
  you need two harnesses and two sets of frames.
