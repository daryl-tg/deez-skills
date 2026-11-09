# Event ingest and fire

*Re-driven 2026-11-10 (nightly), tree `c9bc93a355` (origin/main, v0.493.1), guest lane on 18143, booted with no guest 429. `watch create nightly-probe --inbound`, `edit --classifier-mode accept_all`, `rotate-token --yes` (token kept out of evidence); the door 401 without the bearer and 202 with it (`event_id fdc29d20…`, `deduped:false`); `watch_committed`, `watch_appended`, `watch_fired` for that id (`fired_at` 19:20:31.319Z); the journal held it with `verdict: new story`; CLI `event push` `delivery: daemon`; the Watches row with `Pause`. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261110/r1/` (`cli/ingest-*`, `events2.sse`, `cli/journal.txt`, `02-watches.png`).*

*Re-driven 2026-11-09 (scheduled maintenance), tree `0d3d29cd27` (origin/main, v0.493.0), bare lane on 18145 (dummy `OM_API_KEY`, dead service URLs) with a scripted fake model on 18144. `watch create lane-probe --inbound`, `watch edit --classifier-mode accept_all`, `rotate-token` (token kept out of evidence), `/events/v1` `: stream opened`, ingest without a token 401, with it 202 `{accepted:true, deduped:false}`, and `watch history` showing the row; `event push` from the CLI answers `delivery:"daemon"`. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261109/r1/`.*

*Re-driven 2026-11-09 (nightly), tree `5bfa0ccf6` (origin/main, v0.492.0), guest lane on 18143, booted with no guest 429. door `401` unauthenticated, `202` with one `event_id`, duplicate `200 deduped:true`, paused `409`; `watch_committed`, `watch_appended` and `watch_fired` on that `event_id`; the journal row; CLI push `delivery: daemon`; the Watches row. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261109/r1/` (`cli/12-15`, `events.sse`, `watches.*`).*

*Re-driven 2026-11-08 (nightly), tree `5590b4d1c` (origin/main, v0.492.0), guest lane on 18141, booted in 2 s with no guest 429. `watch create lane-probe --inbound`, `watch edit --classifier-mode accept_all`, `rotate-token`; the door 401 without the token and 202 with it (`event_id 9e4ee570…`); `watch_committed`, `watch_appended`, `watch_fired` on `/events/v1` for that id (`fired_at` 19:19:41.796Z); the journal (`outcome: update`, `verdict: new story`); CLI `event push` `delivery: daemon`; the Watches row `working`, `Last update Just now`. Not re-driven: the plain-text body, the dedupe and the paused 409. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261108/r1/` (`cli/10-17`, `events.sse`, `alerts.png`).*

*Re-driven 2026-11-07 (nightly), tree `05f450fc5` (origin/main, v0.492.0), guest lane on 18141, booted with no guest 429. `watch create lane-probe --inbound`, `edit --classifier-mode accept_all`, `rotate-token --yes` (token redacted); the unauthenticated door push 401 `{"error":"unauthorized"}`, the authorized one 202 `event_id a89cf724…`; `/events/v1` carried `watch_committed`, `watch_appended`, `watch_fired` (`fired_at 19:22:24.367Z`) for it and again for the CLI push (`delivery: daemon`, `628208a2…`); `event-journal get lane-probe --file events.md` held both ids with `verdict: new story`; `/alerts` listed `lane-probe` with `Pause`. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261107/r1/` (`cli/01-07`, `cli/events.sse`, `01-watches.png`, `02-watch-detail.png`).*

*Re-driven 2026-11-06 (nightly), tree `50fcc594b` (origin/main, v0.492.0), guest lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), booted at 19:18Z with no guest 429, host load average 10 falling to about 3.3. `watch create lane-probe --inbound` then `edit --classifier-mode accept_all`; `rotate-token --yes` (token redacted in the evidence); the door push answered 202 `event_id b26679db…`, an unauthenticated push 401; `events.sse` carried `watch_committed`, `watch_appended` and `watch_fired` (`fired_at 19:19:07.191Z`); `event-journal get … --file events.md` held the id, `outcome: update` and `verdict: new story`; the `/alerts` row showed `lane-probe` with `Pause`. Evidence: `http://127.0.0.1:8098/vom-nightly-20261106/r1/` (`events.sse`, `cli/fire-*`, `01-alerts.png`).*

