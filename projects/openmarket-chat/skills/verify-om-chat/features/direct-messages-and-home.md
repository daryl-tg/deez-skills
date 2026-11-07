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
- Edit a group DM's name and picture, and add a mutual connection to it (`RenameGroupDmModal.tsx`, `AddGroupMemberModal.tsx`). Since `5607d23e` any member who may rename can also set or remove a group picture, which `GroupFaces` draws on the DM list row, the conversation header and the rail tile instead of the stacked member faces; with no picture, or a picture that fails to load, the stacked faces stay.

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

The last command returns the literal `dm-saved` (`shell-fixture.tsx:3549`); a
channel edit writes `channel-saved` to the same key (`:3526`). There is no
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

### Group DM name, picture and add (added 2026-10-27; picture since `5607d23e`)

The shell fixture seeds a group DM named **OM chatters**, owned by the viewer `u1` (`shell-fixture.tsx:2039-2045`).

```bash
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=dm&dm=OM%20chatters&alerts=quiet')"
agent-browser find title "Edit group name and picture" click   # header button (ChatPane.tsx:1019); dialog "Edit group"
agent-browser snapshot -i -c                             # well "Set group picture", textbox "Group name", "Save", "Cancel"
agent-browser upload '[data-group-picture] input[type=file]' <image>   # well -> "Change group picture", "Remove picture" appears
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=dm&dm=OM%20chatters&alerts=quiet&panel=members')"
agent-browser find role button click --name "Add someone"   # dialog "Add to group", textbox "Search mutual connections"
```

`addGroupDmMember` and rename resolve to INERT no-ops, so a name save proves nothing. The dialog was **Rename group** until `5607d23e`; a `find title "Rename group"` now misses.

**Group picture.** Each face cluster is `.group-faces` with `data-faces="picture"` or the member count (`data-faces="2"` for OM chatters). The fixture's `session.groupIcons` stub (`shell-fixture.tsx:3349-3360`) keeps the picture locally, because there is no relay:

- Choosing a file previews it in the well (`img.icon-well-img`, a `blob:` URL). **Save** closes the dialog and the header cluster switches to `data-faces="picture"`; the DM list row and the rail tile keep the stacked faces until the next load, because the stub does not notify the list. That is a fixture limit, not the product.
- **Remove picture** then **Save** puts the header back to `data-faces="2"`.
- `&groupPicture=1` seeds the picture at load: the DM row (**Group message OM chatters, 7 members, 3 unread**), the header and, with `&rail=group`, the rail tile all read `data-faces="picture"`.
- Not provable here: the relay multipart upload and its 256 px webp downscale, `DM_GROUP_UPDATED` propagation, and the transcript line "<name> changed the group picture" (`group-events.ts`), which needs a seeded group event.

