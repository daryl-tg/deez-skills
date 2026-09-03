# Tab navigation and parking

A five-tab dock sits under the tab roots: Chats, Servers, Discover, Library,
You. Pushing a detail screen does not replace the tab — the previous route stays
alive and frozen behind it, keeping its state and scroll position, and pressing
the already-selected tab returns to that tab's root. Settings routes are
full-screen and hide the dock.

## Sub-features

- `dock-switch` moves between the five tabs.
- `dock-root` returns to a tab's root by pressing the selected tab.
- `dock-badge` shows the Chats unread count.
- `nav-back` uses a screen's own back control where it has one.
- `nav-parking` keeps a pushed-past route alive rather than unmounting it.

## How to get to it (user POV)

- The dock is always visible. Tap any tab.
- Inside a detail screen, tap the back arrow, or tap the current tab again.

## Driving it with control-openfloor

Preconditions:

- `./control-openfloor doctor` exits zero.
- `./control-openfloor app open` landed on the Chats root.

Stable handles:

| Handle | What it is |
|---|---|
| `label="Primary navigation"` | the dock container — **the app-shell readiness gate** |
| `label="Chats, 654 unread"` | Chats tab; **the count is live, do not exact-match** |
| `label="Servers"`, `label="Discover"`, `label="Library"`, `label="You"` | the other four |
| `label="Back"` | back, **on screens that have it** (DM yes, server screen no) |

- **Confirm the shell.** `snapshot -i` must contain
  `[other] "Primary navigation"`. Its absence means you are on the dev-client
  launcher, not the app — or on a full-screen settings route, which hides the
  dock (see the gotcha below).
- **Switch tabs.** Run
  `./control-openfloor device press 'label="Servers"' --settle`. The settled
  diff shows the previous tab's content removed and `[selected]` moving to
  Servers.
- **Return to a tab root.** From a pushed screen, press the *already-selected*
  tab: `./control-openfloor device press 'label="Servers"' --settle`. The server
  detail is replaced by the server list. This is the one back path that works on
  every screen.
- **Verify parking.** Prove it with *retained state*, not scroll offset — the
  inbox is often too short to scroll. Type into the inbox search, leave, and
  come back:

  ```
  ./control-openfloor device fill 'label="Search chats"' "ger" --settle
  ./control-openfloor device press 'label="Servers"' --settle
  ./control-openfloor device find "Chats, "
  ./control-openfloor device snapshot -i
  ```

  The final snapshot must still show `[text-field] "ger"` and a list filtered to
  the matching row only. Reset to the top — an empty field and a full list —
  would mean the route was unmounted rather than parked. Verified 2026-09-02.
- **Use a screen's own back where it exists.** In a DM,
  `./control-openfloor device back --settle` works and the diff restores the
  inbox.
- **Proof.** The `--settle` diff for each navigation plus screenshots at the
  states that matter. Route identity is not readable from the outside here —
  there is no URL — so the accessible names of the header and dock are the
  identity evidence.

## Gotchas

- **`agent-device back` is not universal.** It works in a DM (`label="Back"` is
  present) and on the settings tree, and fails on the server screen with *"in-app
  back control is not available"* — that screen's back control has **no
  accessible label at all**, appearing as a bare `[button]` with an empty name.
  Prefer the selected-tab press, which works from any tab root.
- **Settings routes hide the dock,** so the selected-tab press is not available
  there. From App theme the way out is
  `press 'role=button label="Back to settings"'`, then `back`. Both need the
  `role=` qualifier — the bare label is ambiguous.
- **Never exact-match the Chats tab label.** It embeds the live unread count and
  drifts with no interaction. Use `find "Chats"` or press one of the other four
  by their fixed names.
- **`wait stable` is not an app-readiness gate.** The dev-client launcher is
  itself a stable screen, so `wait stable` happily returns while you are still
  on it. Gate on `wait 'label="Primary navigation"'`, and retry — a cold bundle
  load outlasts a single wait budget.
- **There is no URL to read.** Unlike the web client there is no hash route, so
  a navigation claim rests on accessible names and the settle diff. Capture both.
- Passive effects keep running on a parked route while layout effects do not, so
  a parked screen can still update its own badges. Assert the screen you are on.
- Every route is a flat sibling of `index` with one `_layout.tsx`
  (`docs/NAVIGATION.md`, pinned by `src/navigation/__tests__/app-dir-shape.test.ts`).
  If a navigation starts collapsing the stack, that test is the first place to
  look — not this recipe.
