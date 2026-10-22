# Alerts

The app-wide alert strip, the channel alerts board, and the alert card in the
tape. Alert feeds ring when a watched condition fires. Webhook conversion lives
in [settings-and-appearance.md](settings-and-appearance.md).

## Sub-features

- **Alert strip** (`packages/chat-ui/src/components/AlertStrip.tsx`): an app-wide
  bar above the content card. It renders `name · actionLine` with a timestamp and
  the buttons **I'm on it** and **Open**.
- **Alerts beacon** in the channel header (`AlertsBeacon.tsx:58-61`). Its name
  carries the state: `Alerts: nothing firing`, `Alerts: N feeds are ringing`, or
  `Alerts: N feeds need an answer`.
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
click **I'm on it** to claim it, or **Open** to read it. In the channel header,
the Alerts beacon says how many feeds are ringing, and the board lists every
feed in the channel so you can open one or start a new alert.

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
| `shell-fixture.html?view=room&alerts=board` | The board dialog open and pinned (`shell-fixture.tsx:1434-1442`) |
| `shell-fixture.html?view=room&alerts=amber` | A second strip state (`:1444`) |
| `shell-fixture.html?view=room&alerts=quiet` | No strip: use this for every non-alert proof |
| `fixture.html?surface=alert-card` | The alert card with its four actions |

On the board, the feed buttons are named with their state, for example
`Ring store-5xx 3 open, nobody on it #ops78d ago` and `Log relay-latency#ops`.
Read the strip through `.alert-strip-text`, not the snapshot tree: its row is a
plain `generic` there.

## Gotchas

- The beacon count and the board disagree, and both are fixture seeding: the
  beacon hardcodes three ringing feeds, and the board renders the two seeded
  rows. Do not report the gap, and do not caption a frame with the beacon count.
- **I'm on it** on the strip changes nothing in the fixture, and **New alert...**
  opens no create dialog. Both are fixture no-ops. Prove the controls render;
  claiming and creating need a daemon lane. Live verification pending.
- `#/alerts` has no fixture `?view=`, so the alerts home page is unreachable here.
  Live verification pending.
- Without `alerts=quiet` the strip shifts every surface below it. That is why
  the other guides add it.

### Verification record

**Last verified:** 2026-10-22. **Product commit:** `cd9f8c72a6522caccc3b6157a4990fb6c9d0b0cf` (origin/main). **Scope:** `/rooms/` lane at 1440x900. The default route showed the strip `store-5xx · check pods` with I'm on it / Open. `alerts=board` opened the **Alerts board** dialog with Ring store-5xx (3 open, nobody on it), Log relay-latency, New alert... and All alerts. `fixture.html?surface=alert-card` rendered Discuss / I'm on it / Mark fixed / Flag noisy. **Limitations:** Claiming, creating a feed, the alerts home page and real feed delivery were not exercised; the fixture no-ops them.
