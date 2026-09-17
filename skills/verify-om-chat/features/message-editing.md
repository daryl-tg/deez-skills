# Message editing

## Sub-features

- Enter and the save button commit changed text.
- An unchanged save closes the editor without a transport request or new edit timestamp.
- Changing text and restoring it before saving also closes without an edit.
- A previously edited message keeps its existing edit metadata on an unchanged save.
- Escape cancels; Shift+Enter adds a newline. A completion menu consumes these keys first.
- Topic labels return to canonical references on save. Empty poll captions stay empty; clearing a nonempty caption remains a real edit.

## How to get to it (user POV)

In a channel, click your message and choose Edit in its toolbar. In a DM, click your outgoing message, choose More, then Edit Message. The editor is named Edit message. Its hint buttons are named cancel and save.

The empty composer also offers Arrow Up to edit your last message when the conversation is at the bottom and the composer is in the public plane.

## Driving it with control-om-chat

Open `tools/visual/shell-fixture.html?view=room&alerts=quiet` or the same route with `view=dm`, using the assigned lane and `control-om-chat url`.

Use the channel toolbar button named Edit — with two precisions measured on
lane 18119, because the obvious spelling of each fails.

The row toolbar is `.msg-toolbar hidden group-hover:flex`: a **CSS** hover,
not a JS one. Dispatching synthetic `mouseover`/`mouseenter`/`pointerover` at
the row leaves it hidden, so a probe built that way reports no Edit control and
reads like the feature is gone. Use `agent-browser hover <selector>`, which
drives a real pointer. Mark the row you want first — the fixture has two
outgoing messages, both labelled `Message from kyle`:

```bash
agent-browser eval '(()=>{const r=[...document.querySelectorAll("[data-message-row]")]
  .find(x=>/Message from kyle/.test(x.getAttribute("aria-label")||""));
  r.setAttribute("data-probe","1");return "marked";})()'
agent-browser hover '[data-probe]'
agent-browser find role button click --name "Edit" --exact
```

`--exact` is not optional. The control carries no `aria-label` — its accessible
name comes from `title="Edit"` — and an inexact match also hits the sidebar's
`Edit ops`, `Edit signals`, `Edit macro` and `Edit equities`, which edit
channels rather than messages. Proven: with the hover held and `--exact`, the
click lands and `[aria-label="Edit message"]` mounts focused. For DMs, the row has the accessible label Message from kyle, the bubble toolbar has More, and its menu item is Edit Message. After opening, wait for the textbox named Edit message and focus it before pressing Enter. Use the button named save for the mouse path.

Capture the open editor and the result, including accessibility snapshots. Observe the target message's content and edit metadata and record outbound edits. Include a changed-content control to prove that the save path actually ran.

The 2026-09-09 unchanged-edit run attached actual ChatSession edit methods to the fixture's loaded state with a recording transport. Its reproducible adapter and browser script live in `/Users/dboon/Documents/dev-notes/unchanged-message-edit/`. The channel and DM journeys proved unchanged Enter, reverted Save, and genuine edits. The channel journey also proved preservation of an existing edit timestamp. DM timestamp preservation was covered by the session regression.

## Gotchas

The stock shell fixture substitutes commitEdit and commitDmEdit. Its timestamps are fixture behavior and cannot prove session logic. Use actual session methods for a session fix, and state when the transport is recorded rather than live.

On agent-browser 0.33.2, click does not document a --button option. Do not treat a successful command with that option as evidence of a right click. Use the visible toolbar and menu controls.

In the recorded DM journey, reopening the message menu after a save selected an incoming row. Fresh fixture navigations between cases avoided this fixture interaction; they did not prove persistence across reload. The fixture also logged a React invalid textarea value warning. Record it.

Full server persistence and other clients receiving the edit require the local auth/relay stack and daemon-pair lane. The fixture cannot prove those outcomes.
