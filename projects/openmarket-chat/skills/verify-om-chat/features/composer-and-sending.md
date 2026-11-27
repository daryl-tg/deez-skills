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
- Agents in the `@` menu (roster-gated, `01bf4481`): the **AGENTS** section
  (tab **Agents N**, `section: "agents"`) with `<owner> | <name>` rows, dimmed
  not-ready rows (`aria-disabled="true"`, the refusal reason in place of the
  detail) that cannot be committed, and an `om` router row
  (`lib/composer-complete.ts:664-711`, `ComposerAutocomplete.tsx:284-337`).
  A member flagged `isAgent` also sorts into AGENTS with an AGENT chip
  (`lib/composer-complete.ts:618`).
  Since `6395fe4b` an agent refused only for `no_grant` is no longer dimmed:
  its detail reads "<name> can't post here yet · Enter allows it"
  (`lib/composer-complete.ts:687-689`), and Enter or a click grants the room,
  rereads the roster and inserts `@name ` (`Composer.tsx:3472-3504`); a refused
  grant puts the refusal text in the row's detail. The row needs the
  `instances.grant` capability (`Composer.tsx:1779`).
  Only your own agents are offered: a member agent is kept only when it posts
  from your account (agent handles are bare names, so ownership is the
  `userId`), and another member's agent is left out even for a typed
  `@sco` (MR !278). While your om is offline your agents stay listed, dimmed
  with "offline · your om is off" and `aria-disabled="true"`, `@om` included;
  click, Enter and Tab insert nothing. Agent rows show the agent's own name,
  not the owner's nickname.
  Fixture seed (both hosts, from MR !278): `?view=room&agentPicker=1` puts
  your `argue` and ana's `scout` in `#ops`; `agentPicker=offline` also reports
  your om offline (on `/chat/` the `om` row appears only for `@o`). Click the
  picker's **Agents N** tab through `button.composer-autocomplete-tab`; a
  role/name find for "Agents" hits the left rail's Agents page instead.
  Without the seed no fixture reports roster support. The root `=1` seed adds
  the two members only, so it has no roster and no `<owner> | <name>` rows;
  the `/chat/` `=1` seed registers an agents desk whose instance list is empty.
  Driven 2026-11-18 on both hosts: `=1` shows **Agents 1** (`argue`) and `@sco`
  lists nothing; `=offline` dims `argue` (and on `/rooms/` the `om` row,
  **Agents 2**), and Enter or Tab on `@arg` leaves the box reading `@arg`.
  The message edit box offers the same list (`InlineMessageEditor.tsx:208-221`,
  `d08eb47d`): with `roleEdit=1&agentPicker=offline` on `/rooms/`, `@arg` in
  **Edit message** shows `argue` dimmed and Tab inserts nothing; with
  `agentPicker=1` Tab inserts `@argue `. The shared roster store
  (`lib/use-roster-agents.ts`) keeps the agents of a failed read, serves an
  om-offline read's last listed agents greyed, re-reads when the list opens,
  and refreshes held lists after an install, pause, resume or allow
  (`e01df6b1`, `85c25912`). No fixture lists an instance, so that store is
  unit-tested only (`packages/chat-ui/test/roster/roster-composer-owner.test.tsx`).
- A bare `@` lists the whole server (`5e38077c`): every member in roster order,
  then every role, in a scrolling `listbox` named **MEMBERS & ROLES** (or
  **MEMBERS** with no role rows). `mentionCandidates` now defaults to no limit
  (`lib/composer-complete.ts:575`); a caller that passes a budget still keeps
  part of it for roles (`:654-657`). The composer and the inline editor pass no budget; only the
  OpenScape chat still passes 20 (`world/WorldChatPane.tsx:181`). On the
  `/rooms/` shell fixture's `#ops`, the list has 14 options: 5 members (ana,
  dax, kyle, mira, rho) and 9 roles (admin, Devops, everyone, Full Stack, here,
  member, mod, owner, traders). **Devops** came with the `roleEdit` seed's role
  list (`f8baae2a`, `tools/visual/shell-fixture.tsx:3515`) and is listed whether
  or not `roleEdit=1` is set. The `/chat/` fixture has no Devops role and lists
  13. The old budget would have shown 10: 5 members plus 5 roles.
- The `@` list is a sectioned picker (`022af9cd`). Its head is a
  `div.composer-autocomplete-tabs[role=group]` named like the listbox, holding
  one `button.composer-autocomplete-tab` per non-empty section: **Members N**,
  **Roles N**, **Agents N** (`Composer.tsx:376-380`,
  `ComposerAutocomplete.tsx:50-59`, `:240`). Rows always run members, then
  roles, then agents, with or without a query (`lib/composer-complete.ts:465`,
  `:660`, `:711`), under `div.composer-autocomplete-group[data-group]` eyebrows
  MEMBERS / ROLES / AGENTS (`ComposerAutocomplete.tsx:284`). A tab click scrolls
  its eyebrow to the top and selects that section's first row; nothing is
  hidden (`:202-211`). The active tab (`.is-active`, `aria-current="true"`)
  follows the scroll (`:213-226`). Tabs take no focus (`tabIndex=-1`, mousedown
  prevented), so Enter after a tab click inserts the selected row. A query
  re-counts the tabs and drops an empty section's tab.
- Server-wide `@` search (`82390825`, `e56940c9`). In a server channel on the
  public plane, a typed `@query` also asks the server's member search, app
  accounts included (`Composer.tsx:2756-2763`; 150 ms after typing stops,
  `lib/people.ts:87`). Hits pass the channel and private-topic walls, judged by
  each hit's own `roleIds`, with owners and admins passing both
  (`lib/composer-scope.ts:404-429`). Since `022af9cd` they join the **Members**
  section, ahead of roles and agents, by a full re-sort (`withFoundMembers`,
  `lib/composer-complete.ts:756-763`). The `@` menu has no "Searching" row: that
  copy belongs to the `MenuSelect` people pickers. The fixture never fires the
  search by itself; see the recipe below.
- A member muted across a server loses the composer there (`591b1e11`). On the
  public plane, in any channel of that server, the whole composer is replaced by
  `div[role=status][data-testid=space-muted-notice]` (`Composer.tsx:5075-5085`).
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
  and a query lists tickets (`Composer.tsx` `composeTicketTrigger`,
  `session.todos.lookup`) under **TICKETS**, one option per ticket ("!1 Fix
  alert dedupe #ops Open"). A bare `!` stays the command list. Nothing is
  highlighted at first, and the popover says so: "Enter sends the text as typed.
  Arrow keys, then Enter or Tab, insert the link." Arrowing to a row and
  pressing Enter inserts `!1 Fix alert dedupe `. In the tape, a ticket link
  inside a sentence renders as the button `button.ticket-ref` titled **Ticket
  !1, Open**, and pressing it opens the ticket. A link alone on its line renders
  the card **Ticket !<n>** (`components/projects/TodoRefCard.tsx`) with its
  status, home channel, priority, assignee, **Open** and **Follow**. An
  unreadable ticket shows `[data-ticket-hidden]` (not driven). Since
  `2db71f67`, losing a channel no longer hides its tickets from the lookup, tags
  or cards (source only).
- Replies, mentions (`@user`, role tags), slash commands, `$` market refs, and
  library-reference pills. `ac43c466` extended the bound-name trick already used
  for topics and multiword roles to `om://doc`, `om://folder` and `om://tag`
  URIs, so a draft can carry a full URI while showing a short label.
- The formatting toolbar and its selection clearance.
- Delivery states: sending, delivered, *"Delivery could not be confirmed"*
  recovery, and the cross-tab draft lease.
- Send disabled while empty; Enter-to-send versus newline. The **Send message**
  button renders when `isMobile || showSendButton` (`Composer.tsx:7349`). The
  ordinary room and DM composer is therefore phone-width only, and desktop
  sends with Enter. Panes that pass `onSubmitText` (`ChatPane.tsx:443`) and the
  remote-control pane (`RemoteControlPane.tsx:384`) also show it on desktop,
  with an `sr-only` "Send" label.
- Sent text must not come back as a draft after a reload or a revisit
  (`cd9f8c72` queues the durable snapshot delete behind the lane's pending
  saves). The fixture cannot show this: it stubs `restoreDurableComposerLane`
  and has no IndexedDB snapshot, so it proves only that the box clears.
- **Code is inert** (`7fbe9218`). The `@`, `#`, `:` and other lists stay shut
  inside code, no chip is drawn there, and a sent mention or link in code stays
  code text. See "Code is inert" below.
- **A typed role name goes out as the role's link** (`5cbe2a54`, which
  reverses `6a118e07`). A typed `@Devops` chips and sends `om://role/<id>` when
  exactly one role offered there holds the name. See "A typed role name goes
  out as the role's link" below.
- The over-limit "send as file" offer and the mass-mention brake, both of which
  can refuse a send that otherwise looks ready.
- **Vim mode** (`b1ed7135`, `1aebc918`), opt-in from Settings → Keyboard
  Shortcuts → **Vim mode** (see
  [settings-and-appearance.md](settings-and-appearance.md)). The engine is a lazy
  chunk (`lib/composer-vim.ts`), driven through the shared
  `lib/use-textarea-vim.ts` hook that the ticket comment box and the edit box
  also use (`4f2accbc`; see [projects.md](projects.md) and
  [message-editing.md](message-editing.md)). Focus lands in
  insert mode. Escape enters normal mode, `v` visual and `V` visual-line.
  Motions, operators with text objects, counts and undo exist in the engine and
  its unit tests; the recipe below drives a subset of them.
  The mode badge is
  `<span class="composer-vim-mode" data-vim-mode="normal|insert|visual|visual-line">`
  (`VimModeLine.tsx`, mounted at `Composer.tsx:7435`) reading NORMAL / INSERT / VISUAL / VISUAL LINE, with
  a pending operator in `.composer-vim-pending`. Enter sends only in insert
  mode. Escape belongs to Vim, so it no longer cancels a reply. Outside insert
  mode a block cursor `span.vim-block-cursor[aria-hidden]` sits on the caret
  (`VimBlockCursor.tsx`, `a420490b`): it gains `data-partial` while an operator
  is pending and `data-pill` over a pill, and turns to an outline when the box
  loses focus. Touch screens
  (coarse pointer) never get Vim. With the setting off none of this renders,
  and Enter and Escape behave as before.
