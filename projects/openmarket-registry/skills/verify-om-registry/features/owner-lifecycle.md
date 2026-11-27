# Owner account and package lifecycle

A publisher's bearer reads their own account and packages, accepts the marketplace terms, checks a
package before publishing it, and manages what they published: yank and unyank a version, change a
package's visibility, and delete a package for good. Every call is a `/v1` JSON route under
`authenticate`, so a seed token drives all of it.

Last verified 2026-11-28 on openmarket-registry `c263de6` (fresh detached worktree, Bun 1.3.14,
lanes 18150 and 18152, seed token `dev-token`). Scope: `/v1/me`, `/v1/me/packages`, terms
acceptance, the validate probe for an ontology-pack (refused) and a wrun-indicator (accepted), the
draft refusal, yank, unyank, visibility, delete and the deleted name's refusal. Limitations: listing
edits, plans, install receipts and grants were not driven; the visibility change was read back
through `/v1/me/packages`, not through the catalog.

## Sub-features

- `me`: `GET /v1/me` answers `{"account_id","terms":{"required_version","accepted_version","url"}}`.
- `me-packages`: `GET /v1/me/packages` answers `{"account_id","scopes":[{"scope","packages":[…]}],"drafts":[]}`
  with each package's kind, visibility, latest and versions.
- `terms-accept`: `POST /v1/me/terms` with `{"version":"<required_version>"}` answers 200
  `{"accepted_version","accepted_at"}`; another version answers 400 `terms_version_mismatch`.
- `publish-validate`: `POST /v1/publish/validate` takes the publish form and writes nothing. A
  watch-pack, wrun-indicator, managed-strategy or agent-plugin on a lane that enables it answers
  200 `{"ok":true,"validate_only":true,…,"writes":0}`; an ontology-pack answers 422
  `validate_unsupported_kind`.
- `drafts`: `PUT /v1/drafts/:scope/:name` answers 422 `unsupported_kind` ("drafts support kinds:
  kscript-indicator"). kScript is retired, so no draft can be written.
- `yank`: `POST /v1/packages/:scope/:name/:version/yank` with `{"advisory":"…"}` answers
  `{"yanked":true,"advisory","yanked_at","latest"}`; `…/unyank` answers `{"yanked":false}`.
- `visibility`: `PATCH /v1/packages/:scope/:name` with `{"visibility":"unlisted"|"public"|…}`
  answers `{"package","visibility"}`.
- `delete`: `DELETE /v1/packages/:scope/:name` answers `{"deleted":true,"name","versions"}`; the
  package then reads 410 `package_deleted`, and a new publish under the name answers 410 too.
- Listing edits, plans, install receipts and grants: live verification pending.

## How to get to it (user POV)

- A publisher's `om` client calls these routes with their key: account status, `om publish
  --dry-run`-style checks, yank, visibility and delete.
- There is no page for them on a bare lane; the signed-in account page needs a session.

## Driving it with control-om-registry

Preconditions:

- A seed-token lane with `@acme/btc-dip-alerts` 1.0.0 published
  ([Publish a package](./publish-a-package.md)). For the accepted validate, start the lane with
  `REGISTRY_WRUN_KINDS=on` and build the Indicator tarball shown there.
- `$CR doctor` passes. Below, `H='authorization: Bearer dev-token'`.

- **Account.** `$CR cli -- curl -fsS $O/v1/me -H "$H"` shows `"accepted_version":null`;
  `curl … $O/v1/me/packages -H "$H"` lists `@acme/btc-dip-alerts` with `"visibility":"public"`.
- **Terms.** Read the version from `GET /v1/terms`, then
  `curl -sS -X POST $O/v1/me/terms -H "$H" -H 'content-type: application/json' -d '{"version":"2026-09-10"}'`
  answers 200. `GET /v1/me` then shows `"accepted_version":"2026-09-10"`. Try `2000-01-01` first to
  see the 400.
- **Validate.** The publish `curl` aimed at `/v1/publish/validate`. Second view:
  `GET /v1/packages/<scope>/<name>` still answers 404.
- **Yank.** Publish 1.0.1, then
  `curl -sS -X POST $O/v1/packages/acme/btc-dip-alerts/1.0.0/yank -H "$H" -H 'content-type: application/json' -d '{"advisory":"probe"}'`.
  Second view: `GET /v1/packages/acme/btc-dip-alerts/1.0.0` carries `"yanked":true` and the
  advisory. Restore with `…/1.0.0/unyank`.
- **Visibility.** `curl -sS -X PATCH $O/v1/packages/acme/btc-dip-alerts -H "$H" -H 'content-type: application/json' -d '{"visibility":"unlisted"}'`.
  Second view: `GET /v1/me/packages` with the bearer lists the package with
  `"visibility":"unlisted"`; `…/summary` carries no visibility field. The package page still
  answers 200. Set it back to `public`.
- **Delete.** Publish a throwaway name and delete that, never the fixture the other guides use:
  `curl -sS -X DELETE $O/v1/packages/acme/throwaway -H "$H"`. Second view: `GET` answers 410
  `package_deleted`, and publishing the name again answers 410.

## Gotchas

- Without a bearer every route here answers 503 `verifier_not_configured` on a seed-token lane,
  not 401.
- A deleted name is a tombstone for the lane's life; the lane's memory is the only way to reset it.
- `/v1/publish/validate` reports `"backend":"mongo"` even on a memory lane; it names the publish
  path, not the store.
