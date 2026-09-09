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

## How to get to it (user POV)

You open the app and land on Home: what is unread, who is waiting, where you
were last. The rail on the left has your DMs; clicking one opens the
conversation with that person's presence in the header. From Home you can also
add a friend, start a DM, or browse public channels.

## Driving it with control-om-chat

```bash
export AGENT_BROWSER_SESSION=verify-dm
agent-browser set viewport 1440 900
agent-browser open "$(./control-om-chat url \
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
| `?view=channels` | Public-channel browse board |
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
agent-browser eval 'document.documentElement.dataset.fixtureDmEdit'
```

The last command returns `saved:c1:m2` for the default `ana` fixture. `c1` is
the stable conversation id carried through the edit; `m2` is the message id.

On the Connections surface the chips are `button`, not `tab`: `"Connections"`,
`"Requests"`, `"Blocked"` — three, and only three, in this lane. The product
also has a second row of `.cx-chip.is-mini` filters (All / Followers /
Following) and a `role="tablist"` "Request type" switch, but both render only
once `tab === "connections"` or a real request filter is active, and the
fixture's tab normalisation (below) never gets there. Measured live: three
`.cx-chip`, zero `.cx-chip.is-mini`, no tablist. There is **no Friends chip** — `#697` cut the surface
down to three (`FriendsPane.tsx:104-106`). Opening Requests adds two more chips
beside them, `"Incoming"` and `"Sent"`.

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
  (`tools/visual/shell-fixture.tsx:2371`) — no parameter, hardcoded tab, unlike
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
