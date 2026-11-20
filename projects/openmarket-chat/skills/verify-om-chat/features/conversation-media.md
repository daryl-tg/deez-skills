# Media and files in a conversation

One dialog lists everything shared in a channel, a topic, a DM or a group DM:
photos and videos as a grid, documents as a list (`7e3f0cde`, #chat 3391).

## Sub-features

- **The door in a channel or topic** is a row in the header's **More channel
  actions** menu, between **Summon your om** and **Channel settings**. It reads
  **Media and files**, or **Topic media and files** while a topic is open
  (`packages/chat-ui/src/components/ConversationMediaEntry.tsx:44-52`,
  `ChatPane.tsx:1321`). The topics list header carries the same row
  (`TopicListView.tsx:497`). The menu now has 14 items in `#ops`.
- **The door in a DM or group DM** is a header icon button named **Media and
  files** (`[data-conversation-media]`, `aria-haspopup="dialog"`), after
  **Nudge** and before the search buttons (`ConversationMediaEntry.tsx:65-75`,
  `ChatPane.tsx:1430`).
- **On a phone** the row sits in the header's ⋯ sheet, and the dialog takes over
  the screen (`mobilePresentation="takeover"`,
  `ConversationMediaDialog.tsx:125`) with a three-column grid.
- **The dialog** is titled **Media and files** (`ConversationMediaDialog.tsx:121`)
  and holds a tablist named **Shared in this conversation** (`:141`) with two
  tabs, **Media** and **Files**, each with a count. **Media** is selected first.
- **Media** is a grid (`[data-media-grid]` of `.media-grid-tile`,
  `MediaGallery.tsx:670-675`). A tile opens the lightbox on that item. The
  lightbox pages across every loaded item with **Previous image** and **Next
  image** (`MediaGallery.tsx:1806`, `:1815`), names the sender and time, and
  counts "1/25". **Escape** closes the lightbox and leaves the dialog open.
- **Files** is a list (`.conversation-media-file`): the file card with its
  **Download <name>** link, then "sender · time".
- **Paging.** A page is 25 messages with attachments, newest first
  (`lib/conversation-media.ts:43`). The footer reads "Newest 25 of 31 messages
  with attachments" with **Load older**, then "All 31 messages with
  attachments". Past 1000 it reads "Newest 1000 messages with attachments; older
  ones aren't listed here" (`ConversationMediaDialog.tsx:235-240`; the cap is
  source only).
- **Empty, loading and failure copy.** "Loading what was shared...", "No photos
  or videos shared here yet." / "No files shared here yet." with the footer
  "Nothing shared yet", and "Couldn't load what was shared: <reason>" with
  **Retry** (`:167`, `:226`).
- **Reopening keeps what was loaded** (`bc2ffd55`, #chat 3413;
  `lib/conversation-media.ts:296-338`). The session keeps the loaded pages of
  the six most recent conversations. A reopen paints them on the first frame
  with no "Loading what was shared...", then re-reads only the newest page and
  merges it: new items go on top, deleted ones in that window drop, and older
  pages and the **Load older** position stay. **Load older** is disabled while
  that refresh runs (`ConversationMediaDialog.tsx:246`). After a failed load
  the conversation is forgotten, so **Retry** starts again from the newest
  page (`:228`).
- **A tile that cannot load** shows "Image unavailable" with **Retry**
  (`MediaRetryBox`, `MediaGallery.tsx:789-798`).
- The list comes from `session.search.attachmentsPage(target, cursor)`
  (`lib/search-seam.ts:318`, `:589`), which asks the store for messages with
  `has: attachment`. A topic narrows the request to that topic.

## How to get to it (user POV)

In a channel or a topic, open the **…** menu in the header and choose **Media
and files**. In a DM, press the picture button in the header. Switch between
**Media** and **Files**, press **Load older** for earlier ones, and press a
picture to see it large and step through the others with the arrows.

## Driving it with control-om-chat

The root shell fixture seeds 31 messages with one image each, and a document on
every fourth (`tools/visual/shell-fixture.tsx:4558`, `:4634`). The seed needs
no query parameter and answers the same for every conversation. Since
`bc2ffd55` it logs each page it serves on `window.__fixtureAttachmentPages`,
and `?mediaDelay=<ms>` makes each answer wait, so a proof can count the reads
and see the first frame of a reopen.

