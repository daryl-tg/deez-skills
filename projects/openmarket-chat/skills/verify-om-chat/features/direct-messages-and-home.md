# Direct messages and Home

The personal half of the app: the Home landing surface, the DM list, one
conversation, and the friends surfaces that feed it.

## Sub-features

- Home as a landing surface: unread summary, recent destinations, a
  "Waiting for you" queue, and the agent entry points.
- The DM list with per-conversation unread counts and presence.
- One direct or group DM conversation: header, tape, composer, and group
  members panel.
- Editing your own DM: More -> Edit Message -> inline editor -> save/cancel.
- Connections: the Connections / Requests / Blocked chips, and their
  empty states.
- The public-channel browse board.
- Inbox and message search openers — **mobile only**, see Gotchas.
- Rename a group DM, and add a mutual connection to it (`RenameGroupDmModal.tsx`, `AddGroupMemberModal.tsx`).

## How to get to it (user POV)

You open the app and land on Home: what is unread, who is waiting, where you
were last. The rail on the left has your DMs; clicking one opens the
conversation with that person's presence in the header. From Home you can also
add a friend, start a DM, or browse public channels.

## Driving it with control-om-chat

```bash
export AGENT_BROWSER_SESSION=verify-dm
agent-browser set viewport 1440 900
agent-browser open "$(control-om-chat url \
  'tools/visual/shell-fixture.html?view=home&alerts=quiet')"
```

Routes:

| Route | State |
|---|---|
| `?view=home` | Home landing surface |
| `?view=dm&dm=ana` | One DM conversation (`dm=` picks the peer; defaults to `ana`) |
| `?view=dm&dm=OM%20chatters` | Seeded group DM with link/file messages and a driveable Members panel |
| `?view=dm&dm=OM%20chatters&panel=members` | The same group DM with Members already open |
| `?view=friends&tab=connections` | Connections — the default, an empty state |
| `?view=friends&tab=requests` | Requests (what this file used to call Pending) |
| `?view=friends&tab=blocked` | Blocked — **currently crashes**, see Gotchas |
| `?view=channels` | Public-channel browse board (Subscribe to / Unsubscribe from rows) |
| `?view=channels&directory=empty` | Empty directory: "This workspace has no public channels yet." |
| `?view=channels&directory=loading` | Loading skeleton, `role=status` named "Loading channels" (any `directory` value except `empty`) |
| `?view=channels&directory=loading&connection=offline` | Unreachable: "The channel directory is out of reach" (any `connection` value except `live`). There is no separate fetch-error state |
| `?view=empty` | No destination selected |
| `?dmTyping=peer` | A typing indicator in the DM — the literal string `peer`, not a name |
| `?inbox=open` | Topic inbox dialog open over the surface |

Handles that resolve today:

```bash
agent-browser find role treeitem click --name "Direct message with ana, 2 unread"
agent-browser find role treeitem click --name "Group message OM chatters, 7 members"
agent-browser find role button   click --name "Members"
agent-browser find role button   click --name "Home: DMs and connections, 1 pending follow request"
agent-browser find role button   click --name "New DM"
agent-browser find role button   click --name "Follow someone"
agent-browser find role button   click --name "See connections"
agent-browser find role button   click --name "Create or Join Server"
```

To drive a DM edit, hover your own seeded message (`"yep, watching the next
print"`), open `More`, choose `Edit Message`, then use the inline controls:

```bash
agent-browser find role button click --name "More"
agent-browser find role menuitem click --name "Edit Message"
agent-browser find role textbox fill --name "Edit message" "replacement text"
agent-browser find role button click --name "save"
agent-browser eval 'document.documentElement.dataset.fixtureMermaidEdit'
```

The last command returns the literal `dm-saved` (`shell-fixture.tsx:3529`); a
channel edit writes `channel-saved` to the same key (`:3506`). There is no
`fixtureDmEdit` key, and the value carries no conversation or message id.
Measured at `f7d7c987`. `More` only appears while the row is hovered, so mark
the row first, then hover it:

