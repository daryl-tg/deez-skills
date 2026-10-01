# Tab navigation and parking

A five-tab dock sits under the tab roots, in this order: Chats, Servers,
Discover, Library, You. Pushing a detail screen does not replace the tab — the
previous route stays alive and frozen behind it, keeping its state and scroll
position, and pressing the already-selected tab returns to that tab's root.
Most pushed routes are full-screen and hide the dock.

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
| `label="Chats"` | the Chats tab **while nothing is unread, and right after a cold start** |
| `label="Chats, 654 unread"` | Chats tab with traffic; **the count is live, do not exact-match** |
| `label="Chats, 3 unread mentions"` | Chats tab when mentions exist — **a mention outranks any amount of traffic and replaces the unread count entirely** |
| `label="Servers"`, `label="Discover"`, `label="Library"`, `label="You"` | the other four |
| `label="Back"` | back, **on screens that have it** (DM yes, server screen no); qualify with `role=button` where a header wraps it |

- **Confirm the shell.** `snapshot -i` must contain
  `[other] "Primary navigation"`. Its absence means you are on the dev-client
  launcher, not the app — or on a full-screen settings route, which hides the
  dock (see the gotcha below).
- **Switch tabs.** Run
  `./control-openfloor device press 'label="Servers"' --settle`. The settled
  diff shows the previous tab's content removed and `[selected]` moving to
  Servers.
- **Return to a tab root.** From a pushed screen *that still shows the dock*,
  press the already-selected tab:
  `./control-openfloor device press 'label="Servers"' --settle`. The server
  detail is replaced by the server list.

  This is **not** a universal escape — it only works where the dock is present,
  and the rule is a two-entry list in source:
  `TAB_BAR_ROUTES = ['index', 'server/[spaceId]/index']`
  (`src/rooms/bottom-tabs-dock-geometry.tsx`). The dock shows on the home floor
  and on a server's channel list, and **nowhere else** — not on a channel, a DM,
  either details route, settings, activity, apps, library, docs, follows, help,
  alerts, invite or `new/*`. Matches what driving showed on 2026-09-03. On every
  other route, use the screen's own back control.

  That constant is also why the selected-tab press works on the server screen
  despite its unlabelled back control — the server screen keeps the dock. And a
  rename there breaks the dock silently (`docs/NAVIGATION.md` §7), which is
  exactly what the "Confirm the shell" step would catch.
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
  would mean the route was unmounted rather than parked. Re-verified
  2026-09-03: after `fill … "ger"` → Servers → Chats, the field still held
  `ger`, the list still showed only `geraldlee, Sep 1, …` plus the
  search-history hint.
- **Use a screen's own back where it exists.** In a DM,
  `./control-openfloor device back --settle` works and the diff restores the
  inbox. Elsewhere the control is labelled but ambiguous — `role=button` is
  required for `Back` (Alerts), `Back to chats` (Activity),
  `Back to settings` (App theme) and `Back to server` (server Library).
- **Proof.** The `--settle` diff for each navigation plus screenshots at the
  states that matter. Route identity is not readable from the outside here —
  there is no URL — so the accessible names of the header and dock are the
  identity evidence.

## Gotchas

- **`agent-device back` is not universal.** It works in a DM (`label="Back"` is
  present) and on the settings tree, and fails on the server screen with *"in-app
  back control is not available"* — that screen's back control has **no
  accessible label at all**, appearing as a bare `[button]` with an empty name.
  On the server screen the selected-tab press is the way out, because that is
  one of the few pushed routes that keeps the dock.
- **`back` on a list can select a row instead of going back.** In the jump
  palette, `./control-openfloor device back --settle` opened the first result's
  channel rather than dismissing the palette. Where a screen has no labelled
  back control, check what `back` actually did before treating it as a
  navigation.
- **Settings routes hide the dock,** so the selected-tab press is not available
  there. From App theme the way out is
  `press 'role=button label="Back to settings"'`, then `back`. Both need the
  `role=` qualifier — the bare label is ambiguous.
- **Never exact-match the Chats tab label**, and never assume which of its three
  forms is showing (`Chats`, `Chats, <n> unread`, `Chats, <n> unread mentions`).
  It drifts with no interaction — one session watched `1712` become `959`,
  `445`, then `510`. Press one of the other four by their fixed names, or take
  the tab's ref from a `--settle` diff.
- **`find "Chats"` is not a safe substitute for the tab.** `find` matches by
  *contains*, and the Discover tab's own copy includes the word Chats
  (*"do not become permanent Chats entries"*), so from Discover it can match the
  paragraph and tap the wrong thing.
- **Refs go stale between `control-openfloor device` invocations.** Each
  invocation is a separate `agent-device` call, so a `@ref` you read from one
  shell command may already be pinned to a dead snapshot by the next — pressing
  it can land on whatever now occupies those coordinates, which in this session
  meant the dock. Take refs from a `--settle` diff and use the `~sN`-pinned form
  (`@e20~s142731`), or drive by selector.
- **`wait stable` is not an app-readiness gate.** The dev-client launcher is
  itself a stable screen, so `wait stable` happily returns while you are still
  on it. Gate on `wait 'label="Primary navigation"'`, and retry — a cold bundle
  load outlasts a single wait budget.
- **There is no URL to read.** Unlike the web client there is no hash route, so
  a navigation claim rests on accessible names and the settle diff. Capture both.
- Passive effects keep running on a parked route while layout effects do not, so
  a parked screen can still update its own badges. Assert the screen you are on.
- **A left-up keyboard outlives a navigation and blocks the rows beneath it.**
  After typing in the inbox search, the keyboard stayed over the list; `app
  open` only foregrounds and does not dismiss it, and `device keyboard dismiss`
  reported no dismiss key on this screen. `./control-openfloor app reset` is the
  reliable clear.
- Every route is a flat sibling of `index` with one `_layout.tsx`
  (`docs/NAVIGATION.md`, pinned by `src/navigation/__tests__/app-dir-shape.test.ts`).
  If a navigation starts collapsing the stack, that test is the first place to
  look — not this recipe.
- Five tabs, their order, `Primary navigation`, `dock-root` and `nav-parking`
  all re-verified live 2026-09-03 on `f2c3f88`.
