# Mermaid rendering

## Sub-features

- A fenced `mermaid` block in a persisted channel message renders as an inline SVG diagram.
- The same fence in a direct message uses the identical renderer and safety fallback.
- Invalid or refused Mermaid stays visible as authored code.
- The inline diagram is a keyboard-focusable button named `Open Mermaid diagram as PNG`.
- Enter or click opens the PNG preview region named `Mermaid diagram PNG preview. Right-click or press Shift+F10 for actions.`
- The SVG view box contains the live rendered content, including long labels.

- Library reading mode and editor preview render attribute-free Mermaid label breaks (`<br>`, `<br/>`, `<br />`) without changing source.

## How to get to it (user POV)

Post a fenced Mermaid block in a channel or DM. The message should show the diagram in place of the code fence. Focus the diagram and press Enter, or click it, to open the PNG preview.

## Driving it with control-om-chat

Use the whole-shell fixture with `mermaid=1`:

```bash
export OM_CHAT_LANE_PORT=<assigned-port>
./control-om-chat up
agent-browser open "$(./control-om-chat url 'tools/visual/shell-fixture.html?view=room&alerts=quiet&mermaid=1')"
agent-browser wait --fn 'document.querySelector(".doc-mermaid svg") !== null'
agent-browser snapshot -i -c
```

The DM route is `tools/visual/shell-fixture.html?view=dm&dm=ana&alerts=quiet&mermaid=1`. On both routes, drive the button named `Open Mermaid diagram as PNG`, then check for the named preview region.

For clipping checks, compare `svg.getBBox()` with `svg.viewBox.baseVal`. The view box must contain the content on all four sides. The Playwright recipe is `tools/visual/mermaid-message.visual.ts`.

For library documents, use `tools/visual/shell-fixture.html?view=room&doc=server&mermaid=labels&alerts=quiet`. This seats all three diagrams from OpenScape 2D vs 3D in the real DocPane. Open **Edit**, open a diagram preview, choose **Edit Mermaid Source**, and move the cursor to **End of diagrams.** The selected fence reveals its original source; moving away restores its diagram. **Publish** stays disabled until bytes change. The maintained recipe is `tools/visual/mermaid-library.visual.ts`.

## Gotchas

- `test/message-full-render.test.ts` mounts a room `MessageRow`. It does not prove the real `DmTape` path.
- DOM presence alone misses clipped charts. Inspect a screenshot and assert content containment against the live SVG view box.
- Mermaid rendering and the PNG preview are lazy. Wait for `.doc-mermaid svg` before taking refs or screenshots.
- The shell fixture currently emits an existing React textarea `value` warning. Treat only that exact warning as baseline; new console errors still fail the visual recipe.
- Mermaid accessibility directives belong inside the diagram declaration, after `flowchart LR` for this fixture.

- Assert visible label text, multiple line positions, and positive SVG bounds. The DOM-only Mermaid harness can return an empty SVG successfully. An SVG count alone does not prove rendering.
- The shell fixture must set `dockedDocCollapsed: false`; its truthy fallback otherwise hides every docked document.
