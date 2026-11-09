# The roster task door and run pool

*Re-driven 2026-11-09 (scheduled maintenance), tree `0d3d29cd27` (origin/main, v0.493.0), bare lane on 18145 (dummy `OM_API_KEY`, dead service URLs) with a scripted fake model on 18144. `POST /rpc/v1/roster/tasks {id:"vom-maint-1109-t2", agent:"explain", …, requestedBy:{surface:"om",userId:"me"}}` → `{taskId, runId}`; `?wait=25000` read `completed`, the fake reply as `summary`, `usage {tokens:112, costUsd:0}`. A body without `requestedBy` is `malformed_body` `Invalid field: requestedBy`, and `?wait=30000` is `wait must be 0 to 25000 ms.`. Not re-driven: the cap, dedup, cancel. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261109/r1/`.*

*Re-driven 2026-11-09 (nightly), tree `5bfa0ccf6` (origin/main, v0.492.0), guest lane on 18143, booted with no guest 429. on a guest lane plus a fake model: one `POST /rpc/v1/roster/tasks` to `explain` reached `completed` (`agent ps` shows it). Burst, cap and dedup are not re-driven. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261109/r1/` (`cli/92-94`).*

*Re-driven 2026-11-07 (nightly), tree `05f450fc5` (origin/main, v0.492.0), guest lane on 18141, booted with no guest 429 with `OPENMARKET_LLM_*` pointing at a scripted fake model on 18142 (not a bare lane). `POST /rpc/v1/roster/tasks {id:"vomn1107-t1", agent:"explain", …}` returned `{taskId, runId}`; `GET …/tasks/vomn1107-t1?wait=25000` read `state: completed`, `summary: "fake reply 6"`, `usage.tokens 12`. Not re-driven: the pool cap, dedup, cancel. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261107/r1/` (`cli/106-roster-task.json`).*

*Re-driven 2026-11-06 (nightly), tree `50fcc594b` (origin/main, v0.492.0), bare lane on 18165 (dummy `OM_API_KEY`, dead service URLs) with a scripted fake model on 18164 that reports `usage`. `POST /rpc/v1/roster/tasks` `{id:"vom1106-t1", agent:"explain", …}` returned `{taskId, runId}`; `GET …?wait=25000` read `completed` with the fake reply as `summary` and `usage {tokens:110, costUsd:0}`; `agent ps` read `Agents: 4 at once · 0 running · 0 queued` and the run row. Not re-driven: the cap, dedup, cancel, `agent_busy`, budget. Evidence: `http://127.0.0.1:8098/vom-nightly-20261106/r1/` (`cli/b-task-*.json`, `cli/b-agent-ps.txt`).*

*Re-driven 2026-11-05 (nightly), tree `3a0ea623e` (origin/main, v0.492.0), bare lane on 18165 (dummy `OM_API_KEY`, dead service URLs) with a scripted fake model on 18164. A task-door run answered 200 and `?wait` returned `completed` with the fake reply and `usage.tokens 140`; unpaced submissions to `explain` hit 429 `agent_busy` `explain is busy, 16 waiting` (`queued: 16`, `resumeAt`); paced ones ran to the daily budget ([agent-chat-budget.md](agent-chat-budget.md)); `agent ps --format json` then read `pool {limit:4, running:1, queued:15}`. Guest lane 18163: `agent ps` `{"runs":[],"pool":{"limit":4,…}}`. Evidence: `http://127.0.0.1:8098/vom-nightly-20261105/r1/` (`cli/bare-task1.json`, `cli/bare-agent-busy-429.json`).*

*Re-driven 2026-11-04 (nightly), tree `9acb5fb56` (origin/main, v0.491.0), guest lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), booted in 2 s at 19:19Z with no guest 429, host load average about 3.5. Guest lane, no model: `agent ps` `Agents: 4 at once · 0 running · 0 queued` / `No agent runs.` and `{"runs":[],"pool":{"limit":4,"running":0,"queued":0}}`; a watch agent step's run listed as `explain  watch  failed`, its JSON row carrying `kind: "task"` and `canCancel` beside the fields above; `agent ps <id>` detail; `agent cancel` of it exit 1 `Run already failed.`; `agent cancel run_nope` `Run was not found.`; MCP `agent_run {agent:"zzz"}` `not_found`. The pool, dedup, cap and a running cancel were not re-driven (they need the fake-model rig). Evidence: `http://127.0.0.1:8098/vom-nightly-20261104/r1/` (`cli/48-50`, `cli/69-74`, `cli/110-mcp.json`).*

