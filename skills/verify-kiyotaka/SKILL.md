---
name: verify-kiyotaka
description: Use when a change to the OpenMarket chart frontend (kiyotaka-frontend) needs to be driven and proven in the running app — starting a dev-server lane, exercising a chart surface the way a user would, reading engine state, and capturing screenshot + accessibility evidence someone else can open.
---

# Verify kiyotaka-frontend

The OpenMarket chart browser UI: Vue 3 + Pinia + Quasar served at `/chart/`,
with a WebGL chart engine (TitanCharts) and every data-intensive path in a Web
Worker. This skill is the executable half of verification: how to get a
driveable instance up, how to drive it by accessible name and engine state, and
how to turn what you saw into evidence.

Everything goes through `control-kiyotaka`, which lives in the repo it drives
(`/Users/dboon/Gitlab/kiyotaka-frontend/control-kiyotaka`) so it versions with
the app. It is operator tooling, not app source: it is excluded via
`.git/info/exclude`, so a fresh clone will not have it — regenerate it with
`create-verification-skill` rather than committing it.

## Which skill is this

Four things drive this app. Pick deliberately.

| Reach for | When |
|---|---|
| **this skill** | Prove a user-facing change works: navigate, click, assert rendered + engine state, capture evidence |
| `verify-chart-fix` | A bug fix needs a RED→GREEN gate with no perf regression (perf-sentinel harness, exit-code gated) |
| `headless-probe` | A one-off question answerable by a short Playwright script; no evidence needed |
| `docs-screenshot` | The output is a user-guide PNG, not a proof (`qa/docs-shots` engine, needs a real logged-in session) |

## Pick a lane before you launch

| Lane | Proves | Needs |
|---|---|---|
| **Guest lane** (default) | Chart boot, candles, indicators, symbol search, intervals, layout, rendering, a11y names, responsive states | The lane and v2 gateway reachability. **Nothing else** |
| **Authed lane** | Workspaces, saved layouts, alerts, the DB-backed indicator catalog, Plus-gated surfaces (Replay), marketplace | The operator's local stack (`:3000` orange BFF, `:4001` auth) **and** a login |

The guest lane draws real candles with the backend down, because candles ride
the v2 gateway websocket directly from the worker, not the `/api` proxy. Do not
start the operator's stack to prove something the guest lane already proves.

Guest costs you: a `Guest Mode` badge, an indicator cap (`Indicators 2/3`),
Replay reading `Market Replay is a Plus feature`, and no persistence.

## Launch

```bash
cd /Users/dboon/Gitlab/kiyotaka-frontend
./control-kiyotaka up                       # default port 18097
KIYO_LANE_PORT=18099 ./control-kiyotaka up  # take another slot if 18097 is busy
# -> http://127.0.0.1:18097/chart/
```

`up` binds `127.0.0.1` explicitly with `--strictPort`, records a pidfile under
`.control-kiyotaka/`, and blocks until `/chart/` answers. It refuses a port held
by another checkout rather than stealing a neighbour's lane.

Ports are **assigned**: `18097`–`18197` is the agent range and is deliberately
not tunnelled, so a lane URL is never a review link. Never bind, target, or stop
`8097`, `8098`, or `31337` — and treat `8080` the same way, because that is this
repo's documented dev port and the operator's own server.

**A first launch after a dependency change reinstalls `node_modules` and takes
minutes.** That is `pnpm`, not a hang; watch `.control-kiyotaka/lane-<port>.log`.

