# Appearance and settings

The You tab carries the account's profile, connection state and status, then the
app settings tree. App theme is three independent dials — palette, accent, and
light/dark — over a live preview that renders a miniature chat. Choices persist
across a cold start.

## Sub-features

- `you-overview` shows profile, connection state and status.
- `you-notifications` toggles notifications and opens chat notification rules.
- `settings-tree` lists three groups: **ACCOUNT** (Profile), **APP SETTINGS**
  (Appearance, App theme, Chat notifications, Advanced) and **SUPPORT**
  (Your docs, Follows, Help), over a `Search settings` field that really filters.
- `settings-appearance` is its own screen between the tree and App theme:
  THEME (Match device theme, Theme), MESSAGE DISPLAY (Cozy / Compact),
  TEXT SIZE (Chat text size smaller/bigger, with a percentage),
  LINK PREVIEWS, MOTION (Follow device / Always reduce).
- `theme-palette` picks Warm graphite / Graphite / Slate / Brass.
- `theme-accent` picks Ember / Blurple / Honey.
- `theme-mode` picks System / light / dark.
- `theme-persist` survives a cold start.

## How to get to it (user POV)

- Tap **You** in the bottom dock.
- Tap **Appearance** to reach the settings tree, then **App theme**.

## Driving it with control-openfloor

Preconditions:

- `./control-openfloor doctor` exits zero, start from the Chats root.
- Theme changes are reversible but **not local**. The screen's own footnote
  reads *"Applies to this device, and travels to your OpenMarket web session."*
  — so a theme change is visible in the operator's web client too. Note the
  starting palette and accent before touching them, restore them afterwards, and
  say in the delta that you changed them.
- **Only three dials travel.** `appearance-sync` pushes *scheme, palette and
  accent* to the user-prefs blob the web client reads, and nothing else. The
  Appearance section's dials — message density, chat text size, link previews,
  reduce-motion — stay on this device. That makes them the cheaper things to
  exercise when a claim only needs "a preference persisted".

Stable handles:

| Handle | What it is |
|---|---|
| `label="You"` | the dock tab |
| `label="Open your profile"` | profile row |
| `label="Set status"` | status row |
| `role=button label="Appearance"` | into the settings tree — **role is required** |
| `label="Notifications"` | a `[switch]` |
| `label="Chat notification rules"`, `label="Friends"`, `label="Apps"`, `label="Settings"` | You rows |
| `label="Search settings"`, `label="Clear settings search"` | the tree's filter |
| `label="Profile"`, `label="Appearance"`, `label="App theme"`, `label="Chat notifications"`, `label="Advanced"`, `label="Your docs"`, `label="Follows"`, `label="Help"` | the eight settings rows, in three groups |
| `label="Retry the OpenMarket connection"` | the You tab's reconnect control |
| `label="Log out"` | **destructive**; sign-out calls `clearAll()` on the cache |
| `label="Match device theme"`, `label="Theme"` | the Appearance section's THEME group |
| `label="Cozy"`, `label="Compact"` | MESSAGE DISPLAY |
| `label="Chat text size smaller"`, `label="Chat text size bigger"`, `label="Reset to default"` | TEXT SIZE |
| `label="Show link previews"` | a `[switch]` |
| `label="Follow device"`, `label="Always reduce"` | MOTION |
| `role=button label="Back to settings"` | back from App theme — **role is required** |
| `label="Preview: Graphite · Ember"` | the live preview — **the assertion target**, `"Preview: <Palette> · <Accent>"` |
| `label="Graphite"`, `label="Slate"`, `label="Brass"` | palette swatches — safe by label |
| `label="Blurple"`, `label="Honey"` | accent swatches — safe by label |
| `label="Warm graphite"`, `label="Ember"` | the **first** swatch of each row — these names each match TWO nodes, and pressing by label hits the wrong swatch. See the gotcha. |
| `label="System"`, `label="Dark"`, `label="Cream"` | LIGHT OR DARK rows; the active one carries `[selected]` |
| `[text] "Graphite · Ember"` | the summary line under the dials — a second, screenshot-friendly reading of both dials |

- **Reach App theme.** Two hops named `Appearance`, then the theme screen:

  ```
  ./control-openfloor device press 'label="You"' --settle
  ./control-openfloor device press 'role=button label="Appearance"' --settle   # -> the settings tree
  ./control-openfloor device press 'role=button label="App theme"' --settle
  ```

  The tree's own `Appearance` row goes to the Appearance section instead, and
  that section's `Theme` button reaches the same App theme screen — so
  `press 'role=button label="Appearance"'` twice, then
  `press 'role=button label="Theme"'`, is the equivalent route and the one that
  also exercises `settings-appearance`. Either way the settled diff carries
  `Preview: <Palette> · <Accent>` — record it as the restore target.
