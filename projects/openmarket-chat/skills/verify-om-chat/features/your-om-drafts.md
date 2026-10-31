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

Use the assigned lane and run `control-om-chat doctor`. Open `/rooms/tools/visual/shell-fixture.html?view=agent&alerts=quiet&omSessions=drafts`. The fixture seeds Research A/B at `shell-fixture.tsx:2449-2467` and binds local session switching/creation at `:2748-2800`. These are local synthetic threads, but the running-om presence gate still applies: `ChatPane.tsx:517` renders "om isn't running" when `presence.running === false`, and the poll (`lib/om-health.ts`, `fetch(daemonUrl("/healthz"))`) turns any 404 or non-JSON 200 into `false`. The bare vite lane answers 404, so stub **both** health doors in the browser before opening the page:

```bash
agent-browser network route "**/healthz*" --body '{"uptime_seconds":120,"pid":1,"version":"fixture","started_at":"2026-10-27T00:00:00Z","booting":false,"stalls":[],"channels":[],"loops":[]}'
```

The trailing `*` matters: the pane also polls `/healthz?lite=1`, which `**/healthz` does not match, and that 404 flips the gate to not-running about 30 s after load. `agent-browser network unroute` removes the stub. This proves the UI under a healthy-om answer; it is not a daemon.

The composer's accessible name is `Message ✦ om`, but the textarea has no `aria-label`, so `type 'textarea[aria-label=…]'` fails. Fill it by role: `agent-browser find role textbox fill "<text>" --name "Message ✦ om"`.

The fixture seeds `Research A` and `Research B` buttons and real Composer/AgentThread components. Type distinct text in the `Message ✦ om` textbox, switch via those buttons, and assert the textarea's exact value after each switch. Open `New session`, assert its visible textbox is empty, type new text, press Enter, and verify `New research` contains that exact text. Return to A and B to verify their drafts survived. Repeat session selection through mobile `Open om conversations` at 390px.

Capture paired screenshots and accessibility snapshots. During the new-session landing, its visible textarea is `.om-new-session-landing textarea`; the older composer remains hidden in the DOM, so do not select the first textarea blindly.

### Add context to an om message (added 2026-10-28)

With the `**/healthz*` stub in place on `?view=agent&alerts=quiet&omSessions=drafts`, the om composer's **Add context** button opens a `menu` named **Add context** (`OmComposerContextPopover.tsx:252`). It holds **Add from library** ("Link a doc from your library"), **Link a channel** ("Bring a room into context") and **Link a topic** ("Reference a topic thread"). **Link a channel** swaps the menu for a `listbox` named **Channels** (`:310`), listing the fixture channels (Bitcoin `#bitcoin`, desk-admin `#desk-admin`, equities `#equities`, ...), with **Back to add context** (`:276`). Picking an item and sending with context were not driven. Verified 2026-10-28 at `2dd7aad1` on `/rooms/` (frame 24).

## Gotchas

- This fixture seeds session selection and captures sends locally. It proves composer ownership and the real UI transitions; it does not prove daemon conversation persistence, model execution, or remote delivery.
- The daemon origin supplies presence for Your om. On the bare vite lane the gate is a race: `running` starts `null`, so the rail renders until the first `/healthz` answer, and `poll()` returns early while `document.visibilityState === "hidden"` (`ChatPane.tsx:270`). A background tab therefore stays in the null state and shows the rail. That is why one nightly session passed the gate and replays did not. Use the `**/healthz*` route stub above instead of relying on it.
- The `/chat/` shell fixture seeds om presence as running (its `?view=agent` lands on "your om running" with no stub) but has no `omSessions` seed, so the A/B draft recipe is `/rooms/`-only.
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

