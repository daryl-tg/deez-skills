# Message editing

## Sub-features

- Enter and the save button commit changed text.
- An unchanged save closes the editor without a transport request or new edit timestamp.
- Changing text and restoring it before saving also closes without an edit.
- A previously edited message keeps its existing edit metadata on an unchanged save.
- Escape cancels; Shift+Enter adds a newline. A completion menu consumes these keys first. With Vim mode on (`4f2accbc`), Escape enters NORMAL instead, **Shift+Escape** cancels, and Enter in normal or visual mode is a motion that neither saves nor closes. The hint then reads "shift+escape to cancel • enter to save" with the mode badge `.inline-edit-hint .composer-vim-mode[data-vim-mode]` in front (`InlineMessageEditor.tsx:261`, `:620-621`), and a `.vim-block-cursor` shows outside insert mode.
- Saving an empty edit does not save: it opens the **Delete Message** confirm ("This removes the message for everyone in the channel and cannot be undone.", **Delete**) through `requestRoomMessageDelete` (`MessageRow.tsx:610-640`, `:2670-2676`; `d3aebbb5`). A **CharCounter** shows near the room cap and an over-cap save is refused (`maxLength`, source only).
- Topic labels return to canonical references on save. Empty poll captions stay empty; clearing a nonempty caption remains a real edit.
- A role mention edits as a snug `@Name` chip (`f8baae2a`). The edit box binds the message's `om://role/<id>` references with the room, so the value reads `@Devops` rather than the URI, and the chip is as wide as its name. A colored role gets `composer-token-role-colored` and `--role-color` (`InlineMessageEditor.tsx:234-241`, painted through `DraftBackdrop.tsx:40`). Saving sends the `om://role/…` URI again, and a role picked from the edit box's `@` menu binds the same way.

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
sleep 0.6                      # let the toolbar settle (see Gotchas)
agent-browser find role button click --name "Edit" --exact
```

`--exact` is not optional. The control carries no `aria-label` — its accessible
name comes from `title="Edit"` — and an inexact match also hits the sidebar's
`Edit ops`, `Edit signals`, `Edit macro` and `Edit equities`, which edit
channels rather than messages. Proven: with the hover held and `--exact`, the
click lands and `[aria-label="Edit message"]` mounts focused. On 2026-10-30
(agent-browser 0.33.2) `find role button click --name "Edit" --exact` reported
no match while the hovered toolbar was showing `title="Edit"`. Click it by
selector instead: `agent-browser click '#msg-ops-104 .msg-toolbar button[title="Edit"]'`
(the row's `id` is `msg-<room>-<seq>`). The DM bubble's buttons are also
title-only: hover `#dm-msg-m2` and click `#dm-msg-m2 button[title="More"]`;
`aria-label="More"` matches nothing. For DMs, the row has the accessible label Message from kyle, the bubble toolbar has More, and its menu item is Edit Message. After opening, wait for the textbox named Edit message and focus it before pressing Enter. Use the button named save for the mouse path.

Capture the open editor and the result, including accessibility snapshots. Observe the target message's content and edit metadata and record outbound edits. Include a changed-content control to prove that the save path actually ran.

The 2026-09-09 unchanged-edit run attached actual ChatSession edit methods to the fixture's loaded state with a recording transport. Its reproducible adapter and browser script live in `/Users/dboon/Documents/dev-notes/unchanged-message-edit/`. The channel and DM journeys proved unchanged Enter, reverted Save, and genuine edits. The channel journey also proved preservation of an existing edit timestamp. DM timestamp preservation was covered by the session regression.

### A role mention in the edit box (added 2026-11-07)

`?roleEdit=1` posts kyle's message "**Need from om://role/r-devops**" with a
line of member mentions and opens it already in the edit box
(`tools/visual/shell-fixture.tsx:1342-1353`, `:1653`). It exists on `/rooms/`
only; the `/chat/` fixture has no such seed.

```bash
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=room&alerts=quiet&roleEdit=1')"
agent-browser eval '(()=>{const t=document.querySelector("textarea[aria-label=\"Edit message\"]");return JSON.stringify({value:t.value,toks:[...document.querySelectorAll(".composer-token")].map(e=>e.textContent+"|"+e.className)})})()'
#   value "**Need from @Devops**\n- @ana @dax: please review the retention plan"
#   toks @Devops|composer-token composer-token-role, @ana and @dax as composer-token-mention
```