```bash
agent-browser eval '(()=>{const r=[...document.querySelectorAll("[data-message-row]")]
  .find(e=>/yep, watching the next print/.test(e.textContent));
  r.setAttribute("data-probe","1"); r.scrollIntoView({block:"center"}); return "ok"})()'
agent-browser hover '[data-probe]'
```

Wrap the lookup in an IIFE. A bare top-level `const` persists in the page, so
a second eval on the same load throws `Identifier ... has already been
declared`.

On the Connections surface the chips are `button`, not `tab`: `"Connections 0"`
(the chip now carries its count, so match it non-exactly), `"Requests"` and
`"Blocked"`. That is three, and only three, in this lane. The product
also has a second row of `.cx-chip.is-mini` filters (All / Followers /
Following) and a `role="tablist"` "Request type" switch, but both render only
once `tab === "connections"` or a real request filter is active, and the
fixture's tab normalisation (below) never gets there. Measured live: three
`.cx-chip`, zero `.cx-chip.is-mini`, no tablist. There is **no Friends chip** — `#697` cut the surface
down to three (`FriendsPane.tsx:105-109`). Opening Requests adds two more chips
beside them, `"Incoming"` and `"Sent"`. Requests (`?view=friends&tab=requests`)
also renders the **Request type** tablist (**All**, **Followers NaN**,
**Messages 0**) and the headers **FOLLOWER REQUESTS — NAN** and **MESSAGE
REQUESTS — 0**. The NaN is fixture seeding: `session.pendingIncomingRequests`
and `pendingOutgoingRequests` are unstubbed (`FriendsPane.tsx:241-242`), so two
`INERT` lengths add to NaN. Do not report it as a product bug (re-measured
2026-10-30 on `/rooms/`).

`#697` renamed the friend vocabulary to follow vocabulary throughout, and the
map's old handles went with it: **"Add Friend" is now "Follow someone"**,
**"See all friends" is now "See connections"**, and the sidebar door reads
**"Home: DMs and connections, N pending follow request"**. The *concept* of a
friend survives only internally — a mutual follow is still `rel === "friends"`
in `FriendsPane.tsx`, but every row that used to say "Friends" now says
"Following", and the "Friends" chips on the profile panel and popover were
deleted. Do not expect the word anywhere in the UI.

Observations worth capturing:

```bash
agent-browser get url                            # #/home, and the DM's own route on open
agent-browser snapshot -c | grep -i heading      # "Home" -> "A Online ana"
agent-browser snapshot -c | grep -i textbox      # composer retargets to "Message ana · $ for markets · …"
```

The DM header's presence string (`"A Online ana"`) is a real side effect of the
seeded presence state — a good second observation alongside the route.

### Group DM rename and add (added 2026-10-27)

The shell fixture seeds a group DM named **OM chatters**, owned by the viewer `u1` (`shell-fixture.tsx:2037-2043`).

```bash
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=dm&dm=OM%20chatters&alerts=quiet')"
agent-browser find title "Rename group" click          # header button; dialog "Rename group"
agent-browser snapshot -i -c                             # textbox "Group name" (value "OM chatters"), "Save"
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=dm&dm=OM%20chatters&alerts=quiet&panel=members')"
agent-browser find role button click --name "Add someone"   # dialog "Add to group", textbox "Search mutual connections"
```