**Last verified:** 2026-11-01 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18137) `?view=agent&alerts=quiet&omSessions=drafts` with the `**/healthz*` stub: distinct drafts in **Message ✦ om** survived switching **Research A** ↔ **Research B** (A kept "draft A text", B kept "draft B text"); **New session** opened an empty composer, Enter sent "nightly new session question" into the new thread; **Add context** → the **Add context** menu (Add from library, Link a channel, Link a topic) → **Link a channel** → the **Channels** listbox (Bitcoin, desk-admin, equities, Fed path, FX majors, …). At 390 the **Open om conversations** takeover listed the sessions ([mobile-shell-navigation.md](mobile-shell-navigation.md)). **Limitations:** picking a context item and sending with context; the new session's thread name was not read back. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261101/r1/` (`om-01` to `om-03`, `mobile-04`).

**Previous record:** 2026-10-31 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18135) `?view=agent&alerts=quiet&omSessions=drafts` with the `**/healthz*` route stub: no not-running gate; `alpha draft` in **Research A**, `beta draft` in **Research B**, back to **Research A** read `alpha draft`; **New session** → an empty `.om-new-session-landing` textarea; **Add context** → **Add from library**, **Link a channel**, **Link a topic**. The composer is a textarea whose name is its placeholder **Message ✦ om** (no `aria-label`). **Limitations:** The New-session send (fixture gap), picking a context target, daemon persistence and `/chat/`. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261031/r1/`.

**Previous record:** 2026-10-30 (scheduled maintenance). **Product commit:** `47cb13bf` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` with the `**/healthz*` stub on `?view=agent&omSessions=drafts`: the gate stayed open; **Research A** kept "draft A 1030", **Research B** opened empty and kept "draft B 1030"; **New session** opened an empty landing textarea; **Add context** listed **Add from library**, **Link a channel** and **Link a topic**. **Limitations:** Sending with context, `/chat/`. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261030/r1/` (frame 38).

**Previous record:** 2026-10-29 (nightly maintenance). **Product commit:** `cdfb1b0f` (origin/main; rooms-client 0.108.0). **Scope:** On `/rooms/` with the `**/healthz*` stub, "om isn't running" stayed absent for more than 30 s. **Research A** took "draft A 1029"; **Research B** opened empty and took "draft B 1029"; switching back restored each exact text. **New session** opened an empty `.om-new-session-landing textarea`. **Limitations:** Sending from New session and the 390 px path were not re-driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261029/r1/` (frame 55).

**Previous record:** 2026-10-28 (nightly maintenance). **Product commit:** `2dd7aad1` (origin/main). **Scope:** On `/rooms/` with the `**/healthz*` stub, "om isn't running" stayed absent through more than 30 s of polling. **Research A** took "draft A 1028"; **Research B** opened empty and took "draft B 1028"; switching back restored each exact text. **New session** opened an empty `.om-new-session-landing textarea`. **Add context** and **Link a channel** rendered (section above). **Limitations:** The new-session send, the 390 px drawer and `/chat/` were not re-driven. This proves the UI under a healthy-om answer, not a daemon. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261028/r1/` (frames 23-24).

**Previous record:** 2026-10-27 (maintenance re-drive). **Product commit:** `6c15b0fb286e9dc1b6cb130c9c97cd7e0afa9254` (origin/main). **Scope:** On `/rooms/` with the `**/healthz*` stub, the gate held for 76 s of polling (`/healthz` and `/healthz?lite=1` both 200). Research A took "draft for A maint"; B opened empty and took "draft for B maint"; A restored its text, and so did B. **New session** showed an empty `.om-new-session-landing textarea`, and A still held its draft afterwards. At 390×844, **Open om conversations** → **Research B** restored B's draft with no horizontal overflow. **Limitations:** The new-session send was not re-driven, and the fixture gap above still applies. Daemon persistence, model execution and delivery are not proved. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261027/r1/` (frames 01-05). Previous record: 2026-10-27 nightly (one session, reachability not reproducible), `http://127.0.0.1:8098/vomc-nightly-20261027/r01/` frames 33-36.
