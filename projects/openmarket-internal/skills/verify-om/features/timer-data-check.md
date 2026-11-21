# A timer checks your own numbers

*Re-driven 2026-11-22 (nightly), tree `01482928a5` (origin/main, v0.496.0+internal), guest lane on 18188 through `bootstrap.internal.ts`. Steps 2, 3 and 6 without a channel: `event push steps-1122 --values '{"steps": 8412}'`, a per-minute check `lt 10000` with `within: 1d`; `watch preview` read `Would send: steps 8,412, below 10,000`; after one slot `watch show` read `Last check: 19:39 UTC, steps 8,412, below 10,000`; a check on a watch the home lacks exits 2 `watching_unknown_upstream` with the `Push the number into a watch first` hint. Not re-driven: deliveries, the quiet slot, the missing-data notice, import, a feed read. (`cli/87-*`.) Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261122/r1/`*

*Re-driven 2026-11-21 (nightly), tree `3c4839c59d` (origin/main, v0.496.0+internal), guest lane on 18188 through `bootstrap.internal.ts`. Steps 2 to 4 with no webhook: the data watch `steps` (`--inbound --paused`, `accept_all`, resumed, one push with `--values '{"steps": 8412}'`), the check watch on `* * * * *`, one fire in `watch history steps-check` titled `steps 8,412, below 10,000`, `watch preview` `Would send: steps 8,412, below 10,000`, and the unknown upstream refusal `watching_unknown_upstream`. Not re-driven: delivery to a channel, quiet and holding slots, pause and resume, the feed read, the missing-data notice. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261121/r1/` (`cli/c0-*`).*

