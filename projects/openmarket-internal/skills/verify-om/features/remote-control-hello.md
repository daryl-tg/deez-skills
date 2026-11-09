# Cloud finds the desk: Remote Control hello

*Live-driven 2026-11-09 on main `6d441ef550` (v0.493.0) and branch `daryl/remote-control-refused-reply` (#2425). Relay: production, plus a local rig running kiyotaka-chat-service `daryl/agent-control-capabilities` (!253).*

The hosted `/chat/` page finds the owner's desk through the relay. The browser sends `AGENT_CONTROL_REQUEST {action:"hello"}`. The relay forwards it to every socket of that user that declared `STATUS {platform:"daemon", device}`. The daemon answers with `AGENT_CONTROL_EMIT` carrying `hello_ack {device, awayEnabled, capabilities}`. With no ack inside 2.5 s, the page says "Your desk is offline".

## Probe it

Scripts live in `~/Documents/dev-notes/om-agents-cloud-parity/probes/` and run with the pinned bun 1.4.3.

- **`desk-hello-probe.ts`.** Authenticates as the account in the default home on `wss://chat.openmarket.xyz/ws/rooms` and sends one hello. A healthy desk prints one `hello_ack` line. Nothing back means the desk is dark to cloud.
- **`relay-route-control.ts`.** Declares a throwaway daemon socket and checks the relay routes hellos to it. It separates a relay fault from a daemon fault.
- **`ws-trace.ts`.** A `bun --preload` that logs every `AUTHENTICATE`, `STATUS`, `AGENT_CONTROL_*` and `ERROR` frame a source daemon sends or receives. Boot a source lane with it to see the relay's answer to the daemon's ack.

## Source lane signed in with a real key

1. Make a fresh home holding only `credentials.json` and `device-id`, with `active` naming the account. Never copy the vault.
2. Run `bun packages/cli/src/bootstrap.ts run` with `OM_HOME`, an `OM_BIND` lane port, and a dead `OPENMARKET_LLM_BASE_URL`. The library mirror stays off without `OM_LIBRARY_DIR`.
3. Probe, then stop the lane and delete the home. It holds the operator's key.

## Local relay rig

`~/Documents/dev-notes/om-agents-cloud-parity/rig/` runs Mongo (18122), the store (18121, a tharamine worktree detached at `13445d10`) and a relay (18120, `RELAY_TREE` in `rig-env.sh`). Point a source daemon at it with `OM_API_KEY=$(cat rig/tokens/daemon.jwt)`, `OM_ROOMS_WS_URL=ws://127.0.0.1:18120/ws/rooms` and `OM_ROOM_CHAT_API_URL=http://127.0.0.1:18120/chat`, with the other service URLs dead. `rig/rig-hello-probe.ts` sends the cloud hello with `rig/tokens/voucher.jwt`.

## Gotchas

- **The relay validates `hello_ack.capabilities` against its own list.** Before !253 an unknown name made it refuse the ack with `BAD_FRAME` ("Invalid rooms frame"). The daemon had added `approvals.v1` (#2334) and `assistants.v1` (#2352), so every desk built after #2334 went dark. A daemon change that adds a capability needs a relay that accepts it.
- **Before #2425 the daemon logged nothing about a refused ack.** Since #2425 the first refusal of each kind writes one `channel_error` line with `surface: "remote"` in `agent.log`, again only after a reconnect.
- **The relay drops an over-budget `STATUS` with no error.** The budget is `selfSettings`, 10 per 10 s per `{userId, lane}`. The daemon declares only at link-up and on reconnect. Reproduced with 14 background-lane `STATUS` changes, then a fresh declaration got no hellos for about 15 s. A repeat declaration on a registered socket returns before the budget is charged.
- **A relay checkout sync changes nothing.** Desks and the cloud page talk to the deployed relay.
