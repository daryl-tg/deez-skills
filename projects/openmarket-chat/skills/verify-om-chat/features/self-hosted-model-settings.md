# Self-hosted model servers in OM Settings

*On main since 2026-11-20 as a beta: MR !294 merged as `d0086d12`. Re-driven on main (`84e88e56`) on 2026-11-21 against a scripted daemon: the page, its rows, the connect form and its refusals are proved there; the daemon's own answers are not. See the fixture recipe and the verification record below.*

*Verified: 2026-11-18 to 2026-11-20 on branch `daryl/own-model-settings` (final head `f4415024`). r6 drove the `Beta` chip beside `SELF-HOSTED SERVERS` and the `self-hosted · beta · this machine` review hint. The daemon half is PR #2605 in openmarket-internal, also not on main. Driven on `/rooms/` through the dev pair (daemon 18152, vite 18154) against llama-server on 9931, a fake LocalAI on 8080, a judge proxy on 18153, a prose-only fake on 18155 and a vLLM-shaped 32k fake on 18157. Rounds r1 to r4 ran at their own GUI commits; r5 ran at `cd5c7c93`, before a rebase with no change to these files. Driven: the Self-hosted servers section with Running and Not running rows, Connect making llama.cpp active, connection rows with `Use` and `Active`, `Current model` naming the server, the `Review model` row saving the self-hosted judge after a real check (also through a judge that took 30 s: `Applying` at 32 s, saved at 45 s), the warning under the row when the judge server is down, the `Another server` form with the 32k server's window and fix rows, and focus moving to `Server address` on Add and back to Add on Cancel. Galleries `http://127.0.0.1:8098/own-model/r1/` to `r6/`. Not driven: real Ollama, LM Studio or vLLM servers, the `Copy` button's clipboard write, and the WiringCard's link into this section. The daemon side is [self-hosted-models.md](../../../../openmarket-internal/skills/verify-om/features/self-hosted-models.md) in the om map.*

OM Settings lists the self-hosted model servers on this machine by name and says which are running. A running server connects from a short form and becomes the chat model. Stored connections switch with `Use`. The review model is picked beside the chat model.

## Sub-features

- **Self-hosted servers.** A section headed `Self-hosted servers` with a `Beta` chip under the model section, one row per server (`packages/chat-ui/src/components/OmModelConnections.tsx:394-416`). It reads `Looking for servers` while the probe runs. A running row reads `Running · 1 model` and its base URL (`http://127.0.0.1:9931/v1`) with `Connect`. A stopped row reads `Not running` and `Start: ollama serve` with `Copy`, which copies the start command and reads `Copied` for a moment. Ollama, LM Studio, llama.cpp and vLLM are always listed. Another kind, such as LocalAI, appears only when running. The connected server's row shows `Active` in place of `Connect`.
- **Connect is a form, not one click.** `Connect` on a running row opens the form with `Server address` filled, probes that address at once, and lists its models in `Self-hosted model` (the first is picked, as `qwen3-4b` with `96k window`). The form's own `Connect` then makes it the chat model, closes the form and moves focus to the new connection row.
- **Another server.** The last row reads `Another server` and `Any OpenAI-compatible address: a LAN box or a rented GPU` with `Add`. Add opens the same form empty, with `Server address`, an optional `API key`, `Cancel` and `Check`. `Check` probes the address; once it answers, the model list appears (`Self-hosted model`, or a `Model id` field with "No model list at <url>") and the button reads `Connect`. A refused key reads `Key refused`. An address that does not answer reads `Nothing answered at <url>`.
- **Window refusal.** A server whose window is too small for chat shows `Window: vLLM serves 32,768 tokens, om needs 96k`, `Fix: restart vLLM with --max-model-len 98304` and `Chat: stays on <current chat model>` as an alert, and the form stays open.
- **Connection switching.** Each stored connection is a row. A server row reads its model, then `127.0.0.1:9931 · 96k window`. A subscription or key row reads `anthropic · API key`. The active row shows `Active`. The others show `Use`, named `Use <model> on <host>` for assistive tech.
- **Current model.** The row names the server by label, as in `llama.cpp · unsloth/Qwen3-4B-Instruct-2507-GGUF:Q4_K_M`, or `Anthropic · claude-opus-5-5` on a subscription.
- **Review model.** One row under `Model catalog`, built the same way. A `Review model` select lists the daemon's choices (`auto`, `same-as-chat`, each catalog model and each self-hosted model), then `Apply`. The `auto` option reads `auto (anthropic/claude-haiku-5-5 · fast, same sign-in)` on a Claude home. A choice that follows another model shows `Now: anthropic/claude-haiku-5-5`. Apply sends `model/set {role: "review", choice}`, which runs the daemon's real judge check before it saves. A refusal shows inline. A daemon without `reviewModel` shows no row.
- **No model connected.** When the daemon refuses `model/get` with `agent_not_configured`, the Model section reads `No model connected` (`[data-om-model-none]`, `OmSettingsSurface.tsx:677`) in place of the current-model and catalog rows, and the Self-hosted servers section still lists its rows.
- **A daemon without these routes.** When `model/connections` answers 404 the Self-hosted servers section is not drawn at all, and the Model section reads "This daemon predates these settings. Update om to manage them here." (`[data-om-settings-degraded]`).
- **WiringCard link.** With no assistant configured, the Built-in assistant row reads `Off · chat replies and briefs need it` and carries a `Self-hosted` button (named "Self-hosted servers in OM Settings", `[data-om-self-hosted-link]`) to the Self-hosted servers section. It shows only when the OM page exists and `model/connections` answered (`settings/WiringCard.tsx:285-304`). Source only.

