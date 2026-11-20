# A watch follows an X handle on the free mirror

*Re-driven 2026-11-21 (nightly), tree `3c4839c59d` (origin/main, v0.496.0+internal), guest lane on 18188 through `bootstrap.internal.ts` with `OM_FXTWITTER_BASE_URL=http://127.0.0.1:18190` and `OM_X_POLL_INTERVAL_MS=60000`, a scratch mirror stub on 18190. Steps 1 to 9: two watches created, two reads per handle, `collection state none -> ok`, one 404 on `vomflap` followed 2 ms later by one extra read of `vomok`, the two lane lines, the `waiting · x @vomflap: fxtwitter answered not found, not yet confirmed; om is waiting since …` sentence on `watch show` and `watch list`, then `degraded -> ok` on the next poll, the `X lane` row back to `unofficial, can lapse`, and no gone notice. Not re-driven: the hour that ends in `dead`. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261121/r1/` (`cli/b0-*`, `cli/b1-*`, `cli/b2-*`).*

*Verified: 2026-11-20 (nightly), tree `ba18e48ef3` (origin/main, v0.496.0+internal), guest lane on 18188 started through `bootstrap.internal.ts` with `OM_FXTWITTER_BASE_URL=http://127.0.0.1:18190` and `OM_X_POLL_INTERVAL_MS=60000`, a scratch loopback mirror stub on 18190. First live proof of an X source and of #2607. Driven: two `x:@<handle>` watches created against the stub, the opening read, the `X lane` row, one 404 on one handle held as `waiting` (CLI, JSON, lane log, dashboard row), the canary read of the other handle, and the recovery on the next 200. Not driven: the hour of 404s that ends in `dead`, the gone notice, 410 and 451, the paths with no canary, a 2xx whose body says 404, the official X API lane, a new post arriving after the opening read. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261120/r1/` (`01-watches-x-waiting.png`, `cli/30-x-create.txt`, `cli/31-x-flap-degraded.txt`, `cli/32-x-flap-recovered.txt`).*

A person names an X account and om reads its posts through a public mirror with no key. When the mirror answers "not found" for that account, the watch says om is waiting and keeps reading; it calls the account gone only after an hour of that account's own not-found answers.

## Sub-features

