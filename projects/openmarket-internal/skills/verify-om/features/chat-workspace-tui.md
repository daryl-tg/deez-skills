# Chat workspace TUI (`om chat --workspace`)

*Verified: 2026-10-29 (nightly), tree `32ca0d6c7` (origin/main, v0.467.0), lane on 18103 with a fake model on 18107, tmux at 140x36. Plain `om chat` on a fresh lane showed the What's new card (mode flags `1 0`); ctrl+x listed `w What's new: turn it on` and `x What's new: close this one` and no `b` row; `w` stored `chat.workspace = on` (`stored as tui.workspace`) and reopened the chat as a workspace (`1 1`). There: `▾ WATCHES 2 fired · 1 paused` on row 2, `▾ FIRES 3 today` and the `ctrl+x for commands` bottom row; ctrl+x listed only `b hide sidebar`; a click on `● ws-fired` (row 4) opened its card with its top on row 4; `om sidebar set watches paper` printed `Module 1: watches (show all)`, `Module 2: paper` and `Available: watches (show all|fired|attention), paper, fires`, and `▾ PAPER 2 accounts` appeared within 30 s; ctrl+x `b` left the rule reading `── ctrl+x for commands ─`; eight wheel-ups froze the stream at `reply 2 line 16` and the `Go to recent` pill jumped to `reply 2 line 40`; exit history held the `shell-history-*` lines and the transcript with no chrome; `om sidebar reset` restored `watches (show all)` then `fires`. Over MCP stdio `sidebar_layout` is not a tool (`Tool sidebar_layout not found`). Not re-driven: collapse, the 100-column resize, the live-row timing, the PAPER wheel containment, close-on-click, the near-bottom flip and a live model turn. Evidence: `http://127.0.0.1:8098/vom-nightly-20261029/r1/` (`tui-*.txt`).*

*Verified: 2026-10-28, on main since #2182 (`a521e2fc9`), #2187 (`705d67f2f`) and #2189 (`7cf1f4d40`).*

For #2189, on copies of a real home at 140x36:

- The foot hint read `ctrl+x for commands`, and ctrl+x opened a centered `ctrl+x commands` menu.
- `b` hid the sidebar, and a click on `show sidebar` brought it back. ctrl+x then `q` typed `q`, and a click outside closed the menu.
- With a card open, Esc closed the menu first.
- A card opened from row 3 had its top on row 3; one opened from row 26 flipped to end on row 26.
- A home with no stored layout showed `▾ FIRES` under WATCHES.

For #2187 (tree `96c6ef3bd`): the sidebar's first row was blank and `▾ WATCHES` sat on row 2; a click on a watch row opened its card, a click on the card and a drag across the chat left it open, and a click in the chat closed it. For #2182 (tree `4a1b3b1e3`): the frame fills the screen: no top bar, the divider starts on row 1, and a muted `ctrl+x b hide sidebar` is the sidebar's bottom row. `ctrl+x b` hid the sidebar, so the rule above the composer ended in `ctrl+x b show sidebar` and the footer regained `95 watches (22 armed)`. Pressing it again restored the sidebar, and `ctrl+x q` typed `q`. With `watches fires`, `▾ FIRES 28+ today` listed two-line rows, and a click opened the fire card (Watch, When, Source, Kind, summary). A click on `▾ WATCHES` folded it to `▸ WATCHES` and stored `collapsed true`. Those checks used a copy of a real home with its daemon port pointed at a dead port. Earlier, on 2026-10-27 (tree `4734c802a`, lane 18122 at 140x36, fake model), follow-at-end, the go-to-recent pill, the 100-column hide, exit history, the `1 1`/`0 0` mode flags, the WATCHES row and card, `om sidebar set` and the PAPER wheel containment were driven. A live `anthropic/claude-sonnet-5-5` turn, "only show fired watches in my sidebar", called `sidebar_layout {show: fired}` once, and the chat redrew at once.

`om chat --workspace` (or `om config set chat.workspace on`) opens chat as a
split view on the terminal's alternate screen: transcript left, a sidebar of
modules right (WATCHES then FIRES by default, PAPER optional), today's composer,
mode line and footer underneath. The person scrolls the transcript in the app,
clicks a watch for its card, and asks om or runs `om sidebar` to change what the
sidebar shows. Plain `om chat` keeps its layout, but advertises the workspace
through a **What's new** card that turns it on in one press.

