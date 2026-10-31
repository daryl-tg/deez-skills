# Open World

A per-server 2D space you walk around in: an avatar, click-to-walk movement,
presence bubbles for whoever else is there, and a channel bound to the place
you are standing in. The newest surface in the app, and the only one the shell
fixture cannot reach.

## Sub-features

- The **Open World** entry row in the sidebar, above the channel sections.
- The world canvas: avatar rendering, click-to-walk, camera follow.
- Presence: other occupants and their bubbles.
- Agent activity visualization: agent avatars can read, write, or search with
  the shared book controller. `tools/openscape-preview/activity.html` exercises
  scripted renderer states; authenticated activity still needs live observations.
- The bound channel for a location, including the "No #world channel" state.
- The chat pane and HUD: **Hide** / **Open chat**, the channel nav, the
  composer and its delivery ladder (pending → confirmed, failed → **Retry** /
  **Discard**), **Earlier messages**, the pane resize handle, nameplates with
  role titles, the emote wheel, and the camera controls. Driveable only in
  `tools/openscape-preview/` (see below); the solo harness shows the shell of
  the pane with no occupants.
- The unavailable-world refusal when there is no connected daemon: show
  "Open World requires a connected daemon" and leave the canvas unmounted
  (`WorldView.tsx:158,289-297,709-714`).
- Transport connect / retry, and the offline banner when it cannot reach the
  relay.
- A resizable channel column beside the world (`#948`): a handle
  `[data-world-channel-resize]` (`WorldChatPane.tsx:343-374`) that drags,
  moves with the arrow keys, and resets on Home or double-click. Width is
  76–280px and persists to `localStorage` key `om.chat.world.channelWidth`
  (`channelWidth.ts`). It is present in `mocks/world-solo/index.html?worldprobe=1`
  (measured at `f7d7c987`).
- A **"Open World chat"** group in Settings → Appearance with a **"Chat pane
  font size"** range, 12–24px (`WorldChatPreferences.tsx`), mounted only for a
  home session (`Shell.tsx:4550`; lazy import at `:245`). Reach it through
  `shell-fixture.html?view=settings&settingsPage=appearance`, not
  `settings-fixture.html`; see
  [settings-and-appearance.md](settings-and-appearance.md).

## How to get to it (user POV)

Under a server in the sidebar, above your channels, there is an **Open World**
row. You click it and the pane becomes a place rather than a list of messages —
your avatar standing in a room, other people's avatars where they are, and a
channel for talking to whoever is nearby.

## Driving it with a standalone source Vite lane

**Not through the shell fixture.** `?view=` has no `world` value, and the shell
fixture never stubs the world session port, so the sidebar row is inert there.
Clicking it leaves the route on `#/room/ops` and mounts nothing.

The wrapper lane serves the solo harness directly. At `afabb11c`,
`agent-browser open "$(control-om-chat url 'mocks/world-solo/index.html?worldprobe=1')"`
rendered it with no invalid-hook error, even after that lane had served a dozen
other fixtures. An earlier pass (`cd9f8c72`) hit a React invalid-hook error in
`WorldCanvas` on the wrapper lane. If `agent-browser console` shows one, fall
back to a fresh standalone root Vite process. From the product repo root, use
a free assigned port in the 18097–18197 range and preflight it. The example
below uses 18102:

```bash
world_port=18102
bun x vite --port "$world_port" --strictPort --host 127.0.0.1
```

Then open the standalone fixture in the browser:

```bash
export AGENT_BROWSER_SESSION=verify-world
agent-browser set viewport 1440 900
agent-browser open "http://127.0.0.1:${world_port}/rooms/mocks/world-solo/index.html?worldprobe=1"
```

That mounts `WorldView` directly over a stub session port. **`#946` rebuilt
this surface** — the OpenScape 3D town and channel-chat alpha, then `#947`,
`#948` and `#953` on top — so the observations below replace the older ones.
Re-driven on the source fixture at product commit `f8b68bf7`:

