# Settings and appearance

User, server, and channel settings — and the appearance controls that repaint
every other surface in the app. The most genuinely interactive fixture surface
in the repo: these controls really work, so this is the best place to prove an
interaction end to end.

## Sub-features

- User settings, eighteen entries plus a conditional OM Settings: My Account, Profiles, Privacy, Sealed
  Messages, Appearance, Notifications, Audio, Keyboard Shortcuts,
  Accessibility, Doc Editing, **Recovered Drafts**, Agent Settings — then a Help
  group (How Agents Work, How the Library Works, How Apps Work, Slash Commands,
  Moderating Servers) and Log Out. Recovered Drafts arrived with `#741` and its
  page id is `draft-recovery`, not `recovered-drafts`. It is **ungated** — no
  permission, no flag, no "only when you have orphans" check — so nineteen is
  the count in every state, and a nav that comes back eighteen is a real
  regression rather than a seeding difference.

  **Nineteen is fixture truth, not app truth.** The Agents group gains an
  **OM Settings** row (id `om`) only when the caller supplies `omPage`.
  `Shell.tsx:4606` always does, so the **running app shows twenty**;
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
- Chat background (since `59f4b22c` and `873a57ce`): a personal picture behind
  the messages (**Chat only**) or behind the whole window (**Whole window**),
  with a **Dim** slider (0–100 %). Since `e60bfd73`, `2f4c247d` and `746aaabd`
  the set state is a live preview you drag to position the picture, with a
  **Zoom** group (Fit, Fill or a percentage). It is uploaded to the account and
  follows the user to other devices. The **Advanced** section's **LIVE PREVIEW** shows only
  placeholder people (Avery Lane, Helper Agent, You) on `example.com`, never
  the user's own contacts (`8d487dc1`).
- Avatar positioning (`2f4c247d`): picking a new avatar under **Profiles**
  opens **Position your avatar**, where you drag the part that shows before
  anything uploads.
- The settings nav has no build or version footer since `55a41da9`.
- High-contrast mode and its interaction with every palette. The system
  contrast preset follows `prefers-contrast: more` independently of the
  explicit high-contrast switch (`packages/chat-ui/src/components/settings/appearance.ts`, `prefers-contrast: more` at `:311`).
- Server settings: Overview, Roles, Members, Moderation, Invites, Integrations,
  Work Ledger, Library, Recovery, Import Vault, Danger. There is **no Access
  page on the server host** — Access is a channel page.
- Channel settings: Overview, Access, Webhooks, Moderation, Danger — gated by
  the viewer's role (`ChannelSettings.tsx:733-747`). Overview has no to-do
  control: `83b02ee4` retired the channel's "To-do widgets" dial and the
  per-viewer override with the legacy board (driven 2026-11-15 on both hosts:
  `host=channel&page=overview&perms=owner` shows **Overview**, **Topics** and
  **Channel index**, and no to-do text).
  Webhooks also offers **Convert webhooks to alerts**. Its review step lets the
  owner select legacy webhooks; URLs and senders stay while deliveries become
  alert cards in that channel's tape (`WebhooksPage.tsx:600`,
  `ConvertWebhooksStepper.tsx:342,419`).
- Keyboard Shortcuts carries an **Editing** group with one switch, **Vim mode**
  (`UserSettings.tsx:1110`, `878049d8`/`b1ed7135`). It is off by default and
  stored as `localStorage["om.chat.vimMode"]` (`"true"`/`"false"`). It is synced and
  scoped per account (`lib/prefs.ts`) and turns on Vim keys in the message box
  ([composer-and-sending.md](composer-and-sending.md)) and the doc editor
  ([your-library.md](your-library.md)). It adds no nav entry. The page's search
  keywords gained `vim modal editing`, so searching `vim` narrows the nav to
  Keyboard Shortcuts.
- Settings search, the Esc-to-close rail behavior, and the open/close
  transition. Since `06ee56bd` the dialog also closes on **browser Back**:
  `SettingsShell.tsx:189` calls `useOverlayHistoryDismiss`
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
| `settings-fixture.html?host=user&page=draft-recovery` | Recovered Drafts — **empty state only**; nothing seeds a draft |
| `settings-fixture.html?host=server&page=roles&perms=owner` | Server roles, as owner |
| `settings-fixture.html?host=server&page=moderation&perms=owner` | Server moderation |
| `settings-fixture.html?host=channel&page=access&perms=owner` | Channel access |
| `settings-fixture.html?host=channel&page=overview&perms=owner` | Channel overview |
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
- **Log Out:** `shell-fixture.html?view=settings&alerts=quiet` → button **Log Out** (`--exact`) opens alertdialog **Log Out**, reading "Are you sure you want to log out?", over the **Settings** dialog. Driven on both hosts. Confirming is a no-op (`onLogout={() => {}}`, `shell-fixture.tsx:4504`), so real logout stays pending.
- **Invite link:** `shell-fixture.html?view=server-settings&settingsPage=invites&alerts=quiet` → **Create invite link** opens dialog **Invite link settings**, with expiry and max-uses controls. Creating a link is INERT. The inbound `InviteLanding` has no harness (it is mounted only by `src/App.tsx:738`).

Verified 2026-10-27 at `6c15b0fb` (maintenance pass, fixture lane). Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261027/r1/` (frames 22-23, 31, 40-41).

### The rail account panel (added 2026-11-10)

`UserPill.tsx` is the rail tile at the bottom left, named **Account: <name>,
<status>** (`aria-haspopup="dialog"`). On a shell route with the people stub,
click it; the panel is portaled to `body` and its rows are `.account-row`
buttons with no `aria-label`:

```bash
agent-browser click 'button[aria-label^="Account:"]'   # "Account: kyle, Unknown"
#   panel: K / kyle / Unknown, rows Edit Profile, Online, Copy Username, Settings, Log Out
agent-browser eval '(()=>{[...document.querySelectorAll(".account-row")].find(r=>r.innerText.trim()==="Online").click()})()'
#   presence choices Online, Idle, Do Not Disturb
agent-browser eval '(()=>{[...document.querySelectorAll(".account-row")].find(r=>r.innerText.trim()==="Settings").click()})()'
#   dialog "Settings"
```

Driven on `/rooms/` and `/chat/` at `eae9681d` (2026-11-10); **Settings** was
pressed on `/rooms/` only. The status reads "Unknown" because the fixtures do
not seed presence. Picking a presence, **Edit Profile** and **Copy Username**
were not driven. Mousedown outside, Escape and a window resize close it.

### Why a control is off (added 2026-11-10)

`Button`, `Menu` rows and `MenuSelect` take a `disabledReason`
(`shared/ui/Button.tsx:14-19`, `shared/ui/Menu.tsx:22-25`,
`MenuSelect.tsx:82-86`). With a reason the control stays focusable, is not
`disabled`, carries `aria-disabled="true"` and is described by the reason.
The Projects ticket in mute is the dense case; see
[projects.md](projects.md) (`ticketMuted=1`): twelve controls, all described
by "You're muted in this server until Jan 1, 8:00 AM.", on both hosts.

The notification settings show the other shape. `UnsavedBar` keeps **Save**
truly `disabled` and points `aria-describedby` at the reason:

```bash
agent-browser open "$(control-om-chat url 'tools/visual/settings-fixture.html?host=user&page=notifications')"
agent-browser click '[aria-label="Enable quiet hours"]'
agent-browser fill  '[aria-label="Quiet hours time zone"]' 'Mars/Olympus'
#   "Unknown time zone; keeping Asia/Kuala_Lumpur"; Save disabled,
#   described by "Enter a valid IANA time zone before saving"
```

Driven on `/rooms/` at `eae9681d` (2026-11-10). Evidence:
`http://127.0.0.1:8098/verify-om-chat-maint-20261110/r1/` (frames 14-15, 19-22).

