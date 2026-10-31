# Firecrawl recovery before whitelist

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

## Gotchas

- This pass proves real product policy, persistence, parsing and user surfaces against simulated HTTP responses. It does not prove the external Firecrawl service or delivery of an interactive agent card; the guest lane has no LLM credential. Regression tests cover the offer/drain path.
- Automatic recovery requires a configured client and an eligible direct-read failure or refusal. Script-shell failures are eligible; a refused vendor read moves the source to its 24-hour hold. No-key requests and declined offers do not retry automatically.
- Bun ignores Node's `NODE_OPTIONS=--require` for this preload. The proved rig uses a run-local Bun wrapper that injects `--preload` only for the product bootstrap. Normal build and test commands use the real Bun binary.
- The CLI probes locally. Both the CLI and daemon need the loopback switch and fixture key during the configured phase.
- Use `--no-overview` with `accept_all` on a guest lane: classification alone does not disable model-generated overview text.
- The source's cooldown status contains the Firecrawl wording. A stale coverage clock can take precedence in the watch headline and show `om watch run now`; inspect the source row rather than requiring the headline to repeat the whitelist hint.
- The source status can be clipped visually in the dashboard card. Keep the accessibility snapshot and CLI result with the screenshot so the complete fix is reviewable.
- Poll the real refusal. A local cooldown check is not another origin refusal and must not advance retry history or buy another scrape.
