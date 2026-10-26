# OM Chat feature map

One file per user-facing feature. Each names the routes that reach it, the
handles that drive it, and the traps that have already cost someone a run.

This map is the repo's maintained verification source. **A proof that drives
one convenient entry point is incomplete when the file lists others.** If you
verify channel navigation from the sidebar and the file also lists the mobile
tab bar and the topic breadcrumb, either drive those too or say in the manifest
which you skipped and why.

Each file has the same four sections, in order:

1. **Sub-features** — what actually has to work, itemised.
2. **How to get to it (user POV)** — what a person does, in their words.
3. **Driving it with control-om-chat** — the routes and commands, with real
   accessible names from this repo.
4. **Gotchas** — what breaks, what lies, what the fixture cannot prove.

## Reaching the lane

Every snippet in these files opens its harness through the wrapper:

```bash
cd /Users/dboon/gitlab/openmarket-chat
export OM_CHAT_LANE_PORT=<your assigned 18097-18197 port>   # control-om-chat doctor
control-om-chat up
agent-browser open "$(control-om-chat url '<path>?<query>')"
```

`control-om-chat url` builds the origin from `OM_CHAT_LANE_PORT`, so nothing
here hardcodes a port. That matters more than it looks: lanes are assigned per
run, several worktrees drive at once, and a literal port copied out of a doc
lands you on **another run's app** — where everything renders and every frame
is evidence of the wrong tree.

## The three fixture entry points

The fixture lane serves three different harnesses. Using the wrong one is why a
query parameter "does nothing".

| File | Query vocabulary | Mounts |
|---|---|---|
| `tools/visual/shell-fixture.html` | `?view=`, `?panel=`, `?alerts=`, `?theme=`, … | The whole Shell — rail, sidebar, content, composer |
| `tools/visual/settings-fixture.html` | `?host=user\|server\|channel`, `?page=`, `?perms=`, `?state=`, `?mode=` | The settings surfaces |
| `tools/visual/fixture.html` | `?surface=` | A component gallery (KitchenSink, reactions, polls) |

One surface has a fourth, dedicated harness: the Open World tab, at
`mocks/world-solo/index.html?worldprobe=1`. See
[open-world.md](open-world.md) — it is not reachable through the shell fixture.

