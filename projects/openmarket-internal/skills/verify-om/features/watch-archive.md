# Watch archive and the auto-archive sweep

*Re-driven 2026-11-11 (nightly), tree `0ad4768f66` (origin/main, v0.494.0), guest lane on 18181, booted with no guest 429. `watch archive` (`Undo: om watch unarchive <id>`), `watch list --archived` (`archived 2026-11-11 · by you`), `watch unarchive` (`paused`, with the resume line). The `watch-archive` lane read `ok` on `/healthz`. Not re-driven: the sweep. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261111/r1/`.*

*Re-driven 2026-11-10 (nightly), tree `c9bc93a355` (origin/main, v0.493.1), guest lane on 18143. `watch archive lane-quiet` (`Archived lane-quiet (lane-quiet)`, `Undo: om watch unarchive <id>`), `watch list --archived` (`lane-quiet  lane-quiet  inbound  archived 2026-11-09 · by you`), `watch remove` on it exits 2 `not removed: it is archived`, `watch unarchive` (`Unarchived lane-quiet: paused`, `Resume: om watch resume lane-quiet`), then remove. The list's reason word for a manual archive is `by you` (`ARCHIVE_REASON_WORDS`, `cmd/watch-verbs.ts:3552`; JSON keeps `reason: manual`); the map said `manual`. The sweep is not driven. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261110/r1/` (`cli/wa-*.txt`).*

*Re-driven 2026-11-09 (scheduled maintenance), tree `0d3d29cd27` (origin/main, v0.493.0), bare lane on 18145 (dummy `OM_API_KEY`, dead service URLs) with a scripted fake model on 18144. `watch archive lane-probe` (`Archived … Undo: om watch unarchive <id>`), `watch list --archived` (`archived 2026-11-09 · by you`), `watch unarchive lane-probe` (`Unarchived lane-probe: paused`). `watch archive` takes no `--yes` (`unknown option`). The reboot sweep was not re-driven. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261109/r1/`.*

*Re-driven 2026-11-09 (nightly), tree `5bfa0ccf6` (origin/main, v0.492.0), guest lane on 18143, booted with no guest 429. `watch archive`, `list --archived`, `unarchive` (lands `enabled: false`), then remove. The auto-archive sweep is not driven. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261109/r1/` (`cli/24-29`).*

*Re-driven 2026-11-08 (nightly), tree `5590b4d1c` (origin/main, v0.492.0), guest lane on 18141, booted in 2 s with no guest 429. `watch archive lane-quiet` (`archived[]`, `refused: []`), `watch list --archived`, `watch unarchive` (`enabled:false`). Not re-driven: the reboot sweep and `watch.auto_archive`. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261108/r1/` (`cli/75-77`).*

*Re-driven 2026-11-07 (nightly), tree `05f450fc5` (origin/main, v0.492.0), guest lane on 18141, booted with no guest 429. `watch archive lane-quiet` `{archived:[…], refused:[]}`, `watch list --archived` (`reason: manual`, `by: you`), `watch unarchive` `enabled:false`, `config get watch.auto_archive` default `on`. Not re-driven: the sweep. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261107/r1/` (`cli/25-29`).*

