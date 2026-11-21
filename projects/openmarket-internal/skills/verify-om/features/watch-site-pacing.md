# Watch site pacing (`om watch pacing`)

*Re-checked 2026-11-22 (nightly), tree `01482928a5` (origin/main, v0.496.0+internal), guest lane on 18188 through `bootstrap.internal.ts`. `watch pacing --format json` answered `{"sites": []}` on a lane that met no 429. Not re-driven: a learned pace, its store, a restart. (`cli/32-watch-pacing.out`.) Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261122/r1/`*

*Verified: 2026-11-18 (nightly), tree `db4ba5c6e2` (origin/main, v0.496.0+internal), guest lane on 18188 started through `bootstrap.internal.ts` with `OM_FEED_ALLOW_LOOPBACK=1` and `OM_FEED_POLL_INTERVAL_MS=60000`, a scratch loopback feed stub on 18111 that answers `429` with `Retry-After: 1` while its `mode` file reads `429`. First live proof of #2539 and #2554. Driven: the empty listing, one 429 episode, the runner log's halving lines, the stored `origin_pace` row, the CLI read lagging the daemon by the write window, and the learned pace surviving a lane restart. Not driven: the climb back to 60 a minute, the 7-day drop, the `article_reads` and `link_decoder` scopes (Google News only), the paced status rows on `watch show`, several feeds sharing one site. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261118/r1/` (`cli/watch-pacing.txt`).*

om learns how fast each site lets its watches read it and spreads every feed on that site across the learned rate. A person sees which sites are throttling their watches and how often each feed on them is read.

## Sub-features

- `watch-pacing-list`: `om watch pacing` (CLI only; `watch_pacing` is on no agent or MCP surface). With nothing learned it prints `Every site takes om's full pace.` and `--format json` `{"sites":[]}`. Each learned site is one row: `<host>[ · link decoder|article reads] · 1 every <n> s|min · <n> feed(s) · each read about every <n> min · last 429 <local time>`. JSON rows are `{origin, scope, per_minute, one_every_sec, feeds, refresh_every_min, last_rate_limited_at}`, with `scope` one of `source_polls`, `article_reads`, `link_decoder` (`packages/cli/src/cmd/watch-pacing.ts`, `packages/cli/src/actions/watch/pacing.ts`).
- `watch-pacing-learn`: a 429 halves the site's rate for that kind of request and sets a threshold; clean minutes add rate back (more slowly past the threshold); the floor is 1 read per 10 minutes and the ceiling 60 a minute; a threshold with no 429 for a day is dropped, and a site back at 60 for 7 days is forgotten (`packages/cli/src/shared/origin-limiter.ts`). Each change logs one runner line: `[pace] <host> source polls: 60 -> 30 a minute after 429 on /rss`.
- `watch-pacing-store`: the rate lives in the `origin_pace` table of the home's `om.sqlite` (`origin, scope, per_minute, limited_at, threshold, changed_at`), written at most once a minute per site (`ORIGIN_PACE_WRITE_EVERY_MS` 60 s), so the daemon's next start keeps it.
- `watch-pacing-status` (source only): a paced source's status reads `paced · next read 12:41 · <host> takes about 1 every 24 s`; after 3 h with no read `no read in 3 h · … across <n> feeds · fewer feeds on this site read more often`; after a failed read `held until <time>: <reason>`.

## How to get to it (user POV)

A person whose feeds read slowly, or whose watch says `paced`, runs `om watch pacing` to see which sites answered 429 and how often each feed there is read now. There is nothing to set: om learns and forgets the pace by itself.

## Driving it with control-om

1. Write a scratch stub (any `Bun.serve` on an agent port, here 18111) that serves an RSS feed at `/rss` and answers `429` with `retry-after: 1` while a `mode` file reads `429`. The shipped `helpers/origin-challenge-stub.ts` has no 429 mode.
2. `control-om up --env OM_FEED_ALLOW_LOOPBACK=1 --env OM_FEED_POLL_INTERVAL_MS=60000`, and export `OM_FEED_ALLOW_LOOPBACK=1` for the CLI calls too.
3. `control-om om -- watch page-add http://127.0.0.1:18111/rss --prefer feed --every 60s --format json` → `feed_created`; `watch edit <id> --classifier-mode accept_all` keeps the AI-filter fault out of the way.
4. `control-om om -- watch pacing` → `Every site takes om's full pace.`
5. `echo 429 > mode`. Driven 2026-11-18: the next poll (19:21:55Z) was refused and the feed retried at 2, 4, 8, 16 and 32 s, each a halving in the lane log (`60 -> 30`, `30 -> 15`, `15 -> 7.5`, `7.5 -> 3.8`, `3.8 -> 1.9`, `1.9 -> 0.9`).
6. `watch pacing` right after the first 429 read `127.0.0.1:18111 · 1 every 2 s · 1 feed · each read about every 5 min · last 429 Nov 18 03:21` while the daemon was already at 1.9: the CLI reads the stored row, which trails the daemon by up to the 60 s write window. A minute later it read `1 every 32 s`, and the row held `per_minute 1.875`, `threshold 1.875`.
7. `echo ok > mode`, wait a minute, then `control-om down` and `up` with the same switches: `watch pacing` read `127.0.0.1:18111 · 1 every 1 min · 1 feed · each read about every 5 min · last 429 Nov 18 03:22` (stored `0.9375`).
8. Read-only check of the store: `sqlite3 -readonly .control-om/home-<port>/accounts/guest/om.sqlite "select * from origin_pace"`.

## Gotchas

- The learned pace is per origin: `127.0.0.1:18111` and `127.0.0.1:18112` are two sites. Use a second stub port to drive anything else on a site the pace has slowed, or wait a long time for its next read.
- The pace slows source polls on the lane for the rest of its life; a later recipe on the same stub inherits it. Delete the lane root for a fresh pace.
