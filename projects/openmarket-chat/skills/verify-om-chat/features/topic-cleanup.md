# Topic cleanup

Use the channel menu to review quiet followed topics and resolve the ones that
are finished. Triage reads topics in small batches, shows progress, and keeps a
started resolve job alive after the sheet closes.

## Sub-features

- The **Clean up topics** server-menu action, available only in daemon builds
  outside away mode (`topic-sweep-gate.ts:15`).
- Candidate loading in batches of ten (`TopicCleanupSheet.tsx:21`), with the
  `Topics read` progressbar and `Reading topics · N of M` status.
- Candidate groups: **Looks finished**, **Still active**, and **Not sorted**;
  each group supports individual selection and **Select all in <group>**.
- The **Resolve N topics** action starts the sweep; **Cancel** closes the sheet.
  A running job reports `Resolving topics: N of M done` and continues after the
  sheet closes (`TopicCleanupSheet.tsx:400-430,470-530`).
- Empty-candidate and retryable error states.

## How to get to it (user POV)

Open the server header menu (the **Thanefield Capital** button above the channel list) and choose **Clean up topics**. Review the grouped
quiet topics, select finished ones, and resolve them. You can close the sheet
while a started cleanup continues.

## Driving it with control-om-chat

Run `control-om-chat doctor` before opening the fixture. The source fixture has
`quiet=on` to seed quiet followed topics:

```text
tools/visual/shell-fixture.html?view=room&alerts=quiet&quiet=on
```

The entry is on the **server header menu**, not the channel header's **More
channel actions** (earlier passes looked there and recorded an absence that
was never the gate). On `/rooms/` the root host's `daemonFeatures` is true, so
`Sidebar.tsx:5958` renders **Clean up topics** between **Open World** and
**Notification Settings**:

```bash
agent-browser eval '(()=>{document.querySelector(".sidebar-server-menu-trigger").click();return 1})()'
agent-browser eval '(()=>{[...document.querySelectorAll("[role=menuitem]")].find(i=>/Clean up topics/.test(i.textContent)).click();return 1})()'
```

With no daemon the sheet (a `dialog` named **Clean up topics**) opens in its
retryable error state: "Could not reach om to sort these topics. Pick by hand
below, or retry.", with **Retry**, **Cancel** and **Resolve 0 topics**. Every
quiet topic lands in one group, **Not sorted** (30 rows from the `quiet=on`
seed), each with a checkbox, plus **Select all in Not sorted**. Ticking one row
renames the action **Resolve 1 topic**; **Select all** gives **Resolve 30
topics**. Pressing it closes the sheet and the fixture records the sweep start
as `document.documentElement.dataset.fixtureTopicSweep="30"`. On `/chat/` the
server menu has no **Clean up topics** (15 items), which is the gate working:
the cloud host has no daemon features.

What this lane cannot show: the **Looks finished** / **Still active** groups,
the `role=progressbar` **Topics read** with `Reading topics · N of M`, and a
running job's `Resolving topics: N of M done`. Those need an isolated daemon
with topic triage. Do not target the operator daemon.

## Gotchas

