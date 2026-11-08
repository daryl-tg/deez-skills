# Channel and topic navigation

Moving between a server's channels, and between a channel and one of its
topics. The most-driven surface in the app and the cheapest one to prove.

## Sub-features

- Channel list in the sidebar, grouped by section (`DESK`), with unread and
  mention counts on each row.
- Expanding and collapsing a channel's topic rows ("Hide this channel's
  topics"); the "6 open topics" count beside it is a `title` only, no longer a
  control (see Gotchas).
- Opening a topic from the rail, and the `All N topics in <channel>` overflow
  row.
- The topic view's breadcrumb and its **Back to #channel** return.
- The composer retargeting to whatever is open.
- **Mark As Unread** on a channel or topic row (`503a0a4f`), the inverse of
  Mark As Read: the row turns unread again from the newest message in its own
  lane, skipping your own trailing posts. It is offered only on a row that is
  fully read (no unread, no mention) and has a message, and never on a DM
  (`packages/chat-ui/src/lib/mark-latest-unread.ts`).
- **Mark to revisit** on a channel or topic row (`c2933994`): a personal flag,
  separate from read state, that adds the row to a **Revisit** list behind a
  sidebar toggle. It is stored in `om.chat.revisit`, with at most 50 flags
  (`packages/chat-ui/src/lib/revisit.ts`). See Mark to revisit and the Revisit
  list below.
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
  (`packages/chat-ui/src/components/RightPanels.tsx:228`): a collapse/expand toggle plus one
  button per panel. In the seeded fixture room that is **four** — Library,
  Bookmarks, Members, Pins — carrying `data-slot-tab` values `library`,
  `bookmarks`, `members`, `pins`. The dock filters
  `["todos","library","bookmarks","members","pins","alerts"]` (`RightPanels.tsx:212`)
  against what `rightSlotTabsFor` offers; `alerts` is admitted now, but the
  fixture offers none, so four is still the count here. **To-dos can never appear here**, and not because this room lacks
  one: the personal doors come from `session.rightRailTabs?.(room)`
  (`ChannelToolbar.tsx:229`), which the fixture never stubs, so it resolves
  through the `INERT` proxy — and `INERT[Symbol.iterator]` is an empty
  generator (`shell-fixture.tsx:2541`, the iterator at `:2543-2544`), so
  spreading it yields nothing for every room. Four is the ceiling in this lane, not a seeding accident.
  `"Show or hide side panel"` no longer exists anywhere in `src/`, and the old
  in-panel `tablist` is not merely hidden: every live render site passes
  `showSlotTabs={false}`, so it is dead on every route.
- The **topics primer** on a channel's topic list (`TopicPrimer`,
  `TopicListView.tsx:216`; `div.topic-primer[data-topic-primer]`): "Topics keep
  a long conversation in its own lane, so the channel stays readable. Start one
  below, or from any message with **Turn into topic**." with **New topic** and
  **Dismiss the topics explainer**. Dismissing writes `topicsPrimerSeen` and
  survives reload. Since `cb3e5274` a one-line banner sits on a 28 px row
  (`--topic-primer-row`) with even 12 px padding, and the icon and the dismiss
  glyph both sit 12 px from the edges; on a phone the dismiss hit box is 44 px.
- The desktop rail lives in a `complementary` landmark named **Workspace
  navigation** holding the `nav` **Workspaces, agents and people**, which no
  longer carries `role="toolbar"` (`Shell.tsx:3784`, `:3794`; `01bf4481`). Locate the rail
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

- **Deep link:** load `shell-fixture.html?alerts=quiet#/room/ops/msg/105` with the hash present **at load**; the fixture only seeds a hash when it is empty (`shell-fixture.tsx:2411`). Afterwards `document.documentElement.dataset.messageJump` is `"105"` and the hash is rewritten to `#/room/ops`. On `/chat/`, `messageJump` was also `"105"` but the hash came back empty. An unknown seq should toast "Message link: that message is gone" (`src/lib/routing.ts:655-657`); that was not driven. Push-tap delivery needs the daemon-served rig.
- **New topic pane:** `shell-fixture.html?view=room&alerts=quiet&panel=topic-draft` mounts an aside named **New topic**. Creating the topic was not driven.

Verified 2026-10-27 at `6c15b0fb` (maintenance pass, fixture lane). Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261027/r1/` (frame 25).

### Topic inbox panel and Resolve (added 2026-10-28)

- **Topic inbox:** `shell-fixture.html?view=room&topics=on&panel=inbox&alerts=quiet` mounts an `aside` named **Inbox** with `data-right-panel="inbox"` (`TopicInbox.tsx:376`, mounted from the `rightPanel === "inbox"` branch at `RightPanels.tsx:403`). It reads "Inbox 9", with a `#OPS` group, a stream row (4), **ETF flows, week of the 28th** (2) and **CPI print — Aug** (3). Its buttons are **Close inbox**, **Mark #ops read**, **Topic <name>, followed** and **Mark <name> read**, and its footer hints `⌘⇧U inbox`, `⌥⇧↓ next unread` and `Esc close`. `?inbox=open` only sets `session.inboxOpen` (`shell-fixture.tsx:3119-3121`), and the fixture's `toggleInbox` flips only that flag (`:3437`). So neither `?inbox=open` nor the **Inbox: 9 unread** button opens the panel here: use `panel=inbox`. `TopicCatchUp` is only the keyboard host for those chords and renders nothing. Driven on `/rooms/` and `/chat/`. The mark-read effects are fixture no-ops.
- **Resolve a topic:** open a topic row's menu as described in Gotchas (Mark As Unread), then choose **Resolve <topic> (closes the conversation; the history stays)** (`TopicPill.tsx:148-151`). It opens a `dialog` named **Resolve <topic>**, for example **Resolve Funding flipped negative on Hyperliquid**. The dialog has an optional "What settled it?" note and **Resolve Topic** (`TopicResolvePopover.tsx:113-114`). The fixture implements `openTopicResolvePrompt` (`shell-fixture.tsx:3571`). **Resolve Topic** was pressed on 2026-10-31: the dialog closes with no toast and no row change, because the fixture's resolve is local. Driven on `/rooms/` and `/chat/`. **Add People...** has no route, because the fixture sets `topicAddPicker: null` (`:3306`).

