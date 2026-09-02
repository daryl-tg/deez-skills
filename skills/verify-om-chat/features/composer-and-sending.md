# Composer and sending

Writing a message and putting it on the wire. **Read the gotchas before you
plan a proof here** — this is the one major feature the default fixture lane
cannot verify, and agents lose runs discovering that mid-drive.

## Sub-features

- Typing, and the Send control enabling as a draft becomes non-empty.
- Draft persistence per destination (channel, topic, DM) across navigation.
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

**The fixture lane cannot type into the composer.** See Gotchas. What it *can*
prove:

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

# A seeded draft renders and survives a round trip.
agent-browser open ".../shell-fixture.html?view=room&draft=seeded%20draft%20text"
```

Related handles that do resolve. In the composer row itself:
`"Summon your om here"`, `"Add attachment or action"`,
`"Choose emoji or GIF"`, `"Toggle sealed mode"`, `"Toggle om approval mode"`.
On a message or the recovery banner: `"Add reaction"`,
`"Resend exact message"`, `"Discard & edit as new"`, `"Retry"`, `"Delete"`.
Note the composer's emoji control is `"Choose emoji or GIF"` — `"Add reaction"`
is the message-row control and will not match in the composer.

For anything requiring real text entry or a real send, use the **daemon-pair
lane**:

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

- **The default fixture composer is read-only.** The shell fixture wraps its
  session in an `autofill` proxy whose fallback (`INERT`) is callable and
  truthy, so every predicate the fixture does not spell out answers "yes".
  `session.composerLaneOwnedElsewhere` is unstubbed, so the composer renders
  under *"This draft is open in another tab"* with `readOnly: true`. Typing
  succeeds silently and changes nothing; Send stays disabled.

  Verify it before blaming your change:

  ```bash
  agent-browser eval 'const t=document.querySelector("textarea"); t && t.readOnly'
  ```

  To unlock it, spell the predicate out as `false` in the explicit session map
  in `tools/visual/shell-fixture.tsx`. That is a legitimate part of shipping a
  composer change, not a workaround.

- The same proxy is why *"Delivery could not be confirmed"* is on by default
  (`session.composerDeliveryRecovery` is unstubbed). Both banners are fixture
  artefacts. Do not report them as regressions, and do not caption a screenshot
  as if they were the state under test.

- The composer is a `textarea` with `role="textbox"`, not a `contenteditable`.
  `document.querySelector("[contenteditable=true]")` finds nothing.

- `?sealed=1` is a *different* lock (the agent-lane seal) from the draft lease.
  Do not use it expecting to clear the lease.

- `tools/daemon-pair.ts` refuses to run against a `dist/` built from another
  tree, and it is right to. When it exits with a digest mismatch, rebuild —
  do not set `OM_ROOMS_GUI_DIR` to get past it unless you are deliberately
  bisecting a pinned bundle.
