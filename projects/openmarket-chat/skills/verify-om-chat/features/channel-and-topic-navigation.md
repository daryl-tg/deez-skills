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
  (`packages/chat-ui/src/components/RightPanels.tsx:214`): a collapse/expand toggle plus one
  button per panel. In the seeded fixture room that is **four** — Library,
  Bookmarks, Members, Pins — carrying `data-slot-tab` values `library`,
  `bookmarks`, `members`, `pins`. The dock filters
  `["todos","library","bookmarks","members","pins","alerts"]` (`RightPanels.tsx:199`)
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
  longer carries `role="toolbar"` (`Shell.tsx:3736`, `:3745`; `01bf4481`). Locate the rail
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
| `shell-fixture.html?view=room&topics=on&peek=cpi-print-aug` (`/chat/`), plus `#/room/ops/topic/cpi-print-aug` on `/rooms/` | Topic peek beside the stream — see Gotchas for why `/rooms/` needs the hash |

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

- **Deep link:** load `shell-fixture.html?alerts=quiet#/room/ops/msg/105` with the hash present **at load**; the fixture only seeds a hash when it is empty (`shell-fixture.tsx:2409`). Afterwards `document.documentElement.dataset.messageJump` is `"105"` and the hash is rewritten to `#/room/ops`. On `/chat/`, `messageJump` was also `"105"` but the hash came back empty. An unknown seq should toast "Message link: that message is gone" (`src/lib/routing.ts:619-621`); that was not driven. Push-tap delivery needs the daemon-served rig.
- **New topic pane:** `shell-fixture.html?view=room&alerts=quiet&panel=topic-draft` mounts an aside named **New topic**. Creating the topic was not driven.

Verified 2026-10-27 at `6c15b0fb` (maintenance pass, fixture lane). Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261027/r1/` (frame 25).

### Topic inbox panel and Resolve (added 2026-10-28)

- **Topic inbox:** `shell-fixture.html?view=room&topics=on&panel=inbox&alerts=quiet` mounts an `aside` named **Inbox** with `data-right-panel="inbox"` (`RightPanels.tsx:382`). It reads "Inbox 9", with a `#OPS` group, a stream row (4), **ETF flows, week of the 28th** (2) and **CPI print — Aug** (3). Its buttons are **Close inbox**, **Mark #ops read**, **Topic <name>, followed** and **Mark <name> read**, and its footer hints `⌘⇧U inbox`, `⌥⇧↓ next unread` and `Esc close`. `?inbox=open` only sets `session.inboxOpen` (`shell-fixture.tsx:3117-3119`), and the fixture's `toggleInbox` flips only that flag (`:3419`). So neither `?inbox=open` nor the **Inbox: 9 unread** button opens the panel here: use `panel=inbox`. `TopicCatchUp` is only the keyboard host for those chords and renders nothing. Driven on `/rooms/` and `/chat/`. The mark-read effects are fixture no-ops.
- **Resolve a topic:** open a topic row's menu as described in Gotchas (Mark As Unread), then choose **Resolve <topic> (closes the conversation; the history stays)** (`TopicPill.tsx:146-149`). It opens a `dialog` named **Resolve <topic>**, for example **Resolve Funding flipped negative on Hyperliquid**. The dialog has an optional "What settled it?" note and **Resolve Topic** (`TopicResolvePopover.tsx:113-114`). The fixture implements `openTopicResolvePrompt` (`shell-fixture.tsx:3551`). **Resolve Topic** itself was not pressed. Driven on `/rooms/` and `/chat/`. **Add People...** has no route, because the fixture sets `topicAddPicker: null` (`:3301`).

