# Registry welcome page and personalised search

*Re-driven 2026-11-01 (nightly), tree `7ce379c45` (origin/main, v0.480.3), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 2.9. Real registry only: `welcome` exit 1 `This registry does not offer the welcome page yet.`; `search rsi --format json` returned `{results, total: 42}` led by `@om-core/autocorrelation`, with no `hidden` key (no retired row was dropped); `search rsi --kind wrun-indicator --limit 3` three rows. New for #2234: `search rsi --kind kscript-indicator` and `search demo --kind kscript-library` exit 2 `kind_retired` with no request sent (see [kScript retirement](./kscript-retirement.md)). `terms --format json` exited 1 `registry_unreachable` twice (`https://registry-staging.openmarket.xyz/v1/me: The operation timed out.`), while search, welcome and `om open` answered within a second: the staging registry the terms door reads was unreachable from this host tonight. The fixture branches were not re-driven. Evidence: `http://127.0.0.1:8098/vom-nightly-20261101/r1/` (`cli/32-35b`, `cli/60`, `cli/13*`).*

*Re-driven 2026-10-31 (nightly), tree `dfefe0a21` (origin/main, v0.480.2), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 1.6. Real registry only: `welcome` exit 1 `This registry does not offer the welcome page yet.`; `search rsi --format json` led with `@om-core/autocorrelation`. The fixture branches were not re-driven. Evidence: `http://127.0.0.1:8098/vom-nightly-20261031/r1/` (`cli/76-77`).*

*Re-driven 2026-10-30 (scheduled maintenance), tree `3cb50a821` (origin/main, v0.478.0), fresh lane on 18165, host load average about 140. Real registry only: `welcome` printed "This registry does not offer the welcome page yet."; `search rsi --format json` returned results led by `@om-core/autocorrelation`. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261030/r1/`.*
*Re-driven 2026-10-30 (nightly, real registry only), tree `3cb50a821` (origin/main, v0.478.0), lane on 18163: `welcome` printed `This registry does not offer the welcome page yet.` and exited 1. It takes no `--format` (`unknown option '--format'`). The fixture branches and `search` were not re-driven. Evidence is local only (the `8098` renderer did not answer): `artifacts/vom-nightly-20261030/r1/`.*

*Re-driven 2026-10-29 (scheduled maintenance, smoke depth), tree `7ec575e55` (origin/main, v0.467.0 plus #2194), fresh lane on 18161. `search btc` returned registry `results[]`, and `welcome` still says "This registry does not offer the welcome page yet." (exit 1). Evidence: `http://127.0.0.1:8098/verify-om-maint-20261029/r1/`.*

*Re-driven 2026-10-29 (nightly, smoke depth), tree `32ca0d6c7` (origin/main, v0.467.0), lane on 18103 against the production registry: `welcome` still printed `This registry does not offer the welcome page yet.`, and `search "funding rate" --format json` returned `{results, total}` with no `reasons`. The fixture branches were not re-driven. Evidence: `http://127.0.0.1:8098/vom-nightly-20261029/r1/`.*

