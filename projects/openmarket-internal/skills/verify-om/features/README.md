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
- [Agent creator lifecycle](./agent-creator-lifecycle.md) — on main since #1948 (`b50ca927d`). Guest-lane CLI/RPC reads and refusals are driven. The eight `@om-core` defaults installed from production on 2026-10-29. Runs, the GUI and sharing are still the historical branch record.
- [Chat transcript layout](./chat-transcript-layout.md) — branch `daryl/tui-readability`: your message as a clay-barred panel, unlabelled replies at a 100-column measure, warm bands for fires and digests, faint notice strips, replay identical to live, the spinner above the composer, and the chimes. It needs a local fake model that streams tool calls, and the recipe carries one.
- [Chat workspace TUI](./chat-workspace-tui.md) — on main since #2182 (v0.467.0): `om chat --workspace`, the sidebar (WATCHES, FIRES, PAPER, POSITIONS, CALENDAR, USAGE, up to 3 on), the ctrl+x menu and its panel picker, `om sidebar`, and the What's new card in plain `om chat`. It needs a local fake model, and the recipe carries one.

- [Hosted chart MCP: tenant state, health and readiness](./hosted-chart-mcp-tenant-state.md) — the
  `om-chart-mcp` binary on an agent port against a local Mongo: boot lines,
  `/healthz` vs `/readyz`, index rebuild, refusals; the tool-call path over
  the production gateway stays unverified without an operator key.