- **Live formatting** (`d3aebbb5`). While you type, the backdrop paints
  Markdown in place and keeps the markers visible and faint: runs carry
  `composer-inline-bold`, `-italic`, `-underline`, `-strike`, `-code`,
  `-spoiler`, `-heading`, `-subtext`, `-quote` and `-marker`
  (`lib/composer-inline-format.ts:23`, `composer-inline-format.css`, a lazy
  chunk loaded once the draft holds one of `*~_`|#>`). The textarea value
  stays raw. On both hosts, typing ``**hi** ~~x~~ `c` __u__`` into
  `textarea.composer-field` gives backdrop runs with `composer-inline-bold`,
  `-strike`, `-code`, `-underline` and `-marker` (driven 2026-11-13; `/chat/`
  without the underline run). So a backdrop run is no longer only a
  `composer-token` or a `[data-code-region]`.
- The GIF picker: **Choose emoji or GIF** → **GIFs** opens dialog **Choose a GIF** with **Search KLIPY**; `?view=gif` is a standalone sizing harness (`/rooms/` only; the `/chat/` fixture has no GIF view).
- **Invite card**, **opening-room queue**, **recovery nudge**, the printable-key focus handoff and the 28-entry slash list (each in its own section below, each with the stub it needs).
- **A DM send keeps words typed while it was in flight** (`62fcc01a`). A DM
  send resolves only after its outbox commit, so words typed in that window
  used to land after the sent text, and the box kept both. Now the sent prefix
  is dropped and the rest is kept with its leading whitespace trimmed; a box
  rewritten some other way is left alone, and a refused send keeps everything
  (`Composer.tsx:4412-4423`). The fixture cannot open that window: both
  fixtures' `sendToActiveDurably` resolve at once
  (`tools/visual/shell-fixture.tsx:3931`, `apps/cloud/tools/visual/shell-fixture.tsx:2097`),
  so the proof is the unit test `packages/chat-ui/test/composer/dm-send-clears-while-typing.test.tsx`.
- **Esc steps back out** and **image preview zoom and pan** (each in its own section below; `/rooms/` only).
- **User links and base roles in message text** (`6577416f`, `a5354f9d`,
  `9db9ac06`). A message may carry `om://user/<id>`, where the id is 24
  lowercase hex digits or `guest_<hex>` (rooms-client 0.119.0). The reader
  draws it as `.mention-pill[role=link][data-handle=<handle>]` reading
  `@<nickname, else display name, else handle>`, titled `@<handle>`
  (`Markdown.tsx:551`, the `mentionlink` extension at `:2161`). An id no member
  row names reads `.mention-pill.no-target` **@unknown member**. The base roles
  `om://role/owner|admin|mod|member` read `.mention-pill.role-mention.no-target`
  **@admin** and so on. A link inside a code span stays literal text. A link to
  the viewer counts as a mention: the row takes `mention-wash`
  (`MessageRow.tsx:2164`), and the ping, badge, channel peek and `mentions:`
  search follow it (source and unit tests). Clicking a named pill opens that
  person's card.
- **Picks send links** (`ddb1bd65`, `ef005693`, `bc08428c`, `4a2eaf9b`). A
  person picked from the `@` list shows `@<handle> ` in the box and sends
  `om://user/<id>` (`bindPickedPerson`, `lib/composer-pills.ts:766`; only a
  24-hex or `guest_<hex>` id is linkable, so the fixture's `u-ana` stays a plain
  `@ana`). A picked role shows `@<name> ` and sends `om://role/<id>` through
  `session.bindMentionLinksFor` (`Composer.tsx:3561-3577`). Since `c4028edb`
  and `ed73acae` a person picked in a DM binds the same link. Parked drafts and
  the message edit box keep the same bindings. Neither shell fixture defines
  `bindMentionLinksFor`, so there a role pick deletes the typed `@Dev` and
  inserts nothing until the shim stubs it (recipe below).
- **A typed username goes out as its holder's link** (`3387846a`), because
  since `ca24a4b2` a typed `@handle` names nobody: it draws no pill, washes no
  row and pings no one. The box chips a name that will convert, and code,
  slash lines, to-do markers, app invocations and agent names stay as typed.
  A converted name whose holder is outside the channel meets **Not in this
  channel**. Section "A typed username goes out as its holder's link".
- **An inline image is blocked or waits for a click** unless its host is
  allowlisted, and **a send parked on its uploads shows "Uploading <name> ·
  N%"** on its row (each in its own section below; driven 2026-11-21 on
  `/rooms/`).
- **Pill lines keep their layout** (`85a71071`, `3baeaabc`). A role link on its
  own line renders inside the body's first paragraph, where it was typed
  (the `mentionlink` extension, `Markdown.tsx:545`). A message whose first line
  is a topic link lays out through `refFlowRuns` (`lib/ref-flow.ts:51`): the
  pill's line stays inline, and the lines after it form one block body whose
  blank lines keep their height (`.message-ref-flow`, `.message-ref-block`).
- **Emoji size** (`c8585a98`). Message text draws emoji at 1.375× through the
  `OM Inline Emoji` face at the head of `--font-message` (`shared/tokens.css:647`).
  A message of 1 to 27 emoji and nothing else gets `.jumbo-emoji` at 48 px
  (`--text-jumbo: 3rem`, `tokens.css:892`; `lib/jumbo-emoji.ts:5`;
  `MessageRow.tsx:2483`). Graphemes count once, so a flag or a ZWJ family is
  one. A 28th emoji drops the whole message back to inline size.
- **Letter tiles** (`879a7e5c`, `afd1b543`). A lone regional indicator (🇦–🇿)
  in a message becomes a drawn `span.letter-tile` (`tileLoneLetters`,
  `lib/letter-tile.ts:79-104`; called from `Markdown.tsx`), at
  `--letter-tile-scale` 1.375 inline and 1 inside `.jumbo-emoji`
  (`styles.css:3628`, `:3634`). A pair such as 🇺🇸 stays a native flag, and
  code spans and blocks are skipped. The `:` autocomplete offers it too:
  `:regional_indicator_l` lists **🇱 :regional_indicator_l:** with the tile in
  `.composer-autocomplete-glyph`, and Enter inserts `🇱 `.

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
#   ["om://doc/doc-card⧉ doc:doc-card"]   (the label reads "⧉ doc:<id>" for a doc the session cannot name; read 2026-11-22)

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
`Composer.tsx:6486-6487`), `"Add attachment or action"`,
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

