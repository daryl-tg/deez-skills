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
- **Message menu** (`MessageRow.tsx:3486-3667`). Opened by a right-click on
  kyle's `#ops` row it lists 19 items: four quick reactions, **Add Reaction**,
  **Reply**, **Turn into topic...**, **Add to Channel To-dos**, **Forward**,
  **Edit Message**, **Copy Text**, **Copy Message Link**, **Bookmark
  Message**, **Save to Your Library** (`:3575`), **Pin Message**, **Mark
  Unread**, **Agent**, **Delete Message** and **Copy Message ID** (`:3657`). Opened from the hover
  toolbar's **More** it lists the same 19: the tile row (`MenuQuickBar`,
  `:3491-3495`, with the four recent emoji above it) is unconditional, so the
  quick tiles sit in the menu whether or not the toolbar is showing (measured
  2026-11-02 on both hosts, by a real click and by `eval`). The 11-entry
  reading recorded on 2026-10-31 and 2026-11-01 did not reproduce; read the
  whole menu after it has settled rather than trusting a count.
- **Menus stay on screen** (since `bcff299e`): opened near the bottom or right
  edge, the menu flips up or left instead of running off the viewport, and
  keeps its side as lazy rows land (`shared/ui/Popover.tsx`,
  `useMenuPosition`). The same placement serves the sidebar, channel, topic,
  user and People-pane menus and the **Agent** flyout.
- **Agent submenu** (`MessageRow.tsx:2304-2355`): **Copy for Agent**, **Mark
  for agent** (⌥M), **Ask about this...** and **Capture to doc from here**.
  **Copy for Agent** and **Copy for Agent (since here)** need the host's
  `daemonFeatures` (`MessageRow.tsx:2309`, `:2317`; `d3aebbb5`): true on
  `/rooms/` (`src/lib/session-host.ts:2`), false on `/chat/`
  (`apps/cloud/src/lib/session-host.ts:3`). So on `/chat/` the flyout reads
  **Mark for agent**, **Ask about this...** and **Capture to doc from here**
  only (both hosts driven 2026-11-13: open **More**, then `find role menuitem
  hover --name "Agent"`).
  **Copy for Agent (since here)** and **Summarize thread** appear only in
  their states (a later run of messages; a message with replies). **File as
  source** (`:3587`) appears only when the roster's source-capture scope is
  active.
- **DM bubble menu**: the same verbs in a shorter list, 13 items on kyle's DM
  message: four quick reactions, **Add Reaction**, **Copy Text**, **Reply**,
  **Mark Unread**, **Forward**, **Pin Message**, **Edit Message**, **Delete
  Message** and **Copy Message ID**.
- **Remove Link Previews** (`MessageRow.tsx:3634`) shows only on a message
  with `unfurls`, which no fixture seeds.
- **Forward** from the message menu opens **Forward message** with a **Comment** box (needs the session-capture shim; see the Forward section).
- **Keys on a focused row** (`lib/message-keyboard.ts:12-30`, `MessageRow.tsx:2177-2219`):
  ArrowUp/ArrowDown walk the rows, **R** replies, **E** edits your own
  message, **Delete** asks to delete it (Shift+Delete skips the confirm),
  **+** or **=** opens the emoji picker, **M** opens the message menu, **P**
  opens the author's profile card and **Enter** opens the row's first link or
  image. Alt, Ctrl or Meta held turns them off.
- **Image right-click menu** (`lib/image-menu.ts`, `MediaGallery.tsx:1276`):
  **Copy Image**, **Save Image** and **Open in Browser**. Copy stays greyed
  ("Available after security scan") while the scan is pending.
- **Nothing renders for an attachment still being scanned**
  (`ScanState.tsx:31`, `MediaGallery.tsx:1217`): `ScanPendingCard` returns
  `null`, so the row keeps its text and shows no placeholder and no Retry.
- **@role pill → role popover** (`MessageRow.tsx:2710-2724`, `RolePopover.tsx`,
  `Shell.tsx:4727`): clicking a role mention opens **<Role> role members**
  with "<Role> — <n>" and one row per known holder.

## How to get to it (user POV)

Hover a message and use the small toolbar, or press **More** for the full
menu. In a DM, hover the bubble and press **More**. Point at **Agent** to hand
the message to an agent: copy it in an agent-ready form, mark it for the next
agent run, ask about it, or capture the conversation from here into a doc.

