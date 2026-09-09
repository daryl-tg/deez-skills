# Your om session drafts

## Sub-features

- Unsent text belongs to the selected Your om session.
- Switching A → B → A restores A's text and keeps B's text separate.
- New session starts empty while the previous conversation stays mounted.
- Preparing and sending a new conversation preserves the composed text; returning to an older session restores its draft.
- Private drafts remain in memory, outside durable composer storage.

## How to get to it (user POV)

Open Your om and choose a recent conversation. Type without sending, choose another conversation, then return. Use New session to compose separately. On mobile, open om conversations to choose a recent session.

## Driving it with control-om-chat

Use the assigned lane and run `control-om-chat doctor`. Through an isolated daemon origin proxying that lane, open `/rooms/tools/visual/shell-fixture.html?view=agent&alerts=quiet&omSessions=drafts`. This modifier is available in the `daryl/your-om-session-drafts` candidate and later revisions that contain it.

The fixture seeds `Research A` and `Research B` buttons and real Composer/AgentThread components. Type distinct text in the `Message ✦ om` textbox, switch via those buttons, and assert the textarea's exact value after each switch. Open `New session`, assert its visible textbox is empty, type new text, press Enter, and verify `New research` contains that exact text. Return to A and B to verify their drafts survived. Repeat session selection through mobile `Open om conversations` at 390px.

Capture paired screenshots and accessibility snapshots. During the new-session landing, its visible textarea is `.om-new-session-landing textarea`; the older composer remains hidden in the DOM, so do not select the first textarea blindly.

## Gotchas

- This fixture seeds session selection and captures sends locally. It proves composer ownership and the real UI transitions; it does not prove daemon conversation persistence, model execution, or remote delivery.
- The daemon origin supplies presence for Your om. Direct standalone fixture access may show the not-running surface.
- Private `om:` drafts deliberately do not persist across reload. Test session switches within one app instance; public room/DM/topic draft persistence follows a separate contract.
- New-session preparation changes the active session before sending. Its draft owner must remain stable through that async transition.
- Read both draft storage identity and conversation transition identity when diagnosing carry. Fixing only one leaves either shared storage or a textbox that never swaps.