*Verified: 2026-11-20, merged main `2d01b6b5d4` (#2642 adds a feed as a check's read), real relay `9199a77`. Lane on 18161, hand-started on `bootstrap.internal.ts`, signed in to the made-up account `@rig`, with a webhook listener on 18168. Driven: a per-minute check reading `@rig/agent.<name>` that fired once per reading (three fires, three deliveries, no repeat), its `cursor_ts`, quiet and missing slots, the missing-data notice for a check alone in its tick, pause, and a check the assistant door made behind the owner's card. One defect found: when two or more checks open a missing episode in the same tick, only one is told (Gotchas). Not re-driven on main: `preview`, `edit`, `--clear-check`, remove then import, a source-read check. Evidence root `~/Documents/dev-notes/om-2026-11-20-e2e-verify/run-artifacts/s5/` (`evidence/c7-*`, `evidence/x1-*`, `rig/`). Gallery `http://127.0.0.1:8098/om-1120-e2e/s5/`.*

*Re-driven 2026-11-12 (nightly) on main, tree `82094c3a83` (origin/main, v0.495.0+11; merged as `74ca42aeed`, #2463). Bare lane on 18193 (dummy `OM_API_KEY`, dead service URLs) with a loopback webhook listener on 18194. Driven: `setup webhook`, the data watch and a push of 8,412, create with `--check` (`Check: steps below 10,000 (last over 1d, from steps)`), the new unknown-upstream refusal, `preview` (`Would send: steps 8,412, below 10,000`), two holding slots each delivered as `🔔 Steps check` with `steps 8,412, below 10,000`, a push of 12,034, `preview` (`Would stay quiet: steps 12,034, not below 10,000`), one quiet `irrelevant` slot and no POST for it, `watch list` (`2 sources · every minute, if steps below 10,000`) and `watch show`. Not re-driven on main: pause and resume, the missing-data notice, remove then import, `--clear-check`. The host deep-idled between dark wakes for the first 17 minutes, so slots 21:01 to 21:16 UTC did not run; see Gotchas. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261112/r1/` (`cli/timer-*.txt`).*

*First verified: 2026-11-11 on branch `daryl/timer-data-check` (`b1cb7b34ee` over `f98a580314`), on a bare lane with a webhook listener: the full recipe below. Evidence: `http://127.0.0.1:8098/om-scheduled-data-check/r1/`.*

A timer source can carry a `check`: a rule over numbers another source of the
same watch holds. At each slot om reads the numbers as of the slot and runs the
rule with no model call. A slot whose rule holds sends one sentence and starts
the watch's steps. Any other slot is a quiet history row. When the numbers stop
arriving, one notice goes out per episode.

## Sub-features

- `create`: `watch create <label> --every <cadence> --tz <zone> --source
  context:upstream:<watch> --check '<json>'` prints `Check: steps below 10,000
  (last over 1d, from steps)`. The JSON is a bare rule or `{rule, read,
  on_missing}`.
- `holds`: the slot's row is `update`, titled `steps 8,412, below 10,000`, and
  the channel receives `🔔 <label>` with that sentence.
- `quiet`: the slot's row is `irrelevant`, titled `Checked: steps 12,034, not
  below 10,000`. Nothing is sent.
- `missing`: the row is titled `No steps reading from <source> since <Mon D
  HH:MM>`, and one `⚠️ <label>: check has no reading` notice is sent per
  episode.
- `feed-read` (#2642): a check's read can name a relay feed, `read: {"<key>": {"feed": "@<scope>/<name>"}}`.
  - Each slot reads the rows after the check's cursor, up to the slot: the relay logs `rows?after_ts=<cursor>&to=<slot>`.
  - A new reading is judged once. The slot after it has no row to judge.
  - The cursor is `cursor_ts` in `watch_history.context.check.readings[]`.
  - A slot with no new row is an `irrelevant` row titled `No <key> reading from @<scope>/<name> since <Mon D HH:MM>`.
  - The assistant door writes the read as `{feed, key, take: "last"}` with `on_missing: "tell"`.
- `first-slot`: a new, resumed or re-timed timer runs at its next slot, never
  for a slot before it existed.
- `words`: `watch list` shows `2 sources · every minute, if steps below
  10,000`; `watch show` shows `Reads: clock fires (...), and counts only if
  steps below 10,000` and `Last check: HH:MM UTC, ...`.
- `preview`: `watch preview <watch>` prints `Would send: ...`, `Would stay
  quiet: ...` or `Would warn once: ...`, and writes no row.
- `edit`: `watch edit <watch> --check '<json>'` and `--clear-check`.
- `refusals`: `--check` on a source that is not a timer, `watch source remove`
  of a source a check reads, and an edge operator in a check each exit 2.
  Since the merge, a check that reads a watch this home does not hold exits 2
  too: `The check reads steps from "nosuch", a watch this home does not hold.`
  / `Push the number into a watch first: om watch create "nosuch" --inbound,
  then om event push.` (live 2026-11-12).
- `import`: remove then `watch import <spec file>` re-points the check's read
  to the newly minted source id.

## How to get to it (user POV)

Push numbers into an inbound watch, then create a second watch with a timer, a
`--check`, and the first watch as a context source. `om watch preview` tries it
at once. `om watch history` shows one row per slot.

## Driving it with control-om

Preconditions: a lane the run started, with `OM_LANE_PORT` exported. A bare
lane is enough: nothing here needs an account or a model. To see deliveries,
start a loopback HTTP listener on a second agent port and add it as a channel.

1. `control-om om -- setup webhook --name desk --webhook-url
   http://127.0.0.1:<hook-port>/hook --allow-private-network --format json`.
2. Data watch: `watch create "Steps" --slug steps --inbound --paused`, `watch
   edit steps --classifier-mode accept_all --no-notify`, `watch resume steps`,
   `event push steps --text "<unique>" --values '{"steps": 8412}'`.
3. Check watch: `watch create "Steps check" --every "* * * * *" --tz UTC
   --source context:upstream:steps --check
   '{"rule":{"metric":"steps","op":"lt","value":10000},"read":{"steps":{"source":"steps","within":"1d"}}}'
   --notify-channel desk`. A per-minute timer's default window is one minute,
   so name `within` for a lane.
4. Wait past the next minute. `watch history steps-check` has an `update` row
   and the listener has one POST titled `🔔 Steps check`.
5. Push `{"steps": 12034}`, wait two slots. `watch history steps-check
   --outcome irrelevant` has `Checked: ...` rows and the listener has no new
   POST.
6. `watch list`, `watch show steps-check`, `watch preview steps-check`.
7. `watch pause steps-check`, wait two slots (no new row), `watch resume`,
   wait one slot (a new row).
8. `watch edit steps-check --check` with `"within":"1m"`, push nothing, wait
   four slots: four `No steps reading` rows and exactly one `check has no
   reading` POST.
9. Save `.spec` of `watch show steps-check --format json` to a file, `watch
   remove steps-check --yes`, `watch import <absolute path>`, `watch preview`.

### A check that reads a feed

Needs a signed-in lane and a relay, not a bare lane. The rig is in [feed-quiet-notices-and-rules.md](feed-quiet-notices-and-rules.md), and `bin/om` below is its CLI wrapper.

1. `bin/om feed append agent.<name> --values '{"mood":44}' --cadence 1m --title '<t>'`.
2. `bin/om watch create '<label>' --slug <slug> --every '* * * * *' --tz UTC --check '{"rule":{"metric":"mood","op":"lt","value":20},"read":{"mood":{"feed":"@rig/agent.<name>"}}}' --notify-channel desk`.
3. Push three readings below 20 at chosen moments. `rig/c7-drive.sh` in the 2026-11-20 evidence root is the schedule:
   - a row stamped exactly on a minute and pushed 5 s after that tick fires once at the next slot;
   - a row stamped exactly on a minute and pushed 10 s before the tick fires once at that slot;
   - a row stamped 30 s before a minute and pushed 20 s after the tick fires once at the next slot.
4. Stamp a row with `--rows '[[<ts>,11]]' --columns mood`.
5. Read `watch_history` from the lane's sqlite, one row per slot, with `cursor_ts`. See three `update` rows titled `mood 11, below 20` and so on, and no `update` in the slot after each.
6. The listener has three posts. The relay log's `after_ts` and `to` values agree with the stored cursors.

## Gotchas

- **Defect: a `check has no reading` notice is never sent when two or more checks open a missing episode in one tick.**
  - Repro: a signed-in lane, a webhook channel `desk`, a feed `agent.<name>`. Create two or more per-minute checks on the same feed, by `om watch create … --check` or by the assistant door's `create_watch` with `feed_check` and `om approve`. Append one reading, then push nothing. Wait two slots.
  - Seen with three watches at one slot: all three wrote a `missing` row with `notice_owed: true`. Only the last clock in the tick's scan order was told. The other two wrote `notice_owed` on every later slot and sent nothing for 18 slots, with `errors=[]` in each tick log line and no `notis_notices` or outbox row. Seen with two watches too, where one was never told across 40 slots, a pause and resume, and a daemon restart.
  - Alone in its tick, each watch is told at once.
  - Expected: each watch gets its one notice per episode.
  - Cause: not traced. A read-only probe of the stuck clock (`rig/probe-owed.ts`) finds every precondition of `sendOwedMissingNotice` true (`packages/cli/src/runner/timers/tick.ts:1585`), yet the send is never reached and `notice_told_at_ms` is never set. The state is in the store, since it survives a restart. The lead read `tick.ts:1502-1660` (`owedNoticeClocksByHome`, `sendOwedMissingNotice`) and found no logged error.
  - The code is from #2463 (`74ca42aeed`), not #2642. Whether two source-read checks do the same was not tested.
  - Evidence `evidence/x1-missing-notice-owed.txt`, `evidence/x1-digest.txt`, `evidence/c7-history.txt`.
  - Step 8 above still holds with one check in the tick.
- A 1 m feed check warns after every gap. Any slot with no new row is a `No <key> reading` row, and each gap is its own episode. One check sent six warnings in 14 slots while readings arrived five times. The assistant door offers `every: 1m`, and the Grok recipe's fastest routine is 5 minutes.
- Put every command that carries `--source` or inline JSON in a script file.
  An isolated session's worktree guard refuses them inline.
- A push takes about a second to commit, so a preview run straight after
  `event push` can still read the previous value.
- Quiet rows are not on the default `watch history` page of a watch with no
  upstream source. Use `--outcome irrelevant`.
- After remove and import the watch is a new one with no history, so a
  missing-data notice goes out once more.
- `watch import` takes an absolute path when driven through `control-om`,
  which runs from the repo root.
- The dashboard on a source lane is the stub page, so it is no evidence here.
  Render the CLI transcripts to frames for the gallery.
- The listener's first POST is the channel's own setup test.
- A per-minute timer runs only while the host is awake. On 2026-11-12 the mini deep-idled between dark wakes about 17 minutes apart; the timer ran the 21:00 slot and then the 21:17 slot, with nothing between. Hold `caffeinate -i -s -t <seconds>` for the drive (and stop it after) before counting slots.
