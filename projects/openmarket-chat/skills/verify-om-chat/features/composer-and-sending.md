# Composer and sending

Writing a message and putting it on the wire. This file used to open by saying
the fixture lane could not verify any of it. That stopped being true with
`#777`: the fixture now types and sends. What still needs the daemon-pair lane
is the **wire** — delivery, a second identity, recovery states — not text entry.
Read the gotchas for where the line now falls.

## Sub-features

- Typing, and the Send control enabling as a draft becomes non-empty.
- The composer's placeholder, which names the destination and — since `#826` —
  advertises the market and chart shorthands on channels too, not only in DMs:
  `Message #ops · $ for markets · /chart to post one`. A topic keeps the bare
  `Message in <topic>`, so the three are no longer one channel-shaped pattern
  and two advertisements.
- Draft persistence per destination (channel, topic, DM) across navigation —
  durably for some lanes only. `#777` split them by lane name: `dm:<user>`,
  `room:<room>` and `room:<room>#<topic>` stay localStorage-backed under
  `om.chat.composerDrafts.<userId>`, while anything on an `om:`-prefixed lane is
  rejected at the storage boundary (`isVolatileLane`, `composer-draft-store.ts`)
  and lives in memory only. That covers the private/agent plane, an active
  whisper lane even while nominally public (`om:dm:<user>`), and the
  per-session lanes `#786` added (`om:draft:<owner>`, `om:session:<id>`) —
  they inherit the rule by name rather than needing their own. The
  difference is reload-durability specifically: volatile lanes still survive
  in-tab navigation, because the session's in-memory map is the live source
  either way.
- Attachments: the `+` menu, drag-and-drop, staged chips with per-item removal,
  and — since `#796`/`#798` — a preview of a staged image or video before you
  send it, the image one portaled under `document.body` so composer overflow
  cannot clip it.
- Sent video in the tape (`VideoAttachment.tsx`, reworked in `6c15b0fb`): a
  poster-mode tile (`data-video-mode="poster"`, button `Play <filename>`) that
  becomes the player (`data-video-mode="player"`, a `role=status`
  `[data-video-buffering]` "Buffering" chip) on Play. Progress is judged in
  12 s windows (`VideoAttachment.tsx:28`). Two silent windows in a row (about
  24 s with no bytes) re-mint the URL, at most twice (`:25`, `:35`). Any byte
  progress re-arms the window, so a slow link is never restarted. A decode
  error, or a failure after the second re-mint, lands on the fallback
  (`:401-402`). In a room that is the compact video file card
  (`data-file-family="video"`, `data-attachment-layout="compact"`) with a forced
  `Download <filename>` (`:764-770`). In a DM it is the "<size> · Couldn't play
  here" card with **Retry** and `Download <filename>`. A failed URL mint shows
  "Video unavailable" with **Retry** instead (`MediaRetryBox`, `:763`). Unsigned
  `https://assets.openmarket.xyz`
  images and posters paint a 1100 px CDN variant first (`lib/media-variants.ts`).
- Agents in the `@` menu (roster-gated, `01bf4481`): an agents group with
  `<owner> | <name>` rows, dimmed not-ready rows (`aria-disabled="true"`, the
  refusal reason in place of the detail) that cannot be committed, and an `om`
  router row (`lib/composer-complete.ts:559-621`, `ComposerAutocomplete.tsx:186-223`).
  Since `6395fe4b` an agent refused only for `no_grant` is no longer dimmed:
  its detail reads "<name> can't post here yet · Enter allows it"
  (`lib/composer-complete.ts:599-601`), and Enter or a click grants the room,
  rereads the roster and inserts `@name ` (`Composer.tsx:3643-3676`); a refused
  grant puts the refusal text in the row's detail. The row needs the
  `instances.grant` capability (`Composer.tsx:1762`).
  No fixture reports roster support, so none of it renders on the fixture lane.
- A bare `@` lists the whole server (`5e38077c`): every member in roster order,
  then every role, in a scrolling `listbox` named **MEMBERS & ROLES** (or
  **MEMBERS** with no role rows). `mentionCandidates` now defaults to no limit
  (`lib/composer-complete.ts:507`). Before, a 10-row budget kept half for roles
  (`:475-482`). The composer and the inline editor pass no budget; only the
  OpenScape chat still passes 20 (`world/WorldChatPane.tsx:183`). On the
  `/rooms/` shell fixture's `#ops`, the list has 14 options: 5 members (ana,
  dax, kyle, mira, rho) and 9 roles (admin, Devops, everyone, Full Stack, here,
  member, mod, owner, traders). **Devops** came with the `roleEdit` seed's role
  list (`f8baae2a`, `tools/visual/shell-fixture.tsx:3247`) and is listed whether
  or not `roleEdit=1` is set. The `/chat/` fixture has no Devops role and lists
  13. The old budget would have shown 10: 5 members plus 5 roles.
- Server-wide `@` search (`82390825`, `e56940c9`). In a server channel on the
  public plane, a typed `@query` also asks the server's member search, app
  accounts included (`Composer.tsx:2742-2749`; 150 ms after typing stops,
  `lib/people.ts:87`). Hits pass the channel and private-topic walls, judged by
  each hit's own `roleIds`, with owners and admins passing both
  (`lib/composer-scope.ts:403-428`). They join the list after the rows the
  session holds and before any `agent:` rows (`withFoundMembers`,
  `lib/composer-complete.ts:626-637`). The `@` menu has no "Searching" row: that
  copy belongs to the `MenuSelect` people pickers. The fixture never fires the
  search by itself; see the recipe below.
- A member muted across a server loses the composer there (`591b1e11`). On the
  public plane, in any channel of that server, the whole composer is replaced by
  `div[role=status][data-testid=space-muted-notice]` (`Composer.tsx:5239-5249`).
  It reads "You're muted in this server until 3:40 PM.", "…until Nov 9, 3:40 PM."
  on another day, or "You're muted in this server." when a refusal named no time
  (`lib/space-mutes.ts:29-31`). DMs and group DMs are unaffected.