- **Capture the before state.**
  `./control-openfloor device screenshot --out "$PWD/artifacts/<run>/<rev>/01-theme-before.png" --normalize-status-bar`
- **Change the accent.** Run
  `./control-openfloor device press 'label="Blurple"' --settle`. The settled
  diff must show the preview's name change, e.g.
  `Preview: Graphite · Ember` → `Preview: Graphite · Blurple`. That diff is the
  action-and-result pair; a screenshot alone is not.
- **Prove it persisted.** Run `./control-openfloor app reset` — a real
  `simctl terminate` and relaunch — then re-navigate You → Appearance → App
  theme and read the preview again. Still `Preview: Graphite · Blurple` means
  the value reached disk rather than living in a store.
- **Restore.** Press the original swatch. If the original was the *first* in its
  row, press its **child node** — by ref from a raw snapshot, or by its own
  72pt rect's centre — never by label. See the gotcha.
- **Proof.** Three frames — before, after, after-cold-start — plus the two
  `--settle` diffs. Then
  `./control-openfloor evidence publish <run-id> <revision>`.

## Gotchas

- **Pressing the first swatch by label selects the WRONG swatch — silently.**
  This is worse than the "it does nothing" this file used to claim, and it is
  the single most expensive trap on the screen. iOS gives the swatch *strip*
  the name of its first child, so `label="Ember"` matches **two** nodes: the
  strip (`x16 w370 h114`) and the real swatch (`x33 w72 h80`). `press` takes the
  strip, taps its centre at `x≈201` — which lands inside **Honey's** box — and
  reports success. Verified 2026-09-03: `press 'label="Ember"'` moved
  `Preview: Graphite · Blurple` to `Preview: Graphite · **Honey**`.

  The fix is to press the child, not the strip. Read it out of a raw snapshot
  and press its ref:

  ```
  ./control-openfloor device snapshot --raw     # find the node with value "radio button, …"
  ./control-openfloor device press '@e31'       # -> tapped (69, 479), Warm graphite selected
  ```

  Its rect centre works too (`press 69 645` restored Ember on a 402×874 iPhone
  17 Pro frame), but geometry is frame-dependent — re-read it rather than
  reusing a pair. `Graphite`/`Slate`/`Brass` and `Blurple`/`Honey` remain safe
  by label, because only the first child lends the strip its name.
- **`label="Appearance"` is ambiguous** — `[other]` and `[button]` both match and
  `press` fails with `AMBIGUOUS_MATCH`. Always `role=button label="Appearance"`.
- **Every swatch does report its state — read it with `get attrs`.** The child
  node carries `value: "radio button, checked"` and `selected: true`, first
  swatch included, so
  `./control-openfloor device get attrs 'label="Ember"'` tells you whether Ember
  is active. What you cannot trust is the `-i` snapshot's rendering, where the
  first swatch shows as a `[cell]` and its `[selected]` flag is easy to miss.
  The preview's accessible name (`Preview: <Palette> · <Accent>`) remains the
  cheapest single assertion for both dials at once.
- **`Appearance` names two different rows on two different screens.** On the You
  tab it opens the **whole settings tree**; inside that tree it opens the
  **Appearance section**. Both need `role=button`, and pressing it twice in a
  row is a legitimate route, not a mistake.
- **`Back to settings` is ambiguous too** — `[other]` and `[button]` both match.
  `role=button label="Back to settings"`. Expect this on every wrapped header
  back control: `Back to chats` on Activity and `Back` on the Alerts board have
  the same shape.
- **Settings routes hide the tab dock.** `label="Primary navigation"` is absent
  on App theme and on the settings tree, so the selected-tab press is not a way
  out. Use `press 'role=button label="Back to settings"'` then
  `./control-openfloor device back`.
- **Assert the preview's accessible name, not the swatch's selected state.** The
  preview is the single string that names both dials at once, and it is what
  changes when the choice lands.
- A plain `agent-device open` (no reset) only foregrounds a running app, so the
  app resumes on the same screen. That proves nothing about persistence — use
  `app reset`.
- The `[switch] "Notifications"` toggle changes real push registration. Read it;
  do not flip it to make a screenshot. The same applies to `Log out`, which
  wipes the account-scoped cache.
- **A cold start shows the Chats tab with no count** (`label="Chats"`, not
  `Chats, <n> unread`) until the inbox hydrates. If a recipe presses the dock
  right after `app reset`, that is the label to expect.
- Palette, accent, mode names and the preview handle re-verified live 2026-09-03 on `f2c3f88`; `theme-accent` and `theme-persist` were exercised and restored to `Graphite · Ember`.
