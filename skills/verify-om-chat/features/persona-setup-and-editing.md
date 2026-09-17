# Persona setup and editing

## Sub-features

- Explicit global profile selection, loaded preview, full-profile spotlight, fixed samples and per-profile learning permission.
- Immediate historical setup, active progress, insufficient history, resume and cancellation.
- Manual creation, structured edits, concurrent revision reconciliation and reviewed learning holds.
- Native selfmd pair or folded Markdown import; save separately from selection.
- Evidence-free default export, optional private evidence, and a private saved-voice sample.
- Direct History entry and restore, phone layout, browser Back and owner-scoped offline recovery.

## How to get to it (user POV)

Open Your om, then Voice & away. Voice is the first tab. With no card, choose Set up my voice now, Import a card, or Create manually. A saved setup or imported card needs Use this card before selection. An existing card offers Edit voice, Advanced document, History and Export card. Away and Activity are future destinations; this phase does not arm an agent.

## Driving it with control-om-chat

Use the owned wrapper lane and `tools/visual/shell-fixture.html?view=agent&panel=voice&personaState=empty` for first use, or `personaState=ready` for a selected card. The canonical route is `#/agent/voice`; Away and Activity append their names instead. The legacy `view=agents&panel=persona` entry redirects into Your om.

For actual daemon API integration, use `backend=real&backendOrigin=<owned-synthetic-api-origin>` on the same Shell fixture. Supply a run-owned API server and synthetic HOME. The fixture only forwards library API requests to that origin. Never point setup or restore at the operator's real HOME for a verification run.

Edit voice opens Voice name, About me, Voice rule 1 and Example for voice rule 1 fields. Use Add voice rule, Add boundary, Add example, Save voice and Cancel. Try saved voice is distinct from unsaved text. Import a card opens a Voice card files input accepting SKILL.md plus card.json and optional README.md, or one folded Markdown file. File upload reaches a preview, then Save card, then separate Use this card. Export card defaults Include private evidence and examples to unchecked.

History must open the selected card with the History rail already visible. In the ready fixture, choose r3, Restore this version, then Restore. Assert fixtureRestoreHead=5, fixtureRestoreCalls=1, and changed editor text; rows alone do not prove restore. See home-history-restore.md for failure/retry.

Capture at 1440x1000 and 390x844. With an actual API response cached, go offline, navigate Away then Voice, and verify edits/export are disabled while the current owner's card remains visible. Restore network before ending the run.

## Switching profiles

Use `personaState=profiles` for deterministic multi-profile rendering, or the actual API rig for persisted selection. Add sample profiles creates Brief, Warm, Skeptical, Sarcastic and Show Me without loading one. Existing three-sample homes add only the two missing cards. Choose Profile to load, then Load profile. Assert both Loaded profile text and the API selectedDocId. Repeat in the same mounted panel, then Use default voice and assert a null selection and cleared derived digest. Changing the picker alone must not change the loaded card or its preview. Profile to load is a custom menu button, not a native select. Open it by accessible name and pick the named menu item; Arrow keys, Enter and Escape must work.

The loaded preview shows voice rules and an example from the selected profile. View full profile opens a focused read-only dialog with the complete readable card body, including advanced sections and code blocks. Check the last section against the API report, close with Escape and verify focus returns to View full profile. Reopen and exercise Close. At 390x844, verify the dialog fits the viewport and the body scrolls. Offline cached views must say they are cached, and an account switch must clear the previous profile and close its dialog. Older reports without profileMarkdown may show available details, with a clear limit and the advanced document route.

Open chosen profile opens an inactive card through the library route without loading it. Duplicate names include their paths in the picker. Importing a second card with the same managed skill name can fail to load; verify actionable rename guidance and that the prior selection and digest remain intact.

Samples start fixed. Confirm Learning paused for this profile and the separate global preference description. Allow learning into this profile must preserve a globally disabled setting. Repeat Add sample profiles after editing or opting in; it must preserve both changes without duplicates. No model call is needed to create or load samples.

At desktop width, measure both Learning text and controls. A parent grid with `minmax(0, 1fr) auto` can collapse text to zero width when the new controls contain prose. Check computed widths and readable text, not only horizontal overflow. Capture the fixed-profile explanation at desktop and phone widths. Offline cached profile controls must be disabled.

## Proposed changes review

Use `tools/visual/persona-panel-fixture.html?state=pending-long` for a synthetic 96-line proposal with six separated change hunks. Add `theme=light` for the light palette. The fixture uses the actual `.persona-scroll` viewport and stateful Accept / Not now responses; it does not contact the armed daemon.

Proposed changes is one section near the top. Each proposal starts collapsed with Show changes, Read all, Accept and Not now visible. Show changes expands only that proposal; Hide changes collapses it. Scroll the actual persona pane and measure `.persona-proposal-toolbar` against `.persona-proposal`: the toolbar pins at the pane top while its article continues, then moves out with the article. A 390x600 viewport allows scrolling beyond the whole long proposal. No toolbar may cover the next voice card after its article ends.

Read all opens the Proposed voice changes dialog. Verify Current voice / Proposed voice file headers, old/new line numbers, context, hunk headers and distinct additions/deletions. Long prose wraps at 390px without horizontal overflow. Scroll Full proposed wording to the end and confirm Accept / Not now remain visible. Escape restores focus to Read all. In the pending-long fixture, Accept removes the proposal and changes v7 to v8; Not now removes the proposal and retains v7. Conflict/stale proposals retain the guarded reconciliation path. Hidden metadata must stay absent from the visible diff while clean acceptance retains the complete raw merged payload.

The revamp uses centered content columns beside the sidebar. Check the composed Shell Voice, Away coverage and Activity routes at 1440x1000, rather than measuring against the whole viewport. Voice editing is reached through Edit, Saved profiles holds profile selection, and Manage voice cards holds import/create/export. Existing full-profile viewing is separate from proposal review.

## Gotchas

The canned fixture proves navigation and component behavior. An actual HTTP handler with a synthetic relay adapter proves API integration, not deployed relay delivery. Setup with an injected zero-history learner does not prove a paid model pass. Test durable checkpoint reuse and publication separately in the daemon suite.

The report can legitimately contain text:null for no selected card. Treat it as an empty state, not an old daemon. A missing model must leave the editor usable. Learning may remain off after setup or reviewed-baseline resume. Hand-edited empty rules must not revive stale embedded JSON. Never include private evidence in exported proof artifacts by default.

There is no cross-fork drift report: `sync-shared.ts` was deleted in `f190644c` and the persona UI is one shared implementation under `packages/chat-ui/src/`. A persona change is in `/rooms` and `/chat/` at once, so drive both hosts rather than looking for a twin to reconcile.

The actual API rig must include a synthetic HOME mirror-health entry and directory to prove managed voice skill publication. Missing mirror state should produce an unavailable load and preserve the previous selection; a 200 report by itself is not proof that the voice skill exists. Never configure that rig against the operator’s real mirror.
