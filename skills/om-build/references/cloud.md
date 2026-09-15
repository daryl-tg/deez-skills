# Building and serving the `/chat/` host (`--cloud`)

Read `../SKILL.md` first for the target table, the tunnel rules, and the
port contract. This file is the flow.

## `--cloud` — the hosted `/chat/` product, served locally

`/chat/` is the hosted browser product at `https://openmarket.xyz/chat/`. Since
`f190644c` its **source lives in `~/github/openmarket-chat/apps/cloud`**, inside
the same Bun workspace as the `/rooms` GUI, over the shared
`packages/chat-ui`. This target builds it, validates it, and puts it in front of
Ryan on a local port. It never goes near the daemon.

**The GitLab `openmarket-chat-cloud` repo is no longer where the source is.**
It still owns the image build and the deployment (`Dockerfile`, `deploy/nginx`,
`charts/`), and migrating that release path is a separate change. Building the
frontend there builds a stale tree — do not.

Because `packages/chat-ui` is shared, a UI change you are here to look at is
**also** in `/rooms`. If the change was shared, run `--hosted` too and report
both; a `/chat/` screenshot proves nothing about `/rooms`
(**principle-prove-every-host**).

### Hard rules

- **Never deploy, push, or publish an image.** Deployment is GitOps and
  controller-owned: Reflectful + ArgoCD apply
  `charts/openmarket-chat-cloud` from the GitLab repo. No manual `kubectl`, no
  `helm install`, no image push without Ryan's explicit per-instance OK.
- **Never commit `dist/`.** Neither repo accepts generated output,
  dependencies, credentials, or local endpoint overrides.
- **bun, never pnpm.** The workspace root `bun.lock` covers both hosts.
  `apps/cloud` has no lockfile of its own and is never installed separately.
- **A `/chat/` bundle can never be embedded in the daemon.** It builds at base
  `/chat/` with code-split `assets/chat-<hash>.js`; `/rooms` accepts only
  `index.html` + `assets/rooms.js` + `assets/rooms.css`, for both the embed and
  the `OM_ROOMS_GUI_DIR` loader. If Ryan wants a GUI at `/rooms`, that is
  `--hosted` — a different build of the same shared components, not a flag.
- **Never add a serving API key to the gateway.** The gateway forwards the
  user's bearer token only; the market sidecar mints guest keys per user. A
  shared serving key must never exist.

### 0. Preflight

```bash
cd ~/github/openmarket-chat
git status --short
git rev-parse --abbrev-ref HEAD && git log -1 --oneline
```

`main` must stay releasable; feature work belongs on a branch. There is no
drift check to run here — `tools/sync-shared.ts` and `tools/parity-manifest.json`
were deleted with the fork. The equivalent fence is
`test/chat-ui-workspace.test.ts`, which the ordinary suite runs.

Name what you are about to build:

```bash
git diff --stat main...HEAD -- packages/chat-ui apps/cloud src
```

`packages/chat-ui` touched means both hosts moved.

### 1. Install and build

Install from the **workspace root**, once, for both hosts. Both registry
credentials are required, and Bun 1.3.14 lets a registry-wide npmrc credential
override the scoped ones — so isolate npm config during the install:

```bash
cd ~/github/openmarket-chat
(
  : "${NPM_READ_TOKEN:?Missing OpenMarket registry credential}"
  : "${ORANGECHARTS_NPM_READ_TOKEN:?Missing OrangeCharts registry credential}"
  registry_config_dir="$(mktemp -d)"
  trap 'rm -rf "$registry_config_dir"' EXIT
  XDG_CONFIG_HOME="$registry_config_dir" bun install --frozen-lockfile
)
```

If a credential is missing, stop and ask — never invent a token, never fall back
to another registry.

Then build and check the artifact:

```bash
bun run build:cloud                          # = bun run --cwd apps/cloud build
bun run --cwd apps/cloud check:dist          # node tools/check-dist.mjs
```

