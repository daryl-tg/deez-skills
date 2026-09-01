# Direct messages and Home

The personal half of the app: the Home landing surface, the DM list, one
conversation, and the friends surfaces that feed it.

## Sub-features

- Home as a landing surface: unread summary, recent destinations, a
  "Waiting for you" queue, and the agent entry points.
- The DM list with per-conversation unread counts and presence.
- One DM conversation: header with presence, tape, composer.
- Friends: Online / All / Pending / Blocked tabs, and their empty states.
- The public-channel browse board.
- Inbox and message search openers from the Home header.

## How to get to it (user POV)

You open the app and land on Home: what is unread, who is waiting, where you
were last. The rail on the left has your DMs; clicking one opens the
conversation with that person's presence in the header. From Home you can also
add a friend, start a DM, or browse public channels.

## Driving it with control-om-chat

```bash
export AGENT_BROWSER_SESSION=verify-dm
agent-browser set viewport 1440 900
agent-browser open "http://127.0.0.1:18099/rooms/tools/visual/shell-fixture.html?view=home&alerts=quiet"
```

Routes:

| Route | State |
|---|---|
| `?view=home` | Home landing surface |
| `?view=dm&dm=ana` | One DM conversation (`dm=` picks the peer; defaults to `ana`) |
| `?view=friends&tab=online` | Friends, Online tab |
| `?view=friends&tab=pending` | Friends, Pending — an **empty** state, the one most often unlooked-at |
| `?view=friends&tab=blocked` | Friends, Blocked — likewise empty |
| `?view=channels` | Public-channel browse board |
| `?view=empty` | No destination selected |
| `?dmTyping=<name>` | A typing indicator in the DM |
| `?inbox=open` | Topic inbox dialog open over the surface |

Handles that resolve today:

```bash
agent-browser find role treeitem click --name "Direct message with ana, 2 unread"
agent-browser find role button   click --name "Home: DMs and friends, 1 pending friend request"
agent-browser find role button   click --name "New DM"
agent-browser find role button   click --name "Add Friend"
agent-browser find role button   click --name "See all friends"
agent-browser find role button   click --name "Search messages"
agent-browser find role button   click --name "Inbox"
agent-browser find role button   click --name "Create or Join Server"
```

Observations worth capturing:

```bash
agent-browser get url                            # #/home, and the DM's own route on open
agent-browser snapshot -c | grep -i heading      # "Home" -> "A Online ana"
agent-browser snapshot -c | grep -i textbox      # composer retargets to "Message ana · $ for markets · …"
```

The DM header's presence string (`"A Online ana"`) is a real side effect of the
seeded presence state — a good second observation alongside the route.

## Gotchas

- Home renders **two `<h1>` headings** (`"Home"` and the unread summary). Scope
  by name, not by "the heading", or an assertion will match the wrong one.
- The DM rail rows are `treeitem`; the Home surface's own conversation cards are
  `button` (`"ana · Direct message 2"`). The same conversation is reachable two
  ways with two different roles — verify both if your change touches either.
- Friends' Pending and Blocked tabs are empty by design in the fixture. An
  empty pane there is the state under test, not a failure to load.
- The composer in a DM is subject to the same read-only draft lease as
  everywhere else — see [composer-and-sending.md](composer-and-sending.md).
- Presence in the fixture is seeded, not live. Anything about presence
  *changing* (reachability, going away, reconnect) needs the daemon-pair lane.
