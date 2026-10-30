# Origin challenge backoff

*Re-driven 2026-10-31 (nightly), tree `dfefe0a21` (origin/main, v0.480.2), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), stub on 18166. Steps 1-3 on the dashboard-authored `ui-authored-feed` (resumed from the CLI; it polled `ok GET /rss` each minute). `echo challenge > mode` at 20:26:26Z; the stub logged exactly one `challenge GET /rss` (20:27:14Z) in the following four minutes; the lane log carried `reopen held until 2026-10-30T20:42:14Z: 127.0.0.1 is challenging this machine; next try …` (15 min); `/healthz` showed the stream `reconnecting`, `reconnect_count` 0 and a `cooldown` with `until` and the challenge sentence; two minutes into the hold `watch show` read `FAULT source broken · 127.0.0.1 · since Oct 31 04:28`, an `Error:` line `stream not delivering: 127.0.0.1 is challenging this machine; next try …`, `Cause: … (retrying in 11m)` and the source row `Status: waiting · 127.0.0.1 is challenging this machine since … · next try … · Firecrawl can read it for you`. The doubling and the reopen were not driven; the mode went back to `ok` at 20:30:47Z. Evidence: `http://127.0.0.1:8098/vom-nightly-20261031/r1/` (`cli/A0-A2`).*

*Re-driven 2026-10-30 (scheduled maintenance), tree `3cb50a821` (origin/main, v0.478.0), fresh lane on 18165, host load average about 140. Steps 1-3 and the recovery, with the loopback switch on `up` and the stub on 18166. A UI-authored feed polled `ok` each minute. After `echo challenge > mode`, one `challenge GET /rss` at 02:11:27 logged `reopen held until 02:26:27` (15 min). `/healthz` showed the subscription `reconnecting`, `reconnect_count` 0 and a `cooldown`. `watch show` read `FAULT source waiting · feed 127.0.0.1: 127.0.0.1 is challenging this machine … · Firecrawl can read it for you` with `FIX om setup firecrawl`, and the dashboard detail showed the same sentence. With the stub back on `ok`, the daemon sent nothing until `ok GET /rss` at 02:26:27, then logged `reopened after the window`, and `/healthz` read `open` with no cooldown. The doubling (a still-challenged probe at `until`) was not re-driven. A CLI `page-add` inside the window added `challenge GET /article/1` at 02:13:38, as the Gotchas warn. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261030/r1/` (frame 35, `cli/40`, `cli/42`, `cli/43`).*
*Verified: 2026-10-29 (nightly), tree `32ca0d6c7` (origin/main, v0.467.0), lane on 18104 with `OM_FEED_ALLOW_LOOPBACK=1 OM_FEED_POLL_INTERVAL_MS=60000`, stub on **18112** (another run held 18111). Steps 1-3: `page-add http://127.0.0.1:18112/rss --prefer feed --every 60s` gave `feed_created`, and healthy polls landed. The stub flipped at 19:26:49Z. It logged exactly one `challenge GET /rss` (19:27:07.665Z) in the next three minutes, and the lane logged `reopen held until 2026-10-28T19:42:07.971Z: 127.0.0.1 is challenging this machine; …` (15 min). About 20 s after that line, `/healthz` still read `open` with `cooldown null`, and `watch show` named no challenge. About a minute in, `/healthz` read `reconnecting`, `reconnect_count 0` and a `cooldown` whose `until` matched the log. `watch show` then had `FAULT source waiting · feed 127.0.0.1: Origin stub: 127.0.0.1 is challenging this machine since … · next try … · Firecrawl can read it for you` and `FIX om setup firecrawl`, and the dashboard detail said the same. The headline and the `watch list` cell named the steps fault instead (`judging paused · no model to run the AI filter on`). Steps 4 and on were not re-driven. Evidence: `http://127.0.0.1:8098/vom-nightly-20261029/r1/`.*

