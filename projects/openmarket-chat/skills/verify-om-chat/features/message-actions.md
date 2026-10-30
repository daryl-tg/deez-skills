# Message actions

The message menu and the hover toolbar on a sent message: copy, link, bookmark,
pin, save to the library, forward, mark unread, delete, and the **Agent**
submenu that hands a message to an agent. Editing has its own guide,
[message-editing.md](message-editing.md); forwarding's modal and reactions are
covered in the README inventory and [polls-and-reactions.md](polls-and-reactions.md).

## Sub-features

- **Hover toolbar** on a channel row (`.msg-toolbar`, a CSS hover): React 👍 /
  🔥 / 😂, **Add reaction**, **Reply**, **Edit** (own message), **Turn into
  topic**, **Add to Channel To-dos** and **More**. Every button is named by
  `title` only.
- **Message menu** (`MessageRow.tsx:3380-3560`). Opened by a right-click on
  kyle's `#ops` row it lists 19 items: four quick reactions, **Add Reaction**,
  **Reply**, **Turn into topic...**, **Add to Channel To-dos**, **Forward**,
  **Edit Message**, **Copy Text**, **Copy Message Link**, **Bookmark
  Message**, **Save to Your Library** (`:3469`), **Pin Message**, **Mark
  Unread**, **Agent**, **Delete Message** and **Copy Message ID** (`:3550`). Opened from the hover
  toolbar's **More**, the same menu lists 11: the quick tiles (the four emoji,
  **React**, **Reply**, **Topic**, **To-do**) ride the toolbar and the menu
  starts at **Forward** (measured 2026-10-31 on both hosts).
- **Agent submenu** (`MessageRow.tsx:2225-2270`): **Copy for Agent**, **Mark
  for agent** (⌥M), **Ask about this...** and **Capture to doc from here**.
  **Copy for Agent (since here)** and **Summarize thread** appear only in
  their states (a later run of messages; a message with replies). **File as
  source** (`:3484`) appears only when the roster's source-capture scope is
  active.
- **DM bubble menu**: the same verbs in a shorter list, 13 items on kyle's DM
  message: four quick reactions, **Add Reaction**, **Copy Text**, **Reply**,
  **Mark Unread**, **Forward**, **Pin Message**, **Edit Message**, **Delete
  Message** and **Copy Message ID**.
- **Remove Link Previews** (`MessageRow.tsx:3527`) shows only on a message
  with `unfurls`, which no fixture seeds.

## How to get to it (user POV)

Hover a message and use the small toolbar, or press **More** for the full
menu. In a DM, hover the bubble and press **More**. Point at **Agent** to hand
the message to an agent: copy it in an agent-ready form, mark it for the next
agent run, ask about it, or capture the conversation from here into a doc.

## Driving it with control-om-chat

```bash
export OM_CHAT_LANE_PORT=<assigned-port>
control-om-chat doctor && control-om-chat up
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=room&alerts=quiet')"
agent-browser eval '(()=>{const r=document.getElementById("msg-ops-104");
  r.scrollIntoView({block:"center"}); r.setAttribute("data-probe","1"); return 1})()'
agent-browser hover '[data-probe]'
sleep 0.8
agent-browser click '#msg-ops-104 .msg-toolbar button[title="More"]'
```

Read the menu through the DOM. This pass did so throughout, because `snapshot -i`
listed none of the library doc menu's `menuitem`s on the same lane:

```bash
agent-browser eval '(()=>JSON.stringify([...document.querySelectorAll("[role=menuitem]")]
  .map(m=>m.textContent.trim())))()'
```

For the Agent submenu, mark the **Agent** item and hover it with a real
pointer (`aria-haspopup="menu"`), then read the second `[role=menu]`:

```bash
agent-browser eval '(()=>{const a=[...document.querySelectorAll("[role=menuitem]")]
  .find(m=>m.textContent.trim()==="Agent"); a.setAttribute("data-probe-agent","1"); return 1})()'
agent-browser hover '[data-probe-agent]'
```