*Re-driven 2026-11-05 (nightly), tree `3a0ea623e` (origin/main, v0.492.0), guest lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), booted in 2 s at 19:19Z with no guest 429, host load average about 4.4. `watch create lane-probe --inbound` (`ingest_setup.endpoint` on 18163), `watch edit --classifier-mode accept_all` (`"classifier":{"mode":"accept_all"}`), `rotate-token --yes`; the door answered 202 `{"accepted":true,"event_id":"4efaa3e4…","deduped":false}` and 401 `unauthorized` without the bearer; the stream carried `watch_committed`, `watch_appended`, `watch_fired` (`fired_at` 19:19:22.355Z); the journal held `event-watch-event-id:4efaa3e4…` and `verdict: new story`; `event push` answered `delivery: daemon`; the Watches list held `checkbox "Select lane-probe"`. Evidence: `http://127.0.0.1:8098/vom-nightly-20261105/r1/` (`events.sse`, `cli/ingest-*`, `cli/journal.json`, `alerts.png`).*

*Re-driven 2026-11-04 (nightly), tree `9acb5fb56` (origin/main, v0.491.0), guest lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), booted in 2 s at 19:19Z with no guest 429, host load average about 3.5. On `lane-probe` (inbound, `accept_all`): `rotate-token --yes` (token redacted), unauthenticated door 401, authenticated door 202 `event_id de5220…`, the stream carrying `watch_committed`, `watch_appended`, `watch_fired` for that id (`fired_at 19:19:41.029Z`), `event-journal get lane-probe --file events.md` holding the id, `event push` `delivery: daemon`, and the dashboard row and detail page `/alerts/lane-probe`. Evidence: `http://127.0.0.1:8098/vom-nightly-20261104/r1/` (`cli/10-23`, `cli/events.sse`, `dash/dash-11*`, `dash/dash-12*`).*

*Re-driven 2026-11-03 (nightly), tree `777ee7f21` (origin/main, v0.488.0), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 2.8; the first `up` died on a guest sign-in 429 (35 minutes) and the lane booted in 3 s at 19:55Z. `watch create lane-probe --inbound`, `edit --classifier-mode accept_all`, `rotate-token --yes`; the door answered 202 (`event_id 60574fd0…`) and 401 `{"error":"unauthorized"}` without a bearer; `event push --kind filing` answered `accepted:true`, `delivery:"daemon"` (`12b2ef09…`); `/events/v1` carried `watch_committed`, `watch_appended` and `watch_fired` for each id (`fired_at` 19:56:17Z); `event-journal get lane-probe --file events.md` held both ids; the dashboard row and `/alerts/lane-probe` (H1 `lane-probe`) rendered. Evidence: `http://127.0.0.1:8098/vom-nightly-20261103/r1/` (`cli/80-85`, `cli/events.sse`, `dash-12_alerts_lane-probe.png`).*

*Re-driven 2026-11-02 (scheduled maintenance), tree `587ce2d0b` (origin/main, v0.480.3), lane on 18168 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 5. On `lane-lifecycle` (inbound, `accept_all`): `rotate-token --yes` (token kept in a shell variable), an unauthenticated POST 401 `{"error":"unauthorized"}`, the authorized POST 202 `{"accepted":true,"event_id":"3d1a0df7…","deduped":false}`, `/events/v1` carried `watch_committed`, `watch_appended` and `watch_fired` for that id, and `event-journal get … --file events.md` holds `event-watch-event-id:3d1a0df7…` with `outcome: update`. CLI `event push` answered `delivery:"daemon"`. The `/alerts` list shows the watch with **Pause**.*

*Re-driven 2026-11-02 (nightly), tree `2567b7974` (origin/main, v0.480.3), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 4. `watch create lane-probe --inbound`, `edit --classifier-mode accept_all`, `rotate-token --yes` (a 48-character token, redacted in the evidence). The door push returned `202 {accepted:true, event_id:"73a77abc…", deduped:false}` and the unauthenticated push `401 {"error":"unauthorized"}`; `event push … --kind filing` returned `event_id 97760eaa…`, `accepted:true`, `delivery:"daemon"`. The stream opened first carried `watch_committed`, `watch_appended` and `watch_fired` for each of the two ids (three lines per id). `event-journal get lane-probe --file events.md` held the door id and `outcome: update`. `/alerts` listed `lane-probe` with `Pause`, and `/alerts/lane-probe` opened with the H1 `lane-probe`. Evidence: `http://127.0.0.1:8098/vom-nightly-20261102/r1/` (`cli/40-46`, `events.sse`, `watches.png`, `watch-detail-lane-probe.png`).*