Driven 2026-11-04 at `ce14d4ba` on `/rooms/` (`gdm-01` to `gdm-05`). The `/chat/` fixture has no **OM chatters** seed (`/chat/dm/OM%20chatters` renders no `.group-faces`). Verified 2026-10-27 at `6c15b0fb` (maintenance pass, fixture lane). Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261027/r1/` (frames 20-21).

**Members across the phone breakpoint (added 2026-11-07).** Since `442aec46`
the wide layout records its conversation too, so narrowing a window does not
count as opening a new one: Members open there stays open
(`Shell.tsx:2008-2026`). A member's menu or profile, and a confirm opened from
the panel, return focus into Members rather than the composer (`lib/ui-focus.ts`,
`GroupMemberList.tsx:128`). Open `?view=dm&dm=OM%20chatters&panel=members` at
1440×900, then `agent-browser set viewport 700 900`: driven 2026-11-07 on
`/rooms/`, **Add someone** and **Leave group** stayed mounted and the panel
went full width. Two parts are not reachable here. A member row opens no menu
on click or right-click in the fixture. **Leave group** confirms only for the
last member (`GroupMemberList.tsx:110-119`), and the seeded group has others,
so it calls the no-op `leaveGroupDm` directly. Load at 700 px instead and the
seeded panel never opens. That is the phone default above, not a fault.

### New DM, Create or join a server, Getting started (added 2026-10-28)

- **New DM:** on `shell-fixture.html?view=home&alerts=quiet`, button **New DM** (`HomeHub.tsx:747`) opens a dialog named **New Message**. It has textbox **Search connections** and the four seeded connections ana, dax, mira and rho (`NewMessageModal.tsx:250`). Shell mounts `NewMessageModal` (`Shell.tsx:4510`); the old `NewDmModal` was deleted in `228c35f9`. The sidebar DMS header `+` (**New message**, `Sidebar.tsx:4712`) opens the same **New Message** dialog, and Escape returns focus to the `+`. It lives in the DMS group, which the sidebar shows on `?view=dm` and `?view=home`, not on `?view=room`. Driven on both hosts 2026-10-29. Starting the DM needs the daemon-pair lane.
- **Create or join a server:** the rail button **Create or join a server** (`Shell.tsx:4165`) opens a dialog named **Create or Join a Server**, with **Create a server** and **Join with invite link** (`Modals.tsx:119-160`). **Create a server** moves to **Create your server**, with **Server name**, **Back** and **Create server**. Creating a server, and the channel, topic and doc modals, were not driven.
- **Getting started checklist:** the checklist shows only for an enrolled account or a first-run candidate with zero spaces and zero DMs (`HomeHub.tsx:621-625`, `:284`), and the fixture always has spaces. Seed it in the browser before loading Home:

  ```bash
  agent-browser eval 'localStorage.setItem("om.chat.gettingStarted", JSON.stringify({enrolled:true}))'
  agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=home&alerts=quiet')"
  # heading #getting-started-title "Getting started", "1 of 5 complete":
  # Join or create a server (done), Send your first message (Open a room),
  # Follow someone (Follow), Try the quick switcher (Open), Invite your agent (Learn how)
  agent-browser eval 'localStorage.removeItem("om.chat.gettingStarted")'
  ```

  The key is sticky, like `message=cozy`, so remove it afterwards. The dismiss control is **Dismiss getting started**. "Start here" is a different surface: the `<h2>Start here</h2>` in Browse channels (`BrowseChannels.tsx:432`) shows only on a first run with no subscribed channels (`:257`, `:269`), and no fixture seeds that. `WelcomeToChat` needs zero spaces (`HomeHub.tsx:613`), and no seed gives that either.

Verified 2026-10-28 at `2dd7aad1` on `/rooms/` and `/chat/` (nightly maintenance, fixture lane). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261028/r1/` (frames 10-12, 44).

### Create Category name prompt (added 2026-10-28)

On `shell-fixture.html?view=room&alerts=quiet`, open the sidebar server header button **Thanefield Capital**. Its menu lists Read, Mute, Invite, Server Settings, Create Channel, **Create Category**, Server Library, Open World, Clean up topics (`/rooms/` only), Notification Settings, the mute durations, Leave Server and Copy server ID. **Create Category** (`ServerMenu.tsx:37`) opens `NamePromptModal` (`Modals.tsx:162`) as a dialog named **Create Category**, with the hint "Shows as a separator in the sidebar…", focus in the **Category name** input and a **Create Category** button. Escape closes it. Submitting calls `createCategory` (`Sidebar.tsx:2871`, `:6666`) and was not driven. Find the header button by its text: there are two **Thanefield Capital** buttons, and the sidebar one is the last. The other display-name modals have no seed. `NameEditModal` opens only from `session.openNameEditPrompt` (**Change Name** on your own user menu), which the fixture leaves unstubbed with `nameEditPrompt: null` (`shell-fixture.tsx:3053`). `DisplayNameAskModal` needs `profileReady()`, which the fixture stubs to false.

