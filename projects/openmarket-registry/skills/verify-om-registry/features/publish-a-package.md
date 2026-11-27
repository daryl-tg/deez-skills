# Publish a package

A publisher sends a package to the registry with `POST /v1/publish`: a manifest and a tarball whose
`om-package.json` matches it, under a bearer the registry's verifier accepts. The answer names the
package's page, and the version is then readable through the API and downloadable as a tarball.

Last verified 2026-11-28 on openmarket-registry `c263de6` (fresh detached worktree, Bun 1.3.14,
lanes 18150 and 18152, seed token `dev-token`). Scope: an ontology-pack publish with a seed token,
the refusals without a valid bearer, the package, summary, version, source and metadata reads, an
alias miss, the tarball download and the metrics count; a wrun-indicator publish on
`REGISTRY_WRUN_KINDS=on`; an agent-plugin publish. Limitations: paid packages and tarball custody
rules were not driven; the owner routes (validate, yank, visibility, delete) are in [Owner account
and package lifecycle](./owner-lifecycle.md).

## Sub-features

- `publish-ok`: a valid publish answers 200 with `{"name","version","listing_url"}`.
- `publish-refused`: no bearer, or a bearer the verifier does not know, answers 503
  `verifier_not_configured` when the only verifier is seed tokens.
- `listed-publish`: a wrun-indicator (with `REGISTRY_WRUN_KINDS=on`) publishes and lists; an
  agent-plugin publishes on any lane but stays internal-only while the community is off.
- `package-read`: `GET /v1/packages/:scope/:name` returns kind, latest, publisher, owner,
  `tarball_url`, `sha256` and the version list.
- `package-summary`: `GET …/summary` adds keywords, first and latest publish times, downloads,
  artwork and the version list, but not visibility (read that from `/v1/me/packages`);
  `POST /v1/packages/metadata` with `{"targets":[{"package","version"}]}` answers
  `{"results":[…],"errors":[]}` with the same summary.
- `version-read`: `GET …/:version` returns the manifest, tarball, sha and yank fields;
  `GET …/:version/source` answers 404 `source_not_available` for a version with no inline source.
- `alias-read`: `GET /v1/aliases/:alias` answers 404 for a name no migration minted.
- `tarball-download`: `GET /tarballs/:scope/:name/:version.tgz` returns the tarball as published.

## How to get to it (user POV)

- A publisher runs `om publish` (or any client) against the registry with their key.
- A reader runs `om install @scope/name` or downloads the tarball the package page names.

## Driving it with control-om-registry

Preconditions:

- The lane was started with a seed token:
  `OM_REGISTRY_STATIC_TOKENS='{"dev-token":{"account_id":"acct-dev","tier":"pro"}}' $CR up`.
  Leave `OM_REGISTRY_PLATFORM_API_URL` and `OM_REGISTRY_AUTH_BASE_URL` unset so the first publish
  may claim its scope.
- `$CR doctor` passes. Build fixtures in a scratch directory with `REGISTRY_REPO` set to the
  driven worktree, or `$CR cli` refuses to run there.

- **Build the package.** In a scratch directory write `om-package.json`:
  `{"spec_version":"1.1","name":"@acme/btc-dip-alerts","version":"1.0.0","kind":"ontology-pack","description":"Alert recipes for BTC dip hunting","keywords":["btc","alerts"]}`,
  then `tar -czf pkg.tgz om-package.json`.
- **Publish.** `$CR cli -- curl -sS -w '\nHTTP %{http_code}\n' -X POST http://127.0.0.1:<port>/v1/publish -H 'authorization: Bearer dev-token' -F "manifest=$(cat om-package.json)" -F "tarball=@pkg.tgz;type=application/gzip"`.
  Expect HTTP 200 and `"listing_url":"http://127.0.0.1:<port>/@acme/btc-dip-alerts"`.
- **Refusal.** The same call with no `authorization` header, or `Bearer nope`, answers 503 with
  `"code":"verifier_not_configured"`.
- **Read it back.** `$CR cli -- curl -fsS http://127.0.0.1:<port>/v1/packages/acme/btc-dip-alerts`
  shows `"kind":"ontology-pack"`, `"latest":"1.0.0"`, `"owner_account_id":"acct-dev"`. Then
  `…/summary`, `…/1.0.0`, `…/1.0.0/source` (404) and the metadata `POST`.
- **Download.** `curl -sS -o got.tgz http://127.0.0.1:<port>/tarballs/acme/btc-dip-alerts/1.0.0.tgz`
  answers 200, and `tar -tzf got.tgz` lists `om-package.json`.
- **Second view.** `curl -fsS http://127.0.0.1:<port+1>/metrics | grep '^om_registry_publishes_total'`
  shows `om_registry_publishes_total{app="openmarket-registry",kind="ontology-pack"} 1`.
- **A listed Indicator.** Restart the lane with `REGISTRY_WRUN_KINDS=on`. From the driven worktree
  run a scratch script that writes the manifest
  `{"spec_version":"1.3","name":"@acme/vol-bands","version":"1.0.0","kind":"wrun-indicator","description":"Volatility bands for BTC","keywords":["vol","btc"]}`
  and the bytes of `makeWrunPackageTarGz(manifest)` from `test/wrun-helpers.ts` (it holds
  `om-package.json`, `wrun/metadata.json`, `wrun/module.wasm`, `src/indicator.ts` and
  `README.md`). Publish it with the same `curl`; `GET /v1/search?q=vol` then names it.
- **An agent-plugin.** The bytes of `agentTarball(fixture)` with `agentManifest(fixture)` from
  `test/agent-fixtures.ts` (`om-package.json`, `plugin.json`, `README.md`,
  `agents/<name>/AGENT.md`) publish with 200 on any lane.

## Gotchas

- With only seed tokens configured, an unknown bearer is refused as 503 `verifier_not_configured`,
  not 401. Read the code, not the status.
- The manifest field and the tarball's `om-package.json` must match.
- The tarball builders in `test/` only write bytes. The row must still go through
  `POST /v1/publish`; never seed through the repo's internal setters or test registries.
- Every metrics series starts with an `app` label, so grep `om_registry_publishes_total{app=` or
  the line start, not `…{kind=`.
- Tarballs land in `./data/tarballs` relative to the lane's working directory and survive a restart;
  the metadata does not. Run the lane from a disposable worktree.
- A `guest` tier token is refused unless `OM_REGISTRY_ALLOW_GUEST_PUBLISH=1`; use `pro`.
- From source, not driven: with the marketplace terms gate enforced (`parseTermsGateEnv` in
  `src/main.ts`), a publish from an account that has not accepted the terms answers 403
  `terms_required`; accept them first through `POST /v1/me/terms`. A lane leaves the gate off.
- The tarball comes back byte for byte: `cmp got.tgz pkg.tgz` is silent.
