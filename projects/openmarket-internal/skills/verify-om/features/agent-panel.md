# The dashboard agent panel

*Re-driven 2026-11-01 (nightly), tree `7ce379c45` (origin/main, v0.480.3), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 2.9. On `/alerts`, `Ask your agent` opened `region "Ask your agent"` with `heading "Ask OpenMarket"`, `textbox "Message your agent"` and `button "Send message"`; after `fill @<ref>` and `Send message`, `article "Your message"` appeared and the alert read `No LLM API key configured. Run om init, or export OPENMARKET_LLM_KEY for this shell.` with `button "Reload conversation"` and `link "Check connections"`. `/agent` rendered `Conversations` and `What can I help with?`. Evidence: `http://127.0.0.1:8098/vom-nightly-20261101/r1/` (`dash-agent-panel*`, `dash-agent*`, `cli/dash-agent-panel-alert.txt`).*

*Re-driven 2026-10-31 (nightly), tree `dfefe0a21` (origin/main, v0.480.2), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 1.6. On `/alerts`, `Ask your agent` opened `region "Ask your agent"` with `heading "Ask OpenMarket"`, `textbox "Message your agent"` and `button "Send message"`; after filling the box and sending, `article "Your message"` appeared and the alert read `No LLM API key configured. Run om init, or export OPENMARKET_LLM_KEY for this shell.` with `button "Reload conversation"` and `link "Check connections"`. `/agent` rendered `Conversations` and `What can I help with?`. Evidence: `http://127.0.0.1:8098/vom-nightly-20261031/r1/` (`dash-agent-panel*`, `dash-agent*`).*

*Re-driven 2026-10-30 (scheduled maintenance), tree `3cb50a821` (origin/main, v0.478.0), fresh lane on 18165, host load average about 140. On `/alerts`, **Ask your agent**, a typed message and **Send message** produced the alert "No LLM API key configured. Run `om init`, or export OPENMARKET_LLM_KEY for this shell." with **Reload conversation** and **Check connections**. `/agent` read "What can I help with?" and "No conversations yet." Evidence: `http://127.0.0.1:8098/verify-om-maint-20261030/r1/` (frames 23, 31).*
*Re-driven 2026-10-30 (nightly, render only), tree `3cb50a821` (origin/main, v0.478.0), lane on 18163: `/agent` rendered the H1 `What can I help with?`. The `Ask your agent` button was present on `/alerts`, but the refusal was not re-driven. Evidence is local only (the `8098` renderer did not answer): `artifacts/vom-nightly-20261030/r1/`.*

*Re-driven 2026-10-29 (nightly, smoke depth), tree `32ca0d6c7` (origin/main, v0.467.0), lane on 18104: `Ask your agent` → fill → `Send message` gave the alert `No LLM API key configured.` (it goes on to name `om init` and `OPENMARKET_LLM_KEY`) with `Reload conversation` and `Check connections`. `/agent` showed `Conversations` and `No conversations yet.` Evidence: `http://127.0.0.1:8098/vom-nightly-20261029/r1/`.*

*Re-driven 2026-10-28 (scheduled maintenance, smoke depth), tree `186030b63` (origin/main): `/agent` rendered **Conversations** and **What can I help with?**. No conversation was sent. Steps not named here keep the record below. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261028/r1/`.*

*Verified: 2026-10-28, tree `a8fa10974` (origin/main, v0.466.0), lane on 18104. `Ask your agent` on `/alerts` showed the region, `Ask OpenMarket`, `Open full conversation`, `Close agent panel`, the message box, a disabled `Send message`, the page-context buttons, and the `Explain watches` / `Help me get started here` suggestions. A send produced `article "Your message"` and the alert `No LLM API key configured. Run om init, or export OPENMARKET_LLM_KEY for this shell.` beside `Reload conversation` and `Check connections`. `/agent` showed `Agent conversations`, `Conversations`, `What can I help with?` and `Recent conversations`. A reply needs an LLM credential. Previous stamp `8fe6a8432` is an ancestor (10 commits).*

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
- **The full-page workspace.** `agent-browser open "$(control-om url /agent)"`
  (also the sidebar brand link `OpenMarket, chat with your agent`) renders
  an `Agent conversations` rail with `heading "Conversations"` and, on an
  empty conversation, the H1 `What can I help with?`. Driven at `42d044b02`.
  `Load earlier messages`, the `Stop reply` button and tool approval cards need
  a credentialed conversation and stay unreachable on a guest lane.

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
