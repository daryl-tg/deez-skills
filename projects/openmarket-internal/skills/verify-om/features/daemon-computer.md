# The daemon's own browser

*Re-driven on main 2026-11-13 (nightly), tree `298c469dd7` (v0.495.0+internal), guest lane on 18185. `om computer status` (`Computer: off`, the driver and Chrome rows, `Windows: 0 of 4 in use`); `om computer on` from the run's own shell is refused exit 2 (`refusing to approve from an auto-approve harness`), and from a tmux terminal answers `Computer: on` with the `om computer open <address>` next step; `off`; `history`, `stats` and `sites` on an unused computer; `config set computer.asks bogus` exit 2. The dashboard's Computer page. MCP stdio lists no `computer_*` tool. Not re-driven: a task using the browser, the queue, the owner taking over, the MCP `computer_needs_owner_surface` refusals. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261113/r1/`.*

*On main since 2026-11-12: PR #2442 merged as `9a9fa313d1`, ported onto the public cut (the browser is core; its agent rules live in `packages/cli/src/private/agents/actions/_computer-surface.ts`; `computer-roster.test.ts` moved to `test/private/agents/`). Not yet re-driven on main or on the live daemon. The live build of 2026-11-12 answers `om computer status` with `Computer: off`.*

*Verified: 2026-11-11, branch `daryl/daemon-computer` tree `3e2ae2b37a` (PR #2442, on origin/main `0ad4768f66`), bare lane on 18141 with a scripted fake model on 18142, `agent-browser` 0.33.2 and Google Chrome 157. Gallery `http://127.0.0.1:8098/daemon-computer/r4/` (36 screenshots). Not on main until the PR merges.*

*First verified 2026-11-10 at tree `b9e34f8d2e`, gallery `daemon-computer/r2`, when the feature had one browser and per-site cards by default.*

`om computer on` gives the daemon a browser. The chat agent, watch steps and roster agents read and act through `computer_open`, `computer_read`, `computer_act`, `computer_screenshot` and `computer_status`. By default nothing asks. Each task leases its own window, tasks queue when every window is taken, and the dashboard's Computer page shows who is driving.

## Sub-features

- The switch: `om computer on`, `off`, `status`. `on` refuses when the driver or Chrome is missing and names `om computer setup`.
- Sites and windows: `om computer sites`, `allow`, `revoke`, `readonly`, `hide` and `close`; the `computer.window` setting is `hidden` or `visible` (source only).
- Setup: `om computer setup` downloads the pinned driver after a yes, checks its SHA-256, then offers Chrome. A stale `computer.driver_path` refuses up front.
- Free use: under `computer.asks never` (the default) open, read, every act step and screenshot run with no card, attended and unattended.
- Strict mode: `om config set computer.asks sites` brings back the read card per new site and the act card per site per 24 hours.
- Floors in both modes: `computer_venue_read_only`, `computer_site_read_only`, `computer_password_field`, `computer_payment_field` (any `autocomplete` token starting `cc-`), `computer_key_not_allowed`, `computer_private_address`.
- Source-supported on 2026-11-12 at `3854e41ace`, unit-tested only (`computer-act.test.ts`, `computer-capital.test.ts`), live proof pending: the payment-field refusal, and that `computer.asks` never changes the approval of `order_place`, `wallet_send` or `hyperliquid_transfer`.
- Windows: a signed-in site (`om computer open <address>`, then `release`) uses the `owned` window. Every other site uses `clean-<n>`, emptied per task. `computer.windows` sets the count.
- Leases: 90 seconds idle, 15 minutes at most. `computer_act` step `done` gives the window back. A reaped window reads `closing` until its browser is gone.
- Queue: at most 16 wait. `computer_busy` names the place in line and the holders.
- Reporting: `om computer status` lists windows, holders, sites, steps and waiters. `om computer history` lists ended runs. `ask_owner` shows as `needs you`.
- The owner's hold: `om computer open` takes the owned window only. Agent steps on it get `computer_human_in_control`. Clean windows keep working.
- Roster agents: an agent created with computer tool names gets them, in a run its owner started. Over MCP, `agent_fit`, `agent_create`, `agent_configure` and `agent_run` with a computer tool return `computer_needs_owner_surface`.
- The dashboard's Computer page: the board, a live view per window, Take over and Hand back.

## How to get to it (user POV)

1. `om computer setup`, answering yes, from a real terminal.
2. `om computer on`.
3. In `om chat`, ask for a page. For a site that needs a login: `om computer open <address>`, log in by hand, `om computer release`.
4. Open the dashboard and pick Computer in the sidebar.

## Driving it with control-om

