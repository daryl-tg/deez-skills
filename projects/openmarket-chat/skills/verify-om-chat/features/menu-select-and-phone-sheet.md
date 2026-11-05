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
closed it (2026-11-06, `/rooms/`).

## Gotchas

- A synthetic `click` with the default `detail: 0` reads as a keyboard press,
  and a keyboard press always closes the sheet (`Popover.tsx`: `spent =
  clickSpent && event.detail > 0`). A drag proof built on `new
  MouseEvent("click")` without `detail: 1` closes the sheet and looks like a
  product bug.
- The real Projects pickers (labels, **Assignee**, **Agent**) are not
  reachable in any fixture. The gallery's `people` example uses its own stub
  session.
- The sheet's 72 px downward dismiss and the Enter path were not driven.

### Verification record

**Last verified:** 2026-11-06 (nightly maintenance). **Product commit:** `ea399e62` (GitLab origin/main; rooms-client 0.111.0). **Scope:** `/rooms/` (18180) `fixture.html`: **Labels** multi-pick (count 2 → 3, menu stays open, **Filter Labels**), the **Labels, up to two** cap, the **Labels with create** row; at 390×844 the full-width sheet with **Close Labels**, a 20 px drag kept and a 3 px tap closed. `/chat/` (18181): the gallery mounts the `multi` example. **Limitations:** the `/chat/` picks, the 72 px dismiss, Enter, auto-open and ranking were not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261106/r1/` (`14`–`16`).