*Re-driven 2026-11-06 (nightly) on main, tree `50fcc594b` (origin/main, v0.492.0; #2357 squashed as `9bbf2de24`), guest lane on 18163, booted at 19:18Z with no guest 429; a guest lane boots fine when the guest sign-in answers. Driven: `config get watch.auto_archive` (`unset (default: on)`); the sweep on reboot after a rewind, which logged `auto-archive archived 1, refused 1 (probe-upstream: watch_has_consumers)` and held the notice `Archived 1 unused watch` (`Paused 30+ days: 1`, `See:`, `Undo:` rows); `watch list --archived`; `watch archive probe-upstream probe-quiet` (one archived, one refused, exit 1); `watch remove` on an archived id (exit 2); `watch unarchive`; MCP `watch_unarchive`. Not reproduced: the finished-7-days branch (an expired once-condition was kept; README, known product gaps). Not driven: a delivered notice, any archived view in the TUI or GUI. Evidence: `http://127.0.0.1:8098/vom-nightly-20261106/r1/` (`cli/arch-*`, `cli/mcp-stdio.jsonl`).*

*Verified 2026-11-05 on branch `daryl/watch-archive-sweep` (PR #2357, tree `33bd51ea2` over main `a0a8c7b8b`, v0.492.0), bare lane on 18103, source build: the sweep archived 2 (a paused watch and a finished once-condition) and refused 1. Evidence: `http://127.0.0.1:8098/watch-archive-sweep/r1/`*

`om watch archive <id...>` pauses each watch and moves it out of the live list
into an archive. `om watch unarchive <id>` brings it back, paused. `om watch
list --archived` shows the archive with who archived each watch and why. Once a
day the daemon archives watches paused 30+ days with no fire, and watches whose
every source ended 7+ days ago, and holds one notice listing them. A watch that
another watch reads is never archived. `watch.auto_archive off` turns the sweep
off.

## Sub-features

- `archive`: `watch archive <id...>` moves `watches/<id>.json` to
  `watches/archive/<id>.json`. A watch with readers is refused `Not archived
  <id>: read by <reader>` / `Fix: archive or edit <reader> first`; the command
  exits 1 when any id is refused and ends with `Undo: om watch unarchive <id>`.
- `unarchive`: `watch unarchive <id>` answers `Unarchived <id>: paused` and
  `Resume: om watch resume <id>`.
- `list`: `watch list --archived` prints `<id>  <label>  <kinds>  archived
  <date> · <reason>` (`by you`, `paused 30+ days`, `finished 7+ days`), then `Unarchive: om watch
  unarchive <id>`. JSON puts them under `archived[]` with `{at, by, reason}`.
- `remove-guard`: `watch remove <archived id> --yes` exits 2 `not removed: it
  is archived` with `om watch unarchive <id>, then remove it`.
- `sweep`: the housekeeping tick runs it once per 24 h, gated by the settings
  row `watch_archive_sweep_at`. It skips package, paper-desk and money-step
  watches and broken running ones (`runner/watching/archive-sweep.ts:20-100`).
- `notice`: one held or delivered notice, `Archived N unused watch(es)`, with
  a row per reason, `See: om watch list --archived` and `Undo: om watch
  unarchive <id>`.
- `mcp`: `watch_archive` and `watch_unarchive` are on MCP stdio.

## How to get to it (user POV)

Run `om watch archive <id>` on a watch you no longer use, or leave the daily
sweep on. `om watch list --archived` shows what went, and `om notis` the
sweep's notice. There is no archived view in om chat or the dashboard.

## Driving it with control-om

Preconditions: a lane the run started. The first boot's empty sweep stamps the
gate, so the sweep needs its clocks rewound with the lane stopped.

1. Seed through the lane CLI: `--inbound` watches `probe-paused`,
   `probe-upstream` and `probe-quiet`; `probe-reader --upstream
   probe-upstream`; a once condition with `--once --expires <future>`
   (`probe-finished`). Pause `probe-paused` and `probe-upstream`. Put the
   commands in a script under the scratch folder: inline JSON in a
   `control-om` call trips the worktree guard in an isolated session.
2. `control-om down`, then with a scratch Bun script against
   `.control-om/home-<port>/accounts/guest/`:
   - set `updated_at` 31 days back in `watches/probe-paused.json` and
     `watches/probe-upstream.json`;
   - set the condition source's `expires_at` 8 days back in
     `watches/probe-finished.json`;
   - set `watch_archive_sweep_at` in `om.sqlite`'s `settings` 25 h back.
3. `control-om up` again. Within seconds the lane log has `auto-archive archived
   N, refused 1 (probe-upstream: watch_has_consumers)` and `watches/archive/`
   holds `probe-paused`. On the branch run N was 2 with `probe-finished`; on
   main tonight it was 1.
4. `control-om om -- notis` shows the held notice; `watch list --archived`
   shows `probe-paused … paused 30+ days`.
5. `watch archive probe-upstream probe-quiet` archives one and refuses one
   (exit 1). `watch remove probe-paused --yes` exits 2. `watch unarchive
   probe-paused` answers `Unarchived probe-paused: paused`.

## Gotchas

- The kernel logs an archive move as `removed <id> (watch_archive, mutation
  kernel)`. That is the move, not a delete.
- The sweep runs within a second of boot. An enabled condition watch whose
  facts are not read yet is kept (`unread`), which may be why the rewound
  condition stayed live on main; rewinding its file did not make `watch show`
  read it as ended.
- A paused upstream still has readers, so the sweep refuses it by design.
- The dashboard on a source lane without `bun run build:dashboard` shows only
  the stub page, so it is no evidence for this surface.
