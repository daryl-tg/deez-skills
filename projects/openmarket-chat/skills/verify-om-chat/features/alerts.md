# Alerts

The app-wide alert strip, the channel alerts board, and the alert card in the
tape. Alert feeds ring when a watched condition fires. Webhook conversion lives
in [settings-and-appearance.md](settings-and-appearance.md).

## Sub-features

- **Alert strip** (`packages/chat-ui/src/components/AlertStrip.tsx`): an app-wide
  bar above the content card. It renders `name · actionLine` with a timestamp and
  the buttons **I'm on it** and **Open**, and an icon button named **Dismiss
  this strip** (read 2026-11-22; not pressed).
- **No channel-header beacon since `dc6a9a47`** (2026-10-01). `ChatPane.tsx`
  stopped mounting `AlertsBeacon`; the file survives only for the board's
  `BOARD_WIDTH`. A channel with a live alert feed gets an **Alerts** door on
  the right-edge dock instead (`RightPanels.tsx:230-253`, gated by
  `rightSlotTabsFor`), and the sidebar carries the ringing count. The fixture's
  `#ops` has no live feed, so its dock shows Library, Bookmarks, Members and
  Pins only, and the door is live verification pending (re-measured
  2026-10-30 on both hosts: no `[aria-label^="Alerts:"]` element anywhere).
- **Alerts board** (`AlertsBoard.tsx`): a dialog named **Alerts board** with Ring
  feeds and Log feeds, one button per feed, plus **New alert...** and **All
  alerts**.
- **Feed peek on the board** (`AlertsBoard.tsx:348-378`, `AlertFeedPeek.tsx:91`):
  pointing at a feed row opens a dialog named **<feed> at a glance**. It holds
  the feed name, its class (**Ring** or **Log**) and one stat line. A Ring
  feed with a 30-day series adds 30 bars (**daily trigger counts, 30 days**,
  each titled like "Oct 18 · 1") and reads "67% answered · 3 open · 4m to
  ack". With no series the chart is absent and the line reads **3 open**.
- **Alert card** in the tape (`AlertMessageRow.tsx`), with **Discuss**, **I'm on
  it**, **Mark fixed** and **Flag noisy**.
- **Feed sub-row and alert categories** (since `335c4304`): a feed channel
  keeps its own category and shows a `store-5xx · check pods` sub-row. A
  category marked as an alert category shows a mark and **N ringing** while
  expanded. The derived **Alerts** group is retired.
- Creating a feed (`AlertCreateDialog.tsx`) and the full alerts home
  (`#/alerts`, `AlertsPage.tsx`) exist in source. Neither is reachable in the
  fixture; see Gotchas.

## How to get to it (user POV)

A feed fires and a strip appears across the top of the app naming it. You
click **I'm on it** to claim it, or **Open** to read it. In a channel with a
live feed, the **Alerts** door on the right-edge dock opens that channel's
alerts, and the board lists every feed so you can open one or start a new
alert.

## Driving it with control-om-chat

```bash
export OM_CHAT_LANE_PORT=<assigned-port>
control-om-chat doctor && control-om-chat up
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=room')"            # strip firing
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=room&alerts=board')" # board open
agent-browser open "$(control-om-chat url 'tools/visual/fixture.html?surface=alert-card')"         # tape card
```

| Route | State |
|---|---|
| `shell-fixture.html?view=room` | Strip firing: `.alert-strip` text `store-5xx · check pods` |
| `shell-fixture.html?view=room&alerts=board` | The board dialog open and pinned (`shell-fixture.tsx:1464-1472`) |
| `shell-fixture.html?view=room&alerts=amber` | A second strip state (`tools/visual/shell-fixture.tsx:1476-1477`) |
| `shell-fixture.html?view=room&alerts=quiet` | No strip: use this for every non-alert proof |
| `fixture.html?surface=alert-card` | The alert card with its four actions |

On the board, the feed buttons are named with their state, for example
`Ring store-5xx 3 open, nobody on it #ops78d ago` and `Log relay-latency#ops`.
Read the strip through `.alert-strip-text`, not the snapshot tree: its row is a
plain `generic` there.

### A feed channel stays in its own category; alert categories (since `335c4304`)

