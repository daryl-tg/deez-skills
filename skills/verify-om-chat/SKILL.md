---
name: verify-om-chat
description: Use when a change to the OM Chat GUI (openmarket-chat or openmarket-chat-cloud) needs to be driven and proven in the running app — launching a browser lane, exercising a surface the way a user would, capturing screenshots, and publishing an evidence gallery for review.
---

# Verify OM Chat

OM Chat is a React web GUI served at `/rooms/` (this repo) and `/chat/` (the
hosted twin). This skill is the executable half of verification: how to get a
driveable instance up, how to drive it by accessible name, and how to turn what
you saw into evidence someone else can open.

`$om-chat-feature` owns the *policy* — which gates run, when a revision is
invalidated, what the operator must approve. This skill owns the *mechanics*.
When they disagree, policy wins.

Everything here goes through `control-om-chat`, at
`/Users/dboon/github/openmarket-chat/control-om-chat`.

It sits in the repo it drives, but it does **not** version with it: the file is
untracked, excluded via `.git/info/exclude`, and present on no branch. Two
consequences worth knowing before you plan a run. A `git worktree` of the repo
does not have it, so a lane you start from a worktree fails with
`no such file or directory`. And because the script resolves its own repo from
`dirname "$BASH_SOURCE"`, calling it by absolute path serves the **primary
checkout** whatever your cwd is — so you cannot point it at a worktree by
invoking it from there. To drive a specific tree, copy the script into that
tree and run it from the copy:

```bash
cp /Users/dboon/github/openmarket-chat/control-om-chat <worktree>/
cd <worktree> && OM_CHAT_LANE_PORT=<port> ./control-om-chat doctor
```

That matters more than it sounds: the primary checkout is frequently parked on
somebody else's feature branch, so "run the wrapper" and "drive `main`" are not
the same thing.

## Pick a lane before you launch

Two lanes exist and they prove different claims. Choosing the wrong one is the
most common way a run wastes an hour.

| Lane | Proves | Needs | Cost |
|---|---|---|---|
| **Fixture lane** (default) | Rendering, layout, in-app navigation, panel and dialog behavior, a11y names, responsive states | Nothing but this repo | ~10s to boot |
| **Daemon-pair lane** | The wire: real relay, real auth, two identities, messages that actually send | Local parity stack (auth `4001`, relay `3002`) **and** a fresh `bun run build` | Minutes, and the stack is often down |

