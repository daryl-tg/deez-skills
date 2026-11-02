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
  toolbar's **More** it lists the same 19: the tile row (`MenuQuickBar`,
  `:3385-3389`, with the four recent emoji above it) is unconditional, so the
  quick tiles sit in the menu whether or not the toolbar is showing (measured
  2026-11-02 on both hosts, by a real click and by `eval`). The 11-entry
  reading recorded on 2026-10-31 and 2026-11-01 did not reproduce; read the
  whole menu after it has settled rather than trusting a count.
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

### Touch: long-press sheet and swipe to reply (added 2026-11-01)

`MessageTouchRow` (`MessageTouchRow.tsx:41-145`) spreads `useRowTouch`'s
pointer handlers onto every `[data-message-row]` that is not pending
(`MessageRow.tsx:2293`), and those handlers act only on `pointerType ===
"touch"` (`lib/touch.ts:108-200`). There is no coarse-pointer or
`maxTouchPoints` gate, so a synthetic `PointerEvent` with `pointerType:
"touch"` drives both gestures, **provided the dispatches are paced**: React
flushes a `pointermove` update after the event, not inside it, so read the
row after an `await`, and keep one `pointerId` across the sequence. Driven
2026-11-01 at 390×844 on `/rooms/` (`936f5b64`):

```bash
agent-browser eval '(async()=>{const w=ms=>new Promise(r=>setTimeout(r,ms));const r=document.getElementById("msg-ops-104");
  const b=r.getBoundingClientRect();const x=b.left+40,y=b.top+b.height/2;
  const p=(t,cx)=>r.dispatchEvent(new PointerEvent(t,{pointerType:"touch",pointerId:6,isPrimary:true,bubbles:true,cancelable:true,clientX:cx,clientY:y,button:0,buttons:1}));
  p("pointerdown",x);await w(30);p("pointermove",x+20);await w(30);p("pointermove",x+45);await w(80);
  const mid=r.style.transform;p("pointermove",x+70);await w(80);const far=r.style.transform;p("pointerup",x+70);await w(500);
  return JSON.stringify({mid,far,after:r.style.transform})})()'
#   {"mid":"translateX(45px)","far":"translateX(60.9px)","after":"translateX(0px)"}
#   with .swipe-reply-hint visible mid-swipe and the composer strip reading
#   "Replying to kyle: @ana the alert fired twice…" plus a Cancel reply button
```

Past `SWIPE_COMMIT_PX` (56) the pull gains resistance (70 → 60.9), and the
release past the commit calls `session.setReplyTarget`, which the fixture
implements (`shell-fixture.tsx:3443`). A long press is `pointerdown`, a 700 ms
wait, `pointerup` on the same row: it opens the row menu as a sheet,
`div.msg-sheet[role=menu][data-mobile-sheet]` behind `.msg-sheet-backdrop`,
22 menu items for `msg-ops-104`; Escape closes it.

**Pull to refresh did not fire.** `usePullToRefresh` (`lib/touch.ts:227-290`)
listens for native `touchstart`/`touchmove` on the `[data-tape-scroller]` and
calls `history.backfill` when the pull passes 56 px. Synthetic `TouchEvent`s
reached that element (a capturing listener on `document` saw `touches.length`
1 with the scroller as target, `scrollTop` 0 throughout), but the hook's
`touchmove` never called `preventDefault` and no `.ptr-pull` spacer rendered,
on three attempts including a synchronous one. Pending: either the hook is not
bound (its effect reads `scrollerRef.current` once, keyed on `[enabled,
scrollerRef]`, so a scroller that mounts after the first commit never binds)
or the lane needs real touch emulation. Drive it on a device or with CDP touch
before calling it a product gap.

## Gotchas

- **A mid-session `set viewport` can leave the hover toolbar dead.** A scripted
  session that drove the 390 px composer, switched back to 1440×900 and then
  hovered `#msg-ops-104` got **More** to "click" with zero `menuitem`s, and
  **Edit** mounted no editor. The same steps in a fresh session gave the
  19-item menu and the **Edit message** box. Start a new
  `AGENT_BROWSER_SESSION` after any viewport change before driving hover
  surfaces (2026-11-02, `/rooms/`).
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

