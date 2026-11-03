# om creates an agent (agent_create, agent_list)

*Verified: 2026-11-03, branch `daryl/agent-create-eval` tree `1f6b53df6` (not yet on main), lane on 18152, bare lane with a fake model. Driven: CLI create with and without `--yes`, a TTY decline through `expect`, `agent ls`, an identical rerun (replay), a name clash, and the read grant on real task-door runs for a created agent and a default one. Not driven: `om chat` choosing `agent_create` from a sentence on a real model, and the chat card on a surface (the rows are pinned by `packages/cli/test/agent-create.test.ts` through the same approval carrier). Evidence: `~/Documents/dev-notes/om-agent-creation/run-artifacts/lane-18152-1f6b53df6/`.*

om turns a draft into an installed roster agent behind one tier-3 card, and lists what is installed.

## Sub-features

- `agent_create`: stage, install (shadow: replies held), then try the first sample ask (chat agents). Card rows `Job`, `Reads`, `Brain`, `Project` (work only), `Replies: held for your OK`; question `Create agent <name>?`.
- `reads` from `AGENT_READS` (`@openmarket/contracts/agents`): `room`, `library`, `market` (new `market_read` bundle: `markets`, `points`, `metric_get`, `metric_series`, `metric_list`, `symbol_resolve`), `repo` for work agents.
- Idempotency keys `agent-create.<step>.<sha256 of input>`: an identical rerun replays, a changed field mints new keys.
- Refusals: `name_taken` (hint lists installed names), `sign_in_required`, `agents_unavailable`, `bad_request`.
- `agent_list` / `om agent ls`: name, kind, reads, held or live; job only for owner-authored agents.
- `om agent create --file <draft.json|->` asks the card rows on the terminal; `--yes` skips; no TTY and no `--yes` is `confirmation_required`, exit 2.

## How to get to it (user POV)

Ask om chat "make me an agent that ..."; or write a draft JSON and run `om agent create --file draft.json`. `om agent ls` lists agents.

## Driving it with control-om

A bare lane boots in seconds and the builder accepts its owner. Use the bare-lane recipe (dummy `OM_API_KEY`, every service URL `http://127.0.0.1:9`, `OPENMARKET_LLM_PROVIDER=openai-compatible` pointed at the fake model from `dev-notes/om-agents-cloud-parity/rig/fake-model/server.ts`) and pass the same env on every `control-om om --` call. Export `OM_LANE_PORT` first.

```sh
control-om om -- agent create --file draft.json --yes --format json
# {"agent":"btc-pricer","instanceId":"agent_…","shadow":true,"reads":["room","market"],"sample":{"ask":…,"reply":…,"checks":[{"name":"no-bare-ack","result":"pass"}]}}
control-om om -- agent ls
# btc-pricer  chat  room messages, market data  held  <job>
control-om om -- agent create --file draft.json --format json < /dev/null
# {"error":"confirmation_required","message":"Creating agent <name> needs your yes.",…}  exit 2
```

Read grant on a run (task door, no auth on loopback):

```sh
curl -sS -X POST http://127.0.0.1:$OM_LANE_PORT/rpc/v1/roster/tasks -H 'content-type: application/json' \
  -d '{"id":"verify-1","agent":"btc-pricer","ask":"what is the price of BTC right now?","requestedBy":{"surface":"direct","userId":"local"}}'
curl -sS "http://127.0.0.1:$OM_LANE_PORT/rpc/v1/roster/tasks/verify-1?wait=25000"
```

The fake model calls `markets` for a "price of" ask. Log the last tool message in the fake model to read the result: a `market` agent reaches the action (`network_error` on a dead data URL), a default agent gets `Unknown tool: markets.`

## Gotchas

- The builder's try is a tool-less preview: its forced `markets` call fails by design, separate from the run's grant.
- The roster stores failed builder replies under the idempotency key, so a refused create replays its refusal until a field changes.
- Agents installed from the registry show `job` null: their description is publisher text.
