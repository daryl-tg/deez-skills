# Building the daemon-embedded `/rooms` GUI (`--hosted`)

Read `../SKILL.md` first for the target table, the tunnel rules, and the
port contract. This file is the flow.

## `--hosted` — daemon `/rooms` at 127.0.0.1:31337

`om upgrade` no longer works for standalone installs. It downloads from
`github.com/openmarket-xyz/openmarket-releases`
(`packages/cli/src/runner/update-check.ts:28`), that repo 404s unauthenticated,
and there is no auth path in the updater: `prodDeps().fetchBytes` / `fetchText`
(`packages/cli/src/runner/upgrade-core.ts:217-226`) are bare `fetch` calls with
no `Authorization` header, and neither module reads `GITHUB_TOKEN` / `GH_TOKEN`.
`gh auth login` does not revive it. Until the updater learns to authenticate or
the repo goes public again, a source build is the upgrade path.

The build itself is one command. The part that is easy to get wrong is the rooms
GUI: it is **not** built from the monorepo, and a plain source build serves the
placeholder shell at `/rooms` (`packages/cli/src/dashboard/rooms-gui.ts:1-32`) —
which looks exactly like the GUI broke. Steps 1, 2 and 6 reproduce locally what
`.github/workflows/release.yml:196-240` does in CI.

### Run the script, not the steps

Everything in this target is one command. It is the same sequence every time, so
it lives in a script rather than in an agent's context:

```bash
~/.claude/skills/om-build/scripts/hosted.sh            # gate, build, install, verify
~/.claude/skills/om-build/scripts/hosted.sh --gate     # gate only -- is there anything to do?
~/.claude/skills/om-build/scripts/hosted.sh --force    # build even when the gate says SKIP
~/.claude/skills/om-build/scripts/hosted.sh --no-gui   # daemon only; /rooms serves the placeholder
```

It exits 0 on success **and** on SKIP, non-zero only on a real failure, and it
restores the GUI stubs on every exit path including Ctrl-C. Read its output and
report; the steps below are the reference for what it does and why, and the thing
to fall back on when it fails.

**Three judgment calls it deliberately does not make.** Each one is a decision
about someone else's repo, so it reports and stops rather than acting:

- **It never pulls.** A `PROTOCOL SKEW` line means the GUI pins a newer
  `rooms-client` than the monorepo has, which breaks sign-in -- pull the monorepo
  and run again. Skew the other way (linked newer) is a benign superset.
- **It never switches branches**, and prints what each repo is on so a build off
  a feature branch is never silently reported as `main`.
- **It never rewrites the launchd plist.** It reads the plist to find the daemon
  binary and adapts: a `dist/om` target means launchd runs the build tree, so it
  stops the service before compiling (the compile output *is* the running
  binary); anything else gets the version-directory install and a symlink flip.

### Hard rules

- **The staged GUI assets are never committed.** They are a working-tree
  overwrite of committed stubs. Restore them in step 6 — including when the
  build fails or the session is interrupted. `extra.json.txt` alone is ~14 MB of
  base64; committing it permanently bloats the repo.
- **Never `cp` over the live binary.** Use `mv` (rename) — atomic on POSIX, and
  the running daemon keeps its old inode until restart. `cp` truncates a file
  another process is executing.
- **Never overwrite a Homebrew install.** If the target's realpath contains
  `/Cellar/openmarket/`, brew owns that file (`detectChannel`,
  `upgrade-core.ts:99`); a hand-placed binary drifts from brew's version
  tracking and gets clobbered on the next `brew upgrade`. Install to the
  standalone path instead, or stop and ask.
- **Smoke-test before installing.** `./packages/cli/dist/om --version` must
  print the version you expect. Never swap a binary you have not run.
- **Never sudo.** A bin dir that needs root is a signal to stop and ask, not to
  escalate.

### 0. Preflight

```bash
cd ~/github/openmarket-internal
git status --short                     # note anything dirty BEFORE staging assets
git log -1 --oneline
grep '"version"' packages/cli/package.json

which -a om                            # every om on PATH; the FIRST one wins
om --version
```