- A code-fence panel behind the text. `#799` paints a panel behind each fenced
  region of the draft, incomplete fences included. Since `496e9cf9` and
  `132c4256` the opening and closing fence lines are the panel's padding, and
  the panel runs from the middle of one to the middle of the other
  (`lib/composer-code-panels.ts`). Fence text (`.composer-token-code-fence`) is
  transparent while the caret is outside the block. With the caret inside it
  gains `.is-editing` and shows faint. The language sits top right in
  `.composer-code-panel-language`. `.composer-token-code-marker` no longer
  exists. Do not look for `#797` here: that commit touches
  only `src/editor/live-preview.ts`, so the cursor-based *hiding* of fence
  markers is a doc-editor behaviour, not a composer one.
- Ticket references (`2a683fce`, `96164fbc`). On a Projects server, typing `!`
  lists tickets (`Composer.tsx` `composeTicketTrigger`, `session.todos.lookup`),
  and a picked ticket sends itself. In the tape, a ticket link inside a
  sentence renders as a `TodoRefTag` with its number and status chip. A link
  alone on its line renders the card `section[aria-label="Ticket !<n>"]`
  (`components/projects/TodoRefCard.tsx`). An unreadable ticket shows
  `[data-ticket-hidden]`. **Live verification pending**: neither fixture stubs
  `session.todos`, so the list and the refs cannot resolve there.
- Replies, mentions (`@user`, role tags), slash commands, `$` market refs, and
  library-reference pills. `ac43c466` extended the bound-name trick already used
  for topics and multiword roles to `om://doc`, `om://folder` and `om://tag`
  URIs, so a draft can carry a full URI while showing a short label.
- The formatting toolbar and its selection clearance.
- Delivery states: sending, delivered, *"Delivery could not be confirmed"*
  recovery, and the cross-tab draft lease.
- Send disabled while empty; Enter-to-send versus newline. The **Send message**
  button renders when `isMobile || showSendButton` (`Composer.tsx:7374`). The
  ordinary room and DM composer is therefore phone-width only, and desktop
  sends with Enter. Panes that pass `onSubmitText` (`ChatPane.tsx:438`) and the
  remote-control pane (`RemoteControlPane.tsx:345`) also show it on desktop,
  with an `sr-only` "Send" label.
- Sent text must not come back as a draft after a reload or a revisit
  (`cd9f8c72` queues the durable snapshot delete behind the lane's pending
  saves). The fixture cannot show this: it stubs `restoreDurableComposerLane`
  and has no IndexedDB snapshot, so it proves only that the box clears.
- The over-limit "send as file" offer and the mass-mention brake, both of which
  can refuse a send that otherwise looks ready.
- **Vim mode** (`b1ed7135`, `1aebc918`), opt-in from Settings → Keyboard
  Shortcuts → **Vim mode** (see
  [settings-and-appearance.md](settings-and-appearance.md)). The engine is a lazy
  chunk (`lib/composer-vim.ts`) loaded once the setting is on. Focus lands in
  insert mode. Escape enters normal mode, `v` visual and `V` visual-line.
  Motions, operators with text objects, counts and undo exist in the engine and
  its unit tests; the recipe below drives a subset of them.
  The mode badge is
  `<span class="composer-vim-mode" data-vim-mode="normal|insert|visual|visual-line">`
  (`Composer.tsx:7457-7467`) reading NORMAL / INSERT / VISUAL / VISUAL LINE, with
  a pending operator in `.composer-vim-pending`. Enter sends only in insert
  mode. Escape belongs to Vim, so it no longer cancels a reply. Touch screens
  (coarse pointer) never get Vim. With the setting off none of this renders,
  and Enter and Escape behave as before.
- The GIF picker: **Choose emoji or GIF** → **GIFs** opens dialog **Choose a GIF** with **Search KLIPY**; `?view=gif` is a standalone sizing harness (`/rooms/` only; the `/chat/` fixture has no GIF view).
- **Invite card**, **opening-room queue**, **recovery nudge**, the printable-key focus handoff and the 29-entry slash list (each in its own section below, each with the stub it needs).

## How to get to it (user POV)

You click into the message box at the bottom of a channel, topic, or DM, type,
and press Enter or the send arrow. The box remembers what you were writing if
you navigate away and come back, and it tells you when a message did not make
it.

## Driving it with control-om-chat

**The fixture lane types and sends.** `#777` spelled out the two predicates
that used to lock it (see Gotchas), so a plain `?view=room` composer accepts
keystrokes and Enter appends to the tape:

```bash
agent-browser click "textarea"
agent-browser keyboard type "probe line"
agent-browser press Enter
agent-browser eval '(()=>document.querySelectorAll("[data-message-row]").length)()'
#   one more than before; the textarea is empty and the line is in the tape
```

That is a **local** send into the fixture's seeded store. It proves the write
path, the clear-on-send, and the tape update — and nothing about the relay.
What the lane also proves:

