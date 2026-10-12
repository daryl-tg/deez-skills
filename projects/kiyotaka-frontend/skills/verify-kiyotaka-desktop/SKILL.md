---
name: verify-kiyotaka-desktop
description: Use to drive and prove the OpenMarket desktop shell (Electron, kiyotaka-frontend desktop/) - launch it, capture the chart Turnstile-safe, run its returns, wallet, update and parity lanes.
---

# Verify the OpenMarket desktop shell

The desktop app is an Electron shell in kiyotaka-frontend's `desktop/` workspace package. It loads the web chart at
its real origin, so most of what it shows is the web app, and the shell adds a window, a menu, a link policy, an
`openmarket://` return channel, a two-member bridge (`window.openmarketDesktop`), notifications and an updater. The
contract it proves against is the web repo's `docs/features/desktop/desktop-shell.md`.

Everything runs through `bin/control-kiyotaka-desktop`, beside this file. It resolves the product checkout from your
working directory and drives only what the checkout ships: the vite dev lane and `desktop/tools/verify/*`.

## Which skill is this

| Reach for | When |
|---|---|
| **this skill** | Anything the shell owns, or a web change that must be seen inside the shell: launch, window, links, menu, returns, notifications, updates, the connect dialog and handoff wallet, the parity sweep |
| `verify-kiyotaka` | A web-app behavior in an ordinary browser. The parity sweep replays its map inside the shell |
| `verify-chart-fix` | A chart or data-loading fix that needs its RED to GREEN gate |

## Two rules that cost runs when broken

1. **Never attach Playwright to a Turnstile screen.** Cloudflare Turnstile reads "Verification failed" with
   Playwright attached and "Success" in a plain launch (the 2026-10-12 auth spike). The sign-in screen and anything
   behind it are captured through `capture`, which preloads `desktop/tools/verify/capture.js` into a plain launch and
   takes the frame from the main process. `browser` drives Chromium, never the shell window.
2. **Keep exactly one packaged copy on disk when a scheme-return lane runs.** macOS hands `openmarket://` to whichever
   `xyz.openmarket.desktop` bundle LaunchServices registered, so a second copy takes the returns lane's URLs and
   launches with the wrong profile (unit 3). `doctor` lists every copy, and `run launch ... returns|notify` refuses
   while any copy outside this checkout's `desktop/dist-app` exists.

## Pick a lane

| Lane | Loads | Use for |
|---|---|---|
| **Dev lane** (default) | The web app from this checkout on `127.0.0.1:$KIYO_DESKTOP_LANE_PORT` | Any web change not yet deployed: the handoff wallet, the sign page, the connect dialog gates, a parity sweep |
| **Production** (`--prod`) | `https://openmarket.xyz/chart/` | Shell-only behavior against the deployed chart |

An unpackaged launch, and a packaged build made by `pnpm package:dev`, honour `OPENMARKET_DESKTOP_URL`. A release
build never does.

## Launch

The shell lives in the repo's main checkout, `/Users/dboon/gitlab/kiyotaka-frontend`, only once `daryl/desktop-shell`
has landed on `main`. Before that, run from the feature worktree `/Users/dboon/gitlab/kiyotaka-frontend-desktop-shell`
instead; any checkout that carries `desktop/` works.

```bash
cd /Users/dboon/gitlab/kiyotaka-frontend                    # or the pre-landing worktree named above
CTL=~/github/deez-skills/projects/kiyotaka-frontend/skills/verify-kiyotaka-desktop/bin/control-kiyotaka-desktop
export KIYO_DESKTOP_LANE_PORT=18144                         # assigned from 18097-18197; record it for the run
lsof -nP -iTCP:$KIYO_DESKTOP_LANE_PORT -sTCP:LISTEN || echo free   # preflight: must print free
$CTL lane up                                                # add --testnet for the handoff and sign lanes
```

`lane up` binds `127.0.0.1` with `--strictPort`, refuses a taken port, writes a pidfile under
`desktop/.verify-userdata/control/`, and returns once `/chart/` answers. It reads the main checkout's
`~/gitlab/kiyotaka-frontend/.env.local` into the vite process with `node --env-file`; the file is never copied into the
worktree and never printed (`KIYO_DESKTOP_ENV_FILE` overrides the path). Without it the chart boots with no data and
reads "Retrying data request...".

Electron fetches its binary on first use. If `doctor` says `electron MISSING`, run `pnpm exec install-electron` in
`desktop/` once.