## How to get to it (user POV)

1. Open Settings and pick **OM Settings** under Agents.
2. Scroll past **Model** to **Self-hosted servers**.
3. Press **Connect** on a running server, check the model in the form and press its **Connect**. Or press **Copy** to copy a stopped one's start command.
4. Pick a self-hosted model in **Review model** and press **Apply** to review items on it while chat stays on a subscription.

## Driving it with control-om-chat

The section reads the daemon's `model/probe`, `model/connections`, `model/get`, `model/connect` and `model/set` routes (`POST /rpc/v1/model/<verb>`, `lib/om-model-rpc.ts:318-387`). There are two ways to answer them. The dev daemon proves the real thing. A scripted daemon on the fixture lane proves the page (see "On the fixture lane" below). For the dev daemon, open the shell fixture through it, so the fixture's RPC calls reach the real daemon. The rig (llama-server, judge proxy, scratch home) is in the om map's [self-hosted-models.md](../../../../openmarket-internal/skills/verify-om/features/self-hosted-models.md).

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

### On the fixture lane, with a scripted daemon (added 2026-11-21)

The page calls a module adapter, so the `Object.prototype` seam cannot reach
it, and the fixture assigns `window.fetch` itself. Wrap that assignment with a
getter/setter, as the Sealed Messages stub does
([settings-and-appearance.md](settings-and-appearance.md)). `?modelSeed=claude`
starts on a subscription and `?modelSeed=none` with no model. The script keeps
state, so a connect or a `Use` shows on the next read.

