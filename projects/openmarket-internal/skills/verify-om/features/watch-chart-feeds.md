# Watch charts on their watch's feed

*Verified: 2026-11-17, live on a signed-in daemon (`@dboon333`, free-tier relay scope of 25 feeds) built from PR #2573's first commit (`8c3e1eb75d`). Merged 2026-11-18 as `b935174603`. The realign and the title rewrite were driven live. The quota-triggered slot reclaim in the merged code was not driven live, because the home was already under its limit; its deletion set was proved by the first commit's live run and by replaying the merged code on a copy of the home database. Evidence: `http://127.0.0.1:8098/om-chart-series-adapt/r1/`.*

A charted watch's series loads from the watch's relay feed (#2475), titled by what it measures (#2533). This entry covers how charts made before those changes catch up, and how a home reclaims feed slots when the relay refuses a feed at the account's limit.

## Sub-features

- `realign`: a cleared series whose main pane, or FEED pane, still draws the series' old per-key feed (`feed:<scope>/watch.<slug>.<key>:value`) moves to the watch's feed (`feed:<scope>/watch.<slug>:<key>`) at that watch's next reading. A pane on any other feed or column is left as drawn.
- `legacy-title`: a series or FEED pane titled `<watch label>: <key>` by om takes the measure title a new chart gets (`Current wave height`). A title anyone else wrote stays.
- `slot-reclaim`: a `feed_quota` refusal starts one sweep. It reads every chart workspace the home holds rows for, deletes this scope's auto feeds that no pane draws, no configured or archived watch needs, no stored series names and no published series uses, then lifts the day-long hold so the refused feed is made on the next flush.

## How to get to it (user POV)

Nothing to run. Charts made before #2475 move at their watch's next reading. A blank chart behind `keeps its snapshot: feed_quota` in `runner.log` converts once a sweep frees a slot.

## Driving it

### Read the state

- Chart target: `chart_show <workspace>`, `metadata.symbol`. A legacy target reads `feed:<scope>/watch.<slug>.<key>:value`; a realigned one reads `feed:<scope>/watch.<slug>:<key>`.
- Home feeds: `sqlite3 -readonly <home>/om.sqlite "select key, value from meta where key like 'feed_push_outbox.%'"`. `auto_feeds` lists the feeds this home made, `retired_feeds` the pending deletes, `quota_refused_feeds` the holds.
- Series rows: `collab_sticky_payloads` (`payload_json` `clear`, `framing_json` `feed`).
- The home is under `~/.openmarket/accounts/<user>/`, but the watch store resolves from `OM_HOME=~/.openmarket`. A script pointed at the account directory lists zero watches.

### Live realign (2026-11-17)

1. Before: `qFLlMo4x` targeted `feed:dboon333/watch.kl-precipitation.current_precipitation:value` and stopped on Nov 13. Its row's `framing.feed` already named `@dboon333/watch.kl-precipitation`.
2. Install the build and wait for the watch's next reading (hourly here).
3. Seen at 10:13Z: the target became `feed:dboon333/watch.kl-precipitation:current_precipitation`, and the chart drew through Nov 17.

### Live reclaim (first commit, 2026-11-17)

1. Before: `auto_feeds` held 37 addresses against a cap of 25. `0BHy6V8d` was blank, and `runner.log` read `keeps its snapshot: feed_quota`.
2. After the install, `auto_feeds` held 23: 15 deleted and `watch.significant-wave-height` created. `retired_feeds` and `quota_refused_feeds` were empty.
3. At the watch's next reading (10:34Z) the payload cleared with its feed reference, and the chart drew from the feed.

### Replay on a database copy

`sqlite3 -readonly <home>/om.sqlite ".backup <scratch>/om.sqlite"`, then run the retire or reclaim function against the copy with `OM_HOME=~/.openmarket` and a reader that wraps `savedWorkspaceDocument`. On 2026-11-18 the merged code read 11 workspaces and named the same 15 feeds for the 37-feed state, and made 0 reads and deleted nothing for the current state.

## Gotchas

- The reclaim only runs on a `feed_quota` refusal. A home under its limit never sweeps, so it can only be driven live by filling a scope.
- `keeps its snapshot: no_live_series` every hour on a converted chart is benign: the row is cleared after conversion.
- The screenshot renderer drew `gpVPAxzJ`'s six lower FEED panes empty while their settings were unchanged; not investigated.
- Not covered: a pane in a workspace the home holds no rows for, or on another home of the same account, does not protect its feed.
- The main-pane legend reads `<watch label> · <column>` from the feed declaration and the frontend; om cannot retitle it.
