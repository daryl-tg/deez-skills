# Local reads and discovery

*Re-driven 2026-11-24 (nightly), tree `26d502c689` (origin/main, v0.496.0+internal), guest lane on 18188 through `bootstrap.internal.ts`. The `wrun build` session defect still holds: `wrun create @vom/sess124 <dir> --template sma-codefirst` wrote scaffold 123, one prebuild pass wrote `"session": "extended"`, `wrun validate` exited 0, and `wrun build` exited 2 with `inputSources.night.session` in the `cannot express` line. #2657 and #2661 change only the Pine conversion guide. Also re-read: `config get pages.renderer` (`unset (default: auto)`, rule `auto or off`), `wrun templates`, `skill list`, `notis --since 7d --json`, `secrets status`, `devices list` (`this_device_id`), `channel list` `[]`, `upgrade --show`, `persona show`, `series list`. Source only: #2683's display-only index pin. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261124/r1/` (`cli/30`, `cli/31`, `cli/breadth/33-*`, `cli/breadth/34-*`, `cli/breadth/35-*`).*

*Re-driven 2026-11-22 (nightly), tree `01482928a5` (origin/main, v0.496.0+internal), guest lane on 18188 through `bootstrap.internal.ts`. First live proof of scaffold 122 (#2653) and scaffold 123 (#2655): `wrun create @vom/rec123 <dir> --template sma-codefirst` wrote `{"scaffold_version": 123}`; a QQQ chain read through `underlying` with `chart.derived_ratio()` built with exit 0 and a hidden `chart_derived_ratio` param (`host_fill: "derived_ratio"`, default 0); the old `derivedRatio(...)` placement built with the `nothing declares chart.derived_ratio()` warning on an overlay and with none on a lower pane; a `session: "extended"` candles input reached the sheet after one prebuild pass and `wrun validate` passed it, and `wrun validate` named `wrun_input_session_invalid` for the primary input, an `ohlcv` input and a `view: "forming"` candles input. `wrun build` itself refuses every sheet that carries `session` (exit 2, see Gotchas): a product defect. Also driven: `wrun templates` (93), `config show`, `enum`, `skill list`, `notis`, `om secrets status` and `GET /secrets/status` (`thisDeviceId` on the route only), and five reads new to this guide (`account-and-channel-reads`). Not re-driven: `schema read`, the scaffold refusals for marks and themes, ticket links, the device keys and the QR. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261122/r1/` (`cli/10` to `cli/13`, `cli/33`, `cli/35`, `cli/91`).*

*Re-driven 2026-11-21 (nightly), tree `3c4839c59d` (origin/main, v0.496.0+internal), guest lane on 18188 through `bootstrap.internal.ts`. Secrets: `GET /secrets/status` now carries `thisDeviceId` (equal to the home's `device-id` file), `om secrets status` in JSON does not, `--format text` and `om secrets devices` unchanged. Also re-driven: `config show`, `config get`, `enum`, `schema read`, `skill list`, `wrun templates`, `notis`, `upgrade --show`, `wallet list`. Not re-driven: `wrun create` and `build`, the scaffold refusals, ticket links, the device keys and the QR. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261121/r1/` (`cli/30`, `cli/a1`, `cli/90`).*

*Re-driven 2026-11-20 (nightly), tree `ba18e48ef3` (origin/main, v0.496.0+internal), guest lane on 18188 through `bootstrap.internal.ts`, the guest sign-in minted at boot. `om upgrade --show` prints the plan table as JSON: the guest note reads `600 weight per 60s window and 7 days of history`, Free `30 days of history`, and since #2600 the Plus row reads `On an API key: 365 days of history` (it read `full historical depth`). Also `enum`, `skill list`, `config show`, `notis`, `secrets devices` (`{"devices":[],"unverified":false}`), `persona show`, `sidebar`, `memory list`, `auth status`, `wrun templates`, `chart indicator schema rsi`, `chart drawing schema`, `open @om-core/rsi --print`. `POST /api/away/arm` is still 401 `operator_required`. Not re-driven: the rest of this file. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261120/r1/` (`cli/20-plans.txt`, `cli/52-local-reads.txt`, `cli/56-breadth.txt`).*

*Re-driven 2026-11-19 (nightly), secrets devices only, tree `1e71657cdd` (origin/main, v0.496.0+internal), guest lane on 18188 through `bootstrap.internal.ts`: `om secrets devices` (JSON by default, `{"devices":[],"unverified":false}`), `--format text` `Devices:  none listed`, `GET /secrets/devices` 200 `{"ok":true,"data":{"devices":[]}}`, `om secrets link --help`. The device keys, the versioned list, the QR and the malformed-key refusal are source only. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261119/r1/` (`cli/50-secrets.txt`).*

*Re-driven 2026-11-18 (nightly), tree `db4ba5c6e2` (origin/main, v0.496.0+internal, SDK 0.500.0), guest lane on 18188. First live proof of scaffold 121 (#2546): `wrun create @vom/marks121 <dir> --template liquidation-bursts` writes `scaffold_version 121`; `text.place: 3` and `4` build to `"place": 3` and `4`; `place: 5` exits 2 `marks.0.text.place: text.place must be an integer from 0 to 4`; `param.choice("place", ["Inside short", "Inside only", "Beside"], "Inside short", { style_values: ["fit_short", "fit_only", "beside"] })` with `place: "@place"` builds a sheet holding `"place": "fit_short"` and the param `options [0,1,2]`, `style_values ["fit_short","fit_only","beside"]`, `style_targets [{path: ["marks",0,"text","place"]}]` (`wrun-marks-text-fit-short`). Not re-driven: every other entry. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261118/r1/` (`cli/wrun-build-word.json`, `cli/wrun-place-source.txt`).*

*Re-driven 2026-11-17 (nightly), tree `8e350d253a` (origin/main, v0.495.0+internal), guest lane on 18188 started through `bootstrap.internal.ts`; the guest sign-in was rate limited (429), which these local verbs do not need. First live proofs of scaffold 120 (#2525), the chart-default pin refusal (`ff4daf0cc2`) and the 90-day dark pool text (#2529): `wrun create @vom/marks120 <dir> --template liquidation-bursts` writes `scaffold_version 120`; `text.place: 2` builds to `"place":2`; `text.place: "@place"` bound to a `param.choice` whose `style_values` are place words builds to `"place":"fit"`; `place: 3` and `place: "middle"` are refused, exit 2; a candles input whose interval comes from `param.timeframe("tf", "chart")` is refused by name, exit 2, and the same input at `"1h"` builds (`wrun-marks-text-fit`, `wrun-chart-default-pin`). `wrun templates` is still 93 and `dark-pool-prints` now reads `about 90 days back, at most 15,000 a chart window`. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261117/r1/` (`cli/wrun-place.txt`, `cli/wrun-chart-default-pin.txt`).*

*Re-driven 2026-11-16 (nightly), tree `53885683de` (origin/main, v0.495.0+internal), guest lane on 18188 started through `bootstrap.internal.ts` (PR #24's wrapper), booted with no guest 429. First live proof of scaffold 119 (#2509): `wrun create @vom/marks119 <dir> --template liquidation-bursts` writes `scaffold_version 119`; a build with a word-bound `look` choice, `text.place: 1` and `["theme.down_mark", "theme.up_mark"]` writes them to the sheet; `theme.UP_MARK` in a draw call is refused by name, exit 2; the untouched template's sheet has no `place` key (`wrun-marks-glass-solid`). `wrun templates` is still 93. Not re-driven: the other sub-features. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261116/r1/`.*

*Re-driven 2026-11-15 (nightly), tree `5a4cb146d4` (origin/main, v0.495.0+internal), guest lane on 18185 started through `bootstrap.internal.ts`, no guest 429. First live proofs: the `todo_records_off` refusal against a loopback relay stub (#2500), and the partial-bar wash in four order-flow templates (#2506): `wrun create … --template dark-pool-prints|strike-footprint|flow-marks|option-prints` each wrote scaffold 118; the first two declare a `shown_in_part` output that gates the `Bars with missing prints` wash, and the last two have no wash. `wrun templates` is still 93. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261115/r1/` (`cli/todo-records-off.txt`, `cli/wrun-partial-tint.txt`).*

*Re-driven 2026-11-14 (nightly), tree `05300a3142` (origin/main, v0.495.0+internal), guest lane on 18185 started through `bootstrap.internal.ts`, no guest 429. First live proofs: the sealed-secrets doors and verbs added by the secrets series (`7e5a380b20` to `9d7308e143`), and the weekly-candles refusal (#2503). Not re-driven: the series, plans, `enum` and `schema` reads. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261114/r1/` (`cli/secrets-*`, `cli/wrun-weekly-*`).*

*Re-driven 2026-11-11 (nightly), tree `0ad4768f66` (origin/main, v0.494.0), guest lane on 18181, booted with no guest 429. `config show` (masked key), `config key-info`, `enum`, `wrun templates`, `notis --format json` (the fire row), `wrun create @nightly/sizeprobe --template sma` (`.wrun-scaffold` `scaffold_version: 118`) and `wrun build` on it; `schema read watch_create` is `unknown_intent` with the intent list; `todo list --space x` is `room_social_failed` `Unauthorized`; `skill list` takes no `--format`. Not re-driven: the size-unit warning, `space_muted`, the interval-window warning. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261111/r1/`.*

*Re-driven 2026-11-10 (nightly), tree `c9bc93a355` (origin/main, v0.493.1), guest lane on 18143, booted with no guest 429. `config show` (masked), `enum --list` (`exchange_id` 38), `skill list`, `schema read condition_create`, `wrun templates` (93). First live proof of `wrun-size-unit-words` (#2430): the `cvd-divergence` scaffold builds four CVD outputs with no warning; ungated, build and validate warn; as `@om-core/cvd-probe`, validate exits 2 `wrun_size_unit_word`. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261110/r1/` (`cli/wrun-cvd-*.txt`).*

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
  `CONFIG_KEYS` (`packages/cli/src/cmd/config-keys.ts:175`, rendered into
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
- `wrun-style-names` (added 2026-11-09, #2407): scaffold **118**. The sheet gains a top-level `style_names` table, and `label` / `color_labels` on marks, spans, rays, flags, renderers and outputs. An `@om-core` package with an unnamed Style line, or an unnamed colour list of two or more, is refused `wrun_style_unnamed` at publish and by `om wrun validate` (`runner/wrun/authoring.ts:1381`); other scopes are not refused. The `positioning-regimes` template names every line, so `wrun validate` on an `@om-core` copy passes; the refusal itself is source only.
- `wrun-size-unit-words` (added 2026-11-10, #2430): `wrun build` and `wrun validate` warn when an output's `unit` names a size word (`coins`, `shares`, `sh`, `contracts`) on every market: `output 'cvd' prints " coins" on every market, but only a size_unit 1 market counts in coins: gate it with visible_by: { size_unit: [1] } beside a twin without the word on [0, 2, 3]`. An `@om-core/` package is refused at `wrun validate` (and `om publish`) with `wrun_size_unit_word`, exit 2. The CVD Divergence template (0.3.0) builds `cvd` and `cvd_swing` gated to `size_unit [1]` and the unitless twins `cvd_units` and `cvd_swing_units`, with no warning.
- `wrun-partial-tint` (added 2026-11-15, #2506): the grey `Bars with missing prints` wash covers only a bar that draws part of its data. `dark-pool-prints` and `strike-footprint` scaffold a data-only `shown_in_part` output (`1 on a bar that shows some of its prints but not all of them`) and their `render.bgcolor("served_in_part", …)` reads `where: "shown_in_part"`; `partial` keeps its meaning (since #2529 its description reads `older than the 90 days of prints it keeps or than the window's 15,000 newest`, and the template's `runsOn` ends `about 90 days back, at most 15,000 a chart window`, driven 2026-11-17). `flow-marks` and `option-prints` lose the wash (`it draws nothing, partial reads 1 and no wash covers it`). Proved on the scaffold only: the chart drawing itself belongs to the chart's own verification.
- `wrun-marks-glass-solid` (added 2026-11-16, #2509, scaffold 119, contracts 5.63.0): `plot.marks` takes `look` 5 (glass) and 6 (solid), and `look` may name a `param.choice` whose `style_values` are look words, so the sheet holds the default's word (`"look":"glass"`, the param `style_values ["glass","solid","soft_dot"]`). `text.place` 1 writes a mark's size beside it; a sheet that never names `place` keeps its bytes (no `place` key). `theme.up_mark` and `theme.down_mark` are sheet colour words for a marks section's `colors`. `theme.UP_MARK` in a draw call (`notice.set(16, 14).text(...).color(theme.UP_MARK)`) blocks the build, exit 2 `request_failed`: `src/indicator.ts:77: theme.UP_MARK names the mark colour theme.up_mark, which is a sheet colour token: write "theme.up_mark" on a sheet colour key (a marks section's colors), never in a draw call or a handle colour ...`. The message carries no `WRUN_DECL_DRAW_INVALID` code. A `handles.label({ color: "theme.up_mark" })` declaration built with exit 0 and the sheet kept the word; the chart's paint of it (and of glass, solid and the beside caption) is the chart's own verification. Recipe: `wrun create @vom/marks119 <dir> --template liquidation-bursts`, add `param.choice("look", ["Glass", "Solid", "Soft dot"], "Glass", { style_values: ["glass", "solid", "soft_dot"] });`, set the `bursts` section to `look: "@look", text: { ..., place: 1 }, colors: ["theme.down_mark", "theme.up_mark"]`, then `wrun build <dir> --format json` and read `dist/package/wrun/metadata.json`.
- `wrun-marks-text-fit` (added 2026-11-17, #2525, scaffold 120): `text.place` takes a third place, `fit` (2): the size sits inside its mark where it fits and meets no other mark, beside it otherwise, and is not drawn with no room at all. `text.place` also binds by word as `look` does: `param.choice("place", ["Fit", "Beside", "Inside"], "Fit", { style_values: ["fit", "beside", "inside"] })` with `place: "@place"` builds a sheet holding `"place":"fit"` and the param `options [0,1,2]`, `style_values ["fit","beside","inside"]`, `style_targets [["marks",0,"text","place"]]`. Refusals, exit 2 `request_failed`: `place: 3` → `<dir>/wrun/metadata.json: marks.0.text.place: text.place must be an integer from 0 to 2` at scaffold 120 (since scaffold 121, 3 and 4 build and the range reads `from 0 to 4`); a string literal `place: "middle"` → `src/indicator.ts:18: option 'place' takes a numeric literal or an "@<param>" reference, not a string` (a word goes through a param). Recipe: the `liquidation-bursts` scaffold, then edit the `bursts` section's `text` and `wrun build <dir> --format json`. Whether the chart paints a fit size inside is the chart's own verification.
- `wrun-marks-text-fit-short` (added 2026-11-18, #2546, scaffold 121, SDK 0.500.0): `text.place` takes `fit_short` (3), which writes the size rounded inside the mark (`$21M` for $20.5M) and beside it in full when even that does not fit, and `fit_only` (4), which never writes beside, so a mark too small shows no size. Both bind by index or by word through a `param.choice` with `style_values`; an older kit or chart refuses them by name. `place: 5` exits 2 `text.place must be an integer from 0 to 4`. Whether the chart paints the rounded size is the chart's own verification.
- `wrun-derived-ratio-held` (added 2026-11-22, #2653, scaffold 122): a chain read through another root's `underlying` (QQQ's chain on an NQ chart) draws at `strike * heldRatio(p_chart_derived_ratio())` once the source declares `chart.derived_ratio()`. The sheet gains a hidden param `chart_derived_ratio` with `host_fill: "derived_ratio"` and default 0. A source that reads such a chain, draws on the price pane and does not declare it still builds, with one warning: `src/indicator.ts:<line>: input '<name>' reads the QQQ chain through underlying, and nothing declares chart.derived_ratio(): declare it and draw each strike at strike * heldRatio(p_chart_derived_ratio()), drawing nothing while it reads NaN (...)`. The same source on a `lower` pane builds with no such warning. The held build also warns that a client's own chart in the page would refuse it (`it does not serve parameter.host_fill.derived_ratio`). The held ratio on a drawn chart needs a chart and OPRA data: source only.
- `wrun-input-session` (added 2026-11-22, #2655, scaffold 123, contracts 5.64.0): an input may declare `session: "extended"` to read the market's full session. Only a `candles` input with no `view`, or a `volume_profile_candles` input, and never the first input, may carry it. One prebuild pass writes `"session": "extended"` onto `inputSources.<name>` and `wrun validate <dir>` passes the sheet. `wrun validate` refuses a wrong placement by name, exit 2: `inputSources.<name>.session: wrun_input_session_invalid: source 'ohlcv' takes no session: ...`, `... the primary input (index 0) takes no session: ...`, `... a candles input read with view "forming" takes no session: ...`. `wrun build` cannot build any of these today (see Gotchas). The overnight candles on a regular-hours chart need a chart and CME data: source only.
- `wrun-index-pin-display-only` (added 2026-11-24, #2683, source only): a pin on the `INDICES_OTC` venue (an index, or a yield) plans on the chart's browser lane only; the hosted, cloud and other profiles refuse it with `wrun_pin_venue_display_only`. Needs a chart and a hosted profile to drive.
- `account-and-channel-reads` (added 2026-11-22): five signed-out reads with no guide before. `devices list --format json` answers `{devices: [], this_device_id, lines: []}`; `access packages --format json` answers `{account_id: "guest_...", scopes: [], drafts: []}`; `channel list --format json` answers `[]`; `channel home --format json` lists `discord`, `slack` and `telegram`, each `paired: false`; `app-setup status --format json` answers the desktop checklist (`account`, `agent`, `news`, `complete`). `disconnect --help` names `--revoke-badge`. Renaming or revoking a device, a grant, a paired channel and `disconnect` itself are not driven.
- `wrun-chart-default-pin` (added 2026-11-17, `ff4daf0cc2`, SDK 0.498.0): a build fails when a timeframe setting that defaults to the chart feeds candles, intrabar or a view, naming the input on its own line, instead of building a sheet that publishing would refuse. In the `sma-codefirst` scaffold, add `input("c", ohlcv.close);`, `param.timeframe("tf", "chart");` and `input("d", candles.cells, { interval: "@tf", bars: 200 });`: `wrun build` exits 2 `scaffold build blocked: code-first declaration errors` / `src/indicator.ts:8: input "d" takes its interval from the timeframe setting "tf", whose default "chart" pins none, and the sheet schema refuses that (inputSources.d.interval: wrun_candles_interval_required: ...): pin a default interval (not "chart"), or read the source without a view`. With `"1h"` it builds. Without the leading `ohlcv.close` input both forms fail on `wrun_candles_primary` instead, which is not this rule.
- `wrun-weekly-calendar-backing` (added 2026-11-14, #2503): an input that reads weekly candles (`candles.cells` with `interval: "1w"`) is refused for an `@om-core/` package by `wrun validate` (and `om publish`) with `wrun_weekly_calendar_backing`, exit 2, naming the line and the daily-candles repair. A line ending `// om-allow weekly-candles: <reason>` passes. Any other scope passes with a `warnings[]` entry in `validate`'s JSON and a row under `Warnings:` in `wrun build`.
- `wrun-build-window-warning` (added 2026-11-08, #2405, scaffold 117): `wrun
  build` warns `WRUN_DECL_INTERVAL_WINDOW_SHORT` when a window fed by an input
  pinned to a coarser interval cannot fill: a scalar pin updated once per pinned
  candle, or a `candles.cells` stream with no `bars` or `bars` short of the
  window. The warning names the input, the class and its window, and the repair.
- Local series authoring (`om series create|list|show|delete`) and the marketplace listing refusals of `om series publish --price|--stop-sales|--resume-sales|--free` (#2240), the plan table (`om upgrade --show`, `om usage plans`) and the sealed-secrets reads and doors (`GET /secrets/status`, `/secrets/devices`, `/secrets/link/pending`; `om secrets status|devices`), with the refusals of the link and reset doors.

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
- **Secrets status:** `GET /secrets/status` returns 200 `{"ok":true,"data":{"userId":"guest_…","thisDeviceId":"<12 hex>","readiness":"unminted","hasRecoveryBlob":false,"recoveryUnavailable":true,"recoveryVerified":false,"alarms":[],"presence":{"platform":"darwin","enforced":true}}}`. `thisDeviceId` is new (direct commit `4f2f7b9f45`, live 2026-11-21): it is this install's id, the same value as the home's `device-id` file, so a page can mark this computer in the device list. `om secrets status` in JSON does not carry it (live; the command prints its own fields: `userId`, `guest`, `readiness`, `hasRecoveryBlob`, `identity`, `devices`, `presence`, `recoveryVerified`, `alarms`). It is not a 401, because the lane mints its own guest key. `om secrets status --format text` prints `no identity minted yet`, `recovery: unknown (relay unreachable …)`, `check:    device owner asked before sealed actions` and `alarms:   none`.
- **Secrets devices and link (added 2026-11-14; the two devices reads re-driven 2026-11-19 at `1e71657cdd`):** `GET /secrets/devices` reads `{"ok":true,"data":{"devices":[]}}`. `om secrets devices` defaults to JSON, `{"devices":[],"unverified":false}`; `--format text` prints `Devices:  none listed` (or `Devices:  list failed its signature check · not shown` when unverified). `GET /secrets/link/pending` reads `{"state":"none"}`. Source only (they need a relay and a minted identity): since `3696de32a3` every trusted device has its own key (`ed25519+x25519`, or `p256` for a phone, `b69b7655b8`) and the signed device list carries a `version` pinned in the vault, so an older list reads `unverified`; since `10754ec203` `om secrets link` prints a QR (`om-link:v1:<code>`) above `Code:`, `On the new device: om secrets join <code>` and `Expires:` when stdout is a terminal, and only after the pairing is made, so a guest lane (no sealed keys) gets no code and the HTTP door answers 409 `link_unavailable` `this device has no sealed keys to share yet` (on macOS it may ask for Touch ID first, so skip it on a lane); since `1cbc664f47` a join request whose `deviceKey` is malformed for its `alg` fails the pairing (`link/pending` `{"state":"failed"}`, the CLI `link_failed` `The code didn't match · start again`).
- **Secrets door refusals (added 2026-11-14):** these answer before any relay call or Touch ID prompt.
  - `GET /secrets/reset` is 405 `method_not_allowed`, and `POST /secrets/link/pending` is 405.
  - `GET /secrets/nope` is 404 `unknown secrets verb: nope`.
  - `POST {}` to `/secrets/link/approve` is 400 `pairingId is required`; to `/secrets/link/join` and `/secrets/reset` it is 400 `code is required`. A non-JSON body is 400 `expected JSON body`.
  - A non-loopback `Host` header is 403 `host_not_allowed` from the daemon's own guard, so the secrets-only `secrets_local_only` 403 cannot be reached this way on a loopback lane.

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

### The held ratio and the input session (added 2026-11-22, #2653, #2655)

Needs a lane, network for the build's `bun install`, no chart and no model.

1. `control-om om -- wrun create @you/rec123 <dir> --template sma-codefirst --format json`. `<dir>/.wrun-scaffold` reads `{"scaffold_version": 123}`.
2. Held ratio. Replace `<dir>/src/indicator.ts` with the `HELD_SOURCE` lines of `packages/cli/test/wrun-derived-ratio-held.test.ts` (two inputs, `chart.derived_ratio();`, an overlay line, one mark). `wrun build <dir> --format json` exits 0, and `<dir>/wrun/metadata.json` `params[0]` is `chart_derived_ratio` with `host_fill: "derived_ratio"`, `hidden: true`, `default: 0`.
3. Old placement. Use `OLD_SOURCE` from the same test (`derivedRatio(bar.close(), rows[7])`, no declaration). The build exits 0 and `warnings` holds the `nothing declares chart.derived_ratio()` line. Change `overlay` to `lower` and the line is gone.
4. Session, one pass at a time. Write
   `input("close", ohlcv.close);` and
   `input("night", candles.cells, { interval: "1m", bars: 10, session: "extended", max_cells: 1000 });`
   with a lower line output that writes `f64(in_night_cells())`. From `<dir>`, `node scripts/wrun-prebuild.mjs` exits 0 and `inputSources.night` holds `"session": "extended"`. `wrun validate <dir> --format json` exits 0.
5. Wrong placements. Remove `session` from every `inputSources` entry of `wrun/metadata.json` first. Then move the word to the first input, to a second `ohlcv` input, or add `view: "forming"` to the candles input, run the prebuild once and `wrun validate <dir> --format json`: exit 2 with the `wrun_input_session_invalid` sentence for that placement.
6. The defect. With the step 4 source, run `node scripts/wrun-prebuild.mjs` a second time, or `wrun build <dir>`: `scaffold build blocked: code-first declaration errors`, `wrun/metadata.json carries a field the param(...)/input(...)/output(...) declarations cannot express: inputSources.night.session`.

### The size-unit word guard (added 2026-11-10)

Proves #2430 on a guest lane. No model and no account; the first build runs
`bun install` in the workspace, so it needs the network.

- **Scaffold.** `control-om om -- wrun create @vom/cvd-probe <dir> --template cvd-divergence`.
  Its `metricIds` list `cvd`, `cvd_units`, `cvd_swing` and `cvd_swing_units`.
  `control-om om -- wrun build <dir>` exits 0 with no `coins` line in
  `warnings`.
- **Warn.** In `<dir>/src/indicator.ts`, delete `, visible_by: { size_unit: [1] }`
  from the `output("cvd", …)` line. `wrun build <dir>` and `wrun validate <dir>`
  both exit 0, and `warnings` holds `output 'cvd' prints " coins" on every
  market, but only a size_unit 1 market counts in coins: …`.
- **Refuse.** Rename the package to `@om-core/cvd-probe` in `om-package.json`
  and `package.json`. `wrun validate <dir>` exits 2 with
  `{"error":"wrun_size_unit_word","message":"@om-core/cvd-probe: a unit prints a size word on markets that count in another unit: …"}`
  and a hint naming `visible_by: { size_unit: [code] }` (1 coins, 2 shares,
  3 contracts) and the `// om-allow size-unit: <reason>` opt-out.
- **Proof.** Keep the three JSON results. The opt-out comment and `om publish`
  are not driven.

### Guest-lane reads (added 2026-10-28)

All were driven on a fresh guest lane at `a8fa10974`. Each answers or refuses
with no account:

| Call | Observed |
|---|---|
| `approvals list` / `--format json` | `No pending approvals.` / `[]`; `GET /rpc/v1/approvals` returned `{"ok":true,"data":{"approvals":[]}}` |
| `approvals list --kind draft` / `--kind bogus` (#2258: one inbox of kinds `chain`, `mcp`, `grant`, `draft`, `proposal`, and since #2450 `repo`; see [approvals-ledger.md](./approvals-ledger.md)) | `No pending approvals.` / exit 2 `--kind must be one of: chain \| mcp \| grant \| draft \| proposal \| repo` (2026-11-15); `GET /rpc/v1/approvals/inbox` returned `{"items":[],"counts":{"total":0,"byKind":{…all 0}}}` |
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

### Projects off, against a loopback relay stub (added 2026-11-15, #2500)

The same stub shape proves the refusal on a server where Projects is off. Answer every path containing `todo` with `409` and `{"tag":"TODO_RECORDS_OFF","code":"TODO_RECORDS_OFF","error":"<message>"}`, then:

```bash
control-om om -- todo list --space vom-space --url http://127.0.0.1:<stub-port> --format json
control-om om -- todo create x --room general --url http://127.0.0.1:<stub-port> --format json
```

- Each exits 1 with `error: todo_records_off`, the relay's own message, `details.status` and the hint `Projects is off for this server; its owner switches it on in Server Settings → Projects.` The text form prints the message, then the hint.
- Before #2500 the hint pointed at the legacy board tool (`room_todo_board`), which is gone from every surface, MCP included.
- The stub sees `GET /todos?spaceId=<space>` for the list and `POST /todos` for the create.

## Gotchas

- `om usage plans` is not a Data API read. It reports MODEL provider plan holds.
  See [market data reads](./market-data-reads.md).
- **`wrun build` with no `--format` prints JSON when stdout is not a terminal**
  (the shared `--format` default follows the output: text for a person, JSON
  for a pipe). A driver that captures output and wants the `Warnings:` block
  passes `--format text`.
- **`wrun build` refuses a code-first `session: "extended"` input (seen 2026-11-22 on `01482928a5`, #2655; still on `26d502c689` 2026-11-24).** The build script runs the prebuild twice, once by itself and once as the compiler's transform. The first pass writes `session` onto the sheet. The second pass reads that sheet back and answers `wrun/metadata.json carries a field the param(...)/input(...)/output(...) declarations cannot express: inputSources.<name>.session`, exit 2 `request_failed`. A wrong placement fails the same way, so `wrun build` never shows `wrun_input_session_invalid`; `wrun validate` after one prebuild pass does. A sheet left with `session` blocks every later build of that workspace, whatever the source says, until the field is deleted from `wrun/metadata.json`. `packages/cli/test/wrun-kit-registration.test.ts` runs the prebuild once, which is why it passes. Reported as a product gap in README.md.
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
  `WRUN_SCAFFOLD_VERSION` is 123 since #2655
  (`packages/sdk/src/wrun-sdk-sources.ts:1378`; 122 at #2653, 121 at #2546, 120 at #2525, 119 at #2509, 118 at #2407, 117 at #2405, 116 at #2379, 108 at #2239, 109 at #2245, 110 at #2246, 111 at #2267, 112 at #2273, 113 at #2283, 114 at #2336, 115 at #2339). #2379 also added the `dark-pool-prints` template (93 in all), whose workspace carries the `dark_pool` input and `plot.flags`.** The template sits in group `Order flow`
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