From the keyboard, focus a message and press **R**, **E**, **Delete**, **+**,
**M**, **P** or **Enter**. Right-click an image to copy, save or open it.
Click an **@role** mention to see who holds the role.

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
(`Composer.tsx:6310`; the fixture seeds seq 103, `shell-fixture.tsx:2440`).
Scroll `#msg-ops-104` into view, hover it, and click
`#msg-ops-104 .msg-toolbar button[title="Reply"]`: the strip retargets to
**Replying to kyle: @ana the alert fired twice last night …** and the composer
textarea takes focus. Driven on `/rooms/` and `/chat/` at `936f5b64`.

**Turn into topic** (`[data-turn-into-topic]`, `MessageRow.tsx:3349`) calls
`session.openTopicDraft`, and **Add to Channel To-dos** (`:1846`, `:3363`) calls
`openTodoPromote`. Neither is stubbed in the shell fixture, so both resolve to
`INERT` and nothing opens: no aside, no dialog, no route change. Prove the
offer (the buttons render by `title`) and leave the effect pending. The quick
reactions **React 👍 / 🔥 / 😂** were not pressed.

On a server whose to-dos run in records mode (Projects), the same toolbar
button and menu entry read **Ticket** (since `c99f628c`; **Make ticket**
before), with aria "Make a ticket from this message" (`MessageRow.tsx:1836-1846`),
for any member of the server, a
read-only channel included (`08dea2dd`); a visitor to a public channel sees
neither. Both fixtures leave `session.todos`
unstubbed, so `modeFor` answers `INERT`, which is neither `"off"` nor
`"records"`, and the legacy **To-do** / **Add to Channel To-dos** shows
(re-driven 2026-11-07 on both hosts). With the Projects stub from [projects.md](projects.md)
(`modeFor` "records", `memberOf` true) the **More** menu lists **Ticket** in
place of **To-do**, 19 entries on both hosts (driven 2026-11-13).

### Touch: long-press sheet and swipe to reply (added 2026-11-01)

`MessageTouchRow` (`MessageTouchRow.tsx:41-145`) spreads `useRowTouch`'s
pointer handlers onto every `[data-message-row]` that is not pending
(`MessageRow.tsx:2378`), and those handlers act only on `pointerType ===
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
implements (`shell-fixture.tsx:3470`). A long press is `pointerdown`, a 700 ms
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

### Menus flip at the viewport edge (added 2026-11-05)

There is no `data-side` attribute; read the `role=menu` box and its inline
`--pop-origin`. Size the viewport short before the first navigation, then
scroll the tape so a member's row sits near the bottom:

```bash
agent-browser open about:blank && agent-browser set viewport 1440 700
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=room&alerts=quiet')"
agent-browser eval '(()=>{const s=document.querySelector("[data-tape-scroller]");const r=document.querySelector("#msg-ops-110");s.scrollTop-=(560-r.getBoundingClientRect().top);return 1})()'
agent-browser hover "#msg-ops-110"
agent-browser click "#msg-ops-110 button[aria-label=More]"
agent-browser eval '(()=>{const m=document.querySelector("[role=menu]").getBoundingClientRect();return [m.top,m.bottom,innerHeight]})()'
```

Driven 2026-11-05 on both hosts: **More** at y 546 opened the 16-entry menu
upward, `top 151`, `bottom 542` (4 px above the button), `--pop-origin:
bottom right`, ending in **Agent** and **Copy Message ID**. A `contextmenu` at
y 681 flipped to `bottom 679` (2 px above the cursor). The last rows of `#ops`
(`msg-ops-190`–`192`) are a system line and topic cards with no **More**
button, so use `msg-ops-110`.

Re-driven 2026-11-07 on both hosts after `d1a25e38` (a menu now measures its
full row height and flips when there is more room above): the same `top 151`,
`bottom 542`, `--pop-origin: bottom right`. On `/chat/` the **More** button
sits at x 1364, so after the click the pointer rests over the flipped menu's
**Agent** row and its flyout opens on hover (4 entries, `top 534`, `bottom
676`, `--pop-origin: top right`). Move the pointer away
(`agent-browser mouse move 700 60`) before reading the root menu's box, and
read every `[role=menu]`, not the first.

### The **Agent** flyout by keyboard (added 2026-11-07)

