# Settings and appearance

User, server, and channel settings — and the appearance controls that repaint
every other surface in the app. The most genuinely interactive fixture surface
in the repo: these controls really work, so this is the best place to prove an
interaction end to end.

## Sub-features

- User settings: My Account, Profiles, Privacy, Sealed Messages, Appearance,
  Notifications, Audio, To-dos, Keyboard Shortcuts, Accessibility, Doc Editing,
  Agent Settings — then a Help group (How Agents Work, How the Library Works,
  How Apps Work, Slash Commands, Moderating Servers) and Log Out.
- Appearance: theme (dark / light / sync with OS), palette (Graphite, Slate,
  Moss, Warm, Brass), accent (Clay, Blue, Iris, Plum, White), and per-context
  message density. Density is three nested `radiogroup`s, not tabs: **Chat
  layout** (Bubbles / Streamlined / Custom), and under Custom, **Server channel
  layout** and **Direct message layout** (Bubbles / Streamlined each). A fourth
  radiogroup, **Message display** (Cozy / Compact), sits alongside them.
- High-contrast mode and its interaction with every palette.
- Server settings: roles, moderation, access, invites.
- Channel settings: Overview, Access, Webhooks, Moderation, Danger — gated by
  the viewer's role. Overview carries the per-channel to-do widget placement
  control; the matching per-viewer override lives at `?host=user&page=todos`.
- Settings search, the Esc-to-close rail behavior, and the open/close
  transition.

## How to get to it (user POV)

You click the gear beside your name, a settings dialog opens over the app with
a list of sections down the left. You pick **Appearance**, choose Light theme,
and the whole app repaints behind the dialog — no save button, no reload.

## Driving it with control-om-chat

Settings has **its own fixture**, with a `?host=` / `?page=` / `?perms=`
vocabulary. `?view=` does nothing here.

```bash
export AGENT_BROWSER_SESSION=verify-settings
agent-browser set viewport 1440 900
agent-browser open "$(./control-om-chat url \
  'tools/visual/settings-fixture.html?host=user&page=appearance')"
```

| Route | State |
|---|---|
| `settings-fixture.html?host=user&page=account` | My Account |
| `settings-fixture.html?host=user&page=appearance` | Appearance |
| `settings-fixture.html?host=user&page=appearance&theme=light` | Appearance, opened in light |
| `settings-fixture.html?host=user&page=appearance&contrast=high` | High contrast |
| `settings-fixture.html?host=user&page=notifications` | Notifications |
| `settings-fixture.html?host=user&page=accessibility` | Accessibility |
| `settings-fixture.html?host=user&page=todos` | Per-viewer to-do visibility |
| `settings-fixture.html?host=server&page=roles&perms=owner` | Server roles, as owner |
| `settings-fixture.html?host=server&page=moderation&perms=owner` | Server moderation |
| `settings-fixture.html?host=channel&page=access&perms=owner` | Channel access |
| `settings-fixture.html?host=channel&page=overview&perms=owner` | Channel overview, incl. to-do widget placement |

The dialog is `dialog` named **"Settings"**; the section list is `navigation`
named **"Settings navigation"**. Scope to them when a label is ambiguous.

A complete worked proof — action, resulting state, and a side effect outside
the control:

```bash
agent-browser eval 'document.documentElement.dataset.theme'          # "dark"
agent-browser screenshot artifacts/<run>/<rev>/01-appearance-dark.png

agent-browser find role radio click --name "Light theme"

agent-browser eval 'document.documentElement.dataset.theme'          # "light"
agent-browser snapshot -i -c | grep -i theme
#   radio "Dark theme"  [checked=false]
#   radio "Light theme (selected)" [checked=true]
agent-browser screenshot artifacts/<run>/<rev>/02-appearance-light.png
```

Other handles that resolve today:

```bash
agent-browser find role button   click --name "Notifications"
agent-browser find role searchbox fill  "keyboard" --name "Search settings"
agent-browser find role radio    click --name "Moss palette"
agent-browser find role radio    click --name "Iris accent"
agent-browser find role tab      click --name "Direct message"   # preview toggle, NOT density
```

## Gotchas

- **The accessible name carries the selected state**: the checked radio is
  `"Light theme (selected)"`, not `"Light theme"`. An `--exact` match on the
  bare label stops resolving the moment the control becomes selected — which is
  exactly when a naive assertion runs. Match the `[checked]` attribute from the
  snapshot instead, or allow the suffix. The suffix is not theme-only: it is
  the same shared swatch, so `"Graphite palette (selected)"` and
  `"Clay accent (selected)"` behave identically.
- **Bubbles / Streamlined appear three times** — once in Chat layout, once in
  Server channel layout, once in Direct message layout, with identical names.
  Scope to the enclosing `radiogroup` by its aria-label. Do **not** scope by
  tab: the only `tablist` on this page is "Preview conversation"
  (Server / Direct message), which just swaps the preview mock and changes no
  density setting. `find role tab --name "Direct message"` resolves, and drives
  the wrong control.
- **The three appearance axes land in three different places.** Theme is
  `document.documentElement.dataset.theme`. Palette is
  `document.documentElement.dataset.palette`, but only once you move off the
  Graphite default — it is absent, not `"graphite"`, at first paint. Accent is
  not an attribute at all: it is inline CSS custom properties, so read
  `getComputedStyle(document.documentElement).getPropertyValue("--m-accent")`.
  `dataset.accent` is always undefined and an assertion on it always fails.
- Changing the theme mid-run changes every later screenshot. Capture the frames
  that need dark **before** you flip, or reopen with `?theme=` and start clean.
- `?perms=` gates what server and channel settings render. A missing control
  may be a correct permission outcome rather than a regression — check the
  route you opened before reporting one.