```bash
agent-browser eval '(()=>document.querySelectorAll("canvas").length)()'
#   2, not 0   (unchanged)
agent-browser eval '(()=>document.querySelector(".world-status")?.textContent.trim())()'
#   "world offline, retrying"
agent-browser eval '(()=>document.querySelector(".world-chat-connection")?.textContent.trim())()'
#   "Chat: reconnecting"
agent-browser eval '(()=>document.querySelector(".world-conversation")?.textContent.trim())()'
#   "HideNo #world channel"
```

**Do not reach for `.world-status-area` as the cheap second observation any
more.** The element still exists (`WorldView.tsx:818`) but it is filled through
a **ref**, imperatively, from the running renderer — so with the solo harness
offline it stays **empty**, and an assertion on `#west-bank-street` now fails
against a perfectly healthy rig. Use `.world-status` for liveness instead.

**`.world-chat` and `.world-chat-empty` are gone.** The string *"Create a
#world channel to talk here"* appears nowhere in the source; only an orphaned
`.world-chat-empty` rule survives in `world.css:213`, which is why a grep for
the class still finds something. The unbound state now reads **"No #world
channel"** inside `.world-conversation`, beside a **Hide** control — `#960`
removed its Expand button as redundant, so a recipe that clicks Expand now
finds nothing — and the chat is an overlay (`.world-chat-overlay`) with a
separate connection line (`.world-chat-connection`).

New in the same rebuild, all present in the solo harness: a `.world-minimap`,
two `.world-view-control` buttons named **"Follow player"** and **"Enter
fullscreen"**, and five `.world-look` swatches — **Wayfarer, Ranger,
Surveyor, Violet, Rust** (`packages/chat-ui/src/world/scene/characterModel.ts`, Wayfarer at `:11`).

**Hide** collapses the chat pane and the control then reads **Open chat**
(`WorldChatPane.tsx:400`); **Enter fullscreen** reads **Exit fullscreen** only
once the browser grants fullscreen, which the headless lane did not
(2026-10-31). Open the harness under the lane's `/rooms/` base, as
`control-om-chat url` does: a bare `/mocks/world-solo/index.html` answers with
vite's base-URL notice ("did you mean to visit /rooms/mocks/…") and no canvas,
and a smoke that reads only the HTTP status calls that a mount.

The shared renderer's scripted Agent activity study is a second local harness:
run `bun x vite --config tools/openscape-preview/vite.config.ts --port <assigned-free-port> --strictPort --host 127.0.0.1`, then open
`http://127.0.0.1:<assigned-free-port>/rooms/tools/openscape-preview/activity.html`.
Select a scenario and inspect `window.__activityPreview.sample()` or seek with
the Timeline. This preview uses scripted observations; it does not prove that
live agent cues arrive over the world transport.

`#970` and `#974` also added nameplates — `.world-nameplate` with a role-derived
title and `data-kind` marking agents — but they draw over *occupants*, and the
solo harness has none, so it renders zero nameplates. That is the harness, as
below: proving them needs the relay and a second occupant.

### The chat pane and HUD in `tools/openscape-preview/` (added 2026-11-01)

The solo walk harness above has no occupants and no transport, so it never
shows the chat pane doing anything. `tools/openscape-preview/` does: it mounts
`WorldCanvas`, `WorldSim` and `WorldChatPane` over local fixtures with 32
occupants, five seeded rows and a scripted delivery ladder. It is a separate
Vite config whose server block pins **port 8098, the review renderer's port**
(`tools/openscape-preview/vite.config.ts:38`), so always pass a port:

```bash
world_port=18139                                   # a free agent slot, preflighted
bun x vite --config tools/openscape-preview/vite.config.ts \
  --host 127.0.0.1 --port "$world_port" --strictPort
# base is already /rooms/; / and /rooms/ 302 to the harness, keeping the query
agent-browser open "http://127.0.0.1:${world_port}/rooms/tools/openscape-preview/index.html?worldprobe=1"
```

