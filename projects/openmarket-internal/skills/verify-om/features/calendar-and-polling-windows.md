# Calendar scheduling and polling windows

*Verified: 2026-10-22, tree `db6e76ef5` (origin/main, v0.460.0): occurrence `cocc_ec41afe3ecff5b96ebb91c0a` was admitted through `event push --kind calendar_candidate` and listed as `scheduled`/`candidate`/revision 1. `show` gave keys decisions, event, links, occurrence, revisions, selections and windows. `select` gave `{ok:true,watch_id,occurrence_id,decision:"selected",change_seq:2}`, and `revise --status cancelled` gave `changed:true`, revision 3, with list `cancelled`. Polling windows on a feed source: `--polling-json` stored the block, `window set` gave `state:"scheduled"`, `window cancel --source --origin` gave `cancelled:true`, and a 4 h window was refused naming `polling.bounds.max_window_sec (7200)`. Previous stamp `7e22214fb` is on branch `daryl/watch-narrative`, not an ancestor of main.*

`om calendar` lists and manages scheduled occurrences, while `om watch window`
sets bounded read windows on sources with a polling policy. The calendar needs
occurrences before its selection and review actions have anything to operate on
— and the way to get one on a guest lane is the same inbound door
[event ingest](./event-ingest-and-fire.md) already proves, which is what makes
this whole guide drivable without an account.

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

- A lane the run started. **No account and no LLM credential are needed.** The
  `calendar` command group is wrapped in `requireAuth`, but that is a no-op
  today — a guest credential mints silently on first use, and the real gate
  (`requireNonGuest`) is never applied here. The only real prerequisite is that
  an occurrence exists.

### Admit an occurrence, then review it

A `calendar_candidate` block rides the ordinary inbound push door
(`runner/calendar/blocks.ts`), so one watch and one push is the whole setup:

```bash
control-om om -- watch create calendar-probe --inbound --format json
control-om om -- event push calendar-probe \
  --kind calendar_candidate --text "calendar probe" \
  --calendar-candidates '[{"provider":"verify-om","provider_event_id":"verify-1",
    "provider_occurrence_id":"verify-1-occ","title":"Verify calendar candidate",
    "kind":"macro.release","scheduled_at_ms":<future-epoch-ms>,
    "evidence_url":"https://example.com/verify"}]' \
  --format json
```

`--text` is required whatever the kind, and `evidence_url` must be https.

- **List.** `control-om om -- calendar list --format json` returns the
  occurrence with `status: "scheduled"`, `event_status: "candidate"`,
  `revision: 1`.
- **Use the MINTED id, not yours.** The occurrence comes back under a minted
  `occurrence_id` like `cocc_86eecc95569e678dcae86ddb`; the
  `provider_occurrence_id` you supplied is kept as a field but is NOT the
  handle. Every later verb takes the minted id, and passing your own silently
  finds nothing.
- **Show.** `calendar show <cocc_id> --format json` returns the occurrence plus
  its event, carrying `provider`, `provider_occurrence_id`, `scheduled_at`,
  `evidence_url` and `attributes`.
- **Select.** `calendar select <watch> <cocc_id> --reason "verify" --format json`
  returns `{"ok":true,"decision":"selected","change_seq":2}`.
- **Revise.** `calendar revise <cocc_id> --status cancelled --evidence-url
  https://example.com/verify --format json` returns `changed: true` and
  `revision: 3`; a follow-up `calendar list` shows `status: "cancelled"`.
- **Proof.** Keep the push result, the two `calendar list` payloads either side
  of the revise, and the select receipt. The minted occurrence id ties them.
- The selected watch source must support polling. `watch window set` refuses a
  source without a polling block.

1. Run `control-om om -- calendar list --format json`. A fresh guest lane returns
   an empty `occurrences` and `events` array. Admit an occurrence first (above)
   before proving review actions. `--every` on `window set` is plain seconds
   (`60`): `60s` fails with `every_sec: ... received NaN`, and the window record
   carries `state`, not `status`.
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

The 2026-10-12 guest-lane drive used the `oct12-feed` RSS source. It confirmed
the stored policy and the scheduled-to-cancelled transition. It did not wait
for the scheduled window to run. Occurrence review actions remain unverified
because the guest calendar had no occurrences.

## Gotchas

- Set a polling block before scheduling a window. The policy's bounds limit
  cadence, duration, extensions, daily reads and concurrent windows; invalid
  values are refused rather than clamped.
- The operator can list an empty calendar on a guest lane, but selecting,
  rejecting or revising an occurrence was not reachable because no occurrence
  existed.
- A scheduled window is not proof that a poll ran. This drive cancelled its
  future window before its start time.
