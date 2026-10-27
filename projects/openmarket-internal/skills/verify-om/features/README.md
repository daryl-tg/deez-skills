# om verification map

The maintained source for verifying user-facing behavior in the `om` daemon and
CLI. Read this index before driving, then use the matching feature file as the
recipe.

## Baseline preconditions

- Launch the lane on its **assigned** port. Bind `127.0.0.1`. Never pick a free
  one: `control-om up` (default `18101`, range `18097`–`18197`).
- **Only `up` reads `--port`.** Every other subcommand (`down`, `doctor`, `url`,
  `om`) takes the port from `OM_LANE_PORT` and silently falls back to `18101`.
  Driven 2026-10-23: `control-om down --port 18102` stopped lane 18101 and left
  18102 running. For a second lane, prefix every call: `OM_LANE_PORT=18102
  control-om down`.
- **The conventional `18101` may already be taken.** On 2026-10-26 another
  run's long-lived `kiyotaka-chat-service` node process held it. Doctor said
  `lane BUSY, not ours` and `up` refused. Never stop it: take another slot
  (`up --port 18103`) and set `OM_LANE_PORT=18103` on every later call.
- `control-om doctor` reports the expected origin, an isolated lane home, a
  present dashboard bundle, and a lane that is down or yours. **`dist present`
  does not mean a real bundle.** A fresh worktree that ran `bun run
  dashboard:stubs` reports `dist present (693 bytes)`: those stubs boot the
  daemon but render no dashboard. Run `bun run build:dashboard` (about 700 KB of
  `app.js`) before driving any dashboard guide.
- Never drive an instance this run did not start. The daemon on `31337` is the
  operator's, and it is never a target.
- A source lane is the tree **at boot**. If the repo moves under the run, doctor
  reports `lane version STALE` — relaunch before believing anything driven
  since.
- Every CLI call goes through `control-om om -- <args>`. A bare `om` writes
  the operator's home and looks identical while doing it.

## Driving conventions

- Start every recipe from a lane the run started, unless its preconditions say
  otherwise.
- Prefer ARIA roles and accessible names over CSS selectors or DOM position.
- Terminal actions run through `control-om om --` (the product) or
  `control-om cli --` (repo commands); browser actions through
  `agent-browser` against `control-om url <path>`.
- Pass `--format json` wherever it exists and assert on that, not on the text
  renderer.
- Treat every command as literal. Keep quoted names and flags unchanged.
- A lane home is disposable, so a recipe may mutate freely — but say what it
  created, and never remove proof artifacts.

## Proof and skip reporting

- Capture the user action and the resulting state, not only the final screen.
- CLI proof includes the command, stdout, stderr, and exit code.
- Mutation proof includes a read-only second view of the stored value, ideally
  on a different surface (the daemon's stream, the journal on disk, the
  dashboard table).
- Correlate surfaces on a shared id (`event_id`, watch slug) and timestamp, not
  on "both look right".
- UI proof is a **pair**: an accessibility snapshot and a screenshot, both
  showing app identity. The snapshot is diffable and survives a restyle; the
  screenshot is what a human reads.
- Publish with `control-om evidence publish <run-id> <revision>` and hand back
  the returned `8098` URL. Never an `18097`–`18197` URL.
- Report an unreachable path with the attempted command and the unmet
  precondition. Never report a skipped entry point as verified via another path.

## What a guest lane can and cannot prove

A fresh lane is signed out. It holds a machine-minted Data API key, so live
market data works; it holds no LLM credential, so every model-routed path is
out of reach. Before writing a recipe, place it on the right side of that line:

| Provable on a guest lane | Needs credentials this lane does not have |
|---|---|
| Daemon boot, health, lifecycle, logs | `om chat` and every agent turn |
| Watch CRUD, pause/resume, journals | Event-watch LLM classification, synthesis |
| Inbound ingest → fire → journal (`accept_all`) | Text signals, research studies |
| The dashboard and its RPC families | Registry publish/install, room posting |
| Market data reads (`coins`, `exchanges`, `points`) | Venue execution, wallet, orders |

## Every entry carries its own provenance

Directly under the H1, before the prose, each entry has a one-line
`*Verified: <date>, tree `<commit>` (<version>) — what was driven*`. That line is
the entry's baseline, and it is the ONLY place the baseline lives — a pass that
leaves it stale has destroyed the next pass's ability to diff.