Verified 2026-10-28 at `2dd7aad1` (nightly maintenance, fixture lane). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261028/r1/` (frames 09, 36-37, 41, 43).

### Mute and the sidebar row cluster (added 2026-10-29)

- **Mute a channel:** hover a sidebar channel row and press **More options for
  <name>**. The menu's **Mute** tile is named **Choose how long to mute
  #<name>** (`Sidebar.tsx:414`). Clicking it (hover does not open it) opens a
  submenu with 15m / 1h / 8h / 24h / **Until unmuted**; a muted channel also offers
  **Unmute channel** (`:433`). The same verb sits in the channel header menu as
  **Mute channel** with a **Mute for** chip row (`ChannelHeaderMenus.tsx:175`,
  `:374`), as **Mute conversation** for a DM (`:336`), as **Mute <topic>** on a
  topic pill (`TopicPill.tsx:126`) and on the server menu's quick bar
  (`ServerMenu.tsx:90-95`).
- **What the fixture can show:** only the offer. `session.setRoomAttention` is
  unstubbed in both shell fixtures, so choosing a duration closes the menu with
  no state change and no toast, and `roomAttentionFor` / `roomMuteUntilFor`
  answer `null`. Since `4ca34c9a`, muting a room this socket never joined (an
  alert channel never opened this session) retries over REST after the relay's
  `NOT_IN_ROOM` refusal (`lib/session.ts:35616`, `:35711`). That path is
  covered only by `packages/chat-ui/test/ui/mute-durations.test.ts`. The topic
  pill's mute is stubbed (`tools/visual/shell-fixture.tsx:2950-2960`, writes
  `data-fixture-topic-attention`), but it is a different code path.
- **Topic chevron on hover (`357b2df5`):** a row's right-edge cluster (badge,
  hover actions, topic chevron) is `shrink-0` (`Sidebar.tsx:3489`), so when the
  hover actions **Invite people to <name>**, **Edit <name>** and **More options
  for <name>** appear, the label truncates and the chevron stays put. No seeded
  name is long enough at the default width. Narrow the sidebar first:

  ```bash
  agent-browser eval '(()=>{localStorage.setItem("om.chat.sidebarWidth","200");return 1})()'
  agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=room&alerts=quiet&channels=many&topics=on')"
  # read .topic-side-toggle getBoundingClientRect().left on the options-flow row,
  # hover the row, read it again: equal before and after (x=232 on 2026-10-29)
  agent-browser eval '(()=>{localStorage.removeItem("om.chat.sidebarWidth");return 1})()'
  ```

  The width key is sticky, like `message=cozy`; remove it before any other
  capture. Hover-action names carry no `#`.

### Channel and DM hover peeks (added 2026-10-29)

A hover peek previews a conversation without opening it or marking it read. It
is desktop only. The fetch starts at 440 ms, the popover shows at 500 ms, and
it closes 120 ms after the pointer leaves (`lib/channel-peek.ts:26-28`).
Keyboard focus on the row opens it too. While a row menu is open, or during a
drag, peeks are off (`Sidebar.tsx:2561-2564`).

- **Channel peek:** on `shell-fixture.html?view=room&alerts=quiet`, run
  `agent-browser find role treeitem hover --name "channel signals, 4 unread, 5 unread in topics"`
  and wait about 1.5 s. This mounts a `dialog` named **Preview of signals**
  (`ChannelPeekPopover.tsx`) with an **Open** head (title "Open the channel"),
  **You're caught up**, the three topic rows and the footer "Peeking never
  marks as read". That is on `/rooms/`, where `peekChannel` is stubbed
  (`shell-fixture.tsx:2826`). The `/chat/` fixture has no `peekChannel`, so the
  same hover leaves the popover on its **Loading preview** skeleton.
- **DM peek:** hover the rail face **Direct message with ana, 2 unread**. This
  mounts dialog **Conversation with ana** (`DmPeekPopover.tsx`) with the two
  seeded messages, a textbox **Reply to ana** and the footer "Enter sends · Esc
  closes · Open marks read". Escape closes it. The head **Open** (title "Open
  the conversation") routes to `#/dm/ana` on `/rooms/` and `/chat/dm/ana` on
  `/chat/`. Driven on both hosts. To reopen it, move the pointer off the face
  and back: hovering the same element again does nothing. Sending from the
  reply box is unproved, because `sendDmTo` is unstubbed.

