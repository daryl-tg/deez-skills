# Progress bars in a message

A fenced block tagged `progress` draws as labelled bars in a chat message
(`feb9be62`). It is for scripts and agents that post a status and keep editing
it.

## Sub-features

- **The fence.** Each line is `name: done/total [done|failed|paused|stalled] [| note]`
  (`packages/chat-ui/src/lib/progress-block.ts:4`, `:27`). With no state word a
  row is **done** when `done` equals `total`, and **running** otherwise.
- **Limits.** 1 to 20 rows, names of at most 64 characters and unique without
  regard to case, notes of at most 500 characters, `total` above zero and
  `done` not above `total` (`progress-block.ts:22-24`, `:52`). One bad line
  leaves the whole fence as an ordinary code block. A message draws at most
  four blocks (`Markdown.tsx:115`, `:3704-3726`).
- **What is drawn** (`components/ProgressBlock.tsx:36`, `:111-116`). A
  `.md-progress` group named **Progress**. Each row has its name, a
  `role="progressbar"` track named by the row with `aria-valuenow` as the
  percent and `aria-valuetext` such as "50%, 3 / 6", the percent, and a side
  label: the counts while running, or **Done**, **Failed**, **Paused** or
  **Stalled**. `data-state` on the row carries the state.
- **The line under a bar** is the author's note. Without one it reads "4 total"
  for a done row and "at 1" for a failed, paused or stalled row
  (`progress-block.ts:97-98`). A clamped note gets **Show more** / **Show
  less** (`ProgressBlock.tsx:136`): a button with `aria-expanded`, shown only
  when the note overflows its two lines.
- **The footer** counts in a fixed order, "1 done, 1 running, 1 not started,
  1 paused, 1 stalled, 1 failed" (`progress-block.ts:101-105`). Since
  `14c5a403` a row at zero with no state word counts as **not started**, not
  running. Only the footer says so: the row keeps `data-state="running"`, its
  0% bar and its counts. The footer also reads "Updated just now",
  "N min ago", "N h ago" or "N d ago" from the message's edit time, or its post
  time (`progress-block.ts:119-126`, `MessageRow.tsx:313-314`).
- **Only message rows draw bars** (`MessageRow.tsx:2647`, `:2690`). Documents
  keep the code block (`Markdown.tsx:3704`). Per the repo's
  `docs/feature-map/progress-block.md`, the pins panel, reply previews, the
  forward dialog and the composer also keep it (source only).
- The authored `pre` stays in the DOM with `hidden`, and the bars mount in a
  `.md-progress-host` after it.

## How to get to it (user POV)

Post a message that holds a code fence tagged `progress`, one line per task:
`Upload: 3/6 | Sending files`. Readers see bars. Edit the message to move
them.

## Driving it with control-om-chat

No fixture seeds a progress fence. Send one: the fixture composer echoes it as
a new row. Set the box through the native value setter, because typing a
newline sends.

```bash
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=room&alerts=quiet')"
agent-browser eval '(()=>{const t=document.querySelector("textarea.composer-field");
  const set=Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,"value").set;
  t.focus();set.call(t,"```progress\nUpload: 3/6 | Sending files\nIndex: 4/4\nSync: 2/5 failed | disk full\n```");
  t.dispatchEvent(new Event("input",{bubbles:true}));return 1})()'
agent-browser press Enter
agent-browser eval '(()=>{const r=[...document.querySelectorAll("[data-message-row]")].pop();
  return JSON.stringify({group:r.querySelector(".md-progress").getAttribute("aria-label"),
    bars:[...r.querySelectorAll(".md-progress-row")].map(x=>x.dataset.state+" "+x.querySelector("[role=progressbar]").getAttribute("aria-valuetext")),
    foot:r.querySelector(".md-progress-foot").innerText,pre:getComputedStyle(r.querySelector("pre")).display})})()'
#   group "Progress"
#   bars  ["running 50%, 3 / 6","done 100%, Done","failed 40%, Failed"]
#   foot  "1 done, 1 running, 1 failed" and "Updated 477 d ago" (see Gotchas)
#   pre   "none"
```

On `/rooms/` the three fills measured 230, 459 and 184 px of a 459 px track.
A five-row fence adding `Backfill: 1/8 paused` and `Mirror: 5/9 stalled` gave
"12%, Paused" with "at 1" and "55%, Stalled" with "at 5".