Then find the binary the daemon actually runs — it is not necessarily the one
your shell resolves:

```bash
grep -A2 ProgramArguments ~/Library/LaunchAgents/xyz.openmarket.runner.plist   # macOS
```

Report the delta (installed version → source version) and which path you intend
to replace before building. Two installs on one box is normal and is the usual
cause of "I upgraded and `om --version` didn't change".

**The layout on this box, verified 2026-08-18** — do not assume the older
description of a `~/.local/bin/om` standalone shadowing a Cellar build; it is
the other way round:

- `/opt/homebrew/bin/om` is a **symlink**, not a binary, and it is what launchd
  runs. The standalone installer overwrote brew's link with its own.
- It resolves to `~/.local/opt/openmarket/<version>/bin/om` — one directory per
  installed version. **Run `ls ~/.local/opt/openmarket/` to see which exist**;
  do not trust any list written here, it goes stale every time this skill runs.
- Homebrew's `openmarket` formula was uninstalled 2026-08-18, so brew ships no
  `om` of its own. The symlink's realpath is under `~/.local/opt`, so the
  never-overwrite-brew rule does **not** fire — but re-check with `realpath`,
  since brew still owns the *directory* the symlink lives in and a future
  `brew install openmarket` would fight for that name.
- `~/.local/bin` is **not on PATH here** and contains no `om`. Installing there
  produces a binary neither your shell nor launchd will ever run — the exact
  half-upgraded state this skill warns about.

Resolve the symlink before deciding anything:

```bash
realpath /opt/homebrew/bin/om        # the file that actually runs
```

If that realpath contains `/Cellar/openmarket/`, stop — see the hard rule.

A local-main build usually does **not** change the version string. Say so up
front, or the report reads as a no-op: the honest proof is the asset stamp in
step 7, not `om --version`.

**Say what you are building FROM, before you build it.** This skill compiles the
working tree, not a git ref — uncommitted edits, a feature branch, a detached
HEAD and a linked worktree all get embedded exactly as they sit on disk. Nothing
downstream records that: the `?v=` stamp is a content hash, so it moves, but it
cannot tell anyone *which branch* it came from. A build off someone's half-done
feature branch is indistinguishable from a build off `main` in every artifact
this skill produces.

Capture both repos up front and put it in the opening line and the final report:

```bash
for R in ~/github/openmarket-internal ~/github/openmarket-chat; do
  cd "$R" || continue
  BR=$(git rev-parse --abbrev-ref HEAD)                    # "HEAD" means detached
  [ "$BR" = HEAD ] && BR="detached@$(git rev-parse --short HEAD)"
  D=$(git status --porcelain | wc -l | tr -d ' ')
  WT=$(git rev-parse --git-common-dir)                     # differs from .git in a worktree
  [ "$WT" = .git ] && WT="" || WT=" [linked worktree]"
  UP=$(git rev-parse --abbrev-ref '@{upstream}' 2>/dev/null || echo "no upstream")
  AB=$(git rev-list --left-right --count "$UP"...HEAD 2>/dev/null | awk '{print "behind "$1", ahead "$2}')
  printf '%-22s %s @ %s  %s  dirty=%s%s\n' "$(basename "$R")" "$BR" "$(git rev-parse --short HEAD)" "${AB:-$UP}" "$D" "$WT"
done
```

**State it plainly and early**, e.g.:

> Building from **openmarket-internal** `main @ 2041dae1` (clean) and
> **openmarket-chat** `main @ 20e8862f` (clean).

**Call it out loudly when it is not plain `main`, clean, and level with origin.**
Any of these belongs in the opening line *and* the final report, because the
person reading the report is otherwise entitled to assume it was `main`:

- a branch other than `main` — name it
- `dirty=N` — say how many files, and that uncommitted work is in the binary
- `ahead N` — the build contains commits that are not on origin
- `behind N` — the build is missing commits that are
- a linked worktree — say which path, since two worktrees of one repo can
  disagree and the daemon only gets the one you compiled