Driven 2026-11-07 on `/rooms/`: the `@Devops` chip measured 70 px for 66 px
of text with 2 px side padding, and the value held no `om://role`. Do not
test the `@` pick with another role here: the fixture's role-name stub
(`bindComposerUrisFor`, `:3505-3513`) knows only `r-devops`, so picking
**@traders** shows `@role:r-trader` and the raw URI. That is the stub, not the
product.

## Gotchas

- **Meta+A does not select the edit box's text in headless Chromium.** The
  empty-edit check then saves the old text and closes the editor. Select with
  `agent-browser eval` (`textarea.select()`), then press Backspace and Enter.
- **The empty-edit confirm is `session.openConfirm`.** On the `/rooms/` shell
  fixture it renders the **Delete Message** dialog; wrap `__om.openConfirm`
  with the session-capture shim
  ([message-actions.md](message-actions.md#forward-through-the-session-capture-shim-added-2026-11-09))
  to record its title and button.

The stock shell fixture substitutes commitEdit and commitDmEdit. Its timestamps are fixture behavior and cannot prove session logic. Use actual session methods for a session fix, and state when the transport is recorded rather than live.

On agent-browser 0.33.2, click does not document a --button option. Do not treat a successful command with that option as evidence of a right click. Use the visible toolbar and menu controls.

In the recorded DM journey, reopening the message menu after a save selected an incoming row. Fresh fixture navigations between cases avoided this fixture interaction; they did not prove persistence across reload. The fixture also logged a React invalid textarea value warning. Record it.

**Wait after hovering; do not hover twice.** The row toolbar settles for about
half a second after the pointer arrives (the row grows from 53 to 81 px), and a
`find role button` sent straight after `agent-browser hover` reports **Edit** or
**More** absent even though the button is in the row's `.msg-toolbar`. Scroll the
marked row into view in the marking eval (`r.scrollIntoView({block:"center"})`).
That is required, not tidy-up, for a row you just sent: the newest row sits
under the composer form, and `agent-browser hover` refuses with "covered by
<form.composer-form>". Then
run `agent-browser hover '[data-probe]'` once, wait about 0.6 s (`sleep 0.6`), then
click. Measured 2026-10-26 on both the channel and the DM path. A control of
two back-to-back hovers with no wait failed, so the earlier "hover twice" advice
only worked when command latency happened to supply the wait. On 2026-10-28 that exact sequence still missed **Edit** on the first try,
although `.msg-toolbar` already held the button and the row had grown to 81 px.
When the role lookup misses, read the toolbar directly (`[data-probe]
.msg-toolbar button[title="Edit"]`) and click it by selector, or hover once more
after the wait; never conclude the control is gone.

Full server persistence and other clients receiving the edit require the local auth/relay stack and daemon-pair lane. The fixture cannot prove those outcomes.
- **The inline editor is a lazy surface since `01bf4481`.** After **Edit**, a
  `role=status` skeleton named **Loading message editor**
  (`[data-inline-edit-loading]`) shows first, then the textbox **Edit message**
  mounts. Wait for the textbox; do not assert it synchronously.
- **`/chat/` cannot open the editor in the fixture.** The cloud shell fixture
  stubs `beginEdit` as `noop` (`apps/cloud/tools/visual/shell-fixture.tsx:2013`),
  so **Edit** on `/chat/` does nothing there. That is a harness limit, not a
  product failure.

### Verification record

**Last verified:** 2026-11-13 (nightly maintenance). **Product commit:** `504b08d5` (GitLab origin/main; rooms-client 0.117.0; 32 commits past `eae9681d`). **Scope:** `/rooms/` (18170), people stub and capture shim: with Vim on, the hint reads INSERT then NORMAL with "shift+escape to cancel • enter to save", Enter in NORMAL keeps the editor open, Shift+Escape closes it; with Vim off, an emptied edit + Enter opens **Delete Message** (**Delete**). **Limitations:** the delete was not confirmed; the char counter is source only; `/chat/` cannot open the editor. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261113/r1/` (frames 14, 16).

**Previous record:** 2026-11-09 (nightly maintenance). **Product commit:** `82390825` (GitLab origin/main; rooms-client 0.114.0; 49 commits past `08fe407b`). **Scope:** `/rooms/` (18183) `roleEdit=1`, with the people stub: **Edit message** holds `**Need from @Devops**…`. **Limitations:** saving the edit was not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261109/r1/`.

**Previous record:** 2026-11-08 (nightly maintenance). **Product commit:** `08fe407b` (GitLab origin/main; rooms-client 0.112.0; unchanged since the 2026-11-07 pass). **Scope:** `/rooms/` (18183) `roleEdit=1`: **Edit message** holds `**Need from @Devops**…` with the tokens **@Devops**, **@ana** and **@dax**. **Limitations:** saving the edit was not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261108/r1/`.

**Previous record:** 2026-11-07 (nightly maintenance). **Product commit:** `08fe407b` (GitLab origin/main; rooms-client 0.112.0; 89 commits past `ea399e62`). **Scope:** `/rooms/` (18180): toolbar **Edit** on `msg-ops-104` mounts `[aria-label="Edit message"]`; `?roleEdit=1` opens kyle's role message in the edit box with `@Devops` as a `.composer-token-role` chip (70 px for 66 px of text, 2 px padding) and no `om://role` in the value. `/chat/` (18181): **Edit** mounts nothing (the carried no-op). **Limitations:** picking **@traders** in the edit box shows `@role:r-trader`, because the fixture's role-name stub knows only `r-devops`; the save was not sent. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261107/r1/`.

**Previous record:** 2026-11-06 (nightly maintenance). **Product commit:** `ea399e62` (GitLab origin/main; rooms-client 0.111.0; 74 commits past `873a57ce`). **Scope:** `/rooms/` (18180): toolbar **Edit** on `msg-ops-104` mounts `[aria-label="Edit message"]`; `/chat/` (18181): neither the editor nor the loading marker after 2.5 s (the carried no-op). **Limitations:** the DM path not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261106/r1/`.

**Previous record:** 2026-11-05 (nightly maintenance). **Product commit:** `873a57ce` (GitLab origin/main; rooms-client 0.109.1; 17 commits past `ce14d4ba`). **Scope:** `/rooms/` (18170): hover `msg-ops-104` → toolbar **Edit** mounts `[aria-label="Edit message"]`. `/chat/` (18171): the same click mounts neither the editor nor `[data-inline-edit-loading]` after 4 s (the carried `/chat/` Edit no-op). **Limitations:** the DM **Edit Message** path was not re-driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261105/r1/` (`32`, `44`).

**Previous record:** 2026-11-04 (nightly maintenance). **Product commit:** `ce14d4ba` (GitLab origin/main; rooms-client 0.109.1; 16 commits past `ba4389e7`). **Scope:** `/rooms/` (18160): hover `#msg-ops-104` → `.msg-toolbar button[title="Edit"]` → the **Edit message** box. **Limitations:** save and `/chat/` not re-driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261104/r1/` (`edit-01`).

**Previous record:** 2026-11-03 (nightly maintenance). **Product commit:** `ba4389e7` (GitLab origin/main; rooms-client 0.108.0; one CI-only commit past `3f8f24bc`). **Scope:** `/rooms/` (18143): hover `#msg-ops-104` → `.msg-toolbar button[title="Edit"]` mounts the focused **Edit message** textarea. **Limitations:** a click sent right after another route load missed once and worked when re-driven. Save and wire edits unchanged. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261103/r1/` (`ma-rooms-03-edit`).

**Previous record:** 2026-11-02 (nightly maintenance). **Product commit:** `3f8f24bc` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18137): hover **Message from kyle** → **Edit** (`--exact`) → the **Edit message** textbox mounted focused → typed and Enter → the row shows **(edited)**; `/chat/` (18138): the same **Edit** mounts no editor (the known no-op); **Edit Message** listed in the DM More menu on both hosts. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261102/r1/`.

**Previous record:** 2026-11-01 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18137): the toolbar **Edit** on `msg-ops-104` opened the inline **Edit message** editor with **cancel** and **save**; saving replaced the text and appended **(edited)**. In the DM, ana's bubble **More** → **Edit Message** opened the same editor. **Limitations:** relay persistence; the `/chat/` toolbar **Edit** still opens nothing (`beginEdit` no-op, re-confirmed). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261101/r1/` (`edit-01`, `edit-02`).

**Previous record:** 2026-10-31 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18135): `msg-ops-104` hover → `.msg-toolbar button[title="Edit"]` → the **Edit message** textbox focused; `?view=dm&dm=ana` `#dm-msg-m2` **More** → **Edit Message** → the **Edit message** textbox focused. **Limitations:** Saving, the `(edited)` label and `fixtureMermaidEdit` were not re-asserted; relay persistence; `/chat/` (`beginEdit` is a no-op there). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261031/r1/`.

**Previous record:** 2026-10-30 (scheduled maintenance). **Product commit:** `47cb13bf` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/`: hovering `msg-ops-104` and clicking `button[title="Edit"]` mounted **Edit message** focused; **save** rendered "edited by maint 1030". In `#/dm/ana`, `dm-msg-m2` → `button[title="More"]` → **Edit Message** mounted the editor focused. **Limitations:** Fixture commit only; `/chat/` stubs `beginEdit`. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261030/r1/` (frames 26, 26a, 52).

**Previous record (channel path):** 2026-10-29 (nightly maintenance). **Product commit:** `cdfb1b0f` (origin/main). **Scope:** On `/rooms/`, a message just sent from the composer ("nightly 1029 probe") was marked, scrolled to centre, hovered once and given 0.6 s. Then `find role button --name Edit --exact` landed on the first try and opened the **Edit message** textbox with the old text. Typing " edited" plus Enter closed the editor, and the row read "nightly 1029 probe edited (edited)". Without the scroll, `hover` refused: the newest row sits under `form.composer-form`, the click point is covered, and no toolbar appears. **Limitations:** The DM path and `/chat/` were not re-driven; this is local fixture edit state only. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261029/r1/` (frame 30).

