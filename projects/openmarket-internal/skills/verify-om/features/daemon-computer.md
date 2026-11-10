# The daemon's own browser

*Verified: 2026-11-10, branch `daryl/daemon-computer` tree `b9e34f8d2e` (PR #2442, on origin/main `c0901d5bf6`), bare lane on 18141 with a scripted fake model on 18142, `agent-browser` 0.33.2 and Google Chrome 157. Gallery `http://127.0.0.1:8098/daemon-computer/r2/` (19 screenshots). Not on main until the PR merges.*

`om computer on` gives the daemon a Chrome profile under `OM_HOME`. The owner logs in by hand in a visible window. The agent reads and acts through `computer_open`, `computer_read`, `computer_act`, `computer_screenshot` and `computer_status`, under site grants the daemon keeps. The dashboard's Computer page shows the live page with Take over and Hand back.

## Sub-features

- The switch: `om computer on`, `off`, `status`. Off by default. `on` refuses with no driver installed (exit 2) and under an auto-approve harness.
- Site grants: `om computer sites`, `allow <site> [--act] [--always]`, `revoke`, `readonly`. A venue site takes `read` only.
- The read card: a new site asks once (`SITE`, `OPENS`, `READS`, `REMEMBERED`). A second read on that site shows no card.
- The act card: clicks and typing ask once per site per 24 hours (`SITE`, `DOES`, `ALLOWS`, `NEVER`).
- Refusals with no card: `computer_venue_read_only` on a site om trades on, `computer_password_field`, `computer_key_not_allowed` for a printable key, `computer_page_moved`, `computer_human_in_control`, `computer_off`.
- Unattended: a watch `ai` step reads a granted site and gets `computer_site_not_granted` on any other. It never clicks and mints no grant.
- Status for the agent shows only the site for a page with no read grant. `om computer status` shows the full address.
- The owner's window: `om computer open [address]` makes it visible and holds the computer. `om computer release` hands it back. `om computer hide`, `om computer close`.
- The dashboard's Computer page: status rows, the live frame, Take over and Hand back. Typed input reaches the page only while held.
- The driver's stream is off unless a dashboard viewer is connected.
- The hold survives a daemon restart.

## How to get to it (user POV)

1. Install the driver: `npm install -g agent-browser` (or Homebrew).
2. `om computer on`, from a real terminal.
3. `om computer open https://example.com`, log in by hand, `om computer release`.
4. In `om chat`, ask for a page on that site. Answer the card.
5. Open the dashboard and pick Computer in the sidebar.

## Driving it on a lane

- Bare lane, no account: a dummy `OM_API_KEY`, every service URL at `http://127.0.0.1:9`, `OPENMARKET_LLM_PROVIDER=openai-compatible` pointed at a scripted fake model, as in [persona-chat-tools.md](persona-chat-tools.md). Export `OM_LANE_PORT` on every `control-om om --` call.
- `om computer on` must run inside tmux or another real terminal. A harness parent is refused by design.
- The lane's browser lives in a driver namespace derived from the lane's `OM_HOME` (`om-<16 hex>`). Never drive, list or close a session outside it, and never run `agent-browser close --all`. Other sessions on the machine share the default namespace.
- Real sites used: `https://example.com` (read), `https://httpbin.org/forms/post` (fill and submit), one read of `https://polymarket.com` (venue refusal).
- The scripted model calls `computer_open`, then `computer_act` with the `site` the result returned. `computer_read` needs `site` too.
- The unattended case is a prompt `ai` step with `tools: [computer_open]`, as in [watch-agent-step.md](watch-agent-step.md). A roster-agent step brings its own tools.
- The dashboard page is captured headless as in [ops-dashboard.md](ops-dashboard.md). Start a viewer before expecting `stream status` to read enabled.
- `skill_read` of `computer` is driven from a chat turn. There is no `om skill read` verb.

## What to check

- Filling a field with the text `--headed` leaves the same Chrome process running, still headless, and the page echoes the text. The driver parses a bare `--` argument as its own option, so this is the regression that matters most.
- A second `computer_open` on a granted site paints no card.
- After Take over, an agent call returns `computer_human_in_control`. After Hand back it works.
- `om computer sites` is unchanged after an unattended run.

## Gaps

- A real login with a second factor has not been driven.
- A visible window from a launchd-started daemon has not been driven.
- The stream on a bind that enforces auth has not been driven.
- Linux, Windows, and driver versions above 0.33.2 have not been driven.
- No live eval area covers how a real model chooses these tools.