```bash
cat > "$SCRATCH/fixture-model-stub.js" <<'JS'
(() => {
  const seed = new URLSearchParams(location.search).get("modelSeed");
  if (!seed) return;
  const choices = [
    { value: "auto", label: "auto", hint: "anthropic/claude-haiku-5-5 · fast, same sign-in" },
    { value: "same-as-chat", label: "same-as-chat" },
    { value: "openai-compatible/qwen-judge", label: "openai-compatible/qwen-judge" },
  ];
  let review = { choice: "auto", resolved: "anthropic/claude-haiku-5-5", choices };
  let connections = seed === "none" ? []
    : [{ id: "sub", provider: "anthropic", kind: "subscription", label: "Claude subscription", active: true }];
  const active = () => connections.find((c) => c.active);
  const routes = {
    get: () => {
      const a = active();
      if (!a) return { refuse: "agent_not_configured" };
      const own = a.kind === "endpoint";
      const model = own ? a.model : "claude-opus-5-5";
      return { provider: a.provider, label: own ? "llama.cpp" : "Anthropic", model,
        catalog: [{ id: model, name: model, current: true }], envOverride: null, reviewModel: review };
    },
    connections: () => ({ connections }),
    probe: (b) => {
      if (!b.baseUrl) return { servers: [
        { kind: "llamacpp", label: "llama.cpp", status: "running", baseUrl: "http://127.0.0.1:9931/v1", modelCount: 1 },
        { kind: "ollama", label: "Ollama", status: "not_running", start: "ollama serve" },
      ] };
      const probe = /:9931/.test(b.baseUrl) ? { status: "ok", server: "llama.cpp", models: [{ id: "qwen3-4b", contextWindow: 98304 }] }
        : /:8000/.test(b.baseUrl) ? { status: "ok", server: "vLLM", models: [{ id: "qwen-32k", contextWindow: 32768 }] }
        : /:7777/.test(b.baseUrl) ? { status: "unauthorized" } : { status: "unreachable" };
      return { servers: [{ baseUrl: b.baseUrl, probe }] };
    },
    connect: (b) => {
      const host = b.baseUrl.replace(/^https?:\/\//, "").replace(/\/.*$/, "");
      const row = { id: "c1", provider: "openai-compatible", kind: "endpoint", label: "llama.cpp", active: true, model: b.model, host, contextWindow: 98304 };
      if (/:8000/.test(b.baseUrl)) return { connection: { ...row, id: "c2", label: "vLLM", active: false, contextWindow: 32768 },
        window: { status: "too_small", window: 32768, needed: 98304, cause: "vLLM serves 32,768 tokens, om needs 96k", fix: "restart vLLM with --max-model-len 98304" },
        notes: ["Chat: stays on anthropic/claude-opus-5-5"] };
      connections = connections.filter((c) => c.id !== "c1").map((c) => ({ ...c, active: false })).concat(row);
      return { connection: row, window: { status: "fits", window: 98304 }, notes: [] };
    },
    set: (b) => {
      if (b.role === "review") { review = { choice: b.choice, resolved: null, choices }; return { reviewModel: review }; }
      connections = connections.map((c) => ({ ...c, active: c.id === b.connection }));
      const a = active();
      return { provider: a.provider, model: a.model || "claude-opus-5-5", unknownModel: false, envOverride: null };
    },
  };
  const calls = (window.__modelCalls = []);
  const wrap = (f) => (i, o) => {
    const m = String(typeof i === "string" ? i : (i && (i.url || i.href)) || "").match(/\/rpc\/v1\/model\/([a-z]+)/);
    if (!m || !routes[m[1]]) return f(i, o);
    const body = JSON.parse((o && o.body) || "{}");
    calls.push(m[1] + " " + JSON.stringify(body));
    const data = routes[m[1]](body);
    return Promise.resolve(new Response(JSON.stringify(data.refuse ? { ok: false, error: data.refuse, message: "No model is configured." } : { ok: true, data }),
      { status: 200, headers: { "content-type": "application/json" } }));
  };
  let inner = window.fetch.bind(window);
  Object.defineProperty(window, "fetch", { configurable: true, get: () => wrap(inner), set: (v) => { inner = v; } });
})();
JS
cat "$SCRATCH/fixture-people-stub.js" "$SCRATCH/fixture-model-stub.js" > "$SCRATCH/init-model.js"
agent-browser --init-script "$SCRATCH/init-model.js" open about:blank
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=settings&settingsPage=om&alerts=quiet&modelSeed=claude')"
agent-browser find role button click --name "Connect llama.cpp at 127.0.0.1:9931"   # form: address filled, model qwen3-4b, button Connect
agent-browser click '[data-om-self-hosted-submit]'
#   [data-om-current-model] "llama.cpp · qwen3-4b"
#   [data-om-connection] rows "Claude subscription | anthropic | Use" and "qwen3-4b | 127.0.0.1:9931 · 96k window | Active"
#   the llama.cpp server row ends "Active"; focus is on the new connection row
agent-browser find role button click --name "Use Claude subscription"               # back to "Anthropic · claude-opus-5-5"
```

Driven 2026-11-21 at `84e88e56` on `/rooms/`, with a longer stub that also
listed LM Studio and vLLM as stopped:

- **Another server.** `Add another server` opens the empty form with focus on
  `Server address` and the button `Check`. `http://127.0.0.1:9999/v1` reads
  `Nothing answered at http://127.0.0.1:9999/v1` and `:7777` reads `Key
  refused`, each as an alert with the form still open.
- **Window refusal.** `:8000` lists `qwen-32k` and the button turns to
  `Connect`; pressing it shows one alert with `Window: vLLM serves 32,768
  tokens, om needs 96k`, `Fix: restart vLLM with --max-model-len 98304` and
  `Chat: stays on anthropic/claude-opus-5-5`. The form stays open, and
  `Cancel` returns focus to `Add another server`.
- **Review model.** The row read `Review model | Now:
  anthropic/claude-haiku-5-5 | auto | Apply`. The select lists the daemon's
  choices with their hints. Picking `openai-compatible/qwen-judge` and `Apply`
  sent `model/set {"role":"review","choice":"openai-compatible/qwen-judge"}`
  and `Current model` stayed on the subscription.
