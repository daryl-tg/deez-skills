# Your installed agents from the CLI and om chat

*Verified: 2026-11-04 (nightly), tree `9acb5fb56` (origin/main, v0.491.0; #2282, #2297), guest lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), booted in 2 s with no 429; `INFO [roster] om-skills defaults installed 8 package(s)` at boot. Fake model on 18164 for `om chat`, private tmux server at 140x40. Driven: `agent list` (text and JSON), `agent show explain`, `agent show nosuch` exit 1, `agent configure explain --paused on|off` (receipt and the `paused` state on `list`), `agent configure --brain` exit 1 `unknown option`, `agent ps` (empty, then a failed watch-door run, then the run's detail by full id), `agent cancel run_nope` and `agent cancel <failed run>` exit 1, `agent remote status`; over MCP stdio `agent_list`, `agent_runs`, `agent_run {agent:"zzz"}` `not_found`, `agent_configure {set:{kind}}` `plugin_owned`; in `om chat` the ctrl+x menu row `a agents`, the RUNS and AGENTS tabs, `p` then `y` pausing `explain` (read back as `paused` by `om agent list`) and unpausing it, the `explain` and `librarian` pages (ABOUT, REACH), `/agents a b` usage, `@nope hi`, and the `Draw librarian? y/n` prompt (declined). Not driven: a portrait draw, motion, the AGENTS sidebar module, `agent remote enable|disable`, `agent configure` through the approval card, `--revision`, a cancel of a running run (see [roster-task-pool.md](roster-task-pool.md)). Evidence: `http://127.0.0.1:8098/vom-nightly-20261104/r1/` (`cli/40-53`, `cli/69-74`, `cli/220-225`, `cli/110-mcp.json`, `tui/04-13`).*

`om agent` lists the agents installed on this home, shows one agent's fields and reach, changes the fields a plugin lets you change (model, description, when to use, paused, shadow), and lists or cancels agent runs. In `om chat` the same agents sit in a bottom overlay (ctrl+x `a`) with RUNS and AGENTS tabs, and `/agents <name>` opens one agent's page. A guest home gets six default agents from the registry a few seconds after boot.

## Sub-features

- `list`: `om agent list` prints one row per agent, `name  brain/model  state  N today  vX` (`explain     om/inherits  idle  0 today  v1.0.0`); `--format json` is `{items:[{id,name,origin,version,brain,model,toolCount,portrait,owner,avatar,paused,shadow,machine,live,turnsToday}]}`. A guest lane lists `argue`, `debugger`, `explain`, `fact-check`, `feature`, `librarian`.
- `show`: `om agent show <name>` prints `── About`, `── Reach`, `── Settings`, `── Schedules` with a source after each field (`(plugin)` or `(locked)`); an unknown name exits 1 `No agent named <name> is installed.` with `Run \`om agent list\` for the installed agents.`
- `configure`: `om agent configure <name>` takes `--model <id|inherit>`, `--description`, `--when-to-use a,b`, `--paused on|off`, `--shadow on|off`; text receipt `Paused   on` / `Applies  next run`, JSON `{revision,applied,appliesTo:"next run",agent,set}`. There is no CLI flag for tools, brain or kind; the action refuses those fields `plugin_owned:<field>` and a plugin-locked field `locked:<field>`.
- `ps-cancel`: `om agent ps` heads `Agents: 4 at once · R running · Q queued`; a row is `run_<8>  <agent>  <door>  <state>  <age>  <room>  <ask head>`. `om agent ps <full run id>` prints `Run:`, `Agent:`, `Door:`, `State:`, `Started:`, `Room:`, `Ask:`, `Result:`, `Proposals:`, `Events:`. The short id on a row is not accepted. `om agent cancel` refuses an unknown run `Run was not found.` and an ended one `Run already <state>.` (both exit 1).
- `overlay`: ctrl+x `a` opens `agents` at the foot of the screen. RUNS (`c cancel  o open  tab agents  esc`) and AGENTS (icon, brain/model, state, runs today, version; `enter open  p pause  s shadow  m draw  / filter  tab runs  esc`). `p` asks `Save 1 field? y/n` and answers `saved, applies to the next run`. `m` asks `Draw <agent>? y/n` with `Cost  one model run each`.
- `agent-page`: `/agents <name>` (or `enter` on a row) opens tabs ABOUT, REACH, SETTINGS, SCHEDULES, RUNS; ABOUT reads `Portrait  not drawn, m to draw`, the plugin fields, `Trigger rate  not measured` and `Digest`; REACH reads `Tools`, `Vault`, `Requires` and `Widen  update the plugin`. `/agents a b` prints `Usage: /agents (your agents) · /agents <name> (that agent's page) · /agents draw (draw every agent without a portrait)`.
- `at-door`: `@<name> <ask>` in the composer hands the ask to that agent; an unknown name answers `No agent named nope. Installed agents are argue, debugger, explain, fact-check, feature, librarian`.
- `mcp`: `agent_list`, `agent_runs`, `agent_run`, `agent_run_cancel`, `agent_configure` and `agent_portrait` are listed over MCP stdio; `agent_run` with an unknown agent is `not_found` `No agent named zzz.` with the hint `Installed: argue, debugger, ...`.
- `motion` (source only): `chat.motion on|off` (stored as `tui.motion`, `OM_TUI_MOTION` outranks it) stills the portrait and the status line's breath; a bad value is refused `chat.motion must be on or off.`

## How to get to it (user POV)

- Terminal: `om agent list`, `om agent show <name>`, `om agent configure <name> --paused on`, `om agent ps`.
- In `om chat`: press ctrl+x then `a`, or type `/agents` or `/agents <name>`; type `@<name> <ask>` to hand an ask to one agent.

## Driving it with control-om

Preconditions: a lane the run started, `OM_LANE_PORT` exported, and the lane log's `om-skills defaults installed 8 package(s)` line (the six agents plus two skills). `om chat` needs a model; the fake model and launcher in [chat-workspace-tui.md](chat-workspace-tui.md) work.

1. `control-om om -- agent list` and `--format json`; assert six names and `live` `idle`.
2. `control-om om -- agent show explain`; assert the four section rules and `Tools  library_read, room_read (locked)`. `agent show nosuch` exits 1 with the not-installed line.
3. `control-om om -- agent configure explain --paused on --format json`; assert `applied:["paused"]`, then `agent list` reads `paused` on the `explain` row. Undo with `--paused off`.
4. `control-om om -- agent ps --format json` reads `{"runs":[],"pool":{"limit":4,...}}` on a fresh lane. To get a run without a model, fire a watch agent step ([watch-agent-step.md](watch-agent-step.md)); the run fails `No LLM API key configured` on a guest lane and `agent ps` lists it with door `watch`. Read it with `agent ps <id from --format json>`; `agent cancel <id>` exits 1 `Run already failed.`
5. In tmux: ctrl+x, `a`; `Tab` to AGENTS; move to a row; `p`, `y`; then `control-om om -- agent list` on the CLI shows `paused`. `p`, `y` again to undo. `enter` opens the page; `Tab` walks the tabs; `esc` returns to the list and `esc` closes the overlay.
6. Close the overlay before typing in the composer: while it is open, letters are its keys (`p` pause, `s` shadow, `m` draw).

## Gotchas

- `om agent` has two generations of verbs. `list`, `show`, `configure`, `portrait`, `ps` and `cancel` are always there; `runs`, `pause` and `eval` (retained work runs) still need `OM_DEV=1`, and `om roster` (list, measures) is `OM_DEV=1` only.
- `agent ps` truncates the run id on a row (`run_99b0`); `agent ps run_99b0` answers `Run was not found.` Take the id from `--format json`.
- A watch-door run's `Ask:` is the step's whole `<watch_header boundary=…>` envelope, not only the ask you wrote (README gaps).
- Typing into the composer while the agents overlay is open sends keystrokes to the list. On 2026-11-04 a typed sentence opened `Draw librarian? y/n`; answer `n` and check `agent list --format json` for stray `paused`/`shadow` flags.
- A guest lane's chat shows `⚠ this install holds state from 1 other account (account guest_…)` on a fresh lane home; it is unrelated to the agents.
