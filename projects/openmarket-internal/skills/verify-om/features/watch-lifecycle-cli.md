# Watch lifecycle from the CLI

*Re-driven 2026-11-08 (nightly), tree `5590b4d1c` (origin/main, v0.492.0), guest lane on 18141, booted in 2 s with no guest 429. `watch create`, `edit`, `show`, `pause` (`enabled:false`), `resume`, `history`, `list`; `watch remove lane-quiet` without `--yes` exit 2 `confirmation_required`, then with `--yes` `removed:true`. Not re-driven: `rename`, sources add/remove, the repair verbs. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261108/r1/` (`cli/10-11`, `cli/17`, `cli/70-79`).*

*Re-driven 2026-11-07 (nightly), tree `05f450fc5` (origin/main, v0.492.0), guest lane on 18141, booted with no guest 429. `watch list`, `show`, `pause`, `resume`, `history` on `lane-probe`; `watch remove lane-quiet` without `--yes` exit 2 (`deletes history (0 rows) … It needs a yes.`), with `--yes --format json` `removed: true`, `journal_preserved: true` and no feed row (a guest key has no username, so #2397's `Feed:` row cannot show); `chapters`, `journal-stats`, `event-journal list`. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261107/r1/` (`cli/20-24`, `cli/120-124`).*

*Re-driven 2026-11-06 (nightly), tree `50fcc594b` (origin/main, v0.492.0), guest lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), booted at 19:18Z with no guest 429, host load average 10 falling to about 3.3. `watch list`, `edit --label "Lane Lifecycle Probe"`, `pause`/`resume`, `watch history`, `remove` without `--yes` (exit 2, `It needs a yes.`) and with it (`history deleted (0 rows); journal files kept`); a last-day timer `--every '0 18 L * *' --tz UTC` created and read `working`; `--every month` is `invalid_input` (`use a duration …, a word … or a 5-field cron`). A reader of a paused upstream read `source waiting · probe-upstream is paused · om watch resume probe-upstream`. Archive verbs: [watch-archive.md](watch-archive.md). Evidence: `http://127.0.0.1:8098/vom-nightly-20261106/r1/` (`cli/wl-*`, `cli/tz-l*`, `cli/rd-show.txt`).*

*Re-driven 2026-11-05 (nightly), tree `3a0ea623e` (origin/main, v0.492.0), guest lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), booted in 2 s at 19:19Z with no guest 429, host load average about 4.4. New: monthly timers (#2300) `tz-m` (`'0 9 1,15 * *'`, `Asia/Kuala_Lumpur`) and `tz-l` (`'0 18 L * *'`, UTC) with their worded cards and the raw cron on `watch show`; the upstream stand-down (#2310): `up1` paused with armed reader `rd1` (`readers_stood_down`, `cascade_note`), resumed (`still down from its pause`), `rd1` re-armed, `up1` removed taking `rd1` with it (`via: cascade`), and `up2` removed leaving a two-source `rd2` repaired (`cascade.repaired`, `cascade.rearm`, `up2 is gone → om watch arm rd2`). Re-driven: `cond-probe` `state show`/`state clear`, `state show tz-m` exit 2 `not_a_condition_watch`, `event-journal list`, `watch history`. Evidence: `http://127.0.0.1:8098/vom-nightly-20261105/r1/` (`cli/timer-*`, `cli/up1-*`, `cli/up2-*`, `cli/rd*`, `cli/state-*`).*

*Re-driven 2026-11-04 (nightly), tree `9acb5fb56` (origin/main, v0.491.0), guest lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), booted in 2 s with no 429. `lane-lifecycle`: create, pause (`enabled:false`), resume, `remove --yes` (`removed:true`). `cond-probe` (`--condition '{"metric":"price","selector":{"symbol":"BTCUSDT","exchange":"BINANCE_FUTURES","interval":"MINUTE"},"op":"gt","value":1000000}'`; a tree without `selector` exits 2 `invalid_options` `source.condition: Invalid input`): `state show` `state: null`, `bytes: 0`; `state clear` `{"cleared":true,"record_restarts":null}`; `state show tz-fri` exit 2 `not_a_condition_watch`. Over MCP `watch_state_clear {id}` answered `cleared:true`. `event-journal list`, `watch history`. New: `timer-days` on `tz-fri` (`0 7 * * 5`), `tz-multi` (`0 7 * * 1,4,6,0`), `tz-wk` (`weekdays`), `tz-odd` (`0 0 */2 * *`): each created, `watch show` printing the raw cron and `watch list` one row each. The worded cards were not driven (no chat create card on the CLI; a timer with no step has no arm card). Evidence: `http://127.0.0.1:8098/vom-nightly-20261104/r1/` (`cli/30-36`, `cli/120-129`, `cli/111-mcp2.json`).*

