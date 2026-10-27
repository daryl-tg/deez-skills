# The capability layer over MCP (stdio)

*Verified: 2026-10-28, tree `a8fa10974` (origin/main, v0.466.0), lane on 18103. Over stdio, `mcp serve --stdio --no-fire-bridge` answered `initialize` as `openmarket` 0.466.0 with no stdout leak. `tools/list` returned 451 tools, `watch_list` read with no error, and `order_place` (Hyperliquid, quote 10) was refused with `capital_yolo_harness`: this nightly runs under bypass mode. Also over stdio: `watchlist_list` refused `missing_api_key`, `nervous_status` read, and `markets` with `exchanges:["LIGHTER"]` refused `invalid_arguments` (not a valid `exchange_id`). Over loopback HTTP on 18125: `initialize`, then `notifications/initialized` (202) and 441 tools. **The responses were plain `application/json`, not SSE frames.** The memory round trip ran (save → search → CLI `memory list` → forget → empty list), `watching_overview` read, `watch_feedback` refused `watch_feedback_not_openfeed`, `GET /mcp` returned 405 and other paths 404. Not driven: `--catalog operator`, `--session merged`, `om mcp arm`, the fire bridge, non-loopback badge auth. Previous stamp `8fe6a8432` is an ancestor (10 commits).*

*Second-pass record: 2026-10-27, tree `8fe6a8432`, lane on 18143.* Hosted MCP over loopback HTTP was driven as above. The stdio handshake was re-driven (`openmarket` 0.466.0, 451 tools). Evidence: `http://127.0.0.1:8098/verify-om-maint-20261027/r1/` (`pending-rows.txt`).

An MCP client (Claude Desktop, Cursor, a coding agent) launches `om mcp serve
--stdio` and gets the same registered actions the CLI and chat use, under the
same schemas. Reads run directly. A call that moves capital is refused unless
the operator armed an approval window out of band, so a client that cannot ask
mid-call never places an order on its own.

## Sub-features

- `mcp-handshake`: `initialize` names the server and version.
- `mcp-catalog`: `tools/list` returns the registered actions (the full catalog
  by default, rooms tools included).
- `mcp-read`: a read action such as `watch_list` runs and returns JSON text.
- `mcp-capital-gate`: a capital action returns `capital_not_armed`, with a hint
  naming `om mcp arm`, before the handler can reach a venue.
- `mcp-validation`: invalid arguments come back as one compact `invalid_arguments`
  line (`Schema validation failed: <path>: <msg>`), not the SDK's verbose error.
- Hosted MCP over loopback HTTP (`om mcp serve --http 127.0.0.1:<port>`): the same capability layer on `POST /mcp`, unauthenticated on loopback unless `OM_LOOPBACK_AUTH=1`.

## How to get to it (user POV)

- `om setup claude-desktop` or `om setup cursor-mcp` writes a client config that
  launches `om mcp serve --stdio`. The dashboard's `/connections` page offers
  the same through its `Coding agents` rows.
- Or run `om mcp serve --stdio` by hand and speak newline-delimited JSON-RPC.

## Driving it with control-om

Preconditions: a lane the run started, so the stdio server opens the lane's
home rather than the operator's.

- **Spawn through the wrapper.** `control-om om -- mcp serve --stdio
  --no-fire-bridge` keeps `OM_HOME` and `OM_BIND` on the lane. Write one JSON
  object per line to stdin and read one per line from stdout. Any non-JSON line
  on stdout is a banner leak and a finding.
- **Sequence.** Send `initialize` (`protocolVersion`, empty `capabilities`,
  `clientInfo`), then the notification `notifications/initialized`, then
  `tools/list`. Assert the server name `openmarket`, the lane's version, and
  that the tool names include `watch_list`.
- **A read.** `tools/call` with `{"name":"watch_list","arguments":{}}`. Expect
  no `isError` and the lane's watches in `content[0].text`.
- **The capital gate, without spending anything.** `tools/call` `order_place`
  with **valid** arguments:
  `{"venue":"hyperliquid","asset":"BTC","side":"buy","order_type":"market","size":{"mode":"quote","value":10}}`.
  Expect `isError` and a payload whose `error` is `capital_not_armed`, whose
  message says the call moves capital (family `order`), and whose hint names
  `om mcp arm`. The lane has no venue paired, so nothing could be placed anyway.
  A driver launched with an auto-approve flag gets `capital_yolo_harness`
  instead (see Gotchas).
