# Event ingest and fire

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