```bash
# The composer's destination follows navigation.
agent-browser snapshot -c | grep -i textbox
#   "Message #ops · $ for markets · /chart to post one"
#   -> "Message in CPI print — Aug"
#   -> "Message ana · $ for markets · /chart to post one"

# Send is disabled on an empty draft — but ONLY at a phone width. The Send
# button renders under `max-width: 768px`; on desktop there is no such button
# and Enter sends. Set the viewport first or this looks like a regression.
agent-browser set viewport 390 844
agent-browser find role button text --name "Send message" --exact
agent-browser snapshot -i -c | grep "Send message"        # [disabled]

# The code-fence panel (#799). Cheapest route is to seed the draft, since
# ?draft= feeds the same `text` state the fence parser reads:
agent-browser open ".../shell-fixture.html?view=room&draft=%60%60%60js%0Aconsole.log(1)%0A%60%60%60"
agent-browser eval '(()=>document.querySelectorAll("[data-code-panel]").length)()'
#   1, with [data-code-region] at 4, three .composer-token-code-fence spans whose
#   color is rgba(0, 0, 0, 0) with the caret elsewhere, the label "js", and no
#   .composer-token-code-marker (re-driven 2026-11-06 at ea399e62)

# The dedicated harness (since 496e9cf9) mounts the real Composer alone over a
# literal stub session (room "deals"), so nothing in it is INERT. It takes
# ?draft=<urlencoded>, &theme=dark|light and &width=<px> (default 640) and is
# /rooms/-only:
agent-browser open "$(control-om-chat url 'tools/visual/composer-code-panel-fixture.html?draft=hello%0A%60%60%60ts%0Aconst%20a%3D1%0A%60%60%60&theme=dark&width=640')"
#   [data-code-panel] top 43px, height 44px, computed left 4px (8 px outside the
#   12 px text column); label "ts"; fences transparent
# Put the caret inside the block (focus the textarea, setSelectionRange into
# "const", press ArrowRight): two fences gain .is-editing and read rgb(139, 145, 152)

# A library-reference pill (ac43c466) — typing the URI is enough:
agent-browser click "textarea"
agent-browser keyboard type "see om://doc/doc-card for context"
agent-browser eval '(()=>{const b=document.querySelector(".composer-backdrop");
  return [...b.querySelectorAll("[data-pill]")].map(r=>r.textContent)})()'
#   ["om://doc/doc-card⧉ doc"]

# Or type the fence. Enter SENDS, so Shift+Enter is the only way to type a
# multi-line fence at all.
agent-browser click "textarea"
agent-browser keyboard type '```js'
agent-browser press "Shift+Enter"
agent-browser keyboard type 'const x = 1'
agent-browser press "Shift+Enter"
agent-browser keyboard type '```'
agent-browser eval '(()=>document.querySelectorAll("[data-code-panel]").length)()'
#   1, with [data-code-region] at 3 and .composer-backdrop present

# A seeded draft renders and survives a round trip. ?draft= seeds TWO lanes
# with the same text — room:ops and dm:<?dm= or ana> — so it works whichever
# of the two views you land on.
agent-browser open ".../shell-fixture.html?view=room&draft=seeded%20draft%20text"
```

Related handles that do resolve. In the composer row itself:
`"Summon your om here"` (on a private om lane the same button is `"Back to the room"`,
`Composer.tsx:6614-6615`), `"Add attachment or action"`,
`"Choose emoji or GIF"`, `"Toggle sealed mode"`, `"Toggle om approval mode"`.
On a message or the recovery banner: `"Add reaction"`,
`"Resend exact message"`, `"Discard & edit as new"`, `"Retry"`, `"Delete"`.
Note the composer's emoji control is `"Choose emoji or GIF"` — `"Add reaction"`
is the message-row control and will not match in the composer.

For anything on the **wire** — delivery states, a second identity receiving the
message, reconnection — use the **daemon-pair lane**. Text entry and a local
send no longer need it:

```bash
bun run build                       # the pair refuses a bundle built from another tree
bun tools/daemon-pair.ts            # two zero-login daemons, 31398 / 31399
```

It needs the local parity stack up (auth on `4001`, relay/store on `3002`).
Confirm with `curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:4001/`
before you build — the stack is frequently down, and finding out after a
four-minute build is the expensive order.

The cheaper alternative for a pure logic change is a unit test in `test/`
against the real `ChatSession`, which is what `tools/gui-e2e.ts` drives.

Vim mode. Turn it on through the Settings switch (or seed
`localStorage["om.chat.vimMode"]="true"` and reload). The fixture never writes the key:

```bash
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=settings&settingsPage=shortcuts&alerts=quiet')"
agent-browser find role switch click --name "Vim mode"      # localStorage om.chat.vimMode -> "true"
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=room&alerts=quiet')"
agent-browser find role textbox click --name "Message #ops"
V='(()=>{const b=document.querySelector(".composer-vim-mode");const t=document.querySelector("textarea");
  return JSON.stringify({mode:b?.dataset.vimMode,val:t.value,sel:[t.selectionStart,t.selectionEnd],
  rows:document.querySelectorAll("[data-message-row]").length})})()'
agent-browser eval "$V"                      # mode insert
agent-browser keyboard type "hello world"; agent-browser press Escape
agent-browser eval "$V"                      # mode normal, val "hello world"
agent-browser press 0; agent-browser press d  # .composer-vim-pending reads "d"
agent-browser press w                         # val "world"
agent-browser press Enter                     # normal mode: no new row, draft kept
agent-browser press v; agent-browser press '$' # mode visual, sel [0,5]
agent-browser press V                         # mode visual-line
agent-browser press Escape; agent-browser press i; agent-browser press Enter
agent-browser eval "$V"                      # rows +1, val "", mode STILL insert
```

Reply interplay: open `?view=room&alerts=quiet&reply=1`, focus the box, and press
Escape twice. **Cancel reply** stays. Turn the switch off and the same Escape
removes it, which is the control. Verified on `/rooms/` and on the `/chat/`
cloud fixture, which share the same Vim behavior (the `/chat/` route is
path-based: `/chat/room/ops`).

### GIF picker (added 2026-10-27)

In any room, click **Choose emoji or GIF**, which opens the **Choose an emoji** dialog. Then click the **GIFs** button. It is a `button`, not a `tab`, so `find role tab` fails. The dialog becomes **Choose a GIF**, with textbox **Search KLIPY** and a TRENDING section that stays empty offline: `klipyTrending` is not stubbed and calls the network. Driven on `/rooms/` and `/chat/`. `?view=gif` bypasses the Shell and renders h1 **GIF sizing stability** with **Reopen GIF** (`shell-fixture.tsx:4503-4521`). Sending a GIF is pending. Verified 2026-10-27 at `6c15b0fb` (maintenance pass, fixture lane). Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261027/r1/` (frame 24).

### Chart card and cashtag pill (added 2026-10-28)