The virtual **Alerts** group is gone. `om.chat.alertsGroupAuto` and
`[data-alerts-group]` no longer exist. A channel with a live feed now stays in
the category it is filed in. It carries its feed as a sub-row under the channel
(`alertsRowForRoom`, `lib/alerts-group.ts:83`, rendered at
`packages/chat-ui/src/components/Sidebar.tsx:4698-4706`).

To check the sub-row, open `shell-fixture.html?view=room&alerts=board`. On
**both** hosts, `#ops` under **category Desk, 5 channels** carries
`.channel-alert-row.ringing` with the text **store-5xx · check pods**
(`data-row-key="alert:ops"`). Collapse the category (`button.category-separator`):
the header reads **DESK** and **1 ringing**. Since `fbd77281` the count never wraps or shrinks: `.category-separator-count` computes `white-space: nowrap` and `flex-shrink: 0`, and is one 13 px line (measured 2026-11-20 on `/rooms/`; the fixture has no category name long enough to squeeze it). The old `/chat/` gap, where
`lastRefreshedAt` was missing, no longer applies, because the sidebar row needs
only `feeds.length > 0`. Under `alerts=quiet` there is no sub-row.

A category can also be marked as an **alert category** (`alert: true` in the
space's stored `categories`). It then shows `.category-alerts-mark` and its
ringing count even while expanded (`Sidebar.tsx:4932-4938`, `:4954-4967`). A
plain category shows counts only when collapsed. You mark one from the category
header menu (**Mark as alert category**), or with the **Alert category** box in
**Create Category**. The recipe, with the stubs that make it reachable, is in
[channel-and-topic-navigation.md](channel-and-topic-navigation.md), "Categories:
order, move and alert mark". On both hosts, marking **Desk** writes
`{name:"Desk",alert:true}` and paints the mark. The header then reads **DESK**
and **1 ringing** while expanded. Driven 2026-11-19.

### The board's feed peek (added 2026-11-16)

Both fixtures stub `seriesFor: () => null` (`tools/visual/shell-fixture.tsx:1499`,
`apps/cloud/tools/visual/shell-fixture.tsx:563`), so the bare board shows the
chart-less peek. `alertsStub` is a plain object, so the session-capture shim
from [message-actions.md](message-actions.md) can replace the method:

```bash
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=room&alerts=board')"
agent-browser eval '(()=>{const o=window.__om,pts=[];for(let i=0;i<30;i++){const d=new Date(2026,9,18+i);
  pts.push({day:d.getFullYear()+String(d.getMonth()+1).padStart(2,"0")+String(d.getDate()).padStart(2,"0"),
  triggers:(i*7)%5+1,responses:(i*7)%5})}const s={series:pts,medianAckMs:240000};
  o.alerts.seriesFor=()=>s;o.closeConfirm();return 1})()'
agent-browser find role button hover --name "Ring store-5xx"
agent-browser wait 1200
# dialog "store-5xx at a glance": 30 children in .alert-peek-bars,
# "store-5xx / Ring / 67% answered · 3 open · 4m to ack"
```

Driven 2026-11-16 on both hosts. Without the shim the same hover gives
**store-5xx**, **Ring**, **3 open** and no bars. A **Log** feed's trend line
was not driven.

### Convert to alerts is hidden on an alert channel (added 2026-11-26)

Since `0f3fd22c`, **Convert to alerts...** is offered only on a channel that has
no live, non-archived alert feed. The gate is `convertToAlertsOffered`
(`packages/chat-ui/src/lib/convert-to-alerts.ts:34`), which reads
`session.alerts.hasLiveFeedFor(room)`. It applies to three menus: the channel
title menu, the header **More channel actions** `…`
(`ChannelHeaderMenus.tsx:215-218`) and the sidebar row menu
(`Sidebar.tsx:5338-5341`). A channel whose feeds are all archived is offered it
again. The hosted session has no alerts store, so the entry never shows there
in the product.

Neither fixture's `alertsStub` defines `hasLiveFeedFor`
(`tools/visual/shell-fixture.tsx:1459`; cloud
`apps/cloud/tools/visual/shell-fixture.tsx:535`), so by default the fixtures
offer **Convert to alerts...** everywhere, `#ops` included. Seed the live feed
through the session-capture shim ([README.md](README.md), "Seed spelled-out keys with the session-capture shim"):

```bash
# open shell-fixture.html?view=room&alerts=quiet with the shim init script, then:
agent-browser eval '(()=>{const o=window.__om;o.alerts.hasLiveFeedFor=r=>r==="ops";o.version=Number(o.version)+1;o.closeConfirm();return 1})()'
agent-browser find role button click --name "More channel actions"
#   #ops header menu: 13 items, no "Convert to alerts..." (14 with it before the seed)
# right-click [data-row-key="room:ops"] .channel-row-identity
#   #ops row menu: 11 items, no "Convert to alerts..."
# right-click [data-row-key="room:signals"] .channel-row-identity
#   #signals row menu: 12 items, "Convert to alerts..." still there
```

Driven 2026-11-26 at `0f3fd22c` on both hosts with exactly these counts.
The same seed adds the dock's **Alerts** door (`[data-slot-tab="alerts"]`,
after **Pins**) on both hosts, which the unseeded fixture never shows. Do not
press it on the fixture: it opens the channel's Alerts tab, which blanks the
shell (see Gotchas).