The fallback: send ```` ```progress ```` with `Upload: 7/6`, or with two rows
named `Upload` and `upload`. The row has no `.md-progress`, and its
`pre > code.language-progress` is visible.

Driven 2026-11-21 at `84e88e56` on `/rooms/`, each as one send built in the
`eval` (for example `Array.from({length:21},(_,i)=>"Task"+(i+1)+": 1/2").join("\n")`):

- **Not started.** `Queue: 0/5`, `Upload: 3/6 | Sending files`, `Index: 4/4`,
  `Hold: 0/3 paused` gave the footer "1 done, 1 running, 1 not started, 1
  paused". `Queue` kept `data-state="running"` with "0%, 0 / 5", and `Hold`
  read "0%, Paused" with "at 0". The same on `/chat/` with three rows.
- **Show more.** A note of about 320 characters showed **Show more**
  (`aria-expanded="false"`); pressing it turned it to **Show less**
  (`"true"`). A note past 500 characters is a bad line, so the fence stays
  code.
- **Four blocks.** A message with five fences drew four `.md-progress-host`
  groups and left the fifth as a code block reading `Job5: 5/5`.
- **Twenty rows.** Twenty rows drew one group with 20 rows; 21 rows stayed
  `pre > code.language-progress`.
- **An edit moves the bar.** `__om.beginEdit(<seq of your progress row>)`
  through the shim, a version bump and `closeConfirm()` open the edit box.
  Changing `Upload: 3/10` to `Upload: 7/10` and pressing Enter gave "70%, 7 /
  10", a 326 px fill, the row's edited mark and the footer "Updated just
  now".

### On `/chat/`

The cloud fixture does not import `shared/message-markdown.css` (the root
fixture does, `tools/visual/shell-fixture.tsx:117`; both apps do,
`src/main.tsx:37` and `apps/cloud/src/main.tsx:40`). Without it the block
mounts with the right roles and text but no bars: every track is 0 px wide and
the row reads "Upload50%3 / 6Sending files". Load the sheet through vite
first:

```bash
agent-browser eval '(async()=>{await import("/chat/src/shared/message-markdown.css"); return 1})()'
```

Then the same send measures 230, 459 and 184 px.

## Gotchas

- The echoed row carries the fixture's 2025 clock, so the footer reads
  "Updated 477 d ago" (on 2026-11-20). "Updated just now" and the minute and
  hour forms are unit-tested only.
- Read `aria-valuetext` and `data-state`, not the fill's inline style: the
  width comes from the `--md-progress-value` custom property.
- An edit that moves a bar animates from the old value
  (`Markdown.tsx:3714-3719`). The update was driven on 2026-11-21; the
  animation was not seen. The fill's computed transition was `width 1e-05s`
  in the headless browser, and the bar was at its new width 150 ms after the
  save.
- `pre` is still in the row. A probe that counts `pre` elements finds one even
  when the bars are drawn; check its computed `display`.

### Verification record

**Last verified:** 2026-11-25 (nightly maintenance). **Product commit:** `557ee9ed` (GitLab origin/main; rooms-client 0.125.0; 11 commits past `9c697d6e`). **Scope:** the scripted re-drive of this guide's recipes by the kept step runner (`/rooms/` 18186, `/chat/` 18187 where the guide covers it, openscape 18188 for the world), motion blocks one session at a time; every failing step was re-run alone and compared with this guide. This guide's source did not change in the delta. **Limitations:** unchanged from the previous record. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261125/r1/`.

**Previous record:** 2026-11-24 (nightly maintenance). **Product commit:** `9c697d6e` (GitLab origin/main; rooms-client 0.125.0; 22 commits past `4b6f42b4`). **Scope:** the scripted core-path re-drive of this guide's recipes (`/rooms/` 18186, `/chat/` 18187 where the guide covers it, openscape 18188 for the world); every failed or disagreeing step was re-run alone. This guide's source did not change in the delta. **Limitations:** unchanged from the previous record. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261124/r1/`.

**Previous record:** 2026-11-22 (nightly maintenance). **Product commit:** `4b6f42b4` (GitLab origin/main; rooms-client 0.124.0; one commit past `84e88e56`). **Scope:** `/rooms/` (18186): three bars with their states and footer; the **not started**, paused and stalled rows; **Show more** → **Show less**; a bad count staying code; the four-block cap; an edit moving a bar to 70% with "Updated just now". `/chat/` (18187): two bars with widths once `shared/message-markdown.css` is imported. **Limitations:** the 20-row cap was not re-driven tonight. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261122/r1/`.

**Previous record:** 2026-11-21 (nightly maintenance). **Product commit:** `84e88e56` (GitLab origin/main; rooms-client 0.124.0; 33 commits past `7e3f0cde`). **Scope:** `/rooms/` (18193): the **not started** footer group for a row at zero, **Show more** / **Show less**, the four-block cap, the 20-row cap and its 21-row fallback, and an edit moving a bar from 30% to 70% with "Updated just now". `/chat/` (18194): the **not started** footer, after importing `message-markdown.css`. **Limitations:** the bar's animation was not observed; the minute and hour footer forms and every surface that keeps the code block (pins, reply preview, forward, documents) are source or unit-tested only. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261121/r1/` (frames 01, 21, 29-31).

**Previous record:** 2026-11-20 (nightly maintenance). **Product commit:** `7e3f0cde` (GitLab origin/main; rooms-client 0.122.0; 16 commits past `12f1ea24`). **Scope:** `/rooms/` (18193): a three-row fence sent from the composer drew the **Progress** group, three `progressbar` tracks (50%, 100% Done, 40% Failed), the notes, the footer summary and fills of 230/459/184 px; `Upload: 7/6` and a duplicate name fell back to the code block. `/chat/` (18194): a five-row fence drew all five states with the right roles, value text and footer but no bars until `message-markdown.css` was imported; with the sheet, the same widths as `/rooms/`. **Limitations:** the edit-driven update and its animation, **Show more**, the four-block cap, the 20-row cap and every surface that keeps the code block (pins, reply preview, forward, documents) are source or unit-tested only. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261120/r1/` (frames 07-10).
