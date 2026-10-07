# The dashboard agent panel

*Verified: 2026-10-07, tree `03bd55226` (v0.432.0) — opened panel, previewed/removed page context, sent a message and followed the Connections refusal; opened `/agent`. Real model response needs an LLM credential.*

Since v0.400.0 every dashboard page carries an `Ask your agent` button that
opens a chat panel beside the page. The panel shares the page you are on as
context, offers starter questions, and can hand off to a full conversation. On a
home with no LLM credential it accepts the message and then refuses, pointing at
the new Connections page.

## Sub-features

- `open-panel` toggles the panel from any page.
- `page-context` shares the current page with the agent, previewable and
  removable.
- `suggested-questions` offers one-press starters.
- `send` posts a message and streams a reply.
- `full-conversation` hands off to the whole thread.
- `connections` is where a missing credential is fixed.
- `full-page` is the two-pane `/agent` workspace the panel hands off to.

## How to get to it (user POV)

- Press `Ask your agent` on any dashboard page, type, press send.
- Or press one of the suggested questions.

## Driving it with control-om

Preconditions:

- A lane the run started and a browser session of your own. Nothing else for the
  refusal path; an LLM credential for anything beyond it.

- **Open it.** `agent-browser find role button click --name "Ask your agent"`
  yields `region "Ask your agent"` holding `heading "Ask OpenMarket"`,
  `button "Open full conversation"`, `button "Close agent panel"`,
  `region "Messages"`, `textbox "Message your agent"`,
  `button "Send message"` (disabled while the box is empty),
  `button "Preview shared page context"`, `button "Remove page context"`, and a
  `region "Suggested questions"` with page-specific help (on Watches,
  `Explain watches` and `Help me get started here`; the first prompt follows
  the current page title).
- **Assert the disabled send.** It enables only once the textbox has text; a
  driver that clicks it first silently does nothing.
- **Send, and read the refusal.** Fill the textbox, press `Send message`. The
  message appears as `article "Your message"`, then an `alert` replaces the
  reply. Its text is the whole finding on a guest lane:
  `No LLM API key configured. Run \`om init\`, or export OPENMARKET_LLM_KEY for
  this shell.` beside `button "Reload conversation"` and
  `link "Check connections"`. The accessibility tree renders that paragraph
  empty, so read it with
  `agent-browser eval '(()=>{const a=document.querySelector("[role=alert]");return a?a.innerText:"no alert"})()'`.
- **Follow the route it offers.** `link "Check connections"` leads to
  `/connections`: `heading "Connections"` with sections `AI model` and
  `Coding agents`. The integration rows and disabled `Connect` buttons depend
  on which clients are detected and wired on this machine.
- **Proof.** Keep the panel snapshot, the alert text read through `eval`, and the
  `/connections` snapshot. Together they are the evidence that the unmet
  prerequisite is a credential and not a broken surface.

- **The panel is not the whole surface.** `/agent` is a real route holding a
  two-pane workspace (a conversation history list beside the chat), reached
  either by `Open full conversation` or by the sidebar brand link whose
  accessible name is `OpenMarket, chat with your agent`. It is NOT a nav item,
  so a driver walking the nav will never find it. Open `/agent` directly or use
  `Open full conversation` to inspect the history rail and chat workspace.

## Gotchas

- **A real conversation is out of reach on a guest lane.** The concrete unmet
  prerequisite is an LLM credential (`om init`, or `OPENMARKET_LLM_KEY` in the
  daemon's environment). The chat turn returns `missing_llm_key` with the
  message below (`packages/cli/src/agent/runtime.ts`); `agent_not_configured`
  belongs to the separate model-selection RPC. Report the panel as
  `verified-unreachable` past the send, never as broken — the refusal is the
  feature working.
- The alert's text is invisible to `snapshot`: the paragraph node renders with no
  accessible name. Read it from the DOM or you will report an empty alert.
- `Send message` is disabled until the textbox has content, so a
  fill-then-click sequence is required; clicking first looks like a dead button.
- **Fill it with `agent-browser fill @<ref>`, not with an `eval` that sets
  `value`.** The composer is a controlled React input: a DOM-level value write
  leaves the button disabled and the send silently does nothing, which reads as
  a broken surface. Driven both ways — the ref form works, the eval form does
  not.
- The panel is global, not per page — it appears in snapshots of every route,
  including the watch-authoring dialogs, where it is noise.
- `Remove page context` changes what the agent is told about. If a run ever does
  reach a credentialed conversation, note whether context was attached; two runs
  that differ there are not comparable.
