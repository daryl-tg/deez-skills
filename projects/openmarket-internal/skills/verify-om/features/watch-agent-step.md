# A watch step that wakes a roster agent

*Verified: 2026-11-03, branch `daryl/agent-step-deltas` (PR #2287, head `1ce71d09b`, cut from `origin/main` `9861d061d` after #2282 landed the step), source lane on 18153 (`OM_FEED_ALLOW_LOOPBACK=1 OM_FEED_POLL_INTERVAL_MS=60000`, `OM_LANE_PORT=18153` on every `control-om om` call), guest home, roster defaults installed about 5 s after boot. `watch create lane-agent --inbound --action '{"kind":"ai","payload":{"agent":"explain","ask":"Summarise this event in two lines.","label":"brief"},"channels":[]}'` landed the step with `agent` and `ask`; the flag form `--agent explain --ask ... --label brief` refused `watching_action_destination_unresolved` on the empty home, as every shorthand step does without a channel. `watch edit --classifier-mode accept_all`, `watch rotate-token --yes`, then `watch arm lane-agent brief --yes` printed `Sends to: history only`, `TRIGGER`, and a `STEP` group `Name: brief`, `Agent: explain`, `Ask: "Summarise this event in two lines."`, `Runs: once per fire`, `Tools: from the agent's manifest`, then `steps running` (before the branch's gate fix the same arm refused `model_unresolved`, "an ai step needs a sealed model and no LLM is configured on this home"). A bearer `POST /ingest/v1/lane-agent` answered 202; the errand lane claimed the firing; the roster took the task; the run failed `No LLM API key configured` (the keyless lane's own refusal), stored on the firing row in `accounts/guest/schedules/state.db` as `poisoned`; `watch show` read `steps failing · a lasting error → om watch retry lane-agent` and the history held one `error` step row. Not driven: the deferral and the door-refusal sentence (`the brief step: explain has no active credential.`), which need an installed agent with a credential; both are unit-tested on the branch. Evidence: `~/dev-notes-artifacts/om-agent-roster-schedules/run-artifacts/unit6-followup/`.*

An `ai` step whose payload names `agent` (and optionally `ask`) hands each row of its watch to an installed roster agent through the roster's task door instead of running a prompt. The arm binds the agent, its manifest digest and the ask; the watch delivers the agent's summary like any step's result.

## Sub-features

- `author-json`: `watch create --action '{"kind":"ai","payload":{"agent":"<name>","ask":"<text>","label":"<name>"}}'` lands the step off; `channels: []` makes it history-only on a home with no channel.
- `author-flags`: `--agent <name> [--ask <text>]` on `watch create` and `watch action add` builds the same step (#2287); on a home with no channel it refuses `watching_action_destination_unresolved` like `--ai`.
- `arm-card`: `watch arm <watch> <step> --yes` prints the STEP group `Name`, `Agent`, `Ask` (when set), `Runs`, `Tools: from the agent's manifest`; a keyless home arms it (#2287).
- `fire`: an accepted row fires the step; the errand lane submits one task per firing with the ledger key as id; a run still going after 15 s defers and replays (#2287).
- `status-words`: `watch show` reads `deferred: run <id>`, `agent busy`, `skipped: stale`, or the roster's refusal text for a stood-down agent step (#2287); a failed run reads `steps failing · a lasting error` with `om watch retry`.

## How to get to it (user POV)

- Install an agent (the defaults land after boot), create a watch with an agent step, arm it, let a source fire; read the summary in the watch's channel or `om watch history`.

## Driving it with control-om

Preconditions:

- `control-om doctor` passes and the lane is the run's own. Export `OM_LANE_PORT=<port>` for every `control-om om` call when the lane is not on 18101.
- The lane log shows `INFO [roster] om-skills defaults installed 8 package(s)` before the arm (the arm refuses an agent the home lacks).
- A guest lane proves authoring, the card, the fire and the failure path. A completed run needs an LLM credential for the agent's brain.

- **Create.** `control-om om -- watch create lane-agent --inbound --action '{"kind":"ai","payload":{"agent":"explain","ask":"Summarise this event in two lines.","label":"brief"},"channels":[]}' --format json`; expect `actions[0].kind` `ai` with `payload.agent` and `payload.ask`.
- **Make it model-free.** `control-om om -- watch edit lane-agent --classifier-mode accept_all --format json`.
- **Mint the token.** `control-om om -- watch rotate-token lane-agent --yes --format json`; keep `ingest_token.token`.
- **Arm.** `control-om om -- watch arm lane-agent brief --yes`; expect the STEP group above and `steps running`.
- **Push.** `curl -s -w '\nhttp %{http_code}\n' -X POST "$(control-om url /ingest/v1/lane-agent)" -H "Authorization: Bearer <token>" -H 'Content-Type: application/json' -d '{"text":"<run-id>: ETH broke 4000","kind":"filing"}'`; expect 202. Wait about a minute (tick 10 s, then the errand lane).
- **Read.** `control-om om -- watch show lane-agent` (the steps line), `watch history lane-agent --format json` (one `step` row), and `sqlite3 .control-om/home-<port>/accounts/guest/schedules/state.db "select status, error from schedule_firings_v3 order by rowid desc limit 1;"` for the firing's stored text.

## Gotchas

- Push within ten seconds of `rotate-token` and the daemon may not have reloaded the watch; a 401 then is the reload window, not the token.
- `control-om om --` without `OM_LANE_PORT` writes into the default lane's home and the push answers 401 for a watch the running daemon never saw.
- The fault in `watch show --format json` for a stood-down step carries `detail.reason` and, for an agent step on #2287, `detail.message`; a failed run (`step_failed`, class permanent) carries no message, the text is on the firing row.