In any room, click **Choose emoji or GIF**, which opens the **Choose an emoji** dialog. Then click the **GIFs** button. It is a `button`, not a `tab`, so `find role tab` fails. The dialog becomes **Choose a GIF**, with textbox **Search KLIPY** and a TRENDING section that stays empty offline: `klipyTrending` is not stubbed and calls the network. Driven on `/rooms/` and `/chat/`. `?view=gif` bypasses the Shell and renders h1 **GIF sizing stability** with **Reopen GIF** (`shell-fixture.tsx:4901-4919`). Sending a GIF is pending. Verified 2026-10-27 at `6c15b0fb` (maintenance pass, fixture lane). Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261027/r1/` (frame 24).

### Chart card and cashtag pill (added 2026-10-28)

- **Chart card:** send a message that is only a chart URI, such as `om://chart/BTC?i=15m`. The grammar is `CHART_URI_RE` (`lib/message-preview.ts:18`). The sent row renders a chart card reading **BTC**, **15m** and **Copy link**. Since `ad70e464` the card says **LIVE** only while candles are on its tape. On the fixtures no candle answer has rows, so the card reads **no chart data right now** in `[data-empty-box]` (420 × 120 px on `/rooms/`), with no `.cc-live` (both hosts, 2026-11-21). To see **LIVE** on `/rooms/`, answer `POST /rpc/v1/market/candles` with `{ok:true,data:{rows:[[ts,open,high,low,close,volume],…]}}` through the `window.fetch` getter/setter stub in [settings-and-appearance.md](settings-and-appearance.md) (Sealed Messages): with 40 rows the card read **BTC | 15m | LIVE** and drew its price axis. `/chat/` asks for no candles without a market token, so **LIVE** is not reachable there. An old daemon still reads "market data needs a newer daemon" (`ChartCard.tsx:209`; source only).
- **Cashtag pill:** send `$BTC looks strong`. The row renders a `.cashtag-pill` reading `$BTC`. Clicking the pill opens a peek in the product (`MessageRow.tsx:2488-2492`), but the fixture hard-codes `cashtagPeek: null` (`shell-fixture.tsx:3348`), so the peek cannot be proved here.
- **How to send:** on `/rooms/`, seed the draft with `?draft=om%3A%2F%2Fchart%2FBTC%3Fi%3D15m` or `?draft=%24BTC%20looks%20strong`, focus `textarea[data-composer-input]` and press Enter. The `/chat/` fixture parses `?draft=` (`apps/cloud/tools/visual/shell-fixture.tsx:1247-1250`), but its composer still loads empty on a room or a DM (re-measured 2026-10-30), so use `agent-browser fill 'textarea[data-composer-input]' '<text>'` and press Enter there.
- **Not seeded:** `UnfurlCard` (no fixture seeds `entry.unfurls`, and a send never adds one). `WebhookEmbedBlock` has no seed either (the gallery's webhook rows carry no embeds, `tools/visual/fixture.tsx:1302-1362`), but the shim can append one: copy seq 104 as seq 999 with `userId:"webhook:w9"`, `metadata:{webhook:{id:"w9",name:"alertmanager"},embeds}`, and `text` equal to `flattenEmbeds(embeds)` byte for byte, or the card is skipped. Since `2e836f98` embed text has no indented code blocks: `embedMarkdownText` (`lib/webhook-embed.ts`) trims leading whitespace outside fences and keeps list indent. An embed description with four-space-indented `**Environment:** prod` and `[Source](…)` lines rendered no `<pre>`, a bold **Environment:**, the link and two list items (driven 2026-11-27 on both hosts).

Verified 2026-10-28 at `07f7d04c` on `/rooms/` and `/chat/` (scheduled maintenance, fixture lane). Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261028/r1/` (`*-sent-*.png`).

### A typed role name goes out as the role's link (changed 2026-11-24)

Since `5cbe2a54` (with `1012cd8b`, `a6586d87` and `da90467d`) a role name
typed as `@Devops` goes out as `om://role/<id>`, as a picked role does. This
reverses `6a118e07` (2026-11-20), when a typed role name reached nothing. One
reader drives the chip and the send (`lib/typed-mentions.ts:153-220`, the
shared converter in `@openmarket/rooms-client/shared/handle-mentions`).

- **Which roles a name can reach.** In a channel or a topic: the base roles
  `owner`, `admin`, `mod` and `member`, then the server's named roles minus
  the everyone role (`typed-mentions.ts:141-149`, `:167-175`). In a ticket
  comment or description: the server's named roles only (`:191-200`). In a DM:
  none (`:201-211`).
- **When it converts.** Exactly one offered role holds the name. The match is
  the whole name, case-insensitive. A name may hold spaces (`@Full Stack`), and
  the longest name that fits wins. A prefix (`@trader` for `traders`) stays
  typed.
- **What stays typed.** A name two roles hold, a name a person also holds (the
  person wins), a username two people hold, an app account's name even when a
  role has it (`da90467d`, `:176-184`), an agent's name, code, slash lines and
  `!assign`/`!unassign`/`!todo`/`!edit` markers (`:115-131`). Until the server's
  roles load (`spaceRolesLoaded` false), no role name converts (`a6586d87`).
- **In the box.** A name that will convert draws `composer-token
  composer-token-role` with the typed text, for example `@devops`
  (`lib/composer-pills.ts:563-576`). It gains `composer-token-role-colored`
  only when `session.roleByRefId(id).color` is set (`Composer.tsx:6553-6568`);
  both fixtures answer `color: null` for every role, so no tint shows there.
  `@everyone` and `@here` still paint `composer-token-role`.
- **On the wire and the tape.** `toWireText` rewrites the draft
  (`Composer.tsx:4878-4882`), and the row draws `.mention-pill.role-mention`
  from the link. A name that does not convert is plain text on the tape
  (`Markdown.tsx:2055-2097`).
- **The brake** reads the sent text, so a converted name is braked as its role
  link would be (`lib/mention-brake.ts:16`; source only).

The fixture roles: `/rooms/` has `traders` (`r-traders`), **Full Stack**
(`01j8x4kq7m2v9p3r6t0w5y8z1a`) and **Devops** (`r-devops`)
(`tools/visual/shell-fixture.tsx:3507-3517`). `/chat/` has `traders` and
**Full Stack** only. No shim is needed for a plain conversion. Stub
`spaceRolesFor`, `spaceRolesLoaded` or `spaceMembersFor` on the shim's
`window.__om` and bump `__om.version` for the other cases.

```bash
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=topic&topic=cpi-print-aug&alerts=quiet')"
# wrap __om.sendToActiveDurably to keep its first argument, set the box through the
# native value setter and an input event, wait ~900 ms, read .composer-token, press Enter
#   "ping @Full Stack now"  -> chip "@Full Stack" composer-token-role; wire "ping om://role/01j8x4kq7m2v9p3r6t0w5y8z1a now"
#   "@devops and `@devops` and @traders and @mod and @trader"
#                           -> chips @devops, @traders, @mod; wire
#                              "om://role/r-devops and `@devops` and om://role/r-traders and om://role/mod and @trader"
#   spaceRolesLoaded=()=>false, "hi @mod and @Full Stack"  -> no chip
#   two roles named Twins, "@Twins hi"                       -> no chip; wire "@Twins hi"
#   an isApp member "relay" and a role "relay", "@relay and @Solo" -> chip @Solo only;
#                              wire "@relay and om://role/r-solo"
#   ?view=dm, "hi @traders and @Full Stack"                 -> no chip
```

Traps:

- Press Escape only while the `@` list is open, that is, when the text ends in
  a partial name. With the list shut, Escape leaves the topic, and the Enter
  that follows lands in the channel's composer.
- Wait about 900 ms after the input event before reading the chips. At 400 ms
  the role chip was not drawn yet.

Driven 2026-11-24 at `9c697d6e` on `/rooms/` (18186) and `/chat/` (18187),
except the `@devops`/`@traders`/`@mod` send, which needs **Devops** (`/rooms/`
only). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261124/r1/` (frames
`roles-*`).

### Same-named roles in the `@` list (added 2026-11-24)

Since `634f8e9a` the `@` list offers each named role as its own row, in role
order, and a pick binds that role's own link (`lib/role-refs.ts:30-52`,
`lib/composer-scope.ts:244-256`). A row whose name another offered role shares
(case-insensitive) carries a member count in `.composer-autocomplete-hint`:
"3 members", "1 member" or "no members" (`dda3b7a1`). The count comes from the
`roleIds` of `session.spaceMembersFor(spaceId)`. It is left off when that list
is empty or reaches 500 rows. An unshared name has no hint, and the base roles
keep their own rows with no count.

```bash
# on the topic route above, with the shim: give three spaceMembersFor rows roleIds
# (twin-a on three, twin-b on one), stub spaceRolesFor with Twins/twin-a, Twins/twin-b
# and Solo/r-solo, bump __om.version, then type "@Tw"
#   [role=option] rows: "@Twins ROLE 3 members", "@Twins ROLE 1 member"; "@So" -> "@Solo ROLE", no hint
```

Driven 2026-11-24 at `9c697d6e` on both hosts. A pick from these rows was not
proved: neither fixture defines `bindMentionLinksFor`, so without that stub a
role pick inserts nothing (see "Picks that send links"). The pick is covered
by `packages/chat-ui/test/composer/roles.test.ts`.

### Code is inert (added 2026-11-20)

Since `7fbe9218` nothing inside code is live, in a message, in any composer
and in the doc editor. `a1af61c7`, `1caf3e7b` and `de98f3b4` settle the edges.

- **Composer lists stay shut in code** (`writingCode`,
  `lib/composer-complete.ts:170`). The `@`, `#`, `:`, `$`, `[[` and `!` lists
  do not open when the sigil sits in an inline code span, after a fence that is
  still open, or after a backtick run that is still open. The `@`, `#` and `:`
  lists were driven on 2026-11-20. The `$` and `[[` lists were driven on
  2026-11-21 (`/rooms/`): `buy $` opens **MARKETS** with 8 options and
  `see [[` opens **REFERENCE** with 3; `` `buy $ ``, an open fence before
  `buy $`, and `` `see [[ `` open nothing; `` `x` then $ `` opens **MARKETS**
  again. `!` is source only (it needs the Projects stub).
- **An open run stays open across a closed span inside it** (`de98f3b4`). In
  ``see ``const x = `foo`; @an`` the double backtick never closes, so the `@`
  list stays shut. A backtick inside earlier, closed code opens nothing
  (`a1af61c7`).
- **No chip is drawn in code** (`lib/composer-pills.ts:282`, `:313`, `:599`):
  no mention, mass word, channel, link or picked chip. A picked chip later
  wrapped in code is sent as the words it shows (source and unit tests).
- **A sent message keeps code literal.** A mention, a role link, and a topic,
  doc, folder or tag link inside code stay code text. Cards and pills are
  lifted from the message's prose only (`literalAt`, `Markdown.tsx:2842`), so
  a link on a line inside a multi-line code span no longer splits the span.
- The doc editor's `@`, ticket and `[[` lists skip code the same way
  (`editor/mentions.ts`, `editor/ticket-refs.ts`,
  `editor/live-preview.ts:427`; source only).

```bash
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=room&alerts=quiet')"
# set the box, then read document.querySelector("[role=listbox]"):
#   "@"                           -> MEMBERS & ROLES, 14 options
#   "`@a"                         -> no listbox
#   "`x` @a"                      -> listbox (the span is closed)
#   "```\n@a"                     -> no listbox
#   "see ``const x = `foo`; @an"  -> no listbox
#   "`#o" / "`:smi"               -> no listbox; "#o" and ":smi" open theirs
# send "`@ana` and `om://role/r-devops` in code":
#   no .composer-token before the send; the row has two <code> and no .mention-pill
```

Driven 2026-11-20 at `7e3f0cde` on `/rooms/` and `/chat/` (frames 11, 12, 15).
The edit box agrees: with `roleEdit=1`, appending `` @traders and `@ana` ``
leaves the three seeded chips and adds none (frame 14). On 2026-11-20 the
`$` list was probed with a bare `$` after other text and did not open; the
2026-11-21 strings above do open it.

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

**Changed by `ca24a4b2` (2026-11-21).** A typed `@ana` on the fixture's own ids
is now plain text, so the 2026-11-04 result above no longer shows: `thanks
@ana. and @dax!` drew no chip and no `.mention-pill`. The trimming still
matters where a name converts: with a 24-hex member `nova`, `@everyone and
@nova.` chipped both names, sent `@everyone and om://user/<id>.` and drew
`.mention-pill.no-target` and `.mention-pill[data-handle="nova"]` with the
full stop after it (`/rooms/`, 2026-11-21). The tape tokenizer itself now
trims only for `everyone`, `here` and agents (`Markdown.tsx:2069-2078`).

### Slash commands (added 2026-10-30)

Typing `/` in the composer opens the command list from `SLASH_COMMANDS`
(`lib/slash-commands.ts:70`): 28 options on the root fixture (29 until `f6a1c31b` hid `/nudge` off Projects; counted again 2026-11-22), starting
`/dm`, `/help`, `/topic`, `/channel-invite`, `/invite`, `/join`, `/leave`,
`/follow`. Typing `/shr` narrows it to `/shrug` ("Appends ¯\_(ツ)_/¯ …").
Settings → **Slash Commands** (`settings-fixture.html?host=user&page=slash-commands`)
renders the guide page **Slash commands**. Running a command is pending: the
real handler is `ChatSession.handleSlash` (`lib/session.ts:41061`, called at
`:13592`, `:13810`, `:14137` and `:14203`), and the fixture's send only appends the text, so `/nick`,
`/status`, `/mute` and the daemon-bound verbs (`/chart`, `/capture`,
`/summarize`, `/brief`, `/agent`, `/reset`, `/arm`, `/disarm`) need an
authenticated or daemon rig. Driven 2026-10-30 on `/rooms/` (frame 51).

### App commands (added 2026-11-26, redrawn 2026-11-27)

An app installed in the server publishes commands (`session.appCommandsFor(spaceId)`).
They join the `/` list as rows with an **APP** chip, a hint `@<handle>`, and
argument placeholders `<@name>` for a member and `[name]` for an optional
text argument (`lib/composer-complete.ts:1880`). Since `3adfdf02`, `69a9ed43`,
`47f618d6` and `e20e9166` the picked command is drawn inside the input,
Discord-style:
- The textarea holds `/<command>`, not `@<handle> /<command>`. A required
  first argument adds its name as an option chip, and a member argument adds
  `@`, so the member list opens. The wire head `@<handle> /<command>` comes
  back on send and on park through a `command` binding
  (`lib/app-command-pills.ts:14`).
- The command and the option names paint as chips over the text
  (`.composer-token-command`, `.composer-token-option`;
  `withAppCommandPills`, `lib/app-command-pills.ts:66`). The argument being
  filled gets `is-active`. Option chips sit an en space apart
  (`APP_OPTION_GAP`, `:49`).
- The app's icon sits in the field's gutter (`.composer-app-avatar`,
  `Composer.tsx:6532`), not in a chip.
- A header bar above the box (`[data-testid=app-command-header]`,
  `Composer.tsx:6305`) names the argument being filled and its description,
  else the command. Its **Close /<command>** button (`:6323`) clears the draft.
- Unfilled arguments show as a grey ghost after the text
  (`.composer-app-ghost`, `:6641`). Optional ones collapse to `+N more`
  (`[data-app-command-more]`, `:6656`), which opens an **Options** list.
- A parked draft in wire form (`@app /cmd args`) is rewritten to the short
  form once the app's commands load (`Composer.tsx:2423-2437`,
  `bindAppCommandDraft`, `lib/composer-pills.ts:1409`).
- Sending with a required argument missing is still blocked. A warn toast
  reads `/<command> needs <args>` (`Composer.tsx:4272`) and the draft stays.
- In the tape, a post that parses as an invocation of an app in that room's
  server reads as typed (`8e54db16`): a `/<command>` chip
  (`.app-command-chip`, `[data-testid=app-command-use]`) at the message's own
  size and line height, then its arguments on the same line, wrapping as
  text. A picked member shows as their mention pill. A command with no
  arguments is just the chip. There is no **used** lead-in, and a one-line
  command post is exactly as tall as a one-line text post
  (`MessageRow.tsx:207`, `:2686`; `styles.css:3392-3423`). Webhook posts are
  left as they are.
- Sealed composers and an active private lane get no app rows.

The chip strip above the box (`[data-testid=app-command-slots]`) from
`9b874942` is gone.

The cloud shell fixture answers `appCommandsFor: () => []`
(`apps/cloud/tools/visual/shell-fixture.tsx:2251`). The root one answers
`APP_COMMAND_FIXTURE` (`tools/visual/shell-fixture.tsx:4217`), which holds
`pushover` (`/page <user> [message]`) and `shipit` (`/release-list`) only
under `?tape=apps`, and nothing otherwise. Stub an app through
the session-capture shim ([README.md](README.md), "Seed spelled-out keys with the session-capture shim"):

```bash
agent-browser eval '(()=>{const o=window.__om;o.appCommandsFor=()=>[{appUserId:"aaaaaaaaaaaaaaaaaaaaaaaa",handle:"modbot",commands:[{name:"page",description:"Page a member",args:[{name:"member",description:"Who",required:true,type:"user"},{name:"note",description:"Text"}]}]}];o.appCommandsLoaded=()=>true;window.__toasts=[];const t0=o.toast;o.toast=(...a)=>{window.__toasts.push(a);return t0?.(...a)};o.version=Number(o.version)+1;o.closeConfirm();return 1})()'
# set textarea.composer-field to "/pag" (native value setter + input event)
#   one option: "/page APP Page a member · <@member> [note] @modbot"
agent-browser press Enter
#   value "/page   member @"; .composer-token-command "/page"; one .composer-token-option "member";
#   .composer-app-avatar present; header "M member Who"; no [data-testid=app-command-slots]
agent-browser press Escape      # closes the @ list (in a channel, not a topic)
agent-browser press Enter
#   __toasts [["/page needs member","warn"]]; the draft stays
agent-browser find role button click --name "Close /page"
#   value ""; the header is gone
```

Driven 2026-11-27 at `5acbd605` on both hosts with these readouts, and
re-driven 2026-11-28 at `49bc8c00`. The `+N more` **Options** list,
the member pick, the sent invocation and the app's reply are pending; the
first needs a filled member, the others a store with an installed app.

**App command posts in the tape** (`8e54db16`). The root fixture's
`?tape=apps` (`tools/visual/shell-fixture.tsx:1336-1355`) adds, to `#ops`:
dax "what went out today?"; ana `@shipit /release-list` as a header row;
ana "one sec, checking"; ana `@shipit /release-list` as a continuation; and
two mira `/page` posts with a picked member `bryan` (a 24-hex id, so the
link binds as a pill), one short and one long enough to wrap. The cloud
fixture has no such tape: stub `appCommandsFor` as above and append rows to
`__om.rooms.get("ops").entries` (a new array, copied from the seq 104 post),
then bump `__om.version` and call `__om.closeConfirm()`.

Driven 2026-11-28 (step blocks `d1128-app-command-row` and
`d1128-app-command-row-chat` in `steps-delta-1128.txt`):

- `/rooms/`, `shell-fixture.html?view=room&tape=apps`: four chips (`/release-list`
  twice, `/page` twice) at `15px/24.375px`. A `/release-list` body reads only the
  inline sender name and `/release-list` ("ana (ops)/release-list"). Both
  `/release-list` rows are 32.38 px tall, the same as the plain "one sec,
  checking" row.
  The short `/page` body is one line (24.38 px), "/page @bryan the deploy is
  stuck on canary", with the **@bryan** pill on the chip's line and both
  24.38 px tall. The long one wraps to two lines (48.75 px). No row reads
  **used**.
- `/chat/`, three appended rows: "plain one line", `@shipit /release-list`
  and `@pushover /page someone the deploy is stuck on canary` read
  `/release-list` and `/page someone the deploy is stuck on canary`. All
  three rows are 32.38 px tall, and no row reads **used**.

**The dedicated harness** (`tools/visual/composer-app-command-fixture.html`,
since `69a9ed43`) mounts the real Composer over a stub session with a
`pushover` app whose `/page` takes `<@user> [message]`. It is `/rooms/`-only
and takes `?theme=dark|light`, `&width=<px>` and `&draft=<urlencoded>`.
Sends go to `window.sent`.

```bash
agent-browser open "$(control-om-chat url 'tools/visual/composer-app-command-fixture.html?theme=dark&width=760')"
# "/pag", Enter
#   value "/page   user @"; chips /page and "user" (is-active); header "P user User to page"
agent-browser open "$(control-om-chat url 'tools/visual/composer-app-command-fixture.html?theme=light&draft=%40pushover%20%2Fpage%20%40kyle%20hello')"
#   the parked wire draft restored short: value "/page   user @kyle   message hello"; chips /page, user, message
```

Driven 2026-11-27 on `/rooms/`. The harness does not stub
`bindComposerUrisFor`, so pasted links stay plain there.

### Paste: a link over a selection, an image into the composer (added 2026-11-01)

Both paths are pure client code behind `Composer.tsx:6821-6921`, so a
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

That staged card is the fixture's `acceptFile` stub (`shell-fixture.tsx:4478-4498`)
pushing a pending attachment and stamping `data-fixture-attachment`; no upload
or scan runs. OS drops onto the tape, the topic list or the library
(`useFileDropZone.tsx`) still need a real file through `setInputFiles` or a CDP
drop, and stay pending.

**A pasted link lands as the name it reads as** (share links since
`eae9681d`; user, role and topic links since `82414b0d`). The paste handler
calls `boundPasteInto` (`lib/composer-pills.ts:1474`). It gates on
`draftNeedsBinding` (`:242`): `om://` text, or a share link that the private
`hasRecognizedShareLink` (`:238`, `lib/share-links.ts:123`) accepts. Share links
are `https://openmarket.xyz/chat/…` and `https://chat.openmarket.sh/…` links to
a doc, topic, message or room, with no query or hash. A pasted
`om://user/<24 hex>` or `om://role/<id>` now lands as `@name`, bound to the
link it sends as. Before this, the composer painted `@handle` over 35 hidden
characters. A link the session cannot name, or one glued to a word or inside
code, stays as pasted. The paste is one native undo step. With no selection:

```bash
agent-browser eval '(()=>{const t=document.querySelector("#root textarea");t.focus();
  const dt=new DataTransfer();dt.setData("text/plain","https://openmarket.xyz/chat/room/ops/msg/104");
  const ev=new ClipboardEvent("paste",{clipboardData:dt,bubbles:true,cancelable:true});t.dispatchEvent(ev);
  return JSON.stringify({prevented:ev.defaultPrevented,value:t.value,draft:document.documentElement.dataset.fixtureDraft})})()'
#   /rooms/: {"prevented":true,"value":"↩ #ops·104","draft":"https://openmarket.xyz/chat/room/ops/msg/104"}
```

The share-link readout above is from 2026-11-10 and was not re-driven tonight.

Both fixtures now spell out `bindComposerUrisFor`
(`tools/visual/shell-fixture.tsx:3780`; cloud
`apps/cloud/tools/visual/shell-fixture.tsx:1776`). They resolve roles
(`r-devops` → Devops on `/rooms/`; `r-traders` → traders and the Full Stack id
on `/chat/`), but neither passes a user resolver, so a pasted user link stays
raw until you swap in one through the shim:

```bash
# role link, no stub (/rooms/; use om://role/r-traders on /chat/)
#   paste "om://role/r-devops please look" -> prevented, value "@Devops please look"
# user link: rebuild the binder with a user resolver from the page's own module
agent-browser eval '(async()=>{const u=performance.getEntriesByType("resource").map(e=>e.name).find(n=>/lib\/composer-pills\.ts/.test(n));
  const m=await import(u);const o=window.__om,id="6650a1b2c3d4e5f607182901";
  o.bindComposerUrisFor=(t,r)=>m.bindComposerUrisForDraft(t,()=>undefined,()=>undefined,l=>"#"+l,undefined,x=>x==="r-devops"?"Devops":undefined,x=>x===id?"bryanchow_0112":undefined);
  o.version=Number(o.version)+1;o.closeConfirm();return 1})()'
#   paste "om://user/6650a1b2c3d4e5f607182901 test" -> prevented, value "@bryanchow_0112 test"
```

Driven 2026-11-27 at `5acbd605`: the role paste on both hosts (each with its
own role id) and the stubbed user paste on both hosts. The inline edit box
binds the same way; see [message-editing.md](message-editing.md). The pill's
label baseline (`DraftBackdrop.tsx`, `82414b0d`) is a pixel-level change and
was not measured.

### The older-messages banner past 99 (added 2026-11-02)

`ChatPane.tsx:3280` prints **You're viewing older messages · 99+ new below**
once the count behind the banner passes 99 (`formatUnreadCount`,
`lib/animated-count-parts.ts:35-42`, since `4cd3434f`). No fixture seed raises
a room's new-below count that high (`bulk=120` pads the tape but the reader
sits at the bottom), so this is source-only. The banner itself mounts on
`shell-fixture.html?view=room&history=detached&alerts=quiet` and reads **You're
viewing older messages** with **Jump to present**, with no count, because the
fixture room's `unread` is a constant 0 (`shell-fixture.tsx:1649-1654`; driven
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
2026-11-09 on both hosts. Since `d3aebbb5` the fixtures spell out
`spaceMutes`, so set it through the session-capture shim
(`__om.spaceMutes.until = () => "2099-01-01T00:00:00Z"`, then bump
`__om.version` and call `__om.closeConfirm()`): driven 2026-11-22 on
`/rooms/`, the composer left and the notice read "You're muted in this server
until Jan 1, 8:00 AM.".

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
there (`Shell.tsx:1134-1177`): from `BODY`, `press a` left the textarea focused
with the value `a`. Typing `/` in `#ops` lists 28 commands: /dm, /help, /topic,
/channel-invite, /invite, /join, /leave, /follow, /mute, /nick, /poll,
/status, /chart, /me, /shrug, /spoiler, /tableflip, /unflip, /note, /template,
/todo, /agent, /arm, /brief, /capture, /disarm, /reset and /summarize (driven
2026-11-15 on both hosts). `/nudge` is hidden in a channel that is not on
Projects (`Composer.tsx:1547`, `:3007`). The bare fixture's `#ops` is such a
channel now that `f6a1c31b` reads an unstubbed Projects mode as off, so the
29th entry is gone. `/draw` (`lib/slash-commands.ts:199`) is not listed in the
fixture.

**The legacy to-do grammar is text off Projects.** In a channel that is not on
a Projects server, `/todo`, `/nudge`, `/assign` and `/unassign` post exactly as
typed (`CHANNEL_TODO_FORMS`, `lib/session.ts:1918`, used at `:41074`). The one
exception is `/todo <text> → me|here`, which still files to an Inbox. Typing `!`
offers no verb list there either (`lib/composer-complete.ts:1673-1730`): a 1:1
DM offers only `!nudge`, and a Projects channel offers the ticket verbs. Both
were driven 2026-11-15 on both hosts. `/todo buy milk` + Enter appends a row
reading "/todo buy milk" (rows 16 → 17) and clears the box, and a bare `!`
opens no listbox. The `→ me` capture was not driven.

### Esc steps back out (added 2026-11-16)

With focus outside an editor, each Esc closes the topmost dismissable thing
(`Shell.tsx:1177-1218`). The order is: the poll composer, a modal, the quick
switcher, the topic peek, the right panel, the doc pane, an agent lane, and
finally the topic view, which steps out to its channel. A plain channel keeps
Esc inert. The settings shells handle their own Esc. Blur first with
`eval '(()=>{document.activeElement.blur();return 1})()'`, or the composer's
own rungs take the press. Driven 2026-11-16 on `/rooms/`:

- `?view=topic&topic=cpi-print-aug`: Esc → `#/room/ops`, heading **#ops**.
- **Pins** pressed in the dock (**Close Pins**): Esc closes the panel. A
  second Esc in plain `#ops` changes nothing.
- `?view=room&topics=on&peek=cpi-print-aug` plus the topic hash: Esc closes
  the topic peek.
- `?view=room&doc=journal`: the note opens with the editor focused. Esc there
  only drops to reading (no `contenteditable=true` left; `DocPane.tsx:2216`).
  Esc from `BODY` closes the pane: `data-fixture-doc="closed"` at once, and the
  `[data-doc-pane-header]` leaves after about a second. A read at 700 ms still
  finds the header, which looks like a failure.

The poll composer, modal and switcher rungs were not driven, and nothing was
driven on `/chat/`.

### Zooming and panning an image preview (added 2026-11-16)

Every full-screen image preview shares `ImagePreviewShell.tsx` and
`lib/image-zoom-pan.ts:95`. The pill holds **Zoom out** and **Zoom in**; the
levels are 1, 1.5, 2 and 3 (`image-zoom-pan.ts:26`). The wheel zooms about
the pointer, and a drag pans within a clamp that keeps the image over the
stage. `/rooms/` only: the `/chat/` fixture has no image seed.

```bash
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=room&tape=mosaic5&alerts=quiet')"
agent-browser click 'img[alt="mosaic-1.svg"]'          # .ui-lightbox dialog; Zoom out disabled
agent-browser find role button click --name "Zoom in"   # img.lightbox-img.zoomed, scale(1.5)
# two more: scale(3), Zoom in disabled
agent-browser set viewport 800 600
agent-browser mouse move 400 300 && agent-browser mouse down
agent-browser mouse move 280 240 && agent-browser mouse up   # translate3d(-120px, -60px, 0px) scale(3)
```

At 1440×900 the 400 px mosaic image still fits the stage at 3×, so the clamp
pins it to `translate3d(0px, 0px, 0px)` and a drag reads as a no-op. Use a
smaller viewport. `agent-browser mouse wheel -300` over the stage steps the
zoom up one level at a time, and `+300` steps it back to fit. Driven
2026-11-16.

### Ticket references (added 2026-11-10)

Start the session with the people stub and the Projects stub from
[projects.md](projects.md), which answers `todos.lookup` and `todos.refs`:

```bash
agent-browser --init-script "$SCRATCH/fixture-people-stub.js" \
  --init-script "$SCRATCH/fixture-projects-stub.js" open about:blank
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=room&alerts=quiet')"
agent-browser click 'textarea.composer-field'
agent-browser keyboard type '!fix'        # TICKETS: "!1 Fix alert dedupe #ops Open"
agent-browser press ArrowDown             # Enter alone would send "!fix" as typed
agent-browser press Enter                 # value: "!1 Fix alert dedupe "
agent-browser keyboard type 'needs a look'
agent-browser press Enter                 # row: tag "Ticket !1, Open"
agent-browser click 'textarea.composer-field'
agent-browser keyboard type 'om://todo/s1/2'
agent-browser press Escape
agent-browser press Enter                 # row: card "Ticket !2" (In progress, Ship digest)
```

Pressing the tag routes to `#/todo/s1/1` on `/rooms/` and `/chat/todo/s1/1` on
`/chat/`. Both hosts passed step for step (2026-11-10). The fixture's tape does
not stay pinned to the bottom after these sends, so scroll the card into view
before a screenshot. A typed `!todo <title>` is held in the composer as a ticket
verb rather than sent.

### The `@` picker sections (added 2026-11-14)

With the people stub from [README.md](README.md):

```bash
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=room&alerts=quiet')"
agent-browser click 'textarea.composer-field'
agent-browser keyboard type '@'
# tabs: "Members 5" (aria-current) and "Roles 9"; eyebrows MEMBERS, ROLES; 14 options
agent-browser eval '(()=>{const t=[...document.querySelectorAll(".composer-autocomplete-tab")].find(b=>/^Roles/.test(b.textContent.trim()));t.dispatchEvent(new MouseEvent("mousedown",{bubbles:true}));t.click();return 1})()'
# "Roles 9" is now aria-current; the selected row is "@admin ROLE"; still 14 options
agent-browser press Enter                 # value: "@admin "
```

Clear the box (set the value and dispatch `input`), then type `@tr`: only one
tab, **Roles 1**, and one option, **@traders**. On `/chat/` the tabs read
**Members 5** / **Roles 8** (13 options) and the rest is the same. Driven
2026-11-14 on both hosts. No fixture shows the **Agents** tab: it needs roster
support or an `isAgent` member, and neither fixture has either.

### User links, base roles and a link to the viewer (added 2026-11-17)

No fixture seeds a link, and the fixture ids (`u-ana`, `u1`) are not 24-hex, so
`om://user/u-ana` is never a link. Seed a member with a hex id and posts through
the session-capture shim (README), on either host:

```bash
# people stub + session-capture shim, then ?view=room&alerts=quiet
agent-browser eval '(()=>{const o=window.__om,NOVA="6650a1b2c3d4e5f6a7b8c9d0",GONE="6650a1b2c3d4e5f6a7b8c9ff";
  o.membersFor().push({userId:NOVA,username:"nova",handle:"nova",presence:"online",tier:"member"});
  const nick=o.nicknameFor;o.nicknameFor=(s,u)=>u===NOVA?"Nova Reyes":nick(s,u);
  const r=o.rooms.get("ops");r.entries=[...r.entries,{seq:900,ts:Date.now(),room:"ops",handle:"dax",userId:"u-dax",
  isAgent:false,type:"post",text:`hi om://user/${NOVA}, om://user/${GONE}, om://role/admin and \`om://user/${NOVA}\``}];
  o.closeConfirm();return 1})()'
