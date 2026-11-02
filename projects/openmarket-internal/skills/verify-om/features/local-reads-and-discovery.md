# Local reads and discovery

*Re-driven 2026-11-02 (scheduled maintenance), tree `587ce2d0b` (origin/main, v0.480.3), lane on 18168 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 5. `config show` (`api_key_set:true`, masked), `config key-info` (`tier om_guest`), `config get data.transport` (`default auto`), `enum --list` (`exchange_id` 35), `schema read`, `wrun list`, `series list` `{"series":[]}`, `upgrade --show`, `config set agent.max_tool_calls 250` exit 2 (`at most 249`), `subscriptions` exit 1 `account_required`, `setup default`, `approvals list`, `notis --since 7d --json`, `GET /secrets/status` `readiness:"unminted"`. Series: `series create s1 --watch lane-lifecycle --key v --scope local` → `@local/s1` 0.1.0; `publish s1 --price 9/mo --dry-run` → `seller_session_required`; `--price 1/mo` → `price_below_minimum`; `delete s1 --yes` → `relay:"missing"` (a `publish` before `create` answers `series_not_found`). **wrun at scaffold 110:** `wrun templates` lists `liquidation-map`; `wrun create @lane/liq --template liquidation-map <dir>` wrote `.wrun-scaffold` `scaffold_version: 110`. `config get chat.icons` / `set` / refusal: see [chat-tui-icons.md](./chat-tui-icons.md).*

*Re-driven 2026-11-02 (nightly), tree `2567b7974` (origin/main, v0.480.3), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 4. Before the boot (daemon down, keyless home): `enum --list`, `enum --domain indicator_template` (92), `wrun templates` (92; the text form has 84 `Runs on:` lines, 31 reading `CME futures in your browser`, none reading `through OpenMarket`), `wrun create @lane/option-prints --template option-prints` and `@lane/flow-vwap --template flow-vwap` (`.wrun-scaffold` `{"scaffold_version": 108}`, `src/sdk/declare.ts` and `scripts/wrun-prebuild.mjs` written, the prebuild carrying `visible_by`, `needed_by` and `min_coins`), `skill list`, `skill show indicators` (`min_coins`, `two or none`), `skill show watch` (`watch_state_clear` drops the anchor, `record_restarts`), `config show` (`api_key_set: false`), `setup default`, `upgrade --show`, `schema read` and `schema read condition_create`, `chart indicator schema rsi`. After the boot: `config show` (masked key), `key-info` (`om_guest`, a one-hour expiry), `get data.transport`, `set agent.max_tool_calls 250` exit 2, `get chat.sounds` `unset (default: on)`, `set chat.sounds maybe` exit 2; `notis --since 7d --json` (a `notice` row for `calendar-probe`); `approvals list` `[]`; `setup default nope --force` `channel_not_found`; `nervous status` (`watch_fired` receipt, `unresolved_subject`); `follows` `[]` and `follows show` `not_following`; both `relay trace` refusals; `research study --locate-only` (one occurrence for the door's `event_id`) and `--watch nope` exit 2; `/api/away` 401 `operator_required`; `/secrets/status` 200 `unminted`; `/openapi.json` 137 paths; `vault status` `mode: none`; `usage plans` `providers: []`; `subscriptions` `account_required`; `unsubscribe nope` `confirmation_required`; `wrun list` (`@om-core/accumulate` 0.1.3); `terms` answered from the staging registry (version `2026-09-10`) in 0.5 s. **Series (#2240, #2241):** `series list` `[]`; `create s1 --watch demo --key v --scope local` (`@local/s1` 0.1.0, `rows: 0`); `show --format json` carries `visibility: "public"`, `relay: null`, `relay_refusal: "feed_not_found"`, and the text form prints `Visibility: public` and `Feed: not on the relay yet`; `list --format text` prints the row with no `listed:` marker. The new publish flags refuse locally on a guest: `--price 9/mo --dry-run` → `seller_session_required` ("Selling a feed needs a sign-in session; this home signs in with a login key", hint `OM_LOGIN_LANE=session om login`), `--price 1/mo` → `price_below_minimum` ($2.50 floor), `--price abc` → `invalid_price`, `--stop-sales --yes` → `listing_free`, `--stop-sales --free` → `invalid_options` ("cannot ride one call"), `--price 9/mo` without `--yes` → `confirmation_required`, `--free --yes` → `seller_session_required`. A plain `--dry-run` reached the registry and got `registry_unavailable` (503, "could not confirm this account's username") tonight, not the `publish_rejected` of earlier passes. `series delete s1 --yes` returned `relay: "missing"` and the removed directory. Evidence: `http://127.0.0.1:8098/vom-nightly-20261102/r1/` (`cli/01-15`, `cli/50-65`, `cli/128-153`).*

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
  `CONFIG_KEYS` (`packages/cli/src/cmd/config-keys.ts:160`, rendered into
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

### Guest-lane reads (added 2026-10-28)

All were driven on a fresh guest lane at `a8fa10974`. Each answers or refuses
with no account:

| Call | Observed |
|---|---|
| `approvals list` / `--format json` | `No pending approvals.` / `[]`; `GET /rpc/v1/approvals` returned `{"ok":true,"data":{"approvals":[]}}` |
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
not drive `approvals approve|deny`, `follow review`, `research search-files` or
`research make-image` from a lane: they need a human terminal or spend on a
model.

## Gotchas

- `om usage plans` is not a Data API read. It reports MODEL provider plan holds.
  See [market data reads](./market-data-reads.md).
- `wrun build` compiles and runs `bun install` by default, so it needs the package
  registry. Keep it out of a quick pass.
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
  `WRUN_SCAFFOLD_VERSION` is 110 since #2246 (`5cf89fe95`;
  `packages/sdk/src/wrun-sdk-sources.ts:1204`; 108 at #2239, 109 at #2245).** The template sits in group `Order flow`
  (the chart's price weighted by aggressive options premium, with sigma
  bands). **`wrun create` takes the package name first:** `wrun create
  @you/<name> --template flow-vwap <dir>`; a bare directory is refused
  "package name must look like @scope/short-name". A fresh create writes
  `.wrun-scaffold` `{"scaffold_version": 108}`, an `indicator.ts` whose
  `options_flow` inputs carry the `underlying` knob (`"@chain"`, a select
  of `auto`, `derived`, `QQQ`, `NDX`, `SPY`, `SPX`), and a `src/sdk/declare.ts`
  and `scripts/wrun-prebuild.mjs` that carry the keyed-row words
  (`visible_by`, `needed_by`, `min_coins`). A scaffold-106 or 107 workspace
  refreshes only those two files on its next build. Drive the create into a
  directory outside the product tree, and assert membership, not the count
  (driven 2026-11-01 at 107, 2026-11-02 at 108).
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