## Sub-features

- `workspace-frame` — full screen (no top bar), a divider from row 1, one blank row above the sidebar's first panel, the closing `┴` rule, the sidebar hidden under 110 columns.
- `follow-and-go-to-recent` — follow at the end; scrolled up, the last row is a `↓ Go to recent messages` pill that a click resolves.
- `exit-history` — on quit the terminal history holds the transcript only.
- `watches-module` — `N fired · M paused` header, `●` fired in 24 h with an age, `○` armed, `◌` paused, a chip aside for needs-you/broken; the footer drops its watch count while the sidebar shows.
- `watch-card` — a click opens State, Source, Value, Chain, Recent fires beside the clicked row (its top level with the row, or ending on it near the bottom); Esc or a click in the chat closes it, while a click on the card or a drag across the chat leaves it open.
- `sidebar-layout` — `om sidebar` / `set <module...> [--watches-show all|fired|attention]` / `reset`; the agent tool `sidebar_layout` (terminal chat only).
- `paper-module` — one row per paper account (name, cash, realized P&L), `N accounts` header.
- `contain-scroll` — a wheel over a sidebar section, its header or the hint row never moves the transcript.
- `fires-module` — on by default under WATCHES: every watch's newest fires, two lines a fire (title and age, then the watch), `N today` header, a card per fire. A home with a stored layout keeps it; `om sidebar reset` takes the default.
- `collapse` — a click on `▾ NAME` folds a panel to `▸ NAME`, stored as `collapsed` in the layout.
- `command-menu` — ctrl+x opens a centered `ctrl+x commands` menu of the keys it takes next (`b` hides or shows the sidebar). A listed key, enter or a click runs a row; esc, ctrl+x or a click outside closes it; any other key closes it and types. It scrolls past 8 rows.
- `whats-new-card` — in plain `om chat` only (never in a workspace), a 49-column `What's new` card above the composer. It holds one entry per recent CHANGELOG item. Today's only entry is `Workspace: chat with a live sidebar`, with `[ Turn it on ]` and `ctrl+x for commands`. The button, a click on it, or ctrl+x `w` sets `chat.workspace on` and reopens the chat as a workspace. ✕ or ctrl+x `x` dismisses it (stored in `tui.whats_new.dismissed`). An entry shows only within 60 days of its date, only while its setting is not already applied, and only at 110 columns or wider.
- `sidebar-toggle` — `b` in the ctrl+x menu hides or shows the sidebar for the session. The muted `ctrl+x for commands` hint sits on the sidebar's bottom row, or on the closing rule while it is hidden.

## How to get to it (user POV)

- `om chat --workspace` in a terminal at least 110 columns wide, or
  `om config set chat.workspace on` and plain `om chat`.
- Plain `om chat` on a home that has not turned it on: the What's new card's
  `[ Turn it on ]`, or ctrl+x then `w`.
- `om sidebar set watches paper` (or `watches fires`) from any shell; the open chat redraws within 30 s.
- ctrl+x in the chat for the command menu, and a click on a panel header.
- In the chat: "only show fired watches in my sidebar".

## Driving it with control-om

Preconditions: a lane the run started, from the checkout under test; a private
tmux server; and a model, because `om chat` refuses to open without one (a
guest lane opens the setup walk instead). Use a local fake model: it costs
nothing, and it streams long replies, which the scroll checks need.

