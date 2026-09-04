# Channel and topic navigation

Moving between a server's channels, and between a channel and one of its
topics. The most-driven surface in the app and the cheapest one to prove.

## Sub-features

- Channel list in the sidebar, grouped by section (`DESK`), with unread and
  mention counts on each row.
- Expanding and collapsing a channel's topic rows ("Hide this channel's
  topics", "6 open topics. Cycle topic rows").
- Opening a topic from the rail, and the `All N topics in <channel>` overflow
  row.
- The topic view's breadcrumb and its **Back to #channel** return.
- The composer retargeting to whatever is open.
- The channel header, which is **four** separate mechanisms, not one list:
  - a `tablist` named "Channel view" holding exactly two tabs, **Chat** and
    **Topics 6**;
  - a standalone Alerts beacon `button`, whose name carries its state
    (`Alerts: nothing firing`, `Alerts: 3 feeds are ringing`);
  - an Inbox `button`, whose name also carries its count
    (`Inbox: 9 unread`);
  - the search cluster — `Open search in #ops`, a `combobox` named
    `Search #ops`, and `Open search panel`
    ([search-and-filters.md](search-and-filters.md)).
  Pins, bookmarks and to-dos are none of those — they are menu items behind
  "More channel actions".
- The right-panel **dock**, which is no longer in the header at all. `#694`
  moved it out to its own `nav` named **"Panel functions"**
  (`src/components/RightPanels.tsx:153-218`): a collapse/expand toggle plus one
  button per panel — **Members** and **Library** in the seeded fixture room,
  plus **To-dos** where the room has one; `alerts` is deliberately filtered
  out. `"Show or hide side panel"` no longer exists anywhere in `src/`. The old
  in-panel `tablist` is not merely hidden: every live render site passes
  `showSlotTabs={false}`, so it is dead on every route.

## How to get to it (user POV)

You are in `#ops`. The sidebar lists your channels; under each one sit its live
topics with unread badges. You click a topic — the pane switches to that
topic's conversation, a breadcrumb appears at the top, and the message box now
says it will post into the topic rather than the channel. You click **Back to
#ops** and you are back where you started, composer included.

## Driving it with control-om-chat

```bash
cd /Users/dboon/github/openmarket-chat
export OM_CHAT_LANE_PORT=<your assigned 18097-18197 port>
./control-om-chat up
export AGENT_BROWSER_SESSION=verify-nav
agent-browser set viewport 1440 900
agent-browser open "$(./control-om-chat url \
  'tools/visual/shell-fixture.html?view=room&alerts=quiet')"
```

Routes:

| Route | State |
|---|---|
| `shell-fixture.html?view=room&alerts=quiet` | `#ops` with six open topics in the rail |
| `shell-fixture.html?view=topics` | The channel's topic **list** surface |
| `shell-fixture.html?view=topic&topic=cpi-print-aug` | One topic's own chat, entered directly |
| `shell-fixture.html?view=room&channels=many` | Long channel list — sidebar overflow and scroll |
| `shell-fixture.html?view=room&bulk=120` | A loaded tape, for scroll and virtualisation work |
| `shell-fixture.html?view=room&topics=on&peek=cpi-print-aug` | Topic open in the right sidebar rather than the main pane — **not rendering today, see Gotchas** |

Handles that resolve today:

```bash
agent-browser find role treeitem click --name "CPI print — Aug, 2 mentions, 3 unread"
agent-browser find role treeitem click --name "channel ops, 4 unread, 5 unread in topics"
agent-browser find role treeitem click --name "All 6 topics in ops"
agent-browser find role button   click --name "Back to #ops"
agent-browser find role button   click --name "Hide this channel's topics"
agent-browser find role button   click --name "6 open topics. Cycle topic rows"
agent-browser find role button   click --name "More channel actions"   # then pins/bookmarks/to-dos

# The right-panel dock. This name flips with state — see Gotchas. The dock's
# collapse toggle is NOT driveable here; do not reach for "Expand panel".
agent-browser find role button   click --name "Members"
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
  match them. **This includes the `All N topics in <channel>` overflow row** —
  it looks like a button and is not one, and `find role button` fails on it
  with "none match name".
- The topic-count control's full accessible name is `6 open topics. Cycle topic
  rows`, not `Cycle topic rows`. An `--exact` match on the short form finds
  nothing.
- Alerts is a `button`, not a third tab. `find role tab --name "Alerts"` fails,
  and the name changes with state, so match on the `Alerts:` prefix rather than
  a fixed string.
- **The dock's panel buttons rename themselves.** Each is `"Members"` when that
  panel is shut and `"Close Members"` when it is open — `RightPanels.tsx` builds
  the name as *closes ? "Close " + label : label*. The container classes do
  **not** move with state, whatever an older reading of this file said:
  `.right-panel-dock-standalone > nav.right-panel-dock` is nested and present
  in both states at desktop width, because `#715` hoisted the dock into
  `ConversationRightRegion` where it renders unconditionally. The bare `nav`
  without its wrapper appears only under the mobile overlay
  (`RightPanels.tsx:150`), which is a viewport distinction, not an open one.
  Drive the stable hooks —
  `[data-slot-tab="members"]` and `[data-slot-tab="library"]`, reading
  `aria-pressed` for which panel is open. That pair still works: clicking
  Members flips `aria-pressed` to `true`, renames the button, and puts a
  `.right-panel-drawer` on screen.
