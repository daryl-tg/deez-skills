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
consent queue with content. It takes `state=desk-off`, `theme=light`,
`zoom=200`, `connections=none`, `identity=anonymous` and, since `01bf4481`,
`roster=work-builder|work-proof|projects`, which mount the agent creator's
roster components over scripted `/rpc/v1/roster/*` routes. At `2dd7aad1` (rooms-client 0.107.0), as at `6c15b0fb`, only
`roster=work-builder&connections=none` loads cleanly; see
[agent-creator.md](agent-creator.md) and [om-and-agents.md](om-and-agents.md).
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
one of those expecting `?view=`-style behavior wastes a run. The same goes for
`painted-surfaces-calibration.html` (opened by `painted-surfaces.calibration.ts`)
and `theme-contrast-fixture.html` (opened by `theme-contrast.visual.ts`), which
no feature file uses.

**Two shell-fixture CSS gaps matter for visual claims.** Neither
`tools/visual/shell-fixture.tsx` nor its `/chat/` twin imports
`components/code-block.css` or `shared/alerts.css`; only the app entries do.
Code blocks and the alert strip and board therefore render unstyled there. See
[code-blocks.md](code-blocks.md) for the injection recipe and
[alerts.md](alerts.md).

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

Five more, found on 2026-10-27 and documented nowhere else: `dmTyping=peer`
(the DM counterparty is typing; also on `/chat/`), `showQuiet=1` (quiet topics
shown), and `contrastScene=1` with its companions `archive=1` and
`art=flat|failed` (the theme-contrast scene). `omSessions=drafts|daemon` is
covered in [om-and-agents.md](om-and-agents.md).

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

- **`switcher=open`** (`shell-fixture.tsx:3033`) seeds the quick-switcher
  palette, and it really does mount — see
  [channel-and-topic-navigation.md](channel-and-topic-navigation.md), whose
  "nothing to drive here" note this parameter contradicts.
- **`reply=1`** (`:2429`) seeds a reply target, the entry at `seq === 103`.
- **`tape=lists`** (`:1336`) selects a mosaic-tape variant.
- **`perms=noupload`** (`:2921`) makes `canUploadServerWide` answer false on
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
- [agent-creator.md](agent-creator.md) — local creation/import/sharing, native coding lifecycles, revocation/rollback. On origin/main since `01bf4481`; only the fixture form is re-verified on main, and the account-lane receipts are branch history.
- [alerts.md](alerts.md) — alert strip, beacon, board and tape card.
- [polls-and-reactions.md](polls-and-reactions.md) — poll cards, results, roster cache, reactions, reactors and themed reaction scenes.
- [profiles.md](profiles.md) — the profile drawer, its section tabs and its header entry.
- [code-blocks.md](code-blocks.md) — fenced code blocks in messages: wrapping, the copy control and the fixture stylesheet gap.

## Surface inventory

Source discovery: 2026-10-27, product tree `6c15b0fb286e9dc1b6cb130c9c97cd7e0afa9254` (origin/main), six commits past the 2026-10-26 pass (`5820fbea`). The churn: `01bf4481` landed the agent creator (MR !75, as a subset of its branch) and split about 1,100 lines of `styles.css` into per-component sheets; `2350a0fd` wraps chat code blocks; `2a737b9e` landed hosted Voice and Away over Remote Control; `cb3e5274` evens the topics primer; and `6c15b0fb` reworks video loading, CDN media variants, DM grants and transport-error copy. Six read-only readers re-read the route parser (`src/lib/routing.ts`), Shell views and right panels, the settings navs, the mobile tab bar, `components/roster/`, the secondary components under `packages/chat-ui/src/components/`, the `apps/cloud` host and `desktop/`, and audited every guide against the churn. Line citations across the map were remapped through the `5820fbea..6c15b0fb` diff, and four README citations that were already stale were corrected. "live verified <date>" means driven on the fixture lane on that date. It never means wire delivery. Rows re-driven this pass carry 2026-10-27, and rows not re-driven keep their earlier date. Pending rows keep their source path and prerequisite until proved or removed with source evidence.

