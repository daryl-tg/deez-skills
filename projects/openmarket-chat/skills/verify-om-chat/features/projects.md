# Projects

A server's ticket tracker: the **Projects** page with its Table and Board, the
bulk bar, each card's menu, a channel's **Tickets in #channel** panel with its
**New ticket** form, and the single-ticket page with its files, comment box and
home chip. Needs you and every write are not proved yet; see [Gotchas](#gotchas).

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
- **Opening a ticket**. **!<n> <title>** routes to `#/todo/<spaceId>/<n>`
  (`/chat/todo/<spaceId>/<n>` on the cloud host).
- **Ticket page** (`TodoTicket.tsx`). The breadcrumb **Projects** / `!1`, the
  title `h1.ticket-title` (its **Rename** button), **Follow**, **More actions**,
  the side column's comboboxes **Status**, **Assignee**, **Priority** and **Add a
  label**, **Set due date**, the rows Home channel, Creator and Assigned by, the
  **Followers** region, and the note "Anyone in this server can change this
  ticket. Every change lands in Activity." (`TodoTicket.tsx:304`).
- **Ticket files** (`TodoAttachments.tsx`, `eae9681d`). Each file is a card with
  a download control and **Open in panel**. Below the files sits the button
  **Attach a file to the ticket** (text "Attach a file"). From source, any
  server member gets it, whatever the home channel allows. It renders only while the ticket holds
  fewer than ten files: at ten it is gone, with no disabled stand-in.
- **Comment box** (`TodoCommentBox.tsx`). The textbox **Comment** (placeholder
  "Add a comment"), the icon-only paperclip **Attach a file**, **Mention
  someone**, and **Comment** (disabled while empty). The paperclip caps the
  files staged on one comment at ten; the ticket's own ten-file cap does not
  touch it.
- **Server mute** (`ticket-mute.tsx`). While the viewer is muted in the server,
  a `status` banner reads "You're muted in this server until <time>. You can
  read tickets but can't change them." Both attach buttons stay in place with
  `aria-disabled="true"` and the mute sentence as their description, and the
  **Comment** textbox turns `readOnly`.
- **Home chip** (`lib/todos/homes.ts:52-58`). The Home channel row reads
  `#ops`, **Deleted channel**, **Private channel** (no channel name is known) or
  `#ops (archived)`. The table's CHANNEL column uses the same names.
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
holding three tickets, a cached ticket controller per ticket (`todos.ticket`),
the `!` lookup (`todos.lookup`) and ticket references (`todos.refs`). It defines
`openTodos` and `openTodo`, which mutate the fixture's live `active` object in
place and repaint through `closeRightPanel()`. It also defines
`knownRoomLabel` and `signingFailedFor`, which neither fixture spells out.
Without `knownRoomLabel` the home chip renders a function, and React logs
"Functions are not valid as a React child" (driven). Without
`signingFailedFor`, `AttachmentView` would treat every file card as failed to
sign (source only).

The stub reads three query parameters: `ticketFiles=<n>` gives ticket 1 that
many files, `ticketMuted=1` mutes the viewer in the server, and
`ticketHome=deleted|private|archived` changes the home chip.

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
  const q = new URLSearchParams(location.search);
  const files = Number(q.get("ticketFiles") || 0);
  recs[0].attachments = Array.from({ length: files }, (_, i) =>
    ({ key: `k${i + 1}`, name: `file-${i + 1}.txt`, size: 1200 + i, mime: "text/plain", scanStatus: "clean" }));
  const byId = new Map(recs.map(r => [r.id, r]));
  const tickets = new Map();
  const ticketFor = (ref) => {
    const key = ref.todoId ?? `${ref.spaceId}/${ref.number}`;
    if (tickets.has(key)) return tickets.get(key);
    const todo = ref.todoId ? byId.get(ref.todoId)
      : recs.find(r => r.spaceId === ref.spaceId && r.number === Number(ref.number));
    const state = { status: todo ? "ready" : "not-found", todo: todo ?? null, followers: [], activity: [],
      olderBefore: null, descriptionRev: todo?.descriptionRev ?? 0, sourceMessageInfo: null };
    const c = { state: () => state, subscribe: () => () => {}, release() {}, dispose() {}, caughtUp() {},
      retry: async () => {}, loadOlder: async () => {}, todoId: () => todo?.id ?? null,
      spaceId: () => todo?.spaceId ?? ref.spaceId ?? null, setFields: async () => {}, remove: async () => {},
      follow: async () => {}, comment: async () => {}, editComment: async () => {}, deleteComment: async () => {} };
    tickets.set(key, c);
    return c;
  };
  const byNumber = (n) => recs.find((t) => t.number === Number(n));
  const refStates = new Map();
  const refStateFor = (key, t) => {
    if (!refStates.has(key)) refStates.set(key, t ? { status: "visible", todo: t, activity: [] } : { status: "hidden" });
    return refStates.get(key);
  };
  const lookupCache = new Map();
  const lookupRows = (space, query) => {
    const k = space + "|" + query.trim();
    if (!lookupCache.has(k)) {
      const needle = query.trim().toLowerCase();
      const rows = needle ? recs.filter((t) => t.spaceId === space &&
        (/^\d+$/.test(needle) ? String(t.number).startsWith(needle) : t.title.toLowerCase().includes(needle)))
        .map((t) => ({ todo: t, exact: String(t.number) === needle })) : [];
      lookupCache.set(k, { status: "ready", rows });
    }
    return lookupCache.get(k);
  };
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
    ticket: ticketFor, homesVersion: () => 0, follow: async () => {},
    lookup: { prefetch: async () => {}, rows: lookupRows, release: () => {} },
    refs: { hold: () => () => {}, subscribe: () => () => {}, setFollowing() {},
      title: (_s, n) => byNumber(n)?.title,
      get: (ref) => refStateFor(`${ref.spaceId}/${ref.number}`, ref.spaceId === S ? byNumber(ref.number) : undefined) },
    roomDeleted: () => q.get("ticketHome") === "deleted",
    archivedHome: () => (q.get("ticketHome") === "archived" ? "#ops (archived)" : null), forgetLabel() {},
    upload: async (_s, f) => ({ key: "k-up", name: f.name, size: f.size, mime: f.type }),
    badge: () => null, mentionCount: () => 0, mentionTotal: () => 0, subscribe: () => () => {},
  }, { get: (t, k) => (k in t ? t[k] : inert) }));
  const open = function (kind, patch) {
    const a = this.active;
    for (const k of Object.keys(a)) delete a[k];
    Object.assign(a, { kind }, patch);
    this.closeRightPanel();
  };
  def("openTodos", function (spaceId, o) { open.call(this, "todos", { spaceId, ...(o && o.roomId ? { roomId: o.roomId } : {}) }); });
  def("signingFailedFor", () => false);
  def("knownRoomLabel", (n) => (n === R && !q.get("ticketHome") ? "#ops" : null));
  if (q.get("ticketMuted") === "1")
    def("spaceMutes", { until: () => "2099-01-01T00:00:00Z", mute: async () => {}, unmute: async () => {} });
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

