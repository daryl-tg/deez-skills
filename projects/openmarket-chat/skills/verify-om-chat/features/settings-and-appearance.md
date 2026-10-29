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
  `Shell.tsx:4551` always does, so the **running app shows twenty**;
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
  explicit high-contrast switch (`packages/chat-ui/src/components/settings/appearance.ts`, `prefers-contrast: more` at `:309`).
- Server settings: Overview, Roles, Members, Moderation, Invites, Integrations,
  Work Ledger, Library, Recovery, Import Vault, Danger. There is **no Access
  page on the server host** — Access is a channel page.
- Channel settings: Overview, Access, Webhooks, Moderation, Danger — gated by
  the viewer's role. Overview carries the per-channel to-do widget placement
  control ("To-do widgets", gated by `canManageTodoDisplay`). The matching
  *per-viewer* override is not reachable from this fixture — see Gotchas.
  Webhooks also offers **Convert webhooks to alerts**. Its review step lets the
  owner select legacy webhooks; URLs and senders stay while deliveries become
  alert cards in that channel's tape (`WebhooksPage.tsx:600`,
  `ConvertWebhooksStepper.tsx:342,419`).
- Keyboard Shortcuts carries an **Editing** group with one switch, **Vim mode**
  (`UserSettings.tsx:1278-1296`, `878049d8`/`b1ed7135`). It is off by default and
  stored as `localStorage["om.chat.vimMode"]` (`"true"`/`"false"`). It is synced and
  scoped per account (`lib/prefs.ts`) and turns on Vim keys in the message box
  ([composer-and-sending.md](composer-and-sending.md)) and the doc editor
  ([your-library.md](your-library.md)). It adds no nav entry. The page's search
  keywords gained `vim modal editing`, so searching `vim` narrows the nav to
  Keyboard Shortcuts.
- Settings search, the Esc-to-close rail behavior, and the open/close
  transition. Since `06ee56bd` the dialog also closes on **browser Back**:
  `SettingsShell.tsx:192` calls `useOverlayHistoryDismiss`
  (`packages/chat-ui/src/lib/overlay-history.ts`), so Esc is no longer the only dismissal path.
- The **Grammar & shortcuts** modal (`ShortcutsModal.tsx`; keymap `mod+/`, `lib/keymap.ts:145`), the **Log Out** confirmation, and the server **Invites** page's invite-link dialog (`InviteLinkDialog.tsx`).

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
| `settings-fixture.html?host=channel&page=webhooks&perms=owner` | Webhooks, including the conversion review step |

On the Webhooks route, choose **Convert webhooks to alerts** and check the
selection review and channel-tape explanation. Cancel to leave the fixture
unchanged. The source fixture proves the wizard's UI; an authenticated server
is still required to prove conversion effects.

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
agent-browser find role searchbox fill  "vim" --name "Search settings"       # -> only Keyboard Shortcuts
agent-browser find role switch   click --name "Vim mode"   # on settings-fixture ?host=user&page=shortcuts,
                                                         # or shell ?view=settings&settingsPage=shortcuts
agent-browser find role radio    click --name "Moss palette"
agent-browser find role radio    click --name "Iris accent"
agent-browser find role tab      click --name "Direct message"   # preview toggle, NOT density
```

### Shortcuts modal, Log Out confirm, invite link (added 2026-10-27)

- **Shortcuts modal:** on any shell route, press `Meta+/` (mod is Meta on macOS). It opens dialog **Grammar & shortcuts**, which **Close shortcuts** dismisses. Both `/rooms/` and `/chat/` were driven. `Control+/` did not open it on `/chat/`, so use Meta.
- **Log Out:** `shell-fixture.html?view=settings&alerts=quiet` → button **Log Out** (`--exact`) opens alertdialog **Log Out**, reading "Are you sure you want to log out?", over the **Settings** dialog. Driven on both hosts. Confirming is a no-op (`onLogout={() => {}}`, `shell-fixture.tsx:4513`), so real logout stays pending.
- **Invite link:** `shell-fixture.html?view=server-settings&settingsPage=invites&alerts=quiet` → **Create invite link** opens dialog **Invite link settings**, with expiry and max-uses controls. Creating a link is INERT. The inbound `InviteLanding` has no harness (it is mounted only by `src/App.tsx:738`).

Verified 2026-10-27 at `6c15b0fb` (maintenance pass, fixture lane). Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261027/r1/` (frames 22-23, 31, 40-41).