`addGroupDmMember` and rename resolve to INERT no-ops, so a save proves nothing. The `/chat/` fixture has no **OM chatters** seed. Verified 2026-10-27 at `6c15b0fb` (maintenance pass, fixture lane). Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261027/r1/` (frames 20-21).

### New DM, Create or join a server, Getting started (added 2026-10-28)

- **New DM:** on `shell-fixture.html?view=home&alerts=quiet`, button **New DM** (`HomeHub.tsx:746`) opens a dialog named **New Message**. It has textbox **Search connections** and the four seeded connections ana, dax, mira and rho (`NewMessageModal.tsx:250`). Shell mounts `NewMessageModal` (`Shell.tsx:4449`); the old `NewDmModal` was deleted in `228c35f9`. The sidebar DMS header `+` (**New message**, `Sidebar.tsx:4680`) opens the same **New Message** dialog, and Escape returns focus to the `+`. It lives in the DMS group, which the sidebar shows on `?view=dm` and `?view=home`, not on `?view=room`. Driven on both hosts 2026-10-29. Starting the DM needs the daemon-pair lane.
- **Create or join a server:** the rail button **Create or join a server** (`Shell.tsx:4106`) opens a dialog named **Create or Join a Server**, with **Create a server** and **Join with invite link** (`Modals.tsx:119-160`). **Create a server** moves to **Create your server**, with **Server name**, **Back** and **Create server**. Creating a server, and the channel, topic and doc modals, were not driven.
- **Getting started checklist:** the checklist shows only for an enrolled account or a first-run candidate with zero spaces and zero DMs (`HomeHub.tsx:620-624`, `:283`), and the fixture always has spaces. Seed it in the browser before loading Home:

  ```bash
  agent-browser eval 'localStorage.setItem("om.chat.gettingStarted", JSON.stringify({enrolled:true}))'
  agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=home&alerts=quiet')"
  # heading #getting-started-title "Getting started", "1 of 5 complete":
  # Join or create a server (done), Send your first message (Open a room),
  # Follow someone (Follow), Try the quick switcher (Open), Invite your agent (Learn how)
  agent-browser eval 'localStorage.removeItem("om.chat.gettingStarted")'
  ```

  The key is sticky, like `message=cozy`, so remove it afterwards. The dismiss control is **Dismiss getting started**. "Start here" is a different surface: the `<h2>Start here</h2>` in Browse channels (`BrowseChannels.tsx:432`) shows only on a first run with no subscribed channels (`:257`, `:269`), and no fixture seeds that. `WelcomeToChat` needs zero spaces (`HomeHub.tsx:612`), and no seed gives that either.

Verified 2026-10-28 at `2dd7aad1` on `/rooms/` and `/chat/` (nightly maintenance, fixture lane). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261028/r1/` (frames 10-12, 44).

### Create Category name prompt (added 2026-10-28)

On `shell-fixture.html?view=room&alerts=quiet`, open the sidebar server header button **Thanefield Capital**. Its menu lists Read, Mute, Invite, Server Settings, Create Channel, **Create Category**, Server Library, Open World, Clean up topics (`/rooms/` only), Notification Settings, the mute durations, Leave Server and Copy server ID. **Create Category** (`ServerMenu.tsx:37`) opens `NamePromptModal` (`Modals.tsx:162`) as a dialog named **Create Category**, with the hint "Shows as a separator in the sidebar…", focus in the **Category name** input and a **Create Category** button. Escape closes it. Submitting calls `createCategory` (`Sidebar.tsx:2852`, `:6596`) and was not driven. Find the header button by its text: there are two **Thanefield Capital** buttons, and the sidebar one is the last. The other display-name modals have no seed. `NameEditModal` opens only from `session.openNameEditPrompt` (**Change Name** on your own user menu), which the fixture leaves unstubbed with `nameEditPrompt: null` (`shell-fixture.tsx:3051`). `DisplayNameAskModal` needs `profileReady()`, which the fixture stubs to false.

