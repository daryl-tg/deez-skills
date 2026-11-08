# The capability layer over MCP (stdio)

*Re-driven 2026-11-09 (nightly), tree `5bfa0ccf6` (origin/main, v0.492.0), guest lane on 18143, booted with no guest 429. `initialize` (`openmarket` 0.492.0), `tools/list` **484**, `watch_list`, `order_place` `capital_yolo_harness` (the driver ran under an auto-approve harness), `todo_get`/`todo_list`/`todo_similar` `not_badge_bound`, zero stdout leaks; first live proof of a locally minted badge (#2411): 57 tools, `todo_list` and `todo_similar` `read_not_granted`. Not re-driven: `file_create`, `channel_default_set`, the HTTP transport. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261109/r1/` (`cli/80`, `cli/81`).*

*Re-driven 2026-11-08 (nightly), tree `5590b4d1c` (origin/main, v0.492.0), guest lane on 18141, booted in 2 s with no guest 429. `initialize` (`openmarket` 0.492.0), `tools/list` **484** (with `watch_list`, `todo_get`, `watch_archive`), `watch_list`, `order_place` `capital_yolo_harness` (the driver ran under an auto-approve harness), `todo_get` `not_badge_bound`. Not re-driven: `file_create`, `channel_default_set`, the stale-version warning, HTTP. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261108/r1/` (`cli/40-mcp-stdio.jsonl`).*

*Re-driven 2026-11-07 (nightly), tree `05f450fc5` (origin/main, v0.492.0), guest lane on 18141, booted with no guest 429; one Python driver over `control-om om -- mcp serve --stdio --no-fire-bridge`, no non-JSON line on stdout. `serverInfo` `openmarket` 0.492.0; `tools/list` **484** (unchanged), and the `markets` and `points` input schemas now carry `cursor` (#2330, #2389). Calls: `watch_list`, `markets {symbolFilter:"BTC", pageSize:3}` (whole answer, no `page`), `order_place {venue:"hyperliquid", asset:"BTC", side:"buy", size:{mode:"quote", value:11}}` `capital_yolo_harness`, `todo_list {spaceId:"openmarket"}` `not_badge_bound`. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261107/r1/` (`cli/90-91`).*

*Re-driven 2026-11-06 (nightly), tree `50fcc594b` (origin/main, v0.492.0), guest lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), booted at 19:18Z with no guest 429, host load average 10 falling to about 3.3; one Python driver over `control-om om -- mcp serve --stdio --no-fire-bridge`, no non-JSON line on stdout. `serverInfo` `openmarket` 0.492.0; `tools/list` **484**: the eleven new `todo_*` tools (`todo_create`, `todo_update`, `todo_comment`, `todo_follow`, `todo_similar`, `todo_delete`, `todo_label_list|create|rename|merge|delete`) and `watch_archive`/`watch_unarchive`; `agent_status_*` are not listed. Calls: `watch_list`, `order_place` `capital_yolo_harness` (bypass permissions), `todo_list` and `todo_create` `not_badge_bound`, `watch_unarchive {id:"probe-quiet"}` `enabled:false`. Not re-driven: loopback HTTP MCP, `file_create`, `channel_default_set`. Evidence: `http://127.0.0.1:8098/vom-nightly-20261106/r1/` (`cli/mcp-stdio.jsonl`).*

*Re-driven 2026-11-05 (nightly), tree `3a0ea623e` (origin/main, v0.492.0), guest lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), booted in 2 s at 19:19Z with no guest 429, host load average about 4.4; one Python driver per session over `control-om om -- mcp serve --stdio`. `tools/list` **471** (the eight new `agent_*` tools: `agent_create`, `agent_fit`, `agent_tools`, `agent_tune`, `agent_tune_apply`, `agent_init`, `agent_try`, `agent_eval`), `coins`, `package_open` (publisher text withheld), `watch_state_clear {id}` `cleared:true`, `agent_list`, `session_grants` `not_badge_bound`; `order_place` with a malformed `size` `invalid_arguments`, and with valid arguments `capital_yolo_harness` because this nightly session runs under bypass permissions. Not re-driven: loopback HTTP MCP, `file_create`, `channel_default_set`. Evidence: `http://127.0.0.1:8098/vom-nightly-20261105/r1/` (`cli/mcp-guest.json`, `cli/mcp-capital.json`).*

