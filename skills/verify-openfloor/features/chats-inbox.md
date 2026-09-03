# Chats inbox

The Chats tab is the unified inbox: direct messages and server rollups in one
list, each row showing a name, a timestamp and a preview, with unread badges.
Above it sit a search field, a filter drawer, an alerts control and a
notifications bell; a floating `+` opens the new-conversation menu.

## Sub-features

- `inbox-list` renders DM rows and server rollup rows in one feed.
- `inbox-search` filters rows by typed text.
- `inbox-filter` opens the filter drawer beside search: an All chats / Servers /
  Direct messages choice plus an `Unread only` switch.
- `inbox-alerts` surfaces ringing feeds.
- `inbox-activity` opens notifications and requests.
- `inbox-new` expands the `+` into New Group / New Server / Add Friend /
  Connections.
- `inbox-jump` opens the jump-to-conversation control.
- `inbox-select` enters row multi-select and its bulk-action menu.

## How to get to it (user POV)

- Launch the app. Chats is the default tab.
- From anywhere, tap **Chats** in the bottom dock.

## Driving it with control-openfloor

Preconditions:

- `./control-openfloor doctor` exits zero.
- `./control-openfloor app open` returned a snapshot containing
  `[other] "Primary navigation"`.

Stable handles on this screen:

| Handle | What it is |
|---|---|
| `label="Chats inbox"` | the list container |
| `label="Search chats"` | the search text field |
| `label="Filter chats"` | the filter drawer control |
| `label="Jump to a conversation"` | header jump control |
| `label="Open notifications and requests"` | the bell |
| `label="Start a new conversation"` | the floating `+` |
| `label="Alerts, checking"` / `label="Alerts: 5 feeds are ringing"` | alerts, **text varies with state**; drive it as `id=alerts-header-button` ([alerts](./alerts.md)) |
| `label="Chats viewport"` | the tab's outer container |
| `label="Cancel selection"`, `label="Selection actions"` | multi-select mode; the actions are production writes |

Inside the filter drawer:

| Handle | What it is |
|---|---|
| `label="Close chat filters"` | dismiss |
| `label="All chats, Servers and direct messages"` | the default scope |
| `label="Servers, Only OpenMarket server inboxes"` | server rollups only |
| `label="Direct messages, Only one-to-one conversations"` | DMs only |
| `label="Unread only"` | a `[switch]`, with the copy *"Hide conversations you have read"* |

Row labels follow `"<name>, <when>, <preview>"` for DMs
(`"geraldlee, Yesterday, still removed sadly"`) and
`"<server>, OpenMarket server"` for rollups (`"OpenMarket, OpenMarket server"`).

- **Reach the inbox.** Run `./control-openfloor app open`. The returned snapshot
  carries `label="Chats inbox"` and the dock shows `Chats, <n> unread`
  `[selected]`.
- **Open a conversation.** Match the row on its stable part, never the whole
  label. Run `./control-openfloor device find "geraldlee"`. The transcript
  replaces the list and `label="Back"` appears.
- **Search.** Run
  `./control-openfloor device fill 'label="Search chats"' "ger" --settle`.
  The settled diff shows non-matching rows removed and adds the hint cell
  *"Press Search to look inside channel and DM message history."* — filtering
  the inbox and searching message history are two different things. **The
  field's accessible name becomes the typed text**, so it is
  `label="Search chats"` only while empty; afterwards address it as
  `label="ger"`.

  To clear it, either press the field's own clear control — an **unlabelled
  16×16 `[button]` that appears inside the field only while it has text**, so it
  has to be pressed by coordinates, e.g. `./control-openfloor device press 317
  147` on a 402×874 frame — or type backspaces:
  `./control-openfloor device type $'\b\b\b'`, one per character. Both were
  verified 2026-09-03. `fill … ""` is still rejected, and `app reset` is no
  longer necessary for this.
- **Open the filter drawer.** Run
  `./control-openfloor device press 'label="Filter chats"' --settle`. **This
  fails on a dev client with the Tools button on** — the floating
  `gearshape.fill` overlay swallows the tap and the Expo dev menu opens
  instead. Turn the Tools button off first; see the gotcha.
- **Open activity.** Run
  `./control-openfloor device press 'label="Open notifications and requests"' --settle`.
  Accepting, declining or cancelling a request is a **production write** — read
  the surface, do not action it.
- **New-conversation menu.** Run
  `./control-openfloor device press 'label="Start a new conversation"' --settle`.
  The settled diff adds **four** entries, each labelled `"<Title>, <copy>"`:
  `New Group, Choose friends for a group conversation`,
  `New Server, Create an invite-only OpenMarket server`,
  `Add Friend, Send a friend request by username`, and
  `Connections, Find a friend and open a direct message`. Opening the menu is
  free; creating anything is not. Dismiss it with
  `./control-openfloor device back`.
- **Proof.** Capture the pair:
  `./control-openfloor device screenshot --out "$PWD/artifacts/<run>/<rev>/inbox.png" --normalize-status-bar`
  alongside the `--settle` diff that produced the state. Then
  `./control-openfloor evidence publish <run-id> <revision>`.

## Gotchas

- **Row labels are not stable across a cold boot.** Before the space-roles
  roster warms, rows read `"G, geraldlee, Yesterday, …"` (avatar initial + raw
  handle); after it warms the same row reads `"geraldlee, Yesterday, …"` and
  others resolve to display names (`nicholas_trontal` → `Nicholas`,
  `ryanng0611` → `ryan`). Snapshot twice, or assert only after the roster warms.
- **Unread counts drift with no interaction.** `Chats, 1712 unread` became
  `659`, `657`, `654` across one session. Never exact-match a label containing
  a count, and never assert an exact number as a result.
- The list virtualizes and the scroll area reports the *first* row's label as
  its own name. Assert a row, not the container.
- Long previews are inlined verbatim into the label, including code fences and
  URLs. Match a short leading substring with `find`, not the full label.
- The alerts control's label changes with state (`Alerts, checking` while it
  resolves). Do not build a selector on the ringing variant unless you have
  waited for it.
- **The dev-client Tools button eats `Filter chats`.** With the expo-dev-client
  floating gear on screen (`[other] "gearshape.fill"` in the snapshot), pressing
  `label="Filter chats"` opens the **Expo dev menu**, not the drawer —
  reproducibly, and by raw coordinates too, even though the gear's own image
  rect sits ~30pt lower than the control. Recovery is
  `press 'label="Close"'`. The fix is to turn the Tools button off once, which
  this lane now treats as a precondition (see the skill's Launch section).
- **A text field's label is its content once it has any.** This bites every
  editable target, not just search: capture the handle before you type, and use
  the typed value afterwards.
- **The activity and alerts destinations are their own surfaces.** `inbox-alerts`
  and `inbox-activity` are entry points here; what is behind them lives in
  [alerts](./alerts.md) and [activity-and-requests](./activity-and-requests.md).
  Pressing the bell or the beacon is not verifying those screens.
- **The inbox is often too short to scroll.** `scroll down` returned zero
  changes on a seven-row list. Do not build a parking or virtualization proof on
  scroll offset here — use retained search state instead
  ([tab-navigation-and-parking](./tab-navigation-and-parking.md)).
- Every handle in this file re-verified live 2026-09-03 on `f2c3f88`.
