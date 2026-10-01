# Your om unread sessions

## Sub-features

- A new assistant/watch reply marks its conversation unread, including unopened sessions.
- A round soft static glow appears at the row end, clear of pin/menu actions. The row name includes “unread”; its timestamp is hidden. The dot does not animate.
- Unread sessions sort first within the existing Pinned and Chat lists, preserving served order within read/unread groups. There is no separate Unread heading.
- Opening a visible conversation acknowledges its rendered transcript cursor. A later reply remains unread.
- Watches, settings, the new composer, hidden tabs, and the open mobile drawer do not consume unread replies.
- Unread survives reload; reconnect/focus recover missed events. Upgrade seeds old history read.

## How to get to it (user POV)

Open Your om. An unread session has a soft right-side dot in Chat or Pinned. Select it to read the reply. On a phone, use Open om conversations, then choose that session.

## Driving it with control-om-chat

Run doctor on an assigned source lane. Serve the candidate through an isolated daemon with a real AgentRuntime, conversation registry, and SQLite store; open `/rooms/tools/visual/shell-fixture.html?view=agent&omSessions=daemon` on that daemon origin. This fixture uses the real session model and wire routes; never point it at operator state.

Seed distinct conversations, keep one selected, and append an assistant reply to another through the daemon process so its conversation_updated event reaches the browser. Verify `[data-om-conversation-id] [data-om-session-unread]`, then select the row by its full accessible name. Verify the reply appears and the dot clears. With Watches open, append to the selected conversation and verify the dot remains. Select a different conversation and reload to prove persistence. Repeat selection at 390px via Open om conversations; append while the drawer covers the selected chat and verify unread remains. Save paired screenshots/accessibility snapshots and the authoritative list response.

## Gotchas

- The old global thread boolean misses cold sessions. Updated timestamps count renames and user messages; they are not read cursors.
- Read acknowledgements must use the cursor captured by the rendered pane, not the latest server head or later-mutated thread state.
- KeepMountedOmPane retains hidden content. Checking selection alone is insufficient; connected DOM and hidden/inert ownership must agree.
- Fixture reload/HMR can leave detached React roots. They must never acknowledge messages. The fixture’s duplicate-createRoot console diagnostic is existing debt.
- Assistant input injected through the store proves real HTTP/SSE/read persistence, not vendor evaluation or model execution. Native mobile verification is separate.
- Row actions have existing nested-interactive accessibility debt. Preserve explicit unread labeling and record scoped axe findings honestly.

- The shell fixture forces the reduced-motion class on the root. Remove that fixture class only for normal-motion verification, then test OS reduced motion separately. Sample the actual CSS animation or record a video; a screenshot cannot prove heartbeat timing.
