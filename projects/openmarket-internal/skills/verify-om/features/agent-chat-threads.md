# Chat with one of your agents (the roster context on the chat doors)

*Verified: 2026-11-11 (nightly), tree `0ad4768f66` (origin/main, v0.494.0; #2434), bare lane on 18183 (dummy `OM_API_KEY`, dead service URLs) with a scripted fake model on 18182. Driven: `/chat/turn` with `context.kind: "roster"`: a completed turn as an agent om created, `credential_missing` for a bundled agent, `not_found`, the paused refusal and the 400 on a malformed id; the thread list, create, rename, switch, delete and history. Not driven: the agent page in the GUI (verify-om-chat owns it), the cloud path over Remote Control, a tool card answered as the agent, the hourly budget refusal, a revoked credential. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261111/r1/` (`cli/agent-chat.txt`).*

From an agent's page in OM Chat you chat with that agent the way you chat with om. A turn runs as the agent, with its instructions, tools, model and hourly turn budget, and each agent keeps its own threads across restarts. On the daemon this is the same `/chat/*` doors the dashboard agent panel uses ([agent-panel.md](agent-panel.md)), given a roster context.

## Sub-features

- `turn`: `POST /chat/turn` with `context: {kind: "roster", instanceId, threadId?}` streams the agent's reply as SSE: `: ok`, then `data:` frames by `kind` (`assistant.text` with `delta`, `turn.done` with `usage` and `stopReason`).
- `refusals`: an agent that cannot run answers one `turn.error` frame on HTTP 200 and runs nothing. Seen: `not_found` (`Agent instance was not found.`), `credential_missing` (`This agent has no credential.`), `installation_disabled` (`explain is paused. Resume it on its page.`). In the source and not driven: `credential_revoked`, `budget_exhausted` (`<name> is over its hourly budget until <time>.`), and 503 `agent_chat_unavailable`.
- `threads`: `GET /chat/conversations?kind=roster&instanceId=<id>` lists an agent's threads; `POST /chat/conversations` starts one; `PATCH /chat/conversations/<id>` renames; `POST /chat/conversations/switch` and `/delete` take `{kind, instanceId, id}`.
- `history`: `GET /chat/history?kind=roster&instanceId=<id>` returns the active thread's messages.

## How to get to it (user POV)

Open an agent's page in OM Chat (desktop or cloud) and type in its chat. The GUI half belongs to `verify-om-chat`; this guide covers the daemon doors behind it.

## Driving it with control-om

Use a bare lane with a fake model: `control-om up --port <p>` with `--env OM_API_KEY=om_dummy_proto`, each of `OM_BASE_URL`, `OM_AUTH_BASE_URL`, `OM_COLLAB_REST_URL`, `OM_ROOM_CHAT_API_URL` and `OM_ALERT_TOPICS_URL` set to `http://127.0.0.1:9`, and the same variables exported for every `control-om om --` call, plus `OPENMARKET_LLM_PROVIDER=openai-compatible`, `OPENMARKET_LLM_BASE_URL=http://127.0.0.1:<fake>/v1` and `OPENMARKET_LLM_MODEL=fake` ([agent-create.md](agent-create.md) describes the fake). Export `OM_LANE_PORT` first. Loopback needs no auth header.

1. Read an instance id: `control-om om -- agent list --format json` (`items[].id`, `agent_<32 hex>`), or `GET /rpc/v1/roster/instances` (`result.items`).
2. A bundled agent has no credential on a bare lane:

   ```sh
   curl -sN -X POST http://127.0.0.1:$OM_LANE_PORT/chat/turn -H 'content-type: application/json' \
     -d '{"message":"hello","context":{"kind":"roster","instanceId":"<explain id>"}}'
   # : ok
   # data: {"kind":"turn.error","code":"credential_missing","message":"This agent has no credential."}
   ```

3. An agent om created does: create one with `om agent create --file draft.json` ([agent-create.md](agent-create.md)), then send the same turn with its id. Seen: `assistant.text` with the fake's reply, then `turn.done` with `usage.totalTokens` and `stopReason: "stop"`. The fake was offered 1 tool on this turn and 2 on a task run of the same agent.
4. `GET /chat/history?kind=roster&instanceId=<id>` reads `{threadId, messages, nextBefore}`. Each message has `role`, `content`, `ts`, `turnId` and `ord`; the user row has `authorKind: "operator"` and a `sent` that opens `[turn context: surface=roster; userId=agent-chat:<instance>:<thread>; now=…]`.
5. Threads, all 200 for an agent with or without a credential:
   - list: `{activeId, conversations:[{id, label, preview, messageCount, updatedAt}]}`; the first list already holds one empty thread (`preview: "(empty)"`).
   - create: `POST /chat/conversations {"kind":"roster","instanceId":"<id>"}` returns `{conversation, activeId}` and makes the new thread active.
   - rename: `PATCH /chat/conversations/<thread> {"kind":"roster","instanceId":"<id>","label":"nightly thread"}` returns the row with the label.
   - switch and delete: each returns `{activeId}`.
6. Refusals: an unknown `agent_<32 zeros>` id is `not_found`; after `control-om om -- agent configure explain --paused on` the turn is `installation_disabled`, `explain is paused. Resume it on its page.`; an `instanceId` with a space or `!` is HTTP 400 `invalid_request`, whose message lists the context kinds `'global'|'lane'|'armed'|'roster'`.

## Gotchas

- Refusals ride the stream, so assert on the `turn.error` frame, not the HTTP status. Only a malformed context is a 400.
- A paused agent answers the paused refusal even when it has no credential, so pause is checked first.
- The bundled agents (`explain`, `argue`, `fact-check`, `librarian`, `feature`, `debugger`) have no credential until they are granted a room, which needs a rooms account. For a completed turn on a bare lane, create an agent.
- Listing an agent's threads creates its first one.
- Agent chats use no om memory, and an agent's turn does not wait behind om's turn (CHANGELOG, not driven).
