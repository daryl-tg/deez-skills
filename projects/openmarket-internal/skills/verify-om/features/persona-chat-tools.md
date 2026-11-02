# Persona setup from om chat

*Verified: 2026-11-02. Branch `daryl/persona-tools` at `cc7a755c5`, later rebased to `50c026306` (PR #2256, off origin/main; not on main yet).*

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

Ask `om chat` to set up your persona. om reads a sample of your own room messages and proposes a voice. Nothing is saved until you approve the exact text on a card. The card shows the new voice, the persona it replaces and the tool that manages it, and who uses it: om drafts, and MCP clients when `mcp.operator_voice` is on. The card appears even with auto-approve on. Neither tool is offered over MCP.

## Sub-features

- `persona-show`: reads the persona in force, whether it is stored, its managing tool, the card census and the MCP voice state (`on`, `off` or `on_no_persona`). It is the default of the `persona` routing family and is operator-only over MCP.
- `persona-infer`: reads your own messages and proposes a voice, with one model call. It returns `proposal`, `samples` and `roomsRead`, and saves nothing. Each failure is typed:
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

A guest lane cannot drive this: sampling needs a rooms identity, and chat needs a model. Use a fresh source home that holds only the operator's device key, together with a scripted fake model. Never copy the vault: a copied home that refreshes an OAuth model login rotates the operator's real token.

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