- **Chart card:** send a message that is only a chart URI, such as `om://chart/BTC?i=15m`. The grammar is `CHART_URI_RE` (`lib/message-preview.ts:17`). The sent row renders a chart card reading **BTC · 15m · LIVE** with **Copy link**.
- **Cashtag pill:** send `$BTC looks strong`. The row renders a `.cashtag-pill` reading `$BTC`. Clicking the pill opens a peek in the product (`MessageRow.tsx:2671-2675`), but the fixture hard-codes `cashtagPeek: null` (`shell-fixture.tsx:3072`), so the peek cannot be proved here.
- **How to send:** on `/rooms/`, seed the draft with `?draft=om%3A%2F%2Fchart%2FBTC%3Fi%3D15m` or `?draft=%24BTC%20looks%20strong`, focus `textarea[data-composer-input]` and press Enter. The `/chat/` fixture parses `?draft=` (`apps/cloud/tools/visual/shell-fixture.tsx:1239-1242`), but its composer still loads empty on a room or a DM (re-measured 2026-10-30), so use `agent-browser fill 'textarea[data-composer-input]' '<text>'` and press Enter there.
- **Not seeded:** `UnfurlCard` (no fixture seeds `entry.unfurls`, and a send never adds one) and `WebhookEmbedBlock` (it needs `metadata.embeds` on a webhook sender; the gallery's webhook rows have none, `tools/visual/fixture.tsx:1430-1490`).

Verified 2026-10-28 at `07f7d04c` on `/rooms/` and `/chat/` (scheduled maintenance, fixture lane). Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261028/r1/` (`*-sent-*.png`).

### Typed role mention pill (added 2026-10-30)

Since `389f414e` a role name typed as `@traders` is painted like its
`om://role` pill (`Markdown.tsx:503`, `:2049`, `:2137`). Both shell fixtures
name the role `traders` and colour it `#d19a3a` (`shell-fixture.tsx:3209-3210`;
cloud `:1739`). Click the composer textbox (its name starts **Message #ops**;
the full name is **Message #ops · $ for markets · /chart to post one**), type
`@traders hi` so the space closes the autocomplete, and press Enter. The new
`[data-message-row]` holds a `.mention-pill.role-mention.role-colored` reading
`@traders`, with `style="--role-color: #d19a3a;"` and a computed colour of
`rgb(209, 154, 58)`. Neither fixture stubs `roleIdByMentionName`, so the pill
takes the `no-target` branch (`data-handle="traders"`), not the role link.
Clicking it calls `session.openRoleCard`, which no fixture stubs (see the
@role popover row in the README inventory). Driven 2026-10-30 at `47cb13bf` on
`/rooms/` and `/chat/` (frames 01-03).

### A mention at the end of a sentence (added 2026-11-04)

Since `0fe81331` (and rooms-client 0.109.1, `25343ba5`) a handle followed by a
full stop or dash resolves. Handles may carry `.` and `-` mid-name, so the
capture used to swallow the sentence's full stop and look up a name nobody has.
The tape tokenizer, composer pills and message previews now retry a capture that
names no member, role or broadcast with its trailing `.` or `-` trimmed, and
leave the punctuation as plain text after the pill. A full capture that names
someone still wins, and only trailing punctuation trims (`@maya.dee` stays
unresolved). Source: `lib/mention-capture.ts`, `lib/composer-pills.ts`,
`Markdown.tsx`.

Click the composer textbox (**Message #ops · $ for markets · /chart to post
one**) and type `built by @ana. and @dax- too `. Escape the autocomplete, click
the textbox again and press Enter. The composer backdrop holds
`span.composer-token.composer-token-mention` reading `@ana` followed by the run
`. and …`. The sent `[data-message-row]` holds two `.mention-pill`s, `@ana`
(`data-handle="ana"`) and `@dax` (`data-handle="dax"`), each followed by a text
node starting `.` or `-`. Driven 2026-11-04 at `ce14d4ba` on `/rooms/` and
`/chat/` (`mention-01`, `mention-02-tape-*`, `chat-05-mention`). The
notification side (the store's notify worker) is not provable on the fixture.

### Slash commands (added 2026-10-30)

Typing `/` in the composer opens the command list from `SLASH_COMMANDS`
(`lib/slash-commands.ts:71`): 29 options on the root fixture, starting
`/dm`, `/help`, `/topic`, `/channel-invite`, `/invite`, `/join`, `/leave`,
`/follow`. Typing `/shr` narrows it to `/shrug` ("Appends ¯\_(ツ)_/¯ …").
Settings → **Slash Commands** (`settings-fixture.html?host=user&page=slash-commands`)
renders the guide page **Slash commands**. Running a command is pending: the
real handler is `ChatSession.handleSlash` (`lib/session.ts:43446`, called at
`:15359`, `:15584`, `:15916` and `:15992`), and the fixture's send only appends the text, so `/nick`,
`/status`, `/mute` and the daemon-bound verbs (`/chart`, `/capture`,
`/summarize`, `/brief`, `/agent`, `/reset`, `/arm`, `/disarm`) need an
authenticated or daemon rig. Driven 2026-10-30 on `/rooms/` (frame 51).

### Paste: a link over a selection, an image into the composer (added 2026-11-01)

Both paths are pure client code behind `Composer.tsx:6922-7007`, so a
synthetic `ClipboardEvent` drives them on either host (driven 2026-11-01 on
`/rooms/` and `/chat/` at `936f5b64`):

```bash
# select "docs" in "see docs here", paste a lone URL over it
agent-browser eval '(()=>{const t=document.querySelector("textarea[data-composer-input]");t.focus();
  const set=Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,"value").set;
  set.call(t,"see docs here");t.dispatchEvent(new Event("input",{bubbles:true}));t.setSelectionRange(4,8);
  const dt=new DataTransfer();dt.setData("text/plain","https://example.com/x");
  const ev=new ClipboardEvent("paste",{clipboardData:dt,bubbles:true,cancelable:true});t.dispatchEvent(ev);
  return JSON.stringify({prevented:ev.defaultPrevented,value:t.value,sel:[t.selectionStart,t.selectionEnd]})})()'
#   {"prevented":true,"value":"see [docs](https://example.com/x) here","sel":[11,32]}
```

`planLinkPaste` (`lib/composer-format.ts:267-299`) needs a lone `http(s)://`
URL and a single-line, non-empty selection; the selection lands on the URL
span afterwards. With a file in the clipboard the link branch is skipped:

```bash
agent-browser eval '(()=>{const t=document.querySelector("textarea[data-composer-input]");t.focus();
  const dt=new DataTransfer();dt.items.add(new File([new Uint8Array([137,80,78,71])],"probe.png",{type:"image/png"}));
  t.dispatchEvent(new ClipboardEvent("paste",{clipboardData:dt,bubbles:true,cancelable:true}));
  return document.documentElement.dataset.fixtureAttachment})()'
#   "probe.png", and the region named "Message attachments" reads "probe.png Ready · 1 KB"
```

That staged card is the fixture's `acceptFile` stub (`shell-fixture.tsx:4128-4148`)
pushing a pending attachment and stamping `data-fixture-attachment`; no upload
or scan runs. OS drops onto the tape, the topic list or the library
(`useFileDropZone.tsx`) still need a real file through `setInputFiles` or a CDP
drop, and stay pending.

### The older-messages banner past 99 (added 2026-11-02)

`ChatPane.tsx:3317` prints **You're viewing older messages · 99+ new below**
once the count behind the banner passes 99 (`formatUnreadCount`,
`lib/animated-count-parts.ts:35-42`, since `4cd3434f`). No fixture seed raises
a room's new-below count that high (`bulk=120` pads the tape but the reader
sits at the bottom), so this is source-only. The banner itself mounts on
`shell-fixture.html?view=room&history=detached&alerts=quiet` and reads **You're
viewing older messages** with **Jump to present**, with no count, because the
fixture room's `unread` is a constant 0 (`shell-fixture.tsx:1515-1520`; driven
2026-11-03 on `/rooms/`). See
[channel-and-topic-navigation.md](channel-and-topic-navigation.md) / Unread
labels past 99.

### Server-wide `@` search and the muted notice (added 2026-11-09)

Both need a seam in the init script from
[README.md](README.md) / Stub the people directory first; `autofill` otherwise
answers `people` with `INERT` and the page crashes.

For the search, make `people.searched` return a **cached** object for a query
prefix, for example `{status:"ready",people:[FAR,APP,CARD]}` holding `farouk`
(display name **Farouk Aziz**), the app account `faq-bot`, and `farah` (nickname
**Farah N**, role `admin`). Type `@fa` into `textarea.composer-field` on
`shell-fixture.html?view=room&alerts=quiet`. The listbox **MEMBERS** then holds
**faq-bot**, **Farah N** and **Farouk Aziz**, and Enter inserts `@faq-bot `.
Driven 2026-11-09 on both hosts, with `roleIds: []` so nothing was walled; a hit a
wall removes stays unit-level (`packages/chat-ui/test/composer/mention-walls.test.ts`).

For the notice, return an ISO time from `spaceMutes.until`. On the same route
`[data-testid=space-muted-notice]` reads "You're muted in this server until 4:39 AM."
with no `textarea.composer-field` and all 16 rows still on the tape. Driven
2026-11-09 on both hosts.

### Invite card from a sent invite code (added 2026-11-09)

A message that is only an invite code renders as an invite card. `previewInvite`
is unstubbed in both fixtures, so without a stub the card's `.then` lands on
`INERT`. Seed it, then send the code from the composer:

```bash
cat > "$SCRATCH/fixture-invite-stub.js" <<'JS'
Object.defineProperty(Object.prototype, "previewInvite", { configurable: true, writable: true, enumerable: false,
  value: async () => ({ kind: "ready", name: "Acme Desk", memberCount: 42 }) });
JS
agent-browser type 'textarea' 'acme:0123456789ABCDEF0123456789ABCDEF'
agent-browser press Enter
# -> the new kyle row reads "YOU'VE BEEN INVITED TO JOIN | AD | Acme Desk | 42 members | Join"
```

**Join** was not pressed. The hosted app's open-in-app handoff (`AppHandoff.tsx`)
is a separate, still-pending row.

### Sends queued into a room still opening (added 2026-11-09)

`?fixtureState=loading` empties the rooms and renders the opening shell
(`.conversation-loading`). `queuedSendsFor` is unstubbed, so seed it:

```bash
cat > "$SCRATCH/fixture-queue-stub.js" <<'JS'
Object.defineProperty(Object.prototype, "queuedSendsFor", { configurable: true, writable: true, enumerable: false,
  value: (r) => [{ seq: -1, clientMsgId: "q1", ts: Date.now(), room: r, handle: "kyle", userId: "u1",
                   isAgent: false, type: "post", text: "queued while opening" }] });
JS
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=room&alerts=quiet&fixtureState=loading')"
# -> [data-opening-room-queue] inside .conversation-loading: "kyle | queued while opening"
```

### Recovery nudge (added 2026-11-09)

`recoveryNudge: null` is spelled out in both fixtures, so it needs the
session-capture shim from [message-actions.md](message-actions.md):

```bash
agent-browser eval '(()=>{const o=window.__om;o.recoveryNudge=true;o.hideRecoveryNudge=()=>{o.recoveryNudge=null;o.closeConfirm()};o.closeConfirm();return 1})()'
# -> "Save your recovery code. It's the only way back into your sealed messages if this device is lost."
#    with buttons "Save it now" and "Dismiss recovery reminder"
agent-browser find role button click --name "Dismiss recovery reminder"   # -> the toast is gone
```

**Save it now** was not pressed; the recovery ceremony stays pending.

### Keyboard: a printable key and the slash list (added 2026-11-09)

With nothing focused, a printable key moves focus to the composer and types
there (`Shell.tsx:1142-1185`): from `BODY`, `press a` left the textarea focused
with the value `a`. Typing `/` lists 29 commands: /dm, /help, /topic,
/channel-invite, /invite, /join, /leave, /follow, /mute, /nick, /nudge, /poll,
/status, /chart, /me, /shrug, /spoiler, /tableflip, /unflip, /note, /template,
/todo, /agent, /arm, /brief, /capture, /disarm, /reset and /summarize. No entry
was run; `/draw` (`lib/slash-commands.ts:205`) was not listed in the fixture.

## Gotchas

- **The connection strip waits out a grace delay.** `?connection=reconnecting`
  (`shell-fixture.tsx:2718`) renders **Reconnecting...** in the
  `.ui-connection-strip` (`role=status`, `shared/ui/ConnectionStrip.tsx:93`),
  but only after `CONNECTION_GRACE_MS`: a read 2 s after load finds an empty
  `.ui-connection-strip-slot`, a read at 8 s finds the text (2026-10-31,
  `/rooms/`). `offline` and `degraded` are not `ConnectionStatus` values; the
  type is `live | reconnecting | failed`. The `failed` escalation with its
  **Retry** needs a real flap.

- **The composer is no longer read-only, and the two banners are gone.** For a
  long while the fixture left `session.composerLaneOwnedElsewhere` and
  `session.composerDeliveryRecovery` unstubbed, so the `INERT` proxy answered
  truthy for both, the textarea rendered `readOnly`, and *"This draft is open in
  another tab"* and *"Delivery could not be confirmed"* sat above it. `#777`
  stubbed them — `composerDeliveryRecovery: () => null` and
  `composerLaneOwnedElsewhere: () => false`
  (`tools/visual/shell-fixture.tsx:3633-3634`), with a comment naming the lock
  it was removing. Measured again on `9902d149`:
  `readOnly` is `false` in room, topic and DM, and neither banner renders.

  If you find either banner back, that is a fixture regression rather than the
  expected state — the opposite of the advice this file used to give. And there
  is now no way to stage them on purpose: `composerDeliveryRecovery` is
  hardcoded to `null`, so even `?delivery=fail-once` — which does make a send
  fail — will not raise the recovery banner. Proving those two states needs a
  fixture change, not a query.

- **The fence panel is not a rendered preview, and the tape's code block is not
  the panel.** `#799` is called "preview fenced code blocks" but it renders no
  code: it paints a panel *behind* the textarea, marked
  `.composer-code-panel` / `[data-code-panel]`, with `[data-code-region]` per
  region and a `.composer-backdrop` layer. Meanwhile the seeded tape already
  contains a real `pre.code-wrap` — inside `[role=log]`, not near the composer.
  Assert on `[data-code-panel]`, and check `closest("[role=log]")` before
  believing any `pre` you find is yours.
- **Staged image and video previews are not reachable by query parameter.**
  `#796` and `#798` need a genuinely staged attachment: a ready image renders a
  `button` named `Preview <filename>` and a video one named `Play <filename>`
  inside `.composer-attachment-card`, and clicking either portals an
  `.ui-lightbox[role="dialog"]` under `document.body` — which pages across every
  staged image *and* video, so one click can arrow into the neighbouring file.
  Nothing here stages one: no parameter does it (all `params.get` keys
  enumerated — 73 on `f7d7c987`, 78 distinct on `cd9f8c72`) and the fixture's pending-attachment arrays start empty, fed
  only by `session.acceptFile` behind the real file input. The maintained
  `tools/visual/mobile-conversation.visual.ts:667` path drives the hidden input
  with `setInputFiles`, and the shell fixture accepts the file at
  `tools/visual/shell-fixture.tsx:4128`. Preview/lightbox behavior still needs
  preview-ready attachment metadata and is not established by that fixture
  path.
- **The seeded room video is a stub and only proves the fallback ladder.** The
  default `#ops` tape carries dax's "recording of the retest, plus the notes"
  (`msg-ops-110`, a 15.9 MB `.mov` plus a PDF; `shell-fixture.tsx:1139-1163`).
  Its URL is a truncated `data:video/mp4` stub, so it never decodes. Driven at
  `6c15b0fb`: a fresh load shows the poster tile and `Play Screen Recording …
  .mov`. Play switches to the player with the Buffering chip at `readyState` 0,
  and about 10 s later the row falls back to the compact video file card with
  Download. If the row is already a file card, the ladder has run. Reload to
  see the poster again. This is a decode failure, not a slow link. The
  watchdog's progress re-arm, the re-mint rungs, CDN variants (data URLs are
  never rewritten) and the DM "Couldn't play here" card all need real media.