Teardown is [Cleanup](#cleanup).

## Doctor

One read-only command, before you drive anything:

```bash
./control-kiyotaka doctor
```

It reports the working tree, whether the lane is yours or foreign, whether the
tree actually compiles on demand, the chart-schema seam, backend availability,
v2 gateway reachability, and the harness. It exits non-zero when the instance is
not worth driving.

**The `chart-schema` line is the one that silently burns a run.** `vite.config.ts`
aliases `@orangecharts/chart-schema` to the *sibling* `orange-shared` checkout's
source in dev only, bypassing `node_modules`. A sibling behind this repo's pin
serves a stale `INDICATOR_TYPES` table; a worker indicator control reads a
missing key at module scope, `worker-impl` never evaluates, `WorkerManager` parks
the worker after three attempts — and because the worker owns every websocket,
the only visible symptom is `v2 streaming websocket connection failed` and an
empty chart. Nothing in that error names chart-schema. Doctor compares the two
versions so you never diagnose it from the socket up:

```
chart-schema MISMATCH pinned=0.1.5 sibling=0.1.2
Fix: cd ../orange-shared && git checkout main && git pull --rebase
```

## Drive

Drive through the wrapper — it pins the session and passes the software-GL args
the WebGL canvas needs:

```bash
./control-kiyotaka browser set viewport 1440 900
./control-kiyotaka browser open "$(./control-kiyotaka url)"
./control-kiyotaka browser snapshot -i -c
```

**Set the viewport before you assert layout.** The app has a real mobile shell
and a `Best on Desktop` gate; a screenshot at the wrong size is evidence of the
wrong layout.

**Wait on engine state, never a timer.** The chart answers before it has data:

```bash
./control-kiyotaka browser eval \
  "(()=>{const t=window.tc?.[0];return (t?.metadata?.[0]?.rawData?.length ?? 0)>50})()"
```

Poll that until `true` (a cold boot with a re-optimizing vite can take ~60s).
`window.tc[0].metadata` is the overlay array; `[0].rawData` is candles.

**Drive by ARIA role and accessible name.** The chrome is labelled well:

```bash
./control-kiyotaka browser find role button click --name "Indicators" --exact
./control-kiyotaka browser find role button click --name "BINANCE.F BTCUSDT"
./control-kiyotaka browser find role button click --name "1m"
```

Re-snapshot after anything that changes the page — refs go stale immediately.
`features/` carries the handles per surface. Run `agent-browser skills get core`
for a command this skill does not show.

For a repo command whose exit code matters:

```bash
./control-kiyotaka cli -- pnpm run typecheck
```

## Evidence

Capture the **action and its result**, not just the final screen, and verify a
side effect alongside what is visible. A single after-shot proves the app can
render that state, not that your interaction produced it.

Three observations make a chart claim stand up:

1. **Engine state** — `window.tc[0].metadata` (overlay count, `rawData.length`,
   `settings.ovType`). This is the side effect a screenshot cannot show.
2. **Accessible name** — the heading or control whose label should have changed.
3. **A pixel frame** — the WebGL canvas is invisible to the a11y tree, so a
   screenshot is the only proof the chart actually drew.

Write frames into `artifacts/<run-id>/<revision>/` in the repo (gitignored),
alongside an `evidence-manifest.json`, then validate:

```bash
helpers/new-evidence-manifest.sh <run-id> <revision> "<one-line goal>"
./control-kiyotaka evidence check <run-id> <revision>
```

`evidence check` fails when `captures[]` is empty, names a missing file, or omits
a caption — the three ways a manifest reviews as nothing. There is **no publish
step on this seat**: the renderer on `8098` belongs to OM Chat and reads a
filesystem this machine is not on. Evidence stays local; hand back the artifact
path and say what each frame shows. Never hand back an `18097`–`18197` URL.

Record what you could not prove, too. A manifest that omits the console error it
saw is a manifest nobody can trust twice.

## Cleanup

```bash
./control-kiyotaka down          # by pidfile, never by name
agent-browser close --session verify-kiyotaka
```

**Never `pkill vite`** — it takes out the operator's `8080` server and every
other agent's lane at once. `down` kills the pids it recorded, then sweeps a
survivor **only** once it has confirmed that process's working directory is this
repo and the port is inside the agent range; outside that range it prints the pid
and leaves the kill to you. Two things make the sweep necessary: `pnpm exec` is a
wrapper whose child is the process that actually binds, and vite re-execs when
the dependency graph changes underneath it, reparenting to PID 1 and orphaning
the pidfile.

A lane you started by hand rather than through `up` has no pidfile at all, so
`down` reports `no run-owned lane` and then sweeps the residue. Confirm before
walking away:

```bash
lsof -nP -iTCP:18097 -sTCP:LISTEN
```

Evidence survives teardown; it is on disk in the repo. Run cleanup after a
**failed** attempt too — a crashed drive still leaves a vite holding a port.

## Gotchas that cost a run

**`pnpm run dev -- --port N` drops the args.** Under pnpm 12 vite receives a
literal `--`, ignores the rest, and falls back to `VITE_PORT` — silently binding
**8080**, the operator's port, while you believe you are on your own lane. Only
`pnpm exec vite --port N` passes them. `control-kiyotaka up` does this for you;
never hand-roll the launch.

**The guest signup modal eats the first click, and it comes back.** A guest boot
raises *"See what moves price. / Join for free"* over the chart. Dismiss it with
`find role button click --name "Close"` **immediately before each capture**, not
once at the start — it re-raises, and a frame shot after it returns is a
photograph of the modal. Assert what is on top before you shoot:
`eval "document.querySelectorAll('[role=dialog]').length"`.

**A dialog left open by an earlier drive photographs itself.** Nothing warns you:
the engine read still passes, the a11y snapshot still returns, and the PNG shows
last step's dialog over the chart you meant to capture. Check the dialog count
and the visible text before every screenshot, and open the PNG afterwards.

**Drawing tools have no accessible names.** Every left-toolbar tool snapshots as
`button "More tools"`. Do not drive them by name — use `<ToolGlyph>`'s owning
component or a `data-testid`, and say so rather than photographing a click that
did nothing.

**Ghost-ids are not a reliable handle.** A guest boot logs
`[ghost-id-audit] 11 expected ghost-id(s) NOT registered` for the whole ticker
bar (`tb-symbol-button`, `tb-interval-selector`, …). Prefer ARIA names.

**Assert on rendered or engine state, not console silence.** The app emits benign
errors: a `401` as guest, and with `:3000` down a `[refresh-token] 502` plus
`http proxy error: /api/v1/... ECONNREFUSED`. Match the specific signature of the
bug instead.

**Headless WebGL needs software GL.** Without
`--use-angle=swiftshader --enable-unsafe-swiftshader` the canvas is blank in
every frame while every non-visual assertion still passes. The wrapper passes
them; `agent-browser` called directly does not.

**A clean exit is not proof.** A blank chart, the wrong interval, and guest
chrome all screenshot successfully. Open the PNG.

## When the chart itself misbehaves

Do not patch fetch/cache/pan logic from code inspection. Collect the in-app dump
while reproducing:

```bash
./control-kiyotaka browser eval "window.__enableKiyoLazyLoadDebug()"
# reproduce
./control-kiyotaka browser eval "JSON.stringify(window.__dumpKiyoLazyLoadDebug())"
```

It says whether the frontend did not ask, the worker did not answer, the result
was superseded, the adapter rejected it, or the main thread was blocked. The
runbook is `src/docs/debugging-diagnostics.md`; the build-free probe with
`__qa.profile` / `__qa.runScenario` is `qa/chart-load-probe.js`.

## Helpers

`helpers/new-evidence-manifest.sh <run-id> <revision> "<goal>"` — scaffolds
`artifacts/<run-id>/<revision>/evidence-manifest.json` with the branch, HEAD, and
one caption slot per `*.png` already in the directory. Run it after capturing
frames, fill in the captions, then `evidence check`.

## Where this lives, and how it stays tracked

Two halves, tracked in opposite ways on purpose.

**This skill is tracked in git.** It lives in the skills hub
(`/Users/dboon/Github/deez-skills/skills/verify-kiyotaka`) and reaches
`~/.claude/skills/verify-kiyotaka` as a symlink, exactly like `verify-om-chat`
and `verify-openfloor`. Edit it through either path — they are the same files.
Never copy it into `~/.claude/skills` as a real directory: that is how a feature
map ends up with no history, no diffs, and no way to reach another machine.

**`control-kiyotaka` is deliberately NOT tracked.** It sits at the root of
kiyotaka-frontend, hidden via `.git/info/exclude`, because AGENTS.md keeps that
repo's root to a fixed set of files and this is operator tooling rather than app
source. A fresh clone or a new worktree will not have it. When it is missing,
regenerate it with `create-verification-skill` — do not add it to a commit.

## Keeping this current

`features/` is the maintained source for routes and handles, and it goes stale
the way any documentation does. `maintain-verification-skill` is the upkeep pass —
run it when a mapped handle stops resolving, when a new user-facing surface
lands, or when a gotcha above turns out to be fixed.

**Every maintain pass ends pushed.** A correction proven live and left sitting in
a dirty working tree is a correction the next session on another machine will not
have, so it will rediscover the same drift the hard way. Land it:

```bash
cd /Users/dboon/Github/deez-skills
git checkout -b skills/verify-kiyotaka-<what-changed> origin/main
git add skills/verify-kiyotaka
git commit -m "skills(verify-kiyotaka): <what the live pass proved>"
git push -u origin HEAD
```

Branch off `origin/main`, stage **only** `skills/verify-kiyotaka`, and leave any
unrelated modified skill in the tree alone — the hub usually has another skill
mid-edit, and sweeping it into this commit is how someone else's WIP gets
published. If a branch switch is blocked by those files, stash exactly them by
path and restore them afterwards.

A pass that found nothing worth shipping pushes nothing: say `clean` and stop.