### Settings page bodies (added 2026-10-29)

Open `shell-fixture.html?view=settings&alerts=quiet` (user) or
`?view=server-settings&alerts=quiet` (server, space "Macro Lab"), then click the
page's nav button. `?settingsPage=<id>` lands on a page directly
(`shell-fixture.tsx:2440-2445`; the `/chat/` fixture reads the same param). Ids:
`privacy`, `secrets`, `notifications`, `audio`, `accessibility`, `docs`,
`draft-recovery`, `agent-guide`, `library-guide`, `apps-guide`,
`slash-commands`, `moderation-guide`; server `overview`, `roles`, `members`,
`moderation`, `invites`, `integrations`, `library`, `recovery`, `danger`.
Reload between pages that crash (see Gotchas).

The user nav lists 20 entries in the shell: My Account, Profiles, Privacy, Sealed
Messages, Appearance, Notifications, Audio, To-dos, Keyboard Shortcuts,
Accessibility, Doc Editing, Recovered Drafts, Agent Settings, OM Settings, How
Agents Work, How the Library Works, How Apps Work, Slash Commands, Moderating
Servers, Log Out. The server nav lists 10: Overview, Roles, Members,
Moderation, Invites, Integrations, Library, Recovery, Import Vault, Danger.

What each body opens with, identical on `/rooms/` and `/chat/`:

| Page | First text |
|---|---|
| Privacy | **Privacy** — "Control who can follow you, who can message you…" |
| Sealed Messages | **Sealed Messages** — "Sealed messages are managed by the OM app on the device that holds your keys" |
| Notifications | crashes in the shell fixture; renders in `settings-fixture.html?host=user&page=notifications` (**Notifications**, THIS DEVICE, IN THE CHANNEL **Ringing strip at the top**, NOTIFY ME FOR) |
| Audio | **Audio** — "Choose the microphone, speakers, and processing…" (DEVICES) |
| To-dos | **To-dos** — "Choose which to-do rows appear in chat and topics by default." |
| Accessibility | **Accessibility** — MOTION AND FEEDBACK, **Enable reduced motion** |
| Doc Editing | **Doc Editing** — AUTO-PUBLISH WHILE EDITING |
| Recovered Drafts | **Recovered Drafts** (an h2, no h1) — the empty state |
| Help guides | **How agents work**, **How the library works**, **How apps work**, **Slash commands**, **Moderating servers** |
| Server Overview | **Server Overview** — SERVER NAME, SERVER ICON |
| Roles | **Roles** — traders, Full Stack, @everyone |
| Members | **Members** — "5 members", kyle OWNER, ana ADMIN |
| Moderation | crashes (see Gotchas) |
| Invites | **Invites** — **Create invite link** |
| Integrations | **Integrations** — APPS |
| Library | **Library** — "This server's backend predates library governance…" |
| Recovery | **Library Recovery** |
| Import Vault | **Import Vault** |
| Danger | **Danger** — TRANSFER OWNERSHIP |

There is no server **Access** page. Access is a channel page
(`ChannelSettings.tsx:791`), reached only through
`settings-fixture.html?host=channel&perms=owner`. Toggles and saves on these
pages call unstubbed session methods, so only the bodies are proved, not their
effects.

Verified 2026-10-29 at `cdfb1b0f` (scheduled maintenance, both hosts). Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261029/r1/` (`settings-*`, `server-settings-*`, `settings-fixture-notifications-*`).

## Gotchas

- **Notifications crashes the shell fixture's whole User settings surface.**
  `ChannelStripRow` calls `alerts.stripEnabled()` (`NotificationSettings.tsx:604`),
  and neither fixture's plain-object `alertsStub` has it
  (`shell-fixture.tsx:1435`, `apps/cloud/tools/visual/shell-fixture.tsx:537`).
  `LazySurfaceGate` then swaps the entire dialog, nav included, for **User
  settings could not load** / **Try again**. Any further page click finds no
  button, and **Try again** returns to My Account. Reload before driving the
  next page. Server **Moderation** fails the same way, as **Server settings
  could not load**, because `session.spaceModerationState(...).then` hits
  `INERT`. Both crash on both hosts.
- **`settings-fixture.html` talks to production for some pages.** Its
  `socialConfig` points at `https://api.openmarket.xyz` with key `k-fixture`
  (`settings-fixture.tsx:562`). Notifications and Integrations there can send
  real requests. This pass opened Notifications there once per host and saw no
  such request in the network log. Prefer the shell fixture, and do not drive
  Integrations in `settings-fixture.html`.
