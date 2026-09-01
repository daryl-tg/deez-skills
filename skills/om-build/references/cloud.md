# Building and serving the cloud `/chat/` fork (`--cloud`)

Read `../SKILL.md` first for the target table, the tunnel rules, and the
port contract. This file is the flow.

## `--cloud` — hosted `/chat/` fork, served locally

`openmarket-chat-cloud` is the hosted browser product at
`https://openmarket.xyz/chat/`. This target builds it, validates it, and puts it
in front of Ryan on a local port. It is **not** an upgrade path for anything and
it never goes near the daemon.

### Hard rules

- **Never deploy, push, or publish an image.** Deployment is GitOps and
  controller-owned (`docs/CLOUD_HOSTING.md`): Reflectful + ArgoCD apply
  `charts/openmarket-chat-cloud`. No manual `kubectl`, no `helm install`, no
  image push without Ryan's explicit per-instance OK.
- **Never commit `dist/`.** The cloud repo's policy forbids committing generated
  output, dependencies, credentials, or local endpoint overrides.
- **A cloud bundle can never be embedded in the daemon.** It builds at base
  `/chat/` with code-split `assets/chat-<hash>.js`; `/rooms` accepts only
  `index.html` + `assets/rooms.js` + `assets/rooms.css`, for both the embed and
  the `OM_ROOMS_GUI_DIR` loader (`rooms-gui.ts:296-303`). If Ryan wants a GUI at
  `/rooms`, that is `--hosted`. Making the cloud fork embeddable is a build-mode
  change in the cloud repo, not a flag.
- **Never add a serving API key to the gateway.** The gateway forwards the
  user's bearer token only; the market sidecar mints guest keys per user. A
  shared serving key must never exist.

### 0. Preflight

```bash
cd ~/github/openmarket-chat-cloud
git status --short
git rev-parse --abbrev-ref HEAD && git log -1 --oneline
bun tools/sync-shared.ts --diff        # drift vs the openmarket-chat twin
```

`main` must stay deployable; feature work belongs on a branch.

### 1. Install and build

pnpm is the contract here, not bun — `package.json` pins
`packageManager: pnpm@10.22.0`, and `AGENTS.md` specifies a frozen install.
A `bun.lock` also exists; ignore it for installs.

```bash
pnpm install --frozen-lockfile
pnpm run build            # vite build + worker build + sw build
pnpm run check:dist       # node tools/check-dist.mjs
```

Expected: `check-dist OK: cloud artifact is fingerprinted, source-map free, and
daemon-agent free`. That check is the boundary guard — it fails if daemon-only
endpoints or `/rooms/` packaging leak into the cloud distribution.

Verify the artifact is fingerprinted and rooted at `/chat/`:

```bash
grep -o 'assets/chat-[A-Za-z0-9_-]*\.js' dist/index.html | head -3
ls dist                   # index.html, assets/, icons/, manifest.webmanifest, sw.js
```

### 2. Serve it locally

Three rigs; pick by what Ryan needs to see. Their ports are **reserved** (see
*Remote viewing* above) — 4178 for rig A, 8097 for rig B, 13137 for rig C. Do not substitute a different port because one is busy; free the assigned
one, or report that the tunnel needs another `-L`. Every rig binds 127.0.0.1
explicitly so the forward can reach it.

**A. Static preview of the artifact you just built** — layout, shell, visual work:

```bash
pnpm exec vite preview --port 4178 --strictPort --host 127.0.0.1
# MacBook: http://localhost:4178/chat/
```

4178, not 8098 — 8098 is the device-owned review renderer and this skill never
touches it. `--host 127.0.0.1` is **required here, not optional**. Left off,
`vite preview` binds `[::1]` only: `curl http://127.0.0.1:4178/` refuses while `localhost` on
the mini works — and the tunnel, which dials IPv4 loopback, refuses too. The rig
looks healthy from the mini and is dead from the MacBook. Deep links resolve
(`/chat/rooms` → 200, SPA fallback).

No gateway is present in this rig, so `/chat/api/*`, `/chat/ws/rooms`, and
`/api/v1/auth-v2` are unproxied — login and live data will fail. That is
expected, not a regression.

**B. Dev server with proxies** — iterating on source:

```bash
pnpm run dev -- --host 127.0.0.1    # vite on 8097, strictPort, base /chat/
# MacBook: http://localhost:8097/chat/
```

The script is pinned to `--port 8097 --strictPort` and passes no `--host`, so
append it. 8097 is the operator's own dev-server port: preflight it, and if
something is already listening, ask rather than killing it. It proxies `/api/v1` → `localhost:3000` and `/chat/api/rooms` →
`localhost:3002`; those backends must be running or you get the same auth
failures as rig A.

**C. Gateway parity** — closest to production, when the nginx behavior itself is
what is in question:

```bash
docker build -t om-chat-cloud .
docker run --rm -p 127.0.0.1:13137:8080 \
  -e CHAT_SERVICE=<host:port> -e ROOMS_WS_SERVICE=<host:port> \
  -e THARAMINE_SERVICE=<host:port> -e AUTH_SERVICE=<host:port> \
  om-chat-cloud
# MacBook: http://localhost:13137/chat/
```

13137 is the tunnel's slot for this rig; the `127.0.0.1:` prefix on `-p` keeps
the container off every other interface while staying reachable through the
forward.

Only those four names are substituted into the template
(`NGINX_ENVSUBST_FILTER` in the Dockerfile); anything else in the config stays
literal. Unknown gateway paths return 404 by design.

Kill whatever you started when you are done, and say in the report that it is
gone — a survivor holds a tunnel port, and the next run's rig either refuses to
start or silently serves the stale build to the MacBook.

### 3. Full gate before claiming the work is done

`AGENTS.md` names six, and all six are expected before "complete":

```bash
pnpm install --frozen-lockfile
pnpm run lint
pnpm run typecheck
pnpm run build
pnpm run check:dist
bun test
```

Add the chart validation when anything under `charts/` or `deploy/` changed:

```bash
helm lint charts/openmarket-chat-cloud
helm template openmarket-chat-cloud charts/openmarket-chat-cloud \
  --namespace pub --values charts/openmarket-chat-cloud/values.production.yaml
```

### 4. Report

Branch and HEAD, the entry hash from `dist/index.html`, which rigs were started
and on which ports, the MacBook URL for each (`http://localhost:<port>/chat/`)
and the confirmed 127.0.0.1 binding, whether each still runs or was killed,
`check:dist` and gate results, parity drift from step 0, and anything left for
Ryan. Never report a deploy — this target does not do one.

### Traps (`--cloud`)

| Symptom | Cause | Fix |
|---|---|---|
| `curl 127.0.0.1:<port>` refuses but the log says it is serving, and the MacBook cannot open it either | `vite preview` binds `[::1]` only; the tunnel dials IPv4 loopback | restart it with `--host 127.0.0.1` — `localhost` on the mini masks this, the tunnel does not |
| Mini serves fine, MacBook gets connection refused | the port is not in the tunnel's `-L` set, or the tunnel dropped | use the assigned port from *Remote viewing*; otherwise report that a new `-L` line is needed |
| `--strictPort` refuses to start, or the MacBook shows a build you did not just make | a rig from an earlier session still holds the port | `lsof -nP -iTCP:<port> -sTCP:LISTEN`, kill it by PID, confirm the port is free before starting |
| Login fails / no rooms load in preview | rig A has no gateway; API and WS paths are unproxied | rig B with backends up, or rig C |
| `pnpm install --frozen-lockfile` complains about the pnpm version | `packageManager` pins 10.22.0; PATH pnpm is 10.34.5 as of 2026-08-18 — now *newer* than the pin, not older | `corepack pnpm install --frozen-lockfile`, or proceed if it installs cleanly |
| Tempted to `bun install` because `bun.lock` is there | both lockfiles are committed; the build contract is pnpm | pnpm for install/lint/typecheck/build; bun only for `bun test` |
| Build output has no `rooms.js` | correct — this fork emits `assets/chat-<hash>.js` at base `/chat/` | if `/rooms` is the goal, run `--hosted` |
| Shared file changed but the twin did not move | `test/shared-parity.test.ts` only checks a fork against its own manifest | `bun tools/sync-shared.ts --diff`, then `--refresh` here and a plain sync in the twin |
