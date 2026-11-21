# The research catalog over HTTP

*Re-driven 2026-11-22 (nightly), tree `01482928a5` (origin/main, v0.496.0+internal), guest lane on 18188 through `bootstrap.internal.ts`. The endpoint from source on 18192 against the lane's home: both boot lines, 401 with no bearer, `auth_invalid` with a wrong one, `initialize` with the home's token, **25** tools with no `order_place` and no `watch_list`, `badge_refused` with a badge header. Not re-driven: the four pins (a `backtest_run` with no `target` is refused by its schema first), `search` and `fetch`, the start refusals. (`cli/70-*`.) Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261122/r1/`*

*Verified: 2026-11-21 (nightly), tree `3c4839c59d` (origin/main, v0.496.0+internal), guest lane on 18188 started through `bootstrap.internal.ts`, the endpoint started from source on 18192 against the lane's home. First live proof of #2627 and #2648. Driven: both start refusals, the two boot lines, 401 with no bearer and with a wrong one, 401 `badge_refused`, 404 on another path, `initialize` and `tools/list` (25 tools), `coins`, `metric_list` and `schema_read`, five argument refusals, and `search` and `fetch` on `/mcp/search-fetch`. Not driven: a backtest that runs, `news_catalog`, `news_preview` and `backtest_news` past the guest refusal, a non-loopback bind, `research_catalog_private_feed`. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261121/r1/` (`cli/22` to `cli/29`).*

`om mcp serve --http --catalog research` serves a small read-and-backtest set of tools over HTTP for a research client. It lists market data, metrics, backtests and the public news tools. It lists no watch, order, room or chart tool, and every call needs the home's bearer token, on loopback too.

## Sub-features

- `start`: `om mcp serve --http <host:port> --catalog research`. Stderr prints `om: MCP HTTP server listening on http://<host:port>/mcp` and `om: research catalog: bearer from <home>/runner.token required; search/fetch at /mcp/search-fetch`.
- `http-only`: without `--http` it exits 2 with `om: catalog_http_only: --catalog research is HTTP-only (om mcp serve --http).` A bad value exits 2 with `om: --catalog takes 'full', 'operator' or 'research', got '<value>'`.
- `bearer`: every request needs `Authorization: Bearer <the home's runner.token>`.
  - No header: 401 `auth_required`, with a message that names the missing `Authorization: Bearer <token>` header.
  - A wrong token: 401 `auth_invalid`, `Token is not accepted by this listener.`
  - An agent badge header (`x-om-agent-secret`) beside a good bearer: 401 `badge_refused`, `the research catalog serves the operator session only: drop the agent badge.`