*Re-driven 2026-10-28 (scheduled maintenance, smoke depth), tree `186030b63` (origin/main): `welcome` still refused (`This registry does not offer the welcome page yet.`, exit 1), and `search "btc funding"` returned 3 rows. Steps not named here keep the record below. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261028/r1/`.*

*Verified: 2026-10-28, tree `a8fa10974` (origin/main, v0.466.0), lane on 18103. Against the real registry, `om welcome` still printed `This registry does not offer the welcome page yet.` (exit 1), and `search "btc funding"` returned rows of `name`, `kind`, `description` and `latest`, with no `served`. Against a loopback fixture on 18112, all three welcome branches matched: the guest `om login` hint (exit 1), the keyed `…/welcome?src=om-init` line (exit 0), and `does not offer` once `welcome` was dropped from health (exit 1). Search sent `mode=nl` with no bearer as a guest, and `mode=nl&rank=for-you` with a bearer when keyed. The rows carried `reasons` and `served:"jev"`. Not driven: receipt retraction and `om init --launch`. Previous stamp `8fe6a8432` is an ancestor (10 commits).*

A signed-in user can open a registry page that personalises their watch feed:
`om welcome`, or the last step of `om init`. A user searching the registry gets
plain-language results, and with an account the results are ranked for them.
Both features ask the registry's `/v1/health` what it serves first. Where it
offers neither, the request is the one older builds sent, and the user sees
the old behavior.

## Sub-features

- `welcome-gate`: `om welcome` refuses with `This registry does not offer the
  welcome page yet.` (exit 1) unless health says `welcome: true`. This gate runs
  before the account check.
- `welcome-account`: on a registry that serves the page, a guest or signed-out
  home gets the `om login` hint (exit 1). An account opens
  `<registry>/welcome?src=om-init`, or prints it when headless.
- `init-closing`: `om init` ends with "Personalise your watch feed now?" for an
  account on a serving registry. `--launch welcome|agent|dashboard|nothing`
  answers that question for a script.
- `search-nl`: when health lists `search_modes: ["nl"]`, `om search <words>`
  adds `mode=nl`, and results carry `reasons` (up to two per hit), `served` and
  `class`.
- `search-for-you`: when health also lists `rank_modes: ["for-you"]` and the
  home holds an account key, the request adds `rank=for-you` with a bearer. A
  guest never sends a bearer.

## How to get to it (user POV)

- `om welcome`, or the last step of `om init`.
- `om search "<words>"`, unchanged on the surface: no new flags.

## Driving it with control-om

Preconditions: a lane the run started. The success branches need a registry
that advertises the features. On 2026-10-26 the production registry did not,
so they are driven against a loopback fixture on an assigned agent port
(`18112`). `control-om om --` passes the caller's environment through, so
`OM_REGISTRY_URL`, `OM_API_KEY` and `OM_NO_BROWSER` reach the CLI process.

- **The real registry.** `control-om om -- welcome`: record the refusal it
  gives, `does not offer` or `needs an account`, because that depends on what
  production advertises that day. `control-om om -- search "btc funding"
  --format json`: assert `results[]` with `name`, `kind`, `description` and
  `latest`, and note whether `served` appears.
- **The fixture.** A Bun server answering `GET /v1/health` from a
  `health.json` you edit between calls, and `GET /v1/search` with
  `packages/contracts/fixtures/wire/search-page-nl.json` from the product tree.
  Log each request's path, query and whether it carried `Authorization`. That
  log is the proof of what the CLI sent.
- **Welcome, three branches.** Use health `{"ok":true,"welcome":true}`, then
  `OM_REGISTRY_URL=http://127.0.0.1:18112 control-om om -- welcome`: the
  `om login` hint, exit 1. Add `OM_API_KEY=sk-test OM_NO_BROWSER=1`: exit 0 and
  the `…/welcome?src=om-init` line. Change health to `{"ok":true}` and run the
  same keyed call: `does not offer`, exit 1. That shows the gate comes first.
- **Search.** Use health
  `{"ok":true,"search_modes":["nl"],"rank_modes":["for-you"]}`. As a guest,
  `… search "btc dip" --format json` returns rows with `reasons`, and the log
  shows `mode=nl` with no bearer. With `OM_API_KEY=sk-test`, the log shows
  `mode=nl&rank=for-you` and a bearer.
- **Proof.** Keep the fixture's request log, each command's output and its
  exit code.

## Gotchas

- `OM_API_KEY=sk-test` is not a real key. It only makes the CLI treat the home
  as an account, because an env key's source is `env`, not the stored guest.
  Never send it to the real registry: keep it on calls that also set
  `OM_REGISTRY_URL` to the fixture.
- `om init` cannot be driven here: it exits 2 without a TTY
  (`'om init' requires an interactive terminal.`), and it writes channel,
  credential and service state. Its closing step stays source-only.
- Piped, `om search` prints JSON even without `--format json`. To see the text
  renderer, give it a TTY: `script -q /dev/null control-om om -- search "btc
  dip"`. Driven 2026-10-27 against the fixture, it printed
  `@acme/signal@1.0.0  [watch-pack]  (20 USDC / month)  BTC dip signal: ...`,
  then two indented reasons lines and `1 of 1`.
- **Receipt retraction is the third part of #1947 and is not here.** An
  uninstall or unfollow queues a DELETE to the registry in
  `<home>/receipts/retractions.json` only for an account whose install or
  follow receipt returned an `edge`. A guest never retracts, so the feature stays
  `live verification pending` in the inventory.
- The `Welcome to OpenMarket` block on the dashboard Overview is the
  onboarding checklist ([the ops dashboard](./ops-dashboard.md)), unrelated to
  `om welcome`.
- **A default `search` drops retired kScript rows and counts them.** Since
  #2234 (`4f4903ab9`) a registry row whose `kind` is `kscript-indicator` or
  `kscript-library` is left out; `--format json` carries `hidden: N` only when
  N is above 0 (`cmd/search.ts:129`), and the text form then ends `N shown (K
  retired kScript package(s) left out)`. `--kind kscript-indicator` is refused
  `kind_retired` before any request. `hidden > 0` is source-only: production
  returned no retired row for `rsi` on 2026-11-01. See
  [kScript retirement](./kscript-retirement.md).
- `om terms` reads the registry's terms door, which resolved to
  `registry-staging.openmarket.xyz` on this checkout and timed out
  (`registry_unreachable`, exit 1) on 2026-11-01 while `search` and `welcome`
  answered. Treat a `terms` timeout as the staging registry, not the verb,
  until `search` fails too.