Verified 2026-10-28 at `2dd7aad1` (nightly maintenance, fixture lane). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261028/r1/` (frames 09, 36-37, 41, 43).

### Mute and the sidebar row cluster (added 2026-10-29)

- **Mute a channel:** hover a sidebar channel row and press **More options for
  <name>**. The menu's **Mute** tile is named **Choose how long to mute
  #<name>** (`Sidebar.tsx:418`). Clicking it (hover does not open it) opens a
  submenu with 15m / 1h / 8h / 24h / **Until unmuted**; a muted channel also offers
  **Unmute channel** (`:434`). The same verb sits in the channel header menu as
  **Mute channel** with a **Mute for** chip row (`ChannelHeaderMenus.tsx:175`,
  `:374`), as **Mute conversation** for a DM (`:336`), as **Mute <topic>** on a
  topic pill (`TopicPill.tsx:128`) and on the server menu's quick bar
  (`ServerMenu.tsx:90-95`).
- **What the fixture can show:** only the offer. `session.setRoomAttention` is
  unstubbed in both shell fixtures, so choosing a duration closes the menu with
  no state change and no toast, and `roomAttentionFor` / `roomMuteUntilFor`
  answer `null`. Since `4ca34c9a`, muting a room this socket never joined (an
  alert channel never opened this session) retries over REST after the relay's
  `NOT_IN_ROOM` refusal (`lib/session.ts:35924`, `:36019`). That path is
  covered only by `packages/chat-ui/test/ui/mute-durations.test.ts`. The topic
  pill's mute is stubbed (`tools/visual/shell-fixture.tsx:2952-2962`, writes
  `data-fixture-topic-attention`), but it is a different code path.
- **Topic chevron on hover (`357b2df5`):** a row's right-edge cluster (badge,
  hover actions, topic chevron) is `shrink-0` (`Sidebar.tsx:3510`), so when the
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
it closes 120 ms after the pointer leaves (`lib/channel-peek.ts:27-29`).
Keyboard focus on the row opens it too. While a row menu is open, or during a
drag, peeks are off (`Sidebar.tsx:2580-2583`).

- **Channel peek:** on `shell-fixture.html?view=room&alerts=quiet`, run
  `agent-browser find role treeitem hover --name "channel signals, 4 unread, 5 unread in topics"`
  and wait about 1.5 s. This mounts a `dialog` named **Preview of signals**
  (`ChannelPeekPopover.tsx`) with an **Open** head (title "Open the channel"),
  **You're caught up**, the three topic rows and the footer "Peeking never
  marks as read". That is on `/rooms/`, where `peekChannel` is stubbed
  (`shell-fixture.tsx:2828`). The `/chat/` fixture has no `peekChannel`, so the
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
button **Remove <handle> from this topic** (`RightPanels.tsx:1791-1815`) and
the member menu item **Remove from Topic** (`UserContextMenu.tsx:760`). Since
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
- **Delete Topic:** dispatch `contextmenu` on the topic row's `.channel-row-identity`
  (e.g. **Funding flipped negative on Hyperliquid**), then pick **Delete
  Topic**. The `alertdialog` **Delete ⌗ <topic>** now reads "The topic and all
  of its messages are deleted. This cannot be undone." (`edbb7153`; it used to
  say the messages return to the channel). That commit's real change, keeping
  a removed or deleted topic's messages out of the channel, rides a relay
  `TOPIC_UPDATED` frame and is source-only (`lib/topic-lane.ts`).

Driven 2026-10-30 at `47cb13bf` on `/rooms/` (frames 16-19).

### Sidebar context menus (added 2026-10-31)

Right-click (a `contextmenu` event dispatched on the row's
`.channel-row-identity`) opens the menus below. The permission gate hides the
destructive verbs for the fixture viewer, so these lists are what a member
without manage rights sees. Driven on `/rooms/` (18135) and `/chat/` (18136)
at `936f5b64`.

- **Channel row** (`Sidebar.tsx:6123-6332`), 11 items on `signals` since
  `c2933994` (re-driven 2026-11-06 on both hosts): a
  notification tile named **Notification settings for #signals (Use server
  default)** (a submenu), **Link** (**Copy link to #signals**), **Mute**
  (**Choose how long to mute #signals**, a submenu with 15m / 1h / 8h / 24h /
  **Until unmuted**), **Browse Topics**, **Create Topic**, **Convert to
  alerts...**, **Edit Channel**, **Mark As Read**, **Mark to revisit** (it
  reads **Done revisiting** once flagged), **Import folder...** and
  **Copy channel ID**. **Archive Channel**, **Delete Channel...** and **Move
  to** / **Move up** / **Move down** need manage rights and do not render.
  **Create Topic** opens the dialog **Create Topic in #signals** with a
  **Make topic private** switch and **Create Topic** (`Modals.tsx:370`).
- **Category header** (`Sidebar.tsx:6360-6451`), 3 items on **category Desk,
  5 channels**: **Mark As Read**, **Collapse Category** and **Create Channel in
  Desk**. **Rename Category** and **Delete Category** need manage rights on
  every room in the category and do not render.
- **Server header** (`.sidebar-server-menu-trigger`, `aria-haspopup="menu"`,
  `ServerMenu.tsx:81-267`), 16 items on `/rooms/`: **Read** (**Mark every
  channel in Thanefield Capital as read · ⇧Esc**), **Mute** (**Mute Thanefield
  Capital until you turn it back on (timed mutes below)**), **Invite**, **Server Settings**,
  **Create Channel**, **Create Category**, **Server Library**, **Open World**,
  **Clean up topics**, **Notification Settings** (a submenu), the flat timed
  mutes **15m** / **1h** / **8h** / **24h** (named **Mute Thanefield Capital
  for 15 minutes** and so on), **Leave Server** and **Copy server ID**. On
  `/chat/` the same menu has 15 items: **Clean up topics** is daemon-only
  ([topic-cleanup.md](topic-cleanup.md)). **Create Channel** opens the dialog
  **Create channel** with a **Private channel** switch.
- **DM row**: see [direct-messages-and-home.md](direct-messages-and-home.md).
- **Topics primer → New topic** (`[data-topic-primer-new]`,
  `TopicListView.tsx:224`) opens the same create dialog, titled **Create Topic
  in ##ops**: `TopicListView.tsx:1374` passes a `label` that already carries
  `#`, and the modal title prefixes another (`Create ${noun} in #${label}`).
  The sidebar path passes a bare `roomLabel` and reads **Create Topic in
  #signals**. A product nit, reported 2026-10-31.