Since `30129c57`, Enter, Space or ArrowRight on a submenu row is meant to open
its flyout with focus on the first enabled row, and ArrowLeft or Escape inside
the flyout to close it back onto the row (`ContextMenu.tsx:262-269`,
`:93-98`). Open **More** on `msg-ops-104`, press ArrowDown until
`document.activeElement` is **Agent** (`data-submenu-index="11"`), then press
Enter. Driven 2026-11-07 on both hosts: the flyout mounts (`aria-expanded="true"`,
4 entries) but focus stays on **Agent**, so a further ArrowDown moves within
the root menu and the flyout's ArrowLeft/Escape path cannot be reached.
ArrowRight behaves the same. That is recorded as a product gap, not a recipe
fault; prove the flyout by focus position, not by its mount.

Re-driven 2026-11-08 on both hosts with `HTMLElement.prototype.focus` wrapped
by an `eval` before the key press. ArrowRight mounts the flyout about 18 ms
later, and the flyout's effect does call `focus()` on **Copy for Agent**, but
at that moment the flyout's computed `visibility` is still `hidden`. Chromium
refuses to focus a hidden element, so no `focusin` fires. Which rule still
hides it was not traced: `ContextMenu.tsx:119` hides the flyout until it is
measured, and the effect waits on that same `pos.measured`. A manual `focus()` on the same
row a moment later lands. `test/context-menu-submenu.test.ts:110-116` asserts
the focus under happy-dom, which does not enforce `visibility`, so it passes.

### Forward, through the session-capture shim (added 2026-11-09)

Both fixtures spell out `openForward: noop` and `forwardSource: null`, so no
click opens the modal and an `Object.prototype` stub cannot reach a spelled-out
key. The session-capture shim can: it wraps `window.Proxy`, keeps the
`autofill` target as `window.__om`, and lets you assign over spelled-out keys.
Any `__om` mutation repaints only after `__om.closeConfirm()`, which sets
`confirmDialog = null` and calls the fixture's `emit()`.

```bash
cat > "$SCRATCH/session-capture-shim.js" <<'JS'
(() => {
  const P = Proxy;
  window.Proxy = new P(P, { construct(t, a) {
    const r = Reflect.construct(t, a);
    const [g, h] = a;
    if (g && typeof g === "object" && h && typeof h.has === "function" && "getVersion" in g) window.__om = g;
    return r;
  } });
})();
JS
agent-browser --init-script "$SCRATCH/fixture-people-stub.js" \
  --init-script "$SCRATCH/session-capture-shim.js" open about:blank
```

```bash
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=room&alerts=quiet')"
agent-browser eval '(()=>{const o=window.__om;o.openForward=(s)=>{o.forwardSource=s;o.closeConfirm()};o.closeForward=()=>{o.forwardSource=null;o.closeConfirm()};return 1})()'
agent-browser hover '#msg-ops-104'
agent-browser click '#msg-ops-104 .msg-toolbar button[title="More"]'
agent-browser find role menuitem click --name "Forward"
# -> heading "Forward message", textbox "Comment", button "Forward" (disabled until a destination is picked)
```

The source handed to `openForward` carries `kind`, `room`, `seq`, `handle`,
`preview`, `text`, `ts`, `attachments`, `authorUserId`, `authorDisplayName` and
`authorHandle`. Picking a destination and sending were not driven.

### Keys on a focused row (added 2026-11-10)

Each row is `[data-message-row]` with `tabIndex=-1` and the name "Message
from <author>". The handler ignores any key whose target is not the row
itself, so focus the row, not a button inside it. kyle is the viewer: his
rows in `#ops` are `#msg-ops-104` and `#msg-ops-108`.

```bash
# people stub + session-capture shim (README), ?view=room&alerts=quiet
agent-browser eval 'document.getElementById("msg-ops-104").focus()'
agent-browser press ArrowDown          # activeElement -> msg-ops-105
agent-browser press r                  # "Replying to kyle: …" with Cancel reply
agent-browser eval 'document.getElementById("msg-ops-108").focus()'
agent-browser press e                  # textarea "Edit message" in msg-ops-108 (mounts ~1 s later)
agent-browser press Delete             # alertdialog "Delete Message"
agent-browser press +                  # dialog "Choose an emoji", "Search emoji" focused
#   pick the button titled ":100:" -> html[data-fixture-reaction="ops:108:💯"]
agent-browser press m                  # message menu (Forward, Edit Message, Copy Text, …)
```

