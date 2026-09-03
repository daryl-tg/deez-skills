---
name: verify-openfloor
description: Use when a change to the OpenFloor mobile app (openmarket-chat-app, the Expo/React Native OpenMarket client) needs to be driven and proven on a real iOS simulator — launching the dev client against Metro, exercising a surface the way a user would, capturing screenshots and accessibility snapshots, and publishing an evidence gallery for review.
---

# Verify OpenFloor

OpenFloor is the Expo/React Native OpenMarket client in
`/Users/dboon/Gitlab/openmarket-chat-app`. Its surface is a **dev-client build
on a booted iOS simulator**, driven through `agent-device`. There is no web
target worth driving: `pnpm run export:smoke` is a build diagnostic, and the web
build deliberately has no durable credential, Rooms, or push persistence.

This skill is the executable half of verification: how to get a driveable app
up, how to drive it by accessible name, and how to turn what you saw into
evidence someone else can open. The `om-mobile-feature` family owns the
*policy* — which gates run, what the operator approves, how a branch lands.
This skill owns the *mechanics*. When they disagree, policy wins.

Everything goes through `control-openfloor`, which lives in the repo it drives
(`/Users/dboon/Gitlab/openmarket-chat-app/control-openfloor`) so it versions
with the app.

## What this lane can and cannot prove

**Production is what the simulator talks to.** Mobile never points at a local
backend — the app is wired to `openmarket.xyz/chat`. That single fact sets the
boundary:

| | |
|---|---|
| **Free** | Reads, navigation, layout, a11y names, theming, empty/error states, screenshots anywhere |
| **Write-safe** | The **Home** server only — and see the warning below |
| **Operator's call** | Posting in any other space; changing any space's roles or permissions, Home included |
| **Out of reach here** | Push delivery, Keychain, background lifecycle, deep links from cold, any SQL migration over a database a previous build created — all device-tier |

> **Home currently has no channels.** As of 2026-09-02 the Servers tab shows
> `HO, Home, 0 channels` and the server screen reads *"This server has no
> visible channels."* So the one write-safe room is not reachable, and
> **sending a message cannot be proven in this lane right now.** Report that as
> a verification delta; do not substitute a production channel for it.

Anything device-tier goes in the run's `verificationDelta`, never quietly
omitted and never described as passing.

## Launch

Two processes must be up: Metro, and the app on a booted simulator.

```bash
cd /Users/dboon/Gitlab/openmarket-chat-app
pnpm start          # Metro on 8081, in the background. Leave it running.
./control-openfloor doctor
./control-openfloor app open
```

`app open` foregrounds the app and returns the shell snapshot. `app reset` does
a true cold start (`simctl terminate`, then relaunch) — use it whenever a recipe
says "from a fresh start", and to prove that something persisted.