```bash
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=room&alerts=quiet')"
agent-browser find role button click --name "More channel actions"
agent-browser find role menuitem click --name "Media and files"
agent-browser eval '(()=>{const d=document.querySelector(".conversation-media-dialog");return JSON.stringify({tabs:[...d.querySelectorAll("[role=tab]")].map(t=>t.textContent.trim()),tiles:d.querySelectorAll("[data-media-grid] .media-grid-tile").length,foot:[...d.querySelectorAll("[aria-live]")].map(e=>e.textContent.trim())})})()'
#   tabs ["Media25","Files6"], tiles 25, foot "Newest 25 of 31 messages with attachments" + Load older
agent-browser find role button click --name "Open photo-31.svg"     # .ui-lightbox, "ren … photo-31.svg · 1/25"
agent-browser find role button click --name "Next image"            # photo-30.svg · 2/25
agent-browser press Escape                                          # lightbox closes, dialog stays
agent-browser find role button click --name "Load older"            # Media31, Files8, "All 31 messages with attachments"
agent-browser find role tab click --name "Files"                    # 8 rows, first "positions.xlsx 341 KB Download mika · …"
agent-browser press Escape                                          # dialog closes, focus returns to More channel actions
```

Other doors, same dialog and counts:

- **Topic:** `?view=topic&topic=cpi-print-aug&alerts=quiet`, then the menu row
  **Topic media and files**.
- **Topics list:** press **Topics** in the `#ops` header (`#/room/ops/topics`),
  then the menu row **Media and files**.
- **DM:** `?view=dm&dm=ana&alerts=quiet`, then
  `agent-browser click '[data-conversation-media]'`. The group DM
  `dm=OM%20chatters` has the button too.
- **Phone:** start the session with `open about:blank` and
  `set viewport 390 844`, open the room route, press **More channel actions**
  and pick **Media and files** from the sheet. The dialog carries
  `ui-dialog-mobile-takeover`, is 390 px wide and its grid has three 127 px
  columns.

Reopen (added 2026-11-21), on `?view=room&alerts=quiet&mediaDelay=800`. Give
the menu half a second to open before clicking its row:

```bash
agent-browser find role button click --name "More channel actions"
agent-browser find role menuitem click --name "Media and files"     # after ~1 s: Media 25, Files 6; log [0]
agent-browser find role button click --name "Load older"            # Media 31, Files 8; log [0,1]
agent-browser press Escape
agent-browser find role button click --name "More channel actions"
agent-browser find role menuitem click --name "Media and files"
# read at once (150 ms): 31 tiles, "All 31 messages with attachments", no "Loading what was shared..."
agent-browser eval 'JSON.stringify(window.__fixtureAttachmentPages)'   # [0,1,0]: one refresh of the newest page
```

The failure and empty states need the session-capture shim (README), because
the seed always answers:

```bash
agent-browser eval '(()=>{const o=window.__om;window.__orig=o.search.attachmentsPage;
  o.search.attachmentsPage=async()=>{throw new Error("relay timeout")};return 1})()'
#   open the dialog: "Couldn't load what was shared: relay timeout" and Retry
agent-browser eval '(()=>{window.__om.search.attachmentsPage=window.__orig;return 1})()'
agent-browser find role button click --name "Retry"                 # Media 25, Files 6
agent-browser eval '(()=>{window.__om.search.attachmentsPage=async()=>({media:[],files:[],messages:0,page:0,total:0,token:"t",hasMore:false});return 1})()'
#   reopen: "No photos or videos shared here yet." / Files: "No files shared here yet." / footer "Nothing shared yet"
```

### On `/chat/`

The cloud fixture's search seam has no `attachmentsPage`
(`apps/cloud/tools/visual/shell-fixture.tsx:1672`, `:2541-2562`). The menu row
is there, and choosing it opens nothing: the dialog throws
"session.search.attachmentsPage is not a function" and its lazy-surface gate
swallows the error. Only the lane log and the browser console show it. Assign
a page function through the session-capture shim **before the first open** (a
failed open stays failed until the page reloads):