It exists because this map lives in the skills hub rather than in the repo it
verifies — the operator's standing preference, recorded in SKILL.md under
"Project ownership and verification provenance". Upstream pstack keeps the map
project-local and committed, where `git log` on the file is its own verification
record; a hub map floats free of the repo's history, so the stamp is the only
thing tying an entry to a tree. It is shared by every worktree and rewritten by
whichever session happens to run a pass. Conversational memory of "we checked at commit X"
dies with the session; a stamp in the file survives into the next one, on any
branch, in any tree. Update the stamp in the same edit that re-proves the entry,
and say what you did NOT drive, so a later reader knows which half is old.

`git merge-base --is-ancestor <stamped-commit> HEAD` first: this repo's history
gets rewritten, and a stamped commit that is no longer an ancestor makes commit
counts meaningless. The tree-to-tree diff still answers correctly.

## What this map does NOT cover

The map grows through `create-verification-skill`, `maintain-verification-skill`,
and Clanker work that proves a previously unmapped surface live. Add its recipe,
provenance, and index link, then automatically publish only the changed map
Markdown under the hub's project verification contract. An absent surface is
unmapped, never verified-clean.

## Feature entry contract

An H1 title, the `*Verified:*` line, one paragraph of user-visible behavior, then
exactly four H2s in order: `Sub-features`, `How to get to it (user POV)`,
`Driving it with control-om`, `Gotchas`.

Keep implementation detail out. Name only user paths, stable handles, required
state, commands, and observable proof.

## Features

- [Event ingest and fire](./event-ingest-and-fire.md) — the end-to-end chain,
  provable with no credentials. Start here.
- [Daemon lifecycle and health](./daemon-lifecycle-and-health.md)
- [Watch lifecycle from the CLI](./watch-lifecycle-cli.md)
- [The ops dashboard](./ops-dashboard.md) — the shell and the observation
  surfaces, redesigned in v0.400.0
- [Watch authoring in the dashboard](./watch-authoring-ui.md) — new in v0.400.0:
  the UI now creates watches, not just shows them
- [Calendar scheduling and polling windows](./calendar-and-polling-windows.md)
- [The dashboard agent panel](./agent-panel.md) — new in v0.400.0; reachable on a
  guest lane only as far as its refusal
- [Paper trading accounts](./paper-accounts.md) — new 2026-10-22
- [Market data reads](./market-data-reads.md)
- [Origin challenge backoff](./origin-challenge-backoff.md) — a Cloudflare
  challenge holds every source on the host, provable with a loopback stub.
- [Firecrawl recovery before whitelist](./firecrawl-first-block.md) — first refusal recovery, repeated-refusal whitelist guidance, and no-key setup.
- [The capability layer over MCP (stdio)](./mcp-stdio.md) — new 2026-10-23:
  handshake, catalog, a read, and the capital gate refusing without spending.
- [Chart catalog reads](./chart-catalog-reads.md) — new 2026-10-23: indicator
  and drawing schemas, which need no chart tab.
