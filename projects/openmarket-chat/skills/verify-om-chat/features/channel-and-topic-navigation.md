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
- **Mark As Unread** on a channel or topic row (`503a0a4f`), the inverse of
  Mark As Read: the row turns unread again from the newest message in its own
  lane, skipping your own trailing posts. It is offered only on a row that is
  fully read (no unread, no mention) and has a message, and never on a DM
  (`packages/chat-ui/src/lib/mark-latest-unread.ts`).
- The channel header, which is **four** separate mechanisms, not one list:
  - a `tablist` named "Channel view" holding **Chat** and **Topics**. The
    Topics tab carries the open-topic count in its accessible name when the
    count is positive (for example, **Topics 6** in the seeded room);
  - a standalone Alerts beacon `button`, whose name carries its state
    (`Alerts: nothing firing`, `Alerts: 3 feeds are ringing`, and a third
    state for tuning, `Alerts: 2 feeds need an answer` —
    `AlertsBeacon.tsx:58-61`);
  - an Inbox `button`, whose name also carries its count
    (`Inbox: 9 unread`);
  - the search cluster — `Open search in #ops`, a `combobox` named
    `Search #ops`, and `Open search panel`
    ([search-and-filters.md](search-and-filters.md)).
  To-dos is none of those — it survives as a menu item behind "More channel
  actions", with a state-dependent **Show to-dos** / **Hide to-dos** name.
  **Pins and bookmarks are no longer menu items**: `#740` gave them rail doors
  and dropped them from here. Menu contents depend on session capabilities and
  state; compact mode adds **Topic inbox** and compact actions, so the menu has
  no fixed item count (overflow items around `ChannelHeaderMenus.tsx:535-560`,
  the `More channel actions` trigger at `:598-599`). **Notification
  settings** has its own submenu (`ChannelHeaderMenus.tsx:158`). **Clean up
  topics** is available only where a daemon can triage topics, so it is absent
  from the source fixture. See [topic-cleanup.md](topic-cleanup.md).
- The right-panel **dock**, which is no longer in the header at all. `#694`
  moved it out to its own `nav` named **"Panel functions"**
  (`packages/chat-ui/src/components/RightPanels.tsx:213`): a collapse/expand toggle plus one
  button per panel. In the seeded fixture room that is **four** — Library,
  Bookmarks, Members, Pins — carrying `data-slot-tab` values `library`,
  `bookmarks`, `members`, `pins`. The dock filters
  `["todos","library","bookmarks","members","pins","alerts"]` (`RightPanels.tsx:198`)
  against what `rightSlotTabsFor` offers; `alerts` is admitted now, but the
  fixture offers none, so four is still the count here. **To-dos can never appear here**, and not because this room lacks
  one: the personal doors come from `session.rightRailTabs?.(room)`
  (`ChannelToolbar.tsx:229`), which the fixture never stubs, so it resolves
  through the `INERT` proxy — and `INERT[Symbol.iterator]` is an empty
  generator (`shell-fixture.tsx:2539`, the iterator at `:2541-2542`), so
  spreading it yields nothing for every room. Four is the ceiling in this lane, not a seeding accident.
  `"Show or hide side panel"` no longer exists anywhere in `src/`, and the old
  in-panel `tablist` is not merely hidden: every live render site passes
  `showSlotTabs={false}`, so it is dead on every route.
- The **topics primer** on a channel's topic list (`TopicPrimer`,
  `TopicListView.tsx:214`; `div.topic-primer[data-topic-primer]`): "Topics keep
  a long conversation in its own lane, so the channel stays readable. Start one
  below, or from any message with **Turn into topic**." with **New topic** and
  **Dismiss the topics explainer**. Dismissing writes `topicsPrimerSeen` and
  survives reload. Since `cb3e5274` a one-line banner sits on a 28 px row
  (`--topic-primer-row`) with even 12 px padding, and the icon and the dismiss
  glyph both sit 12 px from the edges; on a phone the dismiss hit box is 44 px.