- `quiet=on` seeds the quiet followed topics the sheet lists and the bottom-rail
  button **Quiet topics 20** (`shell-fixture.tsx:2242-2247`; `showQuiet=1` also
  seeds the shown state). Pressing the button flips `aria-pressed` and shows the
  hidden rows (the sidebar's level-2 treeitems went 14 → 30 on 2026-10-31);
  read the attribute after the re-render, not in the click's own tick.
- **The Quiet topics toggle now persists across reloads** (`47cb13bf`): it
  writes the synced pref `om.chat.sidebarQuietTopics` (`"1"` while shown, key
  absent while hidden; `lib/prefs.ts`, `lib/quiet-topics.ts`). The shell
  fixture swaps `session.quietTopics` for a plain object that never reads or
  writes the pref (`shell-fixture.tsx:2253-2260`), so a reload there cannot
  prove it. Use a real session: press **Quiet topics N**
  (`[data-quiet-topics-row]`, `aria-pressed`), read the key, reload. Source
  discovery 2026-10-30; live verification pending.
- The fixture's sweep stub (`document.documentElement.dataset.fixtureTopicSweep`)
  is reachable on `/rooms/` through the server menu; **Resolve N topics** sets it
  to the selected count. It records the start of a sweep, not a resolve: no
  topic row changes.
- The sheet is a lazy surface. Reading progress is separate from the resolve
  job, which continues outside the sheet after it starts.
- The fixture lane proves the menu entry, the sheet's error fallback, manual
  selection and the sweep start. Triage grouping, progress and the running job
  are source-defined and still need an isolated daemon lane.

### Verification record

**Last verified:** 2026-11-01 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18137) `?view=room&alerts=quiet&quiet=on`: the **Quiet topics 20** toggle flips `aria-pressed` and grows the tree 20 → 36 rows (no pref written, as expected of the fixture); the server menu's **Clean up topics** opens the **Clean up topics** dialog in its fallback ("Could not reach om to sort these topics. Pick by hand below, or retry.", **Retry**, **Cancel**, **Resolve 0 topics**, one **Not sorted** group with 31 checkboxes). `/chat/` (18138): the server menu lists 15 items without the entry. **Limitations:** **Select all** and the sweep start were not re-driven (the script matched **Resolve 0 topics** instead); the 2026-10-31 record for them stands, and the triage groups, progress and running job still need a daemon. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261101/r1/` (`cleanup-01`, `cleanup-02`, `chat-03`).

**Previous record:** 2026-10-31 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18135) `?view=room&alerts=quiet&quiet=on`: server menu → **Clean up topics** opened the **Clean up topics** dialog in its error fallback ("Could not reach om to sort these topics. Pick by hand below, or retry."), **Not sorted** with 30 rows and **Select all in Not sorted**; one tick → **Resolve 1 topic**, select all → **Resolve 30 topics**; pressing it closed the sheet and set `fixtureTopicSweep="30"`. **Quiet topics 20** flipped `aria-pressed` and showed the hidden rows. `/chat/` (18136): the server menu has no **Clean up topics** (15 items). **Limitations:** The **Looks finished** / **Still active** groups, **Topics read** progress, the running job and toggle persistence across reloads (the fixture's `quietTopics` is a plain object). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261031/r1/`.

**Previous record:** 2026-10-30 (scheduled maintenance). **Product commit:** `47cb13bf` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` `?quiet=on`: **Quiet topics 20**, and **More channel actions** offers no Clean up topics. **Limitations:** The sheet and toggle persistence are pending. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261030/r1/`.

**Previous record:** 2026-10-29 (nightly maintenance). **Product commit:** `cdfb1b0f` (origin/main; rooms-client 0.108.0). **Scope:** `?view=room&alerts=quiet&quiet=on` showed the **Quiet topics 20** button. **Limitations:** The cleanup sheet needs a daemon with topic triage. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261029/r1/` (frames 17, 41).

**Previous record:** 2026-10-28 (nightly maintenance). **Product commit:** `2dd7aad1` (origin/main). **Scope:** `?view=room&alerts=quiet&quiet=on` showed the **Quiet topics 20** button. **Limitations:** The channel-menu absence was not re-checked. The sheet and the resolve job remain live verification pending (they need a daemon build with topic triage). Evidence: none captured for this row.

**Previous record:** 2026-10-27. **Product commit:** `6c15b0fb286e9dc1b6cb130c9c97cd7e0afa9254` (origin/main). **Scope:** `?view=room&alerts=quiet&quiet=on` showed the **Quiet topics 20** button. **Limitations:** The channel-menu absence was not re-checked. The sheet and resolve job remain live verification pending (daemon build with topic triage). Previous record: 2026-10-26 at `5820fbea`.