### Settings page bodies (added 2026-10-29)

Open `shell-fixture.html?view=settings&alerts=quiet` (user) or
`?view=server-settings&alerts=quiet` (server, space "Macro Lab"), then click the
page's nav button. `?settingsPage=<id>` lands on a page directly
(`shell-fixture.tsx:2403-2408`; the `/chat/` fixture reads the same param). Ids:
`privacy`, `secrets`, `notifications`, `audio`, `accessibility`, `docs`,
`draft-recovery`, `agent-guide`, `library-guide`, `apps-guide`,
`slash-commands`, `moderation-guide`; server `overview`, `roles`, `members`,
`moderation`, `invites`, `integrations`, `library`, `recovery`, `danger`.
Reload between pages that crash (see Gotchas).

The user nav lists 19 entries in the shell (driven 2026-11-15 on both hosts;
`USER_NAV`, `UserSettings.tsx:121-202`): My Account, Profiles, Privacy, Sealed
Messages, Appearance, Notifications, Audio, Keyboard Shortcuts,
Accessibility, Doc Editing, Recovered Drafts, Agent Settings, OM Settings, How
Agents Work, How the Library Works, How Apps Work, Slash Commands, Moderating
Servers, Log Out. The server nav lists 10: Overview, Roles, Members,
Moderation, Invites, Integrations, Library, Recovery, Import Vault, Danger.

What each body opens with, identical on `/rooms/` and `/chat/`:

| Page | First text |
|---|---|
| Privacy | **Privacy** — "Control who can follow you, who can message you…" |
| Sealed Messages | **Sealed Messages** — "Sealed messages are managed by the OM app on the device that holds your keys" unless a `/secrets/*` fetch stub answers on `/rooms/`; then RECOVERY CODE, TRUSTED DEVICES, LOST A DEVICE and CHANGED IDENTITIES (see Sealed Messages sections below). `/chat/` always shows the managed-by-the-OM-app text. |
| Notifications | crashes in the shell fixture; renders in `settings-fixture.html?host=user&page=notifications` (**Notifications**, THIS DEVICE, a **Sound** group with the range **Notification volume**, IN THE CHANNEL **Ringing strip at the top**, NOTIFY ME FOR) |
| Audio | **Audio** — "Choose the microphone, speakers, and processing…" (DEVICES) |
| Accessibility | **Accessibility** — MOTION AND FEEDBACK, **Enable reduced motion** |
| Doc Editing | **Doc Editing** — AUTO-PUBLISH WHILE EDITING |
| Recovered Drafts | **Recovered Drafts** (an h2, no h1) — the empty state |
| Help guides | **How agents work**, **How the library works**, **How apps work**, **Slash commands**, **Moderating servers** |
| Server Overview | **Server Overview** — SERVER NAME, SERVER ICON |
| Roles | **Roles** — traders, Full Stack, @everyone |
| Members | **Members** — "5 members", kyle OWNER, ana ADMIN |
| Moderation | crashes in the shell dialog (see Gotchas); on `settings-fixture.html?host=server&page=moderation&perms=owner` it renders with the people stub, carrying **Member actions**, **Active timed mutes** and **Channel bans** |
| Invites | **Invites** — **Create invite link** |
| Integrations | **Integrations** — APPS |
| Library | **Library** — "This server's backend predates library governance…" |
| Recovery | **Library Recovery** — since `d3aebbb5` a `status` callout reads "Recovery isn't available yet: servers can't build recovery previews. Nothing here can run until they can." and **Preview recovery** is disabled (`LibraryRecoverySettings.tsx`, `RECOVERY_SERVICE_READY = false`; driven 2026-11-13 on both hosts with `page=recovery&perms=owner`) |
| Import Vault | **Import Vault** |
| Danger | **Danger** — TRANSFER OWNERSHIP |

In the role editor the colour row is a `role=group` named **Role Color**
(`settings/ColorSwatches.tsx`, used at `settings/RolesEditor.tsx:738`): 21
`.color-swatch` buttons, the first **Default (no color)**, the rest **Role
color #xxxxxx**, each with `aria-pressed`. Driven 2026-11-07 on both hosts at
`?host=server&page=roles&perms=owner`: **Role color #e67e22** starts pressed,
and a click on **Role color #1abc9c** moves `aria-pressed="true"` to it. The
class was `.role-swatch` at `ea399e62`.

A **Projects** server page (keywords "labels tickets"; ticket labels) joins
the server nav when the space runs to-dos in records mode and the viewer can
manage the server or ticket labels (`settings/ServerSettings.tsx:207-210`,
`:274-276`). Its gate is `session.todos?.recordsOn(spaceId) === true`, which
`INERT` never satisfies, so neither settings fixture shows it: live
verification pending.

There is no server **Access** page. Access is a channel page
(`ChannelSettings.tsx:739`), reached only through
`settings-fixture.html?host=channel&perms=owner`. Toggles and saves on these
pages call unstubbed session methods, so only the bodies are proved, not their
effects.

