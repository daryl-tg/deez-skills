# Menu select and the phone sheet

The shared `MenuSelect` dropdown (`packages/chat-ui/src/components/MenuSelect.tsx`)
and the bottom sheet every popover becomes on a phone
(`packages/chat-ui/src/shared/ui/Popover.tsx`). Ticket labels and people
pickers in Projects are built on the multi-pick modes.

## Sub-features

- Multi-pick (`f62edd0d`, `45009f94`): a listbox with `aria-multiselectable`,
  a filter input **Filter <label>**, and a menu that stays open after each
  pick. The trigger reads **<label> · N** with the pick count.
- A pick cap: once full, every unchecked row is `aria-disabled`, and the note
  reads "Up to two labels."
- A create row: typing an unknown value offers "Create label '<text>' — Adds
  it to the list and picks it".
- Auto-open on mount, and host ranking of options (the `auto-open` and
  `rank-action` gallery examples).
- The phone sheet (`080c8636`, `e4bb46eb`, `ea399e62`): at 768 px and below,
  a popover opens as a full-width `dialog[aria-modal=true][data-ui-sheet]`
  whatever width its caller sets. Its handle is a button **Close <label>**. A
  tap closes the sheet. A press that moves 8 px or more in any direction is a
  drag and does not close it (`SHEET_TAP_SLOP_PX`). A downward drag of 72 px
  dismisses it. Keyboard Enter always closes it.