- The desktop rail lives in a `complementary` landmark named **Workspace
  navigation** holding the `nav` **Workspaces, agents and people**, which no
  longer carries `role="toolbar"` (`Shell.tsx:3746`, `:3755`; `01bf4481`). Locate the rail
  by those names, not by a toolbar role.
- Message deep links (`#/room/<name>/msg/<seq>`) jump to and flash the message; the **New topic** draft pane (`TopicDraftPane.tsx`, `panel=topic-draft`).

## How to get to it (user POV)

You are in `#ops`. The sidebar lists your channels; under each one sit its live
topics with unread badges. You click a topic — the pane switches to that
topic's conversation, a breadcrumb appears at the top, and the message box now
says it will post into the topic rather than the channel. You click **Back to
#ops** and you are back where you started, composer included.

## Driving it with control-om-chat

```bash
cd /Users/dboon/gitlab/openmarket-chat
export OM_CHAT_LANE_PORT=<your assigned 18097-18197 port>
control-om-chat up
export AGENT_BROWSER_SESSION=verify-nav
agent-browser set viewport 1440 900
agent-browser open "$(control-om-chat url \
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

### Message deep link and New topic pane (added 2026-10-27)

- **Deep link:** load `shell-fixture.html?alerts=quiet#/room/ops/msg/105` with the hash present **at load**; the fixture only seeds a hash when it is empty (`shell-fixture.tsx:2408`). Afterwards `document.documentElement.dataset.messageJump` is `"105"` and the hash is rewritten to `#/room/ops`. On `/chat/`, `messageJump` was also `"105"` but the hash came back empty. An unknown seq should toast "Message link: that message is gone" (`src/lib/routing.ts:607-609`); that was not driven. Push-tap delivery needs the daemon-served rig.
- **New topic pane:** `shell-fixture.html?view=room&alerts=quiet&panel=topic-draft` mounts an aside named **New topic**. Creating the topic was not driven.

Verified 2026-10-27 at `6c15b0fb` (maintenance pass, fixture lane). Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261027/r1/` (frame 25).

### Topic inbox panel and Resolve (added 2026-10-28)

- **Topic inbox:** `shell-fixture.html?view=room&topics=on&panel=inbox&alerts=quiet` mounts an `aside` named **Inbox** with `data-right-panel="inbox"` (`RightPanels.tsx:381`). It reads "Inbox 9", with a `#OPS` group, a stream row (4), **ETF flows, week of the 28th** (2) and **CPI print — Aug** (3). Its buttons are **Close inbox**, **Mark #ops read**, **Topic <name>, followed** and **Mark <name> read**, and its footer hints `⌘⇧U inbox`, `⌥⇧↓ next unread` and `Esc close`. `?inbox=open` only sets `session.inboxOpen` (`shell-fixture.tsx:3117-3119`), and the fixture's `toggleInbox` flips only that flag (`:3419`). So neither `?inbox=open` nor the **Inbox: 9 unread** button opens the panel here: use `panel=inbox`. `TopicCatchUp` is only the keyboard host for those chords and renders nothing. Driven on `/rooms/` and `/chat/`. The mark-read effects are fixture no-ops.
- **Resolve a topic:** open a topic row's menu as described in Gotchas (Mark As Unread), then choose **Resolve <topic> (closes the conversation; the history stays)** (`TopicPill.tsx:146-149`). It opens a `dialog` named **Resolve <topic>**, for example **Resolve Funding flipped negative on Hyperliquid**. The dialog has an optional "What settled it?" note and **Resolve Topic** (`TopicResolvePopover.tsx:113-114`). The fixture implements `openTopicResolvePrompt` (`shell-fixture.tsx:3551`). **Resolve Topic** itself was not pressed. Driven on `/rooms/` and `/chat/`. **Add People...** has no route, because the fixture sets `topicAddPicker: null` (`:3301`).

