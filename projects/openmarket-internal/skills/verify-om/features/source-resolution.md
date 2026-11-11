# Source resolution: one resolver for any source

*Re-checked 2026-11-11 (nightly) against origin/main `0ad4768f66` (v0.494.0): still not on main (PR #2383 open); there is no `resolveSource` ladder, and `om watch resolve <url>` on a guest lane is read as compose text and refused `No LLM credential is configured.` (exit 2).*

*Verified 2026-11-06 on branch (PandaScore since removed, head `1f3d044e1`) `daryl/watch-source-resolution` (PR #2383), tree `e12ec7b94` before its last rebase onto `d2ea2e246`; not on main yet. Lane on 18140 from a detached verify worktree, CLI and lane with `OPENMARKET_LLM_PROVIDER=openai-compatible OPENMARKET_LLM_BASE_URL=http://127.0.0.1:9/v1 OPENMARKET_LLM_MODEL=fake` (a page watch refuses with no model credential, even `--diff-only`) and `OM_FEED_ALLOW_LOOPBACK=1` for the stub. Evidence: `~/Documents/dev-notes/om-source-resolution/evidence/` (`final/`, `resolve-offer-final.txt`, `resolve-applied.txt`, `resolve-corpus-final.json`).*

## What a person sees

- `om watch <url>` takes the best proved read: a feed (site rule, linked feed, the site's feed directory) over the page, with an `instead:` row naming the page. A pasted Fed press-release page became `feeds/press_all.xml` (20 items). A Reddit share link (`/r/<sub>/s/<token>`, a 301 to a JS-challenge page) became the post's `.rss` (53 items).
- A page with no on-topic feed stays a page (Beige Book, Monetary Policy Report).
- A script-built page renders in this machine's Chrome. Best-effort: on 2026-11-06 the network was slow (CDN scripts 8 s) and `app.uniswap.org` refused with `Already rendered in this machine's Chrome and still unreadable.`; on 2026-11-05 the same page planned with 956 chars.
- `om watch resolve <watch> <source>` on a walled page prints `Found: the page linked this feed when om last read it · 5 items`, `Reads:`, `Cost: free` and an `Apply: om watch edit … --source-id … --source 'feed:<url>'` line; applying it prints `source moved: <page> → <feed>` and keeps the source id.

## Recipe

1. `control-om up --port <p> --env OM_FEED_ALLOW_LOOPBACK=1 --env OPENMARKET_LLM_PROVIDER=openai-compatible --env OPENMARKET_LLM_BASE_URL=http://127.0.0.1:9/v1 --env OPENMARKET_LLM_MODEL=fake`, then export `OM_LANE_PORT=<p>` and the same three `OPENMARKET_LLM_*` vars for CLI calls.
2. Feeds by default: `control-om om -- watch page-add <url> --diff-only --yes`.
3. Walled-page resolve needs a stub whose page can be walled while its feed answers (the skill's `origin-challenge-stub.ts` walls the whole origin, feed included, so resolve rightly finds nothing there). A scratch `Bun.serve` on 127.0.0.1 serving `/news` (readable HTML linking `/feeds/news.xml`) and the feed, with a mode file that turns `/news` into 403 `cf-mitigated: challenge`. Add `/news` with `--prefer page --diff-only --every 60s --yes`, flip the wall, wait until `watch_runtime.collection_state.reason` reads `bot_wall_suspected`, then `watch resolve <watch> <source>`.

## Gotchas

- Reddit 429s this machine on and off (the operator's daemon polls several Reddit feeds from the same IP); a site-rule feed then lands with `now: not read yet: <host> is rate limiting this machine`.
- The status row for a walled page shows the Firecrawl offer, not resolve, when Firecrawl can be set up (deliberate precedence).
- `control-om down --port <p>` ignores `--port` without `OM_LANE_PORT` exported.
- No production connector ships (PandaScore was removed 2026-11-06 as too operator-specific); the `connector` rung is tested with a neutral fake only.
