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
- [Chat transcript layout](./chat-transcript-layout.md) — on main since #2217 and #2219 (v0.480.0): your message as a clay-barred panel, unlabelled replies wrapped at the pane less a 2-column margin, warm bands for fires and digests, faint notice strips, replay identical to live, the spinner above the composer, and the chimes (`chat.sounds`). It needs a local fake model that streams tool calls, and the recipe carries one.
- [Chat workspace TUI](./chat-workspace-tui.md) — on main since #2182 (v0.467.0): `om chat --workspace`, the sidebar (WATCHES, FIRES, PAPER, POSITIONS, CALENDAR, USAGE, up to 3 on, dotted rules), the ctrl+x menu and its panel picker, scrolling cards with `o` open (#2207), a click on a transcript fire card (#2225), health-coloured watch dots (#2219), `om sidebar`, and the What's new card in plain `om chat`. It needs a local fake model, and the recipe carries one.

- [Hosted chart MCP: tenant state, health and readiness](./hosted-chart-mcp-tenant-state.md) — the
  `om-chart-mcp` binary on an agent port against a local Mongo: boot lines,
  `/healthz` vs `/readyz`, index rebuild, refusals; the tool-call path over
  the production gateway stays unverified without an operator key.

Not yet mapped, and worth adding when a change touches them: the hosted MCP
tool calls over the production gateway (`chart_*` with a real key), the chart workspace mutations (`om chart` add,
update, remove and drawings, which need a GUI chart tab), the rest of the `om chat` TUI (a real model's turns, slash commands, panels),
packages and the registry, and the execution/venue verbs.


## Surface inventory

Nightly maintenance, **2026-10-31**, against **origin/main `dfefe0a21` (v0.480.2)**, 17 commits past `3cb50a821` (an ancestor). The census:

- **Commands:** `main.ts` has no diff, so the count is unchanged.
- **Actions:** 482 registered, two more than before: `file_create` (research, #2218/#2221, replacing `document_draft`) and `channel_default_set` (system, #2220). `docs/TOOLS.md` lists 480. MCP stdio lists 454 tools.
- **Unchanged:** 30 RPC files and 9 dashboard routes. `apps/dashboard/src` and `runner/http/rpc` have no diff.
- **Scaffold:** `WRUN_SCAFFOLD_VERSION` is still 106.

User-facing changes:

- #2217 and #2219 rewrite the `om chat` transcript (the user panel, no labels, warm bands, the spinner above the composer, one palette, `chat.sounds`) and colour the sidebar dots by health; #2225 opens a transcript fire card on click. All three were first proved on branches and are now on main.
- #2202 (v3 eval triage): unknown metric params are refused by name, `metric_get`/`metric_series` take a bare coin with a `listing_note`, `BYBIT_FUTURES` aliases to `BYBIT` at schema parse, `exchanges` carries reply guidance for unselectable venues, `market_resolve` compares numbers by value.
- #2218/#2221: `file_create` writes `<OM_HOME>/documents/` (`scratch`) or Downloads; `document_draft` is gone.
- #2220: `channel_default_set` and `om setup default --force`.
- The rest is rooms-client ticket work (#2226 to #2230, owned by verify-om-chat) and the forex 17:00 day (#2215, a chart host).

Live this pass, on lane 18163 with a fake model on 18164 and the origin stub on 18166, host load average about 1.6. The first `up` died: a guest sign-in 429 (`Try again in 51 minute(s)`) left the home keyless and the daemon exited after its banner, on this tree and on `3cb50a821` alike (a new product gap, below); the pass waited the window out and booted at 04:13.

- **Driven before the boot, on the lane home:** the key-free local reads (`config`, `chat.sounds`, `setup default`, `enum`, `schema read`, `skill list`, `wrun templates`, `upgrade --show`, `chart indicator schema`) and MCP stdio (454 tools, `file_create` scratch, `channel_default_set` refusal, `document_draft` gone, `order_place`).
- **Driven after the boot:** the fire chain (door, stream, journal, CLI push, dashboard row); watch create/edit/show/pause/resume/remove with the lot fields; the repair and backtest refusals; the journal reads; #2202 on the CLI and over MCP; every dashboard route, the Paper tab, the `/strategies/<unknown>` flicker, the agent panel refusal, and the RSS authoring flow through to a resumed feed polling the stub; origin challenge steps 1-3; paper, calendar, chart catalog, registry, notis, vault, openapi, research locate, nervous, secrets, away; the default agents; plain `om chat` (What's new, a tool turn, 90 columns) and `om chat --workspace` (the fire-card click on main, dot colours, the panel picker).
- **New product gaps:** the keyless-boot exit; `file_create` `downloads` over stdio never answers; CLI `points --exchange BYBIT_FUTURES` is refused.
- **Not re-driven:** Firecrawl (a stale citation was fixed from source), hosted chart MCP, the agent creator beyond `roster list`, the chat approval card and replay, the 20-fire card scroll, `om sidebar set`, hosted MCP over HTTP, `instruments`/`option-chain` under v3, `follows`, `series`, `usage plans`.

Evidence: `http://127.0.0.1:8098/vom-nightly-20261031/r1/` (24 frames plus `cli/` transcripts, `events.sse` and the TUI captures).

Scheduled maintenance, **2026-10-30**, against the same **origin/main `3cb50a821` (v0.478.0)** as the nightly. The host's load average was about 140, but CLI calls answered in seconds, so this pass re-drove every guide on a fresh lane at 18165. The second half ran with the loopback switch, the origin stub on 18166 and a fake model on 18167.
- **Source:** two read-only readers ran. A census from new angles (the `main.ts` names absent from this table, non-RPC HTTP routes, TUI slash commands) found seven outcome groups with no row, added at the bottom of the table. A diff audit of the six guides the last two passes skipped found one stale citation (Firecrawl `status-sentence.ts:2498` → `:2550`).
- **First driven on main:**
  - the origin-challenge hold and recovery (steps 1-3 and the reopen at `until`; the doubling was not re-driven);
  - the hosted chart MCP refusals;
  - the chat workspace CALENDAR and USAGE panels and the What's new `x` dismiss;
  - `vault status`, `terms`, `symbols`, `normalized-symbols`, `block-sizes` and `/openapi.json`.
- **Re-driven:** every other guide at smoke depth or better.
- **Busy-host gap:** CLI `event push` delivered through the daemon this time, so the nightly's `direct` write did not recur at this load.
- **Evidence:** `http://127.0.0.1:8098/verify-om-maint-20261030/r1/` (16 frames plus `cli/` transcripts). It was published with the timeout raised, because the renderer answered slowly. A mechanical count of the status cells gives 87 rows, approximately: 31 fully live verified, 25 partly verified (refusal, empty-state or a pending sub-outcome), 28 pending, and 3 non-outcome or out of scope. 24 rows are `unmapped`. These counts include the branch-only chat transcript row published earlier the same morning. The table before this pass gave 80 / 28 / 23 / 26 / 3 by the same counter.

Nightly maintenance, **2026-10-30**, against **origin/main `3cb50a821` (v0.478.0)**. That is 27 commits past `7ec575e55`, which is an ancestor. The census:

- **Commands:** `main.ts` has no diff, so the count is unchanged.
- **Actions:** 480 registered, one more than before: `doc_patch` (#2191, rooms). `docs/TOOLS.md` lists 478. MCP stdio lists 452 tools.
- **Unchanged:** 30 RPC files and 9 dashboard routes. `apps/dashboard/src` and `runner/http/rpc` have no diff.
- **Scaffold:** `WRUN_SCAFFOLD_VERSION` is still 106.

User-facing changes:

- #2195, #2198 and #2207 add the panel picker, the dotted panel rules, card scrolling and `o` open to the chat workspace. They were first proved on branches and are now on main.
- #2208 adds the target-step stop breaker, with its backtest flags `--max-stops`, `--window-secs` and `--max-loss-usd`.
- #2201: a target lot now follows the entry.
- `held_lots` on `watch_pause` and `paper_lots_left` on `watch_remove`.
- #2206: the agent run ceiling is 500 calls, and `agent.max_tool_calls` is capped at 249.
- #2205: a dropped web-chat stream settles its open approval card.
- #1702: `ActionError.kind` is internal only and kept off the MCP and CLI payloads.
- #2191: `doc_patch` (rooms, owned by verify-om-chat).
- The rest is roster backoff and wrun/SDK chart-host work.

Live this pass, on lane 18163 with a fake model on 18164, at smoke depth or better. The host's load average was near 150 from other sessions. Each source CLI call took 1 to 3 minutes, and `/healthz` took 2 to 3 s, which the CLI's probe reads as down. That produced a product gap (below), and it limited coverage.

- **Driven:**
  - the fire chain: the door, the stream, the journal and the dashboard;
  - watch create, edit, pause, resume and remove, with the new lot fields;
  - the three breaker refusals;
  - the config cap;
  - MCP stdio;
  - every dashboard route;
  - the chat workspace on main: rules, picker, POSITIONS empty state, card foot, `o` and Esc;
  - paper, calendar, coins, exchanges, enum, welcome, the indicator schema and wrun templates.
- **Not re-driven:**
  - origin challenge and Firecrawl;
  - hosted chart MCP;
  - the agent creator;
  - watch authoring UI;
  - the What's new card;
  - most maintenance verbs and journal reads.

Evidence is local only. The device-owned `8098` renderer held its port but answered nothing within 10 s, so nothing was published. The evidence is in `artifacts/vom-nightly-20261030/r1/` in the run's product worktree, `~/github/openmarket-internal-verify-om-nightly-20261030`.

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
| Check the install: doctor, status, logs | `cmd/{doctor,status,logs}.ts` | [daemon-lifecycle-and-health.md](daemon-lifecycle-and-health.md) | 2026-10-31, main `dfefe0a21` (doctor `ok:true`, `status` running, `service status` foreground, `logs` empty, the wrapper's `service install` refusal; the first `up` died on a guest 429, see the README gap); 2026-10-30 scheduled maintenance, main `3cb50a821` (doctor 14 checks, `status` running, `/healthz`). 2026-10-29, main `32ca0d6c7` (14 doctor checks, status, service status) | None. |
| See the daemon's footprint and slow statements; profile a stalled daemon | `runner/http/server.ts:1546`; `runner/db-timing.ts`; `runner/http/rpc/system.ts` (`profile`) | [daemon-lifecycle-and-health.md](daemon-lifecycle-and-health.md) (`profile`, footprint step) | 2026-10-31, main `dfefe0a21` (`stacks` before a start → 409 `not_started` only); 2026-10-28, main `a8fa10974` (`memory`/`slow_sql`/`roster` on `/healthz`; profiler 409/400/200/stacks) | No real slow statement was produced (`OM_DB_SLOW_MS=1` plus a restart would). `start` always says `already:false` (product gap). |
| Look up enum domains, schema intents and bundled skills | `cmd/{enum,schema,skill}.ts`; `packages/sdk/src/types/enum-domains.ts` | [local-reads-and-discovery.md](local-reads-and-discovery.md) | 2026-10-31, main `dfefe0a21` (`enum --list` 26 domains, `enum --domain exchange_id` still 35 values and lists neither `BYBIT_FUTURES` nor `BYBIT_LINEAR`, which #2202 aliases at parse time only; `schema read`, `skill list`); 2026-10-28, main `a8fa10974` (`enum --list`/`--domain`, `schema read`, `skill list`) | `schema read <intent>` and `skill show` undriven. |
| Connect an AI provider or coding agent from the dashboard | `apps/dashboard/src/pages/connections.tsx`; `runner/http/integrations-api.ts` | [ops-dashboard.md](ops-dashboard.md) (Connections) | 2026-10-28, main `a8fa10974` (read-only) | Pressing `Connect` rewires the operator's real coding agents, so it is never driven from a lane. |
| Publish and read live series snapshots | `cmd/series.ts`; `docs/LIVE-SERIES.md` | [local-reads-and-discovery.md](local-reads-and-discovery.md) / Series | local create/list/show live verified 2026-10-27 maintenance, main `8fe6a8432`; publish refused | `series publish --dry-run` with the lane's guest key reached the registry and got `publish_rejected`: kind `live-series` is not accepted by the v1 registry. Real publish and remote read are pending, and possibly blocked by the registry (reported). |
| Resolve a phrase to venue fields; screen and chart metrics | `cmd/{resolve,metric,markets,tenors}.ts`; `runner/metric-params.ts` (`refuseUnknownMetricParams`); `shared/default-listing.ts` (`listing_note`, `unknownSymbolReasons`); `contracts/src/watch-condition.ts` (`unknownParamMessage`) | [market-data-reads.md](market-data-reads.md) / Resolve, metrics and markets | 2026-10-31, main `dfefe0a21` (#2202: `metric get` unknown param → `invalid_query` naming what it takes; bare `--symbol BTC` with no `--exchange` → Binance plus `listing_note`; `metric series` keeps `--exchange` required; `--exchange BYBIT_FUTURES` aliases to `BYBIT` on `metric get` and on MCP `points`/`metric_get`, not on CLI `points`; `AAPL` on `POLYGON` → `venue_not_served`; `resolve "bitcoin dip to 55000"` ranks the 55000 leg first; `markets --exchange LIGHTER` rows; `tenors` still 500); 2026-10-30 scheduled maintenance, main `3cb50a821` (`resolve BTC`, `metric list`, `markets --exchange LIGHTER`; `tenors` still 500); 2026-10-28, main `a8fa10974` (`resolve BTC`; `metric list`, `get`, `series` and `screen`; `markets`, including `--exchange LIGHTER`) | `tenors` returned `server_error` (500) on every attempt, with and without `--exchange DERIBIT`. That is a service fault, so tenors stays unproven. |
| Open a local paper-trading account and read its book | `actions/paper/*.ts`; `runner/http/rpc/paper.ts`; `runner/paper/digest.ts` | [paper-accounts.md](paper-accounts.md) | 2026-10-31, main `dfefe0a21` (create, ls, digest text; the Paper tab row); 2026-10-30 scheduled maintenance, main `3cb50a821` (create, ls, digest); 2026-10-29, main `32ca0d6c7` (create/ls, the Paper tab, and `paper digest` all-accounts and per-account with the new `Steps: none` lead; show/log/set/reset on 2026-10-26) | Open/close/reset-all/`digest-set` and the scheduled edition undriven. Step rows in the digest need a target step. |
| List a venue's instruments and read an options chain | `cmd/instruments.ts`; `cmd/option-chain.ts`; `actions/data/{instruments,option-chain}.ts`; `runner/v3/` | [market-data-reads.md](market-data-reads.md) (Gotchas) | 2026-10-28, main `a8fa10974` (default refusal; v3 rows and expiries; `exchanges` under v3 returned 30 venues, against 48 on `auto`) | Needs `OM_DATA_TRANSPORT=v3` on the CLI call (`OM_DATA_V3_URL` too if the home sets `OM_BASE_URL`); the default transport exits 2 `invalid_query`. The daemon's `counters.symbol_directory_*` (#2173) were not read: that needs `OM_DATA_TRANSPORT=v3` on `up`. Typed-door reads added by #2114 (fx/index candles, ETF flow, FRED) are undriven. |
| Read and clear model-provider plan holds (`usage plans`) | `actions/data/usage-plans.ts`; `cmd/usage.ts` | [market-data-reads.md](market-data-reads.md) (Gotchas) | 2026-10-26, main `ee8e3a7ab` (guest: empty `providers`) | Corrected: this reports MODEL provider plans and holds, not Data API tiers. Populated rows, `--refresh` and `--clear` need a signed-in model provider. |
| Give 👍/👎 feedback on an openfeed alert; a new feed sends today's top 3 | `actions/watch/feedback.ts`; `openfeed/{feedback*,first-look}.ts` | [mcp-stdio.md](mcp-stdio.md) / Hosted MCP (refusal) | refusal live verified 2026-10-28, main `a8fa10974` (`watch_feedback` over MCP: `watch_feedback_not_openfeed`) | There is no CLI verb. Real feedback needs an OpenFeed source (account) and a sent row. |
| Read a chat turn: your message panel, the reply, tool rows, fire bands, notice strips, the replay and the chimes | `agent/channels/{cli-tui-core.ts,tui-theme.ts,tui-band.ts,tui-chime.ts,tui-first-frame.ts}`; `cmd/config-keys.ts` (`chat.sounds`) | [chat-transcript-layout.md](chat-transcript-layout.md) | 2026-10-31, main `dfefe0a21` (lane 18163, fake model: What's new, a tool turn with the user panel at column 3, a 5-column gutter, the tool row, the list and code block, no `Worked for`, the away band, 90-column re-wrap, exit history). Before that, 2026-10-30 on branch `af153e835` (approval card, fire and away bands, `/catchup`, replay, spinner, 71 columns) | Not re-driven on main: the approval card, replay, the spinner frame, notice strips and chimes (unit-tested). The OSC 11 blend was seen through tmux, not a real terminal. |
| Chat in a split view with a watches/fires/paper/positions/calendar/usage sidebar | `agent/channels/{workspace-layout.ts,chord-menu.ts,sidebar/}`; `actions/system/sidebar-layout.ts`; `cmd/sidebar.ts`; `cmd/config-keys.ts` (`chat.workspace`); `runner/watching/status-sentence.ts` (`lateOnly`) | [chat-workspace-tui.md](chat-workspace-tui.md) | 2026-10-31, main `dfefe0a21`: `fire-card-click` on main (#2225: the card level with the clicked row at the transcript's right edge, Esc, `o` to the watch page, column 138 with the sidebar hidden, `no longer stored` after `watch remove`), the #2219 dot colours (green fired, red broken, grey paused), the ctrl+x `p` picker at `2 of 3 on`, and the What's new `x` dismiss. 2026-10-30 scheduled maintenance, main `3cb50a821`: the ctrl+x `p` picker took CALENDAR to `3 of 3 on` (lit panels re-sort to the top), and `om sidebar set watches calendar usage` showed `▾ CALENDAR nothing scheduled` and `▾ USAGE $0 · 24h` (then a fake-model row). 2026-10-30, main `3cb50a821` (lane 18163, fake model). The dotted rules (#2198), the ctrl+x `p` picker to `3 of 3 on` with dim rows (#2195), POSITIONS `none open` / `○ no venue paired`, the watch card foot `esc close · o open · [om watch show …]`, `o` to the watch page and Esc back, and `o` with a draft (#2207). On 2026-10-29, at `32ca0d6c7`: frame, `om sidebar set`/`reset`, PAPER, go-to-recent and exit history. | Undriven on a lane: the 20-fire card scroll and its containment, the FIRES and USAGE `o`, the one-panel floor, collapse, the narrow resize, a live model turn, and the yellow `late` dot (needs an overdue polled source). |
| Open the registry welcome page (`om welcome`) | `cmd/welcome.ts`; `runner/packages/registry-contracts.ts` | [registry-welcome-and-search.md](registry-welcome-and-search.md) | real registry re-read 2026-10-31, main `dfefe0a21` (`does not offer`); real registry re-read 2026-10-30 scheduled maintenance, main `3cb50a821` ("does not offer"); 2026-10-28, main `a8fa10974` (real registry: "does not offer"; fixture: all three gate branches) | On main since #1947. The success path needs a registry advertising `welcome`, which production still did not on 2026-10-27, so it was proved against a fixture. |
| Get plain-language, personalised registry search results | `cmd/search.ts`; `runner/packages/search.ts` | [registry-welcome-and-search.md](registry-welcome-and-search.md) | real registry `search rsi` re-read 2026-10-31, main `dfefe0a21`; 2026-10-28, main `a8fa10974` (fixture: `mode=nl`, `reasons`; with a key, `rank=for-you` + bearer; TTY text renderer with reasons lines) | Production still returns the old shape (no `nl` advertised). |
| Uninstalling or unfollowing tells the registry (receipt retraction) | `actions/packages/uninstall.ts`; `actions/watch/follow.ts`; `runner/packages/{retractions,use-receipts}.ts` | [registry-welcome-and-search.md](registry-welcome-and-search.md) (Gotchas) | live verification pending | Needs an account whose install or follow receipt returned an `edge`, plus a registry advertising `receipt_retract`. A guest never retracts. Signals are `[use-receipts]` log lines and `<home>/receipts/retractions.json`. |
| Finish `om init` by opening the welcome page (`--launch`) | `cmd/init.ts` | [registry-welcome-and-search.md](registry-welcome-and-search.md) (`init-closing`) | live verification pending | `om init` needs a TTY (exit 2 otherwise) and writes channel, credential and service state, so it is never driven on a lane. |
| Watch narrative (sentences, facets, entities from a recipe) | `packages/contracts/src/watch-narrative.ts` | **non-outcome** | n/a | A contracts library with no consumer in the CLI or dashboard at `ee8e3a7ab`, `8fe6a8432`, `a8fa10974` or `32ca0d6c7` (re-grepped 2026-10-29; only `packages/contracts/src/index.ts` exports it). Nothing renders it yet; re-check when one does. |
| Review a scheduled calendar occurrence | `actions/calendar/*`; `runner/calendar/blocks.ts` | [calendar-and-polling-windows.md](calendar-and-polling-windows.md) | 2026-10-31, main `dfefe0a21` (push → list → show → select → revise cancelled); empty `calendar list` re-read 2026-10-30 scheduled maintenance, main `3cb50a821`; 2026-10-28, main `a8fa10974` (occurrence, select, revise, reject, links, polling windows) | None. The window was not waited out to run. |
| Recover a challenged origin through a paid reader | `runner/firecrawl/*` | [firecrawl-first-block.md](firecrawl-first-block.md) | no-key path re-driven 2026-10-30 scheduled maintenance, main `3cb50a821` (inside a hold, `page-add` exited 2 `page_bot_wall_suspected` with the `om setup firecrawl` hint); no-key path re-driven 2026-10-28, main `a8fa10974`; configured path pending | Needs `OM_FIRECRAWL_API_KEY` **and** a redirect of `api.firecrawl.dev/v2/scrape` to a fixture, together. |
| Create, import, Try, install, publish, adopt and revoke an agent | `packages/roster/src/http/roster-api.ts` (`imports/*`, `local-packages/*`, `builder`, `instances/:id/try`) | [agent-creator-lifecycle.md](agent-creator-lifecycle.md) (historical branch closeout) | live verification pending on main | On main since #1948 (`b50ca927d`), HTTP/GUI only. Needs an account, an LLM credential or coding brain, and the openmarket-chat Agents GUI (`verify-om-chat`). |
| Read agent work runs, refuse unknown runs, read roster health and measures | `cmd/{roster,roster-runs,roster-controls,roster-retry}.ts` (`OM_DEV=1`); `packages/roster/src/http/roster-work-api.ts`; `/healthz` `roster` | [agent-creator-lifecycle.md](agent-creator-lifecycle.md) (Guest lane on main) | `roster list` re-read 2026-10-31, main `dfefe0a21` (six defaults); 2026-10-30 scheduled maintenance, main `3cb50a821` (empty runs, `not_found` proof, roster list, executors); 2026-10-28, main `a8fa10974` (empty runs, `not_found`/`malformed_body` refusals, roster list/measures, `/rpc/v1/roster/projects`) | Real runs, plan approval, steer and retry need an installed agent plus a model or brain. |
| Link a coding project and set its delivery | `cmd/project-{token,delivery,unlink}.ts` (`OM_DEV=1`); `/rpc/v1/roster/projects` | [agent-creator-lifecycle.md](agent-creator-lifecycle.md) (Guest lane on main) | refusal only, 2026-10-28, main `a8fa10974` (`project unlink nope` → `not_found`) | Needs a project linked through the GUI and a real forge token. |
| Drive persona and away operations from the web over remote control | `agent/channels/remote-control.ts`; `packages/rooms-client/src/remote-operation-routes.ts` (#2161) | unmapped | live verification pending | Needs `om agent remote enable`, the relay and a signed-in web client; nothing is guest-observable. |
| Compose a watch (or a set) from a natural-language ask | `actions/watch/watch-compose.ts`; `actions/watch/kit.ts` | unmapped | live verification pending | Needs an LLM credential; the single largest `om watch` entry point. |
| Share, follow, fork, install a watch; room shares and knocks | `actions/watch/{share,follow,fork,install,share-room,knocks,relay-door}.ts` | unmapped | live verification pending | Registry + account credential; a follower needs a second home. |
| Attach and arm steps (ai / tool / money) on a watch | `actions/watch/{action-add,action-remove,tools,run-now}.ts` | unmapped | live verification pending | Money steps are capital-gated; ai steps need a model credential. |
| Grow an existing watch with more sources | `actions/watch/{source-add,page-add,search-add,model-add,source-copy}.ts` | [watch-lifecycle-cli.md](watch-lifecycle-cli.md) / Maintenance verbs | timer source add/remove live verified 2026-10-28, main `a8fa10974` | Page, search, model and OpenFeed sources need a credential or account. |
| Repair or retry a watch broken for any non-origin reason | `actions/watch/{repair,retry,lane-retry}.ts` | [watch-lifecycle-cli.md](watch-lifecycle-cli.md) / Maintenance verbs | `repair --rearm` refusal re-driven 2026-10-31, main `dfefe0a21`; retry/repair on a healthy watch plus the `--rearm` and `lane retry` refusals live verified 2026-10-28, main `a8fa10974` | A genuinely broken watch is not constructible on a guest lane. |
| Read the wider journal surface: list, stats, chapters, search | `actions/watch/{journal-search,journal-stats,chapters,journal-list}.ts`; `cmd/event-journal.ts` | [watch-lifecycle-cli.md](watch-lifecycle-cli.md) (journal step) | 2026-10-31, main `dfefe0a21` (`event-journal list` with a removed watch's `watch_id: null`, `journal-stats`, `chapters`, `watch history`); 2026-10-28, main `a8fa10974` (`event-journal list`, `search`, `journal-stats`, empty `chapters`) | Populated chapters undriven (they need a model's summary fold). |
| See and reclassify rows the judge never reached | `actions/watch/unjudged-rows.ts`; `actions/watch/reclassify.ts` | [watch-lifecycle-cli.md](watch-lifecycle-cli.md) / Maintenance verbs | `unjudged` empty read and the `watch_reclassify_daemon_running` refusal live verified 2026-10-28, main `a8fa10974` | Real unjudged rows need an LLM daily cap; reclassify needs the daemon stopped. |
| Rewrite a fired row's recorded verdict | `actions/watch/synthesize.ts` | unmapped | live verification pending | Source says the verb is `om watch amend <watch> <event-id> --weight …` (`cmd/watch-engine-verbs.ts:1825`, `actions/watch/amend.ts`), not `synthesize`. It needs a topic lane and a streamed event. Not driven. |
| Move a watch between devices, mute a remote copy, restore one | `actions/watch/{move-here,move-readiness,mute,restore,adopt-here}.ts` | unmapped | live verification pending | Needs a second device/home for the interesting cases. |
| Read money-step execution history and digests | `actions/watch/{execute-history,execute-digest,execute-paper-reset}.ts` | [watch-lifecycle-cli.md](watch-lifecycle-cli.md) / Maintenance verbs | `execute summary` zeroed 2026-10-31, main `dfefe0a21`; empty-state reads live verified 2026-10-28, main `a8fa10974` (`execute history/summary/list`, `watch execute history`) | Needs executed money steps. `om execute digest list` answered `unknown command 'digest'` on this lane, so the digest's CLI door is unresolved. |
| Session and device identity: sign-in state, rename/revoke devices, account email | `actions/auth/{status,relogin}.ts`; `actions/devices/*`; `actions/account/email.ts` | unmapped | live verification pending | Account credential; revoke is destructive. |
| Mint and revoke API keys | `actions/keys/{create,revoke}.ts` | unmapped | live verification pending | Account credential; security-tiered, revoke is permanent. |
| Pair and manage a notification channel | `actions/system/{channel-add,channel-home,channel-default-set}.ts`; `cmd/setup.ts` (`setup default [name] [--force] [--clear]`); `runner/http/rpc/channel.ts` | pairing unmapped (dashboard shell only); the default-channel read and refusal are in [local-reads-and-discovery.md](local-reads-and-discovery.md) (Guest-lane reads) | `om setup default` read and refusal live verified 2026-10-31, main `dfefe0a21`: the bare read printed `{"default":null,"routing":"none","targets":[]}` (the verb's default format is JSON); `setup default nope`, with `--format json` and with `--force` (#2220), each exited 2 with `channel_not_found` `unknown channel 'nope' — no channels are configured`, hint `om setup list`, `details.channels: []`. Pairing itself is live verification pending | Pairing, `channel_default_set` over chat and MCP, the `channel_failing` refusal and the `routing_note` need a paired Telegram/Discord/Slack channel. `--force` on a failing channel raises a tier-3 card in chat (`agent/risk-tiers.ts`). |
| Read the daemon's own notification history | `actions/system/{notis-list,notis-get}.ts`; `cmd/notis.ts` | [local-reads-and-discovery.md](local-reads-and-discovery.md) | 2026-10-31, main `dfefe0a21` (`notis --since 7d --json` fire rows); 2026-10-28, main `a8fa10974` (`notis --since 7d` rows) | `notis get` and `--after` paging undriven. |
| Inspect resolved config and the active key's claims | `actions/system/{config-show,config-key-info}.ts`; `cmd/config.ts`; `cmd/config-keys.ts` (`chat.sounds`, `chat.workspace`) | [local-reads-and-discovery.md](local-reads-and-discovery.md) | 2026-10-31, main `dfefe0a21`: the new `chat.sounds` key (#2217) read `unset (default: on)`, `stored as tui.sounds`; `set chat.sounds off` printed `om: set chat.sounds=off` and `get --format json` read `value: off`, `source: config`, `stored_as: tui.sounds`; `set chat.sounds maybe` exited 2 `chat.sounds must be on or off.`; `set agent.max_tool_calls 250` still exits 2 (`at most 249`). 2026-10-30, main `3cb50a821`: `config set agent.max_tool_calls 250` was refused (`at most 249`), then `set … 249` and `get` succeeded. On 2026-10-28: `show`, `key-info` and `get` | `config edit` undriven. |
| Upgrade the binary, migrate and restart | `actions/system/upgrade.ts` | unmapped | live verification pending | Risk tier 5, confirm-carded; must never run against a lane. |
| Read the subscription plan and pricing | `actions/system/upgrade-show.ts` | [local-reads-and-discovery.md](local-reads-and-discovery.md) / Plans | `upgrade --show` re-read 2026-10-31, main `dfefe0a21` (guest note `600 weight per 60s window`); `upgrade --show` and `usage plans` live verified 2026-10-27 maintenance, main `8fe6a8432`; `subscriptions` refusal | `om subscriptions` refuses `account_required` for a guest. Buying and cancelling need an account. |
| Watch roster triage: what needs attention, one-click repair | `actions/system/{watching,watching-resolve-attention}.ts` | [watch-lifecycle-cli.md](watch-lifecycle-cli.md) / Maintenance verbs | `POST /rpc/v1/watch/overview` re-read 2026-10-31, main `dfefe0a21`; `POST /rpc/v1/watch/overview` and MCP `watching_overview` live verified 2026-10-28, main `a8fa10974`; resolve-attention 409 refusal | A real attention item (daemon down, paused) was not seeded. |
| Read indicator and drawing schemas (catalog) | `actions/collab/{indicator-schema,indicator-list}.ts`; `cmd/chart.ts` | [chart-catalog-reads.md](chart-catalog-reads.md) | 2026-10-31, main `dfefe0a21` (`indicator schema rsi` → `@om-core/rsi` 0.1.1, `period` int 14 in 1..2500; `nonsense` → exit 2 `indicator_unknown` listing the stock names); 2026-10-30 scheduled maintenance, main `3cb50a821`; 2026-10-28, main `a8fa10974` (`indicator schema`, `indicator list`, `drawing schema`) | The `--chart`/`--workspace` forms, `indicator list`, `drawing schema` and the `wrun/@scope/name/output` metric-id form were not re-driven tonight. |
| Drive chart workspaces, indicators and drawings | `actions/collab/chart-*.ts`, `drawing-*.ts`, `indicator-*.ts` | unmapped | live verification pending | Needs a human's GUI chart tab open on a live collab session; a headless lane has nothing to submit to. |
| Backtest a strategy over historical bars | `actions/research/backtest*.ts` | [watch-lifecycle-cli.md](watch-lifecycle-cli.md) / Maintenance verbs (refusals) | `--window-secs` refusal re-driven 2026-10-31, main `dfefe0a21`; Refusals live verified 2026-10-30, main `3cb50a821`: the stop-breaker flags (#2208) are `--window-secs` without `--max-stops`, a non-numeric `--max-stops`, and `run nope --window-secs 60`, each exit 2. The bare `backtest spec` refusal was also driven. `backtest run nope` was driven 2026-10-28 | A real run needs a watch with a strategy step (`watch create --from-candidate`). A braked package run needs an installed Indicator strategy package. Neither was driven. |
| Browse paid news feeds and read Fast-alerts billing | `actions/news/{feeds,billing,brief,voice}.ts`; `runner/http/rpc/news.ts` | unmapped (dashboard shell only) | live verification pending | Catalog browsing may be guest-ok; billing and follow need an account and a funded vendor relationship. |
| Agent memory: save, search and forget durable notes | `actions/memory/*.ts`; `cmd/memory.ts` | [mcp-stdio.md](mcp-stdio.md) / Hosted MCP | save → search → CLI `memory list` → forget live verified 2026-10-28, main `a8fa10974` over hosted MCP | The slug prefix must match the type (`memory_invalid_slug`). `memory_forget` ran with no approval card on loopback HTTP. |
| Author and compile a custom WASM indicator | `actions/wrun/{create,author,build,source-set,list}.ts`; `cmd/wrun.ts` | [local-reads-and-discovery.md](local-reads-and-discovery.md) (`wrun list`/`templates`/`create`) | 2026-10-29 scheduled maintenance, main `7ec575e55`: `wrun create --template feed-alert-line` scaffolded a workspace at scaffold 106 whose feed input reads `ref: "@you/your-feed"`, and the three Feeds starters' descriptions say "set ref to a feed you published" (#2194); templates still 91. Before that, 2026-10-29 nightly, main `32ca0d6c7` (templates still 91; scaffold 105, #2184). Before that, 2026-10-28, main `186030b63` (list; templates still 91, 30 `runsOn` lines read OPRA "at your own tier" after #2180; the stock `accumulate` 0.1.3 package listed) | `WRUN_SCAFFOLD_VERSION` is 106 since #2194 (`packages/sdk/src/wrun-sdk-sources.ts:1159`). A scaffold-105 workspace refreshes its kit texts once. Drive `wrun create` into a directory outside the product tree, because it writes wherever the positional `[dir]` points. `wrun validate` is undriven; `wrun build` compiles and installs deps, so it needs package-manager access. |
| Arm and tune a live managed-strategy wallet | `cmd/managed.ts` over `actions/managed/*.ts` factories (CLI-only: not in the action registry) | unmapped | live verification pending | Capital-reaching: funded venue wallet plus an explicit arm gate. Out of reach for a guest lane. |
| Place and manage real venue orders; wallet and execution | `cmd/{order,execute,buy,hyperliquid,polymarket}.ts`; `actions/{execute,orders,hyperliquid,wallet,polymarket}/` (`actions/execution/` does not exist) | unmapped | live verification pending | Real money. Needs a funded account and a safe plan; nothing attempted. |
| Reach the capability layer over MCP (stdio) | `cmd/mcp.ts`; `mcp/server.ts`; `mcp/capital-gate.ts` | [mcp-stdio.md](mcp-stdio.md) | 2026-10-31, main `dfefe0a21` (0.480.2, **454** tools: `file_create` and `channel_default_set` added, `document_draft` answers `Tool document_draft not found`; `watch_list`; `channel_default_set {name:"nope"}` → `channel_not_found` with the MCP hint `details.channels names the configured channels`; `order_place` → `capital_yolo_harness` under this driver). The stdio server was driven against the lane home with the daemon down (the guest 429 kept it from booting), which these calls do not need; 2026-10-30 scheduled maintenance, main `3cb50a821` (0.478.0, 452 tools, `watch_list`); 2026-10-30, main `3cb50a821` (handshake 0.478.0, 452 tools including `doc_patch`, a read, a `watch_not_found` payload without `kind`). The capital refusal was last driven 2026-10-28 | `om mcp arm`, `--catalog operator` and `--session merged` undriven. |
| Save a drafted document as a file (`file_create`, #2218/#2221) | `actions/research/file-create.ts`; `shared/document-files.ts`; `shared/user-folders.ts`; `agent/risk-tiers.ts` (`downloads`/`overwrite` tier 3); `agent/rooms-gating-plane.ts` (`SHARED_UNSAFE_TOOLS`) | [mcp-stdio.md](mcp-stdio.md) (`file_create` over stdio) | `scratch` live verified 2026-10-31, main `dfefe0a21` over stdio: `{content, filename:"vom-probe-20261031"}` wrote `<lane home>/accounts/guest/documents/vom-probe-20261031.md` (`bytes`, `format: md`, `destination: scratch`); a second call took `vom-probe-20261031 (2).md`; `filename:"../escape"` → `invalid_filename` (`the filename has a path separator; give a base name only`). `destination:"downloads"` never answered in 120 s and wedged the server (README, known product gaps) | No CLI verb (the manifest marks it bespoke): chat and MCP only. The chat card for `downloads`/`overwrite`, `path_escapes_root` on a symlinked documents folder, `no_downloads_folder`, PDF/DOCX refusals and the tier-3 card are undriven; the `downloads` hang over stdio is a product gap. |
| Reach the capability layer over hosted MCP (HTTP) | `mcp/http.ts` | [mcp-stdio.md](mcp-stdio.md) / Hosted MCP over loopback HTTP | loopback `mcp serve --http` live verified 2026-10-28, main `a8fa10974` (441 tools) | Non-loopback badge auth and `OM_LOOPBACK_AUTH=1` were not driven. |
| Run the hosted chart MCP against Mongo: boot, health, readiness, index rebuild, refusals | `packages/cli/src/hosted/{main,run,config,tenant-store-mongo,tenant-store-health}.ts` | [hosted-chart-mcp-tenant-state.md](hosted-chart-mcp-tenant-state.md) | refusals and `--help` re-driven 2026-10-30 scheduled maintenance, main `3cb50a821` (no Mongo); 2026-10-28, main `a8fa10974` (boot lines, health pair up/down/back, rebuild, four refusals, `--help`) | The tool-call path needs an operator API key on the production gateway; the env-gated suite passed 7/7 on 2026-10-28 once the role also had `readWrite` on `om_hosted_test` (without it the suite fails `Unauthorized`). |
| Publish, install and manage registry packages | `cmd/{packages,publish,install}.ts`; `actions/packages/*` | partially via agent-creator (itself unverified) | live verification pending | Registry credential; `package_delete` is irreversible. |
| Approve an arming or model edit from the dashboard | `runner/http/rpc/{watch-arm-review,watch-edit-review}.ts` | [watch-lifecycle-cli.md](watch-lifecycle-cli.md) / Maintenance verbs (refusal) | `arm-confirm` refusal (400 `approval_expired`) live verified 2026-10-28, main `a8fa10974` | The happy path needs a watch with a money or ai step awaiting approval. |
| Sealed secrets bridge | `runner/http/rpc/secrets.ts` | [local-reads-and-discovery.md](local-reads-and-discovery.md) / Secrets status | `GET /secrets/status` re-read 2026-10-31, main `dfefe0a21` (`unminted`); `GET /secrets/status` live verified 2026-10-27 maintenance, main `8fe6a8432` (200, guest `readiness: unminted`) | Minting, recovery and rooms use need an account. |
| Social chat: rooms, DMs, topics, docs, moderation | `actions/rooms/*` (190); `cmd/room.ts` | **out of scope here** | n/a | Owned by `verify-om-chat` per this repo's boundary rules; this repo holds only the protocol surface and daemon-side actions. Recorded so the gap is not mistaken for an omission. |
| Standalone `/paper` dashboard route | `apps/dashboard/src/paper-plane.tsx` | **non-outcome** | n/a | Mounts only when `strategyRoutes === null` (the OSS export). Unreachable in any lane `control-om` drives; reach Paper via the `/strategies` tab. |
| Review pending approvals from the CLI (`om approvals list\|approve\|deny`) | `cmd/approvals.ts`; `cmd/approve-chain.ts`; `runner/http/approvals-routes.ts`; `main.ts:73` | [local-reads-and-discovery.md](local-reads-and-discovery.md) / Guest-lane reads | `approvals list` `[]` re-read 2026-10-31, main `dfefe0a21`; list live verified 2026-10-28, main `a8fa10974` (`approvals list` printed `No pending approvals.`, `--format json` printed `[]`, and `GET /rpc/v1/approvals` returned `{"approvals":[]}`) | Approve and deny need a pending item and a human terminal, so they are not driven. |
| Sign in or out, connect an LLM or coding agent from the CLI (`login`, `logout`, `llm`, `auth`, `setup`, `connect`, `disconnect`) | `main.ts:78,83,134,~140` | unmapped | live verification pending | Needs an account, a provider key or a TTY. |
| Wipe, export/import or upgrade the local store (`om reset`, `om migrate`, `om upgrade-db`) | `main.ts:202,219,222` | unmapped | live verification pending | Destructive; only on a scratch lane root. |
| Read and steer Away coverage over local HTTP (`/api/away`, `/coverage`, `/sessions`, `/activity`; `POST` `/policy`, `/arm`, `/control`) | `runner/http/away-api.ts:16,55-96`; gate in `runner/http/rooms-routes.ts:85-98` | [local-reads-and-discovery.md](local-reads-and-discovery.md) / Guest-lane reads (refusal) | 401 re-read 2026-10-31, main `dfefe0a21`; refusal live verified 2026-10-28, main `a8fa10974` (`GET /api/away` and `/api/away/coverage` returned 401 `operator_required`) | The reads need operator proof even on loopback: the per-boot GUI session cookie, or a configured runner or desktop token. `/policy` is a `POST`, not a read. `arm` is unsafe. The GUI side belongs to verify-om-chat. |
| Library and persona over local HTTP (conflicts, proposals, persona use/import/learn/sync) | `runner/http/library-api.ts:163-178`; `cmd/rooms-commands.ts` | unmapped | live verification pending | Probably needs rooms; the UI side is verify-om-chat's. |
| Read the follows feed (`om follows`) | `cmd/follows.ts`; `actions/follows/{list,show,feed,review}.ts` | [local-reads-and-discovery.md](local-reads-and-discovery.md) / Guest-lane reads | empty list and refusal live verified 2026-10-28, main `a8fa10974` (`follows` returned zero `summary` counts; `follows show @nobody/nothing` exited 2 with `not_following`) | A populated feed needs a followed share, which needs a registry and an account. `om follow review` prompts for confirmation. |
| Stream live data over WebSocket (`om subscribe`) | `main.ts:196` | unmapped | live verification pending | Not driven; probably needs an API key with stream entitlement. |
| Send a one-shot message to a channel (`om send`) | `cmd/send.ts` | unmapped | live verification pending | Needs a paired channel. |
| Trace a shared alert's fires hop by hop (`om relay`) | `cmd/relay.ts`; `main.ts:212`; `runner/stream/relay-diagnostics.ts` | [local-reads-and-discovery.md](local-reads-and-discovery.md) / Guest-lane reads (refusals) | refusals live verified 2026-10-28, main `a8fa10974` (`relay trace @nobody/nothing` gave `relay_ref_unknown`; a malformed ref gave `relay_ref_invalid`; both exit 2) | A real trace needs a live-shared watch. |
| Nervous system: autonomous chart moments from fires (`om nervous`) | `cmd/nervous.ts`; `actions/collab/nervous-status.ts` | [local-reads-and-discovery.md](local-reads-and-discovery.md) / Guest-lane reads | 2026-10-31, main `dfefe0a21` (`enabled: true`, a `watch_fired` receipt after the ingest fire); 2026-10-28, main `a8fa10974` (`nervous status` showed `enabled: true` and a `watch_fired` receipt for the lane's own ingest fire, "no canvas resolved"; MCP `nervous_status` matched) | A chart moment that lands needs a GUI chart tab. |
| Run research studies (`om research`) | `main.ts:204`; `cmd/research.ts`; `actions/research/*` (10 actions besides backtest) | [local-reads-and-discovery.md](local-reads-and-discovery.md) / Guest-lane reads | `--locate-only` re-read 2026-10-31, main `dfefe0a21`; `study --locate-only` live verified 2026-10-28, main `a8fa10974` (occurrences for an inbound watch; `--watch nope` gave `watch_not_found`) | A full study fetches candles and was not run. `search-files` and `make-image` spend on a model and need one. |
| Open the dashboard or desktop app setup from the CLI (`om dashboard`/`open`, `om app`, `app-setup`, `om claude`) | `cmd/apps.ts`; `cmd/app-setup.ts`; `main.ts:67,69` | unmapped | live verification pending | `dashboard`/`open` launch a browser; not driven on a lane. |
| Keep watchlists (`actions/watchlists/{index,local}.ts`) | `actions/watchlists/`; `actions/collab/collab-rest.ts:65-81` | [mcp-stdio.md](mcp-stdio.md) (refusal) | refusal live verified 2026-10-28, main `a8fa10974` (MCP `watchlist_list` gave `missing_api_key`: guest keys have no workspaces) | There is no CLI verb. The MCP and agent tools need an account. |
| Create, list, edit, pause, resume and remove a watch from the CLI | `cmd/watch-engine-verbs.ts`; `actions/watch/{create,edit,pause-resume,remove,list,show}.ts` | [watch-lifecycle-cli.md](watch-lifecycle-cli.md) | 2026-10-31, main `dfefe0a21` (create, list, edit, show, pause `held_lots: []`, resume, remove `paper_lots_left: []`); 2026-10-30 scheduled maintenance, main `3cb50a821` (pause `held_lots: []`, 409 on a paused door, resume, history); 2026-10-30, main `3cb50a821`: create, edit, show, pause (`held_lots: []`), resume, and remove (`paper_lots_left: []`). The label checks were driven 2026-10-28 | Non-empty `held_lots` and `paper_lots_left` need a money step holding a paper lot. |
| Push an event and see it fire on the door, the stream, the journal and the dashboard | `runner/http/ingest*`; `/events/v1`; `cmd/event-journal.ts` | [event-ingest-and-fire.md](event-ingest-and-fire.md) | 2026-10-31, main `dfefe0a21` (door 202 + 401 unauthenticated, three stream events, the journal id, CLI push `delivery: daemon`, the `/alerts` row); 2026-10-30 scheduled maintenance, main `3cb50a821` (door 202, three stream events on one `event_id`, journal, `working`, 401 unauthenticated; CLI push `delivery:"daemon"` at load about 140); 2026-10-30, main `3cb50a821`: the door returned 202 with one `event_id` on all three stream events, the journal and the dashboard `working`. An unauthenticated push got 401 | On a busy host, CLI `event push` writes `direct` beside a live foreground lane (product gap below). |
| See the daemon's dashboard: Overview, Watches, News, Strategies, Channels, Venues and Receipts | `apps/dashboard/src/{app.tsx,pages/*}` | [ops-dashboard.md](ops-dashboard.md) | 2026-10-31, main `dfefe0a21` (every route's H1 on a bundle built from this tree; the Paper tab; the `/strategies/<unknown>` flicker again); 2026-10-30 scheduled maintenance, main `3cb50a821` (every route's H1; `/strategies/<unknown>` `Loading…`); 2026-10-28, main `a8fa10974` (onboarding on a fresh lane, nav, every route's headings and empty states, the `/strategies/<unknown>` flicker) | Row added 2026-10-28. A populated strategy page needs a strategy, a signal and a venue. |
| Author a watch in the dashboard (`Create watch`) | `apps/dashboard/src/` watch-create flow | [watch-authoring-ui.md](watch-authoring-ui.md) | 2026-10-31, main `dfefe0a21` (RSS through review to `/alerts/ui-authored-feed`, created paused, resumed from the CLI, polled the stub each minute); 2026-10-30 scheduled maintenance, main `3cb50a821` (RSS through review to `/alerts/ui-authored-feed`, `enabled: false`, polls after resume); 2026-10-28, main `a8fa10974` (RSS kind through review to `/alerts/ui-authored-feed`, a paused watch on `watch show`, polls after resume) | Row added 2026-10-28. The other seven kinds were listed, not authored. |
| Ask the dashboard agent; open the `/agent` workspace | `apps/dashboard/src/` agent panel; `/agent` route | [agent-panel.md](agent-panel.md) | refusal re-driven 2026-10-31, main `dfefe0a21` (`No LLM API key configured…`, `Check connections`); `/agent` rendered; refusal re-driven 2026-10-30 scheduled maintenance, main `3cb50a821`; refusal live verified 2026-10-28, main `a8fa10974` (the `No LLM API key configured.` alert, `Check connections`, the `/agent` rail) | A reply needs an LLM credential. Row added 2026-10-28. |
| A challenged host holds every source on it: one probe per window, then the window doubles | `runner/fault-episodes.ts`; `runner/subscriptions/*`; `shared/public-document.ts` | [origin-challenge-backoff.md](origin-challenge-backoff.md) | 2026-10-31, main `dfefe0a21` (steps 1-3 on the UI-authored feed: one challenge poll, the 15-minute hold in the lane log, `/healthz` `reconnecting` with a `cooldown`, `watch show` FAULT/Error/Status rows); 2026-10-30 scheduled maintenance, main `3cb50a821` (one challenged poll, `reopen held until` +15 min, `/healthz` `reconnecting` with a cooldown, the FAULT sentence on CLI and dashboard, silence, then `ok` and `reopened after the window` at `until`; the doubling was not re-driven); 2026-10-28, main `a8fa10974` (hold; one still-challenged probe at `until`; 15 min doubled to 30; recovery at the doubled `until` with `reopened after the window` and `/healthz` `open`) | Row added 2026-10-28. During a long hold the status rows stop naming the challenge (product gap below). |
| Default agents arrive from `@om-core` registry packages after boot | `packages/roster/src/plugins/om-skills-defaults.ts`; `runner/roster-host/registry.ts` (#2167, #2169, #2183) | [agent-creator-lifecycle.md](agent-creator-lifecycle.md) / Default agents | 2026-10-31, main `dfefe0a21` (`installed 8 package(s)` about 4 s after boot; six rows); 2026-10-30 scheduled maintenance, main `3cb50a821` (`installed 8 package(s)`, six registry rows at 1.0.0); install live verified 2026-10-29, main `32ca0d6c7` (`installed 8 package(s)` about 5 s after boot; `roster list` showed six registry agents at 1.0.0). The 404 retry path was driven 2026-10-28 under the old `@om-skills` scope | The six-hour maintenance pass and a withdrawal (410) are undriven. |
| A strategy-package watch holds its queued position, bounds its opening legs, and pages and digests each leg on paper | `runner/watching/steps/target-step.ts`; `runner/paper/{target-sink,target-pager,target-episodes,exit-lane,notices,digest}.ts`; `packages/contracts/src/target-step.ts` (#2176, #2188, #2192, #2201, #2208); `runner/money/{target-breaker,stop-breaker-verdict}.ts`; `runner/paper/entry-record.ts` | unmapped | live verification pending | #2208 adds `stop_breaker {max_stops?, window_secs?, max_loss_usd?}`, the stand-down causes, the arm-card `stop breaker:` line, and the refused close retried on the next row. #2201 means a lot closed by a stop, a limit or a hand holds the step flat until the package books its own exit (`target_entry_exited`). #2188 adds `admit.drift_frac`, `admit.max_event_age_secs` and `cooldown` (opening legs only), with arm-card facts and chain digest version 5. #2192 adds `Paper <acct> · opened/adjusted/closed` notices, `Step:` rows in the digest, `PAPER` rows in `watch execute history`, and research `admission_not_modeled`. All of these need a target step fed by an `ai` producer (a model) and an arm. Offline coverage: `test/paper-target-sink.test.ts` and `test/watch-target-chain.test.ts`. |
| See what's new in plain `om chat` and turn it on in one press | `agent/channels/whats-new-card.ts`; `shared/whats-new{,.generated}.ts`; `cmd/config.ts` (`writeWhatsNewSetting`) | [chat-workspace-tui.md](chat-workspace-tui.md) / `whats-new-card` | 2026-10-31, main `dfefe0a21`: the card (`1 0`), the ctrl+x `w`/`x` rows, `x` closed it (`0 0`). 2026-10-30 scheduled maintenance, main `3cb50a821`: ctrl+x `x` closed the card (flags `1 0` → `0 0`). 2026-10-29, main `32ca0d6c7` (card on a fresh lane; ctrl+x rows `w`/`x`; `w` set `chat.workspace on` and reopened as a workspace) | The ✕ click, paging with several entries, and the 60-day expiry were not driven. |
| A web chat whose tab closes on an open approval card frees the conversation | `agent/channels/web.ts` (#2205) | unmapped | live verification pending | It needs a model plus a web-chat client that holds an approval card and drops its stream. The GUI side belongs to verify-om-chat. Before the fix, `om chat` printed `Waiting for pid <daemon>` until a restart. |
| See where the vault master key lives, and move it into the OS keyring (`om vault status`, `vault protect [--off]`) | `cmd/vault.ts:109-133`; `main.ts:125` | [local-reads-and-discovery.md](local-reads-and-discovery.md) (2026-10-30 stamp) | `vault status` re-read 2026-10-31, main `dfefe0a21` (`mode: none`, `keyring: macOS Keychain (available)`; no `--format`); `vault status` live verified 2026-10-30 scheduled maintenance (`mode: none`, `keyring: macOS Keychain (available)`) | `protect` writes the machine's keychain, so it is not driven on a lane. `vault status` takes no `--format`. Source discovery 2026-10-30. |
| Read and accept the marketplace terms (`om terms`, `terms accept`) | `cmd/terms.ts:290-325`; `main.ts:129` | [local-reads-and-discovery.md](local-reads-and-discovery.md) (2026-10-30 stamp) | read live verified 2026-10-30 scheduled maintenance (`not_applicable: true`, `accepted: false` for a guest) | `accept` needs an account. Source discovery 2026-10-30. |
| List exchange-native and normalized symbols and heatmap block sizes (`om symbols`, `normalized-symbols`, `block-sizes`) | `cmd/{symbols,normalized-symbols,block-sizes}.ts`; `actions/data/{symbols,normalized-symbols}.ts`; `main.ts:167`, `:169`, `:173` | [market-data-reads.md](market-data-reads.md) (2026-10-30 stamp) | live verified 2026-10-30 scheduled maintenance (`--type TRADE_AGG`; `block-sizes --exchange BINANCE`) | `--type` must be a `data_type` value; anything else is refused `invalid_options`. Source discovery 2026-10-30. |
| Cancel a subscription (`om unsubscribe`) | `main.ts:131` (`subscriptions`, `unsubscribe`) | [local-reads-and-discovery.md](local-reads-and-discovery.md) / Plans | refusal live verified 2026-10-30 scheduled maintenance (`confirmation_required`: "Cancelling a subscription moves money and needs confirmation.") | A real cancel needs an account with a subscription and moves money. Source discovery 2026-10-30. |
| Read the daemon's machine-readable route catalog (`GET /openapi.json`) | `runner/http/openapi.ts:78`; `runner/http/server.ts:915-919` | [local-reads-and-discovery.md](local-reads-and-discovery.md) (2026-10-30 stamp) | re-read 2026-10-31, main `dfefe0a21` (200, 137 paths, `info.version` 0.480.2); live verified 2026-10-30 scheduled maintenance (200, 137 paths, `info.version` 0.478.0) | Same auth as `/healthz`. The paths are hand-authored, and `/rpc/v1/approvals` was not among them. Source discovery 2026-10-30. |
| Use the other `om chat` slash commands and prompt history (`/hints`, `/mute`, `/unmute`, `/jobs`, `/catchup`, `/brief`, `/rename`, `/provider`, `/effort`; ctrl+r) | `agent/slash.ts:165-288`; `agent/channels/tui-history-search.ts` | unmapped | live verification pending | The fake-model TUI rig in [chat-workspace-tui.md](chat-workspace-tui.md) reaches them; `/catchup` narration needs a model. Source discovery 2026-10-30. |
| Greet a newly connected chat channel and copy another channel's setup into it | `agent/channels/channel-tour.ts`; `agent/channels/copy-setup.ts` | unmapped | live verification pending | Needs a paired Telegram, Discord or Slack channel. Source discovery 2026-10-30. |

### Known product gaps (reported, not map drift)

- **New 2026-10-31 (`dfefe0a21`): `om points --exchange BYBIT_FUTURES` is still
  refused.** #2202 says every tool that takes an exchange id maps the
  carried-over spelling, and it does on the MCP `points` schema and on `om
  metric get` (both read `BYBIT`); but `cmd/points.ts` hands the raw flag to
  the handler without the schema parse that carries `aliases`, so the API
  answers `parsing list "exchange": "BYBIT_FUTURES" is not a valid value`
  (exit 2). Driven on lane 18163 (`cli/56`, `cli/55`, `cli/95`).
- **Re-observed 2026-10-31:** `tenors` 500; the `/strategies/<unknown>`
  flicker (`Loading…` at 9 and 12 s); `exchange_id` 35 values against 45
  listed by `exchanges`, with `LIGHTER` readable from the CLI only.
- **New 2026-10-31 (`dfefe0a21`): over MCP stdio, `file_create` with
  `destination: "downloads"` never answers, and the server answers nothing
  after it.** Driven three times on the lane home (daemon down): the call
  sat for 120 s and then for 15 min with no result, no `pending_approvals`
  row (`om approvals list` read `[]` throughout, and the table was empty),
  no child process, and the server's main thread blocked in native code with
  `om.sqlite` open; every `tools/call` sent after it timed out too. The
  `scratch` destination answers in milliseconds, and `~/Downloads` on this
  host answers `ls` in about 2 s. The tier-3 card (`agent/risk-tiers.ts`)
  should become an MCP approval row (`mcp/approval-gate.ts`,
  `createOrReusePending`, then a 60 s `DEFAULT_APPROVAL_WAIT_MS` wait for
  `om approve <id>`); the row is never written, so the ask is lost and the
  session is wedged. Evidence: `cli/91-mcp-downloads*` and
  `cli/92-mcp-downloads-approved*` (no answer) in the run's gallery.
- **New 2026-10-31 (`dfefe0a21`, also on `3cb50a821`): a home with no key
  at boot has no daemon.** When the boot-time guest mint fails (here a guest
  sign-in 429, `Too many guest sign-ins. Try again in 51 minute(s)`), the
  runner logs `no API key and guest mint failed; reads retry minting per
  tick`, prints its start banner, and then exits 1 with `om: No OpenMarket
  API key configured`. The roster's start reads the rooms config
  (`packages/roster/src/runtime.ts:2102` → `runner/roster-host/rooms.ts:28`
  → `actions/rooms/_shared.ts:253-259`, which throws `missing_api_key`
  without a key), and `runner/index.ts:5280` awaits it inside `run`, so the
  throw reaches `runForeground`'s `run_failed` exit. The per-tick re-mint the
  boot line promises never gets a tick. Driven on lanes 18163 (`dfefe0a21`)
  and 18165 (`3cb50a821`) with a stack captured through a scratch debug
  line; [market data](market-data-reads.md) saw the same exit on 18144 on
  2026-10-30. The [daemon guide](daemon-lifecycle-and-health.md) records
  the earlier v0.434.0 behaviour (boot continued without a key).
- **New 2026-10-30 (`3cb50a821`):** on a busy host, `om event push`
  bypasses a live foreground daemon. The CLI's probe gives `/healthz` 200 ms
  and then 1 s more (`runner/client.ts:87-91`); a slower answer counts as
  `busy`, which the code's own comment says "is not proof of a down
  daemon". The push then checks the daemon pidfile, but only daemon mode
  writes it (`runner/index.ts:2277`), so a foreground `om run` is
  invisible. The push then writes the journal itself and reports
  `delivery:"direct"` with "The daemon is not running"
  (`actions/watch/push.ts:182-218`): a second writer beside the live
  consumer, which the guard at `push.ts:200` exists to prevent.
  - The read-only surfaces misreport the same way. `status` reads
    `running:false`, `doctor` fails `daemon: not installed`, `notis`
    refuses with `daemon is unavailable`, and the chat reads
    `om not running ✗` with a `broken` chip.
  - Driven at load average about 150, when `/healthz` took 2 to 3 s.
- **Re-observed 2026-10-30:** the `exchange_id` domain still holds 35
  values. `exchanges` now lists 45, and still includes `LIGHTER`.
- **Re-observed 2026-10-30 (scheduled maintenance):** `tenors` 500, the
  Overview `Watch fires` tile at 0 after inbound fires, and
  `/strategies/<unknown>` reading `Loading…`. The busy-host `event push`
  bypass did not reproduce at load average about 140 (`delivery:"daemon"`).
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
