# om creates an agent (agent_create, agent_tools, agent_fit)

*Driven 2026-11-10 on a real model, tree `8c3c5ebdf5` (origin/main, v0.493.1), lane on 18171 from a copy of the signed-in seed home (`dboon_ref`, `anthropic/claude-opus-5-5`), `om chat` TUI in tmux. First drive of chat choosing `agent_create` from a sentence: `create an agent from https://github.com/janestreet/agent_skills` ran `skill_read` x2, `tool_search` (six names), `page_read` x2 (the first behind an origin card), `agent_list`, `agent_tools`, `agent_fit` x2 and `agent_create` behind its card, then installed `socratic-tutor` in shadow and tried the first sample ask. 352 s wall, 38 model rounds, $1.76 on the home's `llm_rounds` ledger. The card read `FIT not run for this draft` although the second fit ran on the identical draft. Then `agent_run` twice from chat and four task-door asks, all completed in 10 to 15 s. Not driven: an `@mention` in a room, a room grant, the GUI card. Evidence: `~/Documents/dev-notes/om-agent-build-socratic-tutor/run-artifacts/` (`agent-log-build.log`, `llm-rounds-ledger.txt`, `frame-03-create-card.txt`, `fit-row-replay.txt`, `fit-row-digests.txt`, `task-door-asks.json`). No gallery: terminal-only run.*

*Re-driven 2026-11-09 (scheduled maintenance), tree `0d3d29cd27` (origin/main, v0.493.0), bare lane on 18145 (dummy `OM_API_KEY`, dead service URLs) with a scripted fake model on 18144. Over MCP stdio, `agent_tools {query:"price markets"}` (`markets` first, weight 5817) and `agent_fit` on the pricer-fit draft (`passed 3/3`; the fake called no tool). The TTY card and create were not re-driven. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261109/r1/`.*

*Re-driven 2026-11-09 (nightly), tree `5bfa0ccf6` (origin/main, v0.492.0), guest lane on 18143, booted with no guest 429. `agent_tools {query:"price markets"}` (`markets` first) and `agent_fit` 3/3 over MCP stdio on a guest lane plus a fake model; `agent_fit` with 2 `sampleAsks` is refused `exactly 3 items`. The fake called no tool, so `refusedTools` was not exercised; the TTY card and create are not driven. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261109/r1/` (`cli/98`, `cli/102`).*