# #msg-ops-900: @Nova Reyes (role=link, title @nova), @unknown member (.no-target),
#   @admin (.role-mention.no-target), and the code span left as om://user/6650…
agent-browser click '#msg-ops-900 .mention-pill[data-handle="nova"]'
# /rooms/: dialog "Profile for nova" (Nova Reyes). /chat/: nothing opens (no openMentionCard there)
```

For a link to the viewer, set `o.auth.userId` to a hex id (the fixture's is
`u1`) and post `om://user/<that id> …` the same way: the row takes
`mention-wash`. The same link inside backticks does not. The pill itself reads
**@unknown member**, because the viewer has no member row under the new id.
Restore `o.auth.userId="u1"` before driving anything else.

### Picks that send links, and pill lines (added 2026-11-18)

Read the wire, not the row: wrap `sendToActiveDurably` and keep its first
argument. (Since `3387846a` a typed username converts too; see the next
section. This recipe proves the pick, because `people.searched` offers a
person who is in no member list.) Offer a 24-hex person through a cached `people.searched` hit (a
member pushed into `membersFor()` or the roster is not offered), and give the
fixture the `bindMentionLinksFor` it lacks from the real module. With the
fixture init and the session-capture shim (README), on `?view=room&alerts=quiet`:

```bash
# /chat/ imports the module from /chat/@fs<worktree>/packages/chat-ui/src/lib/composer-pills.ts
agent-browser eval '(async()=>{const o=window.__om,NOVA="6650a1b2c3d4e5f6a7b8c9d0";
  const P=await import("/rooms/packages/chat-ui/src/lib/composer-pills.ts");
  const hit={status:"ready",people:[{userId:NOVA,handle:"nova",username:"nova",displayName:"Nova Reyes"}]};
  o.people.searched=()=>hit;o.people.search=()=>()=>{};
  o.bindMentionLinksFor=(room,text)=>P.bindMentionLinksForDraft(text,(id)=>(o.spaceRolesFor?.("s1")||[]).find(r=>r.roleId===id)?.name);
  window.__sent=[];const f=o.sendToActiveDurably;o.sendToActiveDurably=(...a)=>{window.__sent.push(a);return f(...a)};
  o.closeConfirm();return 1})()'
agent-browser click 'textarea.composer-field'
agent-browser type 'textarea.composer-field' 'hey @nov'   # one option, Nova Reyes
agent-browser press Enter
agent-browser type 'textarea.composer-field' 'and @Dev'   # /chat/ has no Devops: use @Full
agent-browser press Enter
agent-browser type 'textarea.composer-field' 'please rerun'
agent-browser press Enter
agent-browser eval '(()=>JSON.stringify(window.__sent.map(a=>a[0])))()'
```

