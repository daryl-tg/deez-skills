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

Use the assigned lane and run `control-om-chat doctor`. Open `/rooms/tools/visual/shell-fixture.html?view=agent&alerts=quiet&omSessions=drafts` through an isolated daemon origin proxying that lane. The fixture seeds Research A/B at `shell-fixture.tsx:2449-2467` and binds local session switching/creation at `:2748-2800`. These are local synthetic threads, but the running-om presence gate still applies: direct source-lane access shows only "om isn't running".

The fixture seeds `Research A` and `Research B` buttons and real Composer/AgentThread components. Type distinct text in the `Message ✦ om` textbox, switch via those buttons, and assert the textarea's exact value after each switch. Open `New session`, assert its visible textbox is empty, type new text, press Enter, and verify `New research` contains that exact text. Return to A and B to verify their drafts survived. Repeat session selection through mobile `Open om conversations` at 390px.

Capture paired screenshots and accessibility snapshots. During the new-session landing, its visible textarea is `.om-new-session-landing textarea`; the older composer remains hidden in the DOM, so do not select the first textarea blindly.

## Gotchas

- This fixture seeds session selection and captures sends locally. It proves composer ownership and the real UI transitions; it does not prove daemon conversation persistence, model execution, or remote delivery.
- The daemon origin supplies presence for Your om. Direct standalone fixture access may show the not-running surface.
- Private `om:` drafts deliberately do not persist across reload. Test session switches within one app instance; public room/DM/topic draft persistence follows a separate contract.
- New-session preparation changes the active session before sending. Its draft owner must remain stable through that async transition.
- Read both draft storage identity and conversation transition identity when diagnosing carry. Fixing only one leaves either shared storage or a textbox that never swaps.
- **The fixture's New session path is stale.** The landing's first send calls
  `session.startNewOmSession()` (`ChatPane.tsx`, `prepareSend`; since
  `758ba4dd`), but the `omSessions=drafts` seed binds only `createOmSession`
  (`tools/visual/shell-fixture.tsx:2793`). The unstubbed method resolves to INERT,
  the active session never changes, and the send lands in the session that was
  already open (Research A in the 2026-10-27 drive). That is a fixture gap, not
  proof of a product carry bug. Prove the new-session send on a daemon origin.

### Verification record

**Last verified (partial):** 2026-10-27. **Product commit:** `6c15b0fb286e9dc1b6cb130c9c97cd7e0afa9254` (origin/main). **Scope:** In one browser session on the source lane, `?view=agent&omSessions=drafts` passed the running-om gate and showed the rail (**New session**, **Watches**, **Research A**, **Research B**, "your om running") and the `Message ✦ om` composer. Typing into A, switching to B (empty), typing into B and returning to A restored "draft for A nightly", and B kept "draft for B nightly". **New session** showed an empty `.om-new-session-landing textarea`. At 390×844, **Open om conversations** switching kept the drafts, with no horizontal overflow. **Limitations:** Reachability is not reliable: fresh browser sessions and replays of the same page sequence all stopped at "om isn’t running" (`/healthz` 404), and the trigger was not identified. The new-session send landed in Research A (fixture gap above). Daemon persistence, model execution and delivery are not proved. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261027/r01/` (frames 33-36). Previous attempt: 2026-10-26 at `5820fbea` (gate only).