The fixture lane serves `tools/visual/*fixture.html` from source through vite.
Those fixtures mount the **real** Shell and real components against seeded
state, so what you drive after load is real product code — but the state behind
it is stubbed, and unstubbed session predicates answer **truthy** (see
[Gotchas](#gotchas-that-cost-a-run)). It cannot prove anything that travels the
wire.

Reach for the daemon-pair lane only when the claim is about sending, receiving,
presence, or reconnection. Everything else is the fixture lane.

## Launch

```bash
cd /Users/dboon/github/openmarket-chat

# Ports are ASSIGNED, never discovered. 18097-18197 is the agent range.
# 18097 is the conventional first slot; take the next free one if it is taken.
OM_CHAT_LANE_PORT=18099 ./control-om-chat up
# -> http://127.0.0.1:18099/rooms/
```

`up` binds `127.0.0.1` explicitly, uses `--strictPort`, records a pidfile under
`.control-om-chat/`, and blocks until the shell fixture actually answers. It
refuses to start on a busy port rather than stealing a neighbour's lane.

**Never** bind, target, or stop `8097` (the operator's dev server), `8098` (the
device-owned review renderer), or `31337` (the om daemon). A lane in the
`18097`–`18197` range is deliberately **not** tunnelled to the MacBook, so its
URL is never something you hand back as a review link.

Ready when `control-om-chat up` prints the origin. If it prints a vite error
instead, read `.control-om-chat/lane-<port>.log` — that log carries the React
and vite module errors the browser will otherwise swallow.

Teardown is [Cleanup](#cleanup).

## Doctor

One read-only command, before you drive anything:

```bash
OM_CHAT_LANE_PORT=18099 ./control-om-chat doctor
```

It reports the repo HEAD, whether the lane port is free or already yours,
whether `dist/` was built from this tree, whether `agent-browser` is installed,
and whether the review renderer is answering on `8098`. It exits non-zero when
the instance is not worth driving.

The `dist bundle` line is the one that silently wastes runs. `dist/` is
gitignored, so it never updates from a merge and nothing else says it is stale;
a compiled daemon caches it at boot. **`STALE` is fine for the fixture lane**
(which reads source) and **fatal for the daemon-pair and desktop lanes** — run
`bun run build` first there.

## Drive

Use `agent-browser` through the wrapper (or directly; the wrapper only ensures
it exists). Give the run its own session so you cannot clobber another agent's
browser:

```bash
export AGENT_BROWSER_SESSION=verify-<your-run-id>
agent-browser set viewport 1440 900       # `viewport` is a `set` subcommand
agent-browser open "$(OM_CHAT_LANE_PORT=18099 ./control-om-chat url \
  'tools/visual/shell-fixture.html?view=room&alerts=quiet')"
agent-browser snapshot -i -c
```

**Drive by ARIA role and accessible name, never by coordinates or CSS.** OM
Chat labels its surfaces well and those names are the contract users' screen
readers see:

```bash
agent-browser find role treeitem click --name "CPI print — Aug, 2 mentions, 3 unread"
agent-browser find role button   click --name "Back to #ops"
agent-browser find role button   click --name "Chats" --exact
```

Re-snapshot after anything that changes the page — refs go stale immediately.

Read `features/` for the routes and handles of each surface, and run
`agent-browser skills get core` if you need a command this skill does not show.

For a repo command whose exit code matters:

```bash
./control-om-chat cli -- bun run typecheck
```

## Evidence

Capture the **action and its result**, not just the final screen, and verify a
side effect alongside what is visible. A single after-shot proves the app can
render that state, not that your interaction produced it.

Three observations make a claim stand up, and OM Chat gives all three cheaply:

1. **Route** — `agent-browser get url` (the shell writes a real hash route:
   `#/room/ops` → `#/room/ops/topic/cpi-print-aug`).
2. **Accessible name** — the heading, and any control whose label should follow
   (the composer retargets `Message #ops` → `Message in CPI print — Aug`).
3. **A DOM marker** — `agent-browser eval` against the shell's data attributes
   (`[data-mobile-root]`, `[data-mobile-detail]`, `[data-message-row]`).

Write frames into `artifacts/<run-id>/<revision>/` in the repo, then publish:

```bash
./control-om-chat evidence publish <run-id> <revision>
# -> MacBook review URL: http://127.0.0.1:8098/<run-id>/<revision>/
```

Publishing copies the artifact directory into the renderer's root
(`~/.local/state/om-chat-feature/`). The renderer is device-owned: publish
into it, never start, restart, or replace it, and never hand-author a revision
`index.html`.

Every revision needs an `evidence-manifest.json` beside the frames, in the
`omrx` schema — `capture.screenshots` is a **filename → caption map**, not an
array. A custom shape serves HTTP 200 with an empty gallery: looks published,
reviews as nothing. `evidence publish` validates the shape, confirms every named
file exists, and refuses to print a URL unless the rendered gallery actually
contains `<img` tags. Scaffold one with:

```bash
~/.claude/skills/verify-om-chat/helpers/new-evidence-manifest.sh \
  <run-id> <revision> "<one-line goal>"
```

Then fill in the captions and the `browserEvidence` facts. Record what you
observed, including anything you could not prove — a manifest that omits the
console warning it saw is a manifest nobody can trust twice.

## Cleanup

```bash
agent-browser close                                  # your session only
OM_CHAT_LANE_PORT=18099 ./control-om-chat down       # by pidfile, never by name
```

`down` kills the recorded pid and nothing else. **Never** match on process name:
`pkill vite` takes out the operator's `8097` server and every other session's
lane at once.

If `down` says there is no run-owned lane but the port is still busy, do not
assume it is a neighbour's. Vite re-execs when the dependency graph changes
underneath it — someone syncing the branch, or a dependency install landing
mid-run, is enough — and the new process reparents to PID 1, orphaning the
pidfile. Then `doctor` reports
`BUSY, not ours` about a lane **you** started. Check before you walk away:

```bash
lsof -nP -iTCP:<port> -sTCP:LISTEN
```

A `vite --port <your assigned port> --strictPort --host 127.0.0.1` in the
`18097`–`18197` range with `PPID 1` is your own residue — kill that pid and
delete the stale `.control-om-chat/lane-<port>.pid`. Anything else, leave it
alone and take another port.

Evidence survives teardown. It lives under `~/.local/state/om-chat-feature/`,
not in the repo, so the gallery URL keeps working after the lane is gone.
Confirm it: `curl -s http://127.0.0.1:8098/<run-id>/<revision>/ | grep -c '<img'`.

Run cleanup after a **failed** attempt too. A crashed drive still leaves a vite
process holding an agent port.

## Gotchas that cost a run

**Unstubbed session predicates answer truthy.** The shell fixture wraps its
session in an `autofill` proxy whose fallback (`INERT`) is callable and
truthy. Any predicate the fixture does not spell out therefore returns
"yes" — so blocked, locked, pending, and error states default **on**. This is
why the composer renders read-only under *"This draft is open in another tab"*:
`session.composerLaneOwnedElsewhere` is unstubbed. It is not one view's problem
— `room`, `topic` and `dm` all come up with `textarea.readOnly === true` and the
banner showing. The fixture lane cannot verify typing or sending until that
predicate is spelled out as `false` in `tools/visual/shell-fixture.tsx`.

Check the property, not the appearance: the textarea is `readOnly`, **not**
`disabled`, so it still takes focus and `disabled` reads `false`. Keystrokes are
swallowed silently, and an agent that asserts on `disabled` concludes the
composer works.

The same trap bites methods newly added to a store: when a component starts
calling `session.alerts.stripFeedForRoom(...)` and the fixture's `alertsStub`
does not list it, the surface crashes with `is not a function` and takes the
whole route down. Fixing the stub is part of shipping the feature, not a
separate chore.

**A stale linked `rooms-client` breaks every route at once.** `@openmarket/
rooms-client` may be symlinked to a local `openmarket-internal` checkout whose
`dist/` is behind its `src/`. The symptom is a vite error naming a missing
export (`does not provide an export named ...`) and a blank `#root`. Check with
`bun run rooms-client:status`; fix by rebuilding that package
(`cd ../openmarket-internal/packages/rooms-client && bun run build`). `dist/`
there is gitignored and regenerable.

**`agent-browser viewport` is not a command.** It is `agent-browser set
viewport <w> <h>`. A screenshot at the wrong size is evidence of the wrong
layout. Typing is `type <selector> <text>` — the selector is not optional, and
`type "some text"` treats the text as a selector and fails on it.

**`agent-browser eval` shares one global scope across calls.** A second call
declaring the same name dies with `Identifier 'x' has already been declared`,
and the failure looks like a page problem rather than a shell one. Wrap every
eval in an IIFE and the scope never leaks:

```bash
agent-browser eval '(()=>{const t = document.querySelector("textarea");
  return JSON.stringify({readOnly: t.readOnly});})()'
```

**Not every control in the fixture is wired.** "Search or jump to…" is inert
there. Confirm a control does something before you build a proof on it, and if
it does not, say so rather than photographing a click that did nothing.

## Helpers

`helpers/new-evidence-manifest.sh <run-id> <revision> "<goal>"` — scaffolds
`artifacts/<run-id>/<revision>/evidence-manifest.json` in the omrx schema, with
branch, commits, and a `diffSha256` read from the working tree, and one caption
slot per `*.png` already in the directory. Run it after capturing frames.

## Keeping this current

The feature map in `features/` is the maintained source for routes and handles,
and it goes stale the way any documentation does. `maintain-verification-skill`
is the upkeep pass — run it when a mapped handle stops resolving, when a new
user-facing surface lands, or when a gotcha above turns out to be fixed.