Second pass, 2026-10-27 (scheduled maintenance, same tree `6c15b0fb`): an independent census read the route parser, Shell views, right panels, the settings navs, every `*Modal*`, `*Dialog*`, `*Sheet*`, `*Panel*`, `*Pane*`, `*Popover*` and `*Picker*` under `packages/chat-ui/src/components/`, `apps/cloud/src` and `desktop/src`. It added the thirteen outcomes at the bottom of the table. Every cited path still resolves. A seed reader and live drives moved eight pending rows to partial or full: deep link, group DM, log out, to-dos, invite link, shortcuts modal, GIF picker and import folder. The om gate is now passed reproducibly with an `agent-browser network route "**/healthz*"` stub (see [your-om-drafts.md](your-om-drafts.md)). Rows marked "2026-10-27 maintenance" were driven in this pass; evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261027/r1/`.

Nightly pass, 2026-10-28: product tree `2dd7aad1` (origin/main), five commits past `6c15b0fb`. `5e38077c` lets a bare `@` list the whole server. `52a968b3` names an agent post by its owner, with the persona beside it only when one was picked. `c70fdd28` adds approve-or-keep for a pending `@om-skills` update on the agent card and repins rooms-client to 0.107.0. `2dd7aad1` gives the agent card one switch, one primary action and a **More actions** menu. `2487c142` (Renovate config) is not user-facing. Three read-only readers covered the roster delta, the names and `@` delta, and a path and seed audit of every inventory row; every cited path resolves. Citations were remapped through the diff, and two new rows were added: bare `@` and the agent card. Every guide except your-om-unread was re-driven on `/rooms/` (18131), and the shared-code deltas on `/chat/` (18132). Seven pending rows moved to partial or full: inbox, Getting started, New DM, Create or join a server, Resolve, Invite agent and Add context. Rows marked 2026-10-28 were driven in this pass. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261028/r1/`.