- **Fake model.** Use a second assigned agent port beside the lane's
  (preflight it with `lsof -nP -iTCP:<port> -sTCP:LISTEN`), save this as
  `server.ts` in a scratch directory, and run
  `FAKE_PORT=<fake-port> bun server.ts & echo $! > server.pid`. `FAKE_PORT` is
  required: the script refuses to guess a port.

  ```ts
  // Fake OpenAI-compatible /v1/chat/completions: streams a long numbered reply.
  const port = Number(process.env.FAKE_PORT);
  if (!Number.isInteger(port) || port <= 0) throw new Error("set FAKE_PORT to your assigned port");
  let turn = 0;
  const enc = new TextEncoder();
  Bun.serve({
    hostname: "127.0.0.1",
    port,
    async fetch(req) {
      const url = new URL(req.url);
      if (url.pathname.endsWith("/models")) return Response.json({ data: [{ id: "fake" }] });
      if (!url.pathname.endsWith("/chat/completions")) return new Response("nope", { status: 404 });
      const t = ++turn;
      const lines = Number(process.env.FAKE_LINES ?? "80");
      const delay = Number(process.env.FAKE_DELAY_MS ?? "400");
      const stream = new ReadableStream({
        async start(c) {
          const send = (o: unknown) => c.enqueue(enc.encode(`data: ${JSON.stringify(o)}\n\n`));
          const base = { id: `x${t}`, object: "chat.completion.chunk", created: 0, model: "fake" };
          for (let i = 1; i <= lines; i++) {
            send({ ...base, choices: [{ index: 0, delta: { content: `reply ${t} line ${i}: funding basis open interest skew\n\n` }, finish_reason: null }] });
            await Bun.sleep(delay);
          }
          send({ ...base, choices: [{ index: 0, delta: {}, finish_reason: "stop" }] });
          c.enqueue(enc.encode("data: [DONE]\n\n"));
          c.close();
        },
      });
      return new Response(stream, { headers: { "content-type": "text/event-stream" } });
    },
  });
  ```

  The turn counter is per server, not per chat: title and other side calls
  consume numbers, so `reply 3` may be the first reply on screen.
- **Seed watches** (from [event-ingest-and-fire.md](event-ingest-and-fire.md),
  same commands):
  - `control-om om -- watch create ws-fired --inbound --format json`, then
    `control-om om -- watch edit ws-fired --classifier-mode accept_all --format json`,
    then `control-om om -- event push ws-fired --text "<any unique string> probe" --kind filing --format json`
    (expect `accepted:true`, `delivery:"daemon"`).
  - `control-om om -- watch create ws-armed --inbound --format json`.
  - `control-om om -- watch create ws-paused --inbound --format json`, then
    `control-om om -- watch pause ws-paused --format json`.
- **Seed paper** (optional): `control-om om -- paper create lane-paper-a --cash 5000 -y`
  and `control-om om -- paper create lane-paper-b --cash 1000 -y`; read them back with
  `control-om om -- paper ls --format json` (the verb is `ls`).
- **Launcher.** Write `launch.sh`:

  ```bash
  #!/usr/bin/env bash
  cd <checkout>
  printf '$ shell line before launch\n'; for i in 1 2 3 4 5; do echo "shell-history-$i"; done
  export OPENMARKET_LLM_PROVIDER=openai-compatible OPENMARKET_LLM_BASE_URL=http://127.0.0.1:<fake-port>/v1 OPENMARKET_LLM_MODEL=fake
  OM_LANE_PORT=<lane-port> control-om om -- chat "$@"
  echo "EXITED-$?"; sleep 3600
  ```

- **What's new card (plain chat, fresh lane).** It needs a home with
  `chat.workspace` unset and no dismissals. Run `./launch.sh` with no flag and
  wait about 15 s. A `╭─ What's new ── ✕ ╮` box with
  `Workspace: chat with a live sidebar` and `[ Turn it on ]   ctrl+x for commands`
  sits above the composer. `display -p '#{mouse_any_flag} #{alternate_on}'`
  reads `1 0`: the card turns mouse reporting on. `C-x` opens a menu with
  `w          What's new: turn it on` and `x          What's new: close this one`,
  and no `b` row. Press `w`. The chat reopens on the alternate screen as a
  workspace (`1 1`), and `control-om om -- config get chat.workspace` reads
  `chat.workspace = on` / `source: config (stored as tui.workspace)`. Set it back
  with `control-om om -- config set chat.workspace off` before the plain-mode checks.
- **Start.** `tmux -L ws -f /dev/null new-session -d -s ws -x 140 -y 36 "./launch.sh --workspace"`,
  wait about 15 s. Capture with `tmux -L ws -f /dev/null capture-pane -t ws -p`
  (add `-e` for colour, `-S -` for history).
  - Frame: there is no top bar. Row 1 is transcript text with `│` at column
    104. The sidebar's first row is blank, and row 2 reads `▾ WATCHES` with
    `1 fired · 1 paused` on the right. Under the watch rows, `▾ FIRES`
    lists the seeded fire. The sidebar's last row (just above the `┴` rule)
    is a muted `ctrl+x for commands`.
  - Rows: `● ws-fired <age>`, `◌ ws-paused paused`.
  - The footer's last line has no `N watches` count but keeps the `⚠` badge.
  - The transcript opens with a `🗞 While you were away` banner naming the
    seeded fire, and the footer may carry `🗞 N new`. Both come from the
    seed push and are expected.
  - Launched within a minute of the seed push, `ws-fired` reads `now`.