Verified 2026-10-29 at `cdfb1b0f` (scheduled maintenance, both hosts). Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261029/r1/` (`settings-*`, `server-settings-*`, `settings-fixture-notifications-*`).

### Appearance switches, Profiles and Privacy handles (added 2026-10-31)

- **Appearance** (`settings-fixture.html?host=user&page=appearance`) carries
  three switches above the radiogroups: **Show link previews** (on by default;
  clicking it writes `localStorage["om.chat.linkPreviews"]="false"`, clicking
  again `"true"`; `UserSettings.tsx:1671`, `lib/prefs.ts`), **Underline links**
  and **High contrast mode**. The radiogroups read **Theme** (Dark theme /
  Light theme / Sync with OS theme), **Palette** (five), **Chat layout**
  (Bubbles / Streamlined / Custom; the fixture starts on Custom), **Server
  channel layout** and **Direct message layout** (Bubbles / Streamlined) and
  **Message display** (Cozy / Compact). The layout radios carry no
  `aria-label`; read their `label` text. Remove the key afterwards.
- **Profiles** (`?page=profiles`): heading **Profiles**, the display-name field
  (`justintg`), a custom-status field (`long $BTC`) with **Clear custom status
  after**, **Tell people who you are**, **Change avatar**, and the presence
  choices **Online** / **Idle** / **Do not disturb** (`UserSettings.tsx:1062-1064`).
  The presence radios have no accessible name, and clicking **Idle** changed
  nothing in the fixture (no setter is stubbed). The hint under the avatar
  reads "Click the avatar to change it, then drag to choose which part shows.
  Max 2MB." Feed the hidden `input[type=file][accept="image/*"]` with
  `agent-browser upload` and a `dialog` **Position your avatar** opens
  (`settings/AvatarCropDialog.tsx`) with a `slider` **Avatar position**
  ("Whole picture shown" for a square picture), **Cancel** and **Save**.
  **Cancel** closes it and uploads nothing (driven 2026-11-06 on both hosts).
- **No To-dos page.** `83b02ee4` removed it with `om.chat.todoVisibility`. An
  unknown id falls back to My Account (`UserSettings.tsx:251-260` keeps only
  ids in `USER_NAV`), so `settings-fixture.html?host=user&page=todos` opens
  **My Account** with no radiogroup (driven 2026-11-15 on both hosts).
- **Privacy**: `settings-fixture.html?host=user&page=privacy` renders a blank
  page (no nav, no body) on this lane; use the shell route
  `shell-fixture.html?view=settings&settingsPage=privacy&alerts=quiet`, which
  shows heading **Privacy** and the switch **Private account**. The
  who-can-message choices Everyone / People you follow / No one
  (`UserSettings.tsx:812-826`) are a select, not radios.

Driven 2026-10-31 on `/rooms/` (18135) at `936f5b64`.

### Notification volume (added 2026-10-30)

`3306463a` adds a per-device **Notification volume** to Settings →
Notifications, in a **Sound** group between push enrollment and the tones
(`NotificationSettings.tsx:193`, `NotificationVolume.tsx`). It is a range
`#om-notification-volume`, 0-100 in steps of 1, default 100, with a `NN%`
readout. It is stored on this device only under
`om.chat.notificationVolume` (`lib/notification-volume.ts:22`). `7a1b8a10`
gives every `.slider` a visible track and a fill, set through
`--slider-pct`; the Audio page's **Call volume** carries it too.

Drive it on `settings-fixture.html?host=user&page=notifications`; the shell
fixture's Notifications page crashes (Gotchas). Focus `#om-notification-volume`
and press ArrowLeft five times. The value and readout go to 95 / `95%`,
`--slider-pct` to `95%`, and `localStorage["om.chat.notificationVolume"]` to
`"95"`. Reload and all three still read 95. Remove the key afterwards; it is
sticky. The audio preview needs a real browser with sound and is not proved
here. Driven 2026-10-30 at `47cb13bf` on `/rooms/` (frames 20-21). The same
page on `/chat/` (`/chat/tools/visual/settings-fixture.html?host=user&page=notifications`)
renders without a crash; a click on the track set 50, ArrowLeft set 49, and
`om.chat.notificationVolume` kept `"49"` across a reload (scheduled
maintenance, 2026-10-30).

### Push enrollment (added 2026-11-02)

`settings-fixture.html?host=user&page=notifications` renders
`PushEnrollmentSection` (`settings/NotificationSettings.tsx`) under the volume
slider with a button named **Enable notifications** (it reads **Re-enroll push
on this device** once permission is granted). The button mounts on the lane
(driven 2026-11-02 on `/rooms/`), but the browser permission prompt and the
enrollment itself need a real daemon and a non-headless browser, so pressing it
proves nothing here.

### Motion and feedback sounds (added 2026-11-02)

`settings-fixture.html?host=user&page=accessibility` has a **Motion and
feedback** card (`settings/UserSettings.tsx:1890-1915`) with four switches:
**Enable reduced motion**, **Resolve sound**, **GOAT ceremony sound** and
**GOAT bleat**. On a fresh lane the three sound switches read
`aria-checked="true"` and reduced motion reads `false`. `find role switch click
--name "Resolve sound"` turns it off and writes `om.chat.resolveSound=false`
to `localStorage` (`lib/prefs.ts:535`); assert the key, not only the switch.
**GOAT ceremony sound** and **GOAT bleat** write `om.chat.goatSoundEnabled`
and `om.chat.goatBleatEnabled` the same way (`lib/goat-ceremony.ts:9-10`).
Switching them shows the save receipt **Saved · just now**
(`span.ui-save-receipt[role=status][data-save-flash]`, `shared/ui/SaveReceipt.tsx:16`),
and all three stay off after a reload (2026-11-08, both hosts). The chime
itself (`lib/resolve-chime.ts`) plays on a topic resolve and is not
observable in a headless lane.

### Audio processing (added 2026-11-02)

`settings-fixture.html?host=user&page=audio` renders three processing switches
(`settings/AudioSettings.tsx:333-347`): **Noise suppression**, **Echo
cancellation** and **Automatic input gain**, all `aria-checked="true"` on the
lane. The microphone and device pickers on the same page need a real input
device, so only the switch states are provable here.

Since `0423aaa8` the page no longer asks for the microphone when it opens: it
lists what the browser shows unasked (`AudioSettings.tsx:112-137`), under the
headings **Devices**, **Output** and **Microphone processing**. A **Test
microphone** button (`:264`) starts the only prompt; while a test runs it reads
**Stop test** and a `role="meter"` named **Microphone level** (`:271`) appears,
and a refused prompt reads "Microphone access wasn't granted. Allow it in your
browser, then test again." Driven 2026-11-13 on both hosts: **Test
microphone** present and no meter on open. Pressing it calls `getUserMedia`,
which a headless lane cannot answer, so the test itself stays source only.

### Settings search with no match (added 2026-11-02)

Type into **Search settings** (`input[aria-label="Search settings"]`) a string
nothing matches, such as `zzqqx`: the nav empties and reads **No setting
matches “zzqqx”.** with curly quotes (`settings/SettingsShell.tsx:283`).

The **Discard unsaved changes?** alertdialog (`SettingsShell.tsx:435`) is
reached on `page=profiles` (plural; `page=profile` has no editable input).
Type into the textbox **Display name** (`#om-display-name`,
`settings/UserSettings.tsx:928`); a **Reset** button appears. Press Escape:
the alertdialog reads "Your unsaved changes will be lost." with **Keep
editing** and **Discard changes**. **Keep editing** closes it and keeps the
typed value (2026-11-08, both hosts). **Discard changes** and leaving by a nav
row were not driven.

