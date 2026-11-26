---
name: verify-om-registry
description: "Drive and verify the OpenMarket registry (openmarket-registry: om packages, the catalog site and the /v1 API) in a local Bun lane: publish a fixture through the real API, then drive the catalog, package, scope and report pages. Use after registry changes that affect browsing, package pages, publishing or reads."
---

# Verify OpenMarket Registry

Use this skill to drive the registry as a visitor and as a publisher, and verify its public HTTP behavior. The primary surface is the server rendered catalog and package pages; the `/v1` HTTP API is the machine client surface. This repo does not ship a first party `om` CLI.

## Launch

Everything goes through `control-om-registry`, the tracked wrapper beside this file at
`bin/control-om-registry` in the hub. It is operator tooling, not app source: the product repo never
carries it. It resolves the checkout it drives from `REGISTRY_REPO`, or from
`git rev-parse --show-toplevel` of the directory you call it from, so run it from inside the
openmarket-registry checkout or worktree you mean to drive.

```sh
CR=~/.claude/skills/verify-om-registry/bin/control-om-registry
cd ~/Gitlab/openmarket-registry        # or the worktree you drive
$CR up                                 # default port 18098, metrics 18099
REGISTRY_LANE_PORT=18120 $CR up        # another slot in 18097-18197; metrics on the next port
OM_REGISTRY_STATIC_TOKENS='{"dev-token":{"account_id":"acct-dev","tier":"pro"}}' $CR up   # a lane that accepts publishes
```

`up` runs `bun src/main.ts` with `PORT`, `METRICS_PORT`, `OM_REGISTRY_HOST=127.0.0.1` and
`OM_REGISTRY_PUBLIC_URL` set, stores the PID and log under `artifacts/` as
`.registry-<port>.pid` and `.registry-<port>.log`, and waits for `GET /v1/health`. It refuses an
occupied port or metrics port and a port outside the agent range. The registry uses memory metadata
and local tarball storage; do not set MongoDB, S3, SSO, commerce, or production credentials for this
lane. Do not use this lane as a review URL.

The repo pins Bun 1.4.3 (`packageManager`). Run `bun install --frozen-lockfile` in a fresh
worktree before `up`: a stale `node_modules` exits at boot with `Cannot find module
'@openmarket/contracts/...'`, and `up` then prints the lane log.

The readiness check is successful when `$CR doctor` prints a healthy `/v1/health`, confirms the
listening PID was launched from this checkout on the lane's port, and finds `agent-browser`.

Stop only the PID recorded by this lane:

```sh
$CR down
```

## Doctor

Run `$CR doctor` before browser work. It checks the service health route, the lane PID and its working directory, the port owner, and the browser harness. If it fails, do not drive the service. Read `artifacts/.registry-<port>.log` for startup errors.

## Drive

Read [the feature map](./features/README.md), then follow the matching recipe. All browser operations go through `$CR browser ...`, which delegates to `agent-browser`. Use accessible roles and names. Start from:

```sh
$CR browser open http://127.0.0.1:18098/
$CR browser snapshot -i
```

A new lane is empty. To drive package, scope and report pages, start the lane with the seed token
above and publish a fixture through the real `POST /v1/publish` route, as
[Publish a package](./features/publish-a-package.md) shows: a `tar -czf` of an `om-package.json` and
a `curl -F` with `Authorization: Bearer dev-token`. Never seed rows through internal setters or the
repo's test helpers. An ontology-pack is the simplest fixture, but it is not a listed kind, so it
never appears in the catalog, search or the scope's listing. Each lane owns its port; take another
slot with `REGISTRY_LANE_PORT`. Never drive a service you did not start or stop a process by name.

Traps that cost a run:

- Two searchboxes share the name "Search packages" (header first, page form second);
  `find role searchbox --name` fills the header one. Use the ref you mean.
- A package page's tab radios sit under the cover image, so clicks by ref or label are refused as
  covered. Click the label text: `$CR browser find text "1 Version" click --exact`.
- `find role link --name "Report"` without `--exact` matches the footer's "Report abuse".
- With only seed tokens configured, a missing or unknown bearer answers 503
  `verifier_not_configured`, not 401.
- The metrics port (lane port + 1) is the second view for writes: `om_registry_publishes_total`,
  and `om_registry_kscript_write_attempts_total{op="putReport"}` for a report.

For API reads, use the app surface through the wrapper so the command, output, and exit status are visible:

```sh
$CR cli -- curl -fsS 'http://127.0.0.1:18098/v1/search?q=example'
```

The wrapper has no app-specific CLI to run; `cli --` captures the supplied command's stdout, stderr, and exit code.

## Evidence

Store evidence below `artifacts/<run-id>/<revision>/`. For browser behavior, capture an accessibility snapshot and screenshot after the action and again after the resulting state appears. For example, redirect `browser snapshot -i` to `action.aria.txt` and save `browser screenshot action.png`; keep action and result in separate files. The snapshot and screenshot must show the registry identity. For an API read, save the exact command, response body, and exit code. For a mutation, make a user-facing write and confirm its persisted value through a second, read-only route; restore disposable fixture state afterward.

The empty in-memory lane is suitable for read-only catalog and search proof. Do not claim a skipped package or publishing path was verified. If using a dry run, inspect network requests and other side effects to establish what it actually skipped.

When the local review renderer is available, publish the finished pair with:

```sh
$CR evidence publish <run-id> <revision>
```

Add `evidence-manifest.json` to the artifact directory before publishing. It must include `runId`, `revision`, `goal`, `capturedAt`, `repository`, `branch`, `candidateCommit`, and `diffSha256`. `capture.screenshots` must be a non-empty filename-to-caption object, and every named PNG must exist in the directory. The wrapper validates the manifest, copies the artifact directory into the already-running renderer's root, and confirms the gallery renders image frames. It does not start the renderer or create or replace a revision `index.html`.

## Cleanup

Run `$CR down` after every attempt, including a failed launch or browser iteration. It terminates only the PID that `up` recorded; it does not search by process name. Evidence under `artifacts/` survives teardown. Browser sessions started by this run can be closed with `$CR browser close`.

## Helpers

`bin/control-om-registry` is the one helper, executable in the hub:

```sh
$CR up | down | doctor
$CR browser <agent-browser verb> [args...]
$CR cli -- <command...>
$CR evidence publish <run-id> <revision>
```

## Maintenance

Use `maintain-verification-skill` after user paths, startup requirements, stable handles, or evidence rules change.

## Keeping it current

After proving a map change, commit and push only the changed `features/*.md` straight to the hub's
`main`:

```sh
bin/deez sync-feature-maps openmarket-registry verify-om-registry <file.md>... [--repo <hub worktree>]
```

Pass `--repo` when you edited in an isolated hub worktree. This is the one standing push to `main`
and it covers map Markdown only. `SKILL.md`, the wrapper and the registry go through ordinary
review.
