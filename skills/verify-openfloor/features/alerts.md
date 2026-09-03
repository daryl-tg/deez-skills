# Alerts

The alerts beacon in the Chats header reports whether any monitored feed is
firing, and opens the alerts board: every feed grouped by state, each row naming
its channel, its unanswered count and when it last fired. A feed's own screen
lists its triggers.

## Sub-features

- `alerts-beacon` reports the aggregate state in the Chats header.
- `alerts-board` lists feeds grouped by state.
- `alerts-feed` opens one feed's trigger history.
- `alerts-activity` expands a feed's recent activity inline.
- `alerts-create` opens the new-alert sheet.
- `alerts-help` opens the explainer.
- `alerts-convert` converts a channel's webhooks into alert feeds.

## How to get to it (user POV)

- The beacon sits in the Chats header, left of the notifications bell. Tap it.
- Or from a channel: **Channel tools** → **Convert to alerts…** for
  `alerts-convert`.

## Driving it with control-openfloor

Preconditions:

- `./control-openfloor doctor` exits zero, start from the Chats root.
- **Creating, answering, muting or converting an alert is a production write.**
  Reading the board, opening a feed, expanding activity and reading the
  explainer are free. `alerts-create` and `alerts-convert` may be *opened* but
  not submitted.

Stable handles:

| Handle | What it is |
|---|---|
| `label="Alerts, checking"` | the beacon while it resolves |
| `label="Alerts: <n> feeds are ringing"` | ringing (singular: `<n> feed is ringing`) |
| `label="Alerts: <n> feeds need an answer"` | awaiting an answer (singular: `feed needs`) |
| `label="Alerts: nothing firing"` | quiet — **the beacon still renders and is still the way in** |
| `id=alerts-header-button` | the beacon by identifier — **state-proof, unlike its label** |
| `label="New alert"` | the create control |
| `label="How alerts work"` | the explainer |
| `label="Show <feed> activity"` / `label="Hide <feed> activity"` | a row's inline activity |
| `label="Load older triggers"` | history control on a feed screen |
| `label="Retry"` | the board's error-state retry |
| `label="Alerts"` | the board's own empty/error state block |

Feed rows are a composite: `"<feed>, in <channel>, <verb>, <n> unanswered[,
fired repeatedly with nobody responding for <n> days][, muted], last fired
<when>"`.

- **Read the beacon, then open it.** Because the label changes with state, drive
  it by identifier: `./control-openfloor device press 'id=alerts-header-button'`.
  Capture the label first if the beacon's own state is part of the claim.
- **Read the board.** `./control-openfloor device snapshot -i`. The header reads
  `<n> FEEDS ARE RINGING` over `"<n> feeds across <n> channels · updated <n>s
  ago"`, then a `Firing` section of rows.
- **Expand a feed's activity.**
  `press 'label="Show sentinel activity"' --settle` and assert the rows in the
  diff, then press the `Hide …` twin.
- **Open a feed.** Press the row (its `[button]` twin, not the `[cell]`), then
  assert with `wait text "<feed name>"`.
- **Leave.** The board is full-screen and **hides the dock**, so the
  selected-tab press is not available. Use
  `press 'role=button label="Back"'` — see the gotcha.
- **Proof.** `snapshot -i` (not a settle diff — see below) plus
  `./control-openfloor device screenshot --out "$PWD/artifacts/<run>/<rev>/alerts.png" --normalize-status-bar`.

## Gotchas

- **The board never settles, so `--settle` always times out on it.** The header
  carries a live `updated <n>s ago` ticker. `press … --settle` returns *"not
  settled after 10001ms — the UI kept changing for the whole settle budget"*
  and gives you no diff. Use `snapshot -i` or `wait text` for this screen, and
  reserve `--settle` for the rows, which do settle.
- **The first `Back` press after a settle timeout is swallowed.** Observed
  2026-09-03: `press 'role=button label="Back"'` reported *"Tapped … (28, 90)"*
  and left the board on screen; the second identical press returned to Chats.
  Assert you actually left with `snapshot -i` rather than trusting one press.
- **`label="Back"` is ambiguous here** — an `[other]` and a `[button]` both
  match. Always `role=button label="Back"`. This is the same wrapping-header
  shape as `Appearance`, `Back to settings` and `Back to chats`.
- **Never build a selector on a ringing-state label.** `Alerts, checking` is
  what a cold boot shows, and the count in the ringing variants drifts. Use
  `id=alerts-header-button`.
- **`Alerts` names two different things** — the beacon's states, and an
  `[other]` block that wraps the board's empty and error states. Assert the row
  or the header text, not the bare word.
- Verified live 2026-09-03 on `f2c3f88` (iPhone 17 Pro, iOS 26.5), with the
  board showing `5 FEEDS ARE RINGING` / `10 feeds across 8 channels`.
