---
name: verify-om
description: Use when a change to the `om` daemon or CLI (the openmarket-internal monorepo — packages/cli, packages/sdk, the runner, the action registry, the ops dashboard) needs to be driven and proven in the running product — booting an isolated lane daemon, exercising a surface the way a user would through the CLI and the daemon's HTTP doors, capturing evidence, and publishing a gallery for review.
---

# Verify om

`om` is a local-first market-intelligence daemon: one binary, several surfaces
over one capability layer — the CLI (`om <verb>`), the runner daemon and its
HTTP doors (`/healthz`, `/rpc/v1/*`, `/ingest/v1/*`, `/events/v1`), the React
ops dashboard the daemon serves at `/`, and MCP. This skill is the executable
half of verification: how to get a driveable instance up **without touching the
operator's own daemon**, how to drive it, and how to turn what you saw into
evidence someone else can open.

Sibling skills own neighbouring ground. `verify-om-chat` owns the `/rooms` and
`/chat/` GUI, which lives in a different repo. `om-build` owns building that
GUI. This skill owns everything the open-core repo itself ships.

Everything here goes through `control-om`, at
`/Users/dboon/github/openmarket-internal/control-om`.

## The one fact that makes this safe

**The operator runs a real `om` daemon on `31337` against `~/.openmarket`.**
That home holds their API key, their wallet, their watches and their execution
receipts. A verification run must never reach it.

The lane is a *different root*, not a tenant inside theirs: `control-om` boots
`om run` with `OM_HOME` pointed at `.control-om/home-<port>` and `OM_BIND` at an
assigned agent port. Every `control-om om -- <args>` call carries the same two
variables, so the CLI talks to the lane and writes the lane's root.

A bare `om <verb>` typed in this repo does **not**. It resolves the ambient
`OM_HOME` and `OM_BIND`, which is the operator's. There is no visible
difference in the output. Use the wrapper's `om` door for every CLI call, with
no exceptions.

Since `3a81eb478`, **`OM_HOME` names a root, not a home.** The root holds one
line, `active`, plus `accounts/`; the actual home — database, credentials,
`runner.log`, `watches/`, `event-journal/` — is `accounts/<name>/`, and before
any login that is `accounts/guest/`. So the lane's files are under
`.control-om/home-<port>/accounts/guest/`, and `/healthz` reports that path as
`om_home`, not the root you passed. `om profile` and `OM_PROFILE` are gone.

**The product used to refuse service lifecycle on a non-default home. It does
not any more.** Until the accounts refactor (`3a81eb478`) a non-default home
shared the machine-global unit label, so `om service install|start|stop|restart`
were refused there. Now a non-default root **names a unit of its own**
(`unitNameIsMachineGlobal` in `runner/supervise/unit-name.ts`, consulted by
`unitIsAnotherHomes` in `runner/supervise/index.ts`), so nothing refuses them —
`om service install` on a lane would install a second launchd unit that outlives
the run.

So the guard lives at the wrapper instead: `control-om om -- service
install|uninstall|start|stop|restart` refuses and exits 1. Read-only
`om service status` passes through. Do not work around it, and do not reach for
a bare `om` to do what the wrapper refused.

Everything else the lane can do — `om reset`, orders, token rotation — is
refused by nothing and acts on the lane's home. That is the whole reason a run
is only ever pointed at the lane's home.

## Where the wrapper lives

`control-om` lives in this skill (`bin/control-om`), tracked with it, and is
reached through a symlink on `PATH` (`~/.local/bin/control-om`). It is **never**
placed inside `openmarket-internal`: that repo is the Apache-2.0 public export
with a boundary gate and a license audit, and a file that is not in it cannot
reach its remote.

**It resolves the repo from where you are standing**, via
`git rev-parse --show-toplevel`, so one copy drives whichever worktree your
shell is in — and there are dozens. `cd` into the tree you mean and run
`control-om`; no copying, no per-worktree setup, and nothing to go missing when
you switch branches. Two guards keep that honest: outside a git worktree it
refuses, and inside a checkout that is not openmarket-internal (no
`packages/cli/src/bootstrap.ts`) it refuses by name. `OM_REPO_ROOT` overrides
for the rare call from outside a tree.

