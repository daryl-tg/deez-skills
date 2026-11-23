# Source resolution: one resolver for any source

*Verified: 2026-11-24 (nightly), tree `26d502c689` (origin/main, v0.496.0+internal), guest lane on 18188 through `bootstrap.internal.ts`, a scratch fake model on 18191 and a loopback source stub on 18192 (`OM_FEED_ALLOW_LOOPBACK=1` on the lane and the CLI). First proof on main: f838c0d73b landed the resolver after 2026-11-22. Driven: `om watch <url>` taking the linked feed by default and the page with `--prefer page`; `om watch resolve` on a walled page in text and JSON; its `Apply:` edit moving the source and keeping its id; the `watch_source_not_resolvable` refusal on a healthy feed; an unknown source; `pages.renderer` in `config get`. Not driven: the site-rule and directory rungs, the API and connector rungs, the local Chrome render rung, the composer card's cost row, `watch source add` through the ladder. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261124/r1/` (`cli/10` to `cli/18`, `cli/breadth/33-config-renderer.out`).*

*Earlier: verified 2026-11-06 on branch `daryl/watch-source-resolution` (PR #2383, tree `e12ec7b94`), where a pasted Fed press-release page became `feeds/press_all.xml` (20 items), a Reddit share link became the post's `.rss` (53 items) and a script-built page rendered in local Chrome. Evidence: `~/Documents/dev-notes/om-source-resolution/evidence/`. Those real-site results were not re-driven on main.*

When a person pastes an address, om takes the best read it can prove: a feed, a site-rule feed or an API before the page itself. When a page source later stops (a bot wall, a login wall, an origin cooldown, a script shell or a feed address that answers a web page), `om watch resolve` looks for another way in and prints the command that switches to it.

## Sub-features

- `url-default` — `om watch <url>` with no `--prefer` takes the best proved read before the page. On the stub it printed `feed_created (feed)`, `feed: <origin>/feeds/news.xml`, `instead: watch the page (om watch --prefer page <url>)`, `reads: no source-read model request per poll` and `now: 5 items, newest <date>`. `--prefer page` keeps the page (`created (page)`), and `--prefer feed` takes feeds only.
- `resolve` — `om watch resolve <watch> <source>` takes exactly two positionals plus `--format text|json`. `<source>` is a source id (`src_…`) or the source's name. It runs no model. On a walled page whose last good read linked a feed, the text reads:
  - `Source: <name> · <reason>` (the stored verdict, for example `bot wall suspected` or `origin cooldown`);
  - `Found: the page linked this feed when om last read it · 5 items`;
  - `Reads: <feed url>`, `Cost: free`;
  - `Apply: om watch edit <watch> --source-id <src> --source 'feed:<url>'`.
  With nothing found it prints `Found: nothing else answered (its site rules, the feeds it links, the APIs om reads)` and no `Apply:` line.
- `resolve-json` — `--format json` returns `watch_id`, `watch_slug`, `source_id`, `source_name`, `reason`, `current {adapter, address, rung}`, `read` (`null`, or `{rung, address, adapter, cost, items, newest, why}`) and `apply` (`null`, or `{command, edit {id_or_slug, source_id, source {kind: "listener", stream_ref, latency_class}}}`). A linked feed reads `rung: "declared"`, `cost: "free"`. `apply` is `null` when nothing proved out, and when the best read is the page itself.
- `apply` — running the printed `om watch edit` prints `source moved: <page> → <feed>`. The source keeps its id, and its adapter becomes `feed`.
- `refusals` — a source that is not stopped answers `watch_source_not_resolvable`, exit 2: `Source "<name>" of <watch> is not stopped by a wall, a script shell or a page, so no other read is looked for.` A source name the watch does not have answers `watching_unknown_source` (`"<x>" is not a source on this watch; sources: "<names>"`).
- `renderer-setting` — `pages.renderer` (`auto` or `off`, default `auto`) decides whether a script-built page renders in this machine's Chrome; `OM_PAGES_RENDERER` overrides it. `auto` does nothing without a local Chrome or Chromium.
- `reach` — `watch_source_resolve` is a tier 1 read on the agent, MCP and CLI catalogues. A hosted assistant gets the terminal command, not a card. It is one of the 497 tools on the full stdio face.

## How to get to it (user POV)

- Paste an address: `om watch <url>`, or ask om chat to watch a page.
- When a watch's status names a wall or a cooldown on a page source, run `om watch show <watch>` for the source id, then `om watch resolve <watch> <source>`. Run the printed `Apply:` command to switch.

## Driving it with control-om

Needs a lane, a loopback stub and a model variable for the page source (a page watch refuses with no model credential, even `--diff-only`). No real model is called.

1. Write a scratch `Bun.serve` on an agent port (18192 here) that serves `/news` as readable HTML with an `<a href="/feeds/news.xml">` **in the body**, `/feeds/news.xml` as RSS with 5 items, and a mode file that turns `/news` into `403` with `cf-mitigated: challenge`.
2. `control-om up --port <p> --env OM_FEED_ALLOW_LOOPBACK=1 --env OPENMARKET_LLM_PROVIDER=openai-compatible --env OPENMARKET_LLM_BASE_URL=http://127.0.0.1:<fake>/v1 --env OPENMARKET_LLM_MODEL=fake`. Export `OM_LANE_PORT=<p>` and the same four variables for every CLI call.
3. `control-om om -- watch http://127.0.0.1:<stub>/news --yes` takes the feed (`url-default`).
4. `control-om om -- watch http://127.0.0.1:<stub>/news --prefer page --diff-only --every 60s --yes` adds a page watch. Note its watch id and, from `watch show <w> --format json`, its source id.
5. Flip the mode file to the wall and wait for the next 60 s check. The stub log shows `GET /news challenge`.
6. `control-om om -- watch resolve <w> <src>`, then the same with `--format json` (`resolve`, `resolve-json`).
7. Flip the stub back, run the printed `om watch edit …` and read `source moved:`. `watch show <w> --format json` keeps the source id with `adapter: "feed"`.
8. `control-om om -- watch resolve <feed watch> <its src>` exits 2 with `watch_source_not_resolvable`.

## Gotchas

- The `declared` rung reads the links in the page's stored readable text, not its `<head>`. A stub that only declares `<link rel="alternate" type="application/rss+xml">` gets `Found: nothing else answered` once walled, though `om watch <url>` still found that feed while the page was readable. Put a visible body link to the feed in the stub (2026-11-24).
- Every watch on one origin shares the origin's cooldown. After one walled check, a second page watch on the same stub read `origin cooldown`, not `bot wall suspected`; resolve treats both as stopped.
- The resolver does not re-fetch a walled page. It does fetch the feeds and APIs it tries, so the stub must keep the feed readable.
- `om watch run-now` is not a verb; `om watch run-now <w>` is read as compose text. Use `om watch run now <w>`.
- The status row for a walled page shows the Firecrawl offer, not resolve, when Firecrawl can be set up (deliberate precedence).
- Reddit 429s this machine on and off (the operator's daemon polls several Reddit feeds from the same IP); a site-rule feed then lands with `now: not read yet: <host> is rate limiting this machine`.
- A script-built page's render is best-effort on a slow network: on 2026-11-06 `app.uniswap.org` refused with `Already rendered in this machine's Chrome and still unreadable.`
- No production connector ships (PandaScore was removed 2026-11-06 as too operator-specific); the `connector` rung is tested with a neutral fake only.
- `control-om down --port <p>` ignores `--port` without `OM_LANE_PORT` exported.