Verified 2026-10-28 at `2dd7aad1` (nightly maintenance, fixture lane). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261028/r1/` (frames 09, 36-37, 41, 43).

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
- **The topic-count control is no longer a control.** It used to be a `button`
  named `6 open topics. Cycle topic rows` that cycled hidden → yours → all.
  `#781` deleted the whole cycling feature — `cycleTopicList`, `TopicListMode`
  and the persisted `topicsAllOpen` state went with it. What is left is a plain
  `<span class="channel-topic-cycle" data-channel-topic-count title="6 open
  topics">`: no role, no `aria-label`, not focusable.
  `find role button --name "6 open topics. Cycle topic rows"` now fails with
  "none match name". Read the `title`, or the `[data-channel-topic-count]`
  attribute, if you need the count. "Hide this channel's topics" is a separate
  control and still works.
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
  (`RightPanels.tsx:160`), which is a viewport distinction, not an open one.
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
  (`RightPanels.tsx:204`) rather than on whether a panel is open. `#715` added
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
  `TopicPeekPane` — was not in its diff at all. The Playwright suite is not
  part of the merge gate
  (`lint && typecheck && build && check-dist && test-fast`), which is how it
  rotted unnoticed. Do not spend a run rediscovering this, and do not report it
  as caused by your change.

  **Both mounts exist, and neither renders on the fixture.** An earlier pass read
  the `Shell.tsx` fallback (`:4213-4221`, gated on
  `!conversationRowOwnsRightRegion`) as the only mount and called the empty pane a
  designed outcome. That was wrong. The row-owned mount has been in
  `ConversationRightRegion` since `f190644c` (`RightPanels.tsx:293-300`: gated
  on `session.topicPeek`, `active.kind === "room"`, a matching room and
  `!panelOverlay`; the region itself returns null on mobile or outside a room or
  DM, `:280-288`), and `ChatPane.tsx:1155` and `:1845` render that region. On
  2026-10-28 at `2dd7aad1`, `?view=room&peek=cpi-print-aug`,
  `?view=room&topics=on&peek=cpi-print-aug` and
  `?view=topics&topics=on&peek=cpi-print-aug` at 1440×900 all left no
  `role=region` and no `.topic-peek*` node. The fixture's `openTopicPeek`
  (`shell-fixture.tsx:3354`) does set `topicPeek` and emit. Why the pane stays
  empty was not traced; `TopicPeekPane` reads `session.topics.railViewFor` or
  `inboxFor` (around `TopicPeekPane.tsx:123-128`), which is the next thing to
  check. Clicking a message's topic pill (**Open topic CPI print — Aug, …**)
  opened the topic in the main pane instead. Keep the row `live verification
  pending`, and do not report it as a product bug until a real host is checked.
- "Search or jump to…" in the sidebar is **inert** in the fixture. Clicking it
  opens nothing — confirmed live. But that is a fact about the *control*, not
  about the surface: **`?switcher=open` mounts the quick-switcher**
  (`shell-fixture.tsx:3033` seeds `palette`), and it comes up with real
  content — a `div.quick-switcher` carrying `role="combobox"`, an input
  placeheld `Search messages, or jump anywhere...`, and the empty state
  *"Nowhere recent yet. Type to search, or start with @, #, * or ."* with its
  PROTIP line beneath. So there **is** a switcher to drive here; it just does
  not open from the thing that looks like it opens it. Driven at `cd9f8c72`:
  fill the textbox `Search messages, or jump anywhere...` with `#mac`, and the
  listbox offers the macro topics; Enter jumps to
  `#/room/macro/topic/basis-desk-review` with the heading `#macro / Basis desk
  review`. Type through `find role textbox fill --name ...`; a CSS
  `[aria-label=...]` selector does not match, because the name comes from the
  placeholder.