Verified 2026-10-28 at `07f7d04c` on `/rooms/` and `/chat/` (scheduled maintenance, fixture lane). Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261028/r1/` (`*-create-category-name-prompt.png`).

### DM row menu (added 2026-10-31)

On `shell-fixture.html?view=dm&alerts=quiet`, dispatch a `contextmenu` event
on the `.channel-row-identity` of **Direct message with ana, 2 unread**
(`Sidebar.tsx:6440-6585`). The menu opens with an identity header (**ana**)
and seven items: **Follow**, **Invite to Server** (a submenu), **Add to Desk**,
**Close DM**, **Block**, **Copy @ana** and **Copy user ID**. A followed peer
would read **Unfollow** or **Cancel follow request**, a Desk DM **Remove from
Desk**, and a blocked peer **Unblock**; the fixture seeds none of those. The
follow verbs, `closeDm`, `confirmBlockUserById` and `unblockUserById` are
unstubbed, so the offer is proved and every effect is pending. Driven on
`/rooms/` (18135) and `/chat/` (18136) at `936f5b64`.

## Gotchas

- **Home renders one `<h1>` on desktop**, the unread summary
  (`"2 unread across 1 conversation."`). The `"Home"` heading is inside the
  mobile-only header block (`max-width: 768px`), so at 1440×900 it does not
  exist. Looking for a second heading there is looking for nothing.
- **"Search messages" and "Inbox" are mobile-only too**, in that same header
  block. Neither resolves on desktop Home. The desktop search entry point is
  the sidebar's "Search or jump to…" pill, and that is inert in the fixture —
  so message search has no driveable desktop route here at all.
- **Only `requests` and `blocked` reach the hash.** `?tab=requests` gives
  `#/connections/requests` and `?tab=blocked` gives `#/connections/blocked`.
  Everything else — `connections`, the retired `friends`, and any unknown value
  like `pending` — lands on `#/connections/online` no matter what you passed,
  and no chip renders as active. So the route tells you nothing on the default
  view, and neither does the active state. Assert on the chip list itself.
  The real tab ids are `connections`, `requests`, `blocked`; `friends` retired
  with `#697`, and `online`, `all` and `pending` were never translated.

  Do not try to derive this from `hashForView` — reading that function alone
  predicts `?tab=pending` lands on `#/connections/pending`, and it does not.
  The cause is a **fixture stub**: `openFriends` there is written
  `openFriends: () => navigate({ kind: "friends", tab: "online" })`
  (`tools/visual/shell-fixture.tsx:3293`) — no parameter, hardcoded tab, unlike
  the real `ChatSession.openFriends`, which honours its argument. Boot seeds the
  hash, routing parses it back, the parsed view differs in shape from the raw
  fixture view for every id except `requests` and `blocked`, so navigation
  fires and the argument-blind stub lands on `online` every time. Those two are
  immune only because they round-trip identically and the equality guard
  returns early before the stub is ever called.
- **`?view=friends&tab=blocked` crashes the pane today.** You get *"People
  could not load"* with a Try again / Reload pair. It is fixture seeding, not a
  product regression: the fixture stubs `session.blocks` as `[]` while
  `BlockedView` expects `{rows, …} | null`, so `state?.rows.length` throws on
  the missing `rows`. Do not caption this as a bug in the app, and do not
  "fix" it by editing the map — it needs a fixture-seed change in
  `tools/visual/shell-fixture.tsx`, which belongs to whoever next ships a
  Blocked-tab change.
- The DM rail rows are `treeitem`; the Home surface's own conversation cards are
  `button` (`"ana · Direct message 2"`). The same conversation is reachable two
  ways with two different roles — verify both if your change touches either.
  That card is specifically the "Waiting for you" row, and it is only there
  because the fixture seeds ana with 2 unread.
- **The DM peer id is hardcoded.** The fixture answers `"u-ana"` for
  `dmPeerUserId()` whatever `?dm=` says, so `?view=dm&dm=dax` renders dax's
  name over ana's avatar and presence. Only `dm=ana` is coherent.
- `OM chatters` seeds a group DM tape with a long link and a long-name PDF so
  the narrowed transcript and Members panel can be reviewed together. `just
  me` also resolves as a group route, but it is intentionally sparse. Group
  routing still uses `conversationId`, never the mutable display label; prove
  that wire identity separately with the focused session tests when changing
  routing behavior.
- The composer in a DM is subject to the same read-only draft lease as
  everywhere else — see [composer-and-sending.md](composer-and-sending.md).
- Presence in the fixture is seeded, not live. Anything about presence
  *changing* (reachability, going away, reconnect) needs the daemon-pair lane.

- **From a DM, the rail Home button does not leave the DM.** In DM mode the
  session is already in Home, so `Home: DMs and connections, N pending follow
  request` keeps `#/dm/ana`. Return to the hub with the sidebar `treeitem`
  named **Home**, which lands on `#/home`.