*Re-driven 2026-11-03 (nightly), tree `777ee7f21` (origin/main, v0.488.0), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 2.8; the first `up` died on a guest sign-in 429 (35 minutes) and the lane booted in 3 s at 19:55Z. On `lane-lifecycle`: create, `edit --classifier-mode accept_all`, show, pause (`enabled:false`), resume, list, `remove --yes` (`removed:true`). `watch create cond-probe --condition` (RSI(14) `lt` 30 on `BINANCE_FUTURES:BTCUSDT`, which then fired every minute at RSI 28.7); `watch state show cond-probe` read `state: null`, `bytes: 0`; `watch state clear` `{"cleared":true,"record_restarts":null}`; `watch state show demo` (a timer) exit 2 `not_a_condition_watch`. Over MCP `watch_state_clear` takes `id` (an `id_or_slug` key is refused `invalid_arguments`). Not re-driven: the journal reads, repair/retry/unjudged, the execute reads, the RPC refusals. Evidence: `http://127.0.0.1:8098/vom-nightly-20261103/r1/` (`cli/90-101`, `cli/32-mcp-post2.json`).*

*Re-driven 2026-11-02 (scheduled maintenance), tree `587ce2d0b` (origin/main, v0.480.3), lane on 18168 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 5. `watch create lane-lifecycle --inbound`, `show`, `edit --classifier-mode accept_all`, `list` (columns `WATCH SOURCES STATUS … LAST FIRE`), `pause` → `Paused event watch lane-lifecycle (lane-lifecycle)`, `resume` → `Resumed event watch …`, `history --format json`, and `watch state show` on the inbound watch → exit 2 `not_a_condition_watch`. Not driven: `remove`, the condition-watch `state` values.*

