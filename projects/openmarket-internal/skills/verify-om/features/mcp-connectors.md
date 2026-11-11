# MCP servers the owner connects

*Verified: 2026-11-11, branch `daryl/mcp-client` tree `3e78ff2ffe` (PR #2453, on origin/main `0ad4768f66`), bare lane on 18171 with a scripted fake model on 18172 and fixture MCP servers on 18173 to 18175. Gallery `http://127.0.0.1:8098/mcp-client/r2/` (17 screenshots). Not on main until the PR merges.*

The owner connects an MCP server at the terminal with `om connect add`. The agent lists its tools with `connector_tools` and calls one with `connector_call`. Tool definitions are pinned when the server is added, and a per-connection mode decides when a call asks.

## Sub-features

- `om connect add <name> --url <address>` and `--command <program> -- <args...>` list the server's tools and ask one question that sets the mode. The default is `changes`.
- `--token` and `--header <name>` ask for a secret with the echo off and store it in the vault.
- `om connect login <name>` signs in through the browser. `--paste` takes the address the browser ended on. The verb prints `Signs in at: <host>` and asks when that host is not the server's own.
- `om connect list` shows each connection as `ready`, `needs sign-in`, `needs review` or `unreachable`.
- `om connect set <name> --asks <mode>`. Lowering a mode under an auto-approve harness exits 2. Raising exits 0.
- `om connect review <name>` shows each added or changed tool with the fields that changed, and re-pins on yes.
- `connector_call` under `changes` runs a tool the server marks read only with no card, and paints a four-row card (`CONNECTION`, `TOOL`, `SENDS`, `MODE`) for any other.
- Refusals: `connector_needs_review` after a tool changed, `connector_arguments_too_long_to_show`, `connector_outcome_unknown` after a dropped connection, `connector_unreachable`, `connector_needs_sign_in`.
- The existing `om connect` and `om connect <client>` still wire om into other clients.

## How to get to it (user POV)

1. `om connect add docs --url https://example.com/mcp`, from a real terminal. Answer the question.
2. In `om chat`, ask about that server. The agent lists its tools, then calls one.
3. `om connect list` to see its state.

## Driving it with control-om

- Bare lane as in [persona-chat-tools.md](persona-chat-tools.md). Export `OM_LANE_PORT` on every `control-om om --` call.
- The `om connect` verbs need a real terminal. Run them in tmux on your own named socket with a scratch `OM_HOME`.
- Fixture servers are built with the SDK's own server classes. The test fixtures are `packages/cli/test/_connector-fixture-server.ts` and `_connector-fixture-auth.ts`. Run copies on loopback ports for the lane.
- Command arguments need `--` before them on `add`.
- The sign-in flow is proven against the fixture authorization server by the paste path, with a `curl` request standing in for the browser.
- To show `connector_outcome_unknown`, have the fixture close the connection after it acts, and read the fixture's own log for the call count.
- To show a pin catching a relabel, flip a tool's read-only label on the fixture, call it, then run `om connect review`.
- In chat the lane's own argument cap sits below the card's limit, so the too-long refusal is reached with hidden characters that grow when escaped.
- The secret grep covers the lane home including database bytes, the lane log, the evidence text and the fixture logs. Use a positive control that finds each token in the issuer's own file.

### What to check

- The settings row holds no secret after an add with `--token`.
- The fixture's log shows exactly one call after a dropped connection.
- The card's `SENDS` row shows the whole arguments.
- `om connect` with no verb still reaches the integrations command.

## Gotchas

- A real provider's browser sign-in has not been driven. It needs an account.
- An unattended watch calling a connector is unit-tested only.
- Windows and Linux for the stdio path have not been driven.
- The SDK at 1.32.0 does not check the authorization server's issuer and does not speak the 2026-07-28 protocol revision.
- The CLI closes a connection's pooled client only in its own process. A running chat keeps its client for up to 5 minutes idle.
- One real server (Context7) was listed and called in round one only. Round two used fixtures alone.
