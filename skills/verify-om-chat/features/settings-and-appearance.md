# Settings and appearance

User, server, and channel settings — and the appearance controls that repaint
every other surface in the app. The most genuinely interactive fixture surface
in the repo: these controls really work, so this is the best place to prove an
interaction end to end.

## Sub-features

- User settings: Account, Profiles, Privacy, Sealed Messages, Appearance,
  Notifications, Audio, Keyboard Shortcuts, Accessibility, Doc Editing, Agent
  Settings.
- Appearance: theme (dark / light / sync with OS), palette (Graphite, Slate,
  Moss, Warm, Brass), accent (Clay, Blue, Iris, Plum, White), and per-context
  message density (Bubbles / Streamlined / Custom, split Server vs Direct
  message).
- High-contrast mode and its interaction with every palette.
- Server settings: roles, moderation, access, invites.
- Channel settings: access and permissions, gated by the viewer's role.
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
agent-browser open "http://127.0.0.1:18099/rooms/tools/visual/settings-fixture.html?host=user&page=appearance"
```

| Route | State |
|---|---|
| `settings-fixture.html?host=user&page=account` | My Account |
| `settings-fixture.html?host=user&page=appearance` | Appearance |
| `settings-fixture.html?host=user&page=appearance&theme=light` | Appearance, opened in light |
| `settings-fixture.html?host=user&page=appearance&contrast=high` | High contrast |
| `settings-fixture.html?host=user&page=notifications` | Notifications |
| `settings-fixture.html?host=user&page=accessibility` | Accessibility |
| `settings-fixture.html?host=server&page=roles&perms=owner` | Server roles, as owner |
| `settings-fixture.html?host=server&page=moderation&perms=owner` | Server moderation |
| `settings-fixture.html?host=channel&page=access&perms=owner` | Channel access |

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
agent-browser find role tab      click --name "Direct message"
```

## Gotchas

- **The accessible name carries the selected state**: the checked radio is
  `"Light theme (selected)"`, not `"Light theme"`. An `--exact` match on the
  bare label stops resolving the moment the control becomes selected — which is
  exactly when a naive assertion runs. Match the `[checked]` attribute from the
  snapshot instead, or allow the suffix.
- **Bubbles / Streamlined / Custom appear twice**, once for Server and once for
  Direct message, with identical names. Scope to the `tab` you selected or you
  will drive the wrong one.
- Theme is written to `document.documentElement.dataset.theme`, so it survives
  outside the dialog — that is what makes it a usable side-effect check. Palette
  and accent land as separate attributes; read them the same way rather than
  judging colour from a screenshot.
- Changing the theme mid-run changes every later screenshot. Capture the frames
  that need dark **before** you flip, or reopen with `?theme=` and start clean.
- `?perms=` gates what server and channel settings render. A missing control
  may be a correct permission outcome rather than a regression — check the
  route you opened before reporting one.
