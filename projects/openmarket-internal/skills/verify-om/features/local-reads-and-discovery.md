# Local reads and discovery

*Verified: 2026-10-23, tree `42d044b02` (origin/main, v0.462.0): on a guest lane, `config show --format json` returned `api_key_masked`, `api_key_set`, `api_key_source`, `channels`, `default_channel` and the telemetry flags; `config key-info --format json` returned `tier: om_guest`, an `expires_at` about an hour out and `expired: false`; `config get data.transport` returned `value: null`, `source: default`, `default: auto` and the accepted values; `notis --since 7d --json` returned `rows[]` holding a `notice` for `calendar-probe`; `enum --list` returned `domains[]` (`exchange_id` with 35 values); `enum --domain exchange_id --query BIN --limit 3` returned a page with `total`, `offset`, `limit` and `next_offset`; `schema read` returned `intents[]`; `skill list` printed `openmarket`, `openmarket-watch`, ...; `wrun list` returned the embedded `@om-core/*` packages and `wrun templates` their templates. Not driven: `config set`, `notis --after` paging, `schema read <intent>`, `skill show`, `wrun create`/`build`, and `vault status`.*

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

## Gotchas

- `om usage plans` is not a Data API read. It reports MODEL provider plan holds.
  See [market data reads](./market-data-reads.md).
- `wrun build` compiles and runs `bun install` by default, so it needs the package
  registry. Keep it out of a quick pass.
- `hl_dex` is a dynamic enum domain listed live from the venue. It needs network
  where the static domains do not.
- Per source (`cmd/notis.ts`; not driven), `notis` exits 1 on a runtime error
  and 2 on invalid input, like the other action-backed verbs.
