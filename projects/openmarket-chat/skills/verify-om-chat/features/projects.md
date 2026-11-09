# Projects

A server's ticket tracker: the **Projects** page with its Table and Board, the
bulk bar, each card's menu, and a channel's **Tickets in #channel** panel with
its **New ticket** form. The single-ticket page, Needs you and every write are
not proved yet; see [Gotchas](#gotchas).

## Sub-features

- **Projects page** (`packages/chat-ui/src/components/projects/TodosPage.tsx`,
  mounted by `TodosSurface.tsx` when `session.active.kind` is `"todos"`). The
  heading **Projects**, a counts line ("1 open · 1 in progress"), the buttons
  **Table**, **Board** and **New ticket**, the filter comboboxes **Labels**,
  **Assignee**, **Status**, **Priority**, **Due**, **Channel**, **Group by** and
  **More**, and the searchbox **Search tickets**.
- **Table** (`TodosTable.tsx`). The columns are Select all, TITLE, STATUS,
  ASSIGNEE, LABELS, PRIORITY, DUE, CHANNEL, CREATOR, ASSIGNED BY and UPDATED.
  Each row has a checkbox **Select <title>** and a button **!<n> <title>**, and
  the footer reads "Showing 3 of 3".
- **Bulk bar** (`TodoBulkBar.tsx`). Checking a row shows a `toolbar` named
  **Bulk actions** with **Status**, **Assignee**, **Add labels**, **Remove
  labels** (disabled with no labels), **Priority**, **Due**, **Close as Won't
  do** and **Clear selection**.
- **Board** (`TodosBoard.tsx`). Four `region`s, **Open**, **Assigned**, **In
  progress** and **Done**, each with an H2. Each card is a button named by its
  title, with **More actions for !<n>**, which opens a menu holding **Move
  to…**. The Status filter drops out on the board.
- **Opening a ticket**. **!<n> <title>** routes to `#/todo/<spaceId>/<n>`; the
  ticket page itself is not proved.
- **Channel panel** (`ChannelTodosPanel.tsx`, mounted by `RightPanels.tsx` when
  `rightPanel === "todos"` and the server is on Projects). It is the
  `complementary` region **Tickets in #ops**, with **New ticket in #ops** and
  one button per open ticket, such as "Fix alert dedupe !1 Open High".
- **New ticket form** (`TodoCreateForm.tsx`). It has the textboxes **TITLE** and
  **DESCRIPTION**, **Add a label**, **Priority** (No priority), **Due**,
  **Assignee** (Unassigned), **Home channel** (#ops), **Cancel** and
  **Create**. **Create** stays disabled until the title has text.

## How to get to it (user POV)

Press **Projects** in the server's sidebar actions (beside **Focus** and
**Revisit**) to open the page. Switch between **Table** and **Board** at the
top. Tick a row to bring up the bulk bar. Press a ticket's number to open it. In
a channel, open the tickets panel from the channel header to see that channel's
tickets, and press **+** (**New ticket in #channel**) to make one.

## Driving it with control-om-chat

Neither shell fixture has a `todos` store, so the page needs three init
scripts: the people stub from [README.md](README.md#stub-the-people-directory-first-required-at-82390825)
(with `heldIn`, which the filters read), an error catcher if you want stacks,
and this Projects stub. It answers `session.todos` with a records-mode store
holding three tickets, and defines `openTodos` and `openTodo`, which mutate the
fixture's live `active` object in place and repaint through
`closeRightPanel()`.

```bash
cat > "$SCRATCH/fixture-projects-stub.js" <<'JS'
(() => {
  const S = "s1", R = "ops", ts = "2026-08-09T10:00:00Z";
  const def = (k, v) => Object.defineProperty(Object.prototype, k,
    { value: v, configurable: true, writable: true, enumerable: false });
  const rec = (n, title, status, priority) => ({
    id: `00000000-0000-4000-8000-00000000000${n}`, spaceId: S, number: n, roomId: R,
    topicId: null, title, description: "", descriptionRev: 1, attachments: [],
    status, assigneeId: n === 2 ? "u-dax" : null, assignedById: null, agent: null,
    priority, dueDate: null, labelIds: [], creatorId: "u-ana", people: {},
    sourceMessage: null, closedById: null, closedAt: null, createdAt: ts,
    updatedAt: ts, lastActivityAt: ts, rev: 1, todoSeq: n, legacy: null,
    legacyAssigneeHandle: null });
  const recs = [rec(1, "Fix alert dedupe", "open", "high"),
                rec(2, "Ship digest", "in_progress", "medium"),
                rec(3, "Close the loop", "done", "none")];
  const byId = new Map(recs.map(r => [r.id, r]));
  const views = new Map();
  const viewFor = (key) => {
    if (!views.has(key)) {
      const needs = String(key).includes("needs-you");
      views.set(key, { status: "ready", ids: needs ? [] : recs.map(r => r.id),
        nextCursor: null, total: needs ? 0 : 3,
        counts: { open: 1, in_progress: 1, done: 1, wont_do: 0 }, error: null, countsError: null });
    }
    return views.get(key);
  };
  const labelList = { labels: [] };
  const inert = new Proxy(function () {}, { get: () => inert, apply: () => inert });
  def("todos", new Proxy({
    modeFor: () => "records", recordsOn: () => true, memberOf: () => true,
    spaceForRoom: () => S, today: () => "2026-08-09", switchedAt: () => "2026-08-01T00:00:00Z",
    record: (id) => byId.get(id), view: viewFor,
    refreshView() {}, releaseView() {}, loadMore() {},
    labels: () => labelList, refreshLabels() {}, watchLabels: () => () => {},
    labelsFailed: () => false, labelCreation: () => null, roomLabel: () => "#ops",
    badge: () => null, mentionCount: () => 0, mentionTotal: () => 0, subscribe: () => () => {},
  }, { get: (t, k) => (k in t ? t[k] : inert) }));
  const open = function (kind, patch) {
    const a = this.active;
    for (const k of Object.keys(a)) delete a[k];
    Object.assign(a, { kind }, patch);
    this.closeRightPanel();
  };
  def("openTodos", function (spaceId, o) { open.call(this, "todos", { spaceId, ...(o && o.roomId ? { roomId: o.roomId } : {}) }); });
  def("openTodo", function (ref) { open.call(this, "todo", { ref }); });
})();
JS
agent-browser --init-script "$SCRATCH/fixture-people-stub.js" \
  --init-script "$SCRATCH/fixture-projects-stub.js" open about:blank
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=room&alerts=quiet#/projects/s1')"
agent-browser find role button click --name "Board"
agent-browser find role button click --name "Table"
agent-browser find role checkbox click --name "Select Ship digest"   # -> toolbar "Bulk actions"
agent-browser find role button click --name "Clear selection"
agent-browser find role button click --name "!1 Fix alert dedupe"   # -> #/todo/s1/1
```

The fixture seeds the hash only when it is empty, so `#/projects/s1` reaches
`bindRouting`, which calls the stubbed `openTodos` at boot. On `/chat/` (base
`/chat/`, the cloud lane) the same URL works; the fixture then rewrites the
location to `/chat/projects/s1?view=room&alerts=quiet`.

For the channel panel, open `shell-fixture.html?view=room&alerts=quiet&panel=todos`
with the same two stubs and read the `complementary` **Tickets in #ops**. Press
**New ticket in #ops**, fill **TITLE**, and confirm **Create** turns enabled,
then press **Cancel**.

## Gotchas

- **The ticket page is not reachable yet.** `#/todo/s1/1` routes, then the
  surface boundary shows **Projects could not load** ("Cannot convert object to
  primitive value"), because `todos.ticket(ref)` answers `INERT` instead of a
  `TodoTicketController` (`lib/todos/ticket.ts:155`). A full ticket stub is the
  next harness step.
- **Every column holds every ticket.** The stub returns the same ids for every
  view key, so the Board shows all three tickets under each column. The board
  layout and card menus are real; the per-column split is not.
- **Needs you renders empty.** The page queries the `needs-you` keys
  (`overdue`, `due_soon`, `assigned`, `in_progress`, `updates`), and the stub
  answers them empty, which hides the section.
- **CHANNEL reads "Deleted channel".** `homeName` cannot resolve the stub's
  `roomId: "ops"` to a fixture room. That is a stub artefact, not a product fault.
- **No write is proved.** Create, bulk changes, **Move to…** and the filters hit
  `INERT` or the stub's no-ops. Proving a write needs a daemon-pair lane on a
  records-mode server.
- **The stub keys sit on every plain object.** `todos`, `openTodos` and
  `openTodo` live on `Object.prototype`, so any `x.todos` reads the store. The
  first draft crashed `TopicStream` in `markerCutoffFor` until the store
  answered `switchedAt`. If a new crash names a `todos` reader, add the member
  it reads.
- **Ticket creators must be seeded users.** A record whose `creatorId` is not a
  fixture user (such as `"u1"`) crashed `<Avatar>` with "Functions are not valid
  as a React child" on the first runs. `u-ana` and `u-dax` render "ana (ops)" and
  "D dax".
- **On `/chat/`, do not `reload` after a route change.** The cloud fixture
  rewrites the location to a path (`/chat/room/ops?…`, `/chat/projects/s1?…`).
  A reload then asks the dev server for that path and lands outside the fixture
  (once on `/chart/`). Open the fixture URL again instead.

## Verification record

**Last verified:** 2026-11-09 (scheduled maintenance). **Product commit:** `16da8ecf` (GitLab origin/main; one CI-only commit past `82390825`). **Scope:** with the people and Projects stubs, on `/rooms/` (18141): **Projects** with "1 open · 1 in progress", the 11-column Table and 3 rows, **Board** with the regions Open, Assigned, In progress and Done, **More actions for !1** → **Move to…**, **Select Ship digest** → **Bulk actions** (8 controls), **!1 Fix alert dedupe** → `#/todo/s1/1`, `panel=todos` → **Tickets in #ops**, and **New ticket in #ops** → the form (with **Create** enabled after a title, then **Cancel**). On `/chat/` (18142): the Table and **Tickets in #ops**. **Limitations:** the ticket page fails to load (no ticket controller stub); no write, filter, move or Needs you item was exercised; the per-column board split is a stub artefact. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261109/r1/` (`01`–`10`).
