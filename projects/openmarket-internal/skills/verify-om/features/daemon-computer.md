# The daemon's own browser

*Re-driven 2026-11-18 (nightly), tree `db4ba5c6e2` (origin/main, v0.496.0+internal), guest lane on 18188 with `OM_COMPUTER_ALLOW_LOOPBACK=18112`, computer turned on from a private tmux (the daemon installed the headless shell 157.0.8103.78 in 9 s). First live proof of #2563's named check: a loopback feed answering `403` with `cf-mitigated: challenge` and the title `Just a moment...` was escalated to the browser at 19:29:59Z, waited out for about 15 s, and held at 19:30:14Z with the lane log `[browser-read] 127.0.0.1: 127.0.0.1 asks for a human check (Cloudflare wait page); held from the browser`. `computer sources` read `http://127.0.0.1:18112  held`, `Last: 03:30 through the browser, human check`, `Held: http://127.0.0.1:18112/rss until 04:00 (human check, Cloudflare wait page)`; `watch show` `FAULT feed 127.0.0.1: stub feed: needs a human check since Nov 18 03:30 · 127.0.0.1 asks for a human check (Cloudflare wait page)` / `FIX om computer pass http://127.0.0.1:18112/rss`. Without the loopback switch the same read fails `om's browser could not read it (private address)`. The dashboard Computer page still shows no source row. Not driven: agent windows (names, `read_only`, `allowed_sites`, `computer_bot_check`; they need a model turn), a self-clearing check that clears, the per-site caps (#2531), `page_read` through the browser. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261118/r1/` (`cli/computer-bot-check.txt`, `02-dash-computer.png`).*

*Re-driven 2026-11-17 (nightly), tree `8e350d253a` (origin/main, v0.495.0+internal), guest lane on 18188 (guest sign-in 429 all pass, which none of this needs). First live proofs of #2501, #2521 and #2524: the `browser` row in `om doctor`, `Browser:` in `om status` and `om's browser` in `om setup`; `computer.offers` read, set `off` and back; `computer.sources` is gone (`unsupported config key`); `om computer sources` with no route; `om computer on` in a private tmux, after which the daemon installed the headless shell by itself (9 s, `SHA-256 verified`, 205 MB under the lane home); then a loopback feed whose plain fetch is challenged read through the browser 3 s later, its route kept the browser across a lane restart, retried the plain fetch at 5 and 10 minutes, and went back to the plain fetch on the first direct success; the idle browser closed five minutes after its last read (`blocked-source-route`). `/computer` in om chat ([chat-workspace-tui.md](chat-workspace-tui.md)). Not driven: `om init`'s browser question, the daemon's offer card, a human-check hold through the browser, the memory cap. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261117/r1/` (`01-dash-computer.png`, `cli/computer*.txt`, `cli/blocked-route-*.txt`, `cli/stub-requests.log`).*

*Re-driven 2026-11-14 (nightly), tree `05300a3142` (origin/main, v0.495.0+internal), guest lane on 18185: the `computer.sources` setting read, set `off`, set `on`; the dashboard Computer page rendered. The browser read itself was not re-driven. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261114/r1/` (`cli/computer-sources.txt`, `dash/02-computer.png`).*

*Re-driven on main 2026-11-13 (nightly), tree `298c469dd7` (v0.495.0+internal), guest lane on 18185. `om computer status` (`Computer: off`, the driver and Chrome rows, `Windows: 0 of 4 in use`); `om computer on` from the run's own shell is refused exit 2 (`refusing to approve from an auto-approve harness`), and from a tmux terminal answers `Computer: on` with the `om computer open <address>` next step; `off`; `history`, `stats` and `sites` on an unused computer; `config set computer.asks bogus` exit 2. The dashboard's Computer page. MCP stdio lists no `computer_*` tool. Not re-driven: a task using the browser, the queue, the owner taking over, the MCP `computer_needs_owner_surface` refusals. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261113/r1/`.*

*On main since 2026-11-12: PR #2442 merged as `9a9fa313d1`, ported onto the public cut (the browser is core; its agent rules live in `packages/cli/src/private/agents/actions/_computer-surface.ts`; `computer-roster.test.ts` moved to `test/private/agents/`). Not yet re-driven on main or on the live daemon. The live build of 2026-11-12 answers `om computer status` with `Computer: off`.*

