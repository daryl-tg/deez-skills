---
name: om-build
description: "Build an OM Chat GUI from source and put it in front of the operator: the daemon-embedded /rooms GUI, or the hosted /chat/ cloud fork. Covers both targets and the swap onto the live install. Trigger: om-build [--hosted|--cloud] [--no-gui]"
disable-model-invocation: true
---

# om-build — build an OM Chat GUI from source

Two different products live behind this skill. Pick the target before doing
anything; they share no build, no artifact shape, and no verification.

| Flag | Source repo | Artifact | Where it shows up | Touches the `om` binary |
|---|---|---|---|---|
| `--hosted` (default) | `openmarket-chat` | `assets/rooms.js` + `rooms.css` + `index.html`, embedded into `om` | `http://127.0.0.1:31337/rooms#/` | yes — recompiles and swaps it |
| `--cloud` | `openmarket-chat-cloud` | fingerprinted `assets/chat-<hash>.js` at base `/chat/` | a local server you start, at `/chat/` | never |

The names read backwards if you assume "hosted" means the SaaS:
`--hosted` is the daemon **hosting** the GUI at `/rooms`; `--cloud` is the
`/chat/` fork. No flag means `--hosted`.

**Never mix them in one run.** `--cloud` never writes the `om` binary, never
runs `om service restart`, and never stages anything into the monorepo.
`--hosted` never touches the cloud repo. `--no-gui` means nothing under
`--cloud`.

**Announce at start:** "Using om-build to build and install om from source"
(`--hosted`) or "Using om-build to build and serve the cloud /chat/ fork"
(`--cloud`).

If either fork's copy of a file in `tools/parity-manifest.json` was edited,
run `bun tools/sync-shared.ts --diff` before building. It is the only
cross-fork alarm that exists; both forks can be green while drifting.

---

## Remote viewing — every rig is reached through the SSH tunnel

This skill runs on `dboons-mac-mini`, and nothing it starts is looked at on
that box. The operator views it from the MacBook over an SSH tunnel, so a rig that is
demonstrably serving on the mini can still be invisible — because it took an
unforwarded port, or bound the wrong loopback. Neither failure has a local
symptom: every `curl` in this skill still passes.

The tunnel, run from the MacBook:

```bash
ssh -N \
  -L 4178:127.0.0.1:4178 \
  -L 13137:127.0.0.1:13137 \
  -L 8097:127.0.0.1:8097 \
  -L 8098:127.0.0.1:8098 \
  -L 31337:127.0.0.1:31337 \
  dboon@dboons-mac-mini
```

Ports are **reserved, not chosen**. The authoritative table is `## Reserved
ports` in `~/.claude/CLAUDE.md`; the rows this skill touches:

| Port | Owner / rig | Rule here |
|---|---|---|
| 31337 | the `om` daemon — `--hosted` `/rooms` | never bind it yourself; the daemon owns it, `om service restart` is the only handle |
| 8097 | the operator's local dev server — `--cloud` rig B | operator-owned; preflight, never kill an existing process, never bind from an agent worktree |
| 8098 | device-owned review renderer (singleton) | **hands off** — never start, restart, stop, or replace it. Not an om-build rig |
| 4178 | `--cloud` rig A, `vite preview` | run-owned; stop what you started |
| 13137 | `--cloud` rig C, docker gateway parity | run-owned; stop what you started |
| 18097–18197 | agent-owned test servers | deliberately **not** tunneled — never hand one of these to the operator as a URL |

Two rules follow from the `-L <port>:127.0.0.1:<port>` form, and neither failure
has a local symptom:

- **Only forwarded ports are reachable.** A rig on any other port is a rig the operator
  cannot open. Never pick a port because it happens to be free — take the one
  assigned above, or say plainly in the report that the tunnel needs a new `-L`
  line. The `18097`–`18197` test range is excluded on purpose: those servers are
  agent-internal and are never review surfaces.
