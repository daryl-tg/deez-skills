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
  ticket. Every change lands in Activity." (`TodoTicket.tsx:317`).
- **Ticket files** (`TodoAttachments.tsx`, `TicketFileTiles.tsx`; tiles since
  `bc11d746`). The files are tiles in `ul[aria-label="Ticket files"]`: an image
  is a button **Open <name>** (Enter from the keyboard opens the media viewer,
  `d7c3baf3`), a video **Play <name>**, another file a link **Download
  <name>**, or while unsigned an `aria-disabled` span titled **Preparing
  <name>**. Every tile has a × named **Remove <name> from the ticket**; removing
  toasts "Removed <name> from the ticket" with an **Undo** action that adds the
  key back (`TodoAttachments.tsx:236-245`). Below the files sits the button
  **Attach a file to the ticket** (text "Attach a file"). From source, any
  server member gets it, whatever the home channel allows. It renders only while
  the ticket's files plus its non-failed uploads number fewer than ten: at ten
  it is gone, with no disabled stand-in.
- **Paste and drop** (`ticket-file-inputs.tsx`; `8a0fca82`, `bb736b2d`). A file
  pasted anywhere on the page outside a text field joins the ticket's files
  through `todos.upload`; while it uploads its tile reads **Uploading** (×
  **Cancel uploading <name>**), and a failed upload reads **Upload failed** (×
  **Dismiss <name>**). Dragging files over the page raises two veils, "Drop to
  attach to the ticket" on the Description section (`[data-drop-zone=ticket]`)
  and "Drop to attach to the comment" on the comment box
  (`[data-drop-zone=comment]`); a drop elsewhere is refused.
- **Description** (`TodoDescription.tsx`; `dc47fdcb`, `661e05d8`, `bc0babe4`).
  The saved description keeps its line breaks. Each `- [ ]` task is a
  `span.task-list-marker[role=checkbox]` named by the task's text, with
  `aria-checked`; a click or Space ticks it in place through
  `ticket.saveDescription(text, baseRev)`, and a rejected tick toasts "The
  description changed before your tick saved. It shows the latest now." A
  ticket link reads as a pill, `button.ticket-ref` titled "Ticket !2, In
  progress, dax"; a role reads as its `.mention-pill.role-mention`. **Edit
  description** opens a CodeMirror editor where `!` lists the server's tickets
  and `@` its people and roles (`6c903a66`, `35cff699`), with the Vim status
  line at its foot (`a5dc8187`). The same renderer draws every Markdown task in chat
  messages, docs and agent cards, but there a marker is a read-only
  `span.task-list-marker[role=img]` named **Checked task** or **Unchecked
  task** (on `/rooms/`, `shell-fixture.html?view=room&alerts=quiet&tape=lists`
  shows one of each; `/chat/` has no `tape=lists` seed).
- **Comment box** (`TodoCommentBox.tsx`). The textbox **Comment** (placeholder
  "Add a comment"), the icon-only paperclip **Attach a file**, **Mention
  someone**, and **Comment** (disabled while empty). The paperclip caps the
  files staged on one comment at ten; the ticket's own ten-file cap does not
  touch it. A file pasted into the box or dropped on it stages there (its chip
  has **Remove attachment <name>**; "Uploading files for the comment…" while
  it uploads), and **Comment** posts with files and no text (`9cd9cf96`). `!`
  opens **TICKETS MATCHING !<query>** and `@` opens **MEMBERS & ROLES** with the
  server's roles; ArrowDown then Enter inserts the pick, which the backdrop
  paints as a pill (`composer-token-role`). With Vim mode on, the box runs the
  shared Vim engine: Escape enters NORMAL (`.ticket-comment-bar
  .composer-vim-mode[data-vim-mode]`), a block cursor `.vim-block-cursor`
  shows outside insert mode (`data-partial` while an operator is pending),
  and Ctrl/Cmd+Enter posts (`4f2accbc`, `a420490b`).