*Verified: 2026-11-11, branch `daryl/daemon-computer` tree `3e2ae2b37a` (PR #2442, on origin/main `0ad4768f66`), bare lane on 18141 with a scripted fake model on 18142, `agent-browser` 0.33.2 and Google Chrome 157. Gallery `http://127.0.0.1:8098/daemon-computer/r4/` (36 screenshots). Not on main until the PR merges.*

*First verified 2026-11-10 at tree `b9e34f8d2e`, gallery `daemon-computer/r2`, when the feature had one browser and per-site cards by default.*

`om computer on` gives the daemon a browser. The chat agent, watch steps and roster agents read and act through `computer_open`, `computer_read`, `computer_act`, `computer_screenshot` and `computer_status`. By default nothing asks. Each task leases its own window, tasks queue when every window is taken, and the dashboard's Computer page shows who is driving.

## Sub-features

- The switch: `om computer on`, `off`, `status`. Since #2501 one switch covers agent use and blocked-source reads. `on` checks the driver and Chrome before the human check, so a missing driver refuses with `computer_driver_missing` (or `_too_old`, `computer_chrome_missing`) even from an auto-approve harness; with both present the harness refusal comes next. When on, `status` adds `Sources: <n> through the browser · <n> reads last hour · <n> held · engine headless shell|full Chrome`, and `Loopback: allowed on 127.0.0.1:<port> in the last 24h (test rig)` under `OM_COMPUTER_ALLOW_LOOPBACK`.
- Where it shows (#2521): `om doctor`'s `browser` row (`off · om computer on turns it on`, `on · headless shell`, or a warn naming a missing driver, Chrome or shell); `om status` `Browser:    off → om computer on` or `on · headless shell`; the `om setup` overview `✓ om's browser (on, headless shell)`; `/computer` in om chat; `om init` asks `Turn on om's browser?` once in a real terminal (source only: it needs a TTY and skips on a pipe or a headless box).
- `computer.offers` (default `on`): the daemon raises one owner card to turn the browser on when blocked sites keep breaking watches; a no is quiet for 30 days. Source only for the card.
- Sites and windows: `om computer sites`, `allow`, `revoke`, `readonly`, `hide` and `close`; the `computer.window` setting is `hidden` or `visible` (source only).
- Setup: `om computer setup` downloads the pinned driver after a yes, checks its SHA-256, then offers Chrome and the headless shell, with a download progress line. A stale `computer.driver_path` refuses up front. Since #2521 the daemon installs the headless shell by itself whenever the computer is on and the shell is missing, into `<home>/computer/engines/` (lane log `installing the headless shell 157.0.8103.78 for source reads`, then `installed ... SHA-256 verified`).
- Free use: under `computer.asks never` (the default) open, read, every act step and screenshot run with no card, attended and unattended.
- Strict mode: `om config set computer.asks sites` brings back the read card per new site and the act card per site per 24 hours.
- Floors in both modes: `computer_venue_read_only`, `computer_site_read_only`, `computer_password_field`, `computer_payment_field` (any `autocomplete` token starting `cc-`), `computer_key_not_allowed`, `computer_private_address`.
- Source-supported on 2026-11-12 at `3854e41ace`, unit-tested only (`computer-act.test.ts`, `computer-capital.test.ts`), live proof pending: the payment-field refusal, and that `computer.asks` never changes the approval of `order_place`, `wallet_send` or `hyperliquid_transfer`.
- Windows: a signed-in site (`om computer open <address>`, then `release`) uses the `owned` window. Every other site uses `clean-<n>`, emptied per task. `computer.windows` sets the count.
- Leases (since #2563): a window ends after 10 minutes idle and never while a step runs; a named window has no overall cap; when every window is taken the window idle longest goes, once idle at least 60 s (`runner/computer/leases.ts`). `computer_act` step `done` gives the window back. A reaped window reads `<name|n>: closing` until its browser is gone. The keeper sweeps a stray browser holding a window's profile every 15 s. Source only.
- Agent windows (#2563, source only): `computer_open` takes `name`, `read_only` and `allowed_sites`, refused as `computer_window_read_only`, `computer_site_not_allowed` and `computer_always_refused`. `computer_open` and `computer_act` return `check` and `check_note` on a page with a bot check ("A Cloudflare checkbox is on this page: never click or solve it; call computer_act with ask_owner so the owner passes it."), and a step on a control inside one is refused `computer_bot_check`.
- Queue: at most 16 wait. `computer_busy` names the place in line and the holders.
- Reporting: `om computer status` lists windows as `<name|n>: <holder>, <site>, working|idle for 42s, <n> steps` (the held time is gone since #2563), waiters, and `· 2 sites rate limited` on the `Sources:` row (#2531); the window rows and the rate-limited count are source only. `om computer history` lists ended runs. `ask_owner` shows as `needs you`.
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

Known defects, not fixed (recorded before #2563, whose keeper sweep may retire the first; not re-checked): idle windows end only at the next browser call; steps skip `done`; `computer_open` on an XML feed returns viewer controls, so read with `computer_read` in text mode; `release` marks the site signed in.

Pending proof: the card-field floor on a public checkout page, `om computer off` mid-run, the dashboard live view.

## Blocked sources read through the browser (#2481, on main since 2026-11-13)

What it is: a feed or page source whose host challenges or refuses the plain fetch reads its own address through om's browser, before Firecrawl, with no model call. Since #2501 there is no separate setting: `computer.sources` is gone (`om config get computer.sources` exits 2 `unsupported config key`), and `om computer on|off` covers source reads and agent use together. Since #2501 and #2524 the site's route is remembered: polls go straight to the browser, the plain fetch is tried again after 5 minutes, then 10, 20, 40 and every 60, and one direct success sends the source back to the plain fetch. The route is a database row and survives a restart. Source reads run in om's own `sources-1`/`sources-2` browsers, two at a time at most, take no agent window and leave `om computer history` empty. Since #2563 a read gets 15 s, or 25 s when it meets a check; a self-clearing check (Cloudflare's wait page: a `403`/`503` with `cf-mitigated: challenge`, or a `Just a moment...` title with no widget) is waited out for 15 s, and an interactive one (a checkbox, PerimeterX, DataDome, Akamai, Imperva, AWS WAF, reCAPTCHA, hCaptcha, an access-denied or verification page) is held at once. Vendor words live in `shared/bot-check-words.ts`. Since #2531 (source only): a 429 holds the whole site from the browser for `Retry-After` (at most 6 h), else 30 min doubling to 6 h; a site gets 60 browser reads an hour, past which the read fails `source_site_budget`; one site may take at most 8 of the 32 waiting reads; at 800 MB across both source browsers the second closes after its read; and `page_read` retries a refused page once through the browser (`read_through: browser`, never Firecrawl).

- `om computer sources` lists each routed origin: `<origin>  browser|direct`, `Last: HH:MM through the browser|direct, ok`, `Today: N through the browser, M direct`, `Next direct try: HH:MM` while it routes to the browser, `Held: <address> until HH:MM (human check, <check words>)` (driven 2026-11-18: `(human check, Cloudflare wait page)`, a 30-minute hold) or `(refused)`, and since #2531 `Held: rate limited until HH:MM` and `Browser budget used: 60 this hour` (source only). With none: `No source has needed om's browser yet.`
- `om computer pass <address>` opens the address in your window to pass a human check by hand (source only).

### Blocked-source route on a lane (added 2026-11-17)

Proved with a loopback stub whose challenge spares the browser, so the plain fetch is refused and the browser read is served:

1. Copy `helpers/origin-challenge-stub.ts` into a scratch directory and change its challenge test to `m === "challenge" || (m === "plainchallenge" && !/HeadlessChrome/.test(req.headers.get("user-agent") ?? ""))`, logging the user agent. om's plain fetch sends a desktop Chrome user agent; the headless shell's carries `HeadlessChrome`. Run it on an agent port (18111) from its own data directory with `echo ok > mode`.
2. `control-om up --env OM_FEED_ALLOW_LOOPBACK=1 --env OM_FEED_POLL_INTERVAL_MS=60000 --env OM_COMPUTER_ALLOW_LOOPBACK=18111`. Without the last switch the browser refuses a loopback address.
3. Turn the computer on from a private tmux (`control-om om -- computer on`). The daemon installs the headless shell into the lane home by itself (9 s, 205 MB on 2026-11-17). `computer status` reads `Loopback: allowed on 127.0.0.1:18111 in the last 24h (test rig)` and `Sources: 0 through the browser · ... · engine headless shell`.
4. `OM_FEED_ALLOW_LOOPBACK=1 control-om om -- watch page-add http://127.0.0.1:18111/rss --prefer feed --every 60s` → `feed_created`; the stub logs one plain `ok GET /rss` a minute.
5. `echo plainchallenge > mode`. Driven 2026-11-17: the next poll logged `challenge GET /rss headless=false` at 19:27:31Z and the browser's `ok GET /rss headless=true` at 19:27:34Z. `computer sources` read `http://127.0.0.1:18111  browser`, `Last: 03:27 through the browser, ok`, `Next direct try: 03:32`; `computer status` `Sources: 1 through the browser · 1 reads last hour · 0 held`; `watch show` `Coverage: ok (browser, last poll ...)`. Every later poll went straight to the browser, with no plain request.
6. At 19:32:34Z the plain fetch was tried again, challenged, and the browser read 74 ms later; `Next direct try: 03:42` (10 minutes). A lane restart (`down`, `up` with the same switches) kept the route, `Last` and `Next direct try` unchanged.
7. `echo ok > mode`. The direct try at 19:42:52Z succeeded: `computer sources` read `http://127.0.0.1:18111  direct`, `Last: 03:42 direct, ok`, `Today: 16 through the browser, 1 direct`; `Sources: 0 through the browser`; `watch show` `Coverage: ok (feed, ...)`.
8. The warm browser closes by itself (#2524, `SOURCE_BROWSER_IDLE_MS` 5 minutes): the headless shell and its driver, started at the lane restart (19:32:50Z), exited at 19:46:56Z, five minutes after the last browser read (19:41:52Z). The pre-restart browser was already gone after the restart. Check with `ps` for `chrome-headless-shell` under the lane home's `computer/engines/`.

**Named check on a lane (added 2026-11-18).** Run a second stub on its own agent port (18112) whose `challenge` mode answers every request `403`, `cf-mitigated: challenge`, `<title>Just a moment...</title>`; start the lane with `--env OM_COMPUTER_ALLOW_LOOPBACK=18112`; add the feed, set `--classifier-mode accept_all`, then `echo challenge > mode`. About 15 s after the next poll `computer sources` reads `held` with `(human check, Cloudflare wait page)`. Add `turnstile` or `click to verify` text to the body for `Cloudflare checkbox` (source only).

On a guest lane the watch's headline names the AI-filter fault, so `watch show`'s `reads through om's browser` status line is displaced; read `Coverage:` instead. The dashboard's Computer page shows no `Sources` row (2026-11-17).

Recipe, on a daemon whose cooldowns stand (the live one; a fresh lane often reads the same hosts by plain fetch):

1. `om computer status` reads `Computer: on`.
2. Wait for the source's poll, or restart the daemon so every source polls.
3. `om computer sources` names the host's route (since #2501 source reads no longer appear in `om computer history`).
4. `om watch show <watch>`: the source row reads `working · reads through om's browser`.
5. `om computer stats`: a `source` row; errors `source_human_check` or `source_driver_failed`.
6. A host showing a human check: the source reads `<host> asks for a human check (<check words>); open <address> once` (since #2563, e.g. `(Cloudflare wait page)`); `watch show`'s FIX is `om computer pass <address>`. Nothing is clicked.
7. `/healthz` lists the loop `computer-leases` with verdict `ok`; no browser process stays after a read.

Proven live 2026-11-13: Ars Technica, VentureBeat and Product Hunt feeds served; hltv.org stopped at its check; Reddit failed in the browser too.

Lane notes: see the lane recipe above. A computer switched on in a lane makes its daemon download the headless shell into the lane home; delete the lane home afterwards.

Pending proof: a page source (not a feed) through the browser, and the hand pass (`om computer open`, pass the check, `om computer release`) letting a held source read again.
