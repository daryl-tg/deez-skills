# The first run: `om init`, the model step and chat with no AI

*Verified: 2026-11-11, branch `daryl/first-run-fixes` tree `8d3d0a84f2` (PR #2451, on origin/main `0ad4768f66`), from source in tmux with a scratch `OM_HOME`, a fake `HOME` and a stub `security` command, lane on 18181 and a stub model endpoint on 18182. Gallery `http://127.0.0.1:8098/first-run-fixes/r2/` (9 screenshots). Not on main until the PR merges.*

The model step of `om init` asks how the assistant will reach an AI before it lists providers, a pasted key is checked on the spot, and `om chat` opens signed out when no AI is set up.

## Sub-features

- The first question has four answers: `A login I already have`, `An API key`, `My own endpoint`, `Not now`. Its default is the login answer when a local login is detected and the key answer otherwise.
- The second screen lists only that answer's rows. No default row opens a browser or starts a device sign-in. Esc returns to the first question.
- A pasted key or endpoint is checked once, within 6 seconds: `Checked: <provider> answered`, or `<provider> rejected that key` with try again, keep and skip.
- The default walk does not ask for the Jev or Firecrawl keys. `om init --full` does.
- `om chat` with no AI opens the workspace with `No AI connected · market reads and watches work now · /setup connects one`. A typed message gets the same line.
- A home that finished setup once (`init.completed=1`) opens chat with no prompt. A cancelled walk does not open chat. A pipe exits 2.
- The closing card names the clock time a rate-limited guest sign-in can be retried.
- A new price watch on a guest key records no "broken" fault when its live stream drops. `om watch show` still says the stream is degraded.
- `om watch create --once` on a rule that already holds replies `true now: fires once, now`.

## How to get to it (user POV)

1. `om init` on a new home.
2. Answer the AI question, then pick a row and paste a key.
3. `om chat`.

## Driving it with control-om

- Interactive verbs run in tmux on your own named socket, with a scratch `OM_HOME`, a fake `HOME`, `OM_NO_AGENT_WIRING=1` and a stub `security` command first on PATH. Without the stub the vault step stalls for a minute or more on a fake home.
- Before every Enter on a picker screen, capture the pane and confirm the highlighted row. A blind key sequence opened a real sign-in page twice during the first measurement.
- Never choose a row that opens a browser or starts a device sign-in. Drive the key and endpoint paths against a local stub that answers `/v1/models` and can be switched to answer 401.
- Claude Code login detection reads the macOS keychain, which a scratch `HOME` does not isolate. A failing `security` stub keeps the default on `An API key`.
- A `Import your setup from Grok Bot?` prompt appears on this machine because the app is installed. Scripts must answer it.
- The guest key mint is rate limited per address, and every lane on the machine shares it. Plan for one mint per run, and use `om event push` and local reads for what needs no key.
- The "broken" notice case needs a guest key on a lane: create one price watch, then read the lane log for the 1006 close and "parked" lines, the `watch_runtime` row, and the notice history.

### What to check

- The prompt count from pane transcripts, before and after.
- No model request reaches the stub when a message is typed with no AI.
- A second `om chat` on a finished home shows no prompt.
- The quick start's first watch has exactly one fire in history after three minutes.

## Gotchas

- A real provider's key check has not been driven. The stub proves the flow.
- The hint that names a detected local login is unit-tested only.
- `init-transcript.test.ts` times out on this machine at the Grok Bot import prompt, on main as well.
- The README's install address returned 404 on 2026-11-10 and 2026-11-11, so the compiled install script was read and not run.
- A watch whose author chose the fast lane and that places no order gets no fault on a dropped stream.
