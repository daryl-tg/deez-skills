# Code blocks in messages

## Sub-features

- A fenced block in a message renders as `pre.code-wrap` inside the message's
  `.agent-md.agent-md-chat`, with a `.code-header` band (the language control,
  e.g. **Plain text**) and a copy control: `span.code-copy` with `role="button"`
  and `aria-label="Copy"` (`packages/chat-ui/src/components/Markdown.tsx:2455`).
- A fence tagged `progress` draws as bars, not as a code block, when every
  line parses (`feb9be62`): see [progress-blocks.md](progress-blocks.md).
- Since `2350a0fd`, chat messages wrap long lines instead of scrolling them:
  `.agent-md-chat .code-wrap > code` is `white-space: pre-wrap` and
  `overflow-wrap: anywhere`, so an unbroken token breaks anywhere
  (`packages/chat-ui/src/components/code-block.css`). Documents keep horizontal
  scrolling.
- The `<code>` does any scrolling, never the `<pre>`. The copy control is
  positioned against the `<pre>`, so it stays inside the block on desktop and
  on a phone. The header band is no longer `position: sticky`.
- Copy reads `code.textContent`, so wrapping does not change what is copied.

## How to get to it (user POV)

Send or read a message with a fenced block. A long line (a key, URL or log
line) wraps inside the block. The copy button stays at the block's top right,
however long the line is.

## Driving it with control-om-chat

The default `#ops` tape seeds one block: dax's
`om alert list --room ops --since 24h` (`msg-ops-106`;
`tools/visual/shell-fixture.tsx:1107`, and
`apps/cloud/tools/visual/shell-fixture.tsx:346` on `/chat/`). To prove wrapping,
send a long unbroken line from the composer, because no seed has one.

Both shell fixtures load `code-block.css` through `src/app-styles.ts` since
`27156df5`, as the apps do. Measure on the page as it loads; no injection.
On 2026-11-26 the seeded `msg-ops-106` block read `white-space: pre-wrap` with
its **Copy** control on both hosts.

```bash
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=room&alerts=quiet')"
# Fill the composer (textbox "Message #ops · $ for markets · /chart to post one") with
# ```\n<300 unbroken characters>\n``` through the native value setter plus an input
# event, then press Enter. The new row is the last [data-message-row] pre.
agent-browser eval '(()=>{const p=[...document.querySelectorAll("[data-message-row] pre")].pop();
  const c=p.querySelector("code"), b=p.querySelector(".code-copy").getBoundingClientRect(), r=p.getBoundingClientRect();
  return JSON.stringify({ws:getComputedStyle(c).whiteSpace, fits:c.scrollWidth<=c.clientWidth, copyInside:b.right<=r.right&&b.left>=r.left})})()'
```

Expect `pre-wrap`, `fits: true` and `copyInside: true` at 1440×900 and at
390×844.

## Gotchas

- Records before `27156df5` (2026-11-25 and earlier) measured with the
  stylesheet injected, because the fixtures did not load it then.
- `agent-browser type` into the composer does not reliably keep the newlines
  around a fence. Set the value with the native `HTMLTextAreaElement` setter and
  dispatch `input`, then press Enter.
- A `pre` you find may be the seeded block or the Mermaid source (`msg-ops-116`
  with `?mermaid=1`). Read the row id before believing it is yours.
- The composer's own fence panel (`[data-code-panel]`) is a different surface;
  see [composer-and-sending.md](composer-and-sending.md).

### Verification record

**Last verified:** 2026-11-28 (nightly maintenance). **Product commit:** `49bc8c00` (GitLab origin/main; rooms-client 0.126.0; 12 commits past `5acbd605`). **Scope:** the scripted re-drive of this guide's recipes by the kept step runner (`/rooms/` 18186, `/chat/` 18187 where the guide covers it, openscape 18188 for the world), motion blocks one session at a time, with the `notesForRoom` init script on every session. Every step was compared mechanically with the 2026-11-27 logs at `5acbd605`; apart from timing, dates and the blocks that crashed then on the `notesForRoom` fixture bug, every step gave the same result, so no regression came from the delta. **Limitations:** unchanged from the previous record. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261128/r1/`.

**Previous record:** 2026-11-27 (nightly maintenance). **Product commit:** `5acbd605` (GitLab origin/main; rooms-client 0.125.0; 27 commits past `0f3fd22c`). **Scope:** the scripted re-drive of this guide's recipes by the kept step runner (`/rooms/` 18186, `/chat/` 18187 where the guide covers it, openscape 18188 for the world), motion blocks one session at a time, with a `notesForRoom` init script on every session (see alerts.md, Gotchas). Every block a judge flagged was re-run alone on this tree and on a baseline worktree at `0f3fd22c` (18189/18190); the results matched, so no regression came from the delta. **Limitations:** unchanged from the previous record. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261127/r1/`.