Every verb here that changes state (`applyRoomPositions`, the archive and
category writes, leave, the mute writes) is unstubbed in both fixtures, so the
offer is proved and the effect is pending. Sidebar drag-and-drop
(`text/om-channel`, `text/om-server`, `Sidebar.tsx:5400-5778`) is not
driveable with synthetic `DragEvent`s.

### Resize handles and the sidebar lens (added 2026-11-01)

Two keyboard-driveable `role="separator"` handles sit in the shell, and a
third demo lives in the gallery (driven 2026-11-01 on `/rooms/` at `936f5b64`):

- **Resize channel sidebar** (`.sidebar-resize`): `aria-valuenow` 240 by
  default, `aria-valuemin` 200, `aria-valuemax` 400. Focus it and press
  **ArrowLeft** three times → 210, written to `om.chat.sidebarWidth`; **Home**
  → 200 (the minimum, not the default). This is the key the chevron recipe
  above seeds by hand.
- **Resize the side panel** (`.column-resize`, `RightPanels.tsx:637`,
  `ColumnResize`): present only while a right panel is open and not in overlay
  mode (`panel=pins` read 304, `panel=members` 324, `panel=search` 364; min
  224, max 464). The commit persists to `om.chat.rightPanelWidth`
  (`RightPanels.tsx:61`, `:101`).
- `fixture.html?surface=resizable-panel` mounts the same `ColumnResize` as
  **Resize the side panel** (280–520, starts at 320) over a `#research` mock,
  with the gallery's `reduced-motion` class removed (`fixture.tsx:1567`).

**The sidebar lens renders from prefs, and only from prefs, in this lane.**
`sidebarLensMode` reads `om.chat.sidebarFocus` (a JSON array of space ids) and
`om.chat.sidebarTodos` (`{"home":bool,"spaces":[…]}`) on every render
(`lib/prefs.ts:630`, `:687`, `:992-996`; `Sidebar.tsx:3854-3876`). Seed one and
reload at a desktop width. At 768 px and below (`MOBILE_QUERY` is inclusive)
the To-dos lens is off, and Focus reads only the active space's pref
(`Sidebar.tsx:3874-3876`):

```bash
agent-browser eval '(()=>{localStorage.setItem("om.chat.sidebarFocus",JSON.stringify(["s1"]));return 1})()'
agent-browser reload
#   [data-focus-toggle] reads aria-pressed="true", "Focus on: show all channels"; 26 treeitems → 16
agent-browser eval '(()=>{localStorage.removeItem("om.chat.sidebarFocus");localStorage.setItem("om.chat.sidebarTodos",JSON.stringify({home:false,spaces:["s1"]}));return 1})()'
agent-browser reload
#   since the Projects work (e504adfa): no To-dos toggle, 26 treeitems, nothing pressed
```

**The To-dos lens no longer renders in either fixture.** On 2026-11-06 at
`ea399e62` the seed was re-driven on `/rooms/`. On `/chat/`, the same
**Projects** button showed and there was no **To-dos** toggle. On a server with Projects, the sidebar
shows a **Projects** button instead of the **To-dos** toggle, and the To-dos
lens collapses to all channels (`Sidebar.tsx:3854-3876`). The fixtures leave
`session.todos` unstubbed, so `todos.recordsOn(...)` answers the truthy `INERT`.
Every space then counts as a Projects server. The seeded
`om.chat.sidebarTodos` therefore changes nothing. The To-dos lens is **live
verification pending** until a fixture stubs `todos.recordsOn` to `false` or a
daemon lane drives a server without Projects. The Focus seed still works: 26 →
16 treeitems and **Focus on: show all channels**.

Clicking **Focus: only what needs you** (`Sidebar.tsx:4852`) or pressing ⌘⇧F
changes nothing: `setSidebarFocus` and `cycleSidebarLens` are unstubbed, so
they resolve to `INERT` and write no pref. Clear both keys before any frame
that should show the full tree.

### Mark to revisit and the Revisit list (added 2026-11-06)

User path: right-click a channel or topic in the sidebar and choose **Mark to
revisit**. A flag appears on the row. The sidebar's icon row has a **Revisit**
toggle that swaps the channel tree for the list of flagged rows. **Done
revisiting**, from the list or the row menu, clears a flag.

Driven on `/rooms/` (18180) at `ea399e62`. On `/chat/` (18181), the flag, the
row name and **Revisit: 1 flagged** were driven, but not the list:

```bash
agent-browser eval 'localStorage.removeItem("om.chat.revisit")'
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=room&alerts=quiet&channels=many')"
#   [data-revisit-toggle] reads "Revisit: 0 flagged", aria-pressed="false"
agent-browser eval '(()=>{const r=[...document.querySelectorAll("[role=treeitem]")].find(e=>/channel signals/.test(e.getAttribute("aria-label")||""));const s=r.querySelector(".channel-row-identity")||r;const b=s.getBoundingClientRect();s.dispatchEvent(new MouseEvent("contextmenu",{bubbles:true,clientX:b.x+20,clientY:b.y+8}));return 1})()'
agent-browser find role menuitem click --name "Mark to revisit"
#   treeitem "channel signals, 4 unread, 5 unread in topics, marked to revisit"
#   a [title="Marked to revisit"] flag on the row; toggle "Revisit: 1 flagged"
#   om.chat.revisit = [{"kind":"channel","roomId":"signals","at":<ms>}]
agent-browser eval '(()=>{document.querySelector("[data-revisit-toggle]").click();return 1})()'
#   toggle "Revisit on: show all channels", aria-pressed="true"
#   section[aria-label=Revisit] reads "REVISIT 1" with
#   "Close Revisit, show all channels", "Open #…, flagged now ago", "Done revisiting #…"
```

- The topic row menu carries the same item (`TopicPill.tsx:402`). On **CPI
  print — Aug** it writes `{"kind":"topic","roomId":"ops","topicId":"cpi-print-aug"}`,
  and the treeitem name ends **, marked to revisit**.
- Pressing **Done revisiting** in the list empties it to "Nothing flagged.
  Right-click a channel or topic and choose Mark to revisit." and deletes the key.
- **The list's row names are blank in the fixture**: **Open #, flagged now
  ago**. `knownRoomLabel` and `topicName` are unstubbed (`SidebarRevisitList.tsx:28`).
  Prove the flag, the toggle, the count, the row name and the pref here, but
  not the list labels. Those need a daemon lane.
- "flagged now ago" is product copy, not a fixture artefact. `relativeAge`
  returns `now` under a minute (`lib/time.ts:73-81`), and the label appends
  " ago" (`SidebarRevisitList.tsx:95`). See the README's product gaps.
- The 50-flag cap toast ("You can flag up to 50 channels and topics…",
  `revisit.ts:206-212`) and opening a flagged row from the list were not driven.

### The Projects button (added 2026-11-06)

`ProjectsButton.tsx` puts a **Projects** button in the sidebar's icon row when
`session.todos.recordsOn(spaceId)` is true. Its name grows to "Projects, N
tickets with new activity" or ", a ticket is overdue". Because `INERT` answers
that predicate, both fixtures render a bare **Projects** button
(`aria-pressed="false"`, no count). It carries the class `has-dot`: the
unstubbed `badge.deadline` is `INERT` and therefore truthy, so the deadline
dot is a fixture artifact, not a reading of real deadlines. Clicking it calls
the unstubbed `session.openTodos` and the route stays on `#/room/ops`
(re-driven 2026-11-07 on both hosts). The Projects page, the ticket page and
the badge are **live verification pending**; see the README's Surface
inventory. Since `61daf979`–`08fe407b` the page behind it is no longer empty
on main: the board, the table with its filters and bulk changes, the phone
list, **Needs you** and the new-ticket form are implemented.

### Unread labels past 99 (added 2026-11-02)