Two more standalone harnesses are real, and neither speaks the shell fixture's
grammar. `tools/visual/agent-center-fixture.html` renders the Agent Center's
consent queue with content; its vocabulary is only `state=desk-off`, `theme`
and `zoom` (see [om-and-agents.md](om-and-agents.md)).
`tools/visual/persona-panel-fixture.html` renders the persona panel (heading
**"Voice"**, a `Learning` section and a `switch` named **"Learn from my
messages"**) and takes `theme` plus `state`. Each of the four values below, plus
`pending-long`, lands a different journey (re-driven 2026-10-22 at `cd9f8c72`):

| Route | State |
|---|---|
| `persona-panel-fixture.html` | The voice card (`state=card` is the default): **Edit**, **View full profile**, **Saved profiles** and **Manage voice cards**, which expands to Advanced document / History / **Export card** / **Import a card** / **Create manually** |
| `persona-panel-fixture.html?state=awaiting` | "Set up how om sounds", with **Set up my voice now**, **Import a card** and **Create manually** |
| `persona-panel-fixture.html?state=proposed` | "Your first voice card", with a **Use this card** button |
| `persona-panel-fixture.html?state=pending` | Proposed changes, with **Show changes**, **Read all**, **Accept** and **Not now** |

The shell reaches the same surface at `?view=agent&panel=voice` (or `away`, or
`activity`) — note the **singular** `agent`. `#807` moved the fixture's gate
there, and `?view=agents&panel=persona` now only redirects, arriving after the
persona mock was skipped, so it renders a load failure. `?personaState=` seeds
that mock with `ready` (the default), `empty`, `setup`, `invalid`, `hold` or
`profiles`, and `?backend=real` with `?backendOrigin=<url>` points the persona
scene at a real daemon while everything else stays synthetic. See
[om-and-agents.md](om-and-agents.md).

Since product commit `f8b68bf7`, `tools/visual/agent-draft-share-fixture.html`
is another standalone harness. It mounts the real `AgentDraftDock` with one
loaded, unsent channel draft; editing it reveals **Share with agent**, and the
fixture records the shared revision locally. It does not post the message or
prove daemon delivery. See [agent-draft-sharing.md](agent-draft-sharing.md).

Four more in `tools/visual/` **are** driveable harnesses, and this file used to
imply they were not. Opened by hand on the lane, each comes up with real
content and no error:

- `away-panel-fixture.html` — the whole Away surface, standalone: "Persona /
  Voice / Away coverage / Activity", an `active` state, *"Research om is
  covering you"*, `1h 18m remaining · This Mac`, Refresh, ~20 controls. This is
  the **only** door into the om surface that works from this lane, since the
  shell fixture cannot get past the not-running gate
  ([om-and-agents.md](om-and-agents.md)).
- `compact-attachment-only-fixture.html` — the compact attachment-only row
  layout, with its own explanation of where the author lead-in sits.
- `poll-cache-fixture.html` — a poll with a `roster loads: N` counter, for the
  `#752` roster session cache.
- `poll-results-fixture.html` — the closed-poll results dialog, *"Final
  results · 14 votes"* with per-option percentages.

None of the four is referenced by any Playwright spec or any other file in the
repo, which is why they were mistaken for dead code. They are not dead; they
are undocumented, and each is a cheap proof for a surface with no feature file.

Four more came with the GitLab tree or were never indexed. Each was opened on
the lane at `f7d7c987` and rendered real content:

- `remote-home-fixture.html?state=snapshot|older|recovering|approval|live|empty|unsupported`
  — the away remote-control pane (`RemoteHome`), scripted with no relay or
  daemon. `approval` shows **Approve** / **Deny**, `live` shows **Stop** and
  **Add context**, and `unsupported` reads "Conversation history is not
  supported by this device". See [om-and-agents.md](om-and-agents.md).
- `agent-presentation-fixture.html?state=collapsed|expanded|live|failed` — the
  shared tool-activity disclosure both agent panes render. The toggle is
  "Expand tool activity" or "Collapse tool activity" by state.
- `agent-usage-fixture.html` — the token-usage summary; its recipe is
  [agent-token-usage.md](agent-token-usage.md).
- `dropdown-fixture.html` — every `MenuSelect` trigger shape and state, one
  board per `data-testid` (`board-shapes`, `dd-solid`, `dd-outline`, ...),
  read by `tools/visual/dropdown.visual.ts`.

Genuinely **not** driveable: `person-presence-fixture.html` and
`reaction-scene-fixture.tsx` are opened only by their Playwright visual specs,
and `chat-rendering-gallery.html` is a static mock nothing references. Opening
one of those expecting `?view=`-style behavior wastes a run.

`?view=` values on the shell fixture: `room` (default), `topics`, `topic`,
`required`, `public`, `dm`, `home`, `channels`, `friends`, `library`, `agent`,
`agents`, `empty`, `settings`, `server-settings`, `gif`.

`?view=gif` is the odd one out: it bypasses the Shell entirely and renders a
standalone GIF-sizing debug harness, so none of the normal chrome is there.

`settings` and `server-settings` are the other two exceptions: they open a
`dialog` named **"Settings"** *over* the room rather than replacing it, so the
`h1` stays `#ops` and the route stays `#/room/ops`. An agent that checks the
heading concludes the value is dead. Check for the dialog. `?view=settings`
takes a companion `?settingsPage=` (default `account`); the settings **fixture**
is still the better harness for settings work (see
[settings-and-appearance.md](settings-and-appearance.md)).

Common modifiers, all on the shell fixture: `alerts=quiet|board`,
`theme=dark|light`, `contrast=high`, `palette=slate|moss|warm|brass`,
`channels=many`, `bulk=<n>` (message count), `draft=<text>`, `peek=<topicId>`,
`inbox=open`, `message=cozy`, `text=200` (200% type), `keyboard=<px>`,
`width=stress`.

That list is the common set, not the whole vocabulary — the fixture reads
around sixty parameters. The ones worth knowing beyond the list:
`panel=search|library|topic-draft`, plus `voice|away|activity` which are gated
on `view=agent` (and `searchState=error`, which only renders
once `panel=search` has seeded a run — see
[search-and-filters.md](search-and-filters.md)), `lens=todos|agents` on
`view=library` (which routes to `#/library/todos` and `#/library/agents`),
`profile=1` for the profile panel, and `policy=required|off` for the channel's
topics policy (default `allowed`). When a parameter seems to do nothing, grep
`params.get(` in `tools/visual/shell-fixture.tsx` before concluding it is
dead — and check whether it needs a companion, the way `searchState` needs
`panel=search`.

Sixteen more exist and are documented in no feature file at all, most of them
state seeds worth knowing before you conclude a surface has no route:
`directory=empty`, `dmDisplay`, `dmmuted=1`, `docAccess=readonly`,
`docMode=history|edit`, `docState=reconcile|review|history`,
`fixtureState=loading`, `g1=spacer`, `homeImport=open`, `import=<phase>`,
`lateImage=1` with `lateImageDelay=<ms>`, `libraryState=error`, `links=1`,
`sealedAutoMove=1`, `sealedBusy=1`. None came in with the recent composer work
— they are older seams nobody wrote down. `#792` added one more,
`restore=fail-once`, which makes the first HOME history restore fail so the
retry path can be driven ([home-history-restore.md](home-history-restore.md)).

And sixteen more again, all pre-dating that commit, with what each seeds:
`approval=auto` and `lane=on` (fixture-only approval and lane state),
`capture=1` (a capture overlay — a real parameter, despite reading like the
screenshot guidance elsewhere in this file), `card=1` (a live cursor overlay),
`confirm=topics-only` (auto-opens a confirm dialog), `connection`,
`docs=500` (a 1337-doc library corpus), `failed=room|dm` (a failed-delivery
row), `history=detached` (topics start in detached history), `list=flat` (sets
a localStorage library-list mode — sticky with no companion to clear it, the
same shape as `message=cozy`), `note=long|wrapped` (bench doc variants),
`rail`, `requests=<n>`, `scope=server`, `status=<text>`, and `title=<slug>`
(overrides the room title, default `ops`).

Four more that a `params.get(` sweep finds and no feature file mentioned, all
pre-dating the recent churn:

- **`switcher=open`** (`shell-fixture.tsx:3026`) seeds the quick-switcher
  palette, and it really does mount — see
  [channel-and-topic-navigation.md](channel-and-topic-navigation.md), whose
  "nothing to drive here" note this parameter contradicts.
- **`reply=1`** (`:2342`) seeds a reply target, the entry at `seq === 103`.
- **`tape=lists`** (`:1317`) selects a mosaic-tape variant.
- **`perms=noupload`** (`:2834`) makes `canUploadServerWide` answer false on
  the **shell** fixture. Note this is a different parameter from the
  `?perms=owner` documented for `settings-fixture.html` in
  [settings-and-appearance.md](settings-and-appearance.md) — same spelling,
  different harness, different values. Remember that `canUploadServerWide` is
  cosmetic: the store enforces, so a false here dims a control rather than
  proving a denial.

**`message=cozy` is sticky, and nothing unsets it.** It writes
`om.chat.messageDisplay` to `localStorage` and the fixture has no `else` branch
to clear it, so every later load in that browser session stays cozy — including
the load you meant to capture as the default. A before/after comparison run in
one session therefore shows no difference and looks like a dead parameter.
Clear the key before capturing a default frame:

```bash
agent-browser eval 'localStorage.removeItem("om.chat.messageDisplay")'
```

Cozy is visible as `msg-identity-cozy` on a `[data-message-row]`; the default is
`msg-identity-chassis mt-2` without it. (The settings fixture's `contrast=high`
does clear itself — that asymmetry is why only this one bites.)

`?alerts=quiet` is worth reaching for by default: without it the fixture fires
an app-wide alert strip that shifts every surface below it down. The counts and
the board disagree, and both are fixture seeding: the beacon hardcodes **three**
ringing feeds (`Alerts: 3 feeds are ringing`) while the board renders the
**two** rows actually seeded (`af-store-5xx`, `af-relay-latency`). Do not report
that gap as a product bug, and do not caption a screenshot with the badge count.
Those two are seed **ids**, not rendered text, so grepping a snapshot for
`af-store-5xx` finds nothing and looks like the board failed to render. What
you will find is `store-5xx · check pods` — and that string comes from the
**strip**, which renders `name · actionLine` and is layered above the content,
not from the board's own row, which shows the bare name. Both are on screen
under `?alerts=board`; say which one a caption means.

## Who adds to this map

Two paths, and the first is the cheap one.

**A feature run**, when its terminal gate drives a surface no file covers. That
is the moment the handles are known and the proof is fresh, so writing the file
costs almost nothing. The feature playbooks require it before handing off.

**A maintenance pass**, sweeping recent churn for surfaces the map never heard
of. That works, but it rediscovers from source what a feature run already knew,
and pays a full live sweep to do it. `open-world.md` arrived this way.

## Files

- [channel-and-topic-navigation.md](channel-and-topic-navigation.md)
- [topic-cleanup.md](topic-cleanup.md)
- [mobile-shell-navigation.md](mobile-shell-navigation.md)
- [composer-and-sending.md](composer-and-sending.md)
- [direct-messages-and-home.md](direct-messages-and-home.md)
- [mermaid-message-rendering.md](mermaid-message-rendering.md)
- [settings-and-appearance.md](settings-and-appearance.md)
- [search-and-filters.md](search-and-filters.md)
- [om-and-agents.md](om-and-agents.md)
- [persona-setup-and-editing.md](persona-setup-and-editing.md)
- [home-history-restore.md](home-history-restore.md)
- [your-om-watches.md](your-om-watches.md)
- [your-om-drafts.md](your-om-drafts.md)
- [your-om-unread.md](your-om-unread.md)
- [open-world.md](open-world.md)
- [your-library.md](your-library.md)
- [agent-token-usage.md](agent-token-usage.md)
- [agent-draft-sharing.md](agent-draft-sharing.md)
- [message-editing.md](message-editing.md)
- [agent-creator.md](agent-creator.md) — **branch-only (MR !75, not on origin/main)**: local creation/import/sharing, native coding lifecycles, revocation/rollback. On main only the route-only record applies.
- [alerts.md](alerts.md) — alert strip, beacon, board and tape card.
- [polls-and-reactions.md](polls-and-reactions.md) — poll cards, results, roster cache, reactions, reactors and themed reaction scenes.
- [profiles.md](profiles.md) — the profile drawer, its section tabs and its header entry.

## Surface inventory

Source discovery: 2026-10-26, product tree `5820fbeaca9ded509b4369498f5946f32455c61a` (origin/main). The only product change since the 2026-10-23 pass (`afabb11c`) is `apps/cloud/Dockerfile.market` (`5820fbea`, a market sidecar base-image pin), so no route, screen, setting, fixture or shared UI source changed. This pass also took in a feature run's map notes (hub `fb489ac`) and added the branch-only hosted Voice/Away row below. The census reads the route parser (`src/lib/routing.ts`), Shell views and right panels, the settings navs, the mobile tab bar, the secondary components under `packages/chat-ui/src/components/`, the `apps/cloud` host and `desktop/`. It groups them into user outcomes, and its last full read was 2026-10-22 at `cd9f8c72`. "live verified <date>" means driven on the fixture lane on that date. It never means wire delivery. Rows re-driven this pass carry 2026-10-26, and rows not re-driven keep their earlier date. Pending rows keep their source path and prerequisite until proved or removed with source evidence.

| User outcome | Product source path | Existing guide / sub-feature | Live verification | Remaining prerequisite or gap |
|---|---|---|---|---|
| Move between channels and topics, and back | `packages/chat-ui/src/components/Sidebar.tsx`; `TopicListView.tsx`; `src/lib/routing.ts` | [channel-and-topic-navigation.md](channel-and-topic-navigation.md) | live verified 2026-10-26 | Topic peek pane and dock collapse toggle not driveable in the fixture. |
| Mark a channel or topic unread (`503a0a4f`) | `packages/chat-ui/src/lib/mark-latest-unread.ts`; `Sidebar.tsx:6209`; `TopicPill.tsx:389`; `ChannelHeaderMenus.tsx:141-147` | channel-and-topic-navigation.md / Mark As Unread | offer and gating live verified on `/rooms/` and `/chat/`; effect pending | `markUnreadFrom` / `markRoomRead` are fixture no-ops; the unread effect needs the daemon-pair lane. |
| Jump anywhere with the quick switcher | `packages/chat-ui/src/components/QuickSwitcher.tsx` | channel-and-topic-navigation.md / Gotchas (switcher) | live verified 2026-10-22 | Sidebar pill is inert; reach it with `?switcher=open`. |
| Open a message deep link or push tap (`#/room/<n>/msg/<seq>`) | `src/lib/routing.ts` | unmapped | live verification pending | The fixture never binds routing; needs the daemon-served rig. |
| Clean up quiet topics | `packages/chat-ui/src/components/TopicCleanupSheet.tsx`; `lib/topic-sweep-gate.ts` | [topic-cleanup.md](topic-cleanup.md) | menu absence and quiet seed live verified; sheet pending | Daemon build with topic triage; parity stack down. |
| Navigate on a phone | `packages/chat-ui/src/components/mobile/MobileTabBar.tsx`; `Shell.tsx` | [mobile-shell-navigation.md](mobile-shell-navigation.md) | live verified 2026-10-26 (390×844) | Other widths, Spaces detail, takeovers. |
| Compose and send; delivery recovery; sent drafts stay gone (`cd9f8c72`) | `packages/chat-ui/src/components/Composer.tsx`; `lib/session.ts` | [composer-and-sending.md](composer-and-sending.md) | local send live verified; delivery and draft durability pending | Daemon-pair lane (parity stack 4001/3002 down). |
| Type with Vim keys in the message box and doc editor (`b1ed7135`, `1aebc918`, `878049d8`) | `packages/chat-ui/src/components/Composer.tsx`; `lib/composer-vim.ts`; `lib/vim-mode.ts`; `editor/vim.ts`; `settings/UserSettings.tsx:1278-1296` | [composer-and-sending.md](composer-and-sending.md) / Vim mode; [your-library.md](your-library.md) / Doc editor Vim mode; [settings-and-appearance.md](settings-and-appearance.md) | setting, composer modes and send, reply Escape, doc `:q` live verified 2026-10-26 on `/rooms/`; composer and setting on `/chat/` 2026-10-23 | `:w` (the fixture's `session.docs` has no `publish`); touch suppression, IME, account pref sync. |
| Stage attachments, view attachment-only or sealed rows, open media and risky files | `Composer.tsx`; `AttachmentView.tsx`; `MediaGallery.tsx`; `DangerousDownloadDialog.tsx`; `tools/visual/compact-attachment-only-fixture.html` | composer-and-sending.md / Attachments (partial) | compact attachment-only fixture live verified; staging, lightbox and download pending | Staging needs `setInputFiles`; seeded room images were not in view; transport and cross-device delivery need the daemon lane. |
| Edit a message | `packages/chat-ui/src/components/InlineMessageEditor.tsx`; `MessageRow.tsx` | [message-editing.md](message-editing.md) | live verified 2026-10-26 (channel and DM) | Relay persistence. |
| See Mermaid diagrams and linked-message cards (`908855a1`) | `packages/chat-ui/src/components/Markdown.tsx`; `MessageText.tsx`; `lib/share-links.ts` | [mermaid-message-rendering.md](mermaid-message-rendering.md) | live verified on `/rooms/`; `/chat/` card without diagram | The `/chat/` fixture has no `mermaid=1` seed; the diagram cache (`2e1100a5`) is unit-tested only. |
| Land on Home and open DMs | `packages/chat-ui/src/shared/components/HomeHub.tsx`; `Shell.tsx` | [direct-messages-and-home.md](direct-messages-and-home.md) | live verified 2026-10-26 | Presence changes. |
| Manage connections and requests | `packages/chat-ui/src/components/FriendsPane.tsx` | direct-messages-and-home.md / Connections | requests live verified; blocked pending | `tab=blocked` crashes from fixture seeding (`blocks: []`). |
| Browse public channels, including empty, loading and offline | `packages/chat-ui/src/components/BrowseChannels.tsx` | direct-messages-and-home.md / routes table | live verified 2026-10-22 | Real catalog contents need a daemon. |
| Add people to or rename a group DM | `AddGroupMemberModal.tsx`; `RenameGroupDmModal.tsx` | unmapped | live verification pending | `?channels=groups` seeds the group list only; no add or rename dialog seed. |
| Search with scopes and filters | `packages/chat-ui/src/components/SearchPanel.tsx`; `SearchBar.tsx` | [search-and-filters.md](search-and-filters.md) | live verified 2026-10-26 | Date-filter submission, backend ranking, `/chat/`. |
| Change user, server and channel settings by role | `packages/chat-ui/src/components/settings/` | [settings-and-appearance.md](settings-and-appearance.md) | nav, appearance and permissions live verified | Help and guide pages and most page bodies not driven. |
| Convert webhooks to alerts | `settings/WebhooksPage.tsx`; `settings/ConvertWebhooksStepper.tsx` | settings-and-appearance.md / Webhooks | dialog live verified; effect pending | Conversion effects need the daemon. |
| Log out | `settings/UserSettings.tsx:211` | settings-and-appearance.md (nav entry only) | live verification pending | Confirm dialog and real logout need auth. |
| Set up and edit my voice | `packages/chat-ui/src/components/PersonaPanel.tsx`; `PersonaEditor.tsx` | [persona-setup-and-editing.md](persona-setup-and-editing.md) | live verified 2026-10-26 | Import and export files, learning, offline recovery. |
| Restore a HOME history version | `packages/chat-ui/src/lib/doc-checkpoint.ts`; `LibraryView.tsx` | [home-history-restore.md](home-history-restore.md) | live verified 2026-10-26 | Real HOME writes. |
| Review agent asks, the roster and badge pages | `AgentCenterPane.tsx`; `AgentCenterWork.tsx`; `settings/BadgeDetail.tsx` | [om-and-agents.md](om-and-agents.md) | fixture live verified 2026-10-26 | Authenticated roster actions need the daemon. |
| Use away and remote control, and approve from away | `AwayPanel.tsx`; `RemoteControlPane.tsx`; `tools/visual/remote-home-fixture.html` | om-and-agents.md / Remote control (away) | fixture states live verified; relay pending | Real relay or daemon history and approval delivery. |
| Inspect agent tool activity and token usage | `AgentPresentation.tsx`; `tools/visual/agent-usage-fixture.html` | [agent-token-usage.md](agent-token-usage.md) | live verified 2026-10-26 | Input+output fallback is not seedable; daemon accounting. |
| Share an agent draft revision | `AgentDraftDock.tsx` | [agent-draft-sharing.md](agent-draft-sharing.md) | live verified 2026-10-26 (fixture) | Daemon delivery. |
| Create, import, publish and run agents | branch `daryl/agent-creator-migration-20261007` only (`components/roster/`) | [agent-creator.md](agent-creator.md) (branch-only) | not on origin/main | Merge MR !75, then re-verify on main. |
| Use Voice and Away from the hosted `/chat/` app through the home daemon (Remote Control `operation` verb) | branch `daryl/cloud-persona-parity` only (`fb33a827`): `packages/chat-ui/src/lib/remote-operation.ts`; `apps/cloud/src/lib/{local-operation,away-client,daemon-operations,om-daemon}.ts`; `PersonaPanel.tsx`; `AwayPanel.tsx` | [persona-setup-and-editing.md](persona-setup-and-editing.md) / Hosted /chat/ over Remote Control; [om-and-agents.md](om-and-agents.md) (branch) | not on origin/main | Merge the branch after the relay, rooms-client 0.105.0 and daemon releases, then re-verify on main. The branch rig record (2026-10-23) is in the persona guide. |
| Keep om drafts per session, see unread om replies, manage watches | `AgentSessionRail.tsx`; `OmWatchesSurface.tsx` | [your-om-drafts.md](your-om-drafts.md); [your-om-unread.md](your-om-unread.md); [your-om-watches.md](your-om-watches.md) | live verification pending | Isolated daemon origin; the source route stops at "om isn't running". |
| Browse the Library panel, full page and lenses | `LibraryPanel.tsx`; `LibraryView.tsx` | [your-library.md](your-library.md) | live verified 2026-10-26; Agents lens crashes (fixture gap) | `lens=agents` crashes because the shell fixture never stubs `session.libraryDaemon`. `fetchPersona()` returns `INERT`, and `.tone` throws in `LibraryPersonaCard` (`LibraryView.tsx:6959`, `:6405`). |
| Import, export, file, trash and restore library documents | `packages/chat-ui/src/lib/doc-import.ts`; `doc-export.ts`; `doc-filing.ts`; `doc-trash.ts` | your-library.md (partial) | live verification pending | Session methods are INERT no-ops in the fixture; needs real persistence. |
| Select all inside the doc reader (`2a9df60c`) | `packages/chat-ui/src/components/DocPane.tsx` | your-library.md / Doc reader select-all | live verified 2026-10-22 | Native page select-all is not observable through `agent-browser press`. |
| Review doc proposals, reconcile and read history | `DocPane.tsx`; `DocProposals.tsx`; `DocReconcile.tsx` (fixture `docState=`, `docMode=`, `docAccess=`) | [your-library.md](your-library.md) / Doc pane states | reconcile, history and read-only live verified 2026-10-26; proposals pending | No fixture seed opens an agent proposal (`DocProposalInlineReview.tsx:248`); `docState=review` not driven. |
| Walk Open World | `packages/chat-ui/src/world/`; `mocks/world-solo/` | [open-world.md](open-world.md) | harness live verified 2026-10-26 (wrapper lane) | Movement, occupants and relay. |
| See and act on alerts | `AlertStrip.tsx`; `AlertsBeacon.tsx`; `AlertsBoard.tsx`; `AlertMessageRow.tsx`; `AlertsPage.tsx` | [alerts.md](alerts.md) | rendering live verified; claim, create and alerts home pending | Fixture no-ops; `#/alerts` has no fixture view. |
| Vote in polls and read results | `PollCard.tsx`; `PollComposer.tsx`; `PollResultsDialog.tsx` | [polls-and-reactions.md](polls-and-reactions.md) | rendering, roster cache and the local vote settle on `poll-ux` live verified 2026-10-26; persistence pending | Vote persistence needs the daemon-pair lane. |
| React and see who reacted | `ReactionRow.tsx`; `ReactorsDialog.tsx`; `EmojiPicker.tsx` | polls-and-reactions.md | dialogs live verified; toggle pending | Gallery toggles do not change counts. |
| See a themed scene when any emoji reaction rises (`afabb11c`) | `packages/chat-ui/src/lib/reaction-scene-themes.ts`; `components/reaction-scene-runner.ts`; `tools/visual/fixture.tsx` (`reaction-scene-integration`) | [polls-and-reactions.md](polls-and-reactions.md) / Reaction scenes | live verified 2026-10-26 on `/rooms/` (fall, shake, pulse); `/chat/` 2026-10-23 | Burst, rise and shimmer families; a scene from a real in-shell reaction. |
| Track to-dos, promote messages, react to to-do updates (`d919f889`) | `TodosPanel.tsx`; `TodoPromotePopover.tsx`; `TodoCreateDialog.tsx`; `MessageRow.tsx` | unmapped (only the `lens=todos` route is in your-library.md) | live verification pending | `?panel=todos` crashes with "Todos could not load" in TodoRow. The fixture's `members` seed (`shell-fixture.tsx:2325`) has no `role`, and `TodosPanel.tsx:154` calls `member.role.toLocaleLowerCase()`. That is a fixture gap; `todoPromote: null`; no to-do event seed; `fixture.html?surface=conversation-qol` renders the panel. |
| Open bookmarks, pins and members panels | `BookmarksPanel.tsx`; `RightPanels.tsx` | channel-and-topic-navigation.md / dock (partial) | dock buttons live verified; populated bookmarks pending | `bookmarks: []` stub. |
| Open profiles, popovers and user menus | `ProfilePanel.tsx`; `ProfilePopover.tsx`; `UserContextMenu.tsx` | [profiles.md](profiles.md) | drawer, tabs and Info content live verified 2026-10-26 | Name popover, user context menu, `?card=1`, tab contents beyond Info, real profile fetches. |
| Join voice and calls | `VoiceDock.tsx`; `LiveCallPill.tsx`; `IncomingCallCard.tsx` | unmapped | live verification pending | `voice: null` stub; LiveCallPill not found by name in KitchenSink. |
| Accept an invite link | `InviteLanding.tsx`; `InviteLinkDialog.tsx`; `src/lib/routing.ts` (`#invite/`) | unmapped | live verification pending | Auth and relay. |
| Forward a message | `ForwardModal.tsx` | unmapped | live verification pending | `forwardSource: null` stub. |
| Read the news home | `NewsHomePane.tsx`; `NewsCard.tsx`; `BriefChip.tsx` | unmapped | live verification pending | No fixture view; news store inert. |
| See chart, cashtag, unfurl and webhook cards | `ChartCard.tsx`; `CashtagPeek.tsx`; `UnfurlCard.tsx`; `WebhookEmbedBlock.tsx` | unmapped | live verification pending | No seeds; `cashtagPeek: null`. `3ca79795` made GIF unfurls render whole (`object-contain`) with no site blurb (`UnfurlCard.tsx:41-47`). Only `packages/chat-ui/test/ui/unfurl-cards.test.ts` covers it. |
| Resolve mirror conflicts and run recovery | `MirrorConflictStrip.tsx`; `RecoveryCeremonyDialog.tsx` | unmapped | live verification pending | `mirrorConflictFor` and `recoveryNudge` stubbed null. |
| Open the keyboard shortcuts modal | `ShortcutsModal.tsx` | settings-and-appearance.md (settings page only) | live verification pending | `shortcutsRequest: false` stub. |
| Sign in and boot the hosted `/chat/` app | `packages/chat-ui/src/components/Login.tsx`; `BootViews.tsx`; `apps/cloud/src/App.tsx`; `apps/cloud/src/lib/platform-auth.ts` | unmapped | live verification pending | Auth; hosted artifact (`bun run verify:cloud`). |
| Use the desktop shell: setup, updates, daemon recovery, deep links | `desktop/src/`; `DesktopAppSetup.tsx`; `DaemonRecovery.tsx`; `DesktopUpdateStrip.tsx` | unmapped | live verification pending | Electron via `bun run probe` / `smoke` only. |

Counts: 49 outcomes. 16 are fully live verified on the fixture lane, 16 partially verified (some sub-outcome still pending or failing), 15 pending and 2 branch-only (agent creator; hosted Voice/Away over Remote Control). This pass added the hosted Voice/Away row from the 2026-10-23 feature run and re-drove every mapped guide at `5820fbea`. No outcome changed status. 11 outcomes still have no guide (`unmapped`).