**P** calls `session.openProfileCard`, which neither fixture defines; the key
is consumed (`defaultPrevented`) and nothing opens. Stub it through the shim
(`profileCard` is a spelled-out field, so redefine it with a getter):

```bash
agent-browser eval '(()=>{const o=window.__om;let c=null;
  Object.defineProperty(o,"profileCard",{get:()=>c,configurable:true});
  o.openProfileCard=(t)=>{c=t;o.closeConfirm()};o.closeProfileCard=()=>{c=null;o.closeConfirm()};return 1})()'
agent-browser eval 'document.getElementById("msg-ops-105").focus()'
agent-browser press p                  # dialog "Profile for ana"
```

On `/chat/` the cloud fixture spells `beginEdit: noop` and `editingSeq: null`,
so **E** opens nothing until you stub both:
`o.beginEdit=(s)=>{o.editingSeq=s;o.closeConfirm()}` (and `cancelEdit` the
same way). The editor then mounts in the row, empty. **Enter** needs a row
with a link or image: with `&tape=mosaic5`, focusing `#msg-ops-116` and
pressing Enter opens the image viewer "mosaic-1.svg · 1/5".

**E** on someone else's row is not consumed: the shell's printable-key branch
moves it into the composer (`data-fixture-draft="e"`).

### Image right-click menu (added 2026-11-10)

Only the root fixture seeds images. `&tape=mosaic5` adds dax's five-image post
(`#msg-ops-116`, `mosaic-1.svg`…, `scanStatus: "clean"`, data-URL
`signedUrlFor`). Dispatch `contextmenu` on the tile and spy the effects:

```bash
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=room&alerts=quiet&tape=mosaic5')"
agent-browser eval '(()=>{window.__opened=[];window.open=(...a)=>{window.__opened.push(a);return null};
  window.__dl=[];HTMLAnchorElement.prototype.click=function(){window.__dl.push(this.download)};
  window.__om.attachmentBlob=async()=>new Blob(["<svg/>"],{type:"image/svg+xml"});
  const img=document.querySelector("#msg-ops-116 img.cursor-pointer"),r=img.getBoundingClientRect();
  img.dispatchEvent(new MouseEvent("contextmenu",{bubbles:true,cancelable:true,clientX:r.x+20,clientY:r.y+20}));return 1})()'
# menu: Copy Image, Save Image, Open in Browser (all enabled for a clean image)
agent-browser find role menuitem click --name "Open in Browser"   # __opened: [data:image/svg+xml…, "_blank", "noopener,noreferrer"]
# reopen, then Save Image -> __dl ["mosaic-1.svg"]
# reopen, then Copy Image -> navigator.clipboard.write gets one ClipboardItem of image/svg+xml
```

`attachmentBlob` is unstubbed in both fixtures. Without the stub above, Save
throws on `URL.createObjectURL`, and Copy showed no toast on the lane.

### An attachment still being scanned (added 2026-11-10)

`ScanPendingCard` renders `null` by design. To see the difference, keep the
late image's URL from ever arriving and flip its scan status through the shim:

```bash
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=room&alerts=quiet&lateImage=1&lateImageDelay=99999999')"
#   msg-ops-101: "Image unavailable" with Retry (clean, no URL)
agent-browser eval '(()=>{const o=window.__om,rs=o.rooms.get("ops");
  rs.entries=rs.entries.map(e=>e.seq===101?{...e,attachments:e.attachments.map(a=>({...a,scanStatus:"pending"}))}:e);
  o.closeConfirm();return 1})()'
#   msg-ops-101: text only, no media node, no Retry
```

Replace the arrays rather than mutating them, or memoised rows keep the old
attachment. The cloud fixture has no `lateImage` seed, and an attachment
injected there stays on "Loading <name>" in both states, so this is `/rooms/`
only.

### @role popover (added 2026-11-10)

`&roleEdit=1` seeds kyle's post with `om://role/r-devops`, but opens it in the
editor; cancel the edit first. Neither fixture defines `openRoleCard`, and both
spell `roleCard: null`, so stub through the shim:

