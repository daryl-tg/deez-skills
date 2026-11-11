# Move watch legs stranded by an AI provider switch (`om watch reseal`)

*Verified: 2026-11-12 (nightly), tree `82094c3a83` (origin/main, v0.495.0+11; #2462, merged as `c1d9ae2396`), bare lane on 18193 (dummy `OM_API_KEY`, dead service URLs, `openai-compatible` model `fake` on 18192) and guest lane on 18191. Driven: `reseal_nothing_to_move` on a clean home, two legs sealed on `anthropic/claude-opus-5-5` seeded through the product's own stores, the no-AI refusal, the no-terminal refusal, the terminal card, `--yes --format json` moving the model leg in place and leaving the web search leg as not movable, the stored row read back, and a second run refused. Not driven: the notice from `om config set-provider`, `om init` or the daemon's boot check; the `provider_switched` status words on a real search or page source; the chat card; a moved leg actually running. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261112/r1/` (`cli/reseal-*.txt`).*

When you switch AI provider (say Anthropic out, a ChatGPT sign-in in), search, page and model legs your watches read stay sealed on the old provider and stop running. One card moves every movable leg to the AI chat now uses, in place: each leg keeps its id, query, stream, cursor and run history. A leg the new AI cannot run is listed with its reason and left alone.

## Sub-features

- `verb`: `om watch reseal [--yes|-y] [--format text|json]`. In a terminal it shows a card and asks `Move N sealed leg(s) from <old> to <new>?`. The text result is `Moved N leg(s) to <provider>/<model>`, one row per leg, then `Changed since the card, left as is:` and `Not movable:` rows.
- `card`: rows `Lane: <old api lane> → <new>`, `Moves: <kind> "<label>", <cadence> (<watch>)`, `Not movable: <kind> "<label>", <cadence> (<watch>) · <reason>`, `Keeps: each leg's query, stream, cursor and run history (no re-baseline)`, and `Cap lost: …` when a search cap cannot follow.
- `json`: `{target:{provider, model}|null, moved:[{kind, id, watches, label}], changed:[…], not_movable:[{…, reason}]}`.
- `refusals` (exit 2): `reseal_nothing_to_move` `No sealed leg is stranded on this home.` (hint `Nothing to move.`); with no AI connected, `N sealed legs cannot run on this home's AI` / `no AI is connected on this home; connect one first (om init, or /setup in chat)`; off a terminal without `--yes`, `Needs a yes: the moved legs run paid requests on the new provider` / `Fix: run in a terminal to review every leg, or pass --yes (-y)`; when only unmovable legs remain, `1 sealed leg cannot run on this home's AI` with the reason.
- `not-movable reasons`: `<provider>/<model> has no hosted search` (live); `X search runs only on xAI (Grok); …`, a model run sealed with images or a file store, and a leg on the X API token (source, `shared/provider-reseal.ts`).
- `notice` (source): `om config set-provider`, `om config remove-provider`, the setup provider verbs and `om init` print `<title>? Run om watch reseal, or ask in chat to move your watches.`; the daemon logs `[provider-reseal] <line>` at boot and files one `Watch legs need your current AI` notice per stranded set.
- `status` (source): a stranded leg's status reads `this source was approved on an AI provider this machine is no longer signed in to` with the fix `move it to your current AI (om watch reseal, or ask in chat)`, in place of the `om init` fix.
- `chat`: `watch_reseal` is a tier-3 carded tool in om chat and the CLI. It is not on MCP stdio (live: absent from `tools/list`).

## How to get to it (user POV)

Switch provider with `om config set-provider <p>`, `om init` or `/setup`. The command prints the move line when a leg is stranded. Run `om watch reseal` and answer the card, or ask om chat to move your watches.

## Driving it with control-om

No real credential is needed. A lane cannot seal a search or model leg without a model's consent flow, so seed sealed legs with the product's own stores (the same calls `packages/cli/test/provider-reseal.test.ts` makes).

1. Bare lane with a fake model: `control-om up --port <p>` with `--env OM_API_KEY=om_dummy_proto`, the dead service URLs and `--env OPENMARKET_LLM_PROVIDER=openai-compatible --env OPENMARKET_LLM_BASE_URL=http://127.0.0.1:<fake>/v1 --env OPENMARKET_LLM_MODEL=fake`. **Export the same three `OPENMARKET_LLM_*` variables for every `control-om om --` call**: the reseal resolves the chat AI in the CLI process, and without them it reads `no AI is connected`.
2. `control-om om -- watch reseal --format json` → `reseal_nothing_to_move`, exit 2.
3. `watch create vom-ptj --inbound` and `watch create vom-filings --inbound`.
4. Seed with a scratch Bun script run as `OM_HOME=<lane root> OM_BIND=127.0.0.1:<p> bun seed.ts`, importing from the product tree by absolute path: `openDb()`, then `SearchAuthorityStore.seal({subject, engine: "web", query, cadence_sec: 86400, provider: "anthropic", model: "claude-opus-5-5", api_lane: "anthropic-messages", credential_source: "chat", cap_enforceable: true}, …)` attached with `SourceAttachmentStore.sealPending` and `commit({watchId: "vom-ptj", …})`, and `ModelAuthorityStore.seal(sealedModelLegOf({prompt, tools: [], output: "rows", max_tool_calls: 0}, 86400, {…anthropic lane, credential_type: "oauth", search_reach: "none", search_cap_enforceable: false}))` bound with `bindWatch(id, "vom-filings")`.
5. `watch reseal` with no AI in the CLI env → the no-AI refusal naming 2 legs. With the env → the no-terminal refusal.
6. In a terminal (`script -q <file> control-om om -- watch reseal`), seen: `Lane: anthropic-messages → openai-compatible`, `Moves: model run "List each new filing since the last run.", every day (vom-filings)`, `Not movable: web search "Paul Tudor Jones", every day (vom-ptj) · openai-compatible/fake has no hosted search`, `Keeps: …`, and the question `Move 1 sealed leg from anthropic/claude-opus-5-5 to openai-compatible/fake?` with `No` selected.
7. `watch reseal --yes --format json` → `target {openai-compatible, fake}`, `moved` the model leg with its id unchanged, `not_movable` the search leg. Read back: `sqlite3 -readonly <lane>/accounts/guest/om.sqlite "select id, provider, model, api_lane, credential_source from watch_model_authority"` → the same `ma-…` id on `openai-compatible|fake|openai-compatible|chat`; the search row is still on `anthropic`.
8. `watch reseal --yes` again → exit 2, `1 sealed leg cannot run on this home's AI` / `openai-compatible/fake has no hosted search`.

## Gotchas

- The card's prompt is a select with `No` focused. A piped `n` does not answer it; drive it in tmux, or capture the card and stop the process you started.
- A leg seeded onto an `--inbound` watch has no matching source in the watch's spec, so `watch list` and `watch show` do not show the stranded words for it. The status words need a real search, page or model source; they are source-only here.
- The boot check runs only at daemon start and files only a new stranded set. To see `[provider-reseal]` in `runner.log`, seed before `up`.
- `openai-compatible` has no hosted search, so a web search leg always lands in `not_movable` on a fake-model lane.