*Re-driven 2026-11-01 (nightly), tree `7ce379c45` (origin/main, v0.480.3), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 2.9. `watch create lane-probe --inbound` → `--classifier-mode accept_all` → `rotate-token --yes` (a 48-character token). The stream, opened first, carried `watch_committed`, `watch_appended` and `watch_fired` once each for the door push's `event_id` `d83bf0dc…` (202, `deduped:false`) and again for the CLI push's `026a4204…` (`delivery:"daemon"`); the unauthenticated push got 401. `event-journal get lane-probe --file events.md` held `event-watch-event-id:d83bf0dc…`. `/alerts` listed `lane-probe` with a `Pause` button and `/alerts/lane-probe` rendered its H1. Evidence: `http://127.0.0.1:8098/vom-nightly-20261101/r1/` (`events.sse`, `cli/50-56`, `dash-alerts*`).*

*Re-driven 2026-10-31 (nightly), tree `dfefe0a21` (origin/main, v0.480.2), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 1.6. `watch create lane-probe --inbound` → `--classifier-mode accept_all` → `rotate-token --yes` (a 48-character token). The stream, opened first, carried `watch_committed`, `watch_appended` and `watch_fired` once each for the door push's `event_id` `59e4975e…` (202, `deduped:false`); the unauthenticated push got 401. `event-journal get lane-probe --file events.md` held `event-watch-event-id:59e4975e…`, and the CLI push answered `delivery:"daemon"` on this idle host. `/alerts` listed `lane-probe` with a `Pause` button and `/alerts/lane-probe` rendered its H1. Evidence: `http://127.0.0.1:8098/vom-nightly-20261031/r1/` (`events.sse`, `cli/10-15`, `dash-alerts*`).*

*Re-driven 2026-10-30 (scheduled maintenance), tree `3cb50a821` (origin/main, v0.478.0), fresh lane on 18165, host load average about 140. `watch create maint-1030 --inbound` (`ingest_setup.token_minted: false`) → `--classifier-mode accept_all` → `rotate-token --yes`. An unauthenticated door push got 401. The stream, opened first, carried `watch_committed`, `watch_appended` and `watch_fired` for the door push's `event_id` `79a0c9cc…` (202, `deduped:false`). `event-journal get maint-1030 --file events.md` held the probe with `outcome: update` and `verdict: new story`, and `/alerts/maint-1030` read `working`. CLI `event push` returned `accepted:true` with `delivery:"daemon"`: at this load the busy-host `direct` write from the nightly did not recur. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261030/r1/` (frame 22, `cli/01-05`, `cli/events.sse`).*
*Re-driven 2026-10-30 (nightly, smoke depth), tree `3cb50a821` (origin/main, v0.478.0), lane on 18163, under a host load average near 150. `watch create probe-1030 --inbound` → `--classifier-mode accept_all`. `event push` returned `accepted:true`, but with `delivery:"direct"` and the note `The daemon is not running…`, although the lane was up (see Gotchas). An unauthenticated door push got 401. After `rotate-token --yes`, the door push got `202 {accepted:true, event_id:"1d7e0eba…", deduped:false}`. The stream, opened first, carried `watch_committed`, `watch_appended` and `watch_fired` with that id. `event-journal get probe-1030 --file events.md` held both probe texts, and the dashboard `/alerts/probe-1030` read `working`. Evidence is local only (the `8098` renderer did not answer): `artifacts/vom-nightly-20261030/r1/`.*