```bash
agent-browser open "$(control-om-chat url 'tools/visual/settings-fixture.html?host=user&page=profiles')"
agent-browser fill '#om-display-name' 'Nightly Probe'
agent-browser press Escape
agent-browser find role button click --name "Keep editing"
```

### Chat background and the live preview (added 2026-11-05)

User path: **Settings** → **Appearance** → **CHAT BACKGROUND** (a `region`
with `data-settings-group="chat-background"`, between Accent and Advanced;
`ChatBackgroundSettings.tsx`, mounted at `UserSettings.tsx:1406`). Click
**Upload picture**, pick a PNG, JPEG or WebP, then choose **Chat only** or
**Whole window** and set **Dim**. **Remove** clears it.

Handles, as driven on 2026-11-06 at `ea399e62` on `/rooms/`. The position
picker and **Zoom in** were also driven on `/chat/`:

- The group opens with the hint "Only you see it. It follows your account to
  your other devices."
- Empty: the drop zone reads **No picture yet** and "PNG, JPEG or WebP, up to
  5 MB. You can also drop a picture here.", with `button` **Upload picture**.
  The `radiogroup` **Cover** (`radio` **Chat only**, checked, and **Whole
  window**) is disabled (`aria-disabled="true"`), and so is the **Dim** range
  `#om-chat-background-dim`, which already shows 90 %. There is no **Remove**.