Driven 2026-11-18: the box read `hey @nova and @Devops please rerun` and the
wire `hey om://user/6650a1b2c3d4e5f6a7b8c9d0 and om://role/r-devops please rerun`
(on `/chat/`, `om://role/01j8x4kq7m2v9p3r6t0w5y8z1a` for **Full Stack**). The
row reads **@unknown member** and a `.role-mention` pill, since `people.held`
answers null. Without the `bindMentionLinksFor` line the role pick leaves
`hey @nova and please rerun` on both hosts.

For the pill lines, set the box through the native value setter and an `input`
event, then press Enter: `om://role/admin\n\nrequesting review\n\ncc desk` draws
`.mention-pill.role-mention` inside the first `<p>` of `.agent-md`, at the top of
the row. `om://topic/cpi-print-aug\n\nfirst\n\nsecond` draws `.message-ref-flow`
with one `.message-ref-block` whose `.agent-md` children read `BR,P,BR,P,…` and
no `<p>` inside `.message-ref-inline-text`. Both hosts, 2026-11-18.

### A typed username goes out as its holder's link (added 2026-11-21)

Since `ca24a4b2` a typed `@handle` names nobody: only an `om://user/<id>` link
does, for the pill, the row wash, the ping and the non-member gate. Since
`3387846a` the composer closes the gap for the sender. A typed `@username` is
rewritten to its holder's link on send, when exactly one person where the
message goes holds that username (`lib/typed-mentions.ts:153-220`,
`lib/mention-users.ts:402-417`). Since `5cbe2a54` the same reader also sends
typed role names as role links (see "A typed role name goes out as the role's
link").

- **Where it resolves.** In a channel or topic: the server's members plus the
  channel roster, without agent rows and app accounts. In a DM: its
  participants first, then everyone else the session holds (`97833bf3`,
  `47997903`). A name two people hold, or nobody holds, stays as typed.
- **What the box shows.** A name that will convert paints
  `composer-token-mention`; any other typed name paints nothing
  (`lib/composer-pills.ts:563-576`). The match ignores case.
- **What stays as typed** (`typed-mentions.ts:115-131`): text in code, a slash
  line, a whole `!assign`, `!unassign`, `!todo` or `!edit` marker
  (`1f4b7273`), an app's name or `@app /command` invocation (`430a7faf`), a
  name that wakes an agent, `@everyone` and `@here`, and a turn to an agent.
- **Only the box converts** (`314a2f67`): `toWireText` rewrites the draft
  (`Composer.tsx:4878-4882`) and the session posts what it is handed.
- **The non-member gate reads the link** (`lib/mention-audit.ts:44`,
  `Composer.tsx:4370`). A converted name whose holder is on the server but not
  in the channel roster opens **Not in this channel** with **Back** and **Send
  Anyway** (`MentionWarnDialog.tsx:38`). A typed name that did not convert
  never warns.
- The sent row draws the link as
  `<span class="mention-pill" data-handle="nova" role="link" title="@nova">`.

The fixture's own ids (`u-ana`, `u1`) are not link ids, so nothing converts
there until a 24-hex member exists. With the people stub and the
session-capture shim (README), on `?view=room&alerts=quiet`, either host:

```bash
agent-browser eval '(()=>{const o=window.__om,NOVA={userId:"6650a1b2c3d4e5f6a7b8c9d0",username:"nova",handle:"nova",presence:"online",tier:"member"};
  o.membersFor("ops").push(NOVA);            // the server's members (the same array as spaceMembersFor("s1"))
  o.rosters.get("ops").members.push(NOVA);   // the channel roster; leave this out to meet the gate
  window.__wire=[];const f=o.sendToActiveDurably;o.sendToActiveDurably=function(...a){window.__wire.push(a[0]);return f.apply(this,a)};
  o.isAppAccount=()=>false;                  // since da90467d; see below
  o.version=Number(o.version)+1;o.closeConfirm();return 1})()'
# set the box through the native value setter and an input event, press Escape (the @ list), then Enter
#   "ping @nova please"        -> chip composer-token-mention "@nova"; wire "ping om://user/6650a1b2c3d4e5f6a7b8c9d0 please";
#                                 row: .mention-pill[data-handle=nova][role=link][title="@nova"] "@nova"
#   "yo @NOVA and @Nova"       -> two chips; both go out as the link
#   "hey @nova and @ana ok"    -> one chip; "@ana" (u-ana) stays typed and draws no pill
#   "see `@nova` here"         -> no chip; wire unchanged; no pill
#   "!todo @nova fix the feed" -> no chip; wire unchanged
#   "/shrug @nova"             -> no chip; wire unchanged
#   "@nobody hi"               -> no chip; wire unchanged; plain text
```

The `o.version` bump is required: the composer rebuilds its reader per session
version, and `closeConfirm()` alone repaints without it, so the chip never
appears and the send goes out as typed.

The `isAppAccount` stub is required since `da90467d`. The reader now keeps
typed any roster member for whom `session.isAppAccount(userId)` is truthy
(`typed-mentions.ts:182-184`). Neither shell fixture defines `isAppAccount`,
so the fixture answers a truthy stand-in for everyone, and without the stub
`@nova` stays typed in the composer and in the edit box (measured 2026-11-24
on `/rooms/`; with the stub both hosts convert).

In a DM (`?view=dm&dm=ana&alerts=quiet`), give the peer a link id first:
`o.dms.get("ana").counterparties[0].userId="6650a1b2c3d4e5f6a7b8c9d1"`, push
`nova` into `o.membersFor("ops")`, wrap the send and bump the version as above.
Then `hi @ana see this` sends `hi om://user/…c9d1 see this`, `ask @nova about
it` sends nova's link (a person outside the DM), and `ask @zed` stays typed.
Typing `cc @an` lists **MEMBERS** with `ana`; Enter inserts `@ana ` with its
chip and the send carries the link. A pick and a typed name read the same on
the wire, so this does not tell the pick binding from the conversion.

Driven 2026-11-21 at `84e88e56`: the room strings on `/rooms/` (all of them)
and `/chat/` (the member, code and marker strings), the gate on `/rooms/`, and
the DM on both hosts. Not driven: a username two people hold, an app account,
an agent's name, a staged story card, the topic opener (`c9c5206d`) and the
world pane, which has no pill layer and never converts
(`world/WorldChatPane.tsx:140-162`). The row wash, ping and OS notification
for a link need a store.

### Blocked and click-to-load inline images (added 2026-11-21)

A Markdown image in a message never loads on its own unless its host is
allowlisted (`Markdown.tsx:92-98`, `:2434-2444`). Send
`![cross-origin plain](http://example.com/a.png) and ![secure](https://example.com/b.png) and ![data](javascript:alert(1))`:

- The `http:` image on another origin and the non-http scheme each draw
  `span.image-embed.blocked[role=img]` reading **Image blocked: <alt>**.
- The `https:` image draws `.image-embed[role=button]` named **Load image
  secure from example.com**.
- The row holds no `<img>`.

Driven 2026-11-21 at `84e88e56` on `/rooms/`. Pressing the load button and an
allowlisted host were not driven.

### Uploading line on a parked send (added 2026-11-21)

A send that waits on its own uploads shows `div.uploading-send-progress` under
its row, reading **Uploading <name> · N%**, or **Uploading N files · N%**
(`MessageRow.tsx:2820-2842`). The row must be yours, still pending (a negative
`seq`), with no delivery state, while `session.attachmentUploads` holds
uploads for the room that have not failed. The fixture spells out
`attachmentUploads: []`, so seed both through the shim:

```bash
agent-browser eval '(()=>{const o=window.__om,r=o.rooms.get("ops");
  r.entries=[...r.entries,{seq:-1,clientMsgId:"p1",room:"ops",handle:"kyle",userId:"u1",type:"post",text:"here is the report",ts:Date.now(),isAgent:false}];
  o.attachmentUploads=[{room:"ops",name:"report.pdf",progress:0.4,status:"uploading"}];
  o.isAppAccount=()=>false;                  // since da90467d; see below
  o.version=Number(o.version)+1;o.closeConfirm();return 1})()'
# .uploading-send-progress -> "Uploading report.pdf · 40%"
```

Assign a new `entries` array: a `push` onto the old one does not repaint the
tape. Driven 2026-11-21 at `84e88e56` on `/rooms/`. A real upload, the
several-files wording and the hand-off to the delivery state were not driven.

### Jumbo and inline emoji (added 2026-11-17)

`/rooms/` has a seed: `shell-fixture.html?view=room&alerts=quiet&tape=emoji`
(`tools/visual/shell-fixture.tsx:1320`) appends ana `😭`, dax `test 😭`, mira
`😭😭😭` and kyle 28 × `😭`. Read `.jumbo-emoji` and its computed `font-size`
on each of the last four rows: 48px, none, 48px, none. dax's `<p>` has
`font-family` starting `"OM Inline Emoji"` at 15px. `/chat/` has no `tape=`
seed. Type `😭😭` into `textarea.composer-field` and press Enter: the fixture
echoes kyle's row, and its `.jumbo-emoji` reads 48px.

### Letter tiles in the composer and in messages (added 2026-11-25)

Driven on `/rooms/` (18186) and `/chat/` (18187) at `557ee9ed`, no seed
needed (the fixtures echo sends):

- Type `:regional_indicator_l` into `textarea.composer-field`: one option,
  **🇱:regional_indicator_l:**, whose glyph cell holds a `.letter-tile` with
  `data-letter="L"`. Enter leaves `🇱 ` in the box.
- Send `go 🇱 now and 🇺🇸` (set the value with the native setter and dispatch
  `input`, then Enter): the echoed row holds exactly one tile, L, 24 px tall at
  a 15 px body, and the 🇺🇸 pair stays a native flag. The tile's
  `textContent` is still `🇱`.
- Send `🇱` alone: the row is `.jumbo-emoji` at 48 px and the tile is 55×55.
- Send `` `🇱` in code ``: the code span keeps the raw character, no tile.
- The picker side (search, the 26 tiles, the reaction chip) is in
  [polls-and-reactions.md](polls-and-reactions.md).

### Long drafts scroll in a wrapper (changed 2026-11-26)

Since `4bef5710` the textarea no longer scrolls itself.
- `div.composer-field-scroll` (`Composer.tsx:6506`, `styles.css:6854`) wraps the
  textarea and its `.composer-backdrop` in one grid cell. It is capped at
  `max-height: 320px` (295 px on a phone) and owns the scrollbar.
- `applyComposerAutogrow` (`Composer.tsx:1033`) sets the textarea to its full
  `scrollHeight` with `overflow: hidden` and `scrollTop` 0.
- `.composer-backdrop` is `position: relative`.
- The user-visible fix: a selection's highlight stays on its text while a long
  draft scrolls.

Read scroll state from the wrapper, never from the textarea:

```bash
# set textarea.composer-field to 40 lines (native value setter + input event)
agent-browser eval '(()=>{const t=document.querySelector("textarea.composer-field"),s=t.closest(".composer-field-scroll");return JSON.stringify({tScroll:t.scrollTop,tOverflow:getComputedStyle(t).overflowY,sMax:getComputedStyle(s).maxHeight,sH:s.clientHeight,tH:t.offsetHeight,bPos:getComputedStyle(document.querySelector(".composer-backdrop")).position})})()'
#   tScroll 0, tOverflow "hidden", sMax "320px", sH 320, tH 900, bPos "relative"
# select all, then set the wrapper's scrollTop to 200: wrapper 200, textarea 0, selection [0, 310] kept
```

Driven 2026-11-26 at `0f3fd22c` on both hosts at 1440×900. The highlight
drifting off its text on HiDPI happened on the compositor thread and cannot be
seen headless. It is covered by `packages/chat-ui/test/ui/autogrow-scope.test.ts`
and `test/composer-tall-mode.test.ts`.

### Agent cards, link previews and the download warning (added 2026-11-22)

Three things a message or a download can draw that no fixture seeds. Each was
driven through the session-capture shim by appending rows to `#ops` (assign a
new `entries` array; copy an ordinary post such as seq 104 as the template, not
the last row, which is a system row).

**Agent card.** An agent's message holding a fenced ` ```om-card ` JSON block
draws a card instead of the code (`tryParseAgentCard`,
`agent-md-components.tsx:81`; `MessageRow.tsx:2621`): title, description,
fields, footer and action buttons. Pressing an action calls
`session.runCardAction(<id>)`. The same fence from a person, and a fence whose
JSON does not parse, stay code blocks.

```bash
agent-browser eval '(()=>{const o=window.__om,r=o.rooms.get("ops"),t=r.entries.find(e=>e.seq===104);window.__card=[];o.runCardAction=(id)=>window.__card.push(id);const card=JSON.stringify({title:"Deploy?",description:"v1.2 to prod",fields:[{name:"Env",value:"prod",inline:true}],footer:"expires in 5m",actions:[{id:"go",label:"Go",style:"primary"},{id:"no",label:"No",style:"danger"},{id:"off",label:"Off",style:"secondary",disabled:true}]});const mk=(seq,x)=>({...t,seq,ts:Date.now(),...x});r.entries=[...r.entries,mk(301,{handle:"om",userId:"u-om",isAgent:true,text:"Plan:\n```om-card\n"+card+"\n```"}),mk(302,{handle:"ana",userId:"u-ana",isAgent:false,text:"human:\n```om-card\n"+card+"\n```"}),mk(303,{handle:"om",userId:"u-om",isAgent:true,text:"bad:\n```om-card\n{not json\n```"}),mk(304,{handle:"dax",userId:"u-dax",isAgent:false,text:"read https://example.com/a",unfurls:[{url:"https://example.com/a",title:"Example Domain",description:"A preview of the page",siteName:"Example"}]})];o.closeConfirm();return 1})()'
#   #msg-ops-301 .agent-card: "Deploy? v1.2 to prod Env prod expires in 5m", buttons Go, No, Off (disabled)
#   #msg-ops-302 and #msg-ops-303 keep pre > code.language-om-card
agent-browser find role button click --name "Go" --exact
agent-browser eval 'JSON.stringify(window.__card)'    # ["go"]
```

**Link preview card.** A row whose entry carries `unfurls` draws
`[data-unfurl-card]` under the text (`UnfurlCard.tsx:59`, gated on **Show link
previews**, `MessageRow.tsx:1773`): `#msg-ops-304` above reads "Example /
Example Domain / A preview of the page" and links to the URL. The same append
also proves the screen-reader line: the tape's polite live region reads "4 new
messages" for the four rows.

**The cashtag teach chip.** The first time a cashtag is on screen, a chip sits
above the composer (`[data-cashtag-teach]`, `ChatPane.tsx:5307-5328`): "$BTC is
live market data. Click it for the chart. Type $ to add your own." with a
**Dismiss** button. It belongs to `ChatPane`'s own tape, so open
`?view=room&alerts=quiet&policy=off`, send `$BTC looks strong` and read the
chip. On the default topics-allowed view the same send draws the pill and no
chip.

**Potentially dangerous download.** Before a risky file or link downloads, an
alert dialog asks first (`DangerousDownloadDialog.tsx`, mounted at
`Shell.tsx:4811`). Seed the request the session would set:

```bash
agent-browser eval '(()=>{const o=window.__om;window.__dl=[];o.closeDangerousDownload=()=>{o.dangerousDownload=null;o.closeConfirm()};o.dangerousDownload={kind:"link",name:"setup.exe",domain:"files.example.com",url:"https://files.example.com/setup.exe",onProceed:()=>window.__dl.push("proceed")};o.closeConfirm();return 1})()'
#   alertdialog "Potentially dangerous download": setup.exe; "This file may contain code or harmful content. Only download
#   it if you trust files.example.com. OM has not malware-scanned or verified this file as safe. Running it could damage
#   your computer or steal your data."; checkbox "Always trust files.example.com"; Cancel (focused), Download anyway
```

Enter on the focused **Cancel** closes it and downloads nothing. Ticking the
box and pressing **Download anyway** runs the download and writes the domain
to `localStorage["om.trustedDownloadDomains"]` (`["files.example.com"]`). A
request of `kind:"attachment"` reads "…if you trust the sender." and has no
trust box. An archive name adds "Files inside this archive may also be
harmful."

All four driven 2026-11-22 at `4b6f42b4`: the agent card, the preview card and
the download dialog on both hosts, the teach chip on `/rooms/`. Limits: the
rows and the request are seeded, so the agent's real card post, the relay's
unfurl, the click that raises the dialog (`MessageText.tsx:702`,
`lib/dangerous-files.ts`) and a real download were not driven. The chip's
**Dismiss** and its retirement by a pill click were not pressed.

## Gotchas

- **The connection strip waits out a grace delay.** `?connection=reconnecting`
  (`shell-fixture.tsx:2980`) renders **Reconnecting...** in the
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
  (`tools/visual/shell-fixture.tsx:3917-3918`), with a comment naming the lock
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
  `tools/visual/shell-fixture.tsx:4478`. Preview/lightbox behavior still needs
  preview-ready attachment metadata and is not established by that fixture
  path.
- **The seeded room video is a stub and only proves the fallback ladder.** The
  default `#ops` tape carries dax's "recording of the retest, plus the notes"
  (`msg-ops-110`, a 15.9 MB `.mov` plus a PDF; `shell-fixture.tsx:1132-1156`).
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
  `class="composer-token composer-token-doc"`, reading `om://doc/doc-card ⧉ doc:doc-card` (a `.composer-token-wire` run and a `.composer-token-label` run)
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

**Last verified:** 2026-11-28 (nightly maintenance). **Product commit:** `49bc8c00` (GitLab origin/main; rooms-client 0.126.0; 12 commits past `5acbd605`). **Scope:** new tonight: the posted app command row as typed (`/rooms/` `?tape=apps`, `/chat/` with shim-appended rows), with chip font, row heights, the inline pill and the wrap. Then the scripted re-drive of this guide's recipes by the kept step runner (`/rooms/` 18186, `/chat/` 18187 where the guide covers it, openscape 18188 for the world), motion blocks one session at a time, with the `notesForRoom` init script on every session. Every step was compared mechanically with the 2026-11-27 logs at `5acbd605`; apart from timing, dates and the blocks that crashed then on the `notesForRoom` fixture bug, every step gave the same result, so no regression came from the delta. **Limitations:** unchanged from the previous record. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261128/r1/`.

**Previous record:** 2026-11-27 (nightly maintenance). **Product commit:** `5acbd605` (GitLab origin/main; rooms-client 0.125.0; 27 commits past `0f3fd22c`). **Scope:** new tonight on both hosts: an app command drawn in the input (`/page   member @`, the command and option chips, the gutter avatar, the header, **Close /page**, the blocked-send toast); a pasted role link and a stubbed user link landing as names; a seeded webhook embed with no `<pre>`. On `/rooms/` the app-command harness (the pick, the parked wire draft restored short). Then the scripted re-drive of this guide's recipes by the kept step runner (`/rooms/` 18186, `/chat/` 18187 where the guide covers it, openscape 18188 for the world), motion blocks one session at a time, with a `notesForRoom` init script on every session (see alerts.md, Gotchas). Every block a judge flagged was re-run alone on this tree and on a baseline worktree at `0f3fd22c` (18189/18190); the results matched, so no regression came from the delta. **Limitations:** the `+N more` Options list, the member pick, a real app send, the share-link paste on `/chat/` and the pill-label baseline were not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261127/r1/`.

**Previous record:** 2026-11-26 (nightly maintenance). **Product commit:** `0f3fd22c` (GitLab origin/main; rooms-client 0.125.0; 7 commits past `557ee9ed`). **Scope:** new tonight on both hosts: app commands with `appCommandsFor` stubbed (the `/` row, the inserted invocation, the argument chips, the blocked send and toast, the **used** row) and the long-draft scroll wrapper. Then the scripted re-drive of this guide's recipes by the kept step runner (`/rooms/` 18186, `/chat/` 18187 where the guide covers it, openscape 18188 for the world), motion blocks one session at a time; two read-only judges compared every result with its expectation and each flagged block was re-run alone. **Limitations:** the member pick, a real app send and the HiDPI selection drift were not driven; in a topic the fixture echoes no sent row, so the `/chat/` role pill after a topic send cannot be read (the wire is right). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261126/r1/`.

**Previous record:** 2026-11-25 (nightly maintenance). **Product commit:** `557ee9ed` (GitLab origin/main; rooms-client 0.125.0; 11 commits past `9c697d6e`). **Scope:** new tonight on `/rooms/` (18186) and `/chat/` (18187): the `:regional_indicator_l` autocomplete row with its tile and the inserted 🇱; a sent lone 🇱 drawn as a tile inline (24 px) and jumbo (55 px), a 🇺🇸 pair left native, and a code span left raw; the rest of the guide by the kept step runner. **Limitations:** sends are fixture echoes. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261125/r1/`.

**Previous record:** 2026-11-24 (nightly maintenance). **Product commit:** `9c697d6e` (GitLab origin/main; rooms-client 0.125.0; 22 commits past `4b6f42b4`). **Scope:** `/rooms/` (18186) and `/chat/` (18187): typed role names going out as role links (`@Full Stack` on both hosts; `@devops`, `@traders`, `@mod` on `/rooms/`), roles not loaded, two same-named roles, an app account's name, a DM; the same-named role rows with member counts; a typed `@nova` with the `isAppAccount` stub on both hosts; plus the core-path re-drive of the rest of the guide. **Limitations:** a pick from a same-named row, the role tint and the brake on a converted name were not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261124/r1/`.

**Previous record:** 2026-11-22 (nightly maintenance). **Product commit:** `4b6f42b4` (GitLab origin/main; rooms-client 0.124.0; one commit past `84e88e56`). **Scope:** `/rooms/` (18186): a local send (16 → 17); the bare `@` list (14, **Members 5 / Roles 9**); the `@` list shut in an open code span and open after it; 28 slash commands; a role link's chip and pill; a typed `@traders` drawing no pill; the doc URI token; live inline formatting; the chart card's no-data state; the cashtag pill; the code panel from a typed fence and from `draft=`; jumbo emoji; link paste over a selection; image paste; the GIF picker; Vim mode in the composer; `reply=1`; the 390 px send button. New: the agent card, the link preview card and the download warning on both hosts, the cashtag teach chip with **Dismiss** on `/rooms/`, and the muted notice through the shim. `/chat/` (18187): a send, the 13-entry `@` list and `reply=1`. **Limitations:** the new rows and the download request are seeds. Delivery states, uploads, the invite card, the queue and the recovery nudge were not re-driven tonight. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261122/r1/`.

**Previous record:** 2026-11-21 (nightly maintenance). **Product commit:** `84e88e56` (GitLab origin/main; rooms-client 0.124.0; 33 commits past `7e3f0cde`). **Scope:** `/rooms/` (18193) and `/chat/` (18194), people stub and session-capture shim. A typed username a 24-hex member holds painted `composer-token-mention`, went out as `om://user/<id>` and drew `.mention-pill[data-handle]` on both hosts, in a room and in a DM (participant and outsider); the case-insensitive match, the code, `!todo`, slash and unknown-name exemptions and the **Not in this channel** gate on `/rooms/`. On the fixture's own ids `@traders`, `@ana` and `@dax` are plain text with no chip and no pill; `@everyone` and an `om://role` link still draw theirs. The chart card read **no chart data right now** on both hosts and **LIVE** on `/rooms/` with stubbed candles. `$` and `[[` lists stay shut in code (`/rooms/`). The blocked and click-to-load image spans and the uploading line (`/rooms/`). The bare `@` list is 14 options and `/` 28 on `/rooms/`. **Limitations:** ambiguous usernames, app accounts, agent names, the staged-card exemption, the topic opener and every store-side effect of a link (wash, ping, notification) are source or unit-tested only; the `!` list in code was not driven; the image load button and a real upload were not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261121/r1/` (frames 02-06, 09, 19, 20, 22, 24, 27, 28, 33).

**Previous record:** 2026-11-20 (nightly maintenance). **Product commit:** `7e3f0cde` (GitLab origin/main; rooms-client 0.122.0; 16 commits past `12f1ea24`). **Scope:** `/rooms/` (18193) and `/chat/` (18194), people stub and session-capture shim. A typed `@traders` paints no chip and sends a plain `.mention-pill` with no `role-mention` or colour, on both hosts; an `om://role` link still draws the role chip and pill (**@Devops** on `/rooms/`, **@Full Stack** on `/chat/`). The `@`, `#` and `:` lists stay shut in an inline span, an open fence and an open backtick run (the `de98f3b4` string included) and open after a closed span; a sent `` `@ana` `` and a coded role link stay code text. The bare `@` list still has 14 options on `/rooms/` and 13 on `/chat/`. On `/rooms/` the picks recipe was re-run: the box read `hey @nova and @Devops please rerun` and the wire `hey om://user/6650a1b2c3d4e5f6a7b8c9d0 and om://role/r-devops please rerun`; without the binding stub a role pick still leaves `ping `. **Limitations:** the brake on a role link that cannot be mentioned, the `$`, `[[` and `!` lists in code, a picked chip later wrapped in code, the doc editor lists and the ticket comment box are source or unit-tested only; the picks recipe was not re-run on `/chat/`; no other section of this guide was re-driven tonight. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261120/r1/` (frames 11-13, 15).

**Previous record:** 2026-11-18 (nightly maintenance). **Product commit:** `c19e2f70` (GitLab origin/main; rooms-client 0.119.0; 28 commits past `c18cfa37`). **Scope:** `/rooms/` (18181) and `/chat/` (18182), fixture init (README) and session-capture shim: `agentPicker=1` listed only the viewer's `argue` and nothing for `@sco`; `agentPicker=offline` dimmed `argue` with "offline · your om is off" and Enter or Tab left `@arg`; on `/rooms/` the **Edit message** box (`roleEdit=1`) showed the same dimmed row, and with `agentPicker=1` inserted `@argue `. A picked person sent `om://user/<id>` and a picked role `om://role/<id>` on both hosts, with `bindMentionLinksFor` stubbed; unstubbed, the role pick dropped the role. A role link on its own line stayed in the first paragraph, and a topic-link line kept the blank lines after it, on both hosts. **Limitations:** the owner rows, `@om` online, the allow row, a failed read keeping agents and the install refresh need a listed instance, which no fixture has; a parked draft keeping picks and the edit box sending picks as links were not driven; send-while-typing (`85c25912`) is unit-only. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261118/r1/`.

**Previous record:** 2026-11-17 (nightly maintenance). **Product commit:** `c18cfa37` (GitLab origin/main; rooms-client 0.119.0; 14 commits past `96644a29`). **Scope:** `/rooms/` (18171) and `/chat/` (18172), people stub and session-capture shim: the seeded `#msg-ops-900` drew **@Nova Reyes**, **@unknown member**, **@admin** and a literal code span on both hosts; on `/rooms/` the Nova pill opened **Profile for nova**, and `om://user/<viewer>` washed its row (`mention-wash`) while the same link in backticks did not. `tape=emoji` on `/rooms/` gave 48px `.jumbo-emoji` on `😭` and `😭😭😭`, none on `test 😭` (15px, `OM Inline Emoji` first) or on 28 × `😭`; on `/chat/` a sent `😭😭` read 48px. **Limitations:** the ping, badge, peek and `mentions:` effects of a link to the viewer were not driven (unit-tested in `test/people/user-links.test.ts`); the composer's non-member gate for a pasted link is unit-only (`composer/mention-warn.test.ts`), because the fixture roster equals the server members; no other composer section was re-driven (the 2026-11-16 record stands). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261117/r1/` (frames 04, 06, 07, 08, 11, 12).

**Previous record:** 2026-11-16 (nightly maintenance). **Product commit:** `96644a29` (GitLab origin/main; rooms-client 0.118.0; unchanged since the 2026-11-15 pass). **Scope:** `/rooms/` (18177), people stub: the Esc ladder's topic → channel, topic peek, right panel and doc pane rungs, and the editor's step back to reading; the image preview on `tape=mosaic5`, with **Zoom in** to 3× (button disabled), the wheel up and back to fit, and a drag pan of (−120, −60) at 800×600. The route smoke loaded both `composer-code-panel-fixture` routes (one `[data-code-panel]`, label **ts**). **Limitations:** the poll composer, modal and switcher rungs were not driven, and neither recipe was driven on `/chat/`, which has no image seed. The other composer recipes keep their 2026-11-15 record. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261116/r1/` (frames 12, 13).

**Previous record:** 2026-11-15 (nightly maintenance). **Product commit:** `96644a29` (GitLab origin/main; rooms-client 0.118.0; 8 commits past `62fcc01a`). **Scope:** `/rooms/` (18175) and `/chat/` (18176), people stub: `/` in `#ops` lists 28 commands without `/nudge`; `/todo buy milk` + Enter appends a row reading "/todo buy milk" (16 → 17) and clears the box; a bare `!` opens no listbox. **Limitations:** `/todo … → me` and the DM `!nudge` were not driven; the other composer recipes were not re-driven (the 2026-11-14 record stands). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261115/r1/` (frames 05, 21).

**Previous record:** 2026-11-14 (nightly maintenance). **Product commit:** `62fcc01a` (GitLab origin/main; 9 commits past `504b08d5`). **Scope:** `/rooms/` (18173) and `/chat/` (18174), people stub: the `@` picker's **Members**/**Roles** tabs, tab click selecting the first role, Enter inserting `@admin `, and `@tr` narrowing to **Roles 1**. **Limitations:** the Agents tab and the scroll-following active tab (the fixture list fits without scrolling); the DM in-flight clear is unit-proved only. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261114/r1/`.

**Previous record:** 2026-11-13 (nightly maintenance). **Product commit:** `504b08d5` (GitLab origin/main; rooms-client 0.117.0; 32 commits past `eae9681d`). **Scope:** `/rooms/` (18170) and `/chat/` (18171), people stub: live formatting (`composer-inline-bold`, `-strike`, `-code`, `-marker`; `-underline` on `/rooms/`); `/rooms/`: Vim NORMAL with one `.vim-block-cursor`; a lone `om://todo/s1/1` sent locally renders its card. **Limitations:** the other inline styles, undo of a pick, and delivery. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261113/r1/` (frames 13, 15, 24).

**Previous record:** 2026-11-10 (scheduled maintenance). **Product commit:** `eae9681d` (GitLab origin/main, rooms-client 0.115.0). **Scope:** with the people stub, a share-link paste into the `#ops` composer: on `/rooms/` (18141) it is prevented and binds to `↩ #ops·104`; on `/chat/` (18142) it is prevented and empties the composer (fixture gap: no `bindComposerUrisFor`). **Limitations:** doc and topic links were not pasted; no send after the paste. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261110/r1/` (frames 10, 18).

**Previous record:** 2026-11-10 (nightly). **Product commit:** `eae9681d` (GitLab origin/main, rooms-client 0.115.0). **Scope:** with the people and Projects stubs, on `/rooms/` (18186) and `/chat/` (18187): `!fix` lists **TICKETS** with "!1 Fix alert dedupe #ops Open"; Enter with nothing highlighted sends `!fix` as typed (`/rooms/`); ArrowDown + Enter inserts `!1 Fix alert dedupe `; the sent row carries **Ticket !1, Open**; a standalone `om://todo/s1/2` renders the card **Ticket !2**; the tag opens ticket 1. Local sends 16 → 18 rows. **Limitations:** the stubbed lookup and refs stand in for the store; the hidden-ticket state, the card's **Follow** and live updates were not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261110/r1/`.

**Previous record:** 2026-11-09 (scheduled maintenance). **Product commit:** `16da8ecf` (GitLab origin/main; one CI-only commit past `82390825`). `/rooms/` (18141): a local send in `#ops` (16 → 17 rows); a printable key from `BODY` focuses the composer; `/` lists 29 commands; the invite card (**Acme Desk**, 42 members, **Join**) after sending an invite code; the opening-room queue ("queued while opening" under `fixtureState=loading`); the recovery nudge shown and dismissed. `/chat/` (18142): the invite card and the recovery nudge. **Limitations:** **Join**, **Save it now** and every slash command were not run; the queue was driven on `/rooms/` only. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261109/r1/`.

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