*Verified: 2026-10-28 (scheduled maintenance), tree `186030b63` (origin/main), fresh lane home on 18145 with `OM_FEED_ALLOW_LOOPBACK=1 OM_FEED_POLL_INTERVAL_MS=60000`, stub on 18111. Steps 1-3 only: `page-add` gave `feed_created`, the healthy polls landed, and the stub flipped to challenge at 01:51:56Z. The stub then logged exactly one `challenge GET /rss` (01:52:37Z) in three minutes. The lane logged `reopen held until 2026-10-28T02:07:37.125Z: 127.0.0.1 is challenging this machine; …` (15 min), and `/healthz` showed `reconnecting`, `reconnect_count` 0 and a `cooldown`. Steps 4 and on (the probe and the doubling) were not re-driven here; the nightly record below covers them. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261028/r1/` (`cli/origin-stub-requests.log`, `dash_origin-challenge-detail.png`).*

*Nightly record: 2026-10-28, tree `a8fa10974` (origin/main, v0.466.0), lane on 18104 with `OM_FEED_ALLOW_LOOPBACK=1 OM_FEED_POLL_INTERVAL_MS=60000` and the stub on 18111, polled by a dashboard-authored feed (`ui-authored-feed`). After the flip, the daemon made one `challenge GET /rss` (19:24:05.818Z) and logged `reopen held until 2026-10-27T19:39:05.910Z: 127.0.0.1 is challenging this machine; next try …`. `/healthz` read `reconnecting`, `reconnect_count 0` and a `cooldown`. Newly driven, with the stub left challenged: exactly one probe at `until` (19:39:05.917Z), then a doubled hold `until 20:09:06.046Z`. The stub was flipped to `ok` before that window ended. There was exactly one `ok GET /rss` at 20:09:06.068Z, the lane logged `reopened after the window`, and `/healthz` read `open`, `cooldown null` and `reconnect_count 0`. `watch show` then read `source working` with no challenge sentence. **12 minutes into the first hold, the status rows no longer named the challenge** (Step 3, and a product gap in the README). Not driven: a 429 `Retry-After`, the AWS WAF and 405 shapes, and the 6 h cap. Previous stamp `8fe6a8432` is an ancestor (10 commits).*

When a site challenges the daemon's IP, every source on
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
- `escalate` (v0.400.0) can retry an eligible refused fetch through an allowed
  third-party transport instead of going quiet; availability follows the
  transport policy and does not require a credentialed home by definition.

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
  `cf-mitigated: challenge` and a "Just a moment..." body. Challenge detection
  (`shared/public-document.ts`, `isChallenge`) also recognizes AWS WAF 202
  challenges (`x-amzn-waf-action: challenge`) and 405 captchas, and a 429 opens
  a cooldown too (its `Retry-After` overrides the doubling, capped at 6 h).
  Challenge markers in an HTTP 200 body are a **page** path
  (`shared/page-normalize.ts`, `bot_wall_suspected`), not the feed path. A bare
  403 proves nothing; on main it is retried once under om's other User-Agent
  (`requestWithReaderAgent`), and a host refusing both is held to one name for
  an hour. Log every request
  with a timestamp: that log is the proof of silence.
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
   `feed_created` (or `adopted` when a watch already reads that URL, as the
   dashboard-authored `ui-authored-feed` did at `db6e76ef5`; resume it). Wait
   for two `ok GET /rss` (at `db6e76ef5` no `GET /article/` followed for this
   stub's items, so do not block on one) in the stub log. Older trees also
   fetched one `ok GET /article/`.
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

   - **On main the row names the host** whenever coverage knows it
     (`status-sentence.ts`, `coverage.host ?? coverage.backend`). Driven at
     `db6e76ef5`: `feed 127.0.0.1: 127.0.0.1 is challenging this machine`.
     `watch list` may show a different fault for the same watch (a guest
     `summary stopped: the credential was refused` on an authored feed with a
     summary step), so read `watch show`'s FAULT rows.
   - **The host is not always named (older trees).** The subject is `place(host)`
     (`shared/watch-error-words.ts`): the hostname when the row knows it,
     the literal words `the source` when it does not. Both forms are current —
     grep `is challenging this machine`, not the host.
   - **A Firecrawl offer is appended on a home holding no key**:
     `· Firecrawl can read it for you`. No loopback filter applies, so it fires
     for `127.0.0.1` on a plain guest lane.
   - **The offered fix changed.** The cooldown branch now returns
     `om setup firecrawl` where it used to return `om watch run now <slug>`. A
     recipe asserting the old fix string fails.
   - **Read these rows early in the hold.** Once the held source is past its
     expected interval, the staleness row displaces the challenge row. Driven
     2026-10-28 on a dashboard-authored feed, 12 minutes into the hold:
     - `watch show` FAULT read `source broken · 127.0.0.1`.
     - The source row and `watch list` read `not checked since <time> ·
       expected every 1 min · om watch run now <slug>`.
     - The dashboard detail page read `broken · expected every 1 min`.
     - Only the `Error:` / `Cause:` lines still carried `127.0.0.1 is
       challenging this machine`.
     This is a product gap (README). Assert the challenge sentence in the
     first minutes of the hold, or on `Error:`, and do not take a missing
     Firecrawl offer later in the hold as drift.
     **"Early" is shorter than it sounds on a 60 s feed.** Driven 2026-10-28
     at `186030b63` on a CLI `page-add --every 60s` watch, only 3 minutes into
     the hold, the `watch list` row had already switched to `not checked since
     09:51 · expected every 1 min · om watch run now`. At the same moment,
     `watch show` still carried `waiting · 127.0.0.1 is challenging this
     machine since … · next try … · Firecrawl can read it…` in its `words`,
     plus `stream not delivering: 127.0.0.1 is challenging this machine` in
     the source `error`. The dashboard detail page showed `broken` beside that
     same `waiting · … challenging …` sentence. Assert on `watch show`, not on
     `watch list`.
4. Proof of the probe: at `until` (15 min after the challenge, plus jitter)
   exactly one more `challenge GET /rss`, then silence again. **The window then
   doubles.** Driven 2026-10-28 with the stub left challenged: the hold opened
   at 19:24:05.825Z `until 19:39:05.910Z`. The stub logged exactly one
   `challenge GET /rss` at 19:39:05.917Z, and the lane logged `reopen held until
   2026-10-27T20:09:06.046Z: 127.0.0.1 is challenging this machine; next try …`.
   That is 30 minutes, double the first window. A separate CLI cooldown,
   recorded by a `page-add` probe of another loopback port at 19:35:50 (`next
   try 19:50:51`), did not delay this stream's probe.
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

- **The surfaces lag the hold line by up to a minute.** Driven 2026-10-29: about 20 s after the lane logged `reopen held until …`, `/healthz` still showed the stream `open` with `cooldown null`, and `watch show` named only the steps fault. Both carried the hold about a minute in. Wait for the `cooldown` object before asserting, rather than reading once.
- **On a guest lane a `page-add` feed leads with its steps fault.** The headline and the `watch list` STATUS cell read `steps judging paused · no model to run the AI filter on · om init`, because the feed carries an AI filter. The challenge is in `watch show`'s `FAULT`/`FIX` rows and in `--format json` `.status.source` (`code: source_retry_waiting`, `fix.command: om setup firecrawl`).
- **18111 is often held by another run** (2026-10-28 and 2026-10-29). Start the stub with `ORIGIN_STUB_PORT=<free agent port>` and check its first line, `origin stub listening on …`, before you trust a `curl`. A `curl` on a port held by another run reaches their server.

- **Escalation follows transport policy.** v0.400.0 added an escalation path
  when an origin refuses this machine. The feed adapter can refetch through a
  third-party transport (`shared/escalating-fetcher.ts`), subject to the
  transport's eligibility and policy checks. A guest lane without a configured
  Firecrawl client proves only the direct-fetch cooldown path; configured
  recovery is tracked separately in `firecrawl-first-block.md`.

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
- **The stub's request log is `requests.log` in its working directory**, not its
  stdout. Stdout prints only `origin stub listening on …`, so a run reading
  stdout sees no requests and concludes the poller is dead. Run it from a
  scratch directory of the run's own (`mkdir -p <run>/origin-stub && cd …`),
  and copy `requests.log` into the artifact directory as the silence proof. The
  helper ships with this skill: `helpers/origin-challenge-stub.ts` under the
  canonical hub path, also reachable as `~/.claude/skills/verify-om/helpers/`
  and `~/.codex/skills/verify-om/helpers/`.
- **Other processes on this machine probe 18111.** Driven 2026-10-23, the log
  caught `ok GET /chat/tools/visual/shell-fixture.html` from something that was
  not the lane. Filter the silence proof on `/rss` (and `/article/`) rather than
  counting every line.
- **A CLI probe during a hold hits the origin.** `page-add` runs in the CLI
  process, outside the daemon's hold. Repeating it while the origin is
  challenged adds a `challenge GET` line to the log and refuses. On
  2026-10-30 the refusal was `page_bot_wall_suspected` (exit 2), because the
  fresh probe met the challenge itself; `page_origin_cooldown` is the other
  branch (`actions/watch/_page-leg.ts:987-990`). Run the Firecrawl no-key step only after the
  recovery proof, never inside the window you are proving silent.
- **The status surfaces trail the hold line by several seconds.** Driven
  2026-10-26: the lane logged `reopen held until …` at the challenged poll. Read
  4 s later, `/healthz` still showed the stream `open` with `cooldown: null`,
  and `watch show` and the detail page had no challenge row. By 13 s all three
  carried the hold. Assert the hold surfaces at least 15 s after the
  `challenge GET`, and re-read before calling a missing row a regression.