Run state stays per-worktree and ignored: each tree gets its own
`.control-om/` (lane homes, pidfiles, logs) and `artifacts/`, both excluded via
`.git/info/exclude`, which lives in the shared common `.git` and therefore
applies to every worktree automatically.

One thing to know when driving two trees at once: the lane port is assigned, not
per-tree, so the second `up` on the same port refuses rather than stealing the
first. Give it `--port` from the `18097`–`18197` range.

## Launch

```bash
cd /Users/dboon/github/openmarket-internal

# Ports are ASSIGNED, never discovered. 18097-18197 is the agent range;
# 18101 is this lane's conventional slot (18097-18099 belong to om-chat lanes).
control-om up
# -> http://127.0.0.1:18101
```

`up` binds `127.0.0.1` explicitly, refuses a busy port rather than stealing a
neighbour's lane, refuses `8097`/`8098`/`31337`/`31338` outright, writes the
dashboard bundle stubs if they are missing, records a pidfile under
`.control-om/`, and blocks until `/healthz` actually answers. Boot is about 20
seconds from source.

Some behaviour only exists under a switch, so `up` takes repeatable
`--env KEY=VALUE` and passes it to the lane daemon:

```bash
control-om up --env OM_FEED_ALLOW_LOOPBACK=1 --env OM_FEED_POLL_INTERVAL_MS=60000
```

It is deliberately explicit rather than forwarding every `OM_*` in your shell —
a stray variable must never reach a lane silently — and it refuses `OM_HOME` and
`OM_BIND`, which the lane owns. `doctor` prints what the running lane was
started with on a `lane env` line. **A switch the CLI also reads must be set on
the CLI call too**: `om` subcommands run in their own process and inherit
nothing from the lane, which is how the origin-challenge recipe fails at its
first step if you set the switch only on `up`.

Ready when it prints the origin. If it prints a boot failure instead, read
`.control-om/lane-<port>.log` — the daemon's own stdout goes there and nothing
else carries it.