Expected: `check-dist OK: cloud artifact is fingerprinted, source-map free, and
daemon-agent free`. That check is the boundary guard — it fails if daemon-only
endpoints, local LLM endpoints, tokenless daemon probing, filesystem mirrors, or
`/rooms/` packaging leak into the cloud distribution.

Verify the artifact is fingerprinted and rooted at `/chat/`:

```bash
cd apps/cloud
grep -o 'assets/chat-[A-Za-z0-9_-]*\.js' dist/index.html | head -3
ls dist                   # index.html, assets/, icons/, manifest.webmanifest, sw.js
```

### 2. Serve it locally

Three rigs; pick by what Ryan needs to see. Their ports are **reserved** (see
*Remote viewing* in `../SKILL.md`) — 4178 for rig A, 8097 for rig B, 13137 for
rig C. Do not substitute a different port because one is busy; free the assigned
one, or report that the tunnel needs another `-L`. Every rig binds 127.0.0.1
explicitly so the forward can reach it.

**A. Static preview of the artifact you just built** — layout, shell, visual work:

```bash
cd ~/github/openmarket-chat/apps/cloud
bunx vite preview --port 4178 --strictPort --host 127.0.0.1
# MacBook: http://localhost:4178/chat/
```

4178, not 8098 — 8098 is the device-owned review renderer and this skill never
touches it. `--host 127.0.0.1` is **required here, not optional**. Left off,
`vite preview` binds `[::1]` only: `curl http://127.0.0.1:4178/` refuses while
`localhost` on the mini works — and the tunnel, which dials IPv4 loopback,
refuses too. The rig looks healthy from the mini and is dead from the MacBook.
Deep links resolve (`/chat/rooms` → 200, SPA fallback).

No gateway is present in this rig, so `/chat/api/*`, `/chat/ws/rooms`, and
`/api/v1/auth-v2` are unproxied — login and live data will fail. That is
expected, not a regression.

**B. Dev server with proxies** — iterating on source:

```bash
cd ~/github/openmarket-chat/apps/cloud
bun run dev -- --host 127.0.0.1    # vite on 8097, strictPort, base /chat/
# MacBook: http://localhost:8097/chat/
```

The script is pinned to `--port 8097 --strictPort` and passes no `--host`, so
append it. 8097 is the operator's own dev-server port: preflight it, and if
something is already listening, ask rather than killing it. It proxies
`/api/v1` → `localhost:3000` and `/chat/api/rooms` → `localhost:3002`; those
backends must be running or you get the same auth failures as rig A.

Note the collision: the root `bun run dev` (the `/rooms` vite server) is pinned
to 8097 too. Only one of them can hold the port. Say in the report which host is
on 8097, because the URL does not tell the operator apart at a glance — check
the base path (`/chat/` vs `/rooms/`).

**C. Gateway parity** — closest to production, when the nginx behavior itself is
what is in question. **This rig spans both repos**: the artifact is built in the
workspace, the `Dockerfile` and `deploy/nginx` templates live in the GitLab
cloud repo, and the image `COPY dist`s from that checkout.

```bash
# stage the freshly built artifact into the deployment repo's build context
rsync -a --delete ~/github/openmarket-chat/apps/cloud/dist/ \
                  ~/github/openmarket-chat-cloud/dist/

cd ~/github/openmarket-chat-cloud
docker build -t om-chat-cloud .
docker run --rm -p 127.0.0.1:13137:8080 \
  -e CHAT_SERVICE=<host:port> -e ROOMS_WS_SERVICE=<host:port> \
  -e THARAMINE_SERVICE=<host:port> -e AUTH_SERVICE=<host:port> \
  om-chat-cloud
# MacBook: http://localhost:13137/chat/
```

`dist/` is gitignored in that repo — staging it is a local build-context step,
never a commit. 13137 is the tunnel's slot for this rig; the `127.0.0.1:` prefix
on `-p` keeps the container off every other interface while staying reachable
through the forward.

