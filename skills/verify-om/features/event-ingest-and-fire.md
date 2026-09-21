# Event ingest and fire

A user points a producer at a watch's inbound door and the daemon takes it from
there: the event is accepted, committed, appended to the watch's journal, and
fired. The fire shows up on the live event stream, in the journal on disk, and
as a row in the dashboard's Alerts table. This is the whole pipeline, and none
of it needs an account.

## Sub-features

- `ingest-cli` pushes an event through `om event push`.
- `ingest-http` pushes the same event through `POST /ingest/v1/<watch>` with a
  minted bearer token.
- `fire-stream` emits `watch_committed`, `watch_appended` and `watch_fired` on
  `/events/v1`.
- `fire-journal` writes the event, its verdict and its id into the watch's
  `events.md`.
- `fire-dashboard` shows the watch as `armed` with a LAST FIRED time.

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
- **Read the stream.** `events.sse` carries three events for that same
  `event_id`: `watch_committed` (with `"outcome":"update"` and the title),
  `watch_appended`, then `watch_fired` with `fired_at` and `"confidence":1`.
  The fired payload leads with `"kind":"listener"`. These names lost their
  `event_` prefix in v0.35 — grep for `^event: watch_` and nothing else.
- **Confirm the stored side effect.** Run
  `control-om om -- event-journal get lane-probe --file events.md --format json`.
  The content holds `<!-- event-watch-event-id:<id> -->`, the pushed text as the
  summary, and `outcome: update` / `verdict: new story`.
- **Confirm the other surface.** Open `$(control-om url /alerts)` and snapshot
  (the nav item is labelled **Watches**; the route is still `/alerts`). The
  table row reads `lane-probe`, `1`, `lane-probe`, `working`, and a LAST FIRED
  cell matching the stream's `fired_at` to the second — the columns are LABEL,
  SOURCES, GOAL, STATUS, LAST FIRED, ACTIONS. There is no KIND cell any more.
- **Proof.** Keep `events.sse` and the two JSON results in the artifact
  directory, capture the pair
  (`agent-browser snapshot -c` to `alerts.aria.txt`, `agent-browser screenshot
  alerts.png`), then `control-om evidence publish <run-id> <revision>` and hand
  back the URL. Every artifact must carry the same `event_id`.

The CLI push is the same pipeline without the HTTP door:
`control-om om -- event push lane-probe --text "..." --kind filing --format json`
returns `{"accepted":true,"delivery":"daemon"}`. Use it when the door is not
what is under test; use the door when it is.

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
