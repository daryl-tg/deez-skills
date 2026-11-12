# Assistant bridge: daemon tools, deposit and wakes through the hosted MCP

*Re-driven 2026-11-09 (scheduled maintenance), tree `0d3d29cd27` (origin/main, v0.493.0), bare lane on 18145 (dummy `OM_API_KEY`, dead service URLs) with a scripted fake model on 18144. On main for the first time: `om assistants` prints `Assistants are off on this daemon. Turn them on with \`om assistants on\`.` and `No assistant has asked yet. Connect one to OpenMarket's MCP server and its first call asks here.`; `--format json` `{"assistants":[]}`; `--help` lists `list`, `on`, `off`, `allow`, `wake` (and the rest); MCP stdio lists `assistant_list` (485 tools) and answers `{assistants:[]}`. Not re-driven on main: the hosted forward, `deposit`, subscribe and signed wakes, which need the hosted binary, Mongo and a relay stand-in. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261109/r1/`.*

*Verified: 2026-11-05 on the unmerged stack #2350, #2352, #2365, #2367, #2378 (top `daryl/assistant-stack-review-fixes`, base main `c1464fcf0`). Status read 2026-11-09: still open, with #2385 (`daryl/assistant-run-improvements`) now stacked on #2378; #2385 is not driven here. Merged since: #2350 as `5dfe76ff38` and #2352 as `bfad02ca24`, released in v0.493.0 (see the record above). Every step below was driven on real local processes with a relay stand-in. A real assistant (Grok Bot) was driven on 2026-11-06 through a temporary tunnel, with a routine webhook as the wake. Pending: an OAuth sign-in from a real assistant, MCP Events from a real vendor, and the production relay with a daemon from this stack.*

An AI assistant connected to the hosted MCP service calls 23 tools on the user's own daemon and a `deposit` tool, and can subscribe to `watch.update` so the daemon posts it a signed webhook. The hosted service forwards over the relay as the operations `mcp.call` and `mcp.events`. The daemon gates it with `om assistants on` and one approval per assistant.

## Sub-features

- `list`: on a host of the om surface `tools/list` adds the daemon tools; root and charts hosts do not. `/directory` there lists them with no trade tool; `/chatgpt` is the chart listing on every host.
- `off`: with the setting off a daemon call answers `daemon_assistants_off` naming the device.
- `ask`: the first call waits 20 s and answers `daemon_asks_you`; `om assistants` shows `asks you` and `om approve <id>`.
- `call`: after approval a call returns the daemon's answer; a second call sends no hello (the device is remembered).
- `deposit`: one journal row in `assistant-inbox-<hash>`; the same `id` answers `deduped: true`.
- `refusals`: `shape_not_served` (arguments above the tool's tier), tool not found for anything off the list, `rate_limited` past the call rate, `daemon_too_old` for a daemon without `assistants.v1`.
- `wake`: `events/subscribe` sends one signed verification challenge, then one delivery per matching row; the subscriber's own inbox never wakes it; at most 10 a minute and 60 an hour per wake.
- `operator view`: `om assistants` rows, `Wake: <watch> to <host>, sent 3m ago, N skipped this hour`, `revoke`, `off`.

## Driving it

Ports from the agent range, all on 127.0.0.1: relay stand-in 18121, receiver 18122, hosted binary 18119, Mongo 18117, lane 18150. Stop each after the run.

1. Mongo as in [hosted-chart-mcp-tenant-state.md](hosted-chart-mcp-tenant-state.md), a run-owned container on 18117.
2. A relay stand-in. The real relay needs a signed-in daemon, and a lane with a dummy key cannot sign in. The stand-in authenticates anything, routes `AGENT_CONTROL_REQUEST` to the daemon socket and carries emits back. The one used on 2026-11-05 is `~/dev-notes-artifacts/om-assistant-broker/run-artifacts/loop-2/e2e/local-relay.ts` (local artifact, not in the hub).
3. Hosted binary from the branch: `bun run --cwd packages/cli build:chart-mcp`, then boot with `OM_HOSTED_CHARTS_URL=https://charts.mcp.openmarket.xyz OM_HOSTED_OM_URL=https://om.mcp.openmarket.xyz OM_HOSTED_RELAY_URL=ws://127.0.0.1:18121` beside the usual bind, port, home and Mongo variables. Requests pick the host with `Host` and `X-Forwarded-Host` headers, so no DNS is needed.
4. Lane daemon from the branch, run from the worktree with `OM_LANE_PORT=18150` exported: `control-om up --port 18150 --env OM_API_KEY=om_dummy_proto --env OM_ROOMS_WS_URL=ws://127.0.0.1:18121` plus dead URLs (`http://127.0.0.1:9`) for `OM_BASE_URL`, `OM_AUTH_BASE_URL`, `OM_COLLAB_REST_URL`, `OM_COLLAB_WS_URL`, `OM_ROOM_CHAT_API_URL`, `OM_ALERT_TOPICS_URL`, and `--env OM_ASSISTANT_WAKE_ALLOW_LOOPBACK=1` for a loopback receiver.
5. A caller key. The hosted verifier checks the key against the production gateway, so the drive reads the operator's stored key through `resolveApiKeyWithSource` and never prints it. A stored device key has no scope claim and lists 37 hosted tools.
6. Walk: `control-om om -- assistants` (off row), `assistants on`, a `watch_list` call (asks), `approve <id>`, the call again, `deposit`, `events/subscribe` with a `whsec_` secret and the receiver's URL, then commit a row with `control-om om -- event push <another assistant's inbox> --text ...`.
7. A receiver that verifies each request itself: HMAC-SHA256 over `webhook-id.webhook-timestamp.body`, key = base64 of the secret after `whsec_`; it answers `{"type":"verification"}` with `{challenge}`.

## What to expect

- A daemon call takes tens of milliseconds on the rig once the device is remembered.
- A delivery arrives about 1 s after the row is accepted (the ingest pipeline is asynchronous).
- 13 rows in under a minute give 10 deliveries and `3 skipped this hour`.
- After `assistants revoke <asst_ id>` no further delivery arrives.

## Driving it with a real assistant: Grok Bot (2026-11-06)

*Driven on the top of the stack with a throwaway key, a stand-in gateway and a scratch lane daemon. No real credential was used.*

- A stand-in gateway replaces the production key check, so a made-up key works: a small server that answers `GET /collab-v2/workspaces` with `[]` and the header `x-om-key-label` for one JWT-shaped key (`alg: none`, claims `jti`, `sub`, `scope`), and 401 otherwise. Point the hosted binary at it with `OM_COLLAB_REST_URL` and `OM_COLLAB_WS_URL`. Chart tools then do nothing useful; daemon tools, deposit and events work.
- Serve the om surface on a plain local address with `OM_HOSTED_PUBLIC_URL=http://127.0.0.1:18119 OM_HOSTED_ROOT_SURFACE=om`. No charts or om host is needed.
- Grok Bot's MCP connector dials from xAI's cloud and cannot reach loopback. Two ways to test: the Bot runs curl against `http://127.0.0.1:18119/mcp` through its local command tool, or a temporary public tunnel (`cloudflared tunnel --url http://127.0.0.1:18119`, which needs the operator's say-so) and the Bot adds the server by URL with the `Authorization: Bearer` header when asked in chat.
- The connector reports its client as `Cursor/1.0.0`. The label the daemon shows comes from the key's label.
- Wake for Grok Bot is not MCP Events. Ask the Bot for a routine with a webhook trigger, read the trigger URL and key from the routine panel, then on the daemon `om setup webhook --webhook-url <url> --bearer-token <key> --name <name>` and a watch whose `notify.channels` names that channel. The setup's own test message already runs the routine once.
- A watch that fires without a model on a bare lane: import a spec with an `inbound` source and `classifier: { mode: "accept_all" }` through `om watch import <file>`, then `om event push <id> --text ...`. `om watch create --inbound` defaults to a model classifier, and an `--every 2m` timer watch never fired on the bare lane.
- Seen: row to the Bot's deposit landing back in its inbox took about 14 s.
- Drive the Bot app as the memory note on Grok Bot automation says, with a session name of your own.

## Operator-added bearer wakes, the instant ask and the bare handshake (2026-11-06)

*Driven on PR #2385 (branch `daryl/assistant-run-improvements`, `be779eb0c`) on the same loopback rig, and again on 2026-11-09 after the stack was rebased onto main as two PRs, #2350 and #2352 (branch `daryl/assistant-daemon-bridge`, `b41a2afc2`). Not merged.*

- First call from a new or revoked assistant: `om assistants revoke <name>`, then one `tools/call`. Expect an answer in tens of milliseconds whose message carries `om approve appr_...`. Seen: 17 ms and 28 ms.
- A bare handshake: POST `initialize` with no `clientInfo`, or with a name and no version. Expect `serverInfo` and no `-32603`.
- Tool list size on the om surface at full scope: 195,000 bytes, 83 tools, `watch_history` 4,369 characters. `packages/cli/test/hosted-daemon-listing-size.test.ts` pins the daemon listings.
- A bearer wake: start a receiver that checks `Authorization: Bearer <key>`, then `om assistants wake "<label>" --url <url> [--watch <ref>]` with the key piped on stdin (the prompt goes to stderr). Push one row with `om event push`. Expect one POST with the key, `webhook-id` and `webhook-timestamp`, and no `webhook-signature`.
- `om assistants` shows `Wake: <watch> to <host>, added by you, sent just now`. `om assistants unwake "<label>"` answers `Removed 1 wake for <label>.` and the next row is not delivered.
- Running `wake` again for the same address keeps one wake and replaces its key and watch.
- The command refuses, before the key prompt and with no row written: plain http, `https://localhost`, a private address, a host that does not resolve.
- On a rig the command itself needs `OM_ASSISTANT_WAKE_ALLOW_LOOPBACK=1` in its own environment to accept `http://127.0.0.1`, as well as the daemon. `control-om om --` passes the shell's environment through.
- Pending proof: a table of the earlier shape being rebuilt on open is covered by a test, not by a live drive. Delivery to a real vendor routine URL with this sender was not driven.

- Since the 2026-11-09 rebase the ask is an approval ledger row: ids are `apr_`, `om approvals list` shows it as `mcp assistant_allow`, and `om approve <id>` admits the next call. The row also fans out as a card to paired messenger DMs and the GUI.

## Live host, driven with Grok Bot as the user (2026-11-10)

*Driven on the deployed internal host `https://om.mcp.openmarket.xyz` (WARP only), production gateway and relay, the operator's live daemon on om 0.493.0.*

- The host is reachable only over WARP. A vendor's cloud connector cannot dial it; a Bot on this Mac reaches it with curl through its local command tool.
- To keep the key out of the Bot: a loopback forwarder (`run-artifacts/live-grok/forwarder.ts`) resolves the stored key through `resolveApiKeyWithSource` and adds the header. The Bot posts plain JSON-RPC to `http://127.0.0.1:18119/mcp`. Stop it when done; it is an unauthenticated door while up.
- Journey that passed: `initialize`, `tools/list` (61 tools on a legacy-scope key), `watch_list` answers `daemon_assistants_off`; `om assistants on`; `watch_list` answers `daemon_asks_you` with `om approve apr_...`; approve; `watch_list` returns the real watches; `watch_history`; `deposit` lands in `assistant-inbox-<hash>`; `watch_mute` and `watch_unmute` on that inbox; asks for a new watch and an order are declined by the model because no such tool is listed.
- Sign-in discovery on the live host: the 401 names `/.well-known/oauth-protected-resource/mcp`; the resource is `https://om.mcp.openmarket.xyz/`; the authorization server document is served by the om host with endpoints at `openmarket.xyz/api/v1/oauth`; dynamic registration of a public client answers 201.
- Seen: `watch_list` on a home with 94 watches answered 1.43 MB in about 5 s. The ask shows the key's label, and a CLI key reads `om <device>`. `om keys create` refuses when the stored key was itself minted.
- Pending proof: an OAuth-minted token through the relay to the daemon, and identity across a token refresh. Both need the operator's browser consent.

## Carded writes through `request_change` (on main since #2449, `92873997bb`, 2026-11-11)

*Driven on a rig of the hosted binary, the stand-in gateway and relay, and a lane daemon on 18150 with a fake model and a webhook channel: the four separate tools on 2026-11-10, the folded tool on 2026-11-11 at `baf9897c05`.*

- `one tool`: the four writes are one hosted tool, `request_change`, with `action` `create_watch`, `edit_watch`, `start_watch` or `plot_inbox`. The old names `watch_create`, `watch_edit`, `watch_arm` and `plot_inbox` answer tool not found. A missing, unknown or wrong-typed `action` answers `invalid_input` with no card; a field of another action answers as an unknown key.

- `carded call`: each action answers `daemon_asks_you` with an `apr_` id and both commands; the same call before the yes names the same card; after `om approve` the same call returns the result once, then asks afresh.
- `read the card`: `om approvals show <id>` prints the headline, `ASSISTANT`, the facts (`NAME`, `SOURCE`, `AI STEP`, `NOTIFIES`), the question and the expiry. `om approvals` alone prints usage; the list is `om approvals list`.
- `refused before any card`: a script condition as an object, a JSON string or nested; a money or tool step; a consent field (`yes`, `authorization`, `chart`, `effects_approved`); a feed that is not https; a `not` rule; an unknown key; a filter on a watch that keeps every row. Each leaves `om approvals list` empty and stores nothing.
- `edit and start guards`: a paused watch is refused on start, and a watch paused between the card and the yes stays paused (the approved row fails with the same sentence). Money and script watches, tooled, owner-off, repair-marked and package-owned steps are unit-test proof only.
- `cap and decline`: a fourth open card answers `daemon_busy`; `om deny` answers `daemon_declined` on the next call.
- `the loop`: create over `inbox: true` with an `ai` step, yes, start, yes, then a `deposit` runs the step on the fake model and posts to the channel receiver.
- `compact listing`: `watching_overview` rows carry `next_fire_at`; forty watches stay under 30,000 bytes (unit test), 84 tools and a 198,469 byte `tools/list` on the full face.
- `deposit then plot`: a plot asked right after a deposit waits about one second for the row; a number never deposited is refused after three.

Recipe, from the worktree with `OM_LANE_PORT=18150` exported and the rig Bun first on PATH (scripts under `run-artifacts/assistant-loops/` of the `om-assistant-broker` task):

- `rig.sh up build` with `RIG_LANE_ENV` carrying the fake model's three `OPENMARKET_LLM_*` values; `fake-model.ts` on 18127 and `channel-receiver.ts` on 18129 first.
- `lane-setup.sh` adds the `desk` webhook channel as default, turns assistants on and approves the connection.
- `call.ts <tool> '<json>'` is one hosted `tools/call`; `SHOW=full` prints the whole answer. Capture the `apr_` id from the full answer, not a clipped one.
- `eval/run-scenarios.ts A B C D E` drives Claude Code headless as the assistant and approves cards as the owner; `eval/scorecard.py run` tabulates it.

Pending proof:

- The plot itself: the lane has no chart without a signed-in account (`no_active_workspace`). Needs a signed-in daemon.
- A money chain refused on start: no venue on the rig.
- The hosted chart, alert and watchlist tools answer `not_found` on this rig (the stand-in gateway returns 404), so a scenario that needs them says nothing about the product.

## Search, then call: ten listed tools and a catalog (on main since #2470, `1107bf7c86`, 2026-11-12)

*Driven on the same rig on 2026-11-12 across the branch's builds `a9478edd5`, `75692ba64` and `aa47768b05` (the PR commit `a47cd995ea` is those rebased onto main): the listings, `find`, `describe`, `read`, `change`, the money-reach refusals, the checks at the yes and the name check on create. Sixty real-client runs (Claude Code headless, Sonnet and Haiku) on the build before the review fixes, sixty on `75692ba64`.*

- `the list`: the om face (root and `/directory`) lists ten tools: `find`, `describe`, `read`, `change`, `deposit`, `watching_overview`, `watch_history`, `watch_show`, `memory_search`, `news_brief`. 12,827 bytes. `/chatgpt` and every charts host list what they listed (51 tools, 156,612 bytes on the rig key). A direct call to any other name answers tool not found.
- `find`: `query` words return eight matches from the daemon and the hosted side merged; no arguments list the categories; `category` lists one. Each match has a `kind`: `read`, `change` or `terminal`.
- `describe`: answers `summary`, `args` (the schema) and, for a `terminal` action, `command` and `flags` (`<command> --help`). The six listed tools and the four catalog tools themselves are described with a `call` field saying to call them by their own name.
- `read`: runs a `free` read. A change, a `terminal` or a listed tool named to it is refused with the call to make.
- `change`: a free change (`watch_pause`, `watch_mute`, `watch_unmute`) runs at once; a `card` action answers `daemon_asks_you`; the four narrow names `create_watch`, `edit_watch`, `start_watch`, `plot_inbox` are their #2449 doors. A hosted chart, alert or watchlist change runs at once under its scope.
- `the generic card`: `om approvals show` prints `ASSISTANT`, `DOES` (the action's summary), one row per argument, a watch named with its label (`IDS: plain-two (Plain two)`), `POLLS` with paid kinds marked on `watch_run_now`.
- `reaches money`: a watch a money watch reads through any number of other watches is refused before any card on pause (by id, by slug, and by slug inside `ids`), a generic card, `edit_watch`, `start_watch`, and `deposit` into an inbox in that chain. An unreadable watch file, or a record under `<home>/series/` that cannot be parsed, refuses the same calls for every watch and is named in the refusal.
- `a new watch's name`: `create_watch` under a name a money watch already reads (a dangling upstream id, a series ref such as `watch/signal/...`) is refused before any card and nothing is stored, not even the assistant's inbox. A free name opens its card.
- `the yes checks again`: a card approved after its watch gained a money reader, or after its rows changed (a rename, a new paid source), fails with one sentence and no handler runs; the assistant's next identical call reads the sentence once.
- `one card per assistant`: the asker is in the card's key. Unit-test proof only; the rig has one credential.
- `wrong keys`: `arguments` in place of `args`, `watch`, `slug` or `id` in place of `id_or_slug`, `q` or `action` on the catalog tools, or a missing `name`, is refused with the keys the tool takes.
- `reach table`: `packages/cli/src/mcp/assistant-reach.ts`, one decision per action; `bun packages/cli/scripts/report-assistant-reach.ts` prints the counts and fails on an undecided action. A new action on main needs its row before the branch's gate passes (seen with `desk_brief` at the rebase).

Recipe additions (same scripts):

- Seed a money chain by writing watch files into the lane home, `<worktree>/.control-om/home-18150/accounts/guest/watches/<id>.json`: copy a stored watch, give it an `upstream` source (`source_id` is `src_` plus 12 hex) naming the watch to read, and one `money` step. `om watch list` shows a file it cannot read as broken, which itself trips the fail-closed guard.
- A money watch with an `upstream` source naming a watch id that does not exist is a valid file (`om watch list` reads `the watch it reads from is gone`) and is the quickest state for the name check: `create_watch {label: "old feed"}` against a dangling `old-feed`.
- A watch whose id differs from its slug has to be written as a file; `om watch create` gives both the same value. The slug-inside-`ids` case needs one.
- `eval/run-scenarios.ts A B C E F G H K L M` with `SCENARIO_FILE=scenarios-all.json`; `python3 eval/tabulate.py <set>` prints medians and each run's call sequence.
- The list's inline token cost: one trivial headless prompt with `ENABLE_TOOL_SEARCH=false`, with and without the server, same sitting (the baseline moves with the client).

Live, 2026-11-12 (hosted `om.mcp.openmarket.xyz` at 0.495.0, image `91-9945cdce`, against the owner's upgraded daemon; the stored key through the product resolver, which is test scaffolding and proves no sign-in):

- `the list`, `find`, `describe`, `read` and the refusals answered as on the rig. Chart-side actions ran through `read` for the first time on real services (`chart_list`, `skill_read`).
- `reaches money`: `watch_archive`, `watch_run_now` and `edit_watch` on two real money watches were refused with no card.
- `change`: `create_watch` raised its card, the owner approved, the handler ran and its failure (`watch_feed_url_gone`) was handed back once.
- `skew`: the hosted build from before #2470 reached the upgraded daemon by `request_change`.
- `chart MCP unchanged`: `/chatgpt` on the old image and on the new image gave the same instructions and tool list, hash for hash, with the same key.
- A real client (Claude Code headless, read-only) answered the agents and cost asks through `find`, `describe` and `read`.

Seen live, not on the rig:

- `watching_overview` on a home with 105 watches answers 105,857 characters and Claude Code refuses it ("exceeds maximum allowed tokens"). The rig's overview is 2 KB, so the rig cannot show this.
- A key without the alerts access finds no alert or watchlist action, though the instructions name them.
- A daemon whose main thread stalls past 2.5 seconds reads as `daemon_offline`.
- The owner's consent to a new assistant lapses after 15 minutes; `om assistants allow <label>` works without an id.

Recipe for a live pass: `live-call.ts init | list | call <tool> '<json>'` and `live-compare.ts` under `run-artifacts/catalog-face/live-deploy/` of the `om-assistant-broker` task read the key through `resolveApiKeyWithSource` and never print it; `forwarder.ts` there is a loopback door on 18160 that adds the key and refuses `change` and `deposit`, for a headless client. Stop it when the run ends. Never approve a card or run a free change on a real watch as the tester.

Pending proof:

- A browser sign-in (OAuth) from a real assistant, and a link surviving a token refresh.
- `deposit` and `plot_inbox` on the new host against a live daemon.
- Two assistants on one daemon (needs a second credential on the rig's gateway).
- The daemon's unlisted `request_change` against a hosted build from main (unit-test proof only).

## Gotchas

- Two links can share one label (the key's label). `allow` and `revoke` then need the `asst_` id, which `om assistants --format json` prints.
- A scratch lane home copied from an earlier build keeps its old links; an old link with a 64-hex id is from before the identity fix and can be ignored.
- `OM_HOSTED_ROOT_SURFACE=om` moves the root to the om surface; `OM_HOSTED_DAEMON_CALLS_PER_MINUTE=3` gives a burst of 1 for a quick rate check.
- A daemon in the public cut has no relay channel, so none of this is reachable there.
- A deposit is stored about a second after it answers `accepted`; a read of the stored row right after can miss it.
- A lane daemon runs from source without watch mode, but every `control-om om --` call runs the current source, so do not drive the lane while files are mid-edit.
- An AI step's answer reaches the channel but not `watch_history` or `om watch history --format json`; only the chat TUI shows it.
- A client that picks tools by name can miss the plot behind `request_change`; the `deposit` listing names it. Seen once each way on 2026-11-11.
- Claude Code calls an MCP tool before loading its schema when its own tool search is on, so a model guesses argument names; a wrong key costs one round trip. It cost 22 refused calls across 60 runs on 2026-11-12.
- The dashboard's `/dashboard/watches` address renders an empty page when opened directly; reach Watches through the sidebar link (it lands on `/alerts`).
- `control-om up` boots `packages/cli/src/bootstrap.ts`, the public entry. Since #2422 the private families load only through `bootstrap.internal.ts`, so a lane has no relay link and an assistant call reads `daemon_offline`. Until the wrapper picks the internal entry, restart the lane daemon by hand with the same env through `bootstrap.internal.ts` and write its pid to the lane's pid file.
- The image tag for the hosted service is set by the platform controller after the pipeline pushes it. A sync made before the pipeline is green applies the old tag; sync again and check the tag. The server version in `initialize` tells which image a host runs.
