# Local reads and discovery

*Re-driven 2026-11-09 (scheduled maintenance), tree `0d3d29cd27` (origin/main, v0.493.0), bare lane on 18145 (dummy `OM_API_KEY`, dead service URLs) with a scripted fake model on 18144. `config show` (masked `om_...roto`, `api_key_source env`), `config set agent.max_tool_calls 250` exit 2 `at most 249`, `enum --list`, `schema read condition_create`, `wrun templates` **93**, `wrun create @vom/sty118 <dir> --template positioning-regimes` writes `.wrun-scaffold` **118** (#2407), `wrun build` and `wrun validate` pass, and an `@om-core/sty118` copy also validates. Not re-driven: `notis`, `terms`, `todo` against a stub, `space_muted`. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261109/r1/`.*

*Re-driven 2026-11-09 (nightly), tree `5bfa0ccf6` (origin/main, v0.492.0), guest lane on 18143, booted with no guest 429. `config show` (masked), `config key-info`, `enum --list` (`exchange_id` 38, `indicator_template` 93), `schema read condition_create`, `skill list`, `wrun templates` 93, `wrun create @vom/pos118 <dir> --template positioning-regimes`, `wrun build` (the `flat` output, #2414), `todo get` on a room-form and a server link, `todo update` and `todo list --space lab` against the real relay (401); first live proof of `space_muted` against a loopback stub (#2417). Not re-driven: `notis`, `terms`, `series`, `follows`, `relay trace`, the secrets status. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261109/r1/` (`cli/30-39`, `cli/51-54`, `cli/60-62`, `cli/70-75`).*

*Re-driven 2026-11-08 (nightly), tree `5590b4d1c` (origin/main, v0.492.0), guest lane on 18141, booted in 2 s with no guest 429. `config show` (masked), `enum --domain exchange_id` (38), `schema read condition_create`, `skill list`, `wrun templates` 93, `wrun create @vom/win117 <dir> --template sma-codefirst` at scaffold **117**, five `wrun build` variants for the new interval-window warning (#2405), the ticket link refusals after #2410 (`todo get om://todo/room/12/5`, `om://todo/lab/12abc`, `om://todo/lab/12`, `12`), `approvals list` `[]`, `calendar list`. Not re-driven: `notis`, `terms`, `series`, `persona show`, `follows`, `relay trace`, the secrets status. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261108/r1/` (`cli/20-26`, `cli/30-34`, `cli/56-59`, `cli/64-65`, `cli/var{A,B,C}.ts`).*

*Re-driven 2026-11-07 (nightly), tree `05f450fc5` (origin/main, v0.492.0), guest lane on 18141, booted with no guest 429. `config show` (masked), `config key-info` `om_guest`, `setup default`, `enum --list` (`exchange_id` 38), `schema read`, `skill list`, `wrun templates` 93, `notis --since 7d --json` (the run's fires), `terms` (`2026-09-10`), `GET /secrets/status` `unminted`, `vault status`, `follows`, `relay trace @nobody/nothing` `relay_ref_unknown`, `todo list --space openmarket --format json` `room_social_failed` 401, `series list` `[]`, `calendar list`, `persona show`. Not re-driven: `wrun create`/`build`. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261107/r1/` (`cli/55`, `cli/60-67`, `cli/80-84`, `cli/138`).*

*Re-driven 2026-11-06 (nightly), tree `50fcc594b` (origin/main, v0.492.0), guest lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), booted at 19:18Z with no guest 429, host load average 10 falling to about 3.3. `config show` (masked key), `setup default`, `enum --domain exchange_id` (38), `wrun templates` 93 (new: `dark-pool-prints`), `wrun create @vom/probe116 <dir> --template dark-pool-prints` (`.wrun-scaffold` `116`, `dark_pool` and `plot.flags` in the files), `schema read condition_create`, `skill list`, `notis` (the archive notice, `held`), `persona show`, `memory list` (the migrated memories), `approvals list` and `--kind bogus`, `approve nope`; `todo list|get|label list|similar --space openmarket` all `room_social_failed` 401; `agent status set|clear` exit 2 `Guests can view but not chat — sign up to participate`. Not re-driven: `wrun build`, the away reads. Evidence: `http://127.0.0.1:8098/vom-nightly-20261106/r1/` (`cli/config-show.txt`, `cli/todo-*`, `cli/agent-status-*`, `cli/wrun-*`).*

*Re-driven 2026-11-05 (nightly), tree `3a0ea623e` (origin/main, v0.492.0), guest lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), booted in 2 s at 19:19Z with no guest 429, host load average about 4.4. `config show` (masked key), `enum --list` (`exchange_id` 38), `wrun list`, `wrun templates` 92, `skill list`, `schema read condition_create`, `config get chat.motion` (`stored as tui.motion`), `approvals list` `[]`, `notis`, `persona show`; `todo list --format json` without `--space` exits 1 `required option '--space <spaceId>' not specified`. Not re-driven: `wrun create`, the memory round trip. Evidence: `http://127.0.0.1:8098/vom-nightly-20261105/r1/` (`cli/config-show.out`, `cli/enum-list.out`, `cli/todo.out`).*

*Re-driven 2026-11-04 (nightly), tree `9acb5fb56` (origin/main, v0.491.0), guest lane on 18163, booted in 2 s with no 429. `enum --list` (`exchange_id` 38, with `CBOT`, `NYMEX`, `COMEX` after `CME`, #2283), `schema read condition_create` (`watch read` is `unknown_intent` listing the intents), `skill list` (`openmarket`, `openmarket-watch`, `openmarket-watch-prompts`; it takes no `--format`), `config show` (masked key), `config get firecrawl.offers` (`unset (default: on)`) and `chat.motion` (`stored as tui.motion`), both refusing a non on/off value, `wrun templates` 92, `wrun create @vom/probe … --template sma` writing `.wrun-scaffold` `{"scaffold_version": 113}`. New: the approvals inbox (`list`, `--kind`, `--kind bogus`, `approve nope`, `/rpc/v1/approvals/inbox`) and the `om todo` refusals. Evidence: `http://127.0.0.1:8098/vom-nightly-20261104/r1/` (`cli/80-86`, `cli/100-105`, `cli/170-177`).*

*Re-driven 2026-11-03 (nightly), tree `777ee7f21` (origin/main, v0.488.0), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 2.8; the first `up` died on a guest sign-in 429 (35 minutes) and the lane booted in 3 s at 19:55Z. Before the boot: `config get chat.workspace` (`unset (default: on)`, #2254), `config get mcp.operator_voice` (`unset (default: off)`, #2250), `enum --list` (`exchange_id` 35), `indicator_template` 92, `wrun templates` 92, `wrun create @lane/vom-ema --template sma` at scaffold 111, `wrun build` (`historyIndependence {stamped:false, reason:"classic"}`, `history_warmup: null`), `skill list` (16; `--format` is refused `unknown option`), `skill show watch`, `skill show nope-skill` exit 2, `schema read`, `setup default`, and `om persona` (`show`, `set "" ` exit 2, `set --source verify`, `show --json`, `clear --if-source other` kept it). After: `config show` (`mcp_operator_voice`), `config key-info` (`tier om_guest`), `notis --since 7d --json` (the `cond-probe` fire rows), `series list` `[]`, `upgrade --show`, `config set agent.max_tool_calls 250` exit 2, `GET /secrets/status` `readiness:"unminted"`. Evidence: `http://127.0.0.1:8098/vom-nightly-20261103/r1/` (`cli/*.txt`).*

*Re-driven 2026-11-02 (scheduled maintenance), tree `587ce2d0b` (origin/main, v0.480.3), lane on 18168 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 5. `config show` (`api_key_set:true`, masked), `config key-info` (`tier om_guest`), `config get data.transport` (`default auto`), `enum --list` (`exchange_id` 35), `schema read`, `wrun list`, `series list` `{"series":[]}`, `upgrade --show`, `config set agent.max_tool_calls 250` exit 2 (`at most 249`), `subscriptions` exit 1 `account_required`, `setup default`, `approvals list`, `notis --since 7d --json`, `GET /secrets/status` `readiness:"unminted"`. Series: `series create s1 --watch lane-lifecycle --key v --scope local` → `@local/s1` 0.1.0; `publish s1 --price 9/mo --dry-run` → `seller_session_required`; `--price 1/mo` → `price_below_minimum`; `delete s1 --yes` → `relay:"missing"` (a `publish` before `create` answers `series_not_found`). **wrun at scaffold 110:** `wrun templates` lists `liquidation-map`; `wrun create @lane/liq --template liquidation-map <dir>` wrote `.wrun-scaffold` `scaffold_version: 110`. `config get chat.icons` / `set` / refusal: see [chat-tui-icons.md](./chat-tui-icons.md).*

*Re-driven 2026-11-02 (nightly), tree `2567b7974` (origin/main, v0.480.3), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 4. Before the boot (daemon down, keyless home): `enum --list`, `enum --domain indicator_template` (92), `wrun templates` (92; the text form has 84 `Runs on:` lines, 31 reading `CME futures in your browser`, none reading `through OpenMarket`), `wrun create @lane/option-prints --template option-prints` and `@lane/flow-vwap --template flow-vwap` (`.wrun-scaffold` `{"scaffold_version": 111}` (2026-11-03), `src/sdk/declare.ts` and `scripts/wrun-prebuild.mjs` written, the prebuild carrying `visible_by`, `needed_by` and `min_coins`), `skill list`, `skill show indicators` (`min_coins`, `two or none`), `skill show watch` (`watch_state_clear` drops the anchor, `record_restarts`), `config show` (`api_key_set: false`), `setup default`, `upgrade --show`, `schema read` and `schema read condition_create`, `chart indicator schema rsi`. After the boot: `config show` (masked key), `key-info` (`om_guest`, a one-hour expiry), `get data.transport`, `set agent.max_tool_calls 250` exit 2, `get chat.sounds` `unset (default: on)`, `set chat.sounds maybe` exit 2; `notis --since 7d --json` (a `notice` row for `calendar-probe`); `approvals list` `[]`; `setup default nope --force` `channel_not_found`; `nervous status` (`watch_fired` receipt, `unresolved_subject`); `follows` `[]` and `follows show` `not_following`; both `relay trace` refusals; `research study --locate-only` (one occurrence for the door's `event_id`) and `--watch nope` exit 2; `/api/away` 401 `operator_required`; `/secrets/status` 200 `unminted`; `/openapi.json` 137 paths; `vault status` `mode: none`; `usage plans` `providers: []`; `subscriptions` `account_required`; `unsubscribe nope` `confirmation_required`; `wrun list` (`@om-core/accumulate` 0.1.3); `terms` answered from the staging registry (version `2026-09-10`) in 0.5 s. **Series (#2240, #2241):** `series list` `[]`; `create s1 --watch demo --key v --scope local` (`@local/s1` 0.1.0, `rows: 0`); `show --format json` carries `visibility: "public"`, `relay: null`, `relay_refusal: "feed_not_found"`, and the text form prints `Visibility: public` and `Feed: not on the relay yet`; `list --format text` prints the row with no `listed:` marker. The new publish flags refuse locally on a guest: `--price 9/mo --dry-run` → `seller_session_required` ("Selling a feed needs a sign-in session; this home signs in with a login key", hint `OM_LOGIN_LANE=session om login`), `--price 1/mo` → `price_below_minimum` ($2.50 floor), `--price abc` → `invalid_price`, `--stop-sales --yes` → `listing_free`, `--stop-sales --free` → `invalid_options` ("cannot ride one call"), `--price 9/mo` without `--yes` → `confirmation_required`, `--free --yes` → `seller_session_required`. A plain `--dry-run` reached the registry and got `registry_unavailable` (503, "could not confirm this account's username") tonight, not the `publish_rejected` of earlier passes. `series delete s1 --yes` returned `relay: "missing"` and the removed directory. Evidence: `http://127.0.0.1:8098/vom-nightly-20261102/r1/` (`cli/01-15`, `cli/50-65`, `cli/128-153`).*

*Re-driven 2026-11-01 (nightly), tree `7ce379c45` (origin/main, v0.480.3), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 2.9. `config show` (masked key), `config key-info` (`om_guest`, `expired: false`), `config get chat.sounds` (`value: null`, `default: on`, `stored_as: tui.sounds`), `config get data.transport` (`default: auto`), `set agent.max_tool_calls 250` exit 2; `enum --list` (26 domains; `indicator_template` now counts **92**), `enum --domain indicator_template` lists `flow-vwap`, `enum --domain exchange_id --query BIN --limit 3`; `schema read` (7 intents); `skill list` (16 names, one per line; it takes no `--format`); `wrun list` (`@om-core/accumulate` 0.1.3); `wrun templates` **92** (new with #2235: `flow-vwap` in group `Order flow`, `runsOn` naming OPRA at the viewer's own tier; 84 `runsOn` entries, 31 with "at your own tier"); `wrun create @vommaint/flow-vwap <dir> --template flow-vwap` scaffolded a workspace whose `.wrun-scaffold` reads `scaffold_version 107` and whose `src/indicator.ts` reads `options_flow.*` inputs with `underlying: "@chain"`; `upgrade --show`; `notis --since 7d --json` (`notice` and `fire` rows); `vault status`; `GET /openapi.json` (200, 137 paths, 0.480.3); `research study --watch lane-probe --locate-only`; `nervous status` (`enabled: true`, `watch_fired` receipts); `GET /secrets/status` (`unminted`); `GET /api/away` 401; `approvals list` `[]` and `GET /rpc/v1/approvals`; `setup default` and `setup default nope --force` (`channel_not_found`); `follows`, `follows show @nobody/nothing`, both `relay trace` refusals, `unsubscribe nope`, `usage plans`, `subscriptions` (`account_required`), `series list`. `terms --format json` exited 1 `registry_unreachable` (the staging registry timed out; see [registry welcome and search](./registry-welcome-and-search.md)). Evidence: `http://127.0.0.1:8098/vom-nightly-20261101/r1/` (`cli/07-13b`, `cli/20-29l`, `cli/48*`).*

*Re-driven 2026-10-31 (nightly), tree `dfefe0a21` (origin/main, v0.480.2), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 1.6. `config key-info` (`om_guest`, `key_set: true`); the new `chat.sounds` key (set/get/refusal, below); `set agent.max_tool_calls 250` exit 2; `setup default` read and refusals (Guest-lane reads); `enum --list` (26 domains), `enum --domain exchange_id` (35, no `BYBIT_FUTURES`), `schema read`, `skill list`, `wrun templates` (91), `upgrade --show`; `notis --since 7d --json` (`fire` rows); `vault status` (`mode: none`, `keyring: macOS Keychain (available)`; it takes no `--format`); `GET /openapi.json` (200, 137 paths, `info.version` 0.480.2); `research study --watch lane-probe --locate-only` (one occurrence); `nervous status` (`enabled: true`, a `watch_fired` receipt); `GET /secrets/status` (`readiness: unminted`); `GET /api/away` 401 `operator_required`; `approvals list` `[]`. Evidence: `http://127.0.0.1:8098/vom-nightly-20261031/r1/` (`cli/26-29c`, `cli/40-43`, `cli/51`, `cli/60-67`, `cli/89-89h`, `cli/93`).*

*Re-driven 2026-10-30 (scheduled maintenance), tree `3cb50a821` (origin/main, v0.478.0), fresh lane on 18165, host load average about 140. `config key-info` (`expired: false`, `tier: om_guest`), `enum --list` (`exchange_id` 35), `skill list`, `notis --since 1d` (the lane's own fires), `wrun templates` 91, `approvals list` (`No pending approvals.`), `nervous status` (`enabled: true`), `sidebar`. New this pass: `vault status` (`mode: none`, `keyring: macOS Keychain (available)`; it takes no `--format`), `terms --format json` (`not_applicable: true`, `accepted: false` for a guest), `unsubscribe nope` (`confirmation_required`), and `GET /openapi.json` (200, 137 paths including `/healthz`). Evidence: `http://127.0.0.1:8098/verify-om-maint-20261030/r1/` (`cli/10`, `cli/11`, `cli/13`).*
*Re-driven 2026-10-30 (nightly, smoke depth), tree `3cb50a821` (origin/main, v0.478.0), lane on 18163. `config set agent.max_tool_calls 250` exited 2 with `om: agent.max_tool_calls must be a positive integer, at most 249.` (the cap fell with the 500-call run ceiling, #2206). `set … 249` printed `om: set agent.max_tool_calls=249`, and `config get agent.max_tool_calls` read `249`, `source: config`, `rule: positive integer, at most 249`, `default: 24`. `wrun templates` still lists 91. `notis --since 1d` was refused `request_failed` (`this home's daemon is unavailable`); that was the busy-host probe, not the verb (see [daemon lifecycle](./daemon-lifecycle-and-health.md)). Evidence is local only (the `8098` renderer did not answer): `artifacts/vom-nightly-20261030/r1/`.*

*Re-driven 2026-10-29 (scheduled maintenance), tree `7ec575e55` (origin/main, v0.467.0 plus #2194), fresh lane on 18161. `wrun templates` returned 91 templates. The three Feeds starters (`feed-alert-line`, `feed-events`, `feed-status-card`) now say "set ref to a feed you published" (#2194). Driven for the first time: `wrun create @vommaint/feed-probe <dir> --template feed-alert-line --format json`, into a directory outside the product tree. It returned `{path, packageId, template, files[29], metricIds[3]}` and wrote `.wrun-scaffold` `{"scaffold_version": 106}`. `src/indicator.ts` reads `ref: "@you/your-feed"`. Also re-driven: `wrun list` (20 packages) and `skill list`. Not driven: `wrun validate` and `wrun build`. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261029/r1/`.*

*Re-driven 2026-10-29 (nightly, smoke depth), tree `32ca0d6c7` (origin/main, v0.467.0), lane on 18103: `config key-info` (`expired:false`), `config get chat.workspace` (new key: `unset (default: off)`, `stored as tui.workspace`), `notis --since 7d` (fire rows), `enum --list` (`exchange_id` count 35), `skill list` (one name per line; it takes no `--format`), `wrun templates` (still 91), `approvals list`, `nervous status`, and `search "funding rate"` (production result shape). `WRUN_SCAFFOLD_VERSION` is now 105 (#2184); only a new scaffold shows it. Evidence: `http://127.0.0.1:8098/vom-nightly-20261029/r1/`.*

*Verified: 2026-10-28 (scheduled maintenance), tree `186030b63` (origin/main), lane on 18143. Re-driven: `status`, `doctor`, `service status`, `logs`, `config show`, `config key-info` (that home's key had `expired: true`, see [market data reads](./market-data-reads.md)), `enum --list` (`exchange_id` still 35), `schema read`, `wrun list` (`@om-core/accumulate` 0.1.3) and `wrun templates` in JSON and text form (91 templates; the #2180 `runsOn` wording, see Gotchas). Evidence: `http://127.0.0.1:8098/verify-om-maint-20261028/r1/` (`cli/01-09.txt`, `cli/09-text.txt`).*

*Nightly record: 2026-10-28, tree `a8fa10974` (origin/main, v0.466.0), lane on 18103. Re-driven: `config show` (`api_key_set`, a masked key), `config key-info` (`om_guest`, not expired), `config get data.transport` (`source default`, `default auto`), `notis --since 7d` (`notice` and `fire` rows), `enum --list` (26 domains), `schema read` (7 intents), `skill list`, `wrun list` (`@om-core/accumulate` at 0.1.3) and `wrun templates` (still 91). Newly driven: the guest-lane reads below (approvals, nervous, follows, relay, research study, away). Not re-driven: series, plans and secrets status (2026-10-27). Not driven: `config set`, `notis --after`, `schema read <intent>`, `skill show`, `wrun create`/`build` and `vault status`. Previous stamp `8fe6a8432` is an ancestor (10 commits).*

*Second-pass record: 2026-10-27, tree `8fe6a8432`, lane on 18143.* Re-driven: `enum --list`, `config show` (`api_key_set` true from the lane's own guest `credentials.json`), `wrun list`, `schema read`. Series, plans and secrets status were added above. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261027/r1/` (`pending-rows.txt`).

The questions a user asks the install itself rather than the market: which key
is in use and when it expires, what a setting is and where its value comes from,
what the daemon has already told me, which values a flag accepts, which bundled
skills exist, and which indicator packages ship. All of them read local state or
bundled constants. None needs an account or a model.

## Sub-features

- `config-show` / `config-key-info` / `config-get`: the masked key, the decoded
  key claims (tier, expiry), and one setting's effective value, source, rule and
  default.
- `config-set` / `config-list` (added 2026-11-02): about 85 settings keys live in
  `CONFIG_KEYS` (`packages/cli/src/cmd/config-keys.ts:157`, rendered into
  `docs/CONFIG_KEYS.md`). `config get <key> --format json` reads `key`, `value`,
  `source` (`default` or `config`), `rule`, `default` and `description`;
  `config set charts.auto_open false` then `get` reads `value "false"`,
  `source "config"`; a value outside the rule exits 2
  (`approvals.writes must be one of: auto, ask.`). There is no `config unset`
  (`unknown command 'unset'`): set the default back. `config list --format json`
  returns every key. Driven 2026-11-02 for `approvals.writes`, `charts.auto_open`,
  `telemetry.product`, `sharing.notify.knocks`, `collab.agent_label`,
  `wallet.cluster`, `nervous.channel` and `chat.icons`; what each key changes at
  runtime is not proved here.
- `notis`: the daemon's own notification history (watch fires, arrivals, notices).
- `enum-list` / `enum-domain`: the enum domain index, and a paged, searchable
  domain.
- `schema-read`: the intents an agent can ask the schema door for.
- `skill-list`: the bundled skill files.
- `wrun-list` / `wrun-templates`: installed indicator packages and scaffold
  templates.
- `wrun-regimes-flat` (added 2026-11-09, #2414): `wrun create <id> <dir> --template positioning-regimes` writes the `flat` histogram output (`theme.muted`), and `wrun build` lists `wrun/<id>/flat` beside `regime`. A flat bar's values are unit-tested; the build proves only the output exists.
- `wrun-style-names` (added 2026-11-09, #2407): scaffold **118**. The sheet gains a top-level `style_names` table, and `label` / `color_labels` on marks, spans, rays, flags, renderers and outputs. An `@om-core` package with an unnamed Style line, or an unnamed colour list of two or more, is refused `wrun_style_unnamed` at publish and by `om wrun validate` (`runner/wrun/authoring.ts:1359`); other scopes are not refused. The `positioning-regimes` template names every line, so `wrun validate` on an `@om-core` copy passes; the refusal itself is source only.
- `wrun-build-window-warning` (added 2026-11-08, #2405, scaffold 117): `wrun
  build` warns `WRUN_DECL_INTERVAL_WINDOW_SHORT` when a window fed by an input
  pinned to a coarser interval cannot fill: a scalar pin updated once per pinned
  candle, or a `candles.cells` stream with no `bars` or `bars` short of the
  window. The warning names the input, the class and its window, and the repair.
- Local series authoring (`om series create|list|show|delete`) and the marketplace listing refusals of `om series publish --price|--stop-sales|--resume-sales|--free` (#2240), the plan table (`om upgrade --show`, `om usage plans`) and the sealed-secrets status read (`GET /secrets/status`).

## How to get to it (user POV)

- `om config show`, `om config key-info`, `om config get <key>`.
- `om notis --since 7d`.
- `om enum --list`, `om enum --domain <d> --query <q>`.
- `om schema read`, `om skill list`, `om wrun list`, `om wrun templates`.

## Driving it with control-om

Preconditions: a lane the run started. Run any data read first (`control-om om
-- coins`) so the guest key exists; before that, `key-info` has nothing to
decode.

- **Key and config.** `control-om om -- config show --format json`: assert
  `api_key_set` true and a masked key, never a raw one. `config key-info
  --format json`: assert `tier` `om_guest` and `expired` false. `config get
  data.transport --format json`: assert `source` `default` and `default` `auto`.
  `config set agent.max_tool_calls 250` exits 2 (`at most 249`); a value
  stored above 249 by an older build reads as 249. `config get chat.sounds`
  (new in #2217) reads `unset (default: on)`, stored as `tui.sounds`;
  `config set chat.sounds off` prints `om: set chat.sounds=off` and silences
  the chat chimes and bells; any value but `on`/`off` exits 2 with
  `chat.sounds must be on or off.` (driven 2026-10-31).
- **Notifications.** Produce one first: an inbound watch left on the default
  classifier emits a `notice` once judging fails on a guest. Then `control-om om
  -- notis --since 7d --json` returns `rows[]` with `at`, `kind`, `watch` and
  `text`.
- **Enums.** `control-om om -- enum --list --format json` returns `domains[]`
  with `name`, `count`, `dynamic` and a `sample`. `enum --domain exchange_id
  --query BIN --limit 3` returns one page with `total` and `next_offset`.
- **Schema intents and skills.** `control-om om -- schema read` returns
  `intents[]`, each with `intent`, `line` and `calls`. `skill list` prints one
  skill name per line.
- **Indicator packages.** `control-om om -- wrun list` returns `packages[]`
  with `id`, `version` and `wasmSha256`. `wrun templates` returns `templates[]`.
  Each entry has `id` and `description`. Picker templates also carry `group`
  and `runsOn`, which is where the template states its data reach. The text
  form (`wrun templates --format text`) prints the latter as `[<group>]` after
  the id and a `Runs on: …` line (`cmd/wrun.ts:583-594`).
- **Proof.** Keep each command, its JSON and its exit code. Redact nothing: none
  of these prints a secret, which is itself the assertion for `config show`.

### Series, plans and secrets status (added 2026-10-27)

- **Series:**
  - `series list` on a fresh lane returns `{"series":[]}`.
  - `series create s1 --watch <watch> --key v --scope local --format json` creates `@local/s1` with version 0.1.0 and `rows: 0`. `list` and `show` then read it back. Since #2240 `show --format json` carries `visibility` (`public` for a fresh local feed; `listed` once it is priced) and the text form prints `Visibility: public` and `Feed: not on the relay yet`; `list --format text` appends ` | listed: $9 / month` only to a priced feed.
  - `series publish s1 --dry-run` (no price) reaches the registry with the lane's guest key. Earlier passes read `publish_rejected` ("kind 'live-series' is not accepted by the v1 registry"); on 2026-11-02 it read `registry_unavailable` (503, "could not confirm this account's username"). Either way exit 2.
  - **Selling a feed (#2240, #2241) refuses locally on a guest, before any relay or registry call.** `series publish s1 --price 9/mo --dry-run` exits 2 `seller_session_required` ("Selling a feed needs a sign-in session; this home signs in with a login key", hint `OM_LOGIN_LANE=session om login`); `--free --yes` reads the same. The price is parsed first: `--price 1/mo` is `price_below_minimum` ($2.50 floor), `--price abc` is `invalid_price` ("Write a monthly price as 9/mo or a one-time price as 20 once (USD)"). `--stop-sales --yes` or `--resume-sales --yes` on an unlisted feed is `listing_free`; two sales flags in one call are `invalid_options` ("cannot ride one call"); `--price` without `--dry-run` or `--yes` is `confirmation_required`. The marketplace origin is `OM_ORANGE_ORIGIN` (default `https://chart.openmarket.xyz`), read only after the session check, so a loopback stub cannot be reached from a guest lane. A real listing, `Visibility: listed (…)`, the `listed:` marker, `feed_tier_required`, `listing_price_locked` and the `series_listed` delete refusal need a sign-in session (pending).
  - `series delete s1 --yes --format json` removes the directory and reports `relay: "missing"` for a feed never declared on the relay.
- **Plans:**
  - `upgrade --show --format json` is static: the guest note is "Guest keys (no sign-in) get 600 weight per 60s window and 7 days of history…", followed by the plan list.
  - `usage plans --format json` returns `{"providers":[]}`.
  - `subscriptions --format json` exits 1 with `account_required`.
- **Secrets status:** `GET /secrets/status` returns 200 `{"ok":true,"data":{"userId":"guest_…","readiness":"unminted","hasRecoveryBlob":false,"recoveryUnavailable":true,"alarms":[]}}`. It is not a 401, because the lane mints its own guest key.

### The interval-window warning (added 2026-11-08)

Proves #2405 on a guest lane. No model and no account are needed; the build
runs `bun install` in the workspace the first time, so it needs the network.

- **Create a code-first workspace** outside the product tree:
  `control-om om -- wrun create @vom/win117 <dir> --template sma-codefirst --format json`.
  `<dir>/.wrun-scaffold` reads `{"scaffold_version": 117}`. Use
  `sma-codefirst`, not `sma`: the declaration scan reads `input(...)` lines in
  `src/indicator.ts`, which only the code-first template has.
- **Warn on a scalar pin.** Replace `src/indicator.ts` with
  `input("close", ohlcv.close);`, `input("w", ohlcv.close, { interval: "1w" });`,
  `input("w_new", ohlcv.close, { interval: "1w", view: "is_new_period" });`,
  `output("ma", line, overlay);`, `let ma = new Sma(50);`, a
  `let value: f64 = NaN;`, and an `onBar` that runs
  `if (in_w_new() == 1.0) value = ma.update(in_w());` then `out_ma(value);`.
  `control-om om -- wrun build <dir> --format json` exits 0, and `warnings[0]`
  reads `src/indicator.ts:2: input 'w' pins 1w and feeds Sma (a window of 50)
  once per 1w candle, but the module reads only the 1w candles that close
  inside the chart's loaded bars, … read the candles from a candles.cells input
  with interval 1w and bars of at least 50, and update the window from its
  blocks`. `--format text` prints the same line under `Warnings:`.
- **Warn on a stream.** Make the `w` input `candles.cells` with
  `{ interval: "1w" }` and update `ma` from the block's close
  (`unchecked(block[i + 4])`, stride 6, over `in_w_view()` and `in_w_cells()`).
  The warning reads `input 'w' hands Sma (a window of 50) its 1w candles with
  no bars, …: declare bars of at least 50 …`. With `bars: 20` it reads `… with
  bars 20, which reach only 20 of them back from now, …`.
- **No warning.** The same stream with `bars: 50`, or the scalar pin updated on
  every chart bar (`value = ma.update(in_w());` with no `is_new_period` gate),
  builds with no `input 'w'` line in `warnings`.
- **Proof.** Keep each module and its build JSON. The other `warnings` entries
  (the download size, `Market check`, `Alerts`) follow the declaration warning
  and vary by variant, so match the `input 'w'` line by substring, not by index
  past the first.

### Guest-lane reads (added 2026-10-28)

All were driven on a fresh guest lane at `a8fa10974`. Each answers or refuses
with no account:

| Call | Observed |
|---|---|
| `approvals list` / `--format json` | `No pending approvals.` / `[]`; `GET /rpc/v1/approvals` returned `{"ok":true,"data":{"approvals":[]}}` |
| `approvals list --kind draft` / `--kind bogus` (#2258: one inbox of five kinds, `chain`, `mcp`, `grant`, `draft`, `proposal`) | `No pending approvals.` / exit 2 `--kind must be one of: chain \| mcp \| grant \| draft \| proposal`; `GET /rpc/v1/approvals/inbox` returned `{"items":[],"counts":{"total":0,"byKind":{…all 0}}}` |
| `approve nope` | exit 2 `nope is not an approval id` / ``Run `om approvals list` to see pending ids.`` |
| `todo get 12` (#2291) | exit 1 `12 is a ticket number, which names a ticket only within its server` / `Pass spaceId and number.` |
| `todo get om://todo/room/12/5`, `todo get om://todo/lab/12abc` (#2410; driven 2026-11-08, `5590b4d1c`) | each exit 1 `invalid_ref` `Not a server ticket link: <ref>` / `Projects lives in servers: pass the server's spaceId and the ticket number`. A ticket link has one form, `om://todo/<spaceId>/<number>`: the retired room form and a link the text runs on from are not links. `todo get om://todo/lab/12` parses and reaches the relay: `room_social_failed` 401 on a guest key. |
| `todo list --space x --format json` | exit 1 `room_social_failed` `Unauthorized` (401): a guest key reaches the relay and is refused; a real ticket needs a rooms account. Over MCP stdio `todo_get` answers `not_badge_bound`. |
| `todo label list`, `todo similar <words>`, `todo get <n>` with `--space openmarket --format json` (#2341, #2342; driven 2026-11-06, `50fcc594b`) | each exit 1 `room_social_failed` `Unauthorized` (401), like `todo list`. The write verbs (`create`, `update`, `comment`, `follow`, `delete`, `label create\|rename\|merge\|delete`) need a rooms account; over MCP stdio `todo_create` answers `not_badge_bound`. |
| `agent status set --file <json>` / `agent status clear` (#2359; driven 2026-11-06) | exit 2 `Guests can view but not chat — sign up to participate`: the status rides the relay as the signed-in user. |
| `setup default` (driven 2026-10-31, `dfefe0a21`) | `{"default":null,"routing":"none","targets":[]}`; the verb's default `--format` is `json`, so a text read needs `--format text` |
| `setup default nope`, also with `--force` (#2220) | exit 2 `channel_not_found`: `unknown channel 'nope' — no channels are configured`, hint `Run \`om setup list\` …`, `details.channels: []`. The `channel_failing` refusal and the `routing_note` line need a paired channel |
| `nervous status --format json` | `{enabled:true, dailyBudgetPerSender:null, receipts:[…]}`. After an ingest fire it held a `watch_fired` receipt reading `no canvas resolved for (no symbol), stayed a notification` |
| `follows --format json` | `{follows:[], summary:{… total:0}}` |
| `follows show @nobody/nothing` | exit 2 `not_following` |
| `relay trace @nobody/nothing` | exit 2 `relay_ref_unknown` (hint: `om watch list names the shares and the follows.`) |
| `relay trace 'not-a-ref!!'` | exit 2 `relay_ref_invalid` |
| `research study --watch <inbound-watch> --locate-only --format json` | `{watch, time_basis:"observed_at", occurrences:[…]}`, with no candle fetch |
| `research study --watch nope --locate-only` | exit 2 `watch_not_found` |
| `curl $(control-om url /api/away)` (and `/api/away/coverage`) | 401 `operator_required`: "Away access requires operator proof." |

The away reads need the daemon GUI's per-boot session cookie, or a configured
runner or desktop token, even on loopback. `/api/away/policy` is a `POST`. Do
not drive `approvals approve|deny` on a real row (an unknown id is safe, above), `follow review`, `research search-files` or
`research make-image` from a lane: they need a human terminal or spend on a
model.

### A server mute, against a loopback relay stub (added 2026-11-09, #2417)

A guest key reaches any `--url`, so a loopback stub proves the refusal's wording with no account. Run a `Bun.serve` on an agent port that answers `POST /todos` with `403` and `{"tag":"SPACE_MUTED","code":"SPACE_MUTED","mutedUntil":"<ISO>","error":"muted"}`, then:

```bash
control-om om -- todo create "x" --room general --url http://127.0.0.1:<stub-port> --format json
```

- Exit 1 `space_muted`, message `You're muted in this server until 3:51 AM` in local time, hint `Reading still works. Changes wait until the mute ends.`, `details.mutedUntil` the ISO end. An end on another day reads `until Nov 10, 5:21 AM`. The text form prints the message and the hint.
- `mutedUntil` absent: the refusal stays `room_authority_required`, as before #2417.
- `todo update --ids a,b --status done` hits `POST /todos/bulk`, whose `200` body is `{"results":[{"todoId":"a","ok":false,"tag":"SPACE_MUTED","mutedUntil":"<ISO>"},…]}`. Nothing changed and every refusal is the mute: `space_muted` at the latest end. One row `ok:true`: exit 1 with the batch report, the muted id under `failed` as `space_muted`.
- The reaction, edit, topic and upload paths share the mapping and are not driven here.

## Gotchas

- `om usage plans` is not a Data API read. It reports MODEL provider plan holds.
  See [market data reads](./market-data-reads.md).
- **`wrun build` with no `--format` prints JSON when stdout is not a terminal**
  (the shared `--format` default follows the output: text for a person, JSON
  for a pipe). A driver that captures output and wants the `Warnings:` block
  passes `--format text`.
- `wrun build` compiles and runs `bun install` by default, so it needs the package
  registry. Keep it out of a quick pass. Its JSON carries `historyIndependence`
  (`{"stamped":false,"reason":"classic"}` for the `sma` starter, driven
  2026-11-03 at `777ee7f21`). **Since #2270 (`777ee7f21`, v0.488.0) a build
  writes the converging warm-up stamp by default** (#2267, scaffold 111): an
  affine EMA or RMA of the chart's own feed gets `history_warmup` kind
  `converges` (tolerance 1e-6, a `gate` record) in the built
  `dist/package/wrun/metadata.json`, never in the workspace's own
  `wrun/metadata.json`. A refused candidate adds the warning `history_warmup not
  written: the converging warm-up's gate refused it (<code>)…`;
  `OM_WRUN_CONVERGES=0` (or `off`) turns it off. Most starters do not qualify:
  the `sma` build wrote `history_warmup: null` and no warning. A stamped build
  has not been driven.
- **The US options templates read OPRA at the viewer's own tier since #2180
  (`f8b2ca3b4`), and since #2243 (`49aa1672f`) their CME clause reads "CME
  futures in your browser".** At `2567b7974` (2026-11-02) the text form had 92
  templates, 84 `Runs on:` lines, 31 reading "in your browser" and none reading
  "through OpenMarket"; #2237 also rewrote every options template's
  `description` in plain words (`strike-matrix` now opens "A price-axis board
  shows this symbol's options…"). Before #2243 the clause read "CME futures
  through OpenMarket's official package", where it used to say
  both went through the official package. Driven 2026-10-28 at `186030b63`:
  91 templates, 83 `Runs on:` lines, 30 with "at your own tier" (the commit's
  thirty sentences) and none with the old "US stocks (OPRA) and CME futures
  through" wording. At `7ce379c45` (#2235) those read 92, 84 and 31: the new
  `flow-vwap` starter is the thirty-first. A JSON assertion that reads only
  `description` misses this field.
- **`wrun templates` gained `flow-vwap` in #2235 (`942d0eb54`, v0.480.3), and
  `WRUN_SCAFFOLD_VERSION` is 117 since #2405 (`2a1e1389f`;
  `packages/sdk/src/wrun-sdk-sources.ts:1285`; 116 at #2379, 108 at #2239, 109 at #2245, 110 at #2246, 111 at #2267, 112 at #2273, 113 at #2283, 114 at #2336, 115 at #2339). #2379 also added the `dark-pool-prints` template (93 in all), whose workspace carries the `dark_pool` input and `plot.flags`.** The template sits in group `Order flow`
  (the chart's price weighted by aggressive options premium, with sigma
  bands). **`wrun create` takes the package name first:** `wrun create
  @you/<name> --template flow-vwap <dir>`; a bare directory is refused
  "package name must look like @scope/short-name". A fresh create writes
  `.wrun-scaffold` with the current scaffold (`{"scaffold_version": 117}` on
  2026-11-08), an `indicator.ts` whose
  `options_flow` inputs carry the `underlying` knob (`"@chain"`, a select
  of `auto`, `derived`, `QQQ`, `NDX`, `SPY`, `SPX`), and a `src/sdk/declare.ts`
  and `scripts/wrun-prebuild.mjs` that carry the keyed-row words
  (`visible_by`, `needed_by`, `min_coins`). A scaffold-106 or 107 workspace
  refreshes only those two files on its next build. Drive the create into a
  directory outside the product tree, and assert membership, not the count
  (driven 2026-11-01 at 107, 2026-11-02 at 108 and 110, 2026-11-03 at 111 with
  `wrun create @lane/vom-ema --template sma <dir>`, 2026-11-04 at 113 with
  `wrun create @vom/probe <dir> --template sma`, 2026-11-08 at 117 with
  `wrun create @vom/win117 <dir> --template sma-codefirst`; `--template rsi` is not a
  template and exits 2 `request_failed` listing the names).
- **`wrun templates` lost six option recipes in v0.466.0** (`5a03ffb43`):
  `dealer-nodes`, `gamma-map`, `zero-dte-levels`, `vol-term-structure`,
  `vol-smile` and `iv-term-structure`. The list went from 97 to 91, and those
  ids are gone from the template enum domain too, so `wrun create --template
  <one of them>` now fails. `expected-move` remains. Assert membership, not a
  count.
- `hl_dex` is a dynamic enum domain listed live from the venue. It needs network
  where the static domains do not.
- Per source (`cmd/notis.ts`; not driven), `notis` exits 1 on a runtime error
  and 2 on invalid input, like the other action-backed verbs.