**Last verified:** 2026-11-03 (nightly maintenance). **Product commit:** `ba4389e7` (GitLab origin/main; rooms-client 0.108.0; one CI-only commit past `3f8f24bc`). **Scope:** `/rooms/` (18143) and `/chat/` (18144): the `msg-ops-104` hover toolbar (nine title-named buttons); **More** opens 19 entries; the **Agent** submenu (**Copy for Agent**, **Mark for agent ⌥M**, **Ask about this...**, **Capture to doc from here**); `reply=1` reads **Replying to dax**; the `dm-msg-m2` bubble menu has 13 items on both hosts. **Limitations:** the `/rooms/` bubble menu missed twice before opening, so re-read after a short wait. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261103/r1/` (`ma-*`).

**Previous record:** 2026-11-02 (scheduled maintenance). **Product commit:** `3f8f24bc` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18141) and `/chat/` (18142): hover `#msg-ops-104` → toolbar **More** → 19 `menuitem`s on both (👍, 🔥, 😂, ❤️, React, Reply, Topic, To-do, Forward, Edit Message, Copy Text, Copy Message Link, Bookmark Message, Save to Your Library, Pin Message, Mark Unread, Agent, Delete Message, Copy Message ID); `reply=1` → **Replying to dax** with **Cancel reply** on both. **Limitations:** the DM menu, right-click, swipe and long-press were not re-driven; a first scripted attempt after a viewport change returned 0 items (new gotcha). Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261102/r1/`.

**Previous record:** 2026-11-02 (nightly maintenance). **Product commit:** `3f8f24bc` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18137) and `/chat/` (18138): the hover toolbar (React 👍 / 🔥 / 😂, Add reaction, Reply, Edit, Turn into topic, Add to Channel To-dos, More, all `title`-named); **Reply** focuses the composer with **Cancel reply**; **More** and a right-click each list 19 entries (👍 🔥 😂 ❤️, React, Reply, Topic, To-do, Forward, Edit Message, Copy Text, Copy Message Link, Bookmark Message, Save to Your Library, Pin Message, Mark Unread, Agent, Delete Message, Copy Message ID); **Agent** → Copy for Agent, Mark for agent ⌥M, Ask about this..., Capture to doc from here (`/rooms/`); the DM More menu (13, with **Edit Message**); at 390×844 on `/rooms/` the paced touch swipe (45 px hint, 60.9 px, settle to 0, **Replying to kyle**) and the 700 ms long press → `.msg-sheet[role=menu][data-mobile-sheet]` with 22 items. **Limitations:** the toolbar **More** listed 19, not the 11 recorded on 2026-10-31 and 2026-11-01, on both hosts and with a real click (see the Message menu bullet); pull to refresh was not re-attempted. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261102/r1/`.

**Previous record:** 2026-11-01 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18137) on `msg-ops-104`: a right-click lists 19 items (the four quick emoji, React, Reply, Topic, To-do, then the eleven verbs through **Copy Message ID**) and the hover toolbar's **More** lists the eleven verbs; the **Agent** submenu (Copy for Agent, Mark for agent, Ask about this..., Capture to doc from here); the toolbar (React 👍 / 🔥 / 😂, Add reaction, Reply, Edit, Turn into topic, Add to Channel To-dos, More); toolbar **Reply** → **Replying to kyle: …** with the composer focused and **Cancel reply**; `?reply=1` → **Replying to dax**; at 390 a long press opened the 22-item sheet and a swipe past 56 px set the same reply target (section above). `/chat/` (18138): the right-click and **More** menus, the **Agent** submenu and the toolbar **Reply**. **Limitations:** every verb is still a fixture no-op; **Turn into topic** and **Add to Channel To-dos** stay inert; pull to refresh did not fire. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261101/r1/` (`actions-01` to `actions-06`, `touch-01`, `touch-02`, `chat-10`, `chat-11`).

**Previous record:** 2026-10-31 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18135): hover `msg-ops-104` → toolbar **React 👍 / 🔥 / 😂**, **Add reaction**, **Reply**, **Edit**, **Turn into topic**, **Add to Channel To-dos**, **More**; **More** → 11 items; a right-click on the row → 19 items; **Agent** → **Copy for Agent**, **Mark for agent** ⌥M, **Ask about this...**, **Capture to doc from here**; `?reply=1` strip and **Reply** retarget; **Turn into topic** inert. `?view=dm&dm=ana`: `#dm-msg-m2` **More** → 13 items. `/chat/` (18136): the same toolbar, **More** → 11, **Agent** submenu (4), DM **More** → 13, `?reply=1` and the **Reply** retarget. **Limitations:** Every verb is a fixture no-op; the clipboard was not read back; **File as source**, **Summarize thread** and **Remove Link Previews** have no seed. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261031/r1/`.

**Previous record:** 2026-10-30 (scheduled maintenance). **Product commit:** `47cb13bf` (GitLab origin/main; rooms-client 0.108.0). **Scope (`/rooms/`, fixture lane):** On `#ops` `msg-ops-104`, the hover toolbar showed its nine title-named buttons, and **More** opened the 19-item menu listed above. Hovering **Agent** opened the submenu with **Copy for Agent**, **Mark for agent ⌥M**, **Ask about this...** and **Capture to doc from here**. On `#/dm/ana`, `dm-msg-m2`'s **More** opened the 13-item DM menu, and **Edit Message** opened the focused editor. **Limitations:** No verb was pressed for its effect (every one is a fixture no-op), the clipboard was not read, and `/chat/` was not driven. **File as source**, **Summarize thread** and **Remove Link Previews** have no seed. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261030/r1/` (frames 49-50, 52).