The lane runs **from source** (`bun packages/cli/src/bootstrap.ts run`), so the
process *is* the working tree: no build step, and no stale-bundle trap for the
daemon or the CLI. The compiled `packages/cli/dist/om` is a different question —
see [Gotchas](#gotchas-that-cost-a-run).

Teardown is [Cleanup](#cleanup).

## Doctor

One read-only command, before you drive anything:

```bash
control-om doctor
```

It reports the repo HEAD, the lane origin and root, whether the dashboard bundle
exists, whether a compiled binary is lying around, whether the lane is down /
yours / somebody else's, the `/healthz` version and auth posture, **whether the
lane's daemon still matches the working tree**, **whether the operator's daemon
is live on 31337**, `agent-browser`, and the review renderer on `8098`. It exits
non-zero when the lane is not worth driving.

Three lines earn their place. `lane version STALE` is the one this skill learned
the hard way: a source lane is the tree **at boot**, not the tree now, and
another session syncing the repo mid-run leaves you driving old code with every
other signal green. Re-run doctor after any surprise, and `down` then `up` when
it fires. `dashboard dist MISSING` is fatal and not obvious:
the daemon imports the bundle at module load, so a checkout that never ran
`bun run dashboard:stubs` fails to boot at all rather than merely losing the SPA.
And `operator om daemon LIVE on 31337` is there so a run can never confuse the
two — that one is not yours, at any point, for any reason.

Expect `daemon_version: warn` from the product's own `om doctor` whenever the
lane and the CLI disagree; that check is what caught a mid-pass tree move before
`control-om doctor` could see it, which is why the wrapper now checks too.

For the product's own self-diagnosis, which is a different question, run
`control-om om -- doctor`. On a fresh lane it reports
`binary: warn — running from a dev checkout`, `llm: warn — no LLM configured`
and `contracts/stream: warn — registry unreachable`. All four are the expected
shape of a guest lane, not findings.

## Drive

Two doors, one lane.

**The CLI** — every `om` call goes through the wrapper so it lands on the lane's
home and port:

```bash
control-om om -- watch list
control-om om -- event push my-watch --text "probe" --format json
control-om om -- status
```

Add `--format json` wherever it exists. The text renderers are the human
surface and change; the JSON is what you assert on.

**The dashboard** — `agent-browser` through the wrapper (or directly; the
wrapper only ensures it exists). Give the run its own session so you cannot
clobber another agent's browser:

```bash
export AGENT_BROWSER_SESSION=verify-om-<your-run-id>
agent-browser set viewport 1440 900
agent-browser open "$(control-om url /alerts)"
agent-browser snapshot -i -c
```

**Drive by ARIA role and accessible name, never by coordinates or CSS.** The
dashboard labels its nav and tables well:

```bash
agent-browser find role link click --name "Watches"
agent-browser get url                       # -> http://127.0.0.1:18101/alerts
```

Label and route drift apart: that nav item was renamed from `Alerts` and its
path was not. Drive by the label the snapshot shows, assert the path.

Re-snapshot after anything that changes the page — refs go stale immediately.
Run `agent-browser skills get core` for a command this skill does not show.

Read `features/` for the routes, handles and recipes of each surface.

For a repo command whose exit code matters:

```bash
control-om cli -- bun run typecheck
```

## Evidence

Capture the **action and its result**, not just the final screen, and verify a
side effect alongside what is visible. A single after-shot proves the daemon can
render that state, not that your interaction produced it.

This product gives you an unusually strong chain for free, because one user
action is observable on four independent surfaces. The worked example is
`features/event-ingest-and-fire.md`, which proves a fire end to end with no
credentials at all:

1. **The door's own answer** — `POST /ingest/v1/<watch>` returns `202` with an
   `event_id`.
2. **The live stream** — `/events/v1` carries `watch_committed`,
   `watch_appended` and `watch_fired` for that same `event_id`. (The `event_`
   prefix these three carried before v0.35 is gone; a grep for the old names
   matches nothing and silently proves nothing.)
3. **The stored side effect** — `om event-journal get <slug> --file events.md`
   contains the pushed text, the classifier verdict and the id.
4. **The other surface** — the dashboard row for that watch, on the nav item
   now labelled **Watches** at the unchanged route `/alerts`, reads `working`
   with a LAST FIRED matching the stream's `fired_at`.

Correlate on the `event_id` and the timestamp. Four surfaces agreeing on one id
is a claim that survives review; a screenshot of a table is not.

**Make the probe text unique per run.** The `event_id` is derived from the
event's content, not minted randomly: the same probe text pushed into two
different fresh lanes produced the identical id. A correlation id that repeats
across runs cannot show which run produced the row, so put the run id in the
text.

Write frames and captured output into `artifacts/<run-id>/<revision>/`, then
publish:

```bash
control-om evidence publish <run-id> <revision>
# -> MacBook review URL: http://127.0.0.1:8098/<run-id>/<revision>/
```

Publishing copies the artifact directory into the renderer's root
(`~/.local/state/om-chat-feature/`). The renderer is device-owned: publish into
it, never start, restart, or replace it, and never hand-author a revision
`index.html`.

The renderer is a **gallery**: it needs at least one image or it publishes a
page with nothing in it, and `evidence publish` refuses that. So a run whose
claim is entirely CLI-side still captures one dashboard frame — the Alerts table
showing the row your command produced is usually the right one.

Every revision needs an `evidence-manifest.json` beside the frames, in the
`omrx` schema — `capture.screenshots` is a **filename → caption map**, not an
array. A custom shape serves HTTP 200 with an empty gallery: looks published,
reviews as nothing. `evidence publish` validates the shape, confirms every named
file exists, and refuses to print a URL unless the rendered gallery actually
contains `<img` tags. Scaffold one with:

```bash
~/.claude/skills/verify-om/helpers/new-evidence-manifest.sh \
  <run-id> <revision> "<one-line goal>"
```

Then fill in the captions and the `daemonEvidence` facts. Record what you
observed, including anything you could not prove — a manifest that omits the
warning it saw is a manifest nobody can trust twice.

**Publishing is disclosure. Redact before you publish.** The artifact directory
is copied wholesale into the renderer's root, so anything in it is readable by
whoever opens the gallery. The live example is `om watch rotate-token`, whose
JSON carries a working ingest bearer token and a ready-to-run `curl` containing
it; saving that result as evidence publishes a credential. Keep the token in a
shell variable, and if a result file must be kept, replace the secret with a
`REDACTED` string before running `evidence publish`.

**Never hand back an `18097`–`18197` URL.** That range is deliberately not
tunnelled to the MacBook; the operator cannot open it. The review URL on `8098`
is the only link a run returns.

## Cleanup

```bash
agent-browser close            # your session only
control-om down              # by pidfile, never by name
```

`down` kills the recorded pid, then re-checks the port and says so if something
still holds it. **Never** match on process name: `pkill bun` takes out every
other agent's lane, the operator's tooling, and quite possibly their daemon.

If `down` reports the port still held, do not assume it is a neighbour's. Check
before you walk away:

```bash
lsof -nP -iTCP:18101 -sTCP:LISTEN
```

A `bun packages/cli/src/bootstrap.ts run` in the `18097`–`18197` range with
`PPID 1` is your own residue — kill that pid and delete the stale
`.control-om/lane-<port>.pid`. Anything else, leave it alone and take another
slot.

The lane root under `.control-om/home-<port>` survives `down` on purpose: its
sqlite, journals and logs — all under `accounts/guest/` — are readable after
teardown. Delete it when you want a genuinely fresh lane, and **always** delete
it before driving a tree that has moved: a root written by an older `om` is
migrated into the accounts layout on the next boot, which is one more thing
changing underneath the run.

Evidence survives teardown too. It lives under `~/.local/state/om-chat-feature/`,
not in the repo, so the gallery URL keeps working after the lane is gone.
Confirm it: `curl -s http://127.0.0.1:8098/<run-id>/<revision>/ | grep -c '<img'`.

Run cleanup after a **failed** attempt too. A crashed drive still leaves a
daemon holding an agent port and a browser session open.

## Gotchas that cost a run

**A copied `om` binary is killed at launch on Apple Silicon.** `bun build
--compile` signs `packages/cli/dist/om` ad hoc for its own path; `cp` it over
the installed binary and every launch dies with `zsh: killed` (exit 137, no
output), while the copy in `dist/` still runs. `/opt/homebrew/bin/om` is a
symlink into `~/.local/opt/openmarket/<version>/bin/om`, so the copy lands
there. Re-sign in place before restarting anything:

```bash
cp packages/cli/dist/om "$(readlink -f /opt/homebrew/bin/om)"
codesign --force --sign - "$(readlink -f /opt/homebrew/bin/om)"
om service restart
```

The daemon keeps running the old binary until the restart, so a killed CLI
never takes it down. Learned 2026-09-19.


**A fresh lane is a GUEST, and that decides what you can prove.** Boot logs
say so directly (`skipped: guest session`). What a guest still gets is a
machine-minted Data API key, so the market-data verbs really work — `om coins`,
`om exchanges`, `om points` all return live data from `api.openmarket.xyz`. What
it does not get is an LLM credential, so anything routed through a model is
unprovable on the lane: `om chat`, event-watch classification, journal
synthesis, text signals. `om doctor` names it as
`llm: warn — no LLM configured`.

**The model-free path through the fire pipeline is `accept_all`, and it is on
`edit`, not `create`.** A watch created `--inbound` defaults its classifier to
`llm_every_event`, so the first push lands the event and then stalls with
`No LLM credential is configured for event-watch classification` — the watch
lists as `broken`, which reads like a product bug and is not. Switch it:

```bash
control-om om -- watch create probe --inbound --format json
control-om om -- watch edit probe --classifier-mode accept_all --format json
```

`om watch create --classifier-mode ...` fails with `unknown option`. The flag
lives on `watch edit` and `watch backfill` only.

**`om alert` is not a verb.** Alerts and event watches are both `om watch`
today. Repo docs (`AGENTS.md` included) still carry `om alert …` examples in
places; they do not run. Check `control-om om -- --help` rather than trusting
a doc. The dashboard's nav item for them is now **Watches**, though its route is
still `/alerts`.

**The ingest door needs a minted token; the CLI push does not.** An
unauthenticated `POST /ingest/v1/<watch>` is `401 {"error":"unauthorized"}`,
which reads like a broken route. Mint once with
`om watch rotate-token <watch> --yes --format json` — the token is **shown once**
and rotation revokes the previous one. `om event push` goes through the CLI's own
home and needs no token, so use it whenever the HTTP door is not the thing under
test.

**`--type` on `om points` takes API enum values, not chart words.** `OHLCV` and
`OHLCV_AGG` are both rejected by the server (`is not a valid value`); candles are
`TRADE_SIDE_AGNOSTIC_AGG`. The symbol flag is `--raw-symbol`, not `--symbol`.
List the live domains with `control-om om -- enum --format json`.

**`stale · tick Nm ago` in the dashboard header is normal on an idle lane.** The
badge reads the last tick the runner recorded, and a lane with nothing to
evaluate does not tick on the interval. It is not evidence of a wedged daemon;
`/healthz` `last_tick_at` says the same thing without the colour.

**The dashboard's Overview has a `restart` button.** On the lane it restarts the
lane. Pointed at anything else it restarts that — never open the dashboard
against `31337` during a run.

**Do not run `bun run dev --profile playwright` in this repo.** `.env.local`
sets `OM_DEV_PLAYWRIGHT_CHAT_PORT=8098`, which is the device-owned review
renderer's port. That profile will fight the renderer every agent on this
machine publishes evidence through.

**`agent-browser viewport` is not a command.** It is `agent-browser set viewport
<w> <h>`. A screenshot at the wrong size is evidence of the wrong layout.

## Helpers

`helpers/origin-challenge-stub.ts` — the loopback origin the origin-challenge
recipe drives: an RSS feed plus article pages that flip to a Cloudflare-style
challenge when a `mode` file says so, logging every request with a timestamp.
Run it from a scratch directory:
`mkdir -p /tmp/origin-stub && cd /tmp/origin-stub && echo ok > mode && bun
~/.claude/skills/verify-om/helpers/origin-challenge-stub.ts &`. The `403` plus
`cf-mitigated: challenge` pair is load-bearing — a bare `403` is never detected
and the run proves nothing.

`helpers/new-evidence-manifest.sh <run-id> <revision> "<goal>"` — scaffolds
`artifacts/<run-id>/<revision>/evidence-manifest.json` in the omrx schema the
`8098` renderer reads, with branch, commits and a `diffSha256` from the working
tree, and one caption slot per `*.png` already in the directory. Run it from the
repo root after capturing frames, then fill every TODO.

## Comparing against the last verified tree

A maintenance pass asks "what moved since this map was last proven?", and the
answer comes from a TREE diff, not a commit count. This repo's history gets
rewritten — the commit a previous pass verified against can stop being an
ancestor of `HEAD`, at which point `git rev-list --count <old>..HEAD` reports a
number that means nothing (measured: 100, against a real range of 78 from a
different base). `git diff <old-commit>..HEAD -- <paths>` still answers
correctly, because git diffs trees whether or not they share history.

So: record the commit a pass verified, diff against it next time, and check
`git merge-base --is-ancestor <old> HEAD` before quoting any commit count.
Finding a commit with a similar diff elsewhere in the graph is not the same
commit — check the whole tree before treating one as a stand-in.

## Keeping this current

The feature map in `features/` is the maintained source for routes, handles and
recipes, and it goes stale the way any documentation does.
`maintain-verification-skill` is the upkeep pass — run it when a mapped handle
stops resolving, when a new user-facing surface lands, or when a gotcha above
turns out to be fixed.
