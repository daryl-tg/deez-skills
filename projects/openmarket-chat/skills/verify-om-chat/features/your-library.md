# Your Library

Notes that live with the conversation. The Library is **two surfaces sharing
one name**, and conflating them is the most common way a Library proof goes
wrong:

- **`LibraryPanel.tsx`** — the docked right-rail panel, filter box and scope
  switch, reached with `?panel=library`. Fixture-complete: nearly everything
  here drives.
- **`LibraryView.tsx`** — the full-page **Your Library** at `?view=library`,
  with its four lenses. Reachable, but its newest lens is a stub away from
  being provable (see Gotchas).

They are not two renderings of one component and they do not share controls.
Say which one a frame shows, always.

## Sub-features

### The docked panel (`?panel=library`)

- **Filter box**: `input[aria-label="Search Library docs"]`
  (`data-library-filter`), placeholder `Search docs...`.
- **Match count**: a `role="status"` element (`data-library-filter-count`).
  The string carries the query in curly quotes, and a settling suffix:
  `1 note matches “a”` / `2 notes match “a”`, plus `" so far"` while the shelf
  has not settled (`LibraryPanel.tsx:2032-2033`). Measured live as
  `2 notes match “a”` — an `--exact` match on a bare `"2 notes match"` misses.
- **Clear control**: `button[aria-label="Clear search"]`
  (`data-library-filter-clear`), rendered **only when the field is non-empty**.
  Absent on a fresh panel; that is the control working, not a regression.
- **Scope switch**: `role="tablist"` named **"Library scope"**
  (`LibraryPanel.tsx:2041-2042`, `data-library-scope-switch`) with two tabs.
  The server tab (`data-library-scope-server`, `:2103`) is named **"Server"**,
  deliberately not "Server library", to disambiguate from the rail's own
  Library door. Accessible names carry counts: `Server · 3 notes`.
- **Expand / collapse**: `button[aria-label="Open Library full page"]`, which
  becomes `"Collapse Library to side panel"` (`LibraryPanel.tsx:1941-1942`).
  The cheap DOM check is `data-library-presentation` on the panel root
  (`:1810`), which flips `side` → `full`.

### The full page (`?view=library`)