- `x-source-create`: `om watch create <name> --source x:@<handle>` stores one listener source with `stream_ref {adapter:"x", channel:"posts", extra:{handle}}` and the default classifier `llm_every_event`. The card row reads `1  @<handle>   x · posts by the X account @<handle>`. The first X watch on a home also carries `x_search_hint` (`X search: not on this AI account (named handles still polled keyless) …`). The stub saw two reads of the handle within 30 ms at creation (the creation probe, then the stream opening).
- `x-lane-row`: `om watch show <name>` prints `X lane: free mirror (fxtwitter) · unofficial, can lapse · last poll <iso>` and `upgrade: om setup x-api (or /setup > X API) · official feed, billed per post`. `om service status` lists each stream under `Subscriptions:` as `x://posts?handle=<handle> — state=open subs=1 buf=0 recv=0`.
- `x-opening-read`: the posts that already existed are the opening read (`Opening read · <time> · what already existed when the watch was born · not sent`); they are judged and kept, and sent nowhere.
- `x-mirror-404-held` (#2607): one not-found answer for a handle, backed by a known account that still answers, is recorded `degraded` with reason `mirror_unverified_404`, never `dead`. The watch reads `waiting · x @<handle>: fxtwitter answered not found, not yet confirmed; om is waiting since <last ok> · next try <time> · om setup x-api for the official feed` in `watch show`, `watch list` and the dashboard row. The `X lane` row reads `free mirror (fxtwitter) · said not found, unconfirmed; om keeps checking (mirror_unverified_404) · last poll <iso>, last ok <iso>, HTTP 404`. `watch show --format json` carries `runtime.worst.collection_state` (`state:"degraded"`, `reason:"mirror_unverified_404"`, `http_status:404`, `interval_ms`) and `x_coverage` (`state:"mirror_degraded"`, `summary:"said not found, unconfirmed; om keeps checking"`). The poll interval stays the same.
- `x-mirror-recovery`: the next validated 200 puts the stream back to `ok`; the `X lane` row returns to `unofficial, can lapse` and no notice was opened.
- `x-mirror-dead` (source only): after `X_MIRROR_NOT_FOUND_CONFIRM_MS` (60 minutes) of the handle's own first-page reads answering not found, the state goes `degraded -> dead (handle_not_found, HTTP 404)`, the poll slows to three times the interval and a gone notice opens (`packages/cli/src/runner/subscriptions/adapters/x.ts`; the sentence is `COVERAGE_REASON_WORDS.mirror_unverified_404` in `packages/cli/src/runner/watching/status-sentence.ts`).

## How to get to it (user POV)

A person runs `om watch create <name> --source x:@<handle>`, or asks om chat to watch an account. They read the watch with `om watch show`, `om watch list` or the dashboard's Watches page. Nothing is set for the mirror; `om setup x-api` moves a home to the official feed.

## Driving it with control-om

Preconditions: two free agent ports (lane and stub). No X access and no model are needed.

1. Write a scratch stub (`Bun.serve` on `127.0.0.1:<stub-port>`) that answers `GET /2/profile/<handle>/statuses` with
   `{"code":200,"results":[{"id":"<numeric id>","text":"…","url":"https://x.com/<handle>/status/<id>","author":{"screen_name":"<handle>","name":"<handle>"},"created_timestamp":<unix seconds>}, …],"cursor":{"top":"t","bottom":"b"}}`,
   and with HTTP 404 `{"code":404,"results":[]}` while a `mode-<handle>` file reads `404`. Log every request with a timestamp.
2. `control-om up --port <lane> --env OM_FXTWITTER_BASE_URL=http://127.0.0.1:<stub-port> --env OM_X_POLL_INTERVAL_MS=60000`. Export both variables for the CLI calls too: `watch create` reads the mirror itself.
3. `control-om om -- watch create vom-x-ok --source x:@vomok --format json`, then `control-om om -- watch create vom-x-flap --source x:@vomflap --format json`. Create the healthy one first: it is the known account that backs a later not-found. The stub log shows two reads per handle.
4. `control-om om -- watch edit <name> --classifier-mode accept_all --format json` on both, or the opening read stalls on `the AI filter has no model to run on`.
5. Lane log (`.control-om/lane-<port>.log`): `[subscriptions] [x] x://posts?handle=vomflap: collection state none -> ok (validated 2xx, HTTP 200); next poll in 60s`.
6. `echo 404 > mode-vomflap` and wait for the next poll (60 s after the last). The stub log shows the 404 for `vomflap` and, a few milliseconds later, one extra read of `vomok`.
7. The lane log gains two lines: `…handle=vomflap: the mirror answered not found and this handle's own reads have not answered not found for an hour yet; recorded degraded (mirror_unverified_404, not_repeated), never dead on one backend answer` and `collection state ok -> degraded (mirror_unverified_404, HTTP 404); next poll in 60s`.
8. `control-om om -- watch show vom-x-flap` opens with the `waiting · x @vomflap: fxtwitter answered not found, not yet confirmed; om is waiting since …` line; `watch list` and the dashboard row at `$(control-om url /alerts)` read the same sentence. `vom-x-ok` is unchanged.
9. `echo ok > mode-vomflap`. After the next poll the log reads `collection state degraded -> ok (validated 2xx, HTTP 200)` and the `X lane` row is back to `unofficial, can lapse`. `control-om om -- notis --watch vom-x-flap` holds no gone notice.

## Gotchas

- `OM_X_POLL_INTERVAL_MS` is clamped to a 60-second floor, so each step waits up to a minute. The default is 5 minutes.
- The hour that ends in `dead` runs on the daemon's own clock. No switch shortens it; only the unit tests (`packages/cli/test/x-mirror-burst.test.ts`) move the clock.
- The lane log calls a good read `validated 2xx`. Serve the full post shape from step 1; a thinner body was not driven.
- On a guest lane `om status` lists an X watch under `Broken:` as `summary stopped: the credential was refused`: that is the missing model, not the mirror.
- Driven 2026-11-20: an MCP `watch_list` read taken 6 seconds after the 404 gave the held watch's `state` column as `working`, and `om watch list` a few seconds later read `waiting`. The MCP rows were not read again, so this may be the store's write lag. Read `om watch show` for the mirror's state.
