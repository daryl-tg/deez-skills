# Firecrawl recovery before whitelist

*Re-driven 2026-11-05 (nightly), tree `3a0ea623e` (origin/main, v0.492.0), guest lane on 18163 inside the origin-challenge hold (stub on 18166), no key: `OM_FEED_ALLOW_LOOPBACK=1 … watch page-add http://127.0.0.1:18166/article/1` exit 2 `page_bot_wall_suspected` (`… 127.0.0.1 is challenging this machine; next try 2026-11-04T19:50:23.125Z (HTTP 403).`, hint `Run \`om setup firecrawl\``), one `challenge GET /article/1`; the feed's FAULT row ended `· Firecrawl can read it for you` with `FIX om setup firecrawl`; `config get firecrawl.offers` `unset (default: on)`. Not re-driven: the fixture-key lane (offer pause, `--deny`), the configured path. Evidence: `http://127.0.0.1:8098/vom-nightly-20261105/r1/` (`cli/firecrawl-nokey.out`, `cli/origin-hold-show.txt`).*

*Re-driven 2026-11-04 (nightly), tree `9acb5fb56` (origin/main, v0.491.0). No key, on the guest lane 18163 inside the origin-challenge hold (stub on 18166): `OM_FEED_ALLOW_LOOPBACK=1 … watch page-add http://127.0.0.1:18166/article/1` exit 2 `page_bot_wall_suspected` (`… 127.0.0.1 is challenging this machine; next try 19:46:54Z (HTTP 403)`, hint `Run \`om setup firecrawl\``), one `challenge GET /article/1`, its own clock against the feed's 19:45:27Z; the feed's FAULT row ended `· Firecrawl can read it for you` with `FIX om setup firecrawl`. Pausing the offers, on main for the first time, on a second lane 18165 booted with `--env OM_FIRECRAWL_API_KEY=<fixture>` (never sent): the drain row `ok`; `config set firecrawl.offers off` → 70 s later `inactive`, `offers paused`; `on` → `ok`, with no `[firecrawl-offer]` line in the lane log; `setup firecrawl --deny 127.0.0.1 --format json` `declined:["127.0.0.1"]`; `firecrawl.offers maybe` exit 2. On 18163 (no key) the row read `no Firecrawl key` while off. Not driven: the configured read path, the seeded offer, the card, the exhausted-credits hold. Evidence: `http://127.0.0.1:8098/vom-nightly-20261104/r1/` (`cli/100-106`, `cli/232`, `cli/260-264`).*