`4cd3434f` routes four counts through `formatUnreadCount`
(`lib/animated-count-parts.ts:35-42`): the channel treeitem's aria-label
(`Sidebar.tsx:3398`, **channel <name>, 99+ unread**), the Home headline
(`shared/components/HomeHub.tsx:694`), the channel peek's header and door
(`ChannelPeekPopover.tsx:94`, `:118`: **99+ new since you last read** and
**99+ unread · open #<title>**) and the older-messages banner
(`ChatPane.tsx:3317`, **You're viewing older messages · 99+ new below**). Above
99 the peek's remainder is zero, so its **+N more unread** line becomes
**More unread · open #<title>** (`:88-89`, `:96`). The topic part of the
sidebar label (**N unread in topics**) and the **N mentions** part stay raw.

Only the headline is reachable on the fixture lane: no channel or topic seed
exceeds 99 (`BASE_CHANNELS` tops out at macro's 12, `channels=many` at 20,
topics at 3; `shell-fixture.tsx:1688-1721`, `:1762`, `:2174`), and the
session store is not on `window`, so a count cannot be raised from
`agent-browser eval`. `rail=counts` seeds one DM at 120 (`:1907`): its
`.rail-badge` reads **99+** while the DM treeitem keeps **120 unread** in its
name. See [direct-messages-and-home.md](direct-messages-and-home.md) / The 99+
headline for the headline proof. A `channel("firehose", 150, 0)` seed in
`BASE_CHANNELS` would make the label and peek forms driveable.

### The bottom pin (added 2026-11-02)

The tape keeps the reader on the newest message until a real input gesture
moves them off it (`lib/bottom-pin.ts`: `arm`, `noteGesture`, `bottomPinFor`;
used by `ChatPane.tsx` and `TopicListView.tsx`). The gestures are an upward
wheel, a touch drag, a `mousedown` on the scroller (a scrollbar grab), or a
`keydown` on it (`bottom-pin.ts:128-131`), followed within 400 ms by an upward
scroll the pin did not write itself. While armed, resize and child-list
observers pull the tape back to the bottom.

On `shell-fixture.html?view=room&alerts=quiet&bulk=120` the scroller is
`[data-tape-scroller]` (`overflow-anchor: none`, `tabindex="0"`). It loads at the
bottom (`scrollHeight - scrollTop - clientHeight` is 0). Prove both halves with a
late-growing row, which is the layout change the pin actually reacts to. Add
`&lateImage=1&lateImageDelay=5000`, so a row grows by about 213 px five seconds
after load:

```bash
D='(()=>{const s=document.querySelector("[data-tape-scroller]");return Math.round(s.scrollHeight-s.scrollTop-s.clientHeight)})()'
# armed: a programmatic scroll is not a gesture, so the late image pulls the tape back
agent-browser eval '(()=>{const s=document.querySelector("[data-tape-scroller]");s.scrollTop-=1500;return 1})()'
sleep 6; agent-browser eval "$D"           # 0
# disarmed: reload, then press PageUp on the focused scroller
agent-browser eval '(()=>{document.querySelector("[data-tape-scroller]").focus();return 1})()'
agent-browser press PageUp; agent-browser press PageUp
sleep 6; agent-browser eval "$D"           # 1414, held
```

Driven 2026-11-03 on `/rooms/` at `ba4389e7`.

Three things do **not** work as a proof on this lane:

- **`agent-browser mouse wheel` and `agent-browser scroll up` never reach the
  scroller.** A `wheel` listener on `[data-tape-scroller]` counted zero events
  after both, with the pointer over the tape, and the distance stayed 0.
- **A viewport change does not separate armed from disarmed.** After a
  programmatic `scrollTop` (armed), a 1440×900 → 1100×640 → 1440×900 round trip
  left the tape where it was (2914 px up). So holding position across a resize
  proves nothing about the gesture.
- The dock's **Collapse panel** toggle is INERT on this fixture, so it cannot
  be the layout change either.

### Tab title and favicon (added 2026-11-03)

The router writes `document.title` on every session change, and repaints the
favicon and the PWA app badge from the same counts (`apps/cloud/src/lib/routing.ts:293-298`;
`lib/badge.ts:196-279`). The title is the per-view title
(`routing.ts:104`, `titleForView`). It reads **OM Chat | #ops | Thanefield
Capital** in a channel, **OM Chat | #ops ⌗ CPI print — Aug | Thanefield
Capital** in a topic and **OM Chat | Home** on Home. A **(N)** prefix, or
**(99+)**, appears only for mentions, DMs and pending agent asks; ordinary room
unread is dot-only (`badge.ts:11-28`, `:207-210`). The favicon is
`link#om-chat-favicon`, which the badge painter replaces with a canvas
`data:image/png` URL.

```bash
agent-browser eval '(()=>document.title+" | "+document.querySelector("link#om-chat-favicon").href.slice(0,22))()'
```

Driven on both hosts on 2026-11-03: the title followed the room and the topic,
and the favicon was a data URL. **Not proved:** the **(N)** prefix. No fixture
seed gives a non-zero badge count, so `rail=counts` (`/rooms/`) and `rail=many`
(`/chat/`) both read **OM Chat | Home**. The dot grade (alert or unread) and
`navigator.setAppBadge` cannot be read on the lane.

## Gotchas

- **"Hide this channel's topics" is a `title`, not an `aria-label`.**
  `find role button click --name "Hide this channel's topics"` resolves it, but
  `button[aria-label="Hide this channel's topics"]` matches nothing. After the
  click the first channel's button reads `title="Show this channel's topics"`
  with `aria-expanded="false"` (`Sidebar.tsx:3601`); assert on `[title*="this
  channel"]` (re-measured 2026-11-02 on both hosts).
- **`panel=members` on a public topic blanks the whole shell, on both hosts.**
  `?view=topic&topic=cpi-print-aug&panel=members&topics=on` leaves `#root`
  empty. The thrown error, read on `/rooms/`, is `session.topicFollowers(...)?.then is not a
  function` (`RightPanels.tsx:1401-1402`): the fixtures never stub
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
  (`RightPanels.tsx:225`), which is a viewport distinction, not an open one.
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
  (`RightPanels.tsx:218`) rather than on whether a panel is open. `#715` added
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
    `src/lib/routing.ts:684-688` closes any open peek when the route equals the
    current view (the Browser-Back rule). Put the peeked topic in the hash
    instead: `shell-fixture.html?view=room&topics=on&peek=cpi-print-aug&alerts=quiet#/room/ops/topic/cpi-print-aug`.
    `routing.ts:670-683` keeps a peek whose topic matches the hash, so the
    pane mounts the same as on `/chat/`.
  - **On both hosts:** Escape closes the pane and returns the route to the
    parent room (`#/room/ops`, `/chat/room/ops`).
  - **Open full works on `/chat/` only.** There it promotes the peek to the full
    topic (heading `#ops/CPI print — Aug`, `/chat/room/ops/topic/cpi-print-aug`).
    The button (`TopicPeekPane.tsx:751-759`, accessible name **Open full**, title
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
  opens the full topic (`TopicActivityCard.tsx:152-164`). So
  `apps/cloud/tools/visual/topic-peek.visual.ts`, which clicks that count,
  reads as stale against source. It was not run either. In the fixture, the
  inbox panel's **Topic CPI print — Aug, followed** row did not open a peek on
  either host. Dedicated peek callers are the inbox (`TopicInbox.tsx:51-67`)
  and the to-dos panel.
- "Search or jump to…" in the sidebar is **inert** in the fixture. Clicking it
  opens nothing — confirmed live. But that is a fact about the *control*, not
  about the surface: **`?switcher=open` mounts the quick-switcher**
  (`shell-fixture.tsx:3035` seeds `palette`), and it comes up with real
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
  as `noop` (`shell-fixture.tsx:3449`, `:3582`). Prove the offer and its gating
  here, never the state change. That needs the daemon-pair lane.
  A synthetic `contextmenu` dispatched on the `treeitem` itself opens nothing;
  dispatch it on the row's `.channel-row-identity` span. A topic `treeitem` is a
  `div` whose only `button` is the hover **More options for <topic>** control
  (re-measured 2026-10-30 on both hosts). The topic row menu then lists Unfollow,
  Mute, Copy link, **Resolve <topic> (closes the conversation; the history
  stays)**, Open Topic, Import Folder..., **Mark As Unread** (only on a fully
  read topic), **Mark to revisit**, Rename, Create Doc from Topic, Set topic
  index... and Delete Topic. On **CPI print — Aug**, which has 3 unread, it
  lists 11 items without **Mark As Unread** (re-driven 2026-11-06 on `/rooms/`).
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

**Last verified:** 2026-11-09 (nightly maintenance). **Product commit:** `82390825` (GitLab origin/main; rooms-client 0.114.0; 49 commits past `08fe407b`). **Scope:** `/rooms/` (18183) and `/chat/` (18184), with the people stub: the **CPI print — Aug** treeitem → `#/room/ops/topic/cpi-print-aug` (`/chat/room/ops/topic/cpi-print-aug`), composer **Message in CPI print — Aug**, **Back to #ops**. **Limitations:** `panel=members` on a topic still renders blank (carried). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261109/r1/`.

**Previous record:** 2026-11-08 (nightly maintenance). **Product commit:** `08fe407b` (GitLab origin/main; rooms-client 0.112.0; unchanged since the 2026-11-07 pass). **Scope:** `/rooms/` (18183) and `/chat/` (18184): the **CPI print — Aug** treeitem → `#/room/ops/topic/cpi-print-aug` (`/chat/room/ops/topic/cpi-print-aug`), composer **Message in CPI print — Aug**, **Back to #ops**; the route smoke on both hosts. **Limitations:** the topic `panel=members` still renders blank (carried). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261108/r1/`.

**Previous record:** 2026-11-07 (nightly maintenance). **Product commit:** `08fe407b` (GitLab origin/main; rooms-client 0.112.0; 89 commits past `ea399e62`). **Scope:** `/rooms/` (18180) and `/chat/` (18181) `view=room`: the **CPI print — Aug, 2 mentions, 3 unread** treeitem → `#/room/ops/topic/cpi-print-aug` (`/chat/room/ops/topic/cpi-print-aug`) and the composer **Message in CPI print — Aug**; the sidebar **Projects** button (`aria-pressed="false"`, class `has-dot`) in place of the To-dos toggle, its click leaving the route unchanged; the route smoke (176 and 145 routes). **Limitations:** Mark to revisit, the lenses and the Projects page not re-driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261107/r1/`.

**Previous record:** 2026-11-06 (nightly maintenance). **Product commit:** `ea399e62` (GitLab origin/main; rooms-client 0.111.0; 74 commits past `873a57ce`). **Scope:** `/rooms/` (18180) and `/chat/` (18181): **CPI print — Aug, 2 mentions, 3 unread** → `#/room/ops/topic/cpi-print-aug` (path route on `/chat/`) and **Back to #ops**; the 11-item channel row menu with **Mark to revisit** on both hosts; flag, row name, **Revisit: 1 flagged**, the Revisit list and **Done revisiting** on `/rooms/`; the topic row's **Mark to revisit**; the inert **Projects** button; the Focus seed (26 → 16) and the To-dos seed that no longer renders. **Limitations:** Revisit list labels are blank in the fixture; the 50-flag cap and opening a flagged row were not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261106/r1/`.

**Previous record:** 2026-11-05 (nightly maintenance). **Product commit:** `873a57ce` (GitLab origin/main; rooms-client 0.109.1; 17 commits past `ce14d4ba`). **Scope:** `/rooms/` (18170) `view=room`: treeitem **CPI print — Aug, 2 mentions, 3 unread** → `#/room/ops/topic/cpi-print-aug`, h1 `#ops / CPI print — Aug`; **Back to #ops** → `#/room/ops`. `/chat/` (18171): the same click lands on the path route `/chat/room/ops/topic/cpi-print-aug`. **Limitations:** the switcher, topics route and mobile doors were covered only by the route smoke. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261105/r1/` (`30`, `smoke/`).

**Previous record:** 2026-11-04 (nightly maintenance). **Product commit:** `ce14d4ba` (GitLab origin/main; rooms-client 0.109.1; 16 commits past `ba4389e7`). **Scope:** `/rooms/` (18160): treeitem **CPI print — Aug, 2 mentions, 3 unread** → `#/room/ops/topic/cpi-print-aug` with **Message in CPI print — Aug**, **Back to #ops** → `#/room/ops`; `switcher=open` mounts the palette ("Search messages, or jump anywhere..."); `view=topics` → `#/room/ops/topics`. `/chat/` (18161): the topic route `/chat/room/ops/topic/cpi-print-aug` with the same composer name. **Limitations:** the bottom pin, mute and mark-unread were not re-driven; their 2026-11-03 records stand. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261104/r1/` (`nav-01-topic`).

**Previous record:** 2026-11-03 (nightly maintenance). **Product commit:** `ba4389e7` (GitLab origin/main; rooms-client 0.108.0; one CI-only commit past `3f8f24bc`). **Scope:** `/rooms/` (18143) and `/chat/` (18144). Sidebar → **CPI print — Aug** retargets the composer to **Message in CPI print — Aug** (`#/room/ops/topic/cpi-print-aug`); **Back to #ops**; **All 6 topics in ops**; `#/room/ops/msg/105` sets `messageJump=105`; the seven `panel=` asides (**New topic**, **Inbox**, **Pinned**, **Bookmarks**, **Members**, **Results**, **Library**); the **Preview of signals** and **Conversation with ana** peeks; **Remove ana from this topic** → **Remove from private topic?**; the 11-item topic row menu, **Delete ⌗ …** and **Resolve …**; the 10-item channel row menu and the mute submenu (15m / 1h / 8h / 24h / **Until unmuted**); **Resize channel sidebar** 240 → 210; the Focus lens (16 treeitems); both halves of the bottom pin with `lateImage`; the tab title and favicon. On `/chat/`: the topic route, the topic peek, and no **Remove …** buttons on `basis-desk-review`. **Limitations:** the bottom pin's touch and scrollbar disarms are source-only; no seed gives the title's **(N)** prefix; the 99+ channel label is still unseeded. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261103/r1/` (`nav-*`, `pin-*`, `sig-01`).

**Previous record:** 2026-11-02 (scheduled maintenance). **Product commit:** `3f8f24bc` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18141) and `/chat/` (18142): **CPI print — Aug, 2 mentions, 3 unread** → `#/room/ops/topic/cpi-print-aug` on `/rooms/` and the composer **Message in CPI print — Aug** on both; **Back to #ops** → `#/room/ops`; **Hide this channel's topics** → `title="Show this channel's topics"`, `aria-expanded="false"` on both; **Resize channel sidebar** present; `view=topics` mounts; `rail=counts` shows **99+** on `/rooms/`. **Limitations:** the peeks, the bottom pin and the right-panel dock were not re-driven; their nightly records stand. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261102/r1/`.

**Previous record:** 2026-11-02 (nightly maintenance). **Product commit:** `3f8f24bc` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18137) and `/chat/` (18138): **CPI print — Aug, 2 mentions, 3 unread** → `#/room/ops/topic/cpi-print-aug` (`/chat/room/ops/topic/cpi-print-aug`) and **Back to #ops**; **Hide this channel's topics** → **Show this channel's topics** with `aria-expanded="false"` (level-2 rows 20 → 18 on `/rooms/`); the channel-row menu (10 entries) and its **Choose how long to mute #ops** tile → **15m / 1h / 8h / 24h / Until unmuted**; the server menu (the sweep entry and the four timed-mute chips on `/rooms/`; 25 entries, five mute entries and no **Clean up topics** on `/chat/`); the topic-row menu (11 entries, **Mark As Unread** and **Set topic index...** listed) → **Resolve <topic>** dialog (**What settled it? · optional**, **Resolve Topic**, **Enter resolves · Esc cancels**) and the **Delete ⌗ <topic>** alertdialog (**Cancel** / **Delete**); `switcher=open` → the `.quick-switcher` combobox, `#mac` → 9 options → Enter landed `#/room/macro/topic/basis-desk-review`; the #macro hover peek (**You're caught up**, **Peeking never marks as read**); **Resize channel sidebar** 240 → 270 (`om.chat.sidebarWidth` 270) and **Resize the side panel** by keyboard after an `eval` focus; the topics primer on both hosts (**Create Topic in ##ops** still doubled; **Dismiss the topics explainer**); **Remove ana from this topic** → **Remove from private topic?** on `/rooms/` (the `/chat/` members panel renders no Remove buttons); the Home headline **99+ unread across 4 conversations.** under `rail=counts`; the bottom pin across a viewport change. **Limitations:** `find role separator` has no `focus` action, focus the separator with `eval` first; `panel=members` on the public topic `cpi-print-aug` still blanks both hosts; the 99+ channel label and peek forms have no seed; the deep link, the DM and topic peeks and the New topic pane were load-smoked only. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261102/r1/`.

**Previous record:** 2026-11-01 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18137): **CPI print — Aug, 2 mentions, 3 unread** → `#/room/ops/topic/cpi-print-aug` with the composer **Message in CPI print — Aug** → **Back to #ops**; dock **Members**; the topic row menu (10 items: Following, Mute, Link, Resolve, Open Topic, Import Folder..., Rename, Create Doc from Topic, Set topic index..., Delete Topic); the channel-row menu (10) and its **Create Topic** → **Create Topic in #signals** with **Make topic private**; the **Desk** category menu (3); the server menu (16, with **Clean up topics**) → **Create Category** and **Create Channel** → **Create channel**; the topic peek under the hash (**Topic CPI print — Aug (peek)**, **Open full**), the DM hover peek (**Conversation with ana**) and the channel hover peek (**Preview of signals**, caught up); the switcher (`#mac` → `#/room/macro/topic/basis-desk-review`); the deep link `#/room/ops/msg/105` flashing row 105; the inbox, New topic, Pinned and Bookmarks panels; the two resize separators and the seeded Focus and To-dos lenses. `/chat/` (18138): topic open and **Back to #ops**, the channel-row menu (10), the server menu (15, no **Clean up topics**), **Create Category**, the DM row menu, the DM hover peek, the topic peek's **Open full** promoting to `/chat/room/ops/topic/cpi-print-aug`, the four panels and the switcher. **Limitations:** **Hide this channel's topics**, Mark As Unread (the `topic in ops` row's menu tonight listed no such entry), **Resolve Topic**, Mute durations and the remove/delete confirms were not re-driven; their 2026-10-31 records stand. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261101/r1/` (`nav-01` to `nav-10`, `peek-01` to `peek-03`, `panels-01`, `lens-01`/`02`, `census-04`, `chat-01` to `chat-05`).