- A menu opened low opens above (`d1a25e38`): `MenuSelect` measures the full
  height of its rows (`wantedHeight`, `MenuSelect.tsx:35`, re-measured at
  `:395`) and flips above when they do not fit below and there is more room
  above, keeping its bottom edge on the trigger. Rows grouped under a heading
  in multi-pick are named "<row> <group>". Driven 2026-11-08 on both hosts:
  the switch to above happens, but the menu is not seated above (see
  [Gotchas](#gotchas)). The message **More** menu's flip is in
  [message-actions.md](message-actions.md).
- The message menu's phone sheet ignores the click a long-press lift lands on
  its backdrop; only a press that began on the backdrop, or a click no pointer
  made, closes it (`ContextMenu.tsx:364-377`). Driven 2026-11-08 on both
  hosts.

## How to get to it (user POV)

Open any dropdown that takes several values, such as a ticket's labels. Pick
several: the menu stays open and the button counts them. On a phone the same
menu rises from the bottom. Tap the grab handle to close it.

## Driving it with control-om-chat

The component gallery's **Dropdown** section mounts every mode, one
`[data-kitchen-example]` each: `filterable`, `render-trigger`,
`option-render`, `footer`, `multi` (**Labels**), `multi-max` (**Labels, up
to two**), `rank-action` (**Labels with create**), `auto-open` and `people`
(**Assignee**). It works on both hosts and mounts about 4 s after load.

```bash
agent-browser open "$(control-om-chat url 'tools/visual/fixture.html')"
agent-browser eval '(()=>{document.querySelector("[data-kitchen-example=multi] [role=combobox]").scrollIntoView({block:"center"});return 1})()'
agent-browser find role combobox click --name "Labels" --exact     # trigger reads "Labels · 2"
#   listbox aria-multiselectable="true"; options bug*, mobile*, web, docs, …; input "Filter Labels"
agent-browser find role option click --name "docs"                 # "Labels · 3", menu still open
agent-browser press Escape
agent-browser find role combobox click --name "Labels, up to two"  # bug, mobile picked; the other six aria-disabled
agent-browser press Escape
agent-browser find role combobox click --name "Labels with create"
agent-browser keyboard type "zzq"                                   # "Create label 'zzq' Adds it to the list and picks it"
```

For the sheet, use a fresh session at a phone width:

```bash
export AGENT_BROWSER_SESSION=verify-sheet
agent-browser set viewport 390 844
agent-browser open "$(control-om-chat url 'tools/visual/fixture.html')"
agent-browser find role combobox click --name "Labels" --exact
#   [data-ui-sheet] role=dialog aria-modal=true, width 390, x 0; handle button "Close Labels"
```

To tell a tap from a drag, dispatch `pointerdown`, `pointermove`, `pointerup`
on the handle button (`pointerType:"touch"`) and end with a `click` whose
`detail` is **1**. A 20 px sideways move left the sheet open. A 3 px move
closed it (2026-11-06, `/rooms/`). A downward drag in 20 px steps to 90 px
dismissed the sheet on release; one to 50 px, followed by a `detail: 1` click,
kept it open. Focusing **Close Labels** and pressing Enter closes it
(2026-11-08, both hosts).

For the low flip, scroll the multi-pick trigger to the bottom of a 1440×900
viewport before opening it (`block:"center"` never flips):

```bash
agent-browser eval '(()=>{document.querySelector("[data-kitchen-example=multi] [role=combobox]").scrollIntoView({block:"end"});return 1})()'
agent-browser find role combobox click --name "Labels" --exact
agent-browser eval '(()=>{const s=document.querySelector(".menu-select-menu");const r=s.getBoundingClientRect();
  return JSON.stringify({top:Math.round(r.top),bottom:Math.round(r.bottom),origin:s.style.getPropertyValue("--pop-origin")})})()'
#   trigger 868-900; menu top 850, bottom 1151, origin "bottom left"
agent-browser eval '(()=>{dispatchEvent(new Event("resize"));return 1})()'
#   menu top 563, bottom 864: seated above
```

For the long-press backdrop, use a fresh session at 390×844 on
`shell-fixture.html?view=room&alerts=quiet`. Long-press `msg-ops-104` with
paced touch `PointerEvent`s (the recipe in
[message-actions.md](message-actions.md) under Touch) to get
`.msg-sheet[role=menu][data-mobile-sheet]` with 22 items. Then:

```bash
agent-browser eval '(()=>{document.querySelector(".msg-sheet-backdrop").dispatchEvent(new MouseEvent("click",{bubbles:true,detail:1}));return 1})()'
#   the sheet stays open: a lift's click never began on the backdrop
agent-browser mouse move 195 40; agent-browser mouse down; agent-browser mouse up
#   the sheet and the backdrop unmount
```

## Gotchas

- A synthetic `click` with the default `detail: 0` reads as a keyboard press,
  and a keyboard press always closes the sheet (`Popover.tsx`: `spent =
  clickSpent && event.detail > 0`). A drag proof built on `new
  MouseEvent("click")` without `detail: 1` closes the sheet and looks like a
  product bug.
- The real Projects pickers (labels, **Assignee**, **Agent**) are not
  reachable in any fixture. The gallery's `people` example uses its own stub
  session.
- **A low multi-pick menu does not seat above (product gap, 2026-11-08, both
  hosts).** With the gallery's **Labels** trigger at the viewport bottom,
  `placeAboveIfNeeded` (`MenuSelect.tsx:689-706`) switches the menu to
  `placement: "above"` (`--pop-origin: bottom left`), but the surface stays at
  `top 850`, 18 px above the trigger's top and over it, and runs 251 px past
  the bottom of the viewport. Waiting
  2 s changes nothing; a window `resize` re-seats it at `563`–`864`, and
  reopening repeats the fault. Read the surface's box, not its origin: the
  origin alone reads like a correct flip.

### Verification record

**Last verified:** 2026-11-09 (nightly maintenance). **Product commit:** `82390825` (GitLab origin/main; rooms-client 0.114.0; 49 commits past `08fe407b`). **Scope:** `/rooms/` and `/chat/` gallery `fixture.html`: **Assignee** lists Unassigned, mira, **Dana** and scout from a real `PeopleDirectory` (the picker example's seed since `KitchenSink.tsx:402-428`). **Limitations:** the low-flip recipe and phone sheet not re-driven tonight; `MenuSelect` server-search `status` is reachable only through Projects. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261109/r1/`.

**Previous record:** 2026-11-08 (nightly maintenance). **Product commit:** `08fe407b` (GitLab origin/main; rooms-client 0.112.0; unchanged since the 2026-11-07 pass). **Scope:** `/rooms/` (18183) and `/chat/` (18184) `fixture.html`: a low **Labels** multi-pick switches to above but stays seated at `top 850` until a resize (product gap); at 390×844 a 90 px handle drag dismisses the sheet, 50 px keeps it, and Enter on **Close Labels** closes it; on `shell-fixture.html` the long-press sheet ignores a lift-style backdrop click and closes on a real press. **Limitations:** auto-open, ranking and real touch hardware. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261108/r1/`.

**Previous record:** 2026-11-07 (nightly maintenance). **Product commit:** `08fe407b` (GitLab origin/main; rooms-client 0.112.0; 89 commits past `ea399e62`). **Scope:** `/rooms/` (18180) `fixture.html` at 390×844: **Labels** opens the full-width sheet (`[data-ui-sheet]`, 390 px, x 0, `aria-modal="true"`, **Close Labels**). `/rooms/` (18180) and `/chat/` (18181) message **More** menus: the 16-entry menu flips above at 1440×700 (`top 151`, `bottom 542`), and on `/rooms/` (18180) and `/chat/` (18181) Enter on **Agent** opens the 4-entry flyout with `aria-expanded="true"` while focus stays on the row. **Limitations:** the multi-pick, cap and create rows, the 72 px dismiss, a low `MenuSelect` flip and the long-press lift were not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261107/r1/`.

**Previous record:** 2026-11-06 (nightly maintenance). **Product commit:** `ea399e62` (GitLab origin/main; rooms-client 0.111.0). **Scope:** `/rooms/` (18180) `fixture.html`: **Labels** multi-pick (count 2 → 3, menu stays open, **Filter Labels**), the **Labels, up to two** cap, the **Labels with create** row; at 390×844 the full-width sheet with **Close Labels**, a 20 px drag kept and a 3 px tap closed. `/chat/` (18181): the gallery mounts the `multi` example. **Limitations:** the `/chat/` picks, the 72 px dismiss, Enter, auto-open and ranking were not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261106/r1/` (`14`–`16`).