**Previous record:** 2026-11-26 (nightly maintenance). **Product commit:** `0f3fd22c` (GitLab origin/main; rooms-client 0.125.0; 7 commits past `557ee9ed`). **Scope:** the seeded block re-read on both hosts with no stylesheet injected (`pre-wrap` with **Copy**), since `27156df5` loads `code-block.css`. Then the scripted re-drive of this guide's recipes by the kept step runner (`/rooms/` 18186, `/chat/` 18187 where the guide covers it, openscape 18188 for the world), motion blocks one session at a time; two read-only judges compared every result with its expectation and each flagged block was re-run alone. **Limitations:** the wrapping send was not re-measured at 390. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261126/r1/`.

**Previous record:** 2026-11-25 (nightly maintenance). **Product commit:** `557ee9ed` (GitLab origin/main; rooms-client 0.125.0; 11 commits past `9c697d6e`). **Scope:** the scripted re-drive of this guide's recipes by the kept step runner (`/rooms/` 18186, `/chat/` 18187 where the guide covers it, openscape 18188 for the world), motion blocks one session at a time; every failing step was re-run alone and compared with this guide. This guide's source did not change in the delta. **Limitations:** unchanged from the previous record. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261125/r1/`.

**Previous record:** 2026-11-24 (nightly maintenance). **Product commit:** `9c697d6e` (GitLab origin/main; rooms-client 0.125.0; 22 commits past `4b6f42b4`). **Scope:** the scripted core-path re-drive of this guide's recipes (`/rooms/` 18186, `/chat/` 18187 where the guide covers it, openscape 18188 for the world); every failed or disagreeing step was re-run alone. This guide's source did not change in the delta. **Limitations:** unchanged from the previous record. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261124/r1/`.

**Previous record:** 2026-11-22 (nightly maintenance). **Product commit:** `4b6f42b4` (GitLab origin/main; rooms-client 0.124.0; one commit past `84e88e56`). **Scope:** `/rooms/` (18186): the seeded block on `msg-ops-106` (`pre.code-wrap`, the **Copy** `span[role=button]`, the language control); **Copy** adding `copied`; with the stylesheet injected, a sent 300-character line wrapping with **Copy** inside the block at 1440 and at 390; a bad `progress` fence staying code. `/chat/` (18187): `pre-wrap` on the seeded block with its stylesheet injected. **Limitations:** the clipboard was not read back. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261122/r1/`.

**Previous record:** 2026-11-20 (nightly maintenance). **Product commit:** `7e3f0cde` (GitLab origin/main; rooms-client 0.122.0; 16 commits past `12f1ea24`). **Scope:** `/rooms/` (18193): the seeded `#msg-ops-106` block is `pre.code-wrap` with the **Plain text** header and `span.code-copy[role=button]` **Copy**. A `progress` fence that fails to parse falls back to this block (see progress-blocks.md). **Limitations:** wrapping was not re-measured, and **Copy** was not pressed. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261120/r1/` (frame 10).

**Previous record:** 2026-11-09 (nightly maintenance). **Product commit:** `82390825` (GitLab origin/main; rooms-client 0.114.0; 49 commits past `08fe407b`). **Scope:** `/rooms/` and `/chat/` `view=room`, with the people stub: `span.code-copy[role=button]` **Copy** and **Code block language**. **Limitations:** the clipboard was not read back. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261109/r1/`.

**Previous record:** 2026-11-08 (nightly maintenance). **Product commit:** `08fe407b` (GitLab origin/main; rooms-client 0.112.0; unchanged since the 2026-11-07 pass). **Scope:** `/rooms/` (18183) and `/chat/` (18184) `view=room`: the code block's `span.code-copy[role=button]` **Copy** and **Code block language**. **Limitations:** the clipboard was not read back. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261108/r1/`.

**Previous record:** 2026-11-07 (nightly maintenance). **Product commit:** `08fe407b` (GitLab origin/main; rooms-client 0.112.0; 89 commits past `ea399e62`). **Scope:** `/rooms/` (18180) and `/chat/` (18181) `view=room`: the code block's **Copy** control (its name is not in `aria-label` or `title`) and **Code block language**. **Limitations:** wrapping not re-driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261107/r1/`.

**Previous record:** 2026-11-06 (nightly maintenance). **Product commit:** `ea399e62` (GitLab origin/main; rooms-client 0.111.0; 74 commits past `873a57ce`). **Scope:** `/rooms/` (18180) and `/chat/` (18181) `view=room`: one **Copy** control. **Limitations:** wrapping not re-driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261106/r1/`.

**Previous record:** 2026-11-04 (nightly maintenance). **Product commit:** `ce14d4ba` (GitLab origin/main; rooms-client 0.109.1; 16 commits past `ba4389e7`). **Scope:** `/rooms/` (18160) `?view=room`: one `.code-copy` control named **Copy**. **Limitations:** wrapping was not re-driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261104/r1/`.