**Previous record:** 2026-10-31 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18135): CPI treeitem → `#/room/ops/topic/cpi-print-aug` and **Message in CPI print — Aug**, **Back to #ops** → `#/room/ops`; **Hide this channel's topics** → **Show this channel's topics** (16 level-2 rows); dock **Members** → **Close Members** with `aria-pressed=true` and `.right-panel-drawer`; topic row menu (11 items), **Resolve Funding flipped negative on Hyperliquid** and **Resolve Topic** pressed (closes, no change), **Delete ⌗ …** alertdialog; switcher `#mac` → `#/room/macro/topic/basis-desk-review`; deep link `msg/105` → `data-message-jump=105`; channel-row **Mute** submenu (five durations); **Preview of signals** and **Conversation with ana** hover peeks; topic peek with the hash and Escape back to `#/room/ops`; **Remove from private topic?**; primer **New topic** → **Create Topic in ##ops**; the channel row, category and server menus and **Create Topic** / **Create Channel** dialogs. `/chat/` (18136): topic → `/chat/room/ops/topic/cpi-print-aug` and back; `peek=cpi-print-aug` plus **Open full** → the full topic; DM peek; the channel peek stays **Loading preview**; switcher → `/chat/room/macro/topic/basis-desk-review`; `panel=inbox` aside **Inbox**; `panel=topic-draft` aside **New topic**; the three sidebar menus (server 15 items). **Limitations:** Every menu verb's effect, public-topic removal, the dock collapse toggle and **Add People...**. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261031/r1/`.