- Bare lane as in [persona-chat-tools.md](persona-chat-tools.md). Export `OM_LANE_PORT` on every `control-om om --` call.
- `om computer on`, `setup`, `open` and `allow` need a real terminal. Run them in tmux on your own named socket. From an auto-approve harness `on` exits 2.
- The `computer_*` tools are not on MCP stdio; the agent reaches them in om chat, watch steps and roster runs.
- The lane's browsers live in a driver namespace derived from the lane's `OM_HOME` (`om-<16 hex>`), one session per window. Never drive, list or close a session outside it, and never run `agent-browser close --all`.
- A direct driver call with different environment variables restarts that session's browser. Go through `om computer` verbs, or match om's settings.
- Real sites used: `https://example.com`, `https://httpbin.org/forms/post`, one read and one refused click on `https://polymarket.com`.
- Two windows at once: a scripted chat turn on one site and a watch `ai` step on another. Capture `om computer status` mid-run.
- The queue: set `computer.windows` to 1, hold the window from a watch step, open a page from chat.
- A watch `tool` step behind a busy window ends at its own time budget (about 100 s) before the queue's bound, so it reports cut short, not `computer_busy`.
- The MCP refusals: `control-om om -- mcp serve --stdio --no-fire-bridge` and one `tools/call` each for `agent_fit` and `agent_run`.
- Setup with nothing installed: an empty `HOME`, a bare `PATH`, `OM_BRAIN_SYSTEM_DIRS` pointing nowhere and a scratch `OM_HOME`. It makes one real download from GitHub.
- The dashboard page is captured headless as in [ops-dashboard.md](ops-dashboard.md).
- The machine's DNS goes through Tailscale. `ERR_NETWORK_CHANGED` on a page open is the network, so rerun once.

### What to check

- Filling a field with the text `--headed` leaves the same Chrome process running, still headless, and the page echoes the text.
- A second task that claims while an expired lease is closing gets the window only after the first browser's process is gone.
- The owner taking the window mid-step gives the agent `computer_human_in_control` and no page text.
- Two firings of one watch show as two runs in history.
- A form on a public page that posts to a loopback listener sends nothing.

## Gotchas

- Typing through the dashboard's live view reaches the owned window and not a clean one. Clicks reach both.
- A run started by a second room member cannot be staged on a bare lane. The refusal is unit-tested.
- A real login with a second factor, a visible window from a launchd-started daemon, and the live view on an auth-enforcing bind have not been driven.
- Linux, Windows, a machine with no Chrome, and driver versions above 0.33.2 have not been driven.
- No live eval area covers how a real model chooses these tools.
- A click is not floored: on a signed-in site with a saved card, `Buy` rides only the skill's rule. The payment-field floor stops typing, not `select` or the browser's autofill.
- Since 2026-11-12 the PR is one level of a stack: main, #2465 database fix, #2442, #2466, #2448, #2451, #2453. Rebasing any level can merge its changelog entry into a released section; check it sits under `[Unreleased]`.

## Live pass on the real daemon (2026-11-13, Grok 4.3)

Proven live:

- `om computer open`, `status`, `release`, `history`, `stats`, `sites`, `forget` and `close` behave as the recipe says.
- A watch ai step created with `--tools computer_open,computer_read` reads a page with nobody attending and delivers to its channel.
- The venue floor refuses a click (`computer_venue_read_only`). A form fill ends with `done`.
- With `computer.windows 1`, a chat ask waits for a watch's window and gets it (`Queue: 1 waited`).

How to drive it:

- `om chat --once` appends to the live `cli` conversation. Send `/new` first and `/resume <id>` after.
- Two `--once` asks at once run one after the other, so contention needs a watch step plus a chat ask.
- Never run `om computer off` in a test: `om computer on` needs a person.
- On Grok, say "load computer_open with tool_search" in the ask, or the turn may loop on `skill_read`.
- Read cost from `om usage llm` before and after a turn.

Known defects, not fixed: idle windows end only at the next browser call; steps skip `done`; `computer_open` on an XML feed returns viewer controls, so read with `computer_read` in text mode; `release` marks the site signed in.

Pending proof: the card-field floor on a public checkout page, `om computer off` mid-run, the dashboard live view.

## Blocked sources read through the browser (#2481, on main since 2026-11-13)

What it is: a feed or page source whose host challenges or refuses the plain fetch reads its own address through om's browser, before Firecrawl, with no model call. Setting `computer.sources`.

Recipe, on a daemon whose cooldowns stand (the live one; a fresh lane often reads the same hosts by plain fetch):

1. `om computer status` reads `Computer: on`.
2. Wait for the source's poll, or restart the daemon so every source polls.
3. `om computer history`: a row `source <host>  clean-1  done` per read, seconds long.
4. `om watch show <watch>`: the source row reads `working · reads through om's browser`.
5. `om computer stats`: a `source` row; errors `source_human_check` or `source_driver_failed`.
6. A host showing a human check: the source reads `<host> asks for a human check; open <address> once`. Nothing is clicked.
7. `/healthz` lists the loop `computer-leases` with verdict `ok`; no browser process stays after a read.

Proven live 2026-11-13: Ars Technica, VentureBeat and Product Hunt feeds served; hltv.org stopped at its check; Reddit failed in the browser too.

Lane notes: start the daemon with `bootstrap.internal.ts run`; switch the computer on in a scratch home through `setComputerEnabled`; to restart, kill the pid that holds the port, not the wrapper's.

Pending proof: a page source (not a feed) through the browser, and the hand pass (`om computer open`, pass the check, `om computer release`) letting a held source read again.