Verified 2026-10-29 at `cdfb1b0f` (scheduled maintenance). Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261029/r1/` (`peek-*`).

### Remove someone from a topic, and Delete Topic (added 2026-10-30)

`2a49cebf` lets a topic's creator, or anyone holding `remove-member`, take a
person off a **public** topic too; before, only private topics had removal.
Who may remove, and the confirm's words, follow the topic kind
(`lib/topic-member-remove.ts`). There are two doors: the roster row's hover
button **Remove <handle> from this topic** (`RightPanels.tsx:1766-1790`) and
the member menu item **Remove from Topic** (`UserContextMenu.tsx:644`). Since
`82badafc` the menu item draws the person-minus glyph, not trash.

- **Private topic (driveable):** load
  `shell-fixture.html?view=topic&topic=basis-desk-review&panel=members&topics=on&alerts=quiet`.
  The members panel lists **Remove ana / dax / mira from this topic** (none
  for `kyle`, who is you). **Remove ana from this topic** opens an
  `alertdialog` **Remove from private topic?** reading "ana loses access to
  this topic and it disappears from their sidebar. You can add them back any
  time." with **Cancel** and **Remove**. **Remove** closes it and changes
  nothing, because `removeTopicMember` is unstubbed. A failure would toast
  `Remove failed: <userFacingErrorText>` (`1c7c90e7`).
- **Public topic (source-only):** the public confirm is **Remove from topic?**
  ("… leaves this topic's member list and stops getting its notifications.
  They stay in the channel …"). No fixture reaches it. See the Gotchas entry
  on `panel=members` for a public topic.
- **The member menu does not open in the fixture.** The shell fixture sets
  `userMenu: null` and never stubs `openUserMenu`, so a right-click on a
  roster row opens nothing. **Remove from Topic** and its glyph are
  source-only there.
- **Delete Topic:** dispatch `contextmenu` on the topic row's inner `button`
  (e.g. **Funding flipped negative on Hyperliquid**), then pick **Delete
  Topic**. The `alertdialog` **Delete ⌗ <topic>** now reads "The topic and all
  of its messages are deleted. This cannot be undone." (`edbb7153`; it used to
  say the messages return to the channel). That commit's real change, keeping
  a removed or deleted topic's messages out of the channel, rides a relay
  `TOPIC_UPDATED` frame and is source-only (`lib/topic-lane.ts`).

Driven 2026-10-30 at `47cb13bf` on `/rooms/` (frames 16-19).

## Gotchas

- **`panel=members` on a public topic blanks the whole shell, on both hosts.**
  `?view=topic&topic=cpi-print-aug&panel=members&topics=on` leaves `#root`
  empty. The thrown error, read on `/rooms/`, is `session.topicFollowers(...)?.then is not a
  function` (`RightPanels.tsx:1376-1377`): the fixtures never stub
  `topicFollowers`, so the call answers `INERT`, whose `then` is not a
  function. No error boundary wraps `MemberList`. The same effect line was in
  `cdfb1b0f`, so this predates `2a49cebf`; it is a fixture gap, not that
  commit's regression. Use the private `basis-desk-review` seed for roster
  work.

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
  (`RightPanels.tsx:161`), which is a viewport distinction, not an open one.
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
  (`RightPanels.tsx:205`) rather than on whether a panel is open. `#715` added
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
- **The topic peek renders on both hosts, but each host needs its own URL.**
  Found and driven 2026-10-28 (maintenance) at `07f7d04c`, 1440×900:
  - **`/chat/`:** `shell-fixture.html?view=room&topics=on&peek=cpi-print-aug`
    mounts `[data-topic-peek="cpi-print-aug"]`, a 440 px pane beside the
    still-visible `Messages in stream` log, with its own log **Messages in CPI
    print — Aug** (2 rows) and the buttons **Previous topic**, **Next topic**,
    **Open topic and summon your om**, **Open full** and **Close the topic
    peek**.
  - **`/rooms/`:** the same query mounts nothing, because the hash router
    wipes the seed at boot. The fixture writes `#/room/ops`, and
    `src/lib/routing.ts:648-652` closes any open peek when the route equals the
    current view (the Browser-Back rule). Put the peeked topic in the hash
    instead: `shell-fixture.html?view=room&topics=on&peek=cpi-print-aug&alerts=quiet#/room/ops/topic/cpi-print-aug`.
    `routing.ts:634-647` keeps a peek whose topic matches the hash, so the
    pane mounts the same as on `/chat/`.
  - **On both hosts:** Escape closes the pane and returns the route to the
    parent room (`#/room/ops`, `/chat/room/ops`).
  - **Open full works on `/chat/` only.** There it promotes the peek to the full
    topic (heading `#ops/CPI print — Aug`, `/chat/room/ops/topic/cpi-print-aug`).
    The button (`TopicPeekPane.tsx:742-750`, accessible name **Open full**, title
    "Open this topic as the full view") calls `session.promoteTopicPeek`. Only
    the `/chat/` fixture stubs that (`apps/cloud/tools/visual/shell-fixture.tsx:1855`).
    The root fixture does not, so on `/rooms/` the call lands on `INERT`, and the
    pane stays open with heading `#ops`. Measured 2026-10-29 at `cdfb1b0f`, by
    role and by selector. This is a fixture gap, not a product fault; prove
    promotion on `/chat/`.

  Earlier passes recorded this as "renders nothing anywhere" because they only
  tried the bare query on `/rooms/`. The repo's own
  `tools/visual/topic-peek-drop.visual.ts` uses that bare URL, which explains
  its old failure. It was not run this pass. **Clicks that no longer peek:** a
  topic activity card in the stream, including its message count, always
  opens the full topic (`TopicActivityCard.tsx:151-163`). So
  `apps/cloud/tools/visual/topic-peek.visual.ts`, which clicks that count,
  reads as stale against source. It was not run either. In the fixture, the
  inbox panel's **Topic CPI print — Aug, followed** row did not open a peek on
  either host. Dedicated peek callers are the inbox (`TopicInbox.tsx:51-67`)
  and the to-dos panel.
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

