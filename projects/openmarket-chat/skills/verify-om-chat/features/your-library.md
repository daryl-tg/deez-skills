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
present in this lane; Archive is the newest. **`?lens=agents` crashes in this
lane (still at `afabb11c`).** The hash reaches `#/library/agents`, but the surface reads
"Your Library could not load" with Try again / Reload OM Chat, and the console
shows `TypeError: Cannot read properties of undefined (reading 'tone')` in
`LibraryPersonaCard`. The cause is now isolated to the fixture. The shell fixture never
stubs `session.libraryDaemon`, so the autofill proxy answers `INERT`
(`shell-fixture.tsx:2564-2569`). `LibraryView.tsx:6959` awaits
`daemon?.fetchPersona()`, gets the truthy `INERT` back and takes the `ready`
branch (`:6960`). `personaStatusPresentation` (`:6168-6188`) then matches no
`status.state` and returns `undefined`, and `.tone` throws (`:6405`). The
production client rejects unlisted states (`src/lib/om-daemon.ts:1548`), so
this is a fixture gap, not a product bug. Stubbing `libraryDaemon: null` would
render the card's `unavailable` branch instead. Until the fixture changes, assert only
the route for the Agents lens here, and report the crash rather than
captioning it as the lens.

Archive renders `data-home-library-archive` (`LibraryView.tsx:8706`) with an
"Archived" heading, a **Refresh** button, and per-row **Restore** buttons on
`data-home-archived-doc={docId}` (`:8756`).
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
`?libraryState=error` (`:4208`, applied only while the active view is library).

### Import folder and the To-dos panel (added 2026-10-27)

- **Import folder:** `shell-fixture.html?view=home&alerts=quiet&homeImport=open` opens dialog **Import folder into Your Library** on `/rooms/`. On `/chat/` the same URL showed no dialog. `import=<phase>` (`shell-fixture.tsx:4157`) seeds later phases, which were not driven.
- **To-dos panel:** the shell's `?panel=todos` crashes into the lazy-surface error **Todos could not load** with **Try again** and **Reload OM Chat** (`[data-lazy-surface-error="Todos"]`) on both hosts. The roster `members` seed has no `role`, and `TodosPanel.tsx:154` calls `member.role.toLocaleLowerCase()`. This is a fixture gap. The panel itself renders on the component gallery instead: `fixture.html?surface=conversation-qol` shows tabs **To-dos 4 / Bookmarks / Members / Pins**, the seeded row "Audit the launch copy" and **Add a to-do**. Promote (`todoPromote: null`) has no seed.

Verified 2026-10-27 at `6c15b0fb` (maintenance pass, fixture lane). Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261027/r1/` (frames 28-30).

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
`session.docs` stub (`shell-fixture.tsx:3926-4002`) has no `publish` method, so
`:w`, like the **Publish** button, calls a method that does not exist. Driven,
Publish stayed enabled and `fixtureDocDirty` stayed `true`. (The
"Fixture publish is not configured" stub at `:4275` belongs to the checkpoint
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

## Gotchas

- **The Archive lens renders its chrome and never fills — and it does not
  error either.** `?view=library&lens=archive` lands correctly
  (`aria-current="page"`, `data-home-library-archive` present) and then shows
  exactly `"Archived"` and a `Refresh` button: zero rows, no message, no
  failure text, and it stays that way. `session.archivedDocs` and
  `session.restoreDoc` are **not stubbed anywhere in the fixture**, so
  `LibraryView.tsx:8702`'s `await session.archivedDocs(homeSpaceId)` resolves
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

**Last verified:** 2026-10-27. **Product commit:** `6c15b0fb286e9dc1b6cb130c9c97cd7e0afa9254` (origin/main). **Scope:** `lens=todos` routed to `#/library/todos` with "Review the launch checklist", and `doc=server&docState=history` showed **Version history** at `9`. **Limitations:** The panel filter, full page, `lens=agents` (fixture crash), reconcile, read-only, doc Vim, select-all, `:w`, proposals and import/export/trash/move/restore were not re-driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261027/r01/` (frame 25). Previous record: 2026-10-26 at `5820fbea`.
