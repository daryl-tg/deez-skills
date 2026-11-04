# Persona setup from om chat

*Re-read 2026-11-05 (nightly), CLI only, tree `3a0ea623e` (origin/main, v0.492.0), guest lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), booted in 2 s at 19:19Z with no guest 429, host load average about 4.4: `om persona show` printed the default persona and its `MCP clients:` row. The chat flow (`persona_infer`, the card) was not re-driven. Evidence: `http://127.0.0.1:8098/vom-nightly-20261105/r1/` (`cli/persona-show.out`).*

*Re-driven 2026-11-03 (nightly), tree `777ee7f21` (origin/main, v0.488.0; #2256 merged as `0d6993613`). First drive on main, on a **guest** lane home (18163, daemon down in a guest sign-in 429, no rooms identity), source `om chat --no-workspace`, tmux 140x40, auto-approve on, a scripted fake model on 18164. Seeded `om persona set "voice: clipped, wry. vom-nightly-20261103" --source verify` and `config set mcp.operator_voice on`. "set up my persona" ran `tool_search` (`names: persona_infer, persona_set`) and then `persona_infer {pasted: <7 lines>}` → `{"proposal":…,"samples":7,"roomsRead":0}` with the reply guidance to show it and ask. "yes save it" raised the card (`approval needed` / `persona_set`; `VOICE` over two lines, `REPLACES voice: clipped, wry. … (managed by verify)`, `USED BY om drafts, MCP clients`, `Save this as your persona?`, no `d` row for a short voice). `n` → `What should the agent do instead?`, Esc → `✗ declined persona_set`, `om persona show` unchanged; a second yes and `y` → `✓ approved persona_set`, and `om persona show` printed the new text as `Your persona` with no managing tool. CLI: `persona set ""` exit 2 (`a persona cannot be blank; remove the stored one with \`om persona clear\``), `persona clear --if-source other` → `persona left in place, managed by verify, not other`, `persona show --json` `{…,"source":"verify","mcpOperatorVoice":true}`. MCP stdio: `persona_show` is listed and answered `mcpOperatorVoice: "on"`; `persona_set` → `Tool persona_set not found` (and `persona_infer` is not listed). Not driven: room sampling (needs a rooms identity), a real model's tool choice, the thin-sample and no-model refusals. Evidence: `http://127.0.0.1:8098/vom-nightly-20261103/r1/` (`tui/09`–`14`, `cli/persona-*.txt`, `cli/30-mcp-pre.json`, `fake-log.jsonl`).*

*Verified: 2026-11-02. Branch `daryl/persona-tools` at `cc7a755c5`, later rebased to `50c026306` (PR #2256, then off origin/main; on main since `0d6993613`, v0.487.0).*

*Setup: source `om chat`, tmux 140x44, auto-approve on. The home was fresh, holding only the operator's device key (`credentials.json`, `device-id`; no vault). The daemon port was 18173, with nothing listening. The model was a scripted fake on 18172.*

*What happened:*
- *"set up my persona" ran `tool_search` → `persona_infer` (40 own messages from 12 real rooms, 12 s).*
- *"yes save it" raised the `persona_set` card. Its rows were `VOICE … (+2 lines)`, `REPLACES voice: clipped, wry` and `USED BY om drafts, MCP clients`; `d` showed the full text.*
- *`y` stored the exact text, which `om persona show` printed back. `n` stored nothing.*

*Not driven:*
- *a real model's tool choice;*
- *`persona_show` from chat;*
- *the thin-sample and no-model refusals (unit-tested only).*

*Evidence: `~/dev-notes-artifacts/om-persona-tools/run-artifacts/` (text captures; nothing was published to 8098).*

Ask `om chat` to set up your persona. om reads a sample of your own room messages, or messages you paste, and proposes a voice. Nothing is saved until you approve the exact text on a card. The card shows the new voice, the persona it replaces and the tool that manages it, and who uses it: om drafts, and MCP clients when `mcp.operator_voice` is on. The card appears even with auto-approve on. Neither tool is offered over MCP.

## Sub-features

- `persona-show`: reads the persona in force, whether it is stored, its managing tool, the card census and the MCP voice state (`on`, `off` or `on_no_persona`). It is the default of the `persona` routing family and is operator-only over MCP.
- `persona-infer`: reads your own room messages, or `pasted` text (one message per line, up to 40,000 characters, replacing room history), and proposes a voice with one model call. It returns `proposal`, `samples` and `roomsRead`, and saves nothing. Each failure is typed:
  - `persona_thin_sample`: under 5 own messages;
  - `llm_not_configured`;
  - `persona_infer_empty`;
  - `persona_infer_too_long`;
  - `persona_infer_failed`, which names a refused call's reason.
- `persona-set-card`: a tier 3 card with the rows `VOICE`, `REPLACES` and `USED BY`, and the full text under `d details`. `y` stores the exact text and drops any managing tool. `n` stores nothing.
- `persona-routing`: "set up my persona" and "make you sound like me" load `persona_infer`. "set my persona to …" loads `persona_set`. News-style asks still load `news_voice`.

## How to get to it (user POV)

- In `om chat`, type "set up my persona". om shows a proposal and asks whether to save it.
- Answer yes. A card titled `approval needed` / `persona_set` appears. Press `y` to save, `n` to decline, or `d` for the full text.
- Afterwards, `om persona show` prints the saved text, plus the `MCP clients:` row.

## Driving it with control-om

**On a guest lane (since main `0d6993613`).** `pasted` needs no rooms identity, so a lane home plus a scripted fake model drives infer, the card and both answers. Have the fake call `tool_search {names:["persona_infer","persona_set"]}` first (the two load deferred), then `persona_infer {pasted:"<5 or more lines>"}` after the search result, and `persona_set {text}` on "yes". Launch with `--no-workspace` if the transcript must be read in scrollback. Expect `roomsRead: 0`.

**Room sampling.** A guest lane cannot sample rooms: that needs a rooms identity. Use a fresh source home that holds only the operator's device key, together with a scripted fake model. Never copy the vault: a copied home that refreshes an OAuth model login rotates the operator's real token.

- **Home.** Make a root with `active` set to the account name. In `accounts/<name>/`, copy only `credentials.json` and `device-id` (the device key is a non-rotating `apiKey`). Let om create the database. Seed it:
  - `om persona set "voice: clipped, wry"`;
  - `om config set mcp.operator_voice on` (optional, for the `MCP clients` row).
- **Launcher.**
  - Export `OM_HOME=<root>` and `OM_BIND=127.0.0.1:<dead agent port>`.
  - Export `OPENMARKET_LLM_PROVIDER=openai-compatible`, `OPENMARKET_LLM_BASE_URL=http://127.0.0.1:<fake port>/v1`, `OPENMARKET_LLM_MODEL=fake` and `OPENMARKET_LLM_KEY=fake`.
  - Run `bun packages/cli/src/bootstrap.ts chat`.
- **Fake model.** An OpenAI-compatible stream that decides from the request:
  - a request with no tools is the infer call (and title calls): answer with the persona text;
  - on "set up my persona", call `tool_search {query}` if `persona_infer` is not offered, otherwise call `persona_infer {}`, otherwise reply with the proposal;
  - on "yes", call `persona_set {text}`.

  Log each request's offered persona tools and the decision as JSONL. That log is the tool trail.
- **Drive.**
  - `tmux send-keys -l "set up my persona"`, then confirm the composer shows it before sending `Enter`. A key sent during boot is dropped.
  - Wait for the reply, then send "yes save it". Capture the card, press `d` and capture again, then `y`.
  - Run `om persona show` on the same home.
  - For the decline path, repeat and press `n`. The prompt asks "What should the agent do instead?"; Esc is a plain no. `om persona show` is unchanged.
- **Teardown.** Kill the tmux server and the fake model, then delete the home. It holds the operator's device key.

## Gotchas

- A copy of the real `om.sqlite` without its vault fails every model call with "The OpenAI-compatible credential could not be read for this call", even with the env override. Start from an empty home instead.
- A copied real home also resumes its last conversation and its away digest. The fresh home starts clean.
- The `[reply guidance]` lines and the raw JSON on screen come from the scripted fake echoing the tool result. They are not the product's reply.
