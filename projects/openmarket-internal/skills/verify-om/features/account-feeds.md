# Account feeds: log numbers, chart them, delete one, and the feed limit

*Re-checked 2026-11-22 (nightly), tree `01482928a5` (origin/main, v0.496.0+internal), guest lane on 18188 through `bootstrap.internal.ts`. Signed out: `series feeds --format json` answered `{relay: "signed_out", feeds: []}` and `feed key probe` exits 2 `feed_signed_out` with the `Run om login` hint, before any confirmation. One line cite corrected (`hosted/catalog.ts:283-284`). Not re-driven: everything that needs a relay or an account. (`cli/40-series-feeds.out`, `cli/40-feed-key.*`.) Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261122/r1/`*

*Verified: 2026-11-20, merged main `2d01b6b5d4` (#2612, #2628, #2644), real relay `9199a77`, real collab `18845f6`, on a local rig with the made-up accounts `@rig` (free tier, 25 feeds) and `@rig2`. Lane on 18141 through `bootstrap.internal.ts`. Driven, 14 of 14 claims: `om feed append`, `show`, `key` and `delete` at the CLI and a pty, the `feed_append` and `feed_show` tools over MCP stdio, `chart series push --feed`, `chart grid` and `chart symbol` on feed cells, the daemon's refusals, the assistant door, the hosted charts face with no daemon, the `agent.*` money rule at authoring and at the arm, `find`, the dropped `cadence_s`, the quota refusal on five faces, and one test file under an egress trap. A second slice on the same tree drove `observed_cadence_s`, `late_s` and both money guards again. Not driven: a browser drawing a feed, a real MCP OAuth token on a deployed hosted build, `om chat` calling these tools, the quota hint when no feed is offline or when the listing fails, a quota hint naming a watch's feed. Limits: the grid write went to a stand-in for tharamine's desired-grid route. Evidence root `~/Documents/dev-notes/om-2026-11-20-e2e-verify/run-artifacts/s3/` (`evidence/c01` to `c14`, `rig/`). Galleries `http://127.0.0.1:8098/om-1120-e2e/s3/` and `http://127.0.0.1:8098/om-1120-e2e/s5/`.*

A job or an assistant logs numbers to a feed on the owner's account and charts it. The first append declares the feed, private. A push key for a plain `curl` is rotated only at a terminal. The hosted charts face serves the same two tools under `agent.<name>` with no daemon. A person lists feeds with `om series feeds`, deletes one at a terminal, and reads a feed-limit refusal that names the feeds offline longest and the way out.

## Sub-features

- `append`: `om feed append <name> --values '{"<column>": <n>}'`, or `--rows '[[ts, v1, ...]]' --columns a,b`, with `--title`, `--cadence`, `--units`. The tool is `feed_append`.
  - The first call answers `created: true, accepted: 1`. A second reading in the same stored slot answers `replaced: 1`.
  - The answer is `{address, created, accepted, replaced, refused, stored_grain_s, chart_targets: [{column, exchange: "OM", symbol: "feed:<scope>/<name>:<column>"}]}`.
  - `--format text` prints `Feed:`, `Accepted:`, `Replaced:`, `Grain:` and one `Chart: OM feed:…` row per column.
  - The feed is private. An anonymous relay read answers 403 `feed_private`.
  - No answer on any face carries a push key (`omfd_`).