*Verified: 2026-11-03, tree `496000505` (#2282, v0.489.0), source lanes on 18150 (bare lane with a fake model, 95 timing trials) and 18152 (the `dboon_ref` test account copied from `~/dev-notes-artifacts/om-agents-live-e2e/rig/lane/home-18124`, anthropic `claude-opus-5-5`, 10 chat-agent tasks). Work agents re-driven on 18152 compiled from `4f4f9bd8e` (v0.491.0), because coding runs need the compiled daemon. Driven: task submit and long-poll, `om agent ps`, `om agent cancel`, the pool across 4 agents, `OM_ROSTER_POOL=2`, one-agent serial queue, the 16-deep cap and its 429, dedup of identical asks, watch-door coalescing, and one debugger-template and one feature-template work run by room mention. Evidence and numbers: `~/Documents/dev-notes/om-agents-perf-quality-eval/run-artifacts/` (`speed-results.md`, `quality-results.md`, `work/`).*

An agent task goes in through `POST /rpc/v1/roster/tasks` (what `agent_run` and a watch agent step call) and runs in a pool of up to four at once, one per agent. A repeated ask inside a minute returns the first run, watch-door asks with the same text and distinct inputs inside 5 s join one queued run, and a seventeenth queued ask to one agent is refused `agent_busy` with a `resumeAt`. `om agent ps` lists runs with the pool and queue positions. `om agent cancel <run>` stops a running run.

## Sub-features

- `task-door`: submit `{id, agent, ask, place?, inputs?, requestedBy:{surface, userId}}`, then `GET /rpc/v1/roster/tasks/<id>?wait=25000` until `state` is terminal; the result carries `summary`, `proposals`, `artifacts` and `usage`. Loopback needs no auth. A reused task id is a replay of the first run.
- `pool`: four different chat agents finish together (7.48 s against 7.82 s alone at a 2 s model round); asks to one agent run one after another in server-arrival order.
- `depth-cap`: sixteen queued per agent; the seventeenth gets HTTP 429 `agent_busy` with `resumeAt` and `queued: 16`.
- `budget` (#2304): a chat agent's runs stop at 40,000 tokens a run, 50 runs a day and 400,000 tokens a day; the door refuses the 51st run 429 `budget_exhausted` and a run that crosses the per-run cap fails `budget_exhausted`. Recipe and strings: [agent-chat-budget.md](agent-chat-budget.md). The per-agent `--model` dial (`om agent configure <name> --model`) applies to the next task run.
- `dedup` and `coalesce`: ten identical asks make one run; five watch-door asks with distinct `inputs` join one run.
- `ps` and `cancel`: `om agent ps --format json` shows `pool {limit, running, queued}`, `queuePosition` and `stalled`; `om agent cancel <run>` reaches `cancelled` in about half a second.
- `work-mention`: a work agent with a Claude brain takes a room mention through preparing, running, verifying and publishing to a local commit and a threaded reply naming it (309 s for a one-line fix).

## How to get to it (user POV)

- Ask om chat to have an agent do something (`agent_run`), arm a watch whose `ai` step names an agent, or mention a work agent in a room. Watch runs with `om agent ps`; stop one with `om agent cancel`.

## Driving it with control-om

Preconditions:

- The rig is `R=~/Documents/dev-notes/om-agents-perf-quality-eval/rig`. Run it from `~/github/openmarket-internal`.
- For pool and timing work, a bare lane needs no account and spends nothing. `$R/lane-up.sh <port> <hold-ms> [KEY=VALUE...]` puts the pinned Bun 1.4.3 (`~/dev-notes-artifacts/om-agents-live-e2e/rig/bun-1.4.3/bun-darwin-aarch64`) first on PATH, starts `$R/fake-model.ts` on port plus one holding `<hold-ms>` per round (2000 is a good default), boots the lane with a dummy `OM_API_KEY`, every OpenMarket service URL on dead `127.0.0.1:9`, and `OPENMARKET_LLM_PROVIDER=openai-compatible`, `OPENMARKET_LLM_BASE_URL`, `OPENMARKET_LLM_MODEL=fake` at the fake, then waits until `GET /rpc/v1/roster/instances` lists all six agents (`/healthz` answers before they install). Extra pairs go to the lane, for example `OM_ROSTER_POOL=2`. `$R/lane-down.sh <port>` stops the lane and the fake.
- Export `OM_LANE_PORT=<port>` for every `control-om` call.
- The lane's database is `.control-om/home-<port>/accounts/<account>/om.sqlite`; `<account>` is `guest` on a bare lane.
- For room context or work runs, a signed-in account home and, for work, the compiled daemon (`bun run build`, `control-om up --compiled`) and a linked project.

Steps:

1. Submit `curl -s -X POST http://127.0.0.1:<port>/rpc/v1/roster/tasks -H 'content-type: application/json' -d '{"id":"<fresh id>","agent":"explain","ask":"what is a funding rate","requestedBy":{"surface":"om","userId":"me"}}'`. `agent` is the installed name. Then `curl -s 'http://127.0.0.1:<port>/rpc/v1/roster/tasks/<id>?wait=25000'` until `result.state` is terminal; expect `completed` and a non-empty `result.result.summary`.
2. Read phases with `sqlite3 -readonly .control-om/home-<port>/accounts/guest/om.sqlite < $R/phases.sql`; each row is run id, then ms for queued to preparing, preparing to running, running to publishing, publishing to terminal, and total.
3. Burst four agents with `python3 -I $R/burst.py --port <port> argue,explain,fact-check,librarian`; expect one wall about the length of a single run.
4. Burst seventeen asks to one agent (`$R/measure.sh s5 1` with `OM_LANE_PORT` exported); expect sixteen accepted and one 429.
5. Stop with `$R/lane-down.sh <port>`.

## Gotchas

- A run starts and ends on a driver tick. About 1.8 s before start and 1 s before completion are waiting, plus about 0.8 s on the 1 s outbox poll. `OM_ROSTER_DRIVER_MS=500` shows it.
- A task with `place` set to a room does not tell the agent which room it is in unless the room has a place doc, so agents search `#general` and often miss the thread.
- Task runs skip the agent's own `verify` rules; an empty reply reads `completed`. Task replies are not posted to the room.
- The shipped `debugger` and `feature` agents install with no brain on every machine (the roster's brain probe reports Claude Code signed out), so a mention only investigates. Build work agents from the templates with brain `claude` to get commits.
- The feature template pauses for plan approval when the project has `planFirst`; the plan appears under Agent Center, not in the room. A plan plus work can exceed the project's default token budget and end `cancelled` after the commit.
- Relinking a project mints a new project id. The old worktree root's owner marker then refuses every run as "A required setup step failed" until that root is moved aside.
- On a cold lane the 429's `resumeAt` is the 60 s floor, whatever the queue holds.
- The daemon's LLM health probe sends one tools-free "ping" round at boot; it is not part of any run.
