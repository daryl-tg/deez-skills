# Mermaid rendering

## Sub-features

- A fenced `mermaid` block in a persisted channel message renders as an inline SVG diagram.
- The same fence in a direct message uses the identical renderer and safety fallback.
- Invalid or refused Mermaid stays visible as authored code.
- The inline diagram is a keyboard-focusable button named `Open Mermaid diagram as PNG`.
- Enter or click opens the PNG preview region named `Mermaid diagram PNG preview. Right-click or press Shift+F10 for actions.`
- The SVG view box contains the live rendered content, including long labels.

- Library reading mode and editor preview render attribute-free Mermaid label breaks (`<br>`, `<br/>`, `<br />`) without changing source.
- A linked-message card (a message link on its own line) renders the target's markdown, code and Mermaid through `MessageText` (`908855a1`). A message link inside a card stays an inline citation, so cards never nest.
- Rendered diagrams are cached per viewer and purged at logout or account switch (`2e1100a5`, `lib/mermaid-svg-cache.ts`). This is not visible in the fixture. Diagrams must simply still render, and unit tests cover the cache.

## How to get to it (user POV)

Post a fenced Mermaid block in a channel or DM. The message should show the diagram in place of the code fence. Focus the diagram and press Enter, or click it, to open the PNG preview.

## Driving it with control-om-chat

Use the whole-shell fixture with `mermaid=1`:

```bash
export OM_CHAT_LANE_PORT=<assigned-port>
control-om-chat up
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=room&alerts=quiet&mermaid=1')"
agent-browser wait --fn 'document.querySelector(".doc-mermaid svg") !== null'
agent-browser snapshot -i -c
```

The DM route is `tools/visual/shell-fixture.html?view=dm&dm=ana&alerts=quiet&mermaid=1`. On both routes, drive the button named `Open Mermaid diagram as PNG`, then check for the named preview region.

Linked-message card: on the room route, send a standalone share link to the seeded Mermaid post. At `afabb11c` it is still seq 116, but re-measure, because the fixture's `post()` counter (`shell-fixture.tsx:1056`) shifts when seeds change:

```bash
agent-browser find role textbox fill --name 'Message #ops · $ for markets · /chart to post one' 'https://openmarket.xyz/chat/room/ops/msg/116'
agent-browser press Enter
agent-browser eval '(()=>{const r=[...document.querySelectorAll("[data-message-row]")].pop();return JSON.stringify({author:r.querySelector(".forwarded-author")?.innerText,svg:r.querySelectorAll(".forwarded-content .doc-mermaid svg").length})})()'
```

Expect author `kyle` and one svg. Then send a link to that new post (seq 117). Expect one `.forwarded-content`, zero nested `.forwarded-content`, and an inline citation `↩ #·116`. The origin must be `OM_CHAT_SHARE_ORIGIN` (`https://openmarket.xyz/chat`, `share-links.ts:3`). The fixture's `?links=1` plain URLs are not share links and never make a card.

For clipping checks, compare `svg.getBBox()` with `svg.viewBox.baseVal`. The view box must contain the content on all four sides. The Playwright recipe is `tools/visual/mermaid-message.visual.ts`.

For library documents, use `tools/visual/shell-fixture.html?view=room&doc=server&mermaid=labels&alerts=quiet`. This seats all three diagrams from OpenScape 2D vs 3D in the real DocPane. Open **Edit**, open a diagram preview, choose **Edit Mermaid Source**, and move the cursor to **End of diagrams.** The selected fence reveals its original source; moving away restores its diagram. **Publish** stays disabled until bytes change. The maintained recipe is `tools/visual/mermaid-library.visual.ts`.

## Gotchas

- `packages/chat-ui/test/message/full-render.test.ts` mounts a room `MessageRow`. It does not prove the real `DmTape` path.
- DOM presence alone misses clipped charts. Inspect a screenshot and assert content containment against the live SVG view box.
- Mermaid rendering and the PNG preview are lazy. Wait for `.doc-mermaid svg` before taking refs or screenshots.
- The shell fixture currently emits an existing React textarea `value` warning. Treat only that exact warning as baseline; new console errors still fail the visual recipe.
- Mermaid accessibility directives belong inside the diagram declaration, after `flowchart LR` for this fixture.
- **The `/chat/` fixture has no `?mermaid=1` seed** (`apps/cloud/tools/visual/shell-fixture.tsx` has no mermaid branch). On that host a linked-message card renders, but it resolves seq 116 to a plain message, so the diagram-in-card proof is `/rooms/`-only until the cloud fixture gains the seed.

- Assert visible label text, multiple line positions, and positive SVG bounds. The DOM-only Mermaid harness can return an empty SVG successfully. An SVG count alone does not prove rendering.
- The shell fixture must set `dockedDocCollapsed: false`; its truthy fallback otherwise hides every docked document.

### Verification record

**Last verified:** 2026-10-29 (nightly maintenance). **Product commit:** `cdfb1b0f` (origin/main; rooms-client 0.108.0). **Scope:** `?view=room&alerts=quiet&mermaid=1` rendered `.doc-mermaid` with an `svg` and the control **Open Mermaid diagram as PNG**. **Limitations:** `/chat/` and the diagram cache not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261029/r1/` (frames 08, 37).

**Previous record:** 2026-10-28 (nightly maintenance). **Product commit:** `2dd7aad1` (origin/main). **Scope:** `?view=room&alerts=quiet&mermaid=1`: `msg-ops-116` rendered `.doc-mermaid` with an `svg` and the control **Open Mermaid diagram as PNG**. **Limitations:** The preview region, the linked-message cards, the DM route, `/chat/`, unsafe or invalid diagrams and the PNG export were not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261028/r1/` (frame 15).

**Previous record:** 2026-10-27. **Product commit:** `6c15b0fb286e9dc1b6cb130c9c97cd7e0afa9254` (origin/main). **Scope:** `?mermaid=1`: `msg-ops-116` rendered `.doc-mermaid` with the `role=button` control **Open Mermaid diagram as PNG**. **Limitations:** The preview region, the linked-message cards (seq 116/117), the DM route, `/chat/`, unsafe or invalid diagrams and the cache were not re-driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261027/r01/` (frame 28). Previous record: 2026-10-26 at `5820fbea`.
