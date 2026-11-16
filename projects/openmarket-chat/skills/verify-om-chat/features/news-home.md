# News home

The **News** view: stories the operator's news watches have fired, plus filing
one into a room so it rides the next message. Source:
`packages/chat-ui/src/components/NewsHomePane.tsx`, mounted by
`ChatPane.tsx:808-814` when `session.active.kind === "news"`; the composer chip
is `NewsStagedChip` in `NewsCard.tsx`.

## Sub-features

- **The wire** (`NewsHomePane.tsx`): an `h1` **News**, a `role=feed` of
  stories (titles are `h2`/`h3`), the **On the wire** heading with a
  **Wire layout** group (**List**, **Cards**), and **Mark all N read**.
- **Your watches**: one row per news watch with its sync state, for example
  **CPI watch** "Live · chat only".
- **File a story into a room**: **File to a room** on a story
  (`NewsHomePane.tsx:573`) stages it. The row then reads "Staged — it rides
  your next message in a room." with **Undo**. In a public channel's composer
  the story shows as a chip ("attaches below your message") with **Remove
  attached story** (`NewsCard.tsx:153`).
- **Related story suggestion** in the composer (**Attach**, **Dismiss story
  suggestion**), from `session.news.matchDraft`. Not reachable: see Gotchas.
- The rail's **News** feature (`Shell.tsx:2534-2545`) and the `news` key
  binding (`:907`) exist only when `session.news.supported === true`, which
  needs a daemon news plane behind the origin.

## How to get to it (user POV)

Press **News** on the rail, or go to `#/news`. Read the wire, switch between
list and cards, and press **File to a room** on a story. Then open a channel:
the story waits in the composer and goes out under your next message.

## Driving it with control-om-chat

Neither fixture can reach the view on its own. `#/news` calls
`session.openNews()`, which neither fixture defines, and the fixture `news`
store is an inert plain object with `supported: false`
(`tools/visual/shell-fixture.tsx:2768-2782`). There is no `?view=news`. With the
people stub and the session-capture shim from
[message-actions.md](message-actions.md), replace the `news` store and point
`active` at the view. Keep the original `active` descriptor so you can return
to a room:

```bash
cat > "$SCRATCH/news-seed.js" <<'JS'
(() => {
  const o = window.__om; const now = Date.now();
  const fire = (i, outcome) => ({ watchId: "w1", eventId: "e" + i, watchLabel: "CPI watch", slug: "cpi-" + i,
    title: "CPI prints hot, story " + i, outcome, createdAt: new Date(now - i * 6e4).toISOString(),
    sourceSortMs: now - i * 6e4, summary: "Core CPI beat consensus.", sourceUrl: "https://example.com/" + i });
  const n = { supported: true, fires: [fire(1, "major_update"), fire(2, "update")],
    watches: [{ id: "w1", label: "CPI watch", notifyChannels: [] }], sync: new Map(), lastError: null, brief: null,
    stagedStory: null, unreadCount: () => 0, unreadKeys: () => new Set(), markSeen() {}, markAllSeen() {},
    matchDraft: () => null, observeDraft() {}, dismissDraftMatch() {},
    clearStagedStory() { n.stagedStory = null; o.closeConfirm(); },
    stageStory(f) { n.stagedStory = f; o.closeConfirm(); }, attachBlock: () => "" };
  for (const k of Object.keys(o.news || {})) if (!(k in n)) n[k] = o.news[k];
  o.news = n;
  window.__activeDesc = Object.getOwnPropertyDescriptor(o, "active");
  Object.defineProperty(o, "active", { configurable: true, get: () => ({ kind: "news" }) });
  o.closeConfirm();
  return 1;
})()
JS
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=room&alerts=quiet')"
agent-browser eval "$(cat "$SCRATCH/news-seed.js")"
# h1 "News"; headings: CPI prints hot, story 1 / On the wire / CPI prints hot, story 2 / Your watches
agent-browser find role button click --name "File to a room"
# "Staged" line and an Undo button; __om.news.stagedStory.title === "CPI prints hot, story 1"
agent-browser eval '(()=>{const o=window.__om;Object.defineProperty(o,"active",window.__activeDesc);o.closeConfirm();return 1})()'
# back in #ops: the composer chip "CPI prints hot, story 1 / attaches below your message",
# button "Remove attached story"
```

`outcome` must be one of `corroboration`, `update` or `major_update`
(`lib/news-format.ts:25`). The store fields `NewsHomePane` reads are `fires`,
`watches`, `sync` (a `Map`), `lastError`, `brief`, `unreadKeys()`,
`markSeen()`, `markAllSeen()`, `stageStory()` and `clearStagedStory()`.

## Gotchas

- **The fixture `news` store crashes the pane if you only flip `active`.** It
  is a plain object, so missing members are `undefined`, not `INERT`, and
  `unreadKeys()` runs in a `useState` initializer. Replace the whole store.
- **`active` is a getter with no setter.** A plain `__om.active = …` does
  nothing. Use `Object.defineProperty`, and restore the saved descriptor to
  leave the view.
- **The seeded store is not the daemon.** Unread counts, sync and backfill
  rows, the brief and the wire's paging come from the daemon's news RPCs. Read
  this guide as proof of rendering and staging, not of delivery. Sending a
  message with the chip attached was not driven.
- **The Related story strip is unreachable.** Both fixtures answer
  `matchDraft: () => null`, and the seed above keeps that. The two-word and
  rarity-weighted matching is covered by `test/ui/news-format.test.ts` only.
- `lib/news.ts` holds a raw NUL byte, so plain `grep` reports no matches. Use
  `grep -a`.

### Verification record

**Last verified:** 2026-11-16 (nightly maintenance). **Product commit:** `96644a29` (GitLab origin/main; rooms-client 0.118.0; unchanged since the 2026-11-15 pass). **Scope:** `/rooms/` (18177) and `/chat/` (18178), people stub, session-capture shim and the seed above: the News home with two stories, **On the wire**, **Your watches** and **Mark all 2 read**; **File to a room** → the Staged line and **Undo** (`/rooms/`); back in `#ops`, the composer chip with **Remove attached story** on both hosts. **Limitations:** seeded store only, with no daemon news plane; the rail button, `#/news`, the brief, sync rows, the Related story strip and the send with a staged story were not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261116/r1/` (frames 07-10).
