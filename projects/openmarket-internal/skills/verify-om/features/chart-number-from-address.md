# Chart a number from an address you paste

*Verified: 2026-11-20, merged main `2d01b6b5d4` (#2637, which is this commit), relay `9199a77`, collab `18845f6`. Lane on 18131 through `control-om`, signed in to the made-up account `@rig`, on a real model (anthropic `claude-opus-5-5`, 5 turns) in the plain REPL. Driven, 5 claims: the key ask with no key on file, the same ask once the key is stored, the watch feed on the rig relay and the `FEED` record in the rig collab, the address typed with its key inside it, and the declined replace. 4 hold. **Claim 14 does not: in chat, declining to replace a key is reported as a save** (Gotchas). Third-party read: `api.nasa.gov` with NASA's public demo key. Not driven: a chart drawn in a browser, the `chart_create` branch (a chart was already active), a second reading and the follower's own conversion, the TUI. "Never fetched" for the typed-key address rests on refusal words that only the no-read branch produces. NASA's logs are not visible. Evidence root `~/Documents/dev-notes/om-2026-11-20-e2e-verify/run-artifacts/s2/` (`phaseB/`, `harness/`, `rig/`). Gallery `http://127.0.0.1:8098/om-1120-e2e/s2/`.*

A person pastes an address and asks om to chart a number from it. The composer reads the address, picks the number and stores a daily watch with one reading field. When the site needs a key, om says so and opens the hidden site-key box. No key is ever sealed into the stored address. The reply hands back the push that charts the watch's feed.

## Sub-features

- `key-ask`: with no key on file the composer answers `Not placed: … api.nasa.gov needs a site key (it answered 403)`. `next[0]` is `site_key_add {name: nasa, site: https://api.nasa.gov}`, and the hidden box opens. No watch is created.
- `read-with-key`: with the key stored, the same ask answers `nasa is on file`, reruns with the key and reads the number (63115). The watch stores field `value` at `$.near_earth_object_count` on the address with no key in it.
- `chart-next`: `next` is `chart_series_push {id: watch.<slug>.value, source: {kind: watch, key: value}}` when a chart is active. The target form is `feed:<scope>/watch.<slug>:value`.
- `feed-and-record`: the relay gets `PUT …/watch.<slug> 201` and `POST …/rows 200`. Collab's store holds a `FEED` record with `address: @rig/watch.<slug>, column: value`.
- `typed-key-address`: an address typed with `?api_key=<key>` and no key on file answers `<host>'s address carries api_key: save it as a site key instead` (`packages/cli/src/actions/watch/_number-scout.ts:758-760`). The plan's address and the handed-back request carry no key. `next` is `site_key_add`. No watch is stored.
- `decline-replace`: declining `Replace it?` in chat goes on and is not reported as a cancel. The words `Kept <name> for <site>` print only from `om setup key` at a terminal.

## How to get to it (user POV)

In `om chat`: `chart the near-earth object count from https://api.nasa.gov/neo/rest/v1/stats daily`. Paste the key into the hidden box when it opens. Ask again. Approve the chart push.

## Driving it with control-om

Preconditions: the local relay, mongod and collab rig, a lane signed in to the rig's made-up account, and a model. The rig scripts are the evidence root's `rig/` folder (`relay/server.ts`, `collab/collab-harness.ts`, `collab/upstream-stub.ts`, `lane-seed.ts`). The lane env is `harness/env-b.sh`.

### The lane

1. Start mongod (one-node `rs0`), the relay harness and the collab pair on agent ports.
2. Boot the lane with `OM_LEDGER_ORIGIN`, `OM_COLLAB_REST_URL` and `OM_COLLAB_WS_URL` at the rig, and every other OpenMarket origin at `http://127.0.0.1:9`. Leave the model-lane origins unset.
3. For a real model, follow the `om-live-eval-seed-safely` recipe: an empty `om.sqlite` plus the chat lane's two vault rows and `vault.key`. Never copy a whole home. Delete the copies at teardown.
4. Run `lane-seed.ts` after the vault rows and `vault.key` are in place, and before the second boot.
5. `control-om om -- llm status` reads usable, with an expiry hours ahead. Read it again after the last turn: the same expiry means the lane did not refresh the token.
6. `control-om om -- chart select <workspace>` for the active-chart branch.
7. `watch_compose` and its key ask need no OpenMarket service. They ran with every origin dead except the rig relay and collab.

### The turns

Run `OM_PLAIN_CHAT=1 control-om om -- chat` in a tmux pane.

1. No key on file. Send the ask. See `[tool] watch_kit`, `[tool] watch_compose`, the `Not placed` line, `[tool] site_key_add` and the box. Press Esc. The reply says nothing is set up.
2. Send the ask with `?api_key=<NASA's public demo key>` in the address. See the `carries api_key` refusal and the box.
3. Store the key at the box (`nasa`, sent as `?api_key=`). Send the first ask again. See the reading, the stored watch and the chart push card. Answer yes.
4. Ask to replace the saved key. At `Replace it? [y/N]` answer `n`. Read what the reply claims.
5. A wait loop must match both card prompts, `[Y/n]:` and `[y/N]:`.

### Read-backs

- `agent_messages` for the compose result: `unplaced`, `readings`, `next`. `harness/dump-turns.py <om.sqlite> [min_ord]` dumps the rows.
- The watch file's `page.reading.fields`.
- `approvals.result_json` for the push note.
- `collab_sticky_payloads.framing_json`. It gains `feed` once the series is converted.
- The relay's request log, and the collab stub's `logs/workspaces.json`.
- The vault ciphertext hash of `sitekey:nasa` before and after a decline.

### The same push from the CLI

`control-om om -- chart series push --id watch.<slug>.value --title "<title>" --watch <slug> --key value --format json` is the compose result's `next` step with no model turn. Once the relay holds the feed it answers `Charted from the watch's feed`. Evidence `phaseB/c12-repush-cli.txt`.

## Gotchas

- **Defect, claim 14: in chat, declining to replace a key is reported as a save.**
  - Repro: a lane with a model and site key `nasa` stored. `OM_PLAIN_CHAT=1 om chat`. Say `I want to replace my saved nasa key for api.nasa.gov with a new one. Open the box.` Answer `n` at `Replace it? [y/N]`.
  - Seen: om hands the model `{"done":true,"name":"nasa","site":"https://api.nasa.gov","stored":true,"kept":true}`. The model answered "I saved your new key as nasa". A fresh conversation answered "The key named nasa is saved". 2 of 2. The vault ciphertext was unchanged.
  - Expected: `Kept nasa for https://api.nasa.gov`, or words that mean it.
  - Cause: `siteKeyHandoffResult` (`packages/cli/src/agent/channels/cli-tui-core.ts:4835-4853`) answers `done: true, stored: true` with a bare `kept: true` (line 4851). The `site_key_add` description and output schema (`packages/cli/src/actions/system/site-key-add.ts:37-46`, `:102-112`) describe only the `done: false` handoff.
  - Fixed: PR #2664, merged 2026-11-23 as `3fac49fe14` after an independent verifier pass (`~/Documents/dev-notes/om-2026-11-20-e2e-verify/verify-pr-2664/`). Open: the TUI tool line cuts the kept sentence at 72 characters (`RESULT_PREVIEW_MAX`), and a way change still answers `stored: true` with no word that the key is unchanged; no real-model turn covers the way change. A kept result answers `kept: true` and `Kept <name> for <site>. The key on file is unchanged; no new key was saved.`, with no `stored` flag; the TUI tool line prints the same. `Kept …` alone next to `stored: true` was misread 1 of 2 times. Final code on `claude-opus-5-5`: 2 of 2 replies said no new key was saved. Evidence `~/Documents/dev-notes/om-2026-11-20-e2e-verify/fix-site-key-kept-words/`.
  - The TUI shares the function (`cli-tui-core.ts:15136`). Not driven there.
  - Evidence `phaseB/c14-t4-screen.txt`, `c14-t4-tool-trail.txt`, `c14-t5-tool-trail.txt`, `c14-cli-kept.txt`.
- **Known, not verified-good: a chart pushed from chat stays a snapshot until the watch's next reading.**
  - The chat turn's push saved a snapshot series and said the chart moves to the watch's feed once its history reaches the relay. The lane made the feed 40 s later. For the next 5.5 minutes nothing wrote to collab.
  - The same push again stored the `FEED` record.
  - Cause: `packages/cli/src/actions/collab/series-push.ts:694-722` returns `awaiting_history` and nothing in the chat process retries. The daemon's follower converts only on a later `watch_committed` for that watch (`packages/cli/src/runner/collab/series-follow-push.ts:593`) or its own retry, armed only from its own flush (`:279`).
  - For a daily reading that is up to a day.
  - Evidence `phaseB/c12-relay-readback.txt`, `c12-collab-readback.txt`.
- **Known, not verified-good: a key typed inside an address stays in chat history and `agent.log`.** The typed sentence was in 2 `tool_call` lines of `agent.log`, 8 `agent_messages` rows and 3 search rows. The paste guard skips addresses, and the scrubber cannot know a key that was never stored. No watch, reading, snapshot or stream id held it. Evidence `phaseB/c11-c13-store-scan.txt`.
- The relay feed is made by a 5-minute loop after the first push queues it.
- The limit on NASA's public demo key is per address and per IP family, and om reads over IPv4. Check `curl -4` before a run. On 2026-11-20 IPv4 answered 429 with a 12-hour retry while IPv6 answered 200.
- The new daily watch went `degraded (http_429)` two seconds after compose read its number, and `om watch run now` was refused for hours. Plan on one reading.
- Without a key NASA answers an HTML 403 (`API_KEY_MISSING`).
- On a fresh home the keyed `watch_compose` ran `auto-approved` with the card's rows printed. `chart_series_push` asked. Not checked against the intended default.
- A signed-out browser cannot read collab, so no chart was drawn. What is proven is the row in the rig relay and the record in the rig collab.
