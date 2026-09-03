# Your Library and to-dos

The Library tab is the account's own document workspace: personal notes in
folders, documents other people shared, and open to-dos, under three segment
tabs. A folder here is a path prefix rather than a record, so notes are created
by typing a path and there is no empty folder to make.

## Sub-features

- `docs-yours` lists this account's own documents, grouped by folder.
- `docs-shared` lists documents shared with this account.
- `docs-todos` lists open to-dos.
- `docs-daily` opens today's daily note.
- `docs-search` filters the document list.
- `docs-create` creates a note at a typed path.
- `docs-folders` expands, collapses and renames folders.
- `docs-open` opens a document into the library editor.

## How to get to it (user POV)

- Tap **Library** in the bottom dock. It is the fourth of five tabs.
- Or from Settings → SUPPORT → **Your docs**, which lands on the same screen.

## Driving it with control-openfloor

Preconditions:

- `./control-openfloor doctor` exits zero, start from the Chats root.
- **Creating, renaming and completing are production writes.** Reading the
  lists, searching them, expanding folders and opening a document are free.
  `docs-create`, `docs-folders`' rename, and completing a to-do are the
  operator's call.

Stable handles:

| Handle | What it is |
|---|---|
| `label="Library"` | the dock tab |
| `label="Your Library"` | the screen title |
| `label="Yours"` / `label="Shared with me, 0"` / `label="Todos, 0"` | the segment tabs; **the last two carry live counts** |
| `label="Open today's daily note"` | the daily-note control |
| `label="Expand all folders"` / `label="Collapse all folders"` | **one control, two labels**, by current state |
| `label="Add documents to your library"` | the add control |
| `label="Search your docs"` | the search field |
| `label="Clear search"` | its labelled clear control |
| `label="New note path"` | the create field |
| `label="Create note"` | create; `[disabled]` until the path field has text |
| `label="Expand <folder>"` / `label="Collapse <folder>"` | a folder row's disclosure |
| `label="Rename <folder>"` | a folder row's rename control |
| `label="Open <title or path>"` | a document row |
| `label="Complete <todo title>"` | a to-do's completion control |
| `label="Open the doc for <todo title>"` | a to-do's document |
| `label="Open source message in #<channel>"` | a to-do's originating message |

- **Open the tab.** `./control-openfloor device press 'label="Library"' --settle`.
  The settled diff carries `Your Library`, the three segment tabs, and
  `Open today's daily note`.
- **Read each segment.** Press `Shared with me, …` and `Todos, …` on their
  stable leading substring with `find`, never on the full label — both embed a
  live count. `./control-openfloor device find "Shared with me"`.
- **Search.** `fill 'label="Search your docs"' "journal" --settle`, then clear
  with `press 'label="Clear search"'`.
- **Verify the create gate without creating.**
  `./control-openfloor device snapshot -i` on arrival shows
  `[button] "Create note" [disabled]` beside an empty `New note path`. That
  disabled state is the assertion; typing a path to watch it enable is one
  keystroke away from a real document, so leave it.
- **Expand a folder.** `press 'label="Expand Journal"' --settle` and assert the
  document rows in the diff, then `press 'label="Collapse Journal"'`.
- **Proof.** The `--settle` diff plus
  `./control-openfloor device screenshot --out "$PWD/artifacts/<run>/<rev>/library.png" --normalize-status-bar`.

## Gotchas

- **Two segment tabs carry live counts** (`Shared with me, 0`, `Todos, 0`). They
  are the same hazard as the Chats tab's unread count: never exact-match, never
  assert the number.
- **The disclosure and the expand-all control both flip their own labels.** A
  selector on `Expand …` stops matching the moment the thing is open. Read the
  current label out of the settle diff rather than assuming which half you are
  on.
- **This screen is not the server Library.** `Your Library` (this file) is
  personal; `Open <server> Library` is a space's shared destination and lives in
  [servers-and-channels](./servers-and-channels.md). They are different routes
  with different contents, and the word "Library" appears in the dock, in the
  server screen, and in Channel tools.
- **`Create note` is one press from a production document.** It sits next to a
  text field on the default screen, so be deliberate about what you fill.
- Verified live 2026-09-03 on `f2c3f88` (iPhone 17 Pro, iOS 26.5).