- **Bind 127.0.0.1.** The forward's far side connects to IPv4 loopback on the
  mini. A server bound to `[::1]` only is up, listening, and answers `localhost`
  on the mini — while the MacBook gets connection refused. Pass
  `--host 127.0.0.1` explicitly rather than trusting a framework default.
  (`0.0.0.0` / `*` also works, since it includes IPv4 loopback; `[::1]`-only is
  the one that breaks.)

Before handing over any URL, confirm the binding — this is the check that
separates "serving" from "reachable":

```bash
lsof -nP -iTCP:<port> -sTCP:LISTEN    # want 127.0.0.1:<port>; `[::1]:<port>` alone is broken
```

The forward is symmetric, so the URL to hand over is the same number:
`http://localhost:<port>/...` on the MacBook.

Preflight the port before starting a rig. A listener left from an earlier
session either trips `--strictPort` or, worse, keeps answering — and the operator
reviews the *previous* build believing it is this one. Kill only a process this
run started; on 8097 and 8098 kill nothing at all.

---

## Pick the target, then read its flow

Both flows are long because both are exact. Neither is summarised here; open the
one you need and follow it.

| Target | Flow |
|---|---|
| `--hosted` (default), the daemon `/rooms` GUI at `127.0.0.1:31337` | [`references/hosted.md`](references/hosted.md) |
| `--cloud`, the `/chat/` fork served locally | [`references/cloud.md`](references/cloud.md) |

### Running `scripts/hosted.sh`

The script takes its paths from the environment and does not care where it is
invoked from, so the hub path and the installed symlink behave identically.

```bash
# canonical, from the hub
~/github/deez-skills/skills/om-build/scripts/hosted.sh --gate

# equivalent, through the installed symlink
~/.claude/skills/om-build/scripts/hosted.sh --gate
```

| Flag | Does |
|---|---|
| *(none)* | Gate, then build and install if the gate says to |
| `--gate` | Gate only. Prints `BUILD` or `SKIP` and exits. **Read-only** |
| `--force` | Build even when the gate says `SKIP` |
| `--no-gui` | Daemon only; `/rooms` serves the placeholder |

**Start with `--gate`.** It reports provenance for both repos and runs seven
checks — live inode against disk, version pin, served stamp against the built
bundle, and whether GUI, rooms-client, or CLI source is newer than the artifact
it produced. A `SKIP` means the daemon is already serving what is on disk, and
building anyway just burns time.

Override the paths when the layout differs:

```bash
OM_MONO=~/somewhere/openmarket-internal \
OM_GUI=~/somewhere/openmarket-chat \
  ~/github/deez-skills/skills/om-build/scripts/hosted.sh --gate
```

Staged assets overwrite committed stubs during a build, and the script restores
them on **every** exit path including failure and Ctrl-C. Do not interrupt it
and then hand-revert; let its own cleanup run.

## The rules that outlive either flow

These hold whichever target you picked, and every one of them has been paid for.

- **Ports are assigned, never chosen.** See
  **principle-bind-assigned-ports** for the authoritative table.
- **Bind `127.0.0.1` explicitly.** A `[::1]`-only bind is up, listening, and
  answers on the mini while the MacBook gets connection refused.
- **Confirm the binding before handing over a URL.** `lsof -nP -iTCP:<port>
  -sTCP:LISTEN` is what separates "serving" from "reachable".
- **Preflight the port.** A listener left from an earlier session either trips
  `--strictPort` or keeps answering, and then the operator reviews the previous
  build believing it is this one.
- **Kill only what this run started**, and prove it died. `pkill` returns before
  the process does, and a survivor holding the port makes the next run verify
  against the old binary.
- **Never hand over an `18097`–`18197` URL.** Those are not tunnelled.
- **`8098` is hands off.** Never start, restart, stop, or replace the review
  renderer. It is not an om-build rig.
