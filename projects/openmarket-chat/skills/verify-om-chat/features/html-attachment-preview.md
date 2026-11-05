# HTML attachment preview

An `.html` file attached to a message can be previewed in place, inside a
sandbox that runs no script and loads nothing from the network (`76fe3a03`).

## Sub-features

- A **Preview** button on an `.html` attachment card
  (`[data-html-preview-open]`, `packages/chat-ui/src/components/AttachmentView.tsx`),
  beside its **Download <file>** link.
- Files over 2 MB get no **Preview**. The size line reads "3.0 MB · too large
  to preview (over 2 MB)".
- The preview `dialog`, named by the file name
  (`components/HtmlAttachmentPreview.tsx`), with **Download**, **Close
  preview** and the note "Scripts are turned off and nothing loads from the
  internet, so links don't open and some pages may look different. Download
  the file to see it in full."
- The frame is `iframe[title="Preview of <file>"]` with an empty `sandbox`
  attribute. Its `srcdoc` carries a `default-src 'none'` CSP
  (`lib/html-preview.ts`).
- Failure copy: "The preview couldn't load. Download it instead." (not driven).

## How to get to it (user POV)

In a conversation, find a message with an `.html` file attached and press
**Preview**. The page opens in a large dialog. Close it with **Close preview**,
or download the file instead.

## Driving it with control-om-chat

The shell fixtures seed no `.html` attachment. A dedicated harness mounts
`AttachmentView` with three rows. It is `/rooms/`-only, and it takes
`?theme=light` (anything else is dark) and `?probe=<url>` (default
`http://127.0.0.1:31479`, the address the malicious sample tries to reach):

```bash
agent-browser open "$(control-om-chat url 'tools/visual/html-attachment-fixture.html')"
agent-browser eval '(()=>JSON.stringify([...document.querySelectorAll("[data-testid^=html-]")].map(r=>r.dataset.testid+": "+r.innerText.replace(/\n/g," / "))))()'
#   html-benign: q3-desk-report.html / 2 KB / Preview / Download
#   html-malicious: malicious-test.html / 2 KB / Preview / Download
#   html-large: huge-export.html / 3.0 MB · too large to preview (over 2 MB) / Download
agent-browser eval '(()=>{document.querySelector("[data-testid=html-malicious] [data-html-preview-open]").click();return 1})()'
agent-browser eval '(()=>{const f=document.querySelector("[role=dialog] iframe");return JSON.stringify({title:f.title,sandbox:f.getAttribute("sandbox"),csp:/default-src .none./.test(f.srcdoc),pwned:typeof window.__pwned})})()'
#   {"title":"Preview of malicious-test.html","sandbox":"","csp":true,"pwned":"undefined"}
agent-browser find role button click --name "Close preview"
```

## Gotchas

- The frame has an opaque origin, so `contentDocument` is unreadable. Assert
  on the `sandbox` attribute, the `srcdoc` and the parent's globals, or read
  the frame through an ARIA snapshot.
- Proving "nothing loads from the network" needs a listener on the `?probe=`
  address that counts requests. This map's 2026-11-06 drive did not start
  one, so the network half is source-backed only.
- `/chat/` has no copy of this harness. The component is shared, but the
  `/chat/` attachment path is not driven.

### Verification record

**Last verified:** 2026-11-06 (nightly maintenance). **Product commit:** `ea399e62` (GitLab origin/main; rooms-client 0.111.0). **Scope:** `/rooms/` (18180) `html-attachment-fixture.html`: the three rows; **Preview** on the malicious row opened the dialog **malicious-test.html** with **Download** and **Close preview**; the frame had `sandbox=""`, a `default-src 'none'` CSP and no `window.__pwned`; **Close preview** closed it. **Limitations:** no probe listener was run; the benign preview and the failure copy were not driven; `/chat/` has no harness. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261106/r1/` (`17`, `18`).