Four sidebar lenses, each stamped `data-home-library-lens-{id}` and carrying
`aria-current="page"` when active: **Todos** (`?lens=todos`), **Shared docs**,
**Agents** (`?lens=agents`), and **Archive** (`?lens=archive`). All four are
present in this lane; Archive is the newest. **`?lens=agents` renders on both
hosts since `e7c375ce`.** It crashed on `/rooms/` through 2026-11-03 ("Your
Library could not load", `TypeError … reading 'tone'` in `LibraryPersonaCard`):
the shell fixture never stubs `session.libraryDaemon`, so the autofill proxy
answers `INERT` (`shell-fixture.tsx:2553-2558`), `LibraryView.tsx:6972` takes the
`ready` branch, and `personaStatusPresentation` matched no state. It now has a
`default` branch, "Unknown status" (`LibraryView.tsx:6169-6201`), and the
production client no longer rejects unlisted states (`src/lib/om-daemon.ts:1393`
checks only that `state` is a string). Driven 2026-11-04 at `ce14d4ba`:
`/rooms/` `?view=library&lens=agents` reaches `#/library/agents` with h1
**Agents**, the access text "Read access lets an agent inspect notes and queue
proposals…", **Open Front Desk**, the **Agent persona note** card with **Sync
now** and **LAST SYNC Unknown status**, and the **Living daily note** card.
"Unknown status" is the fixture's `INERT` report, not a real persona state; a
real state needs `backend=real`. On `/chat/` the same route reaches
`/chat/library/agents` with the same access text.

Archive renders `data-home-library-archive` (`LibraryView.tsx:8728`) with an
"Archived" heading, a **Refresh** button, and per-row **Restore** buttons on
`data-home-archived-doc={docId}` (`:8778`).
- Import a folder into Your Library (`ImportFolderModal.tsx`; `homeImport=open`), and the conversation To-dos panel (`TodosPanel.tsx`).

## How to get to it (user POV)

Open a channel and the Library is the rail panel beside it — the notes for
this channel, or for the whole server if you flip the scope. Type to narrow
them. If you want the whole vault instead, expand it to a full page, where
your to-dos, shared docs, agent notes and the archive each get a lens.

## Driving it with control-om-chat

The panel half is the fixture-complete one. Start there:

```bash
export AGENT_BROWSER_SESSION=verify-library
agent-browser set viewport 1440 900
agent-browser open "$(control-om-chat url \
  'tools/visual/shell-fixture.html?view=room&alerts=quiet&panel=library&scope=server')"
```

`?scope=server` selects the server tab at boot (`shell-fixture.tsx:230`). A
five-observation proof, each step verified live on lane 18116:

```bash
# 1. panel up, server scope selected, no clear control yet
agent-browser eval '(()=>document.querySelector("[data-library-presentation]").dataset.libraryPresentation)()'
#   "side"

# 2. type into the filter, then read the status line
agent-browser eval '(()=>document.querySelector("[data-library-filter-count]")?.textContent)()'
#   "2 notes match “a”"     <- curly quotes, query included

# 3. the clear control appears only now
agent-browser eval '(()=>document.querySelector("[data-library-filter-clear]")?.getAttribute("aria-label"))()'
#   "Clear search"

# 4. expand
agent-browser eval '(()=>document.querySelector("[data-library-presentation]").dataset.libraryPresentation)()'
#   "full"

# 5. browser Back collapses it WITHOUT a route change
agent-browser eval '(()=>JSON.stringify([document.querySelector("[data-library-presentation]").dataset.libraryPresentation, location.hash]))()'
#   ["side","#/room/ops"]
```

Step 5 is the one worth keeping. `#837` made Back collapse the expanded panel
through a same-URL `pushState`/`popstate` pair, so the hash is **unchanged**
across the collapse. A proof that asserts on the route will see nothing happen
and call it broken; assert on `data-library-presentation`.

Other seeding routes confirmed present in the fixture: `?docs=500` (a
1337-doc corpus, `shell-fixture.tsx:285`), `?list=flat` (**not sticky** — it
writes `localStorage["om.chat.libraryList"]` and the `else` branch at
`:134-135` removes it, so the next load without the parameter clears it;
measured live: `flat`, then `null`), `?note=long|wrapped`, and
`?libraryState=error` (`:4210`, applied only while the active view is library).

### Import folder and the To-dos panel (added 2026-10-27)

- **Import folder:** `shell-fixture.html?view=home&alerts=quiet&homeImport=open` opens dialog **Import folder into Your Library** on `/rooms/`. On `/chat/` the same URL showed no dialog. `import=<phase>` (`shell-fixture.tsx:4159`) seeds later phases, which were not driven.
- **To-dos panel:** the shell's `?panel=todos` crashes into the lazy-surface error **Todos could not load** with **Try again** and **Reload OM Chat** (`[data-lazy-surface-error="Todos"]`) on both hosts. The roster `members` seed has no `role`, and `TodosPanel.tsx:154` calls `member.role.toLocaleLowerCase()`. This is a fixture gap. The panel itself renders on the component gallery instead: `fixture.html?surface=conversation-qol` shows tabs **To-dos 4 / Bookmarks / Members / Pins**, the seeded row "Audit the launch copy" and **Add a to-do**. Promote (`todoPromote: null`) has no seed.

- **Library to-dos lens per host:** `?view=library&lens=todos` routes to `#/library/todos` on `/rooms/` with "Review the launch checklist". On `/chat/` it routes to `/chat/library/todos` and shows the cloud fixture's own seed instead: a **Todos** heading with **1 open** beside it and "Share the customer notes". The two read as "Todos · 1 open" on screen but are separate text nodes, so `innerText.includes("Todos · 1 open")` is false; assert "1 open" and "Share the customer notes" (re-measured 2026-11-02 on `/chat/`). Both seeds are fine; assert the right one for each host.

Verified 2026-10-27 at `6c15b0fb` (maintenance pass, fixture lane). Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261027/r1/` (frames 28-30). Re-driven 2026-10-28 at `07f7d04c`, after the todos-lens batching fix in that commit, which changes no fixture-visible behaviour because both fixtures stub `todoBoards` and `ensureTodoBoard`. Results: the shell `?panel=todos` still fails with the `TodoRow` `toLocaleLowerCase` crash on both hosts, conversation-qol still shows **To-dos 4**, **Audit the launch copy** and **Add a to-do**, and the lens results are as above. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261028/r1/`.

### Doc menu (added 2026-10-29)

On `shell-fixture.html?view=room&alerts=quiet&panel=library&scope=server`,
right-click the **runbook.md** treeitem in the library panel, or focus it and
press the ContextMenu key (`LibraryPanel.tsx:696`, `:1194`). Either one opens
`DocContextMenu` (`DocContextMenu.tsx`, mounted at `Shell.tsx:4600-4606`), a
`menu` with no accessible name and 12 items: Open, Open in floating window,
Edit, History, Share..., Copy link, Export as Markdown..., Copy path, Move /
rename, Make read-only, Archive and Delete. Escape closes it. The full page's
**More note actions** button and doc links in messages open the same menu
(`LibraryView.tsx:5523`, `MessageText.tsx:1756`).

The verbs are not proved: `setDocReadOnly` and `setDocRestriction` are
unstubbed. The `/chat/` fixture stubs `openDocMenu` as a no-op
(`apps/cloud/tools/visual/shell-fixture.tsx:2398`), so no menu opens there.
The **Set topic index...** picker (`DocIndexPicker.tsx`) has no fixture route
(`docIndexPicker: null`, `shell-fixture.tsx:4147`).

Verified 2026-10-29 at `cdfb1b0f` (scheduled maintenance; menu on `/rooms/`, absence on `/chat/`). Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261029/r1/` (`doc-menu-*`).

### Today's note (added 2026-11-01)

The full page's **Today's note ⌘D** button (`[data-library-action="daily-note"]`
with `data-daily-note-day` set to the local day, `LibraryView.tsx:3233-3241`;
the add menu lists it as **Daily note**, `:3771`, `:4138`; the `d` key at
`:1766`) calls `session.openDailyNote()` (`:1597`; `lib/session.ts:39005`),
which the fixture never stubs. On `?view=library&alerts=quiet` the button is
there with `data-daily-note-day="2026-11-01"`, and clicking it opens nothing:
no doc pane, no `.library-daily-note` section (`:6568`), no toast, hash still
`#/library`. Driven 2026-11-01 on `/rooms/` at `936f5b64`. The daily note
itself is live verification pending.

## Doc pane states (`doc=server`)

Three fixture seeds render doc-pane states that no other guide covers. Each needs
`doc=server`: `docState` and `docMode` do nothing without it
(`shell-fixture.tsx:400-466`), and `doc=journal` cannot reconcile because the
conflict model is built against the server doc.

| Route (`shell-fixture.html?view=room&alerts=quiet&doc=server&…`) | What renders |
|---|---|
| (none) | The reader, with **Edit** and **Version history** |
| `docState=reconcile` | A `dialog` named **Two versions of this doc** with **Use every ↓** (twice), **what both started from**, **write it myself**, **Combine** ("1 passage left to settle") and **Later**. **Later** closes it and sets `dataset.fixtureDocReconcile=dismissed` |
| `docState=history` | History mode: a `select` named **Version history** at `9`, revisions r9 / r8 |
| `docAccess=readonly` | The reader keeps **Version history** but drops **Edit** |

`docState=review` (an auto-sync receipt in edit mode) exists too but was not
driven. No fixture seed opens an agent's doc **proposal**
(`DocProposalInlineReview.tsx:248`, "Review <author>'s proposal for <path>"),
so proposals remain live verification pending.

## Doc editor Vim mode

With Settings → Keyboard Shortcuts → **Vim mode** on
([settings-and-appearance.md](settings-and-appearance.md)), the CodeMirror
editor runs `@replit/codemirror-vim` (`editor/vim.ts`). Its root carries
`data-vim="on"` and a bottom `.cm-vim-panel` reads `--NORMAL--` or
`--INSERT--`. Escape changes Vim's mode only; it no longer leaves editing.
`:w` is the surface's Cmd/Ctrl+S (publish in DocPane, quiet flush in Library) and
`:q` is **Done** (`DocPane.tsx:2128-2135`). Toggling the setting reconfigures
open editors live. `?view=room&alerts=quiet&doc=journal` opens straight into
edit mode (**Edit Journal/2026/2026-08-07.md**):

```bash
D='(()=>JSON.stringify({vim:!!document.querySelector("[data-vim=on]"),
  panel:document.querySelector(".cm-vim-panel")?.textContent,
  mode:document.documentElement.dataset.fixtureDocMode}))()'
agent-browser eval "$D"                                   # vim true, --NORMAL--
agent-browser press i; agent-browser eval "$D"             # --INSERT--
agent-browser press Escape; agent-browser press Escape     # --NORMAL--, still editing
agent-browser press :; agent-browser press q; agent-browser press Enter
agent-browser eval "$D"                                   # mode "view", editor gone
```

Send ex commands one key at a time with `press`. `agent-browser keyboard type
":w"` inserts the literal text into the document, because it bypasses the Vim
keymap, even in normal mode. `:w` cannot be proved here. The fixture's
`session.docs` stub (`shell-fixture.tsx:3928-4004`) has no `publish` method, so
`:w`, like the **Publish** button, calls a method that does not exist. Driven,
Publish stayed enabled and `fixtureDocDirty` stayed `true`. (The
"Fixture publish is not configured" stub at `:4277` belongs to the checkpoint
restore store, not to this pane.)

## Doc reader select-all

Since `2a9df60c`, Cmd/Ctrl+A in a doc opened on the right selects only the
document body while the pane is the reader's last place (just opened, or the
last pointerdown or focusin landed inside it). A click or focus elsewhere hands
select-all back to the browser. Text fields (composer, edit-mode CodeMirror,
tag input) keep their own, and a handler that already prevented the chord (the
file tree) wins. Drive it in read mode on
`shell-fixture.html?view=room&alerts=quiet&doc=server` (`doc=journal` and
`note=long` do not mount the reader):