**Previous record (channel path):** 2026-10-28 (nightly maintenance). **Product commit:** `2dd7aad1` (origin/main). **Scope:** On `/rooms/`, kyle's `msg-ops-104` → **Edit** opened the **Edit message** textbox; a changed value plus **save** closed the editor, and the row read "edited by nightly 1028 (edited)". The first `hover` plus 0.6 s plus `find role button --name Edit --exact` reported no **Edit**, although `.msg-toolbar` held `button[title="Edit"]` and the row had grown to 81 px. A second hover succeeded. **Limitations:** The DM path and `/chat/` were not re-driven; this is local fixture edit state only. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261028/r1/` (frame 32).

**Previous record (DM path):** 2026-10-27 (maintenance re-drive). **Product commit:** `6c15b0fb286e9dc1b6cb130c9c97cd7e0afa9254` (origin/main). **Scope:** On `/rooms/` `?view=dm&dm=ana`, hovering kyle's last bubble → **More** → menuitem **Edit Message** → textbox **Edit message** → **save** replaced the text and closed the editor. **Open question, not yet a product finding:** no `edited` label rendered on the DM bubble. The fixture's `commitDmEdit` sets top-level `message.editedAt` (`tools/visual/shell-fixture.tsx:3553`), and the bubble label is gated on `flags.bubbles && entry.editedAt` (`MessageRow.tsx:3252`). The session's real DM edit paths write `metadata.editedAt` instead (`lib/session.ts:11927`, `:12306`). Whether a real edited DM shows the label was not traced; prove it on the daemon-pair lane before reporting it. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261027/r1/` (frame 15).

**Previous record:** verified 2026-10-27. **Product commit:** `6c15b0fb286e9dc1b6cb130c9c97cd7e0afa9254` (origin/main). **Scope:** On `/rooms/`, kyle's `msg-ops-108` **Edit** showed **Loading message editor**, then the **Edit message** textbox; `save` closed it, and the row read the new text plus `(edited)`. On `/chat/`, **Edit** was a no-op (fixture `beginEdit: noop`). **Limitations:** The DM **More** → **Edit Message** path was not re-driven. Local fixture edit state only; relay persistence and other viewers are pending. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261027/r01/` (frames 18-19, 40). Previous record: 2026-10-26 at `5820fbea`.
