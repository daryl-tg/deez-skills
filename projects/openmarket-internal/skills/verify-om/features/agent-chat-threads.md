# Chat with one of your agents (the roster context on the chat doors)

*Re-driven 2026-11-12 (nightly), tree `82094c3a83` (origin/main, v0.495.0+11), bare lane on 18193 (dummy `OM_API_KEY`, dead service URLs) with a fake model on 18192: `/chat/turn` with `context.kind: "roster"` to the bundled `explain` with no credential answered (`assistant.text` with the fake's text, then `turn.done` with `totalTokens: 15`), and `agent_credentials` went from 0 rows to one `explain` row with no `revoked_at`. This is #2464 on main; the `credential_missing` refusal in the next line is history. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261112/r1/` (`cli/agentchat-01-first-chat-mint.txt`).*

*Verified: 2026-11-11 (nightly), tree `0ad4768f66` (origin/main, v0.494.0; #2434), bare lane on 18183 (dummy `OM_API_KEY`, dead service URLs) with a scripted fake model on 18182. Driven: `/chat/turn` with `context.kind: "roster"`: a completed turn as an agent om created, `credential_missing` for a bundled agent, `not_found`, the paused refusal and the 400 on a malformed id; the thread list, create, rename, switch, delete and history. Not driven: the agent page in the GUI (verify-om-chat owns it), the cloud path over Remote Control, a tool card answered as the agent, the hourly budget refusal, a revoked credential. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261111/r1/` (`cli/agent-chat.txt`).*

*Verified: 2026-11-11, branch `a14ad17143`, merged as `615ed679f3` (#2464). Source lanes 18141 (fix) and 18143 (base `f98a580314`) on a home seeded only with the operator's LLM login rows (`vault_secrets` `llm:auth-profiles`, `llm:lane-salt:v2`, plus `agent.model.%`), dead service URLs, model claude-opus-5. Driven: `hi` to argue (base: a parenthesised silence note on both tries; fix: a real answer), `hi` to an agent with no credential (base: `credential_missing`; fix: answers and a live credential is minted). Not driven: `credential_revoked` live (unit test only). Evidence: `http://127.0.0.1:8098/agent-direct-chat-20261111/r1/`.*

From an agent's page in OM Chat you chat with that agent the way you chat with om. A turn runs as the agent, with its instructions, tools, model and hourly turn budget, and each agent keeps its own threads across restarts. On the daemon this is the same `/chat/*` doors the dashboard agent panel uses ([agent-panel.md](agent-panel.md)), given a roster context.

## Sub-features

- `turn`: `POST /chat/turn` with `context: {kind: "roster", instanceId, threadId?}` streams the agent's reply as SSE: `: ok`, then `data:` frames by `kind` (`assistant.text` with `delta`, `turn.done` with `usage` and `stopReason`).
- `refusals`: an agent that cannot run answers one `turn.error` frame on HTTP 200 and runs nothing. Seen: `not_found` (`Agent instance was not found.`), `installation_disabled` (`explain is paused. Resume it on its page.`). In the source and not driven: `credential_revoked` (`This agent's credential was revoked.`; a revoked credential is never re-minted), `budget_exhausted` (`<name> is over its hourly budget until <time>.`), and 503 `agent_chat_unavailable`.
- `threads`: `GET /chat/conversations?kind=roster&instanceId=<id>` lists an agent's threads; `POST /chat/conversations` starts one; `PATCH /chat/conversations/<id>` renames; `POST /chat/conversations/switch` and `/delete` take `{kind, instanceId, id}`.
- `history`: `GET /chat/history?kind=roster&instanceId=<id>` returns the active thread's messages.

## How to get to it (user POV)

Open an agent's page in OM Chat (desktop or cloud) and type in its chat. The GUI half belongs to `verify-om-chat`; this guide covers the daemon doors behind it.

## Driving it with control-om

Use a bare lane with a fake model: `control-om up --port <p>` with `--env OM_API_KEY=om_dummy_proto`, each of `OM_BASE_URL`, `OM_AUTH_BASE_URL`, `OM_COLLAB_REST_URL`, `OM_ROOM_CHAT_API_URL` and `OM_ALERT_TOPICS_URL` set to `http://127.0.0.1:9`, and the same variables exported for every `control-om om --` call, plus `OPENMARKET_LLM_PROVIDER=openai-compatible`, `OPENMARKET_LLM_BASE_URL=http://127.0.0.1:<fake>/v1` and `OPENMARKET_LLM_MODEL=fake` ([agent-create.md](agent-create.md) describes the fake). Export `OM_LANE_PORT` first. Loopback needs no auth header.

1. Read an instance id: `control-om om -- agent list --format json` (`items[].id`, `agent_<32 hex>`), or `GET /rpc/v1/roster/instances` (`result.items`).
2. A bundled agent has no credential on a bare lane until its first chat, which mints one (since #2464):

   ```sh
   curl -sN -X POST http://127.0.0.1:$OM_LANE_PORT/chat/turn -H 'content-type: application/json' \
     -d '{"message":"hi","context":{"kind":"roster","instanceId":"<explain id>"}}'
   # : ok
   # data: {"kind":"assistant.text",...} ... {"kind":"turn.done",...}
   ```

   Read the minted credential back: `sqlite3 <lane home>/accounts/<profile>/om.sqlite "select name, revoked_at from agent_credentials"` lists `<owner> | explain`. The reply is real only with a real model (see Gotchas); on the scripted fake it is the fake's text.

3. An agent om created runs the same way: create one with `om agent create --file draft.json` ([agent-create.md](agent-create.md)), then send the same turn with its id. Seen: `assistant.text` with the fake's reply, then `turn.done` with `usage.totalTokens` and `stopReason: "stop"`. The fake was offered 1 tool on this turn and 2 on a task run of the same agent.
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
- The bundled agents (`explain`, `argue`, `fact-check`, `librarian`, `feature`, `debugger`) get their credential on their first chat (#2464); before that they had one only after a room grant.
- A real model on a lane without the operator's channels, watches or rooms identity: seed a fresh lane home with `active`, `credentials.json` and `vault.key`, boot once, stop, then copy only `vault_secrets` rows `llm:auth-profiles` and `llm:lane-salt:v2` and the `agent.model.%` settings from the live `om.sqlite`, and boot again with dead service URLs. The daemon refreshes an LLM OAuth token only within 60 s of expiry, so a short lane cannot rotate the live one. A copied lane home also carries `.om-runner.lock`; delete it before booting the copy.
- Listing an agent's threads creates its first one.
- Agent chats use no om memory, and an agent's turn does not wait behind om's turn (CHANGELOG, not driven).