- **`modelSeed=none`.** The Model section reads `No model connected` and the
  server rows still offer `Connect`.
- **No stub.** The four daemon-backed sections each read "This daemon predates
  these settings. Update om to manage them here." and there is no Self-hosted
  servers section.

The stub proves what the page does with an answer. It does not prove the
daemon's probe, its window floor, the judge check behind `Apply`, or which
servers a real machine lists.

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
- The cloud `/chat/` host has no model settings by design, since model calls run on the daemon. Its **OM Settings** page still mounts, makes no `model/*` call, and shows the "predates these settings" notice in each section, with no Self-hosted servers section. On the `/chat/` fixture the page throws "session.refreshApprovalMode(...).then is not a function" until the session-capture shim assigns `__om.refreshApprovalMode = async () => null`, and `settingsPage=om` does not select the page there: open `?view=settings` and press **OM Settings** (2026-11-21).
- A scripted daemon keeps its state in the page. A reload starts again from the seed.

### Verification record

**Last verified:** 2026-11-26 (nightly maintenance). **Product commit:** `0f3fd22c` (GitLab origin/main; rooms-client 0.125.0; 7 commits past `557ee9ed`). **Scope:** the scripted re-drive of this guide's recipes by the kept step runner (`/rooms/` 18186, `/chat/` 18187 where the guide covers it, openscape 18188 for the world), motion blocks one session at a time; two read-only judges compared every result with its expectation and each flagged block was re-run alone. This guide's source did not change in the delta. **Limitations:** the last-call readback catches the re-read `get`, not the `set` (step fault). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261126/r1/`.

**Previous record:** 2026-11-25 (nightly maintenance). **Product commit:** `557ee9ed` (GitLab origin/main; rooms-client 0.125.0; 11 commits past `9c697d6e`). **Scope:** the scripted re-drive of this guide's recipes by the kept step runner (`/rooms/` 18186, `/chat/` 18187 where the guide covers it, openscape 18188 for the world), motion blocks one session at a time; every failing step was re-run alone and compared with this guide. This guide's source did not change in the delta. **Limitations:** **Apply review model** was not re-proved (carried). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261125/r1/`.

**Previous record:** 2026-11-24 (nightly maintenance). **Product commit:** `9c697d6e` (GitLab origin/main; rooms-client 0.125.0; 22 commits past `4b6f42b4`). **Scope:** the scripted core-path re-drive of this guide's recipes (`/rooms/` 18186, `/chat/` 18187 where the guide covers it, openscape 18188 for the world); every failed or disagreeing step was re-run alone. This guide's source did not change in the delta. **Limitations:** **Apply review model** recorded no `set` call tonight; the rest of the block matched. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261124/r1/`.

**Previous record:** 2026-11-22 (nightly maintenance). **Product commit:** `4b6f42b4` (GitLab origin/main; rooms-client 0.124.0; one commit past `84e88e56`). **Scope:** `/rooms/` (18186) against the scripted model daemon: the section, the connect form with its probed address, **Connect** → `llama.cpp · qwen3-4b` and two connection rows, **Use Claude subscription**, the window refusal for a second server, **Review model** → `openai-compatible/qwen-judge` → **Apply review model** (`set {"role":"review",…}`), and **No model connected** with `modelSeed=none`. **Limitations:** a real daemon and real servers were not driven; `/chat/` was not re-driven tonight. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261122/r1/`.

**Previous record:** 2026-11-21 (nightly maintenance). **Product commit:** `84e88e56` (GitLab origin/main; rooms-client 0.124.0; the feature merged as `d0086d12`). **Scope:** `/rooms/` (18193), `shell-fixture.html?view=settings&settingsPage=om` with the people stub and a scripted `model/*` daemon: the Self-hosted servers section with its `Beta` chip, running and stopped rows and `Another server`; the connect form (probe, model pick, `Connect`), the `Active` connection row, `Current model` and focus; `Use` back to the subscription; `Nothing answered at`, `Key refused` and the window refusal; the `Review model` row and its `Apply` call; `No model connected`; the page with no stub. `/chat/` (18194): the degraded page through the shim. **Limitations:** every daemon answer was scripted, so the real probe, window floor, judge check and server list rest on the 2026-11-18 to 2026-11-20 branch run above. `Copy`, the `Model id` field, a refused `Use` and the WiringCard button were not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261121/r1/` (frames 10-14, 25).