For the ticket page, open the ticket route directly. Use a fresh query value
each time, because a hash-only change does not reload the fixture:

```bash
T='tools/visual/shell-fixture.html?view=room&alerts=quiet'
agent-browser open "$(control-om-chat url "$T&ticketFiles=2#/todo/s1/1")"
#   two file cards, "Attach a file to the ticket", the comment paperclip "Attach a file"
agent-browser open "$(control-om-chat url "$T&ticketFiles=10#/todo/s1/1")"
#   ten cards, no "Attach a file to the ticket"; the paperclip stays
agent-browser open "$(control-om-chat url "$T&ticketFiles=2&ticketMuted=1#/todo/s1/1")"
#   the mute banner; both attach buttons aria-disabled; Comment readOnly
agent-browser open "$(control-om-chat url "$T&ticketHome=archived#/todo/s1/1")"
#   Home channel "#ops (archived)" (also: deleted, private)
```

The ticket button's name contains the paperclip's, so match **Attach a file**
with `--exact`, or select by `aria-label`.

The fixture seeds the hash only when it is empty, so `#/projects/s1` reaches
`bindRouting`, which calls the stubbed `openTodos` at boot. On `/chat/` (base
`/chat/`, the cloud lane) the same URL works; the fixture then rewrites the
location to `/chat/projects/s1?view=room&alerts=quiet`.