- **Mark As Unread is gated by state, and the click is a no-op here.** The
  sidebar row menu (right-click a channel or topic `treeitem`) spells it
  **Mark As Unread**; the channel header menus spell it **Mark as unread**.
  Match case-insensitively. In the default dial-on fixture every channel row
  carries unread, so no channel row offers it; the fully read topic row
  `Funding flipped negative on Hyperliquid` does, and `CPI print — Aug` (3
  unread) does not. Load `?policy=off` to see it on channel rows and after
  `Mark as read` in `More channel actions`. **Mark as read** does not clear the
  seeded unread either: the fixture stubs `markRoomRead` and `markUnreadFrom`
  as `noop` (`shell-fixture.tsx:3431`, `:3562`). Prove the offer and its gating
  here, never the state change. That needs the daemon-pair lane.
  A synthetic `contextmenu` dispatched on the `treeitem` itself opens nothing;
  dispatch it on the row's inner `button`. The topic row menu then lists Unfollow,
  Mute, Copy link, **Resolve <topic> (closes the conversation; the history
  stays)**, Open Topic, Import Folder..., **Mark As Unread**, Rename, Create Doc
  from Topic, Set topic index... and Delete Topic (re-driven 2026-10-28 on both
  hosts).
- **A panel button renames itself when open**, Library included: after the
  click, `Library` reads `Close Library` and `data-library-presentation` is
  `side`.
- The **Open World** row above `DESK` is inert here too. It renders as a
  `treeitem` in its own `tree`, but clicking it leaves the route on
  `#/room/ops` and mounts no canvas — the shell fixture never stubs the world
  session port. Drive that surface from its own harness instead
  ([open-world.md](open-world.md)).
- **The topics primer shows only while `topicsPrimerSeen` is unset.** Once a
  session dismisses it, every later load in that browser hides it. Clear
  `localStorage` before capturing the banner.

### Verification record

**Last verified:** 2026-10-28 (nightly maintenance). **Product commit:** `2dd7aad1` (origin/main). **Scope:** The CPI topic treeitem gave `#/room/ops/topic/cpi-print-aug` and the composer **Message in CPI print — Aug**; **Back to #ops** gave `#/room/ops`. `?switcher=open` mounted `.quick-switcher` (`role=combobox`, placeholder "Search messages, or jump anywhere...", "Nowhere recent yet."), and `#mac` then Enter reached `#/room/macro/topic/basis-desk-review`. The deep link `#/room/ops/msg/105`, present at load, set `messageJump=105` and rewrote the hash to `#/room/ops`. `panel=topic-draft` mounted the **New topic** aside. `?view=topics` showed the primer with 12 px padding. The topic row menu offered **Mark As Unread** on the read topic, and the inbox panel and Resolve dialog rendered (section above), on both hosts. **Limitations:** The topic peek still renders nothing (Gotchas), the dock was not re-driven, and Mark As Unread effects are fixture no-ops. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261028/r1/` (frames 01, 04, 08-09, 36-37, 41, 43).

**Previous record:** 2026-10-27. **Product commit:** `6c15b0fb286e9dc1b6cb130c9c97cd7e0afa9254` (origin/main). **Scope:** The CPI topic treeitem gave `#/room/ops/topic/cpi-print-aug`, and **Back to #ops** gave `#/room/ops`; `aside[aria-label="Workspace navigation"]` held the rail `nav` with no role. `?switcher=open` mounted the switcher with its empty state; `#mac` then Enter reached `#/room/macro/topic/basis-desk-review`. `?view=topics` showed the primer at 52 px with 12 px padding on every side and both glyphs 12 px from the edges; dismissing it survived reload, and at 390×844 the dismiss hit box was 44×44. On `/chat/`, the primer had 12 px top and bottom padding, and the CPI topic reached `/chat/room/ops/topic/cpi-print-aug`. **Limitations:** Mark As Unread, the dock and the channel menu were not re-driven; Mark As Unread effects remain fixture no-ops. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261027/r01/` (frames 02-03, 20, 38-39). Previous record: 2026-10-26 at `5820fbea`.
