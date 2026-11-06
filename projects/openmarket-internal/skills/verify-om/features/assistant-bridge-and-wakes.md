# Assistant bridge: daemon tools, deposit and wakes through the hosted MCP

*Verified: 2026-11-05 on the unmerged stack #2350, #2352, #2365, #2367, #2378 (top `daryl/assistant-stack-review-fixes`, base main `c1464fcf0`). Not on main yet. Every step below was driven on real local processes with a relay stand-in. A real assistant (Grok Bot) was driven on 2026-11-06 through a temporary tunnel, with a routine webhook as the wake. Pending: an OAuth sign-in from a real assistant, MCP Events from a real vendor, and the production relay with a daemon from this stack.*

An AI assistant connected to the hosted MCP service calls 23 tools on the user's own daemon and a `deposit` tool, and can subscribe to `watch.update` so the daemon posts it a signed webhook. The hosted service forwards over the relay as the operations `mcp.call` and `mcp.events`. The daemon gates it with `om assistants on` and one approval per assistant.

## Sub-features

- `list`: on a host of the om surface `tools/list` adds the daemon tools; root and charts hosts do not. `/directory` there lists them with no trade tool; `/chatgpt` is the chart listing on every host.
- `off`: with the setting off a daemon call answers `daemon_assistants_off` naming the device.
- `ask`: the first call waits 20 s and answers `daemon_asks_you`; `om assistants` shows `asks you` and `om approve <id>`.
- `call`: after approval a call returns the daemon's answer; a second call sends no hello (the device is remembered).
- `deposit`: one journal row in `assistant-inbox-<hash>`; the same `id` answers `deduped: true`.
- `refusals`: `shape_not_served` (arguments above the tool's tier), tool not found for anything off the list, `rate_limited` past the call rate, `daemon_too_old` for a daemon without `assistants.v1`.
- `wake`: `events/subscribe` sends one signed verification challenge, then one delivery per matching row; the subscriber's own inbox never wakes it; at most 10 a minute and 60 an hour per wake.
- `operator view`: `om assistants` rows, `Wake: <watch> to <host>, sent 3m ago, N skipped this hour`, `revoke`, `off`.

## Driving it

Ports from the agent range, all on 127.0.0.1: relay stand-in 18121, receiver 18122, hosted binary 18119, Mongo 18117, lane 18150. Stop each after the run.

1. Mongo as in [hosted-chart-mcp-tenant-state.md](hosted-chart-mcp-tenant-state.md), a run-owned container on 18117.
2. A relay stand-in. The real relay needs a signed-in daemon, and a lane with a dummy key cannot sign in. The stand-in authenticates anything, routes `AGENT_CONTROL_REQUEST` to the daemon socket and carries emits back. The one used on 2026-11-05 is `~/dev-notes-artifacts/om-assistant-broker/run-artifacts/loop-2/e2e/local-relay.ts` (local artifact, not in the hub).
3. Hosted binary from the branch: `bun run --cwd packages/cli build:chart-mcp`, then boot with `OM_HOSTED_CHARTS_URL=https://charts.mcp.openmarket.xyz OM_HOSTED_OM_URL=https://om.mcp.openmarket.xyz OM_HOSTED_RELAY_URL=ws://127.0.0.1:18121` beside the usual bind, port, home and Mongo variables. Requests pick the host with `Host` and `X-Forwarded-Host` headers, so no DNS is needed.
4. Lane daemon from the branch, run from the worktree with `OM_LANE_PORT=18150` exported: `control-om up --port 18150 --env OM_API_KEY=om_dummy_proto --env OM_ROOMS_WS_URL=ws://127.0.0.1:18121` plus dead URLs (`http://127.0.0.1:9`) for `OM_BASE_URL`, `OM_AUTH_BASE_URL`, `OM_COLLAB_REST_URL`, `OM_COLLAB_WS_URL`, `OM_ROOM_CHAT_API_URL`, `OM_ALERT_TOPICS_URL`, and `--env OM_ASSISTANT_WAKE_ALLOW_LOOPBACK=1` for a loopback receiver.
5. A caller key. The hosted verifier checks the key against the production gateway, so the drive reads the operator's stored key through `resolveApiKeyWithSource` and never prints it. A stored device key has no scope claim and lists 37 hosted tools.
6. Walk: `control-om om -- assistants` (off row), `assistants on`, a `watch_list` call (asks), `approve <id>`, the call again, `deposit`, `events/subscribe` with a `whsec_` secret and the receiver's URL, then commit a row with `control-om om -- event push <another assistant's inbox> --text ...`.
7. A receiver that verifies each request itself: HMAC-SHA256 over `webhook-id.webhook-timestamp.body`, key = base64 of the secret after `whsec_`; it answers `{"type":"verification"}` with `{challenge}`.

## What to expect

- A daemon call takes tens of milliseconds on the rig once the device is remembered.
- A delivery arrives about 1 s after the row is accepted (the ingest pipeline is asynchronous).
- 13 rows in under a minute give 10 deliveries and `3 skipped this hour`.
- After `assistants revoke <asst_ id>` no further delivery arrives.

## Driving it with a real assistant: Grok Bot (2026-11-06)

*Driven on the top of the stack with a throwaway key, a stand-in gateway and a scratch lane daemon. No real credential was used.*

- A stand-in gateway replaces the production key check, so a made-up key works: a small server that answers `GET /collab-v2/workspaces` with `[]` and the header `x-om-key-label` for one JWT-shaped key (`alg: none`, claims `jti`, `sub`, `scope`), and 401 otherwise. Point the hosted binary at it with `OM_COLLAB_REST_URL` and `OM_COLLAB_WS_URL`. Chart tools then do nothing useful; daemon tools, deposit and events work.
- Serve the om surface on a plain local address with `OM_HOSTED_PUBLIC_URL=http://127.0.0.1:18119 OM_HOSTED_ROOT_SURFACE=om`. No charts or om host is needed.
- Grok Bot's MCP connector dials from xAI's cloud and cannot reach loopback. Two ways to test: the Bot runs curl against `http://127.0.0.1:18119/mcp` through its local command tool, or a temporary public tunnel (`cloudflared tunnel --url http://127.0.0.1:18119`, which needs the operator's say-so) and the Bot adds the server by URL with the `Authorization: Bearer` header when asked in chat.
- The connector reports its client as `Cursor/1.0.0`. The label the daemon shows comes from the key's label.
- Wake for Grok Bot is not MCP Events. Ask the Bot for a routine with a webhook trigger, read the trigger URL and key from the routine panel, then on the daemon `om setup webhook --webhook-url <url> --bearer-token <key> --name <name>` and a watch whose `notify.channels` names that channel. The setup's own test message already runs the routine once.
- A watch that fires without a model on a bare lane: import a spec with an `inbound` source and `classifier: { mode: "accept_all" }` through `om watch import <file>`, then `om event push <id> --text ...`. `om watch create --inbound` defaults to a model classifier, and an `--every 2m` timer watch never fired on the bare lane.
- Seen: row to the Bot's deposit landing back in its inbox took about 14 s.
- Drive the Bot app as the memory note on Grok Bot automation says, with a session name of your own.

## Gotchas

- Two links can share one label (the key's label). `allow` and `revoke` then need the `asst_` id, which `om assistants --format json` prints.
- A scratch lane home copied from an earlier build keeps its old links; an old link with a 64-hex id is from before the identity fix and can be ignored.
- `OM_HOSTED_ROOT_SURFACE=om` moves the root to the om surface; `OM_HOSTED_DAEMON_CALLS_PER_MINUTE=3` gives a burst of 1 for a quick rate check.
- A daemon in the public cut has no relay channel, so none of this is reachable there.
