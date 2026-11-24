# The research catalog over HTTP and stdio

*Re-driven 2026-11-25 (nightly), tree `d5ff40419` (origin/main, v0.497.0+internal), guest lane on 18188 through `bootstrap.internal.ts`, over stdio. Still **26** tools. First live proof of #2684: with `OPENMARKET_LLM_PROVIDER=google` and a dummy key on the CLI call, `web_research {"question":"nightly probe q"}` is `web_search_uncapped_provider` `The model provider (google) does not enforce a search-call cap on its API, and web research here runs only under one.`, hint `om chat and a terminal run it on any provider.`; with no model on the call it is still `llm_not_configured`. The pinned and capped refusals now cross MCP whole (`web_research: sources is fixed at ["web"] on the research endpoint.`, `web_research: max_searches is at most 5 on the research endpoint.`, `news_catalog: feed is not taken on the research endpoint.`). Source only: #2666's news allow-list and the HTTP answer budget (#2693). (`cli/mcp-research-web.txt`, `cli/mcp-tool-counts.txt`.) Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261125/r1/`*

*Verified: 2026-11-24 (nightly), tree `26d502c689` (origin/main, v0.496.0+internal), guest lane on 18188 through `bootstrap.internal.ts`. First live proof of #2675 (stdio), #2680 (`web_research`) and #2667 with #2649 (the inbox gate), all over stdio: `--catalog research` serves **26** tools, `catalog_operator_only` with `--face lean` and with `--session`, the `--catalog bogus` sentence, `coins`, `order_place` not found, `web_research` `research_catalog_pinned` (`sources: ["x"]`) and `research_catalog_capped` (`max_searches: 6`), a third `web_research` passing the guard to `llm_not_configured`, and `research_catalog_private_watch` from `backtest_run` on an inbox watch and on a watch reading it and from `research_study` on the reader, with a timer watch answering `backtest_no_history` and an empty study. Not re-driven tonight: the HTTP endpoint (bearer, `search-fetch`, the four older pins), the HTTP second boot line (source only), a `web_research` answer (needs a model credential). Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261124/r1/` (`cli/22`, `cli/23`, `cli/26`, `cli/27`).*

*Re-driven 2026-11-22 (nightly), tree `01482928a5` (origin/main, v0.496.0+internal), guest lane on 18188 through `bootstrap.internal.ts`. The endpoint from source on 18192 against the lane's home: both boot lines, 401 with no bearer, `auth_invalid` with a wrong one, `initialize` with the home's token, **25** tools with no `order_place` and no `watch_list`, `badge_refused` with a badge header. Not re-driven: the four pins (a `backtest_run` with no `target` is refused by its schema first), `search` and `fetch`, the start refusals. (`cli/70-*`.) Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261122/r1/`*

*Verified: 2026-11-21 (nightly), tree `3c4839c59d` (origin/main, v0.496.0+internal), guest lane on 18188 started through `bootstrap.internal.ts`, the endpoint started from source on 18192 against the lane's home. First live proof of #2627 and #2648. Driven: both start refusals, the two boot lines, 401 with no bearer and with a wrong one, 401 `badge_refused`, 404 on another path, `initialize` and `tools/list` (25 tools), `coins`, `metric_list` and `schema_read`, five argument refusals, and `search` and `fetch` on `/mcp/search-fetch`. Not driven: a backtest that runs, `news_catalog`, `news_preview` and `backtest_news` past the guest refusal, a non-loopback bind, `research_catalog_private_feed`. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261121/r1/` (`cli/22` to `cli/29`).*

