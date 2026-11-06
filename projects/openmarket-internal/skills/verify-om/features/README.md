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
- [Watch archive and the auto-archive sweep](./watch-archive.md) — #2357, on main since `9bbf2de24`; re-proved on main 2026-11-06
- [Source resolution: one resolver for any source](./source-resolution.md) — PR #2383, branch only; proved on a lane 2026-11-06
- [The approval ledger from the CLI](./approvals-ledger.md) — new 2026-11-06 (#2253 to #2344): `om approvals list`, `om approve`, `om deny` on ledger rows, the harness refusal and the stream frames; the money, chain and fan-out paths are pending
- [Import another agent's setup](./migrate-from-other-agents.md) — new 2026-11-06 (#2366): `om migrate hermes|openclaw|grok-bot` with `--dry-run` and `--yes`
- [Watches with blanks](./watches-with-blanks.md) — branch `daryl/generic-watches`, unmerged; stream follow, registry install, `om want` and search are pending proof
- [A watch step that wakes a roster agent](./watch-agent-step.md) — author, arm, fire
  and read an `ai` step that names `agent` and your `ask`; on main since #2287, keyless-lane path proven 2026-11-04
- [Your installed agents from the CLI and om chat](./agents-cli-and-tui.md) — new
  2026-11-04 (#2282, #2297): `om agent list|show|configure|ps|cancel`, the agents
  overlay (ctrl+x `a`), `/agents` pages and `@name`; 2026-11-05 adds the model
  dial's checks and the agent page's Scope, Model and SETTINGS rows (#2306)
- [Agent files, scopes and trust](./agent-files-and-scopes.md) — new 2026-11-05
  (#2306, #2318): `agent init|try|eval`, `om install <dir> --preflight`, read-only
  installed files and `agents.lock.json`, user and project scopes, `agent trust`,
  and `agent_tune` writing `AGENT.local.md`
- [The roster task door and run pool](./roster-task-pool.md) — submit, pool, cap,
  dedup, cancel and work mentions; a bare lane with a fake model needs no account
- [The ops dashboard](./ops-dashboard.md) — the shell and the observation
  surfaces, redesigned in v0.400.0
- [Watch authoring in the dashboard](./watch-authoring-ui.md) — new in v0.400.0:
  the UI now creates watches, not just shows them
- [Calendar scheduling and polling windows](./calendar-and-polling-windows.md)
- [Chat TUI icon modes](./chat-tui-icons.md) — `chat.icons` emoji, nerd or ascii,
  switched live from the What's new card
- [The dashboard agent panel](./agent-panel.md) — new in v0.400.0; reachable on a
  guest lane only as far as its refusal
- [Paper trading accounts](./paper-accounts.md) — new 2026-10-22
- [Market data reads](./market-data-reads.md)
- [Origin challenge backoff](./origin-challenge-backoff.md) — a Cloudflare
  challenge holds every source on the host, provable with a loopback stub.
- [Firecrawl recovery before whitelist](./firecrawl-first-block.md) — first refusal recovery, repeated-refusal whitelist guidance, and no-key setup.
- [The capability layer over MCP (stdio)](./mcp-stdio.md) — new 2026-10-23:
  handshake, catalog, a read, and the capital gate refusing without spending.
- [Roster ACP host launch and teardown](./roster-acp-host-launch.md) — new
  2026-10-31 (PR #2231, on main since `3498391e7`): the host refuses an unguarded
  launch and tears down its own process group.
- [Chart catalog reads](./chart-catalog-reads.md) — new 2026-10-23: indicator
  and drawing schemas, which need no chart tab.
- [Registry welcome page and personalised search](./registry-welcome-and-search.md)
  — new on main 2026-10-26 (#1947): `om welcome`'s gates and `om search`'s
  health handshake, driven against a loopback fixture registry.
- [Local reads and discovery](./local-reads-and-discovery.md) — new 2026-10-23:
  config and key claims, notification history, enums, schema intents, skills,
  indicator packages.
- [om creates an agent](./agent-create.md) — `agent_create`, `agent_tools`, `agent_fit` and `om agent create`; on main since #2295 and #2303 (re-driven 2026-11-05 on a bare lane): anti-jobs, up to 8 named tools, the fit run, the TTY card and create with `--yes`; the card's Fit row did not see an MCP fit run on main (gap); om chat on a real model pending.
- [A chat agent stops loudly at its budget](./agent-chat-budget.md) — on main since #2304 (re-driven 2026-11-05 on a bare lane): the per-run 40,000-token stop and the 51st run of the day refused 429 `budget_exhausted`, one inbox item each; the daily-token, hourly and @mention paths are not driven.
- [Agent creator lifecycle](./agent-creator-lifecycle.md) — on main since #1948 (`b50ca927d`). Guest-lane CLI/RPC reads and refusals are driven. The eight `@om-core` defaults installed from production on 2026-10-29. Runs, the GUI and sharing are still the historical branch record.
- [Chat transcript layout](./chat-transcript-layout.md) — on main since #2217 and #2219 (v0.480.0): your message as a clay-barred panel, unlabelled replies wrapped at the pane less a 2-column margin, warm bands for fires and digests, faint notice strips, replay identical to live, the spinner above the composer, and the chimes (`chat.sounds`). It needs a local fake model that streams tool calls, and the recipe carries one.
- [Chat shell mode](./chat-shell-mode.md) — on main since #2362: `!` on an empty composer enters a magenta shell mode, the command runs inline with its exit, and its output rides the next message to the model once. Needs a fake model that names markers it received.
- [Chat workspace TUI](./chat-workspace-tui.md) — on main since #2182 (v0.467.0), and `om chat`'s default since #2254 (v0.487.0; `--no-workspace` or `chat.workspace off` for the scrollback chat): the sidebar (WATCHES, FIRES, PAPER, POSITIONS, CALENDAR, USAGE, up to 3 on, dotted rules), the ctrl+x menu and its panel picker, scrolling cards with `o` open (#2207), a click on a transcript fire card (#2225), health-coloured watch dots (#2219), `om sidebar`, and the What's new card in plain `om chat`. It needs a local fake model, and the recipe carries one.
- [Persona setup from om chat](./persona-chat-tools.md) — on main since #2256 (`0d6993613`, v0.487.0): `persona_show`, `persona_infer` (a proposal from your own messages, or `pasted` ones) and the carded `persona_set`. A guest lane plus a scripted fake model drives it through `pasted`; room sampling needs the operator device key, and the recipe carries both.
- [Persona auto-learning and loading into the card](./persona-auto-learning.md) — on main since v0.489.0 (#2275; the CLI rows re-read 2026-11-04): learning applies every update with no approval, and a persona set by hand or by a tool folds into the loaded card (tools merge by rule). It needs a TEST account on a scratch home with `OM_LIBRARY_DIR`, and the recipe carries the headless sign-in.

- [Assistant bridge: daemon tools, deposit and wakes through the hosted MCP](./assistant-bridge-and-wakes.md) — not on main (stack #2350 to #2385, driven 2026-11-05 and 2026-11-06): an assistant on the hosted MCP calls the daemon over a relay stand-in, behind `om assistants on` and one approval; `events/subscribe` and a signed webhook per watch update

- [Hosted chart MCP: tenant state, health and readiness](./hosted-chart-mcp-tenant-state.md) — the
  `om-chart-mcp` binary on an agent port against a local Mongo: boot lines,
  `/healthz` vs `/readyz`, index rebuild, refusals; the tool-call path over
  the production gateway stays unverified without an operator key.
- [Retired kScript package kinds](./kscript-retirement.md) — new on main
  2026-11-01 (#2234, v0.480.3): `search --kind`, `publish`, `install`, the
  chart reference and the MCP tools refuse `kind_retired` before any request,
  and `om open` / `package_open` resolve Indicator packages only.

Not yet mapped, and worth adding when a change touches them: the hosted MCP
tool calls over the production gateway (`chart_*` with a real key), the chart workspace mutations (`om chart` add,
update, remove and drawings, which need a GUI chart tab), the rest of the `om chat` TUI (a real model's turns, slash commands, panels),
the real publish and install paths of packages and the registry (the retired-kind refusals and `om open` are in
[kScript retirement](./kscript-retirement.md)), and the execution/venue verbs.


## Surface inventory

Nightly maintenance, **2026-11-06**, against **origin/main `50fcc594b` (v0.492.0, no cut since)**, 48 commits past the 2026-11-05 nightly's `3a0ea623e` (an ancestor). The census:

- **Commands:** `main.ts` has no diff. New verbs: `om migrate hermes|openclaw|grok-bot` (#2366), `om watch archive|unarchive` and `watch list --archived` (#2357), `om agent status set|clear` (#2359), and the ticket writes `om todo create|update|comment|follow|similar|delete` with `om todo label list|create|rename|merge|delete` (#2341, #2342, #2355).
- **Actions:** 519 registered, fifteen more: `watch_archive`, `watch_unarchive`, `agent_status_set`, `agent_status_clear`, six `todo_*` writes and five `todo_label_*`. `docs/TOOLS.md` lists 517. MCP stdio lists **484** live: the eleven new `todo_*` tools plus `watch_archive` and `watch_unarchive`. `agent_status_*` are badge-only and not on the operator stdio list.
- **Settings:** `watch.auto_archive` (on/off, default on). `plan.fallback_model` now also covers a dead chat sign-in (#2332). `CONFIG_KEYS` is at `cmd/config-keys.ts:157`.
- **Unchanged:** `.env.sample`, 30 RPC files and 9 dashboard routes (`apps/dashboard/src` has no diff).
- **Scaffold:** `WRUN_SCAFFOLD_VERSION` is 116 (#2336 at 114, #2339 at 115, #2379 at 116; `packages/sdk/src/wrun-sdk-sources.ts:1266`). `wrun templates` lists 93; the new one is `dark-pool-prints`. `exchange_id` still has 38 values.
- **Citation audit:** about 100 `path:line` citations checked; five stale ones fixed in current-state rows (`server.ts:1538` → `:1539-1544`, `server.ts:916-920` → `:921-925`, `vault.ts:109-133` → `:108-133`, `config-keys.ts:156` → `:157`, `wrun-sdk-sources.ts:1234` → `:1266`).

User-facing changes:

- #2253 to #2344 (eleven PRs): one approval ledger behind every card. `om approve`/`om deny` answer a ledger row, a money card is answered only on its card, MCP chain requests are read-only owner cards, the Firecrawl offer and the room-access knock are ledger rows, and a card shows on every DM and om chat window. New guide: [approvals-ledger.md](approvals-ledger.md). Most of the fan-out is pending below.
- #2366: `om migrate` imports a Hermes, OpenClaw or Grok Bot setup. New guide: [migrate-from-other-agents.md](migrate-from-other-agents.md).
- #2357: watch archive and the daily sweep, now on main. [watch-archive.md](watch-archive.md) is re-proved on main and rewritten to the entry contract.
- #2307, #2309, #2328, #2363, #2362: `r` reads more, Enter opens a card's page (`o` now types), `l` opens a fire's link, `/` searches a watch page's Latest, the list pages share one frame, and `!` shell mode is on main. [chat-workspace-tui.md](chat-workspace-tui.md) and [chat-shell-mode.md](chat-shell-mode.md) are updated. What's new has 14 entries.
- Tickets and agent status (#2341 to #2364, #2380, #2359): refusals only on a guest lane; the rest needs a rooms account. Pending rows below.
- #2332, #2327, #2361, #2373, #2360, #2379, #2336, #2339: pending rows below. #2331, #2345, #2346, #2348, #2349, #2354, #2369 to #2372, #2302 have nothing to see.

Live this pass, host load average 10 at the start and about 3.3 later:

- **Lanes:** guest lane 18163 booted at 19:18Z with no 429. Bare lane 18165 with a scripted fake model on 18164. Origin stub on 18166.
- **First drives on main:** the archive sweep on reboot and the archive verbs; `om migrate` on all three test fixtures; the approval ledger (`approvals list` on seeded rows, `om approve` refused from an auto-approve harness, `om deny` on an MCP row and on an order card, `approval_changed`/`approval_resolved` on `/events/v1`); the ticket and agent-status refusals; 484 MCP tools; `wrun create --template dark-pool-prints` at scaffold 116; `r`, Enter and `l` on a sidebar fire card; `/` on a watch page; the `/watches` and `/usage` frames; What's new `1 of 14` and `2 of 14`; shell mode on main.
- **Re-driven:** the fire chain, daemon health, every dashboard route, the Create-watch dialog's kinds and the feed step, the agent panel refusal, local reads, market data, paper, calendar, chart catalog, the real registry, the kScript refusal, the roster ACP refusal, the task door on the bare lane, and the origin-challenge hold.
- **Doc drift fixed:** `o` → Enter on cards, the What's new count and second entry, shell mode now on main, the MCP tool count, `wrun templates` 93 and scaffold 116, the archive guide's shape, five citations.
- **New gaps:** see the gaps list (`watch show` calls a held feed `broken` and suggests `run now`; `om migrate` with no platform blocks headless; the archived-condition rewind; the Latest list's `filtered out` for unsent fires; `approvals list` names a tool card `mcp`).
- **Not re-driven:** loopback HTTP MCP; `instruments`/`option-chain`; the Firecrawl no-key refusal and the offer row; the hosted chart MCP; the registry fixture branches; polling windows; the persona flows; agent create, fit and both budget stops; agent files, scopes and tune beyond `agent list --lock`; the watch agent step; the transcript layout beyond the shell rows; the icons switch; the UI-authored feed past its first step.

Evidence: `http://127.0.0.1:8098/vom-nightly-20261106/r1/` (dashboard frames, `aria/`, `cli/` transcripts, `events.sse`, `approvals.sse`, `tui/` captures).

Nightly maintenance, **2026-11-05**, against **origin/main `3a0ea623e` (v0.492.0)**, 25 commits past the 2026-11-04 nightly's `9acb5fb56` (an ancestor). The census:

- **Commands:** `main.ts` has no diff. New `om agent` verbs `create --file`, `init`, `try`, `eval` (moved out of `OM_DEV`) and `trust [--forget]`; `agent list --lock` and `--here`; `om install --preflight`. `om roster`, `agent runs` and `agent pause` still need `OM_DEV=1`.
- **Actions:** 504 registered, nine more: `agent_create`, `agent_eval`, `agent_fit`, `agent_init`, `agent_tools`, `agent_trust`, `agent_try`, `agent_tune`, `agent_tune_apply`. `docs/TOOLS.md` lists 502. MCP stdio lists **471** live (all but `agent_trust`, which is on no posture).
- **Unchanged:** `CONFIG_KEYS`, `.env.sample`, 30 RPC files, 9 dashboard routes (only `pages/watch-detail.tsx` changed), `WRUN_SCAFFOLD_VERSION` 113 (`wrun-sdk-sources.ts:1234`), `wrun templates` 92 and `exchange_id` 38, both read live.
- **Citation audit:** 94 `path:line` citations checked; four stale ones fixed here (`main.ts:63` → `:65`, `runtime.ts:2107` → `:2160`, `authoring.ts:1161-1179` → `:1166-1188`, `status-sentence.ts:4727-4751` → `:4724-4770`).

User-facing changes:

- #2295, #2303: om creates an agent from a draft, now on main. #2304: the chat budget, now on main. Both guides are re-proved on main.
- #2306, #2318: the model dial, the authoring kit, tune, install with pins, read-only files and a lock, user and project scopes with trust. New guide: [agent-files-and-scopes.md](agent-files-and-scopes.md). [agents-cli-and-tui.md](agents-cli-and-tui.md) is updated.
- #2300: monthly and every-other-week timers and a summary on chosen days. #2310: a paused or removed upstream stands its readers down. Both are in [watch-lifecycle-cli.md](watch-lifecycle-cli.md).
- #2311, #2315, #2326: `/provider` picker, the away-band click, Esc out of `/setup`. These are in [chat-workspace-tui.md](chat-workspace-tui.md). The What's new card has 11 entries.
- Pending rows below: #2314, #2305, #2308, #2325, #2333 and #2335.
- Nothing to see: #2002, #2299, #2312, #2317, #2319, #2322, #2324.

Live this pass, host load average about 4.4:

- **Lanes:** guest lane 18163, booted in 2 s at 19:19Z with no 429. Bare lane 18165 with a scripted fake model on 18164 (it reports `usage`). Origin stub on 18166.
- **Driven:** every guide except `persona-auto-learning` and the `persona-chat-tools` chat flow.
- **First drives on main:** agent create and fit, both budget stops, the agent files and scopes, tune over MCP, the model dial, monthly timers, the upstream stand-down, Esc from `/setup`, the 11 What's new titles.
- **Re-driven:** the fire chain, daemon health, every dashboard route, the RSS authoring flow, paper, calendar, chart catalog, the real registry, the kScript refusals, local reads, market data, MCP stdio, the hosted chart MCP refusals, the roster ACP refusal, and the origin-challenge hold with its recovery and the Firecrawl no-key refusal.
- **Doc drift fixed:**
  - the What's new count and the Nerd icons ordinal;
  - `eval` is no longer behind `OM_DEV`;
  - `agent_fit` takes the draft at top level;
  - the door's 16-queue `agent_busy` ahead of the budget;
  - the `agent list` JSON and text fields;
  - four citations.
- **New gaps:** see the gaps list:
  - the create card misses an MCP fit;
  - the `agent init` scaffold is refused in a scope;
  - the remove refusal omits the cascade;
  - a paused upstream reads `is gone`;
  - `agent trust` asks nothing;
  - `/provider` on an env provider.
- **Not re-driven:**
  - loopback HTTP MCP and the memory round trip;
  - `instruments`/`option-chain`;
  - the sidebar card clicks and picker, the spinner and tool rows;
  - the doubling branch and the configured Firecrawl path;
  - the hosted chart MCP against Mongo;
  - the registry fixture branches;
  - polling windows and the Paper tab;
  - the persona chat flow;
  - the icons switch itself.

Evidence: `http://127.0.0.1:8098/vom-nightly-20261105/r1/` (dashboard frames, `cli/` transcripts, `events.sse`, `tui/` captures).

Nightly maintenance, **2026-11-04**, against **origin/main `9acb5fb56` (v0.491.0)**, 35 commits past the 2026-11-03 nightly's `777ee7f21` (an ancestor). The census:

- **Commands:** new `om todo` (`list`, `get`) and `om agent` `list`, `show`, `configure`, `portrait`, `ps`, `cancel` (always on); `runs`, `pause`, `eval` stay behind `OM_DEV=1`; `om approvals list` takes `--kind`. `main.ts` moved by two or three lines, so the `main.ts` citations in 12 rows below are fixed.
- **Actions:** 495 registered, ten more: `agent_run`, `agent_runs`, `agent_run_cancel`, `agent_list`, `agent_configure`, `agent_portrait`, `firecrawl_offers_pause`, `firecrawl_offers_resume`, `todo_list`, `todo_get`. `docs/TOOLS.md` lists 493. MCP stdio lists **463** (the six `agent_*` and the two `todo_*`; the Firecrawl pair is agent-only).
- **Settings:** `firecrawl.offers` (on/off, default on, #2265) and `chat.motion` (on/off, default on, stored as `tui.motion`, #2297).
- **Unchanged:** 30 RPC files and 9 dashboard routes (`apps/dashboard/src` has no diff; #2298 is test-only). New daemon routes ride the roster API (`/rpc/v1/roster/tasks`, `/instances`, `/runs`) and `GET /rpc/v1/approvals/inbox`.
- **Scaffold:** `WRUN_SCAFFOLD_VERSION` is 113 (#2283, `packages/sdk/src/wrun-sdk-sources.ts:1234`); `wrun templates` still lists 92; `exchange_id` has 38 values.
- **Citation audit:** 17 stale `path:line` citations found by a reader; fixed here (`main.ts` in 12 rows, `config-keys.ts:154` → `:156`) and in the guides (`wrun-sdk-sources.ts:1217` → `:1234`, `sidebar/contract.ts:94` → `:98`, `tui-icons.ts:39` → `:43`, `tui-turn-row.ts:15` → `:17`).

User-facing changes:

- #2269, #2282, #2297: agents run alone (the task door, `agent_run`, `@name`, `@om`), a run pool of 4, `om agent list|show|configure|ps|cancel`, the agents overlay (ctrl+x `a`) and `/agents` pages, portraits and `chat.motion`. New guide: [agents-cli-and-tui.md](agents-cli-and-tui.md); new rows below.
- #2287: a watch's agent step carries `ask`, authors from the CLI and says why it stopped. [watch-agent-step.md](watch-agent-step.md) is re-proved on main.
- #2284: timers on chosen days, said in words on the cards. New `timer-days` sub-feature in [watch-lifecycle-cli.md](watch-lifecycle-cli.md).
- #2258 and #2301: one approvals inbox of five kinds, three drafts per topic, DM drafts. #2291: `om todo`. #2265: Firecrawl offer pause and durable deny, now on main. #2275, #2288, #2289: persona learning applies itself, `Room drafts: first N of M`, the hold routes gone. #2292: the hosted chat reaches home-daemon agents. #2285: the mode line aligns with the input. #2262, #2281, #2273, #2283, `9acb5fb56`, `e4346c6a9`: instruments cap, v3 markets, wrun pins and contracts (pending rows below). #2296 and #2298 have nothing to see.

Live this pass, on lane 18163 with a fake model on 18164, the origin stub on 18166 and a fixture-key lane on 18165, host load average about 3.5. The guest lane booted in 2 s at 19:19Z with no 429.

- **Driven:** every guide except `agent-create` (branch-only, `daryl/agent-create-eval`), `persona-chat-tools` (its chat flow) and `registry-welcome-and-search`'s fixture branches. **First drives on main:** the agent step with `ask` (#2287), the `om agent` verbs, the agents overlay and pages, `@nope`, the approvals inbox, the `om todo` refusals, `Room drafts: first 23 of 40 lines`, the Firecrawl pause path and `--deny`, the 8-entry What's new card, MCP's 463 tools. **Re-driven:** the fire chain, watch CRUD and state verbs, every dashboard route, the RSS authoring flow, the agent panel refusal, the origin-challenge hold AND its recovery at `until`, the Firecrawl no-key refusal, paper, calendar with the polling windows, chart catalog, the real registry, the kScript refusals, local reads, market data, the default agents, the hosted chart MCP refusals, the roster ACP refusal.
- **Doc drift fixed:** the What's new ordinals (Nerd icons is now 8 of 8), the ctrl+x menu's `a agents`, the `OM_DEV` verb list, the agent step and persona and Firecrawl pause guides now on main, scaffold 113, the approvals and todo reads, 17 citations.
- **Resolved:** MCP `package_open` answered in a fresh session (the 2026-11-03 `tool_failed` did not recur).
- **New observations:** see the gaps list (`agent ps` shows the watch envelope as the ask; `setup firecrawl --deny` says `action: allowed`; a guest feed's summary FAULT reads `the credential was refused`; a fresh lane's chat warns of state from another guest account).
- **Not re-driven:** loopback HTTP MCP, the memory round trip, `instruments`/`option-chain`, the sidebar card clicks and picker, `om sidebar set`, the spinner and tool rows, the doubling branch, the Firecrawl configured path, the hosted chart MCP against Mongo, the registry fixture branches, the kScript `<dir>` refusals, the Paper tab, the persona chat flow.

Evidence: `http://127.0.0.1:8098/vom-nightly-20261104/r1/` (dashboard frames, `cli/` transcripts, `events.sse`, `tui/` captures).

Nightly maintenance, **2026-11-03**, against **origin/main `777ee7f21` (v0.488.0)**, 26 commits past the scheduled pass's `587ce2d0b` (an ancestor). The census:

- **Commands:** `main.ts` has no diff, so the count is unchanged.
- **Actions:** 485 registered, three more: `persona_show`, `persona_infer` and `persona_set` (rooms, #2256, in `actions/rooms-registry.ts`; `actions/index.ts` has no diff). `docs/TOOLS.md` lists 483. MCP stdio lists **455** tools: `persona_show` only, since `persona_infer` and `persona_set` are not offered there.
- **Settings:** `mcp.operator_voice` is new (on/off, default off, #2250), and `chat.workspace` now defaults to `on` (#2254).
- **Unchanged:** 30 RPC files and 9 dashboard routes. `apps/dashboard/src` and `runner/http/rpc` have no diff.
- **Scaffold:** `WRUN_SCAFFOLD_VERSION` is 111 (#2267, `packages/sdk/src/wrun-sdk-sources.ts:1217`), and `wrun templates` still lists 92.
- **Citation audit:** about 80 `path:line` citations; three were stale and are fixed (`cmd/config-keys.ts:160` → `:154` here and in local reads, `push.ts:200` → `:201`, `rpc/system.ts:403` → `:404`).

User-facing changes:

- #2254: `om chat` opens as the workspace by default; `--no-workspace` (one session) or `config set chat.workspace off` keeps the scrollback chat; the What's new card now shows in the workspace, leads with `Workspace is now the default` / `[ Turn it off ]`, and pages with ctrl+x `.` and `,`. The workspace, icons and transcript guides are rewritten for it.
- #2256: `om chat` sets up your persona (`persona_show`, `persona_infer` with room sampling or `pasted` lines, the carded `persona_set`); `cmd/persona.ts` moved its sampling into `runner/rooms/persona-{sample,view}.ts` with no CLI change. #2250: `mcp.operator_voice` adds the persona to a badge session's brief, and `om persona show` ends with an `MCP clients:` row.
- #2260: a Hyperliquid name search also searches HIP-3. #2224: Polymarket `points` need a condition id; a TPO read without `from` asks for the lookback and marks `stale_newest_session`. New rows below.
- #2267 and #2270: a wrun build writes the converging warm-up stamp by default (`OM_WRUN_CONVERGES=0` turns it off). New row below.
- #2257: a daemon-raised card no longer holds the conversation. New pending row below. #2251 is a redraw speed-up with nothing to see.
- #2249 and #2259 change warm-up bar planning and the `dealer-positioning` recipe (a chart host); #2248 and #2266 are rooms-client work (verify-om-chat); the wrun17 and wrun18 heads and the contracts 5.51 to 5.53 and SDK releases are kit changes.

Live this pass, on lane 18163 with a fake model on 18164 and the origin stub on 18166, host load average about 2.8. The first `up` died on a guest sign-in 429 (`Try again in 35 minute(s)`, read through one `coins` call). The key-free surfaces were driven on the keyless home meanwhile, including all of #2254 and the persona flow (chat needs no daemon); the lane booted in 3 s at 19:55Z.

- **Driven:** every guide. **First drives on main:** the workspace default, the `[ Turn it off ]` card, ctrl+x `.` paging and both flags; the persona flow on a guest lane through `pasted` (infer, the card, decline, approve); `om persona` and `mcp.operator_voice` on the CLI and over MCP; the HIP-3 search and the Polymarket id refusal on the CLI and over MCP; `wrun create` at scaffold 111 and a `wrun build` with no stamp. **Re-driven:** the fire chain, watch CRUD and the state verbs, MCP stdio, every dashboard route, the RSS authoring flow, the agent panel refusal, the origin-challenge hold and its recovery at `until`, the Firecrawl no-key refusal, paper, calendar with the polling windows, chart catalog, the real registry, the kScript refusals, local reads, the default agents, the hosted chart MCP refusals, the roster ACP refusal.
- **Doc drift fixed:** the chat guides' plain-chat recipes (a bare launch is now the workspace), the What's new card's text, keys and placement, the icons recipe (the Nerd entry is second), the persona guide (on main; the `pasted` path), the operator-voice notes (on main), scaffold 111 and the build stamp, three citations.
- **New product gaps and observations:** see the gaps list (`package_open` over MCP, `points --type TPO_AGG` 500).
- **Not re-driven:** loopback HTTP MCP, the memory round trip, `instruments`/`option-chain`, the sidebar card clicks and the picker, `om sidebar set`, replay and the spinner, the doubling branch, the Firecrawl configured path, the hosted chart MCP against Mongo, the registry fixture branches, the kScript `<dir>` refusals, the journal reads and maintenance verbs beyond the state verbs, the Paper tab.

Evidence: `http://127.0.0.1:8098/vom-nightly-20261103/r1/` (17 dashboard frames, `cli/` transcripts, `events.sse`, `tui/` captures, `fake-log.jsonl`).

Scheduled maintenance, **2026-11-02**, against **origin/main `587ce2d0b` (v0.480.3)**, seven commits past the nightly's `2567b7974` (an ancestor). Lane 18168 (fresh guest home, `OM_FEED_ALLOW_LOOPBACK=1`), origin stub 18169, fake model 18170, a private tmux server; all stopped. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261102/r1/`.

- **Delta:**
  - #2231 (`3498391e7`) and #2247 (`587ce2d0b`) are now on main. Their rows and guides no longer say "pending on main".
  - The `[footprint]` line, the `__roster-acp` refusal from the source CLI, and the `chat.icons` What's new switch were each driven on main.
  - #2245 and #2246 raised `WRUN_SCAFFOLD_VERSION` to 110 (`wrun-sdk-sources.ts:1204`), and `wrun create --template liquidation-map` wrote 110.
  - `908ff8371` and `5ba9c0155` are SDK and hosted-worker only.
- **Census, new angles:** config keys, environment switches and dashboard empty states. About 85 `CONFIG_KEYS` had no coverage. Four rows were added at the bottom of the table: config get/set (partly proved), env switches (pending), dashboard empties (partly) and channel webhooks (pending).
- **Citation audit:** all 75 `path:line` citations were checked. These were stale and are now fixed:
  - `server.ts:1546` → `:1538`, and `:915-919` → `:916-920`;
  - `rpc/system.ts:403` → `:404`;
  - `wrun-sdk-sources.ts:1180` → `:1204`;
  - `main.ts:236` → `:237`, `:212` → `:213`, and `:67,69` → `:68,69`;
  - `gen-indicator-kit-bundle.ts:253` → `:598`, and `:253-260` → `:306-316`;
  - `runner/index.ts:2284` → `:2285`, and `:5293` → `:5296`.
- **Re-driven at `587ce2d0b`:** every guide except `hosted-chart-mcp-tenant-state` (it needs Mongo and the chart-mcp build). Each re-driven guide carries a scheduled-maintenance stamp naming what was and was not driven.
- **Newly observed:**
  - The Firecrawl no-key page probe is not held by a feed's cooldown. Once the origin answers again it reads `llm_not_configured`.
  - On a dashboard-authored 1-minute feed, the hold's FAULT row names the host without a feed title.

Nightly maintenance, **2026-11-02**, against **origin/main `2567b7974` (v0.480.3)**, 17 commits past `7ce379c45` (an ancestor). The census:

- **Commands:** `main.ts` has no diff, so the count is unchanged.
- **Actions:** 482 registered, none added or removed (`actions/index.ts` has no diff; the same 19 categories). `docs/TOOLS.md` lists 480. MCP stdio lists 454 tools; two descriptions changed (`series_publish`, `watch_state_clear`) and `series_publish` gained `price`, `stop_sales`, `resume_sales` and `free`.
- **Unchanged:** 30 RPC files and 9 dashboard routes. `apps/dashboard/src` and `runner/http/rpc` have no diff.
- **Scaffold:** `WRUN_SCAFFOLD_VERSION` is 108 (#2239, `packages/sdk/src/wrun-sdk-sources.ts:1180`), and `wrun templates` still lists 92.

User-facing changes:

- #2240 and #2241 sell a live-series feed: `om series publish --price 9/mo|20 once` (at least $2.50; needs a sign-in session and a plan that can sell), `--stop-sales`, `--resume-sales` and `--free`; `series show` prints `Visibility:` and `series list` marks a listed feed; `series delete` refuses a listed one; `OM_ORANGE_ORIGIN` names the marketplace (default `https://chart.openmarket.xyz`). New row below; the refusals are in [local reads](local-reads-and-discovery.md).
- #2244 anchors a target-step chain's package record at its first arm, so a re-arm keeps it; `om watch state clear` drops the anchor and reports `record_restarts` (`now` or `at_next_arm`), and the arm card says where the record runs from. New row below; the guest-reachable half is in [watch lifecycle](watch-lifecycle-cli.md).
- #2242 sizes a paper target leg against the lot held at booking (`target_entry_exited`, `target_close_noop`, `target_open_deferred`; `planned … on … held` leg lines). Recorded on the target-step row; needs a condition fire.
- #2239 (scaffold 108): keyed rows and tapes (`visible_by`, `needed_by`) and the `min_coins` tape floor; `wrun create` refreshes `src/sdk/declare.ts` and `scripts/wrun-prebuild.mjs`. #2243: the templates' `runsOn` reads `CME futures in your browser`. #2237: the 42 options Indicators' descriptions, labels and cookbook pages are rewritten in plain words (the `wrun templates` descriptions changed).
- #2238 is rooms-client ticket work (verify-om-chat); the contracts 5.46 to 5.48 and SDK 0.483 to 0.485 releases and the `docs/indicators` pages are chart-host and documentation changes.

Live this pass, on lane 18163 with a fake model on 18164 and the origin stub on 18166 (hosted MCP over HTTP on 18165), host load average about 4. The first `up` died on a guest sign-in 429 (`Try again in 15 minute(s)`, read through one `coins` call); the key-free surfaces were driven on the keyless home meanwhile (enum, wrun templates and create, skills, config, schema, chart catalog, the kScript refusals, MCP stdio `tools/list`, the hosted chart MCP refusals), and the lane booted in 2 s at 19:41Z with the eight defaults installing 4 s later.

- **Driven:** every guide. The fire chain (door 202 and 401, three stream events per id, the journal, CLI push `delivery: daemon`, the dashboard row and detail); watch CRUD, the journal reads, the maintenance verbs and refusals, the RPC refusals; MCP stdio (454 tools, thirteen calls) and hosted HTTP (444 tools); every dashboard route, the Paper tab, the agent panel refusal, the RSS authoring flow through to a resumed feed polling the stub; the origin-challenge hold AND the recovery at `until`; the Firecrawl no-key refusal inside the hold; paper, calendar (occurrence review and the polling windows), chart catalog, the real registry, local reads, the default agents, the hosted chart MCP refusals with exit codes; plain `om chat` (What's new, a tool turn) and `om chat --workspace` (the frame, the sidebar watch-row card). **New:** the #2240 sales refusals on the CLI and the `capital_yolo_harness` answer over MCP; `watch state show`/`clear` on a timer watch (`not_a_condition_watch`) and on an RSI condition watch (`record_restarts: null`, `cleared <id>`); `wrun create` at scaffold 108 with the `in your browser` lines; `symbols` needing `--type`.
- **Doc drift fixed:** the wrun row's stale citation (`wrun-sdk-sources.ts:1159` → `:1180`, 106 → 108); the `wrun create` form (package name first); the series section (the sales flags, `Visibility:`, the `registry_unavailable` dry-run); `symbols` needs `--type`; the `indicator list`/`drawing schema` and `schema read <intent>`/`skill show` gaps closed.
- **Observations, not gaps:** a plain `series publish --dry-run` read `registry_unavailable` (503, "could not confirm this account's username") where earlier passes read `publish_rejected`; `symbols --type TRADE_AGG` answers 3.27 million raw symbols (198 MB) with no paging; `exchanges` carries `refusedTypes` (five data types the guest plan refuses) and the home then wrote `last-plan-refusal.json` `{"kind":"data_type"}`, which is what the chat footer's `data limit hit` chip reads (the 2026-11-01 "possible gap" has a cause); a challenged feed's FAULT names the host with the feed title (`127.0.0.1: Origin stub`); the Firecrawl probe of an article inside a hold runs its own `next try` clock; a scaffold-108 workspace carries no `WRUN-OFFCHART` note in `src/sdk` but five in `scripts/wrun-prebuild.mjs`.
- **Re-observed product gaps:** the guest sign-in 429 leaves a keyless home with no daemon (the boot exit); `tenors` 500; `points --exchange BYBIT_FUTURES` refused; the `/strategies/<unknown>` flicker; the `indicator_unknown` hint naming the retired kScript form; the hold's status rows displaced by `not checked since` at 5 minutes; a second profiler `start` saying `already:false`; `exchange_id` 35 against 45 venues.
- **Not re-driven:** the memory round trip, `instruments`/`option-chain` under v3, the agent creator beyond the guest reads, the chat approval card and replay, the 20-fire card scroll, `om sidebar set`, the panel picker, the Firecrawl configured path, the doubling branch, the hosted chart MCP against Mongo, the registry fixture branches, `--keys period`.

Evidence: `http://127.0.0.1:8098/vom-nightly-20261102/r1/` (dashboard and TUI frames, `cli/` transcripts, `events.sse`, the stub and lane-log excerpts).

Nightly maintenance, **2026-11-01**, against **origin/main `7ce379c45` (v0.480.3)**, 13 commits past `dfefe0a21` (an ancestor). The census:

- **Commands:** `main.ts` has no diff, so the count is unchanged.
- **Actions:** 482 registered, none added or removed (rooms 193, watch 75, chart 45, system 34, market-data 19, packages 17, execution 13, hyperliquid 12, paper 11, research 11, news 9, polymarket 8, wallet 8, polymarket-account 6, calendar 6, wrun 5, memory 4, payments 4, state 2). `docs/TOOLS.md` lists 480. MCP stdio lists 454 tools; four descriptions changed for the retirement (`package_install`, `package_open`, `package_search`, `chart_indicator_add`).
- **Unchanged:** 30 RPC files and 9 dashboard routes. `apps/dashboard/src` and `runner/http/rpc` have no diff.
- **Scaffold:** `WRUN_SCAFFOLD_VERSION` is 107 (#2235), and `wrun templates` lists 92.

User-facing changes:

- #2234 retires the kScript package kinds: `kscript-indicator` and `kscript-library` leave `PACKAGE_KINDS`; `om search --kind`, `om publish`, `om install`, `om open`, `chart_indicator_add` and `chart_indicator_schema` refuse `kind_retired`; a default search drops such rows and counts them as `hidden`; `om open` and `package_open` resolve Indicator packages only (`kind` always `wrun-indicator`, no `script_id`). New guide: [kScript retirement](kscript-retirement.md).
- #2235 adds the `flow-vwap` starter (group `Order flow`) and the `options_flow` `underlying` knob; scaffold 107 refreshes `src/sdk/declare.ts` and `scripts/wrun-prebuild.mjs`.
- #2223 keeps the daemon's remote-control link re-dialing after a failed first dial (about 1, 5, 15 and 60 min, then stop) and pages `📡 Remote control offline` once; a guest never dials, and its `agent.log` reads `remote control dark: guest session`.
- #2236, the wrun14/wrun15 hosted heads and the SDK releases are kit and contracts changes a chart host shows; #2232 and #2233 are rooms-client ticket fixes (verify-om-chat).

Live this pass, on lane 18163 with a fake model on 18164 and the origin stub on 18166, host load average about 2.9. The guest mint landed at boot (no 429 tonight) and the eight default agents installed 6 s later.

- **Driven:** every guide. The fire chain (door, stream, journal, CLI push, dashboard row); watch CRUD with the lot fields, the journal reads, the maintenance verbs and refusals; the RPC refusals; MCP stdio (454 tools, the capital gate, `file_create`, `channel_default_set`, the aliases, the kScript refusals and the `package_open` Indicator path); every dashboard route, the Paper tab, the flicker, the agent panel refusal, the RSS authoring flow to a resumed feed; the origin-challenge hold AND its recovery at `until`; the Firecrawl no-key refusal inside the hold; paper, calendar (occurrence review and the polling windows), chart catalog, registry, local reads, the default agents, hosted chart MCP refusals; plain `om chat` (What's new, a tool turn, 90 columns) and `om chat --workspace` (frame, picker, the fire-card click). New: the kScript refusals on the CLI and over MCP, `om open @om-core/rsi` and `package_open`, `wrun create --template flow-vwap` at scaffold 107, the `remote control dark: guest session` gate line.
- **New product gap:** the `indicator_unknown` hint still names the retired kScript form.
- **Observations, not gaps:** `terms` timed out against the staging registry twice while production answered; three consecutive dashboard loads returned Chrome's `chrome-error://chromewebdata/` with the daemon healthy, and a retry rendered them; the first MCP `package_search` and `package_open` of one session stalled 30 s, a fresh session answered in 250 ms.
- **Not re-driven:** hosted MCP over loopback HTTP, the memory round trip, `instruments`/`option-chain` under v3, the agent creator beyond the guest reads, the chat approval card and replay, the 20-fire card scroll, `om sidebar set`, the Firecrawl configured path, the doubling branch.

Evidence: `http://127.0.0.1:8098/vom-nightly-20261101/r1/` (dashboard frames, `cli/` transcripts, `events.sse`, the TUI captures).

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

Scheduled maintenance, **2026-10-29**, against **origin/main `7ec575e55`**, one commit past the nightly's `32ca0d6c7`. #2194 moves the Indicator kit to scaffold 106. The three Feeds starters read a placeholder `@you/your-feed` (`@you/your-events` for `feed-events`) until `ref` is set. The kit build refuses internal notes in the texts it bundles (`packages/cli/scripts/gen-indicator-kit-bundle.ts:598`). The diff touches nothing under `cmd/`, `main.ts`, `actions/`, `rpc/` or `apps/dashboard/src`; only `runner/wrun/authoring.ts` changed under `packages/cli/src`. So the command, action, RPC and route counts below still hold, and no outcome row was added.

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

- **Commands:** one new top-level command, `sidebar` (`main.ts:65`). That makes 95 by this table's convention, or 98 quoted names in the `COMMAND_MODULES` `names:` arrays, against 97 before.
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
  `--help`. With `OM_DEV=1` in the CLI process, main.ts:237 also registers
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
| Check the install: doctor, status, logs | `cmd/{doctor,status,logs}.ts` | [daemon-lifecycle-and-health.md](daemon-lifecycle-and-health.md) | 2026-11-04, main `9acb5fb56` (boot in 2 s with no 429; doctor `ok:true`, `status` running, `service status`, `logs`, the wrapper refusing `service install`); 2026-11-03, main `777ee7f21` (the first `up` died on a guest 429, 35 minutes; then a 3-second boot; doctor `ok:true`, `status` running, `service status`, `logs` empty, the wrapper's `service install` refusal); 2026-11-02, main `2567b7974` (boot in 2 s once the guest 429 window passed; doctor `ok:true`, 14 checks; `status` running; `service status` INACTIVE loops; `logs` the CLI line only; the wrapper's `service install` refusal); 2026-11-01, main `7ce379c45` (boot in 2 s with the guest mint landing; doctor `ok:true`, `status` running, `service status` foreground, `logs` empty, the wrapper's `service install` refusal); 2026-10-31, main `dfefe0a21` (doctor `ok:true`, `status` running, `service status` foreground, `logs` empty, the wrapper's `service install` refusal; the first `up` died on a guest 429, see the README gap); 2026-10-30 scheduled maintenance, main `3cb50a821` (doctor 14 checks, `status` running, `/healthz`). 2026-10-29, main `32ca0d6c7` (14 doctor checks, status, service status) | None. |
| See the daemon's footprint and slow statements; profile a stalled daemon | `runner/http/server.ts:1539-1544`; `runner/db-timing.ts`; `runner/http/rpc/system.ts` (`profile`) | [daemon-lifecycle-and-health.md](daemon-lifecycle-and-health.md) (`profile`, footprint step) | 2026-11-04, main `9acb5fb56` (`/healthz` `memory.rss_mb` 496, `slow_sql: []`; profiler `stacks` 409 before `start`); 2026-11-03, main `777ee7f21` (`/healthz` `memory`/`slow_sql`; profiler 409, 200 twice with `already:false`, `stacks` 15 samples; `{action:"stop"}` → `bad_request`); 2026-11-02, main `2567b7974` (`memory`/`slow_sql`/`roster` on `/healthz`; profiler 409/400/200/stacks; a second `start` repeated `started_at` with `already:false`); 2026-11-01, main `7ce379c45` (`memory`/`slow_sql`/`roster` on `/healthz`; `stacks` before a start → 409 `not_started`); 2026-10-31, main `dfefe0a21` (`stacks` before a start → 409 `not_started` only); 2026-10-28, main `a8fa10974` (`memory`/`slow_sql`/`roster` on `/healthz`; profiler 409/400/200/stacks) | No real slow statement was produced (`OM_DB_SLOW_MS=1` plus a restart would). `start` always says `already:false` (product gap). |
| Read the daemon's memory footprint from its log over days | `runner/footprint.ts`; `runner/index.ts` (heartbeat `onBeat`) | [daemon-lifecycle-and-health.md](daemon-lifecycle-and-health.md) (footprint line) | 2026-11-04, main `9acb5fb56` (`[footprint] rss 434 MB heap_used 140 MB heap_total 181 MB pressure normal`); 2026-11-03, main `777ee7f21` (`[footprint] rss 664 MB heap_used 157 MB heap_total 194 MB pressure normal` at the first heartbeat); 2026-11-02, main `587ce2d0b` (scheduled; lane 18168: `[footprint] rss 396 MB heap_used 154 MB heap_total 195 MB pressure normal` in the lane log at the first heartbeat); earlier 2026-10-30, branch `daryl/roster-teardown-footprint` PR #2231 (lane 18103: lines at +30 s, +5 min, +10 min, `pressure normal` matching sysctl 1) | On main since `3498391e7`. A source lane logs it to the lane log, not `runner.log`. |
| A stdio servant says when its om version differs from the daemon's | `mcp/sse-bridge.ts` (`probeDaemon`, `versionMismatchWarner`) | [mcp-stdio.md](mcp-stdio.md) (Stale-version warning) | 2026-10-30, branch PR #2231 (0.480.2 servant against the 0.478.0 daemon: one `openmarket.servant` warning) | On main since `3498391e7`; not re-driven on main. Only the daemon-older wording was driven live; servant-older is test-pinned. Needs a live servant's badge in env. |
| The roster ACP host refuses an unguarded launch and tears down its group | `bootstrap/roster-acp.ts`; `bootstrap/process-group.ts`; `packages/roster/src/adapters/acp-guardian.ts` | [roster-acp-host-launch.md](roster-acp-host-launch.md) | 2026-11-04, main `9acb5fb56` (the unguarded refusal, exit 2); 2026-11-03, main `777ee7f21` (the unguarded refusal, exit 2); 2026-11-02, main `587ce2d0b` (scheduled; the unguarded refusal from the source CLI: `control-om om -- __roster-acp claude /usr/bin/true` exit 2 with the refusal line); earlier 2026-10-30, branch PR #2231 (unguarded probe: exit 2 and the refusal line, no agent; detached SIGTERM-only probe: no survivor) | On main since `3498391e7`; the teardown ladder is proved only on the branch. Driven through the rig probe, not the daemon's roster. |
| Look up enum domains, schema intents and bundled skills | `cmd/{enum,schema,skill}.ts`; `packages/sdk/src/types/enum-domains.ts` | [local-reads-and-discovery.md](local-reads-and-discovery.md) | 2026-11-04, main `9acb5fb56` (`enum --list` with `exchange_id` 38, `schema read condition_create`, `skill list`); 2026-11-03, main `777ee7f21` (`enum --list`, `indicator_template` 92, `schema read`, `skill list` (`--format` refused `unknown option`), `skill show watch`, `skill show nope-skill` exit 2); 2026-11-02, main `2567b7974` (`enum --list`, `indicator_template` 92, `schema read` and `schema read condition_create`, `skill list`, `skill show indicators` and `skill show watch`, `skill show nope-skill` refused); 2026-11-01, main `7ce379c45` (`enum --list` 26 domains, `exchange_id` 35, `indicator_template` 92 with `flow-vwap`; `schema read` 7 intents; `skill list` 16 names); 2026-10-31, main `dfefe0a21` (`enum --list` 26 domains, `enum --domain exchange_id` still 35 values and lists neither `BYBIT_FUTURES` nor `BYBIT_LINEAR`, which #2202 aliases at parse time only; `schema read`, `skill list`); 2026-10-28, main `a8fa10974` (`enum --list`/`--domain`, `schema read`, `skill list`) | None. |
| Connect an AI provider or coding agent from the dashboard | `apps/dashboard/src/pages/connections.tsx`; `runner/http/integrations-api.ts` | [ops-dashboard.md](ops-dashboard.md) (Connections) | 2026-11-03, main `777ee7f21` (read-only; the first load hit Chrome's `ERR_NETWORK_CHANGED` page, a retry rendered **Connections**); 2026-11-02, main `2567b7974` (read-only: `AI model`); 2026-11-01, main `7ce379c45` (read-only: `AI model`, `Coding agents`); 2026-10-28, main `a8fa10974` (read-only) | Pressing `Connect` rewires the operator's real coding agents, so it is never driven from a lane. |
| Publish and read live series snapshots | `cmd/series.ts`; `docs/LIVE-SERIES.md` | [local-reads-and-discovery.md](local-reads-and-discovery.md) / Series | 2026-11-03, main `777ee7f21` (`series list` `[]`; over MCP `series_publish {price, dry_run}` → `capital_yolo_harness`); `series create/list/show/delete` and the #2240 refusals 2026-11-02, main `2567b7974` (`visibility: public`; `--price 9/mo --dry-run` `seller_session_required`, `1/mo` `price_below_minimum`, `abc` `invalid_price`, `--stop-sales` `listing_free`, two flags `invalid_options`, no `--yes` `confirmation_required`; plain `--dry-run` `registry_unavailable` 503); `series list` `[]` re-read 2026-11-01, main `7ce379c45`; local create/list/show live verified 2026-10-27 maintenance, main `8fe6a8432`; publish refused | A plain `series publish --dry-run` with the guest key reaches the registry and is refused: `publish_rejected` (kind `live-series` not accepted, 2026-10-27 to 2026-11-01) or `registry_unavailable` (503, 2026-11-02). Selling needs a sign-in session (`seller_session_required`), so a real publish, the remote read and the listing are pending; see the new sales row below. |
| Resolve a phrase to venue fields; screen and chart metrics | `cmd/{resolve,metric,markets,tenors}.ts`; `runner/metric-params.ts` (`refuseUnknownMetricParams`); `shared/default-listing.ts` (`listing_note`, `unknownSymbolReasons`); `contracts/src/watch-condition.ts` (`unknownParamMessage`) | [market-data-reads.md](market-data-reads.md) / Resolve, metrics and markets | 2026-11-04, main `9acb5fb56` (`resolve BTC` exact perp); 2026-11-03, main `777ee7f21` (`resolve BTC`, `resolve "bitcoin dip to 55000"` (a Polymarket candidate with `condition_id`), `metric list`, `markets` with HIP-3; `tenors` 500 again); 2026-11-02, main `2567b7974` (`resolve BTC`, `metric list/get/series/screen`, `markets` BTC and `--exchange LIGHTER`; `tenors` 500 again); 2026-11-01, main `7ce379c45` (the #2202 refusals and notes again; `metric get --exchange BYBIT_FUTURES` aliased to `BYBIT` and read `no_recent_trade` for BTC `rsi`; `resolve BTC` and the dip phrase; `metric list`; `markets --exchange LIGHTER` rows; `tenors` still 500); 2026-10-31, main `dfefe0a21` (#2202: `metric get` unknown param → `invalid_query` naming what it takes; bare `--symbol BTC` with no `--exchange` → Binance plus `listing_note`; `metric series` keeps `--exchange` required; `--exchange BYBIT_FUTURES` aliases to `BYBIT` on `metric get` and on MCP `points`/`metric_get`, not on CLI `points`; `AAPL` on `POLYGON` → `venue_not_served`; `resolve "bitcoin dip to 55000"` ranks the 55000 leg first; `markets --exchange LIGHTER` rows; `tenors` still 500); 2026-10-30 scheduled maintenance, main `3cb50a821` (`resolve BTC`, `metric list`, `markets --exchange LIGHTER`; `tenors` still 500); 2026-10-28, main `a8fa10974` (`resolve BTC`; `metric list`, `get`, `series` and `screen`; `markets`, including `--exchange LIGHTER`) | `tenors` returned `server_error` (500) on every attempt, with and without `--exchange DERIBIT`. That is a service fault, so tenors stays unproven. |
| Open a local paper-trading account and read its book | `actions/paper/*.ts`; `runner/http/rpc/paper.ts`; `runner/paper/digest.ts` | [paper-accounts.md](paper-accounts.md) | 2026-11-04, main `9acb5fb56` (refusal, create, `ls`, digest); 2026-11-03, main `777ee7f21` (create without `--yes` refused, create, ls, show, digest text); 2026-11-02, main `2567b7974` (create without `--yes` refused; two creates, ls, show, digest text; the Paper tab rows); 2026-11-01, main `7ce379c45` (create, ls, show, digest text; the Paper tab row); 2026-10-31, main `dfefe0a21` (create, ls, digest text; the Paper tab row); 2026-10-30 scheduled maintenance, main `3cb50a821` (create, ls, digest); 2026-10-29, main `32ca0d6c7` (create/ls, the Paper tab, and `paper digest` all-accounts and per-account with the new `Steps: none` lead; show/log/set/reset on 2026-10-26) | Open/close/reset-all/`digest-set` and the scheduled edition undriven. Step rows in the digest need a target step. |
| List a venue's instruments and read an options chain | `cmd/instruments.ts`; `cmd/option-chain.ts`; `actions/data/{instruments,option-chain}.ts`; `runner/v3/` | [market-data-reads.md](market-data-reads.md) (Gotchas) | default-transport refusal re-driven 2026-11-02, main `2567b7974` (`instruments BINANCE BTC` `invalid_query`); default-transport refusal re-driven 2026-11-01, main `7ce379c45` (`instruments BINANCE BTCUSDT --limit 3` exit 2 `invalid_query`); 2026-10-28, main `a8fa10974` (default refusal; v3 rows and expiries; `exchanges` under v3 returned 30 venues, against 48 on `auto`) | Needs `OM_DATA_TRANSPORT=v3` on the CLI call (`OM_DATA_V3_URL` too if the home sets `OM_BASE_URL`); the default transport exits 2 `invalid_query`. The daemon's `counters.symbol_directory_*` (#2173) were not read: that needs `OM_DATA_TRANSPORT=v3` on `up`. Typed-door reads added by #2114 (fx/index candles, ETF flow, FRED) are undriven. |
| Read and clear model-provider plan holds (`usage plans`) | `actions/data/usage-plans.ts`; `cmd/usage.ts` | [market-data-reads.md](market-data-reads.md) (Gotchas) | 2026-11-02, main `2567b7974` (guest: empty `providers`); 2026-11-01, main `7ce379c45` (guest: empty `providers`); 2026-10-26, main `ee8e3a7ab` (guest: empty `providers`) | Corrected: this reports MODEL provider plans and holds, not Data API tiers. Populated rows, `--refresh` and `--clear` need a signed-in model provider. |
| Give 👍/👎 feedback on an openfeed alert; a new feed sends today's top 3 | `actions/watch/feedback.ts`; `openfeed/{feedback*,first-look}.ts` | [mcp-stdio.md](mcp-stdio.md) / Hosted MCP (refusal) | refusal live verified 2026-10-28, main `a8fa10974` (`watch_feedback` over MCP: `watch_feedback_not_openfeed`) | There is no CLI verb. Real feedback needs an OpenFeed source (account) and a sent row. |
| Read a chat turn: your message panel, the reply, tool rows, fire bands, notice strips, the replay and the chimes | `agent/channels/{cli-tui-core.ts,tui-theme.ts,tui-band.ts,tui-chime.ts,tui-first-frame.ts}`; `cmd/config-keys.ts` (`chat.sounds`) | [chat-transcript-layout.md](chat-transcript-layout.md) | 2026-11-04, main `9acb5fb56` (smoke: a fake-model text turn in the workspace and replayed in `--no-workspace`; no tool rows); 2026-11-03, main `777ee7f21` (in the workspace: the `┃` panel, `✓ watch_list → 7 watches`, the away band; with `--no-workspace` the `persona_set` card, `✗ declined` and `✓ approved` rows); 2026-11-02, main `2567b7974` (lane 18163, fake model 18164: the away banner, the `┃` user panel, `✓ watch_list → 4 watches`, the reply; the footer's `data limit hit` chip); 2026-11-01, main `7ce379c45` (lane 18163, fake model: What's new, ctrl+x `x`, a tool turn with the user panel at column 3 and a 5-column gutter, the away band, the 90-column re-wrap); 2026-10-31, main `dfefe0a21` (lane 18163, fake model: What's new, a tool turn with the user panel at column 3, a 5-column gutter, the tool row, the list and code block, no `Worked for`, the away band, 90-column re-wrap, exit history). Before that, 2026-10-30 on branch `af153e835` (approval card, fire and away bands, `/catchup`, replay, spinner, 71 columns) | Not re-driven on main: the approval card, replay, the spinner frame, notice strips and chimes (unit-tested). The OSC 11 blend was seen through tmux, not a real terminal. |
| Run a shell command from the chat composer with `!` and ask the agent about it | `agent/channels/{tui-shell-run.ts,cli-tui-core.ts}`; `runner/script-evaluator/spawner.ts` (`spawnIsolated`) | [chat-shell-mode.md](chat-shell-mode.md) | 2026-11-06, main `50fcc594b` (bare lane 18165, fake model 18164: enter in magenta, `echo` with `exit 0 · 0.0s`, no model request until the next message, which carried the output); verified 2026-11-05 on branch `daryl/bang-shell-composer` over `a0a8c7b8b` (lane 18121, fake model 18122: enter, run, agent-reads, consumed-once, recall, esc stop) | Not driven live: the busy-turn queue (unit-tested), rooms sending `!` as text, `--no-workspace`, a 1 MiB output. |
| Pick how chat draws watch and source icons (emoji, Nerd Font, ascii) | `shared/{tui-icons,tui-icon-mode}.ts`; `cmd/config-keys.ts` (`chat.icons`); `cmd/chat.ts` (`applyIconSetting`); `agent/channels/{watches-panel,watches-page-tabs}.ts` | [chat-tui-icons.md](chat-tui-icons.md) | 2026-11-04, main `9acb5fb56` (the `Nerd Font icons` entry is now `8 of 8` in the workspace card; not pressed); 2026-11-03, main `777ee7f21` (the card's second entry behind `Workspace is now the default`: ctrl+x `.` paged to it, ctrl+x `w` stored `nerd`); 2026-11-02, main `587ce2d0b` (scheduled; lane 18168, fake model 18170, tmux: the card **Nerd Font icons**, ctrl+x `w` stored `nerd`, the `/watches` header glyph U+1F440 → U+F0208 in the same session; `config set chat.icons maybe` exit 2); earlier 2026-11-02, branch PR #2247 at `2be28d04d` (lane 18131, fake model 18132: What's new `w` stored `chat.icons = nerd`, `/watches` in the same session drew U+F0208 and U+F01C/U+F19C/U+F099) | `ascii`, the env override and the page tabs are unit-tested only; the `/watches` glyphs were not re-read after the 2026-11-03 switch. |
| Let MCP clients write as-you drafts and posts in the operator's persona voice (opt-in) | `mcp/rooms-gate.ts` (`operatorVoiceLines`); `cmd/config-keys.ts` (`mcp.operator_voice`); `cmd/persona.ts` (`MCP clients:` row); `actions/rooms/session-grants.ts` (`operatorVoice`); `actions/system/config-show.ts` (`mcp_operator_voice`) | [mcp-stdio.md](mcp-stdio.md) (Operator voice in the badge brief) | 2026-11-03, main `777ee7f21` (guest lane, no badge: `config set mcp.operator_voice on`, `persona show` `MCP clients: write as you`, `--json` `mcpOperatorVoice: true`; MCP `config_show` `"on"`, `persona_show` `"on"`, `session_grants` `not_badge_bound`); 2026-11-02, branch PR #2250 at `0775fc2da` (operator home and badge: off brief byte-identical to 0.480.3, on brief ends with the persona digest, `session_grants` `operatorVoice: "off"`, `config_show` `"off"`) | On main since `6b8a48c05` (v0.487.0). The badge brief needs a badge session and was proved only on the branch; a live client writing in the voice and the OM Chat GUI persona panel are undriven. |
| Chat in a split view with a watches/fires/paper/positions/calendar/usage sidebar | `agent/channels/{workspace-layout.ts,chord-menu.ts,sidebar/}`; `actions/system/sidebar-layout.ts`; `cmd/sidebar.ts`; `cmd/config-keys.ts` (`chat.workspace`); `runner/watching/status-sentence.ts` (`lateOnly`) | [chat-workspace-tui.md](chat-workspace-tui.md) | 2026-11-04, main `9acb5fb56`: the workspace by default (`1 1`), WATCHES and FIRES, the ctrl+x menu gaining `a agents`, a fake-model turn, `--no-workspace` (`1 0`); 2026-11-03, main `777ee7f21`: plain `om chat` opens the workspace (`1 1`) by default (#2254); `--workspace` with the setting off and `--no-workspace` with it on; the seeded frame (`2 fired · 2 paused`, `○ … broken`, `◌` paused, `▾ FIRES 8 today`) and a tool turn; 2026-11-02, main `2567b7974`: the frame, `▾ WATCHES 1 fired · 0 paused` with `broken`/`late` rows, `▾ FIRES 2 today`, the sidebar watch-row click card and Esc, the What's new card and `x`; 2026-11-01, main `7ce379c45`: the frame, ctrl+x `p` at `2 of 3 on`, `fire-card-click` (the card ending on the clicked row, `╮` two left of the divider, Esc, `o` to the watch page, column 138 with the sidebar hidden), `om sidebar --format json`. 2026-10-31, main `dfefe0a21`: `fire-card-click` on main (#2225: the card level with the clicked row at the transcript's right edge, Esc, `o` to the watch page, column 138 with the sidebar hidden, `no longer stored` after `watch remove`), the #2219 dot colours (green fired, red broken, grey paused), the ctrl+x `p` picker at `2 of 3 on`, and the What's new `x` dismiss. 2026-10-30 scheduled maintenance, main `3cb50a821`: the ctrl+x `p` picker took CALENDAR to `3 of 3 on` (lit panels re-sort to the top), and `om sidebar set watches calendar usage` showed `▾ CALENDAR nothing scheduled` and `▾ USAGE $0 · 24h` (then a fake-model row). 2026-10-30, main `3cb50a821` (lane 18163, fake model). The dotted rules (#2198), the ctrl+x `p` picker to `3 of 3 on` with dim rows (#2195), POSITIONS `none open` / `○ no venue paired`, the watch card foot `esc close · o open · [om watch show …]`, `o` to the watch page and Esc back, and `o` with a draft (#2207). On 2026-10-29, at `32ca0d6c7`: frame, `om sidebar set`/`reset`, PAPER, go-to-recent and exit history. | Undriven on a lane: the 20-fire card scroll and its containment, the FIRES and USAGE `o`, the one-panel floor, collapse, the narrow resize, a live model turn, and the yellow `late` dot (needs an overdue polled source). |
| Open the registry welcome page (`om welcome`) | `cmd/welcome.ts`; `runner/packages/registry-contracts.ts` | [registry-welcome-and-search.md](registry-welcome-and-search.md) | 2026-11-04, main `9acb5fb56` (`does not offer the welcome page yet`, exit 1); 2026-11-03, main `777ee7f21` (`does not offer the welcome page yet`, exit 1); real registry re-read 2026-11-02, main `2567b7974` (`does not offer`); real registry re-read 2026-11-01, main `7ce379c45` (`does not offer`); real registry re-read 2026-10-31, main `dfefe0a21` (`does not offer`); real registry re-read 2026-10-30 scheduled maintenance, main `3cb50a821` ("does not offer"); 2026-10-28, main `a8fa10974` (real registry: "does not offer"; fixture: all three gate branches) | On main since #1947. The success path needs a registry advertising `welcome`, which production still did not on 2026-10-27, so it was proved against a fixture. |
| Get plain-language, personalised registry search results | `cmd/search.ts`; `runner/packages/search.ts` | [registry-welcome-and-search.md](registry-welcome-and-search.md) | 2026-11-04, main `9acb5fb56` (`search rsi`); 2026-11-03, main `777ee7f21` (`search rsi` 42, `search "btc funding"` 2); real registry `search rsi` re-read 2026-11-02, main `2567b7974` (`total: 42`, no `hidden`, no `served`; `btc funding` `total: 2`); real registry `search rsi` re-read 2026-11-01, main `7ce379c45` (`total: 42`, no `hidden`; `--kind kscript-indicator` refused `kind_retired`, see the kScript row); real registry `search rsi` re-read 2026-10-31, main `dfefe0a21`; 2026-10-28, main `a8fa10974` (fixture: `mode=nl`, `reasons`; with a key, `rank=for-you` + bearer; TTY text renderer with reasons lines) | Production still returns the old shape (no `nl` advertised). |
| Uninstalling or unfollowing tells the registry (receipt retraction) | `actions/packages/uninstall.ts`; `actions/watch/follow.ts`; `runner/packages/{retractions,use-receipts}.ts` | [registry-welcome-and-search.md](registry-welcome-and-search.md) (Gotchas) | live verification pending | Needs an account whose install or follow receipt returned an `edge`, plus a registry advertising `receipt_retract`. A guest never retracts. Signals are `[use-receipts]` log lines and `<home>/receipts/retractions.json`. |
| Finish `om init` by opening the welcome page (`--launch`) | `cmd/init.ts` | [registry-welcome-and-search.md](registry-welcome-and-search.md) (`init-closing`) | live verification pending | `om init` needs a TTY (exit 2 otherwise) and writes channel, credential and service state, so it is never driven on a lane. |
| Watch narrative (sentences, facets, entities from a recipe) | `packages/contracts/src/watch-narrative.ts` | **non-outcome** | n/a | A contracts library with no consumer in the CLI or dashboard at `ee8e3a7ab`, `8fe6a8432`, `a8fa10974` or `32ca0d6c7` (re-grepped 2026-10-29; only `packages/contracts/src/index.ts` exports it). Nothing renders it yet; re-check when one does. |
| Review a scheduled calendar occurrence | `actions/calendar/*`; `runner/calendar/blocks.ts` | [calendar-and-polling-windows.md](calendar-and-polling-windows.md) | 2026-11-04, main `9acb5fb56` (push, list, show, select, revise refusal and change, `links watch`); 2026-11-03, main `777ee7f21` (push, list, show, select, links, `revise --status cancelled --evidence-url` (the flag is required), list `cancelled`; polling windows set, list, cancel); 2026-11-02, main `2567b7974` (push → list → show → select → revise cancelled → links `[]`; the polling policy and `window set/list/cancel` on the loopback feed, `--every 60s` refused); 2026-11-01, main `7ce379c45` (push → list → show → select → revise cancelled → `links` `[]`; on `ui-authored-feed` a stored `--polling-json` policy, `window set --every 60s` refused `NaN`, `--every 60` scheduled `win_…`, `list`, `cancel` by origin → `cancelled`); 2026-10-31, main `dfefe0a21` (push → list → show → select → revise cancelled); empty `calendar list` re-read 2026-10-30 scheduled maintenance, main `3cb50a821`; 2026-10-28, main `a8fa10974` (occurrence, select, revise, reject, links, polling windows) | None. The window was not waited out to run. |
| Recover a challenged origin through a paid reader | `runner/firecrawl/*` | [firecrawl-first-block.md](firecrawl-first-block.md) | 2026-11-04, main `9acb5fb56` (no key, inside the hold: `page_bot_wall_suspected` with its own clock; the pause path on a fixture-key lane, see the #2265 row); 2026-11-03, main `777ee7f21` (no key, inside the hold: `page_bot_wall_suspected` with the `om setup firecrawl` hint; the probe's own `next try` 20:15 against the feed's 20:12); no-key path re-driven 2026-11-02, main `2567b7974` (inside the hold, `page-add …/article/1` → `page_bot_wall_suspected` with the `om setup firecrawl` hint; the source `Status` row and the dashboard detail carried `Firecrawl can read it for you`); no-key path re-driven 2026-11-01, main `7ce379c45` (inside a hold, `page-add …/article/1` exited 2 `page_bot_wall_suspected` with the `om setup firecrawl` hint); no-key path re-driven 2026-10-30 scheduled maintenance, main `3cb50a821` (inside a hold, `page-add` exited 2 `page_bot_wall_suspected` with the `om setup firecrawl` hint); no-key path re-driven 2026-10-28, main `a8fa10974`; configured path pending | Needs `OM_FIRECRAWL_API_KEY` **and** a redirect of `api.firecrawl.dev/v2/scrape` to a fixture, together. |
| om creates an agent from a draft: anti-jobs, named tools, fit run (`agent_create`, `agent_tools`, `agent_fit`, `om agent create`) | `packages/cli/src/actions/agents/{create,tools,fit,_grantable,_roster-door}.ts`; `cmd/agent-create.ts`; builder `tools`, `fit` and `draft-fit` in `packages/roster/src/{builder,plugins/local-package,preview-turn}.ts` | [agent-create.md](agent-create.md) | 2026-11-05, main `3a0ea623e` (create `--yes` and no-TTY refusal, MCP `agent_tools` and two `agent_fit` runs, TTY card decline and yes; the card's `Fit` read `not run for this draft` after the MCP fit, gap); 2026-11-03, branch `daryl/agent-creator-sharp` `1e4cf9f03` (two fit rounds over MCP, card `Fit` row pass and not run); `7e93059ef` (`Won't`/`Tools` rows, offered tools on a run, old `reads` draft refused); `1f6b53df6` (create, `--yes`/no-TTY/TTY decline, replay, `name_taken`) | Chat on a real model pending (needs an LLM credential); the fake model proves plumbing, not draft quality. Row added 2026-11-03, rewritten 2026-11-04. |
| A chat agent's run or day budget refuses loudly (`budget_exhausted`) | `packages/roster/src/chat-budget.ts`; task door and `watcher.ts` in `packages/roster/src/` | [agent-chat-budget.md](agent-chat-budget.md) | 2026-11-05, main `3a0ea623e` (per-run token stop with fake `usage`, 51st run 429, one inbox item each, `agent_busy` at 16 queued); 2026-11-03, branch `daryl/agent-budgets-loud` `2e933a0cf` | Daily-token and hourly stops and the @mention path not driven (rooms for @mention). Row added 2026-11-04. |
| Create, import, Try, install, publish, adopt and revoke an agent | `packages/roster/src/http/roster-api.ts` (`imports/*`, `local-packages/*`, `builder`, `instances/:id/try`) | [agent-creator-lifecycle.md](agent-creator-lifecycle.md) (historical branch closeout) | live verification pending on main | On main since #1948 (`b50ca927d`), HTTP/GUI only. Needs an account, an LLM credential or coding brain, and the openmarket-chat Agents GUI (`verify-om-chat`). |
| Read agent work runs, refuse unknown runs, read roster health and measures | `cmd/{roster,roster-runs,roster-controls,roster-retry}.ts` (`OM_DEV=1`); `packages/roster/src/http/roster-work-api.ts`; `/healthz` `roster` | [agent-creator-lifecycle.md](agent-creator-lifecycle.md) (Guest lane on main) | 2026-11-04, main `9acb5fb56` (`OM_DEV=1`: `agent runs` empty, `agent pause nope` `Work run was not found.`, `roster list` six rows, `roster measures`); 2026-11-03, main `777ee7f21` (`agent runs` empty, `agent pause nope` `not_found`, `roster measures` zeroed); `roster list` (six defaults), empty `agent runs`, the `not_found` refusals and `roster measures` re-driven 2026-11-02, main `2567b7974`; `roster list` (six defaults), empty `agent runs`, the `not_found` refusals and `roster measures` re-read 2026-11-01, main `7ce379c45`; `roster list` re-read 2026-10-31, main `dfefe0a21` (six defaults); 2026-10-30 scheduled maintenance, main `3cb50a821` (empty runs, `not_found` proof, roster list, executors); 2026-10-28, main `a8fa10974` (empty runs, `not_found`/`malformed_body` refusals, roster list/measures, `/rpc/v1/roster/projects`) | Real runs, plan approval, steer and retry need an installed agent plus a model or brain. |
| Link a coding project and set its delivery | `cmd/project-{token,delivery,unlink}.ts` (`OM_DEV=1`); `/rpc/v1/roster/projects` | [agent-creator-lifecycle.md](agent-creator-lifecycle.md) (Guest lane on main) | refusal re-driven 2026-11-02, main `2567b7974`; refusal re-driven 2026-11-01, main `7ce379c45`; refusal only, 2026-10-28, main `a8fa10974` (`project unlink nope` → `not_found`) | Needs a project linked through the GUI and a real forge token. |
| Drive persona and away operations from the web over remote control | `agent/channels/remote-control.ts`; `packages/rooms-client/src/remote-operation-routes.ts` (#2161); `agent/rooms-context.ts` (`SESSION_PARK_LADDER_MS`), `runner/remote-control-notice.ts` (#2223) | unmapped; the guest gate is in [daemon-lifecycle-and-health.md](daemon-lifecycle-and-health.md) (2026-11-01 stamp) | #2292 on main since v0.491.0 (`om agent remote` and the hosted chat's roster operations); 2026-11-04, main `9acb5fb56` `agent remote status` `{"enabled":false}` only; roster operations live verified 2026-11-03 on branch `daryl/agents-cloud-parity` (`c7c8c6f95`, not on main): every roster RPC is a `roster.*` operation; over a local relay `roster.instances.list` matched the lane's HTTP answer, `roster.tasks.submit` + `roster.tasks.read wait=20000` completed, `roster.instances.grant` and `roster.instances.try` 200, `roster.capabilities` 200; remote turns call `agent_run` and the `@name` door (evidence `dev-notes/om-agents-cloud-parity/run-artifacts/u3-remote-roster.log`, `u4-remote-turns.log`, `u2b-remote-writes.log`); guest gate re-read 2026-11-02, main `2567b7974` (`agent.log` `remote control dark: guest session`); guest gate live verified 2026-11-01, main `7ce379c45` (`agent.log` `channel_error {"surface":"remote","message":"remote control dark: guest session …"}` at boot); the operations and the #2223 retry ladder are live verification pending | Needs `om agent remote enable`, the relay and a signed-in web client. #2223 re-dials a failed first dial after about 1, 5, 15 and 60 min, then stops and pages `📡 Remote control offline` once; a guest never dials, so only the dark line is observable here. |
| Compose a watch (or a set) from a natural-language ask | `actions/watch/watch-compose.ts`; `actions/watch/kit.ts` | unmapped | live verification pending | Needs an LLM credential; the single largest `om watch` entry point. |
| Share, follow, fork, install a watch; room shares and knocks | `actions/watch/{share,follow,fork,install,share-room,knocks,relay-door}.ts` | unmapped | live verification pending | Registry + account credential; a follower needs a second home. |
| Attach and arm steps (ai / tool / money) on a watch | `actions/watch/{action-add,action-remove,tools,run-now}.ts` | unmapped | live verification pending | Money steps are capital-gated; ai steps need a model credential. |
| Grow an existing watch with more sources | `actions/watch/{source-add,page-add,search-add,model-add,source-copy}.ts` | [watch-lifecycle-cli.md](watch-lifecycle-cli.md) / Maintenance verbs | timer `source add`/`remove` re-driven 2026-11-02, main `2567b7974`; timer `source add`/`remove` re-driven 2026-11-01, main `7ce379c45`; timer source add/remove live verified 2026-10-28, main `a8fa10974` | Page, search, model and OpenFeed sources need a credential or account. |
| Repair or retry a watch broken for any non-origin reason | `actions/watch/{repair,retry,lane-retry}.ts` | [watch-lifecycle-cli.md](watch-lifecycle-cli.md) / Maintenance verbs | `retry`, `repair`, `repair --rearm`, `lane retry` re-driven 2026-11-02, main `2567b7974`; `retry`, `repair`, `repair --rearm` (`not_a_condition_watch`) and `lane retry` re-driven 2026-11-01, main `7ce379c45`; `repair --rearm` refusal re-driven 2026-10-31, main `dfefe0a21`; retry/repair on a healthy watch plus the `--rearm` and `lane retry` refusals live verified 2026-10-28, main `a8fa10974` | A genuinely broken watch is not constructible on a guest lane. |
| Read the wider journal surface: list, stats, chapters, search | `actions/watch/{journal-search,journal-stats,chapters,journal-list}.ts`; `cmd/event-journal.ts` | [watch-lifecycle-cli.md](watch-lifecycle-cli.md) (journal step) | 2026-11-02, main `2567b7974` (`event-journal list` with the removed watch's `watch_id: null`, `journal-stats` `accepted_total: 2`, `chapters: []`); 2026-11-01, main `7ce379c45` (`event-journal list` with the removed watch's `watch_id: null`, `journal-stats`, `chapters`, `watch history`); 2026-10-31, main `dfefe0a21` (`event-journal list` with a removed watch's `watch_id: null`, `journal-stats`, `chapters`, `watch history`); 2026-10-28, main `a8fa10974` (`event-journal list`, `search`, `journal-stats`, empty `chapters`) | Populated chapters undriven (they need a model's summary fold). |
| See and reclassify rows the judge never reached | `actions/watch/unjudged-rows.ts`; `actions/watch/reclassify.ts` | [watch-lifecycle-cli.md](watch-lifecycle-cli.md) / Maintenance verbs | re-driven 2026-11-02, main `2567b7974` (`unjudged --days 1` `[]`, `reclassify` `watch_reclassify_daemon_running`); re-driven 2026-11-01, main `7ce379c45`; `unjudged` empty read and the `watch_reclassify_daemon_running` refusal live verified 2026-10-28, main `a8fa10974` | Real unjudged rows need an LLM daily cap; reclassify needs the daemon stopped. |
| Rewrite a fired row's recorded verdict | `actions/watch/synthesize.ts` | unmapped | live verification pending | Source says the verb is `om watch amend <watch> <event-id> --weight …` (`cmd/watch-engine-verbs.ts:1825`, `actions/watch/amend.ts`), not `synthesize`. It needs a topic lane and a streamed event. Not driven. |
| Move a watch between devices, mute a remote copy, restore one | `actions/watch/{move-here,move-readiness,mute,restore,adopt-here}.ts` | unmapped | live verification pending | Needs a second device/home for the interesting cases. |
| Read money-step execution history and digests | `actions/watch/{execute-history,execute-digest,execute-paper-reset}.ts` | [watch-lifecycle-cli.md](watch-lifecycle-cli.md) / Maintenance verbs | `execute summary` zeroed, `execute history demo` `[]` and `watch execute history demo` re-driven 2026-11-02, main `2567b7974`; `execute summary` zeroed, `execute history demo` `[]` and `watch execute history demo` re-driven 2026-11-01, main `7ce379c45`; `execute summary` zeroed 2026-10-31, main `dfefe0a21`; empty-state reads live verified 2026-10-28, main `a8fa10974` (`execute history/summary/list`, `watch execute history`) | Needs executed money steps. `om execute digest list` answered `unknown command 'digest'` on this lane, so the digest's CLI door is unresolved. |
| Session and device identity: sign-in state, rename/revoke devices, account email | `actions/auth/{status,relogin}.ts`; `actions/devices/*`; `actions/account/email.ts` | unmapped | live verification pending | Account credential; revoke is destructive. |
| Mint and revoke API keys | `actions/keys/{create,revoke}.ts` | unmapped | live verification pending | Account credential; security-tiered, revoke is permanent. |
| Pair and manage a notification channel | `actions/system/{channel-add,channel-home,channel-default-set}.ts`; `cmd/setup.ts` (`setup default [name] [--force] [--clear]`); `runner/http/rpc/channel.ts` | pairing unmapped (dashboard shell only); the default-channel read and refusal are in [local-reads-and-discovery.md](local-reads-and-discovery.md) (Guest-lane reads) | `setup default` read and the `nope --force` refusal re-driven 2026-11-02, main `2567b7974`; `setup default` read and the `nope --force` refusal re-driven 2026-11-01, main `7ce379c45`; `om setup default` read and refusal live verified 2026-10-31, main `dfefe0a21`: the bare read printed `{"default":null,"routing":"none","targets":[]}` (the verb's default format is JSON); `setup default nope`, with `--format json` and with `--force` (#2220), each exited 2 with `channel_not_found` `unknown channel 'nope' — no channels are configured`, hint `om setup list`, `details.channels: []`. Pairing itself is live verification pending | Pairing, `channel_default_set` over chat and MCP, the `channel_failing` refusal and the `routing_note` need a paired Telegram/Discord/Slack channel. `--force` on a failing channel raises a tier-3 card in chat (`agent/risk-tiers.ts`). |
| Read the daemon's own notification history | `actions/system/{notis-list,notis-get}.ts`; `cmd/notis.ts` | [local-reads-and-discovery.md](local-reads-and-discovery.md) | 2026-11-03, main `777ee7f21` (`notis --since 7d --json` listed the `cond-probe` fires); 2026-11-02, main `2567b7974` (`notis --since 7d --json`: a `notice` row for `calendar-probe`); 2026-11-01, main `7ce379c45` (`notis --since 7d --json` `notice` and `fire` rows); 2026-10-31, main `dfefe0a21` (`notis --since 7d --json` fire rows); 2026-10-28, main `a8fa10974` (`notis --since 7d` rows) | `notis get` and `--after` paging undriven. |
| Inspect resolved config and the active key's claims | `actions/system/{config-show,config-key-info}.ts`; `cmd/config.ts`; `cmd/config-keys.ts` (`chat.sounds`, `chat.workspace`) | [local-reads-and-discovery.md](local-reads-and-discovery.md) | 2026-11-04, main `9acb5fb56` (`config show` masked); 2026-11-03, main `777ee7f21` (`config show` with `mcp_operator_voice`, `config key-info` `tier om_guest`); 2026-11-02, main `2567b7974` (`show`, `key-info` `om_guest`, `get data.transport`, `get chat.sounds`, the `max_tool_calls 250` and `chat.sounds maybe` refusals); 2026-11-01, main `7ce379c45` (`show`, `key-info`, `get chat.sounds`, `get data.transport`, `set agent.max_tool_calls 250` exit 2); 2026-10-31, main `dfefe0a21`: the new `chat.sounds` key (#2217) read `unset (default: on)`, `stored as tui.sounds`; `set chat.sounds off` printed `om: set chat.sounds=off` and `get --format json` read `value: off`, `source: config`, `stored_as: tui.sounds`; `set chat.sounds maybe` exited 2 `chat.sounds must be on or off.`; `set agent.max_tool_calls 250` still exits 2 (`at most 249`). 2026-10-30, main `3cb50a821`: `config set agent.max_tool_calls 250` was refused (`at most 249`), then `set … 249` and `get` succeeded. On 2026-10-28: `show`, `key-info` and `get` | `config edit` undriven. |
| Upgrade the binary, migrate and restart | `actions/system/upgrade.ts` | unmapped | live verification pending | Risk tier 5, confirm-carded; must never run against a lane. |
| Read the subscription plan and pricing | `actions/system/upgrade-show.ts` | [local-reads-and-discovery.md](local-reads-and-discovery.md) / Plans | 2026-11-03, main `777ee7f21` (`upgrade --show`); `upgrade --show`, `usage plans` and the `subscriptions` refusal re-read 2026-11-02, main `2567b7974`; `upgrade --show`, `usage plans` and the `subscriptions` refusal re-read 2026-11-01, main `7ce379c45`; `upgrade --show` re-read 2026-10-31, main `dfefe0a21` (guest note `600 weight per 60s window`); `upgrade --show` and `usage plans` live verified 2026-10-27 maintenance, main `8fe6a8432`; `subscriptions` refusal | `om subscriptions` refuses `account_required` for a guest. Buying and cancelling need an account. |
| Watch roster triage: what needs attention, one-click repair | `actions/system/{watching,watching-resolve-attention}.ts` | [watch-lifecycle-cli.md](watch-lifecycle-cli.md) / Maintenance verbs | `POST /rpc/v1/watch/overview` and the `resolve-attention` 409 re-read 2026-11-02, main `2567b7974`; `POST /rpc/v1/watch/overview` and the `resolve-attention` 409 re-read 2026-11-01, main `7ce379c45`; `POST /rpc/v1/watch/overview` re-read 2026-10-31, main `dfefe0a21`; `POST /rpc/v1/watch/overview` and MCP `watching_overview` live verified 2026-10-28, main `a8fa10974`; resolve-attention 409 refusal | A real attention item (daemon down, paused) was not seeded. |
| Read indicator and drawing schemas (catalog) | `actions/collab/{indicator-schema,indicator-list}.ts`; `cmd/chart.ts` | [chart-catalog-reads.md](chart-catalog-reads.md) | 2026-11-04, main `9acb5fb56` (`schema rsi`, `schema nonsense`, `indicator list`, `drawing schema`); 2026-11-03, main `777ee7f21` (`schema rsi`, `schema nonsense`, `list --query rsi`, `drawing schema`); 2026-11-02, main `2567b7974` (`indicator schema rsi`, `nonsense` → `indicator_unknown`, `indicator list --query rsi`, `drawing schema`); 2026-11-01, main `7ce379c45` (`indicator schema rsi`, `nonsense` → `indicator_unknown`, `indicator list --query rsi`, `drawing schema`; `@backquant/order-blocks` → `kind_retired`); 2026-10-31, main `dfefe0a21` (`indicator schema rsi` → `@om-core/rsi` 0.1.1, `period` int 14 in 1..2500; `nonsense` → exit 2 `indicator_unknown` listing the stock names); 2026-10-30 scheduled maintenance, main `3cb50a821`; 2026-10-28, main `a8fa10974` (`indicator schema`, `indicator list`, `drawing schema`) | The `--chart`/`--workspace` forms, `--keys period` and the `wrun/@scope/name/output` metric-id form were not driven. |
| Drive chart workspaces, indicators and drawings | `actions/collab/chart-*.ts`, `drawing-*.ts`, `indicator-*.ts` | unmapped | live verification pending | Needs a human's GUI chart tab open on a live collab session; a headless lane has nothing to submit to. |
| Backtest a strategy over historical bars | `actions/research/backtest*.ts` | [watch-lifecycle-cli.md](watch-lifecycle-cli.md) / Maintenance verbs (refusals) | the three `spec`/`run` refusals re-driven 2026-11-02, main `2567b7974`; the four refusals re-driven 2026-11-01, main `7ce379c45`; `--window-secs` refusal re-driven 2026-10-31, main `dfefe0a21`; Refusals live verified 2026-10-30, main `3cb50a821`: the stop-breaker flags (#2208) are `--window-secs` without `--max-stops`, a non-numeric `--max-stops`, and `run nope --window-secs 60`, each exit 2. The bare `backtest spec` refusal was also driven. `backtest run nope` was driven 2026-10-28 | A real run needs a watch with a strategy step (`watch create --from-candidate`). A braked package run needs an installed Indicator strategy package. Neither was driven. |
| Browse paid news feeds and read Fast-alerts billing | `actions/news/{feeds,billing,brief,voice}.ts`; `runner/http/rpc/news.ts` | unmapped (dashboard shell only) | live verification pending | Catalog browsing may be guest-ok; billing and follow need an account and a funded vendor relationship. |
| Agent memory: save, search and forget durable notes | `actions/memory/*.ts`; `cmd/memory.ts` | [mcp-stdio.md](mcp-stdio.md) / Hosted MCP | save → search → CLI `memory list` → forget live verified 2026-10-28, main `a8fa10974` over hosted MCP | The slug prefix must match the type (`memory_invalid_slug`). `memory_forget` ran with no approval card on loopback HTTP. |
| Author and compile a custom WASM indicator | `actions/wrun/{create,author,build,source-set,list}.ts`; `cmd/wrun.ts` | [local-reads-and-discovery.md](local-reads-and-discovery.md) (`wrun list`/`templates`/`create`) | 2026-11-04, main `9acb5fb56` (`wrun templates` 92, `wrun create … --template sma` at scaffold 113; no build); 2026-11-03, main `777ee7f21` (`wrun templates` 92, `wrun create @lane/vom-ema --template sma` at scaffold 111, `wrun build` with `historyIndependence {stamped:false, reason:"classic"}`); 2026-11-02, main `2567b7974`: `wrun templates` 92 (text: 84 `Runs on:`, 31 `in your browser`, none `through OpenMarket`), `wrun create @lane/option-prints` and `@lane/flow-vwap` at scaffold 108 (`declare.ts` and the prebuild carry `visible_by`/`needed_by`/`min_coins`), `wrun list`; 2026-11-01, main `7ce379c45`: `wrun templates` 92 (`flow-vwap`, group `Order flow`), `enum --domain indicator_template` 92, `wrun list`, and `wrun create --template flow-vwap` at scaffold **107** with `underlying: "@chain"` inputs (#2235). 2026-10-29 scheduled maintenance, main `7ec575e55`: `wrun create --template feed-alert-line` scaffolded a workspace at scaffold 106 whose feed input reads `ref: "@you/your-feed"`, and the three Feeds starters' descriptions say "set ref to a feed you published" (#2194); templates still 91. Before that, 2026-10-29 nightly, main `32ca0d6c7` (templates still 91; scaffold 105, #2184). Before that, 2026-10-28, main `186030b63` (list; templates still 91, 30 `runsOn` lines read OPRA "at your own tier" after #2180; the stock `accumulate` 0.1.3 package listed) | `WRUN_SCAFFOLD_VERSION` is 110 since #2246 (`packages/sdk/src/wrun-sdk-sources.ts:1204`; 106 at #2194, 107 at #2235, 108 at #2239, 109 at #2245); `wrun create --template liquidation-map` wrote `scaffold_version: 110` on 2026-11-02 (scheduled, `587ce2d0b`). A workspace at an older scaffold refreshes `src/sdk/declare.ts` and `scripts/wrun-prebuild.mjs` once. `wrun create` takes the package name first (`@you/<name>`). Drive `wrun create` into a directory outside the product tree, because it writes wherever the positional `[dir]` points. `wrun validate` is undriven; `wrun build` compiles and installs deps, so it needs package-manager access. |
| Arm and tune a live managed-strategy wallet | `cmd/managed.ts` over `actions/managed/*.ts` factories (CLI-only: not in the action registry) | unmapped | live verification pending | Capital-reaching: funded venue wallet plus an explicit arm gate. Out of reach for a guest lane. |
| Place and manage real venue orders; wallet and execution | `cmd/{order,execute,buy,hyperliquid,polymarket}.ts`; `actions/{execute,orders,hyperliquid,wallet,polymarket}/` (`actions/execution/` does not exist) | unmapped | live verification pending | Real money. Needs a funded account and a safe plan; nothing attempted. |
| Reach the capability layer over MCP (stdio) | `cmd/mcp.ts`; `mcp/server.ts`; `mcp/capital-gate.ts` | [mcp-stdio.md](mcp-stdio.md) | 2026-11-04, main `9acb5fb56` (463 tools, with the six `agent_*` tools and `todo_list`/`todo_get` new; 15 calls); 2026-11-03, main `777ee7f21` (455 tools (`persona_show` added), 18 calls across three sessions); 2026-11-02, main `2567b7974` (0.480.3, 454 tools with the daemon down; thirteen calls after boot, including `series_publish` with `price` → `capital_yolo_harness` and `watch_state_clear demo` → `not_a_condition_watch`); 2026-11-01, main `7ce379c45` (0.480.3, 454 tools; `watch_list`; `order_place` → `capital_yolo_harness`; `package_search` `kind_retired`; `chart_indicator_schema` and `chart_indicator_add` `kind_retired`; `package_open @om-core/rsi` success; `file_create` scratch; `channel_default_set nope`; `watch_show nope`; the `points` and `metric_get` aliases); 2026-10-31, main `dfefe0a21` (0.480.2, **454** tools: `file_create` and `channel_default_set` added, `document_draft` answers `Tool document_draft not found`; `watch_list`; `channel_default_set {name:"nope"}` → `channel_not_found` with the MCP hint `details.channels names the configured channels`; `order_place` → `capital_yolo_harness` under this driver). The stdio server was driven against the lane home with the daemon down (the guest 429 kept it from booting), which these calls do not need; 2026-10-30 scheduled maintenance, main `3cb50a821` (0.478.0, 452 tools, `watch_list`); 2026-10-30, main `3cb50a821` (handshake 0.478.0, 452 tools including `doc_patch`, a read, a `watch_not_found` payload without `kind`). The capital refusal was last driven 2026-10-28 | `om mcp arm`, `--catalog operator` and `--session merged` undriven. |
| Save a drafted document as a file (`file_create`, #2218/#2221) | `actions/research/file-create.ts`; `shared/document-files.ts`; `shared/user-folders.ts`; `agent/risk-tiers.ts` (`downloads`/`overwrite` tier 3); `agent/rooms-gating-plane.ts` (`SHARED_UNSAFE_TOOLS`) | [mcp-stdio.md](mcp-stdio.md) (`file_create` over stdio) | `scratch` and the `invalid_filename` refusal re-driven 2026-11-02, main `2567b7974`; `scratch` re-driven 2026-11-01, main `7ce379c45`; `scratch` live verified 2026-10-31, main `dfefe0a21` over stdio: `{content, filename:"vom-probe-20261031"}` wrote `<lane home>/accounts/guest/documents/vom-probe-20261031.md` (`bytes`, `format: md`, `destination: scratch`); a second call took `vom-probe-20261031 (2).md`; `filename:"../escape"` → `invalid_filename` (`the filename has a path separator; give a base name only`). `destination:"downloads"` never answered in 120 s and wedged the server (README, known product gaps) | No CLI verb (the manifest marks it bespoke): chat and MCP only. The chat card for `downloads`/`overwrite`, `path_escapes_root` on a symlinked documents folder, `no_downloads_folder`, PDF/DOCX refusals and the tier-3 card are undriven; the `downloads` hang over stdio is a product gap. |
| Let a connected assistant call the daemon, deposit, and be woken (unmerged stack #2350 to #2385, with `om assistants wake` for a bearer-key webhook) | `packages/cli/src/hosted/{forward,relay-link,daemon-tools,events,daemon-rate}.ts`; `runner/http/{assistants-call,assistants-events,assistant-consent}.ts`; `runner/assistant-{links,wakes,wake-sender,inbox}.ts`; `cmd/assistants.ts` | [assistant-bridge-and-wakes.md](assistant-bridge-and-wakes.md) | 2026-11-05, branch `daryl/assistant-stack-review-fixes`: list per host, off, ask, approve, call, deposit, refusals, subscribe, signed delivery, own-inbox skip, send budget, revoke, `/chatgpt` pinned, root cutover, rate limit | 2026-11-06: Grok Bot through its local command tool and its own MCP connector over a temporary tunnel, and a routine webhook woken by a watch row. Pending: an OAuth sign-in and token refresh from a real assistant, MCP Events from a real vendor, the production relay with a daemon from the stack; needs a relay stand-in and either the operator's stored key or a stand-in gateway |
| Reach the capability layer over hosted MCP (HTTP) | `mcp/http.ts` | [mcp-stdio.md](mcp-stdio.md) / Hosted MCP over loopback HTTP | loopback `mcp serve --http` re-driven 2026-11-02, main `2567b7974` (444 tools against stdio's 454; JSON body, no `mcp-session-id`; `GET /mcp` 405); loopback `mcp serve --http` live verified 2026-10-28, main `a8fa10974` (441 tools) | Non-loopback badge auth and `OM_LOOPBACK_AUTH=1` were not driven. |
| Run the hosted chart MCP against Mongo: boot, health, readiness, index rebuild, refusals | `packages/cli/src/hosted/{main,run,config,tenant-store-mongo,tenant-store-health}.ts` | [hosted-chart-mcp-tenant-state.md](hosted-chart-mcp-tenant-state.md) | 2026-11-04, main `9acb5fb56` (the four refusals exit 2; no Mongo); 2026-11-03, main `777ee7f21` (the four refusals exit 2, `--help` exit 0; no Mongo); refusals (each exit 2) and `--help` re-driven 2026-11-02, main `2567b7974` (no Mongo); refusals and `--help` re-driven 2026-11-01, main `7ce379c45` (no Mongo); refusals and `--help` re-driven 2026-10-30 scheduled maintenance, main `3cb50a821` (no Mongo); 2026-10-28, main `a8fa10974` (boot lines, health pair up/down/back, rebuild, four refusals, `--help`) | The tool-call path needs an operator API key on the production gateway; the env-gated suite passed 7/7 on 2026-10-28 once the role also had `readWrite` on `om_hosted_test` (without it the suite fails `Unauthorized`). |
| Publish, install and manage registry packages | `cmd/{packages,publish,install}.ts`; `actions/packages/*` | [kscript-retirement.md](kscript-retirement.md) (the retired-kind refusals); the real paths partially via agent-creator (itself unverified) | retired-kind refusals live verified 2026-11-02, main `2567b7974`; retired-kind refusals live verified 2026-11-01, main `7ce379c45` (`publish --dry-run`/`--validate` and `install <dir>` on kscript manifests → exit 2 `kind_retired`); a real publish or install is live verification pending | Registry credential; `package_delete` is irreversible. |
| Approve an arming or model edit from the dashboard | `runner/http/rpc/{watch-arm-review,watch-edit-review}.ts` | [watch-lifecycle-cli.md](watch-lifecycle-cli.md) / Maintenance verbs (refusal) | 400 `invalid_input` on a non-UUID token re-driven 2026-11-02, main `2567b7974`; 400 `invalid_input` on a non-UUID token re-driven 2026-11-01, main `7ce379c45`; `arm-confirm` refusal (400 `approval_expired`) live verified 2026-10-28, main `a8fa10974` | The happy path needs a watch with a money or ai step awaiting approval. |
| Sealed secrets bridge | `runner/http/rpc/secrets.ts` | [local-reads-and-discovery.md](local-reads-and-discovery.md) / Secrets status | 2026-11-03, main `777ee7f21` (`GET /secrets/status` `readiness:"unminted"`); `GET /secrets/status` re-read 2026-11-02, main `2567b7974` (`unminted`); `GET /secrets/status` re-read 2026-11-01, main `7ce379c45` (`unminted`); `GET /secrets/status` re-read 2026-10-31, main `dfefe0a21` (`unminted`); `GET /secrets/status` live verified 2026-10-27 maintenance, main `8fe6a8432` (200, guest `readiness: unminted`) | Minting, recovery and rooms use need an account. |
| Social chat: rooms, DMs, topics, docs, moderation | `actions/rooms/*` (190); `cmd/room.ts` | **out of scope here** | n/a | Owned by `verify-om-chat` per this repo's boundary rules; this repo holds only the protocol surface and daemon-side actions. Recorded so the gap is not mistaken for an omission. |
| Standalone `/paper` dashboard route | `apps/dashboard/src/paper-plane.tsx` | **non-outcome** | n/a | Mounts only when `strategyRoutes === null` (the OSS export). Unreachable in any lane `control-om` drives; reach Paper via the `/strategies` tab. |
| Review pending approvals from the CLI (`om approvals list\|approve\|deny`) | `cmd/approvals.ts`; `cmd/approve-chain.ts`; `runner/http/approvals-routes.ts`; `main.ts:76` | [local-reads-and-discovery.md](local-reads-and-discovery.md) / Guest-lane reads | 2026-11-04, main `9acb5fb56` (#2258 inbox: `approvals list` and `--kind draft` `No pending approvals.`, `--kind bogus` exit 2 naming the five kinds, `approve nope` exit 2, `GET /rpc/v1/approvals/inbox` all zero); `approvals list` `[]` re-read 2026-11-02, main `2567b7974`; `approvals list` `[]` and `GET /rpc/v1/approvals` re-read 2026-11-01, main `7ce379c45`; `approvals list` `[]` re-read 2026-10-31, main `dfefe0a21`; list live verified 2026-10-28, main `a8fa10974` (`approvals list` printed `No pending approvals.`, `--format json` printed `[]`, and `GET /rpc/v1/approvals` returned `{"approvals":[]}`) | Approve and deny need a pending item and a human terminal, so they are not driven. |
| Sign in or out, connect an LLM or coding agent from the CLI (`login`, `logout`, `llm`, `auth`, `setup`, `connect`, `disconnect`) | `main.ts:81,86,137,~143` | unmapped | live verification pending | Needs an account, a provider key or a TTY. |
| Wipe, export/import or upgrade the local store (`om reset`, `om migrate`, `om upgrade-db`) | `main.ts:205,222,225` | unmapped | live verification pending | Destructive; only on a scratch lane root. |
| Read and steer Away coverage over local HTTP (`/api/away`, `/coverage`, `/sessions`, `/activity`; `POST` `/policy`, `/arm`, `/control`) | `runner/http/away-api.ts:16,55-96`; gate in `runner/http/rooms-routes.ts:85-98` | [local-reads-and-discovery.md](local-reads-and-discovery.md) / Guest-lane reads (refusal) | 401 re-read 2026-11-02, main `2567b7974`; 401 re-read 2026-11-01, main `7ce379c45`; 401 re-read 2026-10-31, main `dfefe0a21`; refusal live verified 2026-10-28, main `a8fa10974` (`GET /api/away` and `/api/away/coverage` returned 401 `operator_required`) | The reads need operator proof even on loopback: the per-boot GUI session cookie, or a configured runner or desktop token. `/policy` is a `POST`, not a read. `arm` is unsafe. The GUI side belongs to verify-om-chat. |
| Set up your persona from `om chat` (propose from your own messages, save on a card) | `actions/rooms/persona-{show,infer,set}.ts`; `runner/rooms/persona-{propose,sample,view}.ts` | [persona-chat-tools.md](persona-chat-tools.md) | 2026-11-04, main `9acb5fb56` (CLI `persona show`/`set`/`clear` only; the chat flow was not re-driven); live verified 2026-11-03, main `777ee7f21` on a guest lane: `tool_search` → `persona_infer {pasted}` (`samples 7`, `roomsRead 0`) → the card under auto-approve → `n` stored nothing (`✗ declined`), `y` stored the exact text and dropped the managing tool; CLI `persona set/show/clear` refusals; live verified 2026-11-02, branch `daryl/persona-tools` `cc7a755c5` (PR #2256): `tool_search` → `persona_infer` (40 messages, 12 rooms) → card under auto-approve → `y` stored, `n` stored nothing | On main since `0d6993613`. Room sampling needs a rooms identity (proved only on the branch); the tool choice was a scripted fake model, not a real one. |
| Persona learning applies itself; a loaded persona joins the learned card | `runner/rooms/persona-{learn,fold,merge,view}.ts`; `runner/rooms/library-persona.ts`; `cmd/persona.ts` (`show` rows) | [persona-auto-learning.md](persona-auto-learning.md) | 2026-11-04, main `9acb5fb56` (on main since v0.489.0; CLI `show` `Learning: on, updates apply as you post`, `Room drafts: first 23 of 40 lines`, learning off; the learning itself was not re-driven); 2026-11-03, branch PR #2275 at `2d240ff0e` (test account `@dboon_ref`, daemon 18174 with `OM_LIBRARY_DIR`: hand-set fold to a new loaded card, tool union, tool second write, `clear --if-source`, `Room drafts` and `From` rows) | Not on main. A learn pass, undo, first card from posts and the length refusal were not driven live (no model on the test account). |
| Library and persona over local HTTP (conflicts, proposals, persona use/import/learn/sync) | `runner/http/library-api.ts:163-178`; `cmd/rooms-commands.ts` | unmapped | live verification pending | Probably needs rooms; the UI side is verify-om-chat's. |
| Read the follows feed (`om follows`) | `cmd/follows.ts`; `actions/follows/{list,show,feed,review}.ts` | [local-reads-and-discovery.md](local-reads-and-discovery.md) / Guest-lane reads | empty list and `not_following` re-driven 2026-11-02, main `2567b7974`; empty list and `not_following` re-driven 2026-11-01, main `7ce379c45`; empty list and refusal live verified 2026-10-28, main `a8fa10974` (`follows` returned zero `summary` counts; `follows show @nobody/nothing` exited 2 with `not_following`) | A populated feed needs a followed share, which needs a registry and an account. `om follow review` prompts for confirmation. |
| Stream live data over WebSocket (`om subscribe`) | `main.ts:199` | unmapped | live verification pending | Not driven; probably needs an API key with stream entitlement. |
| Send a one-shot message to a channel (`om send`) | `cmd/send.ts` | unmapped | live verification pending | Needs a paired channel. |
| Trace a shared alert's fires hop by hop (`om relay`) | `cmd/relay.ts`; `main.ts:215`; `runner/stream/relay-diagnostics.ts` | [local-reads-and-discovery.md](local-reads-and-discovery.md) / Guest-lane reads (refusals) | both refusals re-driven 2026-11-02, main `2567b7974`; both refusals re-driven 2026-11-01, main `7ce379c45`; refusals live verified 2026-10-28, main `a8fa10974` (`relay trace @nobody/nothing` gave `relay_ref_unknown`; a malformed ref gave `relay_ref_invalid`; both exit 2) | A real trace needs a live-shared watch. |
| Nervous system: autonomous chart moments from fires (`om nervous`) | `cmd/nervous.ts`; `actions/collab/nervous-status.ts` | [local-reads-and-discovery.md](local-reads-and-discovery.md) / Guest-lane reads | 2026-11-02, main `2567b7974` (`enabled: true`, a `watch_fired` receipt `unresolved_subject`; MCP `nervous_status`); 2026-11-01, main `7ce379c45` (`enabled: true`, `watch_fired` receipts; MCP `nervous_status` matched); 2026-10-31, main `dfefe0a21` (`enabled: true`, a `watch_fired` receipt after the ingest fire); 2026-10-28, main `a8fa10974` (`nervous status` showed `enabled: true` and a `watch_fired` receipt for the lane's own ingest fire, "no canvas resolved"; MCP `nervous_status` matched) | A chart moment that lands needs a GUI chart tab. |
| Run research studies (`om research`) | `main.ts:207`; `cmd/research.ts`; `actions/research/*` (10 actions besides backtest) | [local-reads-and-discovery.md](local-reads-and-discovery.md) / Guest-lane reads | `--locate-only` (one occurrence for the door's `event_id`) and `--watch nope` re-driven 2026-11-02, main `2567b7974`; `--locate-only` and `--watch nope` re-driven 2026-11-01, main `7ce379c45`; `--locate-only` re-read 2026-10-31, main `dfefe0a21`; `study --locate-only` live verified 2026-10-28, main `a8fa10974` (occurrences for an inbound watch; `--watch nope` gave `watch_not_found`) | A full study fetches candles and was not run. `search-files` and `make-image` spend on a model and need one. |
| Open the dashboard or desktop app setup from the CLI (`om dashboard`/`open`, `om app`, `app-setup`, `om claude`) | `cmd/apps.ts`; `cmd/app-setup.ts`; `main.ts:70,72` | unmapped | live verification pending | `dashboard`/`open` launch a browser; not driven on a lane. |
| Keep watchlists (`actions/watchlists/{index,local}.ts`) | `actions/watchlists/`; `actions/collab/collab-rest.ts:65-81` | [mcp-stdio.md](mcp-stdio.md) (refusal) | refusal re-driven 2026-11-02, main `2567b7974` (`missing_api_key`); refusal re-driven 2026-11-01, main `7ce379c45` (`missing_api_key`); refusal live verified 2026-10-28, main `a8fa10974` (MCP `watchlist_list` gave `missing_api_key`: guest keys have no workspaces) | There is no CLI verb. The MCP and agent tools need an account. |
| Create, list, edit, pause, resume and remove a watch from the CLI | `cmd/watch-engine-verbs.ts`; `actions/watch/{create,edit,pause-resume,remove,list,show}.ts` | [watch-lifecycle-cli.md](watch-lifecycle-cli.md) | 2026-11-04, main `9acb5fb56` (`lane-lifecycle` create/pause/resume/remove, `cond-probe`, four timer watches); 2026-11-03, main `777ee7f21` (`lane-lifecycle` create/edit/show/pause/resume/list/remove); 2026-11-02, main `2567b7974` (create, list, edit label, show, pause `held_lots: []`, resume, remove `paper_lots_left: []`); 2026-11-01, main `7ce379c45` (create, list, edit label, show, pause `held_lots: []`, resume, remove `paper_lots_left: []`); 2026-10-31, main `dfefe0a21` (create, list, edit, show, pause `held_lots: []`, resume, remove `paper_lots_left: []`); 2026-10-30 scheduled maintenance, main `3cb50a821` (pause `held_lots: []`, 409 on a paused door, resume, history); 2026-10-30, main `3cb50a821`: create, edit, show, pause (`held_lots: []`), resume, and remove (`paper_lots_left: []`). The label checks were driven 2026-10-28 | Non-empty `held_lots` and `paper_lots_left` need a money step holding a paper lot. |
| Push an event and see it fire on the door, the stream, the journal and the dashboard | `runner/http/ingest*`; `/events/v1`; `cmd/event-journal.ts` | [event-ingest-and-fire.md](event-ingest-and-fire.md) | 2026-11-04, main `9acb5fb56` (door 202 and 401, three stream events per id, the journal, CLI push, the dashboard row); 2026-11-03, main `777ee7f21` (door 202 and 401, three stream events per id, both ids in the journal, CLI push `delivery: daemon`, the dashboard row and detail); 2026-11-02, main `2567b7974` (door 202 + 401, three stream events for each of two ids, the journal id, CLI push `delivery: daemon`, the dashboard row and detail); 2026-11-01, main `7ce379c45` (door 202 + 401, three stream events for each of two ids, the journal id, CLI push `delivery: daemon`, the `/alerts` row); 2026-10-31, main `dfefe0a21` (door 202 + 401 unauthenticated, three stream events, the journal id, CLI push `delivery: daemon`, the `/alerts` row); 2026-10-30 scheduled maintenance, main `3cb50a821` (door 202, three stream events on one `event_id`, journal, `working`, 401 unauthenticated; CLI push `delivery:"daemon"` at load about 140); 2026-10-30, main `3cb50a821`: the door returned 202 with one `event_id` on all three stream events, the journal and the dashboard `working`. An unauthenticated push got 401 | On a busy host, CLI `event push` writes `direct` beside a live foreground lane (product gap below). |
| See the daemon's dashboard: Overview, Watches, News, Strategies, Channels, Venues and Receipts | `apps/dashboard/src/{app.tsx,pages/*}` | [ops-dashboard.md](ops-dashboard.md) | 2026-11-04, main `9acb5fb56` (every route's H1 on the first load, a bundle built from this tree); 2026-11-03, main `777ee7f21` (every route's H1 on a bundle built from this tree; `/connections` and `/venues` needed one retry past Chrome's `ERR_NETWORK_CHANGED` page); 2026-11-02, main `2567b7974` (every route's H1 on a bundle built from this tree; the Paper tab; the nav click; the `/strategies/<unknown>` flicker); 2026-11-01, main `7ce379c45` (every route's H1 on a bundle built from this tree; the Paper tab; the `/strategies/<unknown>` flicker; a one-off `chrome-error` on three loads that a retry cleared); 2026-10-31, main `dfefe0a21` (every route's H1 on a bundle built from this tree; the Paper tab; the `/strategies/<unknown>` flicker again); 2026-10-30 scheduled maintenance, main `3cb50a821` (every route's H1; `/strategies/<unknown>` `Loading…`); 2026-10-28, main `a8fa10974` (onboarding on a fresh lane, nav, every route's headings and empty states, the `/strategies/<unknown>` flicker) | Row added 2026-10-28. A populated strategy page needs a strategy, a signal and a venue. |
| Author a watch in the dashboard (`Create watch`) | `apps/dashboard/src/` watch-create flow | [watch-authoring-ui.md](watch-authoring-ui.md) | 2026-11-04, main `9acb5fb56` (the RSS flow to `/alerts/vom-nightly-feed-1104`, created paused, resumed from the CLI and polled the stub); 2026-11-03, main `777ee7f21` (the RSS flow to `/alerts/vom-nightly-feed-1103`, created paused; not resumed (its host was held)); 2026-11-02, main `2567b7974` (`Create a watch` → `RSS or Atom feed` → `Set up a feed` → `Review your watch` → `/alerts/ui-authored-feed`, created paused, resumed from the CLI, two stub polls in a minute); 2026-11-01, main `7ce379c45` (RSS through review to `/alerts/ui-authored-feed`, created paused, resumed from the CLI, polled the stub each minute); 2026-10-31, main `dfefe0a21` (RSS through review to `/alerts/ui-authored-feed`, created paused, resumed from the CLI, polled the stub each minute); 2026-10-30 scheduled maintenance, main `3cb50a821` (RSS through review to `/alerts/ui-authored-feed`, `enabled: false`, polls after resume); 2026-10-28, main `a8fa10974` (RSS kind through review to `/alerts/ui-authored-feed`, a paused watch on `watch show`, polls after resume) | Row added 2026-10-28. The other seven kinds were listed, not authored. |
| Ask the dashboard agent; open the `/agent` workspace | `apps/dashboard/src/` agent panel; `/agent` route | [agent-panel.md](agent-panel.md) | 2026-11-04, main `9acb5fb56` (the `No LLM API key configured` alert); 2026-11-03, main `777ee7f21` (the `No LLM API key configured` alert with **Reload conversation** and **Check connections**); refusal re-driven 2026-11-02, main `2567b7974` (`No LLM API key configured…`, `Check connections` → `/connections`; `/agent` `What can I help with?`); refusal re-driven 2026-11-01, main `7ce379c45` (`No LLM API key configured…`, `Check connections`; `/agent` rendered); refusal re-driven 2026-10-31, main `dfefe0a21` (`No LLM API key configured…`, `Check connections`); `/agent` rendered; refusal re-driven 2026-10-30 scheduled maintenance, main `3cb50a821`; refusal live verified 2026-10-28, main `a8fa10974` (the `No LLM API key configured.` alert, `Check connections`, the `/agent` rail) | A reply needs an LLM credential. Row added 2026-10-28. |
| A challenged host holds every source on it: one probe per window, then the window doubles | `runner/fault-episodes.ts`; `runner/subscriptions/*`; `shared/public-document.ts` | [origin-challenge-backoff.md](origin-challenge-backoff.md) | 2026-11-04, main `9acb5fb56` (one challenge poll at 19:30:26Z, held to 19:45:27Z, FAULT `source waiting · feed 127.0.0.1: …`, `/healthz` cooldown; `ok GET /rss` at 19:45:27.130Z, `reopened after the window`); 2026-11-03, main `777ee7f21` (one challenge poll at 19:57:27Z, held to 20:12:27Z, FAULT and `Cause:` rows, `/healthz` cooldown; `ok GET /rss` at `until`, `reopened after the window`, `/healthz` `open`); 2026-11-02, main `2567b7974` (steps 1-3 and the recovery on a CLI `page-add` feed: one challenge poll, the 15-minute hold, the lagging rows at 5 min, one `ok GET /rss` at `until`, `reopened after the window`, `/healthz` `open`); 2026-11-01, main `7ce379c45` (steps 1-3 and the recovery on the UI-authored feed: one challenge poll, the 15-minute hold line, `/healthz` `reconnecting` with a `cooldown`, the challenge sentence on `watch show`'s source row and the dashboard detail; exactly one `ok GET /rss` at `until`, `reopened after the window`, `/healthz` `open` 58 s later); 2026-10-31, main `dfefe0a21` (steps 1-3 on the UI-authored feed: one challenge poll, the 15-minute hold in the lane log, `/healthz` `reconnecting` with a `cooldown`, `watch show` FAULT/Error/Status rows); 2026-10-30 scheduled maintenance, main `3cb50a821` (one challenged poll, `reopen held until` +15 min, `/healthz` `reconnecting` with a cooldown, the FAULT sentence on CLI and dashboard, silence, then `ok` and `reopened after the window` at `until`; the doubling was not re-driven); 2026-10-28, main `a8fa10974` (hold; one still-challenged probe at `until`; 15 min doubled to 30; recovery at the doubled `until` with `reopened after the window` and `/healthz` `open`) | Row added 2026-10-28. During a long hold the status rows stop naming the challenge (product gap below). |
| Default agents arrive from `@om-core` registry packages after boot | `packages/roster/src/plugins/om-skills-defaults.ts`; `runner/roster-host/registry.ts` (#2167, #2169, #2183) | [agent-creator-lifecycle.md](agent-creator-lifecycle.md) / Default agents | 2026-11-04, main `9acb5fb56` (`installed 8 package(s)` at boot; six agents on `agent list` and `roster list`); 2026-11-03, main `777ee7f21` (`roster list` six `registry` rows); 2026-11-02, main `2567b7974` (`installed 8 package(s)` 4 s after boot; six rows); 2026-11-01, main `7ce379c45` (`installed 8 package(s)` about 6 s after boot; six rows); 2026-10-31, main `dfefe0a21` (`installed 8 package(s)` about 4 s after boot; six rows); 2026-10-30 scheduled maintenance, main `3cb50a821` (`installed 8 package(s)`, six registry rows at 1.0.0); install live verified 2026-10-29, main `32ca0d6c7` (`installed 8 package(s)` about 5 s after boot; `roster list` showed six registry agents at 1.0.0). The 404 retry path was driven 2026-10-28 under the old `@om-skills` scope | The six-hour maintenance pass and a withdrawal (410) are undriven. |
| A strategy-package watch holds its queued position, bounds its opening legs, and pages and digests each leg on paper | `runner/watching/steps/target-step.ts`; `runner/paper/{target-sink,target-pager,target-episodes,exit-lane,notices,digest}.ts`; `packages/contracts/src/target-step.ts` (#2176, #2188, #2192, #2201, #2208); `runner/money/{target-breaker,stop-breaker-verdict}.ts`; `runner/paper/entry-record.ts` | unmapped | live verification pending | #2208 adds `stop_breaker {max_stops?, window_secs?, max_loss_usd?}`, the stand-down causes, the arm-card `stop breaker:` line, and the refused close retried on the next row. #2201 means a lot closed by a stop, a limit or a hand holds the step flat until the package books its own exit (`target_entry_exited`). #2188 adds `admit.drift_frac`, `admit.max_event_age_secs` and `cooldown` (opening legs only), with arm-card facts and chain digest version 5. #2192 adds `Paper <acct> · opened/adjusted/closed` notices, `Step:` rows in the digest, `PAPER` rows in `watch execute history`, and research `admission_not_modeled`. All of these need a target step fed by an `ai` producer (a model) and an arm. Offline coverage: `test/paper-target-sink.test.ts` and `test/watch-target-chain.test.ts`. #2242 (`ec0e0b261`) sizes a paper target leg against the lot held at booking (leg lines `planned … on … held`; row ends `target_entry_exited`, `target_close_noop`, `target_open_deferred`) and #2244 (`d5a061cf9`) anchors the package record at the chain's first arm (the arm card's `record starts at the arm` / `record runs from <time>`, the lookback-cap refusal pointing at `om watch state clear`); both need an armed target chain and a condition fire. |
| See what's new in `om chat` and turn the workspace off (or Nerd icons on) in one press | `agent/channels/whats-new-card.ts`; `shared/whats-new{,.generated}.ts`; `cmd/config.ts` (`writeWhatsNewSetting`) | [chat-workspace-tui.md](chat-workspace-tui.md) / `whats-new-card` | 2026-11-04, main `9acb5fb56`: the workspace card is `1 of 8` (Workspace, agent portraits, the agents page, moving portraits, Firecrawl pause, a watch agent's ask, MCP voice, Nerd icons); plain chat `1 of 7`; 2026-11-03, main `777ee7f21`: the workspace card `What's new · 1 of 2` (`Workspace is now the default`, `[ Turn it off ]`), ctrl+x `.` to `Nerd Font icons`, the `w` row following the entry on screen, ctrl+x `w` on the first entry reopened plain chat and stored `chat.workspace off`; 2026-11-02, main `2567b7974`: the card (`1 0`), the ctrl+x `w`/`x` rows, `x` closed it; 2026-11-01, main `7ce379c45`: the card (`1 0`), the ctrl+x `w`/`x` rows, `x` closed it (`0 0`). 2026-10-31, main `dfefe0a21`: the card (`1 0`), the ctrl+x `w`/`x` rows, `x` closed it (`0 0`). 2026-10-30 scheduled maintenance, main `3cb50a821`: ctrl+x `x` closed the card (flags `1 0` → `0 0`). 2026-10-29, main `32ca0d6c7` (card on a fresh lane; ctrl+x rows `w`/`x`; `w` set `chat.workspace on` and reopened as a workspace) | The ✕ click, the `‹ ›` arrows and the 60-day expiry were not driven. Since #2254 the workspace entry shows only in a workspace and a plain-chat card only for an entry that still applies there. |
| A web chat whose tab closes on an open approval card frees the conversation | `agent/channels/web.ts` (#2205) | unmapped | live verification pending | It needs a model plus a web-chat client that holds an approval card and drops its stream. The GUI side belongs to verify-om-chat. Before the fix, `om chat` printed `Waiting for pid <daemon>` until a restart. |
| See where the vault master key lives, and move it into the OS keyring (`om vault status`, `vault protect [--off]`) | `cmd/vault.ts:108-133`; `main.ts:127` | [local-reads-and-discovery.md](local-reads-and-discovery.md) (2026-10-30 stamp) | `vault status` re-read 2026-11-02, main `2567b7974`; `vault status` re-read 2026-11-01, main `7ce379c45`; `vault status` re-read 2026-10-31, main `dfefe0a21` (`mode: none`, `keyring: macOS Keychain (available)`; no `--format`); `vault status` live verified 2026-10-30 scheduled maintenance (`mode: none`, `keyring: macOS Keychain (available)`) | `protect` writes the machine's keychain, so it is not driven on a lane. `vault status` takes no `--format`. Source discovery 2026-10-30. |
| Read and accept the marketplace terms (`om terms`, `terms accept`) | `cmd/terms.ts:290-325`; `main.ts:131` | [local-reads-and-discovery.md](local-reads-and-discovery.md) (2026-10-30 stamp) | 2026-11-04, main `9acb5fb56` (`terms` read the staging `2026-09-10` terms); 2026-11-03, main `777ee7f21` (`terms` read the staging `2026-09-10` terms); read 2026-11-02, main `2567b7974`: answered from the staging registry (version `2026-09-10`) in 0.5 s; read failed 2026-11-01, main `7ce379c45`: `registry_unreachable`, the staging registry timed out (environment); read live verified 2026-10-30 scheduled maintenance (`not_applicable: true`, `accepted: false` for a guest) | `accept` needs an account. Source discovery 2026-10-30. |
| List exchange-native and normalized symbols and heatmap block sizes (`om symbols`, `normalized-symbols`, `block-sizes`) | `cmd/{symbols,normalized-symbols,block-sizes}.ts`; `actions/data/{symbols,normalized-symbols}.ts`; `main.ts:169`, `:169`, `:173` | [market-data-reads.md](market-data-reads.md) (2026-10-30 stamp) | re-driven 2026-11-02, main `2567b7974` (bare `symbols` exit 2 `invalid_options`; `symbols --type TRADE_AGG` 3.27 M `rawSymbols`, a 198 MB answer; `normalized-symbols --type TRADE_AGG`; `block-sizes`); re-driven 2026-11-01, main `7ce379c45` (`symbols`, `normalized-symbols --type TRADE_AGG`, `block-sizes`); live verified 2026-10-30 scheduled maintenance (`--type TRADE_AGG`; `block-sizes --exchange BINANCE`) | `--type` must be a `data_type` value; anything else is refused `invalid_options`. Source discovery 2026-10-30. |
| Cancel a subscription (`om unsubscribe`) | `main.ts:133` (`subscriptions`, `unsubscribe`) | [local-reads-and-discovery.md](local-reads-and-discovery.md) / Plans | refusal re-driven 2026-11-02, main `2567b7974`; refusal re-driven 2026-11-01, main `7ce379c45`; refusal live verified 2026-10-30 scheduled maintenance (`confirmation_required`: "Cancelling a subscription moves money and needs confirmation.") | A real cancel needs an account with a subscription and moves money. Source discovery 2026-10-30. |
| Read the daemon's machine-readable route catalog (`GET /openapi.json`) | `runner/http/openapi.ts:78`; `runner/http/server.ts:921-925` | [local-reads-and-discovery.md](local-reads-and-discovery.md) (2026-10-30 stamp) | 2026-11-04, main `9acb5fb56` (`/openapi.json` 200, 1,065,106 bytes); 2026-11-03, main `777ee7f21` (`/openapi.json` 200, 1.06 MB); re-read 2026-11-02, main `2567b7974` (200, 137 paths, `info.version` 0.480.3); re-read 2026-11-01, main `7ce379c45` (200, 137 paths, `info.version` 0.480.3); re-read 2026-10-31, main `dfefe0a21` (200, 137 paths, `info.version` 0.480.2); live verified 2026-10-30 scheduled maintenance (200, 137 paths, `info.version` 0.478.0) | Same auth as `/healthz`. The paths are hand-authored, and `/rpc/v1/approvals` was not among them. Source discovery 2026-10-30. |
| Use the other `om chat` slash commands and prompt history (`/hints`, `/mute`, `/unmute`, `/jobs`, `/catchup`, `/brief`, `/rename`, `/provider`, `/effort`; ctrl+r) | `agent/slash.ts:165-288`; `agent/channels/tui-history-search.ts` | unmapped | live verification pending | The fake-model TUI rig in [chat-workspace-tui.md](chat-workspace-tui.md) reaches them; `/catchup` narration needs a model. Source discovery 2026-10-30. |
| Greet a newly connected chat channel and copy another channel's setup into it | `agent/channels/channel-tour.ts`; `agent/channels/copy-setup.ts` | unmapped | live verification pending | Needs a paired Telegram, Discord or Slack channel. Source discovery 2026-10-30. |
| A kScript (legacy) package is refused by name on every verb | `shared/retired-kinds.ts`; `cmd/{search,install,open,publish,chart}.ts`; `actions/packages/{search,open}.ts`; `actions/collab/{indicator-add,indicator-schema}.ts`; `runner/packages/{search,publish,indicator-launch}.ts`; `runner/wrun/install.ts` (#2234) | [kscript-retirement.md](kscript-retirement.md) | 2026-11-04, main `9acb5fb56` (`search --kind kscript-indicator`, `install` `package_deleted`, MCP `package_search`); 2026-11-03, main `777ee7f21` (`search --kind kscript-indicator` exit 2 `kind_retired`, `install @backquant/order-blocks` `package_deleted`, MCP `package_search` `kind_retired`); 2026-11-02, main `2567b7974` (every refusal again on the CLI and over MCP; `hidden` still source-only); 2026-11-01, main `7ce379c45` (`search --kind kscript-indicator` and `kscript-library`, `publish --dry-run` and `--validate`, `install <dir>`, `chart indicator schema @ref`, and over MCP `package_search`, `chart_indicator_schema` and `chart_indicator_add`, each `kind_retired` with no request sent; a default `search rsi` with no `hidden`) | `om open` or `om install` of a registry kScript ref and a search with `hidden > 0` need a registry that still lists one; production answered `package_deleted` for `@backquant/order-blocks`. Row added 2026-11-01. |
| Open an Indicator package on a chart from the CLI or an agent (`om open`, `package_open`) | `cmd/open.ts`; `actions/packages/open.ts`; `runner/packages/indicator-launch.ts` | [kscript-retirement.md](kscript-retirement.md) (`open-indicator-only`) | 2026-11-04, main `9acb5fb56` (CLI `open @om-core/rsi --print` 0.3.4; MCP `package_open` answered, so the 2026-11-03 `tool_failed` did not recur); 2026-11-03, main `777ee7f21` (CLI `open @om-core/rsi --print` 0.3.4; MCP `package_open` `tool_failed` after 30 s in two sessions (README gap)); 2026-11-02, main `2567b7974` (`open @om-core/rsi --print --format json`: `kind: wrun-indicator` 0.3.4, the `wrunRef` URL; the text form prints the URL; `package_open` the same); 2026-11-01, main `7ce379c45` (`open @om-core/rsi --print --format json`: `kind: wrun-indicator`, `version 0.3.4`, `chart_url …?wrunRef=%40om-core%2Frsi%400.3.4`, `wrun_ref`, no `script_id`; the text form printed the URL alone; MCP `package_open` the same with the publisher text withheld) | The browser launch itself is not driven (`--print` only). Row added 2026-11-01. |
| Sell a feed on the marketplace (`series publish --price`, `--stop-sales`, `--resume-sales`, `--free`) | `cmd/series.ts`; `actions/series/publish.ts`; `runner/series/{store,listing,orange-listing.client}.ts`; `shared/env-vars.ts` (`OM_ORANGE_ORIGIN`) | [local-reads-and-discovery.md](local-reads-and-discovery.md) / Series | refusals live verified 2026-11-02, main `2567b7974` (`seller_session_required` for `--price` and `--free`, `price_below_minimum`, `invalid_price`, `listing_free`, the two-flag `invalid_options`, `confirmation_required`; over MCP `series_publish` with `price` is `capital_yolo_harness` under bypass, so the sale is capital-gated) | Pending: the sale itself (`Visibility: listed (…)`, the `listed:` list marker, the Stripe payout link, `feed_tier_required`, `listing_price_locked`, `has_subscribers`, the `series_listed` delete refusal). Needs a sign-in session (`OM_LOGIN_LANE=session om login`), a plan that can sell and a payout setup; `OM_ORANGE_ORIGIN` could name a loopback marketplace stub, but it is read only after the session check. Row added 2026-11-02 (#2240, #2241). |
| Wipe a condition watch's persisted state and restart a target package's record (`watch state show`, `watch state clear`) | `actions/watch/state-clear.ts`; `cmd/watch-condition.ts`; `runner/timers/frozen-capital.ts` (`targetRecordFact`); `runner/readings.ts` (the lookback-cap refusal) | [watch-lifecycle-cli.md](watch-lifecycle-cli.md) / Maintenance verbs | 2026-11-04, main `9acb5fb56` (`state show` `state: null`, `state clear` `record_restarts: null`, `not_a_condition_watch` on a timer, MCP `watch_state_clear`); 2026-11-03, main `777ee7f21` (`state show` `state: null`, `state clear` `record_restarts: null`, the timer refusal; MCP `watch_state_clear {id}`); 2026-11-02, main `2567b7974` (`not_a_condition_watch` on the timer watch, on the CLI and over MCP; on an RSI rule `state show` `state: null`, `state clear` `{cleared: true, record_restarts: null}`, `--format text` `cleared <id>`; `watch_not_found` on an unknown id) | `record_restarts` `now`/`at_next_arm`, the arm card's `record starts at the arm` / `record runs from <time>` rows and the lookback-cap refusal need an armed target chain on a strategy package, which needs a terminal yes (pending). Row added 2026-11-02 (#2244). |
| Change a settings key from the CLI (`config get`, `set`, `list`) and be refused outside its rule | `cmd/config-keys.ts:157` (`CONFIG_KEYS`, about 85 keys); `docs/CONFIG_KEYS.md` | [local-reads-and-discovery.md](local-reads-and-discovery.md) (`config-set` / `config-list`) | 2026-11-04, main `9acb5fb56` (`firecrawl.offers` and `chat.motion` new: get, set, and `must be on or off.`); 2026-11-03, main `777ee7f21` (`config get chat.workspace` `unset (default: on)`, `mcp.operator_voice` `default: off`, `chat.icons` after the card `nerd`; `config set agent.max_tool_calls 250` exit 2); partly: 2026-11-02 (scheduled), main `587ce2d0b`, lane 18168: get on eight keys across the approvals, charts, telemetry, sharing, collab, wallet, nervous and chat groups; `set charts.auto_open false` read back as `source config`; `approvals.writes sometimes` exit 2; `config list` | The runtime effect of each key is pending: the agent, news, plan and nervous keys need an LLM key or a channel, and the wallet and execute caps need an armed money path. There is no `config unset`. |
| Opt out of telemetry and update checks with environment switches (`OM_TELEMETRY`, `DO_NOT_TRACK`, `OM_NO_UPDATE_CHECK`, `OM_PLAIN_CHAT`, `OM_NO_AGENT_WIRING`, `OM_MCP_LAZY`) | `shared/env-vars.ts` (`OM_TELEMETRY` :347, `DO_NOT_TRACK` :354, `OM_NO_UPDATE_CHECK` :317, `OM_PLAIN_CHAT` :622, `OM_NO_AGENT_WIRING` :677, `OM_MCP_LAZY` :669); `docs/ENV_VARS.md` | unmapped | live verification pending | `config get telemetry.product` names the precedence (`OM_TELEMETRY=off or DO_NOT_TRACK=1 still win`); the switches themselves were not driven |
| Read the dashboard's empty and error states (no watches, no channels, no strategies, watch detail and chart-view empties) | `apps/dashboard/src/pages/alerts.tsx:288`; `pages/channels.tsx:136`; `pages/strategies.tsx:130`; `pages/watch-detail.tsx` (80, 226, 294, 402, 659, 768); `lib/chart-view.ts` (104, 113, 130, 204, 409) | [ops-dashboard.md](ops-dashboard.md) | partly: 2026-11-02 (scheduled) every route on a fresh lane was captured (`/alerts`, `/channels`, `/strategies` frames in the evidence) | the per-string assertions and the watch-detail and chart-view empties were not read one by one |
| Connect, edit and remove a channel webhook from the dashboard | `apps/dashboard/src/pages/channels.tsx:136`; `components/channel-editor.tsx:39` | unmapped | live verification pending | local CRUD a guest can reach; not driven |
| Search Hyperliquid markets by name and get HIP-3 listings too; an unread venue is not a miss (#2260) | `actions/data/markets.ts:43-58`; `execution/shared/instrument-resolver.ts` | [market-data-reads.md](market-data-reads.md) / Hyperliquid name search and Polymarket ids | 2026-11-04, main `9acb5fb56` (`--symbol-filter GOLD` → `xyz:GOLD`); 2026-11-03, main `777ee7f21` (`--symbol-filter GOLD` → `xyz:GOLD` beside `PAXG`, `SP500` → two HIP-3 rows, the unfiltered browse core only; MCP `markets` the same) | The `could not be read, so … is unchecked there, not missing` wording needs a Hyperliquid outage: source only. |
| Polymarket points need a condition id; a stale TPO series says so (#2224) | `actions/data/points.ts` (`requirePolymarketConditionId` `:425`, `markStaleTpo` `:202`) | [market-data-reads.md](market-data-reads.md) / Hyperliquid name search and Polymarket ids | 2026-11-04, main `9acb5fb56` (a slug → exit 2 `invalid_query`; TPO still 500); 2026-11-03, main `777ee7f21` (a slug → exit 2 `invalid_query` on the CLI and over MCP; the `resolve` condition id read a series) | `stale_newest_session` live verification pending: `points --type TPO_AGG` answered 500. |
| A wrun build writes the converging warm-up stamp by default (#2267, #2270; scaffold 111) | `runner/wrun/authoring.ts:1166-1188`; `cmd/wrun.ts` (`Warnings:`) | [local-reads-and-discovery.md](local-reads-and-discovery.md) (Gotchas, `wrun build`) | 2026-11-03, main `777ee7f21` (partly: an `sma` build wrote no stamp and no warning, as a non-EMA recipe should) | A stamped build (an EMA or RMA of the chart's own feed), the gate's refusal warning and `OM_WRUN_CONVERGES=0` are live verification pending. |
| A card the daemon raises (a Firecrawl offer, a finished build's arm cards) no longer holds the conversation while it waits (#2257); since #2316 it parks on the approval ledger for 24 h | `agent/channels/parked-cards.ts`; `runner/approvals/ledger.ts` (`runCardedCall` is gone) | [approvals-ledger.md](approvals-ledger.md) | live verification pending | a turn that raises a card on the bare lane's fake model, then `Waiting for your OK (<id>)` and a second message while it stands |
| List, show and change your installed agents (`om agent list`, `show`, `configure`; `agent_list`, `agent_configure`) (#2297) | `cmd/agent-list.ts`; `actions/agents/{list,configure}.ts`; `packages/roster/src/http/roster-api.ts` (configure) | [agents-cli-and-tui.md](agents-cli-and-tui.md) (`list`, `show`, `configure`) | 2026-11-04, main `9acb5fb56` (six agents, `show explain`, `show nosuch` exit 1, `--paused on\|off` read back on `list`, `--brain` unknown option; MCP `agent_configure {set:{kind}}` `plugin_owned:kind`) | `--revision`, `--model`, the approval card and a `locked:` refusal not driven |
| See agent runs and the pool, read one, cancel one (`om agent ps`, `cancel`; `agent_runs`, `agent_run_cancel`) (#2282) | `cmd/agent-runs.ts`; `actions/agents/{runs,run-cancel}.ts`; `packages/roster/src/pool.ts` | [agents-cli-and-tui.md](agents-cli-and-tui.md) (`ps-cancel`); [roster-task-pool.md](roster-task-pool.md) | 2026-11-04, main `9acb5fb56` (empty pool `4 at once`, a failed watch-door run and its detail, `cancel` `Run was not found.` and `Run already failed.`) | a running cancel needs a model (the rig in roster-task-pool) |
| Open the agents overlay and an agent's page in `om chat` (ctrl+x `a`, `/agents`, `/agents <name>`) (#2282, #2297) | `agent/channels/{agents-panel,agents-page,agents-form}.ts`; `agent/slash.ts`; `agent/channels/workspace-layout.ts` | [agents-cli-and-tui.md](agents-cli-and-tui.md) (`overlay`, `agent-page`) | 2026-11-04, main `9acb5fb56` (RUNS and AGENTS tabs, `p` `y` pause read back on the CLI and undone, ABOUT and REACH pages, `/agents a b` usage, the draw prompt declined) | the AGENTS sidebar module (`om sidebar set watches agents`) and the SETTINGS/SCHEDULES/RUNS tabs not driven |
| Agents draw their own portraits; portraits move (`om agent portrait`, `agent_portrait`, `chat.motion`) (#2297) | `actions/agents/portrait.ts`; `shared/{tui-motion,portrait-motion,mascot}.ts`; `cmd/config-keys.ts` (`chat.motion`) | [agents-cli-and-tui.md](agents-cli-and-tui.md) (`motion`) | partly: 2026-11-04, main `9acb5fb56` (`chat.motion` get and refusal; `Portrait  not drawn, m to draw`; the What's new entries) | a draw is one model run and needs a model that returns a valid drawing; motion not observed |
| Hand an ask to an agent: `@name <ask>` in om chat, `agent_run`, `@om` in a room (#2269) | `agent/channels/agent-door.ts`; `actions/agents/run.ts`; `runner/roster-host/runtime.ts` | [agents-cli-and-tui.md](agents-cli-and-tui.md) (`at-door`, `mcp`); [roster-task-pool.md](roster-task-pool.md) | partly: 2026-11-04, main `9acb5fb56` (`@nope hi` in chat names the installed agents; MCP `agent_run {agent:"zzz"}` `not_found`) | a completed `@name` run needs a model; `@om` needs a room |
| Give a watch's agent step your own ask; `watch show` says why it stopped (#2287) | `cmd/watch-verbs.ts` (`--agent`, `--ask`); `agent/channels/arm-card.ts`; `shared/agent-step-words.ts`; `runner/timers/errands.ts` | [watch-agent-step.md](watch-agent-step.md) | 2026-11-04, main `9acb5fb56` (three authoring refusals, the arm card's `Ask:` row, a fire to `steps failing` and a failed run in `agent ps`) | the `no active credential` stand-down sentence and a completed run |
| Timers on chosen days of the week, said in words on every card (#2284) | `shared/timer-rhythm.ts`; `actions/watch/{_create-approval,_card,_source-add-approval}.ts`; `runner/watching/children-view.ts` | [watch-lifecycle-cli.md](watch-lifecycle-cli.md) (`timer-days`) | partly: 2026-11-05, main `3a0ea623e` (monthly `'0 9 1,15 * *'` and `'0 18 L * *'` created; the create JSON's `card` worded; `watch show` prints the raw cron); 2026-11-04, main `9acb5fb56` (`--every '0 7 * * 5' --tz UTC` and three more) | the arm and source-add cards are chat-lane and need a model; every-other-week and the days cadence have no CLI flag; the sidebar cadence not read |
| Read a server's Projects tickets (`om todo list`, `get`; `todo_list`, `todo_get`) (#2291) | `cmd/todo.ts`; `actions/rooms/{todos,_todos}.ts` | [local-reads-and-discovery.md](local-reads-and-discovery.md) (guest-lane reads) | refusals only, 2026-11-06, main `50fcc594b` (`todo list\|get --space openmarket` `room_social_failed` 401, MCP `todo_list` `not_badge_bound`); 2026-11-04, main `9acb5fb56` (`todo get 12` `invalid_ref`, `todo list --space x` `room_social_failed` 401, MCP `todo_get` `not_badge_bound`) | a real ticket needs a rooms account |
| An agent badge stages drafts into a one-to-one DM, and keeps up to 3 per topic (#2301, #2258) | `actions/rooms/draft-stage.ts`; `runner/agent-drafts.ts` (`AGENT_DRAFT_LANE_CAP`) | unmapped (the GUI half is verify-om-chat's) | live verification pending | a badge-bound MCP session and a rooms account |
| Pause the Firecrawl offer cards (`firecrawl.offers`), and a denied site stays denied (#2265) | `runner/firecrawl/{policy,offer-drain}.ts`; `actions/firecrawl/offers-pause.ts`; `cmd/setup-firecrawl.ts` | [firecrawl-first-block.md](firecrawl-first-block.md) (Pausing the offers) | 2026-11-04, main `9acb5fb56` (fixture-key lane 18165: `offers paused` then `ok`; `--deny 127.0.0.1` `declined`; `maybe` refused) | the seeded offer, the card and the exhausted-credits hold |
| Markets with a category list from v3 on a signed-in home (#2281) | `runner/v3/markets-map.ts` | unmapped | live verification pending | a signed-in home on the v3 socket |
| A big `instruments` page keeps its leading rows under the reply cap in om chat (#2262) | `actions/data/instruments.ts` | unmapped | live verification pending | the model-facing path (a model) and a Deribit chain read; the CLI and MCP keep the whole page |
| An Indicator pins a CME Group market (and CBOT, NYMEX, COMEX), and a pinned symbol may be any listed spelling (#2273, #2283, `9acb5fb56`) | `packages/contracts/src/wrun-words*.ts`; `packages/sdk/src/wrun-metadata-schema-core.ts`; `packages/sdk/src/wrun-sdk-sources.ts:1266` | [local-reads-and-discovery.md](local-reads-and-discovery.md) (scaffold) | partly: 2026-11-04, main `9acb5fb56` (`exchange_id` 38 with `CBOT`, `NYMEX`, `COMEX`; a create at scaffold 113) | a pinned build and the runner's refusal by name |
| Monthly timers, every-other-week timers and a summary on chosen days, said in words (#2300) | `shared/timer-rhythm.ts:80,115`; `packages/contracts/src/event-watch-authoring.ts` (`every_weeks`, `anchor`); `actions/watch/_compose-plan.ts` | [watch-lifecycle-cli.md](watch-lifecycle-cli.md) (`timer-days`) | partly: 2026-11-05, main `3a0ea623e` (monthly crons through `--every`, worded create cards) | every-other-week and the `days` delivery cadence are chat or source JSON only (a model); live verification pending for those |
| A paused or removed upstream stands down the chains reading it (#2310) | `actions/watch/pause-resume.ts:220,310,312`; `actions/watch/_removal-plan.ts:1581`; `runner/watching/{materialize,chain-close-words,status-sentence}.ts` | [watch-lifecycle-cli.md](watch-lifecycle-cli.md) (`upstream-stand-down`) | 2026-11-05, main `3a0ea623e` (pause, resume, re-arm, remove with a cascade and with a repair) | the batch pause form and the approval card wording (chat lane) not driven |
| Write, try and grade an agent folder; install it as an agent plugin (`agent init`, `try`, `eval`, `om install <dir> --preflight`) (#2306) | `cmd/agent-credentials.ts:126-170`; `actions/agents/{init,try,eval}.ts`; `cmd/install.ts:216-300`; `runner/roster-host/plugin-install.ts` | [agent-files-and-scopes.md](agent-files-and-scopes.md) (`init`, `try`, `eval`, `install`) | 2026-11-05, main `3a0ea623e` (guest lane and bare lane) | pins and `pin_failed`, a registry install: live verification pending |
| Installed agent files are read-only, a lock file records them, user and project scopes with trust (`agent list --lock`, `--here`, `agent trust`) (#2318) | `packages/roster/src/{scope-sync,scope-shadow,trusted-dirs}.ts`; `packages/roster/src/plugins/{agents-lock,release-copy}.ts`; `cmd/agent-list.ts:271-327` | [agent-files-and-scopes.md](agent-files-and-scopes.md) | 2026-11-05, main `3a0ea623e` (tamper restore, lock, user scope and shadow, project scope trust and forget) | the TUI trust card; `agent init`'s scaffold is refused by the scope loader (gaps) |
| Dial an agent's model; tune an agent with words (`agent configure --model`, `agent_tune`, `agent_tune_apply`) (#2306) | `agent/auth/agent-model.ts`; `actions/agents/{configure,tune,tune-apply}.ts`; `agent/channels/cli-tui-core.ts` (tune prompt) | [agents-cli-and-tui.md](agents-cli-and-tui.md) (`configure`); [agent-files-and-scopes.md](agent-files-and-scopes.md) (`tune`) | 2026-11-05, main `3a0ea623e` (model refusals and applies on a bare lane; tune over MCP writing `AGENT.local.md`) | the TUI tune prompt and a model-window refusal not driven |
| A granted agent joins its room at once (#2325) | `packages/roster/src/http/roster-api.ts` (`onRoomGranted`); `packages/roster/src/runtime.ts` | unmapped | live verification pending | a rooms account and a room grant |
| Esc out of `/setup` repaints the split-view chat (#2326) | `patches/@earendil-works%2Fpi-tui@0.87.1.patch` | [chat-workspace-tui.md](chat-workspace-tui.md) (`setup-esc`) | 2026-11-05, main `3a0ea623e` (bare lane, tmux) | none |
| `/provider` opens a picker and never claims a switch that will not hold (#2311) | `agent/slash.ts` (`applyProviderChoice`, `providerChoices`); `agent/channels/cli-tui-core.ts` (`promptProviderPicker`) | [chat-workspace-tui.md](chat-workspace-tui.md) (`provider-picker`) | partly: 2026-11-05, main `3a0ea623e` (the no-provider answers on an env-configured fake) | the picker and the switch answers need a stored provider credential: live verification pending |
| A click on a `While you were away` story opens its fire card (#2315) | `agent/channels/cli-tui-core.ts` (`ArrivalDigest.onStoryClick`); `agent/channels/tui-band.ts` | [chat-workspace-tui.md](chat-workspace-tui.md) (`away-story-click`) | live verification pending | fires during an away window plus SGR mouse input in tmux |
| Feed notices open with the source's headline; om chat replays paired-chat notices as quotes (#2314) | `runner/watch-engine/notify.ts` (`underItsHeadline`); `agent/channels/cli-tui-core.ts` (`quoteSourceTextForPeople`) | unmapped | live verification pending | a feed fire delivered to a paired channel (Telegram, Discord, Slack); a guest lane has none |
| Claude Desktop and Cursor get the merged MCP entry from `om connect` (#2305) | `cmd/integrations.ts` (`wireJsonClient`); `cmd/mcp-setup.ts:415` | unmapped | live verification pending | `om connect` writes the real `~/Library/Application Support/Claude` and `~/.cursor` from `os.homedir()` and has no path override; not driven on this host |
| The Claude Code sign-in is read from the keychain entry under the OS user first (#2308) | `agent/auth/providers/anthropic-claude-cli.ts:37-44` | unmapped | live verification pending | reads the real login keychain; not drivable without touching it |
| Official indicators split days at the trade date; publish refuses a UTC day key; the runner reads `time.trade_date` and `time.session` (#2333, #2335) | `packages/sdk/src/wrun-host/session-facts*.ts`; `cmd/publish.ts`; `runner/wrun/` | unmapped | live verification pending | `wrun_utc_period_key` needs a package that keys by UTC day; the time facts need a CME or US-stock metric read |
| Answer or decline a pending card from the CLI; one approval ledger behind every card (`om approvals list`, `om approve`, `om deny`; `/rpc/v1/approvals*`) (#2253, #2255, #2274, #2316) | `runner/approvals/{ledger,model,wire,inbox,frames}.ts`; `cmd/approvals.ts:329-362`; `runner/http/approvals-routes.ts` | [approvals-ledger.md](approvals-ledger.md) | 2026-11-06, main `50fcc594b` (two seeded rows listed, `om approve` refused from an auto-approve harness, `om deny` on both, `approval_changed`/`approval_resolved` on `/events/v1`) | `om approve` succeeding needs an operator shell outside an agent harness |
| A card that can move money is answered only on its card (`answer_on_card`); a typed size must match (`approval_typed_mismatch`) (#2344) | `runner/approvals/wire.ts:105-118`; `actions/capital.ts` | [approvals-ledger.md](approvals-ledger.md) | live verification pending | from an agent session the harness refusal answers first; needs an operator terminal and a seeded order card |
| An MCP chain request is a read-only owner card only a terminal can approve (#2340) | `mcp/chain-approval-gate.ts`; `cmd/approve-chain.ts:70-100` | [approvals-ledger.md](approvals-ledger.md) | live verification pending | a seeded `chain_arm` row and an interactive terminal (`terminal_required` otherwise) |
| A card shows on every paired DM and om chat window, and one answer closes the rest; follow-ups reach every surface (#2321, #2329, #2334) | `agent/channels/{approval-fanout,approval-streams,standing-cards,parked-cards}.ts` | [approvals-ledger.md](approvals-ledger.md) | live verification pending | a paired messenger DM or a second om chat window on the same conversation |
| The Firecrawl offer is an approval row: 24 h, `om approve` answers it, `--deny` closes it (#2337) | `runner/firecrawl/offer-drain.ts`; `cmd/setup-firecrawl.ts:188` | [firecrawl-first-block.md](firecrawl-first-block.md) (source note) | live verification pending | a fixture Firecrawl key and a challenged host |
| An agent's room-access knock is an approval card (`room_grant`, 7-day expiry, `agent grants approve --only`) (#2338) | `runner/agent-grant-requests.ts`; `runner/approvals/grant-events.ts` | unmapped | live verification pending | a badge session on a rooms account |
| Bring a Hermes, OpenClaw or Grok Bot setup into om (`om migrate <platform>`, `--dry-run`, `--yes`) (#2366) | `cmd/migrate.ts:723-770`; `migrate/sources.ts`; `migrate/readers/*.ts` | [migrate-from-other-agents.md](migrate-from-other-agents.md) | 2026-11-06, main `50fcc594b` (plans for all three fixtures; Hermes applied with `--yes`, re-plan reads `exists`) | routines land as paused watches only with a default channel; bare `om migrate` blocks headless |
| Archive a watch, unarchive it, and let a daily sweep archive unused ones (`watch archive`, `unarchive`, `list --archived`, `watch.auto_archive`) (#2357) | `actions/watch/archive.ts`; `runner/watching/archive-sweep.ts:20-100`; `cmd/watch-verbs.ts` | [watch-archive.md](watch-archive.md) | 2026-11-06, main `50fcc594b` (sweep `archived 1, refused 1`, the verbs, MCP `watch_unarchive`) | the finished-7-days branch was not reproduced; no TUI or GUI archive view |
| Write a server's tickets and labels (`om todo create\|update\|comment\|follow\|similar\|delete`, `om todo label …`; eleven `todo_*` tools) (#2341, #2342, #2355) | `actions/rooms/{todo-writes,todo-labels}.ts`; `cmd/todo.ts:539-640` | [local-reads-and-discovery.md](local-reads-and-discovery.md) (guest-lane reads) | refusals only, 2026-11-06, main `50fcc594b` (`todo label list`, `similar` `room_social_failed` 401; MCP `todo_create` `not_badge_bound`) | a rooms account with a Projects server |
| Tell your profile card what an agent is working on (`om agent status set\|clear`, `agent_status_*`, automatic `Last active`) (#2359) | `cmd/agent-status.ts`; `actions/rooms/agent-status.ts:283,299`; `mcp/agent-status-baseline.ts:12` | [agents-cli-and-tui.md](agents-cli-and-tui.md) (2026-11-06 stamp) | refusal only, 2026-11-06, main `50fcc594b` (`Guests can view but not chat — sign up to participate`, exit 2) | a signed-in rooms account; `Last active` needs a badge session |
| A ticket handed to an agent queues one run that reports on the ticket; creation intake; assignments end on a switched server (#2380, #2356, #2343) | `packages/roster/src/` (ticket delegation and intake) | unmapped | live verification pending | a relay with a switched Projects server |
| A ticket's read names its source message's author and time (#2353, #2364) | `actions/rooms/todos.ts:109-121` | unmapped | live verification pending | a rooms account with a ticket made from a message |
| `r` grows a sidebar or transcript card in place; Enter opens the card's page (`o` now types); `l` opens a fire's link (#2307, #2328, #2363) | `agent/channels/cli-tui-core.ts:30372-30388`; `agent/channels/sidebar/contract.ts:100-112` | [chat-workspace-tui.md](chat-workspace-tui.md) (`card-open-page`, `read-more`, `fire-link`) | 2026-11-06, main `50fcc594b` (bare lane, fake model, tmux 140x40) | the transcript-card `r` and the wheel inside a grown card were not driven |
| Search a watch page's Latest with `/` (#2363) | `agent/channels/watch-page-latest.ts:347-353`; `agent/channels/watch-page-view.ts:875` | [chat-workspace-tui.md](chat-workspace-tui.md) (`latest-search`) | 2026-11-06, main `50fcc594b` | Enter reading older pages was not driven |
| The watch page and the list pages share one frame with a detail panel that follows the cursor (#2309) | `agent/channels/tui-page-frame.ts`; `agent/channels/watch-page-*.ts`; `actions/watch/edit.ts` (`step_enabled`) | [chat-workspace-tui.md](chat-workspace-tui.md) (`page-frame`) | partly: 2026-11-06, main `50fcc594b` (the watch page, `/watches`, `/usage`) | a step's on/off switch needs a watch with a step; `/notis`, `/follows`, `/packages`, `/wallet` not opened |
| A chat turn answers only on the provider you chose; a dead sign-in stops with its cause (#2332) | `agent/llm-live-check.ts`; `cmd/config-keys.ts` (`plan.fallback_model`) | unmapped | live verification pending | a stored, expired Anthropic sign-in |
| A pasted picture becomes a package cover on the first ask (#2327) | `agent/cover-image.ts` | unmapped | live verification pending | an image paste, a package and a model that calls `package_artwork_set` |
| A v3 listing ranks past 50 rows, and says so when its stats could not be read (`Stats: not available`) (#2361, #2373) | `runner/v3/market-stats-map.ts:49`; `runner/data-transport.ts:2065-2074`; `cmd/markets.ts` | unmapped | live verification pending | a signed-in home on the v3 socket |
| An official Indicator that declares its buy/sell lane in Coin and in USD is warned at build and refused at publish (`wrun_trades_unit_pair`) (#2360) | `runner/wrun/trades-unit-pairs.ts`; `runner/wrun/authoring.ts:1214,1250,1355`; `runner/packages/publish.ts` | unmapped | live verification pending | a metadata fixture with both lanes; publish needs a sign-in |
| Dark pool prints: `plot.flags`, the diamond look and the `dark_pool` input (#2379, scaffold 116) | `runner/wrun/data.ts:2220`; `packages/sdk/src/wrun-sdk-sources.ts:1266` | [local-reads-and-discovery.md](local-reads-and-discovery.md) (scaffold) | partly: 2026-11-06, main `50fcc594b` (`wrun create --template dark-pool-prints` wrote scaffold 116 with `dark_pool` and `plot.flags`) | the data needs a signed-in fetch; the hosted refusal is corpus-only |
| Option kits keep the call wall at or above spot and the put wall at or below, by signed net gamma (#2336, #2339) | `packages/sdk/src/` (option-strikes kit) | unmapped | live verification pending | a chart host running the kit on live options data |

### Known product gaps (reported, not map drift)

- **New 2026-11-06 (`50fcc594b`), possible gap: `watch show` names an origin hold late, as `broken`, and suggests `run now`.** A `page-add` feed on the challenged stub was held (`reopen held until 19:46:17Z: 127.0.0.1 is challenging this machine`, `/healthz` `reconnecting`, one `challenge GET /rss` at 19:31:17Z). At 19:32Z `watch show` led with `steps the AI filter has no model to run on · 1 item waiting` and its source row read `found 1 · awaiting judge`, with no hold. From the status pass at 19:38Z it read `FAULT source broken · 127.0.0.1: Origin stub · since Nov 6 03:38`, a headline item `not checked since Nov 6 03:30 · expected every 1 min · om watch run now …`, and `Error: … stream not delivering: 127.0.0.1 is challenging this machine; next try …`; only the source's own `Status:` row and the dashboard read `waiting · 127.0.0.1 is challenging this machine … · Firecrawl can read it for you`. On 2026-11-05 the FAULT row itself read `source waiting · feed 127.0.0.1: … challenging … Firecrawl can read it for you`.
- **New 2026-11-06, observation: `om migrate` with no platform blocks in a headless session.** Detection reads `~/Downloads` for a Grok Bot export, and in a launchd session with no one at the screen that `readdir` never returned (killed after 120 s; a plain `bun` readdir of `~/Downloads` hung the same way). The platform subcommands with `--source` do not read it.
- **New 2026-11-06, unconfirmed: the archive sweep kept an expired once-condition.** With its `expires_at` rewound 8 days in the stopped lane's watch file, the reboot sweep logged `archived 1, refused 1` (the paused watch and the upstream), and `watch show` read the condition `working`. The file was hand-edited, so this is not a product claim; the 2026-11-05 branch run archived the same shape.
- **New 2026-11-06, observation: a watch page's Latest counts fires that reached no channel as `filtered out`.** Three accepted fires read `0 kept · 3 filtered out`, each `not sent: no notification channel`, and the page opened on `nothing kept yet`.
- **New 2026-11-06, observation: `approvals list` files a carded tool call under kind `mcp`.** A seeded `order_place` `tool_call` row listed as `mcp` (text and `--kind mcp`); `om deny --format json` on it reported `kind: tool_call`.
- **Re-observed 2026-11-06:** `tenors` 500; `points --exchange BYBIT_FUTURES` `is not a valid value`.
- **New 2026-11-05 (`3a0ea623e`), gap: `om agent create`'s card does not see a fit run made over MCP.** On the bare lane, `agent_fit` over MCP stdio on the exact draft (`passed 3/3`) was followed by `om agent create --file` in a TTY, whose card read `Fit  not run for this draft`; it did so twice. The card reads `POST /rpc/v1/roster/local-packages/draft-fit`, keyed by the package digest (`builder.ts:1716`), and got a 404. Not traced further (`tui/03-create-card-fit.txt`, `cli/mcp-fit.json`).
- **New 2026-11-05, gap: `om agent init`'s scaffold cannot be used as a user or project agent.** It writes `tools: ["room_read","library_read"]`, and the scope loader refuses that with `A draft names tools, never a bundle: room_read, library_read` (`packages/roster/src/plugins/local-package.ts:72`). Nothing installs and only the lane log says why. The same folder installs through `om install <dir>`.
- **New 2026-11-05, possible consent gap: the non-terminal `watch remove <upstream>` refusal omits the cascade.** `confirmation_required` read `Removing up1 deletes history (0 rows), 0 backbone entries and 0 overview snapshots; journal files kept. It needs a yes.` and `--yes` then also removed the reader watch `rd1` (`cascade.removed[]` `via: cascade`). The terminal question was not read.
- **New 2026-11-05, possible copy gap: a reader's `watch show` says the upstream `is gone` when it is only paused** (`steps the brief step is not approved yet · up1 is gone`).
- **New 2026-11-05, observation: `om agent trust <dir>` asks nothing on the CLI**, with stdin closed and no `--yes`; it trusts the directory and installs its agents. Other mutating verbs refuse `confirmation_required` in that shape.
- **New 2026-11-05, observation: `/provider` says `No AI providers connected yet` while om chat answers through an `OPENMARKET_LLM_*` env provider** (footer `openai-compatible/fake`).
- **Observation 2026-11-05:** a just-installed local agent reads `1 today` on `agent list` with no run; `om roster list` keeps a removed user-scope agent.
- **Re-observed 2026-11-05:** `tenors` 500; `points --exchange BYBIT_FUTURES` refused; `exchange_id` 38 values. A guest's resumed feed reads `summary stopped: the credential was refused` though no LLM is configured. A never-read dashboard-authored feed's hold row still names no feed title (`feed 127.0.0.1: 127.0.0.1 is challenging …`), while a CLI feed that read once names it (`feed 127.0.0.1: Origin stub: …`).

- **New 2026-11-04 (`9acb5fb56`), possible gap: `om agent ps` shows a watch-door run's ask as the whole step envelope.** The row reads `<watch_header boundary="520994813deb…"> HEADER Watch: lane-agent (lan…` and the detail's `Ask:` runs to several hundred characters, while the ask the user wrote (`Summarise this event in two lines.`) is buried inside it. The overlay's RUNS tab shows the same. Driven on lane 18163 (`cli/69`, `cli/73`).
- **New 2026-11-04, possible copy gap: `om setup firecrawl --deny 127.0.0.1 --format json` answers `"action":"allowed"`** beside `"declined":["127.0.0.1"]` and `"hosts":[]`. The decline is stored; the action word names the opposite (`cli/263`).
- **New 2026-11-04, possible gap: a guest lane's feed watch reads `FAULT summary stopped: the credential was refused`** (and `Status: summary stopped: the credential was refused`) when the summary has no LLM at all, which the chat footer calls `no LLM connected`. Seen on the dashboard-authored feed after its first poll (`cli/231`).
- **Observation 2026-11-04:** `om chat` on a fresh lane home opened with `⚠ this install holds state from 1 other account (account guest_8c9c4e7d-…); signed in as no account.` The lane root was created tonight by this run alone (`tui/01-launch.txt`). Not traced.
- **Resolved 2026-11-04:** MCP `package_open {ref:"@om-core/rsi"}` answered in about a second in a fresh stdio session (`cli/111-mcp2.json`); the 2026-11-03 `tool_failed` after 30 s did not recur.
- **Re-observed 2026-11-04:** `tenors` 500; `points --exchange BYBIT_FUTURES` refused; `points --type TPO_AGG` 500; the `indicator_unknown` hint naming the retired kScript form. `exchange_id` now lists 38 values against 45 from `exchanges`.

- **New 2026-11-03 (`777ee7f21`), possibly a gap: `package_open` over MCP stdio answers `tool_failed` after 30 s.** `{ref:"@om-core/rsi"}` failed that way in two fresh sessions on lane 18163 while `om open @om-core/rsi --print` answered at once on the same home. On 2026-11-01 the first such call stalled once and a fresh session answered in 250 ms (`cli/31-mcp-post.json`, `cli/32-mcp-post2.json`).
- **New 2026-11-03: `points --type TPO_AGG --exchange BINANCE_FUTURES --raw-symbol BTCUSDT --lookback 24h` answers 500** (`server_error`), so #2224's `stale_newest_session` cannot be seen (`cli/71`). Re-observed the same night: `tenors` 500, CLI `points --exchange BYBIT_FUTURES` `Bad Request`, the profiler's second `start` `already:false`, the `indicator_unknown` hint naming the kScript form, the guest sign-in 429 leaving a keyless home with no daemon.
- **Observation 2026-11-03:** `om persona show --json` spells the MCP voice as a boolean (`"mcpOperatorVoice": true`) where MCP `persona_show` says `"on"`; and turning the workspace off from the card left the welcome block twice in the terminal's scrollback (once from the workspace's exit history, once from the plain reopen).
- **New 2026-11-01 (`7ce379c45`), re-observed 2026-11-02 (`2567b7974`): the `indicator_unknown` hint still names the
  retired kScript form.** `om chart indicator schema nonsense` (and
  `chart_indicator_schema` over MCP) lists `a registry kScript (legacy)
  indicator package (@scope/name)` among the accepted forms
  (`actions/collab/_indicator-series.ts:59`), while the same verb refuses that
  form `kind_retired` since #2234. Stale copy. Driven on lane 18163 (`cli/64`,
  `cli/66`).
- **Re-observed 2026-11-01:** `tenors` 500; `points --exchange BYBIT_FUTURES`
  refused on the CLI (`cli/43b`); the `/strategies/<unknown>` flicker
  (`Loading…` at 12 s); `exchange_id` 35 values against 45 listed by
  `exchanges`; the status rows displaced the challenge 4.5 minutes into a
  15-minute hold (`watch show` FAULT `source broken · 127.0.0.1`, `watch list`
  `not checked since … · om watch run now`, while the source row and the
  `Error:`/`Cause:` lines kept the sentence). Possible, new 2026-11-01: `metric get --metric
  rsi --symbol BTC --exchange BYBIT_FUTURES` (aliased to `BYBIT`) answered
  `ok: false`, `error: no_recent_trade` with `last_print_at_sec: null` over a
  64-hour window (`cli/44`), while the lane home's `last-plan-refusal.json`
  recorded `{"kind":"data_type"}` at 19:23:10Z, inside that call and with no
  other market read in flight: a 403 `type not permitted` from the guest plan
  on the trade read, surfaced to the user as "no recent trade" and to the chat
  footer as `data limit hit`. The correlation is by timestamp, not a trace.
- **Environment 2026-11-01, not gaps:** `om terms` answered
  `registry_unreachable` twice (`https://registry-staging.openmarket.xyz/v1/me:
  The operation timed out.`) while `search`, `welcome` and `open` answered
  within a second (`cli/13`, `cli/13b`); three consecutive dashboard loads
  (`/strategies`, `/channels`, `/connections`) came back as
  `chrome-error://chromewebdata/` with `/healthz` answering in under a
  millisecond and nothing in the lane log, and a retry four minutes later
  rendered all three; the first MCP `package_search` and `package_open` of one
  stdio session stalled 30 s (the driver's timeout), a fresh session answered
  both in about 250 ms (`cli/90b`, `cli/90c`).

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
  (`packages/roster/src/runtime.ts:2160` → `runner/roster-host/rooms.ts:28`
  → `actions/rooms/_shared.ts:253-259`, which throws `missing_api_key`
  without a key), and `runner/index.ts:5296` awaits it inside `run`, so the
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
  writes it (`runner/index.ts:2285`), so a foreground `om run` is
  invisible. The push then writes the journal itself and reports
  `delivery:"direct"` with "The daemon is not running"
  (`actions/watch/push.ts:182-218`): a second writer beside the live
  consumer, which the guard at `push.ts:201` exists to prevent.
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
- **Re-observed 2026-11-02 (`2567b7974`, scaffold 108):** a workspace from
  `om wrun create` carries no `WRUN-OFFCHART` note under `src/sdk/` any more,
  but `scripts/wrun-prebuild.mjs` still holds five (`WRUN-OFFCHART round 2 G`).
- **New 2026-10-29 (`7ec575e55`), possible gap:** #2194's CHANGELOG says
  every workspace's `scripts/wrun-prebuild.mjs` drops internal round and
  program notes. A workspace scaffolded by `om wrun create` at scaffold 106
  still carries nine of them, for example `WRUN-OFFCHART round 2 G`. They are
  copied from `packages/sdk/src/wrun-slots.ts` and `wrun-style/widgets.ts`.
  The new vocabulary gate (`assertNoInternalVocabulary`) scans only the
  browser kit bundle's files (`gen-indicator-kit-bundle.ts:306-316`), not the
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
    (`runner/watching/status-sentence.ts:4724-4770`, `ROW.sourceStale`; `fetchFix` at `:733`).
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
  (`runner/http/rpc/system.ts:404`). Driven 2026-10-27 at `8fe6a8432`; re-observed 2026-10-28 at `a8fa10974`.
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