- **The dock's collapse toggle is dead in this lane, and lies about its state.**
  It reads `"Collapse panel"` even with the panel plainly shut, `"Expand panel"`
  never appears, `aria-expanded` is not rendered at all, and clicking it changes
  nothing. Do not build a proof on it and do not report it as a product bug.

  `#715` rebuilt the toggle around a right *region* that stays open while the
  panel collapses, so the label now keys on `session.rightRegionOpen()`
  (`RightPanels.tsx:187`) rather than on whether a panel is open. `#715` added
  that seam and `#735` swapped its body to route through `rightRegionTenant`,
  which is why a docked note counts as open and a topic peek does not. The
  fixture stubs none of `rightRegionOpen`, `collapseRightRegion` or
  `expandRightRegion`, so all three fall through to the `INERT` proxy: truthy
  for the label, a no-op for the click, and not a boolean — which is why React
  drops `aria-expanded` instead of printing it. Spelling those three out in
  `tools/visual/shell-fixture.tsx` is what would fix it.

  The split within one dock is the useful lesson. Its panel buttons read
  `rightRegionTenant(session)`, which branches on `session.rightPanel` — a
  **field** the fixture spells out, so it yields real booleans and
  `aria-pressed` works. The toggle calls `session.rightRegionOpen()` — a
  **method** the fixture never mentions, so it yields `INERT`. Stubbed field
  versus unstubbed method, same component, opposite outcomes: when half a
  control works and half does not, that is the first thing to check.
- **The topic peek pane does not render right now.** `?peek=<topicId>` is read
  (it seeds `session.topicPeek`), and the gate needs `active.kind ===
  "room"`, a matching room, and a viewport wider than the `max-width: 1099px`
  overlay query — all satisfied at 1440×900. `[data-topic-peek]` is still
  absent. This is not a query you are getting wrong: the repo's own
  `tools/visual/topic-peek-drop.visual.ts` drives the identical URL and fails
  on `expect(pane).toBeVisible()`, and it fails on `main` as far back as
  `25fe4e6b`, and still fails at `50a5b29f`. Do not read `#689` ("unify the peek
  hover machine into PeekIntent") as a fix for it: that commit touches
  `channel-peek.ts` and `dm-peek.ts`, the sidebar **hover popovers**, which are
  a different mechanism from the topic side pane. This seam —
  `?peek=` → `fixtureTopicPeek` → `session.topicPeek` → the gate →
  `TopicPeekPane` — was not in its diff at all. The gate itself did move,
  though: `#731` lifted it out of `Shell.tsx` into `ConversationRightRegion`
  (`RightPanels.tsx:241`), byte-identical, now called from `ChatPane.tsx` and
  `TopicListView.tsx` rather than from one Shell site. Same boolean, new owner —
  look there when it next needs checking. The Playwright suite is not
  part of the merge gate
  (`lint && typecheck && build && check-dist && test-fast`), which is how it
  rotted unnoticed. Do not spend a run rediscovering this, and do not report it
  as caused by your change — but do check whether it has been fixed before
  planning a proof that needs the peek pane.
- "Search or jump to…" in the sidebar is **inert** in the fixture. Clicking it
  opens nothing; there is no quick-switcher dialog to drive here.
- The **Open World** row above `DESK` is inert here too. It renders as a
  `treeitem` in its own `tree`, but clicking it leaves the route on
  `#/room/ops` and mounts no canvas — the shell fixture never stubs the world
  session port. Drive that surface from its own harness instead
  ([open-world.md](open-world.md)).