The DM path is `?view=dm&dm=ana&alerts=quiet`: hover `#dm-msg-m2`, then click
`#dm-msg-m2 button[title="More"]`.

### Hover toolbar: Reply, Turn into topic, To-dos (added 2026-10-31)

Open `shell-fixture.html?view=room&alerts=quiet&reply=1`. The composer shows
the reply strip **Replying to dax** with a **Cancel reply** button
(`Composer.tsx:5610`; the fixture seeds seq 103, `shell-fixture.tsx:2429`).
Scroll `#msg-ops-104` into view, hover it, and click
`#msg-ops-104 .msg-toolbar button[title="Reply"]`: the strip retargets to
**Replying to kyle: @ana the alert fired twice last night …** and the composer
textarea takes focus. Driven on `/rooms/` and `/chat/` at `936f5b64`.

**Turn into topic** (`[data-turn-into-topic]`, `MessageRow.tsx:3249`) calls
`session.openTopicDraft`, and **Add to Channel To-dos** (`:3263`) calls
`openTodoPromote`. Neither is stubbed in the shell fixture, so both resolve to
`INERT` and nothing opens: no aside, no dialog, no route change. Prove the
offer (the buttons render by `title`) and leave the effect pending. The quick
reactions **React 👍 / 🔥 / 😂** were not pressed.

## Gotchas

- **The toolbar buttons have no `aria-label`.** Their names come from
  `title`, `find role button --name "Edit" --exact` reported no match on
  2026-10-30, and `button[aria-label="More"]` matches nothing. Click by
  `button[title="…"]` inside the row's `id` (`msg-<room>-<seq>`, or
  `dm-msg-<id>` in a DM).
- **Every verb is a fixture no-op except the clipboard.** The shell fixture
  stubs `toggleBookmark`, `togglePin`, `markUnreadFrom`, `removeUnfurls`,
  `askAgentAboutMessage`, `summarizeThreadWithAgent` and `captureFromSeq`
  as `noop` or `asyncNoop` (`shell-fixture.tsx:3484-3566`), and `openForward` never sets
  `forwardSource`. Prove the offer here; the effects need the daemon-pair lane.
  The copy verbs write to the clipboard, which this lane did not read back.
- A data attribute set by `eval` can vanish when React re-renders the row.
  Prefer the row's `id` in selectors after the hover.

## Verification record

**Last verified:** 2026-10-31 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18135): hover `msg-ops-104` → toolbar **React 👍 / 🔥 / 😂**, **Add reaction**, **Reply**, **Edit**, **Turn into topic**, **Add to Channel To-dos**, **More**; **More** → 11 items; a right-click on the row → 19 items; **Agent** → **Copy for Agent**, **Mark for agent** ⌥M, **Ask about this...**, **Capture to doc from here**; `?reply=1` strip and **Reply** retarget; **Turn into topic** inert. `?view=dm&dm=ana`: `#dm-msg-m2` **More** → 13 items. `/chat/` (18136): the same toolbar, **More** → 11, **Agent** submenu (4), DM **More** → 13, `?reply=1` and the **Reply** retarget. **Limitations:** Every verb is a fixture no-op; the clipboard was not read back; **File as source**, **Summarize thread** and **Remove Link Previews** have no seed. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261031/r1/`.

**Previous record:** 2026-10-30 (scheduled maintenance). **Product commit:** `47cb13bf` (GitLab origin/main; rooms-client 0.108.0). **Scope (`/rooms/`, fixture lane):** On `#ops` `msg-ops-104`, the hover toolbar showed its nine title-named buttons, and **More** opened the 19-item menu listed above. Hovering **Agent** opened the submenu with **Copy for Agent**, **Mark for agent ⌥M**, **Ask about this...** and **Capture to doc from here**. On `#/dm/ana`, `dm-msg-m2`'s **More** opened the 13-item DM menu, and **Edit Message** opened the focused editor. **Limitations:** No verb was pressed for its effect (every one is a fixture no-op), the clipboard was not read, and `/chat/` was not driven. **File as source**, **Summarize thread** and **Remove Link Previews** have no seed. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261030/r1/` (frames 49-50, 52).
