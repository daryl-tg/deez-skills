# Persona setup and editing

## Sub-features

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

## Gotchas

The canned fixture proves navigation and component behavior. An actual HTTP handler with a synthetic relay adapter proves API integration, not deployed relay delivery. Setup with an injected zero-history learner does not prove a paid model pass. Test durable checkpoint reuse and publication separately in the daemon suite.

The report can legitimately contain text:null for no selected card. Treat it as an empty state, not an old daemon. A missing model must leave the editor usable. Learning may remain off after setup or reviewed-baseline resume. Hand-edited empty rules must not revive stale embedded JSON. Never include private evidence in exported proof artifacts by default.

In a named worktree, sync-shared.ts defaults to the primary desktop checkout. Pass the twin path explicitly for a real cross-fork drift report. Do not overwrite an unrelated dirty twin to make a fence green.