The two repos are independent here. Building `main` in the monorepo while the
GUI sits on a feature branch is legitimate and common — but it must be said,
because `om --version` will look like a normal release while `/rooms` serves
something that exists only on that branch.

### 0.5. The skip gate — run this before building anything

Most invocations of this skill have nothing to do. Rebuilding anyway costs a
compile, a binary swap and a daemon restart, and it re-rolls the asset stamp so
the report *looks* like work happened when nothing changed.

Six conditions. **All six clean means stop and report one line.** Any one dirty
means build, and the reason is what you say you are building for.

```bash
OM_BIN=$(realpath /opt/homebrew/bin/om)   # a symlink here — resolve it, or stat reads the link
MONO=~/github/openmarket-internal
GUI=~/github/openmarket-chat

need=0; why=""
flag() { need=1; why="${why:+$why; }$1"; }

health=$(curl -s http://127.0.0.1:31337/healthz)

# 1. the daemon is running the binary that is on disk (not a pre-swap inode)
pid=$(printf '%s' "$health" | sed -n 's/.*"pid":\([0-9]*\).*/\1/p')
if [ -z "$pid" ]; then
  flag "daemon not answering on 31337"
else
  disk=$(stat -f '%i' "$OM_BIN")
  live=$(lsof -p "$pid" 2>/dev/null | awk '$4=="txt" && $NF ~ /bin\/om/ {print $(NF-1); exit}')
  [ "$disk" = "$live" ] || flag "daemon runs inode $live, disk has $disk"
fi

# 2. version pin matches what the daemon reports
src_ver=$(grep -m1 '"version"' "$MONO/packages/cli/package.json" | grep -o '[0-9][0-9.]*')
run_ver=$(printf '%s' "$health" | sed -n 's/.*"version":"\([^"]*\)".*/\1/p')
[ "$src_ver" = "$run_ver" ] || flag "daemon $run_ver, source $src_ver"

# 3. the stamp the daemon serves matches the bundle on disk
built=$(grep -o 'rooms\.js?v=[a-f0-9]*' "$GUI/dist/index.html" 2>/dev/null | head -1)
served=$(curl -s http://127.0.0.1:31337/rooms/ | grep -o 'rooms\.js?v=[a-f0-9]*' | head -1)
{ [ -n "$built" ] && [ "$built" = "$served" ]; } || flag "served $served, built $built"

# 4-6. any source newer than the artifact it produces
newer() { find "$1" -type f -newer "$2" 2>/dev/null | wc -l | tr -d ' '; }
n=$(newer "$GUI/src" "$GUI/dist/index.html");                                    [ "$n" = 0 ] || flag "$n GUI src file(s) newer than dist"
n=$(newer "$MONO/packages/rooms-client/src" "$MONO/packages/rooms-client/dist/version.js"); [ "$n" = 0 ] || flag "$n rooms-client src file(s) newer than dist"
n=$(newer "$MONO/packages/cli/src" "$OM_BIN");                                   [ "$n" = 0 ] || flag "$n packages/cli src file(s) newer than the installed binary"

[ "$need" -eq 0 ] && echo "SKIP — nothing to build" || echo "BUILD — $why"
```

**On `SKIP`, stop.** Do not build, do not stage, do not restart. Report exactly
one line and end:

> Nothing to build — daemon `<version>` (pid `<pid>`) already serving stamp
> `<stamp>`; GUI `<repo>@<sha>` and monorepo `<sha>` both clean and already
> compiled in.

That is the whole report. No tables, no per-step narration, no "checks passed"
list — there were no checks worth reporting because nothing ran.

**Why six and not two.** Version-and-stamp alone is not sufficient, and three
separate runs proved it:

- `rooms-client` `dist` and `src` can both read the same version while the
  source has moved underneath — the constant tracks releases, not content. A
  wire-contract change (`rooms-protocol.ts`) shipped stale this way.
- The GUI's own `src` can be untouched while its **dependency** moved, so the
  bundle is stale even though `find src -newer dist` says zero. Rebuilding
  `rooms-client` alone re-rolled the GUI stamp, which is the proof.