The dialog (`settings/ConvertChannelHost.tsx`) changed in the same commit:
- The title `Convert to alerts · #<channel>` sits on one line with an ellipsis
  (`span.convert-channel-title`, `:102`).
- The create state is 480 px wide.
- The "Name the feed" line is gone while the name is empty.
- If the dialog opens on an alert channel it shows only a refusal
  (`p[data-convert-already-alerts]`, `:165`): "#ch is already an alert
  channel. Add alerts from its Alerts tab, or bind more webhooks on the
  channel's Webhooks page."

The dialog is not reachable on the fixtures. `openConvertToAlerts` answers the
inert stand-in, and `Shell.tsx` mounts the host from its own state.
Live verification pending.

## Gotchas

- **`surface=alert-card` mounts late.** 1.8 s after `open` none of the four
  card actions were in `innerText`; at 2.5 s all four were. Wait for
  **Discuss** before asserting the rest (2026-11-02, `/rooms/`).
- Do not look for the old `Alerts: N feeds are ringing` beacon or caption a
  frame with its count. It has not rendered since `dc6a9a47`; the board's two
  seeded rows are the only feed list in the fixture.
- **I'm on it** on the strip changes nothing in the fixture, and **New alert...**
  opens no create dialog. Both are fixture no-ops. Prove the controls render;
  claiming and creating need a daemon lane. Live verification pending.
- `#/alerts` has no fixture `?view=`, so the alerts home page is unreachable here.
  Live verification pending.
- Without `alerts=quiet` the strip shifts every surface below it. That is why
  the other guides add it.
- **The shell fixtures style alerts since `27156df5`.** They load
  `shared/alerts.css` through `src/app-styles.ts`, like the apps. Under
  `alerts=board` the strip reads `display: flex`, padding `7px 12px` and a
  tinted band on both hosts (2026-11-26). Frames from before `27156df5` showed
  the strip and board as unstyled text; do not compare against them.
- **`?panel=alerts` blanks the whole shell on both hosts.** It is the
  channel's Alerts tab (`AlertsPanel.tsx`, mounted at `RightPanels.tsx:448-458`
  and opened in the product by `session.openAlertsTab`). The fixture's
  plain-object `alertsStub` (`shell-fixture.tsx:1459`) lacks members the
  panel reads, among them `feedViewClaimed`, `selectedFeedId`,
  `setSelectedFeed`, `tapeFeedFilter` and `setTapeFeedFilter`. Which one throws
  first was not isolated. No error boundary wraps the panel, so `#root`
  unmounts to an empty page, with only React's "An error occurred in the
  <AlertsPanel> component" warning in the console (2026-10-29, `cdfb1b0f`).
  The Alerts tab is live verification pending.
- **The board popover starts `visibility: hidden` until it has measured its
  anchor.** A role query fired right after load finds nothing. Wait about a
  second, or poll for the **Alerts board** dialog's computed visibility.

### Verification record