- **A reference pill is a backdrop token, not a DOM node in the textarea.**
  Typing an `om://doc/...` URI into the composer paints a run in
  `.composer-backdrop` carrying `data-pill="true"` and
  `class="composer-token composer-token-doc"`, reading `om://doc/doc-card ⧉ doc`
  while `textarea.value` keeps the raw URI. Query the backdrop, not the page:
  a bare `[data-pill]` sweep also catches the sidebar's `rail-pill` and
  `unread-pill` elements and will make you think you found one when you have
  not. The *bound short label* half — a friendly name standing in for the URI —
  comes from dragging or pasting out of the Library with its metadata, and
  nothing in the fixture seeds `referenceBindings`, so that half is unreached
  here for the same reason the staged previews are.
- **HTTPS share links bind to chips too, and this half *is* seeded.** `#965`
  and the shareable-links work make a recognised link —
  `https://openmarket.xyz/chat/room/<room>`, `/topic/<id>`, `/msg/<seq>` or
  `/doc/<id>` (`share-links.ts`, `parseShareLink`) — paint as a pill, and the
  fixture wires the resolver (`bindComposerUrisFor`), so a channel link
  resolves. Typing `see https://openmarket.xyz/chat/room/ops please` at
  `f7d7c987` painted one `.composer-backdrop` run,
  `composer-token composer-token-channel composer-token-painted` with
  `data-pill="true"`, holding a hidden `.composer-token-wire` (the exact URL)
  and a visible `.composer-token-label` reading `#ops`; `textarea.value` kept
  the full URL, which is what sends. A link with a query string or credentials
  is refused by design and stays plain text — use a bare route when you mean
  to prove the chip.