```bash
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=room&alerts=quiet&roleEdit=1')"
agent-browser eval '(()=>{const o=window.__om;o.cancelEdit();
  o.openRoleCard=(a)=>{o.roleCard={role:{roleId:a.roleId,name:"Devops",color:"#d19a3a"},
    holders:[{userId:"u-ana",username:"ana"},{userId:"u-dax",username:"dax"}],knownHolders:2,
    directoryTruncated:false,spaceId:a.spaceId,room:a.room,x:a.x,y:a.y};o.closeConfirm()};
  o.closeRoleCard=()=>{o.roleCard=null;o.closeConfirm()};o.closeConfirm();return 1})()'
agent-browser click '.mention-pill.role-mention'   # "@Devops" -> dialog "Devops role members", "Devops — 2", ana, dax
agent-browser press Escape                         # closes; roleCard back to null
```

The cloud fixture has no `roleEdit` seed and resolves only
`01j8x4kq7m2v9p3r6t0w5y8z1a` (Full Stack); `r-devops` there reads "@unknown
role". Set an entry's `text` to `ping om://role/01j8x4kq7m2v9p3r6t0w5y8z1a`
through `__om.rooms.get("ops")`, add the same stubs, and the pill opens **Full
Stack role members**.

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
  as `noop` or `asyncNoop` (`shell-fixture.tsx:3511-3595`), and `openForward` never sets
  `forwardSource`. Prove the offer here; the effects need the daemon-pair lane.
  The copy verbs write to the clipboard, which this lane did not read back.
- A data attribute set by `eval` can vanish when React re-renders the row.
  Prefer the row's `id` in selectors after the hover.

## Verification record

**Last verified:** 2026-11-13 (nightly maintenance). **Product commit:** `504b08d5` (GitLab origin/main; rooms-client 0.117.0; 32 commits past `eae9681d`). **Scope:** `/rooms/` (18170) and `/chat/` (18171), people and Projects stubs: the **More** menu (19 entries, **Ticket** in place of **To-do**); the **Agent** flyout with **Copy for Agent** on `/rooms/` and without it on `/chat/`; `tape=lists` task markers as `role=img`. **Limitations:** no menu verb's effect was driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261113/r1/` (frames 21-23).

**Previous record:** 2026-11-10 (scheduled maintenance). **Product commit:** `eae9681d` (GitLab origin/main, rooms-client 0.115.0). **Scope:** `/rooms/` (18141) and `/chat/` (18142) with the people stub and the session-capture shim. Focused-row keys on both hosts: ArrowDown, **R** (reply strip), **Delete** (**Delete Message**), **+** (**Choose an emoji**, then `:100:` stamped `ops:108:💯`), **M** (the menu: 11 items read 0.8 s after the key on `/rooms/`, 19 on `/chat/`; see the settling note under Sub-features), **P** (**Profile for ana**, with the `openProfileCard` stub), **E** (**Edit message**; on `/chat/` only with the `beginEdit` stub, and empty). On `/rooms/` only: **Enter** on the mosaic row opens the viewer; the image menu's three items with their window.open, download and clipboard effects; the pending-scan branch rendering nothing where a clean URL-less image shows "Image unavailable" and Retry. The @role popover on both hosts (`r-devops` on `/rooms/`, Full Stack injected on `/chat/`). **Limitations:** no real clipboard read-back; the disabled **Copy Image** state is not reachable (a pending attachment has no URL); Shift+Delete, and the menu verbs' effects, not driven; `/chat/` lacks the image, late-image and role seeds. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261110/r1/`.

**Previous record:** 2026-11-09 (scheduled maintenance). **Product commit:** `16da8ecf` (GitLab origin/main; one CI-only commit past `82390825`). `/rooms/` (18141) and `/chat/` (18142), with the people stub and the session-capture shim: `#msg-ops-104` **More** → **Forward** opens **Forward message** with **Comment** and a disabled **Forward**, on both hosts; on `/rooms/`, 19 menu entries on the same row. **Limitations:** no destination was picked and nothing was forwarded. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261109/r1/`.

**Previous record:** 2026-11-09 (nightly maintenance). **Product commit:** `82390825` (GitLab origin/main; rooms-client 0.114.0; 49 commits past `08fe407b`). **Scope:** `/rooms/` and `/chat/`, with the people stub: `#msg-ops-104` toolbar **More** lists 19 entries on both hosts (Forward, Edit Message, Copy Text, Copy Message Link, Bookmark Message, Save to Your Library, Pin Message, Mark Unread, Agent, Delete Message, Copy Message ID, …). **Limitations:** keyboard flyout not re-driven tonight (unchanged since 2026-11-08). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261109/r1/`.

**Previous record:** 2026-11-08 (nightly maintenance). **Product commit:** `08fe407b` (GitLab origin/main; rooms-client 0.112.0; unchanged since the 2026-11-07 pass). **Scope:** `/rooms/` (18183) and `/chat/` (18184): the keyboard **Agent** flyout re-driven with `focus()` instrumented (the call lands while the flyout is `visibility: hidden`); at 390×844 the long-press sheet with 22 items. **Limitations:** every verb is a fixture no-op. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261108/r1/`.

