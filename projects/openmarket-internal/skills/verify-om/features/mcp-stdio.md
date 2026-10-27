# The capability layer over MCP (stdio)

*Verified: 2026-10-27, tree `8fe6a8432` (origin/main, v0.466.0), lane on 18103: `mcp serve --stdio --no-fire-bridge` answered `initialize` as `openmarket` 0.466.0 with no stdout leak. `tools/list` returned 451 tools including `watch_list` and `order_place`, and `package_search`'s kind enum now includes `agent-plugin`. `watch_list` ran with no error. `order_place` (Hyperliquid, quote 10) was refused, but with **`capital_yolo_harness`, not `capital_not_armed`**, because this nightly session ran under `--permission-mode bypassPermissions` (see Gotchas). Not driven: hosted HTTP, `--catalog operator`, `--session merged`, `om mcp arm` and the fire bridge. Previous stamp `ee8e3a7ab` is an ancestor of this tree (15 commits).*

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
