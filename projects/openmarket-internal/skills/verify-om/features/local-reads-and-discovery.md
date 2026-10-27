# Local reads and discovery

*Verified: 2026-10-27, tree `8fe6a8432` (origin/main, v0.466.0), lane on 18103: `config show` (`api_key_set`, a masked key), `config key-info` (`om_guest`, not expired) and `config get data.transport` (`source default`, `default auto`). `notis --since 7d` returned `fire` and `notice` rows. `enum --list` returned 26 domains, `enum --domain exchange_id --query BIN --limit 3` returned `total 3`, `schema read` returned 7 intents and `skill list` printed the bundled skills. `wrun list` returned `{packages, skipped}`, and **`wrun templates` returned 91, down from 97**: `5a03ffb43` removed six option recipes. Not driven: `config set`, `notis --after`, `schema read <intent>`, `skill show`, `wrun create`/`build` and `vault status`. Previous stamp `ee8e3a7ab` is an ancestor of this tree (15 commits).*

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

## Gotchas

- `om usage plans` is not a Data API read. It reports MODEL provider plan holds.
  See [market data reads](./market-data-reads.md).
- `wrun build` compiles and runs `bun install` by default, so it needs the package
  registry. Keep it out of a quick pass.
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
