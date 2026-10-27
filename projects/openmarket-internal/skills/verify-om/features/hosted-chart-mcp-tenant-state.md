# Hosted chart MCP: tenant state, health and readiness

*Verified: 2026-10-28, tree `a8fa10974` (origin/main, v0.466.0). The binary was rebuilt from main (`bun run build:chart-mcp`; #2173 changed the `runner/v3` input) and run on 18119 against a run-owned `mongo:7` on 18117 with the production role shape. The boot lines matched (`symbol directory: no saved snapshot …`, `indexes ready`, `listening on …/api/mcp`). `/healthz` and `/readyz` returned 200 in under 5 ms. With the store stopped, `/healthz` stayed 200 and flipped to `unreachable` by about 6 s, while `/readyz` returned 503 in 2 s. On restart, `/readyz` returned 200 within 3 s. A key swap printed `rebuilt index by_tenant_workspace`, and a clean restart printed none. The four refusals exited 2 with no password echoed, and `--help` exited 0. **The env-gated suite passed 7/7**, after granting the role `readWrite` on `om_hosted_test` (step 7). Not driven: the tool-call path over the production gateway (needs an operator key). Previous stamp `8fe6a8432` is an ancestor (10 commits).*

The hosted chart MCP (`packages/cli/src/hosted/`, built by `bun run build:chart-mcp` into `dist/om-chart-mcp`, served at mcp.openmarket.xyz) runs the daemon's chart tools per API key. Each key's state lives in the Mongo database named by `OM_HOSTED_MONGO_URI` (`om_hosted`) behind the `TenantState` seam. Since #2160 (on main) the service has no SQLite home path or boot import, and `openDb` throws `tenant_binding_present` under a tenant binding. `OM_HOME` (default `/data`) now holds only the symbol-directory snapshot `.hosted-symbol-directory.json`.

## Sub-features

- `boot` connects to Mongo, creates or rebuilds its three indexes, and logs `tenant store: mongo <db>, indexes ready`. It then prints `om-chart-mcp listening on http://<bind>:<port>/api/mcp (gateway https://collab.openmarket.xyz)`. A fresh `OM_HOME` first logs `symbol directory: no saved snapshot at <OM_HOME>/.hosted-symbol-directory.json; the first lookup loads it`. It refuses to start (exit 2, `om-chart-mcp: <message>`) without `OM_HOSTED_MONGO_URI`, with a URI that names no database, with a relative `OM_HOME`, or with any of `OM_API_KEY`, `OM_DATA_API_KEY`, `OM_COLLAB_AUTH_TOKEN`, `OM_COLLAB_WORKSPACE_ID` or `OM_ACCOUNT` set.
- `help`: `--help`/`-h` prints the routes (`POST /`, `/mcp`, `/api/mcp`, `/chatgpt`), the public GET routes and the env list, then exits 0.
- `healthz` is liveness: always 200 while the process serves; its body names the store or says `unreachable` from a background ping every 10 s. It never waits on Mongo.
- `readyz` is readiness: races a ping against 2 s and answers 503 `{ok:false, tenant_store:"unreachable"}` while the store is down.
- `index-rebuild` (store) drops and recreates an owned index whose keys changed (Mongo code 86) and logs `tenant store: rebuilt index <name>`; a TTL option change (85) goes through `collMod`, then drop-and-rebuild where the role lacks `collMod`.

## How to get to it (user POV)

- An agent adds the server with its API key: `claude mcp add openmarket --transport http https://mcp.openmarket.xyz/ --header "Authorization: Bearer <key>"` and calls `chart_status`, `chart_create`, `chart_drawing_add` and the rest.
- Operators read `/healthz` and `/readyz` without a bearer, and the pod log for the boot lines.

## Driving it with control-om

The hosted binary is not the daemon, so `control-om` lanes do not apply; the same port discipline does. Allocate one port from `18097`–`18197`, bind `127.0.0.1`, never `31338`.

1. A Mongo to talk to. A local container with auth on and the production role shape:
   `docker run -d --name <run-owned-name> -p 127.0.0.1:18117:27017 -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=rootpw mongo:7`, then as root `use om_hosted; db.createUser({user:"om_chart_mcp", pwd:"mcppw", roles:[{role:"readWrite", db:"om_hosted"}]})`. Grant the same role on `om_hosted_test` for the env-gated suite, which refuses any database not ending in `_test`.
2. Build and boot: `cd packages/cli && bun run build:chart-mcp`, then
   `OM_HOSTED_BIND=127.0.0.1 OM_HOSTED_PORT=18119 OM_HOME=$(mktemp -d) OM_HOSTED_MONGO_URI='mongodb://om_chart_mcp:mcppw@127.0.0.1:18117/om_hosted?readPreference=primaryPreferred&ssl=false' ./dist/om-chart-mcp`.
   Expect `tenant store: mongo om_hosted, indexes ready`, then `om-chart-mcp listening on http://127.0.0.1:18119/api/mcp (gateway https://collab.openmarket.xyz)`. `OM_HOSTED_DATA_DIR`, its `.tenant-homes` sentinel, `OM_HOSTED_HOME_RETENTION_MS` and the `boot import` line are gone since #2160.
3. Health pair: `curl -s -w ' %{http_code} %{time_total}\n' http://127.0.0.1:18119/healthz` and the same for `/readyz`. Both 200 in under 50 ms with the body `{"ok":true,"tenants":0,"sockets":0,"tenant_store":"mongo om_hosted"}`.
4. Store down: `docker stop <run-owned-name>`, then the pair again. `/healthz` stays 200 within 50 ms and its body flips to `"tenant_store":"unreachable"` within about 12 s; `/readyz` answers 503 in about 2 s. `docker start <run-owned-name>`, and `/readyz` is 200 again within seconds.
5. Index rebuild: the owned key is `{"_id.homeId":1,"_id.workspaceId":1}` (`hosted/tenant-store-mongo.ts`), next to `_id_` and `ttl_touchedAt`. Swap it for a different key under the same name: in `mongosh`, `db.marks.dropIndex("by_tenant_workspace"); db.marks.createIndex({"_id.workspaceId":1,"_id.homeId":1},{name:"by_tenant_workspace"})`. Restart the binary and expect `tenant store: rebuilt index by_tenant_workspace` before `indexes ready`. A second clean restart prints no `rebuilt` line. The earlier `_id.credentialId` key is wrong: recreating it under the right name never reproduces the conflict.
6. Refusals, each exit 2 on one `om-chart-mcp:` line, driven 2026-10-27 and again 2026-10-28. A `symbol directory: no saved snapshot at <OM_HOME>/…` line precedes it, so match the `om-chart-mcp:` line rather than the whole output:
   - no URI: `OM_HOSTED_MONGO_URI is required: each key's state lives in Mongo; set it to a mongodb:// URL that names its database (mongodb://user:password@host:27017/om_hosted)`;
   - a URI with no database path: `OM_HOSTED_MONGO_URI must be a mongodb:// URL that names its database (...)` (the password is never echoed);
   - `OM_HOME=relative/dir`: `OM_HOME must be an absolute path, got 'relative/dir'`;
   - `OM_API_KEY=x`: `refusing to start with OM_API_KEY set: this process serves many accounts and must carry no credential or workspace pointer of its own`.
7. Env-gated suite: `cd packages/cli && OM_TEST_MONGO_URI='mongodb://om_chart_mcp:mcppw@127.0.0.1:18117/om_hosted_test?authSource=om_hosted&readPreference=primaryPreferred&ssl=false' bun test test/hosted-tenant-store-mongo.test.ts` (the `authSource` is needed because the user lives in `om_hosted`). **The step-1 role is not enough for it.** The suite writes `om_hosted_test`, so first run, as root, `db.getSiblingDB("om_hosted").grantRolesToUser("om_chart_mcp",[{role:"readWrite",db:"om_hosted_test"}])`. Without it the suite fails `Unauthorized` (`not authorized on om_hosted_test to execute command { delete: "tenants" … }`). Driven 2026-10-28: 7 pass with the grant, failing without it.
8. Evidence from the program's runs: `~/Documents/dev-notes/hosted-mcp-mongo-state/run-artifacts/` (`unit2-health-paths*.txt`, `unit3b-index-fix-smoke.txt`, `unit6-hosted-rig.txt`).

## Gotchas

- The tool-call path needs a real OpenMarket API key against the production collab gateway; the fake-gateway harness (`test/fakes/hosted-harness.ts`) covers it in tests, and release N's first hour in production was its live observation. No recipe here claims it on a local port.
- A failing Mongo ping took about 10 s per call before the background monitor existed; if `/healthz` ever blocks again, the chart's 5 s probe timeout would restart the pod in a loop. The 50 ms figure in step 3 is the thing to watch.
- `tenants._id` and `marks._id.homeId` are the 32-hex home id (`homeNameFor`), not the full credential hash.
- Give the Mongo container a run-owned name and a free agent port. Other rigs already hold Mongo containers on this machine (seen 2026-10-27: `cpp-rig-mongo` on 18106 and `om-registry-mongo-test` on 27018). Stop and remove only the container your run started.
- Never point the env-gated suite at `om_hosted`: it wipes the database it names, and refuses unless the name ends in `_test`.