- [Registry welcome page and personalised search](./registry-welcome-and-search.md)
  — new on main 2026-10-26 (#1947): `om welcome`'s gates and `om search`'s
  health handshake, driven against a loopback fixture registry.
- [Local reads and discovery](./local-reads-and-discovery.md) — new 2026-10-23:
  config and key claims, notification history, enums, schema intents, skills,
  indicator packages.
- [Agent creator lifecycle](./agent-creator-lifecycle.md) — on main since #1948 (`b50ca927d`). Guest-lane CLI/RPC reads and refusals were driven 2026-10-27. Runs, the GUI and sharing are still the historical branch record.

- [Hosted chart MCP: tenant state, health and readiness](./hosted-chart-mcp-tenant-state.md) — the
  `om-chart-mcp` binary on an agent port against a local Mongo: boot lines,
  `/healthz` vs `/readyz`, index rebuild, refusals; the tool-call path over
  the production gateway stays unverified without an operator key.

Not yet mapped, and worth adding when a change touches them: the hosted MCP
tool calls over the production gateway (`chart_*` with a real key), the chart workspace mutations (`om chart` add,
update, remove and drawings, which need a GUI chart tab), the `om chat` TUI,
packages and the registry, and the execution/venue verbs.


## Surface inventory

Source discovery re-run **2026-10-27** against **origin/main `8fe6a8432`
(v0.466.0)**, 15 commits past the previous census at `ee8e3a7ab` (an
ancestor). The user-facing changes are as follows. #1948 (`b50ca927d`) put the
agent creator's daemon side on main. `2060ff0a5` added the `/healthz`
footprint, slow-statement timing and an on-demand profiler RPC. #2161 added
remote-control operations over the relay, and #2160 made the hosted chart MCP
Mongo-only. `5a03ffb43` removed six option recipes. The rest is wrun/options
recipe work and an `@openmarket/shared` import move. Counts were re-taken from
source and are unchanged except where noted:

- **94 top-level command names** in `packages/cli/src/main.ts`, unchanged
  (`welcome` arrived with #1947). `alerts` is staff-only and hidden from
  `--help`. With `OM_DEV=1` in the CLI process, main.ts:236 also registers
  `roster` and `project`, plus `runs`, `pause`, `cancel`, `steer` and `eval`
  under the existing `agent` (#1948).
- **478 registered actions** (unchanged at `8fe6a8432`; #1948 added none) across 19 categories, counted by loading the
  `registry` array in `packages/cli/src/actions/index.ts` (unchanged from
  `42d044b02`; 477 at `db6e76ef5`, the one addition there being
  `chart_indicator_schema`; 481 with
  `OM_CHART_MULTIPLAYER=1`): rooms 192, watch 75, chart 45, system 32,
  market-data 19, packages 17, execution 13, hyperliquid 12, paper 11,
  research 10, news 9, wallet 8, polymarket 8, polymarket-account 6, calendar
  6, wrun 5, payments 4, memory 4, state 2. `docs/TOOLS.md` lists 476.
- **9 dashboard routes** plus the detail routes (`/`, `/agent`, `/alerts`,
  `/alerts/:idOrSlug`, `/news`, `/strategies`, `/strategies/:idOrSlug`,
  `/connections`, `/channels`, `/venues`, `/receipts`; `/paper` is not mounted
  in this build), and **30 runner RPC files** (`system.ts` gained the
  `profile` route). `apps/dashboard/src` is unchanged since `42d044b02`.

**The previous headline was wrong.** It claimed ~803 actions (797 at
`7e22214fb`) across 21 categories, but its own per-category numbers summed to
482. No `strategy` or `transient` category is registered at either tree: the
seven `actions/managed/*.ts` files declare `category: "strategy"` but are
built by factories behind `om managed` (`cmd/managed.ts`) and never enter the
registry. Seventeen guides exist. This table is the gap
between the guides and the surface.

Rows marked `live verification pending` are source-supported and undriven;
source inspection is not proof. Keep them across passes until driven, mapped, or
removed with source evidence.

| User outcome | Product source path | Guide / sub-feature | Live verification | Prerequisite or gap |
|---|---|---|---|---|
| Check the install: doctor, status, logs | `cmd/{doctor,status,logs}.ts` | [daemon-lifecycle-and-health.md](daemon-lifecycle-and-health.md) | 2026-10-27, main `8fe6a8432` (14 doctor checks, status, service status) | None. |
| See the daemon's footprint and slow statements; profile a stalled daemon | `runner/http/server.ts:1546`; `runner/db-timing.ts`; `runner/http/rpc/system.ts` (`profile`) | [daemon-lifecycle-and-health.md](daemon-lifecycle-and-health.md) (`profile`, footprint step) | 2026-10-27, main `8fe6a8432` (`memory`/`slow_sql`/`roster` on `/healthz`; profiler 409/400/200/stacks) | No real slow statement was produced (`OM_DB_SLOW_MS=1` plus a restart would). `start` always says `already:false` (product gap). |
| Look up enum domains, schema intents and bundled skills | `cmd/{enum,schema,skill}.ts`; `packages/sdk/src/types/enum-domains.ts` | [local-reads-and-discovery.md](local-reads-and-discovery.md) | 2026-10-27, main `8fe6a8432` (`enum --list`/`--domain`, `schema read`, `skill list`) | `schema read <intent>` and `skill show` undriven. |
| Connect an AI provider or coding agent from the dashboard | `apps/dashboard/src/pages/connections.tsx`; `runner/http/integrations-api.ts` | [ops-dashboard.md](ops-dashboard.md) (Connections) | 2026-10-27, main `8fe6a8432` (read-only) | Pressing `Connect` rewires the operator's real coding agents, so it is never driven from a lane. |
| Publish and read live series snapshots | `cmd/series.ts`; `docs/LIVE-SERIES.md` | unmapped | live verification pending | `list`/`show`/`create` look local per source; `publish` needs an account. |
| Resolve a phrase to venue fields; screen and chart metrics | `cmd/{resolve,metric,markets,tenors}.ts` | [market-data-reads.md](market-data-reads.md) (sub-features only) | live verification pending | Guest-drivable per source; this pass drove only `enum`, `coins`, `exchanges`, `points`, `instruments` and `option-chain`. |
| Open a local paper-trading account and read its book | `actions/paper/*.ts`; `runner/http/rpc/paper.ts` | [paper-accounts.md](paper-accounts.md) | 2026-10-27, main `8fe6a8432` (create/ls + Paper tab; show/log/set/reset on 2026-10-26) | Open/close/reset-all/digest undriven. |
| List a venue's instruments and read an options chain | `cmd/instruments.ts`; `cmd/option-chain.ts`; `actions/data/{instruments,option-chain}.ts`; `runner/v3/` | [market-data-reads.md](market-data-reads.md) (Gotchas) | 2026-10-26, main `ee8e3a7ab` (default refusal; v3 rows and expiries) | Needs `OM_DATA_TRANSPORT=v3` on the CLI call (`OM_DATA_V3_URL` too if the home sets `OM_BASE_URL`); the default transport exits 2 `invalid_query`. Typed-door reads added by #2114 (fx/index candles, ETF flow, FRED) are undriven. |
| Read and clear model-provider plan holds (`usage plans`) | `actions/data/usage-plans.ts`; `cmd/usage.ts` | [market-data-reads.md](market-data-reads.md) (Gotchas) | 2026-10-26, main `ee8e3a7ab` (guest: empty `providers`) | Corrected: this reports MODEL provider plans and holds, not Data API tiers. Populated rows, `--refresh` and `--clear` need a signed-in model provider. |
| Give 👍/👎 feedback on an openfeed alert; a new feed sends today's top 3 | `actions/watch/feedback.ts`; `openfeed/{feedback*,first-look}.ts` | unmapped | live verification pending | Needs an account, registry, LLM credential and a channel destination. `watch_feedback` has no CLI verb (MCP or chat only). Its refusal on a non-OpenFeed watch, `watch_feedback_not_openfeed`, is guest-reachable over MCP per source but undriven. |
| Open the registry welcome page (`om welcome`) | `cmd/welcome.ts`; `runner/packages/registry-contracts.ts` | [registry-welcome-and-search.md](registry-welcome-and-search.md) | 2026-10-27, main `8fe6a8432` (real registry: "does not offer"; fixture: all three gate branches) | On main since #1947. The success path needs a registry advertising `welcome`, which production still did not on 2026-10-27, so it was proved against a fixture. |
| Get plain-language, personalised registry search results | `cmd/search.ts`; `runner/packages/search.ts` | [registry-welcome-and-search.md](registry-welcome-and-search.md) | 2026-10-27, main `8fe6a8432` (fixture: `mode=nl`, `reasons`; with a key, `rank=for-you` + bearer; TTY text renderer with reasons lines) | Production still returns the old shape (no `nl` advertised). |
| Uninstalling or unfollowing tells the registry (receipt retraction) | `actions/packages/uninstall.ts`; `actions/watch/follow.ts`; `runner/packages/{retractions,use-receipts}.ts` | [registry-welcome-and-search.md](registry-welcome-and-search.md) (Gotchas) | live verification pending | Needs an account whose install or follow receipt returned an `edge`, plus a registry advertising `receipt_retract`. A guest never retracts. Signals are `[use-receipts]` log lines and `<home>/receipts/retractions.json`. |
| Finish `om init` by opening the welcome page (`--launch`) | `cmd/init.ts` | [registry-welcome-and-search.md](registry-welcome-and-search.md) (`init-closing`) | live verification pending | `om init` needs a TTY (exit 2 otherwise) and writes channel, credential and service state, so it is never driven on a lane. |
| Watch narrative (sentences, facets, entities from a recipe) | `packages/contracts/src/watch-narrative.ts` | **non-outcome** | n/a | A contracts library with no consumer in the CLI or dashboard at `ee8e3a7ab` or `8fe6a8432` (re-grepped 2026-10-27). Nothing renders it yet; re-check when one does. |
| Review a scheduled calendar occurrence | `actions/calendar/*`; `runner/calendar/blocks.ts` | [calendar-and-polling-windows.md](calendar-and-polling-windows.md) | 2026-10-27, main `8fe6a8432` (occurrence, select, revise, reject, links, polling windows) | None. The window was not waited out to run. |
| Recover a challenged origin through a paid reader | `runner/firecrawl/*` | [firecrawl-first-block.md](firecrawl-first-block.md) | no-key path re-driven 2026-10-27, main `8fe6a8432`; configured path pending | Needs `OM_FIRECRAWL_API_KEY` **and** a redirect of `api.firecrawl.dev/v2/scrape` to a fixture, together. |
| Create, import, Try, install, publish, adopt and revoke an agent | `packages/roster/src/http/roster-api.ts` (`imports/*`, `local-packages/*`, `builder`, `instances/:id/try`) | [agent-creator-lifecycle.md](agent-creator-lifecycle.md) (historical branch closeout) | live verification pending on main | On main since #1948 (`b50ca927d`), HTTP/GUI only. Needs an account, an LLM credential or coding brain, and the openmarket-chat Agents GUI (`verify-om-chat`). |
| Read agent work runs, refuse unknown runs, read roster health and measures | `cmd/{roster,roster-runs,roster-controls,roster-retry}.ts` (`OM_DEV=1`); `packages/roster/src/http/roster-work-api.ts`; `/healthz` `roster` | [agent-creator-lifecycle.md](agent-creator-lifecycle.md) (Guest lane on main) | 2026-10-27, main `8fe6a8432` (empty runs, `not_found`/`malformed_body` refusals, roster list/measures, `/rpc/v1/roster/projects`) | Real runs, plan approval, steer and retry need an installed agent plus a model or brain. |
| Link a coding project and set its delivery | `cmd/project-{token,delivery,unlink}.ts` (`OM_DEV=1`); `/rpc/v1/roster/projects` | [agent-creator-lifecycle.md](agent-creator-lifecycle.md) (Guest lane on main) | refusal only, 2026-10-27, main `8fe6a8432` (`project unlink nope` → `not_found`) | Needs a project linked through the GUI and a real forge token. |
| Drive persona and away operations from the web over remote control | `agent/channels/remote-control.ts`; `packages/rooms-client/src/remote-operation-routes.ts` (#2161) | unmapped | live verification pending | Needs `om agent remote enable`, the relay and a signed-in web client; nothing is guest-observable. |
| Compose a watch (or a set) from a natural-language ask | `actions/watch/watch-compose.ts`; `actions/watch/kit.ts` | unmapped | live verification pending | Needs an LLM credential; the single largest `om watch` entry point. |
| Share, follow, fork, install a watch; room shares and knocks | `actions/watch/{share,follow,fork,install,share-room,knocks,relay-door}.ts` | unmapped | live verification pending | Registry + account credential; a follower needs a second home. |
| Attach and arm steps (ai / tool / money) on a watch | `actions/watch/{action-add,action-remove,tools,run-now}.ts` | unmapped | live verification pending | Money steps are capital-gated; ai steps need a model credential. |
| Grow an existing watch with more sources | `actions/watch/{source-add,page-add,search-add,model-add,source-copy}.ts` | unmapped | live verification pending | Page/search/model sources need a model credential; a feed source does not. |
| Repair or retry a watch broken for any non-origin reason | `actions/watch/{repair,retry,lane-retry}.ts` | unmapped | live verification pending | Needs a watch in a genuinely broken state to repair. |
| Read the wider journal surface: list, stats, chapters, search | `actions/watch/{journal-search,journal-stats,chapters,journal-list}.ts`; `cmd/event-journal.ts` | [watch-lifecycle-cli.md](watch-lifecycle-cli.md) (journal step) | 2026-10-27, main `8fe6a8432` (`event-journal list`, `search`, `journal-stats`, empty `chapters`) | Populated chapters undriven (they need a model's summary fold). |
| See and reclassify rows the judge never reached | `actions/watch/unjudged-rows.ts`; `actions/watch/reclassify.ts` | unmapped | live verification pending | `watch unjudged` is new this range; needs a daily-cap state to observe. |
| Rewrite a fired row's recorded verdict | `actions/watch/synthesize.ts` | unmapped | live verification pending | Destructive projection rewrite; no guide at all. |
| Move a watch between devices, mute a remote copy, restore one | `actions/watch/{move-here,move-readiness,mute,restore,adopt-here}.ts` | unmapped | live verification pending | Needs a second device/home for the interesting cases. |
| Read money-step execution history and digests | `actions/watch/{execute-history,execute-digest,execute-paper-reset}.ts` | unmapped | live verification pending | Needs executed money steps; distinct from the event journal. |
| Session and device identity: sign-in state, rename/revoke devices, account email | `actions/auth/{status,relogin}.ts`; `actions/devices/*`; `actions/account/email.ts` | unmapped | live verification pending | Account credential; revoke is destructive. |
| Mint and revoke API keys | `actions/keys/{create,revoke}.ts` | unmapped | live verification pending | Account credential; security-tiered, revoke is permanent. |
| Pair and manage a notification channel | `actions/system/{channel-add,channel-home}.ts`; `runner/http/rpc/channel.ts` | unmapped (dashboard shell only) | live verification pending | Needs a real Telegram/Discord/Slack credential. |
| Read the daemon's own notification history | `actions/system/{notis-list,notis-get}.ts`; `cmd/notis.ts` | [local-reads-and-discovery.md](local-reads-and-discovery.md) | 2026-10-27, main `8fe6a8432` (`notis --since 7d` rows) | `notis get` and `--after` paging undriven. |
| Inspect resolved config and the active key's claims | `actions/system/{config-show,config-key-info}.ts`; `cmd/config.ts` | [local-reads-and-discovery.md](local-reads-and-discovery.md) | 2026-10-27, main `8fe6a8432` (`show`, `key-info`, `get`) | `config set`/`edit` undriven. |
| Upgrade the binary, migrate and restart | `actions/system/upgrade.ts` | unmapped | live verification pending | Risk tier 5, confirm-carded; must never run against a lane. |
| Read the subscription plan and pricing | `actions/system/upgrade-show.ts` | unmapped | live verification pending | Account/billing state; note the filename does not match the outcome. |
| Watch roster triage: what needs attention, one-click repair | `actions/system/{watching,watching-resolve-attention}.ts` | unmapped | live verification pending | Needs watches in attention-needing states. |
| Read indicator and drawing schemas (catalog) | `actions/collab/{indicator-schema,indicator-list}.ts`; `cmd/chart.ts` | [chart-catalog-reads.md](chart-catalog-reads.md) | 2026-10-27, main `8fe6a8432` (`indicator schema`, `indicator list`, `drawing schema`) | The `--chart`/`--workspace` forms and the `wrun/@scope/name/output` metric-id form are undriven. |
| Drive chart workspaces, indicators and drawings | `actions/collab/chart-*.ts`, `drawing-*.ts`, `indicator-*.ts` | unmapped | live verification pending | Needs a human's GUI chart tab open on a live collab session; a headless lane has nothing to submit to. |
| Backtest a strategy over historical bars | `actions/research/backtest*.ts` | unmapped | live verification pending | Condition-source backtests are guest-key drivable; fixed-view/ai-step kinds need accepted event-watch rows first. |
| Browse paid news feeds and read Fast-alerts billing | `actions/news/{feeds,billing,brief,voice}.ts`; `runner/http/rpc/news.ts` | unmapped (dashboard shell only) | live verification pending | Catalog browsing may be guest-ok; billing and follow need an account and a funded vendor relationship. |
| Agent memory: save, search and forget durable notes | `actions/memory/*.ts`; `cmd/memory.ts` | unmapped | live verification pending | `memory_save`/`forget` are agent-tool-only — they need a live `om chat` turn, not the bare CLI. |
| Author and compile a custom WASM indicator | `actions/wrun/{create,author,build,source-set,list}.ts`; `cmd/wrun.ts` | [local-reads-and-discovery.md](local-reads-and-discovery.md) (`wrun list`/`templates` only) | 2026-10-27, main `8fe6a8432` (list; templates down to 91 after `5a03ffb43`) | `wrun create`/`validate` are filesystem-only and undriven; `wrun build` compiles and installs deps, so it needs package-manager access. |
| Arm and tune a live managed-strategy wallet | `cmd/managed.ts` over `actions/managed/*.ts` factories (CLI-only: not in the action registry) | unmapped | live verification pending | Capital-reaching: funded venue wallet plus an explicit arm gate. Out of reach for a guest lane. |
| Place and manage real venue orders; wallet and execution | `cmd/{order,execute,buy,hyperliquid,polymarket}.ts`; `actions/{execute,orders,hyperliquid,wallet,polymarket}/` (`actions/execution/` does not exist) | unmapped | live verification pending | Real money. Needs a funded account and a safe plan; nothing attempted. |
| Reach the capability layer over MCP (stdio) | `cmd/mcp.ts`; `mcp/server.ts`; `mcp/capital-gate.ts` | [mcp-stdio.md](mcp-stdio.md) | 2026-10-27, main `8fe6a8432` (handshake, 451 tools, a read, `capital_yolo_harness` under a bypass-mode driver) | `om mcp arm`, `--catalog operator` and `--session merged` undriven. |
| Reach the capability layer over hosted MCP (HTTP) | `mcp/http.ts` | unmapped | live verification pending | Needs hosted auth and scopes. |
| Run the hosted chart MCP against Mongo: boot, health, readiness, index rebuild, refusals | `packages/cli/src/hosted/{main,run,config,tenant-store-mongo,tenant-store-health}.ts` | [hosted-chart-mcp-tenant-state.md](hosted-chart-mcp-tenant-state.md) | 2026-10-27, main `8fe6a8432` (boot lines, health pair up/down/back, rebuild, four refusals, `--help`) | The tool-call path needs an operator API key on the production gateway; the env-gated suite was not run this pass. |
| Publish, install and manage registry packages | `cmd/{packages,publish,install}.ts`; `actions/packages/*` | partially via agent-creator (itself unverified) | live verification pending | Registry credential; `package_delete` is irreversible. |
| Approve an arming or model edit from the dashboard | `runner/http/rpc/{watch-arm-review,watch-edit-review}.ts` | unmapped | live verification pending | Needs a watch with a money/ai step awaiting approval. |
| Sealed secrets bridge | `runner/http/rpc/secrets.ts` | unmapped | live verification pending | Security-sensitive; GUI never holds keys. |
| Social chat: rooms, DMs, topics, docs, moderation | `actions/rooms/*` (190); `cmd/room.ts` | **out of scope here** | n/a | Owned by `verify-om-chat` per this repo's boundary rules; this repo holds only the protocol surface and daemon-side actions. Recorded so the gap is not mistaken for an omission. |
| Standalone `/paper` dashboard route | `apps/dashboard/src/paper-plane.tsx` | **non-outcome** | n/a | Mounts only when `strategyRoutes === null` (the OSS export). Unreachable in any lane `control-om` drives; reach Paper via the `/strategies` tab. |

### Known product gaps (reported, not map drift)

- `POST /rpc/v1/system/profile` `{"action":"start"}` always answers
  `already: false`, even when the profiler is already armed. A second start
  returns the FIRST `started_at` with `already: false`
  (`runner/http/rpc/system.ts:403`). Driven 2026-10-27 at `8fe6a8432`.
- `/strategies/<unknown>` **flickers** between `No strategy named <slug>. Back to
  Strategies.` and `Loading…` on a ~12 s cycle. Re-observed 2026-10-27 at
  `8fe6a8432` with the same cadence (`Loading…` at 12 s and 24 s). Driven 2026-10-26 at
  `ee8e3a7ab`, sampled every 3 s: the 404 text at 3–9 s, `Loading…` at 12 s,
  the 404 text at 15–21 s, `Loading…` at 25 s. `money/show` answered 404
  each time. The slow `Loading…` read on 2026-10-23 fits this cycle. The
  `Unavailable.` read on 2026-10-22 is a third branch of the same page
  (`pages/strategy-detail.tsx:357-370`) that has not been seen since. The cause
  is not isolated.

- The "paper book" link on a strategy detail page points at `/paper?account=<id>`,
  a route this build does not mount; driven at `7e22214fb` it renders the shell
  with an empty `main` — no content, no 404.
- `AGENTS.md`'s capital-line section documents a `strategy_*` verb family
  (`strategy_create`, `strategy_resume`, `strategy_edit`, `strategy_remove`,
  `strategy_paper_reset`) that no longer exists in source. No `strategy`
  category is registered at all; the managed verbs exist only behind
  `om managed` (`cmd/managed.ts`).
