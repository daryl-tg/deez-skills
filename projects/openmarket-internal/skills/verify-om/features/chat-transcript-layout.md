# Chat transcript layout (`om chat`)

*Verified: 2026-10-30, branch `daryl/tui-readability` at `af153e835` (before its rebase onto origin/main `3cb50a821`), lane 18113, fake model 18114, tmux at 140x40 and 71x40. Driven: `turn`, `tool-row`, `approval-card`, `fire-band`, `away-band`, `catchup-band`, `replay`, `spinner` (plain and workspace), `narrow`. Not driven live: the notice strips (unit-tested), the chimes (unit-tested; one real Tink played during a red check), the OSC 11 reply from a real terminal (tmux answers it). Evidence: Artifact gallery `https://claude.ai/artifact/3jtQoAsFm8DcfxUH2BSekd`, frames under the worktree's `artifacts/vom-tui-readability/r1/`.*

*Re-verified for #2219: 2026-10-30, branch `daryl/watch-status-dots` (off origin/main `cbe10ee19`), lane 18113, fake model 18114, tmux at 160x36 then 90x30. A long reply wrapped at column 119 of a 124-column workspace pane and rewrapped at 90; the user panel ran to the divider; footer codes read `36` mode and model, `31` badge, `32` om running, `90` separators. Evidence: `http://127.0.0.1:8098/vom-dots/r2/`.*

What the transcript looks like, in plain and workspace mode. The workspace
frame itself (sidebar, cards, ctrl+x) is `chat-workspace-tui.md`.

## Sub-features

- `turn` — your message is a clay `┃` bar on a raised tint, one padded row above and below. om's reply has no label, starts at column 5 and wraps at the pane's width less a 2-column margin (the 100-column cap was removed in #2219). No `▣ om` footer and no `Worked for` row.
- `tool-row` — one row per call, arguments truncated first; the result hangs on its own `→` row.
- `hanging-wrap` — every wrapped row hangs under its own text, never back at column 0.
- `code-block` — a muted tint, no fences, no bar.
- `approval-card` — the irreversible tone is down (`#e08072`); a decline leaves a `✗ declined` step row.
- `fire-band` — a watch or alert fire is a warm tinted band with a bold clay `om` mark. No left bar: a solid left bar belongs to your message only.
- `away-band` / `catchup-band` — "While you were away" and `/catchup` use the same band; stories in aligned columns, age right-aligned. At 71 columns the title cuts with `…`.
- `notice-strip` — jobs, spend, follows, relay, stand-downs, the beta countdown and update notices sit on a faint strip with a toned label.
- `replay` — `om chat --resume` replays the conversation exactly as it looked live, under a faint `resuming from N prior turns · M earlier messages not shown` marker.
- `spinner` — only while om works, directly above the composer; idle has no status row. In `--workspace` it is the transcript pane's last row, left of the divider.
- `chimes` — macOS local: Tink when an approval card opens, Glass when a turn over 3 s ends; SSH and other systems ring BEL. `om config set chat.sounds off` silences all of it.
- `palette` — clay accent `#d97757`, muted `#8b9198`, up, down, warn; tints blend over the terminal's real background (OSC 11, first frame held up to 100 ms). `OM_TUI_ACCENT` overrides the accent. The footer, mode line and watch attention badge are the exception (#2219): the terminal's own cyan, green, red, yellow and gray, with `OM_TUI_ACCENT` replacing the cyan.

## How to get to it (user POV)

`om chat`, ask something that calls a tool, then read the screen. `om chat --resume` for the replay.

## Driving it with control-om

A guest lane has no model, so drive it with a fake OpenAI-compatible server.

1. `control-om up --port 18113`, then every call as `OM_LANE_PORT=18113 control-om om -- …`.
2. Fake model on `18114`: a `Bun.serve` on `127.0.0.1` that answers `/v1/models` with `{data:[{id:"fake"}]}` and streams `/v1/chat/completions` as SSE. When the last message is not a tool result, it streams one `tool_calls` delta for a tool present in `body.tools` (`watch_list` for "watches", `watch_remove` for "remove", which raises the irreversible card); after a tool result it streams a markdown reply with a list and a fenced block.
3. Launch in tmux on a private server: `tmux -L vomtui -f /dev/null new -d -s p -x 140 -y 40 ./launch.sh`, where `launch.sh` exports `COLORTERM=truecolor`, `OPENMARKET_LLM_PROVIDER=openai-compatible`, `OPENMARKET_LLM_BASE_URL=http://127.0.0.1:18114/v1`, `OPENMARKET_LLM_MODEL=fake` and runs `OM_LANE_PORT=18113 control-om om -- chat "$@"`.
4. Fires: create a `--inbound` watch, `watch edit --classifier-mode accept_all`, then `event push` while the chat is open.
5. Capture: `capture-pane -p -e` for ANSI and `-p` for text. Convert the ANSI to HTML (a ~50-line script mapping SGR 38/48;2 and 38/48;5 to spans on a `#282c33` page) and screenshot it with `agent-browser`. Assert on the `.txt`; the PNG is for the reviewer.

## Gotchas

- `control-om down` takes `OM_LANE_PORT`, never `--port`.
- tmux answers OSC 11 with its own background, so the tint blend shown is tmux's, not a real terminal's.
- Dismissing the What's new card leaves blank rows under the footer in plain mode (pre-existing flow-mode shrink).
- Kill the tmux server with `tmux -L vomtui kill-server`; never a bare `tmux kill-server`.
