# Self-hosted model servers in OM Settings

*Verified: 2026-11-18 and 2026-11-19, NOT on main yet. MR !294, branch `daryl/own-model-settings`, head `432ed297`. The daemon half is PR #2605 in openmarket-internal, also not on main. Driven on `/rooms/` through the dev pair (daemon 18152, vite 18154) against llama-server on 9931, a fake LocalAI on 8080, a judge proxy on 18153, a prose-only fake on 18155 and a vLLM-shaped 32k fake on 18157. Rounds r1 to r4 ran at their own GUI commits; r5 ran at `cd5c7c93`, before a rebase with no change to these files. Driven: the Self-hosted servers section with Running and Not running rows, Connect making llama.cpp active, connection rows with `Use` and `Active`, `Current model` naming the server, the `Review model` row saving the self-hosted judge after a real check (also through a judge that took 30 s: `Applying` at 32 s, saved at 45 s), the warning under the row when the judge server is down, the `Another server` form with the 32k server's window and fix rows, and focus moving to `Server address` on Add and back to Add on Cancel. Galleries `http://127.0.0.1:8098/own-model/r1/` to `r5/`. Not driven: real Ollama, LM Studio or vLLM servers, the `Copy` button's clipboard write, and the WiringCard's link into this section. The daemon side is [self-hosted-models.md](../../../../openmarket-internal/skills/verify-om/features/self-hosted-models.md) in the om map.*

OM Settings lists the self-hosted model servers on this machine by name and says which are running. A running server connects with one click and becomes the chat model. Stored connections switch with `Use`. The review model is picked beside the chat model.

## Sub-features

- **Self-hosted servers.** A section headed `Self-hosted servers` under the model section, one row per server. A running row reads `Running · 1 model` and its base URL (`http://127.0.0.1:9931/v1`) with `Connect`. A stopped row reads `Not running` and `Start: ollama serve` with `Copy`, which copies the start command and reads `Copied` for a moment. Ollama, LM Studio, llama.cpp and vLLM are always listed. Another kind, such as LocalAI, appears only when running. The connected server's row shows `Active` in place of `Connect`.
- **Another server.** The last row reads `Another server` and `Any OpenAI-compatible address: a LAN box or a rented GPU` with `Add`. Add opens a form with `Server address`, an optional `API key` and the probed model list (`Self-hosted model`, or a `Model id` field). A refused key reads `Key refused`. An address that does not answer reads `Nothing answered at <url>`.
- **Window refusal.** A server whose window is too small for chat shows `Window: vLLM serves 32,768 tokens, om needs 96k`, `Fix: restart vLLM with --max-model-len 98304` and `Chat: stays on <current chat model>` as an alert, and the form stays open.
- **Connection switching.** Each stored connection is a row. A server row reads its model, then `127.0.0.1:9931 · 96k window`. A subscription or key row reads `anthropic · API key`. The active row shows `Active`. The others show `Use`, named `Use <model> on <host>` for assistive tech.
- **Current model.** The row names the server by label, as in `llama.cpp · unsloth/Qwen3-4B-Instruct-2507-GGUF:Q4_K_M`, or `Anthropic · claude-opus-5-5` on a subscription.
- **Review model.** One row under `Model catalog`, built the same way. A `Review model` select lists the daemon's choices (`auto`, `same-as-chat`, each catalog model and each self-hosted model), then `Apply`. The `auto` option reads `auto (anthropic/claude-haiku-5-5 · fast, same sign-in)` on a Claude home. A choice that follows another model shows `Now: anthropic/claude-haiku-5-5`. Apply sends `model/set {role: "review", choice}`, which runs the daemon's real judge check before it saves. A refusal shows inline. A daemon without `reviewModel` shows no row.
- **WiringCard link.** With no assistant configured, the Built-in assistant row reads `Off · chat replies and briefs need it` and carries a button to the Self-hosted servers section. Source only.

## How to get to it (user POV)

1. Open Settings and pick **OM Settings** under Agents.
2. Scroll past **Model** to **Self-hosted servers**.
3. Press **Connect** on a running server, or **Copy** to copy a stopped one's start command.
4. Pick a self-hosted model in **Review model** and press **Apply** to review items on it while chat stays on a subscription.

## Driving it with control-om-chat

The plain fixture cannot prove this. The section reads the daemon's `model/probe`, `model/connections`, `model/get` and `model/set` routes. Open the shell fixture through the dev daemon instead, so the fixture's RPC calls reach the real daemon. The rig (llama-server, judge proxy, scratch home) is in the om map's [self-hosted-models.md](../../../../openmarket-internal/skills/verify-om/features/self-hosted-models.md).

```bash
# in the openmarket-internal worktree
OM_DEV_HOME=<scratch home> OM_DEV_BIND=127.0.0.1:18152 OM_DEV_CHAT_PORT=18154 \
OM_DEV_CHAT_REPO=<openmarket-chat worktree> bun scripts/dev.ts

agent-browser open 'http://127.0.0.1:18152/rooms/tools/visual/shell-fixture.html?view=settings&settingsPage=om&alerts=quiet'
```

- Never set `OM_DEV_LOOPBACK_AUTH` on the pair. It makes every RPC call from the GUI answer 401.
- Stop `bootstrap.internal.ts run` as well as the dev script when tearing the pair down.
- Pick a `MenuSelect` option by clicking the combobox (`Model` or `Review model`), then clicking the option's ref from a fresh snapshot.
- Handles: buttons `Connect <label> at <host>`, `Copy the start command for <label>`, `Add another server`, `Use <model> on <host>`, `Apply review model`. Fields `Server address`, `API key`, `Self-hosted model`, `Model id`. Data attributes `data-om-self-hosted-server="<kind>"`, `data-om-current-model`, `data-om-review-model`, `data-om-review-model-error`.

### What to check

- With llama-server on 9931 and a LocalAI fake on 8080, the section lists both as running, then Ollama, LM Studio and vLLM as not running with their start commands (`gui-self-hosted.png`).
- Connect on llama.cpp. `Current model` reads `llama.cpp · <model>`, the connection row reads `127.0.0.1:9931 · 96k window` with `Active`, and the server row shows `Active` (`gui-self-hosted-connected.png`).
- On a home with chat on Claude and the judge proxy stored, `Review model` first reads `auto` with `Now: anthropic/claude-haiku-5-5` (`gui-review-model-before.png`). Pick `openai-compatible/qwen-judge` and Apply. The proxy logs one judge call (about 50 s on the mini), and the row reads the self-hosted pick while `Current model` stays `Anthropic · claude-opus-5-5` (`gui-review-model.png`).
- With two stored servers, `Use` on the inactive one moves `Active` and `Current model` to it (`gui-switched.png`, r1 layout).

## Gotchas

- The page opened straight from vite (18154) has no daemon behind its RPC calls. Open it through the daemon's port.
- `gui-off-state.png`, `gui-detected.png`, `gui-window-refused.png`, `gui-connected.png`, `gui-switched.png` and `gui-form-polished.png` are r1 captures with the retired `Your own model` card. The switching rows and window rows in them still exist. The card does not.
- `gui-role-choice.png` and `gui-reviews-row.png` are r3's connect-form role questions and `Reviews items` row. r4 removed both in favor of the `Review model` row.
- A 32k server cannot become the chat model. `Use` on it is refused by the daemon's window floor by design, and the rows say why.
- The judge check on Apply takes about 50 s with a 4B model on the shared mini. The button reads `Applying` until it answers.
- Only `/rooms/` was driven. The cloud `/chat/` host has no model settings by design, since model calls run on the daemon.