*Re-driven 2026-11-03 (nightly), tree `777ee7f21` (origin/main, v0.488.0), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 2.8; the first `up` died on a guest sign-in 429 (35 minutes) and the lane booted in 3 s at 19:55Z. No key, inside the hold: `OM_FEED_ALLOW_LOOPBACK=1 … watch page-add http://127.0.0.1:18166/article/1` exit 2 `page_bot_wall_suspected` (`… 127.0.0.1 is challenging this machine; next try 20:15:27Z (HTTP 403)`, hint `Run \`om setup firecrawl\``): the probe made one `challenge GET /article/1` and runs its own clock (20:15 against the feed's 20:12). The feed's status row read `Firecrawl can read it for you`. The configured path was not driven. Evidence: `http://127.0.0.1:8098/vom-nightly-20261103/r1/` (`cli/203`, `cli/202`).*

*Re-driven 2026-11-02, branch `daryl/firecrawl-offer-pause` tree `d26f65d8f` (on origin/main `760571859`, v0.487.0), lane on 18105 from source with `--env OM_FIRECRAWL_API_KEY=<fixture>` (never sent: the drain only checks a key resolves). Pause path only, see "Pausing the offers" below: `config set firecrawl.offers off` read back on `/healthz` `.loops[firecrawl-offers]` as `inactive`, reason `offers paused`, one pass (60 s) later; a refusing host seeded during the pause raised no card; `config set firecrawl.offers on` and the next pass raised it (`[firecrawl-offer] probe-a.example.test: no answer`, the guest lane's expected settlement). `setup firecrawl --deny 127.0.0.1 --format json` answered `declined: ["127.0.0.1"]`. The CLI door needs `OM_LANE_PORT=18105` on a non-default lane port or it writes a fresh `home-18101`. Evidence: `http://127.0.0.1:8098/firecrawl-offer-pause-20261102/r1/`.*

*Re-driven 2026-11-02 (scheduled maintenance), tree `587ce2d0b` (origin/main, v0.480.3), lane on 18168 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 5. No-key path inside the hold above. `watch page-add http://127.0.0.1:18169/article/2` while the stub answered challenge → exit 2 `page_bot_wall_suspected` (`127.0.0.1 is challenging this machine; next try …`, hint `om setup firecrawl`), with its own `next try` (03:19 against the feed's 03:14). **With the stub back on `ok`, `page-add …/article/1` inside the same feed hold answered `llm_not_configured`** ("a page watch needs one for its setup read"): the page probe is not held by the feed's cooldown, so the article itself must be challenged at the moment of the call.*

*Re-driven 2026-11-02 (nightly), tree `2567b7974` (origin/main, v0.480.3), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 4. No-key path only, inside the hold above: `watch page-add http://127.0.0.1:18166/article/1 --format json` exit 2 `page_bot_wall_suspected` ("127.0.0.1 is challenging this machine; next try 2026-11-01T20:04:38Z (HTTP 403)", hint `Run om setup firecrawl to retry public pages this machine cannot read`); the probe itself reached the stub (`challenge GET /article/1`) and its `next try` ran from that probe, not from the feed's hold. The feed source's `Status` row and the dashboard detail carried `Firecrawl can read it for you`. The configured path is still pending. Evidence: `http://127.0.0.1:8098/vom-nightly-20261102/r1/` (`cli/223-page-add-article-hold`, `cli/224-watch-show-hold-text`, `watch-detail-feed-hold.png`).*

*Re-driven 2026-11-01 (nightly), tree `7ce379c45` (origin/main, v0.480.3), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 2.9. No-key path only, inside the origin-challenge hold (stub on 18166, see [origin challenge](./origin-challenge-backoff.md)). `watch show ui-authored-feed` carried the source row `waiting · 127.0.0.1 is challenging this machine since … · next try … · Firecrawl can read it for you`, and the dashboard detail page showed the same sentence. `OM_FEED_ALLOW_LOOPBACK=1 … watch page-add http://127.0.0.1:18166/article/1 --format json` exited 2 `page_bot_wall_suspected` (`… cannot be watched: 127.0.0.1 is challenging this machine; next try … (HTTP 403).`) with the hint `Run om setup firecrawl to retry public pages this machine cannot read.`, and the stub logged one `challenge GET /article/1`. The configured path is still pending. Evidence: `http://127.0.0.1:8098/vom-nightly-20261101/r1/` (`cli/A3-*`, `cli/A4-firecrawl-nokey-page-add.txt`, `dash-alerts-ui-feed-hold*`).*

*Re-driven 2026-10-30 (scheduled maintenance), tree `3cb50a821` (origin/main, v0.478.0), fresh lane on 18165, host load average about 140. No-key path only, inside the origin-challenge hold (stub on 18166). `watch show` carried `… · Firecrawl can read it for you` with `FIX om setup firecrawl`. A second `watch page-add http://127.0.0.1:18166/article/1` exited 2 with `error: page_bot_wall_suspected` (not `page_origin_cooldown`): the CLI probe hit the origin afresh, got the challenge, and the hint read "Run `om setup firecrawl` to retry public pages this machine cannot read." The configured path is still pending. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261030/r1/` (`cli/41-page-add-held.json`).*
*Verified: 2026-10-29 (nightly), tree `32ca0d6c7` (origin/main, v0.467.0), no-key path only, lane on 18104, a challenged stub on 18112. During the hold on a `page-add` feed, `watch show` carried `… · Firecrawl can read it for you` with `FIX om setup firecrawl`, and `--format json` `.status.source.fix` was `{label: "Firecrawl can read it for you", command: "om setup firecrawl"}`. The dashboard detail showed the same sentence. The `page_origin_cooldown` refusal on a second `page-add` was not re-driven, and the configured path is still pending. Evidence: `http://127.0.0.1:8098/vom-nightly-20261029/r1/`.*

*Verified: 2026-10-28, tree `a8fa10974` (origin/main, v0.466.0), no-key path only, lane on 18104 with `OM_FEED_ALLOW_LOOPBACK=1`, a challenged stub on 18124 and no Firecrawl key in the environment. `watch page-add http://127.0.0.1:18124/rss --prefer feed --every 60s` exited 2 with `page_origin_cooldown` (`127.0.0.1 is challenging this machine; next try …`) and the hint `Run om setup firecrawl to retry public pages this machine cannot read.`, with no `--allow`. The stub logged one `challenge GET /rss`. The configured path (fixture key plus vendor redirect) was not driven. Previous stamp `8fe6a8432` is an ancestor (10 commits).*

A configured Firecrawl connection retries the first eligible direct-read failure or refusal automatically. A later refusal asks to allow that site. A home without a Firecrawl key continues to offer setup. The first recovery does not grant standing access to the site.

## Sub-features

- An eligible direct read can recover after one automatic vendor retry, without a whitelist prompt.
- Repeated refusal makes the site eligible for the existing whitelist offer; paid fetch count stays at one.
- Restarting the daemon preserves the retry history and the site's refusal status.
- A missing key offers `om setup firecrawl`. A configured key after repeated refusal makes the row read `Firecrawl can read it if you allow it`, with the fix label `allow Firecrawl to read <host>` (`status-sentence.ts:2562`). The command it points at is still `om setup firecrawl`; the explicit `om setup firecrawl --allow <host>` appears in the `page-add` CLI hint.
- Existing allowed sites continue to use their standing Firecrawl permission.

## How to get to it (user POV)

1. Connect Firecrawl with `om setup firecrawl`.
2. Watch a public page or feed whose origin challenges this machine.
3. The first eligible direct-read failure retries automatically. If a later read is refused, the source status says `Firecrawl can read it if you allow it`.
4. Allow that site with `om setup firecrawl --allow <host>` when continued reading is wanted.
5. Without a key, the blocked read still points to `om setup firecrawl`.

## Driving it with control-om

Use a fresh, run-owned guest lane. The proved rig uses assigned ports 18121 (daemon), 18122 (origin) and 18123 (vendor response fixture), all bound to loopback. Keep the operator daemon on 31337 untouched.

1. Serve a one-item RSS feed at `http://127.0.0.1:18122/rss`. In challenge mode return HTTP 403 with `cf-mitigated: challenge`; in healthy mode return the feed. Record every request and timestamp.
2. Use a verification-only fetch preload that redirects only `https://api.firecrawl.dev/v2/scrape` to the loopback fixture. Require the isolated lane's `OM_HOME`, strip authorization, and return the production response shape: `{"success":true,"data":{"rawHtml":"<rss>...</rss>","metadata":{"statusCode":200}}}`. Supply a fixture key through the environment, never a real key.
3. With the origin challenged, run the source CLI under the same guarded preload: `OM_LANE_PORT=18121 OM_FEED_ALLOW_LOOPBACK=1 OM_FIRECRAWL_API_KEY=<fixture-only> control-om om -- watch page-add http://127.0.0.1:18122/rss --prefer feed --silent --every 60s --format json`. Expect exit 0 and `feed_created`. The vendor request log contains exactly one scrape and the allowlist is empty.
4. Set the origin healthy, then use `control-om om -- watch edit <watch> --classifier-mode accept_all --no-overview --label 'Firecrawl retry proof' --format json`. Boot the lane with the same guarded preload and fixture key, `OM_FEED_ALLOW_LOOPBACK=1`, and `OM_FEED_POLL_INTERVAL_MS=60000`. Wait for a healthy feed poll. Capture `/alerts` with its accessibility snapshot and screenshot.
5. Challenge the origin again. Wait for an actual failed poll, then capture `/alerts/<watch>` and `control-om om -- watch show <watch> --format json`. The source says it can read the site if allowed. The vendor count stays one and the allowlist stays empty. Repeating `page-add` returns exit 2 and a hint containing `om setup firecrawl --allow 127.0.0.1`.
6. Restart the same lane and repeat the read. A restart must not buy another scrape. Read-only stored state and pending offer eligibility must agree on this watch and host.
7. Stop the lane and restart without the fixture key. Repeat the blocked CLI call without the key. Expect exit 2 and `om setup firecrawl`, without `--allow`. Capture the source status and paired browser evidence.
8. Publish through `control-om evidence publish <run-id> <revision>` and stop the owned lane and fixtures. The review URL uses the device renderer on 8098.

The 2026-09-30 rig and preload are preserved in `/Users/dboon/Documents/dev-notes/firecrawl-first-block/rig/`; its proof is `firecrawl-first-block-20260930/r2`, archived under `delivery-evidence-archive/` in the same notes directory after the task worktree was removed. Recreate the rig under the next run's assigned ports rather than treating these running servers as shared infrastructure.

### Guest-lane reachability (source-established 2026-10-22, tree `7e22214fb`)

Only the no-key path is drivable with nothing configured. `resolveFirecrawlEscalation()`
returns `null` when no key resolves (`runner/firecrawl/escalation.ts`), and
`FirecrawlEscalation.admits()` returns `false` unconditionally while the client
is `null` — synchronously, before any network call. So automatic retry, the
repeated-refusal whitelist offer and restart persistence can never fire without
a key; a bare guest lane can prove only the blocked path and the
`om setup firecrawl` offer.

**The prerequisite for the configured path is cheaper than an account, and it is
two things at once**: `OM_FIRECRAWL_API_KEY` set to any non-empty string (env
wins over the vault, `runner/firecrawl/credentials.ts`) AND an outbound redirect
of `https://api.firecrawl.dev/v2/scrape` to a fixture. The key alone gets a real
401 from the live vendor (`runner/firecrawl/client.ts` posts it as a literal
bearer), which looks like "no key" for the wrong reason. Both together, or
neither.

This guide has had no live pass from this maintenance loop. Its configured-path
steps stay `live verification pending` on that pair.

## Pausing the offers

*On main since #2265 (v0.489.0). Driven on main 2026-11-04 (steps 1, 3's resume and 4); step 2's seeded host was not re-driven.*

`om config set firecrawl.offers off` (a settings on-off key) stops the daemon raising allow cards; `on` resumes. The agent verbs `firecrawl_offers_pause` (`for: 24h` writes `firecrawl.offers.paused_until`) and `firecrawl_offers_resume` write the same rows; they reach om chat only (no CLI verb, and MCP stdio does not list them) (`runner/firecrawl/policy.ts`). While paused, or while `firecrawl.exhausted_until` is in the future, the drain's watchdog row reads `inactive` with the reason (`offers paused`, `offers paused until <ISO>`, `Firecrawl credits exhausted until <ISO>`); the first pass runs 60 s after boot and every 60 s after. `om setup firecrawl --deny <host>` now also writes `firecrawl.offer.<host>=declined`, so a restart never re-offers a denied host.

Recipe, on a run-owned lane with a fixture key:

1. `OM_LANE_PORT=<port> control-om om -- config set firecrawl.offers off`, then within 70 s `curl /healthz | jq '.loops[] | select(.name=="firecrawl-offers")'` reads `verdict: inactive, reason: offers paused`.
2. Seed a refusing host without an origin: a runtime row on `feed://items?url=https://<host>/feed.rss` in `origin_cooldown` plus two `observeSourceChallenge` calls (the drain test's `seedRefusing`; a bun script with `OM_HOME=<lane root>` works). `pendingFirecrawlOffers(db, new Set())` lists the host.
3. The lane log (`.control-om/lane-<port>.log`) carries no `[firecrawl-offer]` line while paused. `config set firecrawl.offers on`, and the next pass logs `[firecrawl-offer] <host>: no answer` (no model on a guest lane) and the row returns to `ok`.
4. `OM_FIRECRAWL_API_KEY=<fixture> control-om om -- setup firecrawl --deny 127.0.0.1 --format json` answers `declined: ["127.0.0.1"]` (the same JSON carries `"action":"allowed"` and `hosts: []`). A bad value, `config set firecrawl.offers maybe`, exits 2 `firecrawl.offers must be on or off.`; on a lane with no key the drain row reads `inactive`, `no Firecrawl key`, whatever the setting.

Not drivable on a guest lane: the card itself (no model) and the exhausted-credits hold (needs a 402 from the vendor fixture); both are unit-pinned in `firecrawl-offer-drain.test.ts`.

## Gotchas

- This pass proves real product policy, persistence, parsing and user surfaces against simulated HTTP responses. It does not prove the external Firecrawl service or delivery of an interactive agent card; the guest lane has no LLM credential. Regression tests cover the offer/drain path.
- Automatic recovery requires a configured client and an eligible direct-read failure or refusal. Script-shell failures are eligible; a refused vendor read moves the source to its 24-hour hold. No-key requests and declined offers do not retry automatically.
- Bun ignores Node's `NODE_OPTIONS=--require` for this preload. The proved rig uses a run-local Bun wrapper that injects `--preload` only for the product bootstrap. Normal build and test commands use the real Bun binary.
- The CLI probes locally. Both the CLI and daemon need the loopback switch and fixture key during the configured phase.
- Use `--no-overview` with `accept_all` on a guest lane: classification alone does not disable model-generated overview text.
- The source's cooldown status contains the Firecrawl wording. A stale coverage clock can take precedence in the watch headline and show `om watch run now`; inspect the source row rather than requiring the headline to repeat the whitelist hint.
- The source status can be clipped visually in the dashboard card. Keep the accessibility snapshot and CLI result with the screenshot so the complete fix is reviewable.
- Poll the real refusal. A local cooldown check is not another origin refusal and must not advance retry history or buy another scrape.