Not yet mapped, and worth adding when a change touches them: the hosted MCP
tool calls over the production gateway (`chart_*` with a real key), the chart workspace mutations (`om chart` add,
update, remove and drawings, which need a GUI chart tab), the rest of the `om chat` TUI (a real model's turns, slash commands, panels),
packages and the registry, and the execution/venue verbs.


## Surface inventory

Scheduled maintenance, **2026-10-29**, against **origin/main `7ec575e55`**, one commit past the nightly's `32ca0d6c7`. #2194 moves the Indicator kit to scaffold 106. The three Feeds starters read a placeholder `@you/your-feed` (`@you/your-events` for `feed-events`) until `ref` is set. The kit build refuses internal notes in the texts it bundles (`packages/cli/scripts/gen-indicator-kit-bundle.ts:253`). The diff touches nothing under `cmd/`, `main.ts`, `actions/`, `rpc/` or `apps/dashboard/src`; only `runner/wrun/authoring.ts` changed under `packages/cli/src`. So the command, action, RPC and route counts below still hold, and no outcome row was added.

Live this pass, on a fresh lane at 18161, at smoke depth:
- **Driven for the first time:** `wrun create`.
- **Re-proved:** the wrun templates.
- **Re-driven:** the ingest → stream → journal fire chain, MCP stdio, the dashboard routes, paper, market reads, and the local, chart, calendar and registry reads.
- **Not re-driven:**
  - the chat workspace TUI and the What's new card;
  - origin challenge and Firecrawl;
  - hosted chart MCP;
  - the agent creator and agent panel;
  - watch authoring UI.

Evidence: `http://127.0.0.1:8098/verify-om-maint-20261029/r1/`.

Nightly maintenance, **2026-10-29**, against **origin/main `32ca0d6c7` (v0.467.0)**, 16 commits past `186030b63` (an ancestor). The census:

- **Commands:** one new top-level command, `sidebar` (`main.ts:63`). That makes 95 by this table's convention, or 98 quoted names in the `COMMAND_MODULES` `names:` arrays, against 97 before.
- **Actions:** 479 registered (`system` 33, up from 32, for `sidebar_layout`). `docs/TOOLS.md` lists 477.
- **Unchanged:** 30 RPC files and 9 dashboard routes. `apps/dashboard/src` has no diff.
- **Scaffold:** `WRUN_SCAFFOLD_VERSION` went from 104 to 105.

User-facing changes:

- #2182, #2187 and #2189 put `om chat --workspace`, `om sidebar`, the `chat.workspace` key and the ctrl+x menu on main. With them comes a What's new card in plain `om chat`, generated from CHANGELOG blocks.
- #2183 moved the default agents to `@om-core`, and production now serves them.
- #2188 and #2192 add target-step admit bounds and a cooldown, a paper pager for target legs, `PAPER` rows in `watch execute history`, a `Steps:` paragraph in `paper digest`, an always-stored scheduled digest edition, and a research `admission_not_modeled` warning.
- #2184 and #2190 move the options packages onto the data plane's book folds. Only a chart host shows that change.

Live this pass: every guide except hosted chart MCP, at smoke depth or better, on lanes 18103 and 18104 (the second with the loopback switch).

- **Driven for the first time:** the default-agent install, `paper digest`, and the What's new card and its `w` action.
- **Re-driven on main:** the chat workspace, first proved on the branch.

Evidence: `http://127.0.0.1:8098/vom-nightly-20261029/r1/`.

Scheduled maintenance, **2026-10-28**, against **origin/main `186030b63`**, five commits past `a8fa10974`. The delta changes nothing under `packages/cli/src` or `apps/`, so the command, action, RPC and dashboard-route counts below still hold. Its user-facing changes:

- #2180 (`f8b2ca3b4`): thirty US options templates now say they read OPRA at the viewer's own tier (`runsOn`, `packages/sdk/src/wrun-sdk-sources.ts`).
- #2171 (`edd772a4c`): the `spot-exposures` recipe moves to 0.7.0 and reads the server's strike kit fold. Its Expiry preset is removed.
- `db59e1d65`: `expected-move` shades each band's far half with one gradient.
- #2181 (`186030b63`): `requestTodosSnapshot` echoes board keys. This is a rooms-client wire change for OM Chat, unpublished and not a daemon surface.

Live this pass:
- every guide except Firecrawl and hosted chart MCP, at smoke depth on lanes 18143 and 18145 (each guide's stamp names what was driven);
- market reads on a fresh home;
- the origin-challenge hold, steps 1-3.

No new outcome rows. The `wrun templates` wording was driven live (see [local reads](local-reads-and-discovery.md)). The two recipe changes render only on a chart host, and that host is outside this skill. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261028/r1/`.

Source discovery re-run **2026-10-28** against **origin/main `a8fa10974`
(v0.466.0, no release cut since)**, 10 commits past `8fe6a8432` (an ancestor).
Counts are unchanged: `main.ts` and `cmd/` have no diff, the registry still
loads 478 actions in the same 19 categories, `docs/TOOLS.md` lists 476, and
there are still 30 RPC files and the same dashboard routes. The user-facing
changes are:

- #2167/#2169: the eight default agents now install from `@om-skills` registry
  packages in the background after boot, and the bundled snapshot is gone.
- #2173: the symbol directory reads v3 first under `OM_DATA_TRANSPORT=v3`.
- #2175: the exchange enum in the v3 contract gains `CRYPTOCAP`, `LIGHTER`,
  `VARIATIONAL` and `VARIATIONAL_SWAP`.
- #2176: a target step holds its queued position, and the paper exit lane
  fills the package's resting stop and limit.
- #2177: wrun polylines take gradients (`WRUN_SCAFFOLD_VERSION` 104).

Six outcome rows were missing for guides that already existed. They are added
at the end of the table, along with two new outcomes. Every guide was
re-driven on two lanes (18103, and 18104 with the loopback switch).
Evidence: `http://127.0.0.1:8098/vom-nightly-20261028/r1/`.

The previous census, of **2026-10-27** against **origin/main `8fe6a8432`
(v0.466.0)**, was 15 commits past `ee8e3a7ab` (an ancestor). Its user-facing changes were these. #1948 (`b50ca927d`) put the
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

**Second pass, 2026-10-27 (scheduled maintenance, same tree `8fe6a8432`).** An independent census of `main.ts`, the action registry files, `runner/http/*` and the dashboard routes found 13 outcome groups with no row; they are added at the bottom of the table, all pending. RPC files (30) and dashboard routes were re-confirmed. The top-level command count from a static read of `main.ts` `names:` arrays is 96 including the `OM_DEV` names, consistent with 94 plus `roster`/`project`; the registry count of 478 was not re-loaded. Live drives moved 13 pending rows to partial (refusal-only or empty-state) or full: series (local), feedback, source add/remove, repair/retry, unjudged, execute reads, plans, watching overview, backtest, memory, hosted MCP over HTTP, arm-confirm and secrets status. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261027/r1/`.

Rows marked `live verification pending` are source-supported and undriven;
source inspection is not proof. Keep them across passes until driven, mapped, or
removed with source evidence.

| User outcome | Product source path | Guide / sub-feature | Live verification | Prerequisite or gap |
|---|---|---|---|---|
| Check the install: doctor, status, logs | `cmd/{doctor,status,logs}.ts` | [daemon-lifecycle-and-health.md](daemon-lifecycle-and-health.md) | 2026-10-29, main `32ca0d6c7` (14 doctor checks, status, service status) | None. |
| See the daemon's footprint and slow statements; profile a stalled daemon | `runner/http/server.ts:1546`; `runner/db-timing.ts`; `runner/http/rpc/system.ts` (`profile`) | [daemon-lifecycle-and-health.md](daemon-lifecycle-and-health.md) (`profile`, footprint step) | 2026-10-28, main `a8fa10974` (`memory`/`slow_sql`/`roster` on `/healthz`; profiler 409/400/200/stacks) | No real slow statement was produced (`OM_DB_SLOW_MS=1` plus a restart would). `start` always says `already:false` (product gap). |
| Look up enum domains, schema intents and bundled skills | `cmd/{enum,schema,skill}.ts`; `packages/sdk/src/types/enum-domains.ts` | [local-reads-and-discovery.md](local-reads-and-discovery.md) | 2026-10-28, main `a8fa10974` (`enum --list`/`--domain`, `schema read`, `skill list`) | `schema read <intent>` and `skill show` undriven. |
| Connect an AI provider or coding agent from the dashboard | `apps/dashboard/src/pages/connections.tsx`; `runner/http/integrations-api.ts` | [ops-dashboard.md](ops-dashboard.md) (Connections) | 2026-10-28, main `a8fa10974` (read-only) | Pressing `Connect` rewires the operator's real coding agents, so it is never driven from a lane. |
| Publish and read live series snapshots | `cmd/series.ts`; `docs/LIVE-SERIES.md` | [local-reads-and-discovery.md](local-reads-and-discovery.md) / Series | local create/list/show live verified 2026-10-27 maintenance, main `8fe6a8432`; publish refused | `series publish --dry-run` with the lane's guest key reached the registry and got `publish_rejected`: kind `live-series` is not accepted by the v1 registry. Real publish and remote read are pending, and possibly blocked by the registry (reported). |
| Resolve a phrase to venue fields; screen and chart metrics | `cmd/{resolve,metric,markets,tenors}.ts` | [market-data-reads.md](market-data-reads.md) / Resolve, metrics and markets | 2026-10-28, main `a8fa10974` (`resolve BTC`; `metric list`, `get`, `series` and `screen`; `markets`, including `--exchange LIGHTER`) | `tenors` returned `server_error` (500) on every attempt, with and without `--exchange DERIBIT`. That is a service fault, so tenors stays unproven. |
| Open a local paper-trading account and read its book | `actions/paper/*.ts`; `runner/http/rpc/paper.ts`; `runner/paper/digest.ts` | [paper-accounts.md](paper-accounts.md) | 2026-10-29, main `32ca0d6c7` (create/ls, the Paper tab, and `paper digest` all-accounts and per-account with the new `Steps: none` lead; show/log/set/reset on 2026-10-26) | Open/close/reset-all/`digest-set` and the scheduled edition undriven. Step rows in the digest need a target step. |
| List a venue's instruments and read an options chain | `cmd/instruments.ts`; `cmd/option-chain.ts`; `actions/data/{instruments,option-chain}.ts`; `runner/v3/` | [market-data-reads.md](market-data-reads.md) (Gotchas) | 2026-10-28, main `a8fa10974` (default refusal; v3 rows and expiries; `exchanges` under v3 returned 30 venues, against 48 on `auto`) | Needs `OM_DATA_TRANSPORT=v3` on the CLI call (`OM_DATA_V3_URL` too if the home sets `OM_BASE_URL`); the default transport exits 2 `invalid_query`. The daemon's `counters.symbol_directory_*` (#2173) were not read: that needs `OM_DATA_TRANSPORT=v3` on `up`. Typed-door reads added by #2114 (fx/index candles, ETF flow, FRED) are undriven. |
| Read and clear model-provider plan holds (`usage plans`) | `actions/data/usage-plans.ts`; `cmd/usage.ts` | [market-data-reads.md](market-data-reads.md) (Gotchas) | 2026-10-26, main `ee8e3a7ab` (guest: empty `providers`) | Corrected: this reports MODEL provider plans and holds, not Data API tiers. Populated rows, `--refresh` and `--clear` need a signed-in model provider. |
| Give 👍/👎 feedback on an openfeed alert; a new feed sends today's top 3 | `actions/watch/feedback.ts`; `openfeed/{feedback*,first-look}.ts` | [mcp-stdio.md](mcp-stdio.md) / Hosted MCP (refusal) | refusal live verified 2026-10-28, main `a8fa10974` (`watch_feedback` over MCP: `watch_feedback_not_openfeed`) | There is no CLI verb. Real feedback needs an OpenFeed source (account) and a sent row. |
| Read a chat turn: your message panel, the reply, tool rows, fire bands, notice strips, the replay and the chimes | `agent/channels/{cli-tui-core.ts,tui-theme.ts,tui-band.ts,tui-chime.ts,tui-first-frame.ts}`; `cmd/config-keys.ts` (`chat.sounds`) | [chat-transcript-layout.md](chat-transcript-layout.md) | 2026-10-30, branch `af153e835` (lane 18113, fake model: turn, tool row, approval card, fire and away bands, `/catchup`, replay, spinner plain and workspace, 71 columns) | Notice strips and chimes are unit-tested only; the OSC 11 blend was seen through tmux, not a real terminal. Not on main yet. |
| Chat in a split view with a watches/fires/paper/positions/calendar/usage sidebar | `agent/channels/{workspace-layout.ts,chord-menu.ts,sidebar/}`; `actions/system/sidebar-layout.ts`; `cmd/sidebar.ts`; `cmd/config-keys.ts` (`chat.workspace`) | [chat-workspace-tui.md](chat-workspace-tui.md) | 2026-10-29, main `32ca0d6c7` (lane 18103, fake model: frame, ctrl+x `b`, watch card, `om sidebar set`/`reset`, PAPER module, go-to-recent, exit history) | On main since #2182. Collapse, the narrow resize and a live model turn were last driven on the branch (2026-10-27/28). The panel picker and POSITIONS/CALENDAR/USAGE (#2195) were driven on a home copy on the branch (2026-10-29), not yet on a lane. |
| Open the registry welcome page (`om welcome`) | `cmd/welcome.ts`; `runner/packages/registry-contracts.ts` | [registry-welcome-and-search.md](registry-welcome-and-search.md) | 2026-10-28, main `a8fa10974` (real registry: "does not offer"; fixture: all three gate branches) | On main since #1947. The success path needs a registry advertising `welcome`, which production still did not on 2026-10-27, so it was proved against a fixture. |
| Get plain-language, personalised registry search results | `cmd/search.ts`; `runner/packages/search.ts` | [registry-welcome-and-search.md](registry-welcome-and-search.md) | 2026-10-28, main `a8fa10974` (fixture: `mode=nl`, `reasons`; with a key, `rank=for-you` + bearer; TTY text renderer with reasons lines) | Production still returns the old shape (no `nl` advertised). |
| Uninstalling or unfollowing tells the registry (receipt retraction) | `actions/packages/uninstall.ts`; `actions/watch/follow.ts`; `runner/packages/{retractions,use-receipts}.ts` | [registry-welcome-and-search.md](registry-welcome-and-search.md) (Gotchas) | live verification pending | Needs an account whose install or follow receipt returned an `edge`, plus a registry advertising `receipt_retract`. A guest never retracts. Signals are `[use-receipts]` log lines and `<home>/receipts/retractions.json`. |
| Finish `om init` by opening the welcome page (`--launch`) | `cmd/init.ts` | [registry-welcome-and-search.md](registry-welcome-and-search.md) (`init-closing`) | live verification pending | `om init` needs a TTY (exit 2 otherwise) and writes channel, credential and service state, so it is never driven on a lane. |
| Watch narrative (sentences, facets, entities from a recipe) | `packages/contracts/src/watch-narrative.ts` | **non-outcome** | n/a | A contracts library with no consumer in the CLI or dashboard at `ee8e3a7ab`, `8fe6a8432`, `a8fa10974` or `32ca0d6c7` (re-grepped 2026-10-29; only `packages/contracts/src/index.ts` exports it). Nothing renders it yet; re-check when one does. |
| Review a scheduled calendar occurrence | `actions/calendar/*`; `runner/calendar/blocks.ts` | [calendar-and-polling-windows.md](calendar-and-polling-windows.md) | 2026-10-28, main `a8fa10974` (occurrence, select, revise, reject, links, polling windows) | None. The window was not waited out to run. |
| Recover a challenged origin through a paid reader | `runner/firecrawl/*` | [firecrawl-first-block.md](firecrawl-first-block.md) | no-key path re-driven 2026-10-28, main `a8fa10974`; configured path pending | Needs `OM_FIRECRAWL_API_KEY` **and** a redirect of `api.firecrawl.dev/v2/scrape` to a fixture, together. |
| Create, import, Try, install, publish, adopt and revoke an agent | `packages/roster/src/http/roster-api.ts` (`imports/*`, `local-packages/*`, `builder`, `instances/:id/try`) | [agent-creator-lifecycle.md](agent-creator-lifecycle.md) (historical branch closeout) | live verification pending on main | On main since #1948 (`b50ca927d`), HTTP/GUI only. Needs an account, an LLM credential or coding brain, and the openmarket-chat Agents GUI (`verify-om-chat`). |
| Read agent work runs, refuse unknown runs, read roster health and measures | `cmd/{roster,roster-runs,roster-controls,roster-retry}.ts` (`OM_DEV=1`); `packages/roster/src/http/roster-work-api.ts`; `/healthz` `roster` | [agent-creator-lifecycle.md](agent-creator-lifecycle.md) (Guest lane on main) | 2026-10-28, main `a8fa10974` (empty runs, `not_found`/`malformed_body` refusals, roster list/measures, `/rpc/v1/roster/projects`) | Real runs, plan approval, steer and retry need an installed agent plus a model or brain. |
| Link a coding project and set its delivery | `cmd/project-{token,delivery,unlink}.ts` (`OM_DEV=1`); `/rpc/v1/roster/projects` | [agent-creator-lifecycle.md](agent-creator-lifecycle.md) (Guest lane on main) | refusal only, 2026-10-28, main `a8fa10974` (`project unlink nope` → `not_found`) | Needs a project linked through the GUI and a real forge token. |
| Drive persona and away operations from the web over remote control | `agent/channels/remote-control.ts`; `packages/rooms-client/src/remote-operation-routes.ts` (#2161) | unmapped | live verification pending | Needs `om agent remote enable`, the relay and a signed-in web client; nothing is guest-observable. |
| Compose a watch (or a set) from a natural-language ask | `actions/watch/watch-compose.ts`; `actions/watch/kit.ts` | unmapped | live verification pending | Needs an LLM credential; the single largest `om watch` entry point. |
| Share, follow, fork, install a watch; room shares and knocks | `actions/watch/{share,follow,fork,install,share-room,knocks,relay-door}.ts` | unmapped | live verification pending | Registry + account credential; a follower needs a second home. |
| Attach and arm steps (ai / tool / money) on a watch | `actions/watch/{action-add,action-remove,tools,run-now}.ts` | unmapped | live verification pending | Money steps are capital-gated; ai steps need a model credential. |
| Grow an existing watch with more sources | `actions/watch/{source-add,page-add,search-add,model-add,source-copy}.ts` | [watch-lifecycle-cli.md](watch-lifecycle-cli.md) / Maintenance verbs | timer source add/remove live verified 2026-10-28, main `a8fa10974` | Page, search, model and OpenFeed sources need a credential or account. |
| Repair or retry a watch broken for any non-origin reason | `actions/watch/{repair,retry,lane-retry}.ts` | [watch-lifecycle-cli.md](watch-lifecycle-cli.md) / Maintenance verbs | retry/repair on a healthy watch plus the `--rearm` and `lane retry` refusals live verified 2026-10-28, main `a8fa10974` | A genuinely broken watch is not constructible on a guest lane. |
| Read the wider journal surface: list, stats, chapters, search | `actions/watch/{journal-search,journal-stats,chapters,journal-list}.ts`; `cmd/event-journal.ts` | [watch-lifecycle-cli.md](watch-lifecycle-cli.md) (journal step) | 2026-10-28, main `a8fa10974` (`event-journal list`, `search`, `journal-stats`, empty `chapters`) | Populated chapters undriven (they need a model's summary fold). |
| See and reclassify rows the judge never reached | `actions/watch/unjudged-rows.ts`; `actions/watch/reclassify.ts` | [watch-lifecycle-cli.md](watch-lifecycle-cli.md) / Maintenance verbs | `unjudged` empty read and the `watch_reclassify_daemon_running` refusal live verified 2026-10-28, main `a8fa10974` | Real unjudged rows need an LLM daily cap; reclassify needs the daemon stopped. |
| Rewrite a fired row's recorded verdict | `actions/watch/synthesize.ts` | unmapped | live verification pending | Source says the verb is `om watch amend <watch> <event-id> --weight …` (`cmd/watch-engine-verbs.ts:1825`, `actions/watch/amend.ts`), not `synthesize`. It needs a topic lane and a streamed event. Not driven. |
| Move a watch between devices, mute a remote copy, restore one | `actions/watch/{move-here,move-readiness,mute,restore,adopt-here}.ts` | unmapped | live verification pending | Needs a second device/home for the interesting cases. |
| Read money-step execution history and digests | `actions/watch/{execute-history,execute-digest,execute-paper-reset}.ts` | [watch-lifecycle-cli.md](watch-lifecycle-cli.md) / Maintenance verbs | empty-state reads live verified 2026-10-28, main `a8fa10974` (`execute history/summary/list`, `watch execute history`) | Needs executed money steps. `om execute digest list` answered `unknown command 'digest'` on this lane, so the digest's CLI door is unresolved. |
| Session and device identity: sign-in state, rename/revoke devices, account email | `actions/auth/{status,relogin}.ts`; `actions/devices/*`; `actions/account/email.ts` | unmapped | live verification pending | Account credential; revoke is destructive. |
| Mint and revoke API keys | `actions/keys/{create,revoke}.ts` | unmapped | live verification pending | Account credential; security-tiered, revoke is permanent. |
| Pair and manage a notification channel | `actions/system/{channel-add,channel-home}.ts`; `runner/http/rpc/channel.ts` | unmapped (dashboard shell only) | live verification pending | Needs a real Telegram/Discord/Slack credential. |
| Read the daemon's own notification history | `actions/system/{notis-list,notis-get}.ts`; `cmd/notis.ts` | [local-reads-and-discovery.md](local-reads-and-discovery.md) | 2026-10-28, main `a8fa10974` (`notis --since 7d` rows) | `notis get` and `--after` paging undriven. |
| Inspect resolved config and the active key's claims | `actions/system/{config-show,config-key-info}.ts`; `cmd/config.ts` | [local-reads-and-discovery.md](local-reads-and-discovery.md) | 2026-10-28, main `a8fa10974` (`show`, `key-info`, `get`) | `config set`/`edit` undriven. |
| Upgrade the binary, migrate and restart | `actions/system/upgrade.ts` | unmapped | live verification pending | Risk tier 5, confirm-carded; must never run against a lane. |
| Read the subscription plan and pricing | `actions/system/upgrade-show.ts` | [local-reads-and-discovery.md](local-reads-and-discovery.md) / Plans | `upgrade --show` and `usage plans` live verified 2026-10-27 maintenance, main `8fe6a8432`; `subscriptions` refusal | `om subscriptions` refuses `account_required` for a guest. Buying and cancelling need an account. |
| Watch roster triage: what needs attention, one-click repair | `actions/system/{watching,watching-resolve-attention}.ts` | [watch-lifecycle-cli.md](watch-lifecycle-cli.md) / Maintenance verbs | `POST /rpc/v1/watch/overview` and MCP `watching_overview` live verified 2026-10-28, main `a8fa10974`; resolve-attention 409 refusal | A real attention item (daemon down, paused) was not seeded. |
| Read indicator and drawing schemas (catalog) | `actions/collab/{indicator-schema,indicator-list}.ts`; `cmd/chart.ts` | [chart-catalog-reads.md](chart-catalog-reads.md) | 2026-10-28, main `a8fa10974` (`indicator schema`, `indicator list`, `drawing schema`) | The `--chart`/`--workspace` forms and the `wrun/@scope/name/output` metric-id form are undriven. |
| Drive chart workspaces, indicators and drawings | `actions/collab/chart-*.ts`, `drawing-*.ts`, `indicator-*.ts` | unmapped | live verification pending | Needs a human's GUI chart tab open on a live collab session; a headless lane has nothing to submit to. |
| Backtest a strategy over historical bars | `actions/research/backtest*.ts` | [watch-lifecycle-cli.md](watch-lifecycle-cli.md) / Maintenance verbs (refusals) | `backtest spec` and `backtest run nope` refusals live verified 2026-10-28, main `a8fa10974` | A real run needs a watch with a strategy step (`watch create --from-candidate`); not driven. |
| Browse paid news feeds and read Fast-alerts billing | `actions/news/{feeds,billing,brief,voice}.ts`; `runner/http/rpc/news.ts` | unmapped (dashboard shell only) | live verification pending | Catalog browsing may be guest-ok; billing and follow need an account and a funded vendor relationship. |
| Agent memory: save, search and forget durable notes | `actions/memory/*.ts`; `cmd/memory.ts` | [mcp-stdio.md](mcp-stdio.md) / Hosted MCP | save → search → CLI `memory list` → forget live verified 2026-10-28, main `a8fa10974` over hosted MCP | The slug prefix must match the type (`memory_invalid_slug`). `memory_forget` ran with no approval card on loopback HTTP. |
| Author and compile a custom WASM indicator | `actions/wrun/{create,author,build,source-set,list}.ts`; `cmd/wrun.ts` | [local-reads-and-discovery.md](local-reads-and-discovery.md) (`wrun list`/`templates`/`create`) | 2026-10-29 scheduled maintenance, main `7ec575e55`: `wrun create --template feed-alert-line` scaffolded a workspace at scaffold 106 whose feed input reads `ref: "@you/your-feed"`, and the three Feeds starters' descriptions say "set ref to a feed you published" (#2194); templates still 91. Before that, 2026-10-29 nightly, main `32ca0d6c7` (templates still 91; scaffold 105, #2184). Before that, 2026-10-28, main `186030b63` (list; templates still 91, 30 `runsOn` lines read OPRA "at your own tier" after #2180; the stock `accumulate` 0.1.3 package listed) | `WRUN_SCAFFOLD_VERSION` is 106 since #2194 (`packages/sdk/src/wrun-sdk-sources.ts:1159`). A scaffold-105 workspace refreshes its kit texts once. Drive `wrun create` into a directory outside the product tree, because it writes wherever the positional `[dir]` points. `wrun validate` is undriven; `wrun build` compiles and installs deps, so it needs package-manager access. |
| Arm and tune a live managed-strategy wallet | `cmd/managed.ts` over `actions/managed/*.ts` factories (CLI-only: not in the action registry) | unmapped | live verification pending | Capital-reaching: funded venue wallet plus an explicit arm gate. Out of reach for a guest lane. |
| Place and manage real venue orders; wallet and execution | `cmd/{order,execute,buy,hyperliquid,polymarket}.ts`; `actions/{execute,orders,hyperliquid,wallet,polymarket}/` (`actions/execution/` does not exist) | unmapped | live verification pending | Real money. Needs a funded account and a safe plan; nothing attempted. |
| Reach the capability layer over MCP (stdio) | `cmd/mcp.ts`; `mcp/server.ts`; `mcp/capital-gate.ts` | [mcp-stdio.md](mcp-stdio.md) | 2026-10-28, main `a8fa10974` (handshake, 451 tools, a read, `capital_yolo_harness` under a bypass-mode driver) | `om mcp arm`, `--catalog operator` and `--session merged` undriven. |
| Reach the capability layer over hosted MCP (HTTP) | `mcp/http.ts` | [mcp-stdio.md](mcp-stdio.md) / Hosted MCP over loopback HTTP | loopback `mcp serve --http` live verified 2026-10-28, main `a8fa10974` (441 tools) | Non-loopback badge auth and `OM_LOOPBACK_AUTH=1` were not driven. |
| Run the hosted chart MCP against Mongo: boot, health, readiness, index rebuild, refusals | `packages/cli/src/hosted/{main,run,config,tenant-store-mongo,tenant-store-health}.ts` | [hosted-chart-mcp-tenant-state.md](hosted-chart-mcp-tenant-state.md) | 2026-10-28, main `a8fa10974` (boot lines, health pair up/down/back, rebuild, four refusals, `--help`) | The tool-call path needs an operator API key on the production gateway; the env-gated suite passed 7/7 on 2026-10-28 once the role also had `readWrite` on `om_hosted_test` (without it the suite fails `Unauthorized`). |
| Publish, install and manage registry packages | `cmd/{packages,publish,install}.ts`; `actions/packages/*` | partially via agent-creator (itself unverified) | live verification pending | Registry credential; `package_delete` is irreversible. |
| Approve an arming or model edit from the dashboard | `runner/http/rpc/{watch-arm-review,watch-edit-review}.ts` | [watch-lifecycle-cli.md](watch-lifecycle-cli.md) / Maintenance verbs (refusal) | `arm-confirm` refusal (400 `approval_expired`) live verified 2026-10-28, main `a8fa10974` | The happy path needs a watch with a money or ai step awaiting approval. |
| Sealed secrets bridge | `runner/http/rpc/secrets.ts` | [local-reads-and-discovery.md](local-reads-and-discovery.md) / Secrets status | `GET /secrets/status` live verified 2026-10-27 maintenance, main `8fe6a8432` (200, guest `readiness: unminted`) | Minting, recovery and rooms use need an account. |
| Social chat: rooms, DMs, topics, docs, moderation | `actions/rooms/*` (190); `cmd/room.ts` | **out of scope here** | n/a | Owned by `verify-om-chat` per this repo's boundary rules; this repo holds only the protocol surface and daemon-side actions. Recorded so the gap is not mistaken for an omission. |
| Standalone `/paper` dashboard route | `apps/dashboard/src/paper-plane.tsx` | **non-outcome** | n/a | Mounts only when `strategyRoutes === null` (the OSS export). Unreachable in any lane `control-om` drives; reach Paper via the `/strategies` tab. |
| Review pending approvals from the CLI (`om approvals list\|approve\|deny`) | `cmd/approvals.ts`; `cmd/approve-chain.ts`; `runner/http/approvals-routes.ts`; `main.ts:73` | [local-reads-and-discovery.md](local-reads-and-discovery.md) / Guest-lane reads | list live verified 2026-10-28, main `a8fa10974` (`approvals list` printed `No pending approvals.`, `--format json` printed `[]`, and `GET /rpc/v1/approvals` returned `{"approvals":[]}`) | Approve and deny need a pending item and a human terminal, so they are not driven. |
| Sign in or out, connect an LLM or coding agent from the CLI (`login`, `logout`, `llm`, `auth`, `setup`, `connect`, `disconnect`) | `main.ts:78,83,134,~140` | unmapped | live verification pending | Needs an account, a provider key or a TTY. |
| Wipe, export/import or upgrade the local store (`om reset`, `om migrate`, `om upgrade-db`) | `main.ts:202,219,222` | unmapped | live verification pending | Destructive; only on a scratch lane root. |
| Read and steer Away coverage over local HTTP (`/api/away`, `/coverage`, `/sessions`, `/activity`; `POST` `/policy`, `/arm`, `/control`) | `runner/http/away-api.ts:16,55-96`; gate in `runner/http/rooms-routes.ts:85-98` | [local-reads-and-discovery.md](local-reads-and-discovery.md) / Guest-lane reads (refusal) | refusal live verified 2026-10-28, main `a8fa10974` (`GET /api/away` and `/api/away/coverage` returned 401 `operator_required`) | The reads need operator proof even on loopback: the per-boot GUI session cookie, or a configured runner or desktop token. `/policy` is a `POST`, not a read. `arm` is unsafe. The GUI side belongs to verify-om-chat. |
| Library and persona over local HTTP (conflicts, proposals, persona use/import/learn/sync) | `runner/http/library-api.ts:163-178`; `cmd/rooms-commands.ts` | unmapped | live verification pending | Probably needs rooms; the UI side is verify-om-chat's. |
| Read the follows feed (`om follows`) | `cmd/follows.ts`; `actions/follows/{list,show,feed,review}.ts` | [local-reads-and-discovery.md](local-reads-and-discovery.md) / Guest-lane reads | empty list and refusal live verified 2026-10-28, main `a8fa10974` (`follows` returned zero `summary` counts; `follows show @nobody/nothing` exited 2 with `not_following`) | A populated feed needs a followed share, which needs a registry and an account. `om follow review` prompts for confirmation. |
| Stream live data over WebSocket (`om subscribe`) | `main.ts:196` | unmapped | live verification pending | Not driven; probably needs an API key with stream entitlement. |
| Send a one-shot message to a channel (`om send`) | `cmd/send.ts` | unmapped | live verification pending | Needs a paired channel. |
| Trace a shared alert's fires hop by hop (`om relay`) | `cmd/relay.ts`; `main.ts:212`; `runner/stream/relay-diagnostics.ts` | [local-reads-and-discovery.md](local-reads-and-discovery.md) / Guest-lane reads (refusals) | refusals live verified 2026-10-28, main `a8fa10974` (`relay trace @nobody/nothing` gave `relay_ref_unknown`; a malformed ref gave `relay_ref_invalid`; both exit 2) | A real trace needs a live-shared watch. |
| Nervous system: autonomous chart moments from fires (`om nervous`) | `cmd/nervous.ts`; `actions/collab/nervous-status.ts` | [local-reads-and-discovery.md](local-reads-and-discovery.md) / Guest-lane reads | 2026-10-28, main `a8fa10974` (`nervous status` showed `enabled: true` and a `watch_fired` receipt for the lane's own ingest fire, "no canvas resolved"; MCP `nervous_status` matched) | A chart moment that lands needs a GUI chart tab. |
| Run research studies (`om research`) | `main.ts:204`; `cmd/research.ts`; `actions/research/*` (10 actions besides backtest) | [local-reads-and-discovery.md](local-reads-and-discovery.md) / Guest-lane reads | `study --locate-only` live verified 2026-10-28, main `a8fa10974` (occurrences for an inbound watch; `--watch nope` gave `watch_not_found`) | A full study fetches candles and was not run. `search-files` and `make-image` spend on a model and need one. |
| Open the dashboard or desktop app setup from the CLI (`om dashboard`/`open`, `om app`, `app-setup`, `om claude`) | `cmd/apps.ts`; `cmd/app-setup.ts`; `main.ts:67,69` | unmapped | live verification pending | `dashboard`/`open` launch a browser; not driven on a lane. |
| Keep watchlists (`actions/watchlists/{index,local}.ts`) | `actions/watchlists/`; `actions/collab/collab-rest.ts:65-81` | [mcp-stdio.md](mcp-stdio.md) (refusal) | refusal live verified 2026-10-28, main `a8fa10974` (MCP `watchlist_list` gave `missing_api_key`: guest keys have no workspaces) | There is no CLI verb. The MCP and agent tools need an account. |
| Create, list, edit, pause, resume and remove a watch from the CLI | `cmd/watch-engine-verbs.ts`; `actions/watch/{create,edit,pause-resume,remove,list,show}.ts` | [watch-lifecycle-cli.md](watch-lifecycle-cli.md) | 2026-10-28, main `a8fa10974` (create, edit with `--label`, pause printing the slug, a `watch show` card with the label, resume, remove) | Row added 2026-10-28; the guide predates it. |
| Push an event and see it fire on the door, the stream, the journal and the dashboard | `runner/http/ingest*`; `/events/v1`; `cmd/event-journal.ts` | [event-ingest-and-fire.md](event-ingest-and-fire.md) | 2026-10-28, main `a8fa10974` (202 with one `event_id` on all three stream events and in the journal; an unauthenticated push got 401) | Row added 2026-10-28. |
| See the daemon's dashboard: Overview, Watches, News, Strategies, Channels, Venues and Receipts | `apps/dashboard/src/{app.tsx,pages/*}` | [ops-dashboard.md](ops-dashboard.md) | 2026-10-28, main `a8fa10974` (onboarding on a fresh lane, nav, every route's headings and empty states, the `/strategies/<unknown>` flicker) | Row added 2026-10-28. A populated strategy page needs a strategy, a signal and a venue. |
| Author a watch in the dashboard (`Create watch`) | `apps/dashboard/src/` watch-create flow | [watch-authoring-ui.md](watch-authoring-ui.md) | 2026-10-28, main `a8fa10974` (RSS kind through review to `/alerts/ui-authored-feed`, a paused watch on `watch show`, polls after resume) | Row added 2026-10-28. The other seven kinds were listed, not authored. |
| Ask the dashboard agent; open the `/agent` workspace | `apps/dashboard/src/` agent panel; `/agent` route | [agent-panel.md](agent-panel.md) | refusal live verified 2026-10-28, main `a8fa10974` (the `No LLM API key configured.` alert, `Check connections`, the `/agent` rail) | A reply needs an LLM credential. Row added 2026-10-28. |
| A challenged host holds every source on it: one probe per window, then the window doubles | `runner/fault-episodes.ts`; `runner/subscriptions/*`; `shared/public-document.ts` | [origin-challenge-backoff.md](origin-challenge-backoff.md) | 2026-10-28, main `a8fa10974` (hold; one still-challenged probe at `until`; 15 min doubled to 30; recovery at the doubled `until` with `reopened after the window` and `/healthz` `open`) | Row added 2026-10-28. During a long hold the status rows stop naming the challenge (product gap below). |
| Default agents arrive from `@om-core` registry packages after boot | `packages/roster/src/plugins/om-skills-defaults.ts`; `runner/roster-host/registry.ts` (#2167, #2169, #2183) | [agent-creator-lifecycle.md](agent-creator-lifecycle.md) / Default agents | install live verified 2026-10-29, main `32ca0d6c7` (`installed 8 package(s)` about 5 s after boot; `roster list` showed six registry agents at 1.0.0). The 404 retry path was driven 2026-10-28 under the old `@om-skills` scope | The six-hour maintenance pass and a withdrawal (410) are undriven. |
| A strategy-package watch holds its queued position, bounds its opening legs, and pages and digests each leg on paper | `runner/watching/steps/target-step.ts`; `runner/paper/{target-sink,target-pager,target-episodes,exit-lane,notices,digest}.ts`; `packages/contracts/src/target-step.ts` (#2176, #2188, #2192) | unmapped | live verification pending | #2188 adds `admit.drift_frac`, `admit.max_event_age_secs` and `cooldown` (opening legs only), with arm-card facts and chain digest version 5. #2192 adds `Paper <acct> · opened/adjusted/closed` notices, `Step:` rows in the digest, `PAPER` rows in `watch execute history`, and research `admission_not_modeled`. All of these need a target step fed by an `ai` producer (a model) and an arm. Offline coverage: `test/paper-target-sink.test.ts` and `test/watch-target-chain.test.ts`. |
| See what's new in plain `om chat` and turn it on in one press | `agent/channels/whats-new-card.ts`; `shared/whats-new{,.generated}.ts`; `cmd/config.ts` (`writeWhatsNewSetting`) | [chat-workspace-tui.md](chat-workspace-tui.md) / `whats-new-card` | 2026-10-29, main `32ca0d6c7` (card on a fresh lane; ctrl+x rows `w`/`x`; `w` set `chat.workspace on` and reopened as a workspace) | Dismiss (✕ or ctrl+x `x`), paging with several entries, and the 60-day expiry were not driven. |

### Known product gaps (reported, not map drift)

- **New 2026-10-29 (`7ec575e55`), possible gap:** #2194's CHANGELOG says
  every workspace's `scripts/wrun-prebuild.mjs` drops internal round and
  program notes. A workspace scaffolded by `om wrun create` at scaffold 106
  still carries nine of them, for example `WRUN-OFFCHART round 2 G`. They are
  copied from `packages/sdk/src/wrun-slots.ts` and `wrun-style/widgets.ts`.
  The new vocabulary gate (`assertNoInternalVocabulary`) scans only the
  browser kit bundle's files (`gen-indicator-kit-bundle.ts:253-260`), not the
  CLI's scaffold. Whether the CLI path is in #2194's scope is the operator's
  call.
- **New 2026-10-29 (`32ca0d6c7`):** the dashboard Overview's `Watch fires`
  tile (`Since the daemon started`) read `0` after two inbound fires landed on
  the lane, both on the stream and in the journal. The tile reads `/healthz`
  `alerts_fired_total` (`apps/dashboard/src/pages/overview.tsx:69`), which
  counts condition-alert fires only. So a home whose watches are all inbound or
  feed watches always reads zero there.
- **Resolved 2026-10-29:** the default agents now install on a fresh home from
  production (`@om-core`, #2183). The 2026-10-28 `@om-skills` 404 below is
  history.
- **Re-observed 2026-10-29:** `om tenors` still returns 500 `server_error`,
  and profiler `start` still says `already: false` on a second start.

- **New 2026-10-28 (maintenance, `186030b63`):** `om doctor` reports
  `api_key: ok` ("Data API key configured") for an expired guest key. On a
  lane home from the previous day, `config key-info` said `"expired": true`
  (`expireAt` an hour after issue) while `coins`, `exchanges` and `points`
  returned `api_key_invalid` (401). The credential keeper's re-mint also failed
  for the run (`guest token refresh has failed for ~3m`), during a guest
  sign-in 429 window. The check reads presence, not validity, so a user whose
  guest key lapsed is told everything is fine. `control-om doctor` now reads
  the expiry itself (harness side).
- **Also seen 2026-10-28:** on a 60 s feed the challenge row is displaced
  after 3 minutes, not 12. See the next item and
  [origin challenge](origin-challenge-backoff.md).
- **New 2026-10-28:** the `exchange_id` domain lags the live venue set. `om
  exchanges` lists 48 venues on `auto`, including `LIGHTER`, `VARIATIONAL` and
  `VARIATIONAL_SWAP`, and `om markets --exchange LIGHTER` returns rows. But
  `enum --domain exchange_id` holds 35 values and finds none of those three.
  MCP `markets` with `exchanges:["LIGHTER"]` is refused with `"LIGHTER" is not
  a valid exchange_id`. So an agent cannot address venues the CLI reads. #2175
  bumped the contract and left tool schemas unchanged. Driven at `a8fa10974`.
- **New 2026-10-28:** during a challenge hold, the status rows stop naming the
  challenge once the held source is overdue. The rows were read 12 minutes
  into a 15-minute hold:
  - `watch show` FAULT read `source broken · 127.0.0.1`.
  - The source row and `watch list` read `not checked since … · expected every
    1 min · om watch run now <slug>`. That is the `source_stale` branch
    (`runner/watching/status-sentence.ts:4680`, `fetchFix`).
  - Only the `Error:`/`Cause:` lines still said `127.0.0.1 is challenging this
    machine`.
  So the fix offered is a fetch that the hold refuses, and the Firecrawl offer
  is gone. Driven at `a8fa10974`.
- **New 2026-10-28:** the default agents are not on the production registry
  yet. A fresh home on main installs no default agents, and its daemon log
  carries a `[roster] om-skills defaults unavailable (registry lookup failed
  (404) … @om-skills/argue …)` ERROR on every retry. The bundled snapshot that
  #2169 removed was the old source. The first publish waits on the
  `om-skills-packages-publish` workflow (#2168). Ship that before the next
  release.
- **New 2026-10-28:** `om tenors` returned `server_error` (HTTP 500) three
  times, with and without `--exchange DERIBIT`. It is a service-side fault.

- `om series publish <name> --dry-run` (and so a real publish) is refused by the registry: `publish_rejected`, "kind 'live-series' is not accepted by the v1 registry". Live series authored locally cannot be published. Driven 2026-10-27 at `8fe6a8432` (second pass).

- `POST /rpc/v1/system/profile` `{"action":"start"}` always answers
  `already: false`, even when the profiler is already armed. A second start
  returns the FIRST `started_at` with `already: false`
  (`runner/http/rpc/system.ts:403`). Driven 2026-10-27 at `8fe6a8432`; re-observed 2026-10-28 at `a8fa10974`.
- `/strategies/<unknown>` **flickers** between `No strategy named <slug>. Back to
  Strategies.` and `Loading…` on a ~12 s cycle. Re-observed 2026-10-27 at
  `8fe6a8432` and 2026-10-28 at `a8fa10974`, with the same cadence (`Loading…`
  at 12 s and 24 s). A source hypothesis, not proved: `useStrategy`
  (`lib/strategy-client.ts:67`) polls every 3 s with the global `retry: 1`.
  A refetch of a query with no data may reset it to pending, so `Loading…`
  shows until the 404 returns. Passing `retry` as a function that refuses a
  404 would settle it. Driven 2026-10-26 at
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
