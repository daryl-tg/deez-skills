# A timer checks your own numbers

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

## Gotchas

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