- **Comments** (`TodoActivity.tsx:126-300`). A comment's files are tiles in
  `ul[aria-label="Comment files"]`; one with no body and no surviving file reads
  "The file in this comment is no longer available.". **Edit** opens the shared
  edit box (`textarea[aria-label="Edit message"]`) with the comment's tiles
  (× **Remove <name> from the comment**), the paperclip **Attach a file to the
  comment**, the note "1 file removed · applies when you save" after a ×, and
  the same `!` ticket list.
- **Loading frame** (`TodoTicket.tsx:510-565`, `c99f628c`). While the ticket
  loads on a live connection, the page shows the **Projects** crumb, `!1`, the
  live region "Loading the ticket…" and skeleton bars.
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
  Pressing a row opens the ticket inside the panel (`ChannelTicket.tsx`,
  `dd968acb`): `complementary` **Ticket !1** with **Back to tickets in #ops**,
  the heading **!1 · #ops**, **Open in Projects**, **Follow** and **Close
  panel**; Escape goes back to the list. A ticket card in chat opens the same
  panel when its room is in the same server (`9ef780c2`).
- **New ticket form** (`TodoCreateForm.tsx`). It has the textboxes **TITLE** and
  **DESCRIPTION**, **Add a label**, **Priority** (No priority), **Due**,
  **Assignee** (Unassigned), **Home channel** (#ops), **Cancel** and
  **Create**. **Create** stays disabled until the title has text. TITLE is
  `aria-required` with an `aria-hidden` `*`; **Home channel** carries one too
  unless the home is fixed, as it is in the panel (`c99f628c`).
- **Message menu entry.** In records mode a message's **More** menu lists
  **Ticket** (aria "Make a ticket from this message", `MessageRow.tsx:1842`).
- **Projects switch** (`ProjectsSettings.tsx:70-190`; `b29feb5a`, `8d2014cc`).
  Server Settings → **Projects** holds a `role=switch` named **Projects**
  (`data-projects-switch`). Switching on first reads the mode: while that read
  is out the switch is `aria-disabled="true"` (never `disabled`, so focus
  stays); if to-dos still wait for migration, a `status` line reads "N to-dos
  in this server haven't moved to Projects yet. Ask for the migration to be
  run, then switch on again."; otherwise **Switch on Projects?** confirms.
  Switching off confirms with **Switch off Projects?**.

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

The stub reads these query parameters:

| Parameter | Effect |
|---|---|
| `ticketFiles=<n>` | ticket 1 holds n files (`file-N.txt`, which sign to null and render as **Preparing file-N.txt**) |
| `ticketFileKind=media` | the first two files are `mosaic-1.svg` and `clip.mov`, which the shell fixture signs, so they render as **Open** / **Play** tiles; with `ticketActivity=1` the comment carries `mosaic-1.svg` too |
| `ticketDesc=1` | ticket 1's description holds two tasks, a ticket link and a second line |
| `ticketActivity=1` | ticket 1 has one comment by the viewer (`u1`), "Blocked on !2 for now", so **Edit** shows |
| `ticketState=loading` | every ticket answers `status:"loading"` (the loading frame) |
| `upload=hold\|fail` | `todos.upload` never settles or rejects (Uploading / Upload failed tiles) |
| `projectsMode=records\|off\|pending\|hold` | what `todos.readMode` and `modeFor` answer, for the Server Settings switch |
| `ticketMuted=1` | mutes the viewer in the server |
| `ticketHome=deleted\|private\|archived` | changes the home chip |

The ticket controller is stateful: `setFields` applies `removeAttachmentKeys` /
`addAttachmentKeys` and notifies subscribers, and `saveDescription` stores the
text. Every write leaves a mark on `<html>`: `data-fixture-set-fields`,
`data-fixture-saved-description` (all saved texts), `data-fixture-comment`
(the `comment(body, keys, requestId)` arguments), `data-fixture-upload` and
`data-fixture-read-mode`.

```bash
cat > "$SCRATCH/fixture-projects-stub.js" <<'JS'
(() => {
  const S = "s1", R = "ops", ts = "2026-08-09T10:00:00Z";
  const def = (k, v) => Object.defineProperty(Object.prototype, k,
    { value: v, configurable: true, writable: true, enumerable: false });
  const mark = (k, v) => { document.documentElement.dataset[k] = typeof v === "string" ? v : JSON.stringify(v); };
  const q = new URLSearchParams(location.search);
  const desc = q.get("ticketDesc") === "1" ? "- [ ] draft the fix\n- [x] reproduce it\n\nsee om://todo/s1/2\nsecond line" : "";
  const rec = (n, title, status, priority) => ({
    id: `00000000-0000-4000-8000-00000000000${n}`, spaceId: S, number: n, roomId: R,
    topicId: null, title, description: n === 1 ? desc : "", descriptionRev: 1, attachments: [],
    status, assigneeId: n === 2 ? "u-dax" : null, assignedById: null, agent: null,
    priority, dueDate: null, labelIds: [], creatorId: "u-ana", people: {},
    sourceMessage: null, closedById: null, closedAt: null, createdAt: ts,
    updatedAt: ts, lastActivityAt: ts, rev: 1, todoSeq: n, legacy: null,
    legacyAssigneeHandle: null });
  const recs = [rec(1, "Fix alert dedupe", "open", "high"),
                rec(2, "Ship digest", "in_progress", "medium"),
                rec(3, "Close the loop", "done", "none")];
  const files = Number(q.get("ticketFiles") || 0);
  const media = q.get("ticketFileKind") === "media";
  const fileOf = (i) => media && i === 0 ? { key: "mosaic-1.svg", name: "mosaic-1.svg", size: 1200, mime: "image/svg+xml", scanStatus: "clean" }
    : media && i === 1 ? { key: "clip.mov", name: "clip.mov", size: 52000, mime: "video/quicktime", scanStatus: "clean" }
    : { key: `k${i + 1}`, name: `file-${i + 1}.txt`, size: 1200 + i, mime: "text/plain", scanStatus: "clean" };
  recs[0].attachments = Array.from({ length: files }, (_, i) => fileOf(i));
  const byId = new Map(recs.map(r => [r.id, r]));
  const tickets = new Map();
  const comment = q.get("ticketActivity") === "1" ? [{
    type: "comment",
    event: { id: "e9", todoId: recs[0].id, spaceId: S, rev: 2, todoSeq: 2, kind: "comment_added",
      actor: { userId: "u1", isAgent: false, source: "gui" }, changes: {}, at: ts, commentId: "c1" },
    comment: { id: "c1", todoId: recs[0].id, authorId: "u1", body: "Blocked on !2 for now",
      attachments: media ? [{ key: "mosaic-1.svg", name: "mosaic-1.svg", size: 1200, mime: "image/svg+xml", scanStatus: "clean" }] : [],
      mentions: [], createdAt: ts, editedAt: null, deletedAt: null } }] : [];
  const ticketFor = (ref) => {
    const key = ref.todoId ?? `${ref.spaceId}/${ref.number}`;
    if (tickets.has(key)) return tickets.get(key);
    const todo0 = ref.todoId ? byId.get(ref.todoId)
      : recs.find(r => r.spaceId === ref.spaceId && r.number === Number(ref.number));
    const loading = q.get("ticketState") === "loading";
    let state = { status: loading ? "loading" : todo0 ? "ready" : "not-found", todo: loading ? null : todo0 ?? null,
      followers: [], activity: todo0 && todo0.number === 1 ? comment : [],
      olderBefore: null, descriptionRev: todo0?.descriptionRev ?? 0, sourceMessageInfo: null };
    const subs = new Set();
    const set = (patch) => { state = { ...state, ...patch }; subs.forEach((f) => f()); };
    const saved = [];
    const c = { state: () => state, subscribe: (f) => { subs.add(f); return () => subs.delete(f); },
      release() {}, dispose() {}, caughtUp() {},
      retry: async () => {}, loadOlder: async () => {}, todoId: () => todo0?.id ?? null,
      spaceId: () => todo0?.spaceId ?? ref.spaceId ?? null,
      setFields: async (p) => {
        mark("fixtureSetFields", p);
        const t = state.todo; if (!t) return;
        let att = t.attachments;
        if (p.removeAttachmentKeys) att = att.filter((a) => !p.removeAttachmentKeys.includes(a.key));
        if (p.addAttachmentKeys) att = att.concat(p.addAttachmentKeys.filter((k) => !att.some((a) => a.key === k))
          .map((k) => (todo0.attachments.find((a) => a.key === k) ?? { key: k, name: k, size: 10, mime: "image/png", scanStatus: "clean" })));
        set({ todo: { ...t, attachments: att, rev: t.rev + 1 } });
      },
      saveDescription: async (text, baseRev) => { saved.push(text); mark("fixtureSavedDescription", saved);
        set({ todo: { ...state.todo, description: text, descriptionRev: baseRev + 1 }, descriptionRev: baseRev + 1 }); return baseRev + 1; },
      remove: async () => {}, follow: async () => {},
      comment: async (...a) => { mark("fixtureComment", a); }, editComment: async (...a) => { mark("fixtureEditComment", a); }, deleteComment: async () => {} };
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
  const uploadMode = q.get("upload");
  const pm = q.get("projectsMode");
  const modeResult = pm === "pending" ? { supported: true, mode: "off", readiness: { legacyTodos: 2, restricted: 1, pending: 3 } }
    : { supported: true, mode: pm === "off" ? "off" : "records", readiness: { legacyTodos: 0, restricted: 0, pending: 0 } };
  def("todos", new Proxy({
    modeFor: () => (pm === "off" || pm === "pending" || pm === "hold" ? "off" : "records"), recordsOn: () => pm !== "off" && pm !== "pending" && pm !== "hold", memberOf: () => true,
    spaceForRoom: () => S, today: () => "2026-08-09", switchedAt: () => "2026-08-01T00:00:00Z",
    record: (id) => byId.get(id), view: viewFor,
    refreshView() {}, releaseView() {}, loadMore() {},
    labels: () => labelList, refreshLabels() {}, watchLabels: () => () => {},
    labelsFailed: () => false, labelCreation: () => null, roomLabel: () => "#ops",
    ticket: ticketFor, homesVersion: () => 0, follow: async () => {},
    ticketTitle: (_s, n) => byNumber(n)?.title,
    readMode: () => { mark("fixtureReadMode", "1"); return pm === "hold" ? new Promise(() => {}) : Promise.resolve(modeResult); },
    setMode: async (_s, m) => mark("fixtureSetMode", m), setLabelCreation: async () => {},
    lookup: { prefetch: async () => {}, rows: lookupRows, release: () => {} },
    refs: { hold: () => () => {}, subscribe: () => () => {}, setFollowing() {},
      title: (_s, n) => byNumber(n)?.title,
      get: (ref) => refStateFor(`${ref.spaceId}/${ref.number}`, ref.spaceId === S ? byNumber(ref.number) : undefined) },
    roomDeleted: () => q.get("ticketHome") === "deleted",
    archivedHome: () => (q.get("ticketHome") === "archived" ? "#ops (archived)" : null), forgetLabel() {},
    upload: (_s, f) => { mark("fixtureUpload", f.name);
      return uploadMode === "hold" ? new Promise(() => {}) : uploadMode === "fail" ? Promise.reject(new Error("upload failed"))
        : Promise.resolve({ key: "k-up", name: f.name, size: f.size, mime: f.type }); },
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

Press the row "Fix alert dedupe !1 Open High" in that panel to open the ticket
inside it (`complementary` **Ticket !1**); Escape returns to **Tickets in #ops**.

### Files, paste, drop, tasks and comments (driven 2026-11-13)

Load the people stub, this stub and the session-capture shim
([message-actions.md](message-actions.md#forward-through-the-session-capture-shim-added-2026-11-09))
in that order. The shell fixture's `toast` is a no-op outside the persona
scene, so capture it before driving a remove:

```bash
T='tools/visual/shell-fixture.html?view=room&alerts=quiet'
agent-browser open "$(control-om-chat url "$T&ticketFiles=3&ticketFileKind=media&_s=1#/todo/s1/1")"
#   tiles: "Open mosaic-1.svg", "Play clip.mov", span "Preparing file-3.txt"
agent-browser eval '(()=>{const b=document.querySelector("button[aria-label=\"Open mosaic-1.svg\"]");b.focus();return 1})()'
agent-browser press Enter            # dialog with the image; Escape closes it
agent-browser eval '(()=>{const o=window.__om;window.__toasts=[];o.toast=(t,k,a)=>{window.__toasts.push({t,k,a})};return 1})()'
agent-browser find role button click --name "Remove clip.mov from the ticket"
agent-browser eval 'window.__toasts.at(-1).t'    # "Removed clip.mov from the ticket" (action label Undo)
agent-browser eval 'window.__toasts.at(-1).a.run(); 1'   # clip.mov's tile returns
```

Paste and drop are synthetic events, not OS gestures (see
[README.md](README.md) on OS file drops). Dispatch them on `.ticket-page`, on
`textarea[aria-label=Comment]` or on a `[data-drop-zone]`:

```bash
agent-browser open "$(control-om-chat url "$T&ticketFiles=1&upload=hold&_s=2#/todo/s1/1")"
agent-browser eval '(()=>{const dt=new DataTransfer();dt.items.add(new File(["x"],"a.png",{type:"image/png"}));document.querySelector(".ticket-page").dispatchEvent(new ClipboardEvent("paste",{clipboardData:dt,bubbles:true,cancelable:true}));return 1})()'
#   tile "a.png Uploading" with "Cancel uploading a.png" (upload=fail: "Upload failed", "Dismiss a.png")
agent-browser eval '(()=>{const dt=new DataTransfer();dt.items.add(new File(["x"],"b.png",{type:"image/png"}));const p=document.querySelector(".ticket-page");for(const t of ["dragenter","dragover"])p.dispatchEvent(new DragEvent(t,{dataTransfer:dt,bubbles:true,cancelable:true}));return 1})()'
#   [data-drop-zone=ticket][data-drop] "Drop to attach to the ticket", [data-drop-zone=comment][data-drop] "Drop to attach to the comment"
```

A files-only comment: open `$T&ticketFiles=1#/todo/s1/1`, paste a file on the
**Comment** textbox (the chip reads **Remove attachment d.png**), and click
**Comment** with the text empty. `data-fixture-comment` reads `["",["k-up"],"<request id>"]`.

Description and comments: open `$T&ticketFiles=1&ticketDesc=1&ticketActivity=1&ticketFileKind=media#/todo/s1/1`.

- `find role checkbox click --name "draft the fix"` flips it to
  `aria-checked="true"`, and `data-fixture-saved-description` gains
  `- [x] draft the fix…`. Focusing a marker and pressing Space ticks it too.
- `button.ticket-ref` is titled "Ticket !2, In progress, dax", and the text
  after the link stays on its own line.
- The comment's **Edit** (the button whose name is exactly "Edit") opens
  `textarea[aria-label="Edit message"]` with **Remove mosaic-1.svg from the
  comment** and **Attach a file to the comment**; a × adds "1 file removed ·
  applies when you save". Typing ` !ship` lists **TICKETS MATCHING !ship**;
  ArrowDown then Enter makes the value end in `!2 Ship digest `.
- In the comment box, `ping @dev` → **MEMBERS & ROLES** **@Devops ROLE** →
  ArrowDown, Enter → `ping @Devops ` with a `composer-token-role` chip.
- Vim: `localStorage.setItem("om.chat.vimMode","true")`, reopen, click
  **Comment**, type, press Escape → `.ticket-comment-bar
  .composer-vim-mode[data-vim-mode=normal]` and one `.vim-block-cursor`; `0`,
  `d` → `.composer-vim-pending` and `data-partial`; `w` deletes the word.

`$T&ticketState=loading#/todo/s1/1` shows the live region "Loading the
ticket…". `$T&panel=todos` → **New ticket in #ops** shows TITLE
`aria-required` with one `aria-hidden` `*`.

### The Server Settings Projects switch (driven 2026-11-13)

Same three init scripts, on `tools/visual/settings-fixture.html` (or the
`/chat/` twin) with `?host=server&page=projects&perms=owner`:

- `projectsMode=records`: **Projects** `role=switch`, `aria-checked="true"`.
- `projectsMode=pending`: `aria-checked="false"`; clicking it reads the mode
  (`data-fixture-read-mode`) and shows the `status` line "3 to-dos in this
  server haven't moved to Projects yet. Ask for the migration to be run, then
  switch on again."
- `projectsMode=hold`: clicking leaves the switch `aria-disabled="true"`,
  unchecked and focused while the read never settles.

The confirmations (**Switch on Projects?**, **Switch off Projects?**) are not
reachable: the settings fixtures spell `openConfirm` as a no-op. Without the
Projects stub the page falls to its error boundary, because the bare
`session.todos` is the inert proxy.

## Gotchas

- **The ticket page needs `todos.ticket`.** Without it, `#/todo/s1/1` routes
  and then the surface boundary shows **Projects could not load** ("Cannot
  convert object to primitive value"): `todos.ticket(ref)` answers `INERT`
  instead of a `TodoTicketController` (`lib/todos/ticket.ts:155`). The stub's
  controller returns one cached `state` object; a fresh object per read would
  loop `useSyncExternalStore`.
- **The Agent row reads "No agent Couldn't list your agents" with Retry.** The
  fixture lists no agents. That is a stub artefact.
- **No real upload is proved.** The fixture cannot pick a file through the
  hidden input, and the stub's `upload` answers at once (or holds or fails on
  `upload=`). Paste and drop are synthetic events. Uploading into the server's
  ticket file area, signing through `getRoomTodoAttachmentUrl` and the
  403/404/429 handling (`lib/attachments-seam.ts`) need the daemon lane.
- **The remove toast needs the capture shim.** The shell fixture's `toast` is a
  no-op outside the persona scene, so without the shim a remove shows no
  toast and **Undo** cannot be pressed.
- **A ticket card opens in the panel only with a shim `showRightPanel`.** On
  `/rooms/`, send `om://todo/s1/1` alone (a local send appends the card), then
  set `__om.showRightPanel=(p)=>{__om.rightPanel=p;__om.closeConfirm()}`
  through the capture shim: clicking the card's title **Fix alert dedupe**
  opens **Tickets in #ops** with **Ticket !1** (`TodoRefCard.tsx:68-75`;
  driven 2026-11-13). The root shell fixture does not define
  `showRightPanel`, so without the shim the click does nothing. The ticket
  list closing on send stays source only.
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
- **No write reaches a store.** Create, bulk changes, **Move to…**, the
  ticket's fields and the filters hit `INERT` or the stub's no-ops. The stub
  records remove, re-add, comment and description calls, which proves the
  call the UI makes, not that the relay accepts it. Proving a write needs a daemon-pair lane on a
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

