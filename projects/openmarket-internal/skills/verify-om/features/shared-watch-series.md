# A shared watch carries its series

*Re-driven 2026-11-24 after two fixes, om `70a057fbe5` (#2699, merged `9f5fc1fd1c`) and `506965cff6` (#2700, merged `cc28549836`), same rig, registry `9b98ef8`, relay `e9e3ad2`. 48 of 48 plain follows and 12 of 12 follows that carry a series exited 0 with no `database is locked` (main had failed 15 of 48); 6 of 6 follows sent right after a share never answered the binding mismatch; 12 unfollow and follow cycles left exactly 1 FEED view in the follower's chart, from 1 add in total. Not verified: the compiled binary, a busy daemon, a production relay's 15 second activation tick.*

*Verified: 2026-11-24, om `dedf578b8e` (the head of #2696, merged as `e42f365a8c`), registry main `9b98ef8` (!278), relay main `e9e3ad2` (!54), collab `18845f6`. Driven on a local rig of the real relay, registry and collab from source, with two om lanes (publisher and follower) and made-up accounts, nothing off loopback. `journey.sh` passed 47 of 47 checks in 516 s. The follower's chart was photographed on 2026-11-23 on the pre-rebase head `8a7bd2b0a8` with the chart app at `c8a88ec824` against a made-up backend stand-in. Not verified: the private and priced doors, a real click on the registry page's button (its request body was replayed to the follower lane), the chart app against production services, the compiled binary.*

A person shares a watch that writes a relay feed (pushed readings, or a charted watch) and the share carries the series. The share card names it and who reads it, the pack manifest holds a `feed` reference, and the feed's access follows the share's door. A person who follows the watch in their own om gets the series recorded on the follow and one chart of it in their own workspace. The registry page of the pack shows the series.

## Sub-features

- `share-series`: `om watch share <watch>` of a feed-bearing watch stages the series by default. The card and `face_rows` carry `Series: N columns, read by anyone` (public door), `read by followers you approve` (knock), `read by people you invite` (private), `read by buyers` (priced). `--no-series` (`series: false`) drops the row and brings back `Producer not included…`. A recipe-only share, a folder share and a share of a watch with blanks stage none. An inbound watch with no declared or known columns stages none.
- `feed-access`: before anything is published the feed is declared `public` on a public door, or `followers` with `followers_of.topic_id` set to the share's topic on any other. A relay refusal stops the share with one line of cause and one of fix (`share_series_refused`, `share_series_quota`, `share_series_topic_not_owned`, `share_series_unreachable`, `share_series_signed_out`) and nothing is published. A later declaration (a readings edit, a key rotation) sends no `visibility`.
- `take-back`: a re-share with `--no-series`, and a package delete, set the feed back to `private`. The new version's manifest has no `feed`.
- `manifest-feed`: the pack manifest carries `feed: {address, title, cadence_s, values: [{key, unit?}]}` beside `share` only. A dry run shows it as `series.feed` in the JSON result, since a dry run has no topic.
- `publisher-show`: `om watch show` on the shared watch prints `Series: read by <who>`.
- `follow-series`: the follow card shows `Series: <title>, N columns, adds a chart to your workspace`; with `--no-chart` (`chart: false`) it shows `Series: <title>, N columns`. The follow watch's `stream` binding stores `feed`, and `chart_id` once charted. The result carries `series: {address, columns, chart: {status: added|off|not_added, …}}`.
- `follow-chart`: one chart named after the watch lands in the follower's workspace: main symbol `feed:<scope>/<name>:<column>` on exchange `OM`, and ONE FEED view, a line over the columns. Candles are added only for a series that holds open, high, low and close. A chart that cannot be made never fails the follow; the result's `row` says why (`no chart sign-in (om login)`, `the chart service did not answer`, `the chart service refused it (<code>)`).
- `chat-receipt`: after a follow from the chat card, the receipt shows `Chart: <url>` under `✓ Following <name>`, or the not-added row.
- `knock-chart`: on a knock door the knock card shows the Series row, the consent is stored as `chart: true` on the knock's pending record, and the chart is made when the publisher approves.
- `follower-show`: `om watch show` on the follow prints `Series: @scope/watch.<slug>, N columns`.
- `series-only-change`: a new version on the same topic whose only change is the series is adopted with no review. The binding gains or drops `feed`; no chart is made. A review raised for another reason carries `Series: added, N columns, adds a chart to your workspace` or `Series: removed`.
- `refollow-once` (#2700): following again after an unfollow reads the chart first and adds only a view it does not hold, so the chart keeps one view however many times the person re-follows. A view the follower removed comes back once; a view they changed is left alone and the missing one is added beside it. A chart that cannot be read answers `not_added` and the follow still lands.
- `follow-opening` (#2699): a follow sent while a fresh share's topic is still activating answers `stream_topic_opening` (`… was shared moments ago and is still opening` / `Nothing was created; run om watch follow … again in a few seconds.`) and creates nothing. A closed topic or a real disagreement keeps `stream_topic_binding_mismatch`.
- `knock-receipt` (#2699): after a knock from the chat card the receipt reads `Access requested for <pkg>. The publisher decides; you'll see their answer here. Open /follows to check it or stop waiting.`, with a line per status (unconfirmed, approved, denied).
- `unfollow-chart`: `watch_unfollow` leaves the chart and answers `Chart: stays in your workspace (<url>)` when the follow had charted.
- `followers-read` (relay): a feed declared `followers` is read by its owner, its token and every signed-in account its topic admits; a stranger, a signed-out reader and a `?chart=` grant get 403 `feed_private` ("…is read by the followers of its owner's topic"). A plain read holds its answer up to 60 s.
- `registry-series-block` (registry): the pack page shows a Series block. On a free public door it draws one server-rendered line from the relay's bars with `Read by anyone`, the state and last reading, the range, the cadence and the columns. On any other door it shows the columns, the cadence and who reads, and makes no relay read.
- `registry-follow-door` (registry): `GET /v1/packages/:scope/:name/follow` answers `manifest.feed` to every caller it answers, a caller who has only knocked included.

## How to get to it (user POV)

The publisher runs `om watch share <watch>` (or asks om chat to share it) and reads the card. A friend opens the registry page `/@scope/name`, sees the series, and presses the page's button (`Follow` on a free posts-only share), or pastes the link or `@scope/name` into om chat, or runs `om watch follow @scope/name`. The follow card names the series. After the yes, the reply links the chart in their own workspace.

## Driving it with control-om

### The rig

The scripts are in the task's evidence folder, `dev-notes/om-series-watch-distribution/run-artifacts/rig/` (README, `scripts/env.sh`, `bin/rig-up`, `bin/rig-down`, `bin/rig-reset`, `journey.sh`). One rig is a relay served on 127.0.0.1 with mongod, a registry over HTTPS with a rig CA (the registry refuses an `http://` origin for device enrollment), a stand-in for auth and the chart backend, collab, and two `control-om` lanes. Every port takes an override from the environment (`RIG_*_PORT`, defaults 18120 to 18129); another run may hold the defaults, so check with `lsof` and move the range. Export `RIG_OM`, `RIG_REGISTRY_TREE` and `RIG_RELAY_TREE` to the trees under test.

- Every om origin is pinned to the rig or to `http://127.0.0.1:9`. An unset `OM_LEDGER_ORIGIN` dials the production relay.
- A lane with no model holds inbound events in intake. The journey sets the watch to `--classifier-mode accept_all` so posts flow.
- Never pipe `rig-up` into another command. The lanes inherit the pipe and the command never returns.

### The journey

`journey.sh` replays, from a clean rig: the public share and its card; the feed staying public after a readings edit; the follow from the registry page's `/open` body through an attached `om chat` (`tty-drive.py`); the receipt's chart link and the workspace's owner; `om watch show`; the follower's workspace views in collab (one FEED, plot `line`); the follower reading the publisher's rows; the knock share (stranger 403, follower 403 then 200 after approval, the daemon charting after approval); a series-only change against a standing follow in both directions; and the take-back. It prints one verdict line per check and exits 0 only when all pass.

### By hand

- Publisher: `watch create "<label>" --slug <slug> --inbound --cadence 1m --column value:% --column volume`, push readings through the rows door, then `watch share <slug> --door public --yes --accept-terms --format json`. Read `face_rows` and `series`.
- Signed-out check: `curl <relay>/api/v2/feeds/<scope>/watch.<slug>/head` answers 200 with `visibility: public`.
- Follower: `watch follow @<scope>/<name> --yes --format json`, then `watch show <follow-slug>`, then read the workspace from collab with the follower's key.
- Which relay build answers, with no credentials and no state change: an unauthenticated `PUT /api/v2/feeds/<any>/<any>` with `{"title":"p","cadence_s":60,"visibility":"followers","followers_of":{"topic_id":"not-hex"}}` answers `feed_invalid` naming `followers_of.topic_id` on a build with `followers`; an older build refuses the visibility.

### The chart frame

The chart app boots against a made-up backend stand-in once it answers `GET /api/v1/workspaces` and the compiled-in hostnames in `src/environment/index.ts` are pinned dead. Isolate the browser with `--proxy-server=http://127.0.0.1:9` (loopback goes direct). The dev server needs about 3 GB of heap for a second full page load.

## Gotchas

- agent-browser's `--allowed-domains` pauses every request and left 517 vite module requests unanswered, so the chart app sat on its start screen. Use the dead proxy.
- A tree older than #2699 (`9f5fc1fd1c`) can exit `om watch follow` 2 with `database is locked` while the follow goes live, about one time in three on the rig, and answers `stream_topic_binding_mismatch` to a follow sent within seconds of a share. Since #2699 a too-early follow answers `stream_topic_opening`; `journey.sh` and `follow-race-setup.sh` poll until the follow lands.
- A tree older than #2700 (`cc28549836`) adds the series' view again on every re-follow; after ten the chart service refuses with `TIER_LIMIT_EXCEEDED` and the follow answers `not_added`. `rig/scripts/follow-series-race.sh` prints the FEED view count per cycle.
- A daemon's first catch-up pass, about 10 s after boot, can post a second follow receipt to the registry for a follow that already posted one (seen 2026-11-24, unchanged by these PRs). Count receipts from the second cycle on.
- After a knock is approved, a plain read by the follower can stay 403 for up to 60 s. The journey waits it out.
- A dry run cannot put `feed` in its staged manifest. Read `series.feed`.
- The registry page cannot call the relay from the browser (CSP). The line is drawn on the server; a relay that does not answer leaves the facts and drops the line.
- An om that sends `feed` to a registry without the field has its share refused for the unknown key. The registry must be deployed first.