```bash
agent-browser click '[data-doc-pane-document]'
agent-browser press Meta+a
agent-browser eval '(()=>{const s=getSelection(),d=document.querySelector("[data-doc-pane-document]");return JSON.stringify({len:s.toString().length,inDoc:d.contains(s.anchorNode)})})()'
```

Expect the selection to cover the document (200 of its 201 characters at
`cd9f8c72`) with its anchor inside it. On load the composer holds focus, so
click the doc first. For the hand-back, click a `[data-message-row]` and
dispatch a cancelable Meta+A `keydown` on `document.body`: `defaultPrevented`
is `false`. `agent-browser press` does not perform the browser's native
page-wide select-all, so an empty selection after a chat click is a harness
artefact, not a failure.

### Doc tags (added 2026-11-02)

The server doc reader (`shell-fixture.html?view=room&alerts=quiet&doc=server`)
renders a `[data-doc-pane-tag-row]` under the header with a **+ tag** button
(`[data-doc-tag-add]`, `DocPane.tsx`). Clicking it mounts an inline `input`
with the placeholder **add tag**; the seeded doc carries no `.doc-tag-pill`
chips, so the chip title (**Search this server's library for #<key>**) and the
tag search it opens are source-only here. Driven 2026-11-02 on `/rooms/`
(18137).

### Library location explainer (added 2026-11-02)

The docked panel opens with an explainer card the first time each user sees
it: `[data-library-venue-explainer]` titled **Choose where shared work lives**
("This panel shows notes filed under this channel or its server. Your Library
is your personal workspace."), with **Open Your Library** and a dismiss button
named **Dismiss library location explanation** (`LibraryPanel.tsx:2117-2140`).
`?view=room&alerts=quiet&panel=library&scope=server` shows it on a fresh
browser session. Dismissing writes
`om.chat.libraryVenueExplainerAcknowledged:<userId>=1` (`u1` on the fixture,
`LibraryPanel.tsx:109-135`), and the card stays gone after a reload. Use a new
`AGENT_BROWSER_SESSION`, or clear that key, before proving it again: a session
that already dismissed it never shows it.

## Gotchas

- **The Archive lens renders its chrome and never fills — and it does not
  error either.** `?view=library&lens=archive` lands correctly
  (`aria-current="page"`, `data-home-library-archive` present) and then shows
  exactly `"Archived"` and a `Refresh` button: zero rows, no message, no
  failure text, and it stays that way. `session.archivedDocs` and
  `session.restoreDoc` are **not stubbed anywhere in the fixture**, so
  `LibraryView.tsx:8715`'s `await session.archivedDocs(homeSpaceId)` resolves
  through the `INERT` proxy, which **answers instead of throwing**. `INERT`'s
  iterator is an empty generator, so the list renders empty and the `catch`
  never runs.

  Predict this one from source and you will get it wrong in a specific way: it
  looks like it should land in the error branch with `"Couldn't load archived
  notes"`, and it does not, because unstubbed does not mean broken here — it
  means silently agreeable. This is the INERT trap in its purest form. The
  archive is `verified-unreachable` for content; the unmet prerequisite is a
  stub for those two methods, which is a harness gap worth closing.
- **`scope=server` empties the channel tab's name.** In that route the context
  tab reads `Channel # · 0 notes` — `#` with no channel after it — while the
  server tab reads `Server · 3 notes`. Do not caption a frame as if the
  channel shelf were empty for a seeded room; check the scope you booted with
  before reading anything into the context tab.
- Per-shelf filter memory is a module-level `Map` keyed by user and tenant
  (`server:${spaceId}` or `context:${room}:${topicId}`), so switching scope or
  channel **restores that shelf's own query** rather than clearing it. A
  filter box that is not empty when you arrive is the feature, not residue.
- Server-scope persistence across same-space channel switches lives in
  `packages/chat-ui/src/lib/rooms-hydration.ts`, not in `LibraryPanel.tsx`. Look there when a
  scope fails to survive a channel change.
- The full page is 8800+ lines and its save-state chip
  (`data-home-library-save-state`) has ten values, `idle` through
  `conflict` and `local-error`. `#860` made `local-error` a clickable manual
  flush. Treat the chip as its own proof surface; do not assert it in passing.

### Verification record

**Last verified:** 2026-11-05 (nightly maintenance). **Product commit:** `873a57ce` (GitLab origin/main; rooms-client 0.109.1; 17 commits past `ce14d4ba`). **Scope:** `/rooms/` (18170) `view=library&lens=agents` → `#/library/agents`, reading **LAST SYNC** **Unknown status**. **Limitations:** the other lenses only by route smoke. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261105/r1/` (`35`).

**Previous record:** 2026-11-04 (nightly maintenance). **Product commit:** `ce14d4ba` (GitLab origin/main; rooms-client 0.109.1; 16 commits past `ba4389e7`). **Scope:** `/rooms/` (18160): `?view=library` → `#/library`; `?view=library&lens=agents` → `#/library/agents` renders (h1 **Agents**, **LAST SYNC Unknown status**), the crash is gone. `/chat/` (18161): `/chat/library/agents`. **Limitations:** the doc menu, todos and archive lenses were not re-driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261104/r1/` (`lib-01-agents-lens`).

**Previous record:** 2026-11-03 (nightly maintenance). **Product commit:** `ba4389e7` (GitLab origin/main; rooms-client 0.108.0; one CI-only commit past `3f8f24bc`). **Scope:** `/rooms/` (18143) and `/chat/` (18144): the docked panel (`scope=server`, Channel 0 / Server 3) with **Choose where shared work lives**; the full page's **Today's note ⌘D**; the server doc reader (**Edit**, **Version history**); `docState=reconcile` → **Two versions of this doc**; `docState=history` at `9`; `docAccess=readonly` drops **Edit**. `/rooms/` only: right-clicking **runbook.md** opens the 12-item doc menu; `lens=todos` shows **Review the launch checklist**; `homeImport=open` → **Import folder into Your Library**. **Limitations:** unchanged. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261103/r1/` (`lib-*`).

**Previous record:** 2026-11-02 (scheduled maintenance). **Product commit:** `3f8f24bc` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18141): `panel=library&scope=server` presentation `side`; the location explainer shown, dismissed (`om.chat.libraryVenueExplainerAcknowledged:u1=1`) and still gone after a reload; `lens=todos` **Review the launch checklist**; `homeImport=open` **Import folder into Your Library**; `doc=server` **+ tag**. `/chat/` (18142): `panel=library&scope=server` presentation `side`; `lens=todos` **1 open** and **Share the customer notes** at `/chat/library/todos`. **Limitations:** the doc menu, Vim mode, select-all and Today's note were not re-driven in this pass; their nightly records stand. The doc outline toggle flips `aria-expanded` to `true` on `doc=journal`, but the outline renders only in view mode (`DocPane.tsx:1818`), so its body and **No headings in this note.** stay unproved. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261102/r1/`.

**Previous record:** 2026-11-02 (nightly maintenance). **Product commit:** `3f8f24bc` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18137): `panel=library&scope=server` → runbook.md right-click → the 12-item menu; the full page (`#/library`) with **Today's note ⌘D** (`data-daily-note-day=2026-11-02`); `lens=todos` → `#/library/todos`; `lens=archive` → `#/library/archive` with `data-home-library-archive`; `homeImport=open` → **Import folder into Your Library**; `doc=server` reader (**Edit**, **Version history**, **+ tag** → an **add tag** input), `docState=reconcile` → **Two versions of this doc** (Result / Changes / Use every ↓ ×2 / what both started from / write it myself / **Combine** "1 passage left to settle", **Later**), `docState=history` → **Version history** at 9 (r9 · current · kyle, r8 · om), `docAccess=readonly` drops **Edit**; `/chat/` (18138): the doc menu does not open (`openDocMenu` noop), `lens=todos` → `/chat/library/todos`, `lens=agents` renders **Agents** (`/rooms/` still shows **Your Library could not load**). **Limitations:** `docState` and `docMode` need `doc=server` (without it a run reads as "nothing renders"); the doc reader select-all and the import flow past the dialog were not re-driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261102/r1/`.

**Previous record:** 2026-11-01 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18137): `panel=library&scope=server` filter `a` → **2 notes match “a”** with **Clear search**, **Open Library full page** → `full`; `lens=todos` → `#/library/todos` (**Todos** current, "Review the launch checklist"); `lens=archive` → `#/library/archive` with **Refresh**; `lens=agents` → **Your Library could not load**; `?view=home&homeImport=open` → **Import folder into Your Library** (**Browse folders...**, **Continue**); `doc=server` → **Edit**, **Version history**, **Close document**; `docState=reconcile` → **Two versions of this doc**, **Later** → `fixtureDocReconcile=dismissed`; `docState=history` → the **Version history** select (2 options); `docAccess=readonly` → no **Edit**; `doc=journal` with `om.chat.vimMode` → `data-vim=on` and `.cm-vim-panel` **--NORMAL--**; the **Today's note ⌘D** button (inert). `/chat/` (18138): `lens=todos` → `/chat/library/todos` ("Share the customer notes"); `lens=agents` renders (Agents, Agent persona note, Living daily note, Note gardener); `docState=reconcile` and `docState=history`. **Limitations:** the `runbook.md` doc menu was not re-opened (the script's row finder missed on the full page; the 2026-10-31 twelve-item record stands); doc verbs, proposals, `docState=review`, import phases and the daily note itself stay pending. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261101/r1/` (`library-01` to `library-06`, `census-03`, `chat-13`).

**Previous record:** 2026-10-31 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18135): `panel=library&scope=server` filter `a` → `2 notes match “a”` with the clear control, **Open Library full page** → `full`; `runbook.md` right-click → 12 items (Open … Delete); `?view=library&lens=todos` → `#/library/todos` with `aria-current`; `lens=archive` → **Archived** and **Refresh**, no rows; `?view=home&homeImport=open` → **Import folder into Your Library**; `doc=server` **Edit** and **Version history**; `docState=reconcile` → **Two versions of this doc**, **Later** → `fixtureDocReconcile=dismissed`; `docState=history` → the **Version history** select; `docAccess=readonly` → no **Edit**; `doc=journal` with `om.chat.vimMode=true` set first → `data-vim=on` and `.cm-vim-panel` **--NORMAL--** (without the pref the editor has no Vim panel). `/chat/` (18136): `lens=todos` → `/chat/library/todos`; `lens=agents` rendered (Agents, Agent persona note, Living daily note, Note gardener); `docState=reconcile` and `docState=history`. **Limitations:** `lens=agents` still crashes on `/rooms/` (smoke, **could not load**); `?panel=todos` crashes on both; doc verbs, proposals, `docState=review`, import phases, the `/chat/` doc menu and the **New doc** entry in the panel's add menu (`LibraryPanel.tsx:1984`) were not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261031/r1/`.

