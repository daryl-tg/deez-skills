# HOME history restore

## Sub-features

- Preview the selected snapshot and mark the current head.
- Confirm restoring an older editable revision as a new head.
- Preserve drafts and navigation; show failures and allow retry.

## How to get to it (user POV)

Your voice → Open card → Outline, history, links and sharing → History → older revision → Restore this version → Restore. On phone, History opens as a separate rail screen; Back to note returns to the editor.

## Driving it with control-om-chat

Use the run-owned wrapper lane and `tools/visual/shell-fixture.html?view=agents&panel=persona`. Add `restore=fail-once` for the error/retry journey. Set the viewport to 1440×900 or 390×844. Wait for Open card navigation before finding the history button. Drive controls by the accessible names above; revision row ages vary, so inspect the snapshot before selecting r3.

The fixture's real checkpoint store records `document.documentElement.dataset.fixtureRestoreCalls`, `fixtureRestoreRequest`, `fixtureRestoreHead`, and `fixtureRestoreToast`. Restoring r3 from r4 should create r5, refresh history to r5/r4/r3, and remove the lowercase bullet from the actual editor. First failure leaves the editor unchanged and retry succeeds.

## Gotchas

The transport is synthetic; this proves mounted Shell/checkpoint/editor behavior, not a real relay write or the daemon's learning hold. Verify the hold separately in daemon tests. The theme comes from the fixture `theme` query, not media emulation. A screenshot of revision rows alone does not prove restore: assert the actual editor content and new head. Restore must not be tested against the operator's live HOME without task authorization.