**Previous record:** 2026-10-30 (scheduled maintenance). **Product commit:** `47cb13bf` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18153): CPI treeitem → `#/room/ops/topic/cpi-print-aug` and **Message in CPI print — Aug**, **Back to #ops** → `#/room/ops`; **Hide this channel's topics** flipped to **Show**; topic row menu (11 items) via `contextmenu` on `.channel-row-identity`; Delete Topic copy; **Resolve Funding flipped negative on Hyperliquid** dialog; **Choose how long to mute #signals** → 15m/1h/8h/24h; **Remove from private topic?** on `basis-desk-review`; deep link `messageJump=105`; topic peek with the hash; `panel=inbox` (**Close inbox**, **Mark #ops read**); `switcher=open`; `panel=pins|bookmarks|topic-draft` asides. `/chat/` (18154): topic navigation and Back, the 11-item topic row menu and Delete Topic. **Limitations:** The `/chat/` fixture has no private `basis-desk-review` topic (the route lands on `#ops` Members). Effects of mute, unread, resolve and delete are fixture no-ops. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261030/r1/` (frames 05-07, 10-13).

**Previous record:** 2026-10-30 (nightly maintenance). **Product commit:** `47cb13bf` (GitLab origin/main; rooms-client 0.108.0). **Scope (`/rooms/`):** On the private topic `basis-desk-review` with `panel=members`, **Remove ana from this topic** opened **Remove from private topic?**, and **Remove** closed it with no change. The topic row menu's **Delete Topic** showed the new `edbb7153` body. `panel=members` on the public `cpi-print-aug` blanked the shell on `/rooms/` and `/chat/` with the `topicFollowers` error in Gotchas. **Limitations:** Only the delta above was driven tonight; the rest of this guide keeps its 2026-10-29 proof. Public-topic removal, the member menu and the glyph are source-only. Evidence is local only: `artifacts/vomc-nightly-20261030/r1/` (frames 16-19).