It runs only under the dev server (`entry.tsx` throws outside `import.meta.env.DEV`),
needs no daemon and no `@cli/*`, and `?worldprobe=1` exposes `window.__omWorld3D`
(`characters()`, `camera()`, `project()`, `render()`, `roofs()`;
`packages/chat-ui/src/world/WorldCanvas.tsx:207-249`). Wait for
`[data-world-renderer][data-world-ready="true"]`; headless Chromium renders the
WebGL town here, and `characters().length` reads 32 (driven 2026-11-01 at `936f5b64`).

**Harness controls** (section **Preview scenarios**): selects **Reading crowd**,
**Character look**, **Movement mode** and **Preview state**; toggles **Preview
titles** and **Role colors** (`aria-pressed`); buttons **Toggle Rowan agent
snapshot**, **Nearby / Shared / Roof / Distant speech** and **Confirm locally**.
Drive the selects with `agent-browser select 'select[aria-label="Preview state"]'
<value>`, not `find role combobox` (which has no `select` action). The
**Preview state** values and what each does to the pane's `role="status"` line:
`conversation` (default, **History loaded**), `channels` (80 channels,
`#world` plus `#channel-1` to `#channel-79`), `delivery` (one **Awaiting
confirmation** row and one **Not sent** row with **Retry** and **Discard**),
`loading` (**Loading history**), `error` (**History unavailable**), `offline`
(**Showing saved history**), `empty` (**No messages yet.**), `missing` (**No
#world channel**, no composer) and `readonly` (the textarea is `disabled`).
Every status line ends in the `<strong>` **Simulated chat**.

**The pane** is `section.world-conversation[aria-label="#world conversation"]`:

- **Hide** collapses it (class `is-collapsed`, `aria-expanded="false"`, the
  `role="log"` and the resize handle unmount) and the control reads **Open
  chat**; clicking that restores both.
- The composer is `textarea[data-testid="world-chat-input"]` named **Message
  #world** (`maxLength` 200), with a **Send** button (`title` **Send
  message**) that is disabled while the draft is empty. Enter sends. A send
  appends `article.world-conversation-message[data-delivery="pending"]`
  reading **Awaiting confirmation** under `You:`, clears the draft and disables
  Send again; the harness's **Confirm locally** flips it to
  `data-delivery="confirmed"` and raises a `.world-speech[data-speaker="solo"]`
  bubble with the same text over the player's nameplate.
- **Earlier messages** appends 18 older rows after about 500 ms (5 → 24).
- `nav[aria-label="OpenMarket chat channels"]` holds one
  `button.world-conversation-channel` per channel with `aria-current="page"` on
  the selected one. Under the `channels` state, clicking **#channel-2** moves
  `aria-current`, renames the section **#channel-2 conversation**, the log
  **#channel-2 message history** and the composer **Message #channel-2**; the
  rows do not change, because the harness shares one row list.