- `packages/cli/src` can move with the GUI untouched — the binary needs a
  rebuild even when `/rooms` would be byte-identical.

**Bias to building.** Every condition is cheap; a compile is not, but shipping a
GUI built against last release's protocol is worse. When a check cannot answer
(daemon down, `dist/` missing, `lsof` returns nothing), that counts as dirty.

**A `git pull` usually forces a build even when content is unchanged**, because
checkout stamps mtimes to now. That is the conservative direction and is fine —
say "source mtimes moved" rather than claiming a code change.

### 1. Build the rooms GUI bundle

Skip steps 1, 2 and 6 entirely on `--no-gui` (`/rooms` will serve the
placeholder; everything else works).

First check the protocol era matches, or the GUI is built against a different
wire contract than the daemon:

```bash
cd ~/github/openmarket-chat && bun run rooms-client:status
```

**Compare the constants, not the package number.** `package.json` says `0.43.0`
on both the registry copy and the monorepo while their constants differ —
published `0.43.0` still carries `VERSION = "0.106.0"`, monorepo source carries
the current release. The package number stopped tracking the protocol era, so
`grep '"version"' package.json` is the wrong field to read. What matters:

```bash
grep VERSION ~/github/openmarket-internal/packages/rooms-client/dist/version.js
```

That must match the version you are about to install. If it does not, or the
status line says `registry copy`, link the GUI to the monorepo source:

```bash
OM_REPO=~/github/openmarket-internal bun run rooms-client:link
```

Stay linked. There is no "unlink once it publishes" milestone while the package
number is frozen — an unlink hands the GUI constants one or more releases behind
the daemon it talks to.

**A linked `rooms-client` does NOT rebuild itself when the monorepo moves.**
`src/version.ts` bumps on every release, so a GUI built against a stale linked
`dist/` silently carries the previous release's `VERSION` / `RUNNER_VERSION`.
Nothing warns you. Whenever the monorepo HEAD moved since the last run, check
and rebuild before building the GUI:

```bash
git -C ~/github/openmarket-internal diff --stat <lastHEAD>..HEAD -- packages/rooms-client/src
cd ~/github/openmarket-internal/packages/rooms-client && bun run build   # exits 2, still emits — see traps
grep VERSION dist/version.js
```

Then build:

```bash
cd ~/github/openmarket-chat
bun install
bun run build
```

`bun install` needs the granular npm token in `~/.npmrc` while
`@openmarket/rooms-client` is private. If the install 404s, do not switch
registries or accounts — use the link flow above, which bypasses npm.

Note the `stamp-asset-versions OK: assets pinned to ?v=<stamp>` line the build
prints. That stamp is what proves the swap landed in step 7.

Verify the five files the embed slots need:

```bash
for f in dist/assets/rooms.js dist/assets/rooms.css dist/index.html dist/sw.js dist/manifest.webmanifest; do
  [ -f "$f" ] && echo "ok $f" || echo "MISSING $f"
done
```

Any `MISSING` means the GUI build failed silently — fix it there, do not
continue with a partial bundle.

### 2. Stage the bundle into the embed slots

Working-tree only. Order matters: the embed is resolved at compile time, so this
must happen before step 3.

```bash
cd ~/github/openmarket-internal
GUI=~/github/openmarket-chat/dist
SLOT=packages/cli/assets/rooms-gui

cp "$GUI/assets/rooms.js"  "$SLOT/rooms.js"
cp "$GUI/assets/rooms.css" "$SLOT/rooms.css"
cp "$GUI/index.html"       "$SLOT/index.html.txt"
bun packages/cli/scripts/pack-rooms-gui-extra.ts "$GUI" "$SLOT/extra.json.txt"
```

`index.html` lands as `index.html.txt` because Bun types `*.html` text imports
as `HTMLBundle`. Everything else in `dist/` (service worker, manifest, icons,
fonts, lazy chunks) packs into the one extras slot — ~137 files today — so new
GUI assets never need a new slot.

Gate on the stub marker being gone:

```bash
grep -l "__OM_ROOMS_GUI_STUB__" "$SLOT/rooms.js" "$SLOT/extra.json.txt" && echo "STILL STUBBED — stop" || echo "staged"
```

While that marker is present, `embeddedRoomsGuiAssets()` returns null and the
daemon serves the placeholder no matter what you compile.

### 3. Compile

```bash
cd ~/github/openmarket-internal
bun install
bun run build          # prebuild builds apps/dashboard, then compiles -> packages/cli/dist/om
```

### 4. Smoke-test the artifact

```bash
ls -la packages/cli/dist/om
./packages/cli/dist/om --version
```

A GUI-embedded binary is noticeably larger than a plain source build (~112 MB
vs ~92 MB). If you want proof rather than inference, boot it in isolation — this
touches neither the live daemon nor `~/.openmarket`:

```bash
OM_HOME=/tmp/om-gui-verify OM_BIND=127.0.0.1:18137 ./packages/cli/dist/om run &   # agent-owned range
sleep 8
curl -s http://127.0.0.1:18137/rooms/ | grep -q OM_ROOMS_GUI_DIR \
  && echo "PLACEHOLDER — the embed did not take" || echo "real GUI embedded"
curl -s http://127.0.0.1:18137/rooms/ | grep -o 'rooms\.js?v=[a-f0-9]*'   # must match step 1's stamp

# Cleanup: kill by PID and PROVE it died. `pkill` returns before the process
# does, and a survivor keeps holding 18137 — the next run's verify then talks
# to the OLD binary and cheerfully prints "real GUI embedded". Seen in the wild.
TESTPID=$(curl -s http://127.0.0.1:18137/healthz | grep -o '"pid":[0-9]*' | cut -d: -f2)
kill $TESTPID 2>/dev/null; sleep 2
kill -0 $TESTPID 2>/dev/null && { kill -9 $TESTPID; sleep 1; }
rm -rf /tmp/om-gui-verify
pgrep -fl "om run" || echo "no strays"          # NOT "dist/om run" — that pattern
lsof -nP -iTCP:18137 -sTCP:LISTEN || echo "18137 free"   # cannot see the installed om
```

The stray check must match `om run`, not `dist/om run`. The narrow pattern only
sees the build-path binary, so it reports "none" while a stray standalone `om`
is still running — a narrower assurance than it sounds like.

### 5. Install and restart

Install a **new version directory** and repoint the symlink. This matches the
standalone installer's own layout, overwrites nothing, and leaves the running
daemon's inode alone until the restart:

```bash
VER=$(./packages/cli/dist/om --version)
mkdir -p ~/.local/opt/openmarket/"$VER"/bin
mv packages/cli/dist/om ~/.local/opt/openmarket/"$VER"/bin/om
chmod +x ~/.local/opt/openmarket/"$VER"/bin/om
ln -sfn ~/.local/opt/openmarket/"$VER"/bin/om /opt/homebrew/bin/om
om service restart
om --version && om service status
```

`/opt/homebrew/bin` is user-writable here, so this never needs sudo; if it ever
does, stop and ask. `mv` across filesystems is not atomic — source and
destination are both under `$HOME`, so this is a rename. The daemon must be
restarted explicitly: a new binary with a still-running old daemon is the
half-upgraded state that reads as a failed upgrade.

Rollback is one command **only when a previous version directory still
exists**:

```bash
ls ~/.local/opt/openmarket/                     # what is actually available
ln -sfn ~/.local/opt/openmarket/<previous-version>/bin/om /opt/homebrew/bin/om
om service restart
```

**Check before you promise a rollback**, and note the asymmetry that trips this:

- A build whose version **differs** from the installed one creates a *new*
  directory, so the outgoing binary survives and rollback is a symlink flip.
- A build at the **same version** — the common case for local work — overwrites
  `<version>/bin/om` in place. The outgoing binary is gone, and the nearest
  rollback target is whatever *older* version directory still exists, not the
  build you just replaced. Rolling back then also reverts the daemon version,
  which may not be what was wanted.

So a same-version rebuild is effectively irreversible unless you copy the
outgoing binary aside first. If that matters for a given run, do it before the
`mv` and say so in the report.