```bash
agent-browser eval '(()=>{const o=window.__om;const page=(p)=>{const total=31,people=["ana","ren","mika"],docs=["Q4 macro notes.pdf","funding-rates.csv","deck-v3.key","positions.xlsx"];const start=p*25,count=Math.max(0,Math.min(25,total-start));const media=[],files=[];for(let i=0;i<count;i++){const n=total-(start+i);const base={senderName:people[n%3],isAgent:false,ts:Date.UTC(2026,10,19,12)-(start+i)*3600000};media.push({...base,id:`m${n}:img`,attachment:{key:`fixture/mosaic-${n}.svg`,name:`photo-${n}.svg`,size:48000+n*911,mime:"image/svg+xml"}});if(n%4===1)files.push({...base,id:`m${n}:doc`,attachment:{key:`fixture/doc-${n}`,name:docs[((n-1)/4)%4],size:120000+n*7919,mime:"application/octet-stream"}});}return {media,files,messages:count,page:p,total,token:"fixture",hasMore:start+count<total,newest:count?Date.UTC(2026,10,19,12)-start*3600000:null,oldest:count?Date.UTC(2026,10,19,12)-(start+count-1)*3600000:null};};
  o.search.attachmentsPage=async(_t,c)=>page((c&&c.page)||0);return 1})()'
```

With it the dialog shows the same tabs, counts, footer and **Load older**. The
cloud fixture cannot sign the image keys, so every tile reads "Image
unavailable" with **Retry**. That is the only place this map reaches the
retry box.

The page function returns `newest` and `oldest` (added 2026-11-21): the reopen
merge reads them, as the root seed's pages now carry them
(`tools/visual/shell-fixture.tsx:4680-4681`). With them, a reopen on `/chat/`
kept 31 tiles on the first frame, and a counter in the page function read
`[0,1,0]`.

## Gotchas

- The seed ignores its target, so a channel, a topic and a DM all list the same
  31 messages. Topic narrowing and real senders need a store session.
- A failed open on `/chat/` is silent on the page. Read the console
  (`agent-browser console`) when a menu click seems to do nothing.
- The tiles' accessible names are **Open <file name>**. `.media-grid-tile` is a
  `div`; the button is inside it.
- With `?search=live` the fixture swaps in the real search seam, which has no
  store behind it. That route was not driven.
- What a reopen keeps lives in the page's session object. A reload, or a new
  `attachmentsPage` that returns different items, is not a reopen. The merge
  of a changed newest page and the six-conversation limit were not driven: the
  seed is static.
- The Files rows in a room use a forced download link; in a DM they use the DM
  file card. Neither download was followed.

### Verification record

**Last verified:** 2026-11-21 (nightly maintenance). **Product commit:** `84e88e56` (GitLab origin/main; rooms-client 0.124.0; 33 commits past `7e3f0cde`). **Scope:** `/rooms/` (18193), `?view=room&mediaDelay=800`: the channel door, 25 tiles and **Media 25 / Files 6** after one read, **Load older** → 31 and 8 after a second, then close and reopen: 31 tiles and "All 31 messages with attachments" on the first frame, no loading text, and `window.__fixtureAttachmentPages` `[0,1,0]`. `/chat/` (18194): the same with a shim-assigned page function that returns `newest` and `oldest`. **Limitations:** the merge of a changed newest page, the disabled **Load older** during a refresh, **Retry** after a failed **Load older**, the six-conversation limit, and the other doors were not driven tonight; the earlier limitations stand. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261121/r1/` (frames 08, 23).

**Previous record:** 2026-11-20 (nightly maintenance). **Product commit:** `7e3f0cde` (GitLab origin/main; rooms-client 0.122.0; 16 commits past `12f1ea24`). **Scope:** `/rooms/` (18193): the channel, topic, topics-list, DM and phone doors; 25 tiles and **Media 25 / Files 6**; the lightbox with **Next image** and **Previous image** and Escape; **Load older** → 31 and 8; the Files rows; Escape returning focus; the failure, **Retry** and empty states through the shim. `/chat/` (18194): the menu row, the silent failure, then the dialog with a shim-assigned page function (25 tiles reading "Image unavailable", **Files 8** after **Load older**). **Limitations:** the seed ignores its target, so topic narrowing is not shown; the 1000 cap, a real download, a video tile and `?search=live` were not driven; the DM door was not driven on `/chat/`. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261120/r1/` (frames 01-06, 18-21).