- **Proof.** Keep the transcript of the four responses. A tiny Bun script that
  spawns the wrapper and matches responses by `id` is enough; the shape to copy
  is `packages/cli/test/mcp-inspector-smoke.test.ts` in the product repo.

### Hosted MCP over loopback HTTP (added 2026-10-27)

```bash
nohup control-om om -- mcp serve --http 127.0.0.1:<agent-port> > .control-om/mcp-http-<port>.log 2>&1 &
curl -s -X POST http://127.0.0.1:<port>/mcp -H 'content-type: application/json' \
  -H 'accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"t","version":"0"}}}'
```

On 2026-10-27 the responses were SSE-framed (`data: {...}`). On 2026-10-28 the same request with the same `accept` header got `Content-Type: application/json` and a bare JSON body, with `src/mcp` unchanged in between. A driver should strip an optional leading `data: ` and parse either form. In this pass no `mcp-session-id` header came back, and calls worked without one.

- `initialize` returned `serverInfo` `openmarket` 0.466.0, `notifications/initialized` answered 202, and `tools/list` returned **441** tools. That is fewer than stdio's 451 on the same lane; the difference was not traced.
- `GET /mcp` answered 405, and any other path answered 404.
- **Memory round trip** (the actions are MCP-only apart from `om memory list`):
  - `memory_save` with `{"slug":"preference-maint-probe","type":"preference","description":"...","body":"..."}` returned the record. `description` is required: without it the call fails schema validation.
  - `memory_search` found it, and `om memory list --format json` listed it.
  - `memory_forget` returned `forgotten: true` with no approval card, and the list was empty again.
  - The slug prefix must match the type: `type:"user"` requires slug `user`, otherwise the call fails with `memory_invalid_slug`.
- `watching_overview` returned the daemon and watches block. `watch_feedback` with `{"id_or_slug":"<timer watch>","signal":"more"}` (`signal` is `more`, `less` or `clear`) refused with `watch_feedback_not_openfeed`.
- Account-only tools refuse before any request. `watchlist_list` gives `missing_api_key` ("guest keys have no workspaces"). An `exchange_id` outside the 35-value domain is refused at schema validation even when `om exchanges` lists it (see [market data](./market-data-reads.md)).

**Teardown trap:** killing the backgrounded `control-om om --` pid leaves its `bun packages/cli/src/bootstrap.ts mcp serve --http …` child running with PPID 1, still holding the port. Check `lsof -nP -iTCP:<port> -sTCP:LISTEN` and kill that child by pid.

## Gotchas

- **Invalid arguments never reach the gate.** `order_place` with a flat `size`
  or a `coin` field returns `invalid_arguments` (`asset: ... expected string`,
  `size: ... expected object`). That is the validation rewriter answering, not the
  capital gate. Use the exact shape above, which the product's own
  `mcp-capital-gate.test.ts` uses.
- **The capital refusal depends on how the DRIVING session was launched.**
  The stdio server walks its parent process tree (`mcp/harness-sniff.ts`). If
  any ancestor carries an auto-approve flag (`--dangerously-skip-permissions`,
  `--permission-mode bypassPermissions`, `--yolo`, ...), `order_place` is
  refused with `capital_yolo_harness` ("No arm counts in this session")
  instead of `capital_not_armed`. An unattended or bypass-mode agent run lands
  on the first. Driven 2026-10-27 from a nightly session under
  `bypassPermissions`. Both are the capital gate refusing before any venue
  call, so either proves the no-spend claim. Assert `isError` and a `capital_`
  code, and record which one you got and why.
- The tool count (451 here) is the stdio catalog, which is not the registry count
  (478 at this tree). Assert membership, not a number.
- `--no-fire-bridge` keeps watch-fire log notifications off stdout, so the
  response stream stays request/response only. Drop it only when the bridge is
  under test.
- Never point a probe at the operator's daemon or a bare `om mcp serve`: it would
  open `~/.openmarket`.