**Last verified:** 2026-11-26 (nightly maintenance). **Product commit:** `0f3fd22c` (GitLab origin/main; rooms-client 0.125.0; 7 commits past `557ee9ed`). **Scope:** new tonight on both hosts: **Convert to alerts...** left out of the `#ops` header and row menus with `alerts.hasLiveFeedFor` stubbed, kept on `#signals`; the dock **Alerts** door appearing under the same stub; the strip styled with no injection since `27156df5`. Then the scripted re-drive of this guide's recipes by the kept step runner (`/rooms/` 18186, `/chat/` 18187 where the guide covers it, openscape 18188 for the world), motion blocks one session at a time; two read-only judges compared every result with its expectation and each flagged block was re-run alone. **Limitations:** the convert dialog is unreachable on the fixtures; the dock door's panel was not opened (it blanks the shell). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261126/r1/`.

**Previous record:** 2026-11-25 (nightly maintenance). **Product commit:** `557ee9ed` (GitLab origin/main; rooms-client 0.125.0; 11 commits past `9c697d6e`). **Scope:** the scripted re-drive of this guide's recipes by the kept step runner (`/rooms/` 18186, `/chat/` 18187 where the guide covers it, openscape 18188 for the world), motion blocks one session at a time; every failing step was re-run alone and compared with this guide. This guide's source did not change in the delta. **Limitations:** the strip's third control is an icon-only **Dismiss this strip**. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261125/r1/`.

**Previous record:** 2026-11-24 (nightly maintenance). **Product commit:** `9c697d6e` (GitLab origin/main; rooms-client 0.125.0; 22 commits past `4b6f42b4`). **Scope:** the scripted core-path re-drive of this guide's recipes (`/rooms/` 18186, `/chat/` 18187 where the guide covers it, openscape 18188 for the world); every failed or disagreeing step was re-run alone. This guide's source did not change in the delta. **Limitations:** unchanged from the previous record. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261124/r1/`.

**Previous record:** 2026-11-22 (nightly maintenance). **Product commit:** `4b6f42b4` (GitLab origin/main; rooms-client 0.124.0; one commit past `84e88e56`). **Scope:** `/rooms/` (18186): the strip **store-5xx · check pods** with **I'm on it**, **Open** and **Dismiss this strip**; `alerts=quiet` removing it; the board (Ring store-5xx, Log relay-latency, **New alert...**, **All alerts**); the ringing sidebar row and the category's **1 ringing** on one line; the alert card gallery. Both hosts: the board's feed peek with a seeded series (30 bars, "67% answered · 3 open · 4m to ack"). `/chat/` (18187): the board and the ringing row. **Limitations:** `panel=alerts`, the claim effect and the category alert mark were not driven. `alerts=amber` showed the same strip text. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261122/r1/`.

**Previous record:** 2026-11-20 (nightly maintenance). **Product commit:** `7e3f0cde` (GitLab origin/main; rooms-client 0.122.0; 16 commits past `12f1ea24`). **Scope:** `/rooms/` (18193), `?view=room&alerts=board`: with **Desk** collapsed the header reads **1 ringing**, and `.category-separator-count` computes `white-space: nowrap`, `flex-shrink: 0` and one 13.2 px line. The board and gallery routes mounted in the route smoke on both hosts. **Limitations:** no category name long enough to squeeze the count; the count was not measured on `/chat/`; the strip, board and card buttons were not pressed tonight. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261120/r1/` (frame 16).

**Previous record:** 2026-11-19 (nightly maintenance). **Product commit:** `12f1ea24` (GitLab origin/main; rooms-client 0.120.0; 12 commits past `c19e2f70`). **Scope:** `/rooms/` (18191) and `/chat/` (18192), with no init script, `view=room&alerts=board`. Both hosts show the `#ops` feed sub-row **store-5xx · check pods** inside **Desk**, with no `[data-alerts-group]`. Collapsed, Desk reads **1 ringing**. With the category stubs and the session-capture shim, **Mark as alert category** on Desk wrote `alert:true` and painted `.category-alerts-mark` on both hosts. **Limitations:** the mark comes from a stubbed `categoriesFor`/`setSpaceCategories`, not a store, and a store-side rename or delete by another viewer was not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261119/r1/` (frames 06, 07, 09).