Verified 2026-10-28 at `07f7d04c` on `/rooms/` and `/chat/` (scheduled maintenance, fixture lane). Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261028/r1/` (`*-create-category-name-prompt.png`).

The sidebar's own **Create channel** button (`Sidebar.tsx:4901`, shown because the fixture stubs `spaceActionVisible` true) opens the same dialog as the server menu's **Create Channel**: **Create channel**, with the textbox **Channel name**, a private-channel checkbox and a **Create channel** submit. Escape closes it. Driven 2026-11-08 on `/rooms/` and `/chat/`. The Library panel's **New doc** is not reachable: it calls `session.requestNewDoc` (`LibraryPanel.tsx:1437`), which neither shell fixture stubs (`newDocRequest: null`, `shell-fixture.tsx:3607`), so no dialog opens.

### DM row menu (added 2026-10-31)

On `shell-fixture.html?view=dm&alerts=quiet`, dispatch a `contextmenu` event
on the `.channel-row-identity` of **Direct message with ana, 2 unread**
(`Sidebar.tsx:6510-6655`). The menu opens with an identity header (**ana**)
and seven items: **Follow**, **Invite to Server** (a submenu), **Add to Desk**,
**Close DM**, **Block**, **Copy @ana** and **Copy user ID**. A followed peer
would read **Unfollow** or **Cancel follow request**, a Desk DM **Remove from
Desk**, and a blocked peer **Unblock**; the fixture seeds none of those. The
follow verbs, `closeDm`, `confirmBlockUserById` and `unblockUserById` are
unstubbed, so the offer is proved and every effect is pending. Driven on
`/rooms/` (18135) and `/chat/` (18136) at `936f5b64`.

### Message requests row (added 2026-11-01)

`?requests=N` (`shell-fixture.tsx:2735-2746`, 0–9) knocks N strangers onto
the pinned **Message requests** row above the DMs. On
`shell-fixture.html?view=dm&requests=3&alerts=quiet` the sidebar shows a
`treeitem` named **3 message requests** (`Sidebar.tsx:4644`); clicking it
changes nothing (`openMessageRequests`, `lib/session.ts:38206`, is unstubbed,
so the click resolves to `INERT`), and the hash stays `#/dm/ana`. The
Connections **Requests** tab's **Messages 0** tab (`FriendsPane.tsx:1171`) is
the other door and renders **No message requests waiting.** without the seed.
Driven 2026-11-01 on `/rooms/` at `936f5b64`. Opening the inbox, accepting or
declining a request need a stub or a daemon.

### The 99+ headline (added 2026-11-02)

Since `4cd3434f` the Home headline caps its count: `formatUnreadCount`
(`lib/animated-count-parts.ts:35-42`, `UNREAD_COUNT_CAP = 99`) prints the
grouped number up to 99 and the literal **99+** past it, and `HomeHub.tsx:694`
wraps only the number in `<b>`. The fixture lane reaches it through the rail
seed: `shell-fixture.html?view=home&alerts=quiet&rail=counts` seeds the **vex**
DM at 120 unread (`shell-fixture.tsx:1907`), and the `h1` reads
**99+ unread across 4 conversations.** (driven 2026-11-02 on `/rooms/`). The
same seed leaves the DM treeitem named **Direct message with vex, 120 unread**
while its `.rail-badge` reads **99+**: the row label does not go through the
formatter, only the pill and the headline do. No channel or topic seed exceeds
99 (`channels=many` tops out at 20), so the sidebar channel label's
**, 99+ unread** form (`Sidebar.tsx:3398`) is source-only here.

## Gotchas

- **`rail=counts` is a `/rooms/` seed only.** The `/chat/` fixture has no
  `counts` branch, so `shell-fixture.html?view=home&alerts=quiet&rail=counts`
  on `/chat/` (it lands on `/chat/home`) reads the
  default **2 unread across 1 conversation.**; prove the **99+** headline on
  `/rooms/` (2026-11-02).
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
  (`tools/visual/shell-fixture.tsx:3298`) — no parameter, hardcoded tab, unlike
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

**Last verified:** 2026-11-08 (nightly maintenance). **Product commit:** `08fe407b` (GitLab origin/main; rooms-client 0.112.0; unchanged since the 2026-11-07 pass). **Scope:** `/rooms/` (18183) and `/chat/` (18184): `view=dm&dm=ana` (`#/dm/ana`, `/chat/dm/ana`), `view=home` ("2 unread across 1 conversation."), and the sidebar **Create channel** dialog (new). **Limitations:** `view=friends&tab=blocked` still reads **could not load** (carried); **New doc** has no stub. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261108/r1/`.

**Previous record:** 2026-11-07 (nightly maintenance). **Product commit:** `08fe407b` (GitLab origin/main; rooms-client 0.112.0; 89 commits past `ea399e62`). **Scope:** `/rooms/` (18180) and `/chat/` (18181): `view=dm` mounts **ana** with 2 rows; `view=home` reads "2 unread across 1 conversation.". `/rooms/` (18180) `view=dm&dm=OM%20chatters&panel=members` opened at 1440 px keeps the group **Members** panel (**Add someone**, **Leave group**) open after `set viewport 700 900`, now full width. **Limitations:** the member menu, the profile return and the last-member **Leave this group?** confirm were not reached (a row click or right-click opens nothing, and the seeded group has other members); `/chat/` has no group DM seed. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261107/r1/`.

