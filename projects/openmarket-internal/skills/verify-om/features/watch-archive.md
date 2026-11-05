# Watch archive and the auto-archive sweep

*Verified 2026-11-05 on branch `daryl/watch-archive-sweep` (PR #2357, tree `33bd51ea2` over main `a0a8c7b8b`, v0.492.0), lane on 18103, source build. Not on main yet: re-prove after #2357 lands. Driven: the daemon sweep on reboot, `watch archive` with one refusal, `watch remove` on an archived id, `watch unarchive`, `watch list --archived`, `config get watch.auto_archive`. Not driven: the TUI and GUI (no archived view exists), a delivered notice (the lane had no channel, so it stayed held). Evidence: `http://127.0.0.1:8098/watch-archive-sweep/r1/`.*

## What it is

- `om watch archive <id...>` pauses each watch, then moves `watches/<id>.json` to `watches/archive/<id>.json`. No live reader looks in the subfolder.
- `om watch unarchive <id>` moves it back paused, with `updated_at` restamped.
- `om watch list --archived` (`watch_list` `archived: true`) lists the archive with who archived each and why.
- The `watch-archive` daemon lane runs on the housekeeping tick, gated to once per 24 h by the settings row `watch_archive_sweep_at`. It takes a watch paused 30+ days with no fire, or one whose every source ended 7+ days ago. `watch.auto_archive` (default on) turns it off.

## Recipe

1. The lane must boot with no guest mint: `--env OM_API_KEY=om_dummy_proto` plus every service URL at `http://127.0.0.1:9` (see the bare-lane recipe). A keyless lane died after its banner on a guest 429.
2. Seed through the lane CLI: two `--inbound` watches paused (`probe-paused`, `probe-upstream`), one running (`probe-quiet`), `probe-reader --upstream probe-upstream`, and a once condition with `--once --expires <future>` (`probe-finished`).
3. `control-om down`, then rewind with a scratch Bun script against the lane home:
   - `updated_at` 31 days back on the two paused watches;
   - the condition source's `expires_at` 8 days back;
   - `watch_archive_sweep_at` in `om.sqlite` `settings` 25 h back.
   The first boot's empty pass already stamped the gate, so without the rewind the sweep waits a day.
4. `control-om up` again. Within seconds the lane log reads `auto-archive archived 2, refused 1 (probe-upstream: watch_has_consumers)`. `watches/archive/` holds `probe-paused` and `probe-finished`.
5. The digest is in `undelivered_notices` and `notis_notices` (`held`): `Archived 2 unused watches`, `Paused 30+ days: 1`, `Finished 7+ days: 1`, `See:` and `Undo:` rows.
6. `watch archive probe-upstream probe-quiet` archives one and refuses one (exit 1). `watch remove probe-paused --yes` on an archived id refuses `it is archived` (exit 2). `watch unarchive probe-paused` answers `Unarchived probe-paused: paused`.

## Gotchas

- The kernel logs an archive move as `removed <id> (watch_archive, mutation kernel)`. That is the move, not a delete.
- `control-om` calls with JSON or computed values trip the worktree guard in an isolated session. Put the seed steps in a script under `.control-om/` and run `bash .control-om/<script>.sh`.
- The dashboard on a source lane without `bun run build:dashboard` shows only the stub page, so it is no evidence for this surface.