**Previous record:** 2026-11-16 (nightly maintenance). **Product commit:** `96644a29` (GitLab origin/main; rooms-client 0.118.0; unchanged since the 2026-11-15 pass). **Scope:** `/rooms/` (18177) and `/chat/` (18178), people stub and session-capture shim: `view=room&alerts=board` → hover **Ring store-5xx** → dialog **store-5xx at a glance**. Bare, it reads **store-5xx**, **Ring**, **3 open** with no chart (`/rooms/`). With a seeded 30-point series it shows 30 bars and "67% answered · 3 open · 4m to ack" on both hosts. The route smoke still finds `?panel=alerts` blank on both hosts. **Limitations:** the series is a seed, not daemon data; the Log trend line and the per-bar hover title were not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261116/r1/` (frames 01, 02).

**Previous record:** 2026-11-09 (nightly maintenance). **Product commit:** `82390825` (GitLab origin/main; rooms-client 0.114.0; 49 commits past `08fe407b`). **Scope:** `/rooms/` and `/chat/` `view=room&alerts=board`, with the people stub: dialog **Alerts board** on both hosts; `[data-alerts-group]` count 1 on `/rooms/` and 0 on `/chat/` (the `/chat/` `alertsStub` has no `lastRefreshedAt`). **Limitations:** no daemon feeds. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261109/r1/`.

**Previous record:** 2026-11-08 (nightly maintenance). **Product commit:** `08fe407b` (GitLab origin/main; rooms-client 0.112.0; unchanged since the 2026-11-07 pass). **Scope:** `/rooms/` (18183) `view=room`: the strip (`store-5xx`); `alerts=board`: the automatic **Alerts** group (new). `/chat/` (18184): no group under `alerts=board`, because the cloud stub lacks `lastRefreshedAt`. **Limitations:** `panel=alerts` still renders blank on both hosts (carried). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261108/r1/`.

**Previous record:** 2026-11-07 (nightly maintenance). **Product commit:** `08fe407b` (GitLab origin/main; rooms-client 0.112.0; 89 commits past `ea399e62`). **Scope:** `/rooms/` (18180) and `/chat/` (18181) `alerts=board`: the strip **store-5xx · check pods**. **Limitations:** `panel=alerts` still blank on both hosts. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261107/r1/`.

**Previous record:** 2026-11-06 (nightly maintenance). **Product commit:** `ea399e62` (GitLab origin/main; rooms-client 0.111.0; 74 commits past `873a57ce`). **Scope:** `/rooms/` (18180) and `/chat/` (18181) `alerts=board`: the strip **store-5xx · check pods**. **Limitations:** `panel=alerts` still blank on both hosts. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261106/r1/`.

**Previous record:** 2026-11-04 (nightly maintenance). **Product commit:** `ce14d4ba` (GitLab origin/main; rooms-client 0.109.1; 16 commits past `ba4389e7`). **Scope:** `/rooms/` (18160) `?view=room&alerts=board` shows `store-5xx`; the route smoke mounted every alerts route except the carried blank `?panel=alerts` (both hosts). **Limitations:** the tape card was not re-driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261104/r1/` (`smoke/`).

**Previous record:** 2026-11-03 (nightly maintenance). **Product commit:** `ba4389e7` (GitLab origin/main; rooms-client 0.108.0; one CI-only commit past `3f8f24bc`). **Scope:** `/rooms/` (18143) and `/chat/` (18144): the firing strip **store-5xx · check pods** with **I'm on it** and **Open**; `alerts=board` → **Alerts board**; `alerts=amber`; the `alert-card` gallery with **Discuss**, **I'm on it**, **Mark fixed** and **Flag noisy**. **Limitations:** `?panel=alerts` is still blank on both hosts. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261103/r1/` (`al-*`).

**Previous record:** 2026-11-02 (scheduled maintenance). **Product commit:** `3f8f24bc` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18141): `view=room` strip **store-5xx · check pods**; `alerts=board` → dialog **Alerts board** with **All alerts**; `surface=alert-card` **Discuss**, **I'm on it**, **Mark fixed**, **Flag noisy** after a 2.5 s mount. `/chat/` (18142): `alerts=board` → **Alerts board**. **Limitations:** `?panel=alerts` still blanks the shell (`#root` empty at 3 s). Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261102/r1/`.