### 6. Restore the stubs — always

```bash
cd ~/github/openmarket-internal
git checkout packages/cli/assets/rooms-gui/
rm -f packages/cli/.*.bun-build
git status --short          # must match what step 0 recorded
```

`bun build --compile` leaves a `packages/cli/.<hash>-00000000.bun-build` temp
file that is not in `.gitignore`, so it shows up as untracked and rides along in
any `git add -A`.

### 7. Verify and report

```bash
om --version
om service status
curl -s http://127.0.0.1:31337/healthz | head -c 200      # the DAEMON's version, not the CLI's
curl -s http://127.0.0.1:31337/rooms/ | grep -q OM_ROOMS_GUI_DIR \
  && echo "live daemon serving PLACEHOLDER" || echo "live daemon serving real GUI"
curl -s http://127.0.0.1:31337/rooms/ | grep -o 'rooms\.js?v=[a-f0-9]*'
```

Then confirm the tunnel side — the GUI is the entire point of this target, and
31337 is forwarded:

```bash
lsof -nP -iTCP:31337 -sTCP:LISTEN    # 127.0.0.1:31337 — reachable through -L
```

Hand over `http://localhost:31337/rooms#/` for the MacBook. If Ryan gets
connection refused there while every curl above passes, the tunnel is down or
was started without the `-L 31337` line — a tunnel symptom, not a build
regression.

`/healthz` is the authoritative version check: `om --version` reports the binary
your shell resolved, which can differ from the one the supervisor is running.
(There is no `om system status` CLI verb — `system_status` is an MCP tool name.)
The served `?v=` stamp is the authoritative *GUI* check, and the only one that
moves when the version does not.

Report: **the branch and sha each repo was built from** (flagged if not clean
`main` level with origin, or a linked worktree), version before → after, the
asset stamp, which binary path was replaced, whether the GUI is embedded or
placeholder, daemon restart result, worktree state, the MacBook URL
(`http://localhost:31337/rooms#/`), and anything left for Ryan (a shadowed `om`
still first on PATH, a skipped GUI, a failed restart, a tunnel that needs
restarting).

Also report **any daemon error line seen after the restart, and whether it
predates this build.** `om service status` shows the most recent error even
after the daemon recovered from it, so the status line alone cannot tell a
regression from a pre-existing condition. Check the log's history before
attributing anything to the swap:

```bash
grep -c "<the error text>" ~/.openmarket/runner.log     # total ever
grep "<the error text>" ~/.openmarket/runner.log | head -1   # first occurrence
```

A count that stops growing after the restart means the new version FIXED it —
worth reporting as such.

**When that grep returns zero, the error is not absent — it is stored, not
logged.** `Last error` is a persisted field on the runner's state, and
`runner.log` rotates (`runner.log.1`, `.2`), so a real, long-standing error can
appear in `om service status` with no trace in any log. Date the underlying
artifact instead:

```bash
ls -la ~/.openmarket/scripts/<script-id>.sh     # mtime older than this build = pre-existing
grep -rl "<script-id>" ~/.openmarket/alerts/    # which alert owns it
```

A script whose mtime predates the build is a pre-existing authoring defect, not
a regression from the swap — report it that way, and name the owning alert.

### Traps (`--hosted`)

