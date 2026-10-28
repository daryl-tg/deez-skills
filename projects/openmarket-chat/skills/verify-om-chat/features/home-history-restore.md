# HOME history restore

## Sub-features

- Preview the selected snapshot and mark the current head.
- Confirm restoring an older editable revision as a new head.
- Preserve drafts and navigation; show failures and allow retry.

## How to get to it (user POV)

Agents → Voice → Manage voice cards → History → older revision → Restore this version → Restore. The card opens with its "Outline, history, links and sharing" rail already on the History tab. On phone, History opens as a separate rail screen; Back to note returns to the editor.

## Driving it with control-om-chat

Use the run-owned wrapper lane and `tools/visual/shell-fixture.html?view=agent&panel=voice`. Add `restore=fail-once` for the error/retry journey. Set the viewport to 1440×900 or 390×844. Click `Manage voice cards`, confirm it reads `aria-expanded="true"` (a click sent about 1.5 s after load can miss), then `History` with `--exact` (the page also carries "Activity See away history").

Do **not** use `?view=agents&panel=persona`. The fixture mocks persona only when the query or hash names a persona section at page load (`shell-fixture.tsx:191-212`), and that URL reaches `#/agents/voice` after load. The panel then reads "Your voice could not be loaded" with a Retry button and no card controls. Drive controls by the accessible names above; revision row ages vary, so inspect the snapshot before selecting r3.

The fixture's real checkpoint store records `document.documentElement.dataset.fixtureRestoreCalls`, `fixtureRestoreRequest`, `fixtureRestoreHead`, and `fixtureRestoreToast`. Restoring r3 from r4 should create r5, refresh history to r5/r4/r3, and remove the lowercase bullet from the actual editor. First failure leaves the editor unchanged and retry succeeds.

Measured at `f7d7c987` with `restore=fail-once`. The first Restore left calls `1`, request `persona-card:3`, no head, and toast "The fixture restore service is unavailable. Try again.", with r4 still current. The retry left calls `2`, head `5`, toast "Reverted to r3 (as r5)", and rows r5 CURRENT / r4 / r3. At 390×844 the same path shows `Back to note` above the History heading.

## Gotchas

The transport is synthetic; this proves mounted Shell/checkpoint/editor behavior, not a real relay write or the daemon's learning hold. Verify the hold separately in daemon tests. The theme comes from the fixture `theme` query, not media emulation. A screenshot of revision rows alone does not prove restore: assert the actual editor content and new head. Restore must not be tested against the operator's live HOME without task authorization.

### Verification record

**Last verified:** 2026-10-29 (nightly maintenance). **Product commit:** `cdfb1b0f` (origin/main; rooms-client 0.108.0). **Scope:** `?view=agent&panel=voice&restore=fail-once` → **Manage voice cards** (confirmed `aria-expanded="true"`) → **History** (`--exact`) listed r4 CURRENT / r3. r3 → **Restore this version** → **Restore** left calls `1`, request `persona-card:3`, no head and the toast "The fixture restore service is unavailable. Try again.". The retry left calls `2`, head `5`, "Reverted to r3 (as r5)", and rows r5 CURRENT / r4 / r3. **Limitations:** Synthetic transport. The first **Manage voice cards** click, sent 1.5 s after load, did not expand the section, so check `aria-expanded` before **History**. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261029/r1/` (frames 07, 53–54).

**Previous record:** 2026-10-28 (nightly maintenance). **Product commit:** `2dd7aad1` (origin/main). **Scope:** `?view=agent&panel=voice&restore=fail-once` → **Manage voice cards** → **History** (`--exact`) listed r4 CURRENT / r3. Selecting r3 → **Restore this version** → **Restore** left calls `1`, request `persona-card:3`, no head and the toast "The fixture restore service is unavailable. Try again." The retry left calls `2`, head `5`, "Reverted to r3 (as r5)", and rows r5 CURRENT / r4 / r3. **Limitations:** 390×844 and real HOME writes were not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261028/r1/` (frame 22).

**Previous record:** 2026-10-27 (maintenance re-drive). **Product commit:** `6c15b0fb286e9dc1b6cb130c9c97cd7e0afa9254` (origin/main). **Scope:** `shell-fixture.html?view=agent&panel=voice&restore=fail-once` → **Manage voice cards** → **History** listed r4 CURRENT / r3. Selecting r3 → **Restore this version** → **Restore** set `fixtureRestoreCalls=1`, `fixtureRestoreRequest=persona-card:3` and the toast "The fixture restore service is unavailable. Try again." The retry set `fixtureRestoreCalls=2`, `fixtureRestoreHead=5` and "Reverted to r3 (as r5)", and the list read r5 CURRENT / r4 / r3. **Limitations:** Synthetic checkpoint store; real HOME writes, learning holds, **Keep current** and the 390 px **Back to note** were not driven. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261027/r1/` (frame 13).
