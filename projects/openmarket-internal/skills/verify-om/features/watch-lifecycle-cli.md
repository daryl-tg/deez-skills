# Watch lifecycle from the CLI

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
- `watch-edit` changes goal, group, filters, classifier mode and caps.
- `watch-pause` / `watch-resume` stop and restart a watch and its sources.
- `watch-remove` deletes a watch and its sources.
- Guest-reachable maintenance verbs on a healthy watch: `retry`, `repair`, `source add/remove`, `unjudged`, the execute reads, the `/rpc/v1/watch/overview` roster; plus the refusals of `repair --rearm`, `lane retry`, `reclassify`, `backtest` and `arm-confirm`.

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
  exits with `invalid_input` ("--label describe[s] a step"). Label
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
| `POST /rpc/v1/watch/overview` `{}` | `{"ok":true,"data":{"daemon":…,"watches":[…]}}` |
| `POST /rpc/v1/watch/resolve-attention` `{"issue_id":"x"}` | 409 `attention_changed` |
| `POST /rpc/v1/watch/arm-confirm` with an unknown token | 400 `approval_expired` |

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
