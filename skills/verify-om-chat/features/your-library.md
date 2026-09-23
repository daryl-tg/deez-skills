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
  has not settled (`LibraryPanel.tsx:2034-2035`). Measured live as
  `2 notes match “a”` — an `--exact` match on a bare `"2 notes match"` misses.
- **Clear control**: `button[aria-label="Clear search"]`
  (`data-library-filter-clear`), rendered **only when the field is non-empty**.
  Absent on a fresh panel; that is the control working, not a regression.
- **Scope switch**: `role="tablist"` named **"Library scope"**
  (`LibraryPanel.tsx:2043-2044`, `data-library-scope-switch`) with two tabs.
  The server tab (`data-library-scope-server`, `:2105`) is named **"Server"**,
  deliberately not "Server library", to disambiguate from the rail's own
  Library door. Accessible names carry counts: `Server · 3 notes`.
- **Expand / collapse**: `button[aria-label="Open Library full page"]`, which
  becomes `"Collapse Library to side panel"` (`LibraryPanel.tsx:1943-1944`).
  The cheap DOM check is `data-library-presentation` on the panel root
  (`:1812`), which flips `side` → `full`.

### The full page (`?view=library`)

Four sidebar lenses, each stamped `data-home-library-lens-{id}` and carrying
`aria-current="page"` when active: **Todos** (`?lens=todos`), **Shared docs**,
**Agents** (`?lens=agents`), and **Archive** (`?lens=archive`). All four are
present in this lane; Archive is the newest.

Archive renders `data-home-library-archive` (`LibraryView.tsx:8706`) with an
"Archived" heading, a **Refresh** button, and per-row **Restore** buttons on
`data-home-archived-doc={docId}` (`:8756`).

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
agent-browser open "$(./control-om-chat url \
  'tools/visual/shell-fixture.html?view=room&alerts=quiet&panel=library&scope=server')"
```

`?scope=server` selects the server tab at boot (`shell-fixture.tsx:215`). A
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
1337-doc corpus, `shell-fixture.tsx:269`), `?list=flat` (**sticky** — it
writes `localStorage["om.chat.libraryList"]` at `:123` with no clearing
branch, so it survives until you clear storage by hand), `?note=long|wrapped`,
and `?libraryState=error` (`:4078`).

## Gotchas

- **The Archive lens renders its chrome and never fills — and it does not
  error either.** `?view=library&lens=archive` lands correctly
  (`aria-current="page"`, `data-home-library-archive` present) and then shows
  exactly `"Archived"` and a `Refresh` button: zero rows, no message, no
  failure text, and it stays that way. `session.archivedDocs` and
  `session.restoreDoc` are **not stubbed anywhere in the fixture**, so
  `LibraryView.tsx:8693`'s `await session.archivedDocs(homeSpaceId)` resolves
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