`om mcp serve --http --catalog research` serves a small read-and-backtest set of tools over HTTP for a research client, and `om mcp serve --stdio --catalog research` serves the same set over stdio (#2675). It lists market data, metrics, backtests, the public news tools and one web search. It lists no watch, order, room or chart tool, and every call needs the home's bearer token, on loopback too.

## Sub-features

- `start`: `om mcp serve --http <host:port> --catalog research`. Stderr prints `om: MCP HTTP server listening on http://<host:port>/mcp` and `om: research catalog: bearer from <home>/runner.token required; search/fetch at /mcp/search-fetch`. Since #2649 a further line reads `om: Exposes: your watches' journals, verdicts and rules (not inbox watches or their readers)` (source only on 2026-11-24).
- `stdio` (#2675): `om mcp serve --stdio --catalog research` lists the same 26 tools as HTTP and never gets the alert-fire bridge. The old `catalog_http_only` refusal is gone. It serves the operator session alone: with `--face lean` or `--session <x>` it exits 2 with `om: catalog_operator_only: --catalog research serves the operator session alone; drop --session and --face lean.` An agent badge identity gets the same code (source). A bad value exits 2 with `om: --catalog takes 'full', 'operator' or 'research', got '<value>'`.
- `bearer`: every request needs `Authorization: Bearer <the home's runner.token>`.
  - No header: 401 `auth_required`, with a message that names the missing `Authorization: Bearer <token>` header.
  - A wrong token: 401 `auth_invalid`, `Token is not accepted by this listener.`
  - An agent badge header (`x-om-agent-secret`) beside a good bearer: 401 `badge_refused`, `the research catalog serves the operator session only: drop the agent badge.`
- `paths`: `/mcp` and `/mcp/search-fetch`. Any other path is 404 `not_found`, `unknown path <path>`.
- `catalog`: `initialize` answers server `openmarket` with no `instructions`. `tools/list` holds 26 tools, each with `readOnlyHint: true` and `destructiveHint: false`:
  - market data: `points`, `markets`, `symbols`, `coins`, `exchanges`, `symbol_resolve`, `normalized_symbols`, `market_resolve`, `enum`, `tenors`
  - metrics: `metric_get`, `metric_list`, `metric_rule`, `metric_screen`, `metric_series`
  - backtests: `backtest_spec`, `backtest_run`, `backtest_sweep`, `backtest_report`, `backtest_news`
  - news (#2648): `news_catalog`, `news_preview`
  - web (#2680): `web_research`
  - `research_study`, `schema_read`, `skill_read`
- `not-listed`: a tool outside the list answers `MCP error -32602: Tool <name> not found` (live for `order_place`, `news_overview`, `watch_list`).
- `pinned-arguments`: the endpoint refuses arguments that would spend a model call or open a chart. Each answer is a tool error with a hint ending `or run it from om chat or a terminal.`
  - `research_catalog_pinned`: `backtest_run: max_llm_calls is fixed at 0 on the research endpoint.`
  - `research_catalog_pinned`: `backtest_run: auto_backfill is fixed at false on the research endpoint.`
  - `research_catalog_pinned`: `news_catalog: feed is not taken on the research endpoint.`
  - `research_catalog_capped`: `backtest_news: max_llm_calls is at most 400 on the research endpoint.`
  - `research_catalog_pinned` for `web_research` with any `sources` but `["web"]`, and `research_catalog_capped` for `max_searches` over 5 (an absent one is filled with 5). Since #2684 these refusals, and `web_search_uncapped_provider`, cross MCP whole: `web_research: sources is fixed at ["web"] on the research endpoint.`, hint `Drop sources, or run it from om chat or a terminal.`; `web_research: max_searches is at most 5 on the research endpoint.` (live 2026-11-25). Before it the message was withheld as publisher text. A call that passes the guard runs one web search on the operator's model credential, and only on a provider that enforces a search-call cap (`openai`, `xai`, `anthropic`); any other provider (`google`, `openrouter`, `openai-codex`) is `web_search_uncapped_provider` `The model provider (<provider>) does not enforce a search-call cap on its API, and web research here runs only under one.`, hint `om chat and a terminal run it on any provider.` (live with `google`). A guest lane with no model answers `llm_not_configured` (its message still withheld), and an `openai-compatible` model answers `web_search_unsupported` before the cap check (source).
  - Source only: `open_chart` is pinned the same way, and `research_catalog_private_feed` refuses a feed that is not a public catalog feed this home follows.
- `search-fetch`: `/mcp/search-fetch` is a second MCP server, `openmarket-research`, with two tools.
  - `search {query}` answers up to 8 results, each `{id: "tool:<name>", title, url: "om://mcp/research/<name>"}`.
  - `search` with `<tool> {json}` as the query answers one `call:<base64url>` id.
  - `fetch {id: "tool:<name>"}` answers that tool's description and schema.
  - `fetch {id: "call:…"}` runs the call and answers its result as text.
  - A tool outside the catalog is `{"error":"not_found","message":"no research tool <name>"}`; any other id is `unknown id <id>`.
- `private-watch` (#2649, #2667): the endpoint reads no inbox watch (an `inbound` source) and no watch downstream of one, through journal, upstream, `input.watch_id` and series edges. Every id or slug such a watch carries, and a name om cannot read, answers `research_catalog_private_watch`: `<tool>: the research endpoint reads no inbox watch, nor a watch that reads one.`, hint `Name a watch from watch_list, or replay market data alone.` It covers `backtest_spec`, `backtest_run`, `backtest_sweep` and `research_study`; `backtest_news` is refused when any watch on its feed's stream is (source). A watch with no inbox upstream passes to its own answer (`backtest_no_history` for a fresh timer watch).
- `guest`: on a guest lane `news_catalog` and `backtest_news` answer `guest_not_allowed` after the endpoint's own argument checks.
- `news-allow-list` (#2666, source only): the news reads answer named fields only. `news_catalog` keeps `provider`, `next_token`, `dropped_rows` and per entry `provider, id, label, kind, curated, sourcePaused, description, alertWhen, query, prompt, interestLabels, watchFor, trackedEntities, customTargets, featured, paid, packageOnly, followerCount, forkCount`; `isFollowing`, `isOwner` and the listing's `next` are dropped. `news_preview` answers `provider`, `preview` and `hint` only, with no `next` step naming `watch_create`. A guest lane cannot reach past `guest_not_allowed`, so unit tests (`mcp-research-catalog.test.ts`) prove it.
- `answer-budget` (#2693, source only): over HTTP, its badge sessions and the `/mcp/search-fetch` adapter, answers are compact and cut at 40,000 characters, as on stdio.

## How to get to it (user POV)

1. Run `om mcp serve --http 127.0.0.1:<port> --catalog research` on the machine that holds the home.
2. Give the research client the address `http://127.0.0.1:<port>/mcp` and the bearer token from `<home>/runner.token`.
3. A client that only speaks search and fetch uses `http://127.0.0.1:<port>/mcp/search-fetch`.

## Driving it with control-om

Preconditions: a lane the run started, `OM_LANE_PORT` exported, and one more free agent port for the endpoint. No account and no model are needed.

1. Refusals first: `control-om om -- mcp serve --stdio --catalog research --face lean </dev/null` and `... --session x </dev/null` exit 2 `catalog_operator_only`. `control-om om -- mcp serve --http 127.0.0.1:<port> --catalog bogus </dev/null` exits 2.
2. Start it from the checkout with the lane's home, and keep the pid:
   `OM_HOME=<checkout>/.control-om/home-<lane> OM_BIND=127.0.0.1:<lane> nohup bun packages/cli/src/bootstrap.internal.ts mcp serve --http 127.0.0.1:<port> --catalog research > research.log 2>&1 & echo $! > research.pid`.
   `control-om om -- mcp serve` works too, but it stays in the foreground.
3. Read `research.log` for the two boot lines. The second names the token file: `<lane home>/accounts/guest/runner.token`.
4. `curl -s -X POST http://127.0.0.1:<port>/mcp` with an `initialize` body and no bearer: expect 401 `auth_required`. Repeat with `Authorization: Bearer wrong`: expect 401 `auth_invalid`.
5. With the bearer, send `initialize`, `notifications/initialized` and `tools/list`. Send `Accept: application/json, text/event-stream` and carry the `Mcp-Session-Id` response header on every later request. Expect 26 tools and no `instructions`.
6. Call `coins` (a real answer on a guest key), then `backtest_run {"target":"<a watch slug>","max_llm_calls":5}`, `backtest_run {"target":"<slug>","auto_backfill":true}`, `news_catalog {"feed":"x"}` and `backtest_news {"feed":"x","max_llm_calls":401}`. Expect the four refusals above.
7. Call `order_place {}`: expect `Tool order_place not found`.
8. Repeat the handshake on `/mcp/search-fetch`. Call `search {"query":"markets"}`, `fetch {"id":"tool:markets"}`, `search {"query":"exchanges {}"}`, then `fetch` the `call:` id it returns.
9. Add the header `x-om-agent-secret: anything` to an `initialize`: expect 401 `badge_refused`.
10. The inbox gate, over either transport: `control-om om -- watch create probe --inbound`, `watch create downstream --upstream probe`, `watch create tick --every 1h`. Call `backtest_run {"target":"probe"}`, `backtest_run {"target":"downstream"}` and `research_study {"watch":"downstream","locate_only":true}`: each is `research_catalog_private_watch`. The same calls on `tick` pass the gate. Over stdio, pipe `initialize`, `notifications/initialized`, `tools/list` and the `tools/call` lines into `control-om om -- mcp serve --stdio --catalog research` and read one JSON line per id.
11. `web_research {"question":"test question","sources":["x"]}` and `{..., "max_searches":6}` show the pin and the cap with no provider call.
12. Stop it: `kill "$(cat research.pid)"`, then `lsof -nP -iTCP:<port> -sTCP:LISTEN` shows nothing.

## Gotchas

- The default bind is `127.0.0.1:31338`, the operator's shared MCP port. Always pass an agent port.
- The bearer is the daemon's own `runner.token`. Read it from the file into a shell variable. Never save it in evidence.
- A schema error comes before a pin. `backtest_run {"max_llm_calls":5}` with no `target` answers `invalid_arguments`, not `research_catalog_pinned`.
- `backtest_run {"open_chart":true}` answers `invalid_arguments` (`open_chart` takes a string). Pass a string to reach the pin.
- `points {type, exchange, rawSymbol, interval, lookback}`, the CLI's flag names, answered `Bad Request` `exchange does not exist`. Read the arguments with `fetch {"id":"tool:points"}` first.
- The research catalog is never on the lean face. A schema error comes before the inbox gate too: `research_study` needs `asset`, `horizons` and `pre`, or `locate_only: true`.
- `mcp-stdio.md` covers the full and lean stdio faces.
