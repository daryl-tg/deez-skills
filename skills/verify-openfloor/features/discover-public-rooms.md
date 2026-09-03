# Discover and public rooms

The Discover tab is the public-room directory: rooms anyone on OpenMarket can
join, listed with an online count and a one-line description, above the rooms
this account has already joined. Joining is deliberate and reversible, and the
screen says so — public rooms do not become permanent Chats entries.

## Sub-features

- `discover-directory` lists open public rooms.
- `discover-search` filters the directory by typed text.
- `discover-joined` lists the rooms this account has joined.
- `discover-join` joins a room from a directory row.
- `discover-open` opens a joined room's conversation.
- `discover-leave` leaves a joined room.

## How to get to it (user POV)

- Tap **Discover** in the bottom dock. It is the third of five tabs.

## Driving it with control-openfloor

Preconditions:

- `./control-openfloor doctor` exits zero, start from the Chats root.
- **Joining and leaving are production writes.** Read the directory; do not
  join or leave. Only `discover-directory`, `discover-search`, `discover-joined`
  and `discover-open` are free.

Stable handles:

| Handle | What it is |
|---|---|
| `label="Discover"` | the dock tab |
| `label="Public Rooms"` | the screen title in the home header |
| `label="Search public rooms"` | the search field |
| `label="Clear public room search"` | a real, labelled clear control |
| `label="Open conversations"` | the directory list container |
| `label="Join public room <name>"` | a directory row's join control |
| `label="Open public room <name>"` | the same control once joined |
| `label="Open joined public room <name>"` | a joined-room row |
| `label="Leave public room <name>"` | leave |
| `label="Jump to a conversation"` | the shared home-header jump control |

- **Open the tab.** `./control-openfloor device press 'label="Discover"' --settle`.
  The settled diff shows `Search public rooms` and `Join public room …` rows.
- **Read the directory.** `./control-openfloor device snapshot -i`. Rows carry a
  name, an `<n> online` line and the copy *"A live public conversation on
  OpenMarket."*; the header explains *"Join, talk, and leave whenever. Public
  Rooms do not become permanent Chats entries."*
- **Search.** `./control-openfloor device fill 'label="Search public rooms"' "trontal" --settle`.
  Unlike the Chats inbox this search is local to the loaded directory. Clear it
  with `press 'label="Clear public room search"'`.
- **Proof.** The `--settle` diff plus
  `./control-openfloor device screenshot --out "$PWD/artifacts/<run>/<rev>/discover.png" --normalize-status-bar`.

## Gotchas

- **`find` is dangerous on this screen.** `find` is a *contains* match, and the
  header copy contains the word *Chats* (*"do not become permanent Chats
  entries"*). `find "Chats"` here can match that paragraph instead of the dock
  tab and tap the wrong thing. Press the dock tab by its own label, or by a
  ref from a settle diff.
- **The join and open controls share one row.** `Join public room <name>`
  becomes `Open public room <name>` once joined, so a selector built on `Join`
  silently stops matching for exactly the rooms you already belong to.
- Verified live 2026-09-03 on `f2c3f88` (iPhone 17 Pro, iOS 26.5).
