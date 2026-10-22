# om verification map

The maintained source for verifying user-facing behavior in the `om` daemon and
CLI. Read this index before driving, then use the matching feature file as the
recipe.

## Baseline preconditions

- Launch the lane on its **assigned** port. Bind `127.0.0.1`. Never pick a free
  one: `control-om up` (default `18101`, range `18097`–`18197`).
- `control-om doctor` reports the expected origin, an isolated lane home, a
  present dashboard bundle, and a lane that is down or yours.
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
- [Agent creator lifecycle](./agent-creator-lifecycle.md) — **branch-only, not on origin/main**: the daemon side is on `origin/daryl/agent-creator-closeout` (`a3a81a5f5`, PR #1948) and the GUI side on openmarket-chat MR !75. See the banner on the guide.

Not yet mapped, and worth adding when a change touches them: the MCP
surface (`om mcp serve --stdio`), charts (`om chart`), the `om chat` TUI,
packages and the registry, and the execution/venue verbs.


## Surface inventory

Source discovery re-run 2026-10-22 against **origin/main `db6e76ef5` (v0.460.0)**.
The earlier census the same day was taken at `7e22214fb`, which is on branch
`daryl/watch-narrative` and is not an ancestor of main (merge-base
`463c0ceca`; main is 188 commits past it, and the branch holds 26 commits main
lacks). The user-facing surface barely differs. Deltas from branch to main:
commands +2 (`instruments`, `option-chain`) and −1 (`welcome`, branch-only);
actions +6 (`watch_feedback`, `chart_drawing_update`, `series_delete`,
`instruments`, `option_chain`, `usage_plans`); the same 21 categories, the same
9 dashboard routes, and 30 RPC files. So on main that is about **92 top-level
commands** (93 names with aliases) and **~803 actions**. The original census at
`7e22214fb`, kept for the deltas: **91 top-level `om` commands** and **797 registered actions across 21
categories** (rooms 190, watch 74, chart 46, system 31, market-data 17, packages
16, execution 13, hyperliquid 12, paper 11, research 10, news 9, wallet 8,
polymarket 8, strategy 7, polymarket-account 6, calendar 6, wrun 5, payments 4,
memory 4, state 2, transient 1), plus 9 dashboard routes and ~29 runner RPC
families. Twelve guides exist. This table is the gap between those two numbers.

Rows marked `live verification pending` are source-supported and undriven;
source inspection is not proof. Keep them across passes until driven, mapped, or
removed with source evidence.

| User outcome | Product source path | Guide / sub-feature | Live verification | Prerequisite or gap |
|---|---|---|---|---|
| Open a local paper-trading account and read its book | `actions/paper/*.ts`; `runner/http/rpc/paper.ts` | [paper-accounts.md](paper-accounts.md) | 2026-10-22, main `db6e76ef5` (create/ls/show/log/set/reset + Paper tab) | Open/close/reset-all/digest undriven. |
| List a venue's instruments and read an options chain | `cmd/instruments.ts`; `cmd/option-chain.ts`; `actions/data/{instruments,option-chain}.ts`; `runner/v3/` | [market-data-reads.md](market-data-reads.md) (stamp) | 2026-10-22, main `db6e76ef5` | New on main. Needs `OM_DATA_TRANSPORT=v3` on the CLI call; the default transport exits 2 `invalid_query`. |
| Read Data API plan tiers | `actions/data/usage-plans.ts`; `cmd/usage.ts` (`usage plans`) | [market-data-reads.md](market-data-reads.md) (stamp) | 2026-10-22, main `db6e76ef5` (guest: empty `providers`) | Populated tiers need a signed-in account. |
| Give 👍/👎 feedback on an openfeed alert; a new feed sends today's top 3 | `actions/watch/feedback.ts`; `openfeed/{feedback*,first-look}.ts` | unmapped | live verification pending | New on main (#2106 and nearby). Needs an account, registry, LLM credential and a channel destination. |
| Open the registry welcome page (`om welcome`) | branch `daryl/watch-narrative` only (`cmd/welcome.ts`) | non-outcome on main | n/a | Removed from main; no recipe should call it there. |
| Review a scheduled calendar occurrence | `actions/calendar/*`; `runner/calendar/blocks.ts` | [calendar-and-polling-windows.md](calendar-and-polling-windows.md) | 2026-10-22, main `db6e76ef5` (occurrence + polling windows) | None — guest-drivable via the inbound door; `calendar links` undriven. |
| Recover a challenged origin through a paid reader | `runner/firecrawl/*` | [firecrawl-first-block.md](firecrawl-first-block.md) | no-key path re-driven 2026-10-22, main `db6e76ef5`; configured path pending | Needs `OM_FIRECRAWL_API_KEY` **and** a redirect of `api.firecrawl.dev/v2/scrape` to a fixture, together. |
| Create, publish, adopt and revoke an agent/text skill | branch `origin/daryl/agent-creator-closeout` only (daemon `a3a81a5f5`, PR #1948) | [agent-creator-lifecycle.md](agent-creator-lifecycle.md) (branch-only) | not on origin/main | Absent from main's source (re-checked at `db6e76ef5`); merge PR #1948 and openmarket-chat MR !75, then verify on main. |
| Compose a watch (or a set) from a natural-language ask | `actions/watch/watch-compose.ts`; `actions/watch/kit.ts` | unmapped | live verification pending | Needs an LLM credential; the single largest `om watch` entry point. |
| Share, follow, fork, install a watch; room shares and knocks | `actions/watch/{share,follow,fork,install,share-room,knocks,relay-door}.ts` | unmapped | live verification pending | Registry + account credential; a follower needs a second home. |
| Attach and arm steps (ai / tool / money) on a watch | `actions/watch/{action-add,action-remove,tools,run-now}.ts` | unmapped | live verification pending | Money steps are capital-gated; ai steps need a model credential. |
| Grow an existing watch with more sources | `actions/watch/{source-add,page-add,search-add,model-add,source-copy}.ts` | unmapped | live verification pending | Page/search/model sources need a model credential; a feed source does not. |
| Repair or retry a watch broken for any non-origin reason | `actions/watch/{repair,retry,lane-retry}.ts` | unmapped | live verification pending | Needs a watch in a genuinely broken state to repair. |
| Read the wider journal surface: search, stats, chapters | `actions/watch/{journal-search,journal-stats,chapters,journal-list}.ts` | unmapped | live verification pending | Needs accumulated journal history. |
| See and reclassify rows the judge never reached | `actions/watch/unjudged-rows.ts`; `actions/watch/reclassify.ts` | unmapped | live verification pending | `watch unjudged` is new this range; needs a daily-cap state to observe. |
| Rewrite a fired row's recorded verdict | `actions/watch/synthesize.ts` | unmapped | live verification pending | Destructive projection rewrite; no guide at all. |
| Move a watch between devices, mute a remote copy, restore one | `actions/watch/{move-here,move-readiness,mute,restore,adopt-here}.ts` | unmapped | live verification pending | Needs a second device/home for the interesting cases. |
| Read money-step execution history and digests | `actions/watch/{execute-history,execute-digest,execute-paper-reset}.ts` | unmapped | live verification pending | Needs executed money steps; distinct from the event journal. |
| Session and device identity: sign-in state, rename/revoke devices, account email | `actions/auth/{status,relogin}.ts`; `actions/devices/*`; `actions/account/email.ts` | unmapped | live verification pending | Account credential; revoke is destructive. |
| Mint and revoke API keys | `actions/keys/{create,revoke}.ts` | unmapped | live verification pending | Account credential; security-tiered, revoke is permanent. |
| Pair and manage a notification channel | `actions/system/{channel-add,channel-home}.ts`; `runner/http/rpc/channel.ts` | unmapped (dashboard shell only) | live verification pending | Needs a real Telegram/Discord/Slack credential. |
| Read the daemon's own notification history | `actions/system/{notis-list,notis-get}.ts` | unmapped | live verification pending | Needs delivered notices to read. |
| Inspect resolved config and the active key's claims | `actions/system/{config-show,config-key-info}.ts` | unmapped | live verification pending | Guest-drivable in principle; simply undriven. |
| Upgrade the binary, migrate and restart | `actions/system/upgrade.ts` | unmapped | live verification pending | Risk tier 5, confirm-carded; must never run against a lane. |
| Read the subscription plan and pricing | `actions/system/upgrade-show.ts` | unmapped | live verification pending | Account/billing state; note the filename does not match the outcome. |
| Watch roster triage: what needs attention, one-click repair | `actions/system/{watching,watching-resolve-attention}.ts` | unmapped | live verification pending | Needs watches in attention-needing states. |
| Drive chart workspaces, indicators and drawings | `actions/collab/chart-*.ts`, `drawing-*.ts`, `indicator-*.ts` | unmapped | live verification pending | Needs a human's GUI chart tab open on a live collab session; a headless lane has nothing to submit to. |
| Backtest a strategy over historical bars | `actions/research/backtest*.ts` | unmapped | live verification pending | Condition-source backtests are guest-key drivable; fixed-view/ai-step kinds need accepted event-watch rows first. |
| Browse paid news feeds and read Fast-alerts billing | `actions/news/{feeds,billing,brief,voice}.ts`; `runner/http/rpc/news.ts` | unmapped (dashboard shell only) | live verification pending | Catalog browsing may be guest-ok; billing and follow need an account and a funded vendor relationship. |
| Agent memory: save, search and forget durable notes | `actions/memory/*.ts`; `cmd/memory.ts` | unmapped | live verification pending | `memory_save`/`forget` are agent-tool-only — they need a live `om chat` turn, not the bare CLI. |
| Author and compile a custom WASM indicator | `actions/wrun/{create,author,build,source-set,list}.ts` | unmapped | live verification pending | No credential needed, but `wrun_build` compiles and installs deps — needs outbound package-manager access and a harness that tolerates a real build. |
| Arm and tune a live managed-strategy wallet | `actions/managed/{arm-disarm,bind-address,set-size,set-drawdown,set-flatten,status}.ts` | unmapped | live verification pending | Capital-reaching: funded venue wallet plus an explicit arm gate. Out of reach for a guest lane. |
| Place and manage real venue orders; wallet and execution | `cmd/{order,execute,buy,hyperliquid,polymarket}.ts`; `actions/{execute,orders,hyperliquid,wallet,polymarket}/` (`actions/execution/` does not exist) | unmapped | live verification pending | Real money. Needs a funded account and a safe plan; nothing attempted. |
| Reach the capability layer over MCP (local and hosted) | `cmd/mcp.ts`; `mcp/server.ts`; `mcp/http.ts` | unmapped | live verification pending | No stdio/JSON-RPC drive recipe in this map; hosted needs auth/scope. |
| Publish, install and manage registry packages | `cmd/{packages,publish,install}.ts`; `actions/packages/*` | partially via agent-creator (itself unverified) | live verification pending | Registry credential; `package_delete` is irreversible. |
| Approve an arming or model edit from the dashboard | `runner/http/rpc/{watch-arm-review,watch-edit-review}.ts` | unmapped | live verification pending | Needs a watch with a money/ai step awaiting approval. |
| Sealed secrets bridge | `runner/http/rpc/secrets.ts` | unmapped | live verification pending | Security-sensitive; GUI never holds keys. |
| Social chat: rooms, DMs, topics, docs, moderation | `actions/rooms/*` (190); `cmd/room.ts` | **out of scope here** | n/a | Owned by `verify-om-chat` per this repo's boundary rules; this repo holds only the protocol surface and daemon-side actions. Recorded so the gap is not mistaken for an omission. |
| Standalone `/paper` dashboard route | `apps/dashboard/src/paper-plane.tsx` | **non-outcome** | n/a | Mounts only when `strategyRoutes === null` (the OSS export). Unreachable in any lane `control-om` drives; reach Paper via the `/strategies` tab. |

### Known product gaps (reported, not map drift)

- `/strategies/<unknown>` renders `Unavailable.` on main `db6e76ef5`. The
  `No strategy named <slug>. Back to Strategies` branch is never taken, even
  though `POST /rpc/v1/money/show` returns 404 `money_not_found`. Driven
  2026-10-22, stable over 20 s. The cause is not isolated (`pages/strategy-detail.tsx:357-370`).

- The "paper book" link on a strategy detail page points at `/paper?account=<id>`,
  a route this build does not mount; driven at `7e22214fb` it renders the shell
  with an empty `main` — no content, no 404.
- `AGENTS.md`'s capital-line section documents a `strategy_*` verb family
  (`strategy_create`, `strategy_resume`, `strategy_edit`, `strategy_remove`,
  `strategy_paper_reset`) that no longer exists in source; the live category is
  entirely `managed_*`.