*Re-driven on main 2026-11-05 (nightly), tree `3a0ea623e` (origin/main, v0.492.0; #2295, #2303), bare lane on 18165 (dummy `OM_API_KEY`, dead service URLs) with a scripted fake model on 18164 that reports `usage`. Driven: `agent create --file draft.json --format json </dev/null` exit 2 `confirmation_required` (`Creating agent pricer-fit needs your yes.`); `--yes` → `{agent, instanceId, shadow:true, tools:["markets"], sample:{ask, reply, checks:[{name:"no-bare-ack",result:"pass"}]}}`; over MCP stdio `agent_tools {query:"price markets"}` (`markets` first, weight 5663), `agent_fit` with `tools:["points"]` (`passed 3/3`, `unusedTools [points]`, `refusedTools [markets]`) and with `["markets"]` (nothing unused or refused); the TTY card in tmux (`Job`, `Won't`, `Tools  markets (1)`, `Fit`, `Brain  om`, `Replies  held for your OK`, `Create agent pricer-card?  ○ Yes / ● No`), a decline (`om: Aborted by user.`, exit 2) and a yes (`Created pricer-card; replies are held for your OK.` plus `Sample:` and `Reply:`). **The card read `Fit  not run for this draft` even right after `agent_fit` on the identical draft, twice** (README gaps). Not driven: om chat choosing `agent_create` on a real model, a coding (`work`) draft. Evidence: `http://127.0.0.1:8098/vom-nightly-20261105/r1/` (`cli/agent-create-*`, `cli/mcp-fit.json`, `tui/01-04`).*

*Verified: 2026-11-03, branch `daryl/agent-creator-sharp` tree `1e4cf9f03` (stacked on PR #2295, not yet on main), lane on 18152, bare lane with a fake model on 18153. Driven: `agent_tools` and `agent_fit` over MCP stdio (two fit rounds), `om agent create` through a TTY for the fitted draft and for a changed draft, and a task-door run of a created agent showing the tools it is offered. Earlier tree `7e93059ef` (same branch): the card's `Won't` and `Tools` rows, the offered tool list, `toolsWire` size, and a refused old `reads` draft. Earlier tree `1f6b53df6` (PR #2295): create with and without `--yes`, a TTY decline, replay, and `name_taken`. Not driven: `om chat` choosing `agent_create` from a sentence on a real model, and the chat card on a GUI surface (its rows come from the same approval carrier and are pinned by `packages/cli/test/agent-create.test.ts`). The fake model is scripted, so the lane proves the plumbing (offered tools, refusals, card rows), not draft quality. Evidence: `~/Documents/dev-notes/om-agent-creation/run-artifacts/lane-18152-{1f6b53df6,7e93059ef,fit}/`, galleries `http://127.0.0.1:8098/agent-create-20261103/r1/` and `http://127.0.0.1:8098/agent-creator-sharp-20261103/r2/`.*

om turns a draft into an installed roster agent behind one tier-3 card. The draft names the agent's job, what it never does, and up to 8 tools; a fit run checks those tools against the sample asks before the card.

## Sub-features

- `agent_create` (tier 3): stage, install (shadow: replies held), then try the first sample ask. Card rows `Job`, `Won't`, `Tools: a, b (n)`, `Fit`, `Brain`, `Project` (work only), `Replies: held for your OK`; question `Create agent <name>?`.
- Draft input is strict: `name`, `job`, `antiJobs` (1-5 single-line entries), `whenToUse`, `tools` (1-8), `template` (`explain`, `fact-check`, `argue`, `debugger`, `feature`, `blank`), `instructions`, `sampleAsks` (exactly 3, single-line), `checks`, and optionally `knowledge` and `work {projectId, brain: claude|codex}` for a coding agent (source). A draft still carrying `reads` is refused as an unknown key.
- `antiJobs` are appended to the instructions as a `You never:` block; instructions plus that block are capped at 4096 bytes.
- `tools` must be grantable (`packages/cli/src/actions/agents/_grantable.ts`): tier-1 reads in `market-data` (not `usage`, `usage_llm`), `polymarket`, `chart` (`symbol_resolve` only), `rooms` (13 room and doc reads) and `news` (not overview, billing, catalog, preview). Anything else is refused with the nearest grantable names. The run holds exactly the named tools plus `post_reply`; work agents also get `repo_read`.
- `agent_tools` (tier 1): ranks grantable tools for a query by relevance, then weight (description plus schema chars), capped at 40 rows. Each row has `name`, `category`, `weight`, `tagline`.
- `agent_fit` (tier 1): runs the draft's sample asks with only its tools and returns per ask `toolsCalled`, `toolsRefused` and checks, plus `passed`, `unusedTools`, `refusedTools`. The record is stored under the package digest; the card's `Fit` row is read from the daemon (`POST /rpc/v1/roster/local-packages/draft-fit`), never from model arguments: `x/3 asks pass` (with `; unused: a, b` and `; refused: c` when there are any), `not run for this draft` (the lookup answered 404), or `unknown`. A coding (`work`) draft has no `Fit` row, and `agent_fit` refuses it `bad_request` `A coding agent has no fit run.` (source).
- A changed draft restages over its uninstalled staged copy.
- Idempotency keys `agent-create.<step>.<sha256 of input>`: an identical rerun replays, a changed field mints new keys.
- Refusals: `name_taken` (reads the installed instances), `sign_in_required`, `agents_unavailable`, `bad_request`, `rpc_failed`, `aborted`.
- `om agent create --file <draft.json|->` shows the card on the terminal, `Fit` row included; `--yes` skips the card and the fit read; no TTY and no `--yes` is `confirmation_required`, exit 2. Listing agents is `om agent list` from #2297, not this feature.

## How to get to it (user POV)

Ask om chat "make me an agent that ...": the skill (`skills/agents.md`) asks up to 3 preference questions in one message, picks tools with `agent_tools`, runs `agent_fit`, then shows the card. Or write a draft JSON and run `om agent create --file draft.json`.

## Driving it with control-om

A bare lane boots in seconds and the builder accepts its owner. Use the bare-lane recipe (dummy `OM_API_KEY`, every service URL `http://127.0.0.1:9`, `OPENMARKET_LLM_PROVIDER=openai-compatible` pointed at a fake model: a `Bun.serve` on `127.0.0.1` answering `/v1/models` and streaming `/v1/chat/completions` as SSE, calling `markets` for a "price of" ask and otherwise streaming text, with a final chunk carrying `usage`) and pass the same env on every `control-om om --` call. Export `OM_LANE_PORT` first.

```json
{"name":"pricer-fit","job":"answers what a coin is trading at, from live market data","antiJobs":["give trade advice"],"whenToUse":["someone asks the price of a coin"],"tools":["markets"],"template":"explain","instructions":"You answer price questions in one plain line: the last price and the venue.","sampleAsks":["what is the price of BTC right now?","what is the price of ETH on Hyperliquid?","summarise the BTC tape"],"checks":["no-bare-ack"]}
```

Fit loop over MCP stdio (`om mcp serve --stdio` with the lane env, `tools/call`). `agent_fit` takes the draft's fields as its top-level arguments; wrapping them in `{"draft": …}` is refused `invalid_arguments` listing every field as `undefined`:

```text
agent_tools {query:"price markets"}            -> markets first, each row with its weight
agent_fit   {draft with tools:["points"]}      -> refusedTools [markets], unusedTools [points]
agent_fit   {draft with tools:["markets"]}     -> nothing refused, nothing unused
```

Card on the terminal (needs a TTY; drive with `expect`):

```sh
control-om om -- agent create --file draft.json
# Job / Won't / Tools markets (1) / Fit 3/3 asks pass / Brain om / Replies held for your OK
# add one antiJob and rerun -> Fit not run for this draft
control-om om -- agent create --file draft.json --format json < /dev/null
# {"error":"confirmation_required","message":"Creating agent <name> needs your yes.",…}  exit 2
```

Offered tools on a run (task door, no auth on loopback):

```sh
curl -sS -X POST http://127.0.0.1:$OM_LANE_PORT/rpc/v1/roster/tasks -H 'content-type: application/json' \
  -d '{"id":"verify-1","agent":"pricer","ask":"what is the price of BTC right now?","requestedBy":{"surface":"direct","userId":"local"}}'
curl -sS "http://127.0.0.1:$OM_LANE_PORT/rpc/v1/roster/tasks/verify-1?wait=25000"
```

Log the tools array in the fake model: a created agent holding `markets, points` was offered exactly `post_reply, markets, points` (14,229 chars of tool wire per step against 59,999 for a bundle-based agent). An ungranted name the model calls answers `Unknown tool: X.`

## Gotchas

- The fake model calls `markets` for any "price of" ask, which is what makes round 1 report `markets` refused. A real model's choices are the parked eval, not this recipe.
- The builder's try is the first sample ask only; `agent_fit` runs all three.
- The roster stores failed builder replies under the idempotency key, so a refused create replays its refusal until a field changes.
- Replaying an older create after its draft was restaged answers `not_found` rather than recovering.
- Fit tokens are not counted against the agent's chat budget ([agent-chat-budget.md](agent-chat-budget.md)).
- The card's `Fit` row reads `not run for this draft` for every fitted draft on main (measured 2026-11-10, tree `8c3c5ebdf5`). A fit is stored under the folder digest, which includes `om-package.json` (`prepareLocalChatFolder`), and `fitForDraft` (`packages/roster/src/builder.ts`) looks it up under the package digest without that file (`prepareLocalChatPackage`). Replay: `POST /rpc/v1/roster/local-packages/draft-fit` with a just-fitted draft answers 404 `This draft has no fit run.` while `roster.builder_fits` in `settings` holds the record. The chat reply still says `Fit: 3/3`, from the tool result.
- The fit and the try name a fixture room `builder` that no relay serves, so a room read fails there (13 of 13 `room_history` calls `ok:false`, 2026-11-10). `agent_fit` still lists the tool under `toolsCalled`, never under `unusedTools`, and a draft with no `checks` passes every ask that returns a reply. Read `passed` as "the run finished", not as a quality score.
- `agent_fit` runs its three asks one after another, about 30 s each on Opus 5.5, so one fit is about 92 s and two rounds are over half of a build's wall time.
- On an Anthropic lane a mid-conversation tool load rewrites the whole cached prefix: `cache_break changed:["tools"] cacheRead:0` in `agent.log` after the `tool_search` load (62,441 tokens written) and again when `agent_run` loaded (81,852). Read spend per round from `llm_rounds` in the home's `om.sqlite` (`cost_usd`, `fingerprint`).
- Creating an agent queues a `portrait` run for it; on the fake model it fails and shows in `agent ps` and the agents overlay.
- Publishing an agent om created (dry runs driven 2026-11-10, tree `16daf71ddc`, lane 18171; the publish itself is pending, not driven). `agent_create` writes `om-package.json` as `@local/<name>`, which the registry never accepts: copy the folder from `<home>/roster/local/<name>/` and rename it `@<username>/<name>` first. `om publish <dir> --dry-run --format json` printed the plan (6 files, 4,194 bytes, the sha256, `cover_need: none` on a lane that cannot draw). `--validate` ran the registry's zero-write gate and answered `validated: true` on staging and with `--registry production`. `om publish` targets staging by default (`DEFAULT_REGISTRY_ORIGIN`), while agent installs read production (`packages/cli/src/runner/roster-host/registry.ts:45`), so an agent meant to be installed needs `--registry production`.
- Over MCP, `package_publish` answers `capital_not_armed` (family `registry`) even with `dry_run: true`, although its description says the dry run raises no card. It needs the operator's `om mcp arm` in their own terminal. Dry-run from the lane CLI instead.
