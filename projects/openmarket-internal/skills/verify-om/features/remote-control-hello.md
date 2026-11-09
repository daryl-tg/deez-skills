# Cloud finds the desk: Remote Control hello

*Re-driven 2026-11-10 (nightly), tree `c9bc93a355` (origin/main, v0.493.1; #2425 on main since `797f44e65d`), bare lane on 18148 (dummy `OM_API_KEY`, dead service URLs, `OM_ROOMS_WS_URL` at a relay stand-in on 18147). `refusal-log` only: the daemon answered three hellos with `AGENT_CONTROL_EMIT`; the stand-in refused each with `BAD_FRAME`; `agent.log` gained one `channel_error` line for the first, none for the second and one after a forced reconnect. The production relay and the probes below are not re-driven. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261110/r1/` (`remote/standin.log`, `remote/agent-log-remote.jsonl`).*

*Live-driven 2026-11-09 on main `6d441ef550` (v0.493.0) and branch `daryl/remote-control-refused-reply` (#2425). Relay: production, plus a local rig running kiyotaka-chat-service `daryl/agent-control-capabilities` (!253).*

The hosted `/chat/` page finds the owner's desk through the relay. The browser sends `AGENT_CONTROL_REQUEST {action:"hello"}`. The relay forwards it to every socket of that user that declared `STATUS {platform:"daemon", device}`. The daemon answers with `AGENT_CONTROL_EMIT` carrying `hello_ack {device, awayEnabled, capabilities}`. With no ack inside 2.5 s, the page says "Your desk is offline". When the relay refuses that answer, the daemon writes one line to `agent.log`.

## Sub-features

- `hello-ack`: a signed-in daemon declares `STATUS {platform:"daemon"}` at link-up and on reconnect, and answers each hello with `hello_ack`.
- `capability-refusal`: the relay checks `hello_ack.capabilities` against its own list and refuses an unknown name with `BAD_FRAME` ("Invalid rooms frame").
- `refusal-log` (#2425): the first refusal of each code and message writes `channel_error {"surface":"remote","message":"the relay refused this desk's reply (BAD_FRAME: Invalid rooms frame); the cloud page cannot reach this desk until om or the relay is updated"}`. The same refusal again logs nothing until the link reconnects. A refusal for a request this desk never answered is ignored.
- `guest-dark`: a guest home or a home with no key holds no relay socket (`remote control dark: guest session`); an environment `OM_API_KEY` counts as signed in.

## How to get to it (user POV)

Open `/chat/` on the hosted site while signed in to the same account as the desk. The page shows the desk, or "Your desk is offline". When it says offline, read `~/.openmarket/accounts/<name>/agent.log` for a `channel_error` line with `"surface":"remote"`.

## Driving it with control-om

### A relay stand-in for the refusal log

No account and no real relay. A stand-in WebSocket server plays the relay; a bare lane dials it.

1. Write a `Bun.serve` WebSocket server on an assigned agent port, bound to `127.0.0.1`. Frames are `{type, payload, timestamp}` JSON. It must:
   - answer `AUTHENTICATE` with `AUTH_SUCCESS {userId, username, handle, connectionId, protocolVersion: 2}`;
   - answer `PING` with `PONG`;
   - on `STATUS` with `platform: "daemon"`, send `AGENT_CONTROL_DELIVER {requestId: "agc-1", action: "hello", originConnectionId: "conn-cloud"}`;
   - on `AGENT_CONTROL_EMIT` with a string `requestId`, send `ERROR {code: "BAD_FRAME", message: "Invalid rooms frame", requestId}`. `RATE_LIMITED`, `FRAME_RATE_WARNING` and `FRAME_RATE_EXCEEDED` are filtered out, so use another code.
   - To prove the once-per-link rule, send a second hello on the same socket, then close it (`ws.close(1011)`); the daemon re-dials in about 5 s and declares `STATUS` again, and one more hello there logs again.
2. Boot a bare lane pointed at it:
   `control-om up --port <p> --env OM_API_KEY=om_dummy_proto --env OM_ROOMS_WS_URL=ws://127.0.0.1:<standin>/ws/rooms` plus `--env <URL>=http://127.0.0.1:9` for `OM_BASE_URL`, `OM_AUTH_BASE_URL`, `OM_COLLAB_REST_URL`, `OM_COLLAB_WS_URL`, `OM_ROOM_CHAT_API_URL` and `OM_ALERT_TOPICS_URL`. The daemon opens several sockets; only the one that sends `STATUS platform=daemon` gets hellos.
3. Read `.control-om/home-<p>/accounts/guest/agent.log` and grep `"surface":"remote"`. Expect one line per distinct refusal per link: three refusals with a reconnect after the second give two lines.
4. Stop the lane with `OM_LANE_PORT=<p> control-om down`, and the stand-in by its recorded pid.

### Probe the production relay

Scripts live in `~/Documents/dev-notes/om-agents-cloud-parity/probes/` and run with the pinned bun 1.4.3.

- **`desk-hello-probe.ts`.** Authenticates as the account in the default home on `wss://chat.openmarket.xyz/ws/rooms` and sends one hello. A healthy desk prints one `hello_ack` line. Nothing back means the desk is dark to cloud.
- **`relay-route-control.ts`.** Declares a throwaway daemon socket and checks the relay routes hellos to it. It separates a relay fault from a daemon fault.
- **`ws-trace.ts`.** A `bun --preload` that logs every `AUTHENTICATE`, `STATUS`, `AGENT_CONTROL_*` and `ERROR` frame a source daemon sends or receives. Boot a source lane with it to see the relay's answer to the daemon's ack.

### Source lane signed in with a real key

1. Make a fresh home holding only `credentials.json` and `device-id`, with `active` naming the account. Never copy the vault.
2. Run `bun packages/cli/src/bootstrap.ts run` with `OM_HOME`, an `OM_BIND` lane port, and a dead `OPENMARKET_LLM_BASE_URL`. The library mirror stays off without `OM_LIBRARY_DIR`.
3. Probe, then stop the lane and delete the home. It holds the operator's key.

### Local relay rig

`~/Documents/dev-notes/om-agents-cloud-parity/rig/` runs Mongo (18122), the store (18121, a tharamine worktree detached at `13445d10`) and a relay (18120, `RELAY_TREE` in `rig-env.sh`). Point a source daemon at it with `OM_API_KEY=$(cat rig/tokens/daemon.jwt)`, `OM_ROOMS_WS_URL=ws://127.0.0.1:18120/ws/rooms` and `OM_ROOM_CHAT_API_URL=http://127.0.0.1:18120/chat`, with the other service URLs dead. `rig/rig-hello-probe.ts` sends the cloud hello with `rig/tokens/voucher.jwt`.

## Gotchas

- **The relay validates `hello_ack.capabilities` against its own list.** Before !253 an unknown name made it refuse the ack with `BAD_FRAME` ("Invalid rooms frame"). The daemon had added `approvals.v1` (#2334) and `assistants.v1` (#2352), so every desk built after #2334 went dark. A daemon change that adds a capability needs a relay that accepts it.
- **Before #2425 (v0.493.1) the daemon logged nothing about a refused ack.** Now the first refusal of each kind logs once per link; a reconnect resets it.
- **A guest lane never dials the relay.** It logs `remote control dark: guest session` and holds no socket, so the stand-in sees nothing. Use a bare lane with an environment `OM_API_KEY`.
- **The relay drops an over-budget `STATUS` with no error.** The budget is `selfSettings`, 10 per 10 s per `{userId, lane}`. The daemon declares only at link-up and on reconnect. Reproduced with 14 background-lane `STATUS` changes, then a fresh declaration got no hellos for about 15 s. A repeat declaration on a registered socket returns before the budget is charged.
- **A relay checkout sync changes nothing.** Desks and the cloud page talk to the deployed relay.
