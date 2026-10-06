# Settings and appearance

User, server, and channel settings — and the appearance controls that repaint
every other surface in the app. The most genuinely interactive fixture surface
in the repo: these controls really work, so this is the best place to prove an
interaction end to end.

## Sub-features

- User settings, nineteen entries: My Account, Profiles, Privacy, Sealed
  Messages, Appearance, Notifications, Audio, To-dos, Keyboard Shortcuts,
  Accessibility, Doc Editing, **Recovered Drafts**, Agent Settings — then a Help
  group (How Agents Work, How the Library Works, How Apps Work, Slash Commands,
  Moderating Servers) and Log Out. Recovered Drafts arrived with `#741` and its
  page id is `draft-recovery`, not `recovered-drafts`. It is **ungated** — no
  permission, no flag, no "only when you have orphans" check — so nineteen is
  the count in every state, and a nav that comes back eighteen is a real
  regression rather than a seeding difference.

  **Nineteen is fixture truth, not app truth.** The Agents group gains an
  **OM Settings** row (id `om`) only when the caller supplies `omPage`.
  `Shell.tsx:4492` always does, so the **running app shows twenty**;
  `settings-fixture.tsx` does not, so this lane shows nineteen — measured, not
  inferred. Count nineteen here and you have confirmed the fixture, not the
  product. To count twenty without a daemon, open Settings through the shell:
  `shell-fixture.html?view=settings&settingsPage=appearance` (measured at
  `f7d7c987`). (It was twenty-one until `#978` retired the matching **Persona**
  row, "now that Agents is its home" — persona is reached through Agents now,
  see [om-and-agents.md](om-and-agents.md).)
- Appearance: theme (dark / light / sync with OS), palette (Graphite, Slate,
  Moss, Warm, Brass), accent (Clay, Blue, Iris, Plum, White), and per-context
  message density. Density is three nested `radiogroup`s, not tabs: **Chat
  layout** (Bubbles / Streamlined / Custom), and under Custom, **Server channel
  layout** and **Direct message layout** (Bubbles / Streamlined each). A fourth
  radiogroup, **Message display** (Cozy / Compact), sits alongside them.
- High-contrast mode and its interaction with every palette. The system
  contrast preset follows `prefers-contrast: more` independently of the
  explicit high-contrast switch (`packages/chat-ui/src/lib/appearance.ts`).
- Server settings: Overview, Roles, Members, Moderation, Invites, Integrations,
  Work Ledger, Library, Recovery, Import Vault, Danger. There is **no Access
  page on the server host** — Access is a channel page.
- Channel settings: Overview, Access, Webhooks, Moderation, Danger — gated by
  the viewer's role. Overview carries the per-channel to-do widget placement
  control ("To-do widgets", gated by `canManageTodoDisplay`). The matching
  *per-viewer* override is not reachable from this fixture — see Gotchas.
- Settings search, the Esc-to-close rail behavior, and the open/close
  transition. Since `06ee56bd` the dialog also closes on **browser Back**:
  `SettingsShell.tsx:191` calls `useOverlayHistoryDismiss`
  (`packages/chat-ui/src/lib/overlay-history.ts`), so Esc is no longer the only dismissal path.

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
agent-browser open "$(control-om-chat url \
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
| `settings-fixture.html?host=user&page=todos` | To-dos — **account-wide defaults only**, not the per-channel override |
| `settings-fixture.html?host=user&page=draft-recovery` | Recovered Drafts — **empty state only**; nothing seeds a draft |
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
- **The per-channel viewer override cannot be reached from the settings
  fixture.** After the to-do consolidation (5416196a) it lives in
  `TodosSettingsPage`, which renders its "this channel" section only when
  `UserSettings` is given an `initialRoom` prop. `settings-fixture.tsx` never
  passes one and has no `room=` parameter, so `?host=user&page=todos` shows
  only the account-wide radiogroups ("Which to-dos appear in chat or topics",
  "Whether to-do status updates appear in chat"). Proving that sub-feature
  needs a fixture change, not a different query.
- **Two Appearance extras exist only in the shell.** `Shell.tsx:4490` passes
  `appearanceExtras` only when `session.mode === "home"`, and today that is the
  **"Open World chat"** group with a **"Chat pane font size"** range, 12–24px
  (`WorldChatPreferences.tsx`, `#world-chat-font-size`). `settings-fixture.tsx`
  passes no extras, so the group is absent there. It is present at
  `shell-fixture.html?view=settings&settingsPage=appearance` (measured at
  `f7d7c987`). The heading is uppercased by CSS, so match it by id or
  `textContent`, not `innerText`.
- **`&mode=away` does not show away Agent Settings.** On
  `?host=user&page=agent-access&mode=away` the page renders only the daemon
  notice, *"Agent grants live on your OM daemon, so this page cannot show them
  from here."* (`front-desk-shared.tsx:94`). The **"Phone reach"** dial in
  source (`AgentAccessPage.tsx:400`) did not render in either mode of this
  fixture (measured at `f7d7c987`). Its away branch reads
  `session.remoteControl()`, which this fixture does not stub; that is the
  likely unmet prerequisite (inferred, not driven).
- `?perms=` gates what server and channel settings render. A missing control
  may be a correct permission outcome rather than a regression — check the
  route you opened before reporting one.

### Verification record

**Last verified:** 2026-10-06. **Product commit:** `231c95f49820399fc10e40e87facee6ba606c6b0`. **Scope:** opened user Appearance, switched from Dark to Light and confirmed selection, then restored Dark. **Limitations:** Other settings pages, server/channel permissions, high contrast, and persisted preference across reload were not exercised.