*Re-driven 2026-11-02 (nightly), tree `2567b7974` (origin/main, v0.480.3), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 4. On `lane-lifecycle`: create, `edit --classifier-mode accept_all --label "Lane Lifecycle Probe"` (slug unchanged), show, pause (`enabled:false`, `held_lots: []`; text `Paused event watch lane-lifecycle (lane-lifecycle)`; `watch show`'s card `Lane Lifecycle Probe · paused`), resume, remove (`removed:true`, `paper_lots_left: []`); `event-journal list` kept `lane-lifecycle` with `watch_id: null`. On the fired `lane-probe`: `journal-stats` (`accepted_total: 2`, `live: 2`), `chapters: []`. On the timer watch `demo`: `retry` and `repair` `working`, `repair --rearm` and `lane retry` exit 2, `unjudged --days 1` `[]`, `reclassify` `watch_reclassify_daemon_running`, `source add … --name t2` then `source remove demo t2 --yes`, `execute history demo` `[]`, `execute summary` zeroed, `watch execute history demo` `No money step`, `backtest spec`, `backtest run nope` and `--window-secs 60` each exit 2. **New: `watch state show` and `watch state clear` (#2244).** On `demo` both refuse exit 2 `not_a_condition_watch` ("watch 'demo' has no condition source"). On an RSI condition watch `cond-probe` (`--condition '{"metric":"rsi","selector":{"market":"BINANCE_FUTURES:BTCUSDT","interval":"HOUR"},"params":{"period":14},"op":"lt","value":30}'`): `state show` returned `states[{source_id, state: null, bytes: 0}]`, `state clear --format json` returned `{"id":"cond-probe","cleared":true,"record_restarts":null}`, `--format text` printed `cleared cond-probe`, and without `--format` the verb prints JSON outside a TTY; `state clear nope` is `watch_not_found`. `record_restarts` `now` and `at_next_arm` need an armed target chain and stay pending. RPC: `overview` 200 `daemon.running: true`, `resolve-attention` 409 `attention_changed`, `arm-confirm` with a non-UUID token 400 `invalid_input`. Evidence: `http://127.0.0.1:8098/vom-nightly-20261102/r1/` (`cli/66-78`, `cli/80-111`).*

*Re-driven 2026-11-01 (nightly), tree `7ce379c45` (origin/main, v0.480.3), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 2.9. On `lane-lifecycle`: create, list, `edit --classifier-mode accept_all --label "Lane Lifecycle Probe"` (the slug stayed `lane-lifecycle`), show, pause (`enabled:false`, `held_lots: []`; the text form printed `Paused event watch lane-lifecycle (lane-lifecycle)` while `watch show`'s card opened `Lane Lifecycle Probe · paused`), resume (`Resumed event watch lane-lifecycle (lane-lifecycle)`), history (`events: []`), remove (`removed:true`, `paper_lots_left: []`, `journal_preserved: true`); `event-journal list` kept `lane-lifecycle` with `watch_id: null`. On the timer watch `demo`: `retry` and `repair` `working`, `repair --rearm` exit 2 `not_a_condition_watch`, `lane retry` exit 2, `unjudged --days 1` `[]`, `reclassify` exit 2 `watch_reclassify_daemon_running`, `source add … --name t2` then `source remove demo t2 --yes`; `execute summary` zeroed, `execute history demo` `{"receipts":[]}`, `watch execute history demo` `No money step`; `backtest spec`, `backtest run nope` and the two stop-breaker refusals each exit 2. On the fired `lane-probe`: `journal-stats` (`accepted_total: 2`, `live: 2`), `chapters: []`, `watch history`. `POST /rpc/v1/watch/overview` `daemon.running: true`; `resolve-attention` 409 `attention_changed`; `arm-confirm` with a non-UUID token 400 `invalid_input` (`token: Invalid UUID; confirmed: Invalid input: expected true`), the schema refusal that precedes the `approval_expired` one the table records for a well-formed unknown token. Evidence: `http://127.0.0.1:8098/vom-nightly-20261101/r1/` (`cli/30-39c`, `cli/87-89f`).*

*Re-driven 2026-10-31 (nightly), tree `dfefe0a21` (origin/main, v0.480.2), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 1.6. Create, list, edit (`accept_all`), show, pause (`enabled:false`, `held_lots: []`), resume, remove (`removed:true`, `paper_lots_left: []`); `event-journal list` kept the removed `lane-lifecycle` with `watch_id: null`. On a timer watch `demo`: `repair --rearm` exit 2 (`no condition source`), `backtest spec --window-secs 60` exit 2 `invalid_backtest_spec_input`. On the fired `lane-probe`: `journal-stats` (`accepted_total: 2`, `live: 2`), `chapters: []`, `watch history`, `execute summary` zeroed, `POST /rpc/v1/watch/overview` (`daemon.running: true`). Evidence: `http://127.0.0.1:8098/vom-nightly-20261031/r1/` (`cli/30-39b`, `cli/87-89e`).*

*Re-driven 2026-10-30 (scheduled maintenance), tree `3cb50a821` (origin/main, v0.478.0), fresh lane on 18165, host load average about 140. `watch pause maint-1030` returned `enabled:false` and `held_lots: []`; a door push to the paused watch got 409; `resume` returned `enabled:true`; `watch history` read. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261030/r1/` (`cli/30-pause.json`).*
*Re-driven 2026-10-30 (nightly, smoke depth), tree `3cb50a821` (origin/main, v0.478.0), lane on 18163: `watch create probe-1030 --inbound`, `edit --classifier-mode accept_all`, `show`, `pause`, `resume` and `list`. `watch pause --format json` now carries `held_lots: []` and `held_lots_error: null`, beside `held_position` and `held_position_error`. `watch remove rm-1030 --yes --format json` carries `paper_lots_left: []` and `paper_lots_left_error: null`. Those fields are new in v0.478.0 (#2208). Four backtest refusals each exited 2: the three new stop-breaker flag refusals and the bare `backtest spec`. Not re-driven: the other maintenance verbs and the journal reads. Evidence is local only (the `8098` renderer did not answer): `artifacts/vom-nightly-20261030/r1/`.*

*Re-driven 2026-10-29 (scheduled maintenance, smoke depth), tree `7ec575e55` (origin/main, v0.467.0 plus #2194), fresh lane on 18161. `watch create --inbound`, `watch edit --classifier-mode accept_all`, `watch pause` (`enabled:false`), `watch resume` (`enabled:true`) and `watch history` (`{watch_id, slug, group, query}`) on `lane-probe`. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261029/r1/`.*

*Re-driven 2026-10-29 (nightly, smoke depth), tree `32ca0d6c7` (origin/main, v0.467.0), lane on 18103: `watch create probe-1029 --inbound`, `edit --classifier-mode accept_all`, and `edit --label "Probe 1029"`. `pause` gave `enabled:false`, with a `watch show` card `Probe 1029 · paused → om watch resume probe-1029`. Then `resume`, `event-journal list` and `search probe`. `watch list --format json` keeps `{folders, revoked, skipped_specs, syncing, unreadable, watches}`. Maintenance verbs were not re-driven. Evidence: `http://127.0.0.1:8098/vom-nightly-20261029/r1/`.*

*Re-driven 2026-10-28 (scheduled maintenance, smoke depth), tree `186030b63` (origin/main): `watch create probe-1028 --inbound`, `edit --classifier-mode accept_all`, `pause` (`enabled:false` on `watch show`), `resume`, `chapters` (empty), `edit --label "Probe 1028"`, `history` and `event-journal list`. Steps not named here keep the record below. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261028/r1/`.*

*Verified: 2026-10-28, tree `a8fa10974` (origin/main, v0.466.0), lane on 18103. The guide's whole sequence was driven: `create --inbound`, `edit --classifier-mode accept_all --label "Lane Lifecycle Probe"` (the result carries the new label), `list`, and `pause`, which printed `Paused event watch lane-lifecycle (lane-lifecycle)`. `watch show` gave `enabled false` with a card `Lane Lifecycle Probe · paused`. The list then read `paused`, since no sync was in flight on this lane. After that came `resume`, `history --kind level` (`No event-watch events`) and `remove --yes` (`history deleted (0 rows); journal files kept`). The journal reads were `event-journal list`, `journal-stats` (`accepted_total 2`) and empty `chapters`. Every row of the maintenance-verb table matched again, with exit 2 on `repair --rearm`, `lane retry` and `backtest`, and exit 1 on `execute digest list`. `watch create --label` is refused (see Pause and resume). Previous stamp `8fe6a8432` is an ancestor (10 commits).*

*Second-pass record: 2026-10-27, tree `8fe6a8432`, lane on 18143.* Re-driven: create → `accept_all` → `event push` (event `16ea1ec5ef28…`), with `watch_committed`/`watch_appended`/`watch_fired` on `/events/v1`. Also re-driven: the journal text, `watch list` `working`, pause/show/resume, `journal-stats`, `chapters`, `event-journal list`, and the door push (202, `578da9324d9c…`) with a rotated token. Maintenance verbs were added above. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261027/r1/` (`pending-rows.txt`).

Watches are the alert engine's unit of work: a label, one or more sources, a
classifier, and somewhere for the fires to go. A user creates one, lists what
exists, reads one in detail, edits it, pauses and resumes it, and removes it.
Every one of those is a local file plus a row in the daemon's store, so the
whole lifecycle is provable on a guest lane.

## Sub-features

- `watch-create` makes a watch on one source (`--inbound`, `--condition`,
  `--every`, `--upstream`, `--stream-ref`).
- `watch-list` shows one row per watch with status and last fire.
- `watch-show` reads one watch: status per part, steps, sources, channel.
- `watch-create` also accepts bands, multiple sources and inline steps; the
  simple inbound recipe does not cover those combinations.
- `event-tools` include `history`, `export`, `backfill`, `reclassify`,
  `rotate-token` and `amend` for stored inbound-watch events. This pass drove
  history and token rotation; the other forms remain unverified.
- `timer-days` (#2284): `watch create <label> --every '<5-field cron>' --tz <zone>` makes a timer on chosen days (`'0 7 * * 5'`, `'0 7 * * 1,4,6,0'`; `--every weekdays|daily|weekly` are words for `0 0 * * 1-5|*|1`). The create, arm and source-add cards (the chat lane) and the sidebar cadence say it in words (`timer, Fridays at 07:00 UTC`, `Mon, Thu, Sat and Sun at 07:00 UTC`, `weekdays at 00:00 UTC`); a cron no rhythm describes stays `timer (cron 0 0 */2 * * UTC)`. The CLI's `watch show` still prints the raw cron: `Reads: clock fires (0 7 * * 5 UTC)`. Asking om chat for "every Friday at 7" composes the same cron (needs a model). Monthly crons (#2300) pass through `--every` too: `'0 9 1,15 * *' --tz Asia/Kuala_Lumpur` and `'0 18 L * *' --tz UTC` are accepted, and the create JSON's `card` reads `timer · monthly on the 1st and 15th at 09:00 Asia/Kuala_Lumpur` and `timer · monthly on the last day at 18:00 UTC`, while `watch show` prints `Reads: clock fires (0 9 1,15 * * Asia/Kuala_Lumpur)`. Every-other-week timers (`every_weeks` 2 to 4 plus an `anchor` date) and a summary on chosen days (`notify.cadence` `{kind:"days"}`) have no CLI flag; they are authored in om chat or as source JSON (source only).
- `upstream-stand-down` (#2310): a chain that reads another watch stands down when that watch is paused or removed. `watch pause <upstream> --format json` carries `readers_stood_down[]` (`{chain_id, watch, has_money, paused, declined, arm_command}`) and `cascade_note` `1 chain reading this watch's rows stood down (<reader>): each waits for its own arm; a resume re-arms nothing.`; the reader's `watch show` heads `<reader> · 2 things need you · source waiting · <upstream> is paused · … · <upstream> is gone · om watch arm <reader>` (the steps row says `is gone` for a pause too). `watch resume <upstream>` returns the same list with `cascade_note` `… is still down from its pause (<reader>): each waits for its own arm.`; `watch arm <reader> <step> --yes` brings it back. On `watch remove <upstream> --yes` a reader whose ONLY source was the upstream is removed with it (`cascade.removed[]` row `via: cascade`, `lost: [<upstream>]`); a reader with another source is repaired (`cascade.repaired[]` with `dropped`, `chains_to_arm`) and listed in `cascade.rearm`, and its `watch show` reads `<upstream> is gone … → om watch arm <reader>`. The non-terminal `remove` refusal (`confirmation_required`) names neither consequence (README gaps).
- `watch-edit` changes goal, group, filters, classifier mode and caps.
- `watch-pause` / `watch-resume` stop and restart a watch and its sources.
- `watch-remove` deletes a watch and its sources.
- Guest-reachable maintenance verbs on a healthy watch: `retry`, `repair`, `source add/remove`, `unjudged`, `state show`/`state clear` on a condition watch (#2244: the clear also restarts a target package's record), the execute reads, the `/rpc/v1/watch/overview` roster; plus the refusals of `repair --rearm`, `lane retry`, `reclassify`, `backtest`, `arm-confirm`, and `state show`/`state clear` on a watch with no condition source.

## How to get to it (user POV)

- `om watch <sentence>` composes a set from natural language (needs a model).
- `om watch create <label> --inbound` builds one directly, no model involved.
- `om watch list`, `om watch show <id>`, `om watch pause|resume|remove <id>`.

## Driving it with control-om

Preconditions:

- A lane the run started. A fresh lane has zero watches — confirm with
  `control-om om -- watch list`, which prints `No watches found.`

- **Create.** Run
  `control-om om -- watch create lane-lifecycle --inbound --format json`.
  Assert `spec_version`, `id`, `enabled: true`, one `sources[]` entry with
  `kind: "inbound"`, and a `card` string. A file appears under
  `.control-om/home-<port>/accounts/guest/watches/` — since `3a81eb478` the
  lane root holds `accounts/`, and the home is the account dir inside it.
- **List.** Run `control-om om -- watch list`. The columns are `WATCH`,
  `SOURCES`, `STATUS`, `CHECKED`, `LAST FIRE`. `CHECKED` (when the daemon last
  read the sources, e.g. `late · 4 min`) is conditional — it renders only while
  some row has words for it — so the column count varies and a positional read
  of "the last column" is unsafe. It is not new; it predates this map.

  **Do not pin the STATUS text.** On a guest lane the cell says the watch has no
  model to judge with, but the words vary for two separate reasons. The part
  label moved from `source` to `steps` in `3a1dea67c`; and two branches then
  coexist, chosen by DAEMON TIMING rather than by version —
  `steps judging paused · no model to run the AI filter on · om init` before the
  daemon's first judge attempt, and
  `steps the AI filter has no model to run on · om init` (plus `· N item(s)
  waiting` once rows are held) after an attempt has actually failed. Both were
  observed in a single pass at v0.408.1 — the first on a just-created inbound
  watch, the second on a feed watch whose source had already been read. A drive can
  land on either without any code changing, and an older build says
  `source judging paused · the classifier is unavailable · om init`. Assert the
  TRANSITION instead — the cell changes once `--classifier-mode accept_all`
  lands — and grep `om init` if you need a stable marker. Whatever it says, it is the missing LLM credential, not the create
  failing: the file is on disk and the daemon knows about it.
- **Show.** Run `control-om om -- watch show lane-lifecycle --format json` and
  assert the source, its classifier and its channel binding.
- **Edit.** Run
  `control-om om -- watch edit lane-lifecycle --classifier-mode accept_all --format json`.
  The result carries an `edited` block naming exactly what changed, and
  `updated_at` moves, and the STATUS cell changes. **Assert that it changed, not
  what it changed to** — the destination is not a contract.

  Worked out the hard way. The same recipe on the same kind of guest lane landed
  on `not read yet` on 2026-09-19 and 09-21, and on `working` (with `LAST FIRE`
  still `never`) twice on 09-24. The code did not change: `not_read_yet` is
  gated on `syncing !== null && notReadYetHere(...)`
  (`actions/watch/list.ts`), and that line is byte-identical across every tree
  involved. `syncing` is non-null only while an account watch-sync is actually
  in flight, so the word is a transient sync indicator, not a lifecycle state —
  which is why the same command yields different cells on different days and why
  an earlier version of this file was wrong twice over: first claiming `working`
  only follows a fire, then explaining the difference as source kind. Neither
  held. Assert the change; grep `om init` while it is unset.

  Re-read with `watch show` to confirm the change is stored, not just echoed.
- **Pause and resume.** Run `control-om om -- watch pause lane-lifecycle`. It
  prints `Paused event watch <id> (<slug>)` — **the parenthesised name is the
  SLUG, not the label** (`renderPaused`/`renderResumed` in `cmd/watch-engine-verbs.ts`). Use a label
  that differs from its slug or the distinction stays invisible. Set it with
  `watch edit <slug> --label "<label>"`, because `watch create … --label`
  exits with `invalid_input` ("--label describe[s] a step"). An edit changes
  the label and leaves the slug, which is derived from the label only at
  create time: label `Lane Lifecycle Probe` on the watch created as
  `lane-lifecycle` prints `Paused event watch lane-lifecycle (lane-lifecycle)`
  (driven 2026-10-28 and 2026-11-01; an older record's `lane-lifecycle-probe`
  was the slug of a watch created under that label). **Assert the
  pause on `watch show`, not on `watch list`**: `watch show <id> --format json`
  carries `spec.enabled: false` and the result's own `card` FIELD opens
  `<label> · paused` (that is `watch show`'s rendered card, not an approval
  card — a bare terminal `om watch pause` raises no confirmation), while
  the list's STATUS cell still reads `not read yet` — the column reports read
  state, not the enabled flag. Note the two surfaces disagree on purpose: the
  lifecycle lines print the SLUG, the card prints the LABEL. Driven with label
  `Lane Lifecycle Probe` on `lane-lifecycle`: `Paused event watch
  lane-lifecycle (lane-lifecycle)` alongside a card opening `Lane Lifecycle
  Probe · paused`. Run
  `control-om om -- watch resume lane-lifecycle`
  (`Resumed event watch <id> (<slug>)`) and confirm `spec.enabled` is back to
  `true`. A watch with attached steps takes an authorization door on resume and
  its receipt gains a `steps running` line, so a bare `--inbound` watch is the
  only shape whose resume output is this short.
  In `--format json`, `watch pause` also reports the paper lots the watch's
  money steps still hold: `held_lots` (`[]` for a watch with no money step)
  and `held_lots_error` (`null` unless the lot read failed). It never reports
  `[]` for a read that did not happen.
- **Remove.** Run `control-om om -- watch remove lane-lifecycle --yes`. It
  prints `Removed event watch <id> (<slug>): history deleted (N rows); journal files kept` — slug again,
  not label. The count is the watch's stored-event count and inflects on exactly
  one: `(1 row)`, but `(0 rows)` and `(2 rows)` — zero takes the plural, so a
  recipe asserting `1 rows` fails. That plain form only holds when no extra
  removal disclosures are
  needed: removal
  appends `destroyed ...`, `paid output gone: ...`, a chart-unbind line, or a
  `warning: N step(s) on another watch read ...` line when any of those apply,
  and a shared watch whose unfollow has not landed prints
  `Unfollow pending for <id> (<slug>): <note>` INSTEAD of the Removed line
  (`removalDisclosure`/`renderRemoved` in `cmd/watch-engine-verbs.ts`). `watch list` is back to `No watches found.` and
  `.control-om/home-<port>/accounts/guest/watches/` is empty — but the journal
  is not gone, which is the point of the trailing clause.
  `--format json` adds `paper_lots_left` (the paper lots the watch hands to
  its accounts, read before they move; `[]` for a watch with no money step)
  and `paper_lots_left_error`.
- **Proof.** Keep the create/edit/show JSON, the `watch list` text before and
  after each transition, and a `ls` of the watches dir at the start and end.
- **Read the journal surface.** With a watch that has accepted rows (the
  `lane-probe` from [event ingest](./event-ingest-and-fire.md) is enough), run
  `control-om om -- event-journal list --format json`, which returns
  `journals[]` of `{slug, watch_id, label}`. A removed watch's journal stays
  listed with `watch_id: null`, which is the `journal files kept` promise made
  visible. Then `control-om om -- watch journal-stats <slug> --format json`
  returns `window_days`, `generated_at` and an `activity` block
  (`accepted_total`, `live`, `relay`, `catchup`, `imported`, `backfill`), and
  `control-om om -- watch chapters <slug> --format json` returns `chapters: []`
  with `developments_folded: 0` on a fresh watch. Chapters need a summary
  fold, which needs a model. `event-journal search <query>` exists
  (`om event-journal search --help`) but was not driven.

### Maintenance verbs on a guest lane (added 2026-10-27)

Seed one timer watch with `control-om om -- watch create demo --every 1h --format json`, which needs no account or LLM. Then:

| Call | Observed |
|---|---|
| `watch retry demo --format json` | status receipt, `status:"working"` |
| `watch repair demo --format json` | `conditions:[]`, `repaired:[]`, `reseeded:[]`, `rearmed:[]`, `status:"working"` |
| `watch repair demo --rearm` | exit 2: "watch 'demo' has no condition source; rearm re-arms a condition's evaluation" |
| `watch lane retry demo` | exit 2: "Event watch 'demo' has no live stream lane, so there is nothing to retry." |
| `watch unjudged --days 1 --format json` | `{"days":1,"since":…,"unjudged":[]}` |
| `watch reclassify demo --format json` | exit 2 `watch_reclassify_daemon_running` (the check runs before the watch lookup) |
| `watch source add demo --source every:2h --name t2 --format json`, then `watch source remove demo t2 --yes` | spec gains, then drops, source `t2` |
| `execute history demo --format json` / `execute summary --format json` / `execute list` | `{"receipts":[]}`, a zeroed summary, "No execution receipts." |
| `watch execute history demo` | `No money step on watch "demo". Nothing has executed for it.` |
| `execute digest list` | `unknown command 'digest'`; the digest's CLI door is unresolved |
| `backtest spec --format json` | exit 2 `invalid_backtest_spec_input` (needs `strategy_slug`, `candidate` or `wrun_strategy`) |
| `backtest run nope --format json` | exit 2 `backtest_target_not_found`, listing the saved watches |
| `backtest spec --window-secs 60 --format json` | exit 2 `invalid_backtest_spec_input`: "set --max-stops and/or --max-loss-usd; --window-secs needs --max-stops." Refused before any strategy or asset check |
| `backtest spec --wrun-strategy @a/b --max-stops x --format json` | exit 2 `invalid_backtest_spec_input`: "--max-stops 'x' is not a finite number." |
| `backtest run nope --window-secs 60 --format json` | exit 2 `invalid_backtest_run_input`, with the same message as `spec`. The flags are refused before the target lookup |
| `POST /rpc/v1/watch/overview` `{}` | `{"ok":true,"data":{"daemon":…,"watches":[…]}}` |
| `POST /rpc/v1/watch/resolve-attention` `{"issue_id":"x"}` | 409 `attention_changed` |
| `POST /rpc/v1/watch/arm-confirm` with an unknown token | 400 `approval_expired` |
| `watch state show demo` / `watch state clear demo` (a timer watch) | exit 2 `not_a_condition_watch`: "watch 'demo' has no condition source" (driven 2026-11-02) |
| `watch state show <condition watch> --format json` | `{"id", "states":[{"source_id", "name", "state": null, "updated_at": null, "bytes": 0}]}` on a never-evaluated rule (driven 2026-11-02 on `cond-probe`, an RSI(14) `lt 30` rule on `BINANCE_FUTURES:BTCUSDT`) |
| `watch state clear <condition watch> --format json` | `{"id", "cleared": true, "record_restarts": null}`; `--format text` prints `cleared <id>`; outside a TTY the bare verb prints JSON. Since #2244 the clear also drops a target chain's record anchor and says when the record restarts (`record_restarts` `now` or `at_next_arm`), which needs an armed target chain (pending) |
| `watch state clear nope` | exit 2 `watch_not_found` |

These prove the verbs answer and refuse correctly on a healthy watch. They do not prove repairing a broken watch, a real backtest, or an approval.

## Gotchas

- `om alert` does not exist. Both alerting kinds are `om watch` now; the
  dashboard's nav item is labelled Watches, at the unchanged route `/alerts`.
- `--classifier-mode` is **not** on `watch create`; it is on `watch edit`,
  `watch backfill` and `watch source add`. Passing it to create fails with `unknown option`.
- `om watch <sentence>` (the composing form) calls a model and asks for
  confirmation. On a guest lane it cannot run — use `watch create`.
- A watch whose source errored lists the part, the why and the fix in one STATUS
  cell, without printing the internal `broken` state name. Read the whole cell
  before reporting a failure; it usually names the credential it wants.
- `watch remove` without `--yes` prompts, and a prompt in a non-interactive
  drive looks like a hang.
- Removal preserves the journal and reserves the slug. A re-create under the
  same label does not start from nothing — check `om event-journal list` before
  concluding a fresh watch inherited state from the change under test.
- Ids are slugs derived from the label. Two creates with the same label collide;
  pick a label unique to the run. Because every lifecycle line prints the slug,
  a slug-shaped label makes the output look like it echoes the label — pick a
  label with spaces or capitals when the proof needs to show which one it is.
- The STATUS vocabulary is wider than this file exercises: `working`, `paused`,
  `broken`, `needs you`, and `waiting` (new, the X free-mirror lane), plus
  `missing` and `stopped` at the edges. Read the cell, do not match a fixed set.
- `pause`, `resume` and `remove` all take several ids at once or `--group
  <name>` for a whole folder, with their own composite confirmation and
  partial-failure exit codes; `remove --force` severs watches whose steps read
  the target. This file drives the single-id form only.
- `watch edit`'s watch argument is now OPTIONAL (`edit [id-or-slug]`): with no
  watch named, `--group <folder>` beside the notify flags bulk-sets delivery for
  every watch in that folder. The single-id form this file drives is unaffected,
  but a typo that drops the id no longer errors — it may edit a whole folder.
- **The CLI is no longer the only front end.** Since v0.400.0 the dashboard
  creates and pauses watches through the same store — see
  [watch authoring](./watch-authoring-ui.md). A watch this file's recipe did not
  create may have been authored there, and a UI-created one lands paused.
- Three verbs landed since this file was written and are not covered here:
  `om watch combine <group-or-ids...> --name <name>` (one head watch reading
  several others, which changes what `pause`/`resume`/`remove` do to the set),
  `om watch preview <watch>` (what the next send would say, sending nothing),
  and `om watch tune <watch-or-folder>` (re-judge this week's rows with hints).
  The plain single-`--inbound` recipe never touches them.
- Removing a SHARED watch tells followers first and is refused outright while
  om cannot reach OpenMarket — unreachable on a guest lane, and not something to
  report as broken from here.
- **OpenFeed receipt wording moved in #2107** (source only, not driven: it needs
  an account with an OpenFeed link). `om watch openfeeds` now says `Feeds: N of
  M in use` (formerly `Slots:`), an OpenFeed `source add` prints `Feed: <meaning>
  · <volume>` (formerly `OpenFeed: <shape> · ...`), and the provenance label is
  `your feed`. A recipe that greps the old words finds nothing.
- **The `watch history` KIND legend changed** at `7a4700048`. `level` now reads
  "a condition watch's level changes, and a package band's row per bar"
  (`om watch history --help`, driven 2026-10-26). A grep for the old wording
  misses it.
- `om watch remove` of a watch that came from an install does NOT retract that
  install's registry receipt. Only `om uninstall` and a person's own unfollow
  queue a retraction, and only for an account (#1947, source only). See
  [registry welcome and search](./registry-welcome-and-search.md).