## Doctor

```bash
OUT=~/Documents/dev-notes/<task>/run-artifacts/<unit>     # the run's evidence folder
mkdir -p "$OUT"
$CTL doctor > "$OUT/doctor.txt" 2>&1; echo "doctor exit $?"; cat "$OUT/doctor.txt"
```

Read-only. It reports the tree and whether it is clean, its distance behind `origin/main`, the Electron binary,
Playwright, every packaged copy on disk, whether the lane on the port is served from this checkout, `/chart/`, and the
dev backend's health. It exits non-zero when the instance is not worth driving: a lane down or foreign, a backend not
`ok`, a missing binary. `doctor --prod` swaps the lane checks for production's `/chart/`. Test the exit code
unpiped; a pipe reports the last command's status.

## Drive

**Capture the chart in the shell.** This is the base recipe and the one every other proof starts from:

```bash
$CTL capture "$OUT/shell-chart.png"
```

It builds the shell, launches it unpackaged on a fresh profile against the lane, waits `CAPTURE_SETTLE_MS` (default
60 s) after the page loads, writes the PNG and a JSON report beside it, and checks five things: the
`desktop: loaded` line, no load failure, the window on the lane URL, a canvas, and a **priced title** such as
`83,214.3 ▲ BTC - USD`. The title is the proof of live candles. A chart with no data still has 18 canvases and reads
`BTC - USD`. Add `--prod` for the deployed chart and `--path '?login=1'` for the sign-in screen. Prove Turnstile with
`--prod`: the dev lane's env uses Cloudflare's test sitekey, which passes anywhere and says "For testing only".

**Run the checkout's lanes.** `run` passes the lane URL as `OPENMARKET_DESKTOP_URL` and runs the lane from its home:

```bash
$CTL run launch <out dir> window links channel      # production chart; window state, link policy, menu, channel
$CTL run launch <out dir> returns                   # dev lane, packaged dev build; scheme, bridge, returns
$CTL run launch <out dir> notify update             # identity and notifications; update round trip on 18150
$CTL run handoff <out dir> hl                       # needs lane up --testnet; MetaMask on a throwaway seed
$CTL run sign <out dir>                             # needs lane up --testnet; the sign page with MetaMask
$CTL run parity <out dir> [step ...]                # every verify-kiyotaka recipe in the shell and in Chromium
```

Each lane prints a JSON summary of its checks and exits non-zero on any failure. The feature map names what each one
proves, its preconditions and its known red checks. Start at `features/README.md`.

**Drive the browser half.** The sign page and anything else that runs in the user's default browser are Chromium
pages; drive them with `$CTL browser <verb>` (agent-browser) or the lanes above. Run `agent-browser skills get core`
for its verbs.

## Evidence

- Write frames to `~/Documents/dev-notes/<task>/run-artifacts/<unit>/`. That path resolves to local disk, outside
  iCloud, and it is where this program's reviews read evidence; there is no review-renderer publish step for the
  shell.
- `$CTL evidence check <dir>` fails on a directory with no PNG or an empty one, and says which frames have a report.
- A shell claim needs the frame and the shell's own line: the `capture:` JSON, a `desktop:` log line, or the lane's
  check name. A screenshot of a chart proves it drew; the line proves which URL and which build.
- Open every PNG. A capture of the "Draw by holding" tip over candles is a fresh guest and is fine; a capture of
  "Retrying data request..." is a lane with no backend.
- Never hand back an `18097`-`18197` URL as a review link; those ports are not tunnelled.

## Cleanup

```bash
$CTL lane down                         # by pidfile, then sweeps only a listener this checkout owns on the port
pgrep -fl 'capture.js|dist-app/.*/OpenMarket' || echo 'no shell left'
```

`capture` quits its own shell. Kill a leftover shell by its pid after checking its command line names your profile
under `desktop/.verify-userdata/`; never by name, since other agents run shells and lanes from the same machine. Run
cleanup after a failed attempt too. Evidence stays where it was written; profiles under `desktop/.verify-userdata/`
are gitignored and wiped by the next run.

## Helpers

`bin/control-kiyotaka-desktop` is the only helper. Its verbs are `doctor`, `lane up|down|url`, `capture`, `run`,
`browser`, `cli -- <command>` and `evidence check`; running it with no verb prints the list.

## Keeping it true

`maintain-verification-skill` is the upkeep pass. A lane or check renamed in `desktop/tools/verify/` changes the
matching feature file in the same change, with its provenance line.
