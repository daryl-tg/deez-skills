# Composer and sending

Writing a message and putting it on the wire. This file used to open by saying
the fixture lane could not verify any of it. That stopped being true with
`#777`: the fixture now types and sends. What still needs the daemon-pair lane
is the **wire** — delivery, a second identity, recovery states — not text entry.
Read the gotchas for where the line now falls.

## Sub-features

- Typing, and the Send control enabling as a draft becomes non-empty.
- Draft persistence per destination (channel, topic, DM) across navigation —
  durably for some lanes only. `#777` split them by lane name: `dm:<user>`,
  `room:<room>` and `room:<room>#<topic>` stay localStorage-backed under
  `om.chat.composerDrafts.<userId>`, while anything on an `om:`-prefixed lane is
  rejected at the storage boundary (`isVolatileLane`, `composer-draft-store.ts`)
  and lives in memory only. That covers the private/agent plane, an active
  whisper lane even while nominally public (`om:dm:<user>`), and the
  per-session lanes `#786` added (`om:draft:<owner>`, `om:session:<id>`) —
  they inherit the rule by name rather than needing their own. The
  difference is reload-durability specifically: volatile lanes still survive
  in-tab navigation, because the session's in-memory map is the live source
  either way.
- Attachments: the `+` menu, drag-and-drop, staged chips with per-item removal.
- Replies, mentions (`@user`, role tags), slash commands, `$` market refs.
- The formatting toolbar and its selection clearance.
- Delivery states: sending, delivered, *"Delivery could not be confirmed"*
  recovery, and the cross-tab draft lease.
- Send disabled while empty; Enter-to-send versus newline. The Send **button**
  is a phone-width control only — desktop has no send affordance but Enter.
- The over-limit "send as file" offer and the mass-mention brake, both of which
  can refuse a send that otherwise looks ready.

## How to get to it (user POV)

You click into the message box at the bottom of a channel, topic, or DM, type,
and press Enter or the send arrow. The box remembers what you were writing if
you navigate away and come back, and it tells you when a message did not make
it.

## Driving it with control-om-chat

**The fixture lane types and sends.** `#777` spelled out the two predicates
that used to lock it (see Gotchas), so a plain `?view=room` composer accepts
keystrokes and Enter appends to the tape:

```bash
agent-browser click "textarea"
agent-browser keyboard type "probe line"
agent-browser press Enter
agent-browser eval '(()=>document.querySelectorAll("[data-message-row]").length)()'
#   one more than before; the textarea is empty and the line is in the tape
```

That is a **local** send into the fixture's seeded store. It proves the write
path, the clear-on-send, and the tape update — and nothing about the relay.
What the lane also proves:

```bash
# The composer's destination follows navigation.
agent-browser snapshot -c | grep -i textbox
#   "Message #ops"  ->  "Message in CPI print — Aug"  ->  "Message ana · $ for markets · /chart to post one"

# Send is disabled on an empty draft — but ONLY at a phone width. The Send
# button renders under `max-width: 768px`; on desktop there is no such button
# and Enter sends. Set the viewport first or this looks like a regression.
agent-browser set viewport 390 844
agent-browser find role button text --name "Send message" --exact
agent-browser snapshot -i -c | grep "Send message"        # [disabled]

# A seeded draft renders and survives a round trip. ?draft= seeds TWO lanes
# with the same text — room:ops and dm:<?dm= or ana> — so it works whichever
# of the two views you land on.
agent-browser open ".../shell-fixture.html?view=room&draft=seeded%20draft%20text"
```

Related handles that do resolve. In the composer row itself:
`"Summon your om here"`, `"Add attachment or action"`,
`"Choose emoji or GIF"`, `"Toggle sealed mode"`, `"Toggle om approval mode"`.
On a message or the recovery banner: `"Add reaction"`,
`"Resend exact message"`, `"Discard & edit as new"`, `"Retry"`, `"Delete"`.
Note the composer's emoji control is `"Choose emoji or GIF"` — `"Add reaction"`
is the message-row control and will not match in the composer.

For anything on the **wire** — delivery states, a second identity receiving the
message, reconnection — use the **daemon-pair lane**. Text entry and a local
send no longer need it:

```bash
bun run build                       # the pair refuses a bundle built from another tree
bun tools/daemon-pair.ts            # two zero-login daemons, 31398 / 31399
```

It needs the local parity stack up (auth on `4001`, relay/store on `3002`).
Confirm with `curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:4001/`
before you build — the stack is frequently down, and finding out after a
four-minute build is the expensive order.

The cheaper alternative for a pure logic change is a unit test in `test/`
against the real `ChatSession`, which is what `tools/gui-e2e.ts` drives.

## Gotchas

- **The composer is no longer read-only, and the two banners are gone.** For a
  long while the fixture left `session.composerLaneOwnedElsewhere` and
  `session.composerDeliveryRecovery` unstubbed, so the `INERT` proxy answered
  truthy for both, the textarea rendered `readOnly`, and *"This draft is open in
  another tab"* and *"Delivery could not be confirmed"* sat above it. `#777`
  stubbed them — `composerDeliveryRecovery: () => null` and
  `composerLaneOwnedElsewhere: () => false`
  (`tools/visual/shell-fixture.tsx:2677-2678`), with a comment naming the lock
  it was removing. Measured again on `490cb8d0`:
  `readOnly` is `false` in room, topic and DM, and neither banner renders.

  If you find either banner back, that is a fixture regression rather than the
  expected state — the opposite of the advice this file used to give. And there
  is now no way to stage them on purpose: `composerDeliveryRecovery` is
  hardcoded to `null`, so even `?delivery=fail-once` — which does make a send
  fail — will not raise the recovery banner. Proving those two states needs a
  fixture change, not a query.

- **A local send is not a wire send.** Enter appends a row to the seeded tape
  and clears the box, which is enough to prove the composer's write path. It
  says nothing about the relay, about a second identity seeing the message, or
  about delivery and recovery states. Keep those claims on the daemon-pair
  lane and say which lane a frame came from.

- The composer is a `textarea` with `role="textbox"`, not a `contenteditable`.
  `document.querySelector("[contenteditable=true]")` finds nothing.

- `?sealed=1` is a *different* lock (the agent-lane seal) from the draft lease.
  Do not use it expecting to clear the lease.

- `tools/daemon-pair.ts` refuses to run against a `dist/` built from another
  tree, and it is right to. When it exits with a digest mismatch, rebuild —
  do not set `OM_ROOMS_GUI_DIR` to get past it unless you are deliberately
  bisecting a pinned bundle.
