# Calendar scheduling and polling windows

*Verified: 2026-10-07, tree `03bd55226` (v0.432.0) — empty guest calendar listed; feed polling policy and bounded window set/list/cancel/re-read. Occurrence actions and recurring/policy boundary branches remain unverified.*

`om calendar` lists and manages scheduled occurrences, while `om watch window`
sets bounded read windows on sources with a polling policy. The calendar needs
occurrences before its selection and review actions have anything to operate on.

## Sub-features

- `calendar-list` reads stored occurrences and their current state.
- `calendar-review` shows an occurrence, its links and available choices, then
  selects, rejects or revises it.
- `polling-policy` adds a default cadence and read limits to a polled source.
- `polling-window` schedules, lists and cancels a source's bounded reads.

## How to get to it (user POV)

- Run `om calendar list` to see scheduled occurrences.
- Set a polling policy on a watch source, then run `om watch window set` to
  choose when that source may be read.
- Use `om watch window list` and `om watch window cancel` to review or cancel
  a scheduled window.

## Driving it with control-om

Preconditions:

- A lane the run started. A guest lane can list an empty calendar and configure
  source polling windows without an LLM credential.
- The selected watch source must support polling. `watch window set` refuses a
  source without a polling block.

1. Run `control-om om -- calendar list --format json`. A fresh guest lane returns
   an empty `occurrences` and `events` array; calendar review actions need a
   selected occurrence and are not proved by this empty result.
2. Create or use a polled feed source. Add a policy with
   `control-om om -- watch edit <watch> --source-id <source-id> --polling-json
   '<policy-json>' --format json`. A minimal policy is
   `{"default":{"every_sec":60},"bounds":{"fastest_sec":60,"max_window_sec":7200,"max_extension_sec":1800,"max_daily_reads":240,"max_concurrent_windows":2}}`.
3. Re-read `watch show <watch> --format json` and confirm the selected source
   stores the `polling` block.
4. Set a window with future UTC instants:

   ```sh
   control-om om -- watch window set <watch> <source-id> \
     --start <start-iso-utc> --end <end-iso-utc> \
     --every 60 --origin verify-window --format json
   ```

5. Run `watch window list <watch> <source-id> --format json`. Confirm the
   window id, UTC bounds, cadence and `scheduled` state.
6. Cancel by source and origin with
   `watch window cancel <watch> --source <source-id> --origin verify-window
   --format json`; list again and confirm the row remains with state `cancelled`.

The 2026-10-07 guest-lane drive used the `maint-oct-07-origin` RSS source. It
confirmed the stored policy and the scheduled-to-cancelled transition. It did
not wait for the scheduled window to run.

## Gotchas

- Set a polling block before scheduling a window. The policy's bounds limit
  cadence, duration, extensions, daily reads and concurrent windows; invalid
  values are refused rather than clamped.
- The operator can list an empty calendar on a guest lane, but selecting,
  rejecting or revising an occurrence was not reachable because no occurrence
  existed.
- A scheduled window is not proof that a poll ran. This drive cancelled its
  future window before its start time.