**Previous record:** 2026-10-30 (scheduled maintenance). **Product commit:** `47cb13bf` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/`: panel search "2 notes match “a”"; **Open Library full page** → `full` and browser Back → `side` with the hash unchanged (wait for the panel's slide-in, or the click lands on the dock); the 12-item `runbook.md` menu (Escape closes it; read `[role=menuitem]` from the DOM); `lens=todos` and `lens=archive` (**Refresh**); `docState=reconcile` → **Two versions of this doc** and `homeImport=open` → **Import folder into Your Library**, each after about 4 s under host load; `lens=agents` still fails ("Your Library failed to load"). `/chat/`: `lens=todos` and `lens=agents` mount. **Limitations:** Doc verbs, proposals. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261030/r1/` (frames 42-44).

**Previous record:** 2026-10-29 (nightly maintenance). **Product commit:** `cdfb1b0f` (origin/main; rooms-client 0.108.0). **Scope:** `lens=todos` routed to `#/library/todos` with "Review the launch checklist" on `/rooms/`, and to `/chat/library/todos` with "Share the customer notes" on `/chat/`. `lens=agents` still crashes on `/rooms/` (lazy-surface **Try again**) and renders on `/chat/`. `panel=library&scope=server` mounted the panel. **Limitations:** History, the panel filter, import and the doc pane were not re-driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261029/r1/` (frames 18, 35–36, 59–60).

**Previous record:** 2026-10-28 (scheduled maintenance). **Product commit:** `07f7d04c` (origin/main). **Scope:** `lens=todos` on both hosts (per-host seeds above), `lens=agents` rendered on `/chat/` and crashed on `/rooms/`, `?panel=todos` crashed on both hosts, and conversation-qol showed **To-dos 4**. **Limitations:** history, the library panel filter, import and the doc pane were not re-driven at this tree. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261028/r1/`.

**Previous record:** 2026-10-28 (nightly maintenance). **Product commit:** `2dd7aad1` (origin/main). **Scope:** `lens=todos` routed to `#/library/todos` with "Review the launch checklist"; `doc=server&docState=history` showed a `select` **Version history** at `9` (r9 · current · kyle, r8 · om); `panel=library&scope=server` mounted the **Library** aside (`data-right-panel=library`); `homeImport=open` opened **Import folder into Your Library**. `?panel=todos` showed the lazy-surface error "Todos could not load … Try again / Reload OM Chat", and `fixture.html?surface=conversation-qol` showed tabs **To-dos 4 / Bookmarks / Members / Pins** with "Audit the launch copy". **Limitations:** `lens=agents` (fixture crash), reconcile, read-only, doc Vim, select-all, `:w`, proposals and `/chat/` were not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261028/r1/` (frame 20). Previous record: 2026-10-27 at `6c15b0fb`.