**Last verified:** 2026-11-13 (nightly maintenance). **Product commit:** `504b08d5` (GitLab origin/main; rooms-client 0.117.0; 32 commits past `eae9681d`). **Scope:** people stub, the extended Projects stub above and the session-capture shim, on `/rooms/` (18170) and `/chat/` (18171). Both hosts: tiles **Open mosaic-1.svg** / **Play clip.mov** / **Preparing file-3.txt**, description ticks (`saveDescription` called), the pill "Ticket !2, In progress, dax", the comment `!` list, a page paste reaching `setFields({addAttachmentKeys})` and, in the final re-drive with the published stubs, × remove with the **Undo** toast and a held **Uploading** tile, the channel-panel ticket **Ticket !1** (Back, Escape) and the Server Settings **Projects** switch (on, pending line, held read). `/rooms/` only: keyboard image open, paste → **Upload failed**, the drag veils, a drop and a paste into the comment, a files-only comment, a comment's **Edit** with tiles and the `!` list, `@` roles, the comment box's Vim, the loading frame, the required TITLE mark, and a sent card opening in the panel (shim `showRightPanel`). **Limitations:** no write reaches a store; paste and drop are synthetic; the description editor's lists, the Settings confirmations and Needs you were not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261113/r1/` (frames 01-12, 26-32, 40).

