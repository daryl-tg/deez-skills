# Self-hosted model servers: Ollama, LM Studio, llama.cpp, vLLM and others

*On main since 2026-11-20 as a beta: PR #2605 squash-merged as `1f6823782e`. #2640 (the server's own token count) merged the same day.*

*Verified: 2026-11-20, merged main `2d01b6b5d4` (#2605, #2640), lane on 18121 through `control-om` (public entry), every OpenMarket origin dead, fake servers on 18122 to 18129. No real model call. Driven, 12 of 12 claims: `model/probe` naming a server by its route and not its port, the machine scan naming a llama.cpp fake on Ollama's port 11434, the window rows in `model/connect` and `om init`, the server's own token count and its guards, the stored rate read by setup, doctor, `model/set` and the turn, seven stored servers routed by model id, a chat turn, the first-turn refusal on a fresh home, the review pick's one judge call and the prose refusal, the `hold` default across two outages, and the beta labels. One defect outside the claims: `om init` crashes when the key is skipped for a typed address (Gotchas). Not driven: `/model` in the TUI, a dashboard frame (the worktree has the stub bundle), real servers of any kind. Evidence root `~/Documents/dev-notes/om-2026-11-20-e2e-verify/run-artifacts/s1/` (`out/`, `pty/`, `fakes/`, `lead/`). Gallery `http://127.0.0.1:8098/om-1120-e2e/s1/`.*

*Driven on main 2026-11-20 (`07c285b9e3`) against a real LAN GPU box: llama.cpp b12532 serving Qwen3.6-35B-A3B (2× RTX 3060), reached through an SSH tunnel on an agent port, so om saw it as loopback and the hint read `this machine`. `model/probe` named it `llamacpp` with a served window of 32,768 and 2 slots; connect refused chat with `Fix: restart llama-server with --ctx-size 196608`; the review pick's real check passed in 4 s with thinking off; a batch of 6 items (3 on topic, 3 off) kept the 3 at confidence 1.00 within 5 s; under the default `hold`, an outage (tunnel closed) posted the held notice, recovery reviewed the held item about 4 minutes later, and a second outage posted a second notice; a first `chat --once` turn answered with the window and fix rows. Evidence in `run-artifacts/verify/box-*.txt`. Never stop a shared server for an outage drive: close your own tunnel.*

*Verified: 2026-11-18 to 2026-11-20 on branch `daryl/own-model-connections` (final head `53e9fbf414`). r6 drove the beta labels and the hold default (`init-beta-r6.txt`, `review-model-r6.txt`). Rounds r1 to r4 ran at their own commits (r1 `364ad74817`, r2 `0d837abc30`, r3 `352cf2e0ef`, r4 `8815c31910`); r5 ran at `ebfbbc0279`, the review fixes, before a changelog-only rebase. Driven from source with a scratch `OM_HOME`: `model/probe {}` against llama-server on 9931 and a fake LocalAI on 8080; `om init` named rows and the not-running path in an `expect` pty; the window rows; status and doctor with the server up and down; `model/connect`, `connections` and `set`; a chat turn routed by model id; usage rows; the review model through `model/get`, `model/set {role:"review"}` and `om setup review-model` with a real judge check. r5 added: the first-turn overflow reply at the final numbers (fresh home, vLLM-shaped 32k fake on 18157), `model/set {role:"review"}` refusing a prose-only server with `judge_model_unusable` and saving nothing, and under `hold` an outage notice, recovery reviewing the held item, and a second outage posting a second notice. Galleries `http://127.0.0.1:8098/own-model/r1/` to `r6/`. Not driven: real Ollama, LM Studio or vLLM servers, the per-server gate ordering, the subject-resolve lane, and the final fallback target (the sign-in's review model; it needs a working hosted sign-in). The GUI half is [self-hosted-model-settings.md](../../../../openmarket-chat/skills/verify-om-chat/features/self-hosted-model-settings.md) in the OM Chat map.*

om connects to any OpenAI-compatible server a person runs. Setup lists the known servers by name and says which are running. om reads the window the server really serves and says in one row what to change when chat does not fit. Several servers can be stored at once, and a model id picks its server. A self-hosted model can be the review model while chat stays on a subscription.

## Sub-features

- **Detection.** `POST /rpc/v1/model/probe` with `{}` lists this machine's servers by name. A running server reads `{kind, label, status: "running", baseUrl, modelCount}`. A stopped one reads `{kind, label, status: "not_running", start}`. Ollama, LM Studio, llama.cpp and vLLM are always listed. Other kinds appear only when running (LocalAI was seen live). Detection checks identity only, by each server's own fingerprint request, never by port: a llama.cpp server on Ollama's port 11434 reads `llamacpp`, and Ollama stays `not_running` (driven 2026-11-20). Each request is bounded near 300 ms and a pass near 1 s. llama.cpp is probed on its default port 9931 and on 8080. The start commands read `ollama serve`, `lms server start` and `vllm serve <model>`.
- **Probe one address.** `model/probe {baseUrl}` answers `{servers: [{baseUrl, probe}]}`. An `ok` probe names `server` (`llamacpp`, `vllm` and so on), each model with its `contextWindow`, and `slots` when the server reports them. llama.cpp's window comes from `/props`.
- **`om init` named rows.** The first question lists each server after the hosted rows. Running servers sort first. `Another server` comes last. The words `Your own model` are gone. A running server goes straight to `Found 1 model.` and `Model:`. Then setup prints `LLM auth saved: 127.0.0.1:9931 (<model>)`, `Skipped: web search needs a hosted model (connect one with om init)` and `Checked: llama.cpp answered`. Only the first self-hosted row carries the beta label, as in `not running · start: ollama serve · beta`.
- **Another server.** The last row asks `Server address`, then `API key (Enter to skip)`. A typed key goes on to `Found 1 model.` Enter at the key prompt crashes (Gotchas).
- **Not running.** Picking a stopped server shows `Ollama: not running` and `Start: ollama serve`, then asks `Started it?` with `Check again` and `Back`.
- **Window rows.** A served window below om's chat floor prints three rows and still saves. `model/connect` returns the same as `window: {status: "too_small", window, needed, cause, fix}`.
  - A counted llama.cpp or vLLM server reads `Window: llama.cpp serves 32,768 tokens, om needs 80k` and `needed: 81920` (#2640). llama.cpp's fix multiplies by its slots: `Fix: restart llama-server with --ctx-size 163840` on 2 slots.
  - Ollama, LM Studio, a failed count and the env path keep the 96k estimate: `om needs 96k`, `set OLLAMA_CONTEXT_LENGTH=98304`, `Context Length 98304`, `--max-model-len 98304`.
  - A server with no window route reads `window: unknown`.
  - The third row reads `Chat: needs the larger window, watches can use this model`. With chat already on another server it reads `Chat: stays on <model>`, and `active` stays there.
- **The server's own count (#2640).** om measures its chat prompt on the server instead of estimating.
  - llama.cpp: `POST /apply-template` (2 messages, 18 tools), then `POST /tokenize` on the rendered prompt.
  - vLLM: one `POST /tokenize` in the chat form, with `messages` and `tools`.
  - The rate is stored per model as `chat_chars_per_token` in the stored endpoint (3.88 on the fakes). About 3.9 gives 80k, so a 65,536 window reads `fits`.
  - A rate outside 1.5 to 8 is rejected: nothing is stored and the decision is back at 96k.
  - A redirect on the count route is refused. The redirect target sees no request.
  - A failed `/apply-template` falls back to the raw text times 1.05.
  - Ollama and LM Studio get no count call and store no rate.
  - Setup, doctor, `model/set` and the turn's floor read the stored rate. With no rate stored, the first `om doctor` and the first refused turn each measure once. The second run of each makes no count call.
- **Overflow reply.** A first chat turn that overflows the server's window answers with `Window:` and `Fix:` rows instead of offering `/clear`. On a stored 32k llama.cpp endpoint it exits 1 and the turn request is never sent.
- **Env path.** `OPENMARKET_LLM_BASE_URL` with no `OPENMARKET_LLM_PROVIDER` resolves to `openai-compatible`. Doctor names the profile `env:OPENMARKET_LLM_BASE_URL`.
- **Status.** `om status` reads `LLM: ✓ <model> on 127.0.0.1:18150 · web search unsupported on this lane`. A stored endpoint adds its window, as in `· 128k window`.
- **Doctor.** The `model` row reads `llama.cpp answers at http://127.0.0.1:18150/v1`. With the server down it reads `nothing answered at <url>`, hinting `Start the model server, or connect another model with om init.` The `window` row warns `llama.cpp serves 32,768 tokens, om needs 80k` on a counted server, or `om needs 96k` with `--ctx-size 98304` where no count exists.
- **Connect, list and switch.** `model/connect {baseUrl, apiKey?, model}` stores the server and returns its connection, the window decision and notes. A sent key never comes back in any response. `model/connections` lists every stored connection, subscriptions and servers alike, with `active` on one. `model/set {connection}` moves chat to it. Ids read `openai-compatible:127.0.0.1-18153-v1`.
- **Routing by model.** `model/set {provider: "openai-compatible", model}` sends chat to the stored server whose model list holds that id, not to the first server stored.
- **Usage.** `usage_llm` counts tokens per self-hosted model with `cost_usd` 0 and the rounds counted as `unpriced_rounds`. The text view lists one row per self-hosted model with cost `self-hosted`, and no host or server kind.
- **The review model is a standard role.** It is set only where role models are set. That means `om setup review-model`, the `/setup` panel row, `model/get` (`reviewModel: {choice, resolved, choices}`) and `model/set {role: "review", choice}`. Connecting a server asks no role question. The choices are `auto` (follows the chat sign-in), `same-as-chat`, each catalog model, and each self-hosted model with the hint `self-hosted · beta · this machine`, or `self-hosted · beta · <host>` for a server elsewhere. `om setup review-model` with no argument prints the pick, also in a pty. The picker that shows the hint is the review model row of the chat `/setup` panel.
- **A real judge check.** Saving a self-hosted review model sends exactly one review call with the judge prompt and verdict schema, from `om setup review-model <pick>` and from `model/set {role: "review"}` alike. A model that answers prose is refused `judge_model_unusable` (HTTP 400, CLI exit 2) and the earlier pick stays.
- **When the review server is down.** `agent.review_when_down` takes `hold` (the default: unset reads `default: hold`) or `chat`. Any other value is refused with `must be one of: chat, hold.` With `hold`, items stay `pending`, one notice per outage reads `Review: <server> not answering; items wait until it is back`, and held items are reviewed on recovery. A second outage posts a second notice with a new id. With `chat`, a batch is reviewed once on the chat sign-in's review model and one notice reads `Review: <server> not answering, reviewing on <model> meanwhile`.
- **Background caps.** A background round to a self-hosted server sends an output cap and `chat_template_kwargs: {enable_thinking: false}`. The cap is the lane's own bound, else 1,024 tokens. One gate per server, sized by its slots, runs a queued chat round ahead of background rounds.
- **Desktop onboarding.** The desktop app-setup list does not offer `openai-compatible` (`5a8577bb0c`). OM Settings covers it.

## How to get to it (user POV)

1. Start a server, such as `llama-server` or `ollama serve`.
2. Run `om init`, pick the server by name and pick a model.
3. Read `om status` and `om doctor` for the server and its window.
4. Run `om setup review-model` to review items on the server while chat stays on a subscription.

## Driving it with control-om

The branch passes ran from the feature worktree's source with a scratch `OM_HOME`, not through `control-om`. The 2026-11-20 pass on main ran on a `control-om` lane with fakes (see "Fakes on agent ports"). CLI verbs ran as `bun packages/cli/src/bootstrap.ts <verb>`. Routes ran as `curl -s -X POST -H 'content-type: application/json' -d '<body>' http://127.0.0.1:<lane>/rpc/v1/model/<verb>` against a source daemon or the dev pair on an agent port. Chat and auth pointed at a dead address (`http://127.0.0.1:9`).

### The real server

```bash
llama-server -hf unsloth/Qwen3-4B-Instruct-2507-GGUF:Q4_K_M --host 127.0.0.1 \
  --ctx-size 98304 -ctk q4_0 -ctv q4_0 -fa on -np 1 -n 512
```

- With no `--port` it listens on 9931, llama.cpp's default, which detection probes. Preflight 9931 first and stop the server afterwards.
- `--ctx-size 98304` fits om's chat floor. Restart it with `--ctx-size 32768 --port 18150` to drive the window rows and doctor's `window` warning.
- `-n 512` caps each reply. Without it the 4B model ran on for 4,073 tokens.
- A fake on 8080 that answers LocalAI's fingerprint proves a kind that is not always listed. A fake on 8000 shaped like vLLM drives the vLLM window rows.

### Fakes on agent ports

The 2026-11-20 pass used no real server. Its scripts are in the evidence root.

- `fakes/fake-server.ts --port <p> --kind llamacpp|vllm|ollama|lmstudio|generic --models <ids> --ctx <n> [--slots] [--rate] [--chat answer|overflow|prose|judge]`. It logs every route it answers.
- A `--mode <file>` JSON flips a running fake: `rate`, `tokenize` (`ok`, `404`, `redirect`), `template` (`ok`, `500`), `chat`, `verdict`.
- `env.sh` holds the lane env (every origin at `http://127.0.0.1:9`) and the helpers `fake`, `unfake`, `rpc <verb> '<json>'` and `since <port>` (the fake's new log lines).
- The lane's `up` arguments are `out/lane-up-args.txt`. They add `OM_FEED_ALLOW_LOOPBACK=1` and `OM_FEED_POLL_INTERVAL_MS=60000`.
- Identity routes are tried in ladder order, so a fake must answer 404 to the earlier ones.
- A fake's `/tokenize` sets the measured rate.
- A judge fake must copy `item_id` and `echo` from the prompt into `{"items": […]}`.
- `feed/add-item.sh` adds an item to the stand-in RSS feed, which one fake also serves.
- `fakes/read-store.ts` prints the stored endpoints with their `chat_chars_per_token`.
- Agent ports drive everything except the machine scan, through `model/probe {baseUrl}`, `model/connect` and `Another server`. The scan needs one fake on a default port such as 11434 (`fakes/fake-server-11434.ts`). Preflight it, hold it for a minute, and stop it.
- `pty/*.exp` drive `om init` and the chat `/setup` review picker. `pty/nav.tcl` holds the shared `shown` and `highlight` steps.

### The judge proxy

Run a Bun server on another agent port (18153 here). It forwards every request to llama-server and answers under a different model id (`qwen-judge`). Store it as its own connection and pick it as the review model. Killing the proxy alone takes the review server down while llama-server keeps serving chat. Have it log `model`, `max_tokens`, `chat_template_kwargs` and the prompt length. The judge check logged `max=5334 kwargs={"enable_thinking":false} chars=12558`.

### Items to judge

Serve a local RSS feed from a Bun server on an agent port (18156 here) and create a watch whose source is that feed. The daemon refuses a loopback feed unless the dev pair sets `OM_DEV_FEED_ALLOW_LOOPBACK=1`. Add an item to the feed to make the watch judge it.

### A home with chat on Claude and a stored server

A scratch script imports from the worktree and calls `ensureSealReady()`, then `connectOwnModel({baseUrl, model})`, then `executeWizardChoice({kind: "anthropic-paste", apiKey: "sk-ant-api03-dummy"}, {}, {activate: true})`. Chat then reads Anthropic on a dummy key, which none of these drives dials.

### The dev pair (daemon plus GUI)

```bash
OM_DEV_HOME=<scratch home> OM_DEV_BIND=127.0.0.1:18152 OM_DEV_CHAT_PORT=18154 \
OM_DEV_CHAT_REPO=<openmarket-chat worktree> OM_DEV_FEED_ALLOW_LOOPBACK=1 \
  bun scripts/dev.ts
```

- Never set `OM_DEV_LOOPBACK_AUTH`. It makes every GUI RPC call answer 401.
- The banner reads `bind http://127.0.0.1:18152` and `gui <worktree> (vite :18154)`.
- Stop `bootstrap.internal.ts run` too when stopping the pair. It outlives the dev script.

### `om init` in a pty

Drive it with `expect`. Put `set stty_init "rows 45 cols 120"` before `spawn`, because an unsized pty hides the re-renders. Send one Enter per menu. A script one Enter short looked like a hang at `Model:` and was not a product bug.

### What to check

- `model/probe {}` lists llama.cpp `running` on 9931 and LocalAI on 8080. Ollama, LM Studio and vLLM read `not_running` with their start commands.
- `model/connect` with an `apiKey` returns no key.
- After `model/set {connection}` to another server, `om chat --once` lands there. After `model/set {provider, model}` with the llama model id, it lands on llama-server.
- `model/get` reads `auto -> anthropic/claude-haiku-5-5` on a Claude home. After `model/set {role: "review", choice: "openai-compatible/qwen-judge"}` it reads the self-hosted pick, and the proxy logs one judge call.
- Under the default `hold`, kill the judge server and add a feed item. It waits as `pending` and one notice posts. Restart the server and the held item is judged. Budget five minutes: held items were reviewed 36 s after one recovery and 221 s after another.
- Run `om config set agent.review_when_down chat`, kill the judge server and add an item. The lane log shows four `llm_transient` retries, then `llama.cpp is not answering; reviewing once on ...`, and one `review_server_down` notice (driven on r3 code only).

### The whats-new file after a rebase

Regenerate with `bun --preload ./scripts/test-plugins.ts packages/cli/scripts/gen-whats-new.ts`. Without the preload the regeneration failed, and the first rebase attempt committed conflict markers.

## Gotchas

- **Defect: `om init` crashes when the API key is skipped for a typed server address.**
  - Repro: fresh home, any OpenAI-compatible server at a non-default address. `om init --accept-risk --no-launch`, pick `Another server`, type the address, press Enter at `API key (Enter to skip)`. Script `pty/init-skip-key.exp` with `ADDR=<address>`.
  - Seen: `om: undefined is not an object (evaluating 'rawKey.trim')`, exit status 2. Nothing saved. No request reached the server. Reproduced by the verifier twice and by the lead.
  - Expected: setup goes on with no key and lists the models.
  - Cause: `packages/cli/src/cmd/openai-compatible-prompt.ts:124` calls `rawKey.trim()`. `prompts.password` at line 166 returns `undefined` for an empty Enter on `@clack/prompts` 1.4.0. Before #2605 the line read `(rawKey ?? "").trim()`.
  - It is in #2605's own squash commit `1f6823782e`. A typed key works, and so does `model/connect`. A server detected on a default port passes an empty string and does not crash.
  - Evidence `pty/init-skip-key-crash-run1.txt`, `pty/init-skip-key-crash-run2.txt`, `out/02b-clack-empty-password.txt`, `lead/lead-redrive.md`.
- **Known, not verified-good:** `model/set {provider, model}` on a too-small self-hosted window answers the hosted sentence (`om needs at least 71,825 input tokens … set agent.context_window_override`). `model/set {connection}` on the same server answers the `Window:` and `Fix:` rows. Evidence `out/06-stored-rate-readers-lane.txt`.
- On the env path (`OPENMARKET_LLM_BASE_URL`, nothing stored) the first-turn refusal probes and counts twice, then prints 96k. No stored endpoint exists to hold the rate. Evidence `out/09-first-turn-too-small.txt`.
- A chat fake that answers the summary lane in plain text opens a `summary_error` episode and posts `⚠️ <watch> is broken` in the middle of a hold drive. Its fix line points at the review model while the failing call ran on the chat model.
- `control-om om -- chat` under `expect` can leave an orphan `bun … chat` if the script ends before the TUI quits. Find it by its `OM_HOME` and kill it by pid.
- `om init` offers `A login I already have (Claude Code signed in on this machine)` as its first row. Never select it in a drive.
- A worktree with dashboard stubs has no dashboard frame. Render the captured text for the gallery.
- A 4B model on the shared mini took about 4.5 minutes to prefill om's chat prompt, about 36k tokens on Qwen's tokenizer. `chat --once` took 4m50s. Budget for it, or drive chat against a fake.
- The save-time judge check takes about 50 s on the mini.
- `overflow-named.txt` (r1) reads `om needs 80k` and `--ctx-size 81920`, which predates the rounding fix. `overflow-r5.txt` is the estimate's reply at 96k and 98304. Since #2640 a counted llama.cpp or vLLM server reads 80k again, from the measured rate. The named rows show only on a conversation's first turn: a home whose earlier `chat --once` succeeded gets the generic `/clear` line, so drive it on a fresh home.
- With a local server down, doctor's `llm` row still blames `a network or VPN change`. The `model` row names the real cause.
- The live fallback ran on r3 code, where the fallback was the chat model. Final code falls back to the chat sign-in's review model (Haiku on a Claude sign-in); that target is unit-tested only. The final hold notice is driven (`hold-r5.txt`, `hold-r5b.txt`).
- The unusable refusal is driven on the final `model/set {role: "review"}` path against a prose-only fake on 18155 (`review-model-r5.txt`).
- `role-offer.txt` and `role-status.txt` show r3's connect-time role question. r4 removed it, so they are not the current surface.
- The per-server gate (slots, chat first) has no live drive. The gate is in-process, and no daemon chat turn ran beside a judge call.
- Subject resolve through a self-hosted model is unit-tested only.
- Ollama's, LM Studio's and vLLM's window routes come from their documented APIs and are pinned by fixtures. No real server of those kinds ran.
- Ports 9931, 8080 and 8000 sit outside the agent range because detection probes them. Preflight each and stop only what you started.
