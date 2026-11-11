# Feed heartbeat and chart reconnect

*Verified: 2026-11-11 (nightly), tree `0ad4768f66` (origin/main, v0.494.0); #2446 merged as `1570839e71`. The heartbeat half was re-driven on main: a lane on 18185 with a seeded username home against a stub relay on 18186. The lane read `inactive`, `no enabled inbound watch` at boot; one push logged head, declare and rows for `nightlyuser/watch.hb-probe-20261111`; `POST …/heartbeat` arrived at boot + 5 min and the lane read `ok`; after `watch pause` the next pass sent nothing and the lane read `inactive` again. A guest lane with an enabled inbound watch reads `inactive`, `not signed in`. Not re-driven on main: the chart reconnect half. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261111/r1/` (`cli/heartbeat-watch-show.txt`).*

*Driven 2026-11-10 on PR #2446's branch (`2f40f65774`), one lane on 18160 against two local stubs: a relay on 18161 and a chart gateway on 18171. All stopped.*

Two daemon behaviours with no visible surface of their own, proven through stubs because a guest lane has no username, no relay feed and no chart workspace.

## Sub-features

- `feed-heartbeat`: the daemon sends each enabled inbound watch's relay feed a heartbeat every 5 minutes, so its chart panes stop reading offline between pushes. A paused watch gets none. `/healthz` lists the lane as `feed-heartbeat`, with `inactive` and a reason when it has nothing to do (`no enabled inbound watch`, `not signed in`, `no account username`).
- `chart-reconnect`: a chart connection the gateway closed after the daemon joined (1008, or a same-user replacement) is parked, retried every 10 to 11 minutes, and resumed. `runner.log` names each close, park and resume, and `om chart status --format json` carries `parked` while a chart waits.
- `bars-pane`: an inbound watch's histogram series converts to a saved bars feed pane, as a line does. Not driven.

## How to get to it (user POV)

Nothing to open. Push rows into an inbound watch from a signed-in daemon and leave it: the chart pane for that feed keeps reading live between pushes. A chart that lost its connection gets its pushed series back within about 11 minutes with no restart.

## Driving it with control-om

### A lane home with a username and no sign-in

`feedPushScope()` reads `username` off the active key record, and `homeLedgerAuth` returns that record's key with no network call. Seed the lane home before the first `up`:

- Create `<worktree>/.control-om/home-<port>/accounts/guest` and write `guest` to `home-<port>/active`.
- Run a seed script with `OM_HOME=<lane home> OM_BIND=127.0.0.1:<lane port>` that calls `setActiveKey(<JWT-shaped string with sub, jti, exp>)` and `setKeyOwnerIdentity(deriveKeyIdentity(key).keyId, { username, email: null })` from `packages/cli/src/runner/credentials/`.
- Point `OM_BASE_URL`, `OM_AUTH_BASE_URL`, `OM_ROOM_CHAT_API_URL`, `OM_ROOMS_WS_URL` and `OM_ALERT_TOPICS_URL` at a dead port (`http://127.0.0.1:9`), so the boot key probe reads unknown and records no revocation.
- Do not set `OM_API_KEY`. It replaces the stored key.
- `control-om om --` calls carry the caller's environment, not `up --env`. Export the same URLs in the shell.

### Heartbeat for an inbound watch's feed

1. Start a stub relay that answers `GET …/head`, `PUT` (declare), `POST …/rows` and `POST …/heartbeat` under `/api/v2/feeds/<scope>/<name>` and logs each request.
2. `control-om up --port <p> --env OM_LEDGER_ORIGIN=http://127.0.0.1:<stub>` plus the dead URLs.
3. `/healthz` `loops` holds `feed-heartbeat`, `inactive`, `no enabled inbound watch`. On a guest lane the reason turns to `not signed in` at the first pass after an inbound watch exists.
4. `watch create probe --inbound`, `watch edit probe --classifier-mode accept_all`, `event push probe --text reading --values '{"aqi": 40}'`. The stub logs head, declare and rows for `<user>/watch.probe` within seconds.
5. The lane passes at boot and every 300 s. Seen: `POST …/watch.probe/heartbeat` at boot+5 min and boot+10 min, loop `ok`.
6. `watch pause probe`. The next pass sends nothing and the loop reads `inactive` again.

Budget 16 minutes from boot.

### A chart connection that closes after it joined

1. Start a stub gateway that serves the collab websocket at `/ws/collab` and REST 200s. Its first connection gets WELCOME with a human and the agent in the roster, then a close with code 1008 and reason "Policy violation". Later connections get WELCOME and stay open. It must answer `REQUEST_STATE_SYNC` or the liveness probe bounces the second socket.
2. Boot with `--env OM_COLLAB_WORKSPACE_ID=<id> --env OM_COLLAB_WS_URL=ws://127.0.0.1:<stub>/ws/collab --env OM_COLLAB_REST_URL=http://127.0.0.1:<stub>`. The boot selection dials that workspace. The stored key serves as the collab token when its `jti` matches `^[A-Za-z0-9_.:-]+$`.
3. Read `.control-om/lane-<port>.log`. Seen within seconds: `collab ws[<id>]: socket closed 1008: Policy violation` and `collab bridge[<id>]: parked after ws closed 1008: Policy violation`.
4. Wait 600 to 660 s. Seen: `collab ws[<id>]: re-dialing (lazy lifecycle retry)` and `collab bridge[<id>]: resumed after the park on 1008: Policy violation`. The stub logs a second connection.
5. `control-om om -- chart status --format json` reads `state: "open"` with no `parked`.

Both run on one lane. To attach a workspace on a running lane without disconnecting others, POST `{"workspaceId": …}` to `/rpc/v1/collab/attach` with the home's `runner.token`. `chart select` is exclusive.

## Gotchas

- Not driven: the same-user close (1000 "New connection from same user") on a lane. Unit tests cover it.
- Not driven: a real relay head staying `live`, and a real chart getting its series back. Both need a signed-in daemon.
- A histogram series converting to a bars feed pane is not driven on a lane. It needs a chart workspace and the chart frontend that draws bars. The rule is `packages/cli/src/runner/collab/series-feed-convert.ts` (`feed_pane_drawn_differently`).
- A stub relay that answers `PUT` with `{"feed":{"version":1}}` (201), `…/rows` with `{"accepted":1,"replaced":0,"refused":[]}`, `…/head` with 404 `feed_not_found` and `…/heartbeat` with 200 is enough for the heartbeat half.
- A signed-in lane also tries to sync saved watches with the registry. `watch list` on the seeded lane printed `syncing your watches paused · the saved watches could not be read (getaddrinfo ENOTFOUND registry-staging.openmarket.xyz) · retrying`; it does not affect the heartbeat.
