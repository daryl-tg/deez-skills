# Hosted chart MCP: tenant state, health and readiness

*Verified: 2026-10-23 and 2026-10-26, trees `2f7ecfde4`, `036c19a7c`, `3baee3c29` and `200dd61dc` (the hosted-mongo-state program, PRs #2131 and #2160) — the binary driven on an agent port against a local `mongo:7` with the production role shape: boot lines, `/healthz` and `/readyz` with the store up, stopped and back, the boot import summary, an index rebuild after a key change, a refused boot without the Mongo URI. The tool-call path (`chart_*` over the production gateway) remains unverified on this machine: it needs an operator API key.*

The hosted chart MCP (`packages/cli/src/hosted/`, built by `bun run build:chart-mcp` into `dist/om-chart-mcp`, served at mcp.openmarket.xyz) runs the daemon's chart tools per API key. Since release N (2026-10-23) each key's state lives in the Mongo database `om_hosted` behind the `TenantState` seam; since release N+1 the service has no SQLite home path at all and `openDb` throws `tenant_binding_present` under a tenant binding.

## Sub-features

- `boot` connects to Mongo, creates or rebuilds its three indexes, logs `tenant store: mongo <db>, indexes ready`, and refuses to start (exit 2) without `OM_HOSTED_MONGO_URI` (N+1) or with a relative `OM_HOME`.
- `healthz` is liveness: always 200 while the process serves; its body names the store or says `unreachable` from a background ping every 10 s. It never waits on Mongo.
- `readyz` is readiness: races a ping against 2 s and answers 503 `{ok:false, tenant_store:"unreachable"}` while the store is down.
- `index-rebuild` (store) drops and recreates an owned index whose keys changed (Mongo code 86) and logs `tenant store: rebuilt index <name>`; a TTL option change (85) goes through `collMod`, then drop-and-rebuild where the role lacks `collMod`.
- `boot-import` (release N only) copied every SQLite home on the volume into Mongo before serving, one summary line `boot import: <n> imported, <k> skipped, <r> refused, <e> kept, <ms> ms`. Gone in N+1.

## How to get to it (user POV)

- An agent adds the server with its API key: `claude mcp add openmarket --transport http https://mcp.openmarket.xyz/ --header "Authorization: Bearer <key>"` and calls `chart_status`, `chart_create`, `chart_drawing_add` and the rest.
- Operators read `/healthz` and `/readyz` without a bearer, and the pod log for the boot lines.

## Driving it with control-om

The hosted binary is not the daemon, so `control-om` lanes do not apply; the same port discipline does. Allocate one port from `18097`–`18197`, bind `127.0.0.1`, never `31338`.

1. A Mongo to talk to. A local container with auth on and the production role shape:
   `docker run -d --name om-hosted-mongo -p 127.0.0.1:18117:27017 -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=rootpw mongo:7`, then as root `use om_hosted; db.createUser({user:"om_chart_mcp", pwd:"mcppw", roles:[{role:"readWrite", db:"om_hosted"}]})`. Grant the same role on `om_hosted_test` for the env-gated suite, which refuses any database not ending in `_test`.
2. Build and boot: `cd packages/cli && bun run build:chart-mcp`, then
   `OM_HOSTED_BIND=127.0.0.1 OM_HOSTED_PORT=18119 OM_HOME=$(mktemp -d) OM_HOSTED_MONGO_URI='mongodb://om_chart_mcp:mcppw@127.0.0.1:18117/om_hosted?readPreference=primaryPreferred&ssl=false' ./dist/om-chart-mcp`.
   Expect `tenant store: mongo om_hosted, indexes ready` then the listening line. (Release N additionally needed `OM_HOSTED_DATA_DIR` pointing at a directory holding the pool's `.tenant-homes` sentinel, and printed the `boot import` line.)
3. Health pair: `curl -s -w ' %{http_code} %{time_total}\n' http://127.0.0.1:18119/healthz` and the same for `/readyz`. Both 200 in under 50 ms with the body `{"ok":true,"tenants":0,"sockets":0,"tenant_store":"mongo om_hosted"}`.
4. Store down: `docker stop om-hosted-mongo`, then the pair again. `/healthz` stays 200 within 50 ms and its body flips to `"tenant_store":"unreachable"` within about 12 s; `/readyz` answers 503 in about 2 s. `docker start om-hosted-mongo`, and `/readyz` is 200 again within seconds.
5. Index rebuild: in `mongosh`, `db.marks.dropIndex("by_tenant_workspace"); db.marks.createIndex({"_id.credentialId":1,"_id.workspaceId":1},{name:"by_tenant_workspace"})`, restart the binary, expect `tenant store: rebuilt index by_tenant_workspace` before `indexes ready`.
6. Refusals: boot without `OM_HOSTED_MONGO_URI` exits 2 with a `HostedConfigError` naming it; `OM_HOME=relative/dir` likewise.
7. Env-gated suite: `cd packages/cli && OM_TEST_MONGO_URI='mongodb://om_chart_mcp:mcppw@127.0.0.1:18117/om_hosted_test?authSource=om_hosted&readPreference=primaryPreferred&ssl=false' bun test test/hosted-tenant-store-mongo.test.ts` (the `authSource` is needed because the user lives in `om_hosted`).
8. Evidence from the program's runs: `~/Documents/dev-notes/hosted-mcp-mongo-state/run-artifacts/` (`unit2-health-paths*.txt`, `unit3b-index-fix-smoke.txt`, `unit6-hosted-rig.txt`).

## Gotchas

- The tool-call path needs a real OpenMarket API key against the production collab gateway; the fake-gateway harness (`test/fakes/hosted-harness.ts`) covers it in tests, and release N's first hour in production was its live observation. No recipe here claims it on a local port.
- A failing Mongo ping took about 10 s per call before the background monitor existed; if `/healthz` ever blocks again, the chart's 5 s probe timeout would restart the pod in a loop. The 50 ms figure in step 3 is the thing to watch.
- `tenants._id` and `marks._id.homeId` are the 32-hex home id (`homeNameFor`), not the full credential hash.
- Never point the env-gated suite at `om_hosted`: it wipes the database it names, and refuses unless the name ends in `_test`.