- `show`: `om feed show @<scope>/<name>`, tool `feed_show`. It answers `{address, state, rows, last_ts, first_ts, cadence_s, units, columns, stored_grain_s, visibility, observed_cadence_s, chart_targets}`, equal to the relay's own head.
  - `observed_cadence_s` is `null` for a one-row feed.
  - `late_s` appears only on a feed that is not live. It equals now minus `last_ts` minus the cadence (#2642).
  - A missing feed answers `feed_not_found`, exit 2. A bad address answers `invalid_options`, `A feed address looks like @scope/name.`
- `key`: `om feed key <name> [--title <t>] [--yes]` rotates the push key.
  - Off a terminal it answers `confirmation_required`, exit 2.
  - In a pty it asks `Rotate the push key for @<scope>/<name>? The old key stops working.` No aborts.
  - Yes prints `Rotated: …`, an `export OM_FEED_KEY=` line and a `curl` line, once.
  - After a second rotation the first key answers 401 `feed_token_invalid`. A key for one feed answers 401 on another.
  - It works for a feed declared anywhere, such as one the hosted face made. The declaration is rebuilt from the relay head, and the home then records it.
  - A name nothing holds answers `feed_not_found`, `Run om feed append <name> first; it declares the feed.`
  - No face has a `feed_key` tool.
- `chart-a-feed`: `om chart series push --feed @<scope>/<name> --key <column> --pane lower` sends `add_indicator`, and collab stores a `FEED` record with the address, column, cadence and pane.
- `feed-cell-check`: `om chart symbol --chart 0 --exchange OM --symbol feed:<scope>/<name>:<column>` and `om chart grid` answer `market.verified: true` for a feed the relay holds. A missing feed answers `verified: false, skipped: "target"` and the warning `feed not found: @<scope>/<name>`.
- `cadence-dropped`: `chart series push` with a cadence on a lower or overlay pane succeeds with the note `cadence_s applies to the main pane only, so it was dropped.` The stored payload carries no `cadence_s`.
- `daemon-refusals`: `feed_append` refuses, with no write to the relay:
  - `feed_daemon_owned` for a `watch.*` feed, an authored series feed and a feed the daemon pushes for a chart series. `… is a feed om pushes to itself.`
  - `feed_money_read` for a feed a money-reaching watch reads. `… so an append here could move money.`
- `agent-feed-money`: a watch that reads an `agent.*` feed and holds a money step is refused `watching_agent_feed_money`: `money never runs on a number an assistant pushes.`
  - It is refused on `watch create` with steps, on `watch action add` of the money step, on `watch edit --check`, and at the arm.
  - A feed with no `agent.` prefix takes the same money step.
- `hosted-feed-tools`: the hosted charts face, with no daemon link, lists `feed_append` and `feed_show` (53 tools on this tree).
  - Each call writes under the caller's own scope, as the caller's key.
  - Only `agent.<name>` is taken. Any other name answers `feed_name_agent_prefix`.
  - One account reading another's feed gets `feed_private`.
- `assistant-door`: on the daemon's own door `feed_append` is a free write that `find` and `describe` class as `kind: "read"`.
  - `read feed_append` appends one reading with no card.
  - `change feed_append` answers `not_a_change`, `Run it with read`.
  - Stamped rows answer `shape_not_served`.
  - `feed_delete` and `feed_key` answer `tool_not_served`.
- `find`: "log my step count every day" and "record a number over time" rank `feed_append` first on the lean stdio face, the hosted om surface and the daemon's door.
- `list`: `om series feeds`. Its shape, the `Left out` line and the `Incomplete` fallback are in [own-data-streams-and-views.md](own-data-streams-and-views.md) (`feed-list`).
- `delete`: `om feed delete <name> [--yes]`.
  - Off a terminal it answers `confirmation_required`, exit 2.
  - The prompt reads `Delete @<scope>/<name>: 1 reading, last Nov 20. This cannot be undone.` No keeps the feed.
  - Yes prints `Deleted: @<scope>/<name>`. The relay logs `DELETE 204`, head and rows then answer 404, and the home record is gone.
  - A watch's feed answers `feed_daemon_owned`, `Remove the watch instead: om watch remove <watch>.`
  - A home record the relay no longer holds prints `Deleted: … (the relay held none; this home's record is gone)`.
  - It is no agent tool. MCP answers `Tool feed_delete not found`, the lean face `unknown_tool`, the assistant door `tool_not_served`.
- `quota`: the 26th feed on a free account answers `feed_quota`.
  - Message: `Feed limit reached: 25 feeds on @rig (Free).`
  - Hint: `Offline longest:` then up to three feeds that are not live, a feed with no readings first, then oldest reading first.
  - The daemon CLI, the MCP tool and the assistant door end `Delete one with om feed delete <name>, or move @rig to a bigger plan.`
  - The hosted charts face and the hosted om surface end `Remove one at your OpenMarket terminal, or move @rig to a bigger plan.`
- `test-no-egress`: `packages/cli/test/inbound-readings-declaration.test.ts` pins `OM_LEDGER_ORIGIN` itself and makes no request off loopback (#2644).

## How to get to it (user POV)

- `om feed append steps --values '{"steps": 4100}'`, then `om feed show @<you>/steps`.
- `om chart series push --feed @<you>/steps --key steps --pane lower` to draw it.
- `om feed key steps` in a terminal, then the printed `curl` from any machine.
- An assistant on the hosted charts face calls `feed_append` with `agent.<name>`.
- `om series feeds` to see every feed. `om feed delete <name>` in a terminal to free a slot.

## Driving it with control-om

### The rig

Every script is in the evidence root's `rig/` folder. No key is kept there: the relay harness makes its own RSA key, its two made-up retail keys and `relay/creds.json` at start.

| Port | Piece | Script |
| --- | --- | --- |
| 18141 | om lane, internal entry | `control-om up`, then `bin/lane-internal-up` |
| 18142 | relay harness on the real relay tree, accounts `@rig` and `@rig2` | `bin/relay-up` |
| 18143 | mongod 8.2.6, one-node `rs0`, no auth | `bin/mongo-up` |
| 18144 | collab, the real App | `collab/collab-harness.ts` |
| 18145 | workspace and auth stub for collab | `collab/upstream-stub.ts` |
| 18146 | gateway key check, `users/me`, and a `/hook` sink | `gateway-standin.ts` |
| 18147 | hosted chart MCP from source | `bin/hosted-up charts 18147 charts` |
| 18148 | rooms relay stand-in | `rooms-relay.ts` |
| 18149 | in turn: listing-fail proxy, hosted om surface, egress trap | `listing-fail-proxy.ts`, `bin/hosted-up om 18149 om`, `trap-proxy.ts` |

1. Edit `rig/env.sh` first. `RIG`, `RIG_SP`, `RIG_OM`, `RIG_RELAY_TREE` and `RIG_COLLAB_TREE` name this run's scratchpad and worktrees. `relay/server.ts`, `lane-seed.ts` and `door-direct.ts` import the same trees by absolute path.
2. `bin/mongo-up`, then `bin/relay-up`. See the relay answer `/__rig/health`.
3. Boot the lane with the env in `env.sh`. Every OpenMarket origin is a loopback stand-in or `http://127.0.0.1:9`. `OM_LEDGER_ORIGIN` is the relay harness.
4. `bun lane-seed.ts` with the lane's `OM_HOME` signs the lane in as `@rig`.
5. `bin/lane-internal-up` restarts the lane on `bootstrap.internal.ts run` and writes the pid file. Only the assistant door needs it.
6. `bin/om <args>` is the CLI on the internal entry with the lane's `OM_HOME` and `OM_BIND`.
7. `bin/egress` lists every rig socket that is not on loopback. Expect 0 for each port.
8. Judge every step from `logs/relay-requests.log`. `bin/relay-get <path> [anon]` reads the relay as the owner or anonymously. `bin/relay-as-owner <METHOD> <path> [body]` sends with the account's key. Neither prints a credential.
9. `relay/tier.txt` switches the account's tier.

### Append, show and the push key

1. `bin/om feed append <name> --values '{"mood":28}' --format json`. See `created: true` and the `OM feed:` target. The relay log reads `GET …/head 404`, `PUT 201`, `POST …/rows 200`.
2. Run it again. See `created: false, replaced: 1`.
3. `bin/om feed append <name2> --rows '[[<ts>,4100,61],…]' --columns steps,bpm --title '<t>' --cadence 1h --units count`. See `accepted: 3` and two chart targets.
4. `bin/relay-get /api/v2/feeds/rig/<name>/rows`, then the same with `anon`. See the rows, then 403 `feed_private`.
5. `bin/om feed show @rig/<name2> --format json`. Compare it with `bin/relay-get /api/v2/feeds/rig/<name2>/head`.
6. `bin/om feed key <name> </dev/null`. See `confirmation_required`, exit 2.
7. In tmux, run `bin/om feed key <name>`. Answer No, then run it again and answer Yes. The relay logs `PUT …?rotate=1 200` only after Yes.
8. Run the printed `curl` with the key in `OM_FEED_KEY`. See 200, and the row on the relay.
9. Rotate again with `--yes --format json`. The first key answers 401.
10. Scan the lane home, the lane log, the rig logs and the evidence for the exact key values and for any `omfd_` string. Expect 0, with a control file that holds them.

### Chart a feed and check a feed cell

1. Needs collab and its stub up, and `bin/om chart select 6650b0b0b0b0b0b0b0b0b0b0`. `bin/om chart status` shows the workspace `open`.
2. `bin/om chart series push --feed @rig/<name2> --key steps --pane lower --format json`. See `action: "add_indicator"`, and the `FEED` record in the stub's `logs/workspaces.json`.
3. `bin/om chart symbol --chart 0 --symbol feed:rig/<name>:mood --exchange OM --format json`. See `verified: true`.
4. The same with a feed the relay does not hold. See the `feed not found` warning.
5. `bin/om chart grid --cols 2 --rows 1 --symbols '[{"symbol":"feed:rig/<name2>:steps","exchange":"OM"},{"symbol":"feed:rig/<missing>:value","exchange":"OM"}]'`. The stub needs its desired-grid route, which the copied `upstream-stub.ts` has.
6. `bin/om chart series push --id <id> --title '<t>' --pane lower --cadence 1h --times '[…]' --values '[1,2,3]'`. See the dropped-cadence note. Repeat without `--cadence` and see no note.

### The daemon's refusals and the money rule

1. `bin/om feed append watch.<slug> --values '{"temp":21}'`. See `feed_daemon_owned`.
2. `bin/om setup webhook --webhook-url http://127.0.0.1:18146/hook --allow-private-network --name desk --default`. A watch with an ai step needs a default channel, and setup sends a test POST, so the sink must be up.
3. Create a watch with a timer check that reads `@rig/<name2>`, an ai step and a money step (`--action '<json>'` twice). Then `bin/om feed append <name2> --values '{"steps":1,"bpm":1}'`. See `feed_money_read`, and no POST in the relay log.
4. `bin/om watch create '<label>' --every 30m --check '<check reading @rig/agent.<name>>' --action '<ai>' --action '<money>'`. See `watching_agent_feed_money`.
5. Create the same watch with no steps, add the ai step, then add the money step. The money step is refused.
6. `bin/om watch edit <money watch> --check '<check reading the agent feed>'`. Refused.
7. The arm. Hand-edit the stored watch file so its check reads the agent feed. `bin/om watch arm <watch> --yes --box order-1.size=5` is refused, and so is the yes at a pty. No epoch is granted.

### The hosted face and the assistant door

1. `bun gateway-standin.ts`, then `bin/hosted-up charts 18147 charts`. The face runs from source with `bun packages/cli/src/hosted/main.ts`.
2. `bun mcp-http.ts http://127.0.0.1:18147/mcp relay/keys/retail-key.txt --list`. See 53 tools with `feed_append` and `feed_show`. With `none` as the key file it answers 401 `missing_bearer`.
3. Call `feed_append` with `{"name":"agent.<name>","values":{…}}` as each account. Read each feed back from the relay under its own account.
4. Call it with a name that has no `agent.` prefix. See `feed_name_agent_prefix`.
5. For the door: `bun rooms-relay.ts`, the lane on the internal entry, `bin/om assistants on`, one call, then `bin/om approve <id>`.
6. `bun door-direct.ts '{"tool":"read","args":{"name":"feed_append","args":{"name":"<name>","values":{"score":5}}}}'` sends `mcp.call` straight to the daemon with the product's own client code. See the append with no card.
7. The same with `"tool":"change"`. See `not_a_change`.
8. `bin/hosted-up om 18149 om` serves the hosted om surface. `change feed_append` there is answered by the hosted tool.

### List, delete and the feed limit

1. `bin/om series feeds --format text`, read against `bin/relay-as-owner GET '/api/v2/feeds?scope=@rig'`.
2. `bin/om feed delete <name> </dev/null`, then in tmux answer No, then Yes. Read the relay log for `DELETE 204` and the head for 404.
3. `bin/om feed delete watch.<slug> --yes`. See `feed_daemon_owned`.
4. Fill the account. Append four hourly feeds with one old stamped row each (`--rows '[[<old ts>,5]]' --cadence 1h`), then live feeds until the relay lists 25.
5. `bin/om feed append <one more> --values '{"v":1}'`. See `feed_quota` and the three names. They equal the relay listing's three oldest feeds that are not live.
6. Repeat through the MCP tool, the door, the hosted charts face and the hosted om surface. The last two name the terminal as the way out.
7. `bin/om feed delete <oldest> --yes`, then the same append succeeds.

### The test under an egress trap

1. `bun trap-proxy.ts` on 18149. Prove it catches a fetch to a made-up `.invalid` host from Bun.
2. `HTTP_PROXY=http://127.0.0.1:18149 HTTPS_PROXY=http://127.0.0.1:18149 NO_PROXY=127.0.0.1,localhost bun test packages/cli/test/inbound-readings-declaration.test.ts`. See 23 pass, 0 fail, and no new line in `logs/trap-proxy.log`.

## Gotchas

- **`change feed_append` never reaches the daemon on the hosted om surface.** #2628 added a hosted tool of the same name, and the hosted tool of a name wins (`packages/cli/src/hosted/catalog.ts:283-284`). The hosted log reads `tool=change action=feed_append plane=hosted`. An assistant there writes `agent.*` feeds only. The daemon's row stays `free` (`packages/cli/src/mcp/assistant-reach.ts:87`), its catalog classes a free tier 1 action as a read, and `change` refuses a read by name (`packages/cli/src/mcp/assistant-tools.ts:607`). Nothing is unprotected. Evidence `evidence/c05b-assistant-door.txt`.
- **Known, not verified-good: a feed cell naming a column the feed lacks reads `verified: true`.** `om chart symbol --symbol feed:rig/<feed>:nope --exchange OM` answers no warning. The check is feed presence only (`packages/cli/src/actions/collab/_market-check.ts:232`, `:239-250`). Evidence `evidence/c04-chart-feed.txt`.
- **Known, not verified-good: arming a money watch on an `agent.*` feed asks for the size and shows the whole card first.** The refusal lands on the yes. Evidence `evidence/c07-agent-feed-money.txt`.
- **"At a terminal" means "not an agent tool", not "needs a tty".** `om feed key --yes` and `om feed delete --yes` run from a plain shell. An agent with a shell tool can run them.
- **Each `chart series push` of rows takes one relay feed.** Four pushes took four of the 25 slots. `om feed delete` removes such a feed and the daemon does not declare it again, but the lane keeps the stored chart series row. Evidence `evidence/c11-series-feeds.txt`, `evidence/c12-feed-delete.txt`.
- `om feed key` on a feed declared elsewhere resets the relay's title to the feed name unless `--title` is passed. The prompt says so.
- `find "keep a daily tally of my weight"` misses `feed_append` on all three faces. "record a number each day and plot it" ranks it fourth on the hosted om surface.
- `find "delete a feed"` on the lean face offers `series_delete`. It cannot remove an account feed, and over MCP it answers `capital_not_armed`.
- `om setup webhook` sends a test POST. A dead port fails the setup, and then a watch with an ai step is refused `watching_action_destination_unresolved`.
- `--ai` and `--money` on one `watch create` answer `invalid_input`. Pass `--action <json>` once per step.
- zsh globs a `?` in an unquoted address. Quote every relay path and URL.
- After a hand restart on the internal entry, `control-om doctor` still reports the launch as `bootstrap.ts`.
- The worktree's dashboard is the stub page. Render command output and tmux captures for the gallery.
- The pre-#2644 test file was not run as a negative control. If the trap missed, it would read the production relay.