- **On `/chat/`, `find role button --name "Members"` hits the dock's Members
  button**, which the open settings dialog covers. Click the nav entry inside
  the dialog instead:
  `[...document.querySelectorAll("[role=dialog] nav button")].find(b => b.textContent.trim() === "Members").click()`.

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
- **Two Appearance extras exist only in the shell.** `Shell.tsx:4549` passes
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
  source (`AgentAccessPage.tsx:401`) did not render in either mode of this
  fixture (measured at `f7d7c987`). Its away branch reads
  `session.remoteControl()`, which this fixture does not stub; that is the
  likely unmet prerequisite (inferred, not driven).
- `?perms=` gates what server and channel settings render. A missing control
  may be a correct permission outcome rather than a regression — check the
  route you opened before reporting one. Measured nav counts at `cd9f8c72`:
  channel `perms=owner` 5 (Overview, Access, Webhooks, Moderation, Danger),
  `perms=member` 1 (Overview); server `perms=owner` 11 (Overview, Roles,
  Members, Moderation, Invites, Integrations, Work Ledger, Library, Recovery,
  Import Vault, Danger), `perms=admin` 10 (no Danger), `perms=member` 4
  (Overview, Roles, Members, Invites). Work Ledger arrives through the server
  admin extra-tab seam, not the static list. The settings fixture also takes
  `state=empty`, `mode=away` and `palette=`.
- The conversion dialog's title names the channel label, not its id:
  **Convert webhooks to alerts · bitcoin** on the fixture's `#btc` channel.

### Verification record

**Last verified:** 2026-10-29 (scheduled maintenance). **Product commit:** `cdfb1b0f` (origin/main; rooms-client 0.108.0). **Scope:** Every user and server settings page body was opened from the shell fixture on `/rooms/` and `/chat/`; see Settings page bodies. Notifications crashed there (`alerts.stripEnabled`), but rendered in `settings-fixture.html` on both hosts. Server Moderation crashed (`spaceModerationState`). **Limitations:** Toggles, saves and the channel Access page were not driven. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261029/r1/`.

**Previous record:** 2026-10-29 (nightly maintenance). **Product commit:** `cdfb1b0f` (origin/main; rooms-client 0.108.0). **Scope:** `settings-fixture.html?host=user&page=shortcuts` showed 19 nav entries and **Vim mode** on `/rooms/` and `/chat/`; `page=appearance` rendered **Appearance**. In the shell, `Meta+/` opened **Grammar & shortcuts**, and `?view=settings` → **Log Out** opened alertdialog **Log Out** ("Are you sure you want to log out?"). **Limitations:** Page bodies beyond these, and the invite link, were not re-driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261029/r1/` (frames 16, 32, 58, 68).

**Previous record:** 2026-10-28 (nightly maintenance). **Product commit:** `2dd7aad1` (origin/main). **Scope:** `settings-fixture.html?host=user&page=shortcuts` showed 19 nav entries and the **Vim mode** switch; `page=appearance` rendered **Appearance** / **Advanced**; `page=agent-access` rendered Agent Settings, Agents, Devices and Recent Logbook. In the shell, `Meta+/` opened **Grammar & shortcuts**; **Log Out** opened alertdialog **Log Out** ("Are you sure you want to log out?") over **Settings**; Invites → **Create invite link** opened **Invite link settings** once the page had loaded (about 2 s; a 1.2 s wait missed the button). **Limitations:** Page bodies without a recipe, palettes, Webhooks conversion, real logout and `/chat/` were not re-driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261028/r1/` (frames 18, 33-34).

**Previous record:** 2026-10-27. **Product commit:** `6c15b0fb286e9dc1b6cb130c9c97cd7e0afa9254` (origin/main). **Scope:** `settings-fixture.html?host=user&page=shortcuts` showed 19 nav entries and the **Vim mode** switch; `page=agent-access` rendered without error. **Limitations:** The `vim` search, palettes, role-specific nav counts, Webhooks conversion, help pages and persisted preferences were not re-driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261027/r01/` (frame 24, 41). Previous record: 2026-10-26 at `5820fbea`.
