# Watch lifecycle from the CLI

*Verified: 2026-09-21, tree `b46838460` (v0.390.1) — create/list/show/edit/pause/resume/remove driven with a label that diverges from its slug.*

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
- `watch-edit` changes goal, group, filters, classifier mode and caps.
- `watch-pause` / `watch-resume` stop and restart a watch and its sources.
- `watch-remove` deletes a watch and its sources.

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
  `steps the AI filter has no model to run on · om init` (plus `· N items
  waiting` once rows are held) after an attempt has actually failed. A drive can
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
  `updated_at` moves. `watch list` now reads `not read yet` — the clean
  before/after pair for this transition, and NOT `working`, which this watch
  only reaches after its first fire. Re-read with `watch show` to confirm the
  change is stored, not just echoed.
- **Pause and resume.** Run `control-om om -- watch pause lane-lifecycle`. It
  prints `Paused event watch <id> (<slug>)` — **the parenthesised name is the
  SLUG, not the label** (`cmd/watch-engine-verbs.ts:3285-3297`). Use a label
  that differs from its slug or the distinction stays invisible: label
  `Lane Lifecycle Probe` prints
  `Paused event watch lane-lifecycle-probe (lane-lifecycle-probe)`. **Assert the
  pause on `watch show`, not on `watch list`**: `watch show <id> --format json`
  carries `spec.enabled: false` and the result's own `card` FIELD opens
  `<label> · paused` (that is `watch show`'s rendered card, not an approval
  card — a bare terminal `om watch pause` raises no confirmation), while
  the list's STATUS cell still reads `not read yet` — the column reports read
  state, not the enabled flag. Note the two surfaces disagree on purpose: the
  lifecycle lines print the SLUG, the card prints the LABEL. Driven with label
  `Lane Lifecycle Probe`: `Paused event watch lane-lifecycle-probe
  (lane-lifecycle-probe)` alongside a card opening `Lane Lifecycle Probe ·
  paused`. Run
  `control-om om -- watch resume lane-lifecycle`
  (`Resumed event watch <id> (<slug>)`) and confirm `spec.enabled` is back to
  `true`. A watch with attached steps takes an authorization door on resume and
  its receipt gains a `steps running` line, so a bare `--inbound` watch is the
  only shape whose resume output is this short.
- **Remove.** Run `control-om om -- watch remove lane-lifecycle --yes`. It
  prints `Removed event watch <id> (<slug>); journal preserved` — slug again,
  not label. That plain form only holds for a fresh watch with no fires: removal
  appends `destroyed ...`, `paid output gone: ...`, a chart-unbind line, or a
  `warning: N step(s) on another watch read ...` line when any of those apply,
  and a shared watch whose unfollow has not landed prints
  `Unfollow pending for <id> (<slug>): <note>` INSTEAD of the Removed line
  (`cmd/watch-engine-verbs.ts:3305-3385`). `watch list` is back to `No watches found.` and
  `.control-om/home-<port>/accounts/guest/watches/` is empty — but the journal
  is not gone, which is the point of the trailing clause.
- **Proof.** Keep the create/edit/show JSON, the `watch list` text before and
  after each transition, and a `ls` of the watches dir at the start and end.

## Gotchas

- `om alert` does not exist. Both alerting kinds are `om watch` now; the
  dashboard's nav item is labelled Watches, at the unchanged route `/alerts`.
- `--classifier-mode` is **not** on `watch create`; it is on `watch edit` and
  `watch backfill`. Passing it to create fails with `unknown option`.
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
- Three verbs landed since this file was written and are not covered here:
  `om watch combine <group-or-ids...> --name <name>` (one head watch reading
  several others, which changes what `pause`/`resume`/`remove` do to the set),
  `om watch preview <watch>` (what the next send would say, sending nothing),
  and `om watch tune <watch-or-folder>` (re-judge this week's rows with hints).
  The plain single-`--inbound` recipe never touches them.
- Removing a SHARED watch tells followers first and is refused outright while
  om cannot reach OpenMarket — unreachable on a guest lane, and not something to
  report as broken from here.