| Symptom | Cause | Fix |
|---|---|---|
| `om --version` unchanged after install | either a different `om` is first on PATH, or local main simply never bumped the version | `which -a om`; then confirm via the `?v=` stamp, not the version |
| Ran the whole build and the stamp came out identical | nothing had changed; the skip gate (step 0.5) was not run | run it first — six conditions, all clean means stop and report one line |
| Skip gate says BUILD right after a `git pull`, with no code change | checkout rewrites mtimes to now | expected and conservative; say "source mtimes moved", not "code changed" |
| `/rooms` shows an install-instructions page | stubs were compiled in | redo steps 1-3; check the stub marker gate in step 2 |
| Daemon still on the old version | binary swapped, daemon not restarted | `om service restart` |
| `bun install` 404s in openmarket-chat | `@openmarket/rooms-client` is private on npm | link from the monorepo (`rooms-client:link`), never a different registry |
| GUI builds but behaves oddly against the daemon | rooms-client era mismatch | compare `dist/version.js` constants in step 1 — NOT the package number; link to source |
| GUI carries the previous release's version constants | linked `rooms-client` `dist/` is stale; it does not rebuild when the monorepo moves | rebuild `packages/rooms-client` before the GUI build (step 1) |
| `bun run build` in `rooms-client` exits 2 with `TS2835` | three extensionless relative imports in `src/shared/` (`attention.ts:18`, `read-state.ts:16,17`); `tsc` emits anyway | expected today — confirm `dist/` is fresh and continue |
| Several `om` processes in Activity Monitor | each Claude Code session spawns two `om mcp serve --stdio` children (one `--catalog operator`); they outlive daemon restarts | `ps -o ppid=` — parented by a `claude` PID means not a leak; only PPID 1 is a daemon |
| `Last error: ... You're reading too fast` after restart | the librarian scans rooms in a burst on startup and trips a read rate limit | pre-existing since 2026-08-09, self-resolves in ~5s; confirm `errors=[]` on the next `[schedule]` line before reporting it |
| Huge diff / 14 MB file in `git status` | staged GUI assets not restored | `git checkout packages/cli/assets/rooms-gui/` |
| Every curl passes on the mini but `/rooms` will not open on the MacBook | tunnel down, or started without `-L 31337:127.0.0.1:31337` | not a build failure — see *Remote viewing*; report the tunnel line Ryan needs |
| `OM_ROOMS_GUI_DIR` set but the daemon ignores it | the launchd plist has no `EnvironmentVariables` key, so the supervised daemon never sees your shell's env; and the watch-and-re-read path is source-only (`setRoomsGuiHotReload(isDevExecPath())`, `rooms-routes.ts:95`) | it is a hand-run-daemon tool, not a shortcut around the embed — do the compile |
| `cannot upgrade: process.execPath is ...` from `om upgrade` | you ran the source entrypoint, not a compiled binary | expected — that guard is `upgrade-core.ts:424` |

### When to stop and hand over the runbook

This skill is tuned to one machine. Other people run these repos with different
paths, a different npm identity, no linked `rooms-client`, or no daemon at all.

**Bail out instead of debugging when any of these is true:**

- Two attempts at the same step have failed.
- The failure is not in the Traps table and is not obviously a typo.
- The environment differs from what step 0 assumes — no `~/.local/bin/om`, no
  launchd plist, repos somewhere else, a Cellar install as the only `om`.
- Anything needs a credential you do not have (the private `@openmarket` scope).

Do not keep probing. Print the runbook below, say which step failed and what the
error was, and stop. A person with the right access finishes it in ten minutes;
an agent guessing at it burns an hour and can leave a half-installed binary.

### The manual runbook — build and run the latest daemon from source

Hand this over verbatim. It assumes nothing this skill set up.

**What you need first**

- `bun` on PATH (`bun --version`).
- Both repos cloned. They are separate — the GUI is **not** in the monorepo:
  - monorepo (daemon + CLI + `rooms-client`): `openmarket-internal`
  - rooms GUI: `openmarket-chat`
- Write access to wherever `om` is installed. Never `sudo`.

If you do not know where the repos are:

```bash
find ~ -maxdepth 4 -type d -name openmarket-internal 2>/dev/null
find ~ -maxdepth 4 -type d -name openmarket-chat 2>/dev/null
```

**Set the paths once. Every step below uses them.**

```bash
export MONO=~/Documents/GitLab/openmarket-internal   # <- yours may differ
export GUI=~/Documents/GitLab/openmarket-chat
export OM_BIN="$(command -v om || echo ~/.local/bin/om)"
echo "$MONO"; echo "$GUI"; echo "$OM_BIN"
```

> If `$OM_BIN` resolves inside `/Cellar/openmarket/`, **stop.** Homebrew owns
> that file and a hand-placed binary gets clobbered on the next `brew upgrade`.
> Install to `~/.local/bin/om` instead and make sure it comes first on PATH.

