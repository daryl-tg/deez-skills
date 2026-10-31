# The capability layer over MCP (stdio)

*Re-driven 2026-11-01 (nightly), tree `7ce379c45` (origin/main, v0.480.3), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 2.9. Lane up. `mcp serve --stdio --no-fire-bridge` answered `initialize` as `openmarket` 0.480.3 and `tools/list` returned **454** tools (`file_create`, `channel_default_set`, `package_open`, `package_search`, `chart_indicator_add` present; `document_draft` and `sidebar_layout` absent). `watch_list` read the lane's watches. `order_place` → `capital_yolo_harness` under this bypass-mode driver. New for #2234 ([kScript retirement](./kscript-retirement.md)): `package_search {query, kind:"kscript-indicator"}` → `isError` `kind_retired` in 0 ms (no registry call; the MCP envelope withholds the publisher-text message as `[publisher text withheld on MCP; read it with the om CLI or in om chat]`), `chart_indicator_schema {indicatorType:"@backquant/order-blocks"}` → `kind_retired` with the hint `Call the package_open tool`, and `chart_indicator_add {workspaceId:"ws_x", chartIndex:0, indicatorType:"@backquant/order-blocks"}` → `kind_retired` before any workspace read (without `workspaceId` the guest lane answers `no_active_workspace` first). `package_open {ref:"@om-core/rsi"}` succeeded: `kind: wrun-indicator`, `version 0.3.4`, `chart_url https://openmarket.xyz/chart/?wrunRef=%40om-core%2Frsi%400.3.4`, `wrun_ref`, `resolved_via: search`, no `script_id`; `{ref:"@backquant/order-blocks"}` → `package_deleted`. A default `package_search` returned rows with every `description` withheld. The first `package_search` and `package_open` of one session sat for 30 s (the driver's timeout) and `package_open` then read `tool_failed`; a fresh session answered both in about 250 ms, so that was a registry stall, not the server. `file_create` (`scratch`) wrote `…/accounts/guest/documents/vom-probe-20261101.md`; `channel_default_set {name:"nope"}` → `channel_not_found`; `watch_show {id_or_slug:"nope"}` → `watch_not_found` with no `kind`; `watchlist_list` → `missing_api_key`; `nervous_status` read. Loopback HTTP, the memory round trip and `downloads` were not re-driven. Evidence: `http://127.0.0.1:8098/vom-nightly-20261101/r1/` (`cli/90-mcp-stdio.jsonl`, `cli/90b-*`, `cli/90c-*`, `cli/90-mcp-stdio-tools.json`).*