**Previous record:** 2026-11-07 (nightly maintenance). **Product commit:** `08fe407b` (GitLab origin/main; rooms-client 0.112.0; 89 commits past `ea399e62`). **Scope:** `/rooms/` (18180) and `/chat/` (18181): `msg-ops-104` **More** lists 19 entries; the hover toolbar's to-do button is titled **Add to Channel To-dos**; at 1440×700 `msg-ops-110` **More** (button top 546) opens the 16-entry menu at `top 151`, `bottom 542`, `--pop-origin: bottom right` on both hosts. Keyboard: Enter or ArrowRight on **Agent** opens the flyout (`aria-expanded="true"`, 4 entries) but focus stays on **Agent**, on both hosts. **Limitations:** **Make ticket** needs a records-mode server; the flyout's ArrowLeft/Escape close could not be reached by keyboard. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261107/r1/`.

**Previous record:** 2026-11-06 (nightly maintenance). **Product commit:** `ea399e62` (GitLab origin/main; rooms-client 0.111.0; 74 commits past `873a57ce`). **Scope:** `/rooms/` (18180) and `/chat/` (18181) `msg-ops-104` toolbar **More**: 19 entries on both (four quick tiles, React … Copy Message ID); no revisit or ticket item was added. **Limitations:** menu flips and the **Agent** flyout not re-driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261106/r1/`.

**Previous record:** 2026-11-05 (nightly maintenance). **Product commit:** `873a57ce` (GitLab origin/main; rooms-client 0.109.1; 17 commits past `ce14d4ba`). **Scope:** `/rooms/` (18170) and `/chat/` (18171) at 1440×700: `msg-ops-110` **More** near the bottom flips the 16-entry menu up to end 4 px above the button; a right-click at y 681 flips it to end 2 px above the cursor (`/rooms/`); a sidebar `contextmenu` dispatched below the fold (y 917) seated its 3-entry menu (**Create Category**, **Invite People**) at `bottom 692`, inside the 8 px margin. **Limitations:** the user, People-pane and **Agent** flyout flips were not driven; the late-row re-placement is proved only by `test/context-menu-position.test.ts`. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261105/r1/` (`18`–`22`).

**Previous record:** 2026-11-04 (nightly maintenance). **Product commit:** `ce14d4ba` (GitLab origin/main; rooms-client 0.109.1; 16 commits past `ba4389e7`). **Scope:** `/rooms/` (18160) and `/chat/` (18161): right-click on `msg-ops-104` (kyle) lists the 19 `menuitem`s; on `/rooms/` a row from dax lists 16 (no Edit Message, Pin Message or Delete Message). **Limitations:** the **Agent** submenu was not opened. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261104/r1/` (`msg-02-menu`, `msg-03-menu-104`).

**Previous record:** 2026-11-03 (nightly maintenance). **Product commit:** `ba4389e7` (GitLab origin/main; rooms-client 0.108.0; one CI-only commit past `3f8f24bc`). **Scope:** `/rooms/` (18143) and `/chat/` (18144): the `msg-ops-104` hover toolbar (nine title-named buttons); **More** opens 19 entries; the **Agent** submenu (**Copy for Agent**, **Mark for agent ⌥M**, **Ask about this...**, **Capture to doc from here**); `reply=1` reads **Replying to dax**; the `dm-msg-m2` bubble menu has 13 items on both hosts. **Limitations:** the `/rooms/` bubble menu missed twice before opening, so re-read after a short wait. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261103/r1/` (`ma-*`).

**Previous record:** 2026-11-02 (scheduled maintenance). **Product commit:** `3f8f24bc` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18141) and `/chat/` (18142): hover `#msg-ops-104` → toolbar **More** → 19 `menuitem`s on both (👍, 🔥, 😂, ❤️, React, Reply, Topic, To-do, Forward, Edit Message, Copy Text, Copy Message Link, Bookmark Message, Save to Your Library, Pin Message, Mark Unread, Agent, Delete Message, Copy Message ID); `reply=1` → **Replying to dax** with **Cancel reply** on both. **Limitations:** the DM menu, right-click, swipe and long-press were not re-driven; a first scripted attempt after a viewport change returned 0 items (new gotcha). Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261102/r1/`.

