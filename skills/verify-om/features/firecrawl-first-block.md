# Firecrawl recovery before whitelist

*Verified: 2026-09-30, tree `780c0254c` (v0.425.0), uncommitted `daryl/firecrawl-first-block` diff `1d541c27baeebc5d0ce1f1562e61ece97c3af11ee650840c872aa2dd5bd5db87` — real CLI, daemon and dashboard with simulated origin and Firecrawl responses; live provider and interactive agent delivery not driven.*

A configured Firecrawl connection recovers the first blocked read of a source automatically. A later refusal asks to allow that site. A home without a Firecrawl key continues to offer setup. The first recovery does not grant standing access to the site.

## Sub-features

- A blocked feed can be created after one automatic recovery, without a whitelist prompt.
- Repeated refusal makes the site eligible for the existing whitelist offer; paid fetch count stays at one.
- Restarting the daemon preserves the retry history and the site's refusal status.
- A missing key offers `om setup firecrawl`; a configured key after repeated refusal offers `om setup firecrawl --allow <host>`.
- Existing allowed sites continue to use their standing Firecrawl permission.

## How to get to it (user POV)

1. Connect Firecrawl with `om setup firecrawl`.
2. Watch a public page or feed whose origin challenges this machine.
3. The first blocked read retries automatically. If a later read is refused, the source status says `Firecrawl can read it if you allow it`.
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

The 2026-09-30 rig and preload are preserved in `/Users/dboon/Documents/dev-notes/firecrawl-first-block/rig/`; its proof is `firecrawl-first-block-20260930/r2`. Recreate the rig under the next run's assigned ports rather than treating these running servers as shared infrastructure.

## Gotchas

- This pass proves real product policy, persistence, parsing and user surfaces against simulated HTTP responses. It does not prove the external Firecrawl service or delivery of an interactive agent card; the guest lane has no LLM credential. Regression tests cover the offer/drain path.
- Bun ignores Node's `NODE_OPTIONS=--require` for this preload. The proved rig uses a run-local Bun wrapper that injects `--preload` only for the product bootstrap. Normal build and test commands use the real Bun binary.
- The CLI probes locally. Both the CLI and daemon need the loopback switch and fixture key during the configured phase.
- Use `--no-overview` with `accept_all` on a guest lane: classification alone does not disable model-generated overview text.
- The source's cooldown status contains the Firecrawl wording. A stale coverage clock can take precedence in the watch headline and show `om watch run now`; inspect the source row rather than requiring the headline to repeat the whitelist hint.
- The source status can be clipped visually in the dashboard card. Keep the accessibility snapshot and CLI result with the screenshot so the complete fix is reviewable.
- Poll the real refusal. A local cooldown check is not another origin refusal and must not advance retry history or buy another scrape.