- **A local send is not a wire send.** Enter appends a row to the seeded tape
  and clears the box, which is enough to prove the composer's write path. It
  says nothing about the relay, about a second identity seeing the message, or
  about delivery and recovery states. Keep those claims on the daemon-pair
  lane and say which lane a frame came from.

- **A send in Vim insert mode stays in insert mode.** The box empties and the
  badge keeps reading INSERT. It does not drop back to normal. Assert that,
  not a return to NORMAL.

- **Turning Vim mode off writes `"false"`.** It does not remove the key. Check
  `localStorage.getItem("om.chat.vimMode") === "true"` rather than checking for
  the key's presence. Remove it yourself between runs in one browser session:
  a later default-state frame otherwise renders with Vim on.

- The composer is a `textarea` with `role="textbox"`, not a `contenteditable`.
  `document.querySelector("[contenteditable=true]")` finds nothing.

- `?sealed=1` is a *different* lock (the agent-lane seal) from the draft lease.
  Do not use it expecting to clear the lease.

- `tools/daemon-pair.ts` refuses to run against a `dist/` built from another
  tree, and it is right to. When it exits with a digest mismatch, rebuild —
  do not set `OM_ROOMS_GUI_DIR` to get past it unless you are deliberately
  bisecting a pinned bundle.