**Previous record:** 2026-11-03 (nightly maintenance). **Product commit:** `ba4389e7` (GitLab origin/main; rooms-client 0.108.0; one CI-only commit past `3f8f24bc`). **Scope:** `/rooms/` (18143) and `/chat/` (18144): the seeded tape renders one `pre` with its `span.code-copy[role=button]` **Copy**. **Limitations:** the wrapping proof (which needs the stylesheet injected) was not re-driven; the 2026-11-02 record stands. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261103/r1/`.

**Previous record:** 2026-11-02 (scheduled maintenance). **Product commit:** `3f8f24bc` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18141) and `/chat/` (18142), `view=room&alerts=quiet` at 1440×900 with `code-block.css` injected (`/rooms/src/…` and `/chat/src/…`): a sent 300-character fence reads `pre-wrap|true|true` (wraps, no horizontal overflow, **Copy** inside the block) on both hosts. **Limitations:** the 390 px width was not re-measured this pass. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261102/r1/`.

**Previous record:** 2026-11-02 (nightly maintenance). **Product commit:** `3f8f24bc` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18137): a 300-character fence sent with `code-block.css` injected wrapped at 958 px with no horizontal overflow and a button inside the `pre`. **Limitations:** `/chat/` was not re-driven tonight (the 2026-11-01 record stands). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261102/r1/`.

**Previous record:** 2026-11-01 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18137) and `/chat/` (18138): with `code-block.css` imported through the lane (`/rooms/src/components/code-block.css`, `/chat/src/components/code-block.css`), a sent fence of 300 unbroken characters rendered `pre.code-wrap > code` with `white-space: pre-wrap`, `overflow-wrap: anywhere`, `scrollWidth === clientWidth` (936 on `/rooms/`, 974 on `/chat/`) and the **Copy** control inside the `pre`, under an `.agent-md-chat` ancestor. **Limitations:** the clipboard write, the seeded short block's **Copy** and the document reader's horizontal scroll were not re-driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261101/r1/` (`codeblock-01-rooms`, `codeblock-01-chat`).

**Previous record:** 2026-10-31 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18135) and `/chat/` (18136): `msg-ops-106` carries `pre.code-wrap` with a `.code-header` and a `.code-copy[aria-label="Copy"]`. **Limitations:** Wrapping with the stylesheet injected, the clipboard write and the doc reader's horizontal scroll were not re-driven (2026-10-29 stands). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261031/r1/`.

**Previous record:** 2026-10-30 (scheduled maintenance). **Product commit:** `47cb13bf` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` with `code-block.css` injected: a sent 300-character fence computed `pre-wrap`, `fits: true` and `copyInside: true` at 1440, and `pre-wrap` 254/254 at 390. A reading taken mid-resize showed `fits: false`, so measure after the viewport settles. `/chat/`: the seeded block has one `pre` and one `.code-copy`. **Limitations:** Clipboard write; doc-reader scroll. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261030/r1/` (frames 24-25).

**Previous record:** 2026-10-29 (nightly maintenance). **Product commit:** `cdfb1b0f` (origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` at 1440×900 with `code-block.css` injected: a sent fence of 300 unbroken characters (the last `[data-message-row] pre`, 301-character `code`) read `pre-wrap`, `fits: true`, `copyInside: true`, copy control **Copy**. **Limitations:** 390×844 and `/chat/` were not re-driven; clipboard write not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261029/r1/` (frame 31).

**Previous record:** 2026-10-28 (nightly maintenance). **Product commit:** `2dd7aad1` (origin/main). **Scope:** On `/rooms/`, with `code-block.css` injected, a sent 300-character unbroken fenced line (`msg-ops-116`) computed `white-space: pre-wrap`, fit its box (`scrollWidth <= clientWidth`) and kept `.code-copy` inside the `<pre>`, at both 1440×900 and 390×844. **Limitations:** The clipboard write, the seeded `msg-ops-106` block, `/chat/` and the document reader's horizontal scroll were not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261028/r1/` (frame 05).

**Previous record:** 2026-10-27. **Product commit:** `6c15b0fb286e9dc1b6cb130c9c97cd7e0afa9254` (origin/main; the change is `2350a0fd`). **Scope:** On `/rooms/`, with `code-block.css` injected, the seeded block's `<code>` computed `pre-wrap` / `anywhere` / `display: block`, the `<pre>` `overflow-x: visible` and the header `static`. A sent 308-character unbroken fenced line (`msg-ops-117`) wrapped with no horizontal overflow and kept **Copy** inside the block, at 1440×900 and 390×844. On `/chat/`, the seeded block computed `pre-wrap` with **Copy** present once the stylesheet was injected. **Limitations:** The real copy-to-clipboard was not exercised. The document reader's horizontal scroll was not re-measured. The bundled app was not driven, so the fixture's missing import was worked around rather than proved absent from the bundle. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261027/r01/` (frames 14-15).