**Previous record:** 2026-11-06 (nightly maintenance). **Product commit:** `ea399e62` (GitLab origin/main; rooms-client 0.111.0; 74 commits past `873a57ce`). **Scope:** `/rooms/` (18180) and `/chat/` (18181): `view=dm` mounts **ana** with 2 rows; `view=home` reads "2 unread across 1 conversation.". **Limitations:** group DM and **Edit group** only by the route smoke. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261106/r1/`.

**Previous record:** 2026-11-05 (nightly maintenance). **Product commit:** `873a57ce` (GitLab origin/main; rooms-client 0.109.1; 17 commits past `ce14d4ba`). **Scope:** `/rooms/` (18170) `view=dm&dm=OM%20chatters`: **Edit group name and picture** opens the dialog **Edit group**. **Limitations:** the picture save and Home headline were not re-driven; their 2026-11-04 record stands. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261105/r1/` (`34`).

**Previous record:** 2026-11-04 (nightly maintenance). **Product commit:** `ce14d4ba` (GitLab origin/main; rooms-client 0.109.1; 16 commits past `ba4389e7`). **Scope:** `/rooms/` (18160): Home **2 unread across 1 conversation.**; `?view=dm&dm=ana` → `#/dm/ana`; the **Edit group** dialog, picture set, save, remove and the `groupPicture=1` seed (see Group DM name, picture and add). `/chat/` (18161): Home headline; no group DM seed. **Limitations:** rename and add are INERT; the relay picture upload is not provable here. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261104/r1/` (`home-01`, `gdm-01` to `gdm-05`).

**Previous record:** 2026-11-03 (nightly maintenance). **Product commit:** `ba4389e7` (GitLab origin/main; rooms-client 0.108.0; one CI-only commit past `3f8f24bc`). **Scope:** `/rooms/` (18143) and `/chat/` (18144): Home **New DM** → **New Message** (**Search connections**); **Create or Join a Server**; the DM with ana; Connections empty state; Requests **FOLLOWER REQUESTS — NAN**; Blocked **People could not load**; 9 subscribe rows and the empty directory; the server header menu → **Create Category** (16 items on `/rooms/`, 15 on `/chat/`). `/rooms/` only: **OM chatters** → **Add to group**; `rail=counts` **99+ unread across 4 conversations.** (the vex DM is still named **120 unread**); the 8-item DM row menu; `requests=3` → **3 message requests**. **Limitations:** unchanged. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261103/r1/` (`dm-*`).

**Previous record:** 2026-11-02 (scheduled maintenance). **Product commit:** `3f8f24bc` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18141): Home **2 unread across 1 conversation.** → **New DM** → **New Message** with **Search connections**; **Direct message with ana, 2 unread** → `#/dm/ana`, composer **Message ana · $ for markets · /chart to post one**; group DM `panel=members` **Add someone**; `rail=counts` → **99+ unread across 4 conversations.** with the row still named **Direct message with vex, 120 unread**. `/chat/` (18142): Home headline, **New DM** → **New Message**, the ana DM; `rail=counts` is not seeded there. **Limitations:** Requests, Browse channels, the DM row menu and the group rename were not re-driven; their nightly records stand. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261102/r1/`.

**Previous record:** 2026-11-02 (nightly maintenance). **Product commit:** `3f8f24bc` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18137) and `/chat/` (18138): Home **2 unread across 1 conversation.** (`#/home`, `/chat/home`) → **New DM** → **New Message**; **Create or join a server** → **Create or Join a Server** (**Create a server**, **Join with invite link**); the Requests tab (**Request type**: All, Followers NaN, Messages); **Browse channels** (5 Subscribe buttons); the DM row menu (ana: Follow, Invite to Server, Add to Desk, Close DM, Block, Copy @ana, Copy user ID); on `/rooms/`: `requests=3` → treeitem **3 message requests** (click inert, hash stays `#/home`); the **Getting started** heading and **Dismiss getting started** with the `om.chat.gettingStarted` seed; **Rename group** → dialog **Rename group** with **Group name**; `rail=counts` → **99+ unread across 4 conversations.** while the vex treeitem keeps **120 unread**. **Limitations:** the `/chat/` DM header still does not open the profile drawer; the typing indicator and the directory states were load-smoked only. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261102/r1/`.

