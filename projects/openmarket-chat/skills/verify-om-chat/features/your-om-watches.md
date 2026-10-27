# Your om watches

## Sub-features

- A single Watches destination in expanded desktop, collapsed desktop, and mobile conversation navigation. The away remote-control pane has none: it mounts the rail with `showWatches={false}` (`RemoteControlPane.tsx:129`) because the cloud pane has no watch RPC. Measured on `remote-home-fixture.html?state=live` at `f7d7c987`.
- Canonical watch state, actions, timing, attention, groups, and schedule diagnostics.
- Whole-watch pause/resume, refreshed persisted state, and daemon refusal messages.
- Structured attention cards: Clear past error, Retire schedule, Attach feed, and Resume watch; technical details expand in place. Attachment and retirement have a confirmation dialog.
- Read-only details for owned scheduler children, including lifecycle, authority, cadence, and next command.
- Recent fires: newest-first execution rows with delivery status, plus loading,
  empty, and error states. Notices do not appear in this execution history.

## How to get to it (user POV)

Open Your om, then Watches in the conversation sidebar. On mobile, open om conversations and choose Watches. Details opens a watch dialog; Back to conversation returns to the existing conversation.

## Driving it with control-om-chat

Run `control-om-chat doctor` against the assigned lane first. Use a run-owned daemon origin that reverse-proxies the candidate Vite lane, with an isolated `OM_HOME` containing QA watches. Open `/rooms/tools/visual/shell-fixture.html?view=agent&alerts=quiet` on that daemon origin. The Shell fixture seeds conversation data; watch reads and mutations must reach the production daemon routes.

Wait for `[data-testid="om-recent-fires"]` and verify a fire row's status
alongside the watch list. The section has independent loading/error/empty states.

Drive accessible names: `Watches`, `Refresh`, `Show details for <label>`, `Close <label> details`, and one toggle per watch whose name alternates between `Pause <label>` and `Resume <label>` (`OmWatchesSurface.tsx:521`). Wait for `[data-om-watch-id]` rows after navigation and the changed switch label after mutation. Verify persistence through `POST /rpc/v1/watch/overview` with `{}`. The pinned `@openmarket/rooms-client` 0.104.0 (`7e57ee84`) posts every watch verb to `/rpc/v1/watch/<verb>` (`src/daemon-watches.ts:472`); there is no `event-watch` path. Capture expanded and collapsed desktop navigation, then mobile `Open om conversations` → `Watches`; verify the sheet closes and no horizontal overflow appears. Save snapshots, screenshots, console/errors, and a scoped accessibility result for `.om-watches-surface`.

## Gotchas

- Unified overview landed in GUI #783 and backend #973. Actionable attention currently lives in the subsequent candidate; it requires attention_items and resolve-attention from the companion daemon/client. Old daemons show an update explanation.
- For attention, seed a recovered error (later non-error source event plus committed journal) and an unowned schedule in an isolated home. Click Clear past error and Retire schedule, verify both cards disappear, and read back the runtime, retirement ledger and retained history. Replaying an obsolete issue must refuse. Never use a real account feed to obtain a screenshot: simulate feed attachment responses explicitly and label that evidence; canonical news-attach tests cover backend delegation.
- An incomplete action can make resume save `enabled` before returning a refusal. Verify the page refreshes after errors and shows the persisted state alongside the refusal.
- Direct fixture access on a standalone Vite origin does not prove trusted daemon routing. The zero-login local path needs the daemon origin.
- A daemon HTTP server without the evaluation loop proves routing and persistence, not scheduled execution or delivery. Keep those claims separate in the evidence manifest. Child lifecycle/authority states need seeded scheduler records or deterministic tests.
- Changing desktop/mobile layout can remount the conversation pane; reopen Watches through the relevant navigation and wait for rows before capturing.
- The shell fixture may log existing duplicate-root and invalid-child warnings. Preserve the actual console output; do not describe it as clean.
- Use a `group` role for labeled action containers and retain the Shell's single main landmark.

### Verification record

**Last attempted:** 2026-10-27 at `6c15b0fb286e9dc1b6cb130c9c97cd7e0afa9254` (origin/main). In the one source-lane session that passed the om gate (see [your-om-drafts.md](your-om-drafts.md)), **Watches** opened `.om-watches-surface` with **Back to conversation**, **Refresh**, and the `[data-testid="om-recent-fires"]` section in its error state: "Recent fires could not be loaded. The daemon did not answer with a readable list of fires." with **Try again**. There were no `[data-om-watch-id]` rows. That proves the surface mounts and renders its fires error branch, not watch behavior. **Live verification pending** for rows, details, pause/resume and attention: they need the daemon origin and QA watches. The surface also has a per-row `Actions for <label>` button (`OmWatchesSurface.tsx:483`). Ended watches render no toggle (`:516`), and attention-card buttons are named `<action label>: <title>` (`:609`). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261027/r01/` (frame 37). Previous attempt: 2026-10-26 at `5820fbea` (gate only).