- **Mouse.** Send SGR bytes as hex, with the escape written as bash ANSI-C
  quoting (`$'\e…'`); a literal `\e` inside plain quotes sends a backslash:

  ```bash
  raw() { tmux -L ws -f /dev/null send-keys -t ws -H $(printf '%s' "$1" | xxd -p -c1 | tr '\n' ' '); }
  raw $'\e[<64;40;15M'                        # one wheel-up over the transcript
  raw $'\e[<0;115;4M'; raw $'\e[<0;115;4m'    # click (press, release) on sidebar row 4
  ```

  - Wheel up: `\e[<64;<col>;<row>M`. Use column 40 for the transcript and 115
    to 120 for the sidebar.
  - Click: `\e[<0;<col>;<row>M`, then `\e[<0;<col>;<row>m`.
- **Follow and go-to-recent.** Type a message and press Enter. While it
  streams, send 8 wheel-ups at column 40 and capture twice, 2 s apart. The
  last `reply N line M` is the same in both, and `Go to recent messages` shows.
  Re-read the pill's row (`grep -n 'Go to recent'`), then click it. The pill is
  gone, and the newest line is on screen.
- **Live row.** First wait until `ws-fired` reads `1 min` (about 70 s after
  the seed push); otherwise the seed's own `now` hides the new one. Open
  `curl -sN --max-time 20 http://127.0.0.1:<lane-port>/events/v1 > events-<n>.sse &`
  (a fresh file per push; it exits after 20 s), push to `ws-fired` again, and
  capture at 1 s intervals. The row reads `now` within about 2 s, and the
  file carries `watch_fired`. Wait 70 s more: the row reads `1 min` with no
  further event.
- **Card.** Click the `● ws-fired` row at column 115, row 4 at 140x36
  (re-read it with `grep -n '● ws-fired'` if the layout differs). A bordered card shows
  the id once, `State fired just now`, `Source inbound · ws-fired`,
  `Value filing · new story`, `Chain no steps`, and `Recent fires` with
  `HH:MM filing · new story` rows. The row is inverse: `grep -cF $'\e[7m'` on the `-e` capture is at least 1.
  The card's top border (`╭` between columns 40 and 104) is on row 4, level
  with the clicked row. Press Escape: the card closes. The flip near the
  bottom needs more rows than the lane seeds; `tui-workspace-mode.test.ts`
  pins it at 140x28.
- **Click to close.** Reopen the card. Click a line inside it
  (`grep -n 'Recent fires'` for its row; the card sits over the chat): it
  stays open. Drag across the chat, which a click never reports:
  `raw $'\e[<0;5;3M'; raw $'\e[<32;12;3M'; raw $'\e[<0;12;3m'`; it stays open.
  Click the chat at column 5, row 2 (press, release): the card closes.
- **Layout from the shell.** Run
  `control-om om -- sidebar set watches --watches-show fired --format text`.
  It prints `Module 1: watches (show fired)` and an `Available: …` line.
  Within 30 s the running chat shows only `ws-fired`.
  `control-om om -- sidebar --format json` names `"show":"fired"`.
  `control-om om -- sidebar reset --format text` prints
  `Module 1: watches (show all)` and `Module 2: fires`, and restores both.
- **Two modules.** Run `control-om om -- sidebar set watches paper` and
  restart the chat. WATCHES sits above `PAPER  2 accounts`, with the rows
  `○ lane-paper-a $5,000.00`. Send 10 wheel-ups at the PAPER row: the
  transcript columns (1-103) and WATCHES are unchanged. The control is the
  same wheel at column 40, which moves the transcript and shows the pill.
- **Fires.** On by default (the lane home stores no layout). Under WATCHES,
  `▾ FIRES  N today` lists the seeded fires newest first,
  two lines each: the title and its age, then the watch's name. Click the
  first line of a fire for its card (Watch, When, Source, Kind, and the
  summary when there is one); Escape closes it.
