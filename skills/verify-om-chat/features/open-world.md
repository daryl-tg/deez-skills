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

That mounts `WorldView` directly over a stub session port. Observations that
tell you it actually came up, rather than rendering an empty shell:

```bash
agent-browser eval '(()=>document.querySelectorAll("canvas").length)()'
#   2, not 0
agent-browser eval '(()=>document.querySelector(".world-status-area")?.textContent)()'
#   "#west-bank-street"
agent-browser eval '(()=>document.querySelector(".world-chat-empty")?.textContent)()'
#   "Create a #world channel to talk here"
```

`#west-bank-street` is the cheap second observation, but be precise about what
it proves. It is **not a channel name**: it is the *area* label the HUD shows,
from `areaAt()` in rooms-client, rendered into `.world-status-area`. It proves
the world loaded a location — nothing about channel binding.

Channel binding is a separate element (`.world-chat`) and in this harness it is
always **unbound**: the stub hands `WorldView` a space whose `rooms` is empty,
so `findWorldRoom()` returns null and the empty state renders. Read
`.world-chat-empty` to prove that state deliberately, and never caption a frame
as if the area label showed a bound channel.

## Gotchas

- **The solo harness has no transport.** It comes up reading *"world offline,
  retrying"* and *"Create a #world channel to talk here"*. That is the harness,
  not a regression — it proves rendering, layout, and the bound-channel empty
  state, and nothing about movement sync, presence, or the wire. Anything about
  two occupants seeing each other needs a real relay.
- **Two canvases, not one.** Assert `>= 1` or exactly 2; a `querySelector`
  written as if there were a single canvas will still pass while testing the
  wrong layer.
- The sidebar row is a `treeitem` inside its own `tree` named "Open World", not
  a button and not part of the `DESK` tree. `find role button` will not match
  it, and in the shell fixture matching it buys you nothing anyway.
- This file is the exception to the map's "three fixture entry points" table.
  If you are verifying a change that touches both the world and ordinary chat,
  you need two harnesses and two sets of frames.
