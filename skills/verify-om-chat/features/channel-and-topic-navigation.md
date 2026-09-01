# Channel and topic navigation

Moving between a server's channels, and between a channel and one of its
topics. The most-driven surface in the app and the cheapest one to prove.

## Sub-features

- Channel list in the sidebar, grouped by section (`DESK`), with unread and
  mention counts on each row.
- Expanding and collapsing a channel's topic rows ("Hide this channel's
  topics", "Cycle topic rows").
- Opening a topic from the rail, and the `All N topics in <channel>` overflow
  row.
- The topic view's breadcrumb and its **Back to #channel** return.
- The composer retargeting to whatever is open.
- The channel header's right-slot tabs (Chat / Topics / Alerts) and panel
  toggles (members, pins, bookmarks, to-dos).

## How to get to it (user POV)

You are in `#ops`. The sidebar lists your channels; under each one sit its live
topics with unread badges. You click a topic — the pane switches to that
topic's conversation, a breadcrumb appears at the top, and the message box now
says it will post into the topic rather than the channel. You click **Back to
#ops** and you are back where you started, composer included.

## Driving it with control-om-chat

```bash
cd /Users/dboon/github/openmarket-chat
OM_CHAT_LANE_PORT=18099 ./control-om-chat up
export AGENT_BROWSER_SESSION=verify-nav
agent-browser set viewport 1440 900
agent-browser open "http://127.0.0.1:18099/rooms/tools/visual/shell-fixture.html?view=room&alerts=quiet"
```

Routes:

| Route | State |
|---|---|
| `shell-fixture.html?view=room&alerts=quiet` | `#ops` with six open topics in the rail |
| `shell-fixture.html?view=topics` | The channel's topic **list** surface |
| `shell-fixture.html?view=topic&topic=cpi-print-aug` | One topic's own chat, entered directly |
| `shell-fixture.html?view=room&channels=many` | Long channel list — sidebar overflow and scroll |
| `shell-fixture.html?view=room&bulk=120` | A loaded tape, for scroll and virtualisation work |
| `shell-fixture.html?view=room&peek=cpi-print-aug` | Topic open in the right sidebar rather than the main pane |

Handles that resolve today:

```bash
agent-browser find role treeitem click --name "CPI print — Aug, 2 mentions, 3 unread"
agent-browser find role treeitem click --name "channel ops, 4 unread, 5 unread in topics"
agent-browser find role button   click --name "Back to #ops"
agent-browser find role button   click --name "Hide this channel's topics"
agent-browser find role button   click --name "All 6 topics in ops"
```

Three independent observations, all cheap:

```bash
agent-browser get url                                   # #/room/ops -> #/room/ops/topic/cpi-print-aug
agent-browser snapshot -c | grep -i heading             # "#ops" -> "Back to #ops Topic CPI print — Aug, followed"
agent-browser snapshot -c | grep -i textbox             # "Message #ops" -> "Message in CPI print — Aug"
```

The composer's accessible name is the side effect worth capturing: it proves
the navigation retargeted the *write* path, not only the read pane.

## Gotchas

- **`?room=` is ignored on `?view=room`.** It only applies to
  `?view=public`. `?view=room&room=btc` silently lands on `#ops`, and a
  screenshot captioned "btc" would be wrong.
- The rail renders the **same three topic titles under every channel**. That is
  fixture seeding, not a bug — do not report it, and do not use topic title
  alone to identify which channel you are in.
- `?alerts=` defaults to firing. Without `alerts=quiet` an app-wide strip sits
  above the content card and every vertical measurement below it shifts.
- Topic rows are `treeitem`, not `button` or `link`. `find role button` will not
  match them.
- "Search or jump to…" in the sidebar is **inert** in the fixture. Clicking it
  opens nothing; there is no quick-switcher dialog to drive here.