- **Chip clicks cannot switch tabs here.** Clicking **Requests** from the
  default view calls the argument-blind `openFriends` stub and stays on
  `#/connections/online`. Load `?view=friends&tab=requests` instead.
- **A DM header can show "Join call (undefined in call)".** That is the
  autofill proxy, not a live call: neither shell fixture stubs
  `session.dmVoiceRosterFor`, so `DmLiveCallPill` (`ChannelToolbar.tsx:149-165`)
  reads `.length` off `INERT` and renders the pill with `undefined`. Seen on
  `?view=dm&dm=ana` on both hosts, 2026-10-29. Never caption it as a call in
  progress, and never report it as a product bug.

### Verification record

**Last verified:** 2026-10-31 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18135): `?view=home` **New DM** → **New Message** (ana, dax, mira, rho); rail **Create or join a server** → **Create or Join a Server**; server menu **Create Category** → **Create Category** and **Create Channel** → **Create channel**; `?view=dm&dm=OM%20chatters` **Rename group** dialog; `?view=friends&tab=requests` → `#/connections/requests` with the **Request type** tablist (All / Followers NaN / Messages 0); `?view=channels&directory=empty` "This workspace has no public channels yet." and `&directory=loading&connection=offline` "The channel directory is out of reach."; the DM row menu. `/chat/` (18136): **New Message**, **Create or Join a Server**, **Create Category**, the DM row menu, and 390×844 Chats → `/chat/dm/ana` → **Back to Chats**. **Limitations:** Sending, creation, rename and add effects; Blocked tab crash; Start here and WelcomeToChat seeds. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261031/r1/`.

**Previous record:** 2026-10-30 (scheduled maintenance). **Product commit:** `47cb13bf` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/`: Home `#/home` with **New DM**, **Follow someone**, **Create or Join Server**, **See connections**; **New DM** → **New Message** with **Search connections**; **Create or Join a Server**; `#/dm/ana`; DMS **New message** → **New Message**; **Rename group** (found with `find title`); **Add someone** → **Add to group**; `tab=requests` chips, tablist and NaN counts; **Browse channels**. **Limitations:** Rename and add are no-ops; `/chat/` DMs were driven only through the hover peek and the mobile path. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261030/r1/` (frames 17-19).

**Previous record:** 2026-10-29 (nightly maintenance). **Product commit:** `cdfb1b0f` (origin/main; rooms-client 0.108.0). **Scope:** Home h1 `2 unread across 1 conversation.` at `#/home` and `/chat/home`. On **OM chatters**, **Rename group** opened **Rename group** (value `OM chatters`), and with `panel=members` **Add someone** opened **Add to group** (**Search mutual connections**). On `?view=dm&dm=ana`, the sidebar DMS header **New message** opened **New Message** (**Search connections**), and Escape returned focus to the `+`, on both hosts. **Limitations:** Starting a DM, rename and add are fixture no-ops. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261029/r1/` (frames 06, 24, 50–51, 61).

**Previous record:** 2026-10-28 (nightly maintenance). **Product commit:** `2dd7aad1` (origin/main). **Scope:** Home h1 `2 unread across 1 conversation.` at `#/home`; `view=dm` landed on `#/dm/ana` with 2 rows; `dm=OM%20chatters` gave `#/dm/OM%20chatters`. **Rename group** opened **Rename group**, and **Add someone** opened **Add to group**. New DM, Create or join a server and the Getting started checklist rendered on both hosts (section above). **Limitations:** Connections, requests, `view=public`, the Blocked tab (fixture crash), presence, a real catalog and every create or send effect were not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261028/r1/` (frames 10-12, 14, 44).

**Previous record:** 2026-10-27. **Product commit:** `6c15b0fb286e9dc1b6cb130c9c97cd7e0afa9254` (origin/main). **Scope:** Home h1 `2 unread across 1 conversation.` at `#/home`; `view=dm` landed on `#/dm/ana` with 2 rows. **Limitations:** Connections, requests, `view=public`, the Blocked tab (fixture crash), presence and a real catalog were not re-driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261027/r01/` (frame 21). Previous record: 2026-10-26 at `5820fbea`.