*Re-driven 2026-10-31 (nightly), tree `dfefe0a21` (origin/main, v0.480.2), lane home 18163 with the daemon down (a guest sign-in 429 kept it from booting; none of these calls needs it). `mcp serve --stdio --no-fire-bridge` answered `initialize` as `openmarket` 0.480.2 and `tools/list` returned **454** tools: `file_create` and `channel_default_set` are new (#2221, #2220), `document_draft` is gone (`Tool document_draft not found`, as the changelog says). `watch_list` read `watches: []`. `file_create` (`scratch`) wrote `…/accounts/guest/documents/vom-probe-20261031.md` and then `(2).md`; `filename:"../escape"` → `invalid_filename`. `channel_default_set {name:"nope"}` → `channel_not_found` (`unknown channel 'nope' — no channels are configured`, hint `details.channels names the configured channels`). `order_place` → `capital_yolo_harness`. **`file_create` with `destination:"downloads"` never answered**: 120 s of silence, and every call queued behind it timed out too, so run it last or not at all (README, known product gaps). Once the lane was up: `points` with `exchanges:["BYBIT_FUTURES"]` plus `rawSymbol` answered `id.exchange: BYBIT` (#2202's alias holds on the MCP schema), `metric_series`/`metric_get` with `selector:{symbol:"BTC"}` carried `listing_note`, `metric_get` with an unknown param → `invalid_query`, `markets {exchanges:["LIGHTER"]}` → `invalid_arguments` with the new `This input cannot address a venue outside the set` sentence, and `watch_show {id_or_slug:"nope"}` → `watch_not_found` with no `kind`. Loopback HTTP and the capital gate's `capital_not_armed` form were not re-driven. Evidence: `http://127.0.0.1:8098/vom-nightly-20261031/r1/` (`cli/90-mcp-pre*`, `cli/91-mcp-downloads*`).*

*Re-driven 2026-10-30 (scheduled maintenance), tree `3cb50a821` (origin/main, v0.478.0), fresh lane on 18165, host load average about 140. `mcp serve --stdio --no-fire-bridge` answered `initialize` as `openmarket` 0.478.0; `tools/list` returned 452 tools including `doc_patch`; `tools/call watch_list` returned `maint-1030`. `watch_show` takes `id_or_slug` (or `group`), not `id`: `{"id":…}` is refused `invalid_arguments` ("pass exactly one of `id_or_slug` … or `group`"). Evidence: `http://127.0.0.1:8098/verify-om-maint-20261030/r1/` (`cli/32-mcp.jsonl`).*
*Re-driven 2026-10-30 (nightly, smoke depth), tree `3cb50a821` (origin/main, v0.478.0), lane on 18163. `mcp serve --stdio --no-fire-bridge` answered `initialize` as `openmarket` 0.478.0. `tools/list` returned **452** tools, one more than before: the new `doc_patch` (#2191). `backtest_spec` was listed. `tools/call watch_list` returned `probe-1030`. `watch_show` with an unknown id returned `isError:true`, and its `structuredContent.data` held only `error: watch_not_found`, `message` and `hint`. The typed `kind` from #1702 is deliberately kept off the MCP payload, so do not assert on it. Loopback HTTP and the capital gate were not re-driven. Evidence is local only (the `8098` renderer did not answer): `artifacts/vom-nightly-20261030/r1/`.*

*Re-driven 2026-10-29 (scheduled maintenance, smoke depth), tree `7ec575e55` (origin/main, v0.467.0 plus #2194), fresh lane on 18161. `mcp serve --stdio --no-fire-bridge` answered `initialize` as `openmarket` 0.467.0. `tools/list` returned 451 tools, and `tools/call watch_list` returned the lane's `lane-probe`. Loopback HTTP was not driven. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261029/r1/`.*

*Re-driven 2026-10-29 (nightly, smoke depth), tree `32ca0d6c7` (origin/main, v0.467.0), lane on 18103: `mcp serve --stdio --no-fire-bridge` answered `initialize` as `openmarket` 0.467.0 with 451 tools and no banner leak. `watch_list` returned the lane's watches, and `order_place` gave `capital_yolo_harness` under this bypass-mode driver. The new registry action `sidebar_layout` is **not** an MCP tool (`Tool sidebar_layout not found`), as its terminal-chat-only scope says. Loopback HTTP was not re-driven. Evidence: `http://127.0.0.1:8098/vom-nightly-20261029/r1/`.*

*Re-driven 2026-10-28 (scheduled maintenance, smoke depth), tree `186030b63` (origin/main): `mcp serve --stdio --no-fire-bridge` answered `initialize` as `openmarket` 0.466.0 and `tools/list` with 451 tools. Loopback HTTP and tool calls were not re-driven. Steps not named here keep the record below. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261028/r1/`.*

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
- **`file_create` over stdio (added 2026-10-31).** `tools/call` `file_create`
  with `{"content":"# probe\n","filename":"vom-probe"}` answers
  `{path, bytes, format:"md", destination:"scratch"}`, the path under the
  lane home's `accounts/guest/documents/`; the same call again takes
  `vom-probe (2).md`; a filename with a separator is refused `invalid_filename`.
  Keep `destination:"downloads"` out of a stdio drive: it answered nothing in
  120 s and the server answered nothing after it either. A driver's
  `proc.kill()` on the wrapper's pid leaves the `exec`'d `bun … mcp serve
  --stdio` child alive with PPID 1 when a call is wedged (it exits on stdin
  EOF only while it is reading); find it by its cwd and kill that pid.
- **`channel_default_set` over stdio (added 2026-10-31).** `{"name":"nope"}`
  on a home with no channels is `isError` with `error: channel_not_found`,
  `details.channels: []`; the happy path needs a paired channel.

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
