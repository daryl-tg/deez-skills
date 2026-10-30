# Alerts

The app-wide alert strip, the channel alerts board, and the alert card in the
tape. Alert feeds ring when a watched condition fires. Webhook conversion lives
in [settings-and-appearance.md](settings-and-appearance.md).

## Sub-features

- **Alert strip** (`packages/chat-ui/src/components/AlertStrip.tsx`): an app-wide
  bar above the content card. It renders `name · actionLine` with a timestamp and
  the buttons **I'm on it** and **Open**.
- **No channel-header beacon since `dc6a9a47`** (2026-10-01). `ChatPane.tsx`
  stopped mounting `AlertsBeacon`; the file survives only for the board's
  `BOARD_WIDTH`. A channel with a live alert feed gets an **Alerts** door on
  the right-edge dock instead (`RightPanels.tsx:178-199`, gated by
  `rightSlotTabsFor`), and the sidebar carries the ringing count. The fixture's
  `#ops` has no live feed, so its dock shows Library, Bookmarks, Members and
  Pins only, and the door is live verification pending (re-measured
  2026-10-30 on both hosts: no `[aria-label^="Alerts:"]` element anywhere).
- **Alerts board** (`AlertsBoard.tsx`): a dialog named **Alerts board** with Ring
  feeds and Log feeds, one button per feed, plus **New alert...** and **All
  alerts**.
- **Alert card** in the tape (`AlertMessageRow.tsx`), with **Discuss**, **I'm on
  it**, **Mark fixed** and **Flag noisy**.
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
| `shell-fixture.html?view=room&alerts=board` | The board dialog open and pinned (`shell-fixture.tsx:1440-1448`) |
| `shell-fixture.html?view=room&alerts=amber` | A second strip state (`:1452-1453`) |
| `shell-fixture.html?view=room&alerts=quiet` | No strip: use this for every non-alert proof |
| `fixture.html?surface=alert-card` | The alert card with its four actions |

On the board, the feed buttons are named with their state, for example
`Ring store-5xx 3 open, nobody on it #ops78d ago` and `Log relay-latency#ops`.
Read the strip through `.alert-strip-text`, not the snapshot tree: its row is a
plain `generic` there.

## Gotchas

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
- **The shell fixture never imports `shared/alerts.css`** (only `src/main.tsx:22`,
  `apps/cloud/src/main.tsx:26` and the two gallery `fixture.tsx` files do). Under
  `alerts=board` the strip and board render as unstyled text. That has been
  true since at least `5820fbea`, so do not judge alert visuals from the shell;
  use `fixture.html?surface=alert-card` or the bundled app.
- **`?panel=alerts` blanks the whole shell on both hosts.** It is the
  channel's Alerts tab (`AlertsPanel.tsx`, mounted at `RightPanels.tsx:386-396`
  and opened in the product by `session.openAlertsTab`). The fixture's
  plain-object `alertsStub` (`shell-fixture.tsx:1435`) lacks members the
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

**Last verified:** 2026-10-31 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18135): `?view=room` strip **store-5xx · check pods** with **I'm on it** and **Open**; `?alerts=board` → dialog **Alerts board** (Ring store-5xx 3 #ops, Log relay-latency #ops, **New alert...**, **All alerts**); `fixture.html?surface=alert-card` → **Discuss**, **I'm on it**, **Mark fixed**, **Flag noisy**. `/chat/` (18136): the strip and the board. `?panel=alerts` still blanks the shell on both (smoke). **Limitations:** Claim and create effects, the dock **Alerts** door, `#/alerts` and the unstyled strip (no `alerts.css` in the fixtures). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261031/r1/`.

**Previous record:** 2026-10-30 (scheduled maintenance). **Product commit:** `47cb13bf` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/`: strip `store-5xx · check pods` with **I'm on it**; `alerts=board` **Alerts board** with **Ring store-5xx…**, **Log relay-latency#ops**, **New alert...** and **All alerts**; `fixture.html?surface=alert-card` **Discuss**, **I'm on it**, **Mark fixed**, **Flag noisy**. `/chat/`: strip and board. On neither host does any element carry an `Alerts:` name, so the beacon sub-feature was rewritten from `dc6a9a47`. **Limitations:** The dock **Alerts** door needs a channel with a live feed. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261030/r1/` (frames 46-47).

**Previous record:** 2026-10-29 (nightly maintenance). **Product commit:** `cdfb1b0f` (origin/main; rooms-client 0.108.0). **Scope:** `?view=room&alerts=board` showed the strip `store-5xx · check pods` and the board with **Ring store-5xx**, **Log relay-latency**, **New alert...** and **All alerts**, on `/rooms/` and `/chat/`. On `/chat/` the board is an `aside` named **Alerts board**; that name is not in `innerText`, so a text search for it misses. Query the label. **Limitations:** Claim, create and the alerts home are fixture no-ops; the fixture stylesheet gap still applies. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261029/r1/` (frames 04, 33, 62).

**Previous record:** 2026-10-28 (nightly maintenance). **Product commit:** `2dd7aad1` (origin/main). **Scope:** `?view=room&alerts=board` showed the strip `store-5xx · check pods` and the **Alerts board** dialog with **Ring store-5xx**, **Log relay-latency**, **New alert...** and **All alerts**. **Limitations:** `surface=alert-card`, claiming, creation and the alerts home were not driven; the fixture still lacks `alerts.css`. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261028/r1/` (frame 17).

**Previous record:** 2026-10-27. **Product commit:** `6c15b0fb286e9dc1b6cb130c9c97cd7e0afa9254` (origin/main). **Scope:** `alerts=board` showed the strip `store-5xx · check pods` and, once measured, the **Alerts board** dialog with **Ring store-5xx 3 open, nobody on it #ops83d ago**, **Log relay-latency#ops**, **New alert...** and **All alerts**. `surface=alert-card` showed Discuss / I'm on it / Mark fixed / Flag noisy. **Limitations:** Claiming, feed creation, the alerts home page and real delivery remain fixture no-ops or pending. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261027/r01/` (frame 26). Previous record: 2026-10-26 at `5820fbea`.