**Last verified:** 2026-10-30 (nightly maintenance). **Product commit:** `47cb13bf` (GitLab origin/main; rooms-client 0.108.0). **Scope (`/rooms/`):** On the private topic `basis-desk-review` with `panel=members`, **Remove ana from this topic** opened **Remove from private topic?**, and **Remove** closed it with no change. The topic row menu's **Delete Topic** showed the new `edbb7153` body. `panel=members` on the public `cpi-print-aug` blanked the shell on `/rooms/` and `/chat/` with the `topicFollowers` error in Gotchas. **Limitations:** Only the delta above was driven tonight; the rest of this guide keeps its 2026-10-29 proof. Public-topic removal, the member menu and the glyph are source-only. Evidence is local only: `artifacts/vomc-nightly-20261030/r1/` (frames 16-19).

**Previous record:** 2026-10-29 (nightly maintenance). **Product commit:** `cdfb1b0f` (origin/main; rooms-client 0.108.0). **Scope:** Topic peek on `/rooms/` (`?view=room&topics=on&peek=cpi-print-aug&alerts=quiet#/room/ops/topic/cpi-print-aug`) mounted `[data-topic-peek="cpi-print-aug"]`, 440 px, with log **Messages in CPI print — Aug**. Escape returned `#/room/ops`. **Open full** did nothing on `/rooms/` (fixture gap, see Gotchas), and on `/chat/` it promoted the peek to `/chat/room/ops/topic/cpi-print-aug`, heading `#ops/CPI print — Aug`. Sidebar chevron (`357b2df5`): with `om.chat.sidebarWidth=200` and `?view=room&channels=many&topics=on`, hovering **options-flow** revealed **Invite people to options-flow**, **Edit options-flow** and **More options for options-flow**. The topic chevron stayed at x=232 while the label truncated (89→40 px on `/rooms/`, 86→40 px on `/chat/`). Channel row **More options for signals** → **Mute** (accessible name **Choose how long to mute #signals**) opened 15m / 1h / 8h / 24h / Until unmuted on both hosts. **Until unmuted** closed the menu with no visible state change and no toast. **Limitations:** Mark As Unread, the quick switcher, the deep link and the inbox were not re-driven. The mute effect, including the `4ca34c9a` REST fallback for never-joined rooms, is unit-test only, because `setRoomAttention` is unstubbed. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261029/r1/` (frames 05, 20–23, 48).

**Previous record:** 2026-10-28 (scheduled maintenance). **Product commit:** `07f7d04c` (origin/main). **Scope:** Topic peek on both hosts: `/chat/` `?view=room&topics=on&peek=cpi-print-aug` and `/rooms/` with `#/room/ops/topic/cpi-print-aug` mounted `[data-topic-peek="cpi-print-aug"]` beside the stream, with log **Messages in CPI print — Aug**; Escape closed it back to the parent room; **Open full** promoted it to `#ops/CPI print — Aug`. `?panel=inbox` rendered the inbox rows on both hosts. **Limitations:** Peek **Previous topic** / **Next topic**, the peek composer and drop target, and channel or DM hover peeks were not driven. The inbox topic row opened no peek in the fixture. The quick switcher, deep link, topic row menu and dock were not re-driven at this tree. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261028/r1/` (`*-topic-peek-*.png`).

**Previous record:** 2026-10-28 (nightly maintenance). **Product commit:** `2dd7aad1` (origin/main). **Scope:** The CPI topic treeitem gave `#/room/ops/topic/cpi-print-aug` and the composer **Message in CPI print — Aug**; **Back to #ops** gave `#/room/ops`. `?switcher=open` mounted `.quick-switcher` (`role=combobox`, placeholder "Search messages, or jump anywhere...", "Nowhere recent yet."), and `#mac` then Enter reached `#/room/macro/topic/basis-desk-review`. The deep link `#/room/ops/msg/105`, present at load, set `messageJump=105` and rewrote the hash to `#/room/ops`. `panel=topic-draft` mounted the **New topic** aside. `?view=topics` showed the primer with 12 px padding. The topic row menu offered **Mark As Unread** on the read topic, and the inbox panel and Resolve dialog rendered (section above), on both hosts. **Limitations:** The topic peek was recorded as rendering nothing (corrected above), the dock was not re-driven, and Mark As Unread effects are fixture no-ops. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261028/r1/` (frames 01, 04, 08-09, 36-37, 41, 43). Previous record: 2026-10-27 at `6c15b0fb`.