**Previous record:** 2026-11-02 (nightly maintenance). **Product commit:** `3f8f24bc` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18137): `view=room` strip **store-5xx · check pods** (with `alerts.css` injected); `alerts=board` → **Alerts board** on both hosts; `fixture.html?surface=alert-card` → **Discuss**, **I'm on it**, **Mark fixed**, **Flag noisy**. **Limitations:** `?panel=alerts` still blanks the shell on both hosts (load smoke). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261102/r1/`.

**Previous record:** 2026-11-01 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18137): `?view=room` strip **store-5xx · check pods** with **I'm on it** and **Open**; `alerts=board` → the **Alerts board** dialog; `fixture.html?surface=alert-card` → the card with **Discuss**, **I'm on it**, **Mark fixed** and **Flag noisy**. `/chat/` (18138): the strip and the board. `?panel=alerts` still blanks the shell on both (smoke). **Limitations:** claim, create, the alerts home and the dock door stay pending; the strip and board remain unstyled in the fixture. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261101/r1/` (`alerts-01` to `alerts-03`, `chat-12`).

**Previous record:** 2026-10-31 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18135): `?view=room` strip **store-5xx · check pods** with **I'm on it** and **Open**; `?alerts=board` → dialog **Alerts board** (Ring store-5xx 3 #ops, Log relay-latency #ops, **New alert...**, **All alerts**); `fixture.html?surface=alert-card` → **Discuss**, **I'm on it**, **Mark fixed**, **Flag noisy**. `/chat/` (18136): the strip and the board. `?panel=alerts` still blanks the shell on both (smoke). **Limitations:** Claim and create effects, the dock **Alerts** door, `#/alerts` and the unstyled strip (no `alerts.css` in the fixtures). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261031/r1/`.

**Previous record:** 2026-10-30 (scheduled maintenance). **Product commit:** `47cb13bf` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/`: strip `store-5xx · check pods` with **I'm on it**; `alerts=board` **Alerts board** with **Ring store-5xx…**, **Log relay-latency#ops**, **New alert...** and **All alerts**; `fixture.html?surface=alert-card` **Discuss**, **I'm on it**, **Mark fixed**, **Flag noisy**. `/chat/`: strip and board. On neither host does any element carry an `Alerts:` name, so the beacon sub-feature was rewritten from `dc6a9a47`. **Limitations:** The dock **Alerts** door needs a channel with a live feed. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261030/r1/` (frames 46-47).

**Previous record:** 2026-10-29 (nightly maintenance). **Product commit:** `cdfb1b0f` (origin/main; rooms-client 0.108.0). **Scope:** `?view=room&alerts=board` showed the strip `store-5xx · check pods` and the board with **Ring store-5xx**, **Log relay-latency**, **New alert...** and **All alerts**, on `/rooms/` and `/chat/`. On `/chat/` the board is an `aside` named **Alerts board**; that name is not in `innerText`, so a text search for it misses. Query the label. **Limitations:** Claim, create and the alerts home are fixture no-ops; the fixture stylesheet gap still applies. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261029/r1/` (frames 04, 33, 62).

**Previous record:** 2026-10-28 (nightly maintenance). **Product commit:** `2dd7aad1` (origin/main). **Scope:** `?view=room&alerts=board` showed the strip `store-5xx · check pods` and the **Alerts board** dialog with **Ring store-5xx**, **Log relay-latency**, **New alert...** and **All alerts**. **Limitations:** `surface=alert-card`, claiming, creation and the alerts home were not driven; the fixture still lacks `alerts.css`. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261028/r1/` (frame 17).

**Previous record:** 2026-10-27. **Product commit:** `6c15b0fb286e9dc1b6cb130c9c97cd7e0afa9254` (origin/main). **Scope:** `alerts=board` showed the strip `store-5xx · check pods` and, once measured, the **Alerts board** dialog with **Ring store-5xx 3 open, nobody on it #ops83d ago**, **Log relay-latency#ops**, **New alert...** and **All alerts**. `surface=alert-card` showed Discuss / I'm on it / Mark fixed / Flag noisy. **Limitations:** Claiming, feed creation, the alerts home page and real delivery remain fixture no-ops or pending. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261027/r01/` (frame 26). Previous record: 2026-10-26 at `5820fbea`.
