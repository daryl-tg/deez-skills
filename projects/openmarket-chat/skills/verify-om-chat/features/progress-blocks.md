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
  four blocks (`Markdown.tsx:113`, `:3718-3740`).
- **What is drawn** (`components/ProgressBlock.tsx:36`, `:111-116`). A
  `.md-progress` group named **Progress**. Each row has its name, a
  `role="progressbar"` track named by the row with `aria-valuenow` as the
  percent and `aria-valuetext` such as "50%, 3 / 6", the percent, and a side
  label: the counts while running, or **Done**, **Failed**, **Paused** or
  **Stalled**. `data-state` on the row carries the state.
- **The line under a bar** is the author's note. Without one it reads "4 total"
  for a done row and "at 1" for a failed, paused or stalled row
  (`progress-block.ts:97-98`). A clamped note gets **Show more** / **Show
  less** (`ProgressBlock.tsx:136`; not driven).
- **The footer** counts states in a fixed order, "1 done, 1 running, 1 paused,
  1 stalled, 1 failed" (`progress-block.ts:101`), and reads "Updated just now",
  "N min ago", "N h ago" or "N d ago" from the message's edit time, or its post
  time (`progress-block.ts:114-121`, `MessageRow.tsx:313-314`).
- **Only message rows draw bars** (`MessageRow.tsx:2653`, `:2697`). Documents
  keep the code block (`Markdown.tsx:3718`). Per the repo's
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

### On `/chat/`

The cloud fixture does not import `shared/message-markdown.css` (the root
fixture does, `tools/visual/shell-fixture.tsx:103`; both apps do,
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
  (`Markdown.tsx:3728-3733`). That update was not driven: no pass has edited
  a progress message in the fixture yet.
- `pre` is still in the row. A probe that counts `pre` elements finds one even
  when the bars are drawn; check its computed `display`.

### Verification record

**Last verified:** 2026-11-20 (nightly maintenance). **Product commit:** `7e3f0cde` (GitLab origin/main; rooms-client 0.122.0; 16 commits past `12f1ea24`). **Scope:** `/rooms/` (18193): a three-row fence sent from the composer drew the **Progress** group, three `progressbar` tracks (50%, 100% Done, 40% Failed), the notes, the footer summary and fills of 230/459/184 px; `Upload: 7/6` and a duplicate name fell back to the code block. `/chat/` (18194): a five-row fence drew all five states with the right roles, value text and footer but no bars until `message-markdown.css` was imported; with the sheet, the same widths as `/rooms/`. **Limitations:** the edit-driven update and its animation, **Show more**, the four-block cap, the 20-row cap and every surface that keeps the code block (pins, reply preview, forward, documents) are source or unit-tested only. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261120/r1/` (frames 07-10).