- `paths`: `/mcp` and `/mcp/search-fetch`. Any other path is 404 `not_found`, `unknown path <path>`.
- `catalog`: `initialize` answers server `openmarket` with no `instructions`. `tools/list` holds 25 tools, each with `readOnlyHint: true` and `destructiveHint: false`:
  - market data: `points`, `markets`, `symbols`, `coins`, `exchanges`, `symbol_resolve`, `normalized_symbols`, `market_resolve`, `enum`, `tenors`
  - metrics: `metric_get`, `metric_list`, `metric_rule`, `metric_screen`, `metric_series`
  - backtests: `backtest_spec`, `backtest_run`, `backtest_sweep`, `backtest_report`, `backtest_news`
  - news (#2648): `news_catalog`, `news_preview`
  - `research_study`, `schema_read`, `skill_read`
- `not-listed`: a tool outside the list answers `MCP error -32602: Tool <name> not found` (live for `order_place`, `news_overview`, `watch_list`).
- `pinned-arguments`: the endpoint refuses arguments that would spend a model call or open a chart. Each answer is a tool error with a hint ending `or run it from om chat or a terminal.`
  - `research_catalog_pinned`: `backtest_run: max_llm_calls is fixed at 0 on the research endpoint.`
  - `research_catalog_pinned`: `backtest_run: auto_backfill is fixed at false on the research endpoint.`
  - `research_catalog_pinned`: `news_catalog: feed is not taken on the research endpoint.`
  - `research_catalog_capped`: `backtest_news: max_llm_calls is at most 400 on the research endpoint.`
  - Source only: `open_chart` is pinned the same way, and `research_catalog_private_feed` refuses a feed that is not a public catalog feed this home follows.
- `search-fetch`: `/mcp/search-fetch` is a second MCP server, `openmarket-research`, with two tools.
  - `search {query}` answers up to 8 results, each `{id: "tool:<name>", title, url: "om://mcp/research/<name>"}`.
  - `search` with `<tool> {json}` as the query answers one `call:<base64url>` id.
  - `fetch {id: "tool:<name>"}` answers that tool's description and schema.
  - `fetch {id: "call:…"}` runs the call and answers its result as text.
  - A tool outside the catalog is `{"error":"not_found","message":"no research tool <name>"}`; any other id is `unknown id <id>`.
- `guest`: on a guest lane `news_catalog` and `backtest_news` answer `guest_not_allowed` after the endpoint's own argument checks.

## How to get to it (user POV)

1. Run `om mcp serve --http 127.0.0.1:<port> --catalog research` on the machine that holds the home.
2. Give the research client the address `http://127.0.0.1:<port>/mcp` and the bearer token from `<home>/runner.token`.
3. A client that only speaks search and fetch uses `http://127.0.0.1:<port>/mcp/search-fetch`.

## Driving it with control-om

Preconditions: a lane the run started, `OM_LANE_PORT` exported, and one more free agent port for the endpoint. No account and no model are needed.

1. Refusals first: `control-om om -- mcp serve --stdio --catalog research </dev/null` exits 2 `catalog_http_only`. `control-om om -- mcp serve --http 127.0.0.1:<port> --catalog bogus </dev/null` exits 2.
2. Start it from the checkout with the lane's home, and keep the pid:
   `OM_HOME=<checkout>/.control-om/home-<lane> OM_BIND=127.0.0.1:<lane> nohup bun packages/cli/src/bootstrap.internal.ts mcp serve --http 127.0.0.1:<port> --catalog research > research.log 2>&1 & echo $! > research.pid`.
   `control-om om -- mcp serve` works too, but it stays in the foreground.
3. Read `research.log` for the two boot lines. The second names the token file: `<lane home>/accounts/guest/runner.token`.
4. `curl -s -X POST http://127.0.0.1:<port>/mcp` with an `initialize` body and no bearer: expect 401 `auth_required`. Repeat with `Authorization: Bearer wrong`: expect 401 `auth_invalid`.
5. With the bearer, send `initialize`, `notifications/initialized` and `tools/list`. Send `Accept: application/json, text/event-stream` and carry the `Mcp-Session-Id` response header on every later request. Expect 25 tools and no `instructions`.
6. Call `coins` (a real answer on a guest key), then `backtest_run {"target":"<a watch slug>","max_llm_calls":5}`, `backtest_run {"target":"<slug>","auto_backfill":true}`, `news_catalog {"feed":"x"}` and `backtest_news {"feed":"x","max_llm_calls":401}`. Expect the four refusals above.
7. Call `order_place {}`: expect `Tool order_place not found`.
8. Repeat the handshake on `/mcp/search-fetch`. Call `search {"query":"markets"}`, `fetch {"id":"tool:markets"}`, `search {"query":"exchanges {}"}`, then `fetch` the `call:` id it returns.
9. Add the header `x-om-agent-secret: anything` to an `initialize`: expect 401 `badge_refused`.
10. Stop it: `kill "$(cat research.pid)"`, then `lsof -nP -iTCP:<port> -sTCP:LISTEN` shows nothing.

## Gotchas

- The default bind is `127.0.0.1:31338`, the operator's shared MCP port. Always pass an agent port.
- The bearer is the daemon's own `runner.token`. Read it from the file into a shell variable. Never save it in evidence.
- A schema error comes before a pin. `backtest_run {"max_llm_calls":5}` with no `target` answers `invalid_arguments`, not `research_catalog_pinned`.
- `backtest_run {"open_chart":true}` answers `invalid_arguments` (`open_chart` takes a string). Pass a string to reach the pin.
- `points {type, exchange, rawSymbol, interval, lookback}`, the CLI's flag names, answered `Bad Request` `exchange does not exist`. Read the arguments with `fetch {"id":"tool:points"}` first.
- The research catalog is not on stdio and not on the lean face. `mcp-stdio.md` covers those.