Only those four names are substituted into the template
(`NGINX_ENVSUBST_FILTER` in the Dockerfile); anything else in the config stays
literal. Unknown gateway paths return 404 by design.

Kill whatever you started when you are done, and say in the report that it is
gone — a survivor holds a tunnel port, and the next run's rig either refuses to
start or silently serves the stale build to the MacBook.

### 3. Full gate before claiming the work is done

From the workspace root. One command covers the cloud host:

```bash
bun run verify:cloud
```

That is cloud typecheck, lint, build, `check:dist`, and `test:ci`, in order.

**If `packages/chat-ui` changed, the rooms gate is also required** — the same
edit is in the `/rooms` bundle:

```bash
bun run lint && bun run typecheck && bun run build
bun --tsconfig-override ./tsconfig.json tools/check-dist.ts
bun --tsconfig-override ./tsconfig.json tools/test-fast.ts
```

Never green a failure with a skip, a baseline entry, a retry, or a longer
timeout. A quarantined file prevents a passing verdict.

Add the chart validation only when anything under the GitLab repo's `charts/`
or `deploy/` changed:

```bash
cd ~/github/openmarket-chat-cloud
helm lint charts/openmarket-chat-cloud
helm template openmarket-chat-cloud charts/openmarket-chat-cloud \
  --namespace pub --values charts/openmarket-chat-cloud/values.production.yaml
```

### 4. Report

Branch and HEAD, whether the diff touched `packages/chat-ui` (and therefore
`/rooms` as well), the entry hash from `apps/cloud/dist/index.html`, which rigs
were started and on which ports, the MacBook URL for each
(`http://localhost:<port>/chat/`) and the confirmed 127.0.0.1 binding, whether
each still runs or was killed, `check:dist` and gate results, and anything left
for Ryan. Never report a deploy — this target does not do one.

### Traps (`--cloud`)

| Symptom | Cause | Fix |
|---|---|---|
| `curl 127.0.0.1:<port>` refuses but the log says it is serving, and the MacBook cannot open it either | `vite preview` binds `[::1]` only; the tunnel dials IPv4 loopback | restart it with `--host 127.0.0.1` — `localhost` on the mini masks this, the tunnel does not |
| Mini serves fine, MacBook gets connection refused | the port is not in the tunnel's `-L` set, or the tunnel dropped | use the assigned port from *Remote viewing*; otherwise report that a new `-L` line is needed |
| `--strictPort` refuses to start, or the MacBook shows a build you did not just make | a rig from an earlier session still holds the port | `lsof -nP -iTCP:<port> -sTCP:LISTEN`, kill it by PID, confirm the port is free before starting |
| 8097 serves `/rooms/` when you wanted `/chat/` | both hosts' dev scripts pin 8097 | only one can run; stop the other, and name the base path in the report |
| Login fails / no rooms load in preview | rig A has no gateway; API and WS paths are unproxied | rig B with backends up, or rig C |
| Reached for `pnpm install`, or for `openmarket-chat-cloud` to build the frontend | both are pre-`f190644c` habits | install once at the workspace root with bun; the cloud repo builds only the image |
| `bun install --frozen-lockfile` 401s on a scope | one of the two registry credentials is missing, or an npmrc entry overrode a scoped one | supply both tokens and isolate `XDG_CONFIG_HOME` as in step 1; never substitute a registry |
| Build output has no `rooms.js` | correct — this host emits `assets/chat-<hash>.js` at base `/chat/` | if `/rooms` is the goal, run `--hosted` |
| Looking for `sync-shared.ts` or a parity manifest | deleted with the fork | nothing to run; the hosts import one package, and `test/chat-ui-workspace.test.ts` is the fence |
| Cloud is green, and the shared change is called done | `verify:cloud` says nothing about `/rooms` | run the rooms gate too when `packages/chat-ui` changed — **principle-prove-every-host** |