- The pane resizes from `button.world-chat-resize` (**Resize chat**, `title`
  **Drag to resize · Arrow keys adjust size · Home or double-click resets**).
  Arrow keys move 16 px: two **ArrowUp** presses wrote
  `--world-chat-width: 420px; --world-chat-height: 212px` on the section and
  `om.chat.world.paneSize` `{"width":420,"height":212}`; **Home** cleared both.
  The channel-column divider is the `role="separator"` **Resize the channel
  list** from the solo harness; at 1440×900 it reads `aria-valuenow` 96 with
  `aria-valuemin` 76 and `aria-valuemax` **238** (the 280 constant is clamped
  by the pane's width).
- Under `delivery`, **Retry** moves the failed row to `data-delivery="retrying"`
  (**Retrying**) and **Discard** removes it.

**Nameplates and titles.** All 32 `span.world-nameplate[data-player][data-kind]`
render here: `solo` is **Town_Visitor** with the subtitle **Builder**, the two
agents are `data-kind="agent"` with the six-hex name (**aaaaaa**, **bbbbbb**),
the owner as subtitle and a `.world-agent-marker` whose screen-reader text is
**Agent**. **Preview titles** adds **Blacksmith** under Rowan and **Echelon IX**
under agent `bbbbbb`.

**Emote wheel.** It arms in this harness because the sim is "connected". Focus
`.world-renderer` (`tabIndex` 0), dispatch `keydown` `{key:"e", code:"KeyE"}`
on it, and `div.world-emote-wheel[role="dialog"][aria-modal="true"][aria-label="Emotes"]`
opens with `.world-emote-choice` buttons **Read**, **Write**, **Search**,
**Greet** and **Sit** and the help line **Release E or click to select · Center
to cancel**. Click the option's `.world-emote-label` while E is still "held",
then dispatch `keyup` E on `document` or `window`: the wheel closes,
`__omWorld3D.characters()` shows `solo` with `emote: "read"` and
`animation.bookVisible`, and the next wheel lists a sixth option, **Stop**.
Escape closes an open wheel. Typing E into the composer does nothing, by design.

**Camera and look.** `button[aria-label="Follow player"]` toggles
`aria-pressed` (true → false on click); `button[aria-label="Enter fullscreen"]`
keeps its label in the headless lane. The **Character look** select (values
`0`–`4`) writes `characters()[solo].preset`; it is the harness's substitute for
the real **Your look** `role="group"` in `WorldView.tsx:822-833`.

**Not here:** the `.world-minimap`, the real **Your look** swatches, the
sidebar **Open World** row, mention warnings, and anything over a relay. Those
stay with the solo harness or the authenticated rig. `tools/openscape-preview/
check.ts` is the repo's own agent-browser driver for this harness and a good
template for its waits.

## Gotchas

- **The solo harness has no transport.** It comes up reading *"world offline,
  retrying"*, *"Chat: reconnecting"* and *"No #world channel"*. That is the harness,
  not a regression — it proves rendering, layout, and the bound-channel empty
  state, and nothing about movement sync, presence, or the wire. Anything about
  two occupants seeing each other needs a real relay.
- The solo route has a stub world endpoint, so it exercises offline/retry.
  The distinct no-daemon-URL refusal hides the canvas and requires a connected
  daemon; do not infer it from the offline banner.
- **Emotes and nameplates need the preview harness.** In the solo harness
  the wheel never arms and no nameplate renders; in `tools/openscape-preview/`
  both work (section above). The rest of this bullet describes the solo
  harness.
- **Emotes are unreachable here, twice over.** The wheel offers Read, Write,
  Search, Greet, Sit and Stop, and opens by **holding `E`** (a menu named "Emotes";
  releasing picks the highlighted one — `WorldEmoteWheel.tsx`). The wheel only
  arms when `status.state === "connected"` and the player is human
  (`WorldView.tsx`), and the solo harness is always offline, so it never
  opens. Even on a connected rig, `agent-browser` has no hold-a-key command —
  `press` is down-and-up — so drive it with a dispatched `keydown` carrying
  `code: "KeyE"`, and do not read a closed wheel off a synthetic event as a
  broken feature.
- **Two canvases, not one.** Assert `>= 1` or exactly 2; a `querySelector`
  written as if there were a single canvas will still pass while testing the
  wrong layer.
- **The world's real source root is `packages/chat-ui/src/world/`.** Both
  `src/world/WorldView.tsx` and `apps/cloud/src/world/WorldView.tsx` are
  one-line re-export shims, so `#946`'s stat showing a dozen `apps/cloud/src/
  world/*` files changed by one line each is the shims being written, not the
  feature. Read the 923-line `packages/chat-ui/src/world/WorldView.tsx`.
- The sidebar row is a `treeitem` inside its own `tree` named "Open World", not
  a button and not part of the `DESK` tree. `find role button` will not match
  it, and in the shell fixture matching it buys you nothing anyway.
- This file is the exception to the map's "three fixture entry points" table.
  If you are verifying a change that touches both the world and ordinary chat,
  you need two harnesses and two sets of frames.

### Verification record

**Last verified:** 2026-11-01 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `tools/openscape-preview/` on its own Vite lane (18139, `--host 127.0.0.1 --port 18139 --strictPort`): the `/` → `/rooms/tools/openscape-preview/index.html` redirect, `data-world-ready="true"` with 32 `characters()`; the chat pane end to end (send → **Awaiting confirmation** → **Confirm locally** → confirmed with a `.world-speech` bubble; **Earlier messages** 5 → 24; **Hide** ↔ **Open chat**; keyboard resize to 420×212 with `om.chat.world.paneSize` and **Home** reset; the **Resize the channel list** separator 96 in 76–238); **Preview state** `channels` (80 channels; **#channel-2** retargets the nav, section, log and composer), `delivery` (**Retry** → retrying, **Discard** removes), `offline`, `readonly` (disabled textarea), `empty`, `error`, `loading` and `missing` status lines; 32 nameplates with agent markers and **Preview titles** (**Blacksmith**, **Echelon IX**); the emote wheel (**Emotes** dialog, five options, **Read** selected → `emote: "read"`, **Stop** on the next open); **Follow player** toggled; **Character look** preset 0 → 2. Solo harness `mocks/world-solo/index.html?worldprobe=1` load-smoked under the `/rooms/` base on the wrapper lane (18137). **Limitations:** the minimap, the real **Your look** group, movement sync, mention warnings, the sidebar row and anything over a relay; the solo harness was not re-driven beyond the smoke. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261101/r1/` (`world-01` to `world-11`).

**Previous record:** 2026-10-31 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18135) `mocks/world-solo/index.html?worldprobe=1` (under the `/rooms/` base): 2 canvases, `.world-status` **world offline, retrying**, `.world-chat-connection` **Chat: reconnecting**, **No #world channel**, `[data-world-channel-resize]`, `.world-minimap`, five `.world-look` swatches, **Follow player**, **Enter fullscreen** (label unchanged after the click) and **Hide** → **Open chat**. **Limitations:** Movement, occupants, nameplates, the emote wheel, relay and transport, and the `tools/openscape-preview/` HUD harness (not driven). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261031/r1/`.

**Previous record:** 2026-10-30 (scheduled maintenance). **Product commit:** `47cb13bf` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` `mocks/world-solo/index.html?worldprobe=1`: two canvases, `.world-status` "world offline, retrying", "Chat: reconnecting", "No #world channel", `[data-world-channel-resize]`, **Follow player**, **Enter fullscreen** and **Hide**. **Limitations:** Movement, occupants, relay. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261030/r1/` (frame 41).

**Previous record:** 2026-10-29 (nightly maintenance). **Product commit:** `cdfb1b0f` (origin/main; rooms-client 0.108.0). **Scope:** `mocks/world-solo/index.html?worldprobe=1` on the wrapper lane showed 2 canvases and "world offline, retrying". **Limitations:** Movement, occupants and relay. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261029/r1/` (frames 10, 40).

**Previous record:** 2026-10-28 (nightly maintenance). **Product commit:** `2dd7aad1` (origin/main). **Scope:** `mocks/world-solo/index.html?worldprobe=1` on the wrapper lane showed 2 canvases and "world offline, retrying". **Limitations:** **Hide** / **Open chat**, follow player, fullscreen, movement, occupants, emotes, relay and the width drag were not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261028/r1/` (frame 30).

**Previous record:** 2026-10-27. **Product commit:** `6c15b0fb286e9dc1b6cb130c9c97cd7e0afa9254` (origin/main). **Scope:** `mocks/world-solo/index.html?worldprobe=1` on the wrapper lane showed 2 canvases and "world offline, retrying". **Limitations:** **Hide** / **Open chat**, follow player, fullscreen, movement, occupants, emotes, relay and the width drag were not re-driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261027/r01/` (frame 31). Previous record: 2026-10-26 at `5820fbea`.
