# HOME history restore

## Sub-features

- Preview the selected snapshot and mark the current head.
- Confirm restoring an older editable revision as a new head.
- Preserve drafts and navigation; show failures and allow retry.

## How to get to it (user POV)

Agents → Voice → Manage voice cards → History → older revision → Restore this version → Restore. The card opens with its "Outline, history, links and sharing" rail already on the History tab. On phone, History opens as a separate rail screen; Back to note returns to the editor.

## Driving it with control-om-chat

Use the run-owned wrapper lane and `tools/visual/shell-fixture.html?view=agent&panel=voice`. Add `restore=fail-once` for the error/retry journey. Set the viewport to 1440×900 or 390×844. Click `Manage voice cards`, then `History` with `--exact` (the page also carries "Activity See away history").

Do **not** use `?view=agents&panel=persona`. The fixture mocks persona only when the query or hash names a persona section at page load (`shell-fixture.tsx:186-204`), and that URL reaches `#/agents/voice` after load. The panel then reads "Your voice could not be loaded" with a Retry button and no card controls. Drive controls by the accessible names above; revision row ages vary, so inspect the snapshot before selecting r3.

The fixture's real checkpoint store records `document.documentElement.dataset.fixtureRestoreCalls`, `fixtureRestoreRequest`, `fixtureRestoreHead`, and `fixtureRestoreToast`. Restoring r3 from r4 should create r5, refresh history to r5/r4/r3, and remove the lowercase bullet from the actual editor. First failure leaves the editor unchanged and retry succeeds.

Measured at `f7d7c987` with `restore=fail-once`. The first Restore left calls `1`, request `persona-card:3`, no head, and toast "The fixture restore service is unavailable. Try again.", with r4 still current. The retry left calls `2`, head `5`, toast "Reverted to r3 (as r5)", and rows r5 CURRENT / r4 / r3. At 390×844 the same path shows `Back to note` above the History heading.

## Gotchas

The transport is synthetic; this proves mounted Shell/checkpoint/editor behavior, not a real relay write or the daemon's learning hold. Verify the hold separately in daemon tests. The theme comes from the fixture `theme` query, not media emulation. A screenshot of revision rows alone does not prove restore: assert the actual editor content and new head. Restore must not be tested against the operator's live HOME without task authorization.

### Verification record

**Last verified:** 2026-10-06. **Product commit:** `231c95f49820399fc10e40e87facee6ba606c6b0`. **Scope:** opened Persona/kyle History, selected r3, confirmed restore, and observed r5 become current. **Limitations:** The configured first failure/retry was not separately observed; the fixture uses a synthetic checkpoint store, so real HOME writes and learning holds remain unverified.
