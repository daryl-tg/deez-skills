# Appearance and settings

The You tab carries the account's profile, connection state and status, then the
app settings tree. App theme is three independent dials — palette, accent, and
light/dark — over a live preview that renders a miniature chat. Choices persist
across a cold start.

## Sub-features

- `you-overview` shows profile, connection state and status.
- `you-notifications` toggles notifications and opens chat notification rules.
- `settings-tree` lists Profile, App theme, Chat notifications, Advanced.
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

Stable handles:

| Handle | What it is |
|---|---|
| `label="You"` | the dock tab |
| `label="Open your profile"` | profile row |
| `label="Set status"` | status row |
| `role=button label="Appearance"` | into the settings tree — **role is required** |
| `label="Notifications"` | a `[switch]` |
| `label="Chat notification rules"`, `label="Friends"`, `label="Apps"`, `label="Settings"` | You rows |
| `label="Search settings"`, `label="Profile"`, `label="App theme"`, `label="Chat notifications"`, `label="Advanced"` | settings tree |
| `label="Back to settings"` | back from App theme |
| `label="Preview: Graphite · Ember"` | the live preview — **the assertion target**, `"Preview: <Palette> · <Accent>"` |
| `label="Graphite"`, `label="Slate"`, `label="Brass"` | palette swatches (**not** `Warm graphite`) |
| `label="Blurple"`, `label="Honey"` | accent swatches (**not** `Ember`) |
| `label="System"`, `label="Dark"`, `label="Cream"` | LIGHT OR DARK rows; the active one carries `[selected]` |
| `[text] "Graphite · Ember"` | the summary line under the dials — the one place the active accent is readable when it is the un-addressable first swatch |

- **Reach App theme.** Run
  `./control-openfloor device press 'label="You"' --settle`, then
  `./control-openfloor device press 'role=button label="Appearance"' --settle`,
  then `./control-openfloor device press 'label="App theme"' --settle`. The
  settled diff carries `Preview: <Palette> · <Accent>` — record it as the
  restore target.
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
  row it is not reachable by label; see the gotcha and use coordinates, then
  record that in the delta.
- **Proof.** Three frames — before, after, after-cold-start — plus the two
  `--settle` diffs. Then
  `./control-openfloor evidence publish <run-id> <revision>`.

## Gotchas

- **The first swatch in each row is not addressable by label.** iOS merges it
  into the parent `[cell]`, whose frame spans the whole row. `press
  'label="Ember"'` taps the row's centre — dead space between Blurple and
  Honey — and returns success while changing nothing. The same applies to
  `Warm graphite` in PALETTE. Only `Blurple`/`Honey` and
  `Graphite`/`Slate`/`Brass` are reachable by name. Reaching `Ember` or `Warm
  graphite` needs raw coordinates (Ember sat at `(69, 633)` on a 402×874 iPhone
  17 Pro frame); geometry is frame-dependent, so re-read it from a screenshot
  rather than reusing that pair.
- **`label="Appearance"` is ambiguous** — `[other]` and `[button]` both match and
  `press` fails with `AMBIGUOUS_MATCH`. Always `role=button label="Appearance"`.
- **The merged first swatch never reports `[selected]`.** Because it is folded
  into the parent `[cell]`, `Ember` shows no selected state even when active,
  while `Graphite` and `Dark` show theirs. Read the summary line
  (`[text] "Graphite · Ember"`) or the preview's accessible name instead of
  inferring the accent from `[selected]` flags.
- **The Appearance row opens the whole settings tree**, not an appearance-only
  screen. App theme is one row inside it, and both it and `Back to settings`
  need the `role=button` qualifier.
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
  do not flip it to make a screenshot.