- Set: a live preview (`settings/ChatBackgroundPreview.tsx`) replaces the old
  preview `img`. It draws a stage card with a fake sidebar (**CHANNELS**,
  `# general`, `# design`, `# markets`), sample lines ("Avery Lane Notes are
  up", "Looks good, ship it") and a **Message #general** box over the picture.
  - A `slider` with `aria-roledescription="position picker"`, named
    **Background position in the chat**, or **Background position in the whole
    window** under **Whole window**. Its `aria-valuetext` starts at "50% from
    top". After two **Zoom in** clicks, ArrowUp twice and ArrowLeft once read
    "40% from top, 45% from left".
  - A `group` **Zoom** with **Zoom out**, **Zoom in**, a readout and **Reset**.
    The readout reads **Fit**, **Fill** or a percentage. A square picture
    starts on **Fill** with **Reset** disabled. One **Zoom in** gives 120 %,
    two give 140 %, and **Reset** returns to **Fill**.
  - The hint reads "Drag to move, pinch to zoom". Source also has "Zoom in to
    move the picture" for when there is nothing to move; that one was not seen
    live.
  - **Replace picture**, **Remove**, **Cover** and **Dim**. Dim runs 0–100 %
    in steps of 5. Below 50 % it adds the note "Text may be hard to read."
- The hidden file input is `input[aria-label="Choose a chat background
  picture"]`; feed it with `agent-browser upload '<that selector>' <file>`.
- The pref is `localStorage["om.chat.chatBackground"]`, shaped
  `{"default":{"url","key","dim"}}`, plus `"cover":"window"` only in window
  mode. Zooming adds `zoom` and `aspect`, and moving adds `position:{x,y}`
  (`lib/chat-background.ts`). **Reset** drops all three. A seed with only
  `url`, `key` and `dim` still parses. **Remove** deletes the key, shows the
  receipt **Chat background removed** and returns to **No picture yet**.
- Painting is CSS on `<html>`: `data-chat-background=""`, `--chat-bg-image`,
  `--chat-bg-dim`, and `data-chat-background-cover="window"` in window mode
  (`lib/chat-background.ts:350`). **Chat only** paints the conversation
  column: since `f8a1e04b`, `[data-chat-backdrop]` sits on
  `ChatBackdropColumn.tsx`, which holds both the `role=log` tape and the
  composer, so the picture runs behind the composer too (one wrapper on room,
  DM and topic, driven 2026-11-13). **Whole window** paints
  `.app-shell` once and turns the five `[data-chat-backdrop-plane]` panels
  translucent.

Upload refusals, driven on both fixtures: a `.gif` toasts "GIFs can't be a
chat background. Pick a PNG, JPEG or WebP picture."; a non-image renamed
`.png` toasts "That file couldn't be read as a picture. Pick a PNG, JPEG or
WebP image."; a real PNG reaches the upload and toasts "The picture could not
be uploaded." because the fixtures' session has no `chatBackgroundHost`. A
successful upload (`POST /users/chat-background`, `attachments-seam.ts:934`)
needs a live host and is **live verification pending**.

To drive the set states with no upload, seed the pref with a loopback URL
(only `https:` or `http:` on `localhost`/`127.0.0.1` paints):

```bash
agent-browser eval "localStorage.setItem('om.chat.chatBackground', JSON.stringify({default:{url:'$(control-om-chat url icons/icon-512.png)',key:null,dim:0.7}}))"
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=settings&settingsPage=appearance&alerts=quiet')"
agent-browser find role radio click --name "Whole window"   # applies; html gets data-chat-background-cover="window"
agent-browser press Escape                                 # .app-shell background-image is the url
```

The **LIVE PREVIEW** (`[aria-label="Message appearance preview"]`, tablist
**Preview conversation**) reads **# sample-channel** with Avery Lane, Helper
Agent (with the **AGENT** chip) and You on the **Server** tab, and **Avery
Lane** with "The new layout is ready on example.com" and an **Example Domain**
card on **Direct message**. It never reads "Jiin", "# design" or
`openmarket.xyz` (`UserSettings.tsx:1447`).

### Server mutes and the Mute Members grant (added 2026-11-09)

`591b1e11` added a mute that holds a member in every channel and in Projects.
Two surfaces come from it, and both are gated on the store's
`permissionsVersion` being at least 7 (`lib/room-actions.ts:77-81`):

- **Moderation** gains an `h2` **Server mutes** (`ModerationPage.tsx:399`) for
  whoever holds `mute-members`. Empty, it reads "No one is muted across this
  server." Each row carries `data-server-mute=<userId>` and "Whole server ·
  {time} remaining", with a **Remove** button for whoever may unmute. A holder
  of `mute-members` with no channel rights still gets the page, without
  **Member actions**, **Active timed mutes** and **Channel bans**.
- **Roles** gains a **Mute Members** row with the hint "Mute a member in every
  channel and in Projects until a set time" (`lib/space-actions.ts:83`), hidden
  below version 7 (`RolesEditor.tsx:472`).

No fixture stubs the version or the grant, so add to the init script from
[README.md](README.md) / Stub the people directory first:
`spacePermissionsVersion: () => 7` and `spaceActionAllowed: () => true`. On
`settings-fixture.html?host=server&page=moderation&perms=owner` the headings
read **Moderation**, **Member actions**, **Server mutes**, **Active timed mutes**
and **Channel bans**, with the empty line above (driven 2026-11-09 on `/rooms/`).
On `settings-fixture.html?host=server&page=roles&perms=owner` open **Permissions**
and find **Mute Members** with its hint (driven 2026-11-09 on both hosts). With
the version stub the tab lists 26 rows, Manage Server through Administrator,
and no **Nudge People**: `6aeb4bbc` dropped that row, because nothing in the app
sends the channel `!nudge` page any more. A role that already holds `nudge`
keeps it, since the editor saves the whole grant list (driven 2026-11-15 on
both hosts). The
member-row flyout is out of reach: `session.userMenu` is `null` and `openUserMenu`
is unstubbed on both shell fixtures, so **Mute in server**, **Remove server mute**
and the row **Remove** are still `live verification pending`.

On `/chat/`, `settings-fixture.html?host=server&page=moderation` renders blank
because the cloud settings fixture has no `spaceModerationState`. The root
fixture spells it out (`tools/visual/settings-fixture.tsx:626`); on `/chat/` it
answers `INERT`, and the page throws "session.spaceModerationState(...).then is
not a function". Add one more init script after the people stub:

```bash
cat > "$SCRATCH/chat-moderation-stub.js" <<'JS'
(() => {
  Object.defineProperty(Object.prototype, "spaceModerationState", {
    value: async () => ({ rooms: [], moreChannels: false }),
    configurable: true, writable: true, enumerable: false });
})();
JS
```

With it, the `/chat/` page shows **Moderation**, **Member actions**, **Active
timed mutes** and **Channel bans** with no console error (driven 2026-11-10).

### Sealed Messages sections (added 2026-11-14)

Since `f0c5d67a` the page is built from sections that follow
`fetchSecretsStatus()` (`settings/SecretsPage.tsx`; nav entry
`UserSettings.tsx:135`). The data comes from a module adapter, not the session:
`src/lib/secrets.ts` fetches `daemonUrl("/secrets/<path>")` and unwraps
`{ok:true,data}`, and any network failure becomes "unavailable"
(`src/lib/secrets.ts:104-147`). The cloud adapter `apps/cloud/src/lib/secrets.ts`
always throws, so `/chat/` only ever shows **Sealed messages are managed by the
OM app on the device that holds your keys. Open OM Chat there to view or save
your recovery code.** The fixtures have no daemon, so `/rooms/` shows the same
text until a fetch stub answers.

The `Object.prototype` seam cannot reach a module adapter, and the fixture
assigns `window.fetch` itself, so the stub wraps the assignment with a
getter/setter. It picks a status from `?secretsSeed=`:

```bash
cat > "$SCRATCH/fixture-secrets-stub.js" <<'JS'
(() => {
  const seed = new URLSearchParams(location.search).get("secretsSeed") || "ready";
  const devices = [
    { deviceId: "d1", label: "MacBook Air", linkedAt: "2026-11-01T09:00:00Z", linkedBy: null },
    { deviceId: "d2", label: "Mac mini", linkedAt: "2026-11-05T09:00:00Z", linkedBy: "d1" },
  ];
  const alarms = [
    { userId: "u-dax", previousIdentityPub: "aa", newIdentityPub: "bb", kind: "verified-reset", raisedAt: "2026-11-10T00:00:00Z" },
    { userId: "u-mira", previousIdentityPub: "cc", newIdentityPub: "dd", kind: "support-reset", raisedAt: "2026-11-11T00:00:00Z" },
  ];
  const base = { userId: "u-self", readiness: "ready", hasRecoveryBlob: true, recoveryVerified: true, devices, alarms };
  const status = {
    ready: base,
    unverified: { ...base, recoveryVerified: false, alarms: [] },
    nocode: { ...base, hasRecoveryBlob: false, alarms: [] },
    badlist: { ...base, devices: undefined, devicesUnverified: true, alarms: [] },
    restore: { userId: "u-self", readiness: "needs-restore", hasRecoveryBlob: true, alarms: [] },
    fresh: { userId: "u-self", readiness: "needs-restore", hasRecoveryBlob: false, alarms: [] },
  }[seed] || base;
  const code = "otter-maple-cinder-velvet-harbor-quill";
  const routes = {
    status: () => status,
    devices: () => ({ devices }),
    "link/start": () => ({ code: "amber-river-stone-lamp", pairingId: "p1", expiresAt: new Date(Date.now() + 300000).toISOString() }),
    "link/pending": () => ({ state: "request", label: "Pixel 9", deviceId: "d3" }),
    "link/approve": () => ({ approved: true }),
    reset: () => ({ code, signedOutOthers: false }),
    "recovery/mint": () => ({ code, rotated: true }),
    "alarms/ack": () => ({ acknowledged: true }),
  };
  const calls = (window.__secretsCalls = []);
  const wrap = (f) => (i, o) => {
    const m = String(typeof i === "string" ? i : (i && (i.url || i.href)) || "").match(/\/secrets\/([^?]+)/);
    if (!m || !routes[m[1]]) return f(i, o);
    calls.push(m[1]);
    return Promise.resolve(new Response(JSON.stringify({ ok: true, data: routes[m[1]]() }),
      { status: 200, headers: { "content-type": "application/json" } }));
  };
  let inner = window.fetch.bind(window);
  Object.defineProperty(window, "fetch", { configurable: true, get: () => wrap(inner), set: (v) => { inner = v; } });
})();
JS
cat "$SCRATCH/fixture-people-stub.js" "$SCRATCH/fixture-secrets-stub.js" > "$SCRATCH/init-secrets.js"
agent-browser --init-script "$SCRATCH/init-secrets.js" open about:blank
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=settings&alerts=quiet&settingsPage=secrets&secretsSeed=ready')"
```

Driven 2026-11-14 on `/rooms/` (18173):

- **`ready`.** h1 **Sealed Messages**, then h2 **Recovery Code** ("A recovery
  code is saved for this account.", a code textbox and **Create a new code**,
  disabled until it holds text), **Trusted Devices** (two `[data-sealed-device]`
  rows, "Linked Nov 1, 2026", and **Add a device**), **Lost a Device** and
  **Changed Identities** (`[data-identity-alarm="u-dax"]` "dax reset their
  sealed keys on Nov 10, 2026 · confirm to keep sending"; `u-mira`'s
  support-reset row is the loud yellow one, each with **Accept new key**).
- **Add a device.** Shows `[data-link-code]` **amber-river-stone-lamp** with
  "Expires in". The section polls `link/pending` (`SealedDevicesSection.tsx:66-89`);
  a few seconds later `[data-link-request]` reads **Give "Pixel 9" your sealed
  keys?** with **Approve** and **Cancel**. **Approve** posts `link/approve` and
  re-reads `status`. Its success toast does not render: the shell fixture's
  `toast` is a no-op.
- **Lost a Device.** **Reset sealed keys** stays disabled after the textbox
  **Recovery code for reset** is filled, and enables once the checkbox **Other
  devices lose access and every other login is signed out** is ticked. Pressing
  it replaces the page with one RECOVERY CODE card: "Write this down somewhere
  safe. It won't be shown again. Your previous code no longer works. Sign out
  your other sessions from your account page.", the code, **Copy** and **I saved
  it**. **I saved it** brings the four sections back.
- **`unverified`.** Recovery Code adds "Re-enter your recovery code once so a
  stolen login can't swap your keys" with **Verify**.
- **`nocode`.** "Recovery code not saved. …" with **Create my recovery code**;
  no Lost a Device section (it needs a saved code).
- **`badlist`.** Trusted Devices reads "This device list failed its check, so it
  isn't shown."
- **`restore`.** h2 **Link This Device** ("On a trusted device, open Sealed
  Messages and press Add a device.", **Link**) and **Restore This Device**
  (**Restore**).
- **`fresh`.** **Link This Device** and **Start Fresh**: the explainer, the
  checkbox **I understand old sealed messages are lost for good** and **Start
  fresh**.

On `/chat/` (18174) the same stub makes no `/secrets/*` call and the page shows
only the managed-by-the-OM-app text. Not driven: **Copy**, **Verify**, **Create a
new code**, **Accept new key**, **Link**/**Restore**/**Start fresh** submits, the
code-expired and code-mismatch notes, and a real daemon.

## Gotchas

- **The shell fixtures do not paint a seeded chat background at boot.** The
  apps call `initChatAppearance()` from `main.tsx`; neither shell fixture does,
  so a seeded `om.chat.chatBackground` leaves `<html>` bare and
  `[data-chat-backdrop]` at `background-image: none`. Change any control in
  **CHAT BACKGROUND** (Cover or Dim) and it applies to the live shell behind
  the dialog. The settings fixture shows the set controls from the seed but
  likewise paints only after a change.

- **Notifications crashes the shell fixture's whole User settings surface.**
  `ChannelStripRow` calls `alerts.stripEnabled()` (`NotificationSettings.tsx:607`),
  and neither fixture's plain-object `alertsStub` has it
  (`shell-fixture.tsx:1425`, `apps/cloud/tools/visual/shell-fixture.tsx:539`).
  `LazySurfaceGate` then swaps the entire dialog, nav included, for **User
  settings could not load** / **Try again**. Any further page click finds no
  button, and **Try again** returns to My Account. Reload before driving the
  next page. Server **Moderation** fails the same way, as **Server settings
  could not load**, because `session.spaceModerationState(...).then` hits
  `INERT`. Both crash on both hosts. The standalone `/chat/` settings fixture
  has the same `spaceModerationState` gap; see Server mute above for its init
  stub.
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
- **Two Appearance extras exist only in the shell.** `Shell.tsx:4604` passes
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

**Last verified:** 2026-11-15 (nightly maintenance). **Product commit:** `96644a29` (GitLab origin/main; rooms-client 0.118.0; 8 commits past `62fcc01a`). **Scope:** `/rooms/` (18175) and `/chat/` (18176): the shell `?view=settings` nav lists 19 entries with no To-dos; `settings-fixture.html?host=user&page=todos` falls back to **My Account** with no radiogroup; `host=channel&page=overview&perms=owner` shows **Overview**, **Topics**, **Channel index** and no to-do control; `host=server&page=roles&perms=owner` → **Permissions**, with the version stub, lists 26 rows with **Manage Labels** and **Mute Members** and no **Nudge People**. **Limitations:** the other page bodies were not re-driven (the 2026-11-14 record stands); no grant was saved. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261115/r1/` (frames 11, 12, 13, 17).

**Previous record:** 2026-11-14 (nightly maintenance). **Product commit:** `62fcc01a` (GitLab origin/main; 9 commits past `504b08d5`). **Scope:** `shell-fixture.html?view=settings&settingsPage=secrets` on `/rooms/` (18173) with the people stub and the `/secrets/*` fetch stub: the six seeds, **Add a device** through **Approve**, and the **Reset sealed keys** gate to the minted-code card; on `/chat/` (18174) the managed-by-the-OM-app text. **Limitations:** a real daemon, toasts (fixture no-op), and the submits listed in the recipe. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261114/r1/`.

**Previous record:** 2026-11-13 (nightly maintenance). **Product commit:** `504b08d5` (GitLab origin/main; rooms-client 0.117.0; 32 commits past `eae9681d`). **Scope:** `settings-fixture.html` on `/rooms/` (18170) and `/chat/` (18171): Audio (**Devices**, **Output**, **Microphone processing**, **Test microphone**, no meter), Server **Recovery** (status callout, **Preview recovery** disabled), Server **Projects** (with the Projects stub; see [projects.md](projects.md)); `/rooms/`: one `[data-chat-backdrop]` holding tape and composer on room, DM and topic. **Limitations:** the microphone test, the Projects confirmations and a painted background. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261113/r1/` (frames 32-33, 39, 43).

**Previous record:** 2026-11-10 (scheduled maintenance). **Product commit:** `eae9681d` (GitLab origin/main, rooms-client 0.115.0). **Scope:** the rail account panel on `/rooms/` (18141) and `/chat/` (18142) with the people stub (five rows; on `/rooms/` also the presence choices and **Settings** opening the Settings dialog); on `/rooms/`, the notification settings' invalid time zone disabling **Save** with its described reason. **Limitations:** no presence change, profile edit or username copy; the time-zone reason was not driven on `/chat/`. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261110/r1/`.

**Previous record:** 2026-11-10 (nightly). **Product commit:** `eae9681d` (GitLab origin/main, rooms-client 0.115.0). **Scope:** `host=server&page=moderation` on `/rooms/` (18186: **Moderation**, **Member actions**, **Active timed mutes**, with the people stub) and on `/chat/` (18187: blank with "session.spaceModerationState(...).then is not a function", then the four headings with the moderation init stub); every `settings-fixture.html?page=` route in the guides mounted on both hosts except `page=privacy`. **Limitations:** `page=privacy` is still blank on both hosts; the `/chat/` stub seeds no channel rows; the Mute in server flyout and the row **Remove** are unreachable. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261110/r1/`.

**Previous record:** 2026-11-09 (nightly maintenance). **Product commit:** `82390825` (GitLab origin/main; rooms-client 0.114.0; 49 commits past `08fe407b`). **Scope:** `/rooms/` and `/chat/` with the people stub: `settings-fixture.html` Appearance, Server Overview and channel Overview headings; **Mute Members** in **Permissions** on both hosts; **Server mutes** with "No one is muted across this server." on `/rooms/`. **Limitations:** `page=privacy` is still blank on both hosts and `/chat/` `host=server&page=moderation` still crashes (`ModerationPage`); the Mute in server flyout and the row **Remove** are unreachable. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261109/r1/`.

**Previous record:** 2026-11-08 (nightly maintenance). **Product commit:** `08fe407b` (GitLab origin/main; rooms-client 0.112.0; unchanged since the 2026-11-07 pass). **Scope:** `/rooms/` (18183) and `/chat/` (18184): `page=appearance` with the Dim slider; **Role Color** on `host=server&page=roles`; the three sound switches with their keys, **Saved · just now** and reload persistence; "No setting matches “zzzq”."; the **Discard unsaved changes?** guard via `page=profiles`. **Limitations:** `page=privacy` blank on both hosts and `host=server&page=moderation` blank on `/chat/` (carried). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261108/r1/`.

**Previous record:** 2026-11-07 (nightly maintenance). **Product commit:** `08fe407b` (GitLab origin/main; rooms-client 0.112.0; 89 commits past `ea399e62`). **Scope:** `/rooms/` (18180) and `/chat/` (18181) `settings-fixture.html?page=appearance` mounts **Appearance** with the chat background and the Dim slider; `?host=server&page=roles&perms=owner`: the **Role Color** group (21 `.color-swatch` buttons, **Default (no color)** `aria-pressed="false"`), and a click moves `aria-pressed="true"` from **Role color #e67e22** to **Role color #1abc9c**. **Limitations:** the Projects settings page needs a records-mode server; `page=privacy` blank on both hosts and `host=server&page=moderation` blank on `/chat/` (route smoke). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261107/r1/`.

**Previous record:** 2026-11-06 (nightly maintenance). **Product commit:** `ea399e62` (GitLab origin/main; rooms-client 0.111.0; 74 commits past `873a57ce`). **Scope:** `/rooms/` (18180) shell fixture `view=settings&settingsPage=appearance`: **CHAT BACKGROUND** empty (**No picture yet**, Cover and Dim disabled, Dim 0–100 step 5); a seeded picture shows the position picker **Background position in the chat** and the **Zoom** group (**Fill** → 140 % after two **Zoom in**, ArrowUp ×2 + ArrowLeft → "40% from top, 45% from left", stored `zoom`, `aspect`, `position`); **Whole window** renames the slider and sets `data-chat-background-cover="window"`; **Reset** returns to **Fill**; Dim 30 % shows "Text may be hard to read."; **Remove** → **Chat background removed**; no build footer. `settings-fixture.html?host=user&page=profiles`: the new avatar hint and **Position your avatar** (**Avatar position**, **Cancel**, **Save**). `/chat/` (18181): the picker, **Zoom in** → 120 %, no footer, and the avatar dialog. **Limitations:** a successful upload, pinch and pointer drag of the picture, and the avatar **Save** upload were not proved. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261106/r1/`.

**Previous record:** 2026-11-05 (nightly maintenance). **Product commit:** `873a57ce` (GitLab origin/main; rooms-client 0.109.1; 17 commits past `ce14d4ba`). **Scope:** `/rooms/` (18170) `settings-fixture.html?host=user&page=appearance`: **CHAT BACKGROUND** empty state, the GIF, unreadable-file and inert-upload toasts, a seeded picture (**Replace picture**, **Remove**, **Dim** 90 % → 80 %), **Whole window** ↔ **Chat only** with `data-chat-background-cover` and the stored `cover`, **Remove** → **Chat background removed**; the **LIVE PREVIEW** Server and Direct message tabs (Avery Lane, Helper Agent **AGENT**, no Jiin or openmarket.xyz). `/rooms/` and `/chat/` (18171) shell fixture `view=settings&settingsPage=appearance`: **Whole window** paints `.app-shell` with the picture and five translucent `[data-chat-backdrop-plane]` panels; **Chat only** paints the `role=log` `[data-chat-backdrop]` on `/chat/`. **Limitations:** a successful upload needs a live host; the other settings pages were covered only by the route smoke. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261105/r1/` (`01`–`15`, `smoke/`).

**Previous record:** 2026-11-04 (nightly maintenance). **Product commit:** `ce14d4ba` (GitLab origin/main; rooms-client 0.109.1; 16 commits past `ba4389e7`). **Scope:** `/rooms/` (18160) and `/chat/` (18161): `?view=settings` opens the dialog **Settings**. **Limitations:** the settings fixture pages were covered only by the route smoke. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261104/r1/` (`smoke/`).

**Previous record:** 2026-11-03 (nightly maintenance). **Product commit:** `ba4389e7` (GitLab origin/main; rooms-client 0.108.0; one CI-only commit past `3f8f24bc`). **Scope:** `/rooms/` (18143) and `/chat/` (18144): 12 `settings-fixture` pages (privacy is blank on both hosts, and `host=server&page=moderation` is blank on `/chat/`); **Light theme**, **Moss palette** and **Iris accent**; searching `vim` narrows to **Keyboard Shortcuts**; `zzqqx` reads **No setting matches “zzqqx”.**; **Convert webhooks to alerts · bitcoin**; **Invite link settings**; `Meta+/` → **Grammar & shortcuts** → **Close shortcuts**. **Limitations:** unchanged. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261103/r1/` (`set-*`).

**Previous record:** 2026-11-02 (scheduled maintenance). **Product commit:** `3f8f24bc` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18141): `page=appearance` **Light theme** → `data-theme` dark → light; **Settings navigation**; **Search settings** `vim` → Keyboard Shortcuts, `zzqqx` → **No setting matches “zzqqx”.**; `page=accessibility` **Resolve sound** on → off with `om.chat.resolveSound=false`; `page=audio` three processing switches on; `host=channel&page=webhooks&perms=owner` **Convert webhooks to alerts**; `page=shortcuts` Vim switch present. `/chat/` (18142): **Light theme** dark → light, **Settings navigation**. **Limitations:** the discard guard was not reached (`page=profile` has no editable input); the other page bodies were not re-driven, so the nightly record below stands for them. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261102/r1/`.

**Previous record:** 2026-11-02 (nightly maintenance). **Product commit:** `3f8f24bc` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18137) and `/chat/` (18138): `?view=settings` → dialog **Settings** over `#ops` (20 nav entries; about 5–6 s after load on `/chat/`); the Appearance radiogroups (Theme, Palette, Chat layout, Server channel layout, Direct message layout, Message display) and **Show link previews** true → false (`/rooms/`); Notifications volume 100 → 99 with `om.chat.notificationVolume=99` (both hosts) and the **Enable notifications** button; **Convert webhooks to alerts** → **Convert webhooks to alerts · bitcoin** (Cancel, **Convert 2**) on both hosts; Server Settings → Invites → **Create invite link** → **Invite link settings** (**Invite link expiry**, **Invite link max uses**, **Create link**, **Done**) on both hosts; ⌘/ → **Grammar & shortcuts**; **Log Out** → the **Log Out** confirm (Cancel / Log Out) on `/rooms/`; the Profiles, To-dos and Slash commands pages render; `page=privacy` is blank on both hosts; `host=server&page=moderation` renders on `/rooms/` and is blank on `/chat/`. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261102/r1/`.

**Previous record:** 2026-11-01 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18137): `?view=settings&settingsPage=shortcuts` → the **Settings** dialog (20 nav items) over `#ops`, **Vim mode** on → `om.chat.vimMode="true"`, **Log Out** → the **Log Out** alertdialog; ⌘/ → the **Grammar & shortcuts** dialog; `settingsPage=privacy` → **Privacy** with **Private account**; `settings-fixture` Appearance (**Show link previews** off → `om.chat.linkPreviews="false"` and back, **Underline links**, **High contrast mode**, the six radiogroups; **Light theme** selects without recolouring the fixture's `<html>`), Notifications (100 → 99, `om.chat.notificationVolume`), Profiles (justintg, long $BTC, Online / Idle / Do not disturb), To-dos (two radiogroups); the settings takeover at 390 ([mobile-shell-navigation.md](mobile-shell-navigation.md)). `/chat/` (18138): the **Settings** dialog mounts about five seconds after load (a 2 s read saw none), **Vim mode**, **Log Out**, ⌘/, **Light theme**, notification volume 100 → 99. Load smoke: every `settings-fixture` page mounted on `/rooms/` except `page=privacy` (blank); on `/chat/` `page=privacy` and `host=server&page=moderation` are blank. **Limitations:** the webhooks **Convert** dialog and the invite-link dialog were not re-driven (2026-10-31 stands); toggles and saves remain unstubbed. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261101/r1/` (`settings-01` to `settings-05`, `mobile-02`, `mobile-03`, `chat-07`).

**Previous record:** 2026-10-31 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18135): **Light theme** → `data-theme=light` (restored); Notifications `#om-notification-volume` ArrowLeft ×5 → 95 / `95%` / `om.chat.notificationVolume="95"` (removed); **Vim mode** switch → `om.chat.vimMode="true"` (reset); **Log Out** alertdialog; Meta+/ → **Grammar & shortcuts**; Invites → **Invite link settings**; channel Webhooks → **Convert webhooks to alerts · bitcoin**; Appearance switches and radiogroups, Profiles, To-dos and Privacy as above. `/chat/` (18136): **Light theme**, volume 95 kept in storage, **Log Out**, Meta+/, and the shell settings nav with 20 entries. **Limitations:** Effects of every toggle beyond local storage; Notifications and server Moderation still crash the shell fixture; Help and guide bodies not re-read; tones and audio preview. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261031/r1/`.

**Previous record:** 2026-10-30 (scheduled maintenance). **Product commit:** `47cb13bf` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/`: `?view=settings` dialog **Settings** and the **Log Out** alertdialog; settings fixture **Light theme** (`data-theme=light`); server **Roles** with `perms=owner`; the **Slash commands** guide page; **Notification volume** renders. `/chat/`: the settings dialog nav (20 entries) and the Notification volume set and persisted (49). **Limitations:** Most page bodies were not re-driven this pass (2026-10-29 stands); Notifications still crashes the shell fixture. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261030/r1/` (frames 09, 21).

**Previous record:** 2026-10-30 (nightly maintenance). **Product commit:** `47cb13bf` (GitLab origin/main; rooms-client 0.108.0). **Scope (`/rooms/`, `settings-fixture.html`):** **Notification volume** moved 100 → 95 with ArrowLeft, wrote `om.chat.notificationVolume`, and survived a reload. **Sound** was the group heading. The Audio page's **Call volume** carried `.slider` with `--slider-pct: 100%`. **Limitations:** Only the delta was driven tonight; the rest of this guide keeps its 2026-10-29 proof. `/chat/` and the sound preview were not driven. Evidence is local only: `artifacts/vomc-nightly-20261030/r1/` (frames 20-21).

**Previous record:** 2026-10-29 (scheduled maintenance). **Product commit:** `cdfb1b0f` (origin/main; rooms-client 0.108.0). **Scope:** Every user and server settings page body was opened from the shell fixture on `/rooms/` and `/chat/`; see Settings page bodies. Notifications crashed there (`alerts.stripEnabled`), but rendered in `settings-fixture.html` on both hosts. Server Moderation crashed (`spaceModerationState`). **Limitations:** Toggles, saves and the channel Access page were not driven. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261029/r1/`.

**Previous record:** 2026-10-29 (nightly maintenance). **Product commit:** `cdfb1b0f` (origin/main; rooms-client 0.108.0). **Scope:** `settings-fixture.html?host=user&page=shortcuts` showed 19 nav entries and **Vim mode** on `/rooms/` and `/chat/`; `page=appearance` rendered **Appearance**. In the shell, `Meta+/` opened **Grammar & shortcuts**, and `?view=settings` → **Log Out** opened alertdialog **Log Out** ("Are you sure you want to log out?"). **Limitations:** Page bodies beyond these, and the invite link, were not re-driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261029/r1/` (frames 16, 32, 58, 68).

**Previous record:** 2026-10-28 (nightly maintenance). **Product commit:** `2dd7aad1` (origin/main). **Scope:** `settings-fixture.html?host=user&page=shortcuts` showed 19 nav entries and the **Vim mode** switch; `page=appearance` rendered **Appearance** / **Advanced**; `page=agent-access` rendered Agent Settings, Agents, Devices and Recent Logbook. In the shell, `Meta+/` opened **Grammar & shortcuts**; **Log Out** opened alertdialog **Log Out** ("Are you sure you want to log out?") over **Settings**; Invites → **Create invite link** opened **Invite link settings** once the page had loaded (about 2 s; a 1.2 s wait missed the button). **Limitations:** Page bodies without a recipe, palettes, Webhooks conversion, real logout and `/chat/` were not re-driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261028/r1/` (frames 18, 33-34).

**Previous record:** 2026-10-27. **Product commit:** `6c15b0fb286e9dc1b6cb130c9c97cd7e0afa9254` (origin/main). **Scope:** `settings-fixture.html?host=user&page=shortcuts` showed 19 nav entries and the **Vim mode** switch; `page=agent-access` rendered without error. **Limitations:** The `vim` search, palettes, role-specific nav counts, Webhooks conversion, help pages and persisted preferences were not re-driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261027/r01/` (frame 24, 41). Previous record: 2026-10-26 at `5820fbea`.
