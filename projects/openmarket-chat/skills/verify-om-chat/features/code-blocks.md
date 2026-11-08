# Code blocks in messages

## Sub-features

- A fenced block in a message renders as `pre.code-wrap` inside the message's
  `.agent-md.agent-md-chat`, with a `.code-header` band (the language control,
  e.g. **Plain text**) and a copy control: `span.code-copy` with `role="button"`
  and `aria-label="Copy"` (`packages/chat-ui/src/components/Markdown.tsx:2403`).
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
`tools/visual/shell-fixture.tsx:1114`, and
`apps/cloud/tools/visual/shell-fixture.tsx:348` on `/chat/`). To prove wrapping,
send a long unbroken line from the composer, because no seed has one.

**Neither shell fixture imports `code-block.css`.** Only the app entries do
(`src/main.tsx:40`, `apps/cloud/src/main.tsx:44`). On the fixture lane the block
renders with `white-space: pre` and an inline `<code>`, which looks like the
pre-`2350a0fd` behavior. Load the real stylesheet into the page through vite
before you measure:

```bash
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=room&alerts=quiet')"
agent-browser eval '(async()=>{await import("/rooms/src/components/code-block.css"); return 1})()'
# /chat/ lane: import("/chat/src/components/code-block.css")
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

- Without the injected stylesheet, the measurements describe the fixture, not
  the product. Say in the manifest that you injected it.
- `agent-browser type` into the composer does not reliably keep the newlines
  around a fence. Set the value with the native `HTMLTextAreaElement` setter and
  dispatch `input`, then press Enter.
- A `pre` you find may be the seeded block or the Mermaid source (`msg-ops-116`
  with `?mermaid=1`). Read the row id before believing it is yours.
- The composer's own fence panel (`[data-code-panel]`) is a different surface;
  see [composer-and-sending.md](composer-and-sending.md).

### Verification record

**Last verified:** 2026-11-09 (nightly maintenance). **Product commit:** `82390825` (GitLab origin/main; rooms-client 0.114.0; 49 commits past `08fe407b`). **Scope:** `/rooms/` and `/chat/` `view=room`, with the people stub: `span.code-copy[role=button]` **Copy** and **Code block language**. **Limitations:** the clipboard was not read back. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261109/r1/`.

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