**Previous record:** 2026-11-02 (nightly maintenance). **Product commit:** `3f8f24bc` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18137) and `/chat/` (18138): the hover toolbar (React 👍 / 🔥 / 😂, Add reaction, Reply, Edit, Turn into topic, Add to Channel To-dos, More, all `title`-named); **Reply** focuses the composer with **Cancel reply**; **More** and a right-click each list 19 entries (👍 🔥 😂 ❤️, React, Reply, Topic, To-do, Forward, Edit Message, Copy Text, Copy Message Link, Bookmark Message, Save to Your Library, Pin Message, Mark Unread, Agent, Delete Message, Copy Message ID); **Agent** → Copy for Agent, Mark for agent ⌥M, Ask about this..., Capture to doc from here (`/rooms/`); the DM More menu (13, with **Edit Message**); at 390×844 on `/rooms/` the paced touch swipe (45 px hint, 60.9 px, settle to 0, **Replying to kyle**) and the 700 ms long press → `.msg-sheet[role=menu][data-mobile-sheet]` with 22 items. **Limitations:** the toolbar **More** listed 19, not the 11 recorded on 2026-10-31 and 2026-11-01, on both hosts and with a real click (see the Message menu bullet); pull to refresh was not re-attempted. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261102/r1/`.

**Previous record:** 2026-11-01 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18137) on `msg-ops-104`: a right-click lists 19 items (the four quick emoji, React, Reply, Topic, To-do, then the eleven verbs through **Copy Message ID**) and the hover toolbar's **More** lists the eleven verbs; the **Agent** submenu (Copy for Agent, Mark for agent, Ask about this..., Capture to doc from here); the toolbar (React 👍 / 🔥 / 😂, Add reaction, Reply, Edit, Turn into topic, Add to Channel To-dos, More); toolbar **Reply** → **Replying to kyle: …** with the composer focused and **Cancel reply**; `?reply=1` → **Replying to dax**; at 390 a long press opened the 22-item sheet and a swipe past 56 px set the same reply target (section above). `/chat/` (18138): the right-click and **More** menus, the **Agent** submenu and the toolbar **Reply**. **Limitations:** every verb is still a fixture no-op; **Turn into topic** and **Add to Channel To-dos** stay inert; pull to refresh did not fire. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261101/r1/` (`actions-01` to `actions-06`, `touch-01`, `touch-02`, `chat-10`, `chat-11`).

**Previous record:** 2026-10-31 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18135): hover `msg-ops-104` → toolbar **React 👍 / 🔥 / 😂**, **Add reaction**, **Reply**, **Edit**, **Turn into topic**, **Add to Channel To-dos**, **More**; **More** → 11 items; a right-click on the row → 19 items; **Agent** → **Copy for Agent**, **Mark for agent** ⌥M, **Ask about this...**, **Capture to doc from here**; `?reply=1` strip and **Reply** retarget; **Turn into topic** inert. `?view=dm&dm=ana`: `#dm-msg-m2` **More** → 13 items. `/chat/` (18136): the same toolbar, **More** → 11, **Agent** submenu (4), DM **More** → 13, `?reply=1` and the **Reply** retarget. **Limitations:** Every verb is a fixture no-op; the clipboard was not read back; **File as source**, **Summarize thread** and **Remove Link Previews** have no seed. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261031/r1/`.

**Previous record:** 2026-10-30 (scheduled maintenance). **Product commit:** `47cb13bf` (GitLab origin/main; rooms-client 0.108.0). **Scope (`/rooms/`, fixture lane):** On `#ops` `msg-ops-104`, the hover toolbar showed its nine title-named buttons, and **More** opened the 19-item menu listed above. Hovering **Agent** opened the submenu with **Copy for Agent**, **Mark for agent ⌥M**, **Ask about this...** and **Capture to doc from here**. On `#/dm/ana`, `dm-msg-m2`'s **More** opened the 13-item DM menu, and **Edit Message** opened the focused editor. **Limitations:** No verb was pressed for its effect (every one is a fixture no-op), the clipboard was not read, and `/chat/` was not driven. **File as source**, **Summarize thread** and **Remove Link Previews** have no seed. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261030/r1/` (frames 49-50, 52).