- **Collapse.** Click the `▾ WATCHES` row (`grep -n '▾ WATCHES'`). It turns
  into `▸ WATCHES`, its rows go, and the panel below takes the space.
  `control-om om -- sidebar --format text` prints `watches (show all,
  collapsed true)`. Click it again to open it.
- **Menu.** `tmux … send-keys -t ws C-x`: a centered box titled
  `ctrl+x commands` with `esc close` on its title row, the row
  `b          hide sidebar` (inverse, selected) and `↑↓ move · enter run`.
  Escape closes it with nothing run. A click outside it closes it too.
- **Toggle.** `C-x` then `b`: no `│`, no `WATCHES`, and the rule above the
  composer ends in `── ctrl+x for commands ─`. The footer's last line has
  its `N watches` count back. `C-x` again shows `show sidebar`; click that
  row (`grep -n 'show sidebar'` for its row and column) and the sidebar
  returns. `C-x` then `q` closes the menu and puts `q` in the composer.
- **Narrow.** `tmux … resize-window -t ws -x 100 -y 36`: no `│` divider, no
  `┴`, and no `ctrl+x for commands` hint; ctrl+x goes to the composer there.
  Resize back to 140 and they return.
- **Exit.** Press `C-c` twice. In `capture-pane -p -S -`, history holds the
  `shell-history-*` lines and the whole transcript (`reply N line 80`). It
  holds no `Go to recent`, `┴`, `ctrl+x for commands` or `om running` rows.
- **Mode flags.** `tmux … display -p -t ws '#{mouse_any_flag} #{alternate_on}'`
  reads `1 1` in workspace mode. Plain `./launch.sh` reads `0 0` only once the
  What's new card is gone (dismissed, applied or out of date); with the card up it
  reads `1 0`.
- **Cleanup.** Press `C-c` twice in the chat, run
  `tmux -L ws -f /dev/null kill-server`, `kill $(cat server.pid)`, then
  `OM_LANE_PORT=<lane-port> control-om down`. Confirm both ports have stopped
  listening.

## Gotchas

- The footer drops its `N watches` count in favour of attention chips while
  any watch is broken or needs you (`⚠ 1 broken · 2 need you · /watches`).
  The chips read the same with the sidebar shown or hidden. So on a lane with
  a `broken` `ws-armed` (see below), hiding the sidebar cannot prove the count
  returns. Driven 2026-10-29.
- The footer may also carry `data limit hit N ago · om usage` after a guest
  market read was refused by the plan within the hour. It is a recorded
  refusal, not a live limit (`om usage` showed 600 of 600 remaining).
- Dismissing the card with ctrl+x `x` writes `tui.whats_new.dismissed`, which
  is a raw settings row: `om config get` refuses that key. Use a fresh lane
  home to see the card again.

- The footer reads `no LLM connected · /setup` with the fake model. The model
  comes only from environment variables, which the footer's stored-config
  read never sees. This is expected.
- The same split makes `ws-armed` differ between surfaces. The daemon has no
  model, so it marks `ws-armed` `broken`, and the footer says so. The chat
  process sees the environment model, so the sidebar lists `○ ws-armed`.
  This is a rig artifact. With a stored credential, both read the same home.
- Below 110 columns the footer's own width fitting drops the watch count in
  both modes, so a narrow workspace cannot prove the count comes back.
  `tui-workspace-mode.test.ts` pins that instead.
- Layout changes from another process land on the chat's 30 s clock tick. A
  `sidebar_layout` tool result in the same chat redraws at once.
- The pill's row moves when the chrome changes height (a queued message
  draining), so re-read its row right before clicking.
- Driving a copy of a real home instead of a lane: point `OM_HOME` at a root
  that holds `active` and `accounts/<name>/`, never at the account folder.
  Given an account folder, om moves it into `accounts/` and plain chat opens
  the setup walk. Copy `om.sqlite` with `sqlite3 -cmd ".timeout 15000" … ".backup …"`
  and check that the copy has a `settings` table. The live daemon holds the
  lock, and a failed backup leaves an empty file that reads as a fresh install.
- The first capture after a push can predate the fire by about 1 s, because
  the daemon commits the event about a second after `event push` returns.
- `curl` on the stream must open before the push; it is live, not a backlog.
