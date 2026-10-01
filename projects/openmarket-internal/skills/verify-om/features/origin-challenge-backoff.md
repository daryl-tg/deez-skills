# Origin challenge backoff

*Verified: entry path, hold arming and the status row 2026-09-24, tree `8d0403322` (v0.408.1) — hold armed at exactly +15:00 and the row byte-identical to the prior pass. The probe, the doubling and recovery were last driven 2026-09-19 at tree `15db727ba` (v0.353.1). Re-drive the full ladder when the HOLD MACHINERY changes — `shared/origin-limiter.ts` (constants), `shared/public-document.ts` (the predicate), or the cooldown/reopen paths of `runner/subscriptions/manager.ts` and `adapters/feed.ts` — and re-drive the STATUS ROW whenever `runner/watching/status-sentence.ts` changes. Both triggers fired this pass and both proved inert; the status-sentence change is gated on `coverage.backend === PAGE_BACKEND`, unreachable from a feed source.*

When a site puts the daemon's IP under a Cloudflare challenge, every source on
that host goes quiet together after the first challenged answer, one probe goes
out per window, and the watch says so in one row: `the source is challenging
this machine · next try <time>`. When the site answers again, the stream reopens
with no reconnect counted. None of it needs an account.

## Sub-features

- `hold-feed` parks or holds a feed stream until the window's end.
- `hold-extracts` stops the article fetches of a held origin without spending
  the drain's slots or writing rows.
- `probe-once` sends exactly one request when the window ends; a second
  challenge doubles the window (15 min to 6 h).
- `status-row` reads `the source is challenging this machine · next try <time>`
  on `om watch show`, and `/healthz` carries the `cooldown` on the stream
  metric. **The renderers disagree about the host on purpose**: the status row
  says the generic `the source`, while the lane log and `/healthz` name it
  (`127.0.0.1 is challenging this machine`). Grepping the row for the hostname
  finds nothing.
- `recover` reopens the stream on a clean probe, logs `reopened after the
  window`, and clears the row.
- `escalate` (v0.400.0, credentialed homes only) retries a refused fetch through
  an address that is not this machine's, instead of going quiet.

## How to get to it (user POV)

- Watch a feed on a site behind Cloudflare, or a page on it. The status line and
  `om watch show` say a source is challenging this machine, and when it will be
  tried again, once a challenge lands.
- `om watch page-add` on a URL this home already watches returns
  `status: "adopted"` and the existing watch id, not `feed_created`. A lane home
  reused between runs will therefore not produce the create result the step
  above quotes.
- `om watch run now <watch>` inside the window sends nothing, but it is refused
  in GENERIC backoff words, not the challenge words: `the daemon is reconnecting
  this watch's source (parked or backing off after a failure); it polls again on
  its own once the source answers`, plus a pointer to `om watch show <id>` for
  the recorded error. Assert the origin's silence, and read the host and the
  next try off `om watch show`.

## Driving it with control-om

Preconditions:

- A stub host on an assigned agent port (`18111` is this recipe's slot). Use the
  bundled one rather than writing another:

  ```bash
  mkdir -p /tmp/origin-stub && cd /tmp/origin-stub && echo ok > mode
  bun ~/.claude/skills/verify-om/helpers/origin-challenge-stub.ts &
  ```

  It answers a small RSS feed at `/rss` with one new item per minute, article
  pages at `/article/<id>`, and flips on the `mode` file to `403` with
  `cf-mitigated: challenge` and a "Just a moment..." body. The predicate is a
  403 **or 503** carrying `cf-mitigated: challenge`
  (`shared/public-document.ts:135-141`); the header is what decides, so a stub
  that returns a bare 403 proves nothing. Log every request with a timestamp:
  that log is the proof of silence.
- The lane booted with `OM_FEED_ALLOW_LOOPBACK=1` (feed polls, page polls and
  extract fetches may reach `127.0.0.0/8`) and, to shorten the wait,
  `OM_FEED_POLL_INTERVAL_MS=60000`:

  ```bash
  control-om up --env OM_FEED_ALLOW_LOOPBACK=1 --env OM_FEED_POLL_INTERVAL_MS=60000
  ```

- **`OM_FEED_ALLOW_LOOPBACK=1` is also needed on the CLI call that creates the
  watch**, not only on the lane. `page-add` probes the URL in the CLI process,
  so a lane-only switch fails at step 1 with
  `{"error":"page_blocked", ... "(blocked_host)"}`, which reads like the stub
  being down. Prefix the call:
  `OM_FEED_ALLOW_LOOPBACK=1 control-om om -- watch page-add ...`. The same
  applies to `om watch run now` against a loopback origin.

Steps:

1. With the stub healthy: `control-om om -- watch page-add
   http://127.0.0.1:18111/rss --prefer feed --every 60s --format json` reads
   `feed_created`. Wait for two `ok GET /rss` and one `ok GET /article/` in the
   stub log.
2. Flip the mode file to `challenge`. Wait for the first `challenge GET /rss`.
3. Proof of the hold, three minutes later: the stub log holds exactly one
   challenge-mode request; the lane log holds one line ENDING
   `reopen held until <ISO>: 127.0.0.1 is challenging this machine; next try
   <ISO>` — the real line is prefixed with the stream id
   (`[subscriptions] feed://items?url=...: `), so grep the substring, not the
   whole line. Note the separator here is a semicolon, while the status row
   renders the same fact with a middle dot and a short local time
   (`· next try Sep 19 13:56`): two renderers, two spellings; `/healthz`
   shows the stream's `connection_state` as `reconnecting` (that is the key's
   name), `reconnect_count` 0, and a `cooldown` object carrying `until` (epoch
   ms) and `error` (the challenge sentence);
   `control-om om -- watch show <slug>` and `om watch list` both carry the
   challenge sentence inside a longer cell. Driven at v0.400.0:
   `source feed 127.0.0.1: unreachable since Sep 23 12:45 · 127.0.0.1 is
   challenging this machine · next try Sep 23 13:00 · Firecrawl can read it for
   you · om setup firecrawl`, with `watch show` additionally splitting it into
   `FAULT` and `FIX` rows. Times render LOCAL while the lane log and `/healthz`
   carry UTC. Match a substring, never the whole cell, and note three things
   that moved in `da6121d24`:

   - **The host is not always named.** The subject is `place(host)`
     (`shared/watch-error-words.ts`): the hostname when the row knows it,
     the literal words `the source` when it does not. Both forms are current —
     grep `is challenging this machine`, not the host.
   - **A Firecrawl offer is appended on a home holding no key**:
     `· Firecrawl can read it for you`. No loopback filter applies, so it fires
     for `127.0.0.1` on a plain guest lane.
   - **The offered fix changed.** The cooldown branch now returns
     `om setup firecrawl` where it used to return `om watch run now <slug>`. A
     recipe asserting the old fix string fails.
4. Proof of the probe: at `until` (15 min after the challenge, plus jitter)
   exactly one more `challenge GET /rss`, then silence again.
5. Flip the mode file back to `ok` before the next `until`. Proof of recovery:
   one `ok GET /rss` at `until`, the lane log line ending `reopened after the
   window` (stream-id prefixed like the hold line), the held article fetches
   resuming in the same second, `/healthz` `connection_state: open` with
   `reconnect_count` still 0 and `cooldown` null, and the watch row no longer
   carrying the challenge sentence.

   **`/healthz` lags the reopen by up to a minute.** Read immediately after the
   log line it still says `reconnecting` and carries the now-EXPIRED cooldown;
   it flips to `open` with `cooldown: null` once the first batch lands (driven:
   log line at 06:26:15, still `reconnecting` at 06:26:48, `open` at 06:27:28).
   Poll it until it settles rather than asserting once — the stale read looks
   exactly like a failed recovery.

## Gotchas

- **A credentialed home no longer just goes quiet.** v0.400.0 added an
  *escalation* path: when an origin refuses this machine — a challenge, or the
  window it opened — the feed adapter can refetch the same URL through a
  third-party transport (`shared/escalating-fetcher.ts`, wired in
  `runner/subscriptions/adapters/feed.ts`, resolved by
  `runner/firecrawl/registry.ts`). The daemon registers that transport at boot
  and at each reconcile from a stored Firecrawl credential; **a home holding no
  key registers `null`, which is "the direct fetcher exactly as it was"**
  (`runner/index.ts` `refreshFirecrawlEscalation`). So everything this entry
  documents is the NO-CREDENTIAL behaviour, and it was re-confirmed intact at
  v0.400.0. What escalation does on a credentialed home is
  `verified-unreachable` from a guest lane; the unmet prerequisite is a
  Firecrawl key (`om setup firecrawl`).

- A page watch needs a model credential even with `--diff-only`, so a guest
  lane proves the feed and extract paths; the page path is on its unit tests.
- Correlate on the stub's request log, not on the lane log alone: the lane
  says nothing on a refused wait, by design, so silence is the evidence.
- The first window is fifteen minutes and the second is thirty, so the full
  steps 1-5 run costs about 50 minutes wall-clock; the hold alone (steps 1-3) is
  provable in about 20. Budget for it, and never shorten it by editing the
  constants under test (`ORIGIN_COOLDOWN_BASE_MS`, the doubling, the 6 h cap).
- `--every 60s` on the create does NOT set the live poll clock for a
  feed-resolved watch: the feed adapter's interval is a process-wide singleton
  read from `OM_FEED_POLL_INTERVAL_MS` at daemon boot. The flag is stored, the
  env var is what makes the rig poll every minute.
- The `[library]` mirror logs `registry answered 403` on a guest lane; it is
  unrelated to the stub and matches a grep for `403`.