*Re-driven 2026-10-29 (scheduled maintenance), tree `7ec575e55` (origin/main, v0.467.0 plus #2194), fresh lane on 18161. `watch create lane-probe --inbound` → `--classifier-mode accept_all` → `rotate-token` (`ingest_token.token`). The POST to `/ingest/v1/lane-probe` returned `202` `{accepted:true, event_id:"c1a2fc12…", deduped:false}`. `/events/v1` carried `watch_committed`, `watch_appended` and `watch_fired` (`fired_at` 2026-10-29T01:35:52.191Z), and `event-journal get … --file events.md` held the probe text. The dashboard `/alerts/lane-probe` rendered the watch. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261029/r1/`.*

*Re-driven 2026-10-29 (nightly, smoke depth), tree `32ca0d6c7` (origin/main, v0.467.0), lane on 18103. `event push probe-1029 --kind filing` returned `accepted:true`, `delivery:"daemon"` and event_id `c6a50278…`. The stream, opened first, carried `watch_committed`, `watch_appended` and `watch_fired` with that id. `event-journal get probe-1029 --file events.md` held the probe text. An unauthenticated door push got 401. After `rotate-token --yes` (`ingest_token.token`), it got `202 {accepted:true, event_id:"ed1c76f2…", deduped:false}`. `notis` listed the fire, and the Watches row read `working`. Evidence: `http://127.0.0.1:8098/vom-nightly-20261029/r1/`.*

*Re-driven 2026-10-28 (scheduled maintenance, smoke depth), tree `186030b63` (origin/main): `event push probe-1028 --kind filing` returned `accepted:true`, `delivery:"daemon"`; `event-journal get --file events.md` then held the event with `outcome: update` and the watch runtime showed `rows: 1`. The SSE `watch_fired` stream was not re-read. Steps not named here keep the record below. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261028/r1/`.*

*Verified: 2026-10-28, tree `a8fa10974` (origin/main, v0.466.0), lane on 18103. `watch create lane-probe --inbound` gave `token_minted: false`. After `edit --classifier-mode accept_all` and `rotate-token --yes`, the door push returned `202 {accepted:true, event_id:"40f5835a…", deduped:false}`, and an unauthenticated push returned 401. The stream opened first carried `watch_committed`, `watch_appended` and `watch_fired`, all with that `event_id`, beside `tick_completed` and `subscription_metric`. `event-journal get lane-probe --file events.md` held `event-watch-event-id:<id>`, `outcome: update` and `verdict: new story`. The CLI `event push` returned `watch_id, event_id, accepted, deduped, delivery, notes`. Not re-driven: the dashboard row (ops-dashboard's lane showed the same row shape). Previous stamp `8fe6a8432` is an ancestor (10 commits).*

A user points a producer at a watch's inbound door and the daemon takes it from
there: the event is accepted, committed, appended to the watch's journal, and
fired. The fire shows up on the live event stream, in the journal on disk, and
as a watch row in the dashboard's selectable Watches list. This is the whole pipeline, and none
of it needs an account.

## Sub-features

- `ingest-cli` pushes an event through `om event push`.
- `ingest-offline` uses the daemon when reachable and falls back to the local
  store when it is down; if the daemon appears live but its endpoint is
  unreachable, the command refuses rather than risking a split write.
- `ingest-http` pushes JSON or plain text through `POST /ingest/v1/<watch>` with
  a minted bearer token (header preferred; `?token=` is supported).
- `fire-stream` emits `watch_committed`, `watch_appended` and `watch_fired` on
  `/events/v1`.
- `fire-journal` writes the event, its verdict and its id into the watch's
  `events.md`.
- `fire-dashboard` shows the watch in the selectable Watches list with its
  status and last-update time; the exact instant is in the row's `time` value.

## How to get to it (user POV)

- Create an inbound watch, then push events into it from a script or a service.
- Read what arrived with `om event-journal get <slug>`, or open the dashboard's
  Alerts page.

## Driving it with control-om

Preconditions:

- `control-om doctor` passes and the lane is the run's own.
- The lane is a guest, so the watch must classify without a model. That is
  `--classifier-mode accept_all`, and the flag is on `watch edit`.

- **Create the door.** Run
  `control-om om -- watch create lane-probe --inbound --format json`. The
  result carries `ingest_setup.endpoint`
  (`http://127.0.0.1:18101/ingest/v1/lane-probe`) and `token_minted: false`.
- **Make it model-free.** Run
  `control-om om -- watch edit lane-probe --classifier-mode accept_all --format json`.
  The result's source shows `"classifier":{"mode":"accept_all"}`. Skip this and
  the first push stalls on a missing LLM credential and the watch lists
  `broken`.
- **Mint the token.** Run
  `control-om om -- watch rotate-token lane-probe --yes --format json` and keep
  `ingest_token.token`. It is shown once.
- **Open the stream first.** Run
  `curl -sN --max-time 20 "$(control-om url /events/v1)" > artifacts/<run>/<rev>/events.sse &`
  and give it a second to print `: stream opened`. Opening it after the push
  proves nothing — the stream is live, not a backlog.
- **Push over the door.** Run
  `curl -s -w '\nhttp %{http_code}\n' -X POST "$(control-om url /ingest/v1/lane-probe)" -H "Authorization: Bearer <token>" -H 'Content-Type: application/json' -d '{"text":"<run-id>: pushed over the ingest door","kind":"filing"}'`.
  Expect `202` and `{"accepted":true,"event_id":"<id>","deduped":false}`.
  Plain text is also accepted with `Content-Type: text/plain`; it becomes the
  event's `text` field. A duplicate returns `200` with `deduped:true`; rejected
  events return `202` with `accepted:false`, and paused watches return `409`.
- **Read the stream.** `events.sse` carries three events for that same
  `event_id`: `watch_committed` (with `"outcome":"update"` and the title),
  `watch_appended`, then `watch_fired` with `fired_at` and `"confidence":1`.
  The fired payload leads with `"kind":"listener"`. These names lost their
  `event_` prefix in v0.35 — grep for `^event: watch_` and nothing else. The
  stream also carries unrelated siblings — `tick_completed` (predates v0.400.0),
  `subscription_metric` (seen at `db6e76ef5`: a transport metrics frame with
  `stream_id`, `adapter_id`, `subscriber_count`, `events_received`, ...)
  and `watch_inventory_changed` (new in v0.408.1, a reconcile-pass diagnostic
  carrying `{watches, armed, alerts, changed_at}`) — so a bare
  `grep '^event:'` returns more than this feature's three, and the second of
  those DOES start with `watch_`. Match `^event: watch_(committed|appended|fired)$`
  if you need it exact. No NEW sibling landed in the v0.390.1→v0.400.0
  range; `watch_fired` only gained an optional `card_eligible` on its
  `condition` branch, which the inbound `listener` flow never takes.
- **Confirm the stored side effect.** Run
  `control-om om -- event-journal get lane-probe --file events.md --format json`.
  The content holds `<!-- event-watch-event-id:<id> -->`, the pushed text as the
  summary, and `outcome: update` / `verdict: new story`.
- **Confirm the other surface.** Open `$(control-om url /alerts)` and snapshot
  (the nav item is labelled **Watches**; the route is still `/alerts`).
  **There is no table** — v0.400.0 replaced it with a selectable list, so assert
  the `listitem` for your watch inside `region "Watches"`: a
  `checkbox "Select <label>"`, a `link "<label>"`, the source count and goal as
  loose `StaticText`, a `time`, the status word, and a `Pause` or `Resume`
  button. [The ops dashboard](./ops-dashboard.md) owns that shape; do not
  re-describe it here.
  **The fire time is not second-precision on this surface.** The row renders
  relative words (`Just now`, `N min ago`), with the exact instant only in the
  `time` element's `datetime` attribute and the row's `title`. For correlating
  against the stream's `fired_at` to the second, use the detail page at
  `/alerts/<id-or-slug>` or the journal, not this row.
- **Proof.** Keep `events.sse` and the two JSON results in the artifact
  directory, capture the pair
  (`agent-browser snapshot -c` to `alerts.aria.txt`, `agent-browser screenshot
  alerts.png`), then `control-om evidence publish <run-id> <revision>` and hand
  back the URL. Every artifact must carry the same `event_id`.

The CLI push is the same pipeline without the HTTP door:
`control-om om -- event push lane-probe --text "..." --kind filing --format json`
returns `watch_id`, `event_id`, `accepted`, `deduped`, `delivery` and `notes`.
Use it when the door is not what is under test; use the door when it is.

## Gotchas

- **On a busy host, `event push` can bypass a live lane.** The CLI gives `/healthz` 200 ms, then one more second (`runner/client.ts:87-91`). A slower answer counts as `busy`, and `event push` then checks the daemon pidfile. A foreground `om run` never writes one: only daemon mode does (`runner/index.ts:2285`). So the push writes the journal itself and reports `delivery:"direct"` with `The daemon is not running…` (`actions/watch/push.ts:182-218`). Driven 2026-10-30 at load average about 150, when `/healthz` took 2 to 3 s. The event still reached the journal, but it never crossed the stream. Use the HTTP door when the stream is under test, and check `uptime` before calling a `direct` result drift. This is a product gap (README).
- An unauthenticated `POST /ingest/v1/<watch>` is `401 {"error":"unauthorized"}`.
  That is the door working, not a broken route.
- `rotate-token` revokes the previous token. Mint once per run and keep it — in
  a shell variable, not in the artifact directory. Its JSON carries a working
  bearer and a `curl` line containing it, and `evidence publish` copies the whole
  directory into a gallery anyone can open. Redact before publishing.
- A watch left on the default `llm_every_event` accepts the event and then
  fails classification, so `watch list` reads `broken` and `event-journal get`
  reports `No LLM credential is configured`. That is the guest lane, not the
  change under test.
- `om watch list` shows LAST FIRE at minute resolution; `/events/v1` and the
  dashboard carry seconds. Correlate on the `event_id` when the minute is
  ambiguous.
- **The `event_id` is derived from the event's content, not minted randomly.**
  The same probe text pushed into two different fresh lanes produced the
  identical id, so an id that repeats across runs proves nothing about which run
  wrote the row. Put the run id in the probe text.
- The journal now lives under `<lane root>/accounts/guest/event-journal/`, not
  directly in the lane root. `om event-journal` finds it either way; a hand-rolled
  path does not.
- Pushes dedupe on the caller's `--id`. Two identical probes without one are two
  events; the same `--id` twice is `deduped: true` and no second fire.
