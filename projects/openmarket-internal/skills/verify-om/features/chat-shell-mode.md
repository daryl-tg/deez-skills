# Chat shell mode (`!` in `om chat`)

*On main since #2362 (squash `a4e42d7bd`, 2026-11-05). The proofs below ran on its branch tree before the merge; not yet re-driven on main.*

*Re-verified 2026-11-05 (r2) after the operator asked for magenta: the shell tone is the new `shell` token `#d16fc4` (SGR `38;2;209;111;196`), 2 sequences on the empty shell composer, 3 on a shell row's bar, 0 teal anywhere. Evidence: `http://127.0.0.1:8098/vom-bang-shell/r2/`.*

*Verified: 2026-11-05, branch `daryl/bang-shell-composer` (uncommitted tree on `a0a8c7b8b`), bare lane 18121 (dummy `OM_API_KEY`, dead service URLs), fake openai-compatible model 18122, tmux 140x40, default workspace. Driven: `enter`, `run`, `agent-reads`, `consumed-once`, `recall`, `stop`. Not driven live: the queue while a turn runs (unit-tested), rooms and DMs sending `!` as text, the plain `--no-workspace` layout, a 1 MiB output. Evidence: `http://127.0.0.1:8098/vom-bang-shell/r1/` (`tui/*.txt`, `tui/fake-model-requests.log`).*

A line starting with `!` in the agent composer runs in the user's shell, prints inline, and rides the user's next message to the model. Source: `packages/cli/src/agent/channels/tui-shell-run.ts` and the `composerMode` machine in `cli-tui-core.ts`.

## Sub-features

- `enter` — `!` on an empty composer moves into the prompt (`!` instead of `❯`); rules and text turn the `shell` magenta `#d16fc4` (SGR `38;2;209;111;196`; r1 was `verify` teal). Backspace on an empty composer leaves. Any wholesale text replacement (↑, ctrl+r, draft restore) sets the mode from the new text.
- `run` — the echoed row has a magenta `┃` (a message's is clay `217;119;87`) and keeps its `!`; output in the code tone, last 40 lines, then a faint `exit N · 1.2s`. `$SHELL -c`, stdin empty, 120 s timeout. stdout prints before stderr, not interleaved.
- `agent-reads` — no model call on the run. The next message's user row carries `The user ran these commands…` with each command, its exit and up to 8,000 chars of output tail (16,000 across runs).
- `consumed-once` — the message after that carries none.
- `recall` — ↑ brings `!` entries back in shell mode, chat entries back under `❯`.
- `stop` — status row `Running <cmd> · Ns · esc to stop`; esc kills the process group and prints `stopped after Ns`.

## How to get to it (user POV)

`om chat`, type `!`, then a command, Enter. Ask the agent about it in the next message.

## Driving it with control-om

1. Bare lane: `control-om up --port 18121` with `--env OM_API_KEY=om_dummy_proto`, every service URL at `http://127.0.0.1:9`, and `OPENMARKET_LLM_PROVIDER=openai-compatible`, `OPENMARKET_LLM_BASE_URL=http://127.0.0.1:18122/v1`, `OPENMARKET_LLM_MODEL=fake`. Export `OM_LANE_PORT=18121`.
2. Fake model: a `Bun.serve` that logs the last user message and replies naming any `VOM_BANG_*` markers it saw, else `No shell output reached me this turn.`
3. `tmux -L vombang new-session -d -s p -x 140 -y 40`, then `send-keys` a script that exports the same LLM env plus `COLORTERM=truecolor` and runs `control-om om -- chat`.
4. Runs with unique markers: `!echo VOM_BANG_X`, then a plain message; assert the reply names the marker and the next one does not.
5. Capture `capture-pane -p -e` and `-p`; count `38;2;209;111;196` in idle vs shell frames.

## Gotchas

- `control-om om --` runs from the repo root, so a `!` command's cwd is the checkout, not the folder tmux started in.
- A worktree-isolated Claude session refuses `tmux` launching a script; leave isolation (keep the tree) to drive it.
- `bun test` runs with colour off, so unit tests assert the `!` glyph; the teal is only provable in a live capture.
- Kill with `tmux -L vombang kill-server`; never a bare `tmux kill-server`.
