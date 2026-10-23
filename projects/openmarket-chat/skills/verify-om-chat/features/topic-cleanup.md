# Topic cleanup

Use the channel menu to review quiet followed topics and resolve the ones that
are finished. Triage reads topics in small batches, shows progress, and keeps a
started resolve job alive after the sheet closes.

## Sub-features

- The **Clean up topics** server-menu action, available only in daemon builds
  outside away mode (`topic-sweep-gate.ts:13`).
- Candidate loading in batches of ten (`TopicCleanupSheet.tsx:21`), with the
  `Topics read` progressbar and `Reading topics · N of M` status.
- Candidate groups: **Looks finished**, **Still active**, and **Not sorted**;
  each group supports individual selection and **Select all in <group>**.
- The **Resolve N topics** action starts the sweep; **Cancel** closes the sheet.
  A running job reports `Resolving topics: N of M done` and continues after the
  sheet closes (`TopicCleanupSheet.tsx:400-430,470-530`).
- Empty-candidate and retryable error states.

## How to get to it (user POV)

Open a server's channel menu and choose **Clean up topics**. Review the grouped
quiet topics, select finished ones, and resolve them. You can close the sheet
while a started cleanup continues.

## Driving it with control-om-chat

Run `control-om-chat doctor` before opening the fixture. The source fixture has
`quiet=on` to seed quiet followed topics:

```text
tools/visual/shell-fixture.html?view=room&alerts=quiet&quiet=on
```

Open **More channel actions**. This source lane does not expose **Clean up
topics**, even with the quiet-topic seed; capture that absence as a fixture
limit. The real action requires a daemon build, an eligible non-away session,
and an isolated daemon with topic triage available. Do not target the operator
daemon. On that owned rig, open the server menu, choose **Clean up topics**,
wait for `role=progressbar` named **Topics read**, inspect each group, select
rows, and capture the **Resolving topics** count after starting a cleanup.

## Gotchas

- `quiet=on` affects the topic rail and inbox but does not add daemon-only menu
  capabilities to the source fixture. Its visible proof is the bottom-rail
  button **Quiet topics 20** (`shell-fixture.tsx:2236-2241`; `showQuiet=1` also
  seeds the shown state). Assert that, not only the missing menu item.
- The fixture does stub a sweep start (it sets
  `document.documentElement.dataset.fixtureTopicSweep`), but nothing in the
  source lane can reach it, because the menu entry needs `daemonFeatures`
  (`topic-sweep-gate.ts:13`).
- The sheet is a lazy surface. Reading progress is separate from the resolve
  job, which continues outside the sheet after it starts.
- This maintenance pass proved the source-lane menu omission, not the sheet's
  live daemon behavior. Product source defines the progress, grouping, and
  action states; an isolated daemon lane is still required for live coverage.

### Verification record

**Last verified:** 2026-10-23. **Product commit:** `afabb11c601d605ffaf2a22a406314baa1fbd2eb` (origin/main). **Scope:** `?quiet=on` rendered **Quiet topics 20** on the rail, and More channel actions listed 14 items with no Clean up topics. **Limitations:** The sheet and resolve job are live verification pending. They need an eligible daemon build and an isolated topic-triage service, and the local parity services (4001, 3002) were down. Previous record: 2026-10-22 at `cd9f8c72`.