**Previous record:** 2026-11-10 (scheduled maintenance). **Product commit:** `eae9681d` (GitLab origin/main, rooms-client 0.115.0). **Scope:** the muted ticket (`ticketFiles=2&ticketMuted=1#/todo/s1/1`) on `/rooms/` (18141) and `/chat/` (18142), probed with `[aria-disabled=true][aria-describedby]`: twelve controls on each host (the title, **Status**, **Assignee**, **Add a label**, **Priority**, **Set due date**, **Add description**, **Attach a file to the ticket**, the **Comment** box, **Attach a file**, **Mention someone** and the **Comment** button), every one focusable, none `disabled`, each described by "You're muted in this server until Jan 1, 8:00 AM.". **Limitations:** no write was attempted. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261110/r1/` (frames 20-21).

**Previous record:** 2026-11-10 (nightly). **Product commit:** `eae9681d` (GitLab origin/main, rooms-client 0.115.0). **Scope:** with the people stub and the extended Projects stub, on `/rooms/` (18186) and `/chat/` (18187): the ticket page for `!1` (title, side-column note, file cards); with `ticketFiles=2`, **Attach a file to the ticket** and the comment paperclip; with `ticketFiles=10`, ten cards and no ticket Attach; with `ticketMuted=1`, the banner "You're muted in this server until Jan 1, 8:00 AM. You can read tickets but can't change them.", both attach buttons `aria-disabled="true"` with the mute sentence, and **Comment** read-only; the Home channel row as `#ops`, **Deleted channel** (both hosts), **Private channel** and `#ops (archived)` (`/rooms/`). On `/rooms/`, the table's CHANNEL column reads `#ops` in all three rows. **Limitations:** no upload, signing, comment or field write; Needs you and the per-column board split are unproved, as before. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261110/r1/`.

**Previous record:** 2026-11-09 (scheduled maintenance). **Product commit:** `16da8ecf` (GitLab origin/main; one CI-only commit past `82390825`). **Scope:** with the people and Projects stubs, on `/rooms/` (18141): **Projects** with "1 open · 1 in progress", the 11-column Table and 3 rows, **Board** with the regions Open, Assigned, In progress and Done, **More actions for !1** → **Move to…**, **Select Ship digest** → **Bulk actions** (8 controls), **!1 Fix alert dedupe** → `#/todo/s1/1`, `panel=todos` → **Tickets in #ops**, and **New ticket in #ops** → the form (with **Create** enabled after a title, then **Cancel**). On `/chat/` (18142): the Table and **Tickets in #ops**. **Limitations:** the ticket page fails to load (no ticket controller stub); no write, filter, move or Needs you item was exercised; the per-column board split is a stub artefact. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261109/r1/` (`01`–`10`).