### Verification record

**Last verified:** 2026-11-09 (scheduled maintenance). **Product commit:** `16da8ecf` (GitLab origin/main; one CI-only commit past `82390825`). `/rooms/` (18141): a local send in `#ops` (16 → 17 rows); a printable key from `BODY` focuses the composer; `/` lists 29 commands; the invite card (**Acme Desk**, 42 members, **Join**) after sending an invite code; the opening-room queue ("queued while opening" under `fixtureState=loading`); the recovery nudge shown and dismissed. `/chat/` (18142): the invite card and the recovery nudge. **Limitations:** **Join**, **Save it now** and every slash command were not run; the queue was driven on `/rooms/` only. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261109/r1/`.

**Previous record:** 2026-11-09 (nightly maintenance). **Product commit:** `82390825` (GitLab origin/main; rooms-client 0.114.0; 49 commits past `08fe407b`). **Scope:** `/rooms/` and `/chat/` with the people stub: a local send in `#ops` (16 → 17 rows); the bare `@` lists 14 on `/rooms/` and 13 on `/chat/`; server-wide `@fa` hits (**MEMBERS**: faq-bot, Farah N, Farouk Aziz; Enter inserts `@faq-bot `) and `[data-testid=space-muted-notice]` on both hosts with the injected seams. **Limitations:** the daemon-pair lane was down (4001, 3002), so a real store search and a real mute frame were not driven; walls removing a hit stay unit-level. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261109/r1/`.

**Previous record:** 2026-11-08 (nightly maintenance). **Product commit:** `08fe407b` (GitLab origin/main; rooms-client 0.112.0; unchanged since the 2026-11-07 pass). **Scope:** `/rooms/` (18183) and `/chat/` (18184): a local send in `#ops` (16 → 17 rows); the bare `@` lists 14 on `/rooms/` and 13 on `/chat/`. **Limitations:** the daemon-pair lane was down (4001, 3002); a send typed in the topic view did not echo a row in the fixture. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261108/r1/`.

**Previous record:** 2026-11-07 (nightly maintenance). **Product commit:** `08fe407b` (GitLab origin/main; rooms-client 0.112.0; 89 commits past `ea399e62`). **Scope:** `/rooms/` (18180) and `/chat/` (18181) `view=room`: a typed message sends (16 → 17 rows); a bare `@` lists 14 options on `/rooms/` (5 members, 9 roles with **@Devops**) and 13 on `/chat/`. **Limitations:** the allow-from-picker agent row needs roster support with `instances.grant`, which no fixture reports; `!` ticket verbs need a Projects server. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261107/r1/`.

**Previous record:** 2026-11-06 (nightly maintenance). **Product commit:** `ea399e62` (GitLab origin/main; rooms-client 0.111.0; 74 commits past `873a57ce`). **Scope:** `/rooms/` (18180) and `/chat/` (18181) `view=room`: a typed message sends (16 → 17 rows). `/rooms/` shell `?draft=` fence: 1 panel, 4 regions, transparent fences, label `js`, no marker spans; `composer-code-panel-fixture.html`: panel left 4px, faint fences with the caret inside. **Limitations:** `!` ticket references need a Projects server and are pending. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261106/r1/`.

**Previous record:** 2026-11-05 (nightly maintenance). **Product commit:** `873a57ce` (GitLab origin/main; rooms-client 0.109.1; 17 commits past `ce14d4ba`). **Scope:** `/rooms/` (18170) and `/chat/` (18171) `view=room`: typing in **Message #ops** and pressing Enter echoed the row locally (16 → 17 rows). **Limitations:** mentions, slash commands, attachments and the trailing-punctuation pill were not re-driven; their 2026-11-04 record stands. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261105/r1/` (`31`, `43`).

**Previous record:** 2026-11-04 (nightly maintenance). **Product commit:** `ce14d4ba` (GitLab origin/main; rooms-client 0.109.1; 16 commits past `ba4389e7`). **Scope:** `/rooms/` (18160) and `/chat/` (18161): the new trailing-punctuation mention (composer token and two sent pills, rows 16 → 17); `/` lists 29 commands on `/rooms/`. **Limitations:** the other send paths were not re-driven; their 2026-11-03 records stand. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261104/r1/` (`mention-01`, `mention-02-tape-rooms`, `mention-02-tape-chat`, `chat-05-mention`).

**Previous record:** 2026-11-03 (nightly maintenance). **Product commit:** `ba4389e7` (GitLab origin/main; rooms-client 0.108.0; one CI-only commit past `3f8f24bc`). **Scope:** `/rooms/` (18143) and `/chat/` (18144): a local send appends a row (16 → 17); the `@traders` pill (`rgb(209, 154, 58)`); the `$BTC` cashtag; `/` lists 29 commands and `/shr` narrows to `/shrug`; a link pasted over a selection gives `see [docs](https://example.com/x) here`; an image paste stages **probe.png Ready · 1 KB**; **Choose emoji or GIF** → **Choose a GIF** with **Search KLIPY**; **Send message** is `disabled` at 390. `/rooms/` only: the chart URI draft renders a card whose text nodes read **BTC**, **15m**, **LIVE** and **Copy link**; a fenced `?draft=` gives one `[data-code-panel]`; Vim mode (`dw` → `world`, `v$` selects 0–5); the `history=detached` banner without a count. **Limitations:** `/chat/` still parses `?draft=` without showing it; delivery stays on the daemon-pair lane. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261103/r1/` (`comp-*`, `banner-01`).

**Previous record:** 2026-11-02 (nightly maintenance). **Product commit:** `3f8f24bc` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18137) and `/chat/` (18138): `$TSLA looks strong` → `.cashtag-pill[role=link][data-cashtag=TSLA]` (the `draft=` seed on `/rooms/`, `fill` on `/chat/`); the `om://chart/BTC?i=15m` send → **BTC 15m LIVE** with **Copy link** (`/rooms/`); `/` → **COMMANDS** (29), `/shr` → **/shrug**; a bare `@` → **MEMBERS & ROLES** (13); **Choose emoji or GIF** → **Choose an emoji** → **GIFs** → **Choose a GIF** with **Search KLIPY**; the link-over-selection paste → `[docs](https://example.com/x)`; `connection=reconnecting&failed=room` → **Reconnecting...** (`role=status`) at 8 s with the failed row (`/rooms/`); the 300-character fence wrapping (958 px, no overflow) with `code-block.css` injected (`/rooms/`). **Limitations:** the cashtag peek and the chart card's actions stay inert; `/chat/` ignores `draft=`; nothing seeds a 99+ banner; the image paste and the Vim motions were not re-driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261102/r1/`.