**1. Get both repos current**

```bash
git -C "$MONO" status --short && git -C "$MONO" pull --ff-only
git -C "$GUI"  status --short && git -C "$GUI"  pull --ff-only
```

Commit or stash anything the status lines show before pulling.

**2. Point the GUI at the monorepo's `rooms-client`, and rebuild it**

`@openmarket/rooms-client` is private on npm. If you cannot install it, link it
from the monorepo instead — that bypasses the registry entirely:

```bash
cd "$GUI" && OM_REPO="$MONO" bun run rooms-client:link
bun run rooms-client:status          # expect: LINKED -> .../packages/rooms-client
```

A linked `rooms-client` does **not** rebuild itself when the monorepo moves, so
rebuild it by hand every time:

```bash
cd "$MONO/packages/rooms-client" && bun run build
grep VERSION dist/version.js         # must match the version you are installing
```

**3. Build the GUI bundle**

```bash
cd "$GUI"
bun install     # skip if it 404s on @openmarket/rooms-client — the link covers it
bun run build
```

Note the `assets pinned to ?v=<stamp>` line. That stamp is your proof later.
Then confirm all five embed inputs exist — a missing one means the build failed
quietly and you must not continue:

```bash
for f in dist/assets/rooms.js dist/assets/rooms.css dist/index.html dist/sw.js dist/manifest.webmanifest; do
  [ -f "$f" ] && echo "ok $f" || echo "MISSING $f"
done
```

**4. Stage the GUI into the binary's embed slots** (working tree only — never commit these)

```bash
cd "$MONO"
SLOT=packages/cli/assets/rooms-gui
cp "$GUI/dist/assets/rooms.js"  "$SLOT/rooms.js"
cp "$GUI/dist/assets/rooms.css" "$SLOT/rooms.css"
cp "$GUI/dist/index.html"       "$SLOT/index.html.txt"
bun packages/cli/scripts/pack-rooms-gui-extra.ts "$GUI/dist" "$SLOT/extra.json.txt"

grep -l "__OM_ROOMS_GUI_STUB__" "$SLOT/rooms.js" "$SLOT/extra.json.txt" \
  && echo "STILL STUBBED — stop" || echo "staged"
```

Skipping this step is the single most common mistake: the build succeeds and
`/rooms` serves an install-instructions page, which looks exactly like the GUI
broke.

**5. Compile**

```bash
cd "$MONO" && bun install && bun run build
ls -la packages/cli/dist/om && ./packages/cli/dist/om --version
```

**6. Install and restart**

```bash
mv packages/cli/dist/om "$OM_BIN"     # mv, never cp — cp truncates a running binary
om service restart
```

**7. Verify — the served stamp, not the version**

```bash
curl -s http://127.0.0.1:31337/healthz | head -c 120
curl -s http://127.0.0.1:31337/rooms/ | grep -o 'rooms\.js?v=[a-f0-9]*'
```

The stamp must equal step 3's. A local build often does **not** change
`om --version`, so the version proves nothing; the stamp is the real check.
If `/rooms` shows install instructions, step 4 did not take.

**8. Put the stubs back — always, including after a failure**

```bash
cd "$MONO"
git checkout packages/cli/assets/rooms-gui/
rm -f packages/cli/.*.bun-build
git status --short                    # must be clean
```

`extra.json.txt` alone is ~14 MB of base64. Committing it permanently bloats the
repo, and `git add -A` will happily sweep it up.

**If it still does not work**, report: which step, the exact error, `om --version`,
the served stamp, and whether `git status` is clean in both repos.

### The real fix (`--hosted` only)

This target is a workaround. The durable repair is teaching the updater to
authenticate: an `OM_GITHUB_TOKEN` → `Authorization: Bearer` header in the two
`prodDeps` fetchers plus `fetchLatestVersion`, and swapping the
latest-release redirect probe for the REST API (the redirect trick only resolves
on public repos). Mention it when this target runs more than once.

---