| User outcome | Product source path | Existing guide / sub-feature | Live verification | Remaining prerequisite or gap |
|---|---|---|---|---|
| Move between channels and topics, and back | `packages/chat-ui/src/components/Sidebar.tsx`; `TopicListView.tsx`; `src/lib/routing.ts` | [channel-and-topic-navigation.md](channel-and-topic-navigation.md) | live verified 2026-10-28 (both hosts for the topic row menu) | Topic peek renders nothing on any `peek=` route (see the guide's Gotchas); dock collapse toggle not driveable in the fixture. |
| Mark a channel or topic unread (`503a0a4f`) | `packages/chat-ui/src/lib/mark-latest-unread.ts`; `Sidebar.tsx:6208`; `TopicPill.tsx:389`; `ChannelHeaderMenus.tsx:141-147` | channel-and-topic-navigation.md / Mark As Unread | offer re-verified 2026-10-28 on `/rooms/` and `/chat/` (topic row menu via a `contextmenu` on the row's inner button); effect pending | `markUnreadFrom` / `markRoomRead` are fixture no-ops; the unread effect needs the daemon-pair lane. |
| Jump anywhere with the quick switcher | `packages/chat-ui/src/components/QuickSwitcher.tsx` | channel-and-topic-navigation.md / Gotchas (switcher) | live verified 2026-10-28 | Sidebar pill is inert; reach it with `?switcher=open`. |
| Open a message deep link or push tap (`#/room/<n>/msg/<seq>`) | `src/lib/routing.ts` | channel-and-topic-navigation.md / Message deep link | fixture jump live verified 2026-10-28 (`#/room/ops/msg/105` at load, `/rooms/`); `/chat/` 2026-10-27 maintenance | Push-tap delivery and the unknown-seq toast need the daemon-served rig; the fixture only seeds a hash when it is empty. |
| Clean up quiet topics | `packages/chat-ui/src/components/TopicCleanupSheet.tsx`; `lib/topic-sweep-gate.ts` | [topic-cleanup.md](topic-cleanup.md) | menu absence and quiet seed live verified; sheet pending | Daemon build with topic triage; parity stack down. |
| Navigate on a phone | `packages/chat-ui/src/components/mobile/MobileTabBar.tsx`; `Shell.tsx` | [mobile-shell-navigation.md](mobile-shell-navigation.md) | live verified 2026-10-28 (390×844) | Other widths, Spaces detail, takeovers. |
| Compose and send; delivery recovery; sent drafts stay gone (`cd9f8c72`) | `packages/chat-ui/src/components/Composer.tsx`; `lib/session.ts` | [composer-and-sending.md](composer-and-sending.md) | local send live verified 2026-10-28; delivery and draft durability pending | Daemon-pair lane (parity stack 4001/3002 down). |
| Type with Vim keys in the message box and doc editor (`b1ed7135`, `1aebc918`, `878049d8`) | `packages/chat-ui/src/components/Composer.tsx`; `lib/composer-vim.ts`; `lib/vim-mode.ts`; `editor/vim.ts`; `settings/UserSettings.tsx:1278-1296` | [composer-and-sending.md](composer-and-sending.md) / Vim mode; [your-library.md](your-library.md) / Doc editor Vim mode; [settings-and-appearance.md](settings-and-appearance.md) | setting and composer modes live verified 2026-10-28 on `/rooms/`; reply Escape and doc `:q` 2026-10-26; `/chat/` 2026-10-23 | `:w` (the fixture's `session.docs` has no `publish`); touch suppression, IME, account pref sync. |
| Stage attachments, view attachment-only or sealed rows, open media and risky files | `Composer.tsx`; `AttachmentView.tsx`; `VideoAttachment.tsx`; `MediaGallery.tsx`; `lib/media-variants.ts`; `lib/dm-attachment-urls.ts`; `DangerousDownloadDialog.tsx`; `tools/visual/compact-attachment-only-fixture.html` | composer-and-sending.md / Attachments; sent video (partial) | compact attachment-only fixture live verified 2026-10-22; room video poster → player → file-card fallback live verified 2026-10-27; staging, lightbox, download, slow-link recovery, CDN variants and DM grants pending | The seeded `.mov` is an undecodable stub, so only the fallback ladder is observable. Seeded images (`?lateImage=1`, `?tape=mosaic5\|7`) are `data:` URLs, which variants never rewrite. Staging needs `setInputFiles`. Slow-link recovery (`6c15b0fb`), DM durable grants and the DM "Couldn't play here" card need real media and the daemon lane. |
| Edit a message | `packages/chat-ui/src/components/InlineMessageEditor.tsx`; `MessageRow.tsx` | [message-editing.md](message-editing.md) | channel path live verified 2026-10-28 (`/rooms/`); DM path 2026-10-27 maintenance, with no `edited` label rendered (open question in the guide) | Relay persistence. The `/chat/` fixture stubs `beginEdit` as a no-op, so `/chat/` editing needs a real host. |
| See Mermaid diagrams and linked-message cards (`908855a1`) | `packages/chat-ui/src/components/Markdown.tsx`; `MessageText.tsx`; `lib/share-links.ts` | [mermaid-message-rendering.md](mermaid-message-rendering.md) | PNG control live verified 2026-10-28; cards 2026-10-26 on `/rooms/`; `/chat/` card without diagram | The `/chat/` fixture has no `mermaid=1` seed; the diagram cache (`2e1100a5`) is unit-tested only. |
| Land on Home and open DMs | `packages/chat-ui/src/shared/components/HomeHub.tsx`; `Shell.tsx` | [direct-messages-and-home.md](direct-messages-and-home.md) | live verified 2026-10-28 | Presence changes. |
| Manage connections and requests | `packages/chat-ui/src/components/FriendsPane.tsx` | direct-messages-and-home.md / Connections | requests live verified; blocked pending | `tab=blocked` crashes from fixture seeding (`blocks: []`). |
| Browse public channels, including empty, loading and offline | `packages/chat-ui/src/components/BrowseChannels.tsx` | direct-messages-and-home.md / routes table | live verified 2026-10-22 | Real catalog contents need a daemon. |
| Add people to or rename a group DM | `AddGroupMemberModal.tsx`; `RenameGroupDmModal.tsx` | direct-messages-and-home.md / Group DM rename and add | dialogs live verified 2026-10-28 (`/rooms/`) | Rename and add are INERT no-ops; `/chat/` has no group DM seed. |
| Search with scopes and filters | `packages/chat-ui/src/components/SearchPanel.tsx`; `SearchBar.tsx` | [search-and-filters.md](search-and-filters.md) | live verified 2026-10-28 (topic search box only); scoped requests and the user filter 2026-10-26 | Date-filter submission, backend ranking, `/chat/`. |
| Change user, server and channel settings by role | `packages/chat-ui/src/components/settings/` | [settings-and-appearance.md](settings-and-appearance.md) | nav, Vim switch, appearance and agent-access pages live verified 2026-10-28; permissions 2026-10-26 | Help and guide pages and most page bodies not driven. Census 2026-10-27: Moderation, Integrations, Secrets, Slash commands, the guide pages, the import stepper, Work Ledger (`settings/WorkLedgerPage.tsx`) and library/draft recovery settings have no recipe. |
| Convert webhooks to alerts | `settings/WebhooksPage.tsx`; `settings/ConvertWebhooksStepper.tsx` | settings-and-appearance.md / Webhooks | dialog live verified; effect pending | Conversion effects need the daemon. |
| Log out | `settings/UserSettings.tsx:216` | settings-and-appearance.md / Log Out confirm | confirm alertdialog live verified 2026-10-28 (`/rooms/`); `/chat/` 2026-10-27 maintenance | Confirm is a fixture no-op (`shell-fixture.tsx:4513`); real logout needs auth. |
| Set up and edit my voice | `packages/chat-ui/src/components/PersonaPanel.tsx`; `PersonaEditor.tsx` | [persona-setup-and-editing.md](persona-setup-and-editing.md) | persona fixture states live verified 2026-10-28 | Import and export files, learning, offline recovery. |
| Restore a HOME history version | `packages/chat-ui/src/lib/doc-checkpoint.ts`; `LibraryView.tsx` | [home-history-restore.md](home-history-restore.md) | live verified 2026-10-28 | Real HOME writes. |
| Review agent asks, the roster and badge pages | `AgentCenterPane.tsx`; `AgentCenterWork.tsx`; `AgentBudgetNotice.tsx`; `settings/BadgeDetail.tsx`; `settings/AgentAccessPage.tsx` | [om-and-agents.md](om-and-agents.md) | fixture live verified 2026-10-28 | Authenticated roster actions need the daemon. The `userFacingErrorText` toast copy (`6c15b0fb`) fires only on injected failures, so it is source-only. |
| Use away and remote control, and approve from away | `AwayPanel.tsx`; `RemoteControlPane.tsx`; `tools/visual/remote-home-fixture.html` | om-and-agents.md / Remote control (away) | fixture states live verified 2026-10-28; relay pending | Real relay or daemon history and approval delivery. |
| Inspect agent tool activity and token usage | `AgentPresentation.tsx`; `tools/visual/agent-usage-fixture.html` | [agent-token-usage.md](agent-token-usage.md) | live verified 2026-10-28 | Input+output fallback is not seedable; daemon accounting. |
| Share an agent draft revision | `AgentDraftDock.tsx` | [agent-draft-sharing.md](agent-draft-sharing.md) | live verified 2026-10-28 (fixture) | Daemon delivery. |
| Create, import, publish and run agents | `packages/chat-ui/src/components/AgentCenterSurface.tsx`; `components/roster/`; `lib/roster-*.ts`; `tools/visual/agent-center-fixture.tsx` (on main since `01bf4481`) | [agent-creator.md](agent-creator.md) | no-provider form, work-agent gating and the roster load failures live verified 2026-10-28 (fixture); review, Try, Add, import, catalog, publish/adopt and work pending | An authenticated daemon lane. Three `agent-center-fixture` roster states fail to load against rooms-client 0.106.0 and still 0.107.0 (fixture gap, see the guide). The branch's 10 extra commits (tip `a0916a25`) are not on main. |
| Use Voice and Away from the hosted `/chat/` app through the home daemon (Remote Control `operation` verb) | `packages/chat-ui/src/lib/remote-operation.ts`; `lib/remote-operator-registry.ts`; `lib/remote-unavailable.ts`; `apps/cloud/src/lib/{local-operation,away-client,daemon-operations,om-daemon}.ts`; `PersonaPanel.tsx`; `AwayPanel.tsx` (on main since `2a737b9e`) | [persona-setup-and-editing.md](persona-setup-and-editing.md) / Hosted /chat/ over Remote Control; [om-and-agents.md](om-and-agents.md) | desk-offline Voice and Away live verified 2026-10-27 on the `/chat/` fixture; the other states and real operations pending | A relay and a home daemon that speak the `operation` verb (the 2026-10-23 branch rig), or a registered operator stub for the off/outdated/busy/no-answer states. |
| Keep om drafts per session, see unread om replies, manage watches | `AgentSessionRail.tsx`; `OmWatchesSurface.tsx` | [your-om-drafts.md](your-om-drafts.md); [your-om-unread.md](your-om-unread.md); [your-om-watches.md](your-om-watches.md) | drafts A/B and New session live verified 2026-10-28 with the `**/healthz*` route stub; Watches mount and fires error branch only (390 px, 2026-10-28); 390 px drawer 2026-10-27 maintenance; unread pending | Watch rows, actions and unread need a daemon origin with a real AgentRuntime and QA watches; the stub answers health only. New-session send lands in the open session (fixture gap). |
| Browse the Library panel, full page and lenses | `LibraryPanel.tsx`; `LibraryView.tsx` | [your-library.md](your-library.md) | live verified 2026-10-28 (`lens=todos`, panel mount); full page and panel filter 2026-10-26; Agents lens crashes (fixture gap) | `lens=agents` crashes because the shell fixture never stubs `session.libraryDaemon`. `fetchPersona()` returns `INERT`, and `.tone` throws in `LibraryPersonaCard` (`LibraryView.tsx:6959`, `:6405`). |
| Import, export, file, trash and restore library documents | `packages/chat-ui/src/lib/doc-import.ts`; `doc-export.ts`; `doc-filing.ts`; `doc-trash.ts`; `ImportFolderModal.tsx`; `DocImportModal.tsx`; `ShareDocModal.tsx`; `Modals.tsx` (`BulkDocMoveModal`, `RefileIntoPrivateModal`) | your-library.md / Import folder (partial) | Import folder dialog live verified 2026-10-28 on `/rooms/`; the rest pending | Session methods are INERT no-ops; share modal has no seed; `homeImport=open` showed no dialog on `/chat/`. |
| Select all inside the doc reader (`2a9df60c`) | `packages/chat-ui/src/components/DocPane.tsx` | your-library.md / Doc reader select-all | live verified 2026-10-22 | Native page select-all is not observable through `agent-browser press`. |
| Review doc proposals, reconcile and read history | `DocPane.tsx`; `DocProposals.tsx`; `DocReconcile.tsx` (fixture `docState=`, `docMode=`, `docAccess=`) | [your-library.md](your-library.md) / Doc pane states | history live verified 2026-10-28; reconcile and read-only 2026-10-26; proposals pending | No fixture seed opens an agent proposal (`DocProposalInlineReview.tsx:248`); `docState=review` not driven. |
| Walk Open World | `packages/chat-ui/src/world/`; `mocks/world-solo/` | [open-world.md](open-world.md) | harness live verified 2026-10-28 (wrapper lane) | Movement, occupants and relay. |
| See and act on alerts | `AlertStrip.tsx`; `AlertsBeacon.tsx`; `AlertsBoard.tsx`; `AlertMessageRow.tsx`; `AlertsPage.tsx` | [alerts.md](alerts.md) | rendering live verified 2026-10-28; claim, create and alerts home pending | Fixture no-ops; `#/alerts` has no fixture view. The shell fixture never imports `shared/alerts.css`, so the strip and board are unstyled there. |
| Vote in polls and read results | `PollCard.tsx`; `PollComposer.tsx`; `PollResultsDialog.tsx` | [polls-and-reactions.md](polls-and-reactions.md) | results, roster cache and the local `poll-ux` vote settle live verified 2026-10-28 | Vote persistence needs the daemon-pair lane. |
| React and see who reacted | `ReactionRow.tsx`; `ReactorsDialog.tsx`; `EmojiPicker.tsx` | polls-and-reactions.md | reactors dialog and emoji picker live verified 2026-10-28; toggle pending | Gallery toggles do not change counts. The lazy-surface failure state (**Try again**) and the loading/truncated/unavailable reactor rows have no fixture seed. |
| See a themed scene when any emoji reaction rises (`afabb11c`) | `packages/chat-ui/src/lib/reaction-scene-themes.ts`; `components/reaction-scene-runner.ts`; `tools/visual/fixture.tsx` (`reaction-scene-integration`) | [polls-and-reactions.md](polls-and-reactions.md) / Reaction scenes | live verified 2026-10-27 maintenance on `/rooms/` (fall, shake, pulse); `/chat/` 2026-10-23 | Burst, rise and shimmer families; a scene from a real in-shell reaction. |
| Track to-dos, promote messages, react to to-do updates (`d919f889`) | `TodosPanel.tsx`; `TodoPromotePopover.tsx`; `TodoCreateDialog.tsx`; `MessageRow.tsx` | your-library.md / To-dos panel | panel live verified 2026-10-28 on `fixture.html?surface=conversation-qol`; shell `?panel=todos` crashes | Shell `members` seed lacks `role` (`TodosPanel.tsx:154`), so `?panel=todos` shows the lazy-surface error on both hosts; `todoPromote: null`; no to-do event seed. |
| Open bookmarks, pins and members panels | `BookmarksPanel.tsx`; `RightPanels.tsx` | channel-and-topic-navigation.md / dock (partial) | dock buttons live verified; populated bookmarks pending | `bookmarks: []` stub. |
| Open profiles, popovers and user menus | `ProfilePanel.tsx`; `ProfilePopover.tsx`; `UserContextMenu.tsx` | [profiles.md](profiles.md) | drawer and tabs live verified 2026-10-28; seeded degraded agent post live verified 2026-10-28 on both hosts | Name popover, user context menu, `?card=1`, tab contents beyond Info and real profile fetches. Agent names now read `<owner> · <persona>` (`DisplayName.tsx:52-158`, `52a968b3`); the fixture's only agent post (`#ops` seq 191) has a degraded handle and renders the owner-only form, so the persona form is unit-test only. |
| Join voice and calls | `VoiceDock.tsx`; `LiveCallPill.tsx`; `IncomingCallCard.tsx` | unmapped | live verification pending | `voice: null` stub; LiveCallPill not found by name in KitchenSink. |
| Accept an invite link | `InviteLanding.tsx`; `InviteLinkDialog.tsx`; `src/lib/routing.ts` (`#invite/`); `settings/` Invites page | settings-and-appearance.md / Invite link (dialog only) | invite-link settings dialog live verified 2026-10-27 maintenance; landing pending | `InviteLanding` is mounted only by `src/App.tsx:738` (no harness); accepting needs auth and relay. |
| Forward a message | `ForwardModal.tsx` | unmapped | live verification pending | `forwardSource: null` stub. |
| Read the news home | `NewsHomePane.tsx`; `NewsCard.tsx`; `BriefChip.tsx` | unmapped | live verification pending | No fixture view; news store inert. |
| See chart, cashtag, unfurl and webhook cards | `ChartCard.tsx`; `CashtagPeek.tsx`; `UnfurlCard.tsx`; `WebhookEmbedBlock.tsx` | unmapped | live verification pending | No seeds; `cashtagPeek: null`. `3ca79795` made GIF unfurls render whole (`object-contain`) with no site blurb (`UnfurlCard.tsx:41-47`). Only `packages/chat-ui/test/ui/unfurl-cards.test.ts` covers it. |
| Resolve mirror conflicts and run recovery | `MirrorConflictStrip.tsx`; `RecoveryCeremonyDialog.tsx` | unmapped | live verification pending | `mirrorConflictFor` and `recoveryNudge` stubbed null. |
| Open the keyboard shortcuts modal | `ShortcutsModal.tsx` | settings-and-appearance.md / Shortcuts modal | live verified 2026-10-28 (`Meta+/`, `/rooms/`); `/chat/` 2026-10-27 maintenance | `/help` request path (`shortcutsRequest: false`) not driven. |
| Sign in and boot the hosted `/chat/` app | `packages/chat-ui/src/components/Login.tsx`; `BootViews.tsx`; `apps/cloud/src/App.tsx`; `apps/cloud/src/lib/platform-auth.ts` | unmapped | live verification pending | Auth; hosted artifact (`bun run verify:cloud`). |
| Use the desktop shell: setup, updates, daemon recovery, deep links | `desktop/src/` (incl. `tray.ts`, `menu.ts`, `permissions.ts`); `DesktopAppSetup.tsx`; `DaemonRecovery.tsx`; `DesktopUpdateStrip.tsx` | unmapped | live verification pending | Electron via `bun run probe` / `smoke` only. |
| Read the topics primer and dismiss it (`cb3e5274`) | `packages/chat-ui/src/components/TopicListView.tsx:214`; `styles.css` (`.topic-primer`) | [channel-and-topic-navigation.md](channel-and-topic-navigation.md) / topics primer | live verified 2026-10-28 on `/rooms/` (12 px padding); 390 and `/chat/` 2026-10-27 | **New topic** from the primer was not driven. |
| Read and copy code blocks in chat (`2350a0fd`) | `packages/chat-ui/src/components/code-block.css`; `Markdown.tsx:2331` | [code-blocks.md](code-blocks.md) | live verified 2026-10-28 with the stylesheet injected (`/rooms/` send at 1440 and 390); `/chat/` seed 2026-10-27 | Neither shell fixture imports `code-block.css`; the clipboard write and the document reader's horizontal scroll were not driven. |
| Mention agents from the composer and act on agent replies (roster-gated, `01bf4481`) | `packages/chat-ui/src/lib/composer-complete.ts:467-524`; `ComposerAutocomplete.tsx`; `roster/RosterEngagementChip.tsx`; `roster/reply-actions.ts`; `ChatPane.tsx` (agent grouping) | composer-and-sending.md / Agents in the `@` menu (source) | live verification pending | No fixture reports roster support (om health roster capabilities), so the agent rows, the engagement chip and the agent reply actions never render. |
| See every member and role on a bare `@` (`5e38077c`) | `packages/chat-ui/src/lib/composer-complete.ts:416`, `:465-472`; `ComposerAutocomplete.tsx:58-61`, `:145-146` | [composer-and-sending.md](composer-and-sending.md) / bare `@` | live verified 2026-10-28 on `/rooms/` and `/chat/` (13 options: 5 members, 8 roles; the old budget showed 10) | OpenScape chat still passes a 20-row budget (`world/WorldChatPane.tsx:183`); not driven there. |
| Run, try and tune an agent from its roster card; approve or keep a pending `@om-skills` update (`2dd7aad1`, `c70fdd28`) | `packages/chat-ui/src/components/roster/RosterShelf.tsx`; `roster/RosterUpdateNotice.tsx`; `AgentCenterSurface.tsx:427`; `shared/ui/Menu.tsx` | [agent-creator.md](agent-creator.md) / agent card and update notice (source) | live verification pending | No fixture renders `RosterShelf`: `agent-center-fixture` mounts `AgentCenterPane` with its own roster section, scripts no `/rpc/v1/roster/instances` and seeds no `pendingUpdate`. Needs an authenticated daemon lane with an installed agent (and a pending update). |
| Retry a lazy surface that failed to load | `packages/chat-ui/src/components/LazySurface.tsx:530-553`; `lazy-surfaces.tsx`; `lib/retryable-loader.ts` | polls-and-reactions.md / Lazy pickers (loading state only) | loading anchor live verified 2026-10-27; failure state (**Todos could not load**, **Try again**, **Reload OM Chat**) live verified 2026-10-28 via shell `?panel=todos` | The failure is a fixture render throw, so retry re-throws; a real chunk-load failure needs a blocked import. |
| Pick a GIF | `packages/chat-ui/src/components/GifPicker.tsx`; `GifCard.tsx`; `tools/visual/shell-fixture.tsx` (`?view=gif`) | composer-and-sending.md / GIF picker | picker live verified 2026-10-28 (`/rooms/`); `/chat/` and `?view=gif` 2026-10-27 maintenance | KLIPY trending/search call the network (empty offline); sending a GIF is pending. |
| See who is typing in a DM | `tools/visual/shell-fixture.tsx` (`dmTyping=peer`); DM typing roster | unmapped | live verification pending | Source says the seed is stale: `?view=dm&dmTyping=peer` sets `DmState.typing` (`shell-fixture.tsx:2029`), but `typing` left `DmState` (`lib/ephemeral-seam.ts:18`) and the strip now reads `session.ephemeral.typistsFor` (`Composer.tsx:1438`), which the fixture never stubs. Not driven; needs an `ephemeral` stub. |
| Create or join a server; create a channel, topic or doc; archive; share a room code | `packages/chat-ui/src/components/Modals.tsx` (`CreateOrJoinServerModal` :119, `CreateTopicModal` :370, `CreateChannelModal` :1066, `InviteModal` :1307, `RoomCodeModal` :1397, `NewDocModal` :1499, `ArchiveModal` :1685); `ServerMenu.tsx` | [direct-messages-and-home.md](direct-messages-and-home.md) / Create or join a server | **Create or Join a Server** dialog and its **Create your server** step live verified 2026-10-28 (both hosts); creation and the channel, topic, doc, archive and room-code modals pending | Reach the dialog from the rail button **Create or join a server**. The channel (`Sidebar.tsx:4846`), topic (`Sidebar.tsx:6167`) and doc (`LibraryPanel.tsx:1984`) entry points were not driven, and creation needs the daemon-pair lane. |
| Set or edit my display name | `Modals.tsx` (`NamePromptModal` :162, `NameEditModal` :691, `DisplayNameAskModal` :911) | unmapped | live verification pending | No seed found. |
| Start a new DM or group message | `NewDmModal.tsx`; `NewMessageModal.tsx` | [direct-messages-and-home.md](direct-messages-and-home.md) / New DM | Home **New DM** → **New Message** dialog live verified 2026-10-28 (both hosts); sending pending | Shell mounts `NewMessageModal` (`Shell.tsx:4459`); the sidebar **New message** button (`Sidebar.tsx:4676`) was not found by name on `?view=room`; starting a DM needs the daemon-pair lane. |
| Peek at a channel, DM or topic before opening it | `ChannelPeekPopover.tsx`; `DmPeekPopover.tsx`; `TopicPeekPane.tsx`; fixture `peekDm`/`peekChannel` stubs (`shell-fixture.tsx:2702`, `:2826`) | unmapped | live verification pending | `?view=room\|topics` with `peek=cpi-print-aug`, with and without `topics=on`, rendered no peek on 2026-10-28, although both mounts exist (`RightPanels.tsx:293-300`, `Shell.tsx:4213-4221`) and the fixture sets `topicPeek`; not traced (see channel-and-topic-navigation.md Gotchas). DM and channel hover popovers were not attempted. |
| Start a topic from the New topic pane | `TopicDraftPane.tsx`; `RightPanels.tsx:416`; fixture `panel=topic-draft` (`shell-fixture.tsx:3060`) | channel-and-topic-navigation.md / New topic pane | pane mount live verified 2026-10-27 maintenance | Creating the topic not driven; `tools/visual/topic-draft.visual.ts` covers it visually. |
| Resolve a topic or add people to it | `TopicResolvePopover.tsx`; `TopicAddPeoplePopover.tsx`; `TopicCard.tsx` | [channel-and-topic-navigation.md](channel-and-topic-navigation.md) / Topic inbox panel and Resolve | **Resolve <topic>** dialog live verified 2026-10-28 from the sidebar topic row menu (both hosts); add people pending | **Resolve Topic** was not pressed (the fixture's resolve is local). **Add People...** has no route: the fixture sets `topicAddPicker: null` (`shell-fixture.tsx:3301`). |
| Invite an agent to a channel and see the channel's agents | `InviteAgentModal.tsx`; `ChannelAgentsPanel.tsx:51`; `ChannelHeaderMenus.tsx` | [om-and-agents.md](om-and-agents.md) / Invite an agent to a channel | **Invite your agent to #ops** no-badge dialog live verified 2026-10-28 (both hosts); channel agents panel pending | The wired-badge state and `ChannelAgentsPanel` need a daemon with a wired badge. |
| Approve an agent's in-channel access request; warn before mentioning an agent that cannot see the room | `AgentConsentCard.tsx`; `MentionWarnDialog.tsx` | unmapped | live verification pending | `?approval=ask\|auto` (`shell-fixture.tsx:2434`) seeds the approval mode only. |
| Open a canvas doc in the right panel | `CanvasPane.tsx:48`; `RightPanels.tsx` (`kind === "doc"`) | unmapped | live verification pending | No seed. |
| Add context to an om message | `OmComposerContextPopover.tsx:41`; `UploadMenu.tsx`; `ComposerAttachmentCard.tsx` | [your-om-drafts.md](your-om-drafts.md) / Add context | **Add context** menu and the **Link a channel** picker live verified 2026-10-28 on `/rooms/` with the `/healthz*` stub | Picking a doc, channel or topic and sending with context were not driven; `/chat/` not driven. |
| Use the settings pages that have no recipe: privacy, sealed messages, notifications and audio, accessibility, docs, draft recovery, the guides; server roles, access, moderation, integrations | `settings/UserSettings.tsx:134-216`; `settings/ServerSettings.tsx`; `settings/ChannelSettings.tsx`; `NotificationSettings.tsx`; `AudioSettings.tsx` | settings-and-appearance.md (nav only) | live verification pending | Reachable with `?view=settings\|server-settings&settingsPage=<id>` (`shell-fixture.tsx:2441-2444`) or the settings fixture; page bodies not driven; tones and audio have no test seed. |
| Catch up from the inbox panel | `RightPanels.tsx:381`; `TopicCatchUp` (fixture `inbox=open`, `shell-fixture.tsx:2439`, `:4514`) | [channel-and-topic-navigation.md](channel-and-topic-navigation.md) / Topic inbox panel | panel live verified 2026-10-28 via `?panel=inbox` (both hosts); mark-read effects pending | `?inbox=open` and the **Inbox: 9 unread** button only flip `session.inboxOpen` (`shell-fixture.tsx:3117-3119`, `:3419`); `TopicCatchUp` renders nothing. Mark-read and the next-unread walk need the daemon-pair lane. |
| See the Getting started checklist and the Start here card | `packages/chat-ui/src/shared/components/GettingStarted.tsx`; `HomeHub.tsx:620-624`; `BrowseChannels.tsx:432` ("Start here") | [direct-messages-and-home.md](direct-messages-and-home.md) / Getting started | checklist live verified 2026-10-28 with the `om.chat.gettingStarted` `{enrolled:true}` localStorage seed (both hosts); Start here pending | Start here shows only on a first run with no subscribed channels (`BrowseChannels.tsx:257`, `:269`); `WelcomeToChat` needs zero spaces (`HomeHub.tsx:612`). No fixture seed gives either. |

Counts: 70 outcomes. 29 are fully live verified on the fixture lane, 26 are partly verified (the status cell names a sub-outcome that is still pending, crashing or failing) and 15 are pending. 12 have no guide (`unmapped`). Tonight's tally counts each row by its status cell, which may differ from earlier hand counts. The 2026-10-28 pass added 2 outcomes, the bare `@` (full) and the roster agent card (pending), and moved 7 rows out of pending and out of `unmapped`. The product delta was 5 commits (`6c15b0fb..2dd7aad1`).