*Re-driven 2026-11-04 (nightly), tree `9acb5fb56` (origin/main, v0.491.0), guest lane on 18163, booted in 2 s with no 429. Two `mcp serve --stdio --no-fire-bridge` sessions through the wrapper, no non-JSON line on stdout: `serverInfo` `openmarket` 0.491.0, **463** tools (455 at `777ee7f21`; new: `agent_list`, `agent_runs`, `agent_run`, `agent_run_cancel`, `agent_configure`, `agent_portrait`, `todo_list`, `todo_get`; `firecrawl_offers_pause`/`resume` are not listed). Calls: `watch_list` (the lane's watches), `order_place` `capital_yolo_harness` (the driver ran under `bypassPermissions`), `agent_list` (six agents), `agent_runs` (the failed watch-door run), `agent_run {agent:"zzz"}` `not_found` with `Installed: …`, `agent_configure {set:{kind}}` `plugin_owned:kind`, `todo_get` `not_badge_bound`, `persona_show` (`mcpOperatorVoice: "off"`), `package_open {ref:"@om-core/rsi"}` answered `wrun-indicator` 0.3.4 with the publisher text withheld (the 2026-11-03 `tool_failed` did not recur), `package_search {kind:"kscript-indicator"}` `kind_retired`, `watch_state_clear {id}` `cleared:true`. Not re-driven: `file_create`, `channel_default_set`, the stale-version warning, loopback HTTP. Evidence: `http://127.0.0.1:8098/vom-nightly-20261104/r1/` (`cli/110-mcp.json`, `cli/111-mcp2.json`).*

*Re-driven 2026-11-03 (nightly), tree `777ee7f21` (origin/main, v0.488.0), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 2.8; the first `up` died on a guest sign-in 429 (35 minutes) and the lane booted in 3 s at 19:55Z. `mcp serve --stdio --no-fire-bridge` answered `openmarket` 0.488.0 and **455** tools (one more: `persona_show`; `persona_infer` and `persona_set` are not offered), no stdout leak, with the daemon down and again after the boot. Calls: `config_show` (`mcp_operator_voice: "on"`), `persona_show`, `session_grants` `not_badge_bound`, `persona_set` `Tool … not found`, `watch_list`, `order_place` `capital_yolo_harness`, `points` (Polymarket slug) `invalid_query`, `markets {symbolFilter:"GOLD"}` with the HIP-3 row, `package_search` kScript `kind_retired`, `channel_default_set nope` `channel_not_found`, `watch_state_clear {id:"demo"}` `not_a_condition_watch`, `series_publish {name, price:"9/mo", dry_run}` `capital_yolo_harness`; `package_open @om-core/rsi` `tool_failed` after 30 s in two sessions. Loopback HTTP was not re-driven. Evidence: `http://127.0.0.1:8098/vom-nightly-20261103/r1/` (`cli/30-32-mcp-*.json`).*

*Re-driven 2026-11-02 (scheduled maintenance), tree `587ce2d0b` (origin/main, v0.480.3), lane on 18168 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 5. `mcp serve --stdio --no-fire-bridge`: `serverInfo` `openmarket` 0.480.3, 454 tools including `watch_list` and `config_key_info`, `watch_list` with no `isError`, `order_place` → `isError` `capital_yolo_harness` (this session runs under `bypassPermissions`), and zero non-JSON stdout lines. The stale-version warning was not re-driven on main.*

*Re-driven 2026-11-02 (nightly), tree `2567b7974` (origin/main, v0.480.3), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 4. With the daemon still down (the 429 window), `mcp serve --stdio --no-fire-bridge` answered `initialize` as `openmarket` 0.480.3 and `tools/list` 454 tools with no stdout leak; `series_publish` now takes `price`, `stop_sales`, `resume_sales` and `free` beside `dry_run`, `registry`, `yes` and `effects_approved`, and the `series_publish` and `watch_state_clear` descriptions changed (#2240, #2244). After the boot, thirteen `tools/call`s on one session: `watch_list` (4 watches), `order_place` `capital_yolo_harness` (bypass mode), `file_create` scratch → `vom-probe.md` then `vom-probe (2).md`, `a/b` → `invalid_filename`, `channel_default_set nope` → `channel_not_found`, `watchlist_list` → `missing_api_key`, `nervous_status` read, `package_search` kScript → `kind_retired` (text withheld), `chart_indicator_schema @backquant/order-blocks` → `kind_retired`, `package_open @om-core/rsi` → `wrun-indicator` 0.3.4, **`series_publish {price:"9/mo", dry_run:true}` → `capital_yolo_harness` ("series_publish moves capital": selling a feed is capital-gated over MCP)**, `watch_state_clear demo` → `not_a_condition_watch`. Over loopback HTTP on 18165: `initialize` answered a bare JSON body (`Content-Type: application/json`, no `mcp-session-id`), `notifications/initialized` 202, `tools/list` **444** tools (stdio 454), `GET /mcp` 405, another path 404; killing the wrapper left the `bun … mcp serve --http` child on the port (killed by pid). Evidence: `http://127.0.0.1:8098/vom-nightly-20261102/r1/` (`cli/20-mcp-tools-list.json`, `cli/210-mcp-calls.json`, `cli/230-231`).*

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
- `mcp-version-warning` (PR #2231, on main since `3498391e7`; not re-driven on main): when the servant's om version and the daemon's `/healthz` version differ, the fire bridge sends one `notifications/message` (`logger` `openmarket.servant`, `level` `warning`) per daemon version and writes the same line to stderr. Older servant: `om MCP servant 0.478.0 is older than the daemon 0.480.2. Restart this Claude Code session to upgrade.` Older daemon: `Daemon 0.478.0 is older than this MCP servant 0.480.2. Restart it to catch up.` The servant never exits on its own.
- Hosted MCP over loopback HTTP (`om mcp serve --http 127.0.0.1:<port>`): the same capability layer on `POST /mcp`, unauthenticated on loopback unless `OM_LOOPBACK_AUTH=1`.
- `mcp-operator-voice` (PR #2250, on main since `6b8a48c05`, v0.487.0): with `om config set mcp.operator_voice on` (default off) and a stored `om persona`, a badge session's `initialize` instructions end with `Operator's voice (room_draft_stage and room_post_as_operator text only; never room_post or replies to the operator):` and the persona digest. `session_grants` returns `operatorVoice`, `config_show` returns `mcp_operator_voice`, and `om persona show` ends with an `MCP clients:` row. No agent or MCP tool sets the key.

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

### Badge ticket reads over stdio (added 2026-11-09, #2411)

A locally minted badge reaches the grant check with no rooms account, because the gate answers before any network call.

```bash
control-om om -- agent credentials create vom-badge --format json   # the result's `secret` is shown once
OM_AGENT_SECRET=<secret> control-om om -- mcp serve --stdio --no-fire-bridge
```

Keep the secret in a shell variable and out of the artifact directory: the create result holds it in clear, and `evidence publish` copies the directory wholesale.

- `initialize` carries the badge brief; its ticket line reads `Tickets (Projects): todo_get, todo_list and todo_similar ride READ on the ticket's SPACE`.
- `tools/list` is the badge catalog: **57** tools, no `watch_list`.
- `tools/call` `todo_list {"spaceId":"vom-space"}` and `todo_similar {"spaceId":"vom-space","title":"x"}` are each `isError` with `read_not_granted`, message `no active read grant for space "vom-space"`, hint `Request access with room_grant_request (resources: [{kind: "space", resource: "vom-space"}])`. Room grants alone no longer list a server's tickets.
- Without a badge the same two calls answer `not_badge_bound`.
- A granted space then reaches the relay, and needs a real account or a stub through `OM_ROOM_CHAT_API_URL`; a badge session rejects a `url`/`apiUrl` input (`badge_url_override_rejected`). `todo_get` on a ticket in a server the badge does not read answers `todo_not_found`. Neither branch is driven here.

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
- Account-only tools refuse before any request. `watchlist_list` gives `missing_api_key` ("guest keys have no workspaces"). An `exchange_id` outside the domain (35 values then, 38 at v0.491.0) is refused at schema validation even when `om exchanges` lists it (see [market data](./market-data-reads.md)).

**Teardown trap:** killing the backgrounded `control-om om --` pid leaves its `bun packages/cli/src/bootstrap.ts mcp serve --http …` child running with PPID 1, still holding the port. Check `lsof -nP -iTCP:<port> -sTCP:LISTEN` and kill that child by pid.

### Stale-version warning over stdio (added 2026-10-31, PR #2231, on main since `3498391e7`)

Needs a servant and a daemon on different om versions. The cheapest pair is a branch build of the servant against the installed daemon on another version; the servant only reads `/healthz` and `/events/v1`, so pointing it at the operator's daemon on `31337` is read-only. A `--session merged` servant needs the badge from a live servant's environment (`ps -E -o command= -p <servant pid> | tr ' ' '\n' | grep '^OM_AGENT_SECRET='`), passed through `env`, never printed.

```bash
( printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"driver","version":"0"}}}' '{"jsonrpc":"2.0","method":"notifications/initialized"}'; sleep 20 ) \
  | env "$SECRET_KV" packages/cli/dist/om mcp serve --stdio --session merged > out.jsonl 2> err.log
grep notifications/message out.jsonl
```

Driven 2026-10-30: a 0.480.2 branch servant against the 0.478.0 daemon answered `initialize` and, within the 20 s window, emitted exactly one `{"method":"notifications/message","params":{"level":"warning","logger":"openmarket.servant","data":"Daemon 0.478.0 is older than this MCP servant 0.480.2. Restart it to catch up."}}` with the same text on stderr. Equal versions emit nothing (driven with the installed servant and daemon both on 0.478.0). The servant-older wording is pinned by `packages/cli/test/mcp-sse-bridge.test.ts` and was not driven live.

### Operator voice in the badge brief (added 2026-11-02, PR #2250, on main since `6b8a48c05`)

Needs a badge session (`--session merged` or a badge stdio servant) against a home with a stored persona. On a lane, store one with `control-om om -- persona set "voice: terse"` and flip the key with `control-om om -- config set mcp.operator_voice on`; the operator's own home works read-only for the off state.

- **Off (default).** `initialize` instructions carry no `Operator's voice` line; `tools/call session_grants` text payload has `"operatorVoice": "off"`; `om config show --format json` has `"mcp_operator_voice": "off"`; `om persona show` ends `MCP clients: off (om config set mcp.operator_voice on)`.
- **On.** The instructions' last two lines are the scope line and the stored digest; `session_grants` gives `"on"`; `om persona show` ends `MCP clients: write as you (om config set mcp.operator_voice off)`. On with no stored persona: no block, and `om persona show` says `nothing sent until a persona is stored`.
- **On a guest lane, no badge (driven 2026-11-03 at `777ee7f21`).** With a stored persona and the key `on`: `config_show` → `"mcp_operator_voice": "on"`; `persona_show` (listed over MCP since #2256) → `"mcpOperatorVoice": "on"`; `session_grants` → `isError` `not_badge_bound` (the session presents no agent badge), so the brief itself cannot be read there. The CLI's `om persona show --json` spells the same fact as a boolean, `"mcpOperatorVoice": true`. The badge brief was not re-driven on main.
- **Reading the result.** `session_grants`' `structuredContent` wraps the payload under `data`; parse `content[0].text` for the field.
- Driven 2026-11-02 on the branch (`d779717eb`..`0775fc2da`, source `bun packages/cli/src/main.ts`) against the operator's home and badge from `~/.claude.json` (`mcpServers.openmarket.env`, never printed): off brief byte-identical to the installed 0.480.3 (3661 chars), on brief 6440 chars ending with the dboon333 digest, `session_grants` `operatorVoice: "off"`, `config_show` `mcp_operator_voice: "off"`. The switch was flipped on and back to an explicit `off` for the on-state check. Evidence (local): `~/dev-notes-artifacts/om-mcp-operator-voice/run-artifacts/instructions-*.txt`, `handshake.ts`, `session-grants-call.ts`. Not driven: a live client writing a draft in the voice.

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