**Previous record:** 2026-11-01 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18137): Home (**2 unread across 1 conversation.**) → **New DM** → **New Message** with **Search connections** and ana / dax / mira / rho; **Create or join a server** → **Create or Join a Server**; the Getting started checklist (5 items) with the `om.chat.gettingStarted` seed; **Requests** tab (**Followers NaN** still); the DM row menu (Follow, Invite to Server, Add to Desk, Close DM, Block, Copy @ana, Copy user ID); **Rename group** on OM chatters; Browse channels (9 public · 4 subscribed) and `directory=empty`; the **3 message requests** row from `?requests=3`. `/chat/` (18138): **New Message**, **Create or Join a Server**, the DM row menu and the DM hover peek. **Limitations:** **Add someone**, **See connections**, **Follow someone** and the blocked tab were not re-driven; every menu verb and the requests inbox stay pending. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261101/r1/` (`home-01` to `home-06`, `census-01`/`02`, `chat-04`, `chat-06`).

**Previous record:** 2026-10-31 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18135): `?view=home` **New DM** → **New Message** (ana, dax, mira, rho); rail **Create or join a server** → **Create or Join a Server**; server menu **Create Category** → **Create Category** and **Create Channel** → **Create channel**; `?view=dm&dm=OM%20chatters` **Rename group** dialog; `?view=friends&tab=requests` → `#/connections/requests` with the **Request type** tablist (All / Followers NaN / Messages 0); `?view=channels&directory=empty` "This workspace has no public channels yet." and `&directory=loading&connection=offline` "The channel directory is out of reach."; the DM row menu. `/chat/` (18136): **New Message**, **Create or Join a Server**, **Create Category**, the DM row menu, and 390×844 Chats → `/chat/dm/ana` → **Back to Chats**. **Limitations:** Sending, creation, rename and add effects; Blocked tab crash; Start here and WelcomeToChat seeds. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261031/r1/`.

**Previous record:** 2026-10-30 (scheduled maintenance). **Product commit:** `47cb13bf` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/`: Home `#/home` with **New DM**, **Follow someone**, **Create or Join Server**, **See connections**; **New DM** → **New Message** with **Search connections**; **Create or Join a Server**; `#/dm/ana`; DMS **New message** → **New Message**; **Rename group** (found with `find title`); **Add someone** → **Add to group**; `tab=requests` chips, tablist and NaN counts; **Browse channels**. **Limitations:** Rename and add are no-ops; `/chat/` DMs were driven only through the hover peek and the mobile path. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261030/r1/` (frames 17-19).

**Previous record:** 2026-10-29 (nightly maintenance). **Product commit:** `cdfb1b0f` (origin/main; rooms-client 0.108.0). **Scope:** Home h1 `2 unread across 1 conversation.` at `#/home` and `/chat/home`. On **OM chatters**, **Rename group** opened **Rename group** (value `OM chatters`), and with `panel=members` **Add someone** opened **Add to group** (**Search mutual connections**). On `?view=dm&dm=ana`, the sidebar DMS header **New message** opened **New Message** (**Search connections**), and Escape returned focus to the `+`, on both hosts. **Limitations:** Starting a DM, rename and add are fixture no-ops. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261029/r1/` (frames 06, 24, 50–51, 61).

**Previous record:** 2026-10-28 (nightly maintenance). **Product commit:** `2dd7aad1` (origin/main). **Scope:** Home h1 `2 unread across 1 conversation.` at `#/home`; `view=dm` landed on `#/dm/ana` with 2 rows; `dm=OM%20chatters` gave `#/dm/OM%20chatters`. **Rename group** opened **Rename group**, and **Add someone** opened **Add to group**. New DM, Create or join a server and the Getting started checklist rendered on both hosts (section above). **Limitations:** Connections, requests, `view=public`, the Blocked tab (fixture crash), presence, a real catalog and every create or send effect were not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261028/r1/` (frames 10-12, 14, 44).

**Previous record:** 2026-10-27. **Product commit:** `6c15b0fb286e9dc1b6cb130c9c97cd7e0afa9254` (origin/main). **Scope:** Home h1 `2 unread across 1 conversation.` at `#/home`; `view=dm` landed on `#/dm/ana` with 2 rows. **Limitations:** Connections, requests, `view=public`, the Blocked tab (fixture crash), presence and a real catalog were not re-driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261027/r01/` (frame 21). Previous record: 2026-10-26 at `5820fbea`.