For the channel panel, open `shell-fixture.html?view=room&alerts=quiet&panel=todos`
with the same two stubs and read the `complementary` **Tickets in #ops**. Press
**New ticket in #ops**, fill **TITLE**, and confirm **Create** turns enabled,
then press **Cancel**.

## Gotchas

- **The ticket page needs `todos.ticket`.** Without it, `#/todo/s1/1` routes
  and then the surface boundary shows **Projects could not load** ("Cannot
  convert object to primitive value"): `todos.ticket(ref)` answers `INERT`
  instead of a `TodoTicketController` (`lib/todos/ticket.ts:155`). The stub's
  controller returns one cached `state` object; a fresh object per read would
  loop `useSyncExternalStore`.
- **The Agent row reads "No agent Couldn't list your agents" with Retry.** The
  fixture lists no agents. That is a stub artefact.
- **No upload is proved.** The fixture cannot pick a file through the hidden
  input, and the stub's `upload` and the ticket controller's writes are
  no-ops. Uploading into the server's ticket file area, signing through
  `getRoomTodoAttachmentUrl` and the 403/404/429 handling
  (`lib/attachments-seam.ts`) need the daemon lane.
- **On `/chat/`, the first ticket render logs a React warning** about the
  `value` prop of a textarea. The only textarea then has a string value, and
  the warning does not appear on `/rooms/` or with `ticketMuted=1`. Its source
  is not traced.
- **Every column holds every ticket.** The stub returns the same ids for every
  view key, so the Board shows all three tickets under each column. The board
  layout and card menus are real; the per-column split is not.
- **Needs you renders empty.** The page queries the `needs-you` keys
  (`overdue`, `due_soon`, `assigned`, `in_progress`, `updates`), and the stub
  answers them empty, which hides the section.
- **CHANNEL reads "Deleted channel" without `knownRoomLabel`.** `homeName`
  asks `session.knownRoomLabel` and `todos.roomDeleted`; under `INERT` both
  answer truthy. The stub answers both, so the column reads `#ops`.
- **No write is proved.** Create, bulk changes, **Move to…**, the ticket's
  fields, comments and the filters hit `INERT` or the stub's no-ops. Proving a write needs a daemon-pair lane on a
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

**Last verified:** 2026-11-10 (nightly). **Product commit:** `eae9681d` (GitLab origin/main, rooms-client 0.115.0). **Scope:** with the people stub and the extended Projects stub, on `/rooms/` (18186) and `/chat/` (18187): the ticket page for `!1` (title, side-column note, file cards); with `ticketFiles=2`, **Attach a file to the ticket** and the comment paperclip; with `ticketFiles=10`, ten cards and no ticket Attach; with `ticketMuted=1`, the banner "You're muted in this server until Jan 1, 8:00 AM. You can read tickets but can't change them.", both attach buttons `aria-disabled="true"` with the mute sentence, and **Comment** read-only; the Home channel row as `#ops`, **Deleted channel** (both hosts), **Private channel** and `#ops (archived)` (`/rooms/`). On `/rooms/`, the table's CHANNEL column reads `#ops` in all three rows. **Limitations:** no upload, signing, comment or field write; Needs you and the per-column board split are unproved, as before. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261110/r1/`.

**Previous record:** 2026-11-09 (scheduled maintenance). **Product commit:** `16da8ecf` (GitLab origin/main; one CI-only commit past `82390825`). **Scope:** with the people and Projects stubs, on `/rooms/` (18141): **Projects** with "1 open · 1 in progress", the 11-column Table and 3 rows, **Board** with the regions Open, Assigned, In progress and Done, **More actions for !1** → **Move to…**, **Select Ship digest** → **Bulk actions** (8 controls), **!1 Fix alert dedupe** → `#/todo/s1/1`, `panel=todos` → **Tickets in #ops**, and **New ticket in #ops** → the form (with **Create** enabled after a title, then **Cancel**). On `/chat/` (18142): the Table and **Tickets in #ops**. **Limitations:** the ticket page fails to load (no ticket controller stub); no write, filter, move or Needs you item was exercised; the per-column board split is a stub artefact. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261109/r1/` (`01`–`10`).