**Ports are assigned, never discovered.** `8081` is Metro, this app's own dev
bundler and a singleton per simulator. `8100` is the OpenFloor evidence
renderer. Never bind, target, or stop `8097`, `8098`, `8099` (om-chat's), or
`31337` (the `om` daemon). If you need a second lane for another worktree, give
it its own Metro port *and* its own simulator — one simulator cannot run two
copies of the same bundle id:

```bash
agent-device open <app> --platform ios --device "iPhone 17"     --session a --metro-port 8081
agent-device open <app> --platform ios --device "iPhone 17 Pro" --session b --metro-port 8082
```

Teardown is [Cleanup](#cleanup).

## Doctor

One read-only command, before you drive anything:

```bash
./control-openfloor doctor
```

It reports the working tree, whether Metro is up **and bundling this checkout**,
the booted simulator, whether the app is installed, `agent-device`, and the
renderer. It exits non-zero when the instance is not worth driving.

The `metro` line is the one that silently wastes runs. Another `expo start` from
a different checkout answers `/status` identically; doctor compares the Metro
process's working directory against this repo by inode, so it reports `FOREIGN`
instead of letting you verify someone else's tree.

`renderer down` is advisory — capture evidence anyway, publish when it is up.

## Drive

Drive through the wrapper so every command lands in the same pinned session:

```bash
./control-openfloor device snapshot -i
./control-openfloor device press 'label="Servers"' --settle
./control-openfloor device fill 'label="Search chats"' "ada" --settle
```

**Drive by accessible name, never by coordinates.** OpenFloor labels its
surfaces well, and those names are the contract a screen-reader user gets.
`features/` is the maintained map of the real handles.

Four rules that come straight from this app's shape:

- **Continue from the `--settle` diff.** Refs go stale after every mutation.
  Re-snapshot with `snapshot -i` only when the diff lacks your next target.
- **Never exact-match a label containing a count.** Inbox rows, server rows and
  the Chats tab embed live unread counts that drift between snapshots — this
  session watched `Chats, 1712 unread` become `659`, `657`, then `654` with no
  interaction. Use `find "OpenMarket, 30 channels"` (contains) or press the
  stable part.
- **Names hydrate after first paint.** A cold boot shows the raw handle with an
  avatar initial (`G, geraldlee`); once the space-roles roster warms, the same
  row resolves to its display name (`geraldlee`, `Nicholas`, `ryan`) via
  `resolveMemberName`. Snapshot twice before asserting a name, or assert after
  the roster has warmed.
- **Verify the named thing.** A bare screenshot is not verification. Confirm
  with the settle diff, `wait text "..."`, `find`, `get`, or `is`.

For a repo command whose exit code matters:

```bash
./control-openfloor cli -- pnpm run typecheck
```

## Evidence

Capture the **action and its result**, and verify a side effect alongside what
is visible. A single after-shot proves the app can render that state, not that
your interaction produced it.

Three observations make an OpenFloor claim stand up:

1. **The settle diff** — the before/after accessible names in one payload. This
   is the diffable half and it survives a restyle.
2. **A screenshot** — what a human reads.
   `./control-openfloor device screenshot --out "$PWD/artifacts/<run>/<rev>/01-x.png" --normalize-status-bar`
   (the flag is `--out`, not `--path`; `--normalize-status-bar` makes frames
   comparable.)
3. **A side effect** — for anything that should persist, `app reset` and
   re-navigate. That is a real `simctl terminate`, so surviving it proves the
   value reached disk rather than living in a store.

Write frames into `artifacts/<run-id>/<revision>/` in the repo, scaffold the
manifest, caption every frame, then publish:

```bash
# Paths are relative to this skill's own directory. It resolves to
# ~/.claude/skills/verify-openfloor on Claude and ~/.codex/skills/verify-openfloor
# on Codex — both symlinks to the same hub copy, so the recipe is identical.
helpers/new-evidence-manifest.sh <run-id> <revision> "<one-line goal>"
# fill in every captures[].state and the verificationDelta
./control-openfloor evidence publish <run-id> <revision>
# -> MacBook review URL: http://127.0.0.1:8100/<run-id>/<revision>/
```

`evidence publish` refuses to print a URL unless the manifest parses, every
`captures[].path` names a file that is really there, and every frame has a
caption. A manifest pointing at a missing frame otherwise publishes fine and
reviews as an empty gallery.

Publishing copies into `~/.local/state/om-mobile-feature/`. The renderer is
device-owned: publish into it, never start, restart, or replace it, and never
hand-author a revision `index.html`.

Record what you could **not** prove in `verificationDelta`. A manifest that
omits the path it failed to reach is a manifest nobody can trust twice.

## Cleanup

```bash
agent-device close --session verify-openfloor    # your session only
```

Leave Metro running — it is the operator's, it is a singleton, and doctor's job
is to tell you whether it is yours to use. Never `pkill node` or `pkill expo`:
that takes out the operator's bundler and every other worktree's lane at once.

Restore anything you mutated, and remember not every "local" preference is
local: App theme states outright that it *"travels to your OpenMarket web
session"*. This session changed the accent to prove the lane and put it back;
say so in the delta.

Evidence survives teardown — it lives under `~/.local/state/om-mobile-feature/`,
not in the simulator. Confirm it:

```bash
ls ~/.local/state/om-mobile-feature/<run-id>/<revision>/
```

Run cleanup after a **failed** attempt too. A crashed drive still holds the
device lease, and the next run meets `DEVICE_IN_USE`.

## Gotchas that cost a run

**`open --relaunch` strands you on the dev-client launcher.** This is a dev
client, not Expo Go. `--relaunch` reliably lands on *Development Build /
DEVELOPMENT SERVERS* and stays there. `control-openfloor app` uses a deep link
to `localhost` instead, polls for the app shell, and presses the RECENTLY OPENED
entry if the launcher is still up. Never press the **DEVELOPMENT SERVERS** row:
`pnpm start` runs `--host lan`, so that row advertises a LAN IP
(`http://192.168.100.113:8081`) which times out. The **RECENTLY OPENED** row
carries `http://localhost:8081` and works.

**The launcher is a *stable* screen, so `wait stable` returns on it.** Gate app
readiness on `wait 'label="Primary navigation"'` — an element only the app shell
has — and give it several attempts, because a cold bundle load outlasts a single
wait budget.

**`DEVICE_IN_USE` with an empty session list is a stale lease.** `agent-device
session list` returning `{"sessions": []}` while `open` rejects with
`DEVICE_IN_USE: ... session "X"` means the lease outlived its owner. Reclaim it
with `agent-device close --session X`. Check the session directory's mtime under
`~/.agent-device/sessions/` before assuming it is stale — a live owner is
someone else's run.

**The server channel screen can collapse the accessibility tree.** Pressing a
channel in a large server (OpenMarket, 23 channels) produced *"Detected an
overly complex or slow accessibility tree. Fell back to the private-ax snapshot
backend"* and a 2-node snapshot. While collapsed, **no selector resolves** —
every `press 'label="…"'` fails with `Selector did not match`. Recovery is
`control-openfloor app open` (a deep-link re-entry), not retrying the selector.
DM conversations do **not** show this; their trees are rich and healthy, so
prefer a DM when the claim is about the shared conversation surface, and say so
if you had to.

**Never clear a text field by pressing `delete`.** `press 'label="delete"'`
resolved to the keyboard but dispatched onto the **`v` key** — four presses
turned `Home` into `Homevvvv`. And `fill <target> ""` is rejected outright
(`Expected text to be a non-empty string`). Use a visible clear control, or
`control-openfloor app reset` and start over.

**The first swatch in a swatch row is not addressable.** On App theme, iOS
merges the first option into the parent `[cell]`, whose frame spans the whole
row: `[cell] "Ember"` sits beside `[other] "Blurple"` and `[other] "Honey"`, and
pressing `label="Ember"` taps the row's centre — dead space — leaving the
selection unchanged with no error. Only the non-first swatches are reachable by
label. The same shape applies to PALETTE (`[cell] "Warm graphite"` +
Graphite/Slate/Brass). Reaching the first swatch needs raw coordinates; note it
in the delta when you do.

**`label="Appearance"` is ambiguous.** Two nodes match (`[other]` and
`[button]`) and `press` fails with `AMBIGUOUS_MATCH`. Narrow it:
`press 'role=button label="Appearance"'`. Expect this wherever a settings row
wraps its own label.

**`agent-device back` is not universal here.** The DM screen has a labelled
`Back` button and `back` works. The **server screen's back control has no
accessible label at all** (`@e7 [button]` with an empty name) and `back` fails
with *"in-app back control is not available"*. The reliable path everywhere:
**press the already-selected tab** to return to that tab's root. That matches
the app's parking model — `LayerStackRouter` moves `state.index` and never
truncates routes (see `docs/NAVIGATION.md`).

**Network-backed surfaces fail live.** Server search hit *"OpenMarket
authentication is temporarily unreachable"* and sat on *"Loading OpenMarket
servers…"* indefinitely. Prefer the cached list; if a search is the point of the
proof, `wait text` for the result and report the failure rather than
photographing a spinner.

**A text field's accessible name becomes its content.** `label="Search chats"`
matches only while the field is empty; after typing `ger` the handle is
`label="ger"`. Capture the target before you type.

**Settings routes hide the tab dock.** `label="Primary navigation"` is absent on
the settings tree and App theme, so the selected-tab press is not a way out
there — use the screen's own `Back to settings`, then `back`.

**`screenshot` takes `--out`, not `--path`.**

## Helpers

`helpers/new-evidence-manifest.sh <run-id> <revision> "<goal>"` — scaffolds
`artifacts/<run-id>/<revision>/evidence-manifest.json` in the schema the
OpenFloor renderer reads, with baseline/candidate commits and a `featureDiffHash`
read from the working tree, and one `captures[]` slot per `*.png` already in the
directory. Run it after capturing frames, then replace every `TODO`.

## Keeping this current

`features/` is the maintained source for the routes and handles of each surface,
and it goes stale the way any documentation does — the handles above were read
off a live simulator on 2026-09-02. `maintain-verification-skill` is the upkeep
pass: run it when a mapped handle stops resolving, when a new user-facing surface
lands, or when a gotcha here turns out to be fixed. The Home-server note is the
first thing to re-check.