**Previous record:** 2026-10-29 (nightly maintenance). **Product commit:** `cdfb1b0f` (origin/main; rooms-client 0.108.0). **Scope:** Topic peek on `/rooms/` (`?view=room&topics=on&peek=cpi-print-aug&alerts=quiet#/room/ops/topic/cpi-print-aug`) mounted `[data-topic-peek="cpi-print-aug"]`, 440 px, with log **Messages in CPI print — Aug**. Escape returned `#/room/ops`. **Open full** did nothing on `/rooms/` (fixture gap, see Gotchas), and on `/chat/` it promoted the peek to `/chat/room/ops/topic/cpi-print-aug`, heading `#ops/CPI print — Aug`. Sidebar chevron (`357b2df5`): with `om.chat.sidebarWidth=200` and `?view=room&channels=many&topics=on`, hovering **options-flow** revealed **Invite people to options-flow**, **Edit options-flow** and **More options for options-flow**. The topic chevron stayed at x=232 while the label truncated (89→40 px on `/rooms/`, 86→40 px on `/chat/`). Channel row **More options for signals** → **Mute** (accessible name **Choose how long to mute #signals**) opened 15m / 1h / 8h / 24h / Until unmuted on both hosts. **Until unmuted** closed the menu with no visible state change and no toast. **Limitations:** Mark As Unread, the quick switcher, the deep link and the inbox were not re-driven. The mute effect, including the `4ca34c9a` REST fallback for never-joined rooms, is unit-test only, because `setRoomAttention` is unstubbed. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261029/r1/` (frames 05, 20–23, 48).

**Previous record:** 2026-10-28 (scheduled maintenance). **Product commit:** `07f7d04c` (origin/main). **Scope:** Topic peek on both hosts: `/chat/` `?view=room&topics=on&peek=cpi-print-aug` and `/rooms/` with `#/room/ops/topic/cpi-print-aug` mounted `[data-topic-peek="cpi-print-aug"]` beside the stream, with log **Messages in CPI print — Aug**; Escape closed it back to the parent room; **Open full** promoted it to `#ops/CPI print — Aug`. `?panel=inbox` rendered the inbox rows on both hosts. **Limitations:** Peek **Previous topic** / **Next topic**, the peek composer and drop target, and channel or DM hover peeks were not driven. The inbox topic row opened no peek in the fixture. The quick switcher, deep link, topic row menu and dock were not re-driven at this tree. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261028/r1/` (`*-topic-peek-*.png`).

**Previous record:** 2026-10-28 (nightly maintenance). **Product commit:** `2dd7aad1` (origin/main). **Scope:** The CPI topic treeitem gave `#/room/ops/topic/cpi-print-aug` and the composer **Message in CPI print — Aug**; **Back to #ops** gave `#/room/ops`. `?switcher=open` mounted `.quick-switcher` (`role=combobox`, placeholder "Search messages, or jump anywhere...", "Nowhere recent yet."), and `#mac` then Enter reached `#/room/macro/topic/basis-desk-review`. The deep link `#/room/ops/msg/105`, present at load, set `messageJump=105` and rewrote the hash to `#/room/ops`. `panel=topic-draft` mounted the **New topic** aside. `?view=topics` showed the primer with 12 px padding. The topic row menu offered **Mark As Unread** on the read topic, and the inbox panel and Resolve dialog rendered (section above), on both hosts. **Limitations:** The topic peek was recorded as rendering nothing (corrected above), the dock was not re-driven, and Mark As Unread effects are fixture no-ops. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261028/r1/` (frames 01, 04, 08-09, 36-37, 41, 43). Previous record: 2026-10-27 at `6c15b0fb`.