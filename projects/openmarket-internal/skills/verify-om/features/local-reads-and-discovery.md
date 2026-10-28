# Local reads and discovery

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
- `notis`: the daemon's own notification history (watch fires, arrivals, notices).
- `enum-list` / `enum-domain`: the enum domain index, and a paged, searchable
  domain.
- `schema-read`: the intents an agent can ask the schema door for.
- `skill-list`: the bundled skill files.
- `wrun-list` / `wrun-templates`: installed indicator packages and scaffold
  templates.
- Local series authoring (`om series create|list|show`), the plan table (`om upgrade --show`, `om usage plans`) and the sealed-secrets status read (`GET /secrets/status`).

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
  - `series create s1 --watch <watch> --key v --scope local --format json` creates `@local/s1` with version 0.1.0 and `rows: 0`. `list` and `show` then read it back.
  - `series publish s1 --dry-run` exits 2 with `publish_rejected`: "the registry refused the pack: kind 'live-series' is not accepted by the v1 registry". So the dry run does reach the registry, using the lane's guest key.
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
  (`f8b2ca3b4`).** Their `runsOn` reads "US stocks (OPRA) at your own tier;
  CME futures through OpenMarket's official package", where it used to say
  both went through the official package. Driven 2026-10-28 at `186030b63`:
  91 templates, 83 `Runs on:` lines, 30 with "at your own tier" (the commit's
  thirty sentences) and none with the old "US stocks (OPRA) and CME futures
  through" wording. A JSON assertion that reads only `description` misses
  this field.
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