**Previous record:** 2026-11-01 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18137) and `/chat/` (18138): a bare `@` lists 13 options and `/` 29 (`/shr` → **/shrug**) on both; `@traders hi` renders `.mention-pill.role-mention.role-colored` at `rgb(209, 154, 58)` on both; `om://chart/BTC?i=15m` renders the chart card (**BTC 15m LIVE**, **Copy link**) on `/rooms/`; `?connection=reconnecting` reads **Reconnecting...** after 8 s; `failed=room` shows kyle's failed row; the link-over-selection paste and the image paste (**Message attachments**: **probe.png Ready · 1 KB**) on both hosts; Vim in the composer with `om.chat.vimMode` (**INSERT** → Escape **NORMAL**, `0` `x` → `ello world`, `d` pending then `w` → `world`, `v l l` → **VISUAL** with selection 0–3). **Limitations:** the cashtag pill and the GIF send were not re-read (the chart card selector in the script missed and the text was read instead); delivery and draft durability still need the daemon-pair lane. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261101/r1/` (`composer-01` to `composer-04`, `paste-01`/`02`, `vim-01`, `chat-09`).

**Previous record:** 2026-10-31 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18135): local send (16 → 17 rows, box cleared); bare `@` → **MEMBERS & ROLES** with 13 options; `/` → 29 commands, `/shr` → `/shrug`; `@traders hi` → `.mention-pill.role-mention.role-colored` in `rgb(209, 154, 58)` with `--role-color: #d19a3a`; `om://chart/BTC?i=15m` → **BTC 15m LIVE** with **Copy link**; `$BTC looks strong` → one `.cashtag-pill`; `?draft=` code fence → one `[data-code-panel]`, three regions, two markers; **Choose emoji or GIF** → **GIFs** → **Choose a GIF** with **Search KLIPY**; `?reply=1` strip and the toolbar **Reply** retarget; `?connection=reconnecting` → **Reconnecting...** after 8 s. `/chat/` (18136): send, bare `@` (13), `/` (29) and `/shr`, the role pill, the chart card, the reply strip and retarget. **Limitations:** Delivery and recovery banners, staged attachments, agent rows in the `@` menu, sending a GIF, slash execution, Vim touch/IME, durable drafts, unfurl and webhook cards. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261031/r1/`.

**Previous record:** 2026-10-30 (scheduled maintenance). **Product commit:** `47cb13bf` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/`: local send (rows 16 → 17), bare `@` (13 options), chart URI card (BTC / 15m / LIVE, Copy link), `$BTC` cashtag pill, `reply=1` **Cancel reply**, **Choose emoji or GIF** → **GIFs** → **Choose a GIF** with **Search KLIPY**, 390 **Send message** disabled when empty, the `/` command list (29) and `/shrug` filter, and the typed role pill. `/chat/`: the typed role pill, and `?draft=` loading an empty composer. **Limitations:** Delivery, attachments, Vim mode and slash-command execution were not driven. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261030/r1/` (frames 01-03, 14-16, 51).

**Previous record:** 2026-10-29 (nightly maintenance). **Product commit:** `cdfb1b0f` (origin/main; rooms-client 0.108.0). **Scope:** On `/rooms/` `?view=room&alerts=quiet`, typing "nightly 1029 probe" and Enter grew `[data-message-row]` 16→17 with that text. A bare `@` listed 13 options (ana, dax, kyle, … plus roles) on `/rooms/` and `/chat/`, and a `/chat/` send landed too. **Limitations:** Delivery, Vim mode, attachments, GIF and the chart card were not re-driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261029/r1/` (frames 28–29, 64).

**Previous record:** 2026-10-28 (nightly maintenance). **Product commit:** `2dd7aad1` (origin/main). **Scope:** On `/rooms/` and `/chat/`, a bare `@` in `Message #ops · $ for markets · /chart to post one` opened listbox **MEMBERS & ROLES** with 13 options (5 members, 8 roles). On `/rooms/`, a fenced 300-character send through the native value setter appended `msg-ops-116` (the id depends on how many sends the session has made) and cleared the composer. The Vim path read `insert` → Escape `normal` → `0` `d` pending "d" → `w` left "world", and the key was cleared. **Choose emoji or GIF** → **GIFs** opened **Choose a GIF** with **Search KLIPY**. **Limitations:** The roster-gated agent rows, video fallback, reply Escape, delivery, recovery, draft durability, staging, touch, IME and pref sync were not driven. `agent-browser keyboard type` with embedded newlines sends early, so fill multi-line drafts through the value setter. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261028/r1/` (frames 02, 05-07, 40).

**Previous record (Vim mode):** 2026-10-27 (maintenance re-drive). **Product commit:** `6c15b0fb286e9dc1b6cb130c9c97cd7e0afa9254` (origin/main). **Scope:** `?view=settings&settingsPage=shortcuts` switch **Vim mode** set `om.chat.vimMode` to `"true"`. In `Message #ops`, `.composer-vim-mode[data-vim-mode]` read `insert`. After typing "hello world" and Escape it read `normal`, `0` `d` showed `.composer-vim-pending` "d", and `w` left "world". The key was cleared afterwards. **Limitations:** Enter-to-send in insert mode, doc `:q`, touch and IME were not driven. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261027/r1/` (frame 16